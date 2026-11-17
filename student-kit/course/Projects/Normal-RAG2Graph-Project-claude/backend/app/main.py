import os
import uuid
from typing import List, Dict, Optional
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

from app.rag_engine import rag_engine

app = FastAPI(title="Normal RAG2Graph Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 內存資料暫存 (供階段 1 示範與測試使用)
JOB_STORE: Dict[str, str] = {}
DOCUMENTS_STORE: Dict[str, dict] = {}

class QueryRequest(BaseModel):
    query: str
    mode: Optional[str] = "vector"

class RetrievedChunk(BaseModel):
    id: str
    source: str
    score: float
    text: str

class ChatResponse(BaseModel):
    answer: str
    chunks: List[RetrievedChunk]

@app.get("/health")
async def health():
    return {"status": "ok", "stage": "Stage 1 Milestone 1"}

def process_upload_task(job_id: str, file_path: str, filename: str, doc_id: str):
    """背景處理任務"""
    try:
        # 開始處理
        JOB_STORE[job_id] = "parsing"
        text = rag_engine.extract_text(file_path, filename)
        
        if not text.strip():
            JOB_STORE[job_id] = "failed"
            return
            
        JOB_STORE[job_id] = "chunking"
        chunks = rag_engine.text_splitter.split_text(text)
        
        if not chunks:
            JOB_STORE[job_id] = "failed"
            return
            
        JOB_STORE[job_id] = "vectorizing"
        embeddings = rag_engine.get_embeddings(chunks, task_type="retrieval_document")
        
        # 寫入 ChromaDB
        ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        metadatas = [{"doc_id": doc_id, "file_name": filename, "chunk_index": i} for i in range(len(chunks))]
        
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            rag_engine.collection.add(
                ids=ids[i:i+batch_size],
                embeddings=embeddings[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                documents=chunks[i:i+batch_size]
            )

        # 處理完成
        JOB_STORE[job_id] = "completed"
        DOCUMENTS_STORE[doc_id] = {
            "id": doc_id,
            "name": filename,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Indexed"
        }
    except Exception as e:
        JOB_STORE[job_id] = "failed"
        print(f"Error processing document {filename}: {e}")
    finally:
        # 清除暫存檔案
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/api/v1/documents/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    doc_id = str(uuid.uuid4())
    
    # 建立暫存檔
    temp_dir = "/tmp/rag_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, f"{doc_id}_{file.filename}")
    
    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    JOB_STORE[job_id] = "parsing"
    
    background_tasks.add_task(process_upload_task, job_id, temp_path, file.filename, doc_id)
    
    return {"job_id": job_id, "doc_id": doc_id}

@app.get("/api/v1/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in JOB_STORE:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": JOB_STORE[job_id]}

@app.get("/api/v1/documents")
async def get_documents():
    return list(DOCUMENTS_STORE.values())

@app.delete("/api/v1/documents/{doc_id}")
async def delete_document(doc_id: str):
    if doc_id in DOCUMENTS_STORE:
        del DOCUMENTS_STORE[doc_id]
    
    try:
        rag_engine.delete_document(doc_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"status": "deleted", "doc_id": doc_id}

@app.post("/api/v1/chat/query", response_model=ChatResponse)
async def chat_query(req: QueryRequest):
    # 1. 使用 ChromaDB 進行 Top-5 檢索
    chunks_dict = rag_engine.retrieve(req.query, top_k=5)
    chunks = [RetrievedChunk(**c) for c in chunks_dict]
    
    # 2. 構建 Context
    context_text = "\n\n".join([f"[{c.source}] {c.text}" for c in chunks])
    
    # 3. 使用 Gemini 2.5 Flash 生成回答
    prompt = f"""請根據以下參考資料回答問題。如果參考資料中沒有答案，請回答「我不知道」。

參考資料：
{context_text}

使用者問題：{req.query}
"""
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    try:
        response = model.generate_content(prompt)
        answer = response.text if response.text else "抱歉，無法生成回答。"
    except Exception as e:
        answer = f"生成回答時發生錯誤：{str(e)}"
    
    return ChatResponse(answer=answer, chunks=chunks)
