"""Timer domain model: pure functions, no I/O, no Textual."""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum


class Phase(StrEnum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


@dataclass(frozen=True)
class TimerState:
    phase: Phase
    remaining_seconds: int
    round_index: int
    is_running: bool
    task_label: str | None


from pomocat.core.config import Config


def next_phase(state: TimerState, cfg: Config) -> TimerState:
    """Transition to the next phase. Pure function.

    WORK → LONG_BREAK if round_index % rounds_until_long_break == 0,
           else SHORT_BREAK. round_index unchanged.
    SHORT_BREAK → WORK, round_index += 1.
    LONG_BREAK → WORK, round_index reset to 1.

    `is_running` and `task_label` are preserved.
    """
    if state.phase == Phase.WORK:
        is_long = state.round_index % cfg.rounds_until_long_break == 0
        new_phase = Phase.LONG_BREAK if is_long else Phase.SHORT_BREAK
        new_seconds = (
            cfg.long_break_minutes if is_long else cfg.short_break_minutes
        ) * 60
        return replace(
            state, phase=new_phase, remaining_seconds=new_seconds,
        )

    if state.phase == Phase.SHORT_BREAK:
        return replace(
            state,
            phase=Phase.WORK,
            remaining_seconds=cfg.work_minutes * 60,
            round_index=state.round_index + 1,
        )

    # LONG_BREAK
    return replace(
        state,
        phase=Phase.WORK,
        remaining_seconds=cfg.work_minutes * 60,
        round_index=1,
    )


def tick(state: TimerState, elapsed_seconds: int = 1) -> TimerState:
    """Advance timer by `elapsed_seconds`. Pure function.

    Returns the same state untouched if `is_running` is False.
    Clamps `remaining_seconds` at 0 (never negative).
    """
    if not state.is_running:
        return state
    new_remaining = max(0, state.remaining_seconds - elapsed_seconds)
    return replace(state, remaining_seconds=new_remaining)
