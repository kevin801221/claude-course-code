"""Tests for pomocat.storage."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pomocat.core.stats import Round
from pomocat.core.timer import Phase
from pomocat.storage import append_round, load_rounds


class TestAppendAndLoad:
    def test_load_when_file_missing_returns_empty(self, isolated_data_dir: Path):
        assert load_rounds() == []

    def test_append_then_load_roundtrips(self, isolated_data_dir: Path):
        r = Round(
            started_at=datetime(2026, 5, 14, 9, 0),
            ended_at=datetime(2026, 5, 14, 9, 25),
            phase=Phase.WORK,
            task_label="寫教材",
            completed=True,
        )
        append_round(r)
        loaded = load_rounds()
        assert loaded == [r]

    def test_append_appends_not_overwrites(self, isolated_data_dir: Path):
        r1 = Round(
            started_at=datetime(2026, 5, 14, 9, 0),
            ended_at=datetime(2026, 5, 14, 9, 25),
            phase=Phase.WORK, task_label=None, completed=True,
        )
        r2 = Round(
            started_at=datetime(2026, 5, 14, 9, 30),
            ended_at=datetime(2026, 5, 14, 9, 35),
            phase=Phase.SHORT_BREAK, task_label=None, completed=True,
        )
        append_round(r1)
        append_round(r2)
        assert load_rounds() == [r1, r2]

    def test_load_skips_corrupt_lines(self, isolated_data_dir: Path, capsys):
        good = Round(
            started_at=datetime(2026, 5, 14, 9, 0),
            ended_at=datetime(2026, 5, 14, 9, 25),
            phase=Phase.WORK, task_label=None, completed=True,
        )
        append_round(good)
        rounds_file = isolated_data_dir / "rounds.jsonl"
        with rounds_file.open("a") as f:
            f.write("not valid json\n")
        append_round(good)
        loaded = load_rounds()
        assert loaded == [good, good]
        captured = capsys.readouterr()
        assert "skipped" in captured.err.lower()

    def test_append_creates_parent_dir(self, isolated_data_dir: Path):
        import shutil
        shutil.rmtree(isolated_data_dir)
        r = Round(
            started_at=datetime(2026, 5, 14, 9, 0),
            ended_at=datetime(2026, 5, 14, 9, 25),
            phase=Phase.WORK, task_label=None, completed=True,
        )
        append_round(r)
        assert isolated_data_dir.exists()
