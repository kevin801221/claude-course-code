# Stock Research AI Team — 講師 Walkthrough

> **對象**:用過 Claude Code、想學「多 agent 平行協作」的人(不需要金融背景)
> **形式**:講師現場帶 / 自學皆可
> **時長**:90 分鐘
> **產出**:一個 4-agent 研究團隊跑通,產出一頁 `research-note.md`,並親眼看到「三鏡頭打架」如何被攤開
> **核心方法**:用同一個對象(一檔股票)、多個獨立鏡頭,讓學生體會 agent team 的不可替代性
>
> ⚠️ 全程是 Claude Code 教學範例,**不是投資建議**。不下買 / 賣 / 持有結論。

---

## 開場(5 分鐘):為什麼不用一個全能 agent?

學生最直覺的想法是:「叫 Claude 研究這檔股票」一句就好,幹嘛拆 4 個?

| 一個全能 agent | 4 個專業 agent |
|---|---|
| 三件事擠在一個 context,容易顧此失彼 | 每個鏡頭 context 乾淨,分析更深 |
| 結論常被最後讀到的資訊帶風向 | 三鏡頭獨立產出,彙整時才碰頭 |
| 矛盾被「喬成一致」藏起來 | 矛盾被攤開 —— 這正是價值所在 |

> **教學金句**:「一個人很難同時當基本面、技術面、新聞面三種專家;agent team 的價值不是更快,是**讓三種鏡頭互相打臉**。」

這跟 `wafer-detection` 的差別也講清楚:wafer 是**有先後階段**的 pipeline(資料→標註→訓練→推論);這裡是**沒有先後、平行的鏡頭**,最後才收斂。兩種都是 agent team,型態不同。

---

## 📁 檔案結構(先讓學生看地圖)

```
stock-groups-skills/
├── .claude/agents/
│   ├── fundamentals-analyst.md      # 鏡頭 1:公司體質
│   ├── technicals-analyst.md        # 鏡頭 2:價量
│   ├── news-sentiment-analyst.md    # 鏡頭 3:市場敘事
│   └── research-synthesizer.md      # 收斂:交叉檢核
├── _Context/
│   ├── data-sources.md              # 去哪抓、欄位、公式
│   └── research-note-template.md    # synthesizer 要填的格式
├── scripts/fetch_prices.py          # 抓價量起手腳本
├── Projects/<ticker>-<date>/        # 每次研究的輸出
└── CLAUDE.md                        # 任務路由 + 免責規則
```

> **教學金句**:「`.claude/agents/` 是團隊名冊,`_Context/` 是給新人的工作手冊,CLAUDE.md 是櫃台的派工規則。」

---

## Phase 0:環境準備(10 分鐘)

**檢查清單貼黑板**:

```bash
node --version          # 18+
claude --version        # 有 Claude Code
uv --version            # 有 uv

cd agent_group_projects/stock-groups-skills
uv sync                 # 裝 yfinance / pandas / matplotlib / requests
cp .env.example .env    # 可選:填 FINNHUB_API_KEY 拿較完整新聞
```

💡 `yfinance` 不用 key,所以**沒填 Finnhub 也能完整跑前兩個鏡頭**。新聞鏡頭沒 key 會自動降級(用 yfinance 的 `Ticker.news`)。先讓所有人不卡 key 就開跑。

先單獨驗一下資料管道通不通:

```bash
uv run python scripts/fetch_prices.py NVDA
```

看到最近 5 天的收盤 + 均線 + RSI,代表資料管道沒問題,可以進場。

---

## Phase 1:第一個 agent ⭐ 最詳細(30 分鐘)

進 Claude Code:

```bash
claude
```

打開 `.claude/agents/fundamentals-analyst.md`,**逐段講 frontmatter**:

- `name` / `description` —— description 寫得好,Claude 才會在「該用它的時候」自動路由過來。這裡刻意寫「公司值多少、賺不賺錢這條鏡頭」,就是給路由用的線索。
- `tools` —— 給了 Bash 是因為它要自己寫 Python 抓 yfinance。
- system prompt 第一句「**只看公司本身的體質,不看線型、不看新聞**」—— 這就是鏡頭隔離。

跑第一檔:

```
研究 NVDA 的基本面
```

Claude 會委派 `fundamentals-analyst`,它會:讀 `_Context/data-sources.md` → 寫腳本抓 `Ticker.info` 與三大表 → 算估值/獲利/成長/財務健康 → 輸出 `Projects/NVDA-<date>/fundamentals.md`。

> **教學金句**:「鏡頭隔離不是限制,是紀律 —— 你不准它偷看新聞,它的基本面結論才不會被新聞情緒污染,等下交叉檢核才有意義。」

**現場故意踩坑**:用拼錯的 `NVDDA`。看 agent 怎麼把抓不到的欄位標成「N/A(資料缺漏)」而不是填 0 或瞎掰。這一刻學生會記住「誠實標缺漏」的設計。

---

## Phase 2:另外兩個鏡頭(20 分鐘,加速)

同樣節奏,但讓學生自己讀 agent 檔、自己下指令:

```
跑 NVDA 的技術面
跑 NVDA 的新聞情緒
```

- `technicals-analyst`:抓日線 → 算 MA/RSI/MACD/布林 → 畫 `technicals_chart.png` → 寫 `technicals.md`。
- `news-sentiment-analyst`:有 Finnhub key 抓 company-news,沒 key 降級用 `Ticker.news` → 標情緒分布 + 關鍵事件 → 寫 `news.md`。

💡 重點不是指標公式多漂亮,是**三個 agent 各跑各的、互不知道對方結論**。到這裡 `Projects/NVDA-<date>/` 應該有三份獨立分析。

---

## Phase 3:收斂 ⭐(20 分鐘)

```
把 NVDA 三份分析彙整成研究筆記
```

`research-synthesizer` 上場 —— 它**不抓新資料**,只讀三份 `.md`,照 `research-note-template.md` 填出 `research-note.md`。

帶學生**只看一欄**:「彼此矛盾的訊號」。

範例對話(實際數字會變,重點是型態):
> 基本面說「估值已經偏貴」、技術面說「多頭排列、動能仍強」、新聞說「法說後分析師上修」。
> synthesizer 不會喬成「所以買」,而是攤開:**貴但有動能 + 敘事支撐,偏多的人賭成長兌現、偏空的人賭估值回歸。**

> **教學金句**:「synthesizer 最大的本事不是『給答案』,是『不把矛盾藏起來』。把矛盾攤平,決策還給人。」

**現場故意踩坑**:直接問 Claude「那我到底該不該買?」。看它如何把問題轉成「若你重視 X 偏多、若你擔心 Y 偏空」,而不是下指令。藉此講免責設計與「不給投資建議」的邊界。

---

## 整合 demo:一條龍跑完(收尾用)

一句話跑完整團隊:

```
研究 TSM,從基本面、技術面、新聞情緒到彙整,全部跑完
```

看 Claude 自動依 CLAUDE.md 路由:三鏡頭分頭跑 → synthesizer 收斂 → `Projects/TSM-<date>/` 一次到位五個檔。

---

## 常見問題 / FAQ

1. **沒有 Finnhub key 能上課嗎?** 能。前兩個鏡頭完全不需要 key,新聞鏡頭自動降級。
2. **yfinance 抓回 None 怎麼辦?** 正常,它不穩。agent 已被要求標「資料缺漏」,不要當 0。
3. **這會給我買賣建議嗎?** 不會,也不該。這是教 agent 協作的範例,輸出刻意停在「事實 + 多空論點」。
4. **跟 sub-agent 章節的差別?** 這裡示範的就是 sub-agent,但重點放在「多個平行鏡頭 + 一個收斂者」這種團隊型態。
5. **能不能改成台股 / 加密貨幣?** 能,換 ticker 即可(台股用 `2330.TW` 之類);新聞來源可能要換,改 `_Context/data-sources.md`。

---

## 卡點對照表 ⭐

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `uv sync` 卡在編譯 | 某些環境 yfinance 依賴要編 | 先 `uv sync`,真不行退而 `uv add yfinance pandas matplotlib requests` 逐個裝 |
| ticker 抓不到任何資料 | 拼錯 / 非美股要加後綴 | 台股 `2330.TW`、港股 `0700.HK`;先用 `scripts/fetch_prices.py` 驗 |
| 新聞一片空 | 沒 Finnhub key + 該股 yfinance 新聞少 | 屬正常,news agent 會標「新聞樣本不足」;要完整就填 key |
| Claude 不自動路由到對的 agent | description 線索不夠 / 指令太籠統 | 指令講清楚鏡頭(「跑基本面」),或檢查 agent 的 description |
| MA200 一片 NaN | 抓的天數不到 200 | 正常,agent 會標「樣本不足」;要 MA200 就拉長 period |
| synthesizer 自己編了三份裡沒有的數字 | 它越權當資料來源了 | 提醒它「只收斂、不引入新數字」,這是它的紀律(已寫在 agent 檔) |

---

## 講師私房筆記

- **時間分配**:Phase 1 一定要慢(30 分),把 frontmatter 跟鏡頭隔離講透;Phase 2 可以飛(學生已會)。Phase 3 留足 20 分,因為「看矛盾」是這堂課的高潮。
- **故意踩坑比口頭講有效**:拼錯 ticker(看誠實標缺漏)、問「該不該買」(看免責邊界)這兩個現場演,印象最深。
- **不同角色推薦**:給工程師看 → 強調 context 隔離與路由;給 PM / 一般人看 → 強調「三鏡頭打架」這個產品價值,弱化程式碼。
- **真實狀況**:yfinance 在不同日子穩定度不一,開課前一天先跑一遍當天要 demo 的 ticker,確認資料拿得到。Finnhub 免費層有 rate limit,一班人同時打可能被限,建議講師自己一個 key demo,學生看降級版即可。
- **接點**:結尾花 5 分鐘講「這 4 個 agent 也能改寫成 4 個 skill」,順勢接到 PPT 的 Skills 章節 —— agent 是「派一個分身去做」,skill 是「把做法打包成可重用能力」,同一批邏輯兩種包裝。

---

## 一句話總結

> **這堂課不是教你分析股票,是教你用 4 個獨立鏡頭 + 1 個收斂者,讓 agent team 把「矛盾」攤開 —— 矛盾,就是團隊不可替代的價值。**

---

## 進階閱讀

- 🔗 同 repo 有階段性的 agent team:[`../computer-vision-wafer-detection/WALKTHROUGH.md`](../computer-vision-wafer-detection/WALKTHROUGH.md)
- 🔗 agent team 不可替代性(盲評一致性):[`../../Projects/08-agent-team-review/`](../../Projects/08-agent-team-review/)
- 🔗 配套課程教案:[`../../docs/walkthroughs/agent_team_walkthrough.md`](../../docs/walkthroughs/agent_team_walkthrough.md)

---

_Last updated: 2026-05-22_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材(同目錄):README.md、_Context/lesson-flow.md、_Context/data-sources.md_
