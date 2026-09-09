# 為平行 Claude Code 代理人初始化平行 Git 工作樹目錄

## 變數 (Variables)
FEATURE_NAME: $ARGUMENTS
NUMBER_OF_PARALLEL_WORKTREES: $ARGUMENTS

## 執行這些指令
> 配合 Batch 和 Task 工具平行執行迴圈

- 建立一個新目錄 `trees/`
- 對於從 1 到 NUMBER_OF_PARALLEL_WORKTREES 的 i：
  - 執行 `git worktree add -b FEATURE_NAME-i ./trees/FEATURE_NAME-i`
  - 執行 `cd trees/FEATURE_NAME-i`，並執行 `git ls-files` 進行驗證
- 執行 `git worktree list` 以確認所有工作樹均已正確建立
