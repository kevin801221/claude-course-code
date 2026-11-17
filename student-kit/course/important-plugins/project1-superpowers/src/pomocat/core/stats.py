"""Stats domain model. Pure functions, no I/O."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from pomocat.core.timer import Phase


@dataclass(frozen=True)
class Round:
    started_at: datetime
    ended_at: datetime
    phase: Phase
    task_label: str | None
    completed: bool


@dataclass(frozen=True)
class DailySummary:
    date: date
    completed_work_count: int
    completed_work_minutes: int
    interrupted_count: int
    task_breakdown: dict[str, int] = field(default_factory=dict)


def daily_summary(rounds: list[Round], target: date) -> DailySummary:
    same_day = [r for r in rounds if r.started_at.date() == target]
    work = [r for r in same_day if r.phase == Phase.WORK]
    completed_work = [r for r in work if r.completed]
    interrupted = [r for r in work if not r.completed]

    breakdown: dict[str, int] = {}
    for r in completed_work:
        key = r.task_label if r.task_label else "(no label)"
        breakdown[key] = breakdown.get(key, 0) + 1

    total_minutes = sum(
        int((r.ended_at - r.started_at).total_seconds() / 60)
        for r in completed_work
    )

    return DailySummary(
        date=target,
        completed_work_count=len(completed_work),
        completed_work_minutes=total_minutes,
        interrupted_count=len(interrupted),
        task_breakdown=breakdown,
    )


def weekly_summary(
    rounds: list[Round], week_start: date,
) -> list[DailySummary]:
    return [
        daily_summary(rounds, week_start + timedelta(days=i))
        for i in range(7)
    ]


def monthly_summary(
    rounds: list[Round], year: int, month: int,
) -> list[DailySummary]:
    import calendar
    _, last = calendar.monthrange(year, month)
    return [
        daily_summary(rounds, date(year, month, d))
        for d in range(1, last + 1)
    ]
