# 🔍 語義搜尋代理人 (Semantic Search Agent)

一個由 Pydantic AI 和具備 PGVector 的 PostgreSQL 驅動的智慧知識庫搜尋系統。該代理人提供語義搜尋與混合搜尋能力，並具備自動策略選擇和結果摘要功能。

## 功能 (Features)

- **語義搜尋**：使用嵌入 (Embeddings) 的純向量相似度搜尋。
- **混合搜尋**：結合語義和關鍵字匹配，以獲得精確結果。
- **智慧策略選擇**：代理人會根據查詢自動選擇最佳搜尋方法。
- **結果摘要**：從搜尋結果中生成連貫的見解。
- **互動式 CLI**：具備即時串流功能的豐富命令列介面。
- **多提供者支援**：支援任何與 OpenAI 相容的 API (OpenAI, Gemini, Ollama 等)。

## 前提條件 (Prerequisites)

- Python 3.10+
- 安裝了 PGVector 擴充功能的 PostgreSQL
- LLM API 金鑰 (OpenAI, Gemini, Ollama, Groq 或任何與 OpenAI 相容的提供者)
- 已包含文件與區塊 (Chunks) 的現有資料庫 (已提供 Schema)

## 安裝 (Installation)

1. **複製或拷貝代理人目錄**：
```bash
cd agents/rag_agent
```

2. **安裝依賴項**：
```bash
pip install -r requirements.txt
```

3. **設定具備 PGVector 的 PostgreSQL**：
```bash
# 最簡單的方法：如果您使用 Supabase/Postgres 等平台，請在 SQL 編輯器中執行 SQL

# 或使用 psql 執行 Schema
psql -d 您的資料庫名稱 -f sql/schema.sql
```

4. **配置環境變數**：
```bash
cp .env.example .env
# 使用您的憑證編輯 .env
```

5. **將文件攝取到資料庫中**：
```bash
# 此步驟在執行代理人之前是必需的
# 它將處理文件並生成嵌入
python -m ingestion.ingest --documents documents/
```

## 配置 (Configuration)

### 必要的環境變數

- `DATABASE_URL`：具備 PGVector 的 PostgreSQL 連線字串。
- `LLM_PROVIDER`：提供者名稱 (openai, anthropic, ollama 等)。
- `LLM_API_KEY`：您的 LLM 提供者 API 金鑰。
- `LLM_MODEL`：要使用的模型 (例如：gpt-4.1-mini, gemini-2.5-flash)。
- `LLM_BASE_URL`：API 基礎 URL (預設：https://api.openai.com/v1)。
- `EMBEDDING_MODEL`：要使用的嵌入模型 (例如：text-embedding-3-small, text-embedding-3-large)。

## 使用方式 (Usage)

### 命令列介面 (CLI)

執行互動式 CLI：
```bash
python -m cli
```

CLI 提供：
- 即時串流回應
- 工具執行可見性
- 對話 (Session) 持久化
- 使用者偏好管理

### 可用指令

- `help` —— 顯示可用指令。
- `info` —— 顯示系統配置。
- `clear` —— 清除螢幕。
- `set <key>=<value>` —— 設定偏好 (例如：`set text_weight=0.5`)。
- `exit/quit` —— 退出應用程式。

## 搜尋策略 (Search Strategies)

代理人會智慧地在兩種搜尋策略之間進行選擇：

### 語義搜尋 (Semantic Search)
最適合概念性查詢和尋找相關內容：
- 「與機器學習類似的概念」
- 「關於人工智慧的想法」
- 「與神經網路相關的內容」

### 混合搜尋 (Hybrid Search)
最適合具體事實和技術術語：
- 「OpenAI GPT-4 規格」
- 「NASDAQ:NVDA 股價」
- 「Sam Altman 的具體語錄」

代理人會根據您的查詢自動選擇適當的策略，或者您也可以在提示詞中明確要求特定的搜尋類型。

## 資料庫設定 (Database Setup)

### Schema 概覽

- **documents**：儲存完整文件及元數據。
- **chunks**：儲存帶有嵌入的文件區塊。
- **match_chunks()**：用於語義搜尋的函式。
- **hybrid_search()**：用於結合搜尋的函式。

## 開發 (Development)

### 執行測試
```bash
pytest tests/
```

### 程式碼格式化
```bash
black .
ruff check .
```

### 專案結構
```
semantic_search_agent/
├── agent.py           # 主要代理人實作
├── cli.py            # 命令列介面
├── dependencies.py   # 代理人依賴項
├── providers.py      # 模型提供者
├── prompts.py        # 系統提示詞
├── settings.py       # 配置
├── tools.py          # 搜尋工具
├── ingestion/        # 文件攝取管線
├── sql/              # 資料庫 Schema
└── documents/        # 範例文件
```
