"""Timer screen: countdown, phase badge, progress bar, keybindings."""
from __future__ import annotations

from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Digits, Footer, Header, ProgressBar, Static

from pomocat import sound
from pomocat.core.stats import Round, daily_summary, weekly_summary
from pomocat.core.timer import Phase, TimerState, next_phase, tick
from pomocat.storage import append_round, load_rounds


class TimerScreen(Screen):
    BINDINGS = [
        ("space", "toggle_pause", "Pause/Resume"),
        ("s", "skip", "Skip"),
        ("r", "reset", "Reset"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, task_label: str | None = None) -> None:
        super().__init__()
        self.task_label = task_label
        self.cfg = None  # filled in on_mount from app
        self.state: TimerState | None = None
        self._phase_started_at: datetime | None = None
        self._phase_total_seconds = 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Vertical(id="timer-body"):
            with Center():
                yield Digits("25:00", id="time-display")
            yield Static("WORK", id="phase-badge")
            yield ProgressBar(total=100, show_eta=False, id="time-progress")
            yield Static("", id="counters")
        yield Footer()

    def on_mount(self) -> None:
        self.cfg = self.app.cfg  # type: ignore[attr-defined]
        self.state = TimerState(
            phase=Phase.WORK,
            remaining_seconds=self.cfg.work_minutes * 60,
            round_index=1,
            is_running=True,
            task_label=self.task_label,
        )
        self._phase_started_at = datetime.now()
        self._phase_total_seconds = self.state.remaining_seconds
        self._update_display()
        self._refresh_counters()
        self.set_interval(1.0, self._tick)

    def _tick(self) -> None:
        assert self.state is not None
        self.state = tick(self.state)
        self._update_display()
        if self.state.remaining_seconds == 0 and self.state.is_running:
            self._on_phase_complete()

    def _update_display(self) -> None:
        assert self.state is not None
        mins, secs = divmod(self.state.remaining_seconds, 60)
        self.query_one("#time-display", Digits).update(f"{mins:02d}:{secs:02d}")
        badge = self.query_one("#phase-badge", Static)
        badge.update(self._badge_text())
        badge.set_class(self.state.phase == Phase.WORK, "phase-work")
        badge.set_class(self.state.phase == Phase.SHORT_BREAK, "phase-short")
        badge.set_class(self.state.phase == Phase.LONG_BREAK, "phase-long")
        progress = self.query_one("#time-progress", ProgressBar)
        if self._phase_total_seconds:
            done = self._phase_total_seconds - self.state.remaining_seconds
            progress.update(progress=int(done / self._phase_total_seconds * 100))

    def _badge_text(self) -> str:
        assert self.state is not None
        label = {
            Phase.WORK: "WORK",
            Phase.SHORT_BREAK: "SHORT BREAK",
            Phase.LONG_BREAK: "LONG BREAK",
        }[self.state.phase]
        if self.state.task_label and self.state.phase == Phase.WORK:
            return f"{label} · {self.state.task_label}"
        return label

    def _build_round(self, completed: bool) -> Round:
        assert self.state is not None
        return Round(
            started_at=self._phase_started_at or datetime.now(),
            ended_at=datetime.now(),
            phase=self.state.phase,
            task_label=self.state.task_label,
            completed=completed,
        )

    def _advance(self, mark_completed: bool) -> None:
        """Record current round and move to the next phase."""
        assert self.state is not None and self.cfg is not None
        append_round(self._build_round(completed=mark_completed))
        self.state = next_phase(self.state, self.cfg)
        self._phase_started_at = datetime.now()
        self._phase_total_seconds = self.state.remaining_seconds
        self._update_display()
        self._refresh_counters()

    def _on_phase_complete(self) -> None:
        sound.play_alarm()
        self._advance(mark_completed=True)

    def _refresh_counters(self) -> None:
        from datetime import date, timedelta
        rounds = load_rounds()
        today = daily_summary(rounds, date.today())
        week_start = date.today() - timedelta(days=date.today().weekday())
        week = weekly_summary(rounds, week_start)
        week_total = sum(d.completed_work_count for d in week)
        self.query_one("#counters", Static).update(
            f"今日完成 {today.completed_work_count} 顆 🍅  ·  "
            f"本週 {week_total} 顆"
        )

    # ── actions ────────────────────────────────────────────────

    def action_toggle_pause(self) -> None:
        from dataclasses import replace
        assert self.state is not None
        self.state = replace(self.state, is_running=not self.state.is_running)
        self._update_display()

    def action_skip(self) -> None:
        self._advance(mark_completed=False)

    def action_reset(self) -> None:
        from dataclasses import replace
        assert self.state is not None and self.cfg is not None
        append_round(self._build_round(completed=False))
        full = {
            Phase.WORK: self.cfg.work_minutes,
            Phase.SHORT_BREAK: self.cfg.short_break_minutes,
            Phase.LONG_BREAK: self.cfg.long_break_minutes,
        }[self.state.phase] * 60
        self.state = replace(self.state, remaining_seconds=full)
        self._phase_started_at = datetime.now()
        self._phase_total_seconds = full
        self._update_display()

    def action_quit(self) -> None:
        assert self.state is not None
        append_round(self._build_round(completed=False))
        self.app.exit()
