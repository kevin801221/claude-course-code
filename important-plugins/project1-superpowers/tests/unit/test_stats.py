"""Tests for pomocat.core.stats."""
from __future__ import annotations

from datetime import date, datetime, timedelta

from pomocat.core.stats import (
    DailySummary,
    Round,
    daily_summary,
    monthly_summary,
    weekly_summary,
)
from pomocat.core.timer import Phase


class TestRound:
    def test_construct(self):
        r = Round(
            started_at=datetime(2026, 5, 14, 9, 0),
            ended_at=datetime(2026, 5, 14, 9, 25),
            phase=Phase.WORK,
            task_label="寫教材",
            completed=True,
        )
        assert r.phase == Phase.WORK
        assert r.task_label == "寫教材"
        assert r.completed is True


class TestDailySummary:
    def _r(self, hour=9, phase=Phase.WORK, completed=True,
           task=None, day=14):
        start = datetime(2026, 5, day, hour, 0)
        return Round(
            started_at=start,
            ended_at=start + timedelta(minutes=25),
            phase=phase,
            task_label=task,
            completed=completed,
        )

    def test_empty_returns_zero_summary(self):
        s = daily_summary([], date(2026, 5, 14))
        assert s.completed_work_count == 0
        assert s.completed_work_minutes == 0
        assert s.interrupted_count == 0
        assert s.task_breakdown == {}

    def test_counts_only_completed_work(self):
        rounds = [
            self._r(phase=Phase.WORK, completed=True),
            self._r(phase=Phase.WORK, completed=False),
            self._r(phase=Phase.SHORT_BREAK, completed=True),
        ]
        s = daily_summary(rounds, date(2026, 5, 14))
        assert s.completed_work_count == 1
        assert s.interrupted_count == 1

    def test_minutes_sum_ended_minus_started(self):
        rounds = [self._r(), self._r(hour=10)]
        s = daily_summary(rounds, date(2026, 5, 14))
        assert s.completed_work_minutes == 50

    def test_task_breakdown_groups_by_label(self):
        rounds = [
            self._r(task="寫教材"),
            self._r(task="寫教材", hour=10),
            self._r(task="debug", hour=11),
            self._r(task=None, hour=12),
        ]
        s = daily_summary(rounds, date(2026, 5, 14))
        assert s.task_breakdown == {
            "寫教材": 2, "debug": 1, "(no label)": 1,
        }

    def test_filters_to_target_date(self):
        rounds = [
            self._r(day=13),
            self._r(day=14),
            self._r(day=15),
        ]
        s = daily_summary(rounds, date(2026, 5, 14))
        assert s.completed_work_count == 1


class TestWeeklySummary:
    def test_returns_seven_days_starting_from_week_start(self):
        result = weekly_summary([], date(2026, 5, 11))
        assert [s.date for s in result] == [
            date(2026, 5, 11),
            date(2026, 5, 12),
            date(2026, 5, 13),
            date(2026, 5, 14),
            date(2026, 5, 15),
            date(2026, 5, 16),
            date(2026, 5, 17),
        ]

    def test_aggregates_per_day(self):
        r1 = Round(
            started_at=datetime(2026, 5, 11, 9), ended_at=datetime(2026, 5, 11, 9, 25),
            phase=Phase.WORK, task_label=None, completed=True,
        )
        r2 = Round(
            started_at=datetime(2026, 5, 13, 10), ended_at=datetime(2026, 5, 13, 10, 25),
            phase=Phase.WORK, task_label=None, completed=True,
        )
        result = weekly_summary([r1, r2], date(2026, 5, 11))
        assert result[0].completed_work_count == 1
        assert result[1].completed_work_count == 0
        assert result[2].completed_work_count == 1


class TestMonthlySummary:
    def test_returns_all_days_in_month(self):
        result = monthly_summary([], 2026, 5)
        assert len(result) == 31
        assert result[0].date == date(2026, 5, 1)
        assert result[-1].date == date(2026, 5, 31)

    def test_february_leap_year(self):
        assert len(monthly_summary([], 2024, 2)) == 29
        assert len(monthly_summary([], 2026, 2)) == 28
