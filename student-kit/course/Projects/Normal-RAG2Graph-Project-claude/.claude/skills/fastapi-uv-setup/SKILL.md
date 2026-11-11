---
name: fastapi-uv-setup
description: 用 uv 初始化 FastAPI 專案。Use when setting up the Python backend, running uv init, scaffolding the FastAPI app, or whenever the user says「建立後端」「setup backend」「uv init」.
---

## 指令順序
1. `cd backend && uv init --package`
2. 編輯 `pyproject.toml` 加入依賴：
   - fastapi, uvicorn, python-multipart
   - llama-index, llama-index-core
   - llama-index-llms-google-genai, llama-index-embeddings-google-genai
   - llama-index-vector-stores-chroma
   - chromadb, pydantic, docx2txt, pypdf, python-slugify
3. `uv sync` 安裝所有依賴
4. 建立程式結構：
   - `app/main.py` — FastAPI 路由、CORS、BackgroundTasks
   - `app/rag_engine.py` — 核心邏輯（parse, chunk, vectorize, query）
   - `app/db.py` — SQLite schema 與 connection manager（M5 才加）
5. 啟動：`uv run uvicorn app.main:app --reload`

## 強制
- 禁止產生 requirements.txt
- 禁止用 pip install
- pyproject.toml 的 build-system 用 hatchling
- CORS 設 allow_origins=["*"]（開發階段）

## LLM 初始化
```python
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
Settings.llm = GoogleGenAI(model="gemini-2.5-flash")
Settings.embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-001")
```
需要環境變數 GOOGLE_API_KEY。
