<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 範例 - 速查卡

## 🚀 安裝速命令

### Slash Commands
```bash
# 安裝全部
cp 01-slash-commands/*.md .claude/commands/

# 安裝單個
cp 01-slash-commands/optimize.md .claude/commands/
```

### Memory
```bash
# 專案 memory
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 個人 memory
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

### Skills
```bash
# 個人 skills
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 專案 skills
cp -r 03-skills/code-review-specialist .claude/skills/
```

### Subagents
```bash
# 安裝全部
cp 04-subagents/*.md .claude/agents/

# 安裝單個
cp 04-subagents/code-reviewer.md .claude/agents/
```

### MCP
```bash
# 設定憑據
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# 安裝設定（專案級）
cp 05-mcp/github-mcp.json .mcp.json

# 或者使用者級：新增到 ~/.claude.json
```

### Hooks
```bash
# 安裝 hooks
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 在 settings 中設定（~/.claude/settings.json）
```

### Plugins
```bash
# 從範例安裝（如果已釋出）
claude --plugin-dir ./07-plugins/pr-review
/plugin install devops-automation
/plugin install documentation
```

### Checkpoints
```bash
# 每次使用者提示後都會自動建立 checkpoint
# 回退：按兩次 Esc 或使用：
/rewind

# 然後選擇：恢復程式碼和對話、恢復對話、
# 恢復程式碼、從這裡開始總結，或算了
```

### Advanced Features
```bash
# 在 settings 中設定（.claude/settings.json）
# 參見 09-advanced-features/config-examples.json

# planning mode
/plan 任務描述

# 許可權模式（使用 --permission-mode 引數）
# default          - 風險操作需要審批
# acceptEdits      - 自動接受檔案編輯，其他操作仍需審批
# plan             - 只讀分析，不做修改
# dontAsk          - 只執行預先批准的工具，其餘一律拒絕
# auto             - 後臺分類器自動決定許可權
# bypassPermissions - 全部接受（--permission-mode bypassPermissions；--dangerously-skip-permissions 與之等效）

# 會話管理
/resume                # 恢復之前的對話
/rename "name"         # 命名當前會話
/fork                  # 分叉當前會話
claude -c              # 繼續最近的對話
claude -r "session"    # 按名稱/ID 恢復會話
```

---

## 📋 功能速覽

| 功能 | 安裝路徑 | 用法 |
|------|----------|------|
| **Slash Commands（55+）** | `.claude/commands/*.md` | `/command-name` |
| **Memory** | `./CLAUDE.md` | 自動載入 |
| **Skills** | `.claude/skills/*/SKILL.md` | 自動觸發 |
| **Subagents** | `.claude/agents/*.md` | 自動委派 |
| **MCP** | `.mcp.json`（專案）或 `~/.claude.json`（使用者） | `/mcp__server__action` |
| **Hooks（33 個事件）** | `~/.claude/hooks/*.sh` | 事件觸發（5 類） |
| **Plugins** | 透過 `/plugin install` | 打包所有能力 |
| **Checkpoints** | 內建 | `Esc+Esc` 或 `/rewind` |
| **Planning Mode** | 內建 | `/plan <task>` |
| **Permission Modes（6 種）** | 內建 | `--allowedTools`、`--permission-mode` |
| **Sessions** | 內建 | `/resume`、`/rename`、`/branch`、`/fork` |
| **Background Tasks** | 內建 | 在後臺執行 |
| **Remote Control** | 內建 | `claude --remote-control` 或 `/remote-control` |
| **Web Sessions** | 內建 | `claude --cloud "task"` |
| **Git Worktrees** | 內建 | `claude -w <name>` |
| **Auto Memory** | 內建 | 自動儲存到 `~/.claude/projects/<project>/memory/` |
| **Task List** | 內建 | `Ctrl+T`（清單）、`/tasks`（後臺工作） |
| **Bundled Skills（5 個）** | 內建 | `/simplify`、`/loop`、`/claude-api`、`/voice`、`/browse` |

---

## 🎯 常見使用場景

### 程式碼審查
```bash
# 方法 1：slash command
cp 01-slash-commands/optimize.md .claude/commands/
# 使用：/optimize

# 方法 2：subagent
cp 04-subagents/code-reviewer.md .claude/agents/
# 使用：自動委派

# 方法 3：skill
cp -r 03-skills/code-review-specialist ~/.claude/skills/
# 使用：自動觸發

# 方法 4：外掛（推薦）
claude --plugin-dir ./07-plugins/pr-review
# 使用：/review-pr
```

### 文件
```bash
# slash command
cp 01-slash-commands/generate-api-docs.md .claude/commands/

# subagent
cp 04-subagents/documentation-writer.md .claude/agents/

# skill
cp -r 03-skills/doc-generator ~/.claude/skills/

# 外掛（完整方案）
/plugin install documentation
```

### DevOps
```bash
# 完整外掛
/plugin install devops-automation

# 命令：/deploy、/rollback、/status、/incident
```

### 團隊規範
```bash
# 專案 memory
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 按你的團隊規範編輯
vim CLAUDE.md
```

### 自動化與 Hooks
```bash
# 安裝 hooks（33 個事件，5 類：command、http、mcp_tool、prompt、agent）
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 範例：
# - 提交前測試：pre-commit.sh
# - 自動格式化程式碼：format-code.sh
# - 安全掃描：security-scan.sh

# 用 Auto Mode 實現全自動工作流程
claude --enable-auto-mode -p "重構並測試 auth 模組"
# 或者用 Shift+Tab 在模式間切換
```

### 安全重構
```bash
# 每次提示前都會自動建立 checkpoint
# 試著重構
# 如果成功：繼續
# 如果失敗：按 Esc+Esc 或使用 /rewind 返回
```

### 複雜實現
```bash
# 使用 planning mode
/plan 實現使用者認證系統

# Claude 會建立詳細計劃
# 你可以審閱並批准
# Claude 會系統化地執行實現
```

### CI/CD 整合
```bash
# 以 headless 模式執行（非互動）。未指定許可權模式時，-p 以 Manual 模式啟動
# （設定值 "default"，v2.1.302+）：需要審批的工具呼叫會被拒絕，因此請新增
# --allowedTools "Bash(npm test *)" 或 --permission-mode auto
claude -p "執行所有測試並生成報告"

# 在 CI 中搭配許可權模式
claude -p "執行測試" --permission-mode dontAsk

# 使用 Auto Mode 實現完全自治的 CI 任務
claude --enable-auto-mode -p "執行測試並修復失敗項"

# 結合 hooks 做自動化
# 參見 09-advanced-features/README.md
```

### 學習與實驗
```bash
# 用 plan mode 做安全分析
claude --permission-mode plan

# 安全實驗 - checkpoint 會自動建立
# 如果需要回退：按 Esc+Esc 或使用 /rewind
```

### Agent 團隊
```bash
# 啟用 agent 團隊
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 或者在 settings.json 中
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }

# 用這句話開始："使用團隊方式實現功能 X"
```

### 定時任務
```bash
# 每 5 分鐘執行一次命令
/loop 5m /check-status

# 一次性提醒：直接用自然語言提出（/loop 會一直重複直到取消）
30 分鐘後提醒我檢查部署
```

---

## 📁 檔案位置參考

```text
Your Project/
├── .claude/
│   ├── commands/              # Slash commands 放這裡
│   ├── agents/                # Subagents 放這裡
│   ├── skills/                # 專案 skills 放這裡
│   └── settings.json          # 專案設定（hooks 等）
├── .mcp.json                  # MCP 設定（專案級）
├── CLAUDE.md                  # 專案 memory
└── src/
    └── api/
        └── CLAUDE.md          # 目錄級 memory

User Home/
├── .claude/
│   ├── commands/              # 個人命令
│   ├── agents/                # 個人 agents
│   ├── skills/                # 個人 skills
│   ├── hooks/                 # hook 指令碼
│   ├── settings.json          # 使用者設定
│   └── CLAUDE.md              # 個人 memory
└── .claude.json               # 個人 MCP 設定（使用者級）

系統目錄/                      # macOS /Library/Application Support/ClaudeCode/，Linux /etc/claude-code/，Windows C:\Program Files\ClaudeCode\
├── managed-settings.json      # 託管設定（企業/組織）
└── managed-settings.d/        # 託管設定的附加檔案（drop-in）
```

---

## 🔍 查詢範例

### 按分類
- **Slash Commands**：`01-slash-commands/`
- **Memory**：`02-memory/`
- **Skills**：`03-skills/`
- **Subagents**：`04-subagents/`
- **MCP**：`05-mcp/`
- **Hooks**：`06-hooks/`
- **Plugins**：`07-plugins/`
- **Checkpoints**：`08-checkpoints/`
- **Advanced Features**：`09-advanced-features/`
- **CLI**：`10-cli/`

### 按使用場景
- **效能**：`01-slash-commands/optimize.md`
- **安全**：`04-subagents/secure-reviewer.md`
- **測試**：`04-subagents/test-engineer.md`
- **文件**：`03-skills/doc-generator/`
- **DevOps**：`07-plugins/devops-automation/`

### 按複雜度
- **簡單**：Slash commands
- **中等**：Subagents、Memory
- **高階**：Skills、Hooks
- **完整**：Plugins

---

## 🎓 學習路徑

### 第 1 天
```bash
# 閱讀總覽
cat README.md

# 安裝一個命令
cp 01-slash-commands/optimize.md .claude/commands/

# 試用
/optimize
```

### 第 2-3 天
```bash
# 設定 memory
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
vim CLAUDE.md

# 安裝 subagent
cp 04-subagents/code-reviewer.md .claude/agents/
```

### 第 4-5 天
```bash
# 設定 MCP
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"
cp 05-mcp/github-mcp.json .mcp.json

# 試用 MCP 命令
/mcp__github__list_prs
```

### 第 2 周
```bash
# 安裝 skill
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 讓它自動觸發
# 直接說：“Review this code for issues”
```

### 第 3 周及以後
```bash
# 安裝完整外掛
claude --plugin-dir ./07-plugins/pr-review

# 使用打包功能
/review-pr
/check-security
/check-tests
```

---

## 🆕 新功能（2026 年 3 月）

| 功能 | 說明 | 用法 |
|------|------|------|
| **Auto Mode** | 透過後臺分類器實現完全自治 | `--enable-auto-mode` 引數，`Shift+Tab` 切換模式 |
| **Channels** | Discord 和 Telegram 整合 | `--channels` 引數，Discord / Telegram bot |
| **Voice Dictation** | 對 Claude 說出命令和上下文 | `/voice` 命令 |
| **Hooks（33 個事件）** | 擴充套件後的 hook 系統，包含 5 類 | command、http、mcp_tool、prompt、agent hook 型別 |
| **MCP Elicitation** | MCP server 可在執行時請求使用者輸入 | 當 server 需要澄清時自動提示 |
| **WebSocket MCP** | MCP 的 WebSocket 傳輸 | 在 `.mcp.json` 中設定 `ws://` URL |
| **Plugin LSP** | 外掛支援 Language Server Protocol | `userConfig`、`${CLAUDE_PLUGIN_DATA}` 變數 |
| **Remote Control** | 從 claude.ai 或 Claude 應用操控本地會話 | `claude --remote-control`（會話內可用 `/remote-control`） |
| **Web Sessions** | claude.ai/code 上的雲端會話 | 在終端中用 `claude --cloud "task"` 啟動 |
| **Desktop App** | 原生桌面應用程式 | 從 claude.ai/download 下載 |
| **Task List** | 管理後臺任務 | `/tasks`（別名 `/bashes`） |
| **Auto Memory** | 從對話中自動儲存記憶 | Claude 將筆記儲存到 `~/.claude/projects/<project>/memory/MEMORY.md`；用 `/memory` 管理 |
| **Git Worktrees** | 用於並行開發的隔離工作區 | `claude --worktree <name>`（或 `-w`） |
| **Model Selection** | 在 Fable 5.1、Fable 5、Opus 5、Sonnet 5.5、Sonnet 5、Sonnet 4.6、Opus 4.8 和 Haiku 4.5 之間切換 | `/model` 或 `--model` 引數（在 Anthropic API 上 `sonnet` 指向 Sonnet 5.5，v2.1.284+） |
| **Agent Teams** | 協調多個 agent 執行任務 | 透過環境變數 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 啟用（實驗性） |
| **Scheduled Tasks** | 使用 `/loop` 執行週期任務 | `/loop 5m /command` 或 CronCreate 工具 |
| **Chrome Integration** | 瀏覽器自動化 | `--chrome` 引數或 `/chrome` 命令 |
| **Keyboard Customization** | 自訂按鍵繫結 | `/keybindings` 命令 |

---

## 💡 小技巧

### 自訂
- 先原樣使用範例
- 再按需求修改
- 分享給團隊前先測試
- 對設定做版本控制

### 最佳實踐
- 用 memory 儲存團隊規範
- 用 plugins 做完整工作流程
- 用 subagents 處理複雜任務
- 用 slash commands 處理快速任務

### 故障排查
```bash
# 檢查檔案位置
ls -la .claude/commands/
ls -la .claude/agents/

# 驗證 YAML 語法
head -20 .claude/agents/code-reviewer.md

# 測試 MCP 連線
echo $GITHUB_PERSONAL_ACCESS_TOKEN
```

---

## 📊 功能矩陣

| 需求 | 用這個 | 範例 |
|------|--------|------|
| 快速快捷操作 | Slash Command（55+） | `01-slash-commands/optimize.md` |
| 團隊規範 | Memory | `02-memory/project-CLAUDE.md` |
| 自動化工作流程 | Skill | `03-skills/code-review-specialist/` |
| 專門任務 | Subagent | `04-subagents/code-reviewer.md` |
| 外部資料 | MCP（+ Elicitation、WebSocket） | `05-mcp/github-mcp.json` |
| 事件自動化 | Hook（33 個事件、5 類） | `06-hooks/pre-commit.sh` |
| 完整方案 | Plugin（+ LSP 支援） | `07-plugins/pr-review/` |
| 安全實驗 | Checkpoint | `08-checkpoints/checkpoint-examples.md` |
| 完全自治 | Auto Mode | `--enable-auto-mode` 或 `Shift+Tab` |
| 聊天整合 | Channels | `--channels`（Discord、Telegram） |
| CI/CD 管線 | CLI | `10-cli/README.md` |

---

## 🔗 快速連結

- **主指南**：`README.md`
- **完整索引**：`INDEX.md`
- **速查卡**：`QUICK_REFERENCE.md`
- **原始指南**：`claude_concepts_guide.md`

---

## 📞 常見問題

**問：我應該先用哪個？**
答：先從 slash commands 開始，按需逐步新增功能。

**問：我可以混用多個功能嗎？**
答：可以！它們可以一起工作。Memory + Commands + MCP 很強大。

**問：怎麼分享給團隊？**
答：把 `.claude/` 目錄提交到 git。

**問：敏感資訊怎麼辦？**
答：用環境變數，不要硬編碼。

**問：我可以改這些範例嗎？**
答：當然可以！它們本來就是可客製化的模板。

---

## ✅ 檢查清單

入門清單：

- [ ] 閱讀 `README.md`
- [ ] 安裝 1 個 slash command
- [ ] 試用該命令
- [ ] 建立專案 `CLAUDE.md`
- [ ] 安裝 1 個 subagent
- [ ] 設定 1 個 MCP 整合
- [ ] 安裝 1 個 skill
- [ ] 試用一個完整外掛
- [ ] 按你的需求客製化
- [ ] 與團隊共享

---

**快速開始**：`cat README.md`

**完整索引**：`cat INDEX.md`

**這張卡片**：建議隨手保留，方便快速查閱！

---

**最後更新**：2026 年 10 月 26 日
**Claude Code 版本**：2.1.310
**來源**：
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/cli-reference
- https://code.claude.com/docs/en/remote-control
- https://code.claude.com/docs/en/agent-teams
- https://code.claude.com/docs/en/memory#storage-location
- https://code.claude.com/docs/en/permission-modes
- https://code.claude.com/docs/en/managed-settings
- https://code.claude.com/docs/en/scheduled-tasks
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/headless
- https://code.claude.com/docs/en/permission-modes#tool-calls-denied-in-claude-p-and-agent-sdk-runs
