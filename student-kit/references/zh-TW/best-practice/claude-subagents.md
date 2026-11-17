# 子代理（Sub-agents）最佳實踐

![Last Updated](https://img.shields.io/badge/Last_Updated-Nov%2005%2C%202026%2011%3A33%20AM%20PKT-white?style=flat&labelColor=555) ![Version](https://img.shields.io/badge/Claude_Code-v2.1.318-blue?style=flat&labelColor=555)<br>
[![Implemented](https://img.shields.io/badge/Implemented-2ea44f?style=flat)](../implementation/claude-subagents-implementation.md)

Claude Code 子代理 —— frontmatter 欄位與官方內建代理類型。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`best-practice/claude-subagents.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-subagents.md)

---

## Frontmatter 欄位（16 個）

| 欄位 | 型別 | 必填 | 說明 |
|-------|------|----------|-------------|
| `name` | string | 是 | 唯一識別名，使用小寫字母與連字號 |
| `description` | string | 是 | 何時該被呼叫。寫入 `"PROACTIVELY"` 可讓 Claude 自動呼叫 |
| `tools` | string/list | 否 | 以逗號分隔的工具白名單（例如 `Read, Write, Edit, Bash`）。省略時繼承全部工具。支援 `Agent(agent_type)` 語法來限制可生成的子代理；舊的 `Task(agent_type)` 別名仍可用 |
| `disallowedTools` | string/list | 否 | 要拒絕的工具，會從繼承或指定的清單中移除 |
| `model` | string | 否 | 使用的模型：`sonnet`、`opus`、`haiku`、完整 model ID（例如 `claude-opus-4-6`），或 `inherit`（預設：`inherit`） |
| `permissionMode` | string | 否 | 權限模式：`default`、`acceptEdits`、`auto`、`dontAsk`、`bypassPermissions` 或 `plan` |
| `maxTurns` | integer | 否 | 子代理停止前的最大代理回合數 |
| `skills` | list | 否 | 啟動時預載進代理脈絡的 skill 名稱（注入完整內容，不只是「可用」而已） |
| `mcpServers` | list | 否 | 此子代理專用的 MCP server —— server 名稱字串或行內 `{name: config}` 物件 |
| `hooks` | object | 否 | 僅作用於此子代理的生命週期 hook。所有 hook 事件都支援；`PreToolUse`、`PostToolUse`、`Stop` 最常用 |
| `memory` | string | 否 | 持久記憶範圍：`user`、`project` 或 `local` |
| `background` | boolean | 否 | 設為 `true` 則永遠以背景任務執行（預設：`false`） |
| `effort` | string | 否 | 此子代理作用時覆寫的努力等級：`low`、`medium`、`high`、`xhigh`、`max`（僅 Opus 4.6）。預設：繼承 session |
| `isolation` | string | 否 | 設為 `"worktree"` 則在臨時 git worktree 中執行（無變更時自動清除） |
| `initialPrompt` | string | 否 | 當此代理以主 session 代理身分執行時（透過 `--agent` 或 `agent` 設定），自動送出作為第一個使用者回合。命令與 skill 都會被處理。會接在使用者提供的 prompt 之前 |
| `color` | string | 否 | 子代理在任務清單與逐字稿中的顯示顏色：`red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink` 或 `cyan` |

---

## ![Official](../%21/tags/official.svg) **（5 個）**

| # | 代理 | 模型 | 工具 | 說明 |
|---|-------|-------|-------|-------------|
| 1 | `general-purpose` | inherit | 全部 | 複雜的多步驟任務 —— 研究、程式碼搜尋與自主工作的預設代理類型 |
| 2 | `Explore` | haiku | 唯讀（無 Write、Edit） | 快速 codebase 搜尋與探索 —— 針對找檔案、搜程式碼、回答 codebase 問題最佳化 |
| 3 | `Plan` | inherit | 唯讀（無 Write、Edit） | plan 模式下的前置研究 —— 在寫程式前探索 codebase 並設計實作方向 |
| 4 | `statusline-setup` | sonnet | Read、Edit | 設定使用者的 Claude Code 狀態列 |
| 5 | `claude-code-guide` | haiku | Glob、Grep、Read、WebFetch、WebSearch | 回答關於 Claude Code 功能、Agent SDK 與 Claude API 的問題 |

---

## 資料來源

- [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [CLI reference — Claude Code Docs](https://code.claude.com/docs/en/cli-reference)
- [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
