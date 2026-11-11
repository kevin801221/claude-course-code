"""arXiv 抓取與解析(依據 _Context/research-findings.md 第 1 節)。

流程:組 query → httpx GET(Atom XML)→ feedparser 解析 → 依 arxivId 去重 → 截最新 N 篇。
純解析 / 去重邏輯(parse_atom / dedup_and_truncate / extract_arxiv_id)不碰網路,方便單元測試。
"""

from __future__ import annotations

import re
import time

import feedparser
import httpx

from . import config
from .models import Paper

# arXiv abs URL 末端的 id,可能帶版本後綴 v1/v2;新式 2505.12345、舊式 cs.AI/0501001。
_ABS_ID_RE = re.compile(r"arxiv\.org/abs/(.+?)(?:v\d+)?$", re.IGNORECASE)


def extract_arxiv_id(entry_id: str) -> str:
    """從 entry id / abs URL 取出乾淨的 arxivId(去掉版本後綴)。

    >>> extract_arxiv_id("http://arxiv.org/abs/2505.12345v2")
    '2505.12345'
    """
    if not entry_id:
        return ""
    m = _ABS_ID_RE.search(entry_id.strip())
    if m:
        return m.group(1)
    # 不是標準 abs URL 就盡量去掉版本後綴後回傳原字串。
    return re.sub(r"v\d+$", "", entry_id.strip())


def _build_query() -> str:
    """組 search_query 值:cat:cs.AI OR cat:cs.LG OR cat:cs.CL。

    用空白連接(非字面 +),交給 httpx 正確百分比編碼;若寫死 '+OR+' 會被編成 %2BOR%2B,
    arXiv 會把 %2B 當字面加號而解析錯誤。
    """
    return " OR ".join(f"cat:{c}" for c in config.ARXIV_CATEGORIES)


def parse_atom(xml: str | bytes) -> list[Paper]:
    """把 arXiv 回傳的 Atom XML 解析成 Paper list(summary 先用原始 abstract)。"""
    feed = feedparser.parse(xml)
    papers: list[Paper] = []
    for entry in feed.entries:
        arxiv_id = extract_arxiv_id(entry.get("id", ""))
        authors = [a.get("name", "").strip() for a in entry.get("authors", [])]
        authors = [a for a in authors if a]
        # title / summary 內常有換行與多重空白,壓成單一空白比較好讀。
        title = re.sub(r"\s+", " ", entry.get("title", "").strip())
        abstract = re.sub(r"\s+", " ", entry.get("summary", "").strip())
        link = entry.get("link", "") or f"https://arxiv.org/abs/{arxiv_id}"
        papers.append(
            Paper(
                title=title,
                authors=authors,
                arxivId=arxiv_id,
                link=link,
                summary=abstract,
            )
        )
    return papers


def dedup_and_truncate(papers: list[Paper], top_n: int | None = None) -> list[Paper]:
    """依 arxivId 去重(保留先出現者)後截前 top_n 篇。

    一篇論文可掛多個分類 → 用 cat:A OR cat:B 抓會重複命中,需去重。
    """
    if top_n is None:
        top_n = config.ARXIV_TOP_N
    seen: set[str] = set()
    result: list[Paper] = []
    for p in papers:
        key = p.arxivId or p.link
        if key in seen:
            continue
        seen.add(key)
        result.append(p)
    return result[:top_n]


def fetch_papers(
    *,
    fetch_size: int | None = None,
    top_n: int | None = None,
    client: httpx.Client | None = None,
) -> list[Paper]:
    """抓 arXiv 最新論文,去重後回傳最新 top_n 篇。

    依 arXiv ToU:單一連線、連續請求自帶 3 秒間隔(本流程只打一次,間隔在多次呼叫時生效)。
    """
    fetch_size = fetch_size or config.ARXIV_FETCH_SIZE
    top_n = top_n or config.ARXIV_TOP_N

    params = {
        "search_query": _build_query(),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": str(fetch_size),
    }

    owns_client = client is None
    if owns_client:
        # 單一連線(arXiv ToU)。
        client = httpx.Client(
            timeout=config.ARXIV_TIMEOUT_SEC,
            limits=httpx.Limits(max_connections=1),
            headers={"User-Agent": "arxiv-daily-reader/0.1 (teaching demo)"},
            follow_redirects=True,  # arXiv 已將 http 端點 301 導向 https
        )
    try:
        # 禮貌間隔:若上次請求距今不足 3 秒就補睡(避免被限流 429)。
        _respect_rate_limit()
        resp = client.get(config.ARXIV_API_URL, params=params)
        resp.raise_for_status()
        papers = parse_atom(resp.content)
        return dedup_and_truncate(papers, top_n)
    finally:
        if owns_client:
            client.close()


_last_request_at: float = 0.0


def _respect_rate_limit() -> None:
    """確保兩次 arXiv 請求間至少間隔 ARXIV_REQUEST_INTERVAL_SEC 秒。"""
    global _last_request_at
    elapsed = time.monotonic() - _last_request_at
    wait = config.ARXIV_REQUEST_INTERVAL_SEC - elapsed
    if wait > 0:
        time.sleep(wait)
    _last_request_at = time.monotonic()
