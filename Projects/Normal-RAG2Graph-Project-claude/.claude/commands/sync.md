---
description: Review IDE Extension 剛完成的改動，按 cli-extension-sync 協議做品質檢查 + commit + 更新 .collab-sync.md
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Read, Edit, Write, Skill(cli-extension-sync)
---

請按照 `cli-extension-sync` skill 的「當 Claude Code CLI 收到 `/sync` 指令時」工作流程執行：

1. 讀取 `.collab-sync.md`，了解 IDE Extension 剛完成什麼
2. 跑 `git status` + `git diff` 盤點未 commit 改動
3. 對照 `CLAUDE.md` 的剛性規則逐條品質驗證（語言、技術棧、工作流程、禁忌）
4. 有問題 → 記在 `.collab-sync.md` 的「反饋」區、不要 commit、回報使用者
5. 沒問題 → 用 Conventional Commits 格式（繁體中文 + `Co-Authored-By`）做 commit
6. 把任務從「待審查」移到「已完成任務」，並在「Extension 的後續任務」寫下一步

如果 `.collab-sync.md` 不存在，先用 `.claude/skills/cli-extension-sync/references/sync_template.md` 建立。

最後輸出一段 200 字以內的中文總結：完成了什麼、commit hash、下一步交給誰。

$ARGUMENTS
