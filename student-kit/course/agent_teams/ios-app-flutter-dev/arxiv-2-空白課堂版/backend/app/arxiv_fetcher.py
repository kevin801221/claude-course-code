"""arXiv 論文抓取模組。

使用官方 API (http://export.arxiv.org/api/query) 抓取最新 cs.AI/LG/CL/CV 論文。
依照 arXiv API 規範：多次呼叫間隔 ≥ 3 秒、加 User-Agent、HTTP 503 走 exponential backoff。
"""

from __future__ import annotations

import os
import time
import logging
from dataclasses import dataclass, field

import feedparser
import httpx

logger = logging.getLogger(__name__)

# ---------- 設定 ----------
ARXIV_API_URL = "https://export.arxiv.org/api/query"
USER_AGENT = "arxiv-reader-app/1.0"

DEFAULT_CATEGORIES = os.getenv(
    "ARXIV_CATEGORIES", "cs.AI,cs.LG,cs.CL,cs.CV"
).split(",")
DEFAULT_TOP_N = int(os.getenv("ARXIV_TOP_N", "5"))
REQUEST_INTERVAL = float(os.getenv("ARXIV_REQUEST_INTERVAL_SEC", "3"))

# exponential backoff 設定
MAX_RETRIES = 4
BACKOFF_BASE = 3.0  # 秒


@dataclass
class ArxivPaper:
    title: str
    authors: list[str]
    arxiv_id: str
    link: str
    abstract: str


def _build_search_query(categories: list[str]) -> str:
    # arXiv API 用空格作 OR 分隔，httpx 的 params 會把空格編成 +，符合 API 預期
    return " OR ".join(f"cat:{c.strip()}" for c in categories)


def fetch_latest_papers(
    top_n: int = DEFAULT_TOP_N,
    categories: list[str] | None = None,
) -> list[ArxivPaper]:
    """從 arXiv 抓最新 top_n 篇論文，回傳 ArxivPaper 清單。

    多次呼叫之間已加 REQUEST_INTERVAL 間隔；HTTP 503 走 exponential backoff。
    若抓取失敗（含網路錯誤），拋出 RuntimeError。
    """
    cats = categories or DEFAULT_CATEGORIES
    search_query = _build_search_query(cats)
    params = {
        "search_query": search_query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": str(top_n),
    }

    headers = {"User-Agent": USER_AGENT}

    for attempt in range(MAX_RETRIES):
        try:
            logger.info("arXiv API 請求 (attempt %d): %s", attempt + 1, params)
            response = httpx.get(
                ARXIV_API_URL,
                params=params,
                headers=headers,
                timeout=30.0,
                follow_redirects=True,
            )
            if response.status_code == 503:
                wait = BACKOFF_BASE * (2 ** attempt)
                logger.warning("arXiv 回 503，等待 %.1f 秒後重試...", wait)
                time.sleep(wait)
                continue
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"arXiv API HTTP 錯誤: {exc}") from exc
        except httpx.RequestError as exc:
            raise RuntimeError(f"arXiv API 網路錯誤: {exc}") from exc

        # 解析 Atom XML
        feed = feedparser.parse(response.text)
        papers: list[ArxivPaper] = []
        for entry in feed.entries:
            arxiv_id = entry.get("id", "").split("/abs/")[-1]
            title = entry.get("title", "").replace("\n", " ").strip()
            authors = [a.name for a in entry.get("authors", [])]
            abstract = entry.get("summary", "").replace("\n", " ").strip()
            # 取 HTML 頁面連結
            link = entry.get("link", f"https://arxiv.org/abs/{arxiv_id}")
            papers.append(ArxivPaper(
                title=title,
                authors=authors,
                arxiv_id=arxiv_id,
                link=link,
                abstract=abstract,
            ))
        logger.info("成功抓到 %d 篇論文", len(papers))

        # arXiv 禮貌間隔（若後續還有請求時）
        time.sleep(REQUEST_INTERVAL)
        return papers

    raise RuntimeError("arXiv API 請求失敗：超過最大重試次數")


# ---------- 內建 sample 資料（fallback 用） ----------
SAMPLE_PAPERS: list[ArxivPaper] = [
    ArxivPaper(
        title="Scaling Laws for Neural Language Models",
        authors=["Jared Kaplan", "Sam McCandlish", "Tom Henighan"],
        arxiv_id="2001.08361",
        link="https://arxiv.org/abs/2001.08361",
        abstract="We study empirical scaling laws for language model performance on the cross-entropy loss. "
                 "The loss scales as a power-law with model size, dataset size, and the amount of compute used for training.",
    ),
    ArxivPaper(
        title="Attention Is All You Need",
        authors=["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"],
        arxiv_id="1706.03762",
        link="https://arxiv.org/abs/1706.03762",
        abstract="We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, "
                 "dispensing with recurrence and convolutions entirely.",
    ),
    ArxivPaper(
        title="BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        authors=["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee"],
        arxiv_id="1810.04805",
        link="https://arxiv.org/abs/1810.04805",
        abstract="We introduce a new language representation model called BERT, which stands for Bidirectional Encoder "
                 "Representations from Transformers.",
    ),
    ArxivPaper(
        title="An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale",
        authors=["Alexey Dosovitskiy", "Lucas Beyer", "Alexander Kolesnikov"],
        arxiv_id="2010.11929",
        link="https://arxiv.org/abs/2010.11929",
        abstract="We show that a pure transformer applied directly to sequences of image patches can perform very well "
                 "on image classification tasks.",
    ),
    ArxivPaper(
        title="Language Models are Few-Shot Learners",
        authors=["Tom B. Brown", "Benjamin Mann", "Nick Ryder"],
        arxiv_id="2005.14165",
        link="https://arxiv.org/abs/2005.14165",
        abstract="We demonstrate that scaling up language models greatly improves task-agnostic, few-shot performance, "
                 "sometimes even becoming competitive with prior state-of-the-art fine-tuning approaches.",
    ),
]
