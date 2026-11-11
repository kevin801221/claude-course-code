"""Config dataclass + TOML I/O. Pure logic, no Textual."""
from __future__ import annotations

import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path

import tomli_w


@dataclass(frozen=True)
class Config:
    work_minutes: int = 25
    short_break_minutes: int = 5
    long_break_minutes: int = 15
    rounds_until_long_break: int = 4
    sound_enabled: bool = True


def load_config(path: Path) -> Config:
    """Load config from TOML; return defaults if file missing.

    Unknown keys are silently dropped; missing keys use defaults.
    """
    if not path.exists():
        return Config()
    with path.open("rb") as f:
        data = tomllib.load(f)
    known_fields = {f.name for f in Config.__dataclass_fields__.values()}
    filtered = {k: v for k, v in data.items() if k in known_fields}
    return Config(**filtered)


def save_config(cfg: Config, path: Path) -> None:
    """Write config to TOML, creating parent dirs if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        tomli_w.dump(asdict(cfg), f)
