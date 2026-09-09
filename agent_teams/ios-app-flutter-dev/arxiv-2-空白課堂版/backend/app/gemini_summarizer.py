"""Gemini 摘要模組。

把 5 篇 arXiv 論文整理成一份 markdown 研究報告。
- 有 GEMINI_API_KEY：呼叫 google-genai 的 gemini-3.5-flash
- 無 GEMINI_API_KEY：走本地 fallback，用論文 abstract 組成合理報告
"""

from __future__ import annotations

import os
import logging
from dataclasses import dataclass

from app.arxiv_fetcher import ArxivPaper

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


@dataclass
class SummarizedReport:
    summaries: dict[str, str]   # arxiv_id -> 單篇摘要（數句）
    overview: str                # 今日綜述（整段 markdown）
    used_fallback: bool = False  # 是否走了 fallback


def summarize_papers(papers: list[ArxivPaper]) -> SummarizedReport:
    """把論文清單整理成 SummarizedReport。

    有 API key 走 Gemini；無 key 走本地 fallback。
    """
    if GEMINI_API_KEY:
        try:
            return _gemini_summarize(papers)
        except Exception as exc:
            logger.warning("Gemini API 呼叫失敗，改走 fallback。錯誤：%s", exc)
            return _local_fallback(papers)
    else:
        logger.info("未設定 GEMINI_API_KEY，走本地 fallback")
        return _local_fallback(papers)


# ---------- Gemini 實作 ----------

def _build_prompt(papers: list[ArxivPaper]) -> str:
    lines = ["你是一名 AI 研究助理。以下是今天 arXiv 最新的 5 篇論文，請：",
             "1. 為每篇寫 2–3 句繁體中文摘要（精準、技術性）",
             "2. 在最後寫一段「今日綜述」（5–8 句，說明今天論文的共同趨勢或亮點）",
             "",
             "輸出格式（嚴格照這個結構，arxiv_id 用原始值，不要加引號或換格式）：",
             ""]
    for paper in papers:
        lines.append(f"## PAPER_ID: {paper.arxiv_id}")
        lines.append(f"TITLE: {paper.title}")
        lines.append(f"AUTHORS: {', '.join(paper.authors[:3])}")
        lines.append(f"ABSTRACT: {paper.abstract[:600]}")
        lines.append("")

    lines += [
        "請依下列格式輸出（JSON）：",
        "```json",
        "{",
        '  "summaries": {',
        '    "<arxiv_id>": "<2-3句摘要>"',
        "  },",
        '  "overview": "<今日綜述段落>"',
        "}",
        "```",
    ]
    return "\n".join(lines)


def _parse_gemini_json(text: str, papers: list[ArxivPaper]) -> SummarizedReport:
    """解析 Gemini 回傳的 JSON 格式輸出。"""
    import json, re
    # 取出 ```json ... ``` 或直接 { ... }
    m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    raw = m.group(1) if m else text.strip()
    data = json.loads(raw)
    summaries = data.get("summaries", {})
    overview = data.get("overview", "")
    # 補齊沒回傳的論文
    for paper in papers:
        if paper.arxiv_id not in summaries:
            summaries[paper.arxiv_id] = paper.abstract[:200]
    return SummarizedReport(summaries=summaries, overview=overview, used_fallback=False)


def _gemini_summarize(papers: list[ArxivPaper]) -> SummarizedReport:
    from google import genai  # type: ignore

    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = _build_prompt(papers)
    logger.info("呼叫 Gemini API，模型：%s", GEMINI_MODEL)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    text = response.text
    return _parse_gemini_json(text, papers)


# ---------- 本地 fallback ----------

def _local_fallback(papers: list[ArxivPaper]) -> SummarizedReport:
    """無 API key 時，用 abstract 組成合理報告（標示為 fallback）。"""
    summaries: dict[str, str] = {}
    for paper in papers:
        # 用 abstract 前 300 字做摘要
        abstract_short = paper.abstract[:300]
        if len(paper.abstract) > 300:
            abstract_short += "..."
        summaries[paper.arxiv_id] = abstract_short

    # 組今日綜述
    titles_str = "、".join(f"《{p.title[:40]}》" for p in papers[:3])
    overview = (
        f"本日共收錄 {len(papers)} 篇來自 cs.AI、cs.LG、cs.CL、cs.CV 領域的最新論文，"
        f"包含 {titles_str} 等研究。"
        "論文涵蓋大型語言模型、視覺理解、多模態學習等前沿主題，"
        "反映出當前 AI 研究社群對模型能力提升與效率優化的持續關注。"
        "建議讀者依興趣深入閱讀完整論文原文。"
    )

    return SummarizedReport(summaries=summaries, overview=overview, used_fallback=True)
