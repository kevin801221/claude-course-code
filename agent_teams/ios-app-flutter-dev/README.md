# 用 Agent teams 蓋一個「arXiv 每日論文閱讀器」App

> **學什麼**:用 Claude Code 原生的 **Agent teams**(實驗功能)協調一個 team lead + 多個 teammate,共享 task list、用 mailbox 互傳訊息,平行蓋出同一個 App。
> **方法**:原生 Agent teams,**不是** git worktree、**不是** sub-agent。
> **產出**:一個跑得起來的 App MVP(後端 Python/uv + 前端 Flutter)+ 一套你能複用的「研究→凍結規格→平行分工→整合驗收」agent team 工作流。

---

## ⚠️ 這是哪一種「多 agent」?先分清楚

Claude Code 有三種讓多個 AI 一起做事的機制,**這個範例用的是第三種(原生 Agent teams)**:

| 機制 | 隊友是什麼 | 怎麼溝通 | 這範例用嗎 |
|---|---|---|---|
| **Sub-agents** | 主對話派出去的分身 | 只回報主對話,彼此不講話 | ❌ |
| **Git worktree 平行** | 你手動開的多個 Claude,各自一份 checkout | git merge 才碰頭 | ❌(這範例**刻意不走** worktree) |
| **原生 Agent teams** ⭐ | team lead 生成的獨立 Claude Code 實例 | **共享 task list + mailbox 直接互傳訊息** | ✅ 就是這個 |

> **教學金句**:「sub-agent 是『派分身回報』,worktree 是『各自回家寫再 merge』,Agent teams 是『一群獨立 Claude 開著共享任務板、邊做邊互相喊話』。」

---

## 要蓋的 App

後端每天抓 arXiv 最新 5 篇科技論文、用 Gemini API(gemini-3.5-flash)整理成一份研究報告;
使用者在 iPhone 上讀,閱讀累積到門檻就跳 60 秒呼吸動畫提醒休息。

⚠️ Claude Code 工作流教學範例。閱讀疲勞 / 呼吸提醒內容僅供 App 功能設計參考,不構成醫療建議。

---

## 兩份教材:完成版 + 空白課堂版

> ⚠️ 兩份**都是你親自開 Agent team 來蓋**的,不是「已經幫你做好的成品」。共用同一份腳本 [`agent-team-playbook.md`](agent-team-playbook.md)。

| 資料夾 | 是什麼 | 什麼時候用 |
|---|---|---|
| [`arxiv-1-完成版/`](arxiv-1-完成版/README.md) | **上課前彩排**:你自己照 playbook 開一個 Agent team,把 App 從零蓋到跑得起來,先做出「一個成功的成品」當底氣 | 上課前一晚自己跑一次 |
| [`arxiv-2-空白課堂版/`](arxiv-2-空白課堂版/README.md) | **上課現場**:同一套方法、乾淨起手 + 120 分鐘帶課 walkthrough,帶學生現場開 team 從零蓋 | 上課現場帶學生做 |

> **學習順序**:先在完成版自己彩排成功一次(Agent teams 是實驗功能,行為偶爾飄,先跑過才不會上課翻車)→ 上課用空白版,現場 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 開 team 真的蓋一遍。
>
> 完整逐步腳本:[`agent-team-playbook.md`](agent-team-playbook.md)。

---

## 為什麼這個 App 適合示範 Agent teams?

官方文件講 Agent teams 最強的場景之一是「**新模組或功能:隊友各自擁有一個獨立部分,不會相互干擾**」。

這個 App 天然能切成**目錄不重疊**的三塊,正好一塊配一個隊友,而且**橫跨後端 + 前端兩個技術棧**:

```
team lead(主管) ── 定共用層 lib/shared/(Report 模型 + ApiClient + 路由)、凍結 API 契約、最後整合
   ├─ teammate backend-owner    ── backend/        後端:arXiv 抓取 + Gemini 摘要 + FastAPI
   ├─ teammate reader-owner     ── lib/reader/     報告閱讀畫面 + 歷史回看
   └─ teammate breathing-owner  ── lib/breathing/  閱讀計時 + 60 秒呼吸動畫
```

> **教學金句**:「這題刻意挑『後端 Python + 前端 Flutter』—— 就是要讓學生看到 Agent teams 不限單一語言,一條 API 契約就能讓兩棧平行幹活。」

研究階段也適合用 Agent teams 的另一個強項「**研究和審查:多個隊友同時調查不同面向**」—— 先派一個研究員隊友把「arXiv 抓取設定 / 閱讀提醒間隔 / 呼吸節奏」查清楚,結論餵進凍結的規格,模組隊友才開工。

---

## 前置需求

| 需求 | 說明 |
|---|---|
| Claude Code **v2.1.32+** | Agent teams 是這版之後才有的功能(`claude --version` 確認) |
| 開實驗旗標 | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`(settings.json 或環境變數,見 playbook) |
| `GEMINI_API_KEY` | 後端呼叫 Gemini 摘要要用;只放後端環境變數,別進前端 / 別 commit |
| Flutter SDK + uv | 要看 App 真的跑起來才需要;研究與規劃階段不用 |

---

## 跟著哪份走

- 想先看成品與「team 怎麼開的」→ [`arxiv-1-完成版/README.md`](arxiv-1-完成版/README.md) 和 `agent-team-playbook.md`
- 要上課帶人現場做 → [`arxiv-2-空白課堂版/WALKTHROUGH.md`](arxiv-2-空白課堂版/WALKTHROUGH.md)
- 團隊分工與 mailbox 規則 → 各版 `_Context/team-roles.md`
