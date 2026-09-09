# Stock Research AI Team — 多 agent 個股研究團隊

> **學什麼**:用 4 個專業 sub-agent 從不同鏡頭研究同一檔股票,再彙整成一頁研究筆記
> **時長**:90 分鐘
> **產出**:一個跑得動的研究團隊 + 一份 `research-note.md`(含基本面 / 技術面 / 新聞情緒三鏡頭交叉檢核)

> ⚠️ **這是 Claude Code 教學範例,不是投資建議。** 全程只整理「決策需要的事實 + 多空論點 + 不確定性」,不下買 / 賣 / 持有指令。

## 為什麼這個範例存在?

`wafer-detection` 教的是「ML pipeline 天然有階段(資料→標註→訓練→推論),分工很清楚」。
這個範例補上另一種 agent team 的型態:**沒有先後階段,而是同一個對象、多個平行鏡頭**。

個股研究天生適合:基本面看「公司值多少」、技術面看「市場怎麼定價」、新聞看「大家在聊什麼」。
三條鏡頭各自獨立才有意義 —— 它們**彼此打架的地方**,正是一個人很難同時兼顧、而 agent team 不可替代的價值。

## 你會用到的 Claude Code 功能

- [x] sub-agents(4 個,各有獨立 system prompt 與鏡頭)
- [x] 任務路由(CLAUDE.md 把 ticker 自動分派給對的 agent)
- [x] 平行 vs 收斂(前 3 個分頭跑,第 4 個 synthesizer 收斂)
- [ ] (進階)把 4 個 agent 改寫成 4 個 skill —— 見 WALKTHROUGH 末段

## 四個 agent

| Agent | 鏡頭 | 產出 |
|---|---|---|
| `fundamentals-analyst` | 公司體質:估值 / 獲利 / 成長 / 財務健康 | `fundamentals.md` |
| `technicals-analyst` | 價量:趨勢 / 動能 / 支撐壓力 / 量能 | `technicals.md` + `technicals_chart.png` |
| `news-sentiment-analyst` | 市場敘事:近期新聞情緒 + 關鍵事件 | `news.md` |
| `research-synthesizer` | 收斂:三鏡頭交叉檢核,標出一致 / 矛盾訊號 | `research-note.md` |

## 起手式

```bash
cd agent_group_projects/stock-groups-skills
uv sync                       # 安裝 yfinance / pandas / matplotlib / requests
cp .env.example .env          # (可選)填 FINNHUB_API_KEY 拿較完整的新聞
claude                        # 進 Claude Code
```

⚠️ 絕不要把 `.env` commit 進 git(`.gitignore` 已保護)。`yfinance` 不需要 key;只有新聞那一鏡頭裝 key 會更完整。

## 流程(進 Claude Code 後)

1. 跟 Claude 說:`研究 NVDA`(或任何 ticker)
2. Claude 依 CLAUDE.md 路由,先讓 `fundamentals-analyst`、`technicals-analyst`、`news-sentiment-analyst` 各自產出分析
3. 再讓 `research-synthesizer` 把三份彙整成 `research-note.md`
4. 全部輸出落在 `Projects/<ticker>-<YYYY-MM-DD>/`

## 資料夾結構

```
.
├── .claude/agents/        # 4 個 sub-agent
├── _Context/              # 領域知識 + 資料來源 + 輸出範本(必讀,別動)
│   ├── lesson-flow.md         # 90 分鐘課程節奏
│   ├── data-sources.md        # yfinance / Finnhub 欄位與指標公式
│   └── research-note-template.md  # synthesizer 要填的格式
├── scripts/fetch_prices.py    # 抓價量起手腳本(agent 會在這基礎上擴充)
├── Projects/              # 每次研究的輸出(目前空)
├── .env.example           # FINNHUB_API_KEY 範本(可選)
├── pyproject.toml         # uv 管理
├── CLAUDE.md              # Claude Code 自動讀取的專案規則
├── WALKTHROUGH.md         # 講師逐步帶課教案
└── README.md              # 你正在看的這份
```

## 卡住了?

看 [WALKTHROUGH.md](WALKTHROUGH.md) 的「卡點對照表」。常見的是:yfinance 偶爾回 `None`、沒裝 Finnhub key 時新聞偏少、ticker 拼錯抓不到資料。

## 進階閱讀

- 配套教案:[WALKTHROUGH.md](WALKTHROUGH.md)
- 同類但有階段性的 agent team:[`../computer-vision-wafer-detection/`](../computer-vision-wafer-detection/)
- agent team 不可替代性的另一個演練:[`../../Projects/08-agent-team-review/`](../../Projects/08-agent-team-review/)
