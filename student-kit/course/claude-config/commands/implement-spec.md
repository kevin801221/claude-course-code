---
description: 依據 SPEC.md 中的任務相依圖（Ticket Graph），自動解析未受阻擋任務並指派 Sub-agents 並行實作
allowed-tools: Bash, Read, Write, Edit, MultiEdit
---

你現在是「並行施工工頭（Task Graph Orchestrator）」，請依據 Matt Pocock 的 Spec-Driven Development 流程執行：

1. **讀取規格文件**：
   - 預設讀取專案中的 `SPEC.md`（若使用者透過 `$ARGUMENTS` 指定其他規格檔，則讀取該檔案）。
   - 檢查專案中是否有 `GLOSSARY.md`，若有，讀取其中的領域專有名詞以確保實作名稱正確對齊。

2. **建立任務相依圖（DAG）**：
   - 解析任務列表，辨識每項任務的 `Blocked by: ...` 條件。
   - 篩選出所有「目前沒有任何前置阻礙（Unblocked）」的任務。

3. **派工與並行實作**：
   - 對於每個 Unblocked 任務，評估是否適合由獨立 Sub-agent 執行。
   - 遵循「高內聚、低耦合」原則，若任務跨不同目錄，委派專職 Sub-agent 進行實作並編寫對應測試。
   - 完成任務後，將其在規格檔中標記為 `[x]`，並重新掃描下一批被解鎖的任務。

4. **驗收與總結**：
   - 跑測試確保所有變更均通過。
   - 條列本次批次施工成果，回報下一步可解鎖的任務清單。
