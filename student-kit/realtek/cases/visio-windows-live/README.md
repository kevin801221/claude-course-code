# 讓 Claude Code 在 Windows 的 Visio 視窗畫圖

把 Claude Code 放左邊、Visio 放右邊。你會看到三個方塊逐一出現、填上文字，最後接起「Claude Code → MCP Server → Visio」。動畫約第 52 秒可以看到左邊呼叫 `add_text`，右邊的方塊出現文字。[作者的雙畫面 GIF](https://github.com/GongRzhe/Office-Visio-MCP-Server#example)

## 1．確認桌面版 Visio 可以自動化

準備 Windows、已安裝且完成啟用的 Microsoft Visio 桌面版、可登入的 Claude Code 和 [uv](https://docs.astral.sh/uv/getting-started/installation/)。先手動啟動 Visio 一次，完成首次登入或授權畫面。第一次安裝套件需要連網。

[下載 Windows 即時 Visio 練習 ZIP](https://raw.githubusercontent.com/kevin801221/claude-course-code/main/student-kit/dist/visio-windows-live.zip)。完整學生包請開啟 `realtek/cases/visio-windows-live/`；獨立下載請開啟解壓後的 `visio-windows-live/`。在有 [.mcp.json](.mcp.json) 的這個資料夾開 PowerShell，依序執行：

~~~powershell
uv sync --locked --python 3.12
uv run --locked python live_visio.py --preflight
uv run --locked python smoke.py --list-only
~~~

第二行會短暫開啟一個獨立的 Visio 視窗，讀取其版本後關閉。看到 `Visio desktop COM OK` 代表桌面自動化已連通。第三行會用專案設定與伺服器交換 MCP 訊息，看到 `PASS tools/list` 和七個工具名稱代表工具探索成功。也可用 [setup.ps1](setup.ps1) 一次執行安裝、上述檢查和提示產生。

## 2．讓 Claude Code 連線，貼上三段提示

~~~powershell
uv run --locked python live_visio.py --prompts
claude
~~~

第一行會印出**三段可以直接貼的中文 prompt**，第一段帶有這次要建立的完整檔案路徑。每次重新產生都會換一個檔名。進入 Claude Code 後允許這個專案的 `visio-live` MCP，輸入 `/mcp` 確認已連線。回到對話，把三段 prompt **分別**貼上，等每段完成再貼下一段。

| 貼哪一段 | 左邊看什麼 | 右邊看什麼 |
| --- | --- | --- |
| ① 建立空白圖 | `create_visio_file` 的 `save_path` | 獨立的 Visio 視窗出現。用 Windows 視窗貼齊，把它放到終端機旁。 |
| ② 建立三個節點 | 每次 `add_shape` 回傳 ID，下一次 `add_text` 用同一個 ID。 | 左、中、右三個方塊分別寫上 Claude Code、MCP Server、Visio。 |
| ③ 接起流程 | `connect_shapes` 用兩個節點 ID，最後用 `list_shapes` 查圖形。 | 出現兩條動態連接線。用滑鼠拖動中間方塊，觀察兩端跟著移動。 |

這個公開伺服器對目前作用中的頁面畫圖。示範時，讓它開的獨立視窗維持在該張圖的第一頁。三段都跑完後，關閉 Claude 前先觀察畫布。上游的工具會逐步儲存，離開伺服器時會關閉其 Visio 視窗。成果在本機的 `output/`，可以重新用 Visio 開啟。

## 3．驗證結果或獨立示範

如要直接測試整條管線，在同一個資料夾執行：

~~~powershell
uv run --locked python smoke.py
~~~

它直接透過 MCP 呼叫公開工具、建立一張新圖，讀回三個節點，再關檔並從儲存的 `.vsdx` 驗證兩條連線的黏附端點。完成時印出 `PASS .vsdx: 3 named nodes, 2 glued connectors` 及完整路徑。這個指令使用本機桌面 Visio，無須呼叫模型。只想先看可用工具時可用 `--list-only`。

若 `/mcp` 找不到 `visio-live`，回到含 [.mcp.json](.mcp.json) 的資料夾，確認 `uv --version` 能執行，再重開 Claude Code。若能列出工具但無法畫圖，執行第一步的 `--preflight`，檢查目前 Windows 使用者能否啟動和使用已授權的桌面 Visio。只有瀏覽器版 Visio 的電腦無法執行 COM 畫圖。

## 用的是哪個 MCP？

這個 Windows 實作使用 GongRzhe 開源的 `office-visio-mcp-server` 1.0.1（MIT）。原作者示範 GIF 左側使用 Claude Desktop，本講義透過 Claude Code 的專案設定呼叫相同工具。本包的 [live_visio.py](live_visio.py) 將 Visio 視窗延後到第一次畫圖才開啟，並讓課堂圖使用獨立的 Visio 實例。原有跨平台 `visio-lab` 教的是讀取、修改與驗證 `.vsdx` 檔案。[公開伺服器原始碼](https://github.com/GongRzhe/Office-Visio-MCP-Server/tree/9b566078f9051028ceafe4912409bce9910943bb) · [PyPI 套件](https://pypi.org/project/office-visio-mcp-server/1.0.1/) · [授權](https://github.com/GongRzhe/Office-Visio-MCP-Server/blob/9b566078f9051028ceafe4912409bce9910943bb/LICENSE) · [Microsoft 的獨立 Visio 視窗說明](https://learn.microsoft.com/en-us/office/vba/api/visio.invisibleapp)
