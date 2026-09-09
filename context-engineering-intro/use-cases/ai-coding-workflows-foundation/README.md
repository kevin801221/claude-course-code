# 🚀 AI 編碼工作流 (AI Coding Workflows)

一個用於開發有效 AI 編碼工作流的全面框架，分為三個階段：**計畫 (Planning)**、**實作 (Implementation)** 和 **驗證 (Validation)**。

## 🧠 主要心智模型 (Primary Mental Model)

核心理念圍繞著「**上下文工程 (Context Engineering)**」—— 系統地準備和組織資訊，以最大限度地發揮 AI 編碼助手的效能。

## 📋 第一階段：計畫 (Planning)

### 1. 🎨 感覺計畫 (Vibe Planning)
使用 `/primer` 斜線命令開始您的探索：
- **新專案**：研究在線資源、類似專案，探索架構和技術棧選項。
- **現有專案**：使用 **Codebase Analyst** 子代理人分析並理解目前的程式碼庫。
- 重點：對想法、概念和可能性的非結構化探索。

### 2. 📝 建立 INITIAL.md (PRD)
生成詳細的產品需求文件 (Product Requirements Document)：
- **新專案**：高層級的 MVP (最小可行性產品)，並附帶支援文件參考。
- **現有專案**：專注且詳細的需求，並帶有整合點。

### 3. ⚙️ 上下文工程組件 (Context Engineering Components)
使用斜線命令準備這些基本元素：

- **RAG** (檢索增強生成)
- **任務管理**
- **記憶系統**
- **提示工程**

#### 🛠️ 支援工具：
- Archon
- PRP 框架
- 網頁搜尋
- GitHub Spec Kit

### 📊 出擊計畫 (Plan of Attack)
使用 `/create-plan` 斜線命令，根據您的 `INITIAL.md` 和上下文工程設定生成結構化的實作策略。

## ⚡ 第二階段：實作 (Implementation)

### 🎯 逐項執行任務 (Execute Task by Task)
- 使用 `/execute-plan` 斜線命令系統地執行您的出擊計畫。
- 遵循在計畫階段建立的結構化計畫。
- 利用上下文工程基礎。

### 🔍 信任但要驗證 (Trust but Verify)
監控 AI 助手以確保它：
- 正確使用 MCP 伺服器。
- 讀取/編輯適當的檔案。
- 正確利用任務管理。
- 產生清晰顯示其理解能力的「思考 (Thinking)」標記 (Tokens)。

## ✅ 第三階段：驗證 (Validation)

### 📊 程式碼審查流程 (Code Review Process)
**AI 助手驗證**：
- 使用 **Validator** 子代理人執行自動化程式碼審查。
- 執行單元測試。
- 執行整合測試。

**人工驗證**：
- 戰略監督。
- 手動測試。

## 🔧 關鍵組件

### 🌐 全局規則 (Global Rules)
- 子代理人協調 (**Codebase Analyst** & **Validator**)。
- 斜線命令整合 (`/primer`, `/create-plan`, `/execute-plan`)。
- 各個階段之間工作流的一致性。

### 🎯 斜線命令參考
- **`/primer`**：透過探索提示初始化感覺計畫階段。
- **`/create-plan`**：從 PRD 生成結構化的出擊計畫。
- **`/execute-plan`**：系統地實作建立的計畫。

### 🤖 子代理人 (Sub-Agents)
- **Codebase Analyst**：專門用於理解和分析現有的程式碼庫。
- **Validator**：專注於系統化的程式碼審查和品質保證。

### 🏆 成功因素
- **結構化方法**：每個階段都建立在前一個階段的基礎上。
- **上下文準備**：徹底的設定可實現更好的 AI 效能。
- **迭代優化**：在每一步都信任但要驗證。
- **工具整合**：針對特定任務利用專門的工具。

該框架將臨時的 AI 互動轉變為系統化、可重複的流程，從而始終如一地產生高品質的程式碼和文件。 🎉
