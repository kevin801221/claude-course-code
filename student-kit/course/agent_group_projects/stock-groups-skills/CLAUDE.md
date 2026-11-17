# Stock Research AI Team — 多 agent 個股研究團隊

個股研究自動化工作區:同一檔股票,4 個專業 agent 用不同視角分頭研究,再彙整成一頁研究筆記。

## 目標
從一個股票代號(ticker)自動完成:基本面 → 技術面 → 新聞情緒 → 彙整成研究筆記。
重點不是「給投資建議」,是教 **agent team 的不可替代性**:每個 agent 帶不同鏡頭,彼此交叉檢核。

## 資料夾
- `_Context/` — 領域知識與資料來源說明(必讀)
- `.claude/agents/` — 4 個 sub-agent
- `Projects/` — 每次研究的輸出(研究筆記 + 圖表)
- `scripts/` — 共用起手腳本(agent 會在這基礎上擴充)

## 任務路由
- 抓財報 / 估值 / 成長 → `fundamentals-analyst`
- 抓價量 / 算技術指標 / 畫圖 → `technicals-analyst`
- 抓近期新聞 / 判讀情緒 → `news-sentiment-analyst`
- 把三份分析彙整成一頁研究筆記 → `research-synthesizer`

預設委派 sub-agent。使用者只給一個 ticker 時,先依序跑前三個分析師,最後交給 synthesizer。

## 規則
- Python 套件用 `uv` 管理(不用 pip)
- 所有路徑用 `pathlib.Path`,不要硬編碼
- 資料來源優先用 `yfinance`(免 API key);新聞用 Finnhub(`FINNHUB_API_KEY` 從 `.env` 載入,可選)
- 每檔研究輸出到 `Projects/<ticker>-<YYYY-MM-DD>/`
- 回應使用繁體中文,技術術語保留英文
- 抓不到資料時明說「資料缺漏」,不要捏造數字

## 重要免責(每份輸出都要帶)
- 這是 **Claude Code 教學範例,不是投資建議**。
- 不下「買 / 賣 / 持有」的明確指令;只整理「決策需要的事實 + 多空論點 + 不確定性」。
- 數字一律標來源與抓取日期。資料有時間差,過期就標註。

## 不要做的事
- 不要動 `_Context/` 的內容(那是教學素材)
- 不要 hardcode API key(用 `.env`)
- 不要把 `Projects/` 的歷史輸出當成最新事實沿用,每次重抓
