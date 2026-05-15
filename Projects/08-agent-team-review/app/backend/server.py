"""便利貼板的後端（教學沙盒，刻意留半成品）。

這是 agent team 跨層演練的起點：
- GET  /api/notes      已實作（回傳全部便利貼）
- POST /api/notes      ❌ 還沒做 —— 這是 backend-owner 隊友的任務
                          （定義契約 + 實作新增便利貼）

用標準函式庫的 http.server，不裝任何套件就能跑：
    uv run python app/backend/server.py
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# 教學用記憶體儲存（重啟就清空，不需要資料庫）
_NOTES: list[dict] = [
    {"id": 1, "text": "歡迎使用便利貼板", "color": "yellow"},
]


def _next_id() -> int:
    return max((n["id"] for n in _NOTES), default=0) + 1


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict | list) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 (http.server 介面)
        if self.path == "/api/notes":
            self._send_json(200, _NOTES)
            return
        self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        # ❌ backend-owner 隊友的任務：
        #    定義 POST /api/notes 契約並實作，務必驗證輸入。
        self._send_json(501, {"error": "POST /api/notes not implemented yet"})

    def log_message(self, *args) -> None:  # 安靜一點
        pass


def main(port: int = 8000) -> None:
    print(f"backend on http://localhost:{port}  (Ctrl+C 結束)")
    ThreadingHTTPServer(("localhost", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
