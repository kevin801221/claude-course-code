# Commands 最佳實踐

![Last Updated](https://img.shields.io/badge/Last_Updated-Nov%2004%2C%202026%2011%3A06%20AM%20PKT-white?style=flat&labelColor=555) ![Version](https://img.shields.io/badge/Claude_Code-v2.1.318-blue?style=flat&labelColor=555)<br>
[![Implemented](https://img.shields.io/badge/Implemented-2ea44f?style=flat)](../implementation/claude-commands-implementation.md)

Claude Code 命令 —— frontmatter 欄位與官方內建 slash command。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`best-practice/claude-commands.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-commands.md)

---

## Frontmatter 欄位（20 個）

| 欄位 | 型別 | 必填 | 說明 |
|-------|------|----------|-------------|
| `name` | string | 否 | 顯示在 `/` 選單中的命令名稱。省略時以目錄名為準 |
| `description` | string | 建議填 | 這個命令做什麼。顯示在自動完成中，也是 Claude 自動探索的依據。省略時取 markdown 內容的第一個非空行。把關鍵使用情境寫在最前面：`description` 與 `when_to_use` 合併後的文字在清單中會被截斷在 1,536 字元 |
| `when_to_use` | string | 否 | 補充說明 Claude 何時該呼叫此 skill —— 觸發語句或範例請求。在清單中附加於 `description` 之後，計入 1,536 字元上限 |
| `argument-hint` | string | 否 | 自動完成時顯示的提示，標示預期的引數（例如 `[issue-number]`、`[filename] [format]`） |
| `arguments` | string/list | 否 | 具名位置引數，供命令內容中的 `$name` 代換使用。接受空白分隔字串或 YAML 清單 —— 名稱依序對應引數位置 |
| `disable-model-invocation` | boolean | 否 | 設為 `true` 可防止 Claude 自動呼叫此命令。同時也會阻止它被預載進子代理，以及在 session 範圍的排程任務以此 skill 為 prompt 觸發時執行。預設：`false` |
| `user-invocable` | boolean | 否 | 設為 `false` 可從 `/` 選單隱藏 —— 命令變成純背景知識。Claude Code 也不會在你輸入 `/name` 時執行它。預設：`true` |
| `paths` | string/list | 否 | 限制此 skill 何時啟用的 glob 樣式。接受逗號分隔字串或 YAML 清單。設定後，Claude 只在處理符合樣式的檔案時自動載入此 skill。樣式相對於 Claude 的當前工作目錄，該目錄外的檔案不會匹配 |
| `allowed-tools` | string/list | 否 | 在呼叫此 skill 的那一回合中，Claude 不需詢問權限即可使用的工具。你送出下一則訊息時授權即解除。接受空白或逗號分隔字串，或 YAML 清單 |
| `disallowed-tools` | string/list | 否 | 此命令作用期間從 Claude 可用工具池中移除的工具。用於絕不該呼叫某些工具的自主 skill。接受空白或逗號分隔字串，或 YAML 清單。你送出下一則訊息時限制即解除。只要還有其他工具存在，就無法移除 `EndConversation` |
| `model` | string | 否 | 此命令執行時使用的模型（例如 `haiku`、`sonnet`、`opus`）。僅套用於當前回合；下一則訊息會回到 session 模型。接受與 `/model` 相同的值，或用 `inherit` 保持當前模型。若該值被你組織的 `availableModels` 白名單排除，或在 auto 模式下不支援，則會被忽略，session 維持當前模型 |
| `effort` | string | 否 | 此 skill 作用時的努力等級。會覆寫 session 的努力等級。選項：`low`、`medium`、`high`、`xhigh`、`max`；可用等級取決於模型 |
| `context` | string | 否 | 設為 `fork` 可在 fork 出的子代理脈絡中執行 |
| `agent` | string | 否 | 設定 `context: fork` 時使用的子代理類型（預設：`general-purpose`） |
| `background` | boolean | 否 | 僅在 `context: fork` 時生效。設為 `false` 可在呼叫此 skill 的那一回合等待 fork 子代理的結果，而非丟到背景執行。預設：`true`。需要 Claude Code v2.1.218 或更新版本 |
| `shell` | string | 否 | `` !`command` `` 區塊使用的 shell —— 接受 `bash`（預設）或 `powershell`。PowerShell 工具在沒有 Git Bash 的 Windows 上預設開啟，在有 Git Bash 的 Windows 上則對 claude.ai 與 Console 帳號預設開啟；在 Bedrock、Agent Platform、Foundry，以及 macOS、Linux、WSL 上需要 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` |
| `metadata` | object | 否 | 自由格式 YAML map，放你自己的鍵值資料，由你自己的工具從 `SKILL.md` 讀取。Claude Code 不會對內容做任何事，非 map 的值會被丟棄。不要重用 `paths` 這類保留欄位名當鍵 |
| `license` | string | 否 | 依 [Agent Skills](https://agentskills.io) 規格，此 skill 適用的授權條款。Claude Code 接受此欄位但不會據此行動 |
| `compatibility` | string | 否 | 依 [Agent Skills](https://agentskills.io) 規格，此 skill 的環境需求，例如適用產品或系統先決條件。最多 500 字元。Claude Code 接受此欄位但不會據此行動 |
| `hooks` | object | 否 | Claude Code 在此 skill 被呼叫時註冊的 hook，並在 session 剩餘時間持續生效 |

---

## ![Official](../%21/tags/official.svg) **（96 個）**

| # | 命令 | 標籤 | 說明 |
|---|---------|-----|-------------|
| 1 | `/design consent`、`/design revoke` | ![Auth](https://img.shields.io/badge/Auth-2980B9?style=flat) | 授予 Claude 存取 Claude Design（claude.ai/design）的權限，或撤銷。當 Claude 的回覆要你執行 `/design consent` 時，請自己在 Claude Code 提示字元輸入 |
| 2 | `/design-login` | ![Auth](https://img.shields.io/badge/Auth-2980B9?style=flat) | 用你的 claude.ai 帳號授權 `/design-sync` 存取 design system。當 `/design-sync` 或 `/design consent` 要你登入時就用 `/design-login`。此登入是針對 claude.ai/design 的獨立版 Claude Design 站點，該站將於 2026 年 12 月 14 日前關閉；參見[從獨立版 Claude Design 遷移到 Claude](https://support.claude.com/en/articles/17440474-migrate-from-standalone-claude-design-to-claude) |
| 3 | `/login` | ![Auth](https://img.shields.io/badge/Auth-2980B9?style=flat) | 登入你的 Anthropic 帳號 |
| 4 | `/logout` | ![Auth](https://img.shields.io/badge/Auth-2980B9?style=flat) | 登出你的 Anthropic 帳號 |
| 5 | `/setup-bedrock` | ![Auth](https://img.shields.io/badge/Auth-2980B9?style=flat) | 透過互動精靈設定 Amazon Bedrock 的驗證、區域與模型鎖定。在設定 `CLAUDE_CODE_USE_BEDROCK=1` 之前不會出現在命令選單，需完整輸入。首次使用 Bedrock 的人也可從登入畫面進入此精靈 |
| 6 | `/setup-vertex` | ![Auth](https://img.shields.io/badge/Auth-2980B9?style=flat) | 透過互動精靈設定 Google Cloud Agent Platform 的驗證、專案、區域與模型鎖定。在設定 `CLAUDE_CODE_USE_VERTEX=1` 之前不會出現在命令選單，需完整輸入。首次使用者也可從登入畫面進入此精靈 |
| 7 | `/upgrade` | ![Auth](https://img.shields.io/badge/Auth-2980B9?style=flat) | 開啟升級頁面以切換到更高方案層級。瀏覽器無法開啟時，會顯示登入提示而不印出網址 |
| 8 | `/auto-mode-setup` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 從你的專案與近期 session 草擬 `autoMode.environment` 項目，接著檢視草稿並存進你的使用者設定。Pro、Max、Ultra 或 Team 方案需要 Claude Code v2.1.228 或更新，原生 Windows 上需 v2.1.233 或更新。Enterprise 方案或使用 Claude Console API key 時需要 v2.1.283 或更新。若找不到此命令，請參見 `/auto-mode-setup` 回傳「Unknown command」的疑難排解頁 |
| 9 | `/color [color\|default]` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 設定當前 session 的提示列顏色。可用顏色：`red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink`、`cyan`。用 `default` 重設。不帶引數執行則隨機挑一個顏色。Remote Control 連線時，顏色會同步到 claude.ai/code。非互動模式（`-p`）也可用 |
| 10 | `/config [key=value ...]` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 開啟設定介面以調整主題、模型、輸出風格與其他偏好。傳入一組或多組 `key=value` 可直接設定而不開介面，例如 `/config theme=dark`、`/config model=sonnet`、`/config thinking=false`。`key=value` 形式無法開啟需要你在面板中確認的設定（例如 `autoContinueAtUsageLimit`），但可以關掉。非互動（`-p`）模式與透過 Remote Control 從 Claude 行動 App 也可用。執行 `/config --help` 可列出可設定的鍵。別名：`/settings` |
| 11 | `/focus` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 切換 focus 檢視，只顯示你最後一次的 prompt、一行工具呼叫摘要（含編輯 diffstat）與最終回覆。工具呼叫摘要也會統計該回合啟動的子代理數，並把已完成的背景任務通知收合成單一計數。選擇會跨 session 保留；可在設定中設 `viewMode` 覆寫。僅在全螢幕繪製模式可用。從 Remote Control 客戶端執行 `/focus [on\|off]` 可只對當前 session 開關 focus 檢視而不改變你儲存的選擇；此功能需要 Claude Code v2.1.281 或更新。VS Code 擴充套件有自己的 Focus 檢視切換，與 `viewMode` 獨立 |
| 12 | `/import [codex\|gemini\|cursor] [--dry-run] [--yes]` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 把你機器上其他 coding agent（目前支援 OpenAI Codex、Google Gemini CLI 或 Cursor）的設定匯入 Claude Code，包括指令檔、MCP server、命令、子代理與 skills。非互動模式（`-p`）下會列出找到的東西，並給你確認匯入的命令。`--dry-run` 只預覽不寫入；`--yes` 跳過互動選擇器。從 Cursor 匯入需要 v2.1.265 或更新。在 Bedrock、Agent Platform（Vertex）、Foundry、AWS 上的 Claude Platform、Claude apps gateway，或關閉 feature-flag 抓取時不可用 |
| 13 | `/keybindings` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 開啟你的鍵盤快捷鍵檔案 |
| 14 | `/output-style [style]` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 列出輸出風格或切換到某一個，例如 `/output-style concise`。需要 Claude Code v2.1.269 或更新 |
| 15 | `/permissions` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 管理工具權限的 allow、ask、deny 規則。開啟互動對話框，可依範圍檢視規則、新增或移除規則、管理工作目錄，以及檢視近期的 auto 模式拒絕紀錄。你也可以從對話框的 Auto mode 分頁檢視與編輯 auto 模式分類器規則。別名：`/allowed-tools` |
| 16 | `/powerup` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 透過附動畫示範的快速互動課程探索 Claude Code 功能 |
| 17 | `/privacy-settings` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 檢視與更新你的隱私設定。僅 Pro、Max、Ultra 方案訂閱者可用 |
| 18 | `/radio` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 在瀏覽器開啟 Claude FM lo-fi 電台。沒有瀏覽器可用時印出串流網址 |
| 19 | `/sandbox` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 切換 sandbox 模式。僅在支援的平台可用 |
| 20 | `/scroll-speed` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 互動式調整滑鼠滾輪捲動速度。僅在全螢幕繪製模式可用。JetBrains 終端機不可用 |
| 21 | `/statusline` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 設定 Claude Code 的狀態列。描述你想要什麼，或不帶引數執行以從你的 shell 提示字元自動設定 |
| 22 | `/stickers` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 訂購 Claude Code 貼紙 |
| 23 | `/terminal-setup` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 在 VS Code、Cursor、Devin Desktop、Alacritty 或 Zed 安裝 Shift+Enter 換行快捷鍵。在 Apple Terminal 則改為啟用 Option+Enter 換行並關閉提示音。在 iTerm2 則開啟剪貼簿存取讓 `/copy` 可用 |
| 24 | `/theme` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 變更色彩主題。包含淺色與深色變體、色盲友善（daltonized）主題、使用你終端機色盤的 ANSI 主題、跟隨終端機淺／深色模式的「Auto（match terminal）」選項，以及從 `~/.claude/themes/` 或外掛載入的自訂主題。選「New custom theme…」可建立自己的主題 |
| 25 | `/tui [default\|fullscreen]` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 設定終端機 UI 繪製器並以該模式重啟，對話內容完整保留。`fullscreen` 啟用無閃爍的 alt-screen 繪製器。不帶引數時印出當前繪製器 |
| 26 | `/voice [hold\|tap\|off]` | ![Config](https://img.shields.io/badge/Config-F39C12?style=flat) | 切換語音聽寫，或以特定模式啟用。需要 Claude.ai 帳號 |
| 27 | `/autocompact [auto\|<tokens>]` | ![Context](https://img.shields.io/badge/Context-8E44AD?style=flat) | 設定自動壓縮視窗：脈絡視窗要滿到什麼程度 Claude Code 才自動壓縮。傳入大小（例如 `500k`），或用 `auto` 回到為你的模型調校過的預設值。Claude Code 會把值存進使用者設定並套用到當前 session。不帶引數時開啟顯示當前視窗的對話框。需要 Claude Code v2.1.221 或更新 |
| 28 | `/context [all]` | ![Context](https://img.shields.io/badge/Context-8E44AD?style=flat) | 以彩色格狀圖視覺化當前脈絡使用量。顯示針對高脈絡消耗工具、記憶膨脹的最佳化建議與容量警告。當對話超出脈絡視窗時，輸出會包含警告，顯示你超出多少以及哪個命令能釋放空間。全螢幕模式下 `/context` 會收合逐項細目以保持格狀圖可見。傳 `all` 可展開 |
| 29 | `/cost` | ![Context](https://img.shields.io/badge/Context-8E44AD?style=flat) | `/usage` 的別名 |
| 30 | `/insights` | ![Context](https://img.shields.io/badge/Context-8E44AD?style=flat) | 產生 HTML 報告分析這台機器上的 Claude Code session，包含你在哪些專案工作、你怎麼用 Claude Code、哪裡出錯，以及值得試的功能。雲端 session 不可用 |
| 31 | `/rate-limit-options` | ![Context](https://img.shields.io/badge/Context-8E44AD?style=flat) | 當 claude.ai 用量上限擋住請求時，顯示可以繼續工作的方式：等待並在上限重設後自動繼續、加購用量額度，或升級方案。你在自己的終端機碰到上限時，Claude Code 也可能自行開啟此選單。需要 claude.ai 訂閱。等待並繼續的選項需要 Claude Code v2.1.234 或更新 |
| 32 | `/stats` | ![Context](https://img.shields.io/badge/Context-8E44AD?style=flat) | `/usage` 的別名。開在 Stats 分頁 |
| 33 | `/status` | ![Context](https://img.shields.io/badge/Context-8E44AD?style=flat) | 開啟設定介面的 Status 分頁，顯示版本、模型、帳號與連線狀態。背景 session 中的 `Session kind` 欄會依是否有終端機附掛而顯示 `background job · attached` 或 `background job · unattended`，其他 session 則顯示 `interactive`。v2.1.221 之前 `/status` 不顯示此欄。Claude 正在回應時也能執行 |
| 34 | `/usage` | ![Context](https://img.shields.io/badge/Context-8E44AD?style=flat) | 顯示 session 成本、方案用量上限與活動統計。Pro、Max、Ultra、Team 或 Enterprise 方案會包含哪些項目計入方案上限的細目。`/cost` 與 `/stats` 是別名 |
| 35 | `/usage-credits` | ![Context](https://img.shields.io/badge/Context-8E44AD?style=flat) | 碰到上限時設定用量額度，或向管理員申請。在瀏覽器開啟你的用量額度帳務設定；但沒有帳務權限的 Team 與 Enterprise 成員則改為從 CLI 送出用量額度申請給管理員，送出前會在對話框確認此申請會通知管理員。沒有瀏覽器可開時（例如透過 SSH）會印出網址（需要 Claude Code v2.1.205 或更新）。舊名 `/extra-usage` |
| 36 | `/bug [report]` | ![Debug](https://img.shields.io/badge/Debug-E74C3C?style=flat) | 回報 bug 或分享你的對話。你可以選擇要包含多少 session 歷史，並在送出任何東西前於同意畫面確認。使用第一方連線且已登入時，報告會送到 Anthropic。在第三方供應商或沒有 Anthropic 憑證時，Claude Code 會把報告寫進 `~/.claude/feedback-bundles/` 底下的本機封存，由你自己轉送。在 VS Code 擴充套件中會開啟該擴充套件自己的回饋對話框（需要 Claude Code v2.1.229 或更新）。Claude 正在回應時執行會立刻開啟對話框。v2.1.232 之前會把命令排隊到該回合結束。v2.1.212 之前 `/bug` 與 `/share` 是 `/feedback` 的別名。別名：`/share` |
| 37 | `/feedback [report]` | ![Debug](https://img.shields.io/badge/Debug-E74C3C?style=flat) | 送出關於 Claude Code 的產品回饋。開啟與 `/bug` 相同的對話框，同意步驟、送出規則與回合中行為都相同。不帶引數時，若 session 中有 Claude 草擬的回饋，會開啟草稿佇列讓你檢視、編輯、送出或丟棄；佇列中也有在對話框撰寫新報告的選項。帶引數時直接開啟對話框 |
| 38 | `/heapdump` | ![Debug](https://img.shields.io/badge/Debug-E74C3C?style=flat) | 把 JavaScript heap 快照與記憶體細目寫到 `~/Desktop` 以診斷高記憶體用量。Linux 上沒有 Desktop 資料夾時寫到家目錄。不出現在命令選單，需完整輸入。只分享 `-diagnostics.json` 檔，因為 `.heapsnapshot` 含有你的對話與憑證。回報記憶體成長的 bug 時很有用 |
| 39 | `/help` | ![Debug](https://img.shields.io/badge/Debug-E74C3C?style=flat) | 顯示說明與可用命令 |
| 40 | `/release-notes` | ![Debug](https://img.shields.io/badge/Debug-E74C3C?style=flat) | 在互動式版本選擇器中檢視 changelog。選特定版本可看其發行說明，或選擇顯示所有版本。說明會出現在你的逐字稿中，但不會進入 Claude 看到的對話 |
| 41 | `/tasks` | ![Debug](https://img.shields.io/badge/Debug-E74C3C?style=flat) | 檢視與管理當前 session 的背景工作，包括已完成的子代理。也可用 `/bashes` |
| 42 | `/copy [N]` | ![Export](https://img.shields.io/badge/Export-7F8C8D?style=flat) | 複製最後一則助理回覆到剪貼簿。傳數字 `N` 可複製倒數第 N 則：`/copy 2` 複製倒數第二則。有程式碼區塊或引言時，會顯示互動選擇器讓你挑個別區塊或整則回覆。在選擇器中按 `w` 可把選取內容寫到檔案而非剪貼簿，透過 SSH 時很有用 |
| 43 | `/export [filename]` | ![Export](https://img.shields.io/badge/Export-7F8C8D?style=flat) | 把當前對話匯出成純文字。帶檔名時直接寫入該檔。不帶時開啟對話框讓你複製到剪貼簿或存成檔案 |
| 44 | `/agents` | ![Extensions](https://img.shields.io/badge/Extensions-16A085?style=flat) | 印出提醒，要你請 Claude 建立或管理子代理，或直接編輯 `.claude/agents/` 或 `~/.claude/agents/`。v2.1.197 及更早版本會開啟建立與管理子代理設定的互動介面 |
| 45 | `/chrome` | ![Extensions](https://img.shields.io/badge/Extensions-16A085?style=flat) | 設定 Claude in Chrome |
| 46 | `/hooks` | ![Extensions](https://img.shields.io/badge/Extensions-16A085?style=flat) | 檢視 hook 設定 |
| 47 | `/ide` | ![Extensions](https://img.shields.io/badge/Extensions-16A085?style=flat) | 管理 IDE 整合並顯示狀態 |
| 48 | `/mcp [reconnect (<server>\|all)\|enable\|disable [<server>\|all]]` | ![Extensions](https://img.shields.io/badge/Extensions-16A085?style=flat) | 管理 MCP server 連線與 OAuth 驗證。不帶引數執行會開啟互動清單，傳 `reconnect <server>` 可重連單一斷線 server，`reconnect all` 可重試每個失敗或需驗證的 server，或傳 `enable`／`disable` 加 server 名稱或 `all` 來改變連線狀態而不開對話框。非互動（`-p`）模式下不帶引數執行會印出 server 狀態的文字摘要 |
| 49 | `/plugin [subcommand]` | ![Extensions](https://img.shields.io/badge/Extensions-16A085?style=flat) | 管理 Claude Code 外掛。不帶引數執行會開啟外掛選單，或傳 `list`、`install`、`enable`、`disable` 等子命令直接執行。Claude Code 可能在安裝過程中啟用外掛；安裝摘要會告訴你它有沒有這麼做，或是否該執行 `/reload-plugins`。 |
| 50 | `/reload-plugins [--force]` | ![Extensions](https://img.shields.io/badge/Extensions-16A085?style=flat) | 重新載入所有啟用的外掛以套用待處理變更，不需重啟。回報每個重載元件的數量並標記任何載入錯誤。當重載會改變載入的 MCP 工具並使 prompt cache 失效時，命令會警告並跳過，除非你傳 `--force`。非互動模式（`-p`）、Agent SDK 與桌面 App 也可用，但那裡只對直接輸入 session 的指令生效，且不套用外掛的 MCP server 變更；需要 Claude Code v2.1.260 或更新 |
| 51 | `/reload-skills` | ![Extensions](https://img.shields.io/badge/Extensions-16A085?style=flat) | 重新掃描 skill 與命令目錄，讓 session 期間在磁碟上新增或變更的 skill 不需重啟即可使用。回報有多少 skill 可用，以及新增或移除了多少 |
| 52 | `/skill-doctor` | ![Extensions](https://img.shields.io/badge/Extensions-16A085?style=flat) | 顯示每個 skill 佔多少脈絡成本、多常被用到，好讓你找出該關掉的 skill。需要 Claude Code v2.1.252 或更新，以及 feature-flag 抓取 |
| 53 | `/skills` | ![Extensions](https://img.shields.io/badge/Extensions-16A085?style=flat) | 列出可用 skill。輸入可依名稱、說明或來源過濾。按 `t` 依 token 數排序。按 `Space` 或 `Enter` 可循環切換該 skill 對 Claude 與 `/` 選單的可見性；`Esc` 儲存並關閉。外掛 skill、設了 `disable-model-invocation: true` 的 skill，以及有受管 `skillOverrides` 項目或使用 `--settings` 旗標的 skill 無法切換 |
| 54 | `/memory` | ![Memory](https://img.shields.io/badge/Memory-3498DB?style=flat) | 編輯 `CLAUDE.md` 檔案、啟用或停用自動記憶，以及檢視自動記憶項目 |
| 55 | `/advisor [model\|off]` | ![Model](https://img.shields.io/badge/Model-E67E22?style=flat) | 啟用或停用 advisor 工具，它會在任務的關鍵時刻諮詢第二個模型取得建議。接受模型名稱（`fable`、`opus`、`sonnet`）或完整 model ID（`fable` 需要 Fable 存取權）；不帶引數時開啟選擇器。在沒有互動終端機的 session 或透過 Remote Control 時，不帶引數會以文字印出當前 advisor 而非開啟選擇器；需要 v2.1.260。用 `off` 停用 |
| 56 | `/effort [level\|auto\|status\|ultracode [on\|off]]` | ![Model](https://img.shields.io/badge/Model-E67E22?style=flat) | 設定努力等級：`low` 到 `xhigh`、`max` 或 `auto`；`status` 印出當前值。`ultracode` 或 `ultracode on` 為該 session 開啟 ultracode，`ultracode off` 關閉；`ultracode` 鍵會保留。`max` 僅限該 session。`on` 與 `off` 引數需要 Claude Code v2.1.284 或更新。若你在 Claude 工作時執行 `/effort`，請留意新等級何時生效。v2.1.205 或更新版本在 `-p` 中可用 |
| 57 | `/fast [on\|off]` | ![Model](https://img.shields.io/badge/Model-E67E22?style=flat) | 開關 fast 模式。Claude 正在回應時執行，Claude Code 會立即切換而不等該回合結束，不過正在跑的回合仍以原速度完成。v2.1.242 之前，Claude Code 會依 feature flag 決定是在回合中執行還是排隊到回合結束，且在不抓取 feature flag 的 session 中一律排隊。在 `-p` 非互動模式中的可用性有限。 |
| 58 | `/model [model]` | ![Model](https://img.shields.io/badge/Model-E67E22?style=flat) | 切換 AI 模型並存為新 session 的預設。支援的模型可用左右方向鍵調整努力等級。不帶引數時開啟選擇器；在某列按 `s` 可只對當前 session 切換。確認切換後，Claude Code 會立即套用而不等當前回覆結束。v2.1.242 之前可能會等待。非互動模式（`-p`）帶模型引數也可用，該情況下僅套用於當前 session 且不會存為預設；需要 Claude Code v2.1.205 或更新 |
| 59 | `/passes` | ![Model](https://img.shields.io/badge/Model-E67E22?style=flat) | 分享一週免費 Claude Code 給朋友。只有帳號符合資格時才看得到 |
| 60 | `/plan [description]` | ![Model](https://img.shields.io/badge/Model-E67E22?style=flat) | 直接從提示字元進入 plan 模式。可傳入描述以進入 plan 模式並立刻開始該任務，例如 `/plan fix the auth bug` |
| 61 | `/add-dir <path>` | ![Project](https://img.shields.io/badge/Project-27AE60?style=flat) | 為當前 session 新增一個可存取檔案的工作目錄。輸入部分路徑可看到符合的目錄建議；按 `Tab` 接受。多數 `.claude/` 設定不會從新增的目錄中被探索到。多數網路路徑（例如 `\\server\share`）無法新增。成功新增後會執行你的 `DirectoryAdded` hook。Claude 正在回應時執行，Claude Code 會立刻請你確認該目錄；確認後，Claude 在同一回合的下一個工具呼叫就能存取它。v2.1.234 之前會把命令排隊到回合結束 |
| 62 | `/diff` | ![Project](https://img.shields.io/badge/Project-27AE60?style=flat) | 檢視你工作樹中的變更，包含 Claude 目前為止所做的編輯 |
| 63 | `/init` | ![Project](https://img.shields.io/badge/Project-27AE60?style=flat) | 用 `CLAUDE.md` 指南初始化專案。設定 `CLAUDE_CODE_NEW_INIT=1` 可進入互動流程，另外會帶你走過 skills、hooks 與個人記憶檔。若 `/init` 發現 OpenAI Codex 或 Google Gemini CLI 的設定，會提議用 `/import` 一併帶過來 |
| 64 | `/review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [--max-findings n\|all\|default] [pr#\|branch\|path]` | ![Project](https://img.shields.io/badge/Project-27AE60?style=flat) | `/code-review` 的別名：檢視當前 diff，或你傳入的 PR 編號、分支或路徑，例如 `/review 1234`，接受相同的努力等級與旗標。不給等級時，review 會沿用你上次輸入的 `low` 到 `max` 等級；確切規則見「用 `/code-review` 在本機檢視」。要做雲端深度檢視請用 `/code-review ultra`。v2.1.223 之前 `/review` 是獨立命令，對指定編號的 GitHub pull request 做單趟唯讀檢視，不帶引數時會列出開啟中的 PR 讓你挑；v2.1.186 到 v2.1.201 期間，它跑的是與 `/code-review medium` 相同的多代理引擎 |
| 65 | `/security-review` | ![Project](https://img.shields.io/badge/Project-27AE60?style=flat) | 分析當前分支待處理變更的安全漏洞。檢視你的分支與 origin 預設分支之間的 diff，找出注入、驗證問題與資料外洩等風險。需要 `origin` remote |
| 66 | `/team-onboarding` | ![Project](https://img.shields.io/badge/Project-27AE60?style=flat) | 從你的 Claude Code 使用歷史產生團隊上手指南。Claude 會分析你過去 30 天的 session、命令與 MCP server 使用狀況，產出一份 markdown 指南，隊友可當第一則訊息貼上以快速完成設定。Team 與 Enterprise 方案的 claude.ai 訂閱者還會拿到一個分享連結，隊友可直接在 Claude Code 開啟 |
| 67 | `/ultrareview [PR or branch]` | ![Project](https://img.shields.io/badge/Project-27AE60?style=flat) | 在雲端沙箱中執行深度、多代理的程式碼檢視。傳 PR 參照可檢視該 pull request，或傳基底分支／commit 以改變比較基準。建議的呼叫方式是 `/code-review ultra`，`/ultrareview` 是別名。Pro、Max、Ultra 含 3 次免費執行，之後需要用量額度 |
| 68 | `/autofix-pr [prompt]` | ![Remote](https://img.shields.io/badge/Remote-5D6D7E?style=flat) | 產生一個雲端 session，監看當前分支的 PR，並在 CI 失敗或審查者留言時推送修正。用 `gh pr view` 從你簽出的分支偵測開啟中的 PR；要監看別的 PR 請先簽出該分支。預設會要求雲端 session 修掉每個 CI 失敗與審查留言；傳 prompt 可給不同指示，例如 `/autofix-pr only fix lint and type errors`。需要 `gh` CLI 與雲端 session 存取權 |
| 69 | `/desktop` | ![Remote](https://img.shields.io/badge/Remote-5D6D7E?style=flat) | 在 Claude Code 桌面 App 中接續當前 session。需要 macOS 或 x64 Windows 與 Claude 訂閱。別名：`/app` |
| 70 | `/install-github-app` | ![Remote](https://img.shields.io/badge/Remote-5D6D7E?style=flat) | 為某個 repository 安裝 Claude GitHub App，並可選擇性地設定 GitHub Actions workflow 與 secrets。會帶你選 repo 並設定整合。僅支援 github.com 的 repository。當你的 repository git remote 在 gitlab.com 或 bitbucket.org 時，命令會印出提示並結束而不開始設定。要從 GitLab pipeline 執行 Claude Code，請見 [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd.md) |
| 71 | `/install-slack-app` | ![Remote](https://img.shields.io/badge/Remote-5D6D7E?style=flat) | 安裝 Claude Slack app。開啟瀏覽器完成 OAuth 流程 |
| 72 | `/mobile` | ![Remote](https://img.shields.io/badge/Remote-5D6D7E?style=flat) | 顯示 QR code 下載 Claude 行動 App。別名：`/ios`、`/android` |
| 73 | `/remote-control` | ![Remote](https://img.shields.io/badge/Remote-5D6D7E?style=flat) | 讓這個 session 可從 claude.ai 進行 Remote Control。登出狀態下執行會印出 Remote Control 需要 claude.ai 訂閱，並告訴你如何登入。別名：`/rc` |
| 74 | `/remote-env` | ![Remote](https://img.shields.io/badge/Remote-5D6D7E?style=flat) | 為你從 CLI 啟動的雲端 session 選擇預設雲端環境 |
| 75 | `/schedule [description]` | ![Remote](https://img.shields.io/badge/Remote-5D6D7E?style=flat) | 建立、更新、列出或執行雲端排程任務（舊稱 routines）。Claude 會用對話方式帶你完成設定。也可以問某個排程任務近期的執行狀況。別名：`/routines` |
| 76 | `/teleport` | ![Remote](https://img.shields.io/badge/Remote-5D6D7E?style=flat) | 把雲端 session 拉進這個終端機。開啟選擇器，接著抓取分支與對話。也可用 `/tp`。需要 claude.ai 訂閱 |
| 77 | `/web-setup` | ![Remote](https://img.shields.io/badge/Remote-5D6D7E?style=flat) | 用你本機的 `gh` CLI 憑證連接 GitHub 帳號以使用雲端 session |
| 78 | `/artifacts` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 列出你擁有或被分享的 artifacts，接著把其中一個附掛到 session、在瀏覽器開啟，或複製其連結。在 artifacts 可用的環境可用 |
| 79 | `/background [prompt]` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 把當前 session 卸離成背景代理執行，釋放這個終端機。傳 prompt 可在卸離前再送一個指示。用 `claude agents` 監看該 session。若要在這個 session 繼續跑的同時把對話複製到新的背景 session，請用 `/fork`。別名：`/bg` |
| 80 | `/branch [name]` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 在當前這點建立對話的分支，讓你能嘗試不同方向而不失去原本的對話。會把你切換進分支並保留原對話，你可用 `/resume` 回去。若想把副本當成獨立背景 session 執行而不切換進去，請用 `/fork`；若想把支線任務交給會回報進這個對話的子代理，請用 `/subtask` |
| 81 | `/btw [question]` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 針對當前 session 問個支線問題，不會加進對話。不帶問題時，Claude Code 會顯示你最近的支線問題，讓你瀏覽先前的答案；若你還沒問過，會印出用法說明 |
| 82 | `/cd <path>` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 把這個 session 移到新的工作目錄，保留對話。輸入部分路徑可看到符合的目錄建議；按 `Tab` 接受。關於 Claude Code 會從新目錄套用什麼、以及 `/cd` 與 `/add-dir` 的差異，請見權限指南 |
| 83 | `/clear [name]` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 以空白脈絡開始新對話。傳名稱可為前一個對話在 `/resume` 選擇器中貼標籤。若想在同一對話中釋放脈絡，請改用 `/compact`。用 `/resume` 可回復前一個對話，或在同一個 Claude Code 行程中從 rewind 選單的「previous session」項目還原。別名：`/reset`、`/new` |
| 84 | `/compact [instructions]` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 透過摘要目前為止的對話來釋放脈絡。可選擇性傳入摘要的聚焦指示 |
| 85 | `/exit` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 離開 CLI。在附掛的背景 session 中，這會卸離而 session 繼續執行。別名：`/quit` |
| 86 | `/fork [prompt]` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 把當前對話複製到新的背景 session，你繼續在這裡工作。傳 prompt 則副本立刻開始處理；不傳則它會在 agent 檢視中等待第一個 prompt。除非副本是就地編輯，否則 Claude Code 會指示它在改動程式碼前先建立自己的 worktree；此隔離指示需要 Claude Code v2.1.221 或更新。若想把支線任務交給結果會回到這個對話的子代理，請用 `/subtask`；若想自己切換進副本，請用 `/branch`。關閉 agent 檢視時，`/fork` 改為產生 fork 子代理 |
| 87 | `/goal [condition\|clear]` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 設定目標 —— Claude 會跨回合持續工作直到條件滿足。不帶引數時顯示當前或最近達成的目標。`clear`、`stop`、`off`、`reset`、`none` 或 `cancel` 可提前移除進行中的目標 |
| 88 | `/list-agents` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 列出 Claude 可傳訊的子代理、agent team 隊友與其他 Claude Code session，並標示各自該用的名稱。也可用 `/peers`。需要 Claude Code v2.1.224 或更新；更早版本會回報 `Unknown command: /list-agents`。隊友列與顯示這個 session 自身名稱的第一行需要 v2.1.239 或更新。僅在跨 session 傳訊啟用時可用 |
| 89 | `/recap` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 隨時產生當前 session 的一行摘要 |
| 90 | `/rename [name]` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 重新命名當前 session 並在提示列顯示名稱。不帶名稱時從對話歷史自動產生。非互動模式（`-p`）也可用。Claude Code 會把新名稱中的控制字元與不可見字元換成空白，並把名稱截斷在 200 字元（需要 Claude Code v2.1.221 或更新）。若移除不可見字元後名稱為空，Claude Code 會以 `That name is empty once invisible characters are removed. Usage: /rename <name>` 拒絕 |
| 91 | `/restart` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 重啟 Claude Code 並接續這個 session，以套用已安裝的更新。更新安裝完畢後頁尾提示時執行。需要 Pro、Max 或 Ultra 方案，以及 macOS 或 Linux 上的原生安裝（不含 WSL）。需要 Claude Code v2.1.288 或更新。別名：`/update` |
| 92 | `/resume [session]` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 依 ID 或名稱接續對話，或開啟 session 選擇器。背景 session 在選擇器中會標上 `bg`。從選擇器或用 ID／名稱接續一個仍在執行的 session，會開啟該 session：你當前的對話移到背景，這個終端機附掛到執行中的那個。在空提示列按 `←` 可回到 agent 檢視，那裡也會列出你離開的對話。v2.1.285 之前，Claude Code 會拒絕並要你用 `claude attach` 開啟該 session 或先停止它。別名：`/continue` |
| 93 | `/rewind` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 把對話與／或程式碼倒回先前某一點，或從選定訊息開始做摘要。參見 checkpointing。別名：`/checkpoint`、`/undo` |
| 94 | `/stop` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 停止你附掛的背景 session，或你以 peek 回覆送達的那個；逐字稿與任何 worktree 都會保留。若只想卸離而不停止，請用 `/exit` 或按 `←` |
| 95 | `/subtask <task>` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 產生一個 fork 子代理：繼承完整對話的背景子代理，它處理任務的同時你繼續工作。它完成後結果會回到這個對話。若想改為把對話複製到獨立的背景 session，請用 `/fork`。關閉 agent 檢視時 `/subtask` 不可用，改由 `/fork` 產生 fork 子代理 |
| 96 | `/workflows` | ![Session](https://img.shields.io/badge/Session-4A90D9?style=flat) | 開啟 workflow 進度檢視，以監看、暫停、恢復或儲存執行中與已完成的 workflow |

像 `/debug` 這類內建 skill 也會出現在 slash command 選單中，但它們不是內建命令。

---

## 資料來源

- [Claude Code Commands](https://code.claude.com/docs/en/commands)
- [Claude Code Interactive Mode](https://code.claude.com/docs/en/interactive-mode)
- [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
