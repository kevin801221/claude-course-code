# 教學總指揮譜 — Claude Code 公開課（12 小時作戰版 ＋ 6 小時逐分鐘精華表）

> ⏱ **只有 6 小時的看這裡**：直接跳到下方 [**6 小時時時刻刻作戰表**](#6-小時時時刻刻作戰表一日精華版)——一張表告訴你每個時段在講哪個 Part、什麼時候切 IDE、開哪個資料夾、何時休息。12 小時的全景與各 Part 細節在後方完整展開。
> 
> **對象**：要拿這套教材**親自交完一整天 12 小時課**的講師（就是你）或深度自學的全端／AI 工程師
> **形式**：講師現場帶課（投影開 PPT，第二螢幕或平板開這份指揮譜）；自學者按圖索驥
> **時長**：12 × 60 分鐘 session（純內容 ~11h，含休息與 Q&A 12h）／ 6 小時一日極速精華
> **產出**：按正確節奏帶完整片 codebase——包含 19 個 PPT Parts、9 個 Projects、4 大 Agent 流水線、原生 Agent Teams 與 Context Engineering 工廠
> **核心方法**：PPT 講觀念（為什麼）→ 切 IDE 跑真實檔案（怎麼做）→ 學員當場敲（記得住）
> **跟現有教材的關係**：
> - **這份（指揮譜 `WALKTHROUGH.md`）** = 鳥瞰圖與駕駛儀表板。一張表看完 19 個 Part 對到哪個 Hour、切不切 IDE、開哪個資料夾、那一刀最容易卡哪。**帶課現場主看這份。**
> - **[`docs/walkthroughs/course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md)** = 逐小時放大鏡。每個 Hour 細到「0–15 min 做什麼、教學金句逐句、預期 Q&A」。**備課時細讀、某小時卡住翻那份。**
> - **專案級落地手冊**：[`Projects/README.md`](Projects/README.md)、[`Projects/09-timetrace/WALKTHROUGH.md`](Projects/09-timetrace/WALKTHROUGH.md)、[`agent_teams/README.md`](agent_teams/README.md)、[`important-plugins/superpowers_production_walkthrough.md`](important-plugins/superpowers_production_walkthrough.md)。

---

## 開場（讀這份前先懂）：為什麼要兩份帶課教案？

一個人帶 12 小時課，最怕兩件事：
1. **「現在到底該講 PPT 還是切 IDE？」迷路**：講著講著投影片切太快，學員還在開終端，節奏全亂。
2. **某一刀切下去學員集體卡住、現場手忙腳亂**：例如按 `e` 導致 VS Code 卡死、MPS 算子不支援、或者是 hook 沒生效。

| 你需要的東西 | 看哪份 |
|---|---|
| 全局方向感（現在第幾 Part、切不切、開哪、時鐘落後幾分鐘） | **這份指揮譜的「全景路線圖」與「時時刻刻作戰表」** |
| 某個 Hour 的逐分鐘腳本 + 金句逐句 + 深入 Q&A | [`docs/walkthroughs/course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md) 對應 Hour |
| 切 IDE 那一瞬間學員會卡什麼、怎麼秒救 | **這份各 Part 的「這一刀的卡點」與「卡點對照表 ⭐」** |
| 時間不夠要砍哪 | **這份「應變：時間不夠怎麼砍」** |

> **教學金句**：「指揮譜是地圖、12h 教案是逐步導航。開車看地圖確認方向，路口才聽導航——別把導航當地圖一路盯著，會撞牆。」

---

## 📁 12 小時全景路線圖（整堂課的儀表板）

全課對應 PPT **338 頁**、**19 個 Part**、**9 個 Mini-Projects**、**4 大 agent 生產線案例**、**原生 Agent Teams** 與 **Context Engineering 工廠**。下表把 Part 對到 Hour、標明切不切 IDE、切了開哪。

> ⚠️ **頁碼會隨版本漂移**（318 → 320 → 338+）。**不要死記頁碼**——認三件事就不會迷路：
> 1. Part 名稱與主題
> 2. PPT 章節分隔頁（深色 navy 底）
> 3. 每頁 footer 的 `▶ 實戰演練：<路徑>`（看到它＝這個 Part 有資料夾可切）。

| Hour | PPT Part | 約略頁段 | 主題 | 切 IDE？ | 開哪個資料夾 → 開哪個檔 | 核心目標 |
|---|---|---|---|---|---|---|
| **H1** | 開場 + Part 1 | 1–25 | 認識 Claude Code 與底層架構 | ❌ 純 PPT + 終端起手 | 終端打 `claude --version`、`claude` | 打破「另一個 Cursor」的誤解，建立 Agentic CLI 認知 |
| **H2** | Part 2–3 | 26–60 | CLI 基礎 + 內建 Slash Commands | ❌ 純 PPT + 終端 demo | 備用終端跑 `/help` `/status` `/init` | 掌握模式切換、`@` `#` `!` 三記號與基本 session 治理 |
| **H3** | **Part 4** ⭐ | 61–75 | **自訂 Slash Commands** | ✅ **全課第一次切** | `Projects/01-weekly-haiku/` → `README.md` | **唯一保留學員自己動手**，體驗 prompt 封裝與重啟生效 |
| **H4** | Part 5–6 | 76–110 | Settings + CLAUDE.md / Memory | 半切（開本 repo 設定） | 本 repo `.claude/settings.json` ＋ `CLAUDE.md` | 三層級設定優先權、權限模式、記憶階層與專案規範綁定 |
| **H5** | **Part 7（前半）** | 111–135 | **Sub-agents 入門** | ✅ 切 | `Projects/02-recipe-genie/` → `README.md` | 隔離 context、定義角色 prompt、tools 限制與自動路由 |
| **H6** | **Part 7（後半）** | 136–160 | **多 Agent 流水線 + 原生 Agent Teams** | ✅ 切三次 | ① `agent_group_projects/computer-vision-wafer-agents-detection-demo/`<br>② `Projects/08-agent-team-review/`<br>③ `agent_teams/ios-app-flutter-dev/` | 4-agent YOLO ML 產線 ＋ 4人 Kanban 審查 ＋ arXiv 論文閱讀器跨棧協作 |
| **H7** | **Part 8** | 161–185 | **Skills 技能三層次 ＋ Matt Pocock AI PM 方案** | ✅ 切三次 | ① `Projects/03-youtube-notes/`<br>② `Projects/07-weekly-reports-skill/`<br>③ `Projects/build-gitnexus-skill-commandline/`<br>（加碼：Matt Pocock 28萬星 AI PM 方案） | 從極簡 SKILL.md 到 production 級；掌握 `/implement-spec`（相依並行派工）、`/pr`（證據與門禁評估）、`/retro`（修環境復盤）與 `GLOSSARY.md` |
| **H8** | **Part 9** ⭐ | 186–215 | **Hooks 生命週期與防護欄** | ✅ 切 | `Projects/04-pomodoro/` ＋ 本 repo `.claude/hooks/` | PreToolUse / Stop / UserPromptSubmit 等 8 種事件，程式碼強制規範 LLM |
| **H9** | **Part 10 + Part 12** | 216–245 ＋ 300–315 | **MCP 外部集成 + Agent SDK** | ✅ 切兩次 | ① `Projects/05-organize-downloads/`<br>② `Projects/06-discord-dm-bot/` | MCP 自建外部插座 ＋ Agent SDK 把 Claude 包進 Python 服務 |
| **H10** | **Part 11（前半）** | 246–280 | **Plugins 生態 + superpowers 14 招** | ✅ 切兩次 | ① `Projects/plugins-from-zero-to-marketplace/`<br>② `important-plugins/superpowers/` | Plugin 從零上架 Marketplace ＋ HARD-GATE / Anti-Pattern 實戰心法 |
| **H11** | **Part 11（後半）+ 旗艦 SaaS** | 281–299 ＋ 專案 | **Pomocat 案例 ＋ TimeTrace 全組件一鏡到底** | ✅ 切兩次 | ① `important-plugins/project1-superpowers/`<br>② `Projects/09-timetrace/` | 看 Pomocat 規格凍結與驗收 ＋ Agents×Skills×MCP×Hooks×Design 終極整合 |
| **H12** | **Part 18 + Part 19** | 316–338 | **Context Engineering 實戰 + 收尾** | ✅ 切 | `agent_group_projects/computer-vision-wafer-detection/` 或 `context-engineering-intro/` | CLAUDE.md + INITIAL.md → `/generate-prp` → `/execute-prp`，發放角色建議 |

> **快速心法**：H1–H2、H4 的 Part 5–6 是「**講觀念**」留 PPT；H3、H5–H11、H12 是「**動手與看 code**」講完概念秒切 IDE。**想要每小時逐分鐘台詞與金句，查閱 [`docs/walkthroughs/course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md)。**

---

## 6 小時時時刻刻作戰表（一日精華版）

> **什麼時候用**：你只有 6 小時（或企業內訓一日課）要把整套帶完。
> **取捨原則**：
> - 保住 **6 大支柱**（slash / memory / sub-agent & agent teams / skill / hook / plugin & MCP）。
> - **絕不砍的單元**：Part 1（起手開竅）、Part 4（第一次切 IDE 留學員自己敲）、Part 6（Memory）、Part 9（Hooks）。
> - **時間紀律**：只在 **Part 4 留 10 分鐘學員自己寫一個 command**；其餘案例一律「**講師 live demo 或開 code 口頭帶，學員專注看**」。
> - Part 13–17（雜項設定與外部資源）整段不講，提供連結給學員自學；Part 18 著重 Context Engineering 概念與 PRP 流程。
>
> 時間欄為「從開課算起的精確時鐘」（0:00 = 講師開場）。認 Part 名稱 + PPT footer 的 `▶ 實戰演練`。

| 時鐘 | 時長 | PPT Part | 主題 | 切 IDE？開哪 | 這刀重點 / 避坑卡點 |
|---|---|---|---|---|---|
| **0:00–0:20** | 20m | 開場 + Part 1 | 認識 Claude Code | ❌ PPT + 終端 demo | 開場一句話：今天你會帶走 6 個能動手的武器。終端 demo `claude`、`@` 帶檔案 |
| **0:20–0:35** | 15m | Part 2–3 | CLI 基礎 + 內建 slash | ❌ PPT + 終端快速 demo | 示範 `/status` `/cost` `/init`；說明 `@` 補全、`#` 記憶與 `!` bash 執行 |
| **0:35–1:15** | 40m | **Part 4** ⭐ | **自訂 Slash Commands** | ✅ **第一次切**：`Projects/01-weekly-haiku/` | **全課唯一保留學員自己動手**。故意改完不重啟 → `/cmd` 找不到 → 退出重進踩坑演練 |
| **1:15–1:35** | 20m | Part 5–6 | Settings + CLAUDE.md / Memory | 半切：本 repo `.claude/settings.json` ＋ `CLAUDE.md` | Part 6 Memory 絕不砍——開本 repo 自己的設定展示真實掛載的 hook 與 skill 規矩 |
| **1:35–1:45** | 10m | — | ☕ **中場休息** | — | 休息，準備進入 Agent 高密度區段 |
| **1:45–2:30** | 45m | **Part 7** | **Sub-agents ＋ 原生 Agent Teams** | ✅ 切 `Projects/02-recipe-genie/` ＋ 口頭開 `agent_teams/` | 故意把 agent description 寫爛 → 不觸發 → 改明確觸發句；比較 sub-agent 與原生 Agent Teams（arXiv 論文閱讀器）的差異 |
| **2:30–3:05** | 35m | **Part 8** | **Skills 技能封裝 ＋ Matt Pocock AI PM** | ✅ 切 `Projects/03-youtube-notes/` ＋ `.claude/skills/` | 對比最小 SKILL.md 與 production 級；加碼展示 Matt Pocock 28萬星技能庫（`GLOSSARY.md` 領域建模、`/implement-spec` 相依並行、`/pr` 證據門禁、`/retro` 復盤） |
| **3:05–3:45** | 40m | **Part 9** ⭐ | **Hooks 自動化防護欄** | ✅ 切 `Projects/04-pomodoro/` ＋ 本 repo `.claude/hooks/` | 絕不砍。故意只放腳本不註冊 settings.json → 沒反應 → 註冊後生效；demo 阻止寫入密鑰 |
| **3:45–3:55** | 10m | — | ☕ **中場休息**（下午回血） | — | 準備迎接 Plugin 與全組件 SaaS 一鏡到底 |
| **3:55–4:25** | 30m | **Part 10** | **MCP 外部世界整合** | ✅ 切 `Projects/05-organize-downloads/` | `claude mcp add` 一行裝完；警告：server 印 log 到 stdout 會搞掛連線，務必改 stderr |
| **4:25–5:20** | 55m | **Part 11** ⭐ | **Plugins ＋ TimeTrace 全組件串接** | ✅ 切 `important-plugins/` ＋ `Projects/09-timetrace/` | Marketplace 安裝 superpowers / ralph-wiggum；一鏡到底展示 Agents×Skills×MCP×Hooks×Design 的 TimeTrace 藍圖 |
| **5:20–5:35** | 15m | Part 12 | Agent SDK（快速帶過） | ✅ 切 `Projects/06-discord-dm-bot/`（口頭/快看） | 只講「SDK = 把 Claude 塞進自己寫的 Python/FastAPI/Bot 裡」，不 live 跑 |
| **5:35–6:00** | 25m | Part 18 + Part 19 | **Context Engineering（概念）+ 角色建議收尾** | ❌ 概念圖解 + 總結 | PRP 流程圖解（INITIAL.md → `/generate-prp` → `/execute-prp`）；依學員角色提供建議與 Q&A |

---

## Phase 0：開課前置檢查（前一晚必做清單）

```bash
# ── 1. 講師環境檢查 ──
claude --version                         # 確認為 2026 最新版本
which -a claude && which uv              # 確認 PATH 正常，Python 工具強制走 uv
which node && node --version             # Node 20+

# ── 2. 提前安裝熱門 Plugin（現場裝＝教學翻車首選）──
/plugin marketplace add anthropics/claude-plugins-official
/plugin install superpowers@claude-plugins-official
/plugin install pr-review-toolkit@claude-plugins-official

# ── 3. 測試本 repo 啟用中的防護 ──
cd ~/claude-code-complete-tutorial
# 嘗試寫入機密測試 hook（預期被 guard-secrets.sh 擋下）
touch .env.test.secret

# ── 4. 備用 session（提前開好）──
# 終端 1：專供切換目錄演練
# 終端 2：常駐 claude REPL 隨時示範
```

### 學員前置作業交代：
- 提前取得教材壓縮包，**禁止上課現場幾十人同時 git clone 耗盡頻寬**。
- 確保安裝 Node.js 20+、`uv`（Python 依賴管理）以及 Claude Code CLI。
- 統一約定 IDE（建議 VS Code 或 Cursor），講師示範開哪，學員就跟著開哪。

> **教學金句**：「現場裝環境是教學車禍第一名——前一晚全都跑過一次，當天專注於概念與節奏。」

---

## Phase 1：第一次切 IDE（H3 · Part 4）⭐ 關鍵轉折點

這是學員「**第一次意識到 Claude Code 能被自己掌控**」的震撼時刻。這刀切得順，整堂課的參與感就確立了。

### PPT 概念停點
投影片講完：
- `.claude/commands/` 目錄結構
- YAML frontmatter 三件套（`name`、`description`、`allowed-tools`）
- 動態參數插槽 `$ARGUMENTS`

當 PPT footer 出現 `▶ 實戰演練：Projects/01-weekly-haiku/` → **暫停 30 秒，切 IDE**。

### 標準操作四動作
```bash
# ① 切到 IDE 開專案資料夾
code ~/claude-code-complete-tutorial/Projects/01-weekly-haiku

# ② 開啟指令檔案，對照講義解構 frontmatter
#    開檔：Projects/01-weekly-haiku/.claude/commands/weekly-haiku.md

# ③ 開啟終端，現場執行示範
cd ~/claude-code-complete-tutorial/Projects/01-weekly-haiku && claude
> /weekly-haiku

# ④ 學員動手練習（留 10 分鐘，本課唯一保留的動手點）
#    複製 weekly-haiku.md 成 daily-mood.md，修改提示詞，退出重開，執行 /daily-mood
```

### 這一刀的卡點與秒救法
| 卡點 | 真實原因 | 現場秒救方案 |
|---|---|---|
| 修改後打 `/daily-mood` 找不到指令 | Claude Code session 尚未重新載入 | **故意不先說，讓全班踩這個坑**，再現場退出重進——勝過口頭提醒十次 |
| `$ARGUMENTS` 沒有接收到值 | 執行時只打了 `/cmd` 沒帶後續文字 | 示範帶參數的寫法：`/daily-mood 剛解完一個大 bug 很爽` |
| frontmatter 語法報錯 | YAML 冒號後少空格或縮排混用 TAB | 強調直接複製現成檔案修改，避免手刻 YAML 縮排 |

> **教學金句**：「自訂 Slash Command 就是把團隊最常用、最容易寫漏的 Prompt 封裝成版本控制的資產。寫一次，全隊共用。」

---

## Phase 2：逐 Part 作戰要點與真實開檔索引

### H1 開場 + Part 1 認識 Claude Code（不切 IDE，純 PPT + 終端）
- **重點**：打破迷思。Claude Code 不是聊天視窗，是「具備完整本機檔案系統與終端執行權限的 Agentic Harness」。
- **現場動作**：終端示範 `claude --version`、啟動 `claude` 輸入 `@` 帶入檔案。
- **卡點**：學員終端報 `command not found: claude` → 檢查 npm global bin 或二進位檔是否有加入 PATH。

### H2 Part 2–3 CLI 基礎 + 內建指令（純 PPT + 快速 demo）
- **重點**：`@` 檔案引用、`#` 記憶、`!` 直接執行 Bash；內建指令 `/help`、`/compact`（上下文壓縮）、`/status`、`/init`、`/cost`。
- **現場動作**：在空白資料夾執行 `/init`，展示 Claude 自動掃描專案並產生 `CLAUDE.md` 骨架的過程。
- **卡點**：`/compact` 後以為所有記憶都保留 → 澄清：上下文壓縮會遺失細節，長期規則必須放 `CLAUDE.md`。

### H4 Part 5–6 Settings + CLAUDE.md / Memory（半切）
- **重點**：Local > Project > User 三層設定覆蓋；Permissions 權限模式（`manual`, `acceptEdits`, `auto`, `plan`, `bypassPermissions`）；CLAUDE.md 的分層載入。
- **實戰切換**：直接開**本教材 Repository 自身**的設定檔當活教材！
  ```bash
  code ~/.claude/CLAUDE.md                                    # 全域層
  code ~/claude-code-complete-tutorial/CLAUDE.md             # 專案層
  code ~/claude-code-complete-tutorial/.claude/settings.json # 啟用中的真實 hook
  ```
- **卡點**：`settings.local.json` 包含個人 API Key 誤推到 GitHub → 檢查 `.gitignore` 是否加入 `settings.local.json`。

### H5 Part 7（前半）Sub-agents 入門 → `Projects/02-recipe-genie/`
- **重點**：Sub-agent 是「隔離上下文的專職助理」。五件套 frontmatter（name, description, tools, model, color）。
- **實戰指令**：
  ```bash
  code ~/claude-code-complete-tutorial/Projects/02-recipe-genie
  # 開啟：.claude/agents/recipe-genie.md
  cd Projects/02-recipe-genie && claude
  > 我想吃辣的、半小時內做完、冰箱有雞肉跟蛋
  ```
- **卡點**：輸入問題後 Claude 沒呼叫 sub-agent → 故意示範把 description 寫得太模糊（「處理日常問題」），改為具體觸發詞後立即自動命中。

### H6 Part 7（後半）多 Agent 產線 + 原生 Agent Teams（切三次）⚠️ 高密度段
1. **Wafer ML 4-Agent 流水線**：
   ```bash
   cd ~/claude-code-complete-tutorial/agent_group_projects/computer-vision-wafer-agents-detection-demo
   code .
   claude
   > /agents  # 現場走 TUI 展示 data-hunter、data-labeler、training-runner、evaluator
   ```
   > ⚠️ **在 `/agents` 確認畫面按 `s` 存檔，切忌按 `e`！** 若 VS Code 已開啟該檔案，按 `e` 會因編輯器衝突卡死。故意演示按 `e` 卡住並用 `Ctrl+C` 解救。
2. **Kanban 審查團隊（Project 08）**：
   ```bash
   code ~/claude-code-complete-tutorial/Projects/08-agent-team-review
   # 4人 team（backend/frontend/test/docs）照 SPEC.md 蓋看板，看契約對齊
   ```
3. **原生 Agent Teams：arXiv 論文閱讀器（跨技術棧平行開發）**：
   ```bash
   code ~/claude-code-complete-tutorial/agent_teams/ios-app-flutter-dev
   # 開啟：agent-team-playbook.md 與 arxiv-1-完成版/
   ```
   - 解說 Team Lead 如何先凍結 `lib/shared/` 契約與 API 模型，再讓 3 個獨立隊友（backend-owner、reader-owner、breathing-owner）在各自資料夾平行推進，透過 Mailbox 互傳進度。

> **教學金句**：「Sub-agent 是派分身交報告，彼此不通氣；Agent Teams 是一群獨立 Claude 共享任務板，邊做邊互相喊話對齊契約。」

### H7 Part 8 Skills 技能三層次 ＋ Matt Pocock 28萬星 AI PM 實戰方案（切三次 ＋ 案例演練）

#### 1. 前半段：技能結構的三層遞進
| 切第幾次 | 開資料夾 → 檔 | 重點學習目標 |
|---|---|---|
| 1. 最小 Skill | `Projects/03-youtube-notes/` → `.claude/skills/youtube-notes/SKILL.md` | 最簡長相：YAML frontmatter 宣告 ＋ 純文字指引 |
| 2. Production 級 | `Projects/07-weekly-reports-skill/` → `README.md` | 完整工程結構：包含 `scripts/`（Python 輔助）與 `references/`（樣板規格） |
| 3. CLI + 圖譜工具包 | `Projects/build-gitnexus-skill-commandline/` → `README.md` | 怎麼把代碼知識圖譜包成可分發的 slash command + helper skill |

#### 2. 後半段：Matt Pocock 專屬技能體系詳細用法與實戰案例 ⭐
> **教學情境**：以開發「**多租戶 Webhook 通知系統（Tenant Webhook System）**」為例，示範 Matt Pocock（`mattpocock/skills`）從規格到上線的完整 6 步工程閉環：

```
[Step 1 領域建模] ─── GLOSSARY.md 鎖定 Tenant, Webhook, Retry, Delivery 等名詞
       │
       ▼
[Step 2 規格生成] ─── /to-spec 訪談沉澱為 SPEC.md（標定測試接縫 Seams）
       │
       ▼
[Step 3 相依圖拆解] ── /to-tickets 拆成帶 Blocked by 的任務相依圖（Ticket Graph）
       │
       ▼
[Step 4 並行派工] ─── /implement-spec 自動辨識 Unblocked 任務，多 Sub-agents 並行 TDD
       │
       ▼
[Step 5 證據 PR] ──── /pr 產出架構圖 + 終端測試 output + 單向門/雙向門風險分級
       │
       ▼
[Step 6 閉環復盤] ─── /retro 掃描對話日誌，輸出環境修訂處方（修環境，不修程式）
```

##### 具體步驟與操作語法：

* **Step 1：定義領域辭典 `GLOSSARY.md`（防止 AI 概念漂移）**
  ```markdown
  # GLOSSARY.md
  - **Tenant**：獨立計費與授權的工作區主體，擁有全域唯一的 TenantID。
  - **WebhookEndpoint**：由客戶登記用來接收事件回調的 HTTPS URL。
  - **DeliveryAttempt**：單次 HTTP POST 發送紀錄，包含 HTTP Status 與耗時。
  ```
  > ⚠️ **講師提示**：過去叫 `CONTEXT.md`，Matt Pocock v1.3 已正式更名為 `GLOSSARY.md`，避免與 LLM Context 混淆。

* **Step 2：執行 `/to-spec` 產生結構化 PRD**
  終端輸入：`> /to-spec`。Claude 根據對話紀錄輸出標準規格 `SPEC.md`，嚴格規範：
  1. Problem Statement（從使用者視角說明痛點）
  2. Solution 與 User Stories（清單化故事）
  3. Testing Seams（只在最頂層 API 接縫進行整合測試，嚴禁過度 Mock）

* **Step 3：執行 `/to-tickets` 拆解相依性工單（Ticket Graph）**
  終端輸入：`> /to-tickets SPEC.md`。輸出宣告了 `Blocked by:` 的任務清單：
  ```markdown
  - [ ] Task 1: Webhook 資料模型與 Migration (Blocked by: None)
  - [ ] Task 2: 後端簽章驗證與發送佇列 /api/webhooks (Blocked by: Task 1)
  - [ ] Task 3: 前端端點設定與 Secret 檢視畫面 (Blocked by: Task 1)
  - [ ] Task 4: 端到端重試與 Exponential Backoff 測試 (Blocked by: Task 2)
  - [ ] Task 5: 驗收與整合收斂 (Blocked by: Task 3, Task 4)
  ```

* **Step 4：執行 `/implement-spec` 啟動相依感知並行派工**
  終端輸入：`> /implement-spec SPEC.md`。
  1. Claude 偵測到 Task 1 是唯一的 Unblocked 任務，先專注完成 Task 1。
  2. Task 1 綠燈後，Claude 立即辨識出 **Task 2 與 Task 3 同時解鎖**！
  3. 自動生成 2 個 Sub-agents 並行施工（一個寫後端 API，一個切前端 UI），各自擁有乾淨 Context，互不污染。
  4. 兩者回報完成後，自動解鎖 Task 4 與 Task 5 進行全鏈條驗收。

* **Step 5：執行 `/pr` 產出高信任度證據導向 PR**
  開發完成後輸入：`> /pr`。Claude 自動抓取 git diff 與測試日誌，生成三區塊審查文件：
  1. **架構 Mermaid 圖**：視覺化 Tenant $\rightarrow$ WebhookQueue $\rightarrow$ Target URL 流向。
  2. **客觀證據（Evidence）**：貼上 `uv run pytest tests/test_webhooks.py` 終端真實輸出（`7 passed in 0.38s`）。
  3. **門禁分級（Door Classification）**：
     - 🚪 **雙向門（低風險）**：前端端點設定畫面 CSS 與按鈕重排。
     - 🚨 **單向門（高風險/架構不可逆）**：新增 `webhook_delivery_attempts` 資料表與索引，請人類 Reviewer 重點審查此處與回滾腳本。

* **Step 6：執行 `/retro` 復盤工作階段（修環境，不修程式）**
  收尾時輸入：`> /retro`。Claude 分析本次對話中的摩擦力，輸出具體處方：
  - 「偵測到測試時一度找不到金鑰：已在 `.env.example` 補上 `WEBHOOK_SIGNING_SECRET`」
  - 「偵測到對話讀取了大型 sqlite db：已在 `.gitignore` 補上 `*.sqlite3`」
  - 「已在 `CLAUDE.md` 補上不可妥協規則：所有 Webhook payload 必須帶 HMAC-SHA256 簽章」

> **教學金句**：「Matt Pocock 方案把工程師從『點單員』拉回『指揮官』——用相依圖調度施工隊、用單向門標定風險、用復盤固化環境。」



### H8 Part 9 Hooks 生命週期與自動化防護欄（切兩處）⭐
- **重點**：Hook 是「管 Claude 的缰繩（Harness）」。8 大生命週期事件（UserPromptSubmit, PreToolUse, PostToolUse, Stop, SessionStart...）。
- **實戰指令**：
  ```bash
  code ~/claude-code-complete-tutorial/Projects/04-pomodoro
  # 觀察 .claude/hooks/ 腳本與 settings.json 的綁定
  # 示範本 repo 的 .claude/hooks/guard-secrets.sh
  ```
- **卡點**：寫了 hook 卻沒執行 → **故意先不寫進 `settings.json`**，跑一次沒反應，補上設定後立即生效。強調 `/hooks` 只是唯讀檢視器，新增必須改 json。

### H9 Part 10 MCP 整合 + Part 12 Agent SDK（切兩次）
1. **MCP 自建與連線**：
   ```bash
   code ~/claude-code-complete-tutorial/Projects/05-organize-downloads
   # 使用 claude mcp add 加入 filesystem server
   ```
   > ⚠️ **MCP 核心鐵則**：自寫 MCP Server 絕不可將 log 印到 `stdout`（會干擾 JSON-RPC 通訊協定導致掛死），所有 debug 訊息必須導向 `stderr`！
2. **Agent SDK 程式整合**：
   ```bash
   code ~/claude-code-complete-tutorial/Projects/06-discord-dm-bot
   # 展示如何用 Python/uv 將 Claude 包入 Discord Bot 商業邏輯
   ```

### H10 Part 11（前半）Plugins 生態 + superpowers 14 招
- **重點**：Marketplace 商店機制、Plugin 的安裝與版本管理；剖析 `superpowers` 的核心心法。
- **實戰指令**：
  ```bash
  code ~/claude-code-complete-tutorial/Projects/plugins-from-zero-to-marketplace
  code ~/claude-code-complete-tutorial/important-plugins/superpowers
  # 閱讀：important-plugins/superpowers_walkthrough.md
  ```
- **核心設計**：深入解構 `brainstorming/SKILL.md` 的 **HARD-GATE**（強制要求探討替代方案）與 **Anti-Pattern**（防止 Claude 偷懶交出簡化架構）。

### H11 Part 11（後半）Pomocat 案例 ＋ TimeTrace 全組件 SaaS 一鏡到底
1. **Pomocat 生產實踐**：
   ```bash
   code ~/claude-code-complete-tutorial/important-plugins/project1-superpowers
   # 對照 docs/superpowers/specs/ 與 docs/superpowers/plans/
   # 搭配 important-plugins/superpowers_production_walkthrough.md
   ```
2. **TimeTrace 全組件一鏡到底（Project 09）**：
   ```bash
   code ~/claude-code-complete-tutorial/Projects/09-timetrace
   # 開啟：Projects/09-timetrace/WALKTHROUGH.md
   ```
   - **高潮講授**：串聯 Agents Team（需求 Spike）→ Skills（流程沉澱）→ MCP（Postgres/GitNexus）→ Hooks（合規攔截）→ Claude Design（UI 切版回 React）。

> **教學金句**：「**Agents 解決速度、Skills 解決重複、MCP 解決連線、Hooks 解決信任、Design 解決美感。**五件事串成一條工作流，才是現代 AI 工程。」

### H12 Part 18 Context Engineering 實戰 + Part 19 收尾
- **重點**：從 Prompt Engineering（把問題說清楚）躍升為 Context Engineering（把工作環境鋪好）。
- **實戰指令**：
  ```bash
  code ~/claude-code-complete-tutorial/agent_group_projects/computer-vision-wafer-detection
  # 對照 CLAUDE.md 與 INITIAL.md
  # 解構 PRP 流程：INITIAL.md → /generate-prp → PRP.md → /execute-prp
  ```
- **收尾**：發放學員角色建議，開放現場 Q&A。

---

## 整合 Demo：一條龍切換節奏心法

整堂 12 小時課的核心節奏就是以下循環：

```
[PPT 講解觀念] 
       │ (講透「為什麼」，建立心智模型)
       ▼
[看見 Footer 提示燈：▶ 實戰演練：<路徑>]
       │
       ▼
[停頓 30 秒] ─── 給學員切換螢幕與心理準備
       │
       ▼
[切 IDE 開指定資料夾]
       │ ── 展開 .claude/ 目錄，看真實檔案（yaml / sh / json）
       ▼
[終端跑真實流程] ─── (H3/H5 留學員操作，其餘講師示範)
       │
       ▼
[踩坑示範 + 秒救] ─── (故意改爛檔案、故意不重啟、故意按錯鍵)
       │
       ▼
[切回 PPT 進入下一個主題]
```

---

## 卡點對照表 ⭐（12 小時切換刀的真實避坑清單）

| 發生階段 | 遇到的卡點現象 | 底層真實原因 | 現場 10 秒救急法 |
|---|---|---|---|
| **H1** | 終端顯示 `claude: command not found` | npm 全域 bin 或二進位安裝檔未加入 `$PATH` | 執行 `which -a claude`，手動補齊 `export PATH="$PATH:$(npm bin -g)"` |
| **H1** | 瀏覽器授權登入轉圈卡住 | 企業內網或 Proxy 攔截 OAuth 回調 | 切換為手動設定環境變數 `export ANTHROPIC_API_KEY="sk-..."` |
| **H2** | 輸入 `@` 檔名沒有跳出補全清單 | 專案目錄檔案過多或模糊搜尋延遲 | 多打 2–3 個字元縮小範圍觸發 fuzzy 搜尋 |
| **H3** | 新寫的自訂 Slash 指令打不出來 | Claude Code 在 session 中會快取 commands | 退出 REPL（打 `exit` 或 `Ctrl+D`）重新啟動 `claude` |
| **H4** | `settings.local.json` 被 git 追蹤到 | 專案根目錄 `.gitignore` 漏設 | 在 `.gitignore` 加入 `.claude/settings.local.json` 並 `git rm --cached` |
| **H5** | 發出提問後 Claude 沒有呼叫 Sub-agent | agent frontmatter 的 `description` 關鍵字太模糊 | 補強 description，寫入具體「當使用者詢問 X 或要求 Y 時」 |
| **H6** | 在 `/agents` TUI 存檔時按下 `e` 導致終端卡死 | VS Code 或背景編輯器正鎖定該 markdown 檔案 | 按 `Ctrl+C` 強制中斷，重來並強調**存檔一律按 `s`** |
| **H6** | 執行 PyTorch 訓練報 MPS 算子不支援 | Apple Silicon 晶片缺少部分底層 GPU 算子 | 終端設定 `export PYTORCH_ENABLE_MPS_FALLBACK=1` 降級 CPU 運算 |
| **H6** | 原生 Agent Teams 無法啟動 | 未開啟設定旗標或版本過低 | 檢查設定檔或設定 `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |
| **H7** | Skill 目錄建好後 Claude 完全不讀 | YAML frontmatter 語法格式有誤或缺少 `name` | 用 linter 檢查，確保前後有完整的 `---` 分隔線 |
| **H7** | 找不到 `CONTEXT.md` 領域詞彙表 | Matt Pocock 規範 v1.3 已正式更名為 `GLOSSARY.md` | 執行 `git mv CONTEXT.md GLOSSARY.md` 即可對齊最新 Skill |
| **H8** | 寫好 hook 腳本測試完全沒反應 | 腳本只放在 `.claude/hooks/` 卻未在 `settings.json` 註冊 | 在 `settings.json` 的 `"hooks"` 物件下綁定事件與腳本路徑 |
| **H9** | MCP Server 啟動報連線中斷 | Server 腳本把 print/log 印到了 `stdout` | 將所有除錯 log 改印到 `sys.stderr` 或寫入獨立 log 檔 |
| **H10** | 安裝 Marketplace Plugin 提示找不到 | 尚未將官方或第三方市集 repo 加入索引 | 先跑 `/plugin marketplace add anthropics/claude-plugins-official` |
| **H11** | 執行 Python 範例報 ModuleNotFoundError | 現代規範強制走 `uv`，誤用了全域 pip | 執行 `uv venv` 建立環境，再用 `uv run` 或 `uv pip install` |
| **H12** | 找不到 `/generate-prp` 指令 | 尚未將 Context Engineering 的 commands 複製進專案 | 將 `context-engineering-intro/.claude/commands/` 複製到本專案 |

---

## 講師私房筆記

### 1. 節奏控制與體力分配
- **H1–H3（上午前段）**：學員注意力最集中。務必穩扎穩打，H3 的自訂 command 練習**寧可少講 5 分鐘投影片，也要讓每個人親手跑出自己的第一個 command**。
- **H4–H6（上午後段）**：多 Agent 與 Agent Teams 觀念密集。切 IDE 前一定要有「30 秒暫停」，避免學員掉隊。
- **H7–H9（下午剛開場）**：學員容易飯後昏睡。用 Hooks 擋寫入機密（guard-secrets）、以及 MCP 接檔案系統的生動 demo 抓回注意力。
- **H10–H12（下午結尾）**：全課高潮。TimeTrace 一鏡到底與 Context Engineering 是全場最具價值的工程落地方案，留足時間並做好 Q&A。

### 2. 故意踩坑（比口述有效十倍）
- **踩坑 1（H3）**：改完 command 故意不重啟，讓終端顯示 command not found，全班大笑之餘永久記住「加 command 要重啟」。
- **踩坑 2（H5）**：刻意把 sub-agent description 寫成「負責處理任務」，詢問食譜時主對話自己回答了，現場改成精確關鍵字後秒被委派。
- **踩坑 3（H8）**：故意只放 hook 腳本不改 `settings.json`，讓學員看見空轉，理解 hook 的配置宣告機制。

### 3. 不同學員角色的帶課指引
| 學員主要背景 | 最有共鳴的章節 | 課堂重點關照點與課後建議 |
|---|---|---|
| **全端工程師** | H3 自訂指令、H8 Hooks、H9 MCP、H11 TimeTrace | 鼓勵將 Pre-commit hook、API 規範檢查與 Next.js/FastAPI 開發流程串接 |
| **AI / 資料工程師** | H5–H6 Wafer ML 流水線、H12 Context Engineering | 專注於多階段資料處理、標註、訓練、驗收的自動化防護與 MPS 算子相容 |
| **技術 PM / 架構師** | H6 Agent Teams、H7 Matt Pocock AI PM 方案、H10 Superpowers、H12 PRP | 強調規格相依性派工（`/implement-spec`）、單向門/雙向門 PR 審查防線、閉環復盤（`/retro`）與領域通用語言（`GLOSSARY.md`） |
| **DevOps / SRE** | H4 Settings、H8 Hooks 阻擋機密、H9 Headless 自動化 | 重點說明 CLI 腳本化、CI/CD 整合、環境變數權限與審計防護 |

### 4. Kevin 親自驗證的真實經驗
- ✅ **「確認存檔按 `s`」**：在 VS Code / Cursor 裡面開著 `.md` 檔案時，在終端 `/agents` 互動中若誤按 `e` 會嘗試叫出外部編輯器，高機率導致終端失去回應。
- ✅ **晶圓 ML 資料集**：Roboflow `wm811k v3` 教學專用版本只包含特定類別且只有 train split，這是教學精簡設計，非下載程式碼損壞。
- ✅ **依賴管理全面 `uv` 化**：不論是 Python MCP Server、FastAPI 後端或是 ML 腳本，統一使用 `uv` 速度提升數倍且避免環境污染。
- ✅ **Superpowers 與 TimeTrace 實戰性**：14 個 Skill、HARD-GATE 檢查點、以及 TimeTrace 的五組件架構均經過完整端到端測試，是真正能帶走的生產力資產。

---

## 一句話總結

> **這份指揮譜給你全景 12 小時與 6 小時的精確導航（19 Part → 雙軌作戰時鐘、何時切 IDE、哪刀會卡）；逐分鐘教案見 `course_12hr_walkthrough.md`。迷路看全景路線，卡住看卡點表，超時看砍場順序——一個人也能把公開課穩穩交出旗艦級水準。**

---

## 配套教材與進階閱讀

- 🔗 [`docs/walkthroughs/course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md) — 逐小時放大鏡（Hour 1–12 逐分鐘腳本、金句、Q&A 逐字稿）
- 🔗 [`docs/walkthroughs/matt_pocock_ai_pm_skills_walkthrough.md`](docs/walkthroughs/matt_pocock_ai_pm_skills_walkthrough.md) — Matt Pocock 28 萬星 AI PM 方案（Spec 驅動開發 × 證據 PR × 閉環復盤）⭐
- 🔗 [Gary Chen YouTube 拆解影片：28 萬星的 Matt Pocock skill 更新拆解！](https://www.youtube.com/watch?v=QqhyqMvdx5Q)
- 🔗 [`Projects/09-timetrace/WALKTHROUGH.md`](Projects/09-timetrace/WALKTHROUGH.md) — TimeTrace 一鏡到底蓋 SaaS 藍圖（3 小時旗艦實戰）
- 🔗 [`Projects/README.md`](Projects/README.md) — 9 個 Mini-Projects 與進階工具包總覽
- 🔗 [`agent_teams/README.md`](agent_teams/README.md) — 原生 Agent Teams 跨技術棧（arXiv 每日論文閱讀器）實戰指南
- 🔗 [`agent_teams/ios-app-flutter-dev/agent-team-playbook.md`](agent_teams/ios-app-flutter-dev/agent-team-playbook.md) — 原生 Agent Teams 現場帶課逐字手冊
- 🔗 [`docs/walkthroughs/agent_team_walkthrough.md`](docs/walkthroughs/agent_team_walkthrough.md) — 4 人 Agent 團隊照 SPEC 蓋 Kanban 看板
- 🔗 [`docs/walkthroughs/hook_walkthrough.md`](docs/walkthroughs/hook_walkthrough.md) — Hooks 8 種事件與生命週期深入剖析
- 🔗 [`important-plugins/superpowers_production_walkthrough.md`](important-plugins/superpowers_production_walkthrough.md) — Superpowers 14 招心法與 Pomocat 落地全流程
- 🔗 [`agent_group_projects/computer-vision-wafer-detection/WALKTHROUGH.md`](agent_group_projects/computer-vision-wafer-detection/WALKTHROUGH.md) — 晶圓瑕疵檢測 4-Agent ML 流水線
- 🔗 [`Claude_Code_建構指南.md`](Claude_Code_建構指南.md) — 完整功能架構 Reference

---

_Last updated: 2026-10-24（全面健全化雙軌作戰表、補齊 Project 09 TimeTrace SaaS 全組件一鏡到底、整合原生 Agent Teams arXiv 實戰與 2026 最新生態規範）_  
_Maintainer: Kevin ([@kevin801221](https://github.com/kevin801221))_  
_對應主簡報：`Claude_Code_完整教學.pptx`（338 頁・19 Part）_
