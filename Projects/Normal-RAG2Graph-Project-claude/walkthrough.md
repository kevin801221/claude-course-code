# 三階段 RAG 教學完整流程

> 這是 `starter-kit` 分支的教學主腳本。會帶你走完 3 個階段，每階段使用不同的技術哲學，學完之後你會對「LLM × 知識管理」這件事有完整的視角。

---

## 三階段全景

| 階段 | 路徑 | 技術核心 | 預估時間 | 你寫什麼 |
|---|---|---|---|---|
| **Stage 1：普通 RAG** | 本分支 `backend/` + `frontend/` | ChromaDB + Gemini Embedding + 固定字切 | 約 90 分鐘 | Python 後端 + Next.js 前端 |
| **Stage 2：LLM Wiki** | 本分支 `wiki-project/` | Markdown wiki + Agent 自律維護 | 約 60 分鐘 | Markdown 提示與 schema |
| **Stage 3：Semantic GraphRAG** | `git checkout feature/semantic-graphrag` | LangChain + SemanticChunker + LLMGraphTransformer | 約 60–90 分鐘 | 主要是「讀別人寫好的 code」並對照 |

> 三個階段不是「越後面越好」，而是**三種不同哲學**：Stage 1 = 取代知識管理（檢索式），Stage 2 = 累積知識（編譯式），Stage 3 = 自動化（混合式）。學完才能看出各自適用情境。

### 🌳 三分支同時並存（用 git worktree，不要 checkout）

教學會在 3 個分支之間切換對比，**強烈建議用 git worktree 同時開三個資料夾**，避免 `git checkout` 把工作區覆蓋掉：

```bash
# 在專案根目錄執行（一次性 setup）
git worktree add .worktree/main main
git worktree add .worktree/semantic-graphrag feature/semantic-graphrag

# 確認結果
git worktree list
# 應該看到：
#   .                                  [starter-kit]   ← 主編輯區（你正在讀這份 walkthrough）
#   .worktree/main                     [main]          ← Stage 1 完工 demo（普通 RAG + naive KG）
#   .worktree/semantic-graphrag        [feature/semantic-graphrag]  ← Stage 3 對照（LangChain GraphRAG）
```

`.worktree/` 已加進 `.gitignore`，不會污染 starter-kit。每個 worktree 有自己的 `.venv` / `node_modules`——**venv 內 binary 是絕對路徑 shebang，move worktree 後要重建 `.venv`**（`rm -rf backend/.venv && uv sync`）。

各 worktree 用途：
| 路徑 | 分支 | 教學角色 |
|---|---|---|
| `.` (本目錄) | `starter-kit` | 親手刻教材（M0–M4 + Stage 2 共創 + Stage 3 讀 code） |
| `.worktree/main/` | `main` | Stage 1 現場 demo 模式（30 分鐘看成品） |
| `.worktree/semantic-graphrag/` | `feature/semantic-graphrag` | Stage 3 對照實驗（LangChain GraphRAG） |

### 📓 配套教材（選用）

| 資源 | 類型 | 配套 Stage | 用途 |
|---|---|---|---|
| [`walkthrough.ipynb`](./walkthrough.ipynb) | Notebook | Stage 1 | 不啟 FastAPI，逐 cell 看 RAG + KG 內部資料流（9 個步驟） |
| [`wiki-walkthrough.ipynb`](./wiki-walkthrough.ipynb) | Notebook | Stage 2 | sandbox 內跑 LLM Wiki 模式（Ingest / Query / Lint / 歸檔） |
| `~/google-agent-ecosystem/llm-wiki-graph/` | 參考實作 | Stage 2 | 真實長期累積的 wiki repo（已 ingest 數十份 podcast 逐字稿），可直接打開 `wiki/graph.html` 看 wiki-link 網絡圖 |

> 三份教材都是**輔助理解用**，不影響主線進度。詳細時機見各 Stage 開頭的 callout。Stage 3 沒有對應教材——`feature/semantic-graphrag` 分支本身就是完整實作可以直接讀。

> ⚠️ **Stage 2 與 Stage 3 的「graph」是兩種不同概念，別搞混**
> - **Stage 2 的 graph**（`llm-wiki-graph/wiki/graph.html`）= **wiki-link 網絡圖**：markdown 頁面之間 `[[link]]` 形成的連線，類似 Obsidian / Roam graph view，節點 = 頁面、邊 = 引用
> - **Stage 3 的 graph**（`feature/semantic-graphrag` 分支）= **entity-relation 知識圖譜**：LLM 從文字抽出的 `(主體, 關係, 客體)` 三元組，節點 = 實體、邊 = 語意關係
>
> 兩者都叫「graph」但本質完全不同——Stage 2 的圖是**人寫的引用結構編譯出來然後LLM Agent 再去重碩關係網路的**，Stage 3 的圖是**LLM 從文字抽出來的，再去存到圖向量空間上，可以用於RAG**。學完兩個 Stage 後你會更清楚這個區別。

---

## Phase 0｜環境準備（5 分鐘，每階段共用）

### 0-1. 確認工具已安裝
```bash
claude --version         # Claude Code CLI（Anthropic 官方 CLI）
code --version           # VS Code（或 JetBrains 任一個裝了 Claude Code Extension 的 IDE）
uv --version             # Python package manager
node --version           # Node.js v18+
echo $GOOGLE_API_KEY     # 確認 .env 或 shell 都有值（給 Gemini API 用，跟 Claude API 是不同 key）
```

> **注意**：本專案後端 LLM 用的是 **Google Gemini**（embedding + 生成），跟 **Claude Code** 是兩個獨立系統。Claude Code 是寫 code 的 agent，Gemini 是被 RAG 後端呼叫的 LLM。兩個 API key 都要設。

### 0-2. 用 IDE 開啟專案（已裝 Claude Code Extension）
```bash
cd /Users/kevinluo/google-agent-ecosystem/Antigravity-work/Normal-RAG2Graph-Project-claude
code .  # VS Code 為例；JetBrains 用 idea . 或自己從 IDE 內開
```

開啟後確認 IDE 右下／側欄能看到 Claude Code Extension 的對話框（icon）。

### 0-3. 確認 Claude Code 有讀到 CLAUDE.md
在 Claude Code 對話框問：
```
你有讀到 CLAUDE.md 嗎？列出技術棧限制。
```
應該回答：FastAPI + uv、ChromaDB、Gemini（embedding 嚴格 `models/gemini-embedding-001`）、Next.js + Tailwind...。

### 0-4. 理解 `.claude/skills/` 的運作機制（**重要！這是本專案的核心**）

打開 `.claude/skills/` 目錄，你會看到 5 個 skill 資料夾（每個 skill 一個資料夾，內含 `SKILL.md` 進入點）。**它們是讓 Claude Code（Extension + CLI）不會「失憶」的關鍵基礎設施**。

#### Claude Code 的 Skill 機制怎麼跑

Claude Code 啟動時掃 `.claude/skills/<name>/SKILL.md`，讀每份檔案開頭的 YAML frontmatter（`name` + `description`）建索引。對話進行時，**模型自己判斷**：「現在做的事跟某個 skill 的 description 對得上嗎？對得上就 invoke，把 SKILL.md 整份載進來當這次回應的 context」。

不需要手動 `/skill xxx`，也不需要使用者明說——是模型自己 trigger。

#### 兩種角色

**🤖 給 Claude Code Extension 的「實作肌肉記憶」（4 個 skill）**

| Skill 路徑 | 觸發描述 | 給 Extension 的指引 |
|---|---|---|
| `.claude/skills/fastapi-uv-setup/SKILL.md` | setting up backend, uv init, FastAPI scaffolding | uv 初始化、依賴清單、`app/` 結構、強制禁 `pip` |
| `.claude/skills/rag-pipeline/SKILL.md` | RAG ingestion, vectorization, chunking | parse → chunk → embed → Chroma、metadata 必含 chunk_id |
| `.claude/skills/graph-extraction/SKILL.md` | knowledge graph, entity extraction, KG schema | 完整 SQLite schema（5 張表）、entity 萃取 prompt、CASCADE 刪除 |
| `.claude/skills/force-graph-ui/SKILL.md` | frontend graph panel, node highlighting | Next.js + react-force-graph-2d 雙面板、節點高亮流程 |

**👥 給 Claude Code CLI 的「協作協議」（1 個 skill + 1 個 slash command）**

| 檔案 | 用途 |
|---|---|
| `.claude/skills/cli-extension-sync/SKILL.md` | Project-scope skill：定義 Extension ↔ CLI 兩邊怎麼透過 `.collab-sync.md` 接力 |
| `.claude/commands/sync.md` | Project-scope slash command：在 CLI 端打 `/sync` 觸發，會 invoke `cli-extension-sync` skill 做 review + commit |

> **跟原 Antigravity 版的差異**：原版 Gemini CLI 的 sync skill 是 user-scope（要 `gemini skills install ... --scope user` 額外安裝）。Claude Code 版改成 project-scope，**clone 完就能用**，少一步 setup。

#### 觸發機制示範

每個 skill 開頭的 YAML frontmatter 寫法：

```yaml
---
name: rag-pipeline
description: 建立 parse → chunk → embed → Chroma 的最小 RAG 流程。Use when implementing document ingestion, vectorization, or retrieval logic, or whenever the user says「建立 RAG」「vectorize」「chunk 文件」「向量檢索」.
---
```

`description` 寫得越具體，Claude Code 越容易 auto-invoke。中英關鍵字都列上去（中文工作描述 + 英文 schema 關鍵字）能提升命中率。

範例：你打「幫我建立 RAG 後端」，Claude Code Extension 會：
1. 比對「建 RAG」「後端」「Python」這些關鍵字
2. **自動 invoke** `Skill(fastapi-uv-setup)` + `Skill(rag-pipeline)`，兩份 SKILL.md 整份載進這次的 context
3. 寫 code 時把「禁 pip」「metadata 必含 chunk_id」這類 constraint 當剛性規則執行

**所以你不用每次重複交代「記得用 uv」「記得 chunk_id 不要漏」**——這些都已經在 skill 裡。

#### 完整流程示意

```
       你在 Claude Code 對話框打 prompt
                  ↓
       Extension 讀 CLAUDE.md（自動）
       + 比對 .claude/skills/*/SKILL.md 的 description
                  ↓
   ┌─────────────────────────────────────┐
   │ 自動 invoke 相關 skill：            │
   │  → fastapi-uv-setup  (uv, app/)     │
   │  → rag-pipeline      (chunk_id 不漏)│
   │  → graph-extraction  (5 張表)       │
   └─────────────────────────────────────┘
                  ↓
       Extension 寫 code + 更新 .collab-sync.md
                  ↓
       你切到終端，跑 `claude` 進入 Claude Code CLI
                  ↓
       打 /sync（觸發 .claude/commands/sync.md）
                  ↓
   ┌─────────────────────────────────────┐
   │ CLI auto-invoke cli-extension-sync  │
   │  → review 改動 + commit + 更新狀態  │
   └─────────────────────────────────────┘
```

#### 自己驗證一下

在 Claude Code 對話框問：
```
你看到 .claude/skills/ 裡有哪些 skill？簡述每個的用途。
```
應該能列出 5 個 skill（4 個實作 + 1 個 sync 協議）。

如果它沒主動 invoke 你需要的 skill，可以**直接點名載入**：
```
請用 Skill(rag-pipeline) 載入相關規則，然後幫我實作 RAG 引擎。
```
這會強制把該 skill 完整內容載進 context。

---

# Stage 1｜普通 RAG（90 分鐘）

> 在這個 stage 你會親手蓋一個能上傳 PDF、用向量檢索回答問題的 RAG 系統。技術棧最傳統，但你會親身體會「chunking 切多大、embedding 怎麼選、為什麼 retrieval 會錯」這些後續 Stage 才講得清楚的痛點。

## 🎭 兩種教學模式：現場 demo vs 親手刻

| 模式 | 時長 | 適合 | 用什麼 |
|---|---|---|---|
| **A. 現場 demo（30 分鐘）** | 30 分鐘 | 給已經寫過 RAG 的人看「成品長怎樣」、時間有限的工作坊、想用 Stage 1 當 Stage 2/3 的對照 | `.worktree/main/` 跑現成版 |
| **B. 親手刻（90 分鐘）** | 90 分鐘 | 第一次寫 RAG、想體會所有坑、學習 Claude Code Extension + CLI 雙 Agent 協作 | 照下面 M0–M4 走 |

> 教學現場可以**先模式 A 暖身（讓觀眾看到終點）**，再進模式 B（自己刻一遍）。或時間緊就只跑 A，把 B 留作課後練習。

---

## 🎬 模式 A：現場 demo 腳本（30 分鐘，用 main worktree）

> 這份腳本不寫一行 code，純粹**用已完工的 main 分支**展示「普通 RAG + 簡易 KG 萃取」。教觀眾「看見成品」，把心力留給 Stage 2/3。

### ⚠️ 術語先校正（30 秒，不可略）

開講前**先把這個寫在白板**，避免整堂課被誤解：

| 名稱 | 在哪 | Graph 怎麼來 | 技術核心 |
|---|---|---|---|
| **普通 RAG** | main | 沒 graph | ChromaDB top-k 向量檢索 |
| **Naive KG 萃取**（main 上的 graph） | main | 直接叫 Gemini 用 prompt 吐 JSON `{source, target, relationship}` 寫進 SQLite | 一個 prompt + SQLite |
| **Semantic GraphRAG**（真正 GraphRAG） | `feature/semantic-graphrag` | LangChain `SemanticChunker` + `LLMGraphTransformer`，有結構化 entity/relation types | LangChain 整套 pipeline |

🎤 **逐字稿**：
> 「main 上有兩件事在跑：一個是普通 RAG（向量檢索），一個是用單一 prompt 從 chunk 抽出 entity-relation 寫進 SQLite，我們叫它 **naive KG 萃取**。**真正的 GraphRAG 在 Stage 3 那個分支**，用的是 LangChain 整套 pipeline。今天 main 是給你看『手刻版本』，不是給你當 GraphRAG 標準答案。」

### 環境準備（講課前 5 分鐘做完）

```bash
cd /Users/kevinluo/google-agent-ecosystem/Antigravity-work/Normal-RAG2Graph-Project-claude
git worktree list   # 應該看到 .worktree/main 已存在；沒有的話：
# git worktree add .worktree/main main

# 確認 .env 有 GEMINI_API_KEY（如果是新環境）
cat .worktree/main/backend/.env

# 啟動兩個 server（背景跑）
.worktree/main/backend/.venv/bin/python -m uvicorn \
  --app-dir .worktree/main/backend app.main:app \
  --host 127.0.0.1 --port 8000 --reload &
(cd .worktree/main/frontend && npm run dev) &
```

打開 http://localhost:3001（或 3000，看 Next.js 報哪個 port）確認頁面載入。

### ⏱️ 30 分鐘 demo 動線

#### T+0 ~ T+5｜開場 + 上傳第一份 PDF

**🎤 你說**：
> 「你看到的是 Stage 1 完工的樣子。我們今天**不是要從零寫它**——你可以課後照 M0–M4 自己刻一遍。今天先看『可以做到什麼』。」

**👉 你做**：
1. 切 Documents tab → 點 Upload → 上傳一份 5–20 頁 PDF（建議準備 2 份題材不同的 fixture，例如 1 份論文 + 1 份產品文件）
2. 看 progress 卡片跑：parsing → chunking → vectorizing → completed（解說：「這就是 Stage 1 的 9 步資料流的前半段」）

**⚠️ 容易卡住**：上傳超過 30 秒沒進度 → 看 backend log（`tail -f /private/tmp/.../tasks/*.output`），通常是 GEMINI_API_KEY 沒讀到。

#### T+5 ~ T+12｜純 RAG 模式：問問題看 chunks

**👉 你做**：
1. 切 Chat tab，問**事實型問題**：例如「這份文件的核心觀點是什麼？」
2. 等回答出來
3. **指右側面板**：「這就是 retrieved chunks——top-5 相關片段，每個有 relevance score。LLM 拿這 5 個片段拼出答案。」

**🎤 你說**：
> 「注意：**這個系統現在『沒有累積』**。我問第 100 個問題的時候，它還是把這份 PDF 重新切、重新撈一次。下一份 PDF 進來，這一份的知識也不會跟它互相連結——除非我同時都丟在 Chroma 裡，但那也只是讓 retrieval 多一個可能來源，不是真的『連結』。這個限制是 Stage 2 要解的。」

**👉 接著問一個刁鑽問題**：「文件作者是誰？」
- 如果答對 → 強調這是「靠 chunking 把首頁切到一起」的運氣
- 如果答錯 → 完美鋪陳「Stage 3 SemanticChunker 反而會把這題答更糟」（前情提要）

#### T+12 ~ T+22｜Naive KG 萃取：切 Graph tab

**👉 你做**：
1. 切到 Graph 視圖（左面板有 Graph icon 或 Network 按鈕）
2. 等 force-graph 渲染出來

**🎤 你說（指 graph）**：
> 「你看到的這張圖，是後端那個 `extract_and_store_kg()` 的產出。它做了一件**很簡單**的事——對每個 chunk 跑一個 prompt：『給我 source-target-relationship 的 JSON』，然後寫進 SQLite。**這個 prompt 大概 5 行、SQLite schema 大概 3 張表**。沒有 LangChain，沒有 entity type system，沒有 ontology——是 hand-rolled 版本。」

**👉 互動**：
1. 點某個節點 → 看「相連邊高亮 + 反查到對應的 retrieved chunks」
2. 點 chat 答案中的人名 → 看圖上的對應節點被高亮

**🎤 你說（指反查）**：
> 「這個是 M7 的 Hybrid 高亮——chat 跟 graph 是綁在一起的。看似炫，**底下其實只是 chunk_id 強綁定**。前端拿到 chat 回應裡的 entity → 反查那個 entity 屬於哪個 chunk → 在 graph 上把那個 chunk 對應的節點找出來高亮。」

**🎤 重要的「反高潮」**：
> 「但這張圖**不可重現**。你重跑一次，prompt 的隨機性會讓邊變一點、節點數變一點。Stage 3 的 LangChain 版本會解這個，因為它有 entity type 限制。」

#### T+22 ~ T+27｜對照實驗（如果時間夠 + 已開 Stage 3 server）

如果你已經把 `.worktree/semantic-graphrag/` 也跑起來（Stage 3 段落會教），現在可以開另一個 browser tab 並排：

| 觀察 | main (Stage 1) | feature/semantic-graphrag |
|---|---|---|
| 上傳同一份 PDF 切出幾 chunks | 看 backend log | 看 backend log |
| Graph 節點顏色 | 全部同色 | 4–6 種 entity type 顏色 |
| 問「作者是誰」 | 八成答對 | 可能答錯（教學案例） |

如果時間不夠，這段留到 Stage 3 講。

#### T+27 ~ T+30｜收尾，引導進 Stage 2

**🎤 你說**：
> 「這就是 Stage 1 能做到的。RAG 的 query 流暢、graph 視覺化漂亮、反查連動好玩——但**它每次 query 都從零開始**。我問 100 次，它不會累積一份『關於這份 PDF 的個人理解』。」
>
> 「Stage 2 我們要換哲學——讓 LLM 在 ingest 時就把知識**編譯**進一個會持續長大的 markdown wiki。Schema 是 LLM 工作流的 SOP 手冊，wiki 是會複利累積的工件。」
>
> 「進 Stage 2 之前，我們不關 main——它接下來是 Stage 2 的『對比樣本』。」

### 🆘 demo 卡住的緊急方案

| 症狀 | 解法 |
|---|---|
| 上傳一直 processing 不完 | backend log 查 API key；最壞情況用 `git diff` 看 `temp_uploads/` 已有 fixture，跳過上傳直接示範 chat |
| Graph tab 點下去空白 | 後端 `/api/v1/graph` 回傳檢查；可能 `extract_and_store_kg` 拋例外但被 swallow——log 看 `local_graph.db` 有沒有資料 |
| Gemini quota 撞牆 | 換另一把 API key；或切去純講解模式（用截圖） |
| port 3000/8000 被佔 | `lsof -i:3000 -t \| xargs kill` / 8000 同理 |

---

## 🛠️ 模式 B：親手刻 90 分鐘（M0–M4）

> 以下是模式 B 的完整流程。如果剛剛跑了模式 A 暖身，可以告訴觀眾「現在我們把剛剛那個 demo 從零寫一遍」。

> **📓 配套 notebook：[`walkthrough.ipynb`](./walkthrough.ipynb)**
>
> 一份**不啟動 FastAPI** 的 step-by-step notebook，把 Stage 1 後端的 9 個核心步驟（parsing → chunking → embedding → ChromaDB → 檢索 → Gemini 生成 → KG 抽取 → SQLite 寫入 → Hybrid 高亮）拆成可獨立執行的 cell。
>
> **建議跑的時機**（擇一即可）：
> - **M2 之前先預習**：對 RAG 完全沒概念的話，先跑一遍 notebook 建立資料流的直覺，再進 M2 動手蓋後端會少卡很多
> - **M2 之後當對照**：寫完 `backend/app/rag_engine.py` 之後跑 notebook，比較自己的 class 結構跟「裸寫流程式呼叫」的差別
> - **Stage 1 完工後當複習**：跑完整個 Stage 1 後再回頭跑 notebook 把每個步驟看清楚
>
> 跑法：`jupyter notebook walkthrough.ipynb`（首次會請你 `uv add` 補幾個依賴）

## M0：AI Studio 設計 RAG UI（15 分鐘）

### 0-1. 開啟 AI Studio
瀏覽器打開 https://aistudio.google.com → 新對話。

### 0-2. 貼入 UI 設計 prompt
```
幫我設計一個 dark-mode 文件問答平台（RAG Chatbot）的完整 UI，用 React + TailwindCSS 寫一個可預覽的單頁元件。

這是一個「純向量檢索 RAG」平台，沒有知識圖譜功能。不要出現任何 graph、knowledge graph、entity、node 相關的 UI。

佈局：
- 左面板固定寬 450px：文件管理 + 聊天
- 右面板佔滿剩餘空間：顯示檢索到的原文片段（Retrieved Chunks）

左面板：
- 頂部：標題 "Smart RAG"，gradient 文字（藍→靛→紫），副標 "Document Q&A Engine"
- 兩個 tab 可切換：Chat 和 Documents

Chat tab：
- 訊息氣泡列表（user = 靛藍漸層圓角靠右，assistant = 深灰卡片靠左）
- 底部圓形輸入框 + 送出按鈕
- 正在回覆時顯示三個跳動圓點

Documents tab：
- 頂部一個大的「Upload New Document」按鈕（靛藍漸層），支援 docx/pdf/txt
- 上傳中顯示 processing 卡片帶 spinner 與階段文字（parsing → chunking → vectorizing → completed）
- 已索引文件清單，每個有檔名、上傳時間、狀態 badge、垃圾桶刪除圖示

右面板（Retrieved Context）：
- 預設空白：中間顯示文件 icon + 「Ask a question to see retrieved chunks here」
- 提問後顯示 top-5 檢索到的原文片段卡片：來源檔名、relevance score 進度條、text snippet（200 字截斷）

整體風格：
- 背景 slate-950，卡片 slate-800/80，邊框 slate-700/50
- glassmorphism：backdrop-blur、半透明背景
- lucide-react icon（Upload, Send, RefreshCw, FileText, MessageSquare, Database, Trash2, Search）

請產出完整可運行的 React 元件程式碼。
```

### 0-3. 保存設計產出
把產出的 .tsx 存進 `AI-studio-example/smart-rag/app/page.tsx` 當參考。

---

## M1：寫 Spec（10 分鐘）

在 Claude Code 貼入：
```
請依 CLAUDE.md 與 AI-studio-example/smart-rag 的 UI 設計，
撰寫 spec/spec.md 與 spec/PRD.md。

Spec 需涵蓋：
- 後端 API 路由（/api/v1/documents/upload、/status/:job_id、/documents、:doc_id DELETE、/chat/query）
- 資料模型（QueryRequest、ChatResponse、RetrievedChunk、Document、Job）
- ChromaDB collection 設計（一個 documents_collection，metadata 帶 doc_id/file_name/chunk_index）
- Gemini 模型用法（embedding：models/gemini-embedding-001 嚴格寫死；生成：gemini-2.5-flash）
- 前後端透過 chunk_id 強綁定

Review 後問我有沒有要調整再開始 M2。
```

---

## M2：最小 RAG 後端（20 分鐘）

### 2-1. 貼入 prompt
```
請按 spec/spec.md 完成最小可運作的 FastAPI 後端：

1. 在 backend/app/main.py 補上 spec 列出的所有 endpoint
2. 新建 backend/app/rag_engine.py 處理：PDF 解析（pypdf）→ 切割（RecursiveCharacterTextSplitter chunk_size=1000 overlap=200）→ Gemini embedding → 寫入 ChromaDB（PersistentClient path=./local_chromadb）
3. /api/v1/chat/query 用 ChromaDB top-5 檢索 + Gemini 2.5 Flash 生成回答
4. 用 uv 安裝依賴：fastapi[standard]、chromadb、google-generativeai、pypdf、langchain-text-splitters、python-multipart

注意：embedding 模型必須是 "models/gemini-embedding-001"，這是憲法強制。
不要動 .env，假設 GOOGLE_API_KEY 已在環境變數。
```

### 2-2. 等 agent 完成後驗證
```bash
cd backend
uv run uvicorn app.main:app --reload
```
另開 terminal：
```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/documents
```

---

## M3：前端聊天介面（20 分鐘）

### 3-1. 貼入 prompt
```
請把 frontend/app/page.tsx 從現在的起手式骨架，改成 AI-studio-example/smart-rag/app/page.tsx 的完整 RAG 聊天介面，並串接 backend API：

- POST /api/v1/documents/upload + 輪詢 /status/:job_id 顯示 parsing→chunking→vectorizing→completed
- GET /api/v1/documents 載入文件清單
- POST /api/v1/chat/query 送 query，把回應的 retrieved_context 顯示在右面板
- DELETE /api/v1/documents/:doc_id 刪除文件

不需 mock 資料，全部打真實 API。API base url 用 http://127.0.0.1:8000/api/v1。
```

### 3-2. 啟動前端
```bash
cd frontend
npm install     # 第一次
npm run dev
```

### 3-3. 端到端測試
打開 http://localhost:3000：
- [ ] 上傳 PDF 看到 progress 變化
- [ ] 文件清單出現
- [ ] 提問能回答 + 右側顯示 chunks

---

## M4：Stage 1 完工 commit（5 分鐘）

在 Claude Code CLI 終端輸入：
```
/sync
```

Claude Code CLI 會：
1. 讀取 `.collab-sync.md` 確認狀態
2. Review Claude Code Extension 剛寫的程式碼
3. 產生 Conventional Commit
4. 更新狀態與下一步任務

完成後可以推上 GitHub（可選）：
```bash
git push -u origin starter-kit
```

🎉 **Stage 1 完成。你現在有一個能用的純向量 RAG 系統。**

> 停一下，思考：剛剛這個系統，每次 query 都要從零撈 chunks，然後 LLM 重新拼湊答案。**沒有任何累積**——你問了 100 個問題，系統不會比第 1 個問題時更聰明。
>
> 這是 Stage 1 的核心限制。Stage 2 會徹底翻轉這個哲學。

---

# Stage 2｜LLM Wiki（60 分鐘）

> 這個 stage 你不寫程式，**你寫提示**。跟 Claude Code Extension + CLI 共創一份 schema，把它們調教成「自律的 wiki 維護者」。

> **📓 配套 notebook：[`wiki-walkthrough.ipynb`](./wiki-walkthrough.ipynb)**
>
> 一份**在 sandbox 跑的 LLM Wiki demo**，把 [`llm-wiki.md`](./llm-wiki.md) 的模式變成可執行版：建立三層架構（raw / wiki / schema）、跑兩輪 Ingest（看 LLM 怎麼**更新**既有實體頁）、Query（讀 index → fan-out 讀頁面 → 帶引用綜合）、Lint（找孤兒頁、斷掉的連結）、把 query 結果歸檔回 wiki。
>
> **重要**：notebook 操作的是 `wiki-walkthrough-demo/` 子資料夾（sandbox），**不會動到 `wiki-project/`**——後者保留「等你動手」的原貌。
>
> **建議跑的時機**：
> - **「起步」之前先跑一遍**：對 llm-wiki 範式完全沒概念的話，先看 sandbox 跑出什麼、產出哪些檔案，再去跟 Claude Code Extension 共創 `wiki-project/CLAUDE.md` 會有更具體的設計直覺
> - **動手卡住時回來看**：如果跟 Claude Code Extension 討論 schema 卡住，回來看 notebook 的 prompt 怎麼寫、index/log 怎麼維護，照抄一段也行
> - **跑完想清空**：`rm -rf wiki-walkthrough-demo/` 即可
>
> 跑法：`jupyter notebook wiki-walkthrough.ipynb`（沿用 Stage 1 已裝的依賴，不需再 `uv add`）

> **🔗 想看真實規模的 wiki 是什麼樣子？** 打開 `~/google-agent-ecosystem/llm-wiki-graph/`：那是已 ingest 數十份 podcast 逐字稿、累積了一段時間的 wiki repo，可以直接瀏覽器開 `wiki/graph.html` 看頁面之間 `[[link]]` 編譯出來的網絡圖，並對照 `CLAUDE.md` 看一份**實戰過的 schema** 長什麼樣。注意這份 graph **不是** Stage 3 的 entity-relation 知識圖譜，是 wiki-link 網絡圖（差別見最上方對照表的 ⚠️ 註解）。

## ⏱️ 60 分鐘逐步講課腳本

> 這個段落是給講者的 **teleprompter 等級腳本**：每個時間區塊都列出「你說什麼」「你做什麼」「觀眾應該有什麼反應」「容易卡住的點」。如果是自學，可以把「你說」當內心獨白讀過去。

### 開場前的環境檢查（講課前 2 分鐘做完）

```bash
# 確認 starter-kit 分支、wiki 素材都在
cd /Users/kevinluo/google-agent-ecosystem/Antigravity-work/Normal-RAG2Graph-Project-claude
git branch --show-current   # 應該是 starter-kit
ls llm-wiki.md wiki-project/ wiki-walkthrough.ipynb
```

如果 Stage 1 demo 還在跑（`.worktree/main` 那個），**保留它不要關**——等等開場要拿來對比。

---

### 🎬 T+0 ~ T+5｜開場：從 Stage 1 切換思維（5 分鐘）

**🎤 你說（逐字稿可改寫）**：
> 「剛剛我們蓋的 Stage 1 是一個 RAG 系統。它能回答問題，能畫出 graph。但我問各位一個問題：**剛剛這個系統在第 100 次 query 的時候，會比第 1 次更聰明嗎？**」
>
> 「不會。它每次 query 都是從零開始撈 chunk、重新拼湊答案。**沒有任何累積**。文件再讀 100 次也沒差。」
>
> 「那如果我們換一個哲學——讓 LLM 在 ingest 的當下就把知識**編譯**進一個會持續長大的知識庫，之後 query 是讀這個編譯好的成品，不是每次都重新跑流水線——這就是 Stage 2。」

**👉 你做**：
1. 切到瀏覽器 Stage 1 demo（http://localhost:3001），指著 force-graph：「這就是 Stage 1，每次 query 重新撈」
2. 切回 IDE，打開 `walkthrough.md` 最頂端的三階段對照表，圈出 Stage 1 vs Stage 2 「你寫什麼」這欄：「Stage 1 寫程式，Stage 2 寫提示」

**🎯 觀眾應該**：意識到「累積」這個關鍵字，產生「那要怎麼累積？」的疑問。

**⚠️ 容易卡住**：如果觀眾問「為什麼不直接給 LLM 大 context？」——回答「因為 context 不會跨 session 持續，wiki 是磁碟上的 markdown 會永遠累積」。

---

### 🎬 T+5 ~ T+18｜核心理念：讀 llm-wiki.md（13 分鐘）

**👉 你做**：打開 `llm-wiki.md`，**全螢幕**。

**🎤 你說（按段落帶讀）**：

**第 9–13 行（核心理念）—— 帶讀並停下來解釋**：
> 「⋯⋯**LLM 不是在 query 時才重新發現知識，而是把知識編譯一次後持續維護**⋯⋯」
>
> 「停一下。這句話是整個 Stage 2 的引擎。RAG 是『lazy』——查的時候才動。Wiki-LLM 是『eager』——存的時候就動。」

**第 17 行（IDE 比喻）—— 強調**：
> 「**編輯器是 IDE，LLM 是程式員，wiki 是 codebase。** ——這個比喻很重要，等等共創 schema 時你會親身體會。你不再是『使用者問問題』，你是『工程師發 spec 給 LLM』。」

**第 31–37 行（三層架構）—— 寫白板 / 畫圖**：
畫這個圖（也可以直接秀第 31–37 行）：
```
[Raw sources]    ← 你選的原始文件，read-only
     ↓ ingest
[Wiki]           ← LLM 寫，markdown，持續維護
     ↑ 規範
[Schema]         ← CLAUDE.md，告訴 LLM 怎麼維護 wiki
```
> 「Stage 2 的核心交付不是 wiki 內容，是 **schema**——也就是 CLAUDE.md。schema 對了，wiki 自己會長。」

**第 41–47 行（Ingest / Query / Lint）—— 快速帶過**：
> 「三個動作：放新東西 (Ingest)、問問題 (Query)、定期健檢 (Lint)。每個都會在 schema 裡寫成 SOP。」

**🎯 觀眾應該**：能用自己的話講出「raw / wiki / schema」三層的分工。

**⚠️ 容易卡住**：
- 「這跟 Notion / Obsidian 有什麼差？」→ 「Notion/Obsidian 是人寫；這裡是 LLM 寫，**你只讀**。」
- 「LLM 寫的會不會錯？」→ 「會。所以有 Lint，定期讓 LLM 自己健檢矛盾與孤兒頁。這是真實的問題，Stage 2 不藏。」

---

### 🎬 T+18 ~ T+25｜看真實規模的 wiki 長什麼樣（7 分鐘，視時間可選）

> 這段是「讓觀眾看到終點」，避免他們覺得 wiki-LLM 只是空想。

**👉 你做**：
```bash
cd ~/google-agent-ecosystem/llm-wiki-graph
ls wiki/
open wiki/graph.html        # 瀏覽器看 wiki-link 網絡圖
code CLAUDE.md              # 看實戰過的 schema 長什麼樣
```

**🎤 你說**：
> 「這是我累積一段時間的真實 wiki，已經 ingest 數十份 podcast。打開 `graph.html` 你看到這張網——**節點是 markdown 頁面，邊是 `[[wiki-link]]` 引用**。沒有資料庫、沒有向量，這張圖是 markdown 之間互引的編譯結果。」
>
> 「⚠️ 注意：**這張圖跟 Stage 1 / Stage 3 的知識圖譜不一樣**。Stage 1/3 的圖是『LLM 從文字抽出來的 entity-relation』；這張圖是『人類引用結構編出來的』——換句話說，wiki 寫得越認真，圖越漂亮。」
>
> 「再看 CLAUDE.md——這份 schema 大概 200 行，4 大 SOP。等等我們也會跟 Claude Code Extension 共創一份這樣的東西。」

**🎯 觀眾應該**：相信「這真的能跑、不只是 toy」。

**⚠️ 如果時間緊**：可以跳過這段，直接進入 T+25。但建議至少花 2 分鐘秀 `graph.html` 截圖。

---

### 🎬 T+25 ~ T+30｜進入 wiki-project，定位 Stage 2 任務（5 分鐘）

**👉 你做**：
```bash
cd /Users/kevinluo/google-agent-ecosystem/Antigravity-work/Normal-RAG2Graph-Project-claude/wiki-project
ls
```
打開 `wiki-project/README.md`，讓觀眾看到「Stage 2 的家」。

**🎤 你說**：
> 「現在我們進入 `wiki-project/`。這就是 Stage 2 的工作區。注意 `raw/` 是空的、`wiki/` 是空的——什麼都沒有。**等一下要無中生有，靠的是一份 prompt + Claude Code Extension。**」
>
> 「跟 Stage 1 完全不一樣：Stage 1 我們開了 IDE 寫 Python 寫 React，這裡我們**只開 chat 窗、只打字**。沒有任何手刻 code。」

**🎯 觀眾應該**：意識到本 Stage 的工具切換（從 IDE 編程切到 chat 共創）。

---

### 🎬 T+30 ~ T+45｜共創 CLAUDE.md schema（15 分鐘，本 Stage 高潮）

**👉 你做**：打開 Claude Code panel，貼入起手式 prompt：

```
請讀取專案根目錄的 llm-wiki.md，那是一份高層的 pattern 描述。
請跟我一起用這個 pattern 來實例化 wiki-project/ 這個資料夾：

1. 先讀完 llm-wiki.md，跟我討論 3 個關鍵設計決策
   （例如：我們的 raw/ 要放什麼類型的文件？wiki/ 的目錄要不要分 entities/concepts/sources/synthesis？）
2. 確認方向後，幫我在 wiki-project/CLAUDE.md 寫一份「給 Claude Code CLI 看的 schema」
3. 完成後更新 .collab-sync.md，交給 Claude Code CLI Review。
```

**🎤 你邊等邊說**：
> 「我刻意叫它『先討論再寫』。這是 Stage 2 最重要的節奏——**不要讓 Claude Code Extension 急著吐 1000 行 schema**，要先確認方向。」

**Claude Code Extension 應該回問你 2–3 個問題**，例如：
- 「這個 wiki 的領域是什麼？」（決定 entity 類別）
- 「raw 來源類型？」（PDF? podcast 逐字稿? Slack?）
- 「規模預期？」（10 份 vs 100 份 vs 1000 份決定要不要 sub-folder）

**🎤 你示範回答**（觀眾現場應該也回答自己的版本）：
> 「我這個 wiki 想累積『LLM Agent 開發實戰心得』，raw 主要是 podcast 逐字稿 + 部落格文章 + 技術 RFC，預期 50–100 份。entities 主要是『人』『產品』『技術概念』。」

**Claude Code Extension 拿到答案後產出 CLAUDE.md**，至少要有：
- 4 大 SOP（Ingest / Query / Lint / 擴充搜尋）
- 頁面 frontmatter 約定（`type:`, `aliases:`, `last_updated:`...）
- `index.md` / `log.md` 維護規則

**🎤 你逐段點評**（這是教學重點）：
> 「看這段 Ingest SOP——它寫『先讀來源、跟使用者討論 2–3 個重點、再寫 wiki 摘要、再更新 index、最後在 log 加一筆』。這個順序是有意設計的：**先共識再動筆，避免 LLM 寫一堆你不滿意的東西**。」
>
> 「再看 frontmatter——`type: entity` vs `type: concept` 看起來只是 metadata，但 Lint SOP 會用這個 type 找『哪些 entity 沒被任何頁面引用』，這就是孤兒檢測。」

**🎯 觀眾應該**：理解 schema 不是死格式，是「LLM 工作流的 SOP 手冊」。

**⚠️ 容易卡住**：
- Claude Code Extension 不問問題就直接寫一大篇 → 打斷它，回「先停，先問我問題再寫」
- Claude Code Extension 寫的 SOP 太抽象 → 要求「給每個 SOP 一個『最小範例』，例如 Ingest SOP 要附一份示範 raw 文件處理後產出的所有頁面 diff」
- 觀眾覺得 schema 太長看不懂 → 強調「這份 schema 你以後**不用每次重看**，是 Claude Code Extension / Claude Code CLI 自動讀的」

---

### 🎬 T+45 ~ T+55｜第一次 Ingest：見證 wiki 從無到有（10 分鐘）

**👉 你做**：
1. 準備一份 raw 文件丟進 `wiki-project/raw/`（podcast 逐字稿 / 一篇技術文章 / 一份 PDF 都行；建議 < 5000 字以節省 demo 時間）
2. 打開 Claude Code CLI 終端：

```
我剛在 wiki-project/raw/ 放了一份新文件 [檔名]，請依 wiki-project/CLAUDE.md 的 Ingest SOP 處理它。
記得跟我討論 2–3 個關鍵重點再動筆。
```

**🎤 你邊等邊說**：
> 「注意這次是 **Claude Code CLI**，不是 Claude Code Extension。為什麼？**因為 Claude Code Extension 是『創造者』，Claude Code CLI 是『維護者』。schema 設計階段用 Claude Code Extension，日常 ingest 用 Claude Code CLI——這是雙 Agent 分工，等等也會跑 `/sync`。」

**Claude Code CLI 應該**先回 2–3 個重點摘要請你確認，然後動筆。

**🎤 觀察 wiki/ 變化時說**（同時用檔案總管展開 `wiki/` 樹狀）：
> 「看這個——它建了 `wiki/sources/[來源].md` 摘要頁，建了 `wiki/entities/張三.md` 實體頁，更新了 `wiki/index.md`、加了一筆 `wiki/log.md`。**一份 raw 進來、5–10 個 wiki 頁面被建立或修改**——這就是『編譯式知識管理』。」
>
> 「重點是：之後我問『張三是誰？』，LLM 不再從 raw 撈、不再重新拼答案——它**讀 `wiki/entities/張三.md`** 就好。每次 ingest 都讓這個 entity 頁面變得更豐富，這就是複利累積。」

**👉 額外動作**（時間夠的話）：
- 用 `git diff` 看 LLM 改了哪些檔案：`cd wiki-project && git diff --stat`
- 試著問一個 query：`gemini "張三主導過哪些專案？"`，觀察它讀 wiki 不讀 raw

**🎯 觀眾應該**：親眼看到「一份 raw → N 個 wiki 頁面」的扇出效應。

---

### 🎬 T+55 ~ T+60｜收尾：對比 + 拋 Stage 3 引子（5 分鐘）

**👉 你做**：在 Claude Code CLI 跑：
```
/sync
```
完成 commit 後，打開 walkthrough.md 三階段對照表。

**🎤 你說**：
> 「我們做完 Stage 1 跟 Stage 2 了，停下來感受差別：」
>
> | 比較項 | Stage 1 RAG | Stage 2 Wiki |
> |---|---|---|
> | 知識在哪裡 | ChromaDB（embedding） | markdown 檔案 |
> | 何時編譯 | query 時動態撈 | ingest 時就寫死 |
> | LLM 角色 | 撈 chunks + 拼答案 | 編寫 + 維護知識庫 |
> | 「Graph」是什麼 | LLM 從文字抽 entity-relation | markdown 之間 wiki-link |
> | 第 100 次 query 比第 1 次聰明嗎 | **不會** | **會**（wiki 累積了） |
>
> 「那 Stage 3 呢？Stage 3 用 LangChain 把 Stage 1 自動化，做 semantic chunking + LLMGraphTransformer。但你會看到一個有趣的反差——**`SemanticChunker` 對作者類查詢反而比 Stage 1 差**。為什麼？等等切到 `feature/semantic-graphrag` 分支看實作就知道。」

**🎯 觀眾應該**：能用一句話講出 Stage 1 vs Stage 2 的本質差。

---

## 🆘 講課中卡住的緊急方案

| 症狀 | 解法 |
|---|---|
| Claude Code Extension 不肯問問題、直接吐一大篇 schema | 打斷：「先停。把這份丟掉。先問我 3 個關鍵問題再寫。」 |
| 共創 schema 卡超過 20 分鐘 | 切到 `~/google-agent-ecosystem/llm-wiki-graph/CLAUDE.md`，現場「抄一份來改」 |
| Claude Code CLI Ingest 跑超過 5 分鐘 | 中斷，改貼 `wiki-walkthrough.ipynb` 已經跑過的截圖 |
| 觀眾混淆 Stage 2 graph vs Stage 1 graph | 翻到 walkthrough.md 最頂端 ⚠️ 那段對照框，照著念 |
| 完全沒時間做 live ingest | 改成「我已經先 ingest 過了」，直接秀 `~/google-agent-ecosystem/llm-wiki-graph/wiki/` 的成品 |

---

## 起步（如果不照腳本走、想自己摸索）

```bash
cd wiki-project
ls
```
你會看到 `README.md`。仔細讀完 README（5 分鐘），照裡面的「起手式 Prompt」貼到 Claude Code Extension 開始。

## Stage 2 完成標準

- [ ] `wiki-project/CLAUDE.md` 有完整 4 大 SOP
- [ ] `wiki-project/raw/` 至少 1 份原始文件
- [ ] `wiki-project/wiki/` 至少 5 個 page（包含 index.md、log.md、overview.md）
- [ ] 跑過一次 Lint，能列出 2 個改進建議
- [ ] Claude Code CLI `/sync` 完成 commit

🎉 **Stage 2 完成。你現在親身體會了「累積式知識」跟「檢索式 RAG」的根本差別。**

> 停一下，思考：Stage 1 跟 Stage 2 的差別不只是技術，是**心智模型**：
> - Stage 1 把文件當「資料倉儲」，每次 query 都重新提取
> - Stage 2 把文件當「論點原料」，編譯一次後持續維護
>
> 那 Stage 3 呢？Stage 3 是「能不能讓 Stage 1 的自動化 + Stage 2 的結構化同時存在」。

---

# Stage 3｜Semantic GraphRAG（60–90 分鐘，主要是讀 code）

> 這個 stage 你不再從零寫，而是**切到對照分支看現成實作**——LangChain 標準堆疊（SemanticChunker + LLMGraphTransformer）的完整 GraphRAG。重點是對比 Stage 1 看出差異。

## 用 worktree 同時開三個分支（推薦）

> 不要 `git checkout` 切過去——那會讓你失去 main demo 跟 starter-kit 的工作區。改用 git worktree 同時保有三個分支的可運行副本：

```bash
# 從 starter-kit 根目錄
git worktree list   # 確認現況

# 三個 worktree 應該長這樣（可能已經建好了）：
# .                                  [starter-kit]   ← 你正在編輯的工作區
# .worktree/main                     [main]          ← Stage 1 完工 demo
# .worktree/semantic-graphrag        [feature/semantic-graphrag]  ← Stage 3 對照

# 沒建的話：
# git worktree add .worktree/semantic-graphrag feature/semantic-graphrag
```

切到對照分支內容看：
```bash
cd .worktree/semantic-graphrag
ls backend/app/      # semantic_rag_engine.py + 保留的 rag_engine.py
ls docs/plans/       # 17-task 實作計畫
```

關鍵檔案：
- `backend/app/semantic_rag_engine.py` 是完整實作
- `backend/app/rag_engine.py` 仍保留當對照
- `frontend/app/components/GraphLegend.tsx` 是新的圖例元件
- `docs/plans/2026-04-24-semantic-graphrag-design.md` 是設計理念
- `docs/plans/2026-04-24-semantic-graphrag-implementation.md` 是 17-task 實作計畫（為 Extension+CLI 雙 Agent 協作設計）

## 啟動 Stage 3 server（在 worktree 裡）

> 注意 port 衝突：main 已經佔了 8000/3001。Stage 3 改用 8001/3002。

```bash
# 確認 .env 存在（從 main worktree 複製或重寫）
cp .worktree/main/backend/.env .worktree/semantic-graphrag/backend/.env

# Backend (port 8001)
cd .worktree/semantic-graphrag/backend
uv sync                              # 第一次跑會多裝 langchain 一系列
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8001 &

# Frontend (port 3002)
cd ../frontend
npm install                          # 依賴比 main 多 GraphLegend 用的東西
PORT=3002 npm run dev &
```

> ⚠️ 前端 hardcode `http://127.0.0.1:8000`，要對到 Stage 3 後端必須改 `frontend/app/page.tsx` 跟 `GraphView.tsx` 的 API base URL，或在前端啟動時用 reverse proxy。最簡單做法：**Stage 3 demo 時先 kill 掉 main 的 8000，把 Stage 3 後端改回 8000**：
> ```bash
> lsof -i:8000 -t | xargs kill
> cd .worktree/semantic-graphrag/backend
> uv run uvicorn app.main:app --reload --port 8000 &
> ```

跑測試確認 Stage 3 backend 健康：
```bash
cd .worktree/semantic-graphrag/backend
uv run pytest -v   # 應該全綠
```

## 🎬 對照實驗腳本（教學高潮，20 分鐘）

> 這是 Stage 3 的核心戲。你會**並排比較 main vs semantic-graphrag**，讓觀眾親眼看到 LangChain 加什麼、減什麼、犧牲什麼。

### 環境準備（demo 前 5 分鐘）

最佳設定：**雙 browser 視窗並排**
- 左視窗：main demo（http://localhost:3001 或 3000）— 已經在跑
- 右視窗：Stage 3 demo（http://localhost:3002，或暫時佔 3000 都可）

如果 port 衝突太麻煩，**改用「先後輪流」**：跑完 main 上傳 + chat + graph 截圖，kill 掉再跑 Stage 3 重做一次。

### T+0 ~ T+5｜兩邊各上傳同一份 PDF

**👉 準備一份「論文型」PDF**（重點是首頁有作者列表）：例如 arxiv 的論文。

**🎤 你說**：
> 「我們上傳同一份 PDF 到兩邊。注意 backend log——你會看到 main 是用 `RecursiveCharacterTextSplitter` 切（chunk_size=1000、overlap=200，固定字數），Stage 3 是用 `SemanticChunker` 切（按語意相似度切，chunk 數會不一樣）。」

兩邊都點 Upload，同時看 progress 跑完。

### T+5 ~ T+10｜對照表第一行：chunk 數

打開兩邊 backend log：
```bash
# main 那邊
grep "chunks" /private/tmp/.../main-backend.log | tail
# semantic 那邊
grep "chunks" /private/tmp/.../semantic-backend.log | tail
```

填入對照表：

| 觀察項 | main (Stage 1) | feature/semantic-graphrag |
|---|---|---|
| 切出幾個 chunk | 例如 47 | 例如 23 |
| 每個 chunk 平均字數 | ~800 | 變動大（300–2500） |

**🎤 你說**：
> 「同一份文件，main 切 47 個固定大小的 chunk，Stage 3 切 23 個語意相似的 chunk——**少一半**。優點：每個 chunk 主題集中，retrieval 命中率理論上更高。缺點：等等問『作者是誰』你會看到。」

### T+10 ~ T+15｜對照表第二行：Graph 結構

兩邊都切到 Graph tab：

| 觀察項 | main (Stage 1) | feature/semantic-graphrag |
|---|---|---|
| Graph 節點顏色種類 | 全部同色（沒 type） | 4–6 種（Person/Organization/Concept/Location/Date/Other） |
| Relation 型別 | 自由文字（每次跑都不一樣） | 固定列表（WORKS_AT / LOCATED_IN / AUTHORED_BY...） |
| 重跑同一份 PDF 的可重現性 | 邊會改變 | 結構穩定 |

**🎤 你說（指 Stage 3 的彩色圖）**：
> 「Stage 3 的圖**有顏色**——這是 LangChain `LLMGraphTransformer` 的功勞。你給它 `allowed_nodes=["Person", "Organization", ...]` 跟 `allowed_relationships=["WORKS_AT", ...]`，它會強制 LLM 只能在這個 ontology 裡選。**這就是『可重現的 graph』**。main 那邊每次跑都會微妙不一樣，因為 prompt 沒給限制。」

### T+15 ~ T+20｜核心教學案例：問「作者是誰」

這是 walkthrough memory 裡記載的關鍵教學點——**Stage 3 反而會敗給 Stage 1**。

**👉 兩邊都問**：「這份論文的作者是誰？列出所有作者跟所屬機構。」

| 結果 | main (Stage 1) | feature/semantic-graphrag |
|---|---|---|
| 答對作者列表 | ✅ 通常對 | ❌ 經常錯 |
| 答對機構 | ✅ 通常對 | ❌ 可能拿到 References 段落的機構 |

**🎤 你說（重點教學）**：
> 「咦？**Stage 3 不是更先進嗎？怎麼答錯了？**」
>
> 「答案在 SemanticChunker 的 chunking 邏輯裡。論文首頁的作者列表是這樣的：『Alice (MIT), Bob (Stanford), Carol (CMU)...』——這在語意上跟內文的『方法』『實驗』段落**主題完全不相關**。SemanticChunker 看到主題斷層就切——**結果首頁作者列表變成一個獨立的小 chunk，topical coherence 很弱、embedding 質量差**。」
>
> 「另一邊，論文 References 段落充滿『Smith et al. (Google), Jones et al. (Microsoft)...』這種模式。當你問『作者是誰』時，retrieval 算 embedding 相似度——**References 段落的密集作者+機構 pattern 反而比首頁那個小 chunk 更接近 query**。」
>
> 「結果：**main 用粗暴的固定字切，反而把首頁作者跟 abstract 切在一起，retrieval 命中**。Stage 3 的『聰明切割』反而傷了它。」
>
> 「**這就是 semantic chunking 的真實代價。** 每個技術選擇都有代價——這是這堂課最重要的一課。」

### T+20 ~ T+30｜其他對照與收尾

剩下的對照（時間夠就跑、不夠就用截圖）：

| 觀察項 | main | semantic |
|---|---|---|
| 問「文件講了哪些核心概念」 | 答得鬆散 | 通常更聚焦（語意切的優勢回來了） |
| Graph 看「實體跟誰連最多」 | Hub 散亂 | Hub 結構清楚 |
| 點 chat 答案的實體反查 graph | 邊有時對不到（型別不固定） | 穩定對到 |

**🎤 收尾**：
> 「對照表填完——這就是 Stage 3 的全貌。LangChain 不是『答案』，它是**一組權衡好的選擇**。你需要不需要 entity type ontology？需要不需要 chunk 的語意聚合？這些都是看用例的。」
>
> 「Stage 1 + Stage 2 + Stage 3 三條路你都看過了。下一步——**完成標準對照表**，回頭看你選哪條路適合自己的情境。」

## Stage 3 完成標準

- [ ] 跑過 backend 測試 `cd backend && uv run pytest -v` 全綠（4 個測試）
- [ ] 上傳 PDF 後 Graph 出現多色節點
- [ ] 點節點能看到「相連邊金色 + 一跳鄰居正常 + 其他節點變暗」
- [ ] Chat 答案中的實體能點擊反查到 Graph
- [ ] 對照表都填完

🎉 **Stage 3 完成。你看完了 LangChain 怎麼把 Stage 1+2 的精神自動化。**

---

# 三階段對照與選擇指南

完成所有 stages 後，這張表會幫你選對工具：

| 你的情境 | 用哪個 stage 的方案 |
|---|---|
| 文件多但更新慢、查詢需求標準化 | **Stage 1** 純 RAG 夠了，最便宜 |
| 文件累積成長、要維護論點演化、需要 contradictions 標記 | **Stage 2** LLM Wiki 路線 |
| 要可重現的結構化 graph、團隊協作、要視覺化 entity 關係 | **Stage 3** Semantic GraphRAG |
| 要兼顧累積與自動化（生產級） | Stage 2 + 3 混合：Wiki 當 source of truth、定期跑 Stage 3 自動圖譜萃取 |

---

# 時間估算

| 階段 | 估時 | 備註 |
|---|---|---|
| Phase 0 環境準備 | 5 min | 一次性 |
| Stage 1（M0–M4） | 70–90 min | 學生會卡在 RAG 細節 |
| Stage 2（wiki-project） | 50–70 min | 卡在「跟 Claude Code Extension 討論 schema」的耐心 |
| Stage 3（feature 分支對照） | 50–70 min | 多花在「讀懂 + 跑對照實驗」 |
| 全部 | **3–4 小時** | 中間可以分天進行 |

---

# 如果卡住了

| 症狀 | 排查 |
|---|---|
| `uv run` 報 module not found | 在 `backend/` 目錄執行；先 `uv sync` |
| 上傳後沒索引 | `cd backend && uv run pytest` 看後端是不是炸；確認 `GOOGLE_API_KEY` 有設 |
| 前端打 API 失敗 | 看瀏覽器 Network → CORS 是否擋住；後端要在 8000 port 跑 |
| Claude Code 沒讀到 CLAUDE.md | 在對話框輸入「請讀取專案根目錄的 CLAUDE.md 並列出技術棧限制」 |
| Claude Code CLI `/sync` 找不到 | 確認 `.claude/commands/sync.md` 存在；CLI 啟動時 `claude` 要在專案根目錄跑（project-scope slash command 才會載入） |
| Skill 沒被自動 invoke | 直接在對話中明說：「請用 Skill(rag-pipeline) 載入規則再實作」強制 invoke |
| Stage 2 Claude Code Extension 不知道怎麼開始 | 重新貼起手式 prompt（README 裡那段），強調「先讀 llm-wiki.md 再討論」 |
| Stage 3 切分支後 backend 起不來 | 兩分支依賴不同：`cd backend && uv sync` 重建 |

---

> **🎓 完成 3 個 stages 後**：你不只會用 RAG，你看得出何時該用、何時不該用。這是這份教學的最終目標。
