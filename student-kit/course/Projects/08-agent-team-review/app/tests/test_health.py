"""骨架 smoke test —— 驗證後端起得來。

agent team 蓋完後，test-owner 會在 app/tests/ 補上 Kanban 的完整測試
（CRUD + edge cases，契約見 app/SPEC.md）。

跑法：  uv run --with pytest pytest app/tests/ -v
"""

from __future__ import annotations

import json
import sys
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from server import Handler  # noqa: E402


@pytest.fixture()
def server():
    httpd = ThreadingHTTPServer(("localhost", 0), Handler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    yield f"http://localhost:{port}"
    httpd.shutdown()


def test_health_ok(server):
    with urllib.request.urlopen(f"{server}/api/health") as r:
        data = json.loads(r.read())
    assert data == {"status": "ok"}
