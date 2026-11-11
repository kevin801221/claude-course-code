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
  → 呼叫 Gemini API(gemini-3.5-flash)整理成 markdown 研究報告
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
- 抓取:arXiv API `http://export.arxiv.org/api/query`,`search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.CV`,
  `sortBy=submittedDate&sortOrder=descending&max_results=5`,加 `User-Agent: arxiv-reader-app/1.0`、多次呼叫間隔 ≥ 3 秒(領域與排序見研究結論)
- 摘要:呼叫 Gemini API(gemini-3.5-flash)把 5 篇整理成一份 markdown 報告(每篇摘要 + 一段綜述);**API key 只從環境變數讀**
- 儲存:每日一份,保留歷史(本地檔案 / SQLite 皆可,MVP 從簡)
- 排程:cron 或可手動觸發的指令(`uv run` 跑得起來)
- 對外:照上面契約提供 `GET /reports/today`、`GET /reports`、`GET /reports/{date}`

## 模組 B:報告閱讀(reader-owner)
- 用共用層的 `ReportApiClient` 拉今日報告 + 歷史清單
- 報告閱讀畫面:render `markdownBody`、列出 5 篇 papers(標題 / 作者 / arXiv 連結)
- 歷史回看:從 `GET /reports` 選日期看舊報告
- 不直接碰 HTTP / 後端細節,只透過 shared 的 client 介面

## 模組 C:呼吸提醒(breathing-owner)
- 閱讀計時:累積閱讀達門檻(**預設 20 分鐘**,見研究結論)觸發;門檻與 demo 短門檻從 `lib/shared/` 常數讀
- 60 秒呼吸動畫:Box Breathing 4-4-4-4(吸 4→屏 4→呼 4→屏 4)× 3 輪,跟著圓圈縮放,做完回到閱讀
- 提示溫和、不強迫(可略過),不宣稱療效

## 共用層(lib/shared/,team lead 先定、凍結)
- `Report` / `Paper` 資料模型(對應上面契約,JSON 可序列化)
- `ReportApiClient`:呼叫後端的介面(`today` / `list` / `byDate`)
- 首頁路由 + 後端 base URL 設定
- `backend/` 骨架(uv 專案 + `.env.example` 放 `GEMINI_API_KEY` 佔位)

## 明確不做(MVP 邊界)
- 不做帳號 / 雲端同步;每日報告全使用者共用、非個人化
- 不做付費 / 訂閱、不做社群分享、不做推播(MVP 用 app 內計時提醒)
- 不接任何第三方分析 SDK;不把 API key 放進前端或 commit 進 repo

## 研究結論(researcher 收斂後填,team lead 已凍結 ✅)

> 來源完整版見 `_Context/research-findings.md`(每條標來源 + 依據強度)。以下為 team lead 拍板、凍結後三模組共用的預設值。
> ⚠️ 與健康相關設定僅供 App 功能設計,非醫療建議。

- **arXiv 領域**:`cs.AI OR cs.LG OR cs.CL OR cs.CV`(4 類;原 3 類加 cs.CV,涵蓋影像/生成;stat.ML 已 cross-list 進 cs.LG 不另加)。依據:arXiv Category Taxonomy(官方)。
- **排序**:`sortBy=submittedDate&sortOrder=descending`(抓「最新投稿」非「最近修訂」),`max_results=5`。依據:arXiv API User's Manual(官方)。
- **禮貌間隔**:多次呼叫之間 ≥ 3 秒,加 `User-Agent: arxiv-reader-app/1.0`,HTTP 503 走 exponential backoff。依據:arXiv API 官方規範。
- **閱讀提醒間隔**:**預設 20 分鐘**(對齊 20-20-20 法則,比 10 分鐘更有文獻依據),可調 10 / 20 / 30 分鐘。另設 `demo` 短門檻供現場 `flutter run` 快速觸發。依據:AAO 20-20-20、ScienceDirect 2025。
- **呼吸節奏**:**Box Breathing 4-4-4-4**(吸 4→屏 4→呼 4→屏 4,一輪 16 秒)× **3 輪** = 48 秒動畫 + 約 12 秒引導文字,湊滿 60 秒。依據:PubMed 2025 對照研究。
- **設計紅線(全員)**:禁無限滑(固定 5 篇有頂有底)、禁紅點 badge 計數、禁罪惡感/streak 推播、禁自動播下一篇。依據:Weizenbaum Journal 2023、CEUR-WS 2024 等。

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
