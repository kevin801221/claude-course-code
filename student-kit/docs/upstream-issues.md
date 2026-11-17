# 來源已知問題與選用方式

這裡記錄來源本來就有的缺件、版本差異與副作用。完整原碼留在course/；課堂優先使用classroom-fixes/。

## Projects/01-weekly-haiku

- 原碼是 command，不是 Skill；現代 Skill 轉寫應另列 adapted，不能兩份同名同時安裝。

## Projects/02-recipe-genie

- docs/GITHUB_SETUP.md 只是發佈導引，非代理執行必要。

## Projects/03-youtube-notes

- notes/ 與 try/ 是已產生的逐字稿/筆記，可另留一份示例，非 Skill 執行依賴。
- 要標示字幕/影片來源與網路限制，不聲稱離線能抓影片。

## Projects/04-pomodoro

- 根 .claude/settings.json 不存在，原 README 安裝指示缺檔；實際設定在 try/.claude/settings.json。
- 原碼全域寫 ~/.claude/.pomodoro-count、無鎖，非精準25分鐘計時器；不預設啟用。

## Projects/05-organize-downloads

- 來源把 mcpServers 放在 .claude/settings.json，並用 /Users/YOUR_USERNAME/Downloads；需提供現版 .mcp.json 或 claude mcp add 修正版。
- 會讀寫/移動真實 Downloads，課堂應用新建 fixture 目錄先 dry-run。

## Projects/06-discord-dm-bot

- 程式明確 import google.genai，不能標為 Claude Agent SDK 完整範例。
- 會送真實 Discord 訊息；不自動啟用，不帶 token。
- 依賴外部模型/平台與訊息長度/錯誤處理，目前未端到端驗證。

## Projects/07-weekly-reports-skill

- fetch_commits.sh 直接拼 commit subject/body，沒有 JSON escaping。臨時 Git repo 用含雙引號 subject 實測，--output 檔案時 exit0 但不是合法 JSON。應另提供修正版或明確列 known issue。
- PR/issues 路線需要 gh 登入與查詢權限。

## Projects/08-agent-team-review

- 此目錄在 PDF 未被精確點名，屬 Part11 概念延伸，不能混稱簡報同名必做作業。
- 起點是 skeleton：health 能跑，不代表 Kanban CRUD 已完成。

## Projects/09-timetrace

- 來源只有5檔，README明示藍圖就緒、成品待跑；不能宣稱含完成版 Next.js dashboard/agents/hooks/MCP。
- PDF未提 TimeTrace 名稱，應列來源延伸專題。

## Projects/build-gitnexus-skill-commandline

- 不能附帶來源機器的索引作為可用索引；學生需在自己的 Repo 建索引。
- GitNexus CLI 版本敏感，安裝/索引需明確分離於離線教材驗收。

## Projects/plugins-from-zero-to-marketplace

- 原 marketplace.json 位於 root、owner為字串、plugins用path，為舊 schema；目前可用版本需另建 .claude-plugin/marketplace.json。
- 原 hooks 需確認 hooks/hooks.json 註冊方式，不把散落 .sh 自動執行當作已註冊。

## Projects/Normal-RAG2Graph-Project-claude

- 不是 PDF 附錄B指定的 Claude Agent SDK × LangGraph AgenticRAG / CRAG / AdaptiveRAG：兩本 notebook 沒有 langgraph、claude_agent_sdk 或 grade_documents。
- notebooks 有5/4個帶 outputs 的 cells，建議清空 outputs/execution_count 再發行並列 adapted-notebook。
- walkthrough.ipynb 文字提 backend/app/graph_db.py，但來源沒有該檔；應列原文不一致。
- 後端 pyproject 指 Python>=3.13，不能套用根離線練習的 Python3.10 最低版。
- AGENTS.md 宣告 GitNexus 索引；本機 query 回 diverged/partial。純原碼包不能宣稱那份索引隨包可用。
- AI-studio-example/ 是額外 UI 對照，可選收錄，非主 frontend 啟動依賴。

## Projects/llm-wiki-graph

- raw/ 與 wiki Markdown 雖是資料/生成內容，原測試把它們當 fixtures；完整可驗收版本需保留。wiki/graph.html 與 canvas.png 可省略，因為程式會重新生成互動圖。
- 原測試綁定 repo 的raw資料與wiki Markdown fixtures（含檔數23與特定標題/summary）。四份.py單獨跑會失敗；保留tracked fixtures後8/8通過。若縮成純程式碼包，需另重寫成自帶fixtures測試並標adapted。

## agent_group_projects/computer-vision-wafer-detection

- 必須保留下載/資料準備/訓練三個腳本，不只四份agent定義。
- 不附資料集、權重或訓練紀錄；訓練需耗時計算與使用者明確開始。
- 推論 agent 的輸出路徑依學生專案產生，沒有 best.pt 不代表原碼缺件。

## agent_group_projects/computer-vision-wafer-agents-detection-demo

- 不可整個刪 Projects/，其中 scripts/run_inference.py 是原碼；應只排除實驗圖/CSV與結果圖片。
- args.yaml 如留作範例要排除機器特定絕對路徑，或清楚標示歷史設定。

## agent_group_projects/computer-vision-wafer-template

- 此處刻意沒有4份完成agent；不能把空白模板描述成遺失原碼。

## agent_teams/ios-app-flutter-dev

- 兩個版本各101份 tracked file，保留 lib/backend/tests、pubspec.yaml+lock、Android/iOS工程與小型 icons/Assets；這些不是可任意砍掉的大型素材。
- 空白課堂版已有共用Flutter/後端骨架；完成版與起點各自依賴版本不同，不能混檔。
- 不帶backend data運行輸出或真實env。
- 部分過去文件稱冥想App；目前實際規格是arXiv每日報告+呼吸提醒。

## context-engineering-intro

- 不可只留下 PRP.md；generate/execute commands、INITIAL範例、validation與use-cases才是完整練習鏈。
- 保留此子專案自身 LICENSE，不只外層course-code LICENSE。
- use-cases含可執行樣板、資料與框架程式，按manifest區分核心碼/案例資料；圖片大圖可轉來源連結。
- claude-code-full-guide/.devcontainer/init-firewall.sh 會配置網路隔離，僅原碼閱讀，不讓學生在既有系統直接執行。

## context-engineering-intro/use-cases/agent-factory-with-subagents

- 此為Context Engineering延伸用例，不把所需外部依賴當作根包已安裝。

## context-engineering-intro/use-cases/ai-coding-wisc-framework

- 此為Context Engineering延伸用例，不把所需外部依賴當作根包已安裝。

## context-engineering-intro/use-cases/ai-coding-workflows-foundation

- 此為Context Engineering延伸用例，不把所需外部依賴當作根包已安裝。

## context-engineering-intro/use-cases/build-with-agent-team

- 此為Context Engineering延伸用例，不把所需外部依賴當作根包已安裝。

## context-engineering-intro/use-cases/mcp-server

- 此為Context Engineering延伸用例，不把所需外部依賴當作根包已安裝。

## context-engineering-intro/use-cases/pydantic-ai

- 此為Context Engineering延伸用例，不把所需外部依賴當作根包已安裝。

## context-engineering-intro/use-cases/template-generator

- 此為Context Engineering延伸用例，不把所需外部依賴當作根包已安裝。

## 其他來源限制

- PM六個Skill不是完整Matt上游套件；其引用的grill-with-docs/prototype/handoff/implement/code-review仍需另外取得，不能把缺指令當安裝失敗。
- notify-team.sh可能對每次Bash發通知；DevOps是需補npm/Kubernetes/服務位址的模板；全域權限setup腳本會寫HOME，均不預設執行。
- 英文音效範例保留跨平台WAV、略去重複MP3；原Setup音檔大小寫已作可攜路徑處理。
- 英文寬鬆settings/MCP設定保存在settings.source.json、mcp.source.json；根Claude配置在claude-config/，需自行選用。
- Notebook已清除輸出，不表示已在本機跑通。
- Ralph上游根授權為Commercial Terms；PR toolkit來源README標MIT。各自通知保留，整包MIT不覆蓋第三方。

## 原文件本來的占位/缺件連結

來源快照有少量.env.local需自行建立、示意路徑、未附簡報或過時連結。已盡量將作者絕對路徑改為包內路徑，略去截圖改連固定來源；未解項完整列於 [full-manifest](../sources/full-manifest.json) 的original_document_issues，不把它們當成已驗證。

## 來源工具的能力界線

- doc-generator只產生同步get_/post_函式的文件草稿，不是完整OpenAPI。
- metrics/complexity腳本多為regex啟發式，不能當正式靜態分析器。
- 05-mcp套件名與路徑是來源設定模板，未逐個對外連線驗證。
- dependency-check在未安裝scanner時可能仍報passed，實際審計需另核對工具退出碼與結果。
