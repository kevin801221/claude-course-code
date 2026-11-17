---
name: workshop-bc
description: 手動執行學生版溫度告警離線實驗，根據這一次產生的檔案解讀研發證據、PRD、SoW 與變更提案。
argument-hint: "[新輸出目錄，預設 outputs/demo]"
disable-model-invocation: true
---

請從能看到 `workshop/`、`fixtures/` 和 `b_research/` 的實驗目錄操作。

1. 執行 `python3 -m workshop demo --offline --out <輸出目錄>`。使用者未填參數時使用 `outputs/demo`。若該目錄已存在，請提示改用另一個新名稱。
2. 依實際結束碼回報。成功時列出本次的研究報告、工作摘要、PRD、SoW、追溯表、CR-001 與檢核報告路徑。
3. 用 `b/metrics.csv` 與 `c/linked/versions/v1/traceability.md` 回答：尖峰情境中哪個候選誤報？持續升溫的實測延遲可否直接填進 REQ-004 的產品門檻？
4. 讀取 `c/linked/changes/CR-001.json`、`c/linked/project.json` 和 `review.md`（位於同一個 `c/linked/` 目錄）。交代提案狀態、目前版本以及結構檢核的結果。本練習的完成點是交出提案，核准與升版留待產品負責人決策。
