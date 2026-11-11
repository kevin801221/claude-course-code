#!/usr/bin/env python3
"""Exercise source hook in isolation; no user config writes or real notifications."""
import json
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    here = Path(__file__).resolve().parent
    source = (here / "source/hooks/pomodoro.sh").read_text(encoding="utf-8")
    expected = 'COUNTER_FILE="$HOME/.claude/.pomodoro-count"'
    assert source.count(expected) == 1, "Source counter path changed; inspect the test."
    with tempfile.TemporaryDirectory(prefix="student-kit-pomodoro-") as directory:
        task_dir = Path(directory)
        counter = task_dir / "counter"
        notification = task_dir / "notification.log"
        # Test-only path injection preserves the distributed original source.
        isolated = source.replace(expected, "COUNTER_FILE=" + "'" + str(counter).replace("'", "'\"'\"'") + "'")
        script = task_dir / "hook.sh"
        script.write_text(isolated, encoding="utf-8")
        bin_dir = task_dir / "bin"
        bin_dir.mkdir()
        notifier = bin_dir / "terminal-notifier"
        notifier.write_text('#!/bin/bash\nprintf "%s\\n" "$*" >> "$POMODORO_TEST_LOG"\n', encoding="utf-8")
        notifier.chmod(0o700)
        env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ.get("PATH", ""), POMODORO_TEST_LOG=str(notification))
        subprocess.run(["bash", str(script)], env=env, check=True)
        assert counter.read_text().strip() == "1"
        assert not notification.exists()
        counter.write_text("49\n")
        subprocess.run(["bash", str(script)], env=env, check=True)
        assert counter.read_text().strip() == "50"
        assert "Claude 番茄鐘" in notification.read_text(encoding="utf-8")
    for settings in [here / "source/settings.json", here / "settings.project.example.json"]:
        json.loads(settings.read_text(encoding="utf-8"))
    print("PASS: count=1, count=50, notification branch")


if __name__ == "__main__":
    main()
