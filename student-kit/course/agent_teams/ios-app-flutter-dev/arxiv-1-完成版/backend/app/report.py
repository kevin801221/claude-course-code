"""報告產生編排:抓 arXiv → Gemini 摘要 → 組 Report → 存檔。"""

from __future__ import annotations

from . import arxiv, gemini, storage
from .models import Report


def generate_today() -> Report:
    """產生今天的報告並存檔,回傳 Report。"""
    return generate_for(storage.today_str())


def generate_for(date: str) -> Report:
    """產生指定日期的報告並存檔(date 僅作為標籤,實際抓的是當下最新論文)。"""
    papers = arxiv.fetch_papers()
    markdown, papers = gemini.summarize(date, papers)
    report = Report(
        date=date,
        title=f"arXiv 每日科技論文摘要 · {date}",
        markdownBody=markdown,
        papers=papers,
    )
    storage.save(report)
    return report
