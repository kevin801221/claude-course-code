# Agent Team Playbook — 用原生 Agent teams 蓋「arXiv 每日論文閱讀器」

> 這份是**可以直接貼上執行的逐步腳本**。你在一個**全新的 Claude Code session** 裡,開啟原生 Agent teams 功能,
> 讓一個 team lead 協調研究員 + 三個模組隊友,平行把 `_Context/app-spec.md` 描述的 App 蓋出來。
>
> **要蓋的 App**:後端每天抓 arXiv 最新 5 篇科技論文、用 gemini-3.5-flash 整理成一份研究報告;
> 使用者在 iPhone 上讀,閱讀累積到門檻就跳 60 秒呼吸動畫提醒休息。
>
> 完成版(`arxiv-1-完成版/`):上課前你自己照這份跑一次,做出一個成功的成品當底氣。
> 空白課堂版(`arxiv-2-空白課堂版/`):上課現場照同一份,從乾淨狀態帶學生做。
>
> ⚠️ 重點是 **Agent teams 工作流**,不是 arXiv 領域知識,也不是 git worktree。
> 健康免責:閱讀疲勞 / 呼吸提醒僅供 App 功能設計,**不是醫療建議**。

---

## 為什麼是 Agent teams,不是 sub-agent / worktree

| | sub-agent | git worktree | **原生 Agent teams(這份)** |
|---|---|---|---|
| 隊友是什麼 | 主對話的分身 | 你手動開的多個 claude | team lead 生成的獨立 Claude Code 實例 |
| 怎麼溝通 | 只回報主對話 | git merge 才碰頭 | **共享 task list + mailbox 直接互傳** |
| 你怎麼開 | 程式自動派 | 自己開終端 + git 指令 | 用自然語言叫 team lead 開 |

關鍵差別:Agent teams 的隊友**彼此能直接喊話**(例如 reader-owner 問 team lead「報告 API 回傳的欄位長怎樣?」),而且大家看同一張 task list。

> **教學金句**:「這個 App 剛好橫跨後端(Python)+ 前端(Flutter),正好示範 Agent teams 怎麼讓『不同技術棧的隊友』靠一條 API 契約平行幹活。」

---

## 📁 要蓋成什麼(資料流一眼看懂)

```
[cron 每日 06:00]
  後端(uv 管理的 Python)
    → 抓 arXiv 最新 5 篇(預設 cs.AI / cs.LG / cs.CL,按提交日期)
    → 呼叫 Gemini API 整理成 markdown 研究報告
    → 存檔(每日一份、保留歷史)
    → FastAPI 提供  GET /reports/today
                                  │
                                  ▼  (前後端契約 = team lead 凍結的共同地基)
  前端(Flutter / iPhone)
    → 拉取報告 → 報告閱讀畫面(可回看歷史)
    → 閱讀計時:累積 10 分鐘 → 跳 60 秒呼吸動畫 → 做完回到閱讀
```

模組切分(刻意讓**目錄不重疊**,平行才不撞檔):

| 模組 | 隊友 | 擁有的檔案範圍 | 不可碰 |
|---|---|---|---|
| **共用層 + 前後端契約** | **team lead(主管)** | `lib/shared/`、路由、`pubspec.yaml`、API 契約 | — |
| **A. 後端**(抓取+摘要+API) | `backend-owner` | `backend/`(uv Python:arXiv 抓取、Gemini 摘要、cron、FastAPI) | 其他模組目錄 |
| **B. 報告閱讀** | `reader-owner` | `lib/reader/`(報告列表 + 閱讀畫面 + 歷史回看) | 其他模組目錄 |
| **C. 呼吸提醒** | `breathing-owner` | `lib/breathing/`(閱讀計時 + 60 秒呼吸動畫) | 其他模組目錄 |

---

## Step 0 — 啟用功能 + 開新 session(5 分鐘)

Agent teams 是**實驗功能,預設關閉**,需要 Claude Code **v2.1.32+**。

1. 確認版本:
   ```bash
   claude --version    # 要 >= 2.1.32
   ```
2. 開旗標 —— 二選一:
   - **settings.json**(`~/.claude/settings.json` 或專案 `.claude/settings.json`):
     ```json
     { "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
     ```
   - **環境變數**:
     ```bash
     export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
     ```
3. 進到要做的版本資料夾,開一個**乾淨的 claude**(這個 session 就是 team lead):
   ```bash
   cd agent_teams/ios-app-flutter-dev/arxiv-1-完成版   # 或 arxiv-2-空白課堂版
   claude
   ```
4. (可選)顯示模式:預設 `in-process`(隊友在同一個終端,Shift+Down 輪流切換)。
   想要每個隊友一個分割視窗 → 需要 tmux 或 iTerm2,在 `~/.claude/settings.json` 設 `"teammateMode": "tmux"`。

> 💡 旗標**只在 claude 啟動時讀**。你在已開的 session 裡才寫 settings.json,要**重開** claude 才生效。
> 旗標沒開,你叫它建 team 它只會用一般 sub-agent 替代,看不到 task list 與 mailbox。確認開了再開始。

---

## Step 1 — 開 team + 研究先行 ⭐(貼這段)

研究先行是 Agent teams 的強項之一(「多個隊友同時調查不同面向」)。先派一個研究員把功能設計依據查清楚,再進開發。貼給 team lead:

```text
建立一個 agent team,目標是把 _Context/app-spec.md 描述的「arXiv 每日論文閱讀器 + 呼吸提醒」App 蓋出來。
先不要寫任何程式碼。

第一步:spawn 一個叫 researcher 的隊友,任務是調查這個 App 的功能設計依據:
1. arXiv 該抓哪些領域分類(cs.AI / cs.LG / cs.CL 之外還有沒有更該收的)、用哪個 API 端點、
   「最新 5 篇」怎麼排序(submittedDate vs lastUpdatedDate)、有沒有取用速率限制要注意
2. 閱讀疲勞與休息間隔的依據:累積閱讀幾分鐘提醒一次合理、深呼吸動畫的吸/吐節奏多少秒
3. 每日論文摘要這類「資訊餵食」App 不該用的「成長駭客」做法(無限滑、紅點焦慮、罪惡感推播)

把結論寫進 _Context/research-findings.md,每個結論標來源,並標明「僅供 App 功能設計、非醫療建議」。
researcher 完成後通知我,先不要進入開發。
```

現場觀察點:你會看到 task list 出現、researcher 開始跑;完成後它會自動通知 team lead(你不用一直問)。

---

## Step 2 — 凍結規格 + team lead 定共用層與契約(貼這段)

```text
把 researcher 的 findings 收斂進 _Context/app-spec.md 對應欄位(arXiv 領域與排序、閱讀提醒間隔、呼吸節奏),
然後宣布「規格凍結」——之後平行開發不再改規格。

接著由你(team lead)親自做共用層,先不要 spawn 開發隊友:
1. 在這個資料夾用 flutter create 出專案骨架(專案名 arxiv_reader)
2. 凍結前後端 API 契約,寫進 lib/shared/(或 _Context/api-contract.md):
   GET /reports/today  →  { date, title, markdownBody, papers: [{ title, authors, arxivId, link, summary }] }
   GET /reports        →  歷史報告清單(date 列表)
3. 定好 lib/shared/:Report / Paper 的 Dart 資料模型(對應上面契約)、ReportApiClient 介面、首頁路由
4. 建 backend/ 空骨架:uv 專案(uv init / pyproject.toml)、.env.example(放 GEMINI_API_KEY 佔位,不放真 key)
5. 把這些 commit/留好,當作後端與前端共同依賴的地基
完成後告訴我契約與共用介面長怎樣。
```

> **為什麼 team lead 自己做契約 + 共用層?** 後端產出什麼、前端就吃什麼,全靠這條 API 契約。
> 契約先定死、再放隊友平行,backend-owner 跟 reader-owner 才不會對欄位各自想像、最後兜不起來。
> 這就是「凍結 = 替代即時對齊」,跨技術棧時尤其關鍵。

---

## Step 3 — 平行開發三模組 ⭐(貼這段)

```text
現在 spawn 三個隊友平行開發,規則:每人只碰自己的目錄;要動 lib/shared/、pubspec.yaml 或 API 契約,
一律先用 mailbox 問我、等我同意,不要自己改。

- teammate backend-owner   → 只碰 backend/ :
    用 uv 管理的 Python + FastAPI。每日抓 arXiv 最新 5 篇(預設 cs.AI/cs.LG/cs.CL,
    端點 http://export.arxiv.org/api/query,sortBy=submittedDate),呼叫 Gemini API 整理成 markdown 報告,
    存成每日一份(保留歷史),用 cron 或可手動觸發的指令排程,照契約提供 GET /reports/today 與 GET /reports。
    API key 只從環境變數讀,絕不寫進程式碼。
- teammate reader-owner    → 只碰 lib/reader/ :
    用 ReportApiClient 拉今日報告 + 歷史清單,做報告閱讀畫面(render markdown)、歷史回看。
- teammate breathing-owner → 只碰 lib/breathing/ :
    閱讀計時(累積 10 分鐘)觸發 → 60 秒呼吸動畫(跟著圓圈吸/吐)→ 做完回到閱讀。

每個隊友要連同自己模組的測試一起做,自己那塊乾淨才算完成
(後端:能跑起來 + GET /reports/today 回得到報告;前端:flutter analyze 0 error)。
動 lib/shared/ 或 API 契約之前要先提計畫、等我批准(require plan approval)。
```

現場觀察點:
- **task list** 三個任務同時 in-progress,三個隊友各做各的
- **mailbox**:reader-owner 多半會傳訊息問你「報告欄位」「呼吸提醒誰負責觸發」之類,你回覆它才繼續 —— 這就是 Agent teams 跟 sub-agent 最大的不同
- **跨技術棧**:backend-owner 在跑 Python/uv,reader-owner 在跑 Flutter,兩個技術棧靠你凍結的契約對接
- 想直接跟某個隊友講話:in-process 用 **Shift+Down** 輪到他再輸入;split-pane 直接點他的視窗

---

## Step 4 — 整合 + 驗收(貼這段)

```text
三個隊友都完成後,由你(team lead)整合,然後跑驗收,把實際輸出貼給我:

後端(在 backend/):
  uv run <啟動指令>          # FastAPI 起得來
  curl GET /reports/today     # 回得到當天報告(papers 有 5 篇、有 markdownBody)
  手動觸發一次每日抓取         # 能產出一份新報告

前端(在 app 根目錄):
  flutter analyze     # 要 0 error
  flutter test        # 要全綠
  flutter run         # 能讀報告、計時到門檻跳呼吸動畫、做完回到閱讀

都過了再說完成。任何一個沒過,協調對應的隊友修到過為止。
```

---

## Step 5 — 收尾:關隊友 + 清理 team(貼這段)

```text
先請所有隊友 shut down,確認沒有隊友還在跑,再 clean up the team。
```

> ⚠️ **一定要由 team lead(主管)做清理**,不要叫隊友清。還有隊友在跑時清理會失敗,先關隊友再清。

---

## 進階(想教更深可加)

- **API key 安全**:backend-owner 只從 `GEMINI_API_KEY` 環境變數讀,`.env` 進 `.gitignore`,repo 只留 `.env.example`。
  這條剛好示範「team lead 在規格就把安全紅線講死,隊友照做」。
- **品質閘門用 hooks**:`TeammateIdle`(隊友要閒置時跑,exit 2 可把他叫回繼續)、`TaskCompleted`(任務標完成時跑,exit 2 可擋下並回饋)。可以用來強制「後端 GET /reports/today 沒回 200 不准標完成」。
- **用 subagent 定義當隊友角色**:把 backend-owner 等寫成 `.claude/agents/*.md`,生成隊友時按名字指定,角色可重用。
- **指定隊友模型**:`Use Sonnet for each teammate.` 可省 token;research/前端 UI 類用 Sonnet 通常夠,後端摘要邏輯也行。
- **Token 成本**:每個隊友是獨立實例、各自一份 context,token 用量隨隊友數線性增加。3–5 人是甜蜜點。

---

## 卡點對照表 ⭐

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 叫它建 team 卻沒 task list / mailbox | 旗標沒生效(在已開的 session 才寫 settings.json) | 重開 claude;`claude --version` 確認 ≥ 2.1.32 |
| backend 與 reader 欄位對不起來 | 契約沒先凍結就放隊友平行 | 回 Step 2,team lead 先把 API 契約定死再 spawn |
| 隊友跑去改 `lib/shared/` | 沒講清楚共用層只有 team lead 能改 | Step 3 prompt 明寫「動 shared/契約先 mailbox 問我、require plan approval」 |
| 清理 team 失敗 | 還有隊友在跑 | 先請所有隊友 shut down,再 clean up |
| Gemini API 報 401 / 沒 key | 真 key 沒設或被誤放進 repo | key 只進環境變數;repo 只留 `.env.example` |

---

## 講師私房筆記

- **節奏**:Step 0–2 約 20 分鐘(環境 + 研究 + 凍結契約),Step 3 平行開發是重頭戲留 40–50 分鐘,Step 4–5 約 20 分鐘。
- **故意踩坑**(比口頭講有效):先**不凍結契約**就直接 spawn backend + reader,讓他們欄位對不上、在 mailbox 互相問,卡住之後再回頭補契約 —— 學生秒懂「凍結 = 替代即時對齊」。
- **跨技術棧是這題的賣點**:刻意挑「後端 Python + 前端 Flutter」就是要讓學生看到 Agent teams 不限單一語言,一條契約就能讓兩棧平行。
- **給不同角色**:後端背景的學生盯 backend-owner 怎麼處理 arXiv + Gemini API;前端背景的盯 reader/breathing 的 UI;主管角度的盯 team lead 怎麼用 mailbox 仲裁。
- **完成版先跑過**:上課前自己照這份在 `arxiv-1-完成版/` 跑一次,確認 arXiv API 抓得到、Gemini key 設好,再帶學生做空白版,才有底氣。

---

## 一句話總結

> **開旗標 → 叫 team lead 建 team → 研究先行 → 凍結 API 契約 + 定共用層 → 三個隊友平行各擁一個目錄(backend / reader / breathing,靠契約對接)→ 整合驗收 → 關隊友清理。**

---

_Last updated: 2026-05-22_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材(同目錄):`_Context/app-spec.md`(要蓋成什麼)、`_Context/team-roles.md`(誰擁有什麼 + mailbox 規則)、`_Context/research-intake.md`(研究員要查什麼)_
_官方文件:Claude Code Docs「協調 Claude Code 工作階段團隊 / Agent teams」_
