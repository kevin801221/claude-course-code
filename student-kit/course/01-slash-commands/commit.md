---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*)
argument-hint: [message]
description: 建立包含上下文的 git commit
---

## 上下文

- 目前的 git 狀態：!`git status`
- 目前的 git diff：!`git diff HEAD`
- 目前分支：!`git branch --show-current`
- 最近的 commit：!`git log --oneline -10`

## 你的任務

根據上述變更，建立一個 git commit。

如果有透過參數提供訊息，就使用它：$ARGUMENTS

否則，分析變更並依照 conventional commits 格式撰寫適當的 commit 訊息：
- `feat:` 表示新功能
- `fix:` 表示錯誤修正
- `docs:` 表示文件變更
- `refactor:` 表示程式碼重構
- `test:` 表示新增測試
- `chore:` 表示維護性工作

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/commands
**相容模型**：Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
