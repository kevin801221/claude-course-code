"""B1 來源證據登錄：離線 fixture、選填 arXiv 官方 API、使用者匯入；去重與 skipped 紀錄。"""
from __future__ import annotations

import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from .util import WorkshopError, check_schema, read_json, utc_now

ARXIV_API = "https://export.arxiv.org/api/query"
_ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def _dedup_key(s: dict) -> str:
    if s.get("doi"):
        return "doi:" + s["doi"].strip().lower()
    if s.get("arxiv_id"):
        return "arxiv:" + re.sub(r"v\d+$", "", s["arxiv_id"].strip())
    return "url:" + s["url_or_path"].strip().rstrip("/")


def dedupe(sources: list[dict]) -> tuple[list[dict], list[dict]]:
    """DOI 優先、其次 arXiv ID（去版本號）、最後網址；保留第一筆。"""
    seen: dict[str, str] = {}
    kept, dups = [], []
    for s in sources:
        k = _dedup_key(s)
        if k in seen:
            dups.append({"source_id": s["source_id"], "duplicate_of": seen[k], "key": k})
        else:
            seen[k] = s["source_id"]
            kept.append(s)
    return kept, dups


def parse_arxiv_atom(xml_text: str, retrieved_at: str) -> list[dict]:
    # ponytail: 不加 defusedxml 依賴；arXiv Atom 不含 DTD，直接拒絕 DOCTYPE/ENTITY 擋 XXE 與 billion laughs
    if re.search(r"<!(DOCTYPE|ENTITY)", xml_text, re.I):
        raise WorkshopError("arXiv 回應含 DTD/ENTITY，拒絕解析")
    root = ET.fromstring(xml_text)
    out = []
    for e in root.findall("a:entry", _ATOM):
        url = (e.findtext("a:id", "", _ATOM) or "").strip()
        aid = url.rsplit("/abs/", 1)[-1] if "/abs/" in url else url
        summary = " ".join((e.findtext("a:summary", "", _ATOM) or "").split())
        doi = e.findtext("arxiv:doi", None, _ATOM)
        out.append({
            "source_id": f"arxiv:{aid}",
            "kind": "arxiv",
            "title": " ".join((e.findtext("a:title", "", _ATOM) or "").split()),
            "url_or_path": url,
            "access_level": "abstract_only",
            "retrieved_at": retrieved_at,
            "locator": "abstract",
            "claim": (summary[:300] + "…") if len(summary) > 300 else summary,
            "limitations": "僅 arXiv 摘要節錄（非全文、未同行審查確認）；摘要中的性能主張未經本教案驗證。",
            "doi": doi.strip() if doi else None,
            "arxiv_id": aid,
            "selection_basis": "context_only",
        })
    return out


def fetch_arxiv(query: str, max_results: int = 5, timeout: float = 15.0) -> str:
    q = urllib.parse.urlencode({"search_query": f"all:{query}", "start": 0, "max_results": max_results})
    req = urllib.request.Request(f"{ARXIV_API}?{q}", headers={"User-Agent": "workshop-bc/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # 只在操作者明確 --online 時呼叫
        return r.read().decode("utf-8")


def collect(fixtures_b: Path, online: bool, arxiv_queries: list[str], import_path: str | None, log) -> dict:
    data = read_json(fixtures_b / "sources.json")
    sources, skipped = list(data["sources"]), list(data["skipped"])
    if online:
        for q in arxiv_queries:
            try:
                sources += parse_arxiv_atom(fetch_arxiv(q), utc_now())
                log(f"arXiv 查詢完成：{q}")
            except Exception as e:  # 查不到就記錄 skipped，不假造結果
                skipped.append({"source_id": f"arxiv-query:{q}", "reason": f"arXiv 查詢失敗：{e}"})
                log(f"arXiv 查詢失敗（記為 skipped）：{q}：{e}")
    if import_path:
        imp = read_json(Path(import_path))
        for s in imp.get("sources", []):
            s.setdefault("access_level", "user_supplied")
            s.setdefault("selection_basis", "context_only")
        sources += imp.get("sources", [])
        skipped += imp.get("skipped", [])
    sources, dups = dedupe(sources)
    out = {"schema_version": "1.0", "mode": "online" if online else "offline",
           "sources": sources, "skipped": skipped, "duplicates_removed": dups}
    errs = check_schema(out, "sources")
    if errs:
        raise WorkshopError("來源登錄格式錯誤：" + "；".join(errs[:5]))
    return out
