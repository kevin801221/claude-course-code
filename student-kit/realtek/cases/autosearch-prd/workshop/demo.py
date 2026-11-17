"""完整 Demo：B → C 獨立 → C 連結 B → 變更提案 → 檢核。不自動接受變更。"""
from __future__ import annotations

import shutil
from argparse import Namespace
from pathlib import Path

from . import b_run, c_change, c_draft, c_review
from .util import REPO, WorkshopError, prepare_out_dir


def demo(args) -> int:
    missing = [t for t in ("cmake", "ctest") if not shutil.which(t)]
    if missing:
        raise WorkshopError(f"Demo 需要 {', '.join(missing)}（CMake ≥ 3.20）與 C++17 編譯器；本工具不自動安裝軟體。", code=2)
    out = prepare_out_dir(Path(args.out))
    b_dir, cs, cl = out / "b", out / "c" / "standalone", out / "c" / "linked"
    fb = REPO / "fixtures" / "c" / "feedback.json"
    print("== 1/5 B 研究 ==")
    rc = b_run.run(Namespace(out=str(b_dir), online=False, arxiv_query=None, import_sources=None,
                             fixtures=str(REPO / "fixtures" / "b"), src=str(REPO / "b_research"),
                             build_dir=str(REPO / "build")))
    if rc:
        print(f"Demo 中止：B 失敗（exit {rc}），見 {b_dir.as_posix()}/run.log")
        return rc
    cfx = str(REPO / "fixtures" / "c")
    print("== 2/5 C 獨立草稿 ==")
    c_draft.draft(Namespace(out=str(cs), research=None, fixtures=cfx))
    print("== 3/5 C 連結 B 證據包 ==")
    c_draft.draft(Namespace(out=str(cl), research=str(b_dir / "evidence.json"), fixtures=cfx))
    print("== 4/5 變更提案（不套用）==")
    c_change.change(cl, fb)
    print("== 5/5 檢核 ==")
    rc = c_review.review(cs) | c_review.review(cl)
    print("\nDemo 完成（未自動接受任何變更）：")
    for label, p in (("B 報告", b_dir / "research-report.md"), ("A 摘要", b_dir / "handoff-a.md"),
                     ("PRD", cl / "versions/v1/prd.md"), ("SoW", cl / "versions/v1/sow.md"),
                     ("追溯表", cl / "versions/v1/traceability.md"), ("變更提案", cl / "changes/CR-001.md"),
                     ("檢核", cl / "review.md")):
        print(f"  {label}：{p.as_posix()}")
    print(f"\n僅由講師另行批准後執行：uv run python -m workshop c apply --project {cl.as_posix()} --cr CR-001 --decision accept")
    return rc
