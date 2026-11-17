# 把 Claude Code 接上 Visio MCP，讀出第一張圖

這個學生 repo 自帶一個名為 `visio-lab` 的 MCP 伺服器。連線成功後，在 Claude Code 貼一句話，請它呼叫工具讀取現有的 Visio 檔案，回報頁名、圖形與箭頭。這個讀檔示範可在 macOS、Windows 或 Linux 執行，無須安裝桌面版 Visio。

<a id="connect-visio"></a>

## 1. 連上這個專案的 MCP

準備好已登入的 Claude Code 和 [uv](https://docs.astral.sh/uv/getting-started/installation/)。第一次下載教材，在終端機執行以下兩行。已經下載的同學可直接開啟學生 repo 根目錄。

```sh
git clone https://github.com/kevin801221/claude-course-code.git
cd claude-course-code
```

接著在同一個終端機執行以下三行。

```sh
cd Projects/visio-mcp-lab
uv sync --locked
claude
```

第一次開啟時，確認專案的 MCP 設定並允許啟用。在 Claude Code 輸入 `/mcp`，找到 **visio-lab**，確認它已連線。如果清單中找不到，先確認你是從 `Projects/visio-mcp-lab` 啟動，以及在終端機能執行 `uv --version`。

**Claude 怎麼知道有什麼工具？** 專案的 [.mcp.json](.mcp.json) 告訴 Claude Code 用 `uv run --locked python server.py` 啟動本機伺服器，並透過標準輸入／輸出（stdio）溝通。連線後，Claude Code 用 MCP 的 `tools/list` 取得每個工具的名稱、用途與參數規格。以 [server.py](server.py) 登記的 `inspect_flowchart` 為例，`path` 是必填的檔案路徑，`page_name` 是選填的頁名。當你請它讀圖，Claude 就能依這份規格呼叫工具，由伺服器開啟檔案並傳回結果。

<a id="read-visio-prompt"></a>

## 2. 貼一句話，驗證真的讀到 Visio 檔

```text
請用 visio-lab 的 inspect_flowchart 讀取 fixtures/starter.vsdx，列出頁名、每個圖形的 ID 和文字，以及每一條箭頭從哪個 ID 指到哪個 ID。
```

在對話中查看工具呼叫，確認輸入有 `path: "fixtures/starter.vsdx"`。對照[課堂起始圖](fixtures/starter.vsdx)，工具應回傳這些資料：

| 回傳欄位 | 起始檔的內容 |
| --- | --- |
| `pages` 與 `page` | 頁面清單只有「申請流程」，這次讀取的頁面也是「申請流程」 |
| `nodes` | ID 1「填寫申請」、ID 2「送出申請」、ID 3「完成登記」 |
| `edges` | 連線 ID 4 從 1 指到 2，連線 ID 5 從 2 指到 3 |

**想直接連 Windows 桌面 Visio？** 在已安裝並啟用 Microsoft Visio 的 Windows 電腦，可貼「請用 `inspect_in_visio` 開啟 `fixtures/starter.vsdx`，列出 Visio 讀到的圖形與連接端點」。這個工具會另開一個 Visio 程序，唯讀開檔後查詢桌面應用程式；前一個 `inspect_flowchart` 則直接讀取 `.vsdx` 檔案。

<a id="classroom-prompt"></a>

## 選修：連線後，再試著修改流程圖

如果還想體驗寫入工具，可將下列 prompt 貼進同一個對話。

```text
請只用 visio-lab 的 MCP 工具修改這份現有圖，不要用 Bash 或重新畫一份。
先用 inspect_flowchart 讀 fixtures/starter.vsdx，找出「送出申請」和「完成登記」的頁名、圖形 ID 和原有連線。
用 add_manager_review 在兩者之間加「主管審核」：通過才到「完成登記」，退回就到「補件」，補件後重新送回「主管審核」。
保留「填寫申請 → 送出申請」，另存 output/reviewed.vsdx。
最後用 verify_manager_review 重讀輸出，列出通過及退回兩條路，附上輸出路徑和驗證結果。
```

### 驗收改圖結果

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
