---
description: 產生 Matt Pocock 式「證據導向 PR」描述（包含架構圖、終端測試證據與單向門/雙向門風險評估）
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(pytest:*), Bash(npm test:*)
---

請依據目前的 Git 變更，撰寫一份高品質、高信任度的「證據導向 Pull Request（PR）」描述（繁體中文）：

1. **蒐集變更與驗證證據**：
   - 執行 `git status` 與 `git diff HEAD~1` 或相對於 main branch 的差異。
   - 執行相關測試指令（例如 `uv run pytest` 或 `npm test`），擷取實際終端輸出作為客觀證據。

2. **產出結構化 PR 內容**：
   依據下方格式輸出：

```markdown
# PR: <動詞開頭的清晰簡述>

## 1. 系統架構變更摘要（Mermaid Diagram）
（繪製一張 Mermaid 圖，清楚展示受本次變更影響的模組或資料流向）

## 2. 客觀驗證證據（Evidence）
- [x] 自動化測試通過證明（貼上真實終端指令與輸出摘要）：
  ```text
  <測試指令與結果>
  ```
- [x] 實際執行效果驗證（Diff 摘要、輸出截圖或日誌）：
  - ...

## 3. 風險評估與決策類型（Door Classification）
- 🚪 **雙向門變更（Two-Way Door，低風險/隨時可逆）**：
  - <例如 UI 微調、註解補充、非破壞性工具更新>
- 🚨 **單向門變更（One-Way Door，高風險/架構不可逆，請重點審查）**：
  - <例如 DB Schema 遷移、API 契約破壞性修改、核心權限架構重構>
  - **回滾預案（Rollback Plan）**：<若發生問題如何快速退回>
```
