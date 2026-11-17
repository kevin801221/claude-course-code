"""驗證 B 證據包（c draft 與 c review 共用；review 時一定重新驗證，不信任起草當下的結果）。"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .util import WorkshopError, check_schema, safe_child, sha256_file


def parse_locator(locator: str) -> dict:
    return dict(kv.split("=", 1) for kv in locator.split(";") if "=" in kv)


def locate_row(csv_path: Path, locator: str):
    """回傳 (檔案行號, 列內容)；找不到回 None。行號含表頭，第一筆資料是第 2 行。"""
    want = parse_locator(locator)
    with open(csv_path, encoding="utf-8", newline="") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            if all(row.get(k) == v for k, v in want.items()):
                return i, row
    return None


def verify(evidence_path) -> dict:
    res = {"ok": False, "reasons": [], "run_id": None, "claims": {}, "artifacts": {}, "path": str(evidence_path)}
    p = Path(evidence_path) if evidence_path else None
    if p is None or not p.is_file():
        res["reasons"].append(f"找不到證據包：{evidence_path}")
        return res
    if p.is_symlink():
        res["reasons"].append("evidence.json 是符號連結，拒絕使用")
        return res
    try:
        ev = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        res["reasons"].append(f"證據包無法解析：{e}")
        return res
    errs = check_schema(ev, "b-evidence")
    if errs:
        res["reasons"] += [f"格式錯誤：{e}" for e in errs[:5]]
        return res
    res["run_id"] = ev["run_id"]
    if ev["status"] != "succeeded":
        res["reasons"].append(f"B run 狀態為 {ev['status']}，不可引用其數值")
    root = p.parent
    for a in ev["artifacts"]:
        try:
            f = safe_child(root, a["path"])
        except WorkshopError as e:
            res["reasons"].append(str(e))
            continue
        if not f.is_file():
            res["reasons"].append(f"產物遺失：{a['path']}")
        elif sha256_file(f) != a["sha256"]:
            res["reasons"].append(f"產物雜湊不符（可能被竄改）：{a['path']}")
        else:
            res["artifacts"][a["path"]] = a["sha256"]
    for c in ev["claims"]:
        if c["artifact_path"] not in res["artifacts"]:
            res["reasons"].append(f"{c['evidence_id']} 引用的產物未通過驗證：{c['artifact_path']}")
            continue
        hit = locate_row(root / c["artifact_path"], c["row_locator"])
        if hit is None:
            res["reasons"].append(f"{c['evidence_id']} 在 {c['artifact_path']} 找不到列：{c['row_locator']}")
            continue
        line, row = hit
        if row.get("value", "") == "" or c["value"] is None or abs(float(row["value"]) - c["value"]) > 1e-9:
            res["reasons"].append(f"{c['evidence_id']} 數值與 {c['artifact_path']} 第 {line} 行不符")
            continue
        res["claims"][c["evidence_id"]] = {**c, "metrics_line": line,
                                           "artifact_sha256": res["artifacts"][c["artifact_path"]]}
    res["ok"] = not res["reasons"]
    return res
