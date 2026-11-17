# Claude Code：全域 vs 專案層級功能

完整比較哪些 Claude Code 功能只存在於全域（`~/.claude/`），哪些同時有全域與專案層級（`.claude/`）的對應版本。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`reports/claude-global-vs-project-settings.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/reports/claude-global-vs-project-settings.md)

## 目錄

1. [概觀](#概觀)
2. [僅限全域的功能](#僅限全域的功能)
3. [雙範圍功能](#雙範圍功能)
4. [設定優先順序](#設定優先順序)
5. [目錄結構比較](#目錄結構比較)
6. [Tasks 系統](#tasks-系統)
7. [Agent Teams](#agent-teams)
8. [設計原則](#設計原則)
9. [資料來源](#資料來源)

---

## 概觀

Claude Code 使用一套**範圍階層**：有些功能同時存在於全域（`~/.claude/`）與專案（`.claude/`）層級，有些則只存在於全域。設計原則是：屬於*個人狀態*或*跨專案協調*的東西放全域；屬於*可由團隊共享的專案設定*則可以放在專案層級。

- `~/.claude/` 是你的**使用者層級家目錄**（全域，所有專案）
- repo 內的 `.claude/` 是你的**專案層級家目錄**（僅限該專案）

---

## 僅限全域的功能

這些**只**存在於 `~/.claude/` 底下，無法限定到某個專案：

| 功能 | 位置 | 用途 |
|---------|----------|---------|
| **Tasks** | `~/.claude/tasks/` | 跨 session 與跨代理的持久任務清單 |
| **Agent Teams** | `~/.claude/teams/` | 多代理協調設定（實驗性，2026 年 2 月） |
| **Auto Memory** | `~/.claude/projects/<hash>/memory/` | Claude 為每個專案自行寫下的學習（個人，永不共享） |
| **憑證與 OAuth** | 系統 keychain + `~/.claude.json` | API key、OAuth token（永不放在專案檔案中） |
| **Keybindings** | `~/.claude/keybindings.json` | 自訂鍵盤快捷鍵 |
| **MCP 使用者 server** | `~/.claude.json`（`mcpServers` 鍵） | 跨所有專案的個人 MCP server |
| **偏好／快取** | `~/.claude.json` | 主題、模型、輸出風格、session 狀態 |

---

## 雙範圍功能

這些在兩個層級都存在，且**專案層級優先於**全域：

| 功能 | 全域（`~/.claude/`） | 專案（`.claude/`） | 優先順序 |
|---------|----------------------|---------------------|------------|
| **CLAUDE.md** | `~/.claude/CLAUDE.md` | `./CLAUDE.md` 或 `.claude/CLAUDE.md` | 專案覆寫全域 |
| **設定** | `~/.claude/settings.json` | `.claude/settings.json` + `.claude/settings.local.json` | 專案 > 全域 |
| **Rules** | `~/.claude/rules/*.md` | `.claude/rules/*.md` | 專案覆寫 |
| **Agents／子代理** | `~/.claude/agents/*.md` | `.claude/agents/*.md` | 專案覆寫 |
| **Commands** | `~/.claude/commands/*.md` | `.claude/commands/*.md` | 兩者皆可用 |
| **Skills** | `~/.claude/skills/` | `.claude/skills/` | 兩者皆可用 |
| **Hooks** | `~/.claude/hooks/` | `.claude/hooks/` | 兩者都會執行 |
| **MCP Servers** | `~/.claude.json`（使用者範圍） | `.mcp.json`（專案範圍） | 三種範圍：local > project > user |

---

## 設定優先順序

使用者可寫的設定依下列覆寫順序套用（由高到低）：

| 優先序 | 位置 | 範圍 | 版本控制 | 用途 |
|----------|----------|-------|-----------------|---------|
| 1 | 命令列旗標 | Session | 不適用 | 單一 session 覆寫 |
| 2 | `.claude/settings.local.json` | 專案 | 否（git-ignored） | 個人的專案專屬設定 |
| 3 | `.claude/settings.json` | 專案 | 是（已 commit） | 團隊共享設定 |
| 4 | `~/.claude/settings.local.json` | 使用者 | 不適用 | 個人全域覆寫 |
| 5 | `~/.claude/settings.json` | 使用者 | 不適用 | 全域個人設定 |

政策層：`managed-settings.json` 由組織強制套用，無法被本機檔案覆寫。

**重要**：`deny` 規則擁有最高的安全優先權，無法被優先序較低的 allow／ask 規則覆寫。

---

## 目錄結構比較

### 全域範圍（`~/.claude/`）

```
~/.claude/
├── settings.json              # 使用者層級設定（所有專案）
├── settings.local.json        # 個人覆寫
├── CLAUDE.md                  # 使用者記憶（所有專案）
├── agents/                    # 使用者子代理（所有專案可用）
│   └── *.md
├── rules/                     # 使用者層級模組化規則
│   └── *.md
├── commands/                  # 使用者層級命令
│   └── *.md
├── skills/                    # 使用者層級 skills
│   └── */SKILL.md
├── tasks/                     # 僅限全域：任務清單
│   └── {task-list-id}/
├── teams/                     # 僅限全域：agent team 設定
│   └── {team-name}/
│       └── config.json
├── projects/                  # 僅限全域：各專案的 auto-memory
│   └── {project-hash}/
│       └── memory/
│           ├── MEMORY.md
│           └── *.md
├── keybindings.json           # 僅限全域：鍵盤快捷鍵
└── hooks/                     # 使用者層級 hooks
    ├── scripts/
    └── config/

~/.claude.json                 # 僅限全域：MCP server、OAuth、偏好、快取
```

### 專案範圍（`.claude/`）

```
.claude/
├── settings.json              # 團隊共享設定
├── settings.local.json        # 個人專案覆寫（git-ignored）
├── CLAUDE.md                  # 專案記憶（./CLAUDE.md 的替代位置）
├── agents/                    # 專案子代理
│   └── *.md
├── rules/                     # 專案層級模組化規則
│   └── *.md
├── commands/                  # 自訂 slash command
│   └── *.md
├── skills/                    # 自訂 skills
│   └── {skill-name}/
│       ├── SKILL.md
│       └── supporting-files/
├── hooks/                     # 專案層級 hooks
│   ├── scripts/
│   └── config/
└── plugins/                   # 已安裝的外掛

.mcp.json                      # 專案範圍的 MCP server（repo 根目錄）
```

---

## Tasks 系統

於 **Claude Code v2.1.16**（2026 年 1 月 22 日）引入，取代已淘汰的 TodoWrite 系統。

### 儲存

Tasks 儲存在本機檔案系統的 `~/.claude/tasks/`（不在雲端資料庫）。這讓任務狀態可稽核、可納入版控，且當機後可復原。

### 工具

| 工具 | 用途 |
|------|---------|
| **TaskCreate** | 以 `subject`、`description` 與 `activeForm` 建立新任務 |
| **TaskGet** | 依 ID 取得特定任務的完整細節 |
| **TaskUpdate** | 變更狀態、設定負責人、新增相依關係或刪除 |
| **TaskList** | 列出所有任務及其當前狀態 |

### 任務生命週期

```
pending  →  in_progress  →  completed
```

### 相依關係管理

任務可透過 `addBlockedBy`／`addBlocks` 阻擋其他任務，形成相依圖以防止過早執行。

### 多 Session 協作

```bash
CLAUDE_CODE_TASK_LIST_ID=my-project-tasks claude
```

共享同一個 ID 的所有 session 都能即時看到任務更新，支援平行工作流與 session 接續。

### 與舊版 Todos 的主要差異

| 功能 | 舊版 Todos | 新版 Tasks |
|---------|-----------|-----------|
| 範圍 | 單一 session | 跨 session、跨代理 |
| 相依關係 | 無 | 完整相依圖 |
| 儲存 | 僅在記憶體 | 檔案系統（`~/.claude/tasks/`） |
| 持久性 | session 結束即消失 | 可跨重啟與當機存活 |
| 多 session | 不可能 | 透過 `CLAUDE_CODE_TASK_LIST_ID` |

---

## Agent Teams

於 **2026 年 2 月 5 日**以實驗功能發布。Agent Teams 讓多個 Claude Code session 能協調處理共享工作。

### 啟用方式

```json
// 在 ~/.claude/settings.json 中
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### 設定

團隊設定放在 `~/.claude/teams/{team-name}/`，支援兩種模式：

| 模式 | 說明 | 需求 |
|------|-------------|--------------|
| **In-process**（預設） | 所有隊友都在你的終端機內執行 | 無 |
| **Split panes** | 每個隊友有自己的窗格 | tmux 或 iTerm2（VS Code 終端機不行） |

---

## 設計原則

「僅限全域 vs 雙範圍」的切分遵循清楚的模式：

| 類別 | 範圍 | 理由 |
|----------|-------|-----------|
| **協調狀態**（tasks、teams） | 僅限全域 | 需要跨越任何單一專案而持續存在 |
| **安全狀態**（憑證、OAuth） | 僅限全域 | 防止不小心 commit 進版控 |
| **個人學習**（auto-memory） | 僅限全域 | 屬於特定使用者，不可團隊共享 |
| **輸入偏好**（keybindings） | 僅限全域 | 使用者的肌肉記憶，與專案無關 |
| **設定**（settings、rules、agents） | 兩個層級 | 團隊需要共享專案專屬行為 |
| **工作流定義**（commands、skills） | 兩個層級 | 可以是個人的，也可以是團隊共享的 |

Auto-memory（`~/.claude/projects/<hash>/memory/`）是個值得注意的混合體：它*關於*特定專案，卻儲存在*全域*，因為它代表的是個人學習而非可團隊共享的設定。

---

## 資料來源

- [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings)
- [Orchestrate Teams of Claude Code Sessions](https://code.claude.com/docs/en/agent-teams)
- [What are Tasks in Claude Code - ClaudeLog](https://claudelog.com/faqs/what-are-tasks-in-claude-code/)
- [Claude Code Task Management - ClaudeFast](https://claudefa.st/blog/guide/development/task-management)
- [Claude Code Tasks Update - VentureBeat](https://venturebeat.com/orchestration/claude-codes-tasks-update-lets-agents-work-longer-and-coordinate-across)
- [Where Are Claude Code Global Settings - ClaudeLog](https://claudelog.com/faqs/where-are-claude-code-global-settings/)
- [Claude Opus 4.6 Agent Teams - VentureBeat](https://venturebeat.com/technology/anthropics-claude-opus-4-6-brings-1m-token-context-and-agent-teams-to-take)
- [How to Set Up Claude Code Agent Teams (Full Walkthrough) - r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1qz8tyy/how_to_set_up_claude_code_agent_teams_full/)
- [Anthropic replaced Claude Code's old 'Todos' with Tasks - r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/comments/1qkjznp/anthropic_replaced_claude_codes_old_todos_with/)
