# WorkshopFlow｜讓三種協作方式交付同一套內訓報名 App

HR 管理三場企業內訓。兩人同時搶最後一席時只能有一人正取；他取消後應按 FIFO 遞補一人。全班做一次 PM 訪談，再由三組用同一份規格與驗收比較交付。本教材沒有預填三組的成績。

## 1. PM 訪談與發放起點

從 repo 根目錄執行 `cd Projects/workshopflow`。需要 Node.js 22.13+（22.x）或 24、npm；本機資料庫用內建 SQLite，無雲端金鑰。安裝依賴需網路；正式使用 Claude Code 另外需要可用的帳號與相應功能。

1. 在 Claude Code 貼 [P1 訪談](prompts/P1-interview.md)，由講師依 [PM 統一回答卡／PRD v1](starter/PRD-v1.md) 回答並凍結需求。
2. 講師閱讀[公平實驗協定](prompts/PROTOCOL.md)，確認相同模型、effort、最多 3 位 worker + 1 位協調人、時限與權限。整理同一份基準，不讓三組各猜一次需求。
3. 對尚不存在的目的地執行（路徑可自選），它會複製三份一樣的 starter、lockfile、fixtures 和 v1 測試；不複製參考解與 CR。**把各自的副本分別交給三組**，不要讓代理以整個教材 repo 為工作目錄。Windows 也可用例如 `node prepare.mjs groups C:/labs/workshop-class-01`。

    node prepare.mjs groups ~/workshop-class-01
    cd ~/workshop-class-01/A-subagents
    npm ci
    npm run build
    npm start

用瀏覽器開 http://127.0.0.1:4100 。此時只有起點頁；尚未實作的規則測試應失敗。B 和 C 改進入自己那組的目錄；若在同一台展示多組，另設 PORT=4101、4102。停止服務按 Ctrl+C；重設目前組別的本機種子用 `npm run reset`。

## 2. 每組在自己的 Claude Code session 操作

先貼 [P2 共同開發任務](prompts/P2-build.md)，再貼 **一種** 模式。從開始規劃、分工到真正跑共同驗收都計入時間。無法使用該功能時記為未執行，不可用一般對話模擬。

| 組別 | 啟動與貼上 | 保留什麼證據 |
|---|---|---|
| A | 正常啟動 `claude`，確認未啟用 Agent Teams，再貼 [A](prompts/A-subagents.md) | 主代理真的呼叫子代理、收到報告與整合驗收 |
| B | 在支援版本啟用 Agent Teams，例如 POSIX shell `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude`，貼 [B](prompts/B-agent-teams.md) | 真實 teammate、任務分工、隊友互傳資訊 |
| C | 核對該環境支援 [Dynamic workflows](https://code.claude.com/docs/en/workflows)，按當前說明啟用並限制最多三個 worker，貼 [C](prompts/C-workflow.md) | 實際腳本、執行紀錄與失敗分支；不能把並行 shell 或普通 subagents 當成 workflow |

核對[官方 Subagents](https://code.claude.com/docs/en/sub-agents)、[Agent Teams](https://code.claude.com/docs/en/agent-teams) 與當天的 runtime。不需要 Agent Board 才能完成 App；若課程另示範看板，依序使用 [M1](prompts/M1-agent-board.md)、[M2](prompts/M2-agent-board-check.md)、[M3](prompts/M3-agent-board-refresh.md)。

## 3. 驗收、發放變更與評分

1. v1 時限到，留存版本與證據（例如各組交一份快照），在各自目錄跑 `npm run build`、`npm test`、`npx playwright install chromium`、`node --test tests/ui.test.mjs`。評分者使用自己的共同測試，不接受參賽組交來的修改版。開發組不應用參考解取代自行開發。
2. 之後才給所有組同一張 [CR-01](prompts/CR-01.md) 與 [增量 API](grading/CR-api.md)：外部員工先審核。把講師提供的 [CR API 測試](grading/cr.test.mjs) 與 [CR 瀏覽器測試](grading/cr-ui.test.mjs) 複製到每個受評專案的 tests/；用 `node --test tests/*.test.mjs` 驗收。v1 與 CR 各階段的時間、修復輪數按協定計；workflow 使用新的執行輸入。
3. 根據 [20 項評分表](grading/RUBRIC.md) 逐項查驗。API 與瀏覽器測試是佐證；另核對來源、決策、版本、真實協作與成本紀錄，不要把測試數量換算成課程分數。填寫[空白比較表](grading/RESULTS.md)。

## 4. 課後參考解：直接跑完成品

從本教材目錄啟動新副本。此例供操作與除錯，**不代表 A/B/C 任一組的真實實驗結果**。

    node prepare.mjs reference ~/workshop-answer-01
    cd ~/workshop-answer-01
    npm ci
    npm run build
    npm start

預設 v1。用 i1、i2 先後報名「最後一席」：i1 正取、i2 候補；在「我的報名」取消 i1，i2 應轉正取。切換 HR 建立場次、調整容量或截止。用外部 e1 報名另一場並存留；按 Ctrl+C，再用同一目錄與同一 DB 執行 `WORKSHOP_PHASE=cr npm start`（PowerShell：`$env:WORKSHOP_PHASE="cr"; npm start`）。e1 的 v1 資料不變；改用 e2 送新申請，只會待審且不占位。HR 核准後再刷新 e2 的「我的報名」。

參考解的 [Express / SQLite 狀態轉換](reference/server/routes.mjs) 與 [四個 React 畫面](reference/src/main.tsx) 以 overlay 疊加同一 starter。SQLite 唯一鍵限制一人一場，寫入與遞補在同一 IMMEDIATE 交易；序號由資料庫產生。v1 和變更版用同一 schema，不重建舊名單。server 只綁 loopback，X-Participant 是課堂模擬，不能作正式登入。服務、資料、瀏覽器都在本機，無金流／Email／外部身分服務。

參考副本的完整驗收：`npx playwright install chromium` 然後 `node --test tests/*.test.mjs`。可改用已安裝 Chrome，例如 macOS：`CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" node --test tests/*.test.mjs`。若只測 API（不算 UI 通過）：`node --test tests/api.test.mjs tests/cr.test.mjs`。
