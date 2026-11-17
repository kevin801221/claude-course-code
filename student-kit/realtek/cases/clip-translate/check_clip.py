"""Exercise the lecturer's real polling script using a temporary clipboard and a fixed translation."""
import os
from pathlib import Path
import shutil
import signal
import subprocess
from tempfile import TemporaryDirectory


def check_clip():
    zsh = shutil.which("zsh")
    if not zsh:
        raise SystemExit("This exercise needs zsh. On Windows, use WSL with zsh for the offline check.")
    script = Path(__file__).with_name("clip-translate.sh").resolve()
    source = "Please restart the application after the update."
    translation = "更新後請重新啟動應用程式。"
    # Each tick is one pass through the unmodified script. The fourth ends this finite test.
    tick = """
n=$(cat tick)
n=$((n + 1))
printf '%s' "$n" > tick
case "$n" in
  1) printf '%s' Retry > clipboard ;;
  2) printf '%s' "$SOURCE_SENTENCE" > clipboard ;;
  4) kill -TERM "$PPID" ;;
esac
"""
    shims = {
        "sleep": tick,
        "pbpaste": "cat clipboard",
        "pbcopy": "cat > clipboard",
        "osascript": 'printf "%s\\n" "$*" >> notifications',
        "claude": 'cat >> requests; printf "%s" "$FIXED_TRANSLATION"',
    }
    with TemporaryDirectory() as scratch:
        directory = Path(scratch).resolve()
        for name, content in shims.items():
            shim = directory / name
            shim.write_text("#!/bin/sh\n" + content + "\n", encoding="utf-8")
            shim.chmod(0o755)
        (directory / "tick").write_text("0")
        (directory / "clipboard").write_text("Ready")
        run = subprocess.run(
            [zsh, "-f", str(script)], cwd=directory,
            env={**os.environ, "PATH": str(directory) + os.pathsep + os.environ["PATH"],
                 "SOURCE_SENTENCE": source, "FIXED_TRANSLATION": translation},
            timeout=10, check=False,
        )
        if run.returncode != -signal.SIGTERM or (directory / "tick").read_text() != "4":
            raise SystemExit("Polling script did not complete the four controlled ticks.")
        if (directory / "requests").read_text(encoding="utf-8") != source + "\n":
            raise SystemExit("Expected just one translation request, containing the long sentence.")
        if (directory / "clipboard").read_text(encoding="utf-8") != translation:
            raise SystemExit("Expected the fixture translation in the temporary clipboard.")
        alerts = (directory / "notifications").read_text(encoding="utf-8").splitlines()
        if len(alerts) != 2 or "翻譯中" not in alerts[0] or "翻好了" not in alerts[1]:
            raise SystemExit("Expected one start and one completion notification.")
    print("PASS: Retry skipped, one request, clipboard updated, no self-translation.")


if __name__ == "__main__":
    check_clip()
