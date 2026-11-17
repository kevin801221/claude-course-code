# Q1．Claude Code 怎麼接上 Visio MCP，並知道該用哪個工具？

從學生 ZIP 解壓後的根目錄執行。先備好 Python 3.11 以上、[uv](https://docs.astral.sh/uv/getting-started/installation/) 和可登入使用的 Claude Code。首次同步會下載 Python 套件。這個實作直接讀取原生 `.vsdx` 檔，可在沒有桌面 Visio 的電腦操作。

## 1．在有設定檔的地方啟動

```sh
cd realtek/cases/visio-mcp
uv sync --locked
claude
```

首次啟動時，依提示信任本專案，允許 `visio-lab`。在 Claude Code 對話內輸入 `/mcp`，確認清單裡的 `visio-lab` 已連線。若顯示 pending approval，回到這個資料夾執行互動版 `claude` 完成核准。在終端機執行 `claude mcp get visio-lab` 可以檢查它讀到的設定。

## 2．貼這段，觀察它選到什麼工具

```text
請用 visio-lab 讀取 fixtures/starter.vsdx。列出這個 Visio 頁面的名稱、各圖形的 ID 和文字，再告訴我每條箭頭從哪個 ID 指到哪個 ID。只讀取檔案。
```

[.mcp.json](.mcp.json) 讓 Claude Code 透過 stdio 啟動 `uv run --locked python server.py`。[server.py](server.py) 公開工具的名稱、說明與參數。Claude 從 `tools/list` 得到這些資訊，再用 `tools/call` 呼叫 `inspect_flowchart`，帶入 `path="fixtures/starter.vsdx"`。

**驗收**　頁面叫「申請流程」。圖形依序是 `1 填寫申請`、`2 送出申請`、`3 完成登記`。連接器 4 從 1 到 2，連接器 5 從 2 到 3。可以自己用 Visio 打開[同一份起始檔](fixtures/starter.vsdx)對照。

## 3．直接驗證 MCP 回傳值

離開 Claude Code 後，在同一個實驗資料夾執行以下命令。完成一次套件同步後，此檢查可離線執行，無須模型帳號。

```sh
uv run --locked python read_starter.py
```

可以在畫面上確認 `tools/list: inspect_flowchart required = ['path']`、三個圖形與兩條連線。若你還想測試改圖，執行 `uv run --locked python smoke_test.py`。在 [README 的選修段落](README.md#classroom-prompt) 可找到主管審核練習。要透過桌面應用程式開檔，另有選用的 `inspect_in_visio` 工具，限已安裝桌面 Visio 的 Windows。

**教材來源**　原始連線設定、程式、鎖檔、範例與測試取自講師的 [claude-course-code](https://github.com/kevin801221/claude-course-code/tree/b1c5315339f8526c07b4d10da2f86ba89f7f8371/Projects/visio-mcp-lab)，沿用 [MIT 授權](LICENSE)。本包另提供這份操作指南與 `read_starter.py`。
