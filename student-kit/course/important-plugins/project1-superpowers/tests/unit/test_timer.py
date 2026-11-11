"""Tests for pomocat.core.timer."""
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from pomocat.core.config import Config
from pomocat.core.timer import Phase, TimerState, next_phase, tick


class TestPhase:
    def test_three_phases_exist(self):
        assert Phase.WORK.value == "work"
        assert Phase.SHORT_BREAK.value == "short_break"
        assert Phase.LONG_BREAK.value == "long_break"

    def test_phase_is_str(self):
        assert Phase.WORK == "work"


class TestTimerState:
    def test_construct_with_all_fields(self):
        s = TimerState(
            phase=Phase.WORK,
            remaining_seconds=1500,
            round_index=1,
            is_running=False,
            task_label=None,
        )
        assert s.phase == Phase.WORK
        assert s.remaining_seconds == 1500
        assert s.round_index == 1
        assert s.is_running is False
        assert s.task_label is None

    def test_is_frozen(self):
        s = TimerState(
            phase=Phase.WORK, remaining_seconds=1500,
            round_index=1, is_running=False, task_label=None,
        )
        with pytest.raises(FrozenInstanceError):
            s.remaining_seconds = 0  # type: ignore[misc]


class TestTick:
    def _state(self, **overrides) -> TimerState:
        defaults = dict(
            phase=Phase.WORK, remaining_seconds=60,
            round_index=1, is_running=True, task_label=None,
        )
        defaults.update(overrides)
        return TimerState(**defaults)

    def test_decrements_when_running(self):
        s = self._state(remaining_seconds=60)
        assert tick(s).remaining_seconds == 59

    def test_decrement_amount_configurable(self):
        s = self._state(remaining_seconds=60)
        assert tick(s, elapsed_seconds=5).remaining_seconds == 55

    def test_does_not_decrement_when_paused(self):
        s = self._state(is_running=False, remaining_seconds=60)
        assert tick(s) == s

    def test_does_not_go_negative(self):
        s = self._state(remaining_seconds=0)
        assert tick(s).remaining_seconds == 0

    def test_clamps_overshoot(self):
        s = self._state(remaining_seconds=3)
        assert tick(s, elapsed_seconds=10).remaining_seconds == 0

    def test_returns_new_instance(self):
        s = self._state()
        assert tick(s) is not s


class TestNextPhase:
    def _state(self, **overrides) -> TimerState:
        defaults = dict(
            phase=Phase.WORK, remaining_seconds=0,
            round_index=1, is_running=True, task_label="x",
        )
        defaults.update(overrides)
        return TimerState(**defaults)

    def test_work_to_short_break_when_round_not_at_threshold(self):
        cfg = Config(rounds_until_long_break=4)
        s = self._state(phase=Phase.WORK, round_index=2)
        nxt = next_phase(s, cfg)
        assert nxt.phase == Phase.SHORT_BREAK
        assert nxt.remaining_seconds == 5 * 60
        assert nxt.round_index == 2  # round doesn't advance on break entry

    def test_every_fourth_work_round_goes_to_long_break(self):
        cfg = Config(rounds_until_long_break=4)
        s = self._state(phase=Phase.WORK, round_index=4)
        nxt = next_phase(s, cfg)
        assert nxt.phase == Phase.LONG_BREAK
        assert nxt.remaining_seconds == 15 * 60

    def test_short_break_returns_to_work_and_advances_round(self):
        cfg = Config()
        s = self._state(phase=Phase.SHORT_BREAK, round_index=2)
        nxt = next_phase(s, cfg)
        assert nxt.phase == Phase.WORK
        assert nxt.round_index == 3
        assert nxt.remaining_seconds == 25 * 60

    def test_long_break_resets_round_to_1(self):
        cfg = Config(rounds_until_long_break=4)
        s = self._state(phase=Phase.LONG_BREAK, round_index=4)
        nxt = next_phase(s, cfg)
        assert nxt.phase == Phase.WORK
        assert nxt.round_index == 1

    def test_preserves_task_label_into_next_work(self):
        cfg = Config()
        s = self._state(phase=Phase.SHORT_BREAK, round_index=1,
                        task_label="寫教材")
        nxt = next_phase(s, cfg)
        assert nxt.task_label == "寫教材"

    def test_break_phase_keeps_running(self):
        cfg = Config()
        s = self._state(phase=Phase.WORK, is_running=True)
        assert next_phase(s, cfg).is_running is True
