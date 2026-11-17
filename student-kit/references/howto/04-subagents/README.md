<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Subagents 完整參考

## 概覽

Subagents 是專門處理某類任務的獨立 AI 助手。它們擁有隔離的上下文、自己的提示詞和工具許可權，適合把複雜工作拆分給不同角色。

## 主要好處

- 上下文隔離
- 角色分工清晰
- 適合並行和委派
- 便於把複雜任務拆開

## 檔案位置

- 專案級：`.claude/agents/`
- 使用者級：`~/.claude/agents/`

## 設定

### 檔案格式

Subagent 通常是一個帶 frontmatter 的 Markdown 檔案。

```yaml
---
name: code-reviewer
description: 審查程式碼品質和安全問題
tools: Read, Grep, Bash
---

# Code Reviewer
```

### 設定欄位

| 欄位 | 說明 |
|------|------|
| `name` | subagent 名稱 |
| `description` | 何時該呼叫它 |
| `tools` | 允許使用的工具。MCP：`mcp__<server>__*` 授予整個伺服器的工具（v2.1.299+：只匹配完全相同的伺服器名） |
| `model` | 指定模型 |
| `prompt` | 任務提示詞 |
| `context` | 上下文策略 |

### 工具設定選項

- 只讀審查
- 限制 Bash
- 允許更強工具集

### 基於 CLI 的設定

你也可以透過命令列或設定檔案定義 subagent。

## 內建 Subagents

Claude Code 自帶一些常見角色，例如：

- 通用助手
- Planning agent
- Explore agent
- claude 兜底 agent
- Statusline 相關 agent
- claude-code-guide agent

## 管理 Subagents

### 使用 `/agents` 命令（推薦）

> **注意**：`/agents` 互動式嚮導已在 v2.1.198 中移除，且自 v2.1.281 起 `/agents` 不再出現在 `/` 選單或 `/help` 中。請讓 Claude 建立或管理 subagent（例如“建立一個審查安全問題的 subagent”），或直接新增 `.claude/agents/<name>.md` 檔案。

```text
建立一個審查程式碼安全漏洞的 subagent。
```

Claude 會為你寫好 `.claude/agents/<name>.md` 檔案，並選擇合適的 frontmatter（工具、模型、描述）。之後你可以手動調整該檔案，或讓 Claude 修改。

### 直接管理檔案

#### 建立專案 subagent

```bash
mkdir -p .claude/agents
```

#### 建立使用者 subagent

```bash
mkdir -p ~/.claude/agents
```

## 使用 Subagents

### 自動委派

主 agent 可以根據任務描述自動把工作分配給合適的 subagent。

### 顯式呼叫

你也可以明確讓 Claude 使用某個 subagent。

### `@` 提及呼叫

在一些場景裡，可以透過 `@agent-name` 方式引用。

### 會話級 agent

可以在整個會話中固定使用某個 agent。

### 列出可用 agents

要檢視已設定的 subagents，可以詢問 Claude，或瀏覽 `.claude/agents/` 和 `~/.claude/agents/`。（`claude agents` 與此無關：它開啟用於後臺會話的 agent view。）

## 可恢復的 agents

某些 subagent 可以先啟動，之後再恢復，便於長任務接力。

## 串聯 Subagents

複雜任務裡可以讓多個 subagent 依次協作，例如：

1. 程式碼審查
2. 測試生成
3. 文件更新

## Subagents 的持久記憶

Subagents 可以擁有自己的 memory 範圍，讓它們在各自職責內保持一致。

### Memory 範圍

- 專案級
- 使用者級
- 子目錄級

### 工作方式

Subagent 會在自己的上下文中讀取對應記憶，不和主會話完全混在一起。

## 後臺 Subagents

### 設定

有些 subagent 可以作為後臺任務執行，不阻塞主會話。

### 快捷鍵

在支援的介面中，可用快捷鍵檢視或切換後臺 subagent。

### 關閉後臺任務

如果你不想讓任務後臺執行，可以在設定中關閉。

## Worktree 隔離

### 設定

可以為 subagent 分配獨立的 worktree。

### 工作方式

這樣不同任務就不會互相汙染檔案狀態。

## 限制可啟動的 Subagents

你可以限制 Claude 只能 spawn 某些 subagent，以降低風險。

### 範例

- 只允許審查類 agent
- 禁止高風險自動化 agent

## `claude agents` CLI 命令

`claude agents` 開啟 **agent view**（v2.1.139+）：按狀態分組的後臺會話全屏列表。它不會列出已設定的 subagent 定義；可用 `claude agents --json` 以指令碼方式讀取會話狀態。

## Agent Teams（實驗性）

Agent teams 是更高階的協作模式，適合多個 subagent 並行處理複雜任務。

### Subagents vs Agent Teams

- Subagents 側重委派單個任務
- Agent teams 側重多角色協作

### 啟用 Agent Teams

透過設定開啟實驗性功能。

### 啟動團隊

團隊模式會把不同任務分配給不同角色。

### 顯示模式

可以選擇更適合終端或圖形介面的顯示方式。

### 導航

你可以在 team 中切換角色、檢視狀態和讀取訊息。

### 團隊設定

適合為大型流程定義清晰角色。

### 架構

agent team 本質上是多個專門角色圍繞同一任務協作。

### 任務分配與訊息

主 agent 會負責把任務拆分並轉發給對應 subagent。

### 計劃審批流程

如果是 plan 驅動流程，團隊會先審計劃再執行。

### 團隊相關 hook 事件

一些 hook 可以在 team 生命週期裡觸發。

### 最佳實踐

- 角色定義要清楚
- 任務邊界要明確
- 不要讓多個 agent 做重複工作

### 侷限

- 實驗性功能可能會變化
- 複雜團隊需要更多設定

## 外掛中的 Subagent 安全

外掛分發的 subagent 要特別注意許可權、工具範圍和邊界條件。

## 架構

### 高層架構

主 agent、subagent、檔案系統和工具許可權共同構成執行鏈。

### 生命週期

1. 建立
2. 分配任務
3. 執行
4. 返回結果
5. 結束或恢復

## 上下文管理

### 關鍵點

- 子上下文儘量小
- 讓每個 subagent 只負責自己的事
- 避免把所有資訊都塞進去

### 效能考慮

過多的上下文會拖慢速度並降低準確性。

### 關鍵行為

subagent 在隔離上下文裡工作，但仍能把結果彙總回主會話。

## 什麼時候使用 Subagents

- 任務可拆分
- 需要隔離上下文
- 需要明確角色分工
- 需要並行協作

## 最佳實踐

### 設計原則

- 單一職責
- 描述明確
- 工具許可權最小化

### System Prompt 最佳實踐

- 任務說明要具體
- 不要寫太長
- 只保留執行任務所需的資訊

### 工具訪問策略

- 審查型 subagent 只讀
- 實現型 subagent 適度開放寫許可權
- 高風險動作要保持審批

## 本目錄中的範例 Subagents

### 1. [Code Reviewer](code-reviewer.md)

用於全面程式碼品質審查。

### 2. [Test Engineer](test-engineer.md)

用於測試策略、覆蓋率和測試生成。

### 3. [Documentation Writer](documentation-writer.md)

用於技術文件寫作和更新。

### 4. [Secure Reviewer](secure-reviewer.md)

用於安全檢查，通常只讀。

### 5. [Implementation Agent](implementation-agent.md)

用於功能實現和程式碼修改。

### 6. [Debugger](debugger.md)

用於定位 bug 和分析異常。

### 7. [Data Scientist](data-scientist.md)

用於分析資料、解釋結果和生成報告。

### 8. [Clean Code Reviewer](clean-code-reviewer.md)

用於按 Clean Code 原則做專門審查。

## 安裝說明

### 方法 1：使用 `/agents`

> **注意**：`/agents` 互動式嚮導已在 v2.1.198 中移除，且自 v2.1.281 起 `/agents` 不再出現在 `/` 選單或 `/help` 中。請讓 Claude 建立或管理 subagent（例如“建立一個審查安全問題的 subagent”），或直接新增 `.claude/agents/<name>.md` 檔案。

```text
建立一個專案級 subagent，用於執行測試並修復失敗。
給它 Bash、Read、Edit 和 Grep 的訪問許可權。
```

Claude 會寫入帶有合適 frontmatter 的 `.claude/agents/<name>.md`。檢查生成的檔案後即可使用。

### 方法 2：複製到專案

```bash
mkdir -p .claude/agents
cp 04-subagents/*.md .claude/agents/
```

### 方法 3：複製到使用者目錄

```bash
mkdir -p ~/.claude/agents
cp 04-subagents/*.md ~/.claude/agents/
```

### 驗證

- 讓 Claude 建立一個 subagent，或直接新增 `.claude/agents/<name>.md` 檔案
- 列出目錄，確認 agent 檔案已就位：`ls .claude/agents/`
- 也可以詢問 Claude 當前會話中有哪些可用的 subagent，它會報告可委派的內建與自訂 agent
- 試著讓 Claude 委派一個簡單任務

## 檔案結構

```text
.claude/agents/
├── clean-code-reviewer.md
├── code-reviewer.md
├── data-scientist.md
├── debugger.md
├── documentation-writer.md
├── implementation-agent.md
├── secure-reviewer.md
├── test-engineer.md
└── README.md
```

## 相關概念

- [Skills 中文指南](../03-skills/README.md)
- [Memory 中文指南](../02-memory/README.md)
- [Hooks 中文指南](../06-hooks/README.md)
- [Plugins 中文指南](../07-plugins/README.md)

---

**最後更新**: 2026 年 10 月 15 日
**Claude Code 版本**: 2.1.300
**來源**:
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/cli-reference
- https://code.claude.com/docs/en/agent-view
- https://code.claude.com/docs/en/sub-agents#permission-modes
- https://code.claude.com/docs/en/sub-agents#available-tools
