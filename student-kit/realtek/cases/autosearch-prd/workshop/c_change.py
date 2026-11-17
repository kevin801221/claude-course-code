"""C2 變更：回饋 → CR（不改任何版本）；只有操作者獨立輸入 --decision accept 才套用。"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from string import Template

from .c_draft import TEMPLATES, load_version, render, version_sha
from .util import WorkshopError, check_schema, read_json, utc_now, write_json, write_text


def _project(project: Path) -> dict:
    if not (project / "project.json").is_file():
        raise WorkshopError(f"找不到 C 專案：{project}/project.json")
    return read_json(project / "project.json")


def _render_cr(cr: dict) -> str:
    diff = "\n".join(f"- {d['req_id']}.{d['field']}：\n  - 前：{json.dumps(d['before'], ensure_ascii=False)}\n"
                     f"  - 後：{json.dumps(d['after'], ensure_ascii=False)}" for d in cr["diff"])
    adds = [f"- 新增 {r['id']} {r['title']}：{r['statement']}" for r in cr["proposal"]["add_requirements"]]
    return Template((TEMPLATES / "cr.md.tmpl").read_text(encoding="utf-8")).substitute(
        cr_id=cr["cr_id"], status=cr["status"], base_version=cr["base_version"], base_sha256=cr["base_sha256"],
        source=f"{cr['source']['feedback_id']} ← {cr['source']['evidence_id']}（{cr['source'].get('kind', '')}）",
        suggestion=cr["suggestion"], affected_requirements="、".join(cr["affected_requirements"]) or "（無）",
        interfaces="、".join(cr["interfaces"]), data_compatibility=cr["data_compatibility"],
        risk_performance=cr["risks"]["performance"], risk_schedule=cr["risks"]["schedule"],
        new_acceptance="\n".join(f"- {a['id']}（{a['req_id']}）：Given {a['given']}／When {a['when']}／Then {a['then']}"
                                 for a in cr["proposal"]["add_acceptance"]) or "- （無）",
        diff="\n".join(adds + ([diff] if diff else [])) or "- （無）", recommendation=cr["recommendation"])


def change(project: Path, feedback: Path) -> int:
    pj = _project(project)
    base = pj["current_version"]
    data = load_version(project, base)
    fb = read_json(feedback)
    for k in ("feedback_id", "source", "suggestion", "proposal"):
        if k not in fb:
            raise WorkshopError(f"回饋檔缺少欄位：{k}")
    p = fb["proposal"]
    reqs = {r["id"]: r for r in data["requirements"]}
    ats = {a["id"] for a in data["acceptance"]}
    evs = {e["evidence_id"] for e in data["evidence"]}
    if fb["source"].get("evidence_id") not in evs:
        raise WorkshopError(f"回饋來源證據不存在：{fb['source'].get('evidence_id')}")
    new_reqs = {r["id"] for r in p.get("add_requirements", [])}
    new_ats = {a["id"]: a for a in p.get("add_acceptance", [])}
    diff, problems = [], []
    for m in p.get("modify_requirements", []):
        if m["id"] not in reqs:
            problems.append(f"要修改的需求不存在：{m['id']}")
            continue
        diff += [{"req_id": m["id"], "field": f, "before": reqs[m["id"]].get(f), "after": v} for f, v in m["fields"].items()]
    for rid in new_reqs & set(reqs):
        problems.append(f"新增需求 ID 已存在：{rid}")
    for aid in set(new_ats) & ats:
        problems.append(f"新增驗收 ID 已存在：{aid}")
    for r in p.get("add_requirements", []):
        if not r.get("acceptance_ids"):
            problems.append(f"新增需求 {r['id']} 沒有驗收")
        for a in r.get("acceptance_ids", []):
            if a not in new_ats and a not in ats:
                problems.append(f"{r['id']} 引用的驗收不存在：{a}")
        for e in r.get("evidence_ids", []):
            if e not in evs:
                problems.append(f"{r['id']} 引用的證據不存在：{e}")
    for a in new_ats.values():
        if a["req_id"] not in reqs and a["req_id"] not in new_reqs:
            problems.append(f"{a['id']} 對應的需求不存在：{a['req_id']}")
    if problems:
        raise WorkshopError("變更提案不成立：" + "；".join(problems))

    affected = sorted({m["id"] for m in p.get("modify_requirements", [])} |
                      {r["id"] for r in data["requirements"] if set(r["interfaces"]) & set(p.get("interfaces", []))})
    cdir = project / "changes"
    cdir.mkdir(exist_ok=True)
    n = 1
    while (cdir / f"CR-{n:03d}.json").exists():
        n += 1
    cr = {"schema_version": "1.0", "cr_id": f"CR-{n:03d}", "status": "proposed", "created_at": utc_now(),
          "base_version": base, "base_sha256": pj["versions"][base]["sha256"],
          "source": {"feedback_id": fb["feedback_id"], **fb["source"]}, "suggestion": fb["suggestion"],
          "affected_requirements": affected, "interfaces": p.get("interfaces", []) + [f"{x}（新欄位）" for x in p.get("new_fields", [])],
          "data_compatibility": p.get("data_compatibility", ""), "risks": p.get("risks", {"performance": "未評估", "schedule": "未評估"}),
          "new_acceptance": sorted(new_ats), "diff": diff, "recommendation": p.get("recommendation", "待決策"),
          "proposal": {"modify_requirements": p.get("modify_requirements", []),
                       "add_requirements": p.get("add_requirements", []), "add_acceptance": p.get("add_acceptance", [])}}
    errs = check_schema(cr, "change-request")
    if errs:
        raise WorkshopError("CR 格式錯誤：" + "；".join(errs[:5]))
    write_json(cdir / f"{cr['cr_id']}.json", cr)
    write_text(cdir / f"{cr['cr_id']}.md", _render_cr(cr))
    print(f"已產生 {cr['cr_id']}（基準 {base}，狀態 proposed）：{cdir.as_posix()}/{cr['cr_id']}.md；未修改任何版本。")
    return 0


def _record(project: Path, entry: dict) -> None:
    with open(project / "decisions.jsonl", "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def apply(project: Path, cr_id: str, decision: str) -> int:
    pj = _project(project)
    f = project / "changes" / f"{cr_id}.json"
    if not f.is_file():
        raise WorkshopError(f"找不到變更提案：{cr_id}")
    cr = read_json(f)
    if cr["status"] not in ("proposed", "deferred"):
        raise WorkshopError(f"{cr_id} 已是 {cr['status']}，不可再決策")
    cur = pj["current_version"]
    entry = {"at": utc_now(), "cr_id": cr_id, "decision": decision, "operator": "manual-cli",
             "base_version": cr["base_version"], "current_version": cur}
    if decision in ("reject", "defer"):
        cr["status"] = "rejected" if decision == "reject" else "deferred"
        write_json(f, cr)
        write_text(project / "changes" / f"{cr_id}.md", _render_cr(cr))
        _record(project, {**entry, "result": f"CR 狀態改為 {cr['status']}；未套用任何變更"})
        print(f"{cr_id} → {cr['status']}；版本維持 {cur}。")
        return 0

    data = load_version(project, cur)
    cur_sha = version_sha(data)
    if cr["base_version"] != cur or cr["base_sha256"] != cur_sha or pj["versions"][cur]["sha256"] != cur_sha:
        _record(project, {**entry, "result": "拒絕套用：提案基準已過期或版本內容不符"})
        raise WorkshopError(f"過期提案，拒絕套用：{cr_id} 基準為 {cr['base_version']}（{cr['base_sha256'][:12]}…），"
                            f"目前為 {cur}（{cur_sha[:12]}…）。請以目前版本重新產生變更提案。")
    new = copy.deepcopy(data)
    reqs = {r["id"]: r for r in new["requirements"]}
    for m in cr["proposal"]["modify_requirements"]:
        reqs[m["id"]].update(copy.deepcopy(m["fields"]))
    for r in copy.deepcopy(cr["proposal"]["add_requirements"]):
        r["status"], r["approved_via"] = "approved", cr_id
        new["requirements"].append(r)
    new["acceptance"] += copy.deepcopy(cr["proposal"]["add_acceptance"])

    nv = f"v{int(cur[1:]) + 1}"
    if (project / "versions" / nv).exists():
        raise WorkshopError(f"版本目錄已存在：{nv}，拒絕覆蓋")
    pj["versions"][nv] = {"label": f"由 {cr_id} 經人工接受產生", "status": "accepted_change", "from_cr": cr_id,
                          "created_at": utc_now(), "sha256": version_sha(new)}
    pj["current_version"] = nv
    brief = read_json(project / "brief.json")
    render(project, nv, new, brief, pj)
    write_json(project / "project.json", pj)
    cr["status"] = "accepted"
    write_json(f, cr)
    write_text(project / "changes" / f"{cr_id}.md", _render_cr(cr))
    _record(project, {**entry, "result": f"已套用，新版本 {nv}；前版 {cur} 保留不變"})
    print(f"{cr_id} 已接受：新版本 {nv}（前版 {cur} 保留於 versions/{cur}/）。請再執行 c review 檢核新版本。")
    return 0
