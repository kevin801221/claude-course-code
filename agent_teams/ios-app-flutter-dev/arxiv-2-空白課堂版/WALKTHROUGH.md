# 用原生 Agent teams 蓋「arXiv 每日論文閱讀器」App — 講師 Walkthrough

> **對象**:用過 Claude Code、想學「原生 Agent teams」協調多實例的人(會基本指令即可,不需要 Flutter / Python 高手)
> **形式**:講師現場帶 / 自學皆可
> **時長**:120 分鐘
> **產出**:一個跑得起來的 App MVP(後端 Python/uv + 前端 Flutter),以及一套可複用的「研究→凍結規格→平行分工→整合驗收」**Agent teams** 工作流
> **核心方法**:開實驗旗標,讓一個 team lead 協調 researcher + 三個模組隊友,共享 task list、用 mailbox 互傳訊息平行開發
>
> ⚠️ Claude Code 工作流教學範例。閱讀疲勞 / 呼吸提醒內容僅供 App 功能設計,非醫療建議。

---

## 開場(10 分鐘):為什麼是 Agent teams,不是 sub-agent 或 worktree?

學生會問:不是有 sub-agent、有 git worktree 平行了嗎?幹嘛用 Agent teams?

| | sub-agent | git worktree 平行 | **原生 Agent teams(這堂)** |
|---|---|---|---|
| 隊友是什麼 | 主對話派的分身 | 你手動開的多個 claude | team lead 生成的獨立 Claude Code 實例 |
| 溝通 | 只回報主對話 | git merge 才碰頭 | **共享 task list + mailbox 直接互傳** |
| 撞檔風險 | 主對話序列化,慢 | 物理隔離但要自己 merge | 各擁不同目錄,mailbox 對齊 shared |
| 怎麼開 | 程式自動派 | 自己開終端 + git 指令 | **自然語言叫 team lead 開** |

> **教學金句**:「sub-agent 是『派分身回報』,worktree 是『各自回家寫再 merge』,Agent teams 是『一群獨立 Claude 開著共享任務板、邊做邊互相喊話』。」

⚠️ Agent teams 是**實驗功能**,要 Claude Code **v2.1.32+** 並開 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`。token 用量比單 session 高很多(每個隊友一份 context),適合「平行探索/新模組」這種真的能各做各的活。

---

## 📁 概念圖(先讓學生看全貌)

```
              你開的 session = team lead(主管)
                        │  建 team、凍結規格與 API 契約、定共用層、整合、清理
        ┌───────────────┼────────────────┬──────────────┐
   researcher       backend-owner     reader-owner    breathing-owner
  研究先行          backend/          lib/reader/      lib/breathing/
 (arXiv/節奏)    (Python/uv+Gemini)  (讀報告/歷史)    (計時+呼吸動畫)
        └──────── 共享 task list(誰認領什麼)+ mailbox(互傳訊息對齊)────────┘
```

對應檔案:`_Context/research-intake.md`(研究單)→ `_Context/app-spec.md`(規格 + API 契約)→ `_Context/team-roles.md`(分工 + mailbox 規則)。
完整可貼的提示在 [`../agent-team-playbook.md`](../agent-team-playbook.md)。

> **教學金句**:「這題刻意橫跨後端 Python + 前端 Flutter —— 兩個技術棧靠一條凍結的 API 契約對接,正好示範 Agent teams 不限單一語言。」

---

## Phase 0:啟用 + 開 session(10 分鐘)🛠

```bash
claude --version        # 要 >= 2.1.32
flutter --version       # 開發階段才需要;研究/規劃可先不裝
uv --version            # 後端要用;後端開發階段才需要

# 開旗標(settings.json 或 export 二選一)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
# 後端摘要要用的 key(只放環境變數,別 commit)
export GEMINI_API_KEY=...

cd agent_teams/ios-app-flutter-dev/arxiv-2-空白課堂版
cat _Context/team-roles.md     # 先讀分工 + mailbox 規則
claude                          # 這個 session 就是 team lead
```

> 💡 旗標**只在 claude 啟動時讀**;在已開的 session 才寫 settings.json,要重開 claude 才生效。
> 旗標沒開,叫它建 team 只會退化成一般 sub-agent,看不到 task list 與 mailbox。先確認開了。
> 顯示模式預設 `in-process`(Shift+Down 切換隊友);要分割視窗需 tmux / iTerm2,設 `"teammateMode": "tmux"`。

---

## Phase 1:開 team + 研究先行 ⭐(25 分鐘)

把 playbook 的 Step 1 貼給 team lead:叫它建 team、先 spawn 一個 `researcher` 隊友,
查「arXiv 抓取設定 / 閱讀提醒間隔 / 呼吸節奏 / 該避免的成長駭客做法」,結論寫進 `_Context/research-findings.md`,先別寫程式碼。

**現場重點**:
- 讓學生看 **task list 出現**、researcher 開始跑
- researcher 完成會**自動通知 team lead**(不用一直問),這就是 mailbox 的價值
- 強調 findings 要標來源、標「非醫療建議」

> **教學金句**:「研究先行不是拖時間 —— 是讓 arXiv 抓幾篇、提醒間隔幾分鐘,有依據而不是拍腦袋。」

---

## Phase 2:凍結規格 + team lead 定共用層與契約 ⭐(20 分鐘)

貼 playbook Step 2:team lead 把 findings 收斂進 `app-spec.md`、**宣布凍結**,
然後**親自**做共用層:`flutter create` 出骨架、凍結 **API 契約**(`GET /reports/today` 的回傳結構)、
定 `lib/shared/`(Report / Paper 模型、ReportApiClient 介面、路由)、建 `backend/` uv 骨架 + `.env.example`,先不要 spawn 開發隊友。

> **教學金句**:「後端產出什麼、前端就吃什麼,全靠這條 API 契約。契約先由 team lead 定死、再放隊友平行 —— 不然後端跟前端對欄位各自想像,最後兜不起來。」

**現場重點**:讓學生理解「凍結 + 先定契約/shared」就是 Agent teams 版的「先對齊再開工」,跨技術棧時尤其關鍵。

---

## Phase 3:平行開發三模組 ⭐⭐⭐(45 分鐘,高潮)

貼 playbook Step 3:spawn `backend-owner` / `reader-owner` / `breathing-owner` 三個隊友,各只碰自己目錄,
要動 `lib/shared/`、`pubspec.yaml` 或 API 契約一律先 mailbox 問 team lead、等批准。

| 隊友 | 只碰 | 做什麼 |
|---|---|---|
| `backend-owner` | `backend/` | Python/uv + FastAPI:抓 arXiv 5 篇 → Gemini 摘要成 markdown 報告 → 照契約提供 API |
| `reader-owner` | `lib/reader/` | 用 ReportApiClient 拉報告,做閱讀畫面(render markdown)+ 歷史回看 |
| `breathing-owner` | `lib/breathing/` | 閱讀計時累積到門檻 → 60 秒呼吸動畫 → 回到閱讀 |

**現場一定要讓學生看到的三件事**:
1. **task list** 三個任務同時 in-progress —— 真平行
2. **mailbox**:reader-owner 傳訊息問 team lead「報告回傳欄位長怎樣」→ team lead 回 → 隊友才繼續(這是跟 sub-agent 最大的差別)
3. **跨技術棧**:backend-owner 在跑 Python/uv,reader-owner 在跑 Flutter,兩棧靠你凍結的契約對接

> **教學金句**:「sub-agent 只會回報結果;Agent teams 的隊友會**主動問你問題**。能對話,是它值得多花 token 的原因。」

---

## 整合 demo:整合 + 驗收 + 清理(收尾,10 分鐘)

貼 playbook Step 4 + Step 5:

```bash
# 後端(在 backend/)
uv run <啟動指令>          # FastAPI 起得來
curl .../reports/today      # 回得到當天報告(papers 5 篇 + markdownBody)

# 前端(在 app 根目錄)
flutter analyze     # 0 error
flutter test        # 全綠
flutter run         # 能讀報告、計時到門檻跳呼吸動畫、做完回到閱讀
```

驗收過 → 請所有隊友 shut down → team lead 執行 **clean up the team**。

> ⚠️ 一定要由 **team lead(主管)** 清理;還有隊友在跑會清理失敗,先關隊友再清。

---

## 常見問題 / FAQ

1. **沒裝 Flutter / uv 能上課嗎?** Phase 0-2(研究 + 規格)幾乎不用;要看 App 跑起來才需要。
2. **旗標開了還是沒看到 task list?** 確認版本 ≥ 2.1.32;in-process 模式隊友是隱藏的,按 Shift+Down 輪流看。
3. **跟 sub-agent 到底差在哪?** sub-agent 只向主對話回報、彼此不講話;Agent teams 隊友共享任務板、能直接互相 mailbox。
4. **token 會不會很貴?** 會,每個隊友一份 context,隨人數線性增加。研究/新模組值得;日常小事用單 session。
5. **沒有 `GEMINI_API_KEY` 怎麼辦?** backend-owner 可先用假資料 / stub 報告把契約打通,key 到位再接真摘要。
6. **能不能巢狀(隊友再開隊友)?** 不行,只有 team lead 能管 team,沒有巢狀團隊。

---

## 卡點對照表 ⭐

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 叫它建 team 卻沒 task list / mailbox | 旗標沒開或版本太舊 | `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`、升到 v2.1.32+ |
| backend 與 reader 欄位對不起來 | 沒先凍結 API 契約就 spawn | 回 Phase 2,team lead 先把契約定死再放平行 |
| 兩個隊友都改到 `lib/shared/` 起衝突 | 違反「shared / 契約只能 team lead 改」 | 隊友動 shared 前要先 mailbox 問、等批准 |
| 主管自己跳下去寫,不等隊友 | team lead 有時會搶做 | 跟它說「Wait for your teammates to complete before proceeding」 |
| 任務卡在 in-progress 不動 | 隊友沒把 task 標完成(已知限制) | 檢查實際做完沒,手動更新狀態或叫 team lead 推一下 |
| Gemini 報 401 / 沒 key | key 沒設或被誤放進 repo | key 只進環境變數;repo 只留 `.env.example` |
| 清理失敗 | 還有隊友在跑 | 先請所有隊友 shut down,再由 team lead 清理 |

---

## 講師私房筆記

- **時間分配**:Phase 1(研究)與 Phase 3(平行開發)是兩個高潮,務必讓學生**親眼看到 task list 同時在動、mailbox 真的有訊息來回**,光講沒感覺。
- **故意製造 mailbox**:Phase 3 可以故意把 API 契約留一個細節沒講清楚(例如報告要不要帶 `summary` 欄位),逼 backend / reader 發 mailbox 對齊 —— 學生一次就懂「能對話」是什麼意思。
- **跨技術棧是這題的賣點**:後端 Python + 前端 Flutter,讓學生看到 Agent teams 不限單一語言,一條契約就能讓兩棧平行。
- **先彩排再上課**:Agent teams 是實驗功能,行為偶爾飄(任務狀態滯後、主管搶做)。**務必先在 `../arxiv-1-完成版/` 自己跑成功一次**,上課才不會翻車。
- **不同角色**:給後端工程師 → 盯 backend-owner 怎麼處理 arXiv + Gemini;給前端 → 盯 reader/breathing 的 UI;給 PM / Lead → 強調「凍結契約 = 平行的前置成本」這個管理觀念。

---

## 一句話總結

> **原生 Agent teams = 一個 team lead 協調多個獨立 Claude 隊友,共享 task list、用 mailbox 互傳訊息;這堂課真正在教的是『研究先行、凍結規格與 API 契約、先定共用層、各擁一個目錄、mailbox 對齊』—— 跨後端前端兩棧也能平行而不亂。**

---

## 進階閱讀

- 🔗 可直接貼的逐步腳本:[`../agent-team-playbook.md`](../agent-team-playbook.md)
- 🔗 上課前彩排版:[`../arxiv-1-完成版/README.md`](../arxiv-1-完成版/README.md)
- 🔗 官方文件:Claude Code Docs「協調 Claude Code 工作階段團隊 / Agent teams」(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`)
- 🔗 sub-agent 對照:[`../../../Projects/02-recipe-genie/`](../../../Projects/02-recipe-genie/)

---

_Last updated: 2026-05-22_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材(同目錄):README.md、_Context/app-spec.md、_Context/team-roles.md、_Context/research-intake.md_
_共用腳本:../agent-team-playbook.md_
