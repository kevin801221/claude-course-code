"""競爭假設 debug 演練用 sample（教學沙盒，藏了一個非顯而易見的 bug）。

回報的症狀：
    使用者連上、送出第一則訊息、收到 echo —— 但只要稍微停頓再送
    第二則，連線就被伺服器斷掉。使用者覺得「app 撐不過一則訊息」。

刻意設計：表面症狀單一，但有 4 個看起來都很可疑的獨立嫌疑點。
單一 agent 容易錨定第一個合理解釋就停手；agent team 讓多個隊友
各查一個假設、互相證偽，才會收斂到真兇。

  嫌疑 A：HEARTBEAT_TIMEOUT 太短？
  嫌疑 B：RECV_BUFFER 只有 16 bytes，長訊息被截斷？
  嫌疑 C：except socket.timeout 把「還在等下一則訊息」當成斷線？
  嫌疑 D：收到資料卻沒更新 last_seen，心跳邏輯失效？

跑法（會自己起 client 模擬真實使用節奏，不需手動連）：
    uv run python debug-sample/chat_server.py

現況：第 1 輪 OK，第 2 輪 DISCONNECTED（穩定復現）。
修好後：印出三輪 echo 並 "OK: 連線撐過三輪"。
"""

from __future__ import annotations

import socket
import threading
import time

HOST, PORT = "localhost", 0
HEARTBEAT_TIMEOUT = 2.0   # recv 輪詢間隔（多久醒來檢查一次連線活性，不是斷線門檻）
IDLE_LIMIT = 10.0         # 真正的斷線門檻：閒置超過這個秒數才視為 client 死亡
RECV_BUFFER = 16          # 嫌疑 B
USER_THINK_TIME = 3.0     # 使用者讀完 echo 再打下一則的真實停頓（> timeout）


def handle_client(conn: socket.socket) -> None:
    conn.settimeout(HEARTBEAT_TIMEOUT)
    last_seen = time.time()
    while True:
        try:
            data = conn.recv(RECV_BUFFER)
        except socket.timeout:
            # 真兇修正：recv 逾時只代表「這個輪詢窗內沒新資料」，
            # TCP 連線仍是活的。心跳逾時 != 連線斷線。
            # 只有真的閒置超過 IDLE_LIMIT 才視為 client 死亡而斷線，
            # 否則繼續等下一則訊息。
            if time.time() - last_seen > IDLE_LIMIT:
                break
            continue
        if not data:
            break
        last_seen = time.time()  # 真的收到資料才更新心跳（last_seen 此時才有意義）
        msg = data.decode("utf-8", errors="ignore")
        conn.sendall(f"echo: {msg}".encode("utf-8"))
    conn.close()


def run_server(ready: threading.Event, port_box: list[int]) -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    port_box.append(srv.getsockname()[1])
    ready.set()
    conn, _ = srv.accept()
    handle_client(conn)
    srv.close()


def main() -> None:
    ready = threading.Event()
    port_box: list[int] = []
    threading.Thread(target=run_server, args=(ready, port_box), daemon=True).start()
    ready.wait()
    port = port_box[0]

    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect((HOST, port))
    for i in range(3):
        cli.sendall(f"hello {i}".encode("utf-8"))
        try:
            reply = cli.recv(1024)
        except OSError as e:
            print(f"DISCONNECTED at round {i}: {e}")
            return
        if not reply:
            print(f"DISCONNECTED at round {i}: server closed connection")
            return
        print(reply.decode("utf-8"))
        time.sleep(USER_THINK_TIME)  # 使用者讀完訊息、想一下再回（真實節奏）
    print("OK: 連線撐過三輪")


if __name__ == "__main__":
    main()
