# arXiv 每日論文閱讀器 App MVP 規格(已凍結 ✅)

> 這份是「規格凍結」的單一真相來源。研究階段結束後,team lead 把研究結論收斂到這裡並**凍結**;
> 之後 teammates 各自照這份做自己的模組,不再邊做邊改。要改規格,回 team lead 對齊全員。
>
> ⚠️ 閱讀疲勞 / 呼吸提醒內容僅供 App 功能設計,不構成醫療建議。

## 一句話定位
後端每天把 5 篇最新 arXiv 科技論文整理成一份可讀的研究報告;你在 iPhone 上讀,讀久了 App 提醒你跟著呼吸動畫休息 60 秒。

## 架構與資料流(切法 A:後端產出成品報告、前端純呈現)
```
[cron 每日 06:00] 後端
  → 抓 arXiv 最新 5 篇(預設 cs.AI / cs.LG / cs.CL,按 submittedDate)
  → 呼叫 Gemini API(gemini-3.5-flash) 整理成 markdown 研究報告
  → 存檔(每日一份、保留歷史)→ FastAPI 提供 GET /reports/today
                        ↓ (前後端契約 = team lead 凍結的共同地基)
[Flutter / iPhone] 拉取報告 → 閱讀畫面 → 閱讀累積 10 分鐘 → 60 秒呼吸動畫 → 回到閱讀
```

## 模組切分 → 對應 Agent team 隊友(目錄不重疊,避免檔案衝突)

| 模組 | 負責隊友 | 擁有的檔案範圍 | 不可碰 |
|---|---|---|---|
| **共用層 + API 契約** | **team lead(主管)** | `lib/shared/`、路由、`pubspec.yaml`、API 契約 | — |
| **A. 後端**(抓取+摘要+API) | teammate `backend-owner` | `backend/` | 其他模組目錄 |
| **B. 報告閱讀** | teammate `reader-owner` | `lib/reader/` | 其他模組目錄 |
| **C. 呼吸提醒** | teammate `breathing-owner` | `lib/breathing/` | 其他模組目錄 |

> 切法刻意讓三個模組**目錄不重疊**,平行開發不會撞檔(對應官方 best practice:「分解工作,使每個隊友擁有不同的檔案集」)。
> 共用層與 API 契約由 team lead 先定好、凍結;隊友要動 shared / 契約 / `pubspec.yaml`,**透過 mailbox 跟 team lead 講**,不自己改。

## 前後端 API 契約(team lead 先定、凍結)
```
GET /reports/today  →  { date, title, markdownBody, papers: [ { title, authors, arxivId, link, summary } ] }
GET /reports        →  歷史報告日期清單(供回看)
GET /reports/{date} →  指定日期的報告(同 /reports/today 結構)
```

## 模組 A:後端(backend-owner)
- 用 **uv 管理的 Python + FastAPI**(禁止 pip)
- 抓取:arXiv API `http://export.arxiv.org/api/query`,`search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL`,
  `sortBy=submittedDate&sortOrder=descending`;**多抓一點(如 `max_results=15`)→ 依 arxivId 去重 → 截最新 5 篇**(一篇掛多分類會重複命中)。
  回傳是 **Atom XML**(非 JSON),用 feedparser 之類解析;**連續呼叫自帶 3 秒間隔、單一連線**(arXiv ToU)。
- 摘要:呼叫 Gemini API(gemini-3.5-flash) 把 5 篇整理成一份 markdown 報告(每篇摘要 + 一段綜述);**API key 只從環境變數 `GEMINI_API_KEY` 讀**
- 儲存:每日一份,保留歷史(本地檔案 / SQLite 皆可,MVP 從簡)
- 排程:cron 或可手動觸發的指令(`uv run` 跑得起來)
- 對外:照上面契約提供 `GET /reports/today`、`GET /reports`、`GET /reports/{date}`

## 模組 B:報告閱讀(reader-owner)
- 用共用層的 `ReportApiClient` 拉今日報告 + 歷史清單
- 報告閱讀畫面:render `markdownBody`、列出 5 篇 papers(標題 / 作者 / arXiv 連結)
- 歷史回看:從 `GET /reports` 選日期看舊報告
- 不直接碰 HTTP / 後端細節,只透過 shared 的 client 介面

## 模組 C:呼吸提醒(breathing-owner)
- 閱讀計時:累積閱讀達門檻(預設 10 分鐘,`AppConfig.readingReminderThreshold`)觸發;門檻**做成可調 / 可關**
- 60 秒呼吸動畫:**Box Breathing 4-4-4-4**(吸 4s → 停 4s → 吐 4s → 停 4s,一輪 16s,做約 4 輪 ≈ 64s);
  圓圈「放大=吸、維持=停、縮小=吐」,做完或略過後回到閱讀並重置計時
- 提示溫和、不強迫(可略過),**不宣稱療效**(實證有限)

## 共用層(lib/shared/,team lead 先定、凍結)
- `Report` / `Paper` 資料模型(對應上面契約,JSON 可序列化)
- `ReportApiClient`:呼叫後端的介面(`today` / `list` / `byDate`)
- 首頁路由 + 後端 base URL 設定
- `backend/` 骨架(uv 專案 + `.env.example` 放 `GEMINI_API_KEY` 佔位)

## 明確不做(MVP 邊界)
- 不做帳號 / 雲端同步;每日報告全使用者共用、非個人化
- 不做付費 / 訂閱、不做社群分享、不做推播(MVP 用 app 內計時提醒)
- 不接任何第三方分析 SDK;不把 API key 放進前端或 commit 進 repo

## 研究結論(researcher 收斂、team lead 凍結 ✅ — 完整依據見 `_Context/research-findings.md`)
- **arXiv 領域與排序**:預設 `cat:cs.AI OR cat:cs.LG OR cat:cs.CL`(可選擴 `cs.CV / cs.RO`);
  排序 `sortBy=submittedDate&sortOrder=descending`(要「今天剛投稿」用 submittedDate,非 lastUpdatedDate)。
  一篇可掛多分類會重複命中 → **多抓一點(如 `max_results=15`)後依 arxivId 去重,再截最新 5 篇**。
  依據:arXiv API User's Manual / Category Taxonomy(查證 2026-05-22)。
- **取用速率**:arXiv ToU 要求**每 3 秒最多 1 次請求、單一連線** → backend 連續呼叫自帶 3 秒間隔。依據:arXiv ToU(2026-05-22)。
- **閱讀提醒間隔**:預設 **10 分鐘**合理(介於 20-20-20 法則與「每小時休息 5 分鐘」之間),
  但**實證有限 / 仍有爭議** → **不宣稱療效、文案中性、門檻做成可調 / 可關**。依據:AAO/AOA 對 20-20-20 說明 + 質疑其實證的近期研究(2026-05-22)。
- **呼吸動畫節奏**:**Box Breathing 4-4-4-4**(吸 4s → 停 4s → 吐 4s → 停 4s,一輪 16s),做 **約 4 輪 ≈ 64s** 對齊 60 秒動畫;
  圓圈「放大=吸、維持=停、縮小=吐」,溫和可略過、不宣稱療效。依據:Box Breathing vs 4-7-8 比較資料(2026-05-22)。
- **設計紅線(全員)**:**不做**無限滑 / 紅點 badge 焦慮 / 罪惡感推播 confirmshaming / 自動播放與個人化無限餵食(暗黑模式);
  每日**固定 5 篇、有明確結尾、非個人化、無未讀數字**,讀完就是讀完。依據:dark patterns 文獻 + 歐盟對成癮性設計監管動向(2026-05-22)。

## 驗收
```bash
# 後端(在 backend/)
uv run <啟動指令>          # FastAPI 起得來
curl .../reports/today      # 回得到當天報告(papers 5 篇 + markdownBody)

# 前端(在 app 根目錄)
flutter analyze            # 0 error
flutter test               # 綠
flutter run                # 能讀報告、計時到門檻跳呼吸動畫、做完回到閱讀
```
