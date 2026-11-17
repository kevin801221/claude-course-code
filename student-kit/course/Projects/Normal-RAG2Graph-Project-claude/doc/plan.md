結構是 Rules（專案憲法）→ Skills（可重用知識包）→ Workflow Prompts（里程碑式引導），最後附   Gemini CLI 的輔助用法。                                                                                                                  
                                                   
  ---                                                                                                                                      
  🎓 教學腳本：用 Antigravity + Gemini CLI 重建 Hybrid GraphRAG                                                                            
                                                                                                                                           
  課程目標：學生從 0 → 普通 RAG → GitHub → Antigravity Workflow → GraphRAG → 雙模式切換 + 反查高亮。                                       
  分節：7 個 Milestone，每節 30–45 分鐘。                                                                                                  
                                                                                                                                           
  ---                                                                                                                                      
  Part A｜Rules：專案憲法（學生第一步就建立）                                                                                              
                                                                                                                                           
在 Antigravity 專案根目錄建立 .agents/rules.md，這是 agent 每次行動都會讀到的「最高指導原則」。教學生把規則寫死，避免 agent 亂發揮。
                                                                                                                                         
  # Project Rules — Hybrid GraphRAG
                                                                                                                                           
  ## 語言                                                                                                                                  
  - 所有回應、commit message、註解一律繁體中文。                                                                                           
  - 變數/函式名維持英文。                                                                                                                  
                  
  ## 技術棧（鎖死）                                                                                                                        
  - Backend: Python 3.10+、FastAPI、uv 管理依賴（禁用 pip/poetry）。
  - Vector: ChromaDB（本地 persistent）。                                                                                                  
  - LLM: Google Gemini（`gemini-2.5-flash` + `gemini-embedding-001`）。                                                                    
  - Frontend: Next.js App Router + TypeScript + TailwindCSS。                                                                              
  - 圖譜視覺化: `react-force-graph-2d`。                                                                                                   
                                                                                                                                           
  ## 工作流程                                                                                                                              
  1. 動手寫 code 前，先產出 / 更新 `spec/spec.md` 與 `spec/PRD.md`。                                                                       
  2. 每完成一個 milestone，必須 `git commit`，訊息由 Gemini CLI 產生。                                                                     
  3. 禁止引入 Celery/Redis/Neo4j，背景工作只用 FastAPI BackgroundTasks。                                                                   
  4. 前後端透過 `chunk_id` 強綁定，Graph 與 Vector 不可分離。                                                                              
                                                                                                                                           
  ## 禁忌                                                                                                                                  
  - 不要 mock 資料庫。                                                                                                                     
  - 不要自行 npm install 未列在 Rules 的套件，先問。                                                                                       
  - 不要動 `.env`、不要 commit API key。                                                                                                   
                                                                                                                                           
  教學重點：告訴學生 Rules = 寫給 agent 看的 CLAUDE.md／AGENTS.md，放在 .agents/ 下 Antigravity 會自動載入。                               
                                                                                                                                           
  ---                                                                                                                                      
  Part B｜Skills：可重用知識包（4 個就夠）
                                          
  在 .agents/skills/ 下建立 4 個 .md。Skill 的寫法是 「何時觸發 + 具體作法」。
                                                                                                                                           
  Skill 1｜skills/rag-pipeline.md
                                                                                                                                           
  ---             
  name: rag-pipeline                                                                                                                       
  description: 建立 parse → chunk → embed → Chroma 的最小 RAG 流程。觸發於「建立 RAG」「vectorize」「chunk 文件」等關鍵字。
  ---                                                                                                                                      
  ## 步驟         
  1. 解析：docx → docx2txt、pdf → pypdf、txt/md → open()。                                                                                 
  2. 切 chunk：LlamaIndex SentenceSplitter(chunk_size=512, chunk_overlap=50)。                                                             
  3. 每個 chunk 產生 UUID 當 `chunk_id`，寫入 Chroma metadata。                                                                            
  4. 查詢：`retriever.retrieve(query)` top_k=5，回傳 chunk_id 供反查。                                                                     
                                                                                                                                           
  ## 強制                                                                                                                                  
  - 空知識庫 → 直接回「請先上傳文件」，禁止 LLM 自由發揮。                                                                                 
  - metadata 必含 `chunk_id`、`doc_id`，否則後續 Graph 反查會斷。                                                                          
                                                                                                                                           
  Skill 2｜skills/graph-extraction.md                                                                                                      
                                                                                                                                           
  ---                                                                                                                                      
  name: graph-extraction
  description: 從 chunk 萃取 canonical entities + relations 存 SQLite。觸發於「GraphRAG」「knowledge graph」「entity extraction」。
  ---                                                                                                                                      
  ## Schema（5 張表）
  documents / chunks / entities / links / entity_chunks                                                                                    
  PRAGMA foreign_keys = ON，ON DELETE CASCADE。
                                                                                                                                           
  ## 萃取 Prompt 樣板                                                                                                                      
  只輸出 JSON，欄位：canonical_name / aliases / group(5 種) / summary / salience。                                                         
  group ∈ {Person, Concept, Org, Event, Location}。                                                                                        
                                                                                                                                           
  ## 合併策略                                                                                                                              
  - entity_id = slug(canonical_name)                                                                                                       
  - 同名自動聯集 aliases                                                                                                                   
  - 每個 chunk 失敗獨立 skip，不中斷整份文件                                                                                               
                                                                                                                                           
  Skill 3｜skills/fastapi-uv-setup.md                                                                                                      
                                                                                                                                           
  ---                                                                                                                                      
  name: fastapi-uv-setup
  description: 用 uv 初始化 FastAPI 專案。觸發於「建立後端」「uv init」。
  ---                                                                                                                                      
  指令順序：
  1. `uv init backend --package`                                                                                                           
  2. `cd backend && uv add fastapi uvicorn python-multipart llama-index chromadb ...`                                                      
  3. 程式結構：app/main.py（路由）、app/db.py（SQLite）、app/rag_engine.py（核心）。                                                       
  4. 啟動：`uv run uvicorn app.main:app --reload`                                                                                          
  禁止產生 requirements.txt。                                                                                                              
                                                                                                                                           
  Skill 4｜skills/force-graph-ui.md
                                                                                                                                           
  ---             
  name: force-graph-ui
  description: Next.js + react-force-graph-2d 雙面板 UI。觸發於「前端圖譜」「highlight node」。                                            
  ---                                                                                                                                      
  - ForceGraph2D 必須 dynamic import ssr:false。                                                                                           
  - 高亮流程：收到 `highlighted_node_ids` → 算重心 → `centerAt` → `zoomToFit` → glow。                                                     
  - 節點點擊 → `GET /graph/node/{id}/chunks` → 側欄顯示原文片段。                                                                          
  - 左右雙面板：左 450px Chat/Index tab，右滿版 ForceGraph。                                                                               
                                                                                                                                           
  教學重點：Skill 跟 Rule 差別在於 —— Rule 是每次都套用，Skill 是「碰到相關任務才載入」。                                                  
                                                                                                                                           
  ---                                                                                                                                      
  Part C｜Workflow Prompts：7 個里程碑（這是課堂節奏）
                                                                                                                                           
  每個 Milestone 給學生一段 prompt，學生複製到 Antigravity 的 Agent Manager，看 agent 跑、review diff、再進下一步。
                                                                                                                                           
  🚩 Milestone 0｜寫 Spec（不寫 Code）                                                                                                     
                                                                                                                                           
  Prompt 給學生貼：                                                                                                                        
  你是資深系統架構師。我要做一個 Hybrid RAG 平台：
  - 使用者上傳 docx/pdf/txt，後端 chunk + embed 存 Chroma。                                                                                
  - 前端左邊 chatbot，右邊顯示文件清單。                                                                                                   
  - 未來會升級成 GraphRAG，要能在「普通 RAG」「GraphRAG」兩種模式切換。                                                                    
                                                                                                                                           
  請依 rules.md，先產出 spec/spec.md 與 spec/PRD.md，涵蓋：                                                                                
  1. 技術棧 2. 資料流 3. API 列表 4. YAGNI 清單。                                                                                          
  禁止寫任何 code，只寫 spec。完成後等我 review。                                                                                          
  教學動作：帶學生讀 spec，討論 YAGNI 清單（讓他們體會「砍需求」比「加需求」重要）。                                                       
                                                                                                                                           
  ---                                                                                                                                      
  🚩 Milestone 1｜最小 RAG 後端（不含 Graph）                                                                                              
                                                                                                                                           
  Prompt：        
  根據 spec/spec.md §1–§4，呼叫 skill: fastapi-uv-setup + rag-pipeline，                                                                   
  建立 backend/：                                                       
  - app/main.py：POST /upload、POST /query、GET /documents、DELETE /documents/{id}                                                         
  - app/rag_engine.py：parse_document、chunk_text、vectorize、query_vector        
  - 不要做 Graph、不要做 SQLite，純 Chroma。                                                                                               
  - 用 BackgroundTasks 跑 ingestion，回傳 job_id，另開 /status/{job_id}。                                                                  
  完成後執行 `uv run uvicorn app.main:app --reload` 驗證啟動成功。                                                                         
  教學動作：用 curl 或 Antigravity 內建 HTTP client 打 API，確認能上傳+問答。                                                              
                                                                                                                                           
  ---                                                                                                                                      
  🚩 Milestone 2｜前端聊天介面                                                                                                             
                                                                                                                                           
  Prompt：        
  呼叫 skill: force-graph-ui（但這一版還沒 Graph，先不要 import ForceGraph）。
  在 frontend/ 建立 Next.js App Router 專案：                                                                                              
  - app/page.tsx：左 450px Chat + Data Index tab，右邊暫時顯示「Graph Coming Soon」佔位。                                                  
  - 串接 http://localhost:8000 的 /upload /query /documents。                                                                              
  - 用 Tailwind + lucide-react icon，深色 glassmorphism 風格。                                                                             
  - 上傳後 2 秒 poll /status/{job_id}，完成後 refresh docs 清單。                                                                          
  跑 `npm run dev` 驗證。                                                                                                                  
  教學動作：這一步完成 = 學生手上已經有一個能用的普通 RAG。讓他們真的上傳文件問答，建立成就感。                                            
                                                                                                                                           
  ---                                                                                                                                      
  🚩 Milestone 3｜第一次 Commit（用 Gemini CLI）
                                                                                                                                           
  教學生這個指令：
  # 初始化 repo                                                                                                                            
  git init && git add .
                                                                                                                                           
  # 用 Gemini CLI 產生 commit message                                                                                                      
  git diff --cached | gemini -p "你是 git commit 專家。                                                                                    
  根據以下 diff，產生一行繁體中文 conventional commit，                                                                                    
  格式：<type>: <description>，不超過 72 字元。只輸出訊息本體。"                                                                           
                                                                                                                                           
  # 貼回去 commit                                                                                                                          
  git commit -m "feat: 建立最小可用 Vector RAG 平台"                                                                                       
  gh repo create hybrid-graphrag --public --source=. --push                                                                                
  教學重點：示範 Gemini CLI 當「純文字管線工具」，不開 IDE 也能跑 AI。可以教 alias：                                                       
  alias gmsg='git diff --cached | gemini -p "產生繁中 conventional commit"'                                                                
                                                                                                                                           
  ---                                                                                                                                      
  🚩 Milestone 4｜Antigravity Workflow 自動化                                                                                              
                                             
  在 .agents/workflows/ci.yaml（或 Antigravity 對應的 workflow 檔）建立：                                                                  
  name: post-commit-sync                                                                                                                   
  trigger: on_commit    
  steps:                                                                                                                                   
    - name: 跑 backend smoke test
      run: cd backend && uv run python -c "from app.main import app; print('ok')"                                                          
    - name: 跑 frontend typecheck                                                                                                          
      run: cd frontend && npx tsc --noEmit
    - name: 推上 GitHub                                                                                                                    
      run: git push origin main
    - name: 用 Gemini 生成 release note                                                                                                    
      agent: gemini                    
      prompt: "讀最新 commit，寫 3 行 changelog 到 CHANGELOG.md"                                                                           
  Prompt 給 Agent：                                                                                                                        
  幫我建立 Antigravity workflow：每次 commit 後自動跑 type check、push 到 GitHub、                                                         
  並叫 Gemini 更新 CHANGELOG.md。檔案放 .agents/workflows/。                                                                               
  教學重點：讓學生體會 workflow = agent 版的 GitHub Actions，但由本地 agent 執行。                                                         
                                                                                                                                           
  ---                                                                                                                                      
  🚩 Milestone 5｜升級成 GraphRAG                                                                                                          
                                                                                                                                           
  Prompt：        
  現在要把 Milestone 1 的純 Vector RAG 升級成 Hybrid GraphRAG。                                                                            
  呼叫 skill: graph-extraction。                               
                                                                                                                                           
  步驟：                                                                                                                                   
  1. 新增 backend/app/db.py，建立 5 張 SQLite 表（documents / chunks / entities / links / entity_chunks），schema 見 skill。               
  2. 修改 process_document：vectorize 後多跑一段「每 chunk LLM 萃取 entities+relations」→ upsert entities / entity_chunks / links。        
  3. 新增 /graph/data、/graph/node/{id}/chunks 兩支 API。                                                                                  
  4. 修改 /chat/query：Chroma top-k → 反查 entity_chunks → 組 prompt 帶上 entities + relations → 回傳 highlighted_node_ids。               
  5. 舊的 /upload /query 行為不變，確保 Milestone 1 的測試仍過。                                                                           
                                                                                                                                           
  完成後用既有的 15W315.docx 做一次端到端測試。                                                                                            
  教學動作：讓學生觀察 graph.db 從空變滿的過程，可用 sqlite3 graph.db ".tables" 驗證。                                                     
                                                                                                                                           
  ---                                                                                                                                      
  🚩 Milestone 6｜雙模式切換（RAG ↔ GraphRAG）
                                                                                                                                           
  Prompt：        
  在 backend/app/main.py 的 /chat/query 加一個 `mode: "vector" | "hybrid"` 參數，                                                          
  - vector：只用 Chroma 檢索，不查 SQLite。                                      
  - hybrid：走 Milestone 5 的 GraphRAG 流程。                                                                                              
  預設 hybrid。                                                                                                                            
                                                                                                                                           
  前端 app/page.tsx 在聊天輸入框上方加一個 toggle switch：                                                                                 
  「⚡ Vector Only ↔ 🕸 GraphRAG」，                                                                                                        
  切到 Vector Only 時右邊 ForceGraph 面板灰階、不回傳 highlighted_node_ids。
  state 用 localStorage 持久化。                                                                                                           
  教學重點：這一步是本課最大 AHA — 學生親眼看到「加上 Graph 之後，同一個問題答案變得有根據」。建議讓學生準備兩題：                         
  1. 「這份教材的核心概念有哪些？」→ 兩模式都答得出。                                                                                      
  2. 「A 概念跟 B 概念有什麼關係？」→ 只有 GraphRAG 能高亮出關係鏈。                                                                       
                                                                                                                                           
  ---                                                                                                                                      
  🚩 Milestone 7｜反查高亮（終局）                                                                                                         
                                                                                                                                           
  Prompt：        
  完成 chunk↔entity 的雙向反查 UI：                                                                                                        
  1. 前端：chatbot 回覆後，收到 highlighted_node_ids →
     GraphView.tsx 算重心、centerAt、zoomToFit、glow（skill: force-graph-ui）。                                                            
  2. 點任一 node → 右側欄顯示 GET /graph/node/{id}/chunks 的原文片段，                                                                     
     帶 salience 進度條。                                                                                                                  
  3. 每個 chunk 卡片加「📍 跳回文件」按鈕，切到 Data Index tab 並捲到對應文件。                                                            
  4. 新增「Chat about this Concept」按鈕，自動把節點名稱塞進聊天框。                                                                       
  然後最後一次 commit：                                                                                                                    
  gmsg  # 呼叫我們 Milestone 3 的 alias                                                                                                    
  git commit -m "$(gmsg)"                                                                                                                  
  git push                                                                                                                                 
                                                                                                                                           
  ---             
  Part D｜Gemini CLI 課堂速查表（貼在白板）                                                                                                
                                                                                                                                           
  教這幾個招式，學生一輩子受用：
                                                                                                                                           
  ┌───────────────────┬───────────────────────────────────────────────────────────┐
  │       場景        │                           指令                            │                                                        
  ├───────────────────┼───────────────────────────────────────────────────────────┤                                                        
  │ 產 commit message │ git diff --cached | gemini -p "繁中 conventional commit"  │
  ├───────────────────┼───────────────────────────────────────────────────────────┤                                                        
  │ code review       │ git diff main | gemini -p "挑 3 個最嚴重的問題，中文"     │                                                        
  ├───────────────────┼───────────────────────────────────────────────────────────┤                                                        
  │ 讀 log 找 bug     │ tail -100 server.log | gemini -p "找出 error 根因"        │                                                        
  ├───────────────────┼───────────────────────────────────────────────────────────┤                                                        
  │ 產 API doc        │ cat app/main.py | gemini -p "生成 OpenAPI-style markdown" │
  ├───────────────────┼───────────────────────────────────────────────────────────┤                                                        
  │ 課堂 Q&A          │ gemini -p "解釋 chunk_id 為什麼要強綁 Chroma metadata"    │
  └───────────────────┴───────────────────────────────────────────────────────────┘                                                        
                  
  ---                                                                                                                                      
  Part E｜課堂節奏建議（3 小時版）
                                                                                                                                           
  ┌─────────────┬─────────────────────────────────────────────┐
  │    時間     │                    內容                     │                                                                            
  ├─────────────┼─────────────────────────────────────────────┤
  │ 0:00 – 0:15 │ 介紹 Rules / Skills / Workflow 三層心智模型 │
  ├─────────────┼─────────────────────────────────────────────┤
  │ 0:15 – 0:30 │ 建立 .agents/rules.md + 4 個 skills         │                                                                            
  ├─────────────┼─────────────────────────────────────────────┤                                                                            
  │ 0:30 – 1:00 │ Milestone 0–1（Spec + Vector RAG 後端）     │                                                                            
  ├─────────────┼─────────────────────────────────────────────┤                                                                            
  │ 1:00 – 1:30 │ Milestone 2–3（前端 + Gemini CLI commit）   │
  ├─────────────┼─────────────────────────────────────────────┤                                                                            
  │ 1:30 – 1:45 │ 休息 ☕                                     │
  ├─────────────┼─────────────────────────────────────────────┤                                                                            
  │ 1:45 – 2:00 │ Milestone 4（Workflow 自動化）              │
  ├─────────────┼─────────────────────────────────────────────┤                                                                            
  │ 2:00 – 2:30 │ Milestone 5（升級 GraphRAG）最重要          │
  ├─────────────┼─────────────────────────────────────────────┤                                                                            
  │ 2:30 – 2:50 │ Milestone 6–7（雙模式 + 高亮）              │
  ├─────────────┼─────────────────────────────────────────────┤                                                                            
  │ 2:50 – 3:00 │ 兩模式對照 demo + Q&A                       │
  └─────────────┴─────────────────────────────────────────────┘                                                                            
                  
  ---                                                                                                                                      
  關於「Antigravity vs Claude Code」的誠實備註給你自己
                                                                                                                                           
  教學時可以這樣對學生說 —— Antigravity 跟 Claude Code 的核心概念其實一模一樣：
  - Rules = CLAUDE.md / AGENTS.md                                                                                                          
  - Skills = .claude/skills/ 或 Antigravity 的 skill pack                                                                                  
  - Workflow = GitHub Actions 的本地 agent 版                                                                                              
                                                                                                                                           
  學會一套，其他工具 5 分鐘上手。這正是這堂課真正的價值：教的是心智模型，不是特定 IDE。                                                    
                                                                                                                                           
  ---                                                                                                                                      
  需要我接著做哪一項？                                                                                                                     
  1. 把這份腳本存成 docs/teaching/antigravity-graphrag-course.md                                                                           
  2. 把 4 個 skill 檔案真的幫你寫出來（可直接放 .agents/skills/）
  3. 把 Milestone 0–7 的 prompts 拆成 7 張學生講義卡                                                                                       
  4. 準備一份「起始專案骨架」給學生 fork，只留空目錄 + rules 