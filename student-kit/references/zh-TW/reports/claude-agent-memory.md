# Claude Code：Agent Memory Frontmatter

子代理的持久記憶 —— 讓代理能跨 session 學習、記憶並累積知識。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`reports/claude-agent-memory.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/reports/claude-agent-memory.md)

---

## 概觀

在 **Claude Code v2.1.33**（2026 年 2 月）引入的 `memory` frontmatter 欄位，讓每個子代理擁有自己基於 markdown 的持久知識庫。在此之前，每次呼叫代理都是從零開始。

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Write, Edit, Bash
model: sonnet
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

---

## 記憶範圍（Memory Scopes）

| 範圍 | 儲存位置 | 納入版控 | 共享 | 最適合 |
|-------|-----------------|-------------------|--------|----------|
| `user` | `~/.claude/agent-memory/<agent-name>/` | 否 | 否 | 跨專案知識（建議的預設值） |
| `project` | `.claude/agent-memory/<agent-name>/` | 是 | 是 | 團隊該共享的專案專屬知識 |
| `local` | `.claude/agent-memory-local/<agent-name>/` | 否（git-ignored） | 否 | 屬於個人的專案專屬知識 |

這些範圍對應設定階層（`~/.claude/settings.json` → `.claude/settings.json` → `.claude/settings.local.json`）。

---

## 運作方式

1. **啟動時**：`MEMORY.md` 的前 200 行會被注入代理的 system prompt
2. **工具存取**：`Read`、`Write`、`Edit` 會自動啟用，讓代理能管理自己的記憶
3. **執行期間**：代理可自由讀寫自己的記憶目錄
4. **整理**：若 `MEMORY.md` 超過 200 行，代理會把細節搬到主題專屬的檔案

```
~/.claude/agent-memory/code-reviewer/     # user 範圍範例
├── MEMORY.md                              # 主檔（載入前 200 行）
├── react-patterns.md                      # 主題專屬檔
└── security-checklist.md                  # 主題專屬檔
```

---

## Agent Memory 與其他記憶系統的比較

| 系統 | 誰寫 | 誰讀 | 範圍 |
|--------|-----------|-----------|-------|
| **CLAUDE.md** | 你（手動） | 主 Claude + 所有代理 | 專案 |
| **Auto-memory** | 主 Claude（自動） | 僅主 Claude | 每專案每使用者 |
| **`/memory` 命令** | 你（透過編輯器） | 僅主 Claude | 每專案每使用者 |
| **Agent memory** | 代理自己 | 僅該特定代理 | 可設定（user/project/local） |

這些系統是**互補的** —— 代理會同時讀 CLAUDE.md（專案脈絡）與自己的記憶（代理專屬知識）。

---

## 實務範例

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
tools: Read, Write, Edit, Bash
model: sonnet
memory: project
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions from your preloaded skills.
As you work, save architectural decisions and patterns to your memory.
```

這把 **skills**（啟動時的靜態知識）與 **memory**（隨時間累積的動態知識）結合起來。

---

## 技巧

- **在 prompt 中要求使用記憶** —— 寫明確指令：`「開始前先檢視你的記憶。完成後把學到的東西更新進記憶。」`
- **呼叫代理時要求檢查記憶**：`「檢視這個 PR，並查你的記憶看有沒有見過類似的模式。」`
- **選對範圍** —— 跨專案用 `user`，團隊共享用 `project`，個人用 `local`

---

## 資料來源

- [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [Manage Claude's memory — Claude Code Docs](https://code.claude.com/docs/en/memory)
- [Claude Code v2.1.33 Release Notes](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
