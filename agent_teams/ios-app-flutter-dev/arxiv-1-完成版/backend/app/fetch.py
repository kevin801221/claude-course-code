"""手動觸發抓取:`uv run python -m app.fetch`。

cron 範例見 backend/README.md。產出當天報告並印出摘要結果。
"""

from __future__ import annotations

from . import config, report


def main() -> None:
    print("[fetch] 開始抓取 arXiv 最新論文 ...")
    print(f"[fetch] 分類:{', '.join(config.ARXIV_CATEGORIES)}")
    print(f"[fetch] Gemini key:{'已設定(真呼叫)' if config.has_gemini_key() else '未設定(佔位摘要)'}")

    rpt = report.generate_today()

    print(f"[fetch] 完成:{rpt.date} 共 {len(rpt.papers)} 篇")
    for i, p in enumerate(rpt.papers, 1):
        print(f"  {i}. {p.title} ({p.arxivId})")
    print(f"[fetch] 已存檔至 {config.DATA_DIR}/report-{rpt.date}.json")


if __name__ == "__main__":
    main()
