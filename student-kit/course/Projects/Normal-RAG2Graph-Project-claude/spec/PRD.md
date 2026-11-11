# Product Requirements Document (PRD)

## 1. 產品概述 (Product Overview)
本專案目標為開發一個可擴展的**文件知識庫與對話引擎 (Hybrid RAG 平台)**。
第一階段（目前）為基礎的「Vector Only」純向量檢索模式，使用者可以上傳常見文件（如 `.docx`, `.pdf`, `.txt`）建立個人化知識庫，並透過對話視窗向內文進行提問並查驗原始資料來源。
後續階段將保留「知識圖譜 (GraphRAG)」的擴充準備，允許系統自主構建知識圖結構，並可切換模式展示強大的關聯分析與視覺化功能。

## 2. 目標使用者 (Target Users)
企業內部員工、研究人員或擁有大量文件的知識工作者，需要從複雜文本中快速爬梳答案、了解資訊間的關聯，並尋求精確來源出處背書的進階使用者。

## 3. 核心功能規格 (Core Features)

### 3.1 文件管理與上傳模組
- **上傳檔案**：透過直覺的按鈕進行文件上傳，支援純文本、Word 及 PDF 檔。
- **進度回饋**：提供階段性的處理進度回饋 (Parsing -> Chunking -> Vectorizing -> Completed)。過程為背景非同步作業，不阻塞使用者前端的瀏覽與操作。
- **狀態列表顯示**：左側「Documents」Tab 區塊展示已索引文件的清單，包含檔名、索引時間以及狀態標籤（例如 Indexed、Processing）。
- **刪除管理**：允許透過 UI 一鍵刪除文件。系統將同步刪除後端關聯的文件紀錄與 ChromaDB 內的向量 Chunk。

### 3.2 智慧對話系統模組 (Chatbot Module)
- **聊天對話 (Chat Interface)**：氣泡式的對話窗呈現，包含打字機等待動畫（跳動提示）與完整的歷史對話紀錄。
- **回答產生**：利用 Google Gemini 高效語言模型解答使用者問題。
- **上下文呈現 (Retrieved Context Panel)**：當使用者提問後，系統右半邊將動態帶出系統認定最相關的文字切塊 (Top Chunks)。顯示每個 Chunk 的來源檔名 (source)、相關度分數 (score) 以及截斷文字片段，幫助使用者了解生成的邏輯與段落依據。前後端透過 `chunk_id` 強綁定，確保可追溯性。

### 3.3 Graph 擴充預備 (For Future Extensibility)
- 已經定義好預留的 `mode="hybrid"` 切換參數。
- UI 介面與後端架構保留了為後續導入 GraphRAG 模式（圖譜視覺化提取與查詢）的彈性空間。

## 4. UI / UX 設計標準
- **整體風格**：採用 "Smart RAG" 深色主題 (Dark-mode, 背景配置 `slate-950` 與 `slate-900`)。
- **佈局設計**：穩定的雙面板設計。左側（固定寬度，如 450px）負責導覽、文件上傳與聊天文字互動；右側（彈性寬度）負責展示檢索出的上下文 (Retrieved Context) 或未來的資料圖譜可視化。
- **視覺質感**：大量使用 Glassmorphism 半透明毛玻璃效果與漸層裝飾（例如 `bg-indigo-500/5` blur 效果），營造高科技與 Premium 質感。
- **圖示系統**：全站 Icons 嚴格依照 `lucide-react`。
- **動態效果**：按鈕、載入狀態 (Loader2, bounce) 與進度條需要有滑順的過渡動畫 (transition-all, shimmer effect)，提升使用者參與感與操作體驗。
