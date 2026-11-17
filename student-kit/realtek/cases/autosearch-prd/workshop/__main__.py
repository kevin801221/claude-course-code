"""統一 CLI：python -m workshop {b run | c draft|change|review|apply | demo}"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .util import REPO, WorkshopError


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="python -m workshop", description="瑞昱工作坊教案 B×C（合成案例，預設離線）")
    sub = ap.add_subparsers(dest="area", required=True)

    b = sub.add_parser("b", help="B 個人技術研發").add_subparsers(dest="cmd", required=True)
    br = b.add_parser("run", help="建置、實測三個候選並產生報告與證據包")
    mode = br.add_mutually_exclusive_group()
    mode.add_argument("--offline", action="store_true", help="預設：只用合成 fixture，不連網")
    mode.add_argument("--online", action="store_true", help="操作者明確選擇才會呼叫 arXiv 官方 API")
    br.add_argument("--arxiv-query", action="append", help="搭配 --online；可重複")
    br.add_argument("--import-sources", help="匯入使用者合法取得的來源 metadata（JSON）")
    br.add_argument("--out", help="輸出目錄（預設 outputs/b/<run_id>；已存在則拒絕）")
    br.add_argument("--fixtures", default=str(REPO / "fixtures" / "b"))
    br.add_argument("--src", default=str(REPO / "b_research"), help="C++ 原始碼目錄")
    br.add_argument("--build-dir", default=str(REPO / "build"))

    c = sub.add_parser("c", help="C PRD／SoW／變更／檢核").add_subparsers(dest="cmd", required=True)
    cd = c.add_parser("draft", help="起草 PRD／SoW／追溯表（基準版 v1）")
    cd.add_argument("--offline", action="store_true", help="預設且唯一模式：外部擷取不在 MVP")
    cd.add_argument("--research", help="選填：B 的 evidence.json")
    cd.add_argument("--out", required=True)
    cd.add_argument("--fixtures", default=str(REPO / "fixtures" / "c"))
    cc = c.add_parser("change", help="把回饋寫成變更提案（不改任何版本）")
    cc.add_argument("--project", required=True)
    cc.add_argument("--feedback", required=True)
    cv = c.add_parser("review", help="程式檢查目前版本，輸出 review.json/review.md")
    cv.add_argument("--project", required=True)
    ca = c.add_parser("apply", help="人工決策：accept 才套用（僅由講師另行批准後執行）")
    ca.add_argument("--project", required=True)
    ca.add_argument("--cr", required=True)
    ca.add_argument("--decision", required=True, choices=["accept", "reject", "defer"])

    d = sub.add_parser("demo", help="B → C 獨立 → C 連結 → 變更提案 → 檢核（不自動接受變更）")
    d.add_argument("--offline", action="store_true", help="預設且唯一模式")
    d.add_argument("--out", required=True)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.area == "b":
            from .b_run import run
            return run(args)
        if args.area == "demo":
            from .demo import demo
            return demo(args)
        from . import c_change, c_draft, c_review
        if args.cmd == "draft":
            return c_draft.draft(args)
        if args.cmd == "change":
            return c_change.change(Path(args.project), Path(args.feedback))
        if args.cmd == "review":
            return c_review.review(Path(args.project))
        return c_change.apply(Path(args.project), args.cr, args.decision)
    except WorkshopError as e:
        print(f"錯誤：{e}", file=sys.stderr)
        return e.code
    except (OSError, ValueError, KeyError) as e:  # 例如專案 JSON 損毀或缺欄位
        print(f"錯誤：讀取或解析失敗（{type(e).__name__}）：{e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
