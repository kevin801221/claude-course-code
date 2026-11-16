# 讓 Claude Code 替既有 Visio 流程加上主管審核

打開 [課堂起始圖](fixtures/starter.vsdx)，會看到「填寫申請 → 送出申請 → 完成登記」。現在團隊決定由主管核准。這個實驗讓 Claude Code 透過 MCP 找到既有連線、插入審核和補件節點，另存成可繼續編輯的 Visio 圖檔。

## 1. 啟動課堂 MCP

需要可使用的 Claude Code 與 [uv](https://docs.astral.sh/uv/getting-started/installation/)。在學生 repo 的根目錄開終端，依序執行：

```sh
cd Projects/visio-mcp-lab
uv sync --locked
claude
```

第一次開啟時，檢查並同意本專案的 [.mcp.json](.mcp.json)。在 Claude Code 輸入 `/mcp`，確認 **visio-lab** 已連線，然後把下一段貼到同一個對話。Windows、macOS、Linux 都可執行這三個檔案操作；Windows 桌面版 Visio 另外提供下方的應用程式驗證。

<a id="classroom-prompt"></a>

## 2. 貼給 Claude Code

```text
請只用 visio-lab 的 MCP 工具修改這份現有圖，不要用 Bash 或重新畫一份。
先用 inspect_flowchart 讀 fixtures/starter.vsdx，找出「送出申請」和「完成登記」的頁名、圖形 ID 和原有連線。
用 add_manager_review 在兩者之間加「主管審核」：通過才到「完成登記」，退回就到「補件」，補件後重新送回「主管審核」。
保留「填寫申請 → 送出申請」，另存 output/reviewed.vsdx。
最後用 verify_manager_review 重讀輸出，列出通過及退回兩條路，附上輸出路徑和驗證結果。
```

## 3. 驗收兩條路

用 Visio 開啟 `output/reviewed.vsdx`。從同一個「主管審核」節點開始，沿著每條箭頭走一遍。

可對照[這張圖的 Mermaid 原始碼](reviewed-flow.mmd)，找出哪一條箭頭會把補件送回原來的審核節點。

| 情境 | 預期路徑 |
| --- | --- |
| 通過 | 送出申請 → 主管審核 → 完成登記 |
| 退回 | 主管審核 → 補件 → 主管審核；此時仍須重新審核 |
| 舊流程 | 填寫申請仍接到送出申請；送出申請已不能直接跳到完成登記 |

用滑鼠拖動「主管審核」，查看連接器端點是否跟隨。若使用 Windows 且已安裝和啟用桌面 Visio，可再貼「請用 inspect_in_visio 開啟 output/reviewed.vsdx，列出 Visio 讀到的圖形和連接端點」。這個工具會在獨立的 Visio 程序中唯讀開檔，讀完即關閉。

## 換自己的流程圖

把測試用的 `.vsdx` 放進 `fixtures/`，在 prompt 代入檔名、頁名與兩個圖形的文字。請 Claude 先列出圖形 ID；同名時，指定要改的兩個 ID。這個範例支援與起始圖相同的結構：同一頁有兩個未旋轉的獨立頂層圖形，兩者之間有一條已黏附、無標籤的直接連接器，旁邊有空間放補件迴圈。圖形需要自帶幾何資料。若你的圖使用樣板主圖形（master）、群組或掃描影像，請先用課堂起始圖練習。

產出檔放 `output/`。重跑相同輸入與目標可重用原結果；輸出位置若已有其他內容，請換一個檔名，避免覆蓋。若 `/mcp` 沒看到伺服器，先確認終端目前位於有 `.mcp.json` 的實驗資料夾，且能執行 `uv --version`，再重新啟動 Claude Code。

## 不呼叫模型，也能測試整條 MCP 管線

在實驗目錄執行：

```sh
uv run --locked python smoke_test.py
```

測試從 [.mcp.json](.mcp.json) 啟動 stdio 伺服器，列出工具、讀起始圖、修改、重開驗證，並檢查重跑與保留原檔。正式上課的成品由上方 prompt 寫到 `output/reviewed.vsdx`。

[server.py](server.py) 定義工具；[visio_flow.py](visio_flow.py) 直接編輯 VSDX 套件中的圖形、連線與黏附端點。課堂起始圖為原創素材。

[Microsoft 的 VSDX 檔案格式說明](https://learn.microsoft.com/en-us/office/client-developer/visio/introduction-to-the-visio-file-formatvsdx) · [Claude Code 的 MCP 設定](https://code.claude.com/docs/en/mcp)
