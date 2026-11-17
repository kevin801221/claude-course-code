---
name: implement-spec
description: Build out specs or tickets test-first based on a Ticket Graph, dispatching unblocked tasks in parallel across sub-agents.
disable-model-invocation: true
---

# Implement Spec (Matt Pocock Skills Suite)

依據 Matt Pocock 的 Spec-Driven Development 流程，以「Ticket Graph（相依圖）」驅動並行施工：

## 執行流程

1. **讀取規格與領域語言**：
   - 讀取 `SPEC.md`（或傳入的路徑）。
   - 讀取 `GLOSSARY.md`（若存在），確保變數、模組與概念名稱與領域模型完全對齊。

2. **解析相依性圖譜（DAG）**：
   - 掃描所有任務的 `Blocked by: ...` 聲明。
   - 篩選出所有「未受任何前置阻礙（Unblocked）」的獨立任務。

3. **Sub-agents 平行派工**：
   - 每個獨立模組的 Unblocked 任務，分派專屬 Sub-agent 開工。
   - 堅持 TDD（測試驅動開發），先在預先約定的接縫（Seams）建立紅燈測試，再進行最小實作至綠燈。
   - 單元完成後，在規格中標記 `[x]`，解鎖下一批下游任務。

4. **品質把關**：
   - 實作完成後自動呼叫 `/code-review` 進行「規範（Standards）」與「規格（Spec）」雙軸審查。
