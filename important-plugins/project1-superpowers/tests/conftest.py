"""Shared fixtures for pomocat tests."""
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest


def pytest_collection_finish(session: pytest.Session) -> None:
    """Force exit 0 when no tests are collected (bootstrap-only).

    Skips when collection errors occurred so real failures aren't masked.
    """
    if session.items:
        return
    if session.testsfailed:
        return
    if session.exitstatus not in (0, 5):  # 5 = NO_TESTS_COLLECTED
        return
    pytest.exit("no tests ran", returncode=0)


@pytest.fixture
def round_factory():
    """Build a Round with sensible defaults; override any field via kwargs."""
    from pomocat.core.timer import Phase  # noqa: PLC0415
    from pomocat.core.stats import Round  # noqa: PLC0415

    def _make(
        started_at: datetime | None = None,
        ended_at: datetime | None = None,
        phase: Phase = Phase.WORK,
        task_label: str | None = None,
        completed: bool = True,
    ) -> Round:
        started_at = started_at or datetime(2026, 5, 14, 9, 0, 0)
        ended_at = ended_at or started_at + timedelta(minutes=25)
        return Round(
            started_at=started_at,
            ended_at=ended_at,
            phase=phase,
            task_label=task_label,
            completed=completed,
        )
    return _make


@pytest.fixture
def isolated_data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect storage.DATA_DIR to a tmp dir for the test."""
    monkeypatch.setattr("pomocat.storage.DATA_DIR", tmp_path)
    monkeypatch.setattr("pomocat.storage.ROUNDS_FILE", tmp_path / "rounds.jsonl")
    monkeypatch.setattr("pomocat.storage.CONFIG_FILE", tmp_path / "config.toml")
    return tmp_path
