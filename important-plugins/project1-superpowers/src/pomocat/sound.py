"""Alarm sound: macOS afplay + terminal bell fallback."""
from __future__ import annotations

import subprocess
import sys
from importlib.resources import as_file, files


def play_alarm() -> None:
    """Play the bundled alarm sound non-blocking.

    On macOS: shell out to `afplay` with the bundled wav.
    Elsewhere: print terminal bell `\\a`.
    """
    if sys.platform != "darwin":
        print("\a", end="", flush=True)
        return
    wav = files("pomocat.assets") / "alarm.wav"
    with as_file(wav) as path:
        subprocess.Popen(
            ["afplay", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
