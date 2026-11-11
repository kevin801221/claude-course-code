# Pydantic AI 上下文工程範本 (Pydantic AI Context Engineering Template)

這是一個全方位的範本，用於使用 Pydantic AI 構建生產級 AI 代理人，並結合了上下文工程的最佳實踐、工具整合、結構化輸出和全面的測試模式。

## 🚀 快速開始 - 複製範本

**2 分鐘內開始：**

```bash
# 複製上下文工程儲存庫
git clone https://github.com/coleam00/Context-Engineering-Intro.git
cd Context-Engineering-Intro/use-cases/pydantic-ai

# 1. 將此範本複製到您的新專案
python copy_template.py /path/to/my-agent-project

# 2. 導航至您的專案
cd /path/to/my-agent-project

# 3. 使用 PRP 工作流開始構建
# 在 PRPs/INITIAL.md 中填寫您想要建立的代理人需求

# 4. 根據您的詳細需求生成 PRP (生成後請驗證 PRP！)
/generate-pydantic-ai-prp PRPs/INITIAL.md

# 5. 執行 PRP 以建立您的 Pydantic AI 代理人
/execute-pydantic-ai-prp PRPs/generated_prp.md
```

如果您不使用 Claude Code，只需告訴您的 AI 編碼助手將 `.claude/commands` 中的 `generate-pydantic-ai-prp` 和 `execute-pydantic-ai-prp` 斜線命令內容作為提示語即可。

## 📖 這是什麼範本？

此範本提供了使用經過驗證的上下文工程工作流構建複雜 Pydantic AI 代理人所需的一切。它結合了：

- **Pydantic AI 最佳實踐**：具備工具、結構化輸出和依賴注入的型別安全代理人。
- **上下文工程工作流**：經過驗證的 PRP (產品需求提示) 方法論。
- **實際範例**：您可以學習和擴展的完整代理人實作。

## 🎯 PRP 框架工作流

此範本使用 3 步驟上下文工程工作流來構建 AI 代理人：

### 1. **定義需求** (`PRPs/INITIAL.md`)
首先清晰地定義您的代理人需要做什麼：
```markdown
# 客戶支援代理人 - 初始需求

## 概述
建立一個聰明的客戶支援代理人，可以處理諮詢、存取客戶數據並適當地呈報問題。

## 核心需求
- 具備上下文和記憶的多輪對話
- 客戶身分驗證和帳戶存取
- 帳戶餘額和交易查詢
- 付款處理和退款處理
...
```

### 2. **生成實作計畫** 
```bash
/generate-pydantic-ai-prp PRPs/INITIAL.md
```
這將建立一個全面的「產品需求提示」文件，其中包括：
- Pydantic AI 技術研究和最佳實踐。
- 具備工具和依賴項的代理人架構設計。
- 帶有驗證迴圈的實作路線圖。
- 安全模式和生產考量。

### 3. **執行實作**
```bash
/execute-pydantic-ai-prp PRPs/your_agent.md
```
這將根據 PRP 實作完整的代理人，包括：
- 使用正確的模型提供者配置建立代理人。
- 具備錯誤處理和驗證的工具整合。
- 使用 Pydantic 驗證的結構化輸出模型。
- 使用 `TestModel` 和 `FunctionModel` 進行全面測試。

## 📂 範本結構

```
pydantic-ai/
├── CLAUDE.md                           # Pydantic AI 全局開發規則
├── copy_template.py                    # 範本部署腳本
├── .claude/commands/
│   ├── generate-pydantic-ai-prp.md     # 代理人的 PRP 生成
│   └── execute-pydantic-ai-prp.md      # 代理人的 PRP 執行
├── PRPs/
│   ├── templates/
│   │   └── prp_pydantic_ai_base.md     # 代理人的基礎 PRP 範本
│   └── INITIAL.md                      # 代理人需求範例
├── examples/
│   ├── basic_chat_agent/               # 簡單的對話代理人
│   │   ├── agent.py                    # 具備記憶和上下文的代理人
│   │   └── README.md                   # 使用指南
│   ├── tool_enabled_agent/             # 具備外部工具的代理人
│   │   ├── agent.py                    # 網頁搜尋 + 計算機工具
│   │   └── requirements.txt            # 依賴項
│   └── testing_examples/               # 全面的測試模式
│       ├── test_agent_patterns.py      # TestModel, FunctionModel 範例
│       └── pytest.ini                  # 測試設定
└── README.md                           # 本檔案
```

## 🤖 內含的代理人範例

### 1. 主代理人參考 (`examples/main_agent_reference/`)
**權威的參考實作**，展示了正確的 Pydantic AI 模式：
- 使用 `settings.py` 和 `providers.py` 進行基於環境的配置。
- 郵件代理人和研究代理人之間的清晰關注點分離。
- 正確的檔案結構，將提示、工具、代理人和 Pydantic 模型分離。
- 與外部 API (Gmail, Brave Search) 的工具整合。

**關鍵檔案：**
- `settings.py`：使用 `pydantic-settings` 進行環境配置。
- `providers.py`：使用 `get_llm_model()` 進行模型提供者抽象。
- `research_agent.py`：整合網頁搜尋和郵件功能的多工具代理人。
- `email_agent.py`：專門用於建立 Gmail 草稿的代理人。

### 2. 基礎對話代理人 (`examples/basic_chat_agent/`)
一個展示核心模式的簡單對話代理人：
- **基於環境的模型配置** (遵循 `main_agent_reference`)。
- **預設為字串輸出** (除非需要，否則不使用 `result_type`)。
- 系統提示詞 (靜態和動態)。
- 具備依賴注入的對話記憶。

**關鍵特點：**
- 簡單的字串回應 (非結構化輸出)。
- 基於設定的配置模式。
- 對話上下文追蹤。
- 清晰、極簡的實作。

### 3. 具備工具功能的代理人 (`examples/tool_enabled_agent/`)
一個具備工具整合能力的代理人：
- **基於環境的配置** (遵循 `main_agent_reference`)。
- **預設為字串輸出** (無不必要的結構)。
- 網頁搜尋和計算工具。
- 錯誤處理和重試機制。

**關鍵特點：**
- `@agent.tool` 裝飾器模式。
- 用於依賴注入的 `RunContext`。
- 工具錯誤處理與恢復。
- 工具的簡單字串回應。

### 4. 結構化輸出代理人 (`examples/structured_output_agent/`)
**新內容**：展示何時使用 `result_type` 進行資料驗證：
- **基於環境的配置** (遵循 `main_agent_reference`)。
- **使用 Pydantic 驗證的結構化輸出** (當特別需要時)。
- 使用統計工具進行數據分析。
- 專業報告生成。

**關鍵特點：**
- 演示 `result_type` 的正確用法。
- 商業報告的 Pydantic 驗證。
- 帶有數值統計的數據分析工具。
- 關於何時使用結構化與字串輸出的清晰說明。

### 5. 測試範例 (`examples/testing_examples/`)
Pydantic AI 代理人的全面測試模式：
- `TestModel` 用於快速開發驗證。
- `FunctionModel` 用於自訂行為測試。
- `Agent.override()` 用於測試隔離。
- Pytest fixtures 和非同步測試。

**關鍵特點：**
- 無需 API 成本的單元測試。
- 模擬 (Mock) 依賴注入。
- 工具驗證和錯誤場景測試。
- 整合測試模式。

## 📚 額外資源

- **Pydantic AI 官方文件**：https://ai.pydantic.dev/
- **上下文工程方法論**：請參閱主儲存庫 README。

## 🆘 支援與貢獻

- **問題 (Issues)**：回報範本或範例的問題。
- **改進**：貢獻額外的範例或模式。
- **疑問**：詢問有關 Pydantic AI 整合或上下文工程的問題。

此範本是更大的上下文工程框架的一部分。請參閱主儲存庫以獲取更多上下文工程範本和方法論。

---

**準備好構建生產級 AI 代理人了嗎？** 從 `python copy_template.py my-agent-project` 開始，並遵循 PRP 工作流！ 🚀
