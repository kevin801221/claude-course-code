name: "多代理人系統：具備郵件草稿子代理人的研究代理人 (Multi-Agent System: Research Agent with Email Draft Sub-Agent)"
description: |

## 目的 (Purpose)
構建一個 Pydantic AI 多代理人系統，其中主「研究代理人 (Research Agent)」使用 Brave Search API，並將「郵件草稿代理人 (Email Draft Agent)」(使用 Gmail API) 作為工具使用。這展示了將代理人作為工具 (Agent-as-tool) 的模式以及外部 API 的整合。

## 核心原則 (Core Principles)
1. **上下文至上 (Context is King)**：包含所有必要的說明文件、範例和注意事項。
2. **驗證迴圈 (Validation Loops)**：提供 AI 可以執行並修復的可執行測試/Lint 檢查。
3. **資訊密集 (Information Dense)**：使用程式碼庫中的關鍵字和模式。
4. **漸進式成功 (Progressive Success)**：從簡單開始，驗證，然後增強。

---

## 目標 (Goal)
建立一個生產級的多代理人系統，使用者可以透過 CLI 研究主題，研究代理人可以將郵件草稿任務委派給郵件草稿代理人。該系統應支援多個 LLM 提供者，並安全地處理 API 身分驗證。

## 為什麼 (Why)
- **業務價值**：自動化研究和郵件草稿工作流。
- **整合**：展示進階的 Pydantic AI 多代理人模式。
- **解決的問題**：減少基於研究的郵件通訊的手動工作量。

## 內容 (What)
一個基於 CLI 的應用程式，具備以下功能：
- 使用者輸入研究查詢。
- 研究代理人使用 Brave API 進行搜尋。
- 研究代理人可以呼叫郵件草稿代理人來建立 Gmail 草稿。
- 結果即時串流回傳給使用者。

### 成功準則 (Success Criteria)
- [ ] 研究代理人成功透過 Brave API 進行搜尋。
- [ ] 郵件代理人使用正確的身分驗證建立 Gmail 草稿。
- [ ] 研究代理人可以將郵件代理人作為工具呼叫。
- [ ] CLI 提供具備工具可見性的串流回應。
- [ ] 所有測試通過，且程式碼符合品質標準。

## 所有需要的上下文 (All Needed Context)

### 說明文件與參考資料 (Documentation & References)
```yaml
# 必讀 - 將這些內容包含在您的上下文視窗中
- url: https://ai.pydantic.dev/agents/
  why: 核心代理人建立模式
  
- url: https://ai.pydantic.dev/multi-agent-applications/
  why: 多代理人系統模式，特別是將代理人作為工具的模式
  
- url: https://developers.google.com/gmail/api/guides/sending
  why: Gmail API 身分驗證和草稿建立
  
- url: https://api-dashboard.search.brave.com/app/documentation
  why: Brave Search API REST 端點
  
- file: examples/agent/agent.py
  why: 代理人建立、工具註冊、依賴項的模式
  
- file: examples/agent/providers.py
  why: 多提供者 LLM 配置模式
  
- file: examples/cli.py
  why: 具備串流回應和工具可見性的 CLI 結構

- url: https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/create_draft.py
  why: 官方 Gmail 草稿建立範例
```

### 目前程式碼庫樹狀圖 (Current Codebase tree)
```bash
.
├── examples/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── providers.py
│   │   └── ...
│   └── cli.py
├── PRPs/
│   └── templates/
│       └── prp_base.md
├── INITIAL.md
├── CLAUDE.md
└── requirements.txt
```

### 期望的程式碼庫樹狀圖 (包含要新增的檔案) (Desired Codebase tree)
```bash
.
├── agents/
│   ├── __init__.py               # 套件初始化
│   ├── research_agent.py         # 具備 Brave Search 的主代理人
│   ├── email_agent.py           # 具備 Gmail 功能的子代理人
│   ├── providers.py             # LLM 提供者配置
│   └── models.py                # 用於資料驗證的 Pydantic 模型
├── tools/
│   ├── __init__.py              # 套件初始化
│   ├── brave_search.py          # Brave Search API 整合
│   └── gmail_tool.py            # Gmail API 整合
├── config/
│   ├── __init__.py              # 套件初始化
│   └── settings.py              # 環境和配置管理
├── tests/
│   ├── __init__.py              # 套件初始化
│   ├── test_research_agent.py   # 研究代理人測試
│   ├── test_email_agent.py      # 郵件代理人測試
│   ├── test_brave_search.py     # Brave 搜尋工具測試
│   ├── test_gmail_tool.py       # Gmail 工具測試
│   └── test_cli.py              # CLI 測試
├── cli.py                       # CLI 介面
├── .env.example                 # 環境變數範本
├── requirements.txt             # 更新後的依賴項
├── README.md                    # 全面的說明文件
└── credentials/.gitkeep         # Gmail 憑證目錄
```

### 已知陷阱與函式庫特殊行為 (Known Gotchas & Library Quirks)
```python
# 重要：Pydantic AI 要求全程非同步 (async) —— 不要在非同步上下文中呼叫同步函式
# 重要：Gmail API 在第一次執行時需要 OAuth2 流程 —— 需要 credentials.json
# 重要：Brave API 有速率限制 —— 免費層每月 2000 次請求
# 重要：將代理人作為工具的模式要求傳遞 ctx.usage 以進行 Token 追蹤
# 重要：Gmail 草稿需要使用正確的 MIME 格式進行 base64 編碼
# 重要：務必使用絕對匯入以保持程式碼整潔
# 重要：將敏感憑證儲存在 .env 中，切勿提交它們
```

## 實作藍圖 (Implementation Blueprint)

### 資料模型與結構 (Data models and structure)

```python
# models.py - 核心資料結構
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ResearchQuery(BaseModel):
    query: str = Field(..., description="要調查的研究主題")
    max_results: int = Field(10, ge=1, le=50)
    include_summary: bool = Field(True)

class BraveSearchResult(BaseModel):
    title: str
    url: str
    description: str
    score: float = Field(0.0, ge=0.0, le=1.0)

class EmailDraft(BaseModel):
    to: List[str] = Field(..., min_items=1)
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None

class ResearchEmailRequest(BaseModel):
    research_query: str
    email_context: str = Field(..., description="生成郵件的上下文")
    recipient_email: str
```

### 任務列表 (List of tasks to be completed)

```yaml
任務 1: 設定配置與環境
建立 config/settings.py:
  - 模式：使用 pydantic-settings，就像範例中使用 os.getenv 一樣
  - 載入帶有預設值的環境變數
  - 驗證所需的 API 金鑰是否存在

建立 .env.example:
  - 包含所有必要的環境變數及其說明
  - 遵循 examples/README.md 的模式

任務 2: 實作 Brave 搜尋工具
建立 tools/brave_search.py:
  - 模式：參考 examples/agent/tools.py 使用非同步函式
  - 使用 httpx 建立簡單的 REST 客戶端 (已在 requirements 中)
  - 優雅地處理速率限制和錯誤
  - 回傳結構化的 BraveSearchResult 模型

任務 3: 實作 Gmail 工具
建立 tools/gmail_tool.py:
  - 模式：遵循 Gmail 快速入門的 OAuth2 流程
  - 將 token.json 儲存在 credentials/ 目錄中
  - 使用正確的 MIME 編碼建立草稿
  - 自動處理驗證刷新 (Refresh)

任務 4: 建立郵件草稿代理人
建立 agents/email_agent.py:
  - 模式：遵循 examples/agent/agent.py 結構
  - 使用帶有 deps_type 模式的 Agent
  - 將 gmail_tool 註冊為 @agent.tool
  - 回傳 EmailDraft 模型

任務 5: 建立研究代理人
建立 agents/research_agent.py:
  - 模式：遵循 Pydantic AI 文件中的多代理人模式
  - 將 brave_search 註冊為工具
  - 將 email_agent.run() 註冊為工具
  - 使用 RunContext 進行依賴注入

任務 6: 實作 CLI 介面
建立 cli.py:
  - 模式：遵循 examples/cli.py 的串流模式
  - 帶有工具可見性的顏色代碼輸出
  - 使用 asyncio.run() 正確處理非同步
  - 對話上下文的對話管理

任務 7: 新增全面的測試
建立 tests/:
  - 模式：鏡像範例測試結構
  - 模擬外部 API 呼叫
  - 測試正常路徑、邊緣情況、錯誤
  - 確保 80% 以上的覆蓋率

任務 8: 建立說明文件
建立 README.md:
  - 模式：遵循 examples/README.md 結構
  - 包含設定、安裝、使用說明
  - API 金鑰配置步驟
  - 架構圖
```

### 各項任務虛擬碼 (Per task pseudocode)

```python
# 任務 2: Brave 搜尋工具
async def search_brave(query: str, api_key: str, count: int = 10) -> List[BraveSearchResult]:
    # 模式：使用 httpx，就像範例中使用 aiohttp 一樣
    async with httpx.AsyncClient() as client:
        headers = {"X-Subscription-Token": api_key}
        params = {"q": query, "count": count}
        
        # 注意事項：如果 API 金鑰無效，Brave API 會回傳 401
        response = await client.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers=headers,
            params=params,
            timeout=30.0  # 重要：設定逾時以避免掛起
        )
        
        # 模式：結構化錯誤處理
        if response.status_code != 200:
            raise BraveAPIError(f"API 回傳了 {response.status_code}")
        
        # 使用 Pydantic 解析並驗證
        data = response.json()
        return [BraveSearchResult(**result) for result in data.get("web", {}).get("results", [])]

# 任務 5: 具備郵件代理人作為工具的研究代理人
@research_agent.tool
async def create_email_draft(
    ctx: RunContext[AgentDependencies],
    recipient: str,
    subject: str,
    context: str
) -> str:
    """根據研究上下文建立郵件草稿。"""
    # 重要：傳遞 usage 以進行 Token 追蹤
    result = await email_agent.run(
        f"建立一封給 {recipient} 的郵件，關於： {context}",
        deps=EmailAgentDeps(subject=subject),
        usage=ctx.usage  # 參考多代理人文件的模式
    )
    
    return f"草稿已建立，ID 為： {result.data}"
```

### 整合點 (Integration Points)
```yaml
環境：
  - 新增至： .env
  - 變數： |
      # LLM 配置
      LLM_PROVIDER=openai
      LLM_API_KEY=sk-...
      LLM_MODEL=gpt-4
      
      # Brave 搜尋
      BRAVE_API_KEY=BSA...
      
      # Gmail (credentials.json 路徑)
      GMAIL_CREDENTIALS_PATH=./credentials/credentials.json
      
配置：
  - Gmail OAuth：第一次執行時會開啟瀏覽器進行授權。
  - Token 儲存： ./credentials/token.json (自動建立)。
  
依賴項：
  - 更新 requirements.txt，新增：
    - google-api-python-client
    - google-auth-httplib2
    - google-auth-oauthlib
```

## 驗證迴圈 (Validation Loop)

### 第一層：語法與風格
```bash
# 首先執行這些 —— 在繼續之前修復任何錯誤
ruff check . --fix              # 自動修復風格問題
mypy .                          # 型別檢查

# 預期：無錯誤。如果有錯誤，請閱讀並修復。
```

### 第二層：單元測試
```python
# test_research_agent.py
async def test_research_with_brave():
    """測試研究代理人是否能正確搜尋"""
    agent = create_research_agent()
    result = await agent.run("AI 安全性研究")
    assert result.data
    assert len(result.data) > 0

async def test_research_creates_email():
    """測試研究代理人是否能呼叫郵件代理人"""
    agent = create_research_agent()
    result = await agent.run(
        "研究 AI 安全性並為 john@example.com 起草郵件"
    )
    assert "draft_id" in result.data

# test_email_agent.py  
def test_gmail_authentication(monkeypatch):
    """測試 Gmail OAuth 流程處理"""
    monkeypatch.setenv("GMAIL_CREDENTIALS_PATH", "test_creds.json")
    tool = GmailTool()
    assert tool.service is not None

async def test_create_draft():
    """測試具備正確編碼的草稿建立"""
    agent = create_email_agent()
    result = await agent.run(
        "建立一封給 test@example.com 關於 AI 研究的郵件"
    )
    assert result.data.get("draft_id")
```

```bash
# 迭代執行測試直到通過：
pytest tests/ -v --cov=agents --cov=tools --cov-report=term-missing

# 如果失敗：除錯特定測試，修復程式碼，重新執行
```

### 第三層：整合測試 (Integration Test)
```bash
# 測試 CLI 互動
python cli.py

# 預期互動：
# 您：研究最新的 AI 安全性進展
# 🤖 助手：[串流研究結果]
# 🛠 使用的工具：
#   1. brave_search (query='AI 安全性進展', limit=10)
#
# 您：關於此內容，為 john@example.com 建立一封郵件草稿
# 🤖 助手：[建立草稿]
# 🛠 使用的工具：
#   1. create_email_draft (recipient='john@example.com', ...)

# 檢查 Gmail 草稿資料夾以確認已建立草稿
```

## 最終驗證檢查表 (Final Validation Checklist)
- [ ] 所有測試通過： `pytest tests/ -v`
- [ ] 無 Lint 錯誤： `ruff check .`
- [ ] 無型別錯誤： `mypy .`
- [ ] Gmail OAuth 流程正常 (瀏覽器開啟，Token 已儲存)
- [ ] Brave Search 回傳結果
- [ ] 研究代理人成功呼叫郵件代理人
- [ ] CLI 具備工具可見性地串流回應
- [ ] 優雅地處理錯誤情況
- [ ] README 包含清晰的設定說明
- [ ] .env.example 包含所有必要的變數

---

## 應避免的反模式 (Anti-Patterns to Avoid)
- ❌ 不要硬編碼 API 金鑰 —— 使用環境變數。
- ❌ 不要在非同步代理人上下文中呼叫同步函式。
- ❌ 不要跳過 Gmail 的 OAuth 流程設定。
- ❌ 不要忽略 API 的速率限制。
- ❌ 在多代理人呼叫中不要忘記傳遞 `ctx.usage`。
- ❌ 不要提交 `credentials.json` 或 `token.json` 檔案。

## 置信度評分 (Confidence Score)：9/10

置信度高，原因如下：
- 有程式碼庫中清晰的範例可供遵循。
- 外部 API 文件齊全。
- 多代理人系統模式成熟。
- 具備全面的驗證關卡。

關於 Gmail OAuth 首次設定的使用者體驗存在細微的不確定性，但說明文件提供了清晰的指引。
