---
description: 清理程式碼、暫存變更並準備一個 pull request
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(npm test:*), Bash(npm run lint:*)
---

# Pull Request 準備清單

建立 PR 之前，先執行以下步驟：

1. 執行 lint：`prettier --write .`
2. 執行測試：`npm test`
3. 檢視 git diff：`git diff HEAD`
4. 暫存變更：`git add .`
5. 依 conventional commits 建立 commit 訊息：
   - `fix:` 表示錯誤修正
   - `feat:` 表示新功能
   - `docs:` 表示文件
   - `refactor:` 表示程式碼重構
   - `test:` 表示新增測試
   - `chore:` 表示維護性工作

6. 產生 PR 摘要，內容包含：
   - 變更了什麼
   - 為什麼變更
   - 執行過哪些測試
   - 可能的影響

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/commands
**相容模型**：Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
