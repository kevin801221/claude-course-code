---
name: gitnexus-helper
description: |
  Help user understand, install, configure, and query GitNexus — a tool that
  indexes any codebase into a knowledge graph and exposes it via MCP for AI
  agents. Triggers when user mentions: GitNexus, gitnexus, codebase graph,
  knowledge graph, dependency graph, call chain analysis, repo structure
  analysis, or asks "怎麼看這個 repo 的架構", "幫我建這個 repo 的 graph",
  "what depends on X module", "show me callers of Y function".
---

# GitNexus Helper

## What is GitNexus

GitNexus 把任何 codebase 索引成「知識圖譜」(knowledge graph)，把
dependency / call chain / type system 等關係用 graph 結構儲存。
透過 MCP 暴露給 AI agents（Claude Code / Cursor / Codex 等）使用，
讓 AI 對 codebase 有「架構級」理解，而不只是 grep 結果。

**官方 repo**: https://github.com/abhigyanpatwari/GitNexus
**Web 視覺化**: https://gitnexus.vercel.app/

## When to use this skill

- User asks 「幫我看這個 repo 的依賴 / 結構 / 架構」
- User asks 「X 模組被哪些檔案用到 / who uses X」
- User asks 「我要重構 X，誰會受影響 / impact analysis」
- User asks 「建一下這個 repo 的 graph」
- User mentions 想用 GitNexus 但不知怎麼開始

## Workflow

### A. User 想「建構」graph (analyze)

→ **直接觸發 `/gitnexus` slash command**，那邊有完整互動式流程。
不要自己跳過 mode 選擇 — 讓使用者選 quick / deep / full。

### B. User 想「查詢」現有 graph

1. 確認 graph 已建好：`gitnexus status`
   - 沒建過 → 引導到 `/gitnexus`
   - 已建過 → 繼續

2. 確認 MCP 有連線：`claude mcp list | grep gitnexus`
   - 沒連 → `npx gitnexus setup`

3. 用 MCP tool 查（Claude 應該有從 gitnexus MCP server 得到工具）。
   常見問法：
   - 「看 src/auth/ 被哪些檔案 import」→ 用 `find_dependencies`
   - 「找 UserService 的所有 caller」→ 用 `find_callers`
   - 「列出測試 X 模組的所有 test 檔」→ 用 `find_tests`

### C. User 抱怨「graph 不準 / 過時」

可能 commit 過後 index stale。跑：

```bash
gitnexus analyze --force   # 強制重建
# 或
gitnexus analyze           # 增量更新
```

PostToolUse hook 會自動偵測 stale 並提示，所以這通常會主動觸發。

## CLI Reference

詳見 `reference/cli-reference.md`（同資料夾下）。

## Critical Rules

- **不要自己決定模式** — quick / deep / full 一定要問使用者
- **不要在沒 confirm 的情況下跑 `--force`** — 會重建整個 graph，浪費時間
- **MCP tool 失敗時** — 先檢查 `gitnexus serve` 還在不在（如果使用者用 bridge mode），再考慮 reset MCP
- **如果使用者只是要「快速看看」repo 結構**，先建議 quick mode 試試，不要一上來就 full + embeddings
