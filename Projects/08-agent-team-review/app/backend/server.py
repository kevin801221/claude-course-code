"""Kanban 看板的後端 —— agent team 的起點骨架。

這是一個「空殼」：只有一個 health check 證明骨架活著。
真正的 Kanban API 由 backend-owner 隊友照 app/SPEC.md 蓋出來。

要做的 endpoint（契約見 app/SPEC.md）：
- GET    /api/cards        列全部卡片
- POST   /api/cards        建卡
- PATCH  /api/cards/{id}   改 status 或 title
- DELETE /api/cards/{id}   刪卡

用標準函式庫的 http.server，零依賴就能跑：
    uv run python app/backend/server.py
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# 教學用記憶體儲存（重啟就清空，不需要資料庫）。
# backend-owner：卡片就存這裡，shape 見 app/SPEC.md。
_CARDS: list[dict] = []


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 (http.server 介面)
        if self.path == "/api/health":
            self._send_json(200, {"status": "ok"})
            return
        # TODO(backend-owner): GET /api/cards —— 照 app/SPEC.md 實作
        self._send_json(404, {"error": "not found"})

    # TODO(backend-owner): do_POST / do_PATCH / do_DELETE
    #   照 app/SPEC.md 定契約 + 實作 + 驗證輸入，不要噴 stack trace。

    def log_message(self, *args) -> None:  # 安靜一點
        pass


def main(port: int = 8000) -> None:
    print(f"backend on http://localhost:{port}  (Ctrl+C 結束)")
    print("這是骨架：目前只有 GET /api/health。Kanban API 由 agent team 照 app/SPEC.md 蓋。")
    ThreadingHTTPServer(("localhost", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
