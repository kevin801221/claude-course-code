# CLI 啟動旗標最佳實踐

![Last Updated](https://img.shields.io/badge/Last_Updated-Mar%2002%2C%202026-white?style=flat&labelColor=555)

從終端機啟動 Claude Code 時可用的啟動旗標、頂層子命令與啟動環境變數參考。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`best-practice/claude-cli-startup-flags.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-cli-startup-flags.md)

---

## 目錄

1. [Session 管理](#session-管理)
2. [模型與設定](#模型與設定)
3. [權限與安全](#權限與安全)
4. [輸出與格式](#輸出與格式)
5. [System Prompt](#system-prompt)
6. [代理與子代理](#代理與子代理)
7. [MCP 與外掛](#mcp-與外掛)
8. [目錄與工作區](#目錄與工作區)
9. [預算與上限](#預算與上限)
10. [整合](#整合)
11. [初始化與維護](#初始化與維護)
12. [除錯與診斷](#除錯與診斷)
13. [設定覆寫](#設定覆寫)
14. [版本與說明](#版本與說明)
15. [子命令](#子命令)
16. [環境變數](#環境變數)

---

## Session 管理

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--continue` | `-c` | 接續當前目錄最近一次的對話 |
| `--resume` | `-r` | 依 ID 或名稱接續特定 session，或顯示互動選擇器 |
| `--from-pr <NUMBER\|URL>` | | 接續與特定 GitHub PR 關聯的 session |
| `--fork-session` | | 接續時建立新的 session ID（搭配 `--resume` 或 `--continue` 使用） |
| `--session-id <UUID>` | | 使用特定 session ID（必須是合法 UUID） |
| `--no-session-persistence` | | 停用 session 持久化（僅 print 模式） |
| `--remote` | | 在 claude.ai 建立新的網頁 session |
| `--teleport` | | 在你的本機終端機接續網頁 session |

---

## 模型與設定

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--model <NAME>` | | 以別名（`sonnet`、`opus`、`haiku`）或完整 model ID 設定模型 |
| `--fallback-model <NAME>` | | 預設模型過載時自動退回的模型（僅 print 模式） |
| `--betas <LIST>` | | API 請求中要帶的 beta header（僅 API key 使用者） |

---

## 權限與安全

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--dangerously-skip-permissions` | | 跳過**所有**權限提示。請極度謹慎使用 |
| `--allow-dangerously-skip-permissions` | | 讓權限略過成為一個選項，但不直接啟用 |
| `--permission-mode <MODE>` | | 以指定權限模式啟動：`default`、`plan`、`acceptEdits`、`bypassPermissions` |
| `--allowedTools <TOOLS>` | | 不需提示即可執行的工具（使用權限規則語法） |
| `--disallowedTools <TOOLS>` | | 完全從模型脈絡中移除的工具 |
| `--tools <TOOLS>` | | 限制 Claude 可用的內建工具（用 `""` 全部停用） |
| `--permission-prompt-tool <TOOL>` | | 指定在非互動模式下處理權限提示的 MCP 工具 |

---

## 輸出與格式

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--print` | `-p` | 印出回覆而不進入互動模式（headless／SDK 模式） |
| `--output-format <FORMAT>` | | 輸出格式：`text`、`json`、`stream-json` |
| `--input-format <FORMAT>` | | 輸入格式：`text`、`stream-json` |
| `--json-schema <SCHEMA>` | | 取得符合 schema 且經驗證的 JSON（僅 print 模式） |
| `--include-partial-messages` | | 包含部分串流事件（需要 `--print` 與 `--output-format=stream-json`） |
| `--verbose` | | 啟用詳細記錄，輸出完整的逐回合內容 |

---

## System Prompt

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--system-prompt <TEXT>` | | 用自訂文字取代整個 system prompt |
| `--system-prompt-file <PATH>` | | 從檔案載入 system prompt 以取代預設（僅 print 模式） |
| `--append-system-prompt <TEXT>` | | 把自訂文字附加到預設 system prompt 之後 |
| `--append-system-prompt-file <PATH>` | | 把檔案內容附加到預設 prompt 之後（僅 print 模式） |

---

## 代理與子代理

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--agent <NAME>` | | 為當前 session 指定代理 |
| `--agents <JSON>` | | 透過 JSON 動態定義自訂子代理 |
| `--teammate-mode <MODE>` | | 設定 agent team 顯示方式：`auto`、`in-process`、`tmux` |

---

## MCP 與外掛

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--mcp-config <PATH\|JSON>` | | 從 JSON 檔或字串載入 MCP server |
| `--strict-mcp-config` | | 只用 `--mcp-config` 中的 MCP server，忽略其他所有來源 |
| `--plugin-dir <PATH>` | | 僅為此 session 從目錄載入外掛（可重複使用） |

---

## 目錄與工作區

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--add-dir <PATH>` | | 新增 Claude 可存取的額外工作目錄 |
| `--worktree` | `-w` | 在隔離的 git worktree 中啟動 Claude（從 HEAD 分支出來） |

---

## 預算與上限

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--max-budget-usd <AMOUNT>` | | API 呼叫在停止前的最大美元金額（僅 print 模式） |
| `--max-turns <NUMBER>` | | 限制代理回合數（僅 print 模式） |

---

## 整合

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--chrome` | | 啟用 Chrome 瀏覽器整合以進行網頁自動化 |
| `--no-chrome` | | 為此 session 停用 Chrome 瀏覽器整合 |
| `--ide` | | 啟動時若剛好只有一個合法 IDE 可用則自動連線 |

---

## 初始化與維護

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--init` | | 執行初始化 hook 並啟動互動模式 |
| `--init-only` | | 執行初始化 hook 後結束（不進入互動 session） |
| `--maintenance` | | 執行維護 hook 後結束 |

---

## 除錯與診斷

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--debug <CATEGORIES>` | | 啟用除錯模式，可選擇性過濾類別（例如 `"api,hooks"`） |

---

## 設定覆寫

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--settings <PATH\|JSON>` | | 要載入的設定 JSON 檔路徑或 JSON 字串 |
| `--setting-sources <LIST>` | | 要載入的來源清單，以逗號分隔：`user`、`project`、`local` |
| `--disable-slash-commands` | | 為此 session 停用所有 skill 與 slash command |

---

## 版本與說明

| 旗標 | 簡寫 | 說明 |
|------|-------|-------------|
| `--version` | `-v` | 輸出版本號 |
| `--help` | `-h` | 顯示說明資訊 |

---

## 子命令

這些是以 `claude <subcommand>` 執行的頂層命令：

| 子命令 | 說明 |
|------------|-------------|
| `claude` | 啟動互動式 REPL |
| `claude "query"` | 以初始 prompt 啟動 REPL |
| `claude agents` | 列出已設定的代理 |
| `claude auth` | 管理 Claude Code 驗證 |
| `claude doctor` | 從命令列執行診斷 |
| `claude install` | 安裝或切換 Claude Code 原生建置版本 |
| `claude mcp` | 設定 MCP server（`add`、`remove`、`list`、`get`、`enable`） |
| `claude plugin` | 管理 Claude Code 外掛 |
| `claude remote-control` | 管理 remote control session |
| `claude setup-token` | 建立長期 token 供訂閱使用 |
| `claude update` / `claude upgrade` | 更新到最新版本 |

---

## 環境變數

這些僅限啟動時的環境變數要在啟動 Claude Code 前於你的 shell 中設定（無法透過 `settings.json` 設定）：

| 變數 | 說明 |
|----------|-------------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | 啟用實驗性 agent teams。也可透過 env 設定 —— 見[設定參考（英文原檔）](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md) |
| `CLAUDE_CODE_TMPDIR` | 覆寫內部檔案的暫存目錄。也可透過 `env` 鍵設定 —— 見[設定參考（英文原檔）](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md) |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` | 啟用額外目錄的 CLAUDE.md 載入。也可透過 `env` 鍵設定 —— 見[設定參考（英文原檔）](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md) |
| `DISABLE_AUTOUPDATER=1` | 停用自動更新。也可透過 `env` 鍵設定 —— 見[設定參考（英文原檔）](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md) |
| `CLAUDE_CODE_EFFORT_LEVEL` | 控制思考深度 —— 見[設定參考（英文原檔）](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md) |
| `USE_BUILTIN_RIPGREP=0` | 使用系統 ripgrep 而非內建版本（Alpine Linux） |
| `CLAUDE_CODE_SIMPLE` | 啟用 simple 模式（只有 Bash + Edit 工具）。也可透過 `env` 鍵設定 —— 見[設定參考（英文原檔）](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md) |
| `CLAUDE_BASH_NO_LOGIN=1` | BashTool 跳過 login shell |
| `CCR_FORCE_BUNDLE=1` | 使用 `claude --remote` 時強制打包／上傳本機 repository。也可透過 `env` 鍵設定 —— 見[設定參考（英文原檔）](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md) |

關於可透過 `settings.json` 中 `"env"` 鍵設定的環境變數（包含 `MAX_THINKING_TOKENS`、`CLAUDE_CODE_SHELL`、`CLAUDE_CODE_ENABLE_TASKS`、`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`、`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` 等），請見 [Claude 設定參考（英文原檔）](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md)。

---

## 資料來源

- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Claude Code Headless Mode](https://code.claude.com/docs/en/headless)
- [Claude Code Setup](https://code.claude.com/docs/en/setup)
- [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [Claude Code Common Workflows](https://code.claude.com/docs/en/common-workflows)
