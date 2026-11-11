# 專案報告：多 Agent 協作開發 Hybrid GraphRAG 平台

> **這份文件為 NotebookLM 產生 PPT 報告的最佳化素材**，詳細記錄了我們如何利用多重 AI Agent 協作，從零打造一個具備雙模式 (Vector/Graph) 切換的次世代 RAG 平台。

---

## 1. 專案願景與核心目標

*   **目標**：從零到一建立一個「文件問答平台」，並具備兩大核心亮點：
    1.  **純向量檢索 (Vector RAG)**：傳統基於 ChromaDB 的文件語意搜尋。
    2.  **知識圖譜檢索 (GraphRAG)**：將文本萃取為實體與關聯 (Entities & Links)，並透過 `react-force-graph-2d` 在前端進行視覺化與高亮互動。使用者可以在這兩個模式之間一鍵切換。
*   **開發模式**：採用 **多 Agent 協作模式 (Multi-Agent Collaboration)**。由人類作為「超級總監」，引導兩個專職的 AI Agent 分工合作，完成從規格開出、架構設計到前後端實作的完整生命週期。

---

## 2. 雙 Agent 協作架構 (The Agent Ecosystem)

我們引入了兩個不同職責的 AI Agent 來建構這個專案：

### Agent A: Antigravity (執行開發者)
*   **載體**：運行在 IDE 內 (如 Cursor, Windsurf, 或原生的 Antigravity IDE)。
*   **職責 (The Maker)**：
    *   撰寫系統規格書 (`Spec` 與 `PRD`)。
    *   建立基於 Python (FastAPI + uv) 的後端與 RAG Pipeline (ChromaDB + SQLite)。
    *   實作基於 Next.js + TailwindCSS 的前端 UI 與 API 串接。

### Agent B: Gemini CLI (架構師與審查者)
*   **載體**：運行在終端機 (Terminal) 的全域 AI 助理。
*   **職責 (The Reviewer)**：
    *   監控 Antigravity 的開發進度。
    *   嚴格執行 Code Review，確保符合 Clean Code 與專案規範。
    *   自動化生成符合 Conventional Commits 格式的 Git Commit，掌控版本控制。

---

## 3. 跨 Agent 協作基礎建設：如何讓兩個 AI 對話？

兩個獨立的 AI Agent 無法直接通話，為了解決這個問題，我們設計了以下「共同記憶」與「標準協議」機制：

### A. 共同記憶檔 (`.antigravity_sync.md`)
我們在專案根目錄建立了一個共享狀態檔案。任何 Agent 在完成工作後，都必須讀寫這個檔案，其中包含：
*   **Current Status (當前狀態)**：現在專案進度到哪裡。
*   **Next Tasks (下一步任務)**：清楚定義 Antigravity 與 Gemini CLI 各自接下來該做什麼。
*   **Feedback (反饋)**：Code Review 的修改建議或稱讚。

### B. 專案憲法 (`.agents/rules.md`)
這是寫給 Antigravity 看的最高指導原則。我們在裡面加入了一條強制規定：
> 「每次完成階段性任務，必須自動讀寫並更新專案根目錄的 `.antigravity_sync.md`，並交由 Gemini CLI 進行 Review 與 Commit。」

### C. Gemini CLI 專屬技能與自動化指令 (`Skill` & `/sync`)
1.  **開發 Skill (`antigravity-collaboration`)**：我們教導 Gemini CLI 如何閱讀同步檔、如何下 `git diff` 指令，以及如何給予 Feedback。並將其全域安裝。
2.  **建立斜線指令 (`/sync`)**：我們將繁瑣的指令封裝成 `/sync`。當人類在終端機輸入 `/sync` 時，Gemini CLI 會「一鍵自動」完成：讀取同步檔 ➔ 檢查程式碼 ➔ Code Review ➔ Git Commit ➔ 更新下一步任務交還給 Antigravity。

---

## 4. 模組化知識包 (Skills) 與設計先行策略

為了保持 Agent 的 Context Window 乾淨高效，我們採用了「模組化」與「設計先行」的策略：

*   **Skills 系統**：我們不把所有技術細節塞進全域 Prompt，而是打包成 4 個情境觸發的技能檔案 (放在 `.agents/skills/`)：
    1.  `rag-pipeline.md`：教導如何切 Chunk 與存入 Chroma。
    2.  `fastapi-uv-setup.md`：強制使用 `uv` 建立 FastAPI 環境。
    3.  `graph-extraction.md`：定義 SQLite 的五張圖譜表與 LLM 萃取邏輯。
    4.  `force-graph-ui.md`：教導如何渲染力導向圖 (Force-Directed Graph)。
*   **AI Studio 原型設計**：在實際寫 Code 前，人類先在 Google AI Studio 用 Prompt 生成前端 UI 的 React 靜態原型。讓 Antigravity 後續有具體的視覺目標可以依循，大幅降低前端刻版的失敗率。

---

## 5. 系統實作與漸進式里程碑 (Milestones)

我們將開發過程拆解為 7 個核心 Milestone，透過雙 Agent 交替接力完成：

*   **M0 - M1: 設計與規格**：完成 AI Studio UI 原型，Antigravity 產出 `spec.md`。Gemini CLI 審查通過。
*   **M2 - M4: 純 Vector RAG 落地**：
    *   Antigravity 開發出具備文件上傳、Chunking、Vectorize 狀態輪詢的 FastAPI 後端。
    *   Antigravity 將前端 Mock 資料替換為真實 API 呼叫。
    *   Gemini CLI 透過 `/sync` 完成 Review 並建立首次的完整功能 Commit。
*   **M5: GraphRAG 架構升級**：
    *   後端引入 SQLite。在處理文件時，多加一個步驟：用 LLM 從每個 Chunk 中萃取 Entities (實體) 與 Relations (關聯)，並寫入資料庫。
*   **M6 - M7: 雙模式切換與視覺化反查 (The AHA Moment)**：
    *   **雙模式 UI**：前端實作 `⚡ Vector Only ↔ 🕸 GraphRAG` 的切換開關。
    *   **視覺化回饋**：當處於 GraphRAG 模式並詢問問題時，AI 產生回答的同時，右側的知識圖譜會針對相關節點與連線發出**高亮光暈 (Glow)**，並自動聚焦 (Zoom to fit)。
    *   **反查機制 (Grounding)**：點擊圖譜上的任何節點，左側會彈出該節點的詳細資訊，並顯示支持這個節點的「原文片段 (Chunks)」，徹底解決 LLM 的幻覺 (Hallucination) 問題。

---

## 6. 總結與未來展望

*   **自動化躍進**：透過 `/sync` 指令與 `.antigravity_sync.md` 共同記憶檔，我們證明了由人類擔任指揮官，協調多個 AI Agent 分工合作，是開發現代複雜架構 (如 Hybrid RAG) 最強大的工作流。
*   **極致的 RAG 體驗**：成功結合了「向量搜尋的廣度」與「知識圖譜的深度」。讓使用者不僅能得到答案，還能「看見」知識的形狀，並驗證知識的來源。