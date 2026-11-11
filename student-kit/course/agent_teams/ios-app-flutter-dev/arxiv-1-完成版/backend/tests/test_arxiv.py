"""arXiv 解析 / 去重 / id 抽取單元測試(不碰網路)。

執行:cd backend && uv run pytest
"""

from __future__ import annotations

from app import arxiv
from app.models import Paper

# 一份精簡 Atom XML:含 4 個 entry,其中兩個是同一篇 (2505.00001) 的不同版本/分類,
# 用來驗證「依 arxivId 去重 → 截前 N 篇」。
SAMPLE_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2505.00001v1</id>
    <title>Paper One on
      Large Models</title>
    <summary>First   abstract with   extra spaces.</summary>
    <author><name>Alice Chen</name></author>
    <author><name>Bob Wang</name></author>
    <link href="https://arxiv.org/abs/2505.00001" rel="alternate"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2505.00002v1</id>
    <title>Paper Two</title>
    <summary>Second abstract.</summary>
    <author><name>Carol Liu</name></author>
    <link href="https://arxiv.org/abs/2505.00002" rel="alternate"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2505.00001v2</id>
    <title>Paper One on Large Models</title>
    <summary>First abstract (duplicate, different version).</summary>
    <author><name>Alice Chen</name></author>
    <link href="https://arxiv.org/abs/2505.00001" rel="alternate"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2505.00003v1</id>
    <title>Paper Three</title>
    <summary>Third abstract.</summary>
    <author><name>Dan Kim</name></author>
    <link href="https://arxiv.org/abs/2505.00003" rel="alternate"/>
  </entry>
</feed>
"""


def test_extract_arxiv_id_strips_version():
    assert arxiv.extract_arxiv_id("http://arxiv.org/abs/2505.12345v2") == "2505.12345"
    assert arxiv.extract_arxiv_id("http://arxiv.org/abs/2505.12345") == "2505.12345"
    assert arxiv.extract_arxiv_id("") == ""


def test_parse_atom_fields():
    papers = arxiv.parse_atom(SAMPLE_ATOM)
    assert len(papers) == 4
    p = papers[0]
    assert p.arxivId == "2505.00001"
    # 標題的內嵌換行 / 多重空白被壓成單一空白
    assert p.title == "Paper One on Large Models"
    assert p.summary == "First abstract with extra spaces."
    assert p.authors == ["Alice Chen", "Bob Wang"]
    assert p.link == "https://arxiv.org/abs/2505.00001"


def test_dedup_by_arxiv_id():
    papers = arxiv.parse_atom(SAMPLE_ATOM)
    deduped = arxiv.dedup_and_truncate(papers, top_n=10)
    ids = [p.arxivId for p in deduped]
    # 2505.00001 出現兩次 → 去重後只剩一個,且保留先出現者
    assert ids == ["2505.00001", "2505.00002", "2505.00003"]


def test_truncate_top_n():
    papers = arxiv.parse_atom(SAMPLE_ATOM)
    deduped = arxiv.dedup_and_truncate(papers, top_n=2)
    assert len(deduped) == 2
    assert [p.arxivId for p in deduped] == ["2505.00001", "2505.00002"]


def test_dedup_keeps_order_and_first_occurrence():
    papers = [
        Paper(title="A", authors=[], arxivId="x", link="l1", summary="s1"),
        Paper(title="A-dup", authors=[], arxivId="x", link="l1", summary="s2"),
        Paper(title="B", authors=[], arxivId="y", link="l2", summary="s3"),
    ]
    deduped = arxiv.dedup_and_truncate(papers, top_n=5)
    assert [p.title for p in deduped] == ["A", "B"]
