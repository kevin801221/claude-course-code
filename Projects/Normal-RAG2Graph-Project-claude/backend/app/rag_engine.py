import os
import uuid
from typing import List, Dict, Any
import pypdf
import logging
logging.getLogger("pypdf").setLevel(logging.ERROR)

import chromadb
import google.generativeai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 依據專案規範，強制寫死使用的 Embedding 模型
EMBEDDING_MODEL = "models/gemini-embedding-001"

class RAGEngine:
    def __init__(self):
        # 載入專案根目錄的 .env 檔案
        from dotenv import load_dotenv
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        dotenv_path = os.path.join(base_dir, ".env")
        load_dotenv(dotenv_path)

        # 初始化 Gemini API
        # 需確保執行環境已設定 GEMINI_API_KEY 環境變數
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)

        # 設定 ChromaDB 的本地持久化路徑
        # 指向專案根目錄下的 local_chromadb
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.chroma_path = os.path.join(base_dir, "local_chromadb")
        self.chroma_client = chromadb.PersistentClient(path=self.chroma_path)
        
        # 建立或取得預設的 Collection (依照規格書命名)
        self.collection_name = "documents_collection"
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)
        
        # 初始化切塊器 (Text Splitter)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def extract_text_from_pdf(self, file_path: str) -> str:
        """解析 PDF 檔案並萃取文字"""
        text = ""
        try:
            with open(file_path, 'rb') as f:
                pdf_reader = pypdf.PdfReader(f)
                for page in pdf_reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            print(f"Error parsing PDF {file_path}: {e}")
        return text

    def extract_text(self, file_path: str, filename: str) -> str:
        """依照副檔名決定萃取邏輯"""
        if filename.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_path)
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error parsing text file {file_path}: {e}")
                return ""

    def get_embeddings(self, texts: List[str], task_type: str = "retrieval_document") -> List[List[float]]:
        """使用 Gemini 產生 Embeddings"""
        if not texts:
            return []
        
        # 為了避免單次過多 token，此處假設 chunk 的總數在 API 限制內
        # 在正式生產環境可考慮進行批次 (batching) 分割
        response = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=texts,
            task_type=task_type
        )
        
        # 確保回傳始終是 List[List[float]] 結構
        embeddings = response.get('embedding')
        if isinstance(embeddings, list) and len(embeddings) > 0 and not isinstance(embeddings[0], list):
            embeddings = [embeddings]
        return embeddings

    def process_document(self, file_path: str, filename: str, doc_id: str):
        """處理單一文件：解析 -> 切塊 -> 向量化 -> 存入 ChromaDB"""
        # 1. Parsing (解析)
        text = self.extract_text(file_path, filename)
        if not text.strip():
            print(f"No text extracted from {filename}")
            return

        # 2. Chunking (切塊)
        chunks = self.text_splitter.split_text(text)
        if not chunks:
            return

        # 3. Vectorizing (向量化)
        embeddings = self.get_embeddings(chunks, task_type="retrieval_document")

        # 4. Insert into ChromaDB
        ids = []
        metadatas = []
        documents = []
        
        for i, chunk in enumerate(chunks):
            # 前後端將透過此 chunk_id 強綁定
            chunk_id = str(uuid.uuid4())
            ids.append(chunk_id)
            documents.append(chunk)
            metadatas.append({
                "doc_id": doc_id,
                "file_name": filename,
                "chunk_index": i
            })

        # 分批寫入以避免單次寫入過大
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            self.collection.add(
                ids=ids[i:i+batch_size],
                embeddings=embeddings[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                documents=documents[i:i+batch_size]
            )

    def delete_document(self, doc_id: str):
        """從 ChromaDB 中刪除特定文件的所有 chunks"""
        self.collection.delete(
            where={"doc_id": doc_id}
        )

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """檢索與 Query 語意最相關的 chunks"""
        # 生成 query 的 embedding
        query_embeddings = self.get_embeddings([query], task_type="retrieval_query")
        if not query_embeddings:
            return []

        # 查詢 ChromaDB
        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=top_k
        )
        
        retrieved_chunks = []
        if results['ids'] and len(results['ids']) > 0:
            ids = results['ids'][0]
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0] if results['distances'] else [0.0] * len(ids)
            
            for i in range(len(ids)):
                # 將 L2/Cosine 距離簡單轉換為近似 score，此部分可依需求優化
                score = max(0.0, 1.0 - (distances[i] / 2.0))
                retrieved_chunks.append({
                    "id": ids[i],
                    "source": metadatas[i].get("file_name", "unknown"),
                    "score": round(score, 3),
                    "text": documents[i]
                })
        
        return retrieved_chunks

# 建立單例物件供 FastAPI 路由使用
rag_engine = RAGEngine()
