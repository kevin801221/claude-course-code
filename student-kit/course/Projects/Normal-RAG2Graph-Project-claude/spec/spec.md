# 技術規格書 (Technical Specification)

## 1. 核心技術棧 (Tech Stack)
依據專案 `rules.md` 強制規定，不得隨意更改：
- **Backend (後端)**： Python 3.10+, FastAPI。依賴管理工具強制使用 `uv`（禁止 pip/poetry）。
- **Frontend (前端)**： Next.js (App Router) + TypeScript + TailwindCSS。
- **Vector Database (向量庫)**： ChromaDB (使用本地 persistent 模式)。
- **LLM / Embedding (語言模型)**： Google Gemini API。生成強制使用 `gemini-2.5-flash`，向量化**絕對強制使用** `"models/gemini-embedding-001"` (不可擅自替換為其他字串，這是專案鐵律)。
- **Graph Visualization (圖譜視覺化)**： 未來擴展強制使用 `react-force-graph-2d`。

## 2. 系統資料流與架構設計 (Data Flow & Architecture)

### 2.1 資料模型 (Data Models)
- **Document**: `{ id: string, name: string, time: string, status: "Indexed" | "Processing" | "Failed" }` 
  前端展示文件使用，對應後端關聯資料（含 `doc_id`, `filename`, `uploaded_at` 等）。
- **Job**: `{ job_id: string, status: "parsing" | "chunking" | "vectorizing" | "completed" }` 
  追蹤文件背景處理階段的任務模型。
- **RetrievedChunk**: `{ id: string, source: string, score: number, text: string }` 
  檢索結果的文字切塊模型，`id` 映射到唯一的 `chunk_id`。
- **QueryRequest**: `{ query: string, mode?: "vector" | "hybrid" }` 
  前端送出提問的要求模型。
- **ChatResponse**: `{ answer: string, chunks: RetrievedChunk[] }` 
  後端回傳的最終生成答案與參考片段，強綁定 `chunk_id`。

### 2.2 ChromaDB Collection 設計
- **單一 Collection**：建立一個名為 `documents_collection` 的 collection 來集中管理所有向量切塊。
- **Metadata 結構**：寫入 ChromaDB 的每一筆紀錄，其 Metadata 必須帶有 `doc_id`、`file_name` 以及 `chunk_index`。
- **前後端強綁定**：ChromaDB 的紀錄 `id` 即為 `chunk_id`，確保前端可以藉由 RetrievedChunk 的 `id` 直接定位到指定的切塊與關聯文件。

## 3. API 路由列表 (API Endpoints)
所有請求路徑前綴 (Prefix): `/api/v1`

- `POST /documents/upload`
  - 功能：接收檔案上傳 (Multipart form)。
  - 邏輯：由 `FastAPI BackgroundTasks` 啟動非同步處理 (Parsing -> Chunking -> Vectorizing)。
  - 回應：`{"job_id": "...", "doc_id": "..."}`
  
- `GET /status/{job_id}`
  - 功能：查詢背景處理任務的即時進度狀態。
  - 回應：`{"job_id": "...", "status": "parsing" | "chunking" | "vectorizing" | "completed"}`

- `GET /documents`
  - 功能：回傳所有已被索引的文件清單。
  - 回應：陣列型態的 `Document` 模型。

- `DELETE /documents/{doc_id}`
  - 功能：刪除特定文件。
  - 邏輯：清除 SQLite 或其他關聯表中的文件紀錄，並刪除 ChromaDB `documents_collection` 中符合 `metadata.doc_id` 的所有 Vectors 與 Chunks。

- `POST /chat/query`
  - 功能：進行 RAG 問答。
  - 邏輯：
    1. 對問題字串進行 Embedding (嚴格使用 `models/gemini-embedding-001`)。
    2. 至 ChromaDB 的 `documents_collection` 進行語意相似度檢索 (Top-K)。
    3. 將檢索出的 Chunks 提供給 LLM (`gemini-2.5-flash`) 生成回覆。
  - 要求：`QueryRequest`
  - 回應：`ChatResponse`

## 4. YAGNI 清單 (You Aren't Gonna Need It - 絕對禁止)
遵守輕量級原則，嚴格執行以下禁止項目：
- **禁止 Celery 與 Redis**：不要為異步任務設立完整任務佇列服務，所有背景處理一律只用 `FastAPI BackgroundTasks`。
- **禁止 Neo4j 等巨型圖資料庫**：不用殺雞用牛刀，Graph 結構未來將單純以 SQLite 的 5 張表格解決。
- **無縫 Streaming (SSE)**：不要優先考慮 SSE 生成字元串流 (Streaming UI)，初版直接等待生成完畢回傳完整的 JSON 結構。
- **多餘的 UI 狀態庫**：不需要 Redux / Zustand，使用 React 內建 Hooks 加上 localStorage 處理深色及模式開關即可。
