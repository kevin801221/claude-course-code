<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 功能目錄

> 一份關於 Claude Code 所有功能的快速參考：命令、agents、skills、plugins 和 hooks。

**導航**: [命令](#斜槓命令) | [許可權模式](#許可權模式) | [Subagents](#subagents) | [Skills](#skills) | [Plugins](#plugins) | [MCP Servers](#mcp-servers) | [Hooks](#hooks) | [Memory](#memory-files) | [2026 年 3 月新功能](#2026-年-3-月新功能)

---

## 概覽

| 功能 | 內建 | 範例 | 總數 | 參考 |
|---------|----------|----------|-------|-----------|
| **Slash Commands** | 60+ | 8 | 68+ | [01-slash-commands/README.md](01-slash-commands/README.md) |
| **Subagents** | 6 | 8 | 14 | [04-subagents/README.md](04-subagents/README.md) |
| **Skills** | 10 個內建 | 6 | 16 | [03-skills/README.md](03-skills/README.md) |
| **Plugins** | - | 3 | 3 | [07-plugins/README.md](07-plugins/README.md) |
| **MCP Servers** | - | 0 | 0 | [05-mcp/README.md](05-mcp/README.md) |
| **Hooks** | 33 個事件 | 0 | 33 | [06-hooks/README.md](06-hooks/README.md) |
| **Memory** | 7 種型別 | 3 | 10 | [02-memory/README.md](02-memory/README.md) |
| **總計** | **116** | **28** | **144** | |

---

## 斜槓命令

命令是使用者手動觸發的快捷操作，用來執行特定任務。

### 內建命令

| 命令 | 說明 | 適用場景 |
|---------|-------------|-------------|
| `/help` | 顯示幫助資訊 | 開始上手、學習命令 |
| `/btw` | 提出不寫入上下文的插話問題 | 臨時補充問題 |
| `/chrome` | 設定 Chrome 整合 | 瀏覽器自動化 |
| `/clear` | 清空對話歷史 | 重新開始、減少上下文 |
| `/diff` | 互動式 diff 檢視器 | 審查變更 |
| `/config` | 檢視/編輯設定 | 自訂行為 |
| `/status` | 顯示會話狀態 | 檢查當前狀態 |
| `/agents` | 已移除：嚮導在 v2.1.198 中移除，該命令在 v2.1.281 中從 `/` 選單和 `/help` 中移除 — 請讓 Claude 建立或管理 subagents，或編輯 `.claude/agents/` | 讓 Claude 管理 subagents |
| `/skills` | 列出可用 skills | 檢視可自動觸發的能力 |
| `/hooks` | 列出已設定的 hooks | 除錯自動化 |
| `/insights` | 分析會話模式 | 最佳化會話使用 |
| `/install-slack-app` | 安裝 Claude Slack 應用 | Slack 整合 |
| `/keybindings` | 自訂鍵盤快捷鍵 | 按鍵客製化 |
| `/mcp` | 列出 MCP servers | 檢查外部整合 |
| `/memory` | 檢視已載入的 memory 檔案 | 除錯上下文載入 |
| `/mobile` | 生成移動端二維碼 | 手機訪問 |
| `/passes` | 與朋友分享一週免費的 Claude Code（僅限符合條件的賬戶） | 推薦好友 |
| `/plugin` | 管理 plugins | 安裝/移除擴充套件 |
| `/plan` | 進入規劃模式 | 複雜實現 |
| `/rewind` | 回退到 checkpoint | 撤銷變更、探索替代方案 |
| `/checkpoint` | `/rewind` 的別名 | 與 `/rewind` 相同 |
| `/cost` | 顯示 token 消耗 | 監控開銷 |
| `/context` | 顯示上下文視窗使用情況 | 管理對話長度 |
| `/export` | 匯出對話 | 儲存以供參考 |
| `/extra-usage` | 設定額外用量限制 | 限流管理 |
| `/feedback` | 提交回饋或 bug 報告 | 報告問題 |
| `/login` | 透過 Anthropic 認證 | 訪問功能 |
| `/logout` | 登出 | 切換賬號 |
| `/sandbox` | 切換 sandbox 模式 | 安全執行命令 |
| `/doctor` | 執行診斷 | 排查問題 |
| `/reload-plugins` | 重新載入已安裝的 plugins。自 v2.1.221 起，大多數安裝會立即生效；僅當安裝摘要提示 `Run /reload-plugins to activate.` 時才需要 | 外掛管理 |
| `/release-notes` | 顯示更新說明 | 檢視新功能 |
| `/remote-control` | 啟用遠端控制 | 遠端訪問 |
| `/permissions` | 管理許可權 | 控制訪問 |
| `/rename` | 重新命名當前會話 | 組織會話 |
| `/resume` | 恢復之前的會話 | 繼續工作 |
| `/tasks` | 檢視後臺任務 | 監控非同步操作 |
| `/copy` | 複製最後一次回覆到剪貼簿 | 快速分享輸出 |
| `/teleport` | 將會話轉移到另一臺機器 | 遠端繼續工作 |
| `/desktop` | 開啟 Claude Desktop 應用 | 切換桌面介面 |
| `/theme` | 更改顏色主題 | 自訂外觀 |
| `/usage` | 顯示 API 使用統計 | 監控配額和消耗 |
| `/fork` | 把當前對話複製到一個新的獨立後臺會話（v2.1.212+） | 並行探索替代方案 |
| `/subtask` | 派生一個繼承當前對話的 forked subagent，完成後把結果返回給本對話（v2.1.212+） | 委派支線任務而不打斷當前思路 |
| `/stats` | 顯示會話統計 | 檢視會話指標 |
| `/statusline` | 設定狀態列 | 自訂狀態顯示 |
| `/stickers` | 訂購 Claude Code 貼紙 | 趣味獎勵 |
| `/fast` | 切換快速輸出模式 | 加快響應 |
| `/terminal-setup` | 設定終端整合 | 設定終端特性 |
| `/upgrade` | 開啟升級頁面以切換到更高套餐 | 套餐升級 |

### 自訂命令（範例）

| 命令 | 說明 | 適用場景 | 作用域 | 安裝 |
|---------|-------------|-------------|-------|--------------|
| `/optimize` | 分析程式碼以做最佳化 | 效能改進 | 專案 | `cp 01-slash-commands/optimize.md .claude/commands/` |
| `/pr` | 準備 Pull Request | 提交 PR 前 | 專案 | `cp 01-slash-commands/pr.md .claude/commands/` |
| `/generate-api-docs` | 生成 API 文件 | 編寫 API 文件 | 專案 | `cp 01-slash-commands/generate-api-docs.md .claude/commands/` |
| `/commit` | 結合上下文建立 git commit | 提交變更 | 使用者 | `cp 01-slash-commands/commit.md .claude/commands/` |
| `/push-all` | 先暫存、提交再 push | 快速釋出 | 使用者 | `cp 01-slash-commands/push-all.md .claude/commands/` |
| `/doc-refactor` | 重構文件結構 | 改進文件 | 專案 | `cp 01-slash-commands/doc-refactor.md .claude/commands/` |
| `/setup-ci-cd` | 搭建 CI/CD 管線 | 新專案 | 專案 | `cp 01-slash-commands/setup-ci-cd.md .claude/commands/` |
| `/unit-test-expand` | 擴充套件測試覆蓋率 | 改進測試 | 專案 | `cp 01-slash-commands/unit-test-expand.md .claude/commands/` |

> **作用域**: `User` = 個人工作流程（`~/.claude/commands/`），`Project` = 團隊共享（`.claude/commands/`）

**參考**: [01-slash-commands/README.md](01-slash-commands/README.md) | [官方文件](https://code.claude.com/docs/en/interactive-mode)

**快速安裝（所有自訂命令）**：
```bash
cp 01-slash-commands/*.md .claude/commands/
```

---

## 許可權模式

Claude Code 提供 6 種許可權模式，用來控制工具呼叫如何被授權。

| 模式 | 說明 | 適用場景 |
|------|-------------|-------------|
| `default` | 每次工具呼叫都詢問 | 親自審查每個操作。自 v2.1.283 起，互動式終端和 VS Code 會話的內建起始模式是 auto |
| `acceptEdits` | 自動接受檔案編輯，其他情況仍詢問 | 可信編輯工作流程 |
| `plan` | 調研並提出計劃；在你批准前不修改原始碼 | 規劃與探索 |
| `auto` | 所有操作，附帶後臺安全分類器檢查 | 長任務、減少許可權提示 |
| `bypassPermissions` | 跳過所有許可權檢查 | CI/CD、無頭環境 |
| `dontAsk` | 跳過需要許可權的工具 | 非互動指令碼 |

> **注意**：`auto` 模式需要滿足合格的套餐、模型和提供商條件 — 參見 [09-advanced-features/](09-advanced-features)。只有在可信且已隔離的環境中才使用 `bypassPermissions`。

**參考**: [官方文件](https://code.claude.com/docs/en/permissions)

---

## Subagents

為特定任務準備的專門化 AI 助手，擁有隔離上下文。

### 內建 Subagents

| Agent | 說明 | 工具 | 模型 | 適用場景 |
|-------|-------------|-------|-------|-------------|
| **general-purpose** | 多步任務、研究 | 所有工具 | 繼承當前模型 | 複雜研究、多檔案任務 |
| **Plan** | 實現規劃 | Read、Glob、Grep、Bash | 繼承當前模型 | 架構設計、規劃 |
| **Explore** | 程式碼庫探索 | Read、Glob、Grep | 繼承（上限為 Opus） | 快速搜尋、理解程式碼 |
| **claude** | 不適合更專門 agent 的任務的通用兜底 agent | 所有工具 | 繼承當前模型 | 沒有專門 agent 的任務；被排程的後臺會話的預設 agent |
| **statusline-setup** | 狀態列設定 | Bash、Read、Write | Sonnet | 設定狀態列顯示 |
| **claude-code-guide** | 幫助與文件 | Read、Glob、Grep | Haiku | 獲取幫助、學習功能 |

### Subagent 設定欄位

| 欄位 | 型別 | 說明 |
|-------|------|-------------|
| `name` | string | agent 標識 |
| `description` | string | 這個 agent 的用途 |
| `model` | string | 模型覆蓋值（`sonnet`、`opus`、`haiku`、`fable`、完整模型 ID 或 `inherit`） |
| `tools` | array | 允許使用的工具列表 |
| `effort` | string | 努力等級（`low`、`medium`、`high`、`xhigh`、`max`；取決於模型） |
| `initialPrompt` | string | agent 作為主會話 agent 執行時（`--agent`）自動提交的第一條使用者訊息 |
| `disallowedTools` | array | 明確禁止該 agent 使用的工具 |

### 自訂 Subagents（範例）

| Agent | 說明 | 適用場景 | 作用域 | 安裝 |
|-------|-------------|-------------|-------|--------------|
| `code-reviewer` | 全面的程式碼品質檢查 | 程式碼審查會話 | 專案 | `cp 04-subagents/code-reviewer.md .claude/agents/` |
| `code-architect` | 功能架構設計 | 新功能規劃 | 專案 | `cp 04-subagents/code-architect.md .claude/agents/` |
| `code-explorer` | 深入分析程式碼庫 | 理解已有功能 | 專案 | `cp 04-subagents/code-explorer.md .claude/agents/` |
| `clean-code-reviewer` | 按 Clean Code 原則審查 | 可維護性審查 | 專案 | `cp 04-subagents/clean-code-reviewer.md .claude/agents/` |
| `test-engineer` | 測試策略與覆蓋率 | 測試規劃 | 專案 | `cp 04-subagents/test-engineer.md .claude/agents/` |
| `documentation-writer` | 技術文件編寫 | API 文件、指南 | 專案 | `cp 04-subagents/documentation-writer.md .claude/agents/` |
| `secure-reviewer` | 面向安全的審查 | 安全審計 | 專案 | `cp 04-subagents/secure-reviewer.md .claude/agents/` |
| `implementation-agent` | 完整功能實現 | 功能開發 | 專案 | `cp 04-subagents/implementation-agent.md .claude/agents/` |
| `debugger` | 根因分析 | Bug 調查 | 使用者 | `cp 04-subagents/debugger.md .claude/agents/` |
| `data-scientist` | SQL 查詢、資料分析 | 資料任務 | 使用者 | `cp 04-subagents/data-scientist.md .claude/agents/` |

> **作用域**: `User` = 個人（`~/.claude/agents/`），`Project` = 團隊共享（`.claude/agents/`）

**參考**: [04-subagents/README.md](04-subagents/README.md) | [官方文件](https://code.claude.com/docs/en/sub-agents)

**快速安裝（所有自訂 agents）**：
```bash
cp 04-subagents/*.md .claude/agents/
```

---

## Skills

可自動觸發的能力包，包含說明、指令碼和模板。

### 範例 Skills

| Skill | 說明 | 何時自動觸發 | 作用域 | 安裝 |
|-------|-------------|-------------------|-------|--------------|
| `code-review` | 全面的程式碼審查 | “Review this code”, “Check quality” | 專案 | `cp -r 03-skills/code-review-specialist .claude/skills/` |
| `brand-voice` | 品牌一致性檢查器 | 編寫營銷文案時 | 專案 | `cp -r 03-skills/brand-voice .claude/skills/` |
| `doc-generator` | API 文件生成器 | “Generate docs”, “Document API” | 專案 | `cp -r 03-skills/doc-generator .claude/skills/` |
| `refactor` | 系統化程式碼重構（Martin Fowler） | “Refactor this”, “Clean up code” | 使用者 | `cp -r 03-skills/refactor ~/.claude/skills/` |

> **作用域**: `User` = 個人（`~/.claude/skills/`），`Project` = 團隊共享（`.claude/skills/`）

### Skill 結構

```
~/.claude/skills/skill-name/
├── SKILL.md          # skill 定義與說明
├── scripts/          # 輔助指令碼
└── templates/        # 輸出模板
```

### Skill Frontmatter 欄位

Skills 支援在 `SKILL.md` 中使用 YAML frontmatter 進行設定：

| 欄位 | 型別 | 說明 |
|-------|------|-------------|
| `name` | string | skill 顯示名稱 |
| `description` | string | 這個 skill 的作用 |
| `when_to_use` | string | 追加到 `description` 的觸發短語或範例請求 |
| `effort` | string | 努力等級（`low`、`medium`、`high`、`xhigh`、`max`；取決於模型） |
| `shell` | string | 內聯 `` !`command` `` 塊使用的 shell（預設 `bash`，或 `powershell`） |

**參考**: [03-skills/README.md](03-skills/README.md) | [官方文件](https://code.claude.com/docs/en/skills)

**快速安裝（所有 skills）**：
```bash
cp -r 03-skills/* ~/.claude/skills/
```

### 內建 Skills

| Skill | 說明 | 何時自動觸發 |
|-------|-------------|-------------------|
| `/simplify` | 審查程式碼品質 | 寫完程式碼後 |
| `/batch` | 將大型變更拆分為 5–30 個獨立單元，每個單元由一個後臺 subagent 在獨立 worktree 中執行 | 大規模並行重構 |
| `/debug [description]` | 為當前會話開啟除錯日誌，並根據會話除錯日誌排查問題 | 除錯 Claude Code 本身 |
| `/loop` | 按間隔執行提示詞 | 週期性任務 |
| `/claude-api` | 使用 Claude API 建置應用 | API 開發 |
| `/code-review` | 按指定強度審查當前 diff 的正確性問題（例如 `/code-review high`）；加 `--comment` 可把結論發成 PR 行內評論。自 v2.1.218 起以**後臺 subagent** 執行 | 寫完程式碼後、合併 PR 前 |
| `/fewer-permission-prompts` | 掃描歷史記錄並給出按優先順序排序的允許列表建議 | 減少重複的許可權提示 |
| `/run` *(v2.1.145+)* | 啟動當前專案的應用，直觀看到改動效果 | 在真實應用裡驗證改動 |
| `/run-skill-generator` *(v2.1.145+)* | 教會 `/run`、`/verify` 如何處理某個具體專案 | 首次為專案設定 `/run` |
| `/verify` *(v2.1.145+)* | 建置、執行並觀察應用，確認修復真的生效 | 端到端驗證修復 |

---

## Plugins

把 commands、agents、MCP servers 和 hooks 打包在一起的集合。

### 範例 Plugins

| Plugin | 說明 | 元件 | 適用場景 | 作用域 | 安裝 |
|--------|-------------|------------|-------------|-------|--------------|
| `pr-review` | PR 審查工作流程 | 3 個 commands、3 個 agents、GitHub MCP | 程式碼審查 | 專案 | `claude --plugin-dir ./07-plugins/pr-review` |
| `devops-automation` | 部署與監控 | 4 個 commands、3 個 agents、K8s MCP | DevOps 任務 | 專案 | `/plugin install devops-automation` |
| `documentation` | 文件生成套件 | 4 個 commands、3 個 agents、模板 | 文件編寫 | 專案 | `/plugin install documentation` |

> **作用域**: `Project` = 團隊共享，`User` = 個人工作流程

### Plugin 結構

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json   # manifest 檔案（.claude-plugin/ 中唯一的檔案）
├── commands/         # Slash commands
├── agents/           # Subagents
├── skills/           # Skills (<name>/SKILL.md)
├── hooks/
│   └── hooks.json    # Hook 設定
├── .mcp.json         # MCP 設定
├── bin/              # 可執行檔案
└── scripts/          # 工具指令碼
```

**參考**: [07-plugins/README.md](07-plugins/README.md) | [官方文件](https://code.claude.com/docs/en/plugins)

**Plugin 管理命令**：
```bash
/plugin list              # 列出已安裝的 plugins
/plugin install <name>    # 安裝 plugin
/plugin uninstall <name>  # 解除安裝 plugin
claude plugin update <name>   # 更新 plugin（CLI；/plugin update 斜槓命令形式僅在正文中被提及，命令參考中並無該條目）
```

---

## MCP Servers

用於訪問外部工具和 API 的 Model Context Protocol servers。

### 常見 MCP Servers

| Server | 說明 | 適用場景 | 作用域 | 安裝 |
|--------|-------------|-------------|-------|--------------|
| **GitHub** | PR 管理、issues、程式碼 | GitHub 工作流程 | 本地 | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` |
| **Database** | SQL 查詢、資料訪問 | 資料庫操作 | 本地 | `claude mcp add db -- npx -y @modelcontextprotocol/server-postgres` |
| **Filesystem** | 高階檔案操作 | 複雜檔案任務 | 本地 | `claude mcp add fs -- npx -y @modelcontextprotocol/server-filesystem` |
| **Slack** | 團隊溝通 | 通知、更新 | 專案 | 在設定中設定 |
| **Google Docs** | 文件訪問 | 文件編輯、審閱 | 專案 | 在設定中設定 |
| **Asana** | 專案管理 | 任務跟蹤 | 專案 | 在設定中設定 |
| **Stripe** | 支付資料 | 財務分析 | 專案 | 在設定中設定 |
| **Memory** | 持久記憶 | 跨會話回憶 | 使用者 | 在設定中設定 |
| **Context7** | 庫文件 | 查詢最新文件 | 使用者 | 在設定中設定（第三方 server） |

> **作用域**: `Local`（本地）= 不帶 `--scope` 的 `claude mcp add` 的預設作用域（僅你自己、當前專案；`~/.claude.json`），`Project` = 團隊（`.mcp.json`，`--scope project`），`User` = 個人（`~/.claude.json`，`--scope user`），`Built-in` = 預裝

### MCP 設定範例

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**參考**: [05-mcp/README.md](05-mcp/README.md) | [MCP 協議文件](https://modelcontextprotocol.io)

**快速安裝（GitHub MCP）**：
```bash
export GITHUB_TOKEN="your_token" && claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

---

## Hooks

在 Claude Code 事件發生時執行的事件驅動自動化。

### Hook 事件

| 事件 | 說明 | 觸發時機 | 使用場景 |
|-------|-------------|----------------|-----------|
| `SessionStart` | 會話開始/恢復 | 會話初始化 | 初始化任務 |
| `Setup` | 儲存庫初始化或維護執行 | 僅在 `--init-only`，或 `--init`/`--maintenance` 搭配 `-p` 時 | 準備工具鏈、安裝依賴 |
| `InstructionsLoaded` | 指令已載入 | `CLAUDE.md` 或規則檔案載入 | 自訂指令處理 |
| `UserPromptSubmit` | 提示詞提交前 | 使用者傳送訊息 | 輸入校驗 |
| `UserPromptExpansion` | 輸入的斜槓命令（skill、自訂命令或 MCP prompt）展開為提示詞 | `UserPromptSubmit` 之後、展開後的提示詞到達 Claude 之前 | 阻止直接使用 `/command`、新增按 skill 的上下文、記錄命令 |
| `PreToolUse` | 工具執行前 | 任意工具執行之前 | 校驗、日誌 |
| `PermissionRequest` | 顯示許可權對話方塊 | 敏感操作前 | 自訂審批流程 |
| `PermissionDenied` | 使用者拒絕許可權請求 | 許可權被拒絕後 | 日誌、分析、策略執行 |
| `PostToolUse` | 工具成功後 | 任意工具完成後 | 格式化、通知 |
| `PostToolUseFailure` | 工具執行失敗 | 工具報錯後 | 錯誤處理、日誌 |
| `PostToolBatch` | 一批工具呼叫完成後 | 工具批次結束 | 彙總報告、批次校驗 |
| `Notification` | 傳送通知時 | Claude 傳送通知 | 外部提醒 |
| `MessageDisplay` | 助手訊息文字顯示時 | 訊息渲染過程中 | 轉換或隱藏顯示文字 |
| `SubagentStart` | 啟動 subagent | subagent 任務開始 | 初始化上下文 |
| `SubagentStop` | subagent 完成 | subagent 任務結束 | 鏈式動作 |
| `Stop` | Claude 完成響應 | 響應完成 | 清理、彙報 |
| `StopFailure` | API 錯誤導致結束 | API 錯誤發生 | 錯誤恢復、日誌 |
| `TeammateIdle` | 隊友 agent 空閒 | agent team 協調 | 分配工作 |
| `TaskCompleted` | 任務標記完成（僅在啟用 todo 工具時觸發 —— 預設僅在 Claude 3.x、Opus 4 至 4.7、Sonnet 4 至 4.6、Haiku 4.5 上可用；`CLAUDE_CODE_ENABLE_TODO_TOOLS=1` 可恢復） | 任務完成 | 任務後處理 |
| `TaskCreated` | 透過 TaskCreate 建立任務（僅在啟用 todo 工具時觸發 —— 預設僅在 Claude 3.x、Opus 4 至 4.7、Sonnet 4 至 4.6、Haiku 4.5 上可用；`CLAUDE_CODE_ENABLE_TODO_TOOLS=1` 可恢復） | 新任務建立 | 任務追蹤、日誌 |
| `ConfigChange` | 設定更新 | 設定被修改 | 響應設定變化 |
| `CwdChanged` | 當前工作目錄變化 | 目錄切換 | 目錄級初始化 |
| `DirectoryAdded` | 會話中註冊了新的工作目錄 | `/add-dir` 或 SDK `register_repo_root` | 為新目錄設定工具鏈 |
| `FileChanged` | 監控檔案發生變化 | 檔案被修改 | 檔案監控、重建 |
| `PreCompact` | 壓縮前 | 上下文壓縮前 | 狀態保留 |
| `PostCompact` | 壓縮完成後 | 壓縮完成 | 壓縮後動作 |
| `PreModelSwitch` | 應用模型切換之前 | 請求切換模型時 | 攔截或否決模型變更 |
| `PostModelSwitch` | 會話模型變更之後 | 模型切換完成 | 記錄或響應模型變更 |
| `WorktreeCreate` | worktree 建立中 | git worktree 建立 | 設定 worktree 環境 |
| `WorktreeRemove` | worktree 被移除 | git worktree 刪除 | 清理 worktree 資源 |
| `Elicitation` | MCP server 請求輸入 | MCP elicitation | 輸入校驗 |
| `ElicitationResult` | 使用者響應 elicitation | 使用者回答 | 響應處理 |
| `SessionEnd` | 會話結束 | 會話終止 | 清理、儲存狀態 |

### 範例 Hooks

| Hook | 說明 | 事件 | 作用域 | 安裝 |
|------|-------------|-------|-------|--------------|
| `validate-bash.py` | 命令校驗 | PreToolUse:Bash | 專案 | `cp 06-hooks/validate-bash.py .claude/hooks/` |
| `security-scan.py` | 安全掃描 | PostToolUse:Write | 專案 | `cp 06-hooks/security-scan.py .claude/hooks/` |
| `format-code.sh` | 自動格式化 | PostToolUse:Write | 使用者 | `cp 06-hooks/format-code.sh ~/.claude/hooks/` |
| `validate-prompt.py` | 提示詞校驗 | UserPromptSubmit | 專案 | `cp 06-hooks/validate-prompt.py .claude/hooks/` |
| `context-tracker.py` | token 使用跟蹤 | Stop | 使用者 | `cp 06-hooks/context-tracker.py ~/.claude/hooks/` |
| `pre-commit.sh` | 提交前校驗 | PreToolUse:Bash | 專案 | `cp 06-hooks/pre-commit.sh .claude/hooks/` |
| `log-bash.sh` | 命令日誌記錄 | PostToolUse:Bash | 使用者 | `cp 06-hooks/log-bash.sh ~/.claude/hooks/` |

> **作用域**: `Project` = 團隊（`.claude/settings.json`），`User` = 個人（`~/.claude/settings.json`）

### Hook 設定

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/validate-bash.py" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/format-code.sh" }
        ]
      }
    ]
  }
}
```

**參考**: [06-hooks/README.md](06-hooks/README.md) | [官方文件](https://code.claude.com/docs/en/hooks)

**快速安裝（所有 hooks）**：
```bash
mkdir -p ~/.claude/hooks && cp 06-hooks/*.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.sh
```

---

## Memory Files

會在多個會話之間自動載入的持久上下文。

### Memory 型別

| 型別 | 位置 | 作用域 | 適用場景 |
|------|----------|-------|-------------|
| **Managed Policy** | 組織管理的策略 | Organization | 統一組織標準 |
| **Project** | `./CLAUDE.md` | Project（團隊） | 團隊規範、專案上下文 |
| **Project Rules** | `.claude/rules/` | Project（團隊） | 模組化專案規則 |
| **User** | `~/.claude/CLAUDE.md` | User（個人） | 個人偏好 |
| **User Rules** | `~/.claude/rules/` | User（個人） | 模組化個人規則 |
| **Local** | `./CLAUDE.local.md` | Local（git 忽略） | 個人的專案專屬偏好，與 `CLAUDE.md` 一起載入；官方支援（[官方文件](https://code.claude.com/docs/en/memory)），需加入 `.gitignore` |
| **Auto Memory** | 自動 | Session | 自動捕捉的洞察和修正 |

> **作用域**: `Organization` = 管理員管理，`Project` = 透過 git 與團隊共享，`User` = 個人偏好，`Local` = 不提交，`Session` = 自動管理

**參考**: [02-memory/README.md](02-memory/README.md) | [官方文件](https://code.claude.com/docs/en/memory)

**快速安裝**：
```bash
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

---

## 2026 年 3 月新功能

| 功能 | 說明 | 使用方式 |
|---------|-------------|------------|
| **Remote Control** | 透過 API 遠端控制 Claude Code 會話 | 使用遠端控制 API 以程式設計方式傳送提示並接收響應 |
| **Web Sessions** | 在雲端會話中執行 Claude Code | 使用 `claude --cloud "task"` 或在 claude.ai/code 啟動 |
| **Desktop App** | Claude Code 的原生桌面應用程式 | 使用 `/desktop` 或從 Anthropic 網站下載 |
| **Agent Teams** | 協調多個 agent 共同處理相關任務 | 設定協作並共享上下文的 teammate agents |
| **Task List** | 後臺任務管理與監控 | 使用 `/tasks` 檢視和管理後臺操作 |
| **Prompt Suggestions** | 上下文感知的命令建議 | 根據當前上下文自動出現建議 |
| **Git Worktrees** | 用於並行開發的隔離 git worktree | 使用 worktree 命令進行安全的並行分支工作 |
| **Sandboxing** | 安全隔離的執行環境 | 使用 `/sandbox` 切換，在受限環境中執行命令 |
| **MCP OAuth** | 為 MCP servers 提供 OAuth 認證 | 在 MCP server 設定中設定 OAuth 憑據以安全訪問 |
| **MCP Tool Search** | 動態搜尋和發現 MCP 工具 | 使用工具搜尋查詢已連線 server 上可用的 MCP 工具 |
| **Scheduled Tasks** | 使用 `/loop` 和 cron 工具設定週期任務 | 使用 `/loop 5m /command` 或 CronCreate 工具 |
| **Chrome Integration** | 透過 Claude in Chrome 擴充套件操控你自己的 Chrome/Edge（可見視窗、沿用你的登入狀態） | 使用 `--chrome` 標誌或 `/chrome` 命令 |
| **Keyboard Customization** | 自訂按鍵對映並支援 chord | 使用 `/keybindings` 或編輯 `~/.claude/keybindings.json` |
| **自動模式（Auto Mode）** | 附帶後臺安全分類器檢查的完全自主執行 | `Shift+Tab` 切換，或使用 `--permission-mode auto` |
| **通道（Channels）** | 多通道通訊（Telegram、Slack 等）（Research Preview） | 設定 channel plugins；2026 年 3 月 |
| **語音輸入（Voice Dictation）** | 用語音輸入提示詞 | 使用麥克風圖示或語音快捷鍵 |
| **Agent Hook Type** | 觸發 subagent 而不是執行 shell 命令的 hook | 在 hook 設定中設定 `"type": "agent"` |
| **Prompt Hook Type** | 將 prompt 傳送給 Claude 模型做單輪評估、由模型以 JSON 返回決定的 hook | 在 hook 設定中設定 `"type": "prompt"` |
| **MCP Elicitation** | MCP servers 可在工具執行期間請求使用者輸入 | 透過 `Elicitation` 和 `ElicitationResult` hook 事件處理 |
| **WebSocket MCP Transport** | 用 WebSocket 連線 MCP server | 在 MCP server 設定中使用 `"transport": "websocket"` |
| **Plugin LSP Support** | 透過 plugins 整合 Language Server Protocol | 在 `plugin.json` 中設定 LSP servers，以獲得編輯器能力 |
| **Managed Drop-ins** | 組織管理的 drop-in 設定（v2.1.83） | 透過 managed policies 由管理員設定，自動應用到所有使用者 |

---

## 快速參考矩陣

### 功能選擇指南

| 需求 | 推薦功能 | 原因 |
|------|---------------------|-----|
| 快捷命令 | Slash Command | 手動、立即執行 |
| 持久上下文 | Memory | 自動載入 |
| 複雜自動化 | Skill | 自動觸發 |
| 專門任務 | Subagent | 隔離上下文 |
| 外部資料 | MCP Server | 實時訪問 |
| 事件自動化 | Hook | 事件觸發 |
| 完整解決方案 | Plugin | 一體化打包 |

### 安裝優先順序

| 優先順序 | 功能 | 命令 |
|----------|---------|---------|
| 1. 必裝 | Memory | `cp 02-memory/project-CLAUDE.md ./CLAUDE.md` |
| 2. 日常使用 | Slash Commands | `cp 01-slash-commands/*.md .claude/commands/` |
| 3. 品質提升 | Subagents | `cp 04-subagents/*.md .claude/agents/` |
| 4. 自動化 | Hooks | `cp 06-hooks/*.sh ~/.claude/hooks/` |
| 5. 整合 | MCP Servers | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` |
| 6. 全量打包 | Plugins | `/plugin install <name>` |

---

## 一條命令完成安裝

```bash
# 建立目錄
mkdir -p .claude/commands .claude/agents ~/.claude/hooks ~/.claude/skills

# 安裝所有功能
cp 01-slash-commands/*.md .claude/commands/
cp 04-subagents/*.md .claude/agents/
cp -r 03-skills/* ~/.claude/skills/
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 設定 MCP
export GITHUB_TOKEN="your_token"
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# 使用 Plugins
claude --plugin-dir ./07-plugins/pr-review
/plugin install devops-automation
```

---

## 其他資源

- [Claude Code Documentation](https://code.claude.com/docs/en/overview)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Skills Repository](https://github.com/luongnv89/skills) - 現成 skills 集合
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Boris Cherny's Claude Code Workflow](https://x.com/bcherny/status/2007179832300581177) - Claude Code 的創造者分享了他的系統化工作流程：並行 agents、共享 `CLAUDE.md`、Plan mode、slash commands、subagents，以及用於長時間自主會話的驗證 hooks。

---

**最後更新**: 2026 年 10 月 18 日
**Claude Code 版本**: 2.1.302
**來源**:
- https://code.claude.com/docs/en/tools-reference#task-tool-availability
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/discover-plugins
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/permission-modes
- https://code.claude.com/docs/en/cli-reference
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/chrome
- https://code.claude.com/docs/en/plugins/manifest-reference
- https://code.claude.com/docs/en/plugins/cli-reference
