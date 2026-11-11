# 平行任務版本執行 (Parallel Task Version Execution)

## 變數 (Variables)
FEATURE_NAME: $ARGUMENTS
PLAN_TO_EXECUTE: $ARGUMENTS
NUMBER_OF_PARALLEL_WORKTREES: $ARGUMENTS

## 指令 (Instructions)

我們將建立 NUMBER_OF_PARALLEL_WORKTREES 個新的子代理人，它們使用 Task 工具平行建立同一個功能的 N 個版本。

請務必閱讀 PLAN_TO_EXECUTE。

這使我們能夠同時平行構建相同的功能，以便我們可以單獨測試和驗證每個子代理人的變更，然後選擇最佳的變更。

第一個代理人將在 `trees/<FEATURE_NAME>-1/` 中執行
第二個代理人將在 `trees/<FEATURE_NAME>-2/` 中執行
...
最後一個代理人將在 `trees/<FEATURE_NAME>-<NUMBER_OF_PARALLEL_WORKTREES>/` 中執行

`trees/<FEATURE_NAME>-<i>/` 中的程式碼將與目前分支中的程式碼完全相同。它將被設定好，供您端到端地構建功能。

每個代理人將在各自的工作區中獨立實作 PLAN_TO_EXECUTE 中詳細說明的工程計畫。

當子代理人完成工作時，請讓子代理人在其各自工作區的根目錄下的全面 `RESULTS.md` 檔案中報告其最終變更。

確保代理人「不要」執行任何測試或其他程式碼 —— 僅專注於程式碼變更。
