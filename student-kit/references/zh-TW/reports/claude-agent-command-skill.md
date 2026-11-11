# Agents vs Commands vs Skills —— 什麼時候用哪個

Claude Code 三種擴充機制的比較：子代理（subagents）、命令（commands）與 skills。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`reports/claude-agent-command-skill.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/reports/claude-agent-command-skill.md)

![slash 選單顯示 time-skill、time-command 與 time-agent](https://raw.githubusercontent.com/kevin801221/claude-code-zh-tw/9c6e34d69eee8cf634bbf269df5f812b6e13e987/reports/assets/agent-command-skill-1.jpg)

---

## 一覽表

| | Agent | Command | Skill |
|---|---|---|---|
| **位置** | `.claude/agents/<name>.md` | `.claude/commands/<name>.md` | `.claude/skills/<name>/SKILL.md` |
| **脈絡** | 獨立子代理行程 | 行內（主對話） | 行內（主對話） |
| **使用者可呼叫** | 不在 `/` 選單 —— 由 Claude 或透過 Agent 工具呼叫 | 可以 —— `/command-name` | 可以 —— `/skill-name`（除非 `user-invocable: false`） |
| **Claude 可自動呼叫** | 可以 —— 透過 `description` 欄位 | 不行 | 可以 —— 透過 `description` 欄位（除非 `disable-model-invocation: true`） |
| **接受引數** | 透過 `prompt` 參數 | `$ARGUMENTS`、`$0`、`$1` | `$ARGUMENTS`、`$0`、`$1` |
| **動態脈絡注入** | 不行 | 可以 —— `` !`command` `` | 可以 —— `` !`command` `` |
| **自己的脈絡視窗** | 有 —— 隔離 | 沒有 —— 共用主脈絡 | 沒有 —— 共用主脈絡（除非 `context: fork`） |
| **模型覆寫** | `model:` frontmatter | `model:` frontmatter | `model:` frontmatter |
| **工具限制** | `tools:` / `disallowedTools:` | `allowed-tools:` | `allowed-tools:` |
| **Hooks** | `hooks:` frontmatter | — | `hooks:` frontmatter |
| **記憶** | `memory:` frontmatter（user/project/local） | — | — |
| **可預載 skills** | 可以 —— `skills:` frontmatter | — | — |
| **MCP servers** | `mcpServers:` frontmatter | — | — |

---

## 各自該在什麼時候用

### 在這些情況用 Agent：

- 任務是**自主且多步驟**的 —— 代理需要在沒有持續指引下探索、決策並行動
- 你需要**脈絡隔離** —— 這些工作不該污染主對話視窗
- 代理需要跨 session 的**持久記憶**（例如一個會學習模式的 code reviewer）
- 你想透過 skills **預載領域知識**而不把主脈絡塞滿
- 任務適合**在背景執行**或在 **git worktree** 中執行
- 你需要**工具限制**或**不同的權限模式**（例如 `acceptEdits`、`plan`）

**範例**：`weather-agent` —— 用它預載的 `weather-fetcher` skill 自主抓取天氣資料，在獨立脈絡中以受限工具執行。

### 在這些情況用 Command：

- 你需要一個**使用者主動觸發的進入點** —— 由使用者明確觸發的工作流
- 這個工作流涉及**編排**其他代理或 skills
- 你想**讓脈絡保持精簡** —— 命令內容在使用者觸發之前不會注入 session 脈絡

**範例**：`weather-orchestrator` —— 使用者觸發它，它詢問攝氏／華氏偏好，呼叫代理，接著呼叫 SVG skill。

### 在這些情況用 Skill：

- 你希望 **Claude 依使用者意圖自動呼叫** —— skill 的 description 會被注入 session 脈絡做語意比對
- 任務是一個**可重複使用的程序**，能從多處被呼叫（命令、代理，或 Claude 自己）
- 你需要**代理預載** —— 在啟動時把領域知識烤進特定代理

**範例**：`weather-svg-creator` —— 使用者要天氣卡片時 Claude 會自動呼叫它；也能從命令中呼叫。

---

## Command → Agent → Skill 架構

這個 repository 示範了一種分層編排模式：

```
使用者觸發 /command
    ↓
Command 編排工作流
    ↓
Command 呼叫 Agent（獨立脈絡、自主）
    ↓
Agent 使用預載的 Skill（領域知識）
    ↓
Command 呼叫 Skill（行內，用於產生輸出）
```

**具體範例** —— 天氣系統：

```
/weather-orchestrator（command —— 進入點，詢問 C/F）
    ↓
weather-agent（agent —— 自主抓取溫度）
    ├── weather-fetcher（agent skill —— 預載的 API 指令）
    ↓
weather-svg-creator（skill —— 行內產生 SVG）
```

---

## Frontmatter 比較

### Agent Frontmatter

```yaml
---
name: my-agent
description: Use this agent PROACTIVELY when...
tools: Read, Write, Edit, Bash
model: sonnet
maxTurns: 10
permissionMode: acceptEdits
memory: user
skills:
  - my-skill
---
```

### Command Frontmatter

```yaml
---
description: Do something useful
argument-hint: [issue-number]
allowed-tools: Read, Edit, Bash(gh *)
model: sonnet
---
```

### Skill Frontmatter

```yaml
---
name: my-skill
description: Do something when the user asks for...
argument-hint: [file-path]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob
model: sonnet
context: fork
agent: general-purpose
---
```

---

## 關鍵差異

### 自動呼叫

| 機制 | Claude 能自動呼叫嗎？ | 如何阻止 |
|-----------|------------------------|----------------|
| Agent | 可以 —— 透過 `description`（用 "PROACTIVELY" 鼓勵它） | 移除或淡化 description |
| Command | 不行 —— 永遠由使用者透過 `/` 發起 | 不適用 |
| Skill | 可以 —— 透過 `description` | 設 `disable-model-invocation: true` |

### 在 `/` 選單中的可見性

| 機制 | 會出現在 `/` 選單嗎？ | 如何隱藏 |
|-----------|---------------------|-------------|
| Agent | 不會 | 不適用 |
| Command | 會 —— 一律出現 | 無法隱藏 |
| Skill | 會 —— 預設出現 | 設 `user-invocable: false` |

### 脈絡隔離

| 機制 | 在自己的脈絡中執行？ | 如何設定 |
|-----------|---------------------|-----------------|
| Agent | 一律是 | 內建行為 |
| Command | 從不 | 不適用 |
| Skill | 可選 | 設 `context: fork` |

---

## 實例演練：「現在幾點？」

這個 repository 為同一個任務（顯示 PKT 當前時間）定義了全部三種機制。當使用者打 **"What is the current time?"** 而沒有明確呼叫任何 `/` 命令時，會發生什麼：

| 機制 | 會觸發嗎？ | 為什麼會／不會 |
|-----------|--------------|---------------|
| `time-command` | 不會 | 命令**從不自動呼叫**。使用者必須明確輸入 `/time-command` 它才會執行。命令沒有自動探索途徑 —— 嚴格由使用者發起。 |
| `time-agent` | **會**（有可能） | 代理的 `description` 說 *「Use this agent to display the current time in Pakistan Standard Time」*。Claude 把它與使用者意圖比對後，可能透過 Agent 工具生成它。不過代理跑在**獨立的脈絡視窗**，對這種簡單任務來說過重了。 |
| `time-skill` | **會**（最可能） | skill 的 `description` 說 *「Display the current time in Pakistan Standard Time (PKT, UTC+5). Use when the user asks for the current time, Pakistan time, or PKT.」*。Claude 比對到之後會透過 Skill 工具呼叫它。因為它**行內**執行且沒有脈絡開銷，是最有效率的選擇。 |

### 解析順序

當多個機制都符合同一個意圖時，Claude 偏好能滿足需求的**最輕量選項**：

```
1. Skill（行內、無脈絡開銷）           ← 優先
2. Agent（獨立脈絡、自主）              ← 當 skill 不可用或任務複雜時使用
3. Command（從不 —— 需要明確打 /）      ← 只有使用者輸入 /time-command 才會
```

### 如果 skill 設了 `disable-model-invocation: true` 會怎樣？

那 Claude 就**無法**自動呼叫該 skill。代理成了唯一能自動呼叫的選項，所以 Claude 會改生成 `time-agent` —— 代價是為一行 bash 命令開一個獨立脈絡視窗。

### 如果 skill 和 agent 都停用自動呼叫會怎樣？

那就**什麼都不會自動觸發**。Claude 會退回自己的一般知識，大概會直接跑 `TZ='Asia/Karachi' date` —— 完全沒有用到任何擴充機制。使用者得明確輸入 `/time-command` 或 `/time-skill` 才用得到。

![使用者問「What is the current time?」時 Claude 自動呼叫 time-skill](https://raw.githubusercontent.com/kevin801221/claude-code-zh-tw/9c6e34d69eee8cf634bbf269df5f812b6e13e987/reports/assets/agent-command-skill-2.png)

---

## 資料來源

- [Claude Code Skills — Docs](https://code.claude.com/docs/en/skills)
- [Claude Code Sub-agents — Docs](https://code.claude.com/docs/en/sub-agents)
- [Claude Code Slash Commands — Docs](https://code.claude.com/docs/en/slash-commands)
- [Skills 最佳實踐](../best-practice/claude-skills.md)
- [Commands 最佳實踐](../best-practice/claude-commands.md)
- [子代理最佳實踐](../best-practice/claude-subagents.md)
