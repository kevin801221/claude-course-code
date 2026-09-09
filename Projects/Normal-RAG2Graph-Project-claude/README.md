# Normal RAG2Graph Project

> 文件上傳 → 自動建知識圖譜 → 雙模式 RAG 問答（Vector / Graph）+ 圖譜視覺化

## 一句話說明

把 PDF 丟進去，後端用 LangChain + Gemini 萃取「實體 + 關係」存進知識圖譜，前端可以用聊天介面問問題、切換 Vector RAG 或 GraphRAG 模式，並把圖譜視覺化呈現。

## 技術棧

| 層 | 技術 | 連接埠 |
|---|---|---|
| 前端 | **Next.js 15（App Router）** + TypeScript + Tailwind | `:3000` |
| 後端 | **FastAPI** + LangChain + Gemini | `:8000` |
| 向量庫 | **ChromaDB**（本地 persistent，存在 `backend/local_chromadb/`） | — |
| 圖譜庫 | **SQLite**（`backend/local_graph.db`） | — |
| LLM | Gemini 2.5 Flash（生成）+ gemini-embedding-001（向量化） | — |

## 你需要先有什麼

| 工具 | 版本 | 安裝 |
|---|---|---|
| Python | 3.13+ | 已有 |
| Node.js | 20+ | `brew install node` |
| uv | latest | `brew install uv` 或 `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Gemini API Key | — | <https://aistudio.google.com/apikey> |

✅ **本專案已經幫你裝好**：`backend/.venv/`、`frontend/node_modules/` 都存在，可以直接跑。

---

## 🚀 怎麼跑（兩個 terminal）

### Step 0：確認 .env 裡有 API Key

```bash
cd /Users/kevinluo/google-agent-ecosystem/Antigravity-work/Normal-RAG2Graph-Project-claude
cat .env
```

應該看到：
```
GOOGLE_API_KEY=AIza...
GEMINI_API_KEY=AIza...
```

> 如果沒有 key，到 <https://aistudio.google.com/apikey> 拿一把，填進去（兩個變數可以填同一把）。

### Step 1：開後端（Terminal 1）

```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

成功會看到：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

驗證：另開 terminal 跑
```bash
curl http://127.0.0.1:8000/api/v1/documents
# 應該回 [] 或現有文件清單
```

或直接開 <http://127.0.0.1:8000/docs> 看 Swagger UI。

### Step 2：開前端（Terminal 2）

```bash
cd frontend
npm run dev
```

成功會看到：
```
  ▲ Next.js 15.x
  - Local:        http://localhost:3000
  ✓ Ready in 1.2s
```

### Step 3：開瀏覽器

👉 <http://localhost:3000>

你會看到：
- **左側**：文件管理 + 聊天視窗
- **右側**：知識圖譜視覺化

---

## 🧪 第一次使用：Hello World 流程

1. 點左邊 **Upload PDF** 上傳一個 PDF（建議用 < 10 頁的測試文件）
2. 等 status 變 **Indexed**（後端會：解析 → 切 chunk → 萃取實體關係 → 存圖譜）
3. 在聊天框輸入問題，例：「這份文件主要在講什麼？」
4. 切換 **mode**：
   - `vector`：純向量檢索 → 找最相似的 chunk
   - `graph`：知識圖譜檢索 → 用實體關係導航
5. 觀察右邊圖譜：被引用的節點會 highlight

---

## 📁 專案結構

```
Normal-RAG2Graph-Project/
├── README.md                ← 本檔（你正在讀的）
├── walkthrough.md           ← 完整功能逐步教學
├── .env                     ← API keys（不入 git）
├── backend/
│   ├── app/
│   │   ├── main.py          ← FastAPI 入口（8 個 API route）
│   │   ├── rag_engine.py    ← 純 Vector RAG
│   │   ├── semantic_rag_engine.py  ← Hybrid GraphRAG
│   │   └── graph_db.py      ← SQLite 圖譜操作
│   ├── local_chromadb/      ← ChromaDB 向量檔案
│   ├── local_graph.db       ← SQLite 圖譜
│   ├── temp_uploads/        ← 上傳暫存
│   └── pyproject.toml       ← uv 管理
├── frontend/
│   ├── app/
│   │   ├── page.tsx         ← 主頁面（聊天 + 圖譜）
│   │   ├── layout.tsx
│   │   └── components/
│   │       └── GraphView.tsx  ← 圖譜視覺化
│   └── package.json
├── spec/                    ← 架構決策、PRD
└── doc/                     ← 設計文件
```

---

## 🔌 API 端點速查

| Method | Path | 功能 |
|---|---|---|
| POST | `/api/v1/documents/upload` | 上傳 PDF（背景處理） |
| GET | `/api/v1/documents/status/{job_id}` | 查處理進度 |
| GET | `/api/v1/documents` | 列出已處理文件 |
| DELETE | `/api/v1/documents/{doc_id}` | 刪除文件 |
| POST | `/api/v1/chat/query` | RAG 問答（vector / graph） |
| GET | `/api/v1/graph` | 取得整個知識圖譜 |
| GET | `/api/v1/graph/node/{node_id}/chunks` | 看某節點的 chunk |
| POST | `/api/v1/graph/reset` | 清空圖譜 |

完整 schema 開 <http://127.0.0.1:8000/docs>。

---

## ⚠️ 常見問題

### 1. 前端打 API 失敗 / CORS 錯誤
前端寫死打 `http://127.0.0.1:8000/api/v1`（在 `frontend/app/page.tsx:47`）。確認後端跑在 **8000** 而不是其他 port。

### 2. 後端啟動 ImportError 或缺套件
重新 sync：
```bash
cd backend
uv sync
```

### 3. 前端跑不起來 / Module not found
重裝：
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 4. Gemini API quota 超額
免費額度有限，到 [AI Studio](https://aistudio.google.com/) 看 quota，或建新 project 拿新 key。

### 5. Port 8000 / 3000 被佔用
```bash
lsof -i:8000   # 看誰佔了
kill -9 <PID>  # 殺掉
```

或改 port：
- 後端：`uv run uvicorn app.main:app --port 8001`（記得也改前端 `API_BASE_URL`）
- 前端：`PORT=3001 npm run dev`

### 6. 想清空所有資料重新開始
```bash
cd backend
rm -rf local_chromadb local_graph.db temp_uploads
mkdir temp_uploads
```

---

## 🧹 收工

兩個 terminal 都按 `Ctrl+C` 停掉。資料庫是本地檔案，下次開機資料還在。

---

## 📚 延伸閱讀

- [`walkthrough.md`](./walkthrough.md) — 完整功能教學
- [`spec/spec.md`](./spec/spec.md) — 架構決策
- [`spec/PRD.md`](./spec/PRD.md) — 產品需求
- [`doc/plan.md`](./doc/plan.md) — 實作計畫
- [`doc/multi_agent_collaboration_presentation.md`](./doc/multi_agent_collaboration_presentation.md) — 多 agent 協作介紹
- [`backend/README.md`](./backend/README.md) — 後端詳細文件

---

## 🆚 跟 StockPulse AI 的差異

| 項目 | StockPulse AI | Normal-RAG2Graph |
|---|---|---|
| 框架 | ADK + LangGraph + A2A | LangChain + Gemini |
| 資料庫 | 無（in-memory） | ChromaDB + SQLite |
| 前端 | Vite + React | **Next.js (App Router)** |
| 部署 | ✅ Cloud Run（已上線） | 本機開發 |
| 重點 | 多 Agent 協作、A2A 協定 | RAG 雙模式、知識圖譜 |
