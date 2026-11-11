"""Config screen: edit Config fields, save to TOML."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Static

from pomocat import storage
from pomocat.core.config import Config, save_config


class ConfigScreen(Screen):
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        cfg: Config = self.app.cfg  # type: ignore[attr-defined]
        yield Header(show_clock=False)
        with Vertical(id="config-body"):
            yield Label("Work minutes")
            yield Input(str(cfg.work_minutes), id="work-minutes-input")
            yield Label("Short break minutes")
            yield Input(str(cfg.short_break_minutes), id="short-break-input")
            yield Label("Long break minutes")
            yield Input(str(cfg.long_break_minutes), id="long-break-input")
            yield Label("Rounds until long break")
            yield Input(str(cfg.rounds_until_long_break), id="rounds-input")
            yield Label("Sound enabled (true/false)")
            yield Input(str(cfg.sound_enabled).lower(), id="sound-input")
            yield Button("Save", id="save-button", variant="primary")
            yield Static("", id="config-toast")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "save-button":
            return
        try:
            new_cfg = Config(
                work_minutes=int(self.query_one("#work-minutes-input", Input).value),
                short_break_minutes=int(self.query_one("#short-break-input", Input).value),
                long_break_minutes=int(self.query_one("#long-break-input", Input).value),
                rounds_until_long_break=int(self.query_one("#rounds-input", Input).value),
                sound_enabled=self.query_one("#sound-input", Input).value.strip().lower() == "true",
            )
        except ValueError:
            self.query_one("#config-toast", Static).update(
                "[red]每個欄位需為整數或 true/false[/]"
            )
            return

        save_config(new_cfg, storage.CONFIG_FILE)
        self.app.cfg = new_cfg  # type: ignore[attr-defined]
        self.query_one("#config-toast", Static).update("[green]已儲存[/]")

    def action_quit(self) -> None:
        self.app.exit()
