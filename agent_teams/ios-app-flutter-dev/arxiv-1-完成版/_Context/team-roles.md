# Agent team 分工與 mailbox 規則

> Agent teams 的隊友各自獨立、各有 context,靠**共享 task list** 看進度、靠 **mailbox** 互傳訊息對齊。
> 這份定義誰是誰、誰擁有哪些檔案、什麼時候該發 mailbox。team lead 生成隊友時把這份規則講給他們。

## 角色

| 角色 | 是誰 | 擁有的檔案範圍 | 職責 |
|---|---|---|---|
| **team lead(主管)** | 你開的那個 session | `lib/shared/`、路由、`pubspec.yaml`、API 契約 | 建 team、研究收斂、凍結規格與契約、定共用層、整合驗收、清理 |
| **researcher** | 隊友 | `_Context/research-findings.md` | 研究先行,查功能設計依據(見 research-intake.md) |
| **backend-owner** | 隊友 | `backend/` | 後端:arXiv 抓取 + Gemini 摘要 + cron + FastAPI |
| **reader-owner** | 隊友 | `lib/reader/` | 報告閱讀畫面 + 歷史回看 |
| **breathing-owner** | 隊友 | `lib/breathing/` | 閱讀計時 + 60 秒呼吸動畫 |

> 切法刻意讓三個模組**目錄不重疊**(官方 best practice:「分解工作,使每個隊友擁有不同的檔案集」),平行才不撞檔。
> 這題刻意橫跨後端(Python)+ 前端(Flutter),示範 Agent teams 不限單一技術棧 —— 兩棧靠 team lead 凍結的 API 契約對接。

## mailbox 規則(什麼時候該喊話)

1. **要動 `lib/shared/`、`pubspec.yaml` 或 API 契約** → 不准自己改,發 mailbox 給 team lead,等同意。共用層與契約是共同地基,只能 team lead 改。
2. **需要 shared / 契約的細節**(Report 欄位、ReportApiClient 介面、API path)→ 直接發 mailbox 問 team lead,不要自己猜。
3. **跨模組依賴**(例:breathing 想知道閱讀計時誰觸發、reader 想知道後端回傳欄位)→ 透過 team lead 確認介面,不要跑去改對方目錄。
4. **完成自己模組** → 標 task 完成 + 通知 team lead(隊友閒置會自動通知,但講清楚做了什麼更好)。

## 階段閘門(不可跳)

1. **研究閘門**:researcher 的 findings 寫完 → team lead 收斂進 app-spec → **凍結**。
2. **契約 / 共用層閘門**:team lead 先把 API 契約 + `lib/shared/` 定好 → 才 spawn 三個開發隊友。
3. **開發閘門**:每個隊友自己模組驗收通過(後端:`GET /reports/today` 回得到報告;前端:`flutter analyze` 0 error + 測試綠)→ 才算完成 → team lead 整合驗收。

> **教學金句**:「閘門就是 Agent teams 版的『先對齊再開工』—— 隊友能用 mailbox 喊話,但共同地基(尤其跨技術棧的 API 契約)還是要 team lead 先定死,不然後端跟前端各做各的對不起來。」

## 計畫批准(plan approval)

要動 shared / API 契約這種有風險的事,叫隊友**先提計畫、等 team lead 批准**再動手(team lead 可在生成時要求 require plan approval)。

## 安全紅線

- Gemini API key **只從環境變數讀**,`.env` 進 `.gitignore`,repo 只留 `.env.example`。
- 任何隊友都不准把 key 寫進程式碼或 commit 進 repo。

## 收尾

整合驗收過 → 請所有隊友 shut down → team lead 執行 clean up the team(隊友還在跑會清理失敗)。
