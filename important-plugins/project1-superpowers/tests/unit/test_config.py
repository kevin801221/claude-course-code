"""Tests for pomocat.core.config."""
from __future__ import annotations

from pathlib import Path

from pomocat.core.config import Config, load_config, save_config


class TestConfig:
    def test_defaults_match_classic_pomodoro(self):
        c = Config()
        assert c.work_minutes == 25
        assert c.short_break_minutes == 5
        assert c.long_break_minutes == 15
        assert c.rounds_until_long_break == 4
        assert c.sound_enabled is True


class TestLoadConfig:
    def test_missing_file_returns_defaults(self, tmp_path: Path):
        assert load_config(tmp_path / "nope.toml") == Config()

    def test_partial_file_merges_with_defaults(self, tmp_path: Path):
        path = tmp_path / "config.toml"
        path.write_text("work_minutes = 50\n")
        c = load_config(path)
        assert c.work_minutes == 50
        assert c.short_break_minutes == 5  # default

    def test_full_file_loads_all_fields(self, tmp_path: Path):
        path = tmp_path / "config.toml"
        path.write_text(
            "work_minutes = 50\n"
            "short_break_minutes = 10\n"
            "long_break_minutes = 20\n"
            "rounds_until_long_break = 3\n"
            "sound_enabled = false\n"
        )
        c = load_config(path)
        assert c == Config(50, 10, 20, 3, False)


class TestSaveConfig:
    def test_save_then_load_roundtrips(self, tmp_path: Path):
        path = tmp_path / "config.toml"
        original = Config(50, 10, 20, 3, False)
        save_config(original, path)
        assert load_config(path) == original

    def test_save_creates_parent_dir(self, tmp_path: Path):
        path = tmp_path / "sub" / "config.toml"
        save_config(Config(), path)
        assert path.exists()
