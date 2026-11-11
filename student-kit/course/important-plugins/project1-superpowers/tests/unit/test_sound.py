"""Tests for pomocat.sound."""
from __future__ import annotations

from unittest.mock import MagicMock

import pomocat.sound as sound_mod
from pomocat.sound import play_alarm


class TestPlayAlarm:
    def test_non_darwin_prints_bell(self, monkeypatch, capsys):
        monkeypatch.setattr(sound_mod.sys, "platform", "linux")
        play_alarm()
        captured = capsys.readouterr()
        assert "\a" in captured.out

    def test_darwin_invokes_afplay_with_bundled_wav(self, monkeypatch):
        monkeypatch.setattr(sound_mod.sys, "platform", "darwin")
        popen = MagicMock()
        monkeypatch.setattr(sound_mod.subprocess, "Popen", popen)
        play_alarm()
        popen.assert_called_once()
        args, _kwargs = popen.call_args
        cmd = args[0]
        assert cmd[0] == "afplay"
        assert cmd[1].endswith("alarm.wav")

    def test_darwin_silences_stdout_and_stderr(self, monkeypatch):
        import subprocess
        monkeypatch.setattr(sound_mod.sys, "platform", "darwin")
        popen = MagicMock()
        monkeypatch.setattr(sound_mod.subprocess, "Popen", popen)
        play_alarm()
        _, kwargs = popen.call_args
        assert kwargs["stdout"] == subprocess.DEVNULL
        assert kwargs["stderr"] == subprocess.DEVNULL
