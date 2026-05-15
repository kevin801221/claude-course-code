"""便利貼板測試（教學沙盒，刻意留半成品）。

已有：GET /api/notes 的 smoke test。
❌ 還沒做 —— test-owner 隊友的任務：
   等 backend-owner 給 POST /api/notes 契約後，補上：
   - happy path：成功新增一張便利貼
   - edge case：空 text、缺欄位、不合法 color
   測試要 deterministic，用執行緒起一個短命 server，不打外部網路。

跑法：  uv run pytest app/tests/ -v
"""

from __future__ import annotations

import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

import sys
from pathlib import Path

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


def test_get_notes_returns_list(server):
    with urllib.request.urlopen(f"{server}/api/notes") as r:
        data = json.loads(r.read())
    assert isinstance(data, list)
    assert data and "text" in data[0]


# ❌ test-owner：在這之下補 POST /api/notes 的測試
