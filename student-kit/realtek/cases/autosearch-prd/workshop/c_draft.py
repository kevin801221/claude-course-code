"""C1 起草：以 requirements.json／acceptance.json／evidence.json 為追溯來源，由模板渲染文件。"""
from __future__ import annotations

import copy
from pathlib import Path
from string import Template

from . import c_bpack
from .util import (REPO, canonical_json, prepare_out_dir, read_json, sha256_bytes,
                   utc_now, warn, write_json, write_text)

TEMPLATES = REPO / "c_prd" / "templates"
PENDING = "待驗證"


def version_sha(data: dict) -> str:
    return sha256_bytes(canonical_json({k: data[k] for k in ("evidence", "requirements", "acceptance")}))


def load_version(project: Path, version: str) -> dict:
    d = project / "versions" / version
    return {"evidence": read_json(d / "evidence.json")["evidence"],
            "requirements": read_json(d / "requirements.json")["requirements"],
            "acceptance": read_json(d / "acceptance.json")["acceptance"]}


def _bullets(items) -> str:
    return "\n".join(f"- {x}" for x in items) or "- （無）"


def _b_status(bp: dict) -> str:
    if bp["status"] == "valid":
        return f"有效（run_id `{bp['run_id']}`）"
    if bp["status"] == "not_provided":
        return "未提供（B 相關數值標「待驗證」）"
    return f"無效：{'；'.join(bp['reasons'][:3])}（B 相關數值已撤除，標「待驗證」）"


def _req_block(r: dict, ev: dict) -> str:
    L = [f"### {r['id']} {r['title']}（狀態：{r['status']}）", "", r["statement"], "",
         "- 行為：" + "；".join(r["behavior"]), "- 例外：" + "；".join(r["exceptions"]),
         "- 來源：" + "、".join(f"{e}（{ev[e]['evidence_kind']}／{ev[e]['decision_status']}）" if e in ev else f"{e}（找不到）"
                              for e in r["evidence_ids"]),
         "- 驗收：" + "、".join(r["acceptance_ids"])]
    t = r.get("target")
    if t:
        val = f"{PENDING}（單位 {t['unit']}）" if t["value"] is None else f"{t['value']} {t['unit']}（{t['status']}）"
        L.append(f"- 目標：{t['name']} = {val}")
    refs = r.get("reference_values") or []
    if refs:
        L += ["- 研究參考值（B 合成資料測量，**非產品門檻**）：", "",
              "  | evidence_id | 候選 | 情境 | 值 | 單位 | run_id | 口徑 |", "  |---|---|---|---|---|---|---|"]
        L += [f"  | {x['evidence_id']} | {x.get('candidate', '')} | {x['scenario']} | {x['value']:g} | {x['unit']} | "
              f"`{x['run_id']}` | {x['basis']} |" for x in refs]
        L += ["", f"  限制：{refs[0].get('limitations', '')}"]
    elif "b_reference" in r:
        L.append(f"- 研究參考值：{PENDING}（沒有有效的 B 證據包）")
    return "\n".join(L)


def _open_questions(brief: dict, data: dict, bp: dict) -> list[dict]:
    oq = list(brief.get("open_questions", []))
    for r in data["requirements"]:
        t = r.get("target")
        if t and t["value"] is None:
            oq.append({"id": f"OQ-{r['id']}", "question": f"{r['id']} 的「{t['name']}」尚未決策（{t['status']}）。",
                       "evidence_ids": r["evidence_ids"], "owner": "產品負責人（待指派）"})
    if bp["status"] != "valid":
        oq.append({"id": "OQ-B", "question": f"B 證據包{_b_status(bp)}；需要時請重跑 B 再連結。",
                   "evidence_ids": [], "owner": "B 研究者"})
    for e in data["evidence"]:
        for other in e.get("conflicts_with", []):
            covered = any({e["evidence_id"], other} <= set(q["evidence_ids"]) for q in oq)
            if e["evidence_id"] < other and not covered:
                oq.append({"id": f"OQ-{e['evidence_id']}-{other}", "question": f"{e['evidence_id']} 與 {other} 主張衝突，待決策。",
                           "evidence_ids": [e["evidence_id"], other], "owner": "產品負責人（待指派）"})
    return oq


def render(project: Path, version: str, data: dict, brief: dict, pj: dict) -> None:
    d = project / "versions" / version
    ev = {e["evidence_id"]: e for e in data["evidence"]}
    vinfo = pj["versions"][version]
    common = {"title": brief["title"], "version": version, "version_label": vinfo["label"],
              "disclaimer": brief["disclaimer"], "b_status": _b_status(pj["b_package"])}
    at_rows = ["| AT | REQ | Given | When | Then | 可驗收結果 | 狀態 |", "|---|---|---|---|---|---|---|"]
    at_rows += [f"| {a['id']} | {a['req_id']} | {a['given']} | {a['when']} | {a['then']} | {a['expected_result']} | 未執行（未來產品驗收） |"
                for a in data["acceptance"]]
    prd = Template((TEMPLATES / "prd.md.tmpl").read_text(encoding="utf-8")).substitute(
        common, problem=brief["problem"], scenarios=_bullets(brief["scenarios"]), scope_in=_bullets(brief["scope_in"]),
        scope_out=_bullets(brief["scope_out"]), assumptions=_bullets(brief["assumptions"]),
        requirements="\n\n".join(_req_block(r, ev) for r in data["requirements"]), acceptance="\n".join(at_rows))
    sow = Template((TEMPLATES / "sow.md.tmpl").read_text(encoding="utf-8")).substitute(
        common, **{k: _bullets(v) for k, v in brief["sow"].items()})

    T = [f"# 追溯表（{version}）", "", "REQ → 證據 → AT → 可驗收結果。AT 是未來產品驗收規格，狀態皆為「未執行」。", "",
         "| REQ | 狀態 | 證據（類型／決策） | AT | 可驗收結果 |", "|---|---|---|---|---|"]
    ats = {a["id"]: a for a in data["acceptance"]}
    for r in data["requirements"]:
        evs = "<br>".join(f"{e}（{ev[e]['evidence_kind']}／{ev[e]['decision_status']}）" if e in ev else f"{e}（找不到）"
                          for e in r["evidence_ids"])
        for a in r["acceptance_ids"] or ["（缺驗收）"]:
            T.append(f"| {r['id']} | {r['status']} | {evs} | {a} | {ats[a]['expected_result'] if a in ats else '（找不到）'} |")
    bev = [e for e in data["evidence"] if e["evidence_kind"] == "b_measurement"]
    T += ["", "## B 研究數據追溯", ""]
    if bev:
        T += [f"證據包：`{pj['b_package']['path']}`", "",
              "| evidence_id | run_id | 產物 | sha256 | 列定位 | 行號 | 值 |", "|---|---|---|---|---|---|---|"]
        T += [f"| {e['evidence_id']} | `{e['b_trace']['run_id']}` | {e['b_trace']['artifact_path']} | `{e['b_trace']['artifact_sha256'][:16]}…` | "
              f"`{e['b_trace']['row_locator']}` | {e['b_trace']['metrics_line']} | {e['value']:g} {e['unit']} |" for e in bev]
        T += ["", f"限制：{bev[0]['b_trace']['limitations']}"]
    else:
        T.append(f"未連結有效的 B 證據包；相關數值{PENDING}。")

    O = [f"# 未決事項（{version}）", ""]
    O += [f"- **{q['id']}**：{q['question']}（證據：{'、'.join(q['evidence_ids']) or '—'}；負責：{q['owner']}）"
          for q in _open_questions(brief, data, pj["b_package"])]

    write_json(d / "evidence.json", {"schema_version": "1.0", "evidence": data["evidence"]})
    write_json(d / "requirements.json", {"schema_version": "1.0", "requirements": data["requirements"]})
    write_json(d / "acceptance.json", {"schema_version": "1.0", "acceptance": data["acceptance"]})
    write_text(d / "prd.md", prd)
    write_text(d / "sow.md", sow)
    write_text(d / "traceability.md", "\n".join(T) + "\n")
    write_text(d / "open-questions.md", "\n".join(O) + "\n")


def link_b(data: dict, bres: dict) -> None:
    """只把通過驗證的 B claim 帶進來，並標明 run_id、情境、口徑與合成資料限制。"""
    for r in data["requirements"]:
        ref = r.get("b_reference")
        if not ref:
            continue
        r["reference_values"] = []
        for cid, c in bres["claims"].items():
            if c["metric"] != ref["metric"] or c.get("split", "eval") != ref["split"]:
                continue
            data["evidence"].append({
                "evidence_id": cid, "evidence_kind": "b_measurement", "decision_status": "proposed",
                "title": c["statement"], "claim": c["statement"], "url_or_path": bres["path"],
                "value": c["value"], "unit": c["unit"],
                "b_trace": {"run_id": bres["run_id"], "artifact_path": c["artifact_path"],
                            "artifact_sha256": c["artifact_sha256"], "row_locator": c["row_locator"],
                            "metrics_line": c["metrics_line"], "scenario": c["scenario"],
                            "candidate": c.get("candidate"), "limitations": c["limitations"]}})
            r["evidence_ids"].append(cid)
            r["reference_values"].append({
                "evidence_id": cid, "value": c["value"], "unit": c["unit"], "run_id": bres["run_id"],
                "scenario": c["scenario"], "metric": c["metric"], "candidate": c.get("candidate"),
                "basis": "B eval 合成資料：首次告警 − 真值首達 45 °C（帶號）",
                "limitations": c["limitations"]})


def draft(args) -> int:
    fx = Path(args.fixtures)
    brief = read_json(fx / "product_brief.json")
    data = {"evidence": read_json(fx / "evidence.json")["evidence"],
            "requirements": read_json(fx / "requirements.seed.json")["requirements"],
            "acceptance": read_json(fx / "acceptance.seed.json")["acceptance"]}
    data = copy.deepcopy(data)
    bp = {"path": None, "status": "not_provided", "run_id": None, "reasons": []}
    if args.research:
        bres = c_bpack.verify(args.research)
        bp = {"path": str(Path(args.research).resolve()), "status": "valid" if bres["ok"] else "invalid",
              "run_id": bres["run_id"], "reasons": bres["reasons"]}
        if bres["ok"]:
            link_b(data, bres)
        else:
            warn(f"B 證據包無效，已撤除相關數值並標「{PENDING}」：" + "；".join(bres["reasons"][:3]))
    project = prepare_out_dir(Path(args.out))
    write_json(project / "brief.json", brief)
    pj = {"schema_version": "1.0", "title": brief["title"], "created_at": utc_now(), "mode": "offline",
          "current_version": "v1", "b_package": bp,
          "versions": {"v1": {"label": "教案基準版本（非正式核准）", "status": "baseline", "from_cr": None,
                              "created_at": utc_now(), "sha256": version_sha(data)}}}
    render(project, "v1", data, brief, pj)
    write_json(project / "project.json", pj)
    print(f"C 草稿完成：{project.as_posix()}/versions/v1/（prd.md、sow.md、traceability.md、open-questions.md）")
    return 0
