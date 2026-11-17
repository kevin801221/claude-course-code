---
name: "PydanticAI 範本生成器 PRP (PydanticAI Template Generator PRP)"
description: "生成 PydanticAI 代理人開發的全面上下文工程範本，包含工具、記憶和結構化輸出"
---

## 目的 (Purpose)

為 **PydanticAI** 生成一個完整的上下文工程範本包，使開發人員能夠利用 PydanticAI 框架快速構建具備工具整合、對話處理和結構化資料驗證功能的智慧 AI 代理人。

## 核心原則 (Core Principles)

1. **PydanticAI 專業化**：與 PydanticAI 的代理人建立、工具和結構化輸出模式深度整合。
2. **完整包生成**：建立包含可運行範例和驗證功能的整個範本生態系統。
3. **型別安全優先**：全程利用 PydanticAI 的型別安全設計和 Pydantic 驗證。
4. **生產就緒**：為生產部署包含安全性、測試和最佳實踐。
5. **上下文工程整合**：將經過驗證的上下文工程工作流應用於 AI 代理人開發。

---

## 目標 (Goal)

為 **PydanticAI** 生成一個完整的上下文工程範本包，包含：

- PydanticAI 特定的 CLAUDE.md 實作指引，包含代理人模式。
- 專為 AI 代理人設計的專門 PRP 生成與執行命令。
- 具備代理人架構模式的領域特定基礎 PRP 範本。
- 全面的可運行範例 (對話代理人、工具整合、多步驟工作流)。
- PydanticAI 特定的驗證迴圈與測試模式。

## 為什麼 (Why)

- **AI 開發加速**：實現生產級 PydanticAI 代理人的快速開發。
- **模式一致性**：維持已建立的 AI 代理人架構模式與最佳實踐。
- **品質保證**：確保對代理人行為、工具和輸出進行全面測試。
- **知識捕捉**：記錄 PydanticAI 特定的模式、陷阱與整合策略。
- **可擴展 AI 框架**：為各種 AI 代理人使用案例建立可重用的範本。

## 內容 (What)

### 範本包組件 (Template Package Components)

**完整的目錄結構：**
```
use-cases/pydantic-ai/
├── CLAUDE.md                           # PydanticAI 實作指引
├── .claude/commands/
│   ├── generate-pydantic-ai-prp.md     # 代理人 PRP 生成
│   └── execute-pydantic-ai-prp.md      # 代理人 PRP 執行  
├── PRPs/
│   ├── templates/
│   │   └── prp_pydantic_ai_base.md     # PydanticAI 基礎 PRP 範本
│   ├── ai_docs/                        # PydanticAI 說明文件
│   └── INITIAL.md                      # 範例代理人功能請求
├── examples/
│   ├── basic_chat_agent/               # 具備記憶的簡單對話代理人
│   ├── tool_enabled_agent/             # 網頁搜尋 + 計算機工具
│   ├── workflow_agent/                 # 多步驟工作流處理
│   ├── structured_output_agent/        # 自訂 Pydantic 模型
│   └── testing_examples/               # 代理人測試模式
├── copy_template.py                    # 範本部署腳本
└── README.md                           # 全面的使用指南
```

**PydanticAI 整合：**
- 使用多個模型提供者 (OpenAI, Anthropic, Gemini) 建立代理人。
- 工具整合模式與函式註冊。
- 使用依賴項進行對話記憶與上下文管理。
- 使用 Pydantic 模型的結構化輸出驗證。
- 使用 TestModel 與 FunctionModel 的測試模式。
- API 金鑰管理與輸入驗證的安全性模式。

**上下文工程調整：**
- PydanticAI 特定的研究流程與文件參考。
- 適合代理人的驗證迴圈與測試策略。
- AI 框架專門化的實作藍圖。
- 與 AI 開發基礎上下文工程原則的整合。

### 成功準則 (Success Criteria)

- [ ] 已生成完整的 PydanticAI 範本包結構。
- [ ] 所有必要檔案均具備 PydanticAI 特定的內容。
- [ ] 代理人模式準確呈現了 PydanticAI 的最佳實踐。
- [ ] 上下文工程原則已為 AI 代理人開發進行調整。
- [ ] 驗證迴圈適合測試 AI 代理人與工具。
- [ ] 範本可立即用於建立 PydanticAI 專案。
- [ ] 與基礎上下文工程框架的整合保持完好。
- [ ] 包含全面的範例與測試文件。

## 所有需要的上下文 (All Needed Context)

### 說明文件與參考資料 (已研究)

```yaml
# 重要 —— 使用 Archon MCP 伺服器獲取更多 Pydantic AI 文件！
- mcp: Archon
  why: 官方 Pydantic AI 文件，可用於 RAG 查詢
  content: 所有 Pydantic AI 文件
  
# PYDANTIC AI 核心文件 —— 基礎框架理解
- url: https://ai.pydantic.dev/
  why: 官方 PydanticAI 文件，包含核心概念與入門
  content: 代理人建立、模型提供者、型別安全、依賴注入

- url: https://ai.pydantic.dev/agents/
  why: 全面的代理人架構、系統提示詞、工具、結構化輸出
  content: 代理人組件、執行方法、配置選項

- url: https://ai.pydantic.dev/models/
  why: 模型提供者配置、API 金鑰管理、備援模型
  content: OpenAI, Anthropic, Gemini 整合模式與身分驗證

- url: https://ai.pydantic.dev/tools/
  why: 函式工具註冊、上下文用法、豐富的回傳、動態工具
  content: 工具裝飾器、參數驗證、文件模式

- url: https://ai.pydantic.dev/testing/
  why: 測試策略、TestModel、FunctionModel、pytest 模式
  content: 單元測試、代理人行為驗證、模擬模型用法

- url: https://ai.pydantic.dev/examples/
  why: 各種 PydanticAI 使用案例的可運行範例
  content: 聊天應用、RAG 系統、SQL 生成、FastAPI 整合

# 上下文工程基礎 —— 要調整的基礎框架
- file: ../../../README.md
  why: 要為 AI 代理人調整的核心上下文工程原則與工作流

- file: ../../../.claude/commands/generate-prp.md
  why: 要為 PydanticAI 開發專門化的基礎 PRP 生成模式

- file: ../../../.claude/commands/execute-prp.md  
  why: 要為 AI 代理人驗證調整的基礎 PRP 執行模式

- file: ../../../PRPs/templates/prp_base.md
  why: 要為 PydanticAI 領域專門化的基礎 PRP 範本結構

# MCP 伺服器範例 —— 參考實作
- file: ../mcp-server/CLAUDE.md
  why: 領域特定實作指引模式的範例
  
- file: ../mcp-server/.claude/commands/prp-mcp-create.md
  why: 專門的 PRP 生成命令結構範例
```

### PydanticAI 框架分析 (來自研究)

```typescript
// PydanticAI 架構模式 (來自官方文件)
interface PydanticAIPatterns {
  // 核心代理人模式
  agent_creation: {
    model_providers: ["openai:gpt-4o", "anthropic:claude-3-sonnet", "google:gemini-1.5-flash"];
    configuration: ["system_prompt", "deps_type", "output_type", "instructions"];
    execution_methods: ["run()", "run_sync()", "run_stream()", "iter()"];
  };
  
  // 工具整合模式
  tool_system: {
    registration: ["@agent.tool", "@agent.tool_plain", "tools=[]"];
    context_access: ["RunContext[DepsType]", "ctx.deps", "dependency_injection"];
    return_types: ["str", "ToolReturn", "structured_data", "rich_content"];
    validation: ["parameter_schemas", "docstring_extraction", "type_hints"];
  };
  
  // 測試與驗證
  testing_patterns: {
    unit_testing: ["TestModel", "FunctionModel", "Agent.override()"];
    validation: ["capture_run_messages()", "pytest_fixtures", "mock_dependencies"];
    evals: ["model_performance", "agent_behavior", "production_monitoring"];
  };
  
  // 生產考量
  security: {
    api_keys: ["environment_variables", "secure_storage", "key_rotation"];
    input_validation: ["pydantic_models", "parameter_validation", "sanitization"];
    monitoring: ["logfire_integration", "usage_tracking", "error_handling"];
  };
}
```

### 開發工作流分析 (來自研究)

```yaml
# PydanticAI 開發模式 (根據文件與範例研究)
專案結構：
  基礎模式： |
    my_agent/
    ├── agent.py          # 主要代理人定義
    ├── tools.py          # 工具函式
    ├── models.py         # Pydantic 輸出模型
    ├── dependencies.py   # 上下文依賴項
    └── tests/
        ├── test_agent.py
        └── test_tools.py

  進階模式： |
    agents_project/
    ├── agents/
    │   ├── __init__.py
    │   ├── chat_agent.py
    │   └── workflow_agent.py
    ├── tools/
    │   ├── __init__.py
    │   ├── web_search.py
    │   └── calculator.py
    ├── models/
    │   ├── __init__.py
    │   └── outputs.py
    ├── dependencies/
    │   ├── __init__.py
    │   └── database.py
    ├── tests/
    └── examples/

套件管理：
  安裝： "pip install pydantic-ai"
  選用依賴： "pip install 'pydantic-ai[examples]'"
  開發依賴： "pip install pytest pytest-asyncio inline-snapshot dirty-equals"

測試工作流：
  單元測試： "pytest tests/ -v"
  代理人測試： "使用 TestModel 進行快速驗證"
  整合測試： "使用帶有速率限制的真實模型"
  評測 (Evals)： "單獨執行效能基準測試"

環境設定：
  API 金鑰： ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"]
  開發環境： "測試時設定 ALLOW_MODEL_REQUESTS=False"
  生產環境： "配置正確的日誌記錄與監控"
```

### 安全性與最佳實踐 (來自研究)

```typescript
// PydanticAI 特定的安全模式 (來自研究)
interface PydanticAISecurity {
  // API 金鑰管理
  api_security: {
    storage: "僅限環境變數";
    access_control: "最小權限原則";
    monitoring: "使用追蹤與告警";
  };
  
  // 輸入驗證與清理
  input_security: {
    validation: "為所有輸入使用 Pydantic 模型";
    sanitization: "轉義使用者內容";
    rate_limiting: "預防濫用模式";
    content_filtering: "阻擋惡意提示詞";
  };
  
  // 提示詞注入預防
  prompt_security: {
    system_prompts: "清晰的指令邊界";
    user_input: "驗證與清理";
    tool_calls: "參數驗證";
    output_filtering: "結構化回應驗證";
  };
  
  // 生產考量
  production_security: {
    monitoring: "建議整合 Logfire";
    error_handling: "日誌中不包含敏感數據";
    dependency_injection: "安全的上下文管理";
    testing: "專注於安全性的單元測試";
  };
}
```

### 常見陷阱與邊緣情況 (來自研究)

```yaml
# 透過研究發現的 PydanticAI 特定陷阱
代理人陷阱：
  模型限制：
    問題： "不同模型具備不同的 Token 限制與能力"
    解決方案： "使用 FallbackModel 進行自動模型切換"
    驗證： "使用多個模型提供者進行測試"
  
  非同步模式：
    問題： "混合使用同步與非同步代理人呼叫會導致問題"
    解決方案： "全程使用一致的 async/await 模式"
    驗證： "測試同步與非同步的執行路徑"
  
  依賴注入：
    問題： "複雜的依賴圖難以除錯"
    解決方案： "保持依賴項簡單且具備良好型別"
    驗證： "單獨對依賴項進行單元測試"

工具整合陷阱：
  參數驗證：
    問題： "工具可能會收到意外的參數類型"
    解決方案： "為工具參數使用嚴格的 Pydantic 模型"
    驗證： "使用無效輸入測試工具"
  
  上下文管理：
    問題： "RunContext 狀態可能變得不一致"
    解決方案： "盡可能設計無狀態工具"
    驗證： "測試每次執行之間的上下文隔離"
  
  錯誤處理：
    問題： "工具錯誤可能導致整個代理人執行崩潰"
    解決方案： "實作重試機制與優雅降級"
    驗證： "測試錯誤場景與恢復"

測試陷阱：
  模型成本：
    問題： "真實模型測試可能非常昂貴"
    解決方案： "開發時使用 TestModel 與 FunctionModel"
    驗證： "將單元測試與昂貴的評測執行分開"
  
  非同步測試：
    問題： "非同步代理人測試需要特殊設定"
    解決方案： "使用 pytest-asyncio 與正確的 fixtures"
    驗證： "測試同步與非同步的程式碼路徑"
  
  確定性行為：
    問題： "AI 回應本質上是非確定性的"
    解決方案： "專注於測試工具呼叫與結構化輸出"
    驗證： "為複雜的斷言使用 inline-snapshot"
```

## 實作藍圖 (Implementation Blueprint)

### 技術研究階段 (已完成)

**PydanticAI 全面分析已完成：**

✅ **核心框架分析：**
- PydanticAI 架構、代理人建立模式、模型提供者整合。
- 來自官方文件與範例的專案結構慣例。
- 依賴注入系統與型別安全設計原則。
- 具備非同步/同步模式與串流支援的開發工作流。

✅ **工具系統調查：**
- 函式工具註冊模式 (@agent.tool vs @agent.tool_plain)。
- 使用 RunContext 與依賴注入的上下文管理。
- 參數驗證、Docstring 提取與 Schema 生成。
- 豐富的回傳類型與多模態內容支援。

✅ **測試框架分析：**
- 無需 API 呼叫的 TestModel 與 FunctionModel 單元測試。
- 用於測試隔離的 Agent.override() 模式。
- 具備非同步測試與 fixtures 的 Pytest 整合。
- 模型效能評估 vs 單元測試的策略。

✅ **安全性與生產模式：**
- 使用環境變數與安全存儲進行 API 金鑰管理。
- 使用 Pydantic 模型與參數 Schema 進行輸入驗證。
- 速率限制、監控以及 Logfire 整合。
- 常見安全漏洞與預防策略。

### 範本包生成

根據研究結果建立完整的 PydanticAI 上下文工程範本：

```yaml
生成任務 1 —— 建立 PydanticAI 範本目錄結構：
  建立完整的用例目錄結構：
    - use-cases/pydantic-ai/
    - 具備 PydanticAI 特定斜線命令的 .claude/commands/
    - 具備代理人專用基礎範本的 PRPs/templates/
    - 具備可運行代理人實作的 examples/
    - 根據範本包要求建立所有子目錄

生成任務 2 —— 生成 PydanticAI 特定 CLAUDE.md：
  建立 PydanticAI 全局規則檔案，包含：
    - PydanticAI 代理人建立與工具整合模式
    - 模型提供者配置與 API 金鑰管理
    - 代理人架構模式 (對話、工作流、工具化)
    - 使用 TestModel/FunctionModel 的測試策略
    - AI 代理人與工具整合的安全性最佳實踐
    - 常見陷阱：非同步模式、上下文管理、模型限制

生成任務 3 —— 建立 PydanticAI PRP 命令：
  生成領域特定的斜線命令：
    - generate-pydantic-ai-prp.md 帶有代理人研究模式
    - execute-pydantic-ai-prp.md 帶有 AI 代理人驗證迴圈
    - 包含 PydanticAI 文件參考與研究策略
    - 代理人特定成功準則與測試需求

生成任務 4 —— 開發 PydanticAI 基礎 PRP 範本：
  建立專門的 prp_pydantic_ai_base.md 範本：
    - 預填入來自研究的代理人架構模式
    - PydanticAI 特定成功準則與驗證關卡
    - 官方文件參考與模型提供者指南
    - 具備 TestModel 的代理人測試模式與驗證策略

生成任務 5 —— 建立可運行的 PydanticAI 範例：
  生成全面的範例代理人：
    - basic_chat_agent：具備記憶的簡單對話
    - tool_enabled_agent：網頁搜尋與計算機整合
    - workflow_agent：多步驟任務處理
    - structured_output_agent：自訂 Pydantic 模型
    - testing_examples：單元測試與驗證模式
    - 包含配置檔案與環境設定

生成任務 6 —— 建立範本複製腳本：
  建立用於範本部署的 Python 腳本：
    - 具備命令列介面的 copy_template.py
    - 將整個 PydanticAI 範本結構複製到目標位置
    - 處理所有檔案：CLAUDE.md, 命令, PRPs, 範例等
    - 錯誤處理與帶有後續步驟的成功回饋

生成任務 7 —— 生成全面的 README：
  建立 PydanticAI 特定的 README.md：
    - 清晰描述：「PydanticAI 上下文工程範本」
    - 範本複製腳本使用說明 (顯眼地放在頂部)
    - 用於 AI 代理人開發的 PRP 框架工作流
    - 帶有 PydanticAI 特定說明的範本結構
    - 帶有代理人建立範例的快速開始指南
    - 可運行範例概覽與測試模式
```

### PydanticAI 專業化細節

```typescript
// PydanticAI 的範本專業化
const pydantic_ai_specialization = {
  agent_patterns: [
    "具備記憶的對話代理人",
    "工具整合代理人", 
    "工作流處理代理人",
    "結構化輸出代理人"
  ],
  
  validation: [
    "代理人行為測試",
    "工具函式驗證", 
    "輸出 Schema 核實",
    "模型提供者相容性"
  ],
  
  examples: [
    "基礎對話代理人",
    "網頁搜尋與計算機工具",
    "多步驟工作流處理",
    "自訂 Pydantic 輸出模型",
    "全面的測試套件"
  ],
  
  gotchas: [
    "非同步/同步混合問題",
    "模型 Token 限制",
    "依賴注入複雜性",
    "工具錯誤處理失敗",
    "上下文狀態管理"
  ],
  
  security: [
    "API 金鑰環境管理",
    "使用 Pydantic 模型進行輸入驗證",
    "提示詞注入預防",
    "速率限制實作",
    "安全的工具參數處理"
  ]
};
```

### 整合點 (Integration Points)

```yaml
上下文工程框架：
  - 基礎工作流：繼承 PRP 生成/執行，並為 AI 代理人開發進行調整
  - 驗證原則：使用 AI 特定測試 (代理人行為、工具驗證) 擴展基礎驗證
  - 文件標準：在為 PydanticAI 專業化的同時維持一致性

PYDANTIC_AI 整合：
  - 代理人架構：包含對話、工具化與工作流代理人模式
  - 模型提供者：支援 OpenAI, Anthropic, Gemini 配置模式
  - 測試框架：開發驗證使用 TestModel/FunctionModel
  - 生產模式：包含安全性、監控與部署考量

範本結構：
  - 目錄組織：遵循具備 AI 特定範例的使用案例範本模式
  - 檔案命名：generate-pydantic-ai-prp.md, prp_pydantic_ai_base.md
  - 內容格式：帶有代理人程式碼範例與配置的 Markdown
  - 命令模式：為 AI 代理人開發工作流擴展斜線命令
```

## 驗證迴圈 (Validation Loop)

### 第一層：PydanticAI 範本結構驗證

```bash
# 驗證完整的 PydanticAI 範本包結構
find use-cases/pydantic-ai -type f | sort
ls -la use-cases/pydantic-ai/.claude/commands/
ls -la use-cases/pydantic-ai/PRPs/templates/
ls -la use-cases/pydantic-ai/examples/

# 驗證複製腳本與代理人範例
test -f use-cases/pydantic-ai/copy_template.py
ls use-cases/pydantic-ai/examples/*/agent.py 2>/dev/null | wc -l  # 應有代理人檔案
python use-cases/pydantic-ai/copy_template.py --help 2>/dev/null || echo "複製腳本需要 Help 選項"

# 預期：所有必要檔案均存在，包含可運行的代理人範例
# 如果缺失：使用 PydanticAI 模式生成缺失組件
```

### 第二層：PydanticAI 內容品質驗證

```bash
# 驗證 PydanticAI 特定內容的準確性
grep -r "from pydantic_ai import Agent" use-cases/pydantic-ai/examples/
grep -r "@agent.tool" use-cases/pydantic-ai/examples/
grep -r "TestModel\|FunctionModel" use-cases/pydantic-ai/

# 檢查 PydanticAI 模式，避免通用內容
grep -r "TODO\|PLACEHOLDER" use-cases/pydantic-ai/
grep -r "openai:gpt-4o\|anthropic:" use-cases/pydantic-ai/
grep -r "RunContext\|deps_type" use-cases/pydantic-ai/

# 預期：真實的 PydanticAI 程式碼，無佔位符，代理人模式已呈現
# 若有問題：新增正確的 PydanticAI 特定模式與範例
```

### 第三層：PydanticAI 功能驗證

```bash
# 測試 PydanticAI 範本功能
cd use-cases/pydantic-ai

# 測試以代理人為核心的 PRP 生成
/generate-pydantic-ai-prp INITIAL.md
ls PRPs/*.md | grep -v templates | head -1  # 應生成代理人 PRP

# 驗證代理人範例是否可解析 (語法檢查)
python -m py_compile examples/basic_chat_agent/agent.py 2>/dev/null && echo "基礎代理人語法 OK"
python -m py_compile examples/tool_enabled_agent/agent.py 2>/dev/null && echo "工具代理人語法 OK"

# 預期：PRP 生成正常，代理人範例語法有效
# 如果失敗：除錯 PydanticAI 命令模式並修復代理人程式碼
```

### 第四層：PydanticAI 整合測試

```bash
# 驗證 PydanticAI 專業化是否維持基礎框架相容性
diff -r ../../.claude/commands/ .claude/commands/ | head -10
grep -r "Context is King" . | wc -l  # 應繼承基礎原則
grep -r "pydantic.ai.dev\|PydanticAI" . | wc -l  # 應有專業化內容

# 測試代理人範例是否具備正確依賴項
grep -r "pydantic_ai" examples/ | wc -l  # 應匯入 PydanticAI
grep -r "pytest" examples/testing_examples/ | wc -l  # 應有測試

# 預期：正確的專業化、可運行的代理人模式、包含測試
# 若有問題：在新增 PydanticAI 功能的同時調整以維持相容性
```

## 最終驗證檢查表 (Final Validation Checklist)

### PydanticAI 範本包完整性

- [ ] 完整的目錄結構： `tree use-cases/pydantic-ai`
- [ ] PydanticAI 特定檔案：具備代理人模式的 CLAUDE.md、專門的指令。
- [ ] 複製腳本存在：具備正確 PydanticAI 功能的 `copy_template.py`。
- [ ] README 內容全面：包含代理人開發工作流與複製說明。
- [ ] 代理人範例可運行：所有範例均使用真實的 PydanticAI 程式碼模式。
- [ ] 包含測試模式：TestModel/FunctionModel 範例與驗證。
- [ ] 說明文件完整：已記錄 PydanticAI 特定的模式與陷阱。

### PydanticAI 的品質與易用性

- [ ] 無佔位符內容： `grep -r "TODO\|PLACEHOLDER"` 回傳為空。
- [ ] PydanticAI 專業化：代理人模式、工具、測試已正確記錄。
- [ ] 驗證迴圈正常：所有指令均可執行並具備代理人特定功能。
- [ ] 框架整合：可與 AI 開發的基礎上下文工程協作。
- [ ] AI 開發就緒：開發人員可立即建立 PydanticAI 代理人。

### PydanticAI 框架整合

- [ ] 繼承基礎原則：保留 AI 開發的 PRP 工作流。
- [ ] 正確的 AI 專業化：包含 PydanticAI 模式、安全性、測試。
- [ ] 指令相容性：斜線命令適用於代理人開發工作流。
- [ ] 文件一致性：在專業化 AI 開發的同時遵循建立的模式。
- [ ] 可維護結構：隨 PydanticAI 框架演進易於更新。

---

## 應避免的反模式 (Anti-Patterns to Avoid)

### PydanticAI 範本生成

- ❌ 不要建立通用的 AI 範本 —— 徹底研究 PydanticAI 的細節。
- ❌ 不要跳過代理人架構研究 —— 理解工具、記憶、驗證。
- ❌ 不要使用佔位符代理人程式碼 —— 包含真實、可運行的 PydanticAI 範例。
- ❌ 不要忽略測試模式 —— TestModel/FunctionModel 對於 AI 至關重要。

### PydanticAI 內容品質

- ❌ 不要假設 AI 模式 —— 為該領域明確記錄 PydanticAI 特定的陷阱。
- ❌ 不要跳過安全性研究 —— API 金鑰、輸入驗證、提示注入至關重要。
- ❌ 不要忽略模型提供者 —— 包含 OpenAI, Anthropic, Gemini 模式。
- ❌ 不要忘記非同步模式 —— PydanticAI 有特定的非同步/同步考量。

### PydanticAI 框架整合

- ❌ 不要破壞上下文工程 —— 維持 AI 開發的 PRP 工作流。
- ❌ 不要重複基礎功能 —— 進行適當的擴展與專業化。
- ❌ 不要忽略 AI 特定驗證 —— 代理人行為測試是獨特的需求。
- ❌ 不要跳過真實範例 —— 包含具備工具與驗證功能的可運行代理人。

**置信度評分：9/10** —— 已完成全面的 PydanticAI 研究，理解框架模式，準備好為 AI 代理人開發生成專門的上下文工程範本。
