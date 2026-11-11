"""Stats screen: today summary + plotext line chart."""
from __future__ import annotations

from datetime import date, timedelta

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static
from textual_plotext import PlotextPlot

from pomocat.core.stats import (
    daily_summary,
    monthly_summary,
    weekly_summary,
)
from pomocat.storage import load_rounds


class StatsScreen(Screen):
    BINDINGS = [
        ("left", "prev_period", "Prev"),
        ("right", "next_period", "Next"),
        ("d", "set_day", "Day"),
        ("w", "set_week", "Week"),
        ("m", "set_month", "Month"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, range_: str = "week") -> None:
        super().__init__()
        self.range_ = range_  # "day" | "week" | "month"
        self._anchor: date = date.today()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Vertical():
            yield Static("", id="stats-summary")
            yield PlotextPlot(id="stats-chart")
        yield Footer()

    def on_mount(self) -> None:
        self._refresh()

    def _refresh(self) -> None:
        rounds = load_rounds()
        summary = self.query_one("#stats-summary", Static)
        chart = self.query_one("#stats-chart", PlotextPlot)
        plt = chart.plt
        plt.clear_data()
        plt.clear_figure()

        if self.range_ == "day":
            d = daily_summary(rounds, self._anchor)
            tasks = ", ".join(
                f"{k}({v})" for k, v in d.task_breakdown.items()
            ) or "—"
            summary.update(
                f"{self._anchor.isoformat()}: "
                f"{d.completed_work_count} 顆 ({d.completed_work_minutes} min) "
                f"· 中斷 {d.interrupted_count} · {tasks}"
            )
            plt.bar(["completed", "interrupted"],
                    [d.completed_work_count, d.interrupted_count])
            plt.title(f"{self._anchor}")
        elif self.range_ == "week":
            week_start = self._anchor - timedelta(days=self._anchor.weekday())
            days = weekly_summary(rounds, week_start)
            summary.update(
                f"Week of {week_start.isoformat()}: "
                f"{sum(d.completed_work_count for d in days)} 顆"
            )
            plt.bar(
                [d.date.strftime("%a") for d in days],
                [d.completed_work_count for d in days],
            )
            plt.title(f"Week of {week_start}")
        else:  # month
            days = monthly_summary(
                rounds, self._anchor.year, self._anchor.month,
            )
            summary.update(
                f"{self._anchor.year}-{self._anchor.month:02d}: "
                f"{sum(d.completed_work_count for d in days)} 顆"
            )
            plt.plot(
                [d.date.day for d in days],
                [d.completed_work_count for d in days],
            )
            plt.title(f"{self._anchor.year}-{self._anchor.month:02d}")

        chart.refresh()

    def _shift(self, direction: int) -> None:
        if self.range_ == "day":
            self._anchor += timedelta(days=direction)
        elif self.range_ == "week":
            self._anchor += timedelta(days=7 * direction)
        else:
            month = self._anchor.month + direction
            year = self._anchor.year
            if month < 1:
                month, year = 12, year - 1
            elif month > 12:
                month, year = 1, year + 1
            self._anchor = self._anchor.replace(year=year, month=month, day=1)
        self._refresh()

    def action_prev_period(self) -> None: self._shift(-1)
    def action_next_period(self) -> None: self._shift(+1)

    def action_set_day(self) -> None:
        self.range_ = "day"; self._refresh()

    def action_set_week(self) -> None:
        self.range_ = "week"; self._refresh()

    def action_set_month(self) -> None:
        self.range_ = "month"; self._refresh()

    def action_quit(self) -> None:
        self.app.exit()
