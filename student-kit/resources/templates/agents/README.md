# 三個各有邊界的子代理

對應講義 Part 11。依 `claude-course-code` 的 reviewer / test-engineer 與 `claude-howto-zh-TW` 的 documentation-writer 改寫。
刪除來源中的固定模型清單、過期版號與硬性涵蓋率目標；保留 `model: inherit`。

| 代理 | 工作 | 預期交付 |
|---|---|---|
| kit-reviewer | 唯讀檢查變更 | 可重現的缺陷與檔案行號 |
| kit-test-engineer | 補關鍵行為測試 | 測試 diff、實際命令與結果 |
| kit-docs-writer | 文件整理 | 可跟做的 README 與未驗證項目 |

## 啟用與操作

1. 在自己的練習專案建立 `.claude/agents/`，只複製這三個 `.md`（不含本 README）。
2. 啟動新 Claude 對話，執行 `/agents` 確認有列出三個名稱。
3. 提示：「請委派 kit-reviewer，檢查目前 git diff，只回報缺陷，不改碼。」
4. 給每個代理明確的目錄與交付物。平行處理時不要讓兩個代理編輯同一檔案。
5. 主對話讀完回報、跑整合驗收，才宣告任務完成。

驗收：reviewer 執行後 diff 不應因審查而改變；測試代理只變更指定測試；文件代理的指令與原碼一致。
工具清單與文字規則有不同作用：給了 Bash 的 reviewer 仍能透過 shell 改檔，文字限制不能取代權限管理。
