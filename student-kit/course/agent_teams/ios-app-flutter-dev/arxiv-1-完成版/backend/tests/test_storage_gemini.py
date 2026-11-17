"""storage 存取 round-trip 與 gemini fallback(沒 key)測試。"""

from __future__ import annotations

import importlib

from app.models import Paper, Report

SAMPLE_PAPERS = [
    Paper(
        title="Test Paper",
        authors=["Alice"],
        arxivId="2505.00001",
        link="https://arxiv.org/abs/2505.00001",
        summary="An abstract.",
    )
]


def _reload_with_data_dir(tmp_path, monkeypatch):
    """把 DATA_DIR 指到暫存目錄,避免污染 backend/data/。"""
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    import app.config as config

    importlib.reload(config)
    import app.storage as storage

    importlib.reload(storage)
    return storage


def test_storage_round_trip(tmp_path, monkeypatch):
    storage = _reload_with_data_dir(tmp_path, monkeypatch)
    report = Report(
        date="2026-05-22",
        title="t",
        markdownBody="## body",
        papers=SAMPLE_PAPERS,
    )
    storage.save(report)
    loaded = storage.load("2026-05-22")
    assert loaded is not None
    assert loaded.date == "2026-05-22"
    assert loaded.papers[0].arxivId == "2505.00001"
    assert storage.list_dates() == ["2026-05-22"]
    assert storage.load("2026-01-01") is None
    assert storage.load("bad-date") is None


def test_list_dates_newest_first(tmp_path, monkeypatch):
    storage = _reload_with_data_dir(tmp_path, monkeypatch)
    for d in ["2026-05-20", "2026-05-22", "2026-05-21"]:
        storage.save(Report(date=d, title="t", markdownBody="b", papers=[]))
    assert storage.list_dates() == ["2026-05-22", "2026-05-21", "2026-05-20"]


def test_gemini_fallback_without_key(monkeypatch):
    # 設成空字串(而非 delenv):load_dotenv 預設不覆蓋既有環境變數,
    # 因此即使專案根目錄 .env 有真 key,reload config 後本測試仍視為「無 key」。
    monkeypatch.setenv("GEMINI_API_KEY", "")
    import app.config as config

    importlib.reload(config)
    import app.gemini as gemini

    importlib.reload(gemini)

    assert config.has_gemini_key() is False
    markdown, papers = gemini.summarize("2026-05-22", SAMPLE_PAPERS)
    assert "未設 GEMINI_API_KEY" in markdown
    assert "今日綜述" in markdown
    # 沒 key 時各篇 summary 沿用 abstract
    assert papers[0].summary == "An abstract."
