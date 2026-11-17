"""A1：乾淨環境、無 API key、無外部請求跑完整 Demo；不自動接受變更。"""
import contextlib
import io
import os
import socket
import unittest
from unittest import mock

from helpers import needs_cmake, read_json, tmpdir
from workshop.__main__ import main


def _no_network(*a, **k):
    raise AssertionError(f"Demo 不應發出外部請求：{a}")


@needs_cmake
class DemoTest(unittest.TestCase):
    def test_offline_demo_no_network(self):
        out = tmpdir() / "demo"
        env = {k: v for k, v in os.environ.items() if "API_KEY" not in k and "TOKEN" not in k}
        buf = io.StringIO()
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch.object(socket.socket, "connect", _no_network), \
                mock.patch.object(socket, "create_connection", _no_network), \
                contextlib.redirect_stdout(buf):
            rc = main(["demo", "--offline", "--out", str(out)])
        self.assertEqual(rc, 0, buf.getvalue())
        for f in ("b/research-report.md", "b/handoff-a.md", "b/evidence.json",
                  "c/standalone/versions/v1/prd.md", "c/linked/versions/v1/prd.md", "c/linked/versions/v1/sow.md",
                  "c/linked/versions/v1/traceability.md", "c/linked/changes/CR-001.md", "c/linked/review.json"):
            self.assertTrue((out / f).is_file(), f)
        self.assertEqual(read_json(out / "b/sources.json")["mode"], "offline")
        self.assertEqual(read_json(out / "c/linked/changes/CR-001.json")["status"], "proposed")
        self.assertEqual(read_json(out / "c/linked/project.json")["current_version"], "v1")
        self.assertFalse((out / "c/linked/decisions.jsonl").exists())
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["demo", "--offline", "--out", str(out)]), 2)  # 不覆蓋既有結果


if __name__ == "__main__":
    unittest.main()
