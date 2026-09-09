"""Gemini 摘要:把當天 5 篇論文整理成一份 markdown 報告。

設計重點(team lead 指示):
- 有 GEMINI_API_KEY → 真呼叫 Gemini(gemini-3.5-flash)。
- 沒 key → fallback 回一段清楚標示「[未設 GEMINI_API_KEY,以下為佔位摘要]」的佔位 markdown,
  用 arXiv 原始 abstract 拼成,讓 GET /reports/today 在沒 key 時也能回完整結構。
key 只從環境變數讀(config.GEMINI_API_KEY),絕不寫進程式碼。
"""

from __future__ import annotations

from . import config
from .models import Paper

_PLACEHOLDER_BANNER = "> [未設 GEMINI_API_KEY,以下為佔位摘要] 真實摘要需設定 key 後重新產生。"


def _format_paper_block(idx: int, paper: Paper, summary: str) -> str:
    authors = ", ".join(paper.authors) if paper.authors else "(作者未提供)"
    return (
        f"### {idx}. {paper.title}\n"
        f"- 作者:{authors}\n"
        f"- arXiv:[{paper.arxivId}]({paper.link})\n\n"
        f"{summary}\n"
    )


def _build_prompt(date: str, papers: list[Paper]) -> str:
    """組給 Gemini 的 prompt:要求輸出一份結構化 markdown 報告。"""
    lines = [
        f"你是一位科技論文編輯。以下是 {date} 從 arXiv 抓到的 {len(papers)} 篇最新論文,",
        "請用繁體中文整理成一份適合每日閱讀的 markdown 研究報告。要求:",
        "1. 開頭一段「## 今日綜述」,用 3-5 句點出今天這幾篇的共同主題或亮點。",
        "2. 接著每篇一個 `###` 小節:標題、作者、arXiv 連結,再用 2-4 句中文摘要這篇在做什麼、",
        "   重點貢獻。不要逐字翻譯 abstract,要消化成讀者看得懂的白話。",
        "3. 只輸出 markdown 內文,不要加程式碼框、不要客套話。",
        "",
        "論文清單(標題 / 作者 / arXiv id / 原始 abstract):",
    ]
    for i, p in enumerate(papers, 1):
        authors = ", ".join(p.authors) if p.authors else "(未提供)"
        lines.append(
            f"\n[{i}] 標題:{p.title}\n作者:{authors}\narXiv:{p.arxivId} ({p.link})\n"
            f"abstract:{p.summary}"
        )
    return "\n".join(lines)


def _fallback_markdown(date: str, papers: list[Paper]) -> tuple[str, list[Paper]]:
    """沒有 key 時,用原始 abstract 拼出佔位報告。papers 的 summary 沿用 abstract。"""
    blocks = [
        f"## 今日綜述",
        _PLACEHOLDER_BANNER,
        "",
        f"{date} 共抓取 {len(papers)} 篇 arXiv 最新論文(cs.AI / cs.LG / cs.CL)。"
        "以下為各篇原始 abstract,設定 GEMINI_API_KEY 後可改為 AI 整理的中文摘要。",
        "",
    ]
    for i, p in enumerate(papers, 1):
        blocks.append(_format_paper_block(i, p, p.summary))
    return "\n".join(blocks), papers


def summarize(date: str, papers: list[Paper]) -> tuple[str, list[Paper]]:
    """回傳 (markdownBody, papers)。

    - papers 的 summary 在有 key 時可被 Gemini 重寫(本 MVP 為求穩定,單篇 summary 維持 abstract,
      由 markdownBody 提供 AI 整理後的綜述與各篇白話摘要;沒 key 時兩者都用 abstract)。
    """
    if not papers:
        return "## 今日綜述\n\n今日無可用論文。", papers

    if not config.has_gemini_key():
        return _fallback_markdown(date, papers)

    try:
        from google import genai

        client = genai.Client(api_key=config.GEMINI_API_KEY)
        resp = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=_build_prompt(date, papers),
        )
        markdown = (resp.text or "").strip()
        if not markdown:
            # 真呼叫但拿到空回應 → 退回佔位,至少結構完整。
            return _fallback_markdown(date, papers)
        return markdown, papers
    except Exception as exc:  # noqa: BLE001 —— 任何 SDK / 網路錯誤都退回佔位,確保 API 不掛
        banner = (
            f"## 今日綜述\n\n> [Gemini 呼叫失敗,以下為佔位摘要] 原因:{exc}\n"
        )
        body, _ = _fallback_markdown(date, papers)
        return banner + "\n" + body, papers
