"""產生 B 的固定合成資料（dev／eval 不同種子與參數）。

每個情境分三檔保存：
  <scenario>.raw.csv     timestamp_s,temp_c       候選唯一能看到的輸入（空值=缺測）
  <scenario>.truth.csv   timestamp_s,true_temp_c  合成真值（先於噪聲生成，不由候選輸出倒推）
  <scenario>.events.json 事件標註（是否有持續升溫事件、真值首達 45°C 時間、干擾、缺測位置）

參數在看任何候選結果前固定；若要調參只能動 dev。尖峰高度刻意避開
SMA(h/5) 與 EMA(αh) 剛好落在 45.0°C 的刀口。
用法：python fixtures/b/generate_data.py [--out fixtures/b]
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

DURATION_S = 180
THRESHOLD_C = 45.0
SCENARIOS = ["stable", "noise", "spike", "sustained_rise", "missing"]

SPLITS = {
    "dev": {"seed": 101, "spikes": [(25, 15.0), (70, 28.0), (130, 22.0)],
            "rise_start": 40, "slope": 0.12, "gaps": [55, 98, 99, 150]},
    "eval": {"seed": 202, "spikes": [(30, 12.0), (75, 20.0), (120, 32.0)],
             "rise_start": 30, "slope": 0.10, "gaps": [50, 51, 86, 87, 140]},
}


def _rise(t: int, p: dict) -> float:
    return min(52.0, 40.0 + max(0, t - p["rise_start"]) * p["slope"])


def build(split: str, scenario: str) -> tuple[list, list, dict]:
    p = SPLITS[split]
    rng = random.Random(p["seed"] * 100 + SCENARIOS.index(scenario))
    truth, raw = [], []
    ev = {"scenario": scenario, "split": split, "has_event": False, "event_start_s": None,
          "t_true_45_s": None, "interference": [], "missing_s": [], "params": {}}
    for t in range(DURATION_S):
        if scenario == "stable":
            tr, sigma = 38.0, 0.1
        elif scenario == "noise":
            tr, sigma = 42.0, 1.0
        elif scenario == "spike":
            tr, sigma = 40.0, 0.2
        else:
            tr, sigma = _rise(t, p), 0.3
        tr = round(tr, 2)
        x = tr + rng.gauss(0.0, sigma)
        if scenario == "spike":
            x += dict(p["spikes"]).get(t, 0.0)
        if scenario == "missing" and t in p["gaps"]:
            x = None
        truth.append(tr)
        raw.append(None if x is None else round(x, 2))

    if scenario == "spike":
        ev["interference"] = [{"t_s": t, "height_c": h, "label": "isolated_spike"} for t, h in p["spikes"]]
        ev["params"] = {"base_c": 40.0, "sigma_c": 0.2}
    elif scenario in ("stable", "noise"):
        ev["params"] = {"base_c": truth[0], "sigma_c": 0.1 if scenario == "stable" else 1.0}
    else:
        ev["has_event"] = True
        ev["event_start_s"] = p["rise_start"]
        ev["t_true_45_s"] = next(t for t, v in enumerate(truth) if v >= THRESHOLD_C)
        ev["params"] = {"base_c": 40.0, "slope_c_per_s": p["slope"], "plateau_c": 52.0, "sigma_c": 0.3}
        if scenario == "missing":
            ev["missing_s"] = list(p["gaps"])
    ev["params"]["seed"] = p["seed"] * 100 + SCENARIOS.index(scenario)
    return raw, truth, ev


def write(out: Path) -> None:
    for split in SPLITS:
        d = out / split
        d.mkdir(parents=True, exist_ok=True)
        for s in SCENARIOS:
            raw, truth, ev = build(split, s)
            with open(d / f"{s}.raw.csv", "w", encoding="utf-8", newline="\n") as f:
                f.write("timestamp_s,temp_c\n")
                f.writelines(f"{t},{'' if v is None else f'{v:.2f}'}\n" for t, v in enumerate(raw))
            with open(d / f"{s}.truth.csv", "w", encoding="utf-8", newline="\n") as f:
                f.write("timestamp_s,true_temp_c\n")
                f.writelines(f"{t},{v:.2f}\n" for t, v in enumerate(truth))
            with open(d / f"{s}.events.json", "w", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(ev, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent))
    write(Path(ap.parse_args().out))
