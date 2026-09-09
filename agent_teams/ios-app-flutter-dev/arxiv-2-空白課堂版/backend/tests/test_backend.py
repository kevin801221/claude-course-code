"""後端測試：Atom 解析、報告組裝、FastAPI 端點。"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import date
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# ---------- Atom 解析測試 ----------

SAMPLE_ATOM_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2505.99999v1</id>
    <title>Test Paper: A Novel Approach</title>
    <summary>This is a test abstract about machine learning.</summary>
    <author><name>Alice Smith</name></author>
    <author><name>Bob Jones</name></author>
    <link href="https://arxiv.org/abs/2505.99999" rel="alternate" type="text/html"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2505.88888v2</id>
    <title>Another Paper: Deep Dive</title>
    <summary>This abstract covers deep learning topics.</summary>
    <author><name>Carol White</name></author>
    <link href="https://arxiv.org/abs/2505.88888" rel="alternate" type="text/html"/>
  </entry>
</feed>"""


def test_arxiv_paper_parsing():
    """測試 feedparser 能正確解析 Atom XML。"""
    import feedparser
    feed = feedparser.parse(SAMPLE_ATOM_XML)

    assert len(feed.entries) == 2

    entry = feed.entries[0]
    arxiv_id = entry["id"].split("/abs/")[-1]
    assert "2505.99999" in arxiv_id
    assert "Test Paper" in entry["title"]
    assert len(entry["authors"]) == 2
    assert entry["authors"][0]["name"] == "Alice Smith"
    assert "machine learning" in entry["summary"]


def test_arxiv_paper_dataclass_from_atom():
    """測試從 Atom feed entry 建立 ArxivPaper。"""
    import feedparser
    from app.arxiv_fetcher import ArxivPaper

    feed = feedparser.parse(SAMPLE_ATOM_XML)
    entry = feed.entries[0]

    paper = ArxivPaper(
        title=entry["title"].replace("\n", " ").strip(),
        authors=[a["name"] for a in entry["authors"]],
        arxiv_id=entry["id"].split("/abs/")[-1],
        link=entry.get("link", ""),
        abstract=entry["summary"].replace("\n", " ").strip(),
    )

    assert paper.title == "Test Paper: A Novel Approach"
    assert paper.authors == ["Alice Smith", "Bob Jones"]
    assert "2505.99999" in paper.arxiv_id
    assert "machine learning" in paper.abstract


# ---------- 報告組裝測試 ----------

def test_build_report_structure():
    """測試 build_report 輸出結構符合 API 契約。"""
    from app.arxiv_fetcher import ArxivPaper
    from app.gemini_summarizer import SummarizedReport
    from app.generate import build_report

    papers = [
        ArxivPaper(
            title="Test Paper",
            authors=["Alice"],
            arxiv_id="2505.12345",
            link="https://arxiv.org/abs/2505.12345",
            abstract="A test abstract.",
        )
    ]
    summarizer_result = SummarizedReport(
        summaries={"2505.12345": "這篇論文提出了一種新方法。"},
        overview="今日論文涵蓋多個 AI 主題。",
        used_fallback=False,
    )
    target_date = date(2026, 5, 23)

    report = build_report(target_date, papers, summarizer_result)

    assert report["date"] == "2026-05-23"
    assert "arXiv 每日科技論文摘要" in report["title"]
    assert "markdownBody" in report
    assert isinstance(report["papers"], list)
    assert len(report["papers"]) == 1

    paper_item = report["papers"][0]
    assert paper_item["title"] == "Test Paper"
    assert paper_item["authors"] == ["Alice"]
    assert paper_item["arxivId"] == "2505.12345"
    assert paper_item["link"] == "https://arxiv.org/abs/2505.12345"
    assert "summary" in paper_item


def test_build_report_fallback_note():
    """測試 fallback 時 markdownBody 包含 fallback 說明。"""
    from app.arxiv_fetcher import ArxivPaper
    from app.gemini_summarizer import SummarizedReport
    from app.generate import build_report

    papers = [ArxivPaper("T", ["A"], "id1", "http://x", "abstract")]
    summarizer_result = SummarizedReport(
        summaries={"id1": "摘要"}, overview="綜述", used_fallback=True
    )
    report = build_report(date.today(), papers, summarizer_result)
    assert "fallback" in report["markdownBody"]


# ---------- 儲存模組測試 ----------

def test_storage_save_and_load():
    """測試儲存後能讀回相同資料。"""
    from app import storage

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(storage, "DATA_DIR", Path(tmpdir)):
            sample_report = {
                "date": "2026-05-23",
                "title": "測試報告",
                "markdownBody": "## 內容",
                "papers": [],
            }
            storage.save_report(sample_report)
            loaded = storage.load_report(date(2026, 5, 23))
            assert loaded is not None
            assert loaded["date"] == "2026-05-23"
            assert loaded["title"] == "測試報告"


def test_storage_list_dates():
    """測試 list_report_dates 回傳新到舊。"""
    from app import storage

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(storage, "DATA_DIR", Path(tmpdir)):
            for d in ["2026-05-21", "2026-05-23", "2026-05-22"]:
                storage.save_report({"date": d, "title": f"報告{d}", "markdownBody": "", "papers": []})

            dates = storage.list_report_dates()
            assert dates == ["2026-05-23", "2026-05-22", "2026-05-21"]


def test_storage_load_nonexistent():
    """測試讀取不存在的報告回 None。"""
    from app import storage

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch.object(storage, "DATA_DIR", Path(tmpdir)):
            result = storage.load_report(date(2099, 1, 1))
            assert result is None


# ---------- FastAPI 端點測試 ----------

@pytest.fixture
def client_with_temp_storage():
    """建立 TestClient，並把 storage.DATA_DIR 重導到臨時目錄。"""
    from fastapi.testclient import TestClient
    from app import storage
    from app.main import app

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        with patch.object(storage, "DATA_DIR", tmp_path):
            yield TestClient(app), tmp_path


def test_health(client_with_temp_storage):
    client, _ = client_with_temp_storage
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_reports_today_404_when_no_report(client_with_temp_storage):
    """今天報告不存在時回 404。"""
    client, _ = client_with_temp_storage
    resp = client.get("/reports/today")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "今日報告尚未產生"


def test_reports_today_returns_report(client_with_temp_storage):
    """儲存今日報告後，/reports/today 能拿到。"""
    from app import storage

    client, tmp_path = client_with_temp_storage
    today_str = date.today().isoformat()
    sample_report = {
        "date": today_str,
        "title": f"arXiv 每日科技論文摘要 · {today_str}",
        "markdownBody": "## 今日綜述\n測試內容",
        "papers": [
            {
                "title": "Paper A",
                "authors": ["Author X"],
                "arxivId": "2505.00001",
                "link": "https://arxiv.org/abs/2505.00001",
                "summary": "摘要內容",
            }
        ],
    }
    with patch.object(storage, "DATA_DIR", tmp_path):
        storage.save_report(sample_report)
        resp = client.get("/reports/today")
        assert resp.status_code == 200
        data = resp.json()
        assert data["date"] == today_str
        assert len(data["papers"]) == 1
        assert data["papers"][0]["arxivId"] == "2505.00001"


def test_reports_list(client_with_temp_storage):
    """/reports 回歷史日期清單（新到舊）。"""
    from app import storage

    client, tmp_path = client_with_temp_storage
    with patch.object(storage, "DATA_DIR", tmp_path):
        for d in ["2026-05-20", "2026-05-22", "2026-05-21"]:
            storage.save_report({"date": d, "title": f"T{d}", "markdownBody": "", "papers": []})
        resp = client.get("/reports")
        assert resp.status_code == 200
        dates = resp.json()
        assert dates == ["2026-05-22", "2026-05-21", "2026-05-20"]


def test_reports_by_date_found(client_with_temp_storage):
    """/reports/{date} 指定日期能找到報告。"""
    from app import storage

    client, tmp_path = client_with_temp_storage
    with patch.object(storage, "DATA_DIR", tmp_path):
        storage.save_report({"date": "2026-05-15", "title": "舊報告", "markdownBody": "x", "papers": []})
        resp = client.get("/reports/2026-05-15")
        assert resp.status_code == 200
        assert resp.json()["date"] == "2026-05-15"


def test_reports_by_date_404(client_with_temp_storage):
    """/reports/{date} 查無資料回 404。"""
    client, _ = client_with_temp_storage
    resp = client.get("/reports/2099-01-01")
    assert resp.status_code == 404


# ---------- fallback 摘要測試 ----------

def test_local_fallback_summary():
    """無 API key 時 fallback 摘要不為空。"""
    from app.arxiv_fetcher import SAMPLE_PAPERS
    from app.gemini_summarizer import _local_fallback

    result = _local_fallback(SAMPLE_PAPERS)
    assert result.used_fallback is True
    assert len(result.summaries) == len(SAMPLE_PAPERS)
    assert len(result.overview) > 20
    for paper in SAMPLE_PAPERS:
        assert paper.arxiv_id in result.summaries
        assert len(result.summaries[paper.arxiv_id]) > 0
