# arXiv 每日論文閱讀器 App — 原生 Agent teams 團隊規則

用 Claude Code 原生的 **Agent teams**(實驗功能)協調一個 team lead + researcher + 三個模組隊友,
端到端蓋出一個「arXiv 每日論文閱讀器 + 呼吸提醒」App MVP 的工作區。**重點是 Agent teams 工作流,不是 arXiv 領域知識,也不是 git worktree。**

> 這是教學素材:逐步腳本看 `agent-team-playbook.md`,帶課看 `arxiv-2-空白課堂版/WALKTHROUGH.md`。
> 兩個版本(`arxiv-1-完成版/` 彩排、`arxiv-2-空白課堂版/` 上課)都是**人類自己開 Agent team 來蓋**,不是請 AI 代為做好。

## 要蓋的 App
後端每天抓 arXiv 最新 5 篇科技論文、用 Gemini API(gemini-3.5-flash)整理成一份研究報告;
使用者在 iPhone 上讀,閱讀累積到門檻就跳 60 秒呼吸動畫提醒休息。

## 目標
研究先行 → 凍結規格與 API 契約 → team lead 定共用層 → 三個隊友平行開發 → 整合驗收 → 清理 team。

## 你現在是什麼角色?
- 你開的這個 session = **team lead(主管)**:建 team、收斂研究、凍結規格與契約、定 `lib/shared/`、整合驗收、清理。
- 被生成的 **researcher / backend-owner / reader-owner / breathing-owner** = 隊友,各只做自己那份(見 `_Context/team-roles.md`)。

## 鐵則(Agent teams 紀律)
1. **規格沒凍結,不准 spawn 開發隊友。** 研究 → 收斂進 `_Context/app-spec.md` → 凍結 → 才平行。
2. **共用層與 API 契約只有 team lead 能改。** 隊友要動 `lib/shared/`、`pubspec.yaml` 或契約,先用 **mailbox** 問 team lead、等批准。
3. **每個隊友只碰自己的目錄**(`backend/`、`lib/reader/`、`lib/breathing/`),跨模組需求走 mailbox,不跑去改別人的檔案。
4. **清理由 team lead 做**:先請所有隊友 shut down,再 clean up the team(有隊友在跑會清理失敗)。

## 技術規則
- 後端:Python,**一律用 uv 管理套件(禁止 pip)**,FastAPI;抓 arXiv API + 呼叫 Gemini API
- 前端:Flutter / Dart;狀態管理用內建 `setState`(MVP 不過度工程,不引入 provider/bloc)
- 前後端靠 team lead 凍結的 **API 契約**對接(`GET /reports/today` 等)
- Gemini API key **只從環境變數讀**(`GEMINI_API_KEY`),`.env` 進 `.gitignore`,repo 只留 `.env.example`
- 不要硬編碼絕對路徑
- commit 訊息用繁體中文、Kevin 風格、不署名工具、無 emoji
- 回應使用繁體中文,技術術語(team lead, teammate, mailbox, task list, Flutter, FastAPI, widget)保留英文

## 啟用
- Agent teams 是實驗功能,需 Claude Code v2.1.32+ 並開 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`。

## 健康內容免責
- 閱讀疲勞 / 呼吸提醒內容僅供 App 功能設計,**不是醫療或心理治療建議**;不宣稱療效;研究引用標來源。

## 不要做的事
- 不要在研究階段就寫程式碼(順序錯了)
- 不要邊開發邊改已凍結的 app-spec 或 API 契約(要改先回 team lead 對齊全員)
- 不要讓隊友自己改 `lib/shared/` 或 API 契約(共同地基只有 team lead 改)
- 不要 commit 任何 secret(尤其 `GEMINI_API_KEY`)/ signing key
