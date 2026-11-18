# 把 Claude Code 接上 Visio MCP，讀出第一張圖

這個學生 repo 自帶一個名為 `visio-lab` 的 MCP 伺服器。連線成功後，在 Claude Code 貼一句話，請它呼叫工具讀取現有的 Visio 檔案，回報頁名、圖形與箭頭。這個讀檔示範可在 macOS、Windows 或 Linux 執行，無須安裝桌面版 Visio。

這份文件可用來現場講解或自己操作。先用第 1、2 節連上 MCP 並讀圖，再用第 3 節看懂工具如何運作，最後用選修實作追一次修改與驗證。課堂可以安排約 15 分鐘，產出一份讀圖結果與一份通過結構驗證的 `output/reviewed.vsdx`。

**Windows 即時畫圖實作**　若要讓 Claude Code 一邊呼叫工具、一邊在桌面版 Visio 畫圖，請開啟[分割畫面操作手冊](../../student-kit/realtek/cases/visio-windows-live/README.md)。這個實作使用公開的 GongRzhe Visio MCP。

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

<a id="how-visio-mcp-works"></a>

## 3. 從你的一句話，追到實際讀寫檔案的程式

你可以先這樣向同學說明。

> 「你負責說需求，Claude 依工具清單選工具、填參數。MCP 伺服器收到呼叫後執行我們寫好的 Python 程式，再把檔案裡讀到的結果交回 Claude。」

### Phase 1｜連線後，Claude 取得工具規格

```text
.mcp.json
  → Claude Code 用 uv run --locked python server.py 啟動本機程序
  → 雙方透過 stdio 傳遞 MCP 訊息
  → Claude Code 用 tools/list 取得名稱、用途與參數規格
  → Claude 根據任務選擇工具，透過 tools/call 呼叫
```

`stdio` 是兩個程序用標準輸入／輸出交換訊息的方式。這裡的連線設定可以直接在專案檔案中找到。

```json
{
  "mcpServers": {
    "visio-lab": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--locked", "python", "server.py"]
    }
  }
}
```

工具名稱、Python 型別與函式說明會由 FastMCP 整理成 MCP 工具規格。例如 `inspect_flowchart(path: str, page_name: str | None = None)` 告訴 Claude，呼叫時要提供 `path`，也可以指定 `page_name`。實際登記方式可查看 `@mcp.tool(...)` 裝飾器。[連線設定](.mcp.json) · [工具登記程式](server.py)

### Phase 2｜一句需求，經過三層實作

```text
你說「讀取這張圖，列出圖形與箭頭」
  → Claude 從 MCP 工具清單選 inspect_flowchart，填入 path
  → server.py 檢查檔案路徑
  → visio_flow.py 開啟 VSDX 套件，定位頁面並讀取 XML
  → Python 回傳 dict，由 MCP SDK 包成工具回應
  → Claude 根據回傳的頁名、ID、文字與連線向你說明
```

| 層次 | 檔案 | 它負責的事 | 講課時可以指給同學看 |
| --- | --- | --- | --- |
| 連線 | `.mcp.json` | 指定本機啟動指令與 stdio 傳輸方式 | `command` 與 `args` 決定哪支程式被啟動 |
| 工具介面 | `server.py` | 用 FastMCP 登記工具，檢查路徑，再呼叫底層函式 | `@mcp.tool`、函式參數、`lab_file()` |
| 檔案操作 | `visio_flow.py` | 用 `zipfile` 開啟套件，用 `lxml` 讀寫指定頁的圖形與連線，驗證後輸出 | `inspect_flow()`、`add_supervisor_review()`、`verify_supervisor_review()` |

在這條 MCP 呼叫流程中，Claude 傳遞的是檔案路徑、頁名與圖形 ID，XML 操作由 Python 函式完成。要擴充一種改圖能力，就要實作對應函式，再把它登記成 Claude 可呼叫的工具。[工具介面](server.py) · [檔案操作](visio_flow.py)

`lab_file()` 把可讀取範圍限制在這個實驗目錄內，輸入須為相對的 `.vsdx` 路徑。它會解析實際路徑，檢查 `..`、絕對路徑與符號連結是否越界。寫入目的地還必須位於 `output/`，並與來源路徑不同。[路徑檢查](server.py)

### Phase 3｜四個工具各自做什麼

| 工具 | 你交給它的資料 | 它實際做的事 | 你可以核對的結果 |
| --- | --- | --- | --- |
| `inspect_flowchart` | `path`，可選的 `page_name` | 讀取指定頁的頂層圖形，以及連接器的起點與終點 | `pages`、`page`、`nodes`、`edges` |
| `add_manager_review` | `source`、`submit_id`、`complete_id`，可選的 `page_name`、`output` | 在指定的送出與完成節點之間插入主管審核及補件迴圈 | `output`、`status`、`valid`、新增節點 ID 與連線 |
| `verify_manager_review` | `path`、`submit_id`、`complete_id`，可選的 `page_name` | 重新開啟已存的檔案，檢查審核路徑、補件回路及端點黏附資料 | `valid` 與實際讀回的節點、連線 |
| `inspect_in_visio` | `path` | 在 Windows 啟動獨立的桌面 Visio，唯讀查詢圖檔 | Visio 版本、各頁圖形與連接端點 |

`add_manager_review` 對應底層的 `add_supervisor_review()`，`verify_manager_review` 對應 `verify_supervisor_review()`。工具清單使用前者的名稱，Python 程式內部使用後者的函式名稱。[四個 MCP 工具](server.py)

`inspect_in_visio` 是這個實驗中連到桌面 Visio 的工具。Python 透過 PowerShell 啟動 `Visio.InvisibleApp`，在背景建立獨立的 Visio 程序，以唯讀、停用巨集及不加入最近檔案的選項開檔。PowerShell 的 `finally` 區塊會關閉圖檔並退出該程序。執行環境需要 Windows、Windows PowerShell，以及已安裝並啟用的桌面 Visio。[Python 包裝](desktop_visio.py) · [PowerShell 與 COM 操作](inspect_in_visio.ps1)

### 一次改圖呼叫的參數長什麼樣子

先用 `inspect_flowchart` 取得頁名和 ID。課堂起始圖回傳「申請流程」，其中「送出申請」為 ID 2，「完成登記」為 ID 3。接著 Claude 可將以下參數傳給 `add_manager_review`。

```json
{
  "source": "fixtures/starter.vsdx",
  "page_name": "申請流程",
  "submit_id": 2,
  "complete_id": 3,
  "output": "output/reviewed.vsdx"
}
```

這段 JSON 是工具呼叫的參數範例，可以在 Claude Code 的工具呼叫紀錄中核對。換一張圖時，使用那張圖實際讀回的頁名與 ID。

對起始圖第一次成功修改時，回應中的重要欄位如下。完整回應還包含 `nodes` 和 `edges`。

```json
{
  "page": "申請流程",
  "status": "applied",
  "valid": true,
  "review_id": 6,
  "supplement_id": 7,
  "output": "output/reviewed.vsdx"
}
```

最後呼叫 `verify_manager_review`，把 `path` 換成 `output/reviewed.vsdx`，沿用 `page_name`、`submit_id` 與 `complete_id`，確認重新讀取的結果仍為 `valid: true`。

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

<a id="how-the-drawing-changes"></a>

## 改圖時，檔案內實際發生的六件事

`.vsdx` 採用 ZIP 套件，裡面包含頁面、圖形、關聯與其他資源。程式直接在套件中讀取 XML，寫出新套件時替換選定頁面的內容。

課堂起始圖的頁面對應 `visio/pages/page1.xml`。程式會先讀套件內的 relationship 與頁面索引，再依 `page_name` 找到真正的頁面檔案。因此，多頁圖檔要指定頁名，實際檔名可能是其他頁面。可以在 `_related()` 與 `_page()` 看這段尋找過程。[頁面定位與改圖程式](visio_flow.py)

### 1. 確認要改的是哪一條連線

檢查 `submit_id` 和 `complete_id` 指向兩個不同、未旋轉、無 master 的獨立頂層圖形，且具有程式需要的幾何資料。兩者之間必須剛好有一條從送出指向完成、已黏附且無標籤的直接連接器。通過前置檢查後，程式移除舊的直接連接器與其端點紀錄。[`_patch()`](visio_flow.py)

### 2. 找到審核與補件的位置

「主管審核」放在兩個原節點中心的中點。「補件」依原流程方向，在上下或左右的兩個候選位置中選一個。程式會檢查頁面邊界和已有節點的矩形範圍，空間不足時回報錯誤。這個配置演算法針對課堂的審核迴圈設計。[`_patch()`](visio_flow.py)

### 3. 建立四條新路徑

```text
送出申請 → 主管審核
主管審核 →〔通過〕→ 完成登記
主管審核 →〔退回〕→ 補件
補件     →〔重新送審〕→ 主管審核
```

原有的「填寫申請 → 送出申請」繼續保留。補件回到同一個審核節點，讓流程能再次判斷通過或退回。

### 4. 把箭頭端點黏到圖形上

`_port()` 在圖形上建立連接點，`_edge()` 為每條連接器寫入兩端的 `Connect` 紀錄，並在端點座標中加入公式。公式的形式如下。

```text
PAR(PNT(Sheet.<圖形 ID>!Connections.X<點位>,
        Sheet.<圖形 ID>!Connections.Y<點位>))
```

`Sheet.<圖形 ID>` 指向目標圖形，`Connections` 指向該圖形上的連接點。公式將連接點換算成頁面座標，讓 Visio 能沿著黏附關係更新箭頭端點。課堂可以用拖動圖形的動作驗收這項效果。[連接點與連線實作](visio_flow.py)

### 5. 先寫到暫存 VSDX，再重開驗證

程式在輸出目錄下建立暫存檔，只替換選定頁面的 XML，其他 ZIP 項目的內容沿用來源資料。接著重新開啟暫存 VSDX，檢查審核與補件節點、四條路徑及標籤、八個端點連結與對應公式，也確認舊的送出到完成直達路徑已移除。[`add_supervisor_review()` 與 `_report()`](visio_flow.py)

這項檢查驗證的是檔案中的流程結構與黏附資料。畫面是否好讀、拖動時箭頭如何顯示，仍可透過前面的 Visio 開檔步驟驗收。

### 6. 驗證通過，再發布正式輸出

暫存檔驗證成功後，程式用 `os.link()` 建立正式輸出。讀取來源與寫入目的地使用不同路徑。相同要求可以重跑，已有檔案的處理方式如下。

| `status` 或錯誤 | 代表什麼 |
| --- | --- |
| `applied` | 本次新增審核與補件流程，並成功建立輸出 |
| `already_applied` | 來源已含同一組有效審核流程，這次沿用它建立新的輸出 |
| `unchanged_output` | 目的地已存在，內容與本次產出相同，直接重用 |
| `Choose a new output name` | 目的地已有不同內容，請指定另一個 `output/` 檔名 |

這個發布方式也會在其他程序先建立同名檔案時進入既有檔案檢查，避免覆蓋那個程序的輸出。[發布與重跑處理](visio_flow.py)

## 換自己的流程圖

把測試用的 `.vsdx` 放進 `fixtures/`，在 prompt 代入檔名、頁名與兩個圖形的文字。請 Claude 先列出圖形 ID；同名時，指定要改的兩個 ID。這個範例支援與起始圖相同的結構：同一頁有兩個未旋轉的獨立頂層圖形，兩者之間有一條已黏附、無標籤的直接連接器，旁邊有空間放補件迴圈。圖形需要自帶幾何資料。若你的圖使用樣板主圖形（master）、群組或掃描影像，請先用課堂起始圖練習。

產出檔放 `output/`。重跑相同輸入與目標可重用原結果；輸出位置若已有其他內容，請換一個檔名，避免覆蓋。若 `/mcp` 沒看到伺服器，先確認終端目前位於有 `.mcp.json` 的實驗資料夾，且能執行 `uv --version`，再重新啟動 Claude Code。

## 不呼叫模型，也能測試整條 MCP 管線

在實驗目錄執行：

```sh
uv run --locked python smoke_test.py
```

測試從 [.mcp.json](.mcp.json) 啟動 stdio 伺服器，列出工具、讀起始圖、修改、重開驗證，並檢查重跑與保留原檔。正式上課的成品由上方 prompt 寫到 `output/reviewed.vsdx`。

## 常見卡點對照

| 看到的狀況 | 要查哪裡 | 下一步 |
| --- | --- | --- |
| `/mcp` 找不到 `visio-lab` | 啟動目錄、`.mcp.json`、`uv --version` | 在本實驗目錄重新啟動 Claude Code，確認啟用專案 MCP |
| 要求指定頁名 | `.vsdx` 有多個頁面 | 使用回應列出的頁名重新呼叫 |
| 頁名或圖形 ID 對不上 | `inspect_flowchart` 的 `page` 與 `nodes` | 以這次檔案的讀取結果填參數 |
| 無法插入主管審核 | 節點結構、直接連線和放置空間 | 先用起始圖跑通，再依「換自己的流程圖」確認輸入條件 |
| 輸出檔已存在且內容不同 | `output` 指向的檔案 | 改用例如 `output/reviewed-2.vsdx` |
| macOS 執行 `inspect_in_visio` 失敗 | 此工具需要 Windows 桌面 Visio | 用 `inspect_flowchart` 與 `verify_manager_review` 檢查檔案，桌面查詢安排在 Windows |
| 想加任意圖形或其他流程 | `server.py` 目前登記的寫入工具 | 為新的操作實作函式並登記 MCP 工具，或使用開頭連結的 Windows 即時畫圖實作 |

## 講師現場講法與驗證順序

**先講 90 秒，再帶操作。**

> 「今天想學的是，怎麼讓 Claude 使用團隊提供的工具。第一步，我們在 `.mcp.json` 寫啟動方式，Claude Code 就能啟動這個 Python 伺服器。第二步，伺服器用 FastMCP 把工具名稱、用途和參數列出來，Claude 收到這份清單後，就知道讀圖要用 `inspect_flowchart`，要傳入檔案路徑。
>
> 等你說要修改流程圖，Claude 會先讀出頁名和圖形 ID，再把這些資料交給寫入工具。實際打開 ZIP、改 XML、建立圖形與箭頭的工作，都在 `visio_flow.py` 裡。主管審核只是這個工具支援的一個操作，你可以從它看懂團隊怎麼把自己的程式能力接到 Claude。
>
> 最後一定看輸出檔和驗證結果。程式先在暫存檔檢查路徑及端點，成功才發布到 `output/`。Claude 再呼叫驗證工具重開一次，告訴你實際讀到了什麼。若要驗收桌面呈現，就用 Visio 開檔、拖動圖形，查看箭頭是否跟隨。」

| 課堂時間 | 展示內容 | 請同學找出的證據 |
| --- | --- | --- |
| 前 3 分鐘 | `.mcp.json` 與 `/mcp` | 啟動指令、伺服器名稱與連線狀態 |
| 接著 3 分鐘 | 讀圖 prompt 與工具回應 | 「申請流程」、ID 2 和 3、原連線 ID 5 |
| 接著 4 分鐘 | `server.py` 和選修改圖 prompt | 工具參數、輸出路徑、`valid: true` |
| 最後 5 分鐘 | 重讀輸出、通過／退回路徑、重跑 | 補件回到審核、相同輸出可重用，並對照原圖 |

可用同一個 prompt 重跑，觀察 `unchanged_output`。對工程同學再打開 `_page()`、`_patch()`、`_edge()` 和 `add_supervisor_review()`，逐一對應頁面選擇、位置計算、黏附端點及驗證後發布。桌面 Visio 的呈現與拖動驗收安排在具備 Windows Visio 的電腦。

`smoke_test.py` 涵蓋 stdio 連線、工具探索、讀圖、修改、結構驗證、重跑、來源與既有輸出保護，以及路徑限制。桌面 Visio 的 COM 呼叫、畫面渲染與拖動效果另以 Windows 開檔驗收。[MCP 驗證腳本](smoke_test.py)

[server.py](server.py) 定義工具；[visio_flow.py](visio_flow.py) 直接編輯 VSDX 套件中的圖形、連線與黏附端點。課堂起始圖為原創素材。

[Microsoft 的 VSDX 檔案格式說明](https://learn.microsoft.com/en-us/office/client-developer/visio/introduction-to-the-visio-file-formatvsdx) · [Claude Code 的 MCP 設定](https://code.claude.com/docs/en/mcp)

配套教材包含本目錄的 `.mcp.json`、`server.py`、`visio_flow.py`、`fixtures/starter.vsdx` 與 `smoke_test.py`。本說明於 2026-11-18 依實際程式核對。
