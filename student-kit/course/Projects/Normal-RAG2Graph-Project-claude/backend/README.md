# Normal-RAG2Graph Backend

這是一個基於 FastAPI 開發的 Hybrid GraphRAG 後端系統，提供純向量檢索 (Vector RAG) 以及知識圖譜 (GraphRAG) 的雙模式 API。

## 技術棧 (Tech Stack)
- **Framework**: FastAPI (Python 3.10+)
- **Dependency Manager**: `uv` (依據專案憲法，強制使用此工具管理套件，不可使用 pip 或 poetry)
- **Vector DB**: ChromaDB (本地 Persistent 模式)
- **Knowledge Graph**: SQLite (`local_graph.db`)
- **LLM**: Google Gemini API
  - 生成與萃取: `gemini-2.5-flash`
  - 向量化 Embedding: `models/gemini-embedding-001` (系統寫死，不可更改)

## 啟動與安裝指南

### 1. 設置環境變數
系統核心依賴於 Google Gemini API，您必須在啟動前設置環境變數。您可以在最外層專案目錄創建 `.env` 檔案，或是直接在終端機 `export` 變數：

```bash
# MacOS / Linux
export GEMINI_API_KEY="AIzaSyYour-Google-Gemini-API-Key-Here"
```
*(注意：為了資料安全，切勿將包含真實 API Key 的 `.env` 提交進版本控制)*

### 2. 啟動後端伺服器 (開發模式)
進入 `backend/` 目錄後，透過 `uv` 強制同步/啟動 uvicorn 進行本機熱連載 (hot-reload)。初次執行時 `uv` 會自動安裝與處理虛擬環境中所需的任何依賴：

```bash
# 確保您在 backend/ 目錄下
cd backend/

# 使用 uv 啟動 FastAPI，預設啟動在 8000 port
uv run uvicorn app.main:app --reload
```

這行指令成功執行後，您會看到如下訊息：
`INFO:     Uvicorn running on http://127.0.0.1:8000`

### 3. API 文件與測試
當伺服器啟動後，您可以直接透過瀏覽器訪問自動生成的 Swagger UI 來測試 API：
- **Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 目錄結構簡介
- `app/`
  - `main.py` - FastAPI 端點與路由的核心定義 (包含 `/documents/upload`, `/chat/query`, `/graph` 等)。
  - `rag_engine.py` - RAG 引擎的商業邏輯，包含使用 Gemini 進行 Embedding 生成、文件切段與混合知識圖譜圖形萃取。
  - `graph_db.py` - Knowledge graph 的輕量級 SQLite 封裝 (Nodes, Edges)。
- `local_chromadb/` - (自動生成) 存放 Chunk 向量資料的本地端資料庫資料夾。
- `local_graph.db` - (自動生成) 存放從文本萃取出的實體與關係的 SQLite 檔案。
