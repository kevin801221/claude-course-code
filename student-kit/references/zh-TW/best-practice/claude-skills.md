# Skills 最佳實踐

![Last Updated](https://img.shields.io/badge/Last_Updated-Nov%2004%2C%202026%2010%3A03%20AM%20PKT-white?style=flat&labelColor=555) ![Version](https://img.shields.io/badge/Claude_Code-v2.1.318-blue?style=flat&labelColor=555)<br>
[![Implemented](https://img.shields.io/badge/Implemented-2ea44f?style=flat)](../implementation/claude-skills-implementation.md)

Claude Code skills —— frontmatter 欄位與官方內建 skills。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`best-practice/claude-skills.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-skills.md)

---

## Frontmatter 欄位（20 個）

| 欄位 | 型別 | 必填 | 說明 |
|-------|------|----------|-------------|
| `name` | string | 否 | 顯示名稱與 `/slash-command` 識別名。省略時以目錄名為準 |
| `description` | string | 建議填 | 這個 skill 做什麼。會顯示在自動完成中，也是 Claude 自動探索的依據 |
| `when_to_use` | string | 否 | 補充說明 Claude 何時該呼叫此 skill —— 觸發語句與範例請求。會附加在 skill 清單中的 `description` 之後，計入 1,536 字元上限 |
| `argument-hint` | string | 否 | 自動完成時顯示的提示（例如 `[issue-number]`、`[filename]`） |
| `arguments` | string/list | 否 | 具名位置引數，供 skill 內容中的 `$name` 代換使用。接受空白分隔字串或 YAML 清單 —— 名稱依序對應引數位置 |
| `disable-model-invocation` | boolean | 否 | 設為 `true` 可防止 Claude 自動呼叫此 skill |
| `user-invocable` | boolean | 否 | 設為 `false` 可從 `/` 選單隱藏 —— skill 變成純背景知識，用於代理預載 |
| `allowed-tools` | string/list | 否 | 此 skill 作用時不需權限提示即可使用的工具 |
| `disallowed-tools` | string/list | 否 | skill 作用期間從 Claude 可用工具池中移除的工具（例如在背景迴圈中封鎖 `AskUserQuestion`）。接受空白／逗號分隔字串或 YAML 清單 —— 限制在下一則訊息解除 |
| `model` | string | 否 | 此 skill 執行時使用的模型（例如 `haiku`、`sonnet`、`opus`） |
| `effort` | string | 否 | 呼叫時覆寫模型的努力等級（`low`、`medium`、`high`、`xhigh`、`max`） |
| `context` | string | 否 | 設為 `fork` 可讓 skill 在隔離的子代理脈絡中執行 |
| `agent` | string | 否 | 設定 `context: fork` 時使用的子代理類型（預設：`general-purpose`） |
| `background` | boolean | 否 | 僅在 `context: fork` 時生效。設為 `false` 可在呼叫的那一回合等待 fork 子代理的結果，而非丟到背景（預設：`true`）。需要 v2.1.218+ |
| `hooks` | object | 否 | 僅作用於此 skill 的生命週期 hook |
| `paths` | string/list | 否 | 限制 skill 自動啟用時機的 glob 樣式。接受逗號分隔字串或 YAML 清單 —— Claude 只在處理符合的檔案時載入此 skill |
| `shell` | string | 否 | `` !`command` `` 區塊使用的 shell —— `bash`（預設）或 `powershell`。需要 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` |
| `metadata` | YAML map | 否 | 自由格式 YAML map，放你自己的鍵值資料（例如授權或目錄欄位），由你自己的工具從 `SKILL.md` 讀取。Claude Code 不會對內容做任何事；非 map 的值會被丟棄。不要重用 frontmatter 既有欄位名（例如 `paths`）當鍵 |
| `license` | string | 否 | 此 skill 適用的授權條款。屬於 [Agent Skills](https://agentskills.io) 規格的一部分。Claude Code 接受此欄位但不會據此行動 |
| `compatibility` | string | 否 | skill 的環境需求（上限 500 字元），例如適用產品或系統先決條件。屬於 [Agent Skills](https://agentskills.io) 規格的一部分。Claude Code 接受此欄位但不會據此行動 |

---

## ![Official](../%21/tags/official.svg) **（25 個）**

| # | Skill | 說明 |
|---|-------|-------------|
| 1 | `code-review` | 以指定的努力等級檢視當前 diff 的正確性 bug（low/medium：findings 較少但信心高；high→max：涵蓋面更廣）—— `--comment` 會把 findings 以行內 PR 留言貼出 |
| 2 | `batch` | 跨多個檔案批次執行命令 |
| 3 | `debug` | 除錯失敗的命令或程式碼問題 |
| 4 | `loop` | 以固定間隔重複執行 prompt 或 slash command（最長 3 天） |
| 5 | `claude-api` | 用 Claude API 或 Anthropic SDK 建構應用 —— 偵測到 `anthropic` / `@anthropic-ai/sdk` import 時觸發 |
| 6 | `fewer-permission-prompts` | 掃描逐字稿找出常見的唯讀 Bash／MCP 呼叫，在 `.claude/settings.json` 加入優先排序的白名單以減少權限提示 |
| 7 | `run` | 啟動並操作專案的 app，在真實 app（而非只有測試）中確認變更有效。需要 v2.1.145 |
| 8 | `verify` | 建置並執行 app 以確認程式碼變更達到預期，不會退回去只跑測試或型別檢查。需要 v2.1.145 |
| 9 | `run-skill-generator` | 教 `/run` 與 `/verify` 如何建置與啟動專案 —— 在 `.claude/skills/run-<name>/` 記錄一份專案專屬的啟動配方。需要 v2.1.145 |
| 10 | `simplify` | 檢視變更過的程式碼找出清理機會（重用、簡化、效率、抽象層級），四個 review 代理平行跑。自 v2.1.154 起它**不**找正確性 bug —— 那要用 `/code-review` |
| 11 | `design` | 把 UI 原型、畫面流程、landing page 或海報畫成同一張畫布上的 artboard，發佈成 artifact，執行 Claude Design 編輯器的研究預覽版。在帳號有開放儲存的情況下，artboard 可直接在畫布上編輯並存成新版本；否則只能檢視與匯出 PNG／PDF。需要可使用 artifacts 的 session。Anthropic API 上可用；Amazon Bedrock、Google Cloud Agent Platform 與 Microsoft Foundry 上不可用。v2.1.234 引入 |
| 12 | `design-sync` | 把你 repo 的 React design system 轉換後上傳到 Claude Design —— 可自行命名 design system（例如 `/design-sync Acme DS`）。首次同步會驗證每個元件，大型 repo 可能跑數小時。僅 Anthropic API 可用（Bedrock、Google Cloud Agent Platform 與 Microsoft Foundry 不可用）。獨立版 Claude Design 將於 2026 年 12 月 14 日關閉 |
| 13 | `dataviz` | 設計圖表、圖形與儀表板，附色票驗證器以產生無障礙且一致的視覺化 —— 任何輸出媒介的任何圖表、圖形、plot 或資料視覺化請求都會觸發。v2.1.198 引入 |
| 14 | `doctor` | 針對你的 Claude Code 設定做安裝／健康檢查。這是唯一不受 `disableBundledSkills` 影響的內建 skill —— 即使該設定開啟仍可輸入。v2.1.205 從內建命令重新歸類為內建 skill |
| 15 | `review` | 對 GitHub pull request 做快速、單趟、唯讀的檢視。要多代理深入檢視請改用 `/code-review <level> <pr#>`。v2.1.186–v2.1.201 期間改用 `/code-review medium` 引擎；v2.1.202 回復為快速單趟檢視。v2.1.108 起可用 Skill 工具呼叫 |
| 16 | `security-review` | 檢視當前 diff 的安全漏洞並建議修補。傳 `--fix` 可套用 findings，或 `--comment` 貼成行內 GitHub PR 留言。v2.1.108 起可用 Skill 工具呼叫 |
| 17 | `workflow-authoring` | 載入撰寫動態 workflow 腳本的參考文件：腳本 API、resume 行為、品質模式與實作範例。Claude 通常會在寫腳本前自行載入。僅在動態 workflow 啟用時可用。需要 v2.1.248 |
| 18 | `skill-doctor` | 回報哪些已載入的 skill 沒被用到，以及各自佔多少脈絡成本，好讓你裁掉它們。v2.1.261 引入 |
| 19 | `update-config` | 透過 `settings.json` 設定 Claude Code harness —— 描述任何設定變更（允許某命令、設環境變數、加 hook），Claude 就會改對應的設定檔；主題或模型這類簡單選項請改用 `/config` |
| 20 | `slides` | 依你的簡報做出新的 Claude Slides artifact（例如 `/slides a quarterly review for the sales team`） |
| 21 | `artifact-capabilities` | 載入已發佈 artifact 可用的 runtime capability 參考文件，例如呼叫 connector 或提供檔案下載，也包含你的帳號有哪些。Claude 通常會在建構用到這些能力的頁面前自行載入。在 artifacts 可用的環境可用 |
| 22 | `artifact-diagramming` | 載入 artifact 的圖解指南：何時該畫圖、該畫什麼、以及如何寫出在淺色與深色主題都清楚的行內 SVG。Claude 通常會在 artifact 需要圖解時自行載入。需要 v2.1.221+ |
| 23 | `claude-in-chrome` | 透過 Claude in Chrome 讓 Claude 在你的瀏覽器中執行任務（測試頁面、填表單、讀 console log）。在 Chrome 整合啟用時可用（例如 `claude --chrome`） |
| 24 | `artifact-design` | 載入已發佈 artifact 頁面的設計指南與基本功 —— 版面、主題、尺寸與文案風格。Claude 通常會在建構任何 artifact 前自行載入。v2.1.281 引入 |
| 25 | `plugin-authoring` | 做出 mod —— 改變 Claude 自身介面或行為的東西，例如即時面板或側欄、prompt 上方的 band、狀態列、toast、slash command，或掛在工具呼叫／prompt 上的 hook。用來製作、修改或除錯 mod 及其 hooks 模組。需要 v2.1.287+ |

另見：[官方 Skills Repository](https://github.com/anthropics/skills/tree/main/skills)，收錄社群維護、可安裝的 skills。

---

## 資料來源

- [Claude Code Skills — Docs](https://code.claude.com/docs/en/skills)
- [Monorepo 中的 Skills 探索機制](../reports/claude-skills-for-larger-mono-repos.md)
- [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
