"""手動觸發報告產生指令。

用法：
    uv run python -m app.generate          # 產出今日報告
    uv run python -m app.generate --force  # 強制重新產出（覆蓋既有）
    uv run python -m app.generate --date 2026-05-23  # 指定日期（不影響 arXiv 抓取，但存成指定日期）

cron 範例（每天 06:00 台灣時間）：
    0 22 * * * cd /path/to/backend && uv run python -m app.generate >> logs/generate.log 2>&1
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import date

from dotenv import load_dotenv

# 載入 backend/.env（若有的話）
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def build_report(report_date: date, papers_data, summarizer_result) -> dict:
    """把抓取結果 + 摘要結果組成契約要求的 Report dict。"""
    from app.arxiv_fetcher import ArxivPaper
    from app.gemini_summarizer import SummarizedReport

    papers_list = []
    for paper in papers_data:
        papers_list.append({
            "title": paper.title,
            "authors": paper.authors,
            "arxivId": paper.arxiv_id,
            "link": paper.link,
            "summary": summarizer_result.summaries.get(paper.arxiv_id, paper.abstract[:200]),
        })

    # 組 markdown body
    fallback_note = "\n\n> **(此為無 API key 時的本地摘要 fallback)**" if summarizer_result.used_fallback else ""
    markdown_parts = [
        f"# arXiv 每日科技論文摘要 · {report_date.isoformat()}",
        "",
        "## 今日綜述",
        summarizer_result.overview,
        "",
        "---",
        "",
        "## 論文列表",
    ]
    for paper in papers_data:
        summary = summarizer_result.summaries.get(paper.arxiv_id, paper.abstract[:200])
        authors_str = "、".join(paper.authors[:3])
        if len(paper.authors) > 3:
            authors_str += " 等"
        markdown_parts += [
            "",
            f"### [{paper.title}]({paper.link})",
            f"**作者**：{authors_str}　**arXiv**：[{paper.arxiv_id}]({paper.link})",
            "",
            summary,
        ]

    if summarizer_result.used_fallback:
        markdown_parts.append(fallback_note)

    markdown_body = "\n".join(markdown_parts)

    return {
        "date": report_date.isoformat(),
        "title": f"arXiv 每日科技論文摘要 · {report_date.isoformat()}",
        "markdownBody": markdown_body,
        "papers": papers_list,
    }


def generate(target_date: date | None = None, force: bool = False) -> dict:
    """執行完整的「抓取→摘要→儲存」流程，回傳 report dict。"""
    from app.arxiv_fetcher import fetch_latest_papers, SAMPLE_PAPERS
    from app.gemini_summarizer import summarize_papers
    from app import storage

    report_date = target_date or date.today()

    if not force and storage.load_report(report_date):
        logger.info("今日報告已存在 (%s)，略過（用 --force 強制重新產出）", report_date.isoformat())
        return storage.load_report(report_date)  # type: ignore

    # 1. 抓取 arXiv
    logger.info("開始抓取 arXiv 最新論文...")
    try:
        papers = fetch_latest_papers()
        logger.info("抓到 %d 篇論文", len(papers))
    except Exception as exc:
        logger.warning("arXiv 抓取失敗：%s，改用內建 sample 資料", exc)
        papers = SAMPLE_PAPERS

    # 2. Gemini 摘要（或 fallback）
    logger.info("開始整理摘要（Gemini 或 fallback）...")
    summarizer_result = summarize_papers(papers)
    if summarizer_result.used_fallback:
        logger.info("使用 fallback 摘要（未設定 GEMINI_API_KEY 或 API 失敗）")

    # 3. 組報告並儲存
    report = build_report(report_date, papers, summarizer_result)
    storage.save_report(report)
    logger.info("報告已產生：%s（%d 篇論文）", report_date.isoformat(), len(papers))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="手動產生今日 arXiv 論文報告")
    parser.add_argument(
        "--force", action="store_true", help="強制重新產出，覆蓋既有報告"
    )
    parser.add_argument(
        "--date", metavar="YYYY-MM-DD", help="指定報告日期（預設今天）"
    )
    args = parser.parse_args()

    target_date: date | None = None
    if args.date:
        try:
            target_date = date.fromisoformat(args.date)
        except ValueError:
            print(f"日期格式錯誤：{args.date}，請用 YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    report = generate(target_date=target_date, force=args.force)
    print(f"\n✅ 報告產生完成：{report['date']}（{len(report['papers'])} 篇論文）")
    if report.get("markdownBody", "").find("fallback") >= 0:
        print("⚠️  使用 fallback 摘要（無 GEMINI_API_KEY）")


if __name__ == "__main__":
    main()
