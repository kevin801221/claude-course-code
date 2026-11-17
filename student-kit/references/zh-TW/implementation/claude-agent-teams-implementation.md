# Agent Teams 實作

![Last Updated](https://img.shields.io/badge/Last_Updated-Mar_12%2C_2026-white?style=flat&labelColor=555)

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`implementation/claude-agent-teams-implementation.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/implementation/claude-agent-teams-implementation.md)

---

<a href="#time-orchestration"><img src="../!/tags/implemented-hd.svg" alt="Implemented"></a>

<p align="center">
  <img src="../implementation/assets/impl-agent-teams.png" alt="Agent Teams 實際運作 —— 搭配 tmux 的分割窗格模式" width="100%">
</p>

Agent Teams 會生成**多個獨立的 Claude Code session**，透過共享任務清單協調。與子代理（單一 session 內的隔離脈絡分支）不同，每個隊友都有自己完整的脈絡視窗，並自動載入 CLAUDE.md、MCP server 與 skills。

---

## ![How to Use](../%21/tags/how-to-use.svg)

這個時間編排工作流完全由一個 agent team 建造。要執行成品：

```bash
cd agent-teams
claude
/time-orchestrator
```

這會啟動 **Command → Agent → Skill** 管線：代理抓取杜拜當前時間，skill 則把 SVG 時間卡片輸出到 `agent-teams/output/dubai-time.svg`。

---

## ![How to Implement](../%21/tags/how-to-implement.svg)

你可以用 agent teams 複製一份天氣編排工作流 —— 在這個例子中，時間編排工作流完全由一個 agent team 建造。

### 1. 安裝 [iTerm2](https://iterm2.com/) 與 tmux

```bash
brew install --cask iterm2
brew install tmux
```

### 2. 啟動 iTerm2 → tmux → Claude

```bash
tmux new -s dev
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude
```

### 3. 用團隊結構下 prompt

<a id="time-orchestration"></a>

把這段 prompt 貼進 Claude，用 agent teams 啟動一個完整的時間編排工作流：

主 prompt：**[agent-teams-prompt.md](https://github.com/kevin801221/claude-code-best-practice/blob/main/agent-teams/agent-teams-prompt.md)**

### 團隊協調流程

```
┌──────────────────────────────────────────────────────────────┐
│                         領隊（你）                             │
│       「建立一個 agent team 來打造時間編排工作流」                │
└──────────────────────────┬───────────────────────────────────┘
                           │ 生成團隊（全部平行）
              ┌────────────┼────────────┐
              ▼            ▼            ▼
   ┌────────────────┐ ┌──────────┐ ┌──────────────┐
   │ Command        │ │ Agent    │ │ Skill        │
   │ Architect      │ │ Engineer │ │ Designer     │
   │                │ │          │ │              │
   │ agent-teams/   │ │ agent-   │ │ agent-teams/ │
   │ .claude/       │ │ teams/   │ │ .claude/     │
   │ commands/      │ │ .claude/ │ │ skills/      │
   │ time-          │ │ agents/  │ │ time-svg-    │
   │ orchestrator.md│ │ time-    │ │ creator/     │
   │                │ │ agent.md │ │              │
   └───────┬────────┘ └────┬─────┘ └──────┬───────┘
           │               │              │
           ▼               ▼              ▼
   ┌──────────────────────────────────────────────────┐
   │              共享任務清單                          │
   │  ☐ 議定資料契約：{time, tz, formatted}            │
   │  ☐ Command 使用 Agent 工具（不是 bash）           │
   │  ☐ Agent 預載 time-fetcher skill                 │
   │  ☐ Skill 從脈絡讀時間（不重抓）                    │
   │  ☐ 所有檔案都在 agent-teams/.claude/ 內           │
   └──────────────────────────────────────────────────┘
                       │
                       ▼
          ┌──────────────────────────────┐
          │  cd agent-teams && claude    │
          │    /time-orchestrator        │
          │   Command → Agent → Skill    │
          └──────────────────────────────┘
```
