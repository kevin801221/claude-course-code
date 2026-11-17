"""計分程式：只讀逐筆輸出（rows）＋真值＋事件標註，三個候選共用。"""
from __future__ import annotations

import csv
import json
from pathlib import Path

# metric -> unit；順序即 metrics.csv 的列順序
METRICS = {
    "mae_c": "°C",
    "coverage": "ratio",
    "onset_count": "count",
    "false_alarms": "count",
    "missed": "flag",
    "detection_latency_s": "s",
    "early_alert": "flag",
}
HEADER = ["split", "candidate", "scenario", "metric", "value", "unit"]


def _f(s: str):
    return None if s == "" else float(s)


def read_rows(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return [{"t": int(r["timestamp_s"]), "temp": _f(r["temp_c"]), "y": _f(r["filtered_c"]),
                 "count": int(r["consecutive"]), "alarm": int(r["alarm"])} for r in csv.DictReader(f)]


def read_truth(path: Path) -> dict[int, float]:
    with open(path, encoding="utf-8", newline="") as f:
        return {int(r["timestamp_s"]): float(r["true_temp_c"]) for r in csv.DictReader(f)}


def read_events(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def onsets(rows: list[dict]) -> list[int]:
    """告警由 0→1 的時間點；不逐筆重複計數。"""
    out, prev = [], 0
    for r in rows:
        if r["alarm"] and not prev:
            out.append(r["t"])
        prev = r["alarm"]
    return out


def score(rows: list[dict], truth: dict[int, float], ev: dict) -> dict:
    pairs = [(r["y"], truth[r["t"]]) for r in rows if r["y"] is not None and r["t"] in truth]
    n_truth = sum(1 for r in rows if r["t"] in truth)
    ons = onsets(rows)
    m = {k: None for k in METRICS}
    m["mae_c"] = sum(abs(y - g) for y, g in pairs) / len(pairs) if pairs else None
    m["coverage"] = len(pairs) / n_truth if n_truth else None
    m["onset_count"] = len(ons)
    if not ev["has_event"]:
        m["false_alarms"] = len(ons)
    else:
        hit = [t for t in ons if t >= ev["event_start_s"]]
        m["missed"] = 0 if hit else 1
        if hit:
            m["detection_latency_s"] = hit[0] - ev["t_true_45_s"]
            m["early_alert"] = 1 if m["detection_latency_s"] < 0 else 0
    return m


def fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, int):
        return str(v)
    return f"{v:.6f}"


def to_rows(split: str, candidate: str, scenario: str, m: dict) -> list[list[str]]:
    return [[split, candidate, scenario, k, fmt(m[k]), METRICS[k]] for k in METRICS]


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(HEADER)
        w.writerows(rows)


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def select(metric_rows: list[dict], candidates: list[str], split: str = "eval",
           latency_tie_s: float = 1.0, mae_tie_c: float = 0.05) -> dict:
    """先以誤報／漏報篩選，再比延遲與 MAE；不硬挑冠軍。"""
    summary = {}
    for c in candidates:
        rs = [r for r in metric_rows if r["split"] == split and r["candidate"] == c]
        val = lambda metric: [float(r["value"]) for r in rs if r["metric"] == metric and r["value"] != ""]
        lat = [x for x in val("detection_latency_s") if x >= 0]  # 提早告警另列，不拿負延遲當「最快」
        mae = val("mae_c")
        summary[c] = {
            "false_alarms": int(sum(val("false_alarms"))),
            "missed": int(sum(val("missed"))),
            "early_alerts": int(sum(val("early_alert"))),
            "mean_latency_s": sum(lat) / len(lat) if lat else None,
            "mean_mae_c": sum(mae) / len(mae) if mae else None,
        }
        summary[c]["passed"] = summary[c]["false_alarms"] == 0 and summary[c]["missed"] == 0
    passed = [c for c in candidates if summary[c]["passed"]]
    if not passed:
        verdict = "無候選通過：每個候選在評估組都有誤報或漏報。"
    elif len(passed) == 1:
        verdict = f"僅 {passed[0]} 通過誤報／漏報篩選；仍需以實機資料複驗。"
    else:
        lats = [summary[c]["mean_latency_s"] for c in passed]
        maes = [summary[c]["mean_mae_c"] for c in passed]
        if None not in lats and max(lats) - min(lats) <= latency_tie_s and max(maes) - min(maes) <= mae_tie_c:
            verdict = f"{', '.join(passed)} 皆通過篩選，延遲與 MAE 差異不足以選出單一方案，列出取捨。"
        else:
            inf = float("inf")
            best = min(passed, key=lambda c: (inf if summary[c]["mean_latency_s"] is None else summary[c]["mean_latency_s"],
                                              summary[c]["mean_mae_c"]))
            verdict = (f"{', '.join(passed)} 皆通過篩選；在本合成評估組中 {best} 平均延遲最短，"
                       "但資料有限，僅列為觀察，建議以實機資料複驗後再決定。")
    early = [f"{c} 有 {summary[c]['early_alerts']} 次提早告警（未計入延遲比較）" for c in passed if summary[c]["early_alerts"]]
    if early:
        verdict += "另：" + "；".join(early) + "。"
    return {"split": split, "summary": summary, "passed": passed, "verdict": verdict}
