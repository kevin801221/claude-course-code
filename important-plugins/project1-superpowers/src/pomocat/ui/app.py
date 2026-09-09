"""Top-level Textual application."""
from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult

from pomocat.core.config import load_config
from pomocat.storage import CONFIG_FILE


class PomocatApp(App):
    CSS_PATH = "pomocat.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(
        self,
        initial_screen: str = "timer",
        initial_task: str | None = None,
        stats_range: str = "week",
    ) -> None:
        super().__init__()
        self.initial_screen = initial_screen
        self.initial_task = initial_task
        self.stats_range = stats_range
        self.cfg = load_config(CONFIG_FILE)

    def on_mount(self) -> None:
        if self.initial_screen == "stats":
            from pomocat.ui.stats_screen import StatsScreen
            self.push_screen(StatsScreen(range_=self.stats_range))
        elif self.initial_screen == "config":
            from pomocat.ui.config_screen import ConfigScreen
            self.push_screen(ConfigScreen())
        else:
            from pomocat.ui.timer_screen import TimerScreen
            self.push_screen(TimerScreen(task_label=self.initial_task))
