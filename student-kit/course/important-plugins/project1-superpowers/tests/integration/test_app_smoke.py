"""End-to-end smoke tests using Textual pilot."""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_app_starts_and_quits():
    from pomocat.ui.app import PomocatApp
    app = PomocatApp(initial_screen="timer", initial_task="test")
    async with app.run_test() as pilot:
        await pilot.press("q")
    # If we got here without hanging, the app started and quit cleanly.


@pytest.mark.asyncio
async def test_timer_screen_pause_resume_keybinding(tmp_path, monkeypatch):
    """Pressing space toggles the running flag."""
    monkeypatch.setattr("pomocat.storage.DATA_DIR", tmp_path)
    monkeypatch.setattr("pomocat.storage.ROUNDS_FILE", tmp_path / "rounds.jsonl")
    monkeypatch.setattr("pomocat.storage.CONFIG_FILE", tmp_path / "config.toml")

    from pomocat.ui.app import PomocatApp
    app = PomocatApp(initial_screen="timer", initial_task="x")
    async with app.run_test() as pilot:
        screen = app.screen
        initial = screen.state.is_running
        await pilot.press("space")
        await pilot.pause()
        assert screen.state.is_running != initial
        await pilot.press("q")


@pytest.mark.asyncio
async def test_stats_screen_opens_with_week_range(tmp_path, monkeypatch):
    monkeypatch.setattr("pomocat.storage.DATA_DIR", tmp_path)
    monkeypatch.setattr("pomocat.storage.ROUNDS_FILE", tmp_path / "rounds.jsonl")
    monkeypatch.setattr("pomocat.storage.CONFIG_FILE", tmp_path / "config.toml")

    from pomocat.ui.app import PomocatApp
    app = PomocatApp(initial_screen="stats", stats_range="week")
    async with app.run_test() as pilot:
        assert app.screen.range_ == "week"
        await pilot.press("q")


@pytest.mark.asyncio
async def test_config_screen_save_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr("pomocat.storage.DATA_DIR", tmp_path)
    monkeypatch.setattr("pomocat.storage.ROUNDS_FILE", tmp_path / "rounds.jsonl")
    monkeypatch.setattr("pomocat.storage.CONFIG_FILE", tmp_path / "config.toml")

    from pomocat.ui.app import PomocatApp
    app = PomocatApp(initial_screen="config")
    async with app.run_test() as pilot:
        screen = app.screen
        # change work_minutes input to 50
        work_input = screen.query_one("#work-minutes-input")
        work_input.value = "50"
        await pilot.click("#save-button")
        await pilot.pause()
        await pilot.press("q")

    from pomocat.core.config import load_config
    saved = load_config(tmp_path / "config.toml")
    assert saved.work_minutes == 50
