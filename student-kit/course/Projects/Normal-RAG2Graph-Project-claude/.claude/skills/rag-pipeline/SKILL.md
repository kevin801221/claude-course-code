---
name: rag-pipeline
description: 建立 parse → chunk → embed → Chroma 的最小 RAG 流程。Use when implementing document ingestion, vectorization, or retrieval logic, or whenever the user says「建立 RAG」「vectorize」「chunk 文件」「向量檢索」.
---

## 步驟
1. 解析：docx → docx2txt、pdf → pypdf、txt/md → open()。
2. 切 chunk：LlamaIndex SentenceSplitter(chunk_size=512, chunk_overlap=50)。
3. 每個 chunk 產生 UUID 當 `chunk_id`，寫入 Chroma metadata。
4. 查詢：`retriever.retrieve(query)` top_k=5，回傳 chunk_id 供反查。

## 強制
- 空知識庫 → 直接回「請先上傳文件」，禁止 LLM 自由發揮。
- metadata 必含 `chunk_id`、`doc_id`，否則後續 Graph 反查會斷。

## Chroma 設定
- `chromadb.PersistentClient(path="./chroma_db")`
- collection name: `"rag_collection"`
- 使用 LlamaIndex 的 `ChromaVectorStore` 整合

## 文件狀態流
upload → parsing → chunking → vectorizing → completed
每階段更新 in-memory jobs dict 的 status/stage。
