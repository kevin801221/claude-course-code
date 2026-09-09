---
name: "PydanticAI 代理人 PRP 範本 (PydanticAI Agent PRP Template)"
description: "用於為 PydanticAI 代理人開發專案生成全面 PRP 的範本"
---

## 目的 (Purpose)

[簡要描述要構建的 PydanticAI 代理人及其主要用途]

## 核心原則 (Core Principles)

1. **PydanticAI 最佳實踐**：與 PydanticAI 的代理人建立、工具和結構化輸出模式深度整合。
2. **生產就緒 (Production Ready)**：為生產部署包含安全性、測試和監控。
3. **型別安全優先**：全程利用 PydanticAI 的型別安全設計和 Pydantic 驗證。
4. **上下文工程整合**：將經過驗證的上下文工程工作流應用於 AI 代理人開發。
5. **全面測試**：使用 TestModel 和 FunctionModel 進行徹底的代理人驗證。

## ⚠️ 實作指引：不要過度工程 (Don't Over-Engineer)

**重要**：保持您的代理人實作專注且實用。不要構建不必要的複雜性。

### 不該做的事：
- ❌ **不要建立幾十個工具** —— 僅構建代理人真正需要的工具。
- ❌ **不要使依賴項過度複雜** —— 保持依賴注入簡單且專注。
- ❌ **不要增加不必要的抽象** —— 直接遵循 `main_agent_reference` 模式。
- ❌ **不要構建複雜的工作流**，除非有明確要求。
- ❌ **不要增加結構化輸出**，除非明確需要驗證 (預設使用字串)。
- ❌ **不要在 `examples/` 資料夾中構建**。

### 應該做的事：
- ✅ **從簡單開始** —— 構建滿足需求的最小可行代理人 (MVP)。
- ✅ **漸進式增加工具** —— 僅實作代理人運作所需的功能。
- ✅ **遵循 `main_agent_reference`** —— 使用經過驗證的模式，不要重新發明輪子。
- ✅ **預設使用字串輸出** —— 僅在需要驗證時才增加 `result_type`。
- ✅ **儘早且頻繁地測試** —— 在構建過程中隨時使用 `TestModel` 進行驗證。

### 關鍵問題：
**「這個代理人真的需要這個功能來完成其核心目標嗎？」**

如果答案是否定的，就不要構建它。保持簡單、專注且功能完善。

---

## 目標 (Goal)

[詳細描述代理人應完成的任務]

## 為什麼 (Why)

[解釋為什麼需要這個代理人以及它解決了什麼問題]

## 內容 (What)

### 代理人類型分類
- [ ] **對話代理人 (Chat Agent)**：具備記憶與上下文的對話介面。
- [ ] **工具化代理人 (Tool-Enabled Agent)**：具備外部工具整合能力的代理人。
- [ ] **工作流代理人 (Workflow Agent)**：多步驟任務處理與編排。
- [ ] **結構化輸出代理人 (Structured Output Agent)**：複雜資料驗證與格式化。

### 模型提供者需求
- [ ] **OpenAI**：`openai:gpt-4o` 或 `openai:gpt-4o-mini`
- [ ] **Anthropic**：`anthropic:claude-3-5-sonnet-20241022` 或 `anthropic:claude-3-5-haiku-20241022`
- [ ] **Google**：`gemini-1.5-flash` 或 `gemini-1.5-pro`
- [ ] **備援策略**：支援多個提供者並具備自動故障切換 (Failover)。

### 外部整合
- [ ] 資料庫連線 (指定類型：PostgreSQL, MongoDB 等)。
- [ ] REST API 整合 (列出所需的服務)。
- [ ] 檔案系統操作。
- [ ] 網頁爬取或搜尋能力。
- [ ] 即時資料源。

### 成功準則 (Success Criteria)
- [ ] 代理人成功處理指定的用例。
- [ ] 所有工具運作正常且具備正確的錯誤處理。
- [ ] 結構化輸出符合 Pydantic 模型的驗證。
- [ ] 使用 TestModel 和 FunctionModel 達成全面的測試覆蓋。
- [ ] 實作了安全措施 (API 金鑰、輸入驗證、速率限制)。
- [ ] 效能滿足需求 (回應時間、吞吐量)。

## 所有需要的上下文 (All Needed Context)

### PydanticAI 說明文件與研究

```yaml
# MCP 伺服器
- mcp: Archon
  query: "PydanticAI agent creation model providers tools dependencies"
  why: 核心框架理解與最新模式

# 必讀的 Pydantic AI 文件 —— 必須研究
- url: https://ai.pydantic.dev/
  why: 官方 PydanticAI 文件及入門指南
  content: 代理人建立、模型提供者、依賴注入模式

- url: https://ai.pydantic.dev/agents/
  why: 全面的代理人架構與配置模式
  content: 系統提示詞、輸出類型、執行方法、代理人組合

- url: https://ai.pydantic.dev/tools/
  why: 工具整合模式與函式註冊
  content: @agent.tool 裝飾器、RunContext 用法、參數驗證

- url: https://ai.pydantic.dev/testing/
  why: 針對 PydanticAI 代理人的測試策略
  content: TestModel, FunctionModel, Agent.override(), pytest 模式

- url: https://ai.pydantic.dev/models/
  why: 模型提供者配置與身分驗證
  content: OpenAI, Anthropic, Gemini 設定、API 金鑰管理、備援模型

# 預建範例
- path: examples/
  why: Pydantic AI 代理人的參考實作
  content: 一系列已構建的簡單 Pydantic AI 範例，包含如何設定模型與提供者

- path: examples/cli.py
  why: 展示與 Pydantic AI 代理人的真實世界互動
  content: 具備串流、工具呼叫可見性及對話處理的對話式 CLI —— 展示使用者實際如何與代理人互動
```

### 代理人架構研究

```yaml
# PydanticAI 架構模式 (遵循 main_agent_reference)
agent_structure:
  configuration:
    - settings.py：使用 pydantic-settings 的基於環境的配置
    - providers.py：使用 get_llm_model() 的模型提供者抽象
    - 用於 API 金鑰與模型選擇的環境變數
    - 切勿硬編碼模型字串，如 "openai:gpt-4o"
  
  agent_definition:
    - 預設使用字串輸出 (除非需要結構化輸出，否則不使用 result_type)
    - 使用來自 providers.py 的 get_llm_model() 進行模型配置
    - 系統提示詞作為字串常量或函式
    - 用於外部服務的 Dataclass 依賴項
  
  tool_integration:
    - 使用 @agent.tool 建立具備 RunContext[DepsType] 的上下文感知工具
    - 工具函式作為可獨立呼叫的純函式 (Pure functions)
    - 工具實作中具備正確的錯誤處理與記錄
    - 透過 RunContext.deps 進行依賴注入
  
  testing_strategy:
    - 使用 TestModel 進行快速開發驗證
    - 使用 FunctionModel 進行自訂行為測試  
    - 使用 Agent.override() 進行測試隔離
    - 使用模擬 (Mocks) 進行全面的工具測試
```

### 安全性與生產考量

```yaml
# PydanticAI 安全模式 (需要研究)
security_requirements:
  api_management:
    environment_variables: ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"]
    secure_storage: "切勿將 API 金鑰提交至版本控制"
    rotation_strategy: "金鑰輪換與管理計畫"
  
  input_validation:
    sanitization: "使用 Pydantic 模型驗證所有使用者輸入"
    prompt_injection: "實作提示詞注入預防策略"
    rate_limiting: "透過正確的節流 (Throttling) 防止濫用"
  
  output_security:
    data_filtering: "確保代理人回應中無敏感數據"
    content_validation: "驗證輸出的結構與內容"
    logging_safety: "不洩露機密的安全性記錄"
```

### 常見 PydanticAI 陷阱 (研究並記錄)

```yaml
# 需要研究並解決的代理人特定陷阱
implementation_gotchas:
  async_patterns:
    issue: "不一致地混合使用同步與非同步代理人呼叫"
    research: "PydanticAI 非同步 (async/await) 最佳實踐"
    solution: "[根據研究記錄]"
  
  model_limits:
    issue: "不同模型具備不同能力與 Token 限制"
    research: "模型提供者比較與能力分析"
    solution: "[根據研究記錄]"
  
  dependency_complexity:
    issue: "複雜的依賴圖可能難以除錯"
    research: "PydanticAI 中的依賴注入最佳實踐"
    solution: "[根據研究記錄]"
  
  tool_error_handling:
    issue: "工具執行失敗可能導致整個代理人運作崩潰"
    research: "工具的錯誤處理與重試模式"
    solution: "[根據研究記錄]"
```

## 實作藍圖 (Implementation Blueprint)

### 技術研究階段

**必須研究 —— 在實作前完成：**

✅ **PydanticAI 框架深挖：**
- [ ] 代理人建立模式與最佳實踐
- [ ] 模型提供者配置與備援策略
- [ ] 工具整合模式 (@agent.tool vs @agent.tool_plain)
- [ ] 依賴注入系統與型別安全
- [ ] 使用 TestModel 和 FunctionModel 的測試策略

✅ **代理人架構調查：**
- [ ] 專案結構慣例 (agent.py, tools.py, models.py, dependencies.py)
- [ ] 系統提示詞設計 (靜態 vs 動態)
- [ ] 使用 Pydantic 模型的結構化輸出驗證
- [ ] 非同步/同步模式與串流支援
- [ ] 錯誤處理與重試機制

✅ **安全性與生產模式：**
- [ ] API 金鑰管理與安全配置
- [ ] 輸入驗證與提示詞注入預防
- [ ] 速率限制與監控策略
- [ ] 記錄與觀測性 (Observability) 模式
- [ ] 部署與擴展考量

### 代理人實作計畫

```yaml
實作任務 1 —— 代理人架構設定 (遵循 main_agent_reference)：
  建立代理人專案結構：
    - settings.py：使用 pydantic-settings 的基於環境配置
    - providers.py：使用 get_llm_model() 的模型提供者抽象
    - agent.py：主要代理人定義 (預設字串輸出)
    - tools.py：具備正確裝飾器的工具函式
    - dependencies.py：外部服務整合 (dataclasses)
    - tests/：全面的測試套件

實作任務 2 —— 核心代理人開發：
  遵循 main_agent_reference 模式實作 agent.py：
    - 使用來自 providers.py 的 get_llm_model() 進行模型配置
    - 系統提示詞作為字串常量或函式
    - 使用 dataclass 進行依賴注入
    - 除非明確需要結構化輸出，否則不使用 result_type
    - 錯誤處理與日誌記錄

實作任務 3 —— 工具整合：
  開發 tools.py：
    - 具備 @agent.tool 裝飾器的工具函式
    - 整合 RunContext[DepsType] 以存取依賴項
    - 具備正確型別提示的參數驗證
    - 錯誤處理與重試機制
    - 工具說明文件與 Schema 生成

實作任務 4 —— 資料模型與依賴項：
  建立 models.py 與 dependencies.py：
    - 用於結構化輸出的 Pydantic 模型
    - 用於外部服務的依賴類別
    - 用於工具的輸入驗證模型
    - 自訂驗證器與約束

實作任務 5 —— 全面測試：
  實作測試套件：
    - 整合 TestModel 用於快速開發
    - 使用 FunctionModel 測試自訂行為
    - 使用 Agent.override() 模式進行隔離
    - 與真實提供者的整合測試
    - 工具驗證與錯誤場景測試

實作任務 6 —— 安全性與配置：
  設定安全模式：
    - 用於 API 金鑰的環境變數管理
    - 輸入清理與驗證
    - 速率限制實作
    - 安全記錄與監控
    - 生產部署配置
```

## 驗證迴圈 (Validation Loop)

### 第一層：代理人結構驗證

```bash
# 驗證完整的代理人專案結構
find agent_project -name "*.py" | sort
test -f agent_project/agent.py && echo "代理人定義存在"
test -f agent_project/tools.py && echo "工具模組存在"
test -f agent_project/models.py && echo "模型模組存在"
test -f agent_project/dependencies.py && echo "依賴模組存在"

# 驗證正確的 PydanticAI 匯入
grep -q "from pydantic_ai import Agent" agent_project/agent.py
grep -q "@agent.tool" agent_project/tools.py
grep -q "from pydantic import BaseModel" agent_project/models.py

# 預期：所有必要檔案均具備正確的 PydanticAI 模式
# 如果缺失：使用正確模式生成缺失的組件
```

### 第二層：代理人功能驗證

```bash
# 測試代理人是否可匯入與實例化
python -c "
from agent_project.agent import agent
print('代理人建立成功')
print(f'模型：{agent.model}')
print(f'工具數：{len(agent.tools)}')
"

# 使用 TestModel 進行驗證測試
python -c "
from pydantic_ai.models.test import TestModel
from agent_project.agent import agent
test_model = TestModel()
with agent.override(model=test_model):
    result = agent.run_sync('測試訊息')
    print(f'代理人回應：{result.output}')
"

# 預期：代理人實例化正常，工具已註冊，TestModel 驗證通過
# 如果失敗：除錯代理人配置與工具註冊
```

### 第三層：全面測試驗證

```bash
# 執行完整測試套件
cd agent_project
python -m pytest tests/ -v

# 測試特定的代理人行為
python -m pytest tests/test_agent.py::test_agent_response -v
python -m pytest tests/test_tools.py::test_tool_validation -v
python -m pytest tests/test_models.py::test_output_validation -v

# 預期：所有測試通過，達成全面覆蓋
# 如果失敗：根據測試失敗內容修復實作
```

### 第四層：生產就緒驗證

```bash
# 驗證安全性模式
grep -r "API_KEY" agent_project/ | grep -v ".py:" # 不應洩露金鑰
test -f agent_project/.env.example && echo "環境範本存在"

# 檢查錯誤處理
grep -r "try:" agent_project/ | wc -l  # 應具備錯誤處理
grep -r "except" agent_project/ | wc -l  # 應具備異常處理

# 驗證日誌設定
grep -r "logging\|logger" agent_project/ | wc -l  # 應具備日誌記錄

# 預期：安全措施到位，錯誤處理全面，日誌已配置
# 若有問題：實作缺失的安全性與生產模式
```

## 最終驗證檢查表 (Final Validation Checklist)

### 代理人實作完整性

- [ ] 完整的代理人專案結構：`agent.py`, `tools.py`, `models.py`, `dependencies.py`
- [ ] 具備正確模型提供者配置的代理人實例化。
- [ ] 具備 @agent.tool 裝飾器與 RunContext 整合的工具註冊。
- [ ] 具備 Pydantic 模型驗證的結構化輸出。
- [ ] 依賴注入已正確配置且經過測試。
- [ ] 包含 TestModel 與 FunctionModel 的全面測試套件。

### PydanticAI 最佳實踐

- [ ] 全程維持型別安全，具備正確的型別提示與驗證。
- [ ] 已實作安全性模式 (API 金鑰、輸入驗證、速率限制)。
- [ ] 錯誤處理與重試機制確保運行穩健。
- [ ] 非同步/同步模式保持一致且適當。
- [ ] 程式碼註解與說明文件便於維護。

### 生產就緒

- [ ] 具備 .env 檔案與驗證的環境配置。
- [ ] 已設定記錄與監控以實現觀測性。
- [ ] 效能優化與資源管理。
- [ ] 具備正確配置管理的部署就緒狀態。
- [ ] 記錄了維護與更新策略。

---

## 應避免的反模式 (Anti-Patterns to Avoid)

### PydanticAI 代理人開發

- ❌ 不要跳過 TestModel 驗證 —— 在開發過程中務必使用 TestModel 進行測試。
- ❌ 不要硬編碼 API 金鑰 —— 為所有憑證使用環境變數。
- ❌ 不要忽略非同步模式 —— PydanticAI 有特定的非同步/同步要求。
- ❌ 不要建立複雜的工具鏈 —— 保持工具專注且可組合。
- ❌ 不要跳過錯誤處理 —— 實作全面的重試與備援機制。

### 代理人架構

- ❌ 不要混用代理人類型 —— 清晰區分對話、工具、工作流與結構化輸出模式。
- ❌ 不要忽略依賴注入 —— 使用正確的型別安全依賴管理。
- ❌ 不要跳過輸出驗證 —— 務必為結構化回應使用 Pydantic 模型。
- ❌ 不要忘記工具說明文件 —— 確保所有工具均具備正確的描述與 Schema。

### 安全性與生產

- ❌ 不要洩露敏感數據 —— 為了安全性，驗證所有輸出與記錄。
- ❌ 不要跳過輸入驗證 —— 清理並驗證所有使用者輸入。
- ❌ 不要忽略速率限制 —— 為外部服務實作正確的節流。
- ❌ 不要未經監控就部署 —— 從一開始就包含正確的觀測性。

**研究狀態：[待完成]** —— 在實作開始前，先完成全面的 PydanticAI 研究。
