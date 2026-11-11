---
description: 清理程式碼、暫存變更並準備 Pull Request
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(npm test:*), Bash(npm run lint:*)
---

# Pull Request 準備清單

在建立 PR 之前，請執行以下步驟：

1. 執行格式化：`prettier --write .`
2. 執行測試：`npm test`
3. 檢視 git diff：`git diff HEAD`
4. 暫存變更：`git add .`
5. 按 conventional commits 建立提交資訊：
   - `fix:` bug 修復
   - `feat:` 新功能
   - `docs:` 文件
   - `refactor:` 程式碼重構
   - `test:` 測試新增
   - `chore:` 維護

6. 生成 PR 摘要，包含：
   - 變更了什麼
   - 為什麼變更
   - 做了哪些測試
   - 可能的影響
