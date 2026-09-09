# agent_teams — 原生 Agent teams 多 Claude 協作

> 這個資料夾收「**用 Claude Code 原生的 Agent teams 功能**(team lead 協調多個獨立 Claude 隊友)」的範例。
> Agent teams 是**實驗功能**,需 Claude Code v2.1.32+ 並開 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`。

## 三種「多 agent」型態,先分清楚

| 型態 | 隊友是什麼 | 隔離 / 協調 | 隊友之間 | 最適合 |
|---|---|---|---|---|
| **Sub-agents** | 主對話委派的分身 | 各自獨立 context,結果回主對話 | 不能互相喊話,只回報主對話 | 把一個大任務拆給專業分身(見 wafer、stock 範例) |
| **原生 Agent teams(這裡)** ⭐ | team lead 生成的**獨立 Claude Code 實例** | **共享 task list + mailbox** | **能直接互傳訊息對齊** | 研究/審查、新模組平行開發、跨層協調 |
| **手動 git worktree** | 你自己開的多個 claude | 檔案系統層級隔離,各自 checkout | 各做各的,git merge 才碰頭 | 沒有 Agent teams 時的手動平行替代方案 |

> **教學金句**:「sub-agent 是『派分身回報』,worktree 是『各自回家寫再 merge』,Agent teams 是『一群獨立 Claude 開著共享任務板、邊做邊互相喊話』。」

## 原生 Agent teams 怎麼運作?

```
        你開的 session = team lead(主管)
                    │ 建 team、分派/協調、整合、清理
     ┌──────────────┼───────────────┐
 teammate A     teammate B      teammate C   ← 各自獨立 Claude Code 實例,各有 context
     └──── 共享 task list(認領工作)+ mailbox(直接互傳訊息)────┘
```

- **task list**:`~/.claude/tasks/{team-name}/`,隊友認領、完成、互相解依賴
- **mailbox**:隊友之間、隊友↔team lead 直接傳訊息;隊友完成會自動通知 team lead
- **subagent 定義可當隊友角色**:把角色寫成 `.claude/agents/*.md`,生成隊友時按名字指定,可重用

代價:每個隊友一份 context,**token 用量比單 session 高很多**。3–5 人是甜蜜點,適合真的能各做各的活。

## 範例清單

| 資料夾 | 在做什麼 | 示範重點 |
|---|---|---|
| [`ios-app-flutter-dev/`](ios-app-flutter-dev/README.md) | 用原生 Agent teams 蓋一個 Flutter 冥想 App,先派 researcher 研究、再三個模組隊友平行開發 | 啟用旗標 → 研究先行 → 凍結規格 → 平行分工(mailbox 對齊 shared)→ 整合驗收 → 清理 team |

> 內含兩份:`冥想-1-完成版/`(上課前自己彩排)、`冥想-2-空白課堂版/`(上課現場帶學生做),共用 `agent-team-playbook.md`。

## 配套教材

- 逐步可貼腳本:[`ios-app-flutter-dev/agent-team-playbook.md`](ios-app-flutter-dev/agent-team-playbook.md)
- 120 分鐘帶課:[`ios-app-flutter-dev/冥想-2-空白課堂版/WALKTHROUGH.md`](ios-app-flutter-dev/冥想-2-空白課堂版/WALKTHROUGH.md)
- sub-agent 對照組:[`../Projects/02-recipe-genie/`](../Projects/02-recipe-genie/README.md)
- 判斷「該不該開 team」的框架:[`../docs/walkthroughs/agent_team_walkthrough.md`](../docs/walkthroughs/agent_team_walkthrough.md)
