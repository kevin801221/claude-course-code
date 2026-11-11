---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*)
argument-hint: [message]
description: 建立帶上下文的 Git 提交
---

## 上下文

- 當前 git 狀態: !`git status`
- 當前 git diff: !`git diff HEAD`
- 當前分支: !`git branch --show-current`
- 最近的提交: !`git log --oneline -10`

## 你的任務

根據上面的變更建立一個單獨的 Git 提交。

如果透過引數傳入了 message，就直接使用它：$ARGUMENTS

否則，分析這些變更，並按照 conventional commits 格式生成合適的提交資訊：
- `feat:` 新功能
- `fix:` 修復 bug
- `docs:` 文件變更
- `refactor:` 程式碼重構
- `test:` 新增測試
- `chore:` 維護任務
