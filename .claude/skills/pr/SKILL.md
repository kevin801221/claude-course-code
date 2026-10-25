---
name: pr
description: Generate an evidence-backed Pull Request description with architectural diagrams, test proof, and One-Way vs Two-Way Door risk classification.
disable-model-invocation: true
---

# Evidence-Backed PR (Matt Pocock Skills Suite)

依據 Matt Pocock v1.3 的「證據導向」架構產生 PR 描述，拒絕無意義的 AI 垃圾水 PR：

## 必須包含的三大區塊

1. **架構摘要圖（Mermaid Diagram）**：
   清楚繪製本次變更影響的模組、資料流向或 API 介面。

2. **客觀驗證證據（Evidence）**：
   - 附上實際執行的測試指令與終端通過結果（例如 `uv run pytest`、`npm test`）。
   - 附上前/後效能或行為比對，證明不是未經驗證的幻覺。

3. **決策風險分級（Door Classification）**：
   - 🚪 **雙向門（Two-Way Door，低風險/隨時可逆）**：UI 調整、文案、非破壞性重構。
   - 🚨 **單向門（One-Way Door，高風險/架構不可逆，要求人類重點審查）**：DB Migration、外部 API 契約破壞性改動、資安與授權層異動。附帶回滾方案。
