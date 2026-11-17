"""C2 程式檢查（可阻擋）：結構錯誤回非零。語意審查由 Claude 透過 /prd-c 另做。"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from string import Template

from . import c_bpack
from .c_draft import TEMPLATES, load_version, version_sha
from .util import REPO, WorkshopError, check_schema, read_json, utc_now, write_json, write_text

PRD_SECTIONS = ["問題", "使用情境", "範圍", "假設", "需求", "驗收"]
SOW_SECTIONS = ["交付物", "責任", "前置條件", "排除項", "驗收程序", "依賴", "變更流程"]
SEMANTIC_NOTE = ("語意審查未執行：離線 CLI 沒有模型。請以 `/prd-c` 讓 Claude 檢查邏輯矛盾、策略對準、範圍膨脹、"
                 "模糊形容詞、數字／單位一致性、術語與錯字，評語寫入 `semantic-review.md`。本報告不代表全部通過。")


def check(project: Path) -> dict:
    pj = read_json(project / "project.json")
    ver = pj["current_version"]
    errors, warnings = [], []
    E = lambda loc, msg: errors.append({"location": loc, "message": msg})
    W = lambda loc, msg: warnings.append({"location": loc, "message": msg})

    for v, info in pj["versions"].items():
        try:
            if version_sha(load_version(project, v)) != info["sha256"]:
                E(f"versions/{v}", "版本內容與記錄的 sha256 不符：已確認的版本被改動")
        except (OSError, ValueError, KeyError) as e:
            E(f"versions/{v}", f"版本檔案缺失或無法解析：{e}")
    try:
        data = load_version(project, ver)
    except (OSError, ValueError, KeyError) as e:
        raise WorkshopError(f"無法讀取目前版本 {ver}：{e}")
    reqs, ats, evs = data["requirements"], data["acceptance"], data["evidence"]
    loc = lambda f, i: f"versions/{ver}/{f}:{i}"

    for name, key in (("requirements", "requirements"), ("acceptance", "acceptance"), ("c-evidence", "evidence")):
        for e in check_schema({"schema_version": "1.0", key: data[key]}, name):
            E(f"versions/{ver}/{key}.json", e)
    for label, items, k in (("需求 ID", reqs, "id"), ("驗收 ID", ats, "id"), ("證據 ID", evs, "evidence_id")):
        for dup, n in Counter(i.get(k) for i in items).items():
            if n > 1:
                E(f"versions/{ver}", f"{label}重複：{dup}（{n} 次）")

    ev = {e.get("evidence_id"): e for e in evs}
    at = {a.get("id"): a for a in ats}
    rq = {r.get("id"): r for r in reqs}
    for r in reqs:
        rid = r.get("id")
        for e in r.get("evidence_ids", []):
            if e not in ev:
                E(loc("requirements.json", rid), f"引用的證據不存在：{e}")
        for a in r.get("acceptance_ids", []):
            if a not in at:
                E(loc("requirements.json", rid), f"引用的驗收不存在：{a}")
            elif at[a].get("req_id") != rid:
                E(loc("requirements.json", rid), f"{a} 標示的需求是 {at[a].get('req_id')}，與 {rid} 不一致")
        if r.get("status") not in ("rejected", "deferred"):
            if not r.get("acceptance_ids"):
                E(loc("requirements.json", rid), "有效需求沒有任何驗收（AT）")
            if not [e for e in r.get("evidence_ids", []) if e in ev]:
                E(loc("requirements.json", rid), "有效需求沒有任何可追溯的證據來源")
        if r.get("status") == "approved":
            st = [ev[e]["decision_status"] for e in r.get("evidence_ids", []) if e in ev]
            if not st or all(s in ("unresolved", "rejected") for s in st):
                E(loc("requirements.json", rid), "已批准的需求只依賴 unresolved／rejected 證據")
        t = r.get("target")
        if t and t.get("value") is not None:
            indep = [e for e in r.get("evidence_ids", []) if e in ev and ev[e]["evidence_kind"] != "b_measurement"
                     and ev[e]["decision_status"] == "approved"]
            if not indep:
                E(loc("requirements.json", rid), "目標值缺少獨立的已批准決策證據；研究測量不能直接寫成產品門檻")
    for a in ats:
        if a.get("req_id") not in rq:
            E(loc("acceptance.json", a.get("id")), f"對應的需求不存在：{a.get('req_id')}")

    # B 證據包：檢核當下重新驗證，不信任起草時的結果
    bp = pj["b_package"]
    bres = c_bpack.verify(bp["path"]) if bp.get("path") else None
    b_ok = bool(bres and bres["ok"])
    b_now = "未提供" if bres is None else ("有效" if b_ok else "無效：" + "；".join(bres["reasons"][:3]))

    def b_claim(cid, value, unit, where):
        if not b_ok:
            E(where, f"B 證據包目前{b_now}，但文件仍宣稱 {cid} = {value} {unit}")
            return
        c = bres["claims"].get(cid)
        if c is None:
            E(where, f"{cid} 不在已驗證的 B 證據包中")
        elif value is None or abs(c["value"] - value) > 1e-9 or c["unit"] != unit:
            E(where, f"{cid} 的數值／單位與 B 證據包不符（文件 {value} {unit}，證據包 {c['value']} {c['unit']}）")

    for e in evs:
        if e.get("evidence_kind") == "b_measurement":
            b_claim(e["evidence_id"], e.get("value"), e.get("unit"), loc("evidence.json", e["evidence_id"]))
            if b_ok and e.get("b_trace", {}).get("run_id") != bres["run_id"]:
                E(loc("evidence.json", e["evidence_id"]), "run_id 與證據包不符")
    for r in reqs:
        for x in r.get("reference_values") or []:
            b_claim(x["evidence_id"], x.get("value"), x.get("unit"), loc("requirements.json", r.get("id")))
    if bres is not None and not b_ok and not any(e.get("evidence_kind") == "b_measurement" for e in evs):
        W("project.json:b_package", f"B 證據包{b_now}；相關數值已標「待驗證」")

    gl = read_json(REPO / "c_prd" / "glossary.json")
    units = [(loc("requirements.json", r.get("id")), r["target"].get("unit")) for r in reqs if r.get("target")]
    units += [(loc("requirements.json", r.get("id")), x.get("unit")) for r in reqs for x in r.get("reference_values") or []]
    units += [(loc("evidence.json", e.get("evidence_id")), e["unit"]) for e in evs if "unit" in e]
    for where, u in units:
        if u not in gl["units"]:
            E(where, f"單位「{u}」不在詞彙表 c_prd/glossary.json")
    texts = [(loc("requirements.json", r.get("id")), " ".join([r.get("statement", "")] + r.get("behavior", []) + r.get("exceptions", [])))
             for r in reqs]
    texts += [(loc("acceptance.json", a.get("id")), " ".join(str(a.get(k, "")) for k in ("given", "when", "then", "expected_result")))
              for a in ats]
    for where, text in texts:
        for al in gl["text_aliases"]:
            if re.search(al["pattern"], text):
                W(where, f"疑似易混用單位（/{al['pattern']}/）；建議用 {al['use']}")

    vdir = project / "versions" / ver
    for fname, secs in (("prd.md", PRD_SECTIONS), ("sow.md", SOW_SECTIONS)):
        f = vdir / fname
        text = f.read_text(encoding="utf-8") if f.is_file() else ""
        for s in secs:
            if not re.search(rf"^## \d+\. {re.escape(s)}\s*$", text, re.M):
                E(f"versions/{ver}/{fname}", f"缺少必填章節：{s}")

    pending = []
    for f in sorted((project / "changes").glob("CR-*.json")) if (project / "changes").is_dir() else []:
        cr = json.loads(f.read_text(encoding="utf-8"))
        pending.append({"cr_id": cr["cr_id"], "status": cr["status"], "base_version": cr["base_version"]})
    return {"schema_version": "1.0", "version": ver, "version_sha256": pj["versions"][ver]["sha256"],
            "reviewed_at": utc_now(), "structural_ok": not errors, "errors": errors, "warnings": warnings,
            "b_package_at_review": {"path": bp.get("path"), "status": b_now,
                                    "run_id": bres["run_id"] if bres else None},
            "change_requests": pending,
            "semantic_review": {"status": "not_run", "note": SEMANTIC_NOTE}}


def review(project: Path) -> int:
    if not (project / "project.json").is_file():
        raise WorkshopError(f"找不到 C 專案：{project}/project.json")
    res = check(project)
    fmt = lambda xs: "\n".join(f"- `{x['location']}`：{x['message']}" for x in xs) or "- （無）"
    md = Template((TEMPLATES / "review.md.tmpl").read_text(encoding="utf-8")).substitute(
        version=res["version"], structural="通過" if res["structural_ok"] else "未通過",
        n_errors=len(res["errors"]), n_warnings=len(res["warnings"]), b_status=res["b_package_at_review"]["status"],
        semantic="未執行", errors=fmt(res["errors"]), warnings=fmt(res["warnings"]), semantic_note=SEMANTIC_NOTE)
    if res["change_requests"]:
        md += "\n## 變更提案\n\n" + "\n".join(f"- {c['cr_id']}：{c['status']}（基準 {c['base_version']}）"
                                          for c in res["change_requests"]) + "\n"
    write_json(project / "review.json", res)
    write_text(project / "review.md", md)
    print(f"檢核 {res['version']}：{'通過' if res['structural_ok'] else '未通過'}（錯誤 {len(res['errors'])}、"
          f"警示 {len(res['warnings'])}）；語意審查未執行。報告：{project.as_posix()}/review.md")
    for x in res["errors"]:
        print(f"  [錯誤] {x['location']}：{x['message']}")
    return 0 if res["structural_ok"] else 1
