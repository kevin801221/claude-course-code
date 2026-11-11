"""Persistent storage for rounds + config at ~/.pomocat/.

JSONL append-only for rounds (crash-safe, no read-modify-write).
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from pomocat.core.stats import Round
from pomocat.core.timer import Phase

DATA_DIR = Path.home() / ".pomocat"
ROUNDS_FILE = DATA_DIR / "rounds.jsonl"
CONFIG_FILE = DATA_DIR / "config.toml"


def _serialize(r: Round) -> dict:
    d = asdict(r)
    d["started_at"] = r.started_at.isoformat()
    d["ended_at"] = r.ended_at.isoformat()
    d["phase"] = r.phase.value
    return d


def _deserialize(d: dict) -> Round:
    return Round(
        started_at=datetime.fromisoformat(d["started_at"]),
        ended_at=datetime.fromisoformat(d["ended_at"]),
        phase=Phase(d["phase"]),
        task_label=d["task_label"],
        completed=d["completed"],
    )


def append_round(r: Round) -> None:
    """Append a single round to rounds.jsonl, creating parent dir if needed."""
    ROUNDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with ROUNDS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_serialize(r), ensure_ascii=False) + "\n")


def load_rounds() -> list[Round]:
    """Read all rounds from rounds.jsonl.

    Corrupt lines are skipped with a warning to stderr.
    Missing file returns empty list.
    """
    if not ROUNDS_FILE.exists():
        return []
    out: list[Round] = []
    for lineno, raw in enumerate(
        ROUNDS_FILE.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not raw.strip():
            continue
        try:
            out.append(_deserialize(json.loads(raw)))
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            print(
                f"pomocat: skipped corrupt line {lineno} in {ROUNDS_FILE} "
                f"({exc})",
                file=sys.stderr,
            )
    return out
