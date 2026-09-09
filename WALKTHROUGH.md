# 教學總指揮譜 — Claude Code 公開課（12 小時作戰版 ＋ 6 小時逐分鐘精華表）

> ⏱ **只有 6 小時的看這裡**：直接跳到下方 [**6 小時時時刻刻作戰表**](#6-小時時時刻刻作戰表一日精華版)——一張表告訴你每個時段在講哪個 Part、什麼時候切 IDE、開哪個資料夾、何時休息。12 小時的全景與各 Part 細節仍在後面，6 小時表會回指到它們。

> **對象**：要拿這套教材**親自交完一整天 12 小時課**的講師（就是你）
> **形式**：講師現場帶。開課時這份開在第二螢幕（或印出來）跟著走
> **時長**：12 × 60 分鐘 session（純內容 ~11h，含休息 12h）
> **產出**：你能「按正確順序」帶完整片 codebase——什麼時候講 PPT、什麼時候切 IDE、開哪個資料夾、開哪個檔、學員會在哪卡住、卡了怎麼救
> **核心方法**：PPT 講觀念（為什麼）→ 切 IDE 跑真實檔案（怎麼做）→ 學員當場敲（記得住）
> **跟現有教材的關係**：
> - **這份（指揮譜）** = 鳥瞰圖。一張表看完 19 個 Part 對到哪個 Hour、切不切 IDE、開哪個資料夾、那一刀最容易卡哪。**帶課時主看這份。**
> - **[`docs/walkthroughs/course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md)** = 逐小時放大鏡。每個 Hour 細到「0–15 min 做什麼、教學金句逐句、預期 Q&A」。**備課時細讀那份、某小時卡住翻那份。**
> - 兩份**分工不重複**：指揮譜給你方向感，12h 教案給你逐分鐘腳本。

---

## 開場（讀這份前先懂）：為什麼要兩份？

一個人帶 12 小時課，最怕兩件事：**①「現在到底該講 PPT 還是切 IDE？」迷路**、**②某一刀切下去學員集體卡住、你手忙腳亂**。

| 你需要的東西 | 看哪份 |
|---|---|
| 全局方向感（現在第幾 Part、切不切、開哪） | **這份指揮譜的「全景路線圖」表** |
| 某個 Hour 的逐分鐘腳本 + 金句逐句 | `course_12hr_walkthrough.md` 對應 Hour |
| 切 IDE 那一瞬間學員會卡什麼、怎麼秒救 | **這份每個 Part 的「這一刀的卡點」** |
| 時間不夠要砍哪 | **這份「應變：時間不夠怎麼砍」** |

> **教學金句**：「指揮譜是地圖、12h 教案是逐步導航。開車看地圖確認方向，路口才聽導航——別把導航當地圖一路盯著，會撞牆。」

---

## 📁 12 小時全景路線圖（這張表是你的整堂課儀表板）

PPT 共 **338 頁**、**19 個 Part**、**8 個 Projects**、**6 個 agent 案例**。下表把 Part 對到 Hour、標明切不切 IDE、切了開哪。

> ⚠️ **頁碼會漂移**（PPT 一直在長：318 → 320 → 338）。**不要死記頁碼**——認三件事就不會迷路：① Part 名稱 ② PPT 章節分隔頁（深色 navy 底）③ 每頁 footer 的 `▶ 實戰演練：<路徑>`（看到它＝這個 Part 有資料夾可切）。下表頁碼是「**約略區段**」，僅供抓節奏。

| Hour | PPT Part | 約略頁段 | 主題 | 切 IDE？ | 開哪個資料夾 → 開哪個檔 |
|---|---|---|---|---|---|
| **H1** | 開場 + Part 1 | 1–約25 | 認識 Claude Code | ❌ 純 PPT + 終端 demo | — |
| **H2** | Part 2–3 | 約26–60 | CLI 基礎 + 內建 Slash Commands | ❌ 純 PPT + 終端 demo | — |
| **H3** | **Part 4** | 約61–75 | **自訂 Slash Commands** | ✅ **本課第一次切** | `Projects/01-weekly-haiku/` → `README.md` |
| **H4** | Part 5–6 | 約76–110 | Settings + CLAUDE.md / Memory | 半切（開本 repo `.claude/`） | 本 repo 根 → `.claude/settings.json` ＋ `CLAUDE.md` |
| **H5** | **Part 7（前半）** | 約111–135 | **Sub-agents 入門** | ✅ 切 | `Projects/02-recipe-genie/` → `README.md` |
| **H6** | **Part 7（後半）** | 約136–160 | **多 agent 真實案例 + Agent Teams** | ✅ 切兩次 | ① `agent_group_projects/computer-vision-wafer-agents-detection-demo/` → `WALKTHROUGH.md`<br>② `Projects/08-agent-team-review/` → `README.md` |
| **H7** | **Part 8** | 約161–185 | **Skills × 3 範例** | ✅ 切三次 | ① `Projects/03-youtube-notes/` ② `Projects/07-weekly-reports-skill/` ③ `Projects/build-gitnexus-skill-commandline/`（皆開 `README.md`） |
| **H8** | **Part 9** | 約186–215 | **Hooks** | ✅ 切 | `Projects/04-pomodoro/` → `README.md`（加碼：本 repo `.claude/hooks/README.md` 真實啟用範例） |
| **H9** | **Part 10 + Part 12** | 約216–245 ＋ 約300–315 | **MCP + Agent SDK** | ✅ 切兩次 | ① `Projects/05-organize-downloads/` ② `Projects/06-discord-dm-bot/`（皆開 `README.md`） |
| **H10** | **Part 11（前半）** | 約246–280 | **Plugins 入門 + superpowers 14 招** | ✅ 切兩次 | ① `Projects/plugins-from-zero-to-marketplace/` → `README.md`<br>② `important-plugins/superpowers/` ＋ `important-plugins/superpowers_walkthrough.md` |
| **H11** | **Part 11（後半）+ Part 13–17** | 約281–299 ＋ 散段 | **Pomocat 真實案例 + 進階雜項** | ✅ 切 | `important-plugins/project1-superpowers/` ＋ `important-plugins/superpowers_production_walkthrough.md` |
| **H12** | **Part 18 + Part 19** | 約316–338 | **Context Engineering 實戰 + 收尾** | ✅ 切 | `agent_group_projects/computer-vision-wafer-detection/` → `WALKTHROUGH.md`（或 `context-engineering-intro/`） |

> **快速心法**：H1–H2、H4 的 Part 5–6、H11 的 Part 13–17 是「**講觀念**」→ 留 PPT。H3、H5–H10、H12 是「**動手做**」→ 講完概念就切 IDE。**每個 Hour 的逐分鐘腳本去 [`course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md) 看對應 Hour。**

---

## 6 小時時時刻刻作戰表（一日精華版）

> **什麼時候用**：你只有 6 小時要把整套帶完（一日精華場）。
> **取捨原則**（沿用下方「應變砍場順序」）：保住 **6 大支柱**（slash / sub-agent / skill / hook / MCP / plugin）＋ **絕不砍的 Part 1 / 4 / 6 / 9**；**只在 Part 4 留學員自己敲**，其餘案例一律「**開 README 口頭帶、不 live 跑**」；Part 13–17 整段不講（給連結自學）；Part 18 只講概念不實作。
> **若你的 6 小時是兩日課的「下半場」**（學員已上過 Part 1–6）：直接從 **2:00 的 Part 7** 開始，把省下的 2 小時還給 Part 7 多 agent 案例、Part 11 plugin 實裝、Part 18 完整實作。
>
> 時間欄是「從開課算起的時鐘」（0:00 = 上課鐘響）。**頁碼不要死記**，認 Part 名稱 + footer 的 `▶ 實戰演練` 就好。

| 時鐘 | 時長 | PPT Part | 主題 | 切 IDE？開哪 | 這刀重點 / 卡點 |
|---|---|---|---|---|---|
| **0:00–0:20** | 20m | 開場 + Part 1 | 認識 Claude Code | ❌ PPT + 終端 demo | 開場一句話：今天你會帶走 6 個能動手的東西。demo `claude` 起手、`@` 檔案 |
| **0:20–0:35** | 15m | Part 2–3 | CLI 基礎 + 內建 slash | ❌ PPT + 終端 demo（飛快） | `@` 補全太快不跳 → 多打幾字觸發 fuzzy |
| **0:35–1:15** | 40m | **Part 4** ⭐ | **自訂 Slash Commands** | ✅ **第一次切**：`Projects/01-weekly-haiku/` | 唯一保留「**學員自己敲**」的一段。故意改完不重啟 → `/cmd` 找不到 → 退出再進 |
| **1:15–1:35** | 20m | Part 5–6 | Settings + CLAUDE.md / Memory | 半切：本 repo `.claude/settings.json` ＋ `CLAUDE.md` | Part 6 Memory 絕不砍——這是最實用的一段 |
| **1:35–1:45** | 10m | — | ☕ **休息** | — | 切換場地心情，agent 段在後面 |
| **1:45–2:30** | 45m | **Part 7** | **Sub-agents（入門 + 案例口頭）** | ✅ 切 `Projects/02-recipe-genie/`；案例口頭開 `agent_group_projects/` README | 故意把 agent description 寫爛 → 不觸發 → 改明確觸發句 → 秒上。wafer / stock 案例**只開 README 口頭帶** |
| **2:30–3:05** | 35m | **Part 8** | **Skills** | ✅ 切 `Projects/03-youtube-notes/`；07 / gitnexus 口頭 | skill 沒自動觸發 → description 加「Use when X」明確情境 |
| **3:05–3:45** | 40m | **Part 9** ⭐ | **Hooks** | ✅ 切 `Projects/04-pomodoro/` ＋ 本 repo `.claude/hooks/README.md` | 絕不砍。故意只放 `.claude/hooks/` 不註冊 `settings.json` → 沒效果 → 加註冊才 work |
| **3:45–3:55** | 10m | — | ☕ **休息**（或午休錨點） | — | 下半場是 plugin 高潮，先回血 |
| **3:55–4:25** | 30m | **Part 10** | **MCP** | ✅ 切 `Projects/05-organize-downloads/` | `claude mcp add` 一行裝完；server 印 log 到 stdout 會連不上 → 改 stderr |
| **4:25–5:20** | 55m | **Part 11** ⭐ | **Plugins + 三大熱門 plugin** | ✅ 切 `Projects/plugins-from-zero-to-marketplace/` ＋ `important-plugins/` | 用 [`important-plugins/plugins_install_and_cases_walkthrough.md`](important-plugins/plugins_install_and_cases_walkthrough.md)：marketplace add → install → 三個案例 |
| **5:20–5:35** | 15m | Part 12 | Agent SDK（快帶） | ✅ 切 `Projects/06-discord-dm-bot/`（口頭/快） | 只講「SDK = 把 Claude 包進你的程式」，不 live |
| **5:35–6:00** | 25m | Part 18 + Part 19 | **Context Engineering（概念）+ 收尾** | ❌ 概念為主（時間夠才切 `context-engineering-intro/`） | 收尾用「學員角色表」點名給個人化建議 + Q&A |

> **快速心法**：0:00–0:35、1:15–1:35、5:35–6:00 是「**講觀念**」段 → 留 PPT；0:35 起的每個切換點 → 講完概念就切 IDE，用 footer 的 `▶ 實戰演練` 當提示燈。每段想要逐分鐘金句，回查 [`course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md) 對應 Hour（6h 版的 Part 對映 12h 版同名 Part）。

### 逐段講師動作（照著做就不會迷路）

**0:00–0:35｜暖身（不切 IDE）**
開場 30 秒立規矩：「今天 6 小時，你會親手碰到 6 樣東西——自訂指令、分身、技能、hook、MCP、plugin。」Part 1 配終端 demo（`claude` 起手、`@` 帶檔、一段對話），Part 2–3 把內建 slash 與模式切換**飛快帶過**，不要在這裡耗——精華在後面。

**0:35–1:15｜Part 4 第一次切 IDE（全課引爆點，唯一留練習）⭐**
PPT 講完 frontmatter 三件套（`name`/`description`/`allowed-tools`）＋ `$ARGUMENTS`，footer 跳 `▶ 實戰演練：Projects/01-weekly-haiku/` → **暫停 30 秒** → 切 IDE 開 `weekly-haiku.md` → 終端跑 `/weekly-haiku` → **留 10 分鐘讓學員把它複製成 `daily-mood.md` 改一個自己的**。故意先不講「要重啟」，讓他踩，再現場退出 `claude` 再進——勝過你講十次。

**1:15–1:35｜Part 5–6 半切（Memory 絕不砍）**
不開 Projects，直接開**本 repo 自己的** `.claude/settings.json` ＋ `CLAUDE.md`——這份教材本身就是最好的真實範例（掛了 hook、會觸發 skill）。重點打在 Part 6：CLAUDE.md / Memory 怎麼讓 Claude「記住專案規則」。

**1:45–2:30｜Part 7 Sub-agents（入門 live + 案例口頭）**
切 `Projects/02-recipe-genie/` 看 agent 的 system prompt + tool list + model；現場**故意把 description 寫成「處理事情」** → Claude 不觸發 → 改成明確觸發句 → 秒上，對比張力最大。剩 10 分鐘**開 README 口頭帶**多 agent 真實案例（`agent_group_projects/computer-vision-wafer-detection/`、`stock-groups-skills/`）＋ Agent Teams 概念（`Projects/08-agent-team-review/`、`agent_teams/`），**不 live 跑**（live 是 12h 才有的奢侈）。

**2:30–3:05｜Part 8 Skills**
切 `Projects/03-youtube-notes/` 看 `SKILL.md` 的資料夾結構與自動觸發；production 級（`07-weekly-reports-skill/`）與 `build-gitnexus-skill-commandline/` 口頭帶過。金句：「skill＝把做法打包成會自動觸發的能力。」

**3:05–3:45｜Part 9 Hooks（絕不砍）⭐**
切 `Projects/04-pomodoro/` 看 shell script + `settings.json` 的 hooks 物件怎麼綁；**故意只放腳本不註冊** → 跑沒效果 → 加註冊才 work。加碼開本 repo `.claude/hooks/README.md`（8 支腳本對照表、真實啟用的 guard-secrets / notify-done）。金句：「hook 不會問 Claude 同不同意才跑——它是『管 Claude 的 harness』。」

**3:55–4:25｜Part 10 MCP**
切 `Projects/05-organize-downloads/`，示範 `claude mcp add` 一行接外部資料源。強調「MCP＝給 Claude 接外部工具/資料的標準插座」。

**4:25–5:20｜Part 11 Plugins + 三大熱門 plugin（下半場高潮）⭐**
先切 `Projects/plugins-from-zero-to-marketplace/` 講「自己做 plugin → 發 marketplace」。接著切 `important-plugins/`，**直接照 [`plugins_install_and_cases_walkthrough.md`](important-plugins/plugins_install_and_cases_walkthrough.md) 帶**：
1. **marketplace add**：`anthropics/claude-plugins-official`、`anthropics/claude-code`、（備）`obra/superpowers-marketplace`
2. **install**：`superpowers@claude-plugins-official`、`ralph-wiggum@claude-code-plugins`、`pr-review-toolkit@claude-plugins-official`
3. **三個案例**：ralph live 跑一個小 `/ralph-loop`（設 `--max-iterations` 當保險絲）→ `/pr-review-toolkit:review-pr` 對改動審查 → superpowers 講 brainstorming 的 HARD-GATE。
時間緊就 ralph 一個 live、另兩個口頭。金句：「marketplace 是商店、plugin 是商品、`@` 後面是去哪間店買。」

**5:20–5:35｜Part 12 Agent SDK（快帶）**
開 `Projects/06-discord-dm-bot/README.md` 口頭帶「SDK＝把 Claude 包進你自己的程式」，不 live。

**5:35–6:00｜Part 18 Context Engineering 概念 + Part 19 收尾**
白板畫一次 `CLAUDE.md + INITIAL.md → /generate-prp → PRP.md → /execute-prp → 功能`，**只講概念不實作**（實作是 12h 的高潮，6h 版留概念）。最後用下方「不同學員角色推薦」表點名給個人化建議，發資源連結，收 Q&A。

### 6 小時版的應變（超時就照這個砍）

1. 先砍 **Part 12 Agent SDK**（5:20–5:35）→ 給連結自學，把 15 分鐘還給前面
2. 再砍 **Part 8 第 2/3 個 skill 案例**（只留 youtube-notes）
3. **Part 7 案例全口頭**（recipe-genie 入門仍 live）
4. **絕對不砍**：Part 4 第一次切 IDE（0:35）、Part 6 Memory、Part 9 Hooks、Part 11 plugin 至少 ralph 一個 live
5. 真的大超時：Part 18 從「概念 + 白板」縮成「一句話 + 給 repo 連結」，保住收尾 Q&A

> **教學金句**：「6 小時版的紀律是『**只留一次學員自己敲（Part 4），其餘開 README 口頭帶**』——動手點留給最有引爆力的第一刀，剩下的時間拿來把支柱講滿。」

---

## Phase 0：開課前置檢查（前一晚就要做，不是當天）

```bash
# ── 講師自己的環境 ──
claude --version                         # 確認最新版
which -a claude && which node            # 確認沒裝重複、PATH 沒撞
open Claude_Code_完整教學.pptx            # 338 頁能開、字型沒破
code ~/claude-code-complete-tutorial     # IDE 開好整個 repo

# ── 提前裝（現場裝＝教學車禍第一名）──
/plugin install superpowers@claude-plugins-official
/plugin install document-skills@anthropic-agent-skills

# ── 備用 session（H6/H12 跑 agent 用）──
cd ~/claude-code-complete-tutorial && claude
```

學員端前一晚要交代：
- 預先發 zip（含 8 個 Projects），**不要現場 clone**
- Roboflow API Key 預先申請（H6 wafer 案例會用到）
- VS Code / Cursor 任選，但**講師示範用哪個就要學員裝哪個**

> ⚠️ **H6 跟 H12 是全課最危險的兩段**——agent 跑起來常出意外（網路 / API / 權限）。**前一晚務必把這兩段的 pipeline 親手跑過一次**，不要當天才第一次跑。

> **教學金句**：「現場裝環境是教學車禍第一名——前一晚都裝好，當天只管教。」

---

## Phase 1：第一次切 IDE（H3 · Part 4）⭐ 最詳細——這刀切好整堂課就順

第一次切 IDE 是學員「**啊，原來這就是 Claude Code**」的轉折點。切壞了整天提不起勁，所以這一刀寫到最細。

**PPT 講到**：`.claude/commands/` 結構、frontmatter 三件套（`name` / `description` / `allowed-tools`）、`$ARGUMENTS`。

**講完概念（footer 出現 `▶ 實戰演練：Projects/01-weekly-haiku/`）→ 切 IDE，標準四動作**：

```bash
# ① 切到 IDE（用你跟學員約定好的那個編輯器）
code ~/claude-code-complete-tutorial/Projects/01-weekly-haiku

# ② 開這個檔，對照 PPT 講的 frontmatter
#    Projects/01-weekly-haiku/.claude/commands/weekly-haiku.md

# ③ 開終端，現場跑一次
cd ~/claude-code-complete-tutorial/Projects/01-weekly-haiku && claude
> /weekly-haiku

# ④ 學員自己改一個（最關鍵的 10 分鐘）
#    複製 weekly-haiku.md → daily-mood.md，改內容，重啟 claude，跑 /daily-mood
```

**這一刀的卡點**（學員一定會卡，先預演救法）：

| 卡點 | 真實原因 | 秒救 |
|---|---|---|
| 改完檔 `/daily-mood` 沒出現 | session 沒重啟 | 退出 `claude` 再進（這裡**故意先不講**，讓他踩，再現場退出再進——比講 10 次有效） |
| `$ARGUMENTS` 沒值 | 學員打 `/cmd` 沒帶參數 | 強調 `/cmd 你的參數` 寫法 |
| frontmatter YAML 報錯 | 冒號 / 縮排錯 | 直接複製範例改，不要手刻 |

> **教學金句**：「自訂 slash command＝把你最常用的 prompt 封裝起來。寫一次、所有 session 共用、commit 進 repo 全隊都能用。」

**講完 → 回 PPT 接 Part 4 剩下幾頁 → 進 H4。** 逐分鐘腳本見 [`course_12hr_walkthrough.md` Hour 3](docs/walkthroughs/course_12hr_walkthrough.md)。

---

## Phase 2：其餘 Part 逐站作戰細節（同節奏，加速）

每站只寫三件你帶課當下需要的：**① PPT 講到哪 ② 切 IDE 的精確指令 ③ 這一刀的卡點**。逐分鐘時間分配 / 金句逐句 → 都在 [`course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md) 對應 Hour。

### H1 開場 + Part 1（純 PPT + 終端 demo）

封面 → 前言 → 目錄 **3 分鐘帶過不要逗留**。Part 1 講 Claude Code 是什麼 / vs Cursor / 安裝 / 認證。**現場動作**：終端打 `claude --version`、`claude` 進 REPL 給大家看長相。**不切 IDE。**
**卡點**：學員 `claude` 找不到（npm bin 沒進 PATH，`which -a claude` 排查）／認證卡瀏覽器（公司網路擋，改設 `ANTHROPIC_API_KEY`）。

### H2 Part 2–3（純 PPT + 終端 demo）

Part 2 講 REPL / Print mode / `@` `#` `!` 三記號 / 快捷鍵。Part 3 講內建 slash（`/help` `/clear` `/compact` `/init` `/model` `/agents` `/mcp` `/cost`）。**現場動作**：備用終端真的打 `/help` `/status`、空資料夾跑 `/init` 看自動產 CLAUDE.md。**不切 IDE。**
**卡點**：`@` 補全沒跳（多打幾字觸發 fuzzy）／`/compact` 後 Claude「忘了」（重要規則寫進 CLAUDE.md 不要靠記憶）。

### H3 Part 4 自訂 Slash Commands ⭐ → 見上方 Phase 1（最詳細那段）

### H4 Part 5–6 Settings + CLAUDE.md / Memory（半切）

Part 5 講三層級設定（local > project > user）、permissions 三區塊（allow / deny / ask）、env。Part 6 講 CLAUDE.md、`/memory`、`#`、`@`、auto-memory。
**這裡不切 Projects，改開「本 repo 自己的設定」當活教材**：

```bash
# IDE 同時開三個檔對照（這就是最好的真實範例）
~/.claude/CLAUDE.md                          # 全域：Kevin 個人偏好（uv / 繁中 / commit 不署名）
~/claude-code-complete-tutorial/CLAUDE.md    # 專案：repo 規則（含「本 repo .claude/ 會生效」一節）
~/claude-code-complete-tutorial/.claude/settings.json  # 真的掛了 guard-secrets + notify-done hook
```

> 💡 本 repo 的 `.claude/settings.json` **真的啟用了 hook**（寫 `.env` 會被 `guard-secrets.sh` 擋）——這是 Part 9 Hooks 的最佳預告，H4 先讓學員「看到它存在」，H8 再講原理。
**卡點**：`settings.local.json` 不小心 commit（`.gitignore` 要有）／CLAUDE.md 寫太長 Claude「忘了」（拆子資料夾 CLAUDE.md）。

### H5 Part 7（前半）Sub-agents 入門 → `Projects/02-recipe-genie/`

PPT 講 sub-agent 是什麼、跟主 session 隔離的好處、`.claude/agents/*.md` frontmatter 五件套（name / description / tools / model / color）。

```bash
code ~/claude-code-complete-tutorial/Projects/02-recipe-genie
# 開 .claude/agents/recipe-genie.md 看 system prompt + tool list + model
cd Projects/02-recipe-genie && claude
> 我想吃辣的、半小時內做完、冰箱有雞肉跟蛋   # 預期：自動路由到 @recipe-genie
```

**這一刀的卡點**：

| 卡點 | 真實原因 | 秒救 |
|---|---|---|
| Claude 沒呼叫 agent | description 觸發詞太弱 | **故意**先寫爛（「處理事情」）讓它不觸發，再改成「當使用者要食譜、料理推薦時」秒觸發——對比效果超強 |
| `/agents` 找不到 | tab 沒切到 Agents | 按 `←` 切左邊 tab |
| agent 用錯工具 | 沒設 tools 限制 | 明列 `tools: Bash, Read, Write` |

> **教學金句**：「Sub-agent 不是另一個模型——是『另一個帶不同 system prompt、隔離記憶但共享檔案系統的 session』。」

### H6 Part 7（後半）多 agent 真實案例 + Agent Teams（切兩次）⚠️ 高風險段

**第一次切（Wafer 4-agent live demo）**：

```bash
cd ~/claude-code-complete-tutorial/agent_group_projects/computer-vision-wafer-agents-detection-demo
code .   # 學員開 WALKTHROUGH.md 跟著看，不一起敲（避免拖節奏）
claude
> /agents          # 講師現場走 9 個畫面建 data-hunter
> 幫我從 Roboflow 抓 WM-811K 資料集    # 預期：🔴 @data-hunter 跳出來
```

> ⚠️ **在 `/agents` Confirm 畫面永遠按 `s`，不要按 `e`**——VS Code 開了 .md tab 沒關，按 `e` 會卡死。**講師故意按一次 `e` 示範卡住 + `Ctrl+C` 救回**，學員回去自己踩這坑機率超高，先讓他看一次。

**第二次切（Agent Teams＝Project 08，這是新單元）**：

```bash
code ~/claude-code-complete-tutorial/Projects/08-agent-team-review
# 開 README.md：4 人 team（backend/frontend/test/docs）照 SPEC 從骨架蓋 Kanban 看板
```

Project 08 的教法：**set 一個 4 人 agent team，丟一份 Kanban SPEC 讓它從骨架蓋完**。一小時內當堂跑完，重點看三個好處——隊友直接對齊契約、backend 完成後下游三個並行解鎖、各自獨立 context 不污染主對話。深講看 [`docs/walkthroughs/agent_team_walkthrough.md`](docs/walkthroughs/agent_team_walkthrough.md)（60 分鐘完整版）。

> **教學金句**：「sub-agent 各自交報告、互不通氣；agent team 隊友直接喊話對齊契約。要隊友之間講話，才需要 team。」

**這一刀的卡點**：

| 卡點 | 真實原因 | 秒救 |
|---|---|---|
| 按 `e` 後 Claude Code 停住 | VS Code 開了 .md tab 沒關 | `Ctrl+C` 救回，下次只按 `s` |
| Roboflow 下載卡 0% | 資料夾已存在 + overwrite=False | script 加 `overwrite=True` |
| MPS 不支援某 op | PyTorch + Apple Silicon 限制 | `export PYTORCH_ENABLE_MPS_FALLBACK=1` |
| Agent Teams 開不起來 | 版本 < v2.1.32 或沒開實驗旗標 | 看 `Projects/08-agent-team-review/.claude/settings.json` 的 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` |

### H7 Part 8 Skills（切三次）

PPT 講 skill＝SKILL.md（YAML frontmatter + 指引內容）、跟 sub-agent 差在哪、description 怎麼寫才會被觸發。三次切一站一檔對比：

| 切第幾次 | 開資料夾 → 檔 | 重點 |
|---|---|---|
| 1 最小 skill | `Projects/03-youtube-notes/` → `.claude/skills/youtube-notes/SKILL.md` | 最簡長相 |
| 2 production 級 | `Projects/07-weekly-reports-skill/` → `README.md`（再看 `references/` `scripts/`） | 對比「最小 vs production」差在哪 |
| 3 command + skill 工具包 | `Projects/build-gitnexus-skill-commandline/` → `README.md`（再看 `INSTALL.md`） | 怎麼包成可分享工具包 |

> **教學金句**：「Sub-agent 是『新員工』、Skill 是『員工手冊』——同一個 Claude 翻手冊照做，不開新 session。」
**這一刀的卡點**：skill 沒自動觸發（description 加「Use when 使用者說 X」明確情境）／`/skills` 看不到（沒重啟 session）。
> ⏱ **超時優先砍順序**：時間緊**寧可砍第 3 站（build-gitnexus）也要把第 2 站（production skill）講完整**。

### H8 Part 9 Hooks → `Projects/04-pomodoro/`

PPT 講 8 種 event、兩張澄清頁（「hook event 不是 slash command」「`/hooks` TUI 是 read-only 檢視器」）。

```bash
code ~/claude-code-complete-tutorial/Projects/04-pomodoro
# 看 .claude/hooks/ 的 shell script + settings.json 的 hooks 物件怎麼綁
# 加碼：開本 repo 的 .claude/hooks/README.md（8 支腳本對照表，真實啟用範例）
```
終端打 `/hooks` 給大家看那個 **read-only TUI**，對照 PPT「TUI 只是查看器、加 hook 要去 settings.json」。
> **教學金句**：「Hook 不會問 Claude 同意才跑——它是『管 Claude 的 harness』，Claude 不知道 hook 存在。」
**這一刀的卡點**：「寫了 hook 沒跑」（只放 `.claude/hooks/` 沒在 settings.json 註冊——**故意先不註冊跑一次看沒效果**，再加上才 work）。

### H9 Part 10 MCP + Part 12 Agent SDK（切兩次）

```bash
# MCP
code ~/claude-code-complete-tutorial/Projects/05-organize-downloads   # 看自寫 MCP server + settings.json mcpServers
# Agent SDK
code ~/claude-code-complete-tutorial/Projects/06-discord-dm-bot       # 看 Claude query() 怎麼用，最進階範例
```
> 📌 PPT 順序上 Part 12 在 Part 11 之後，但 12h 教案把 **Part 12 拉到 H9 跟 MCP 一起教**（同屬「接外部」概念群）。帶課時 PPT 跳到 Part 12 頁段即可，回頭 H10–H11 再補 Part 11。
> **教學金句**：「MCP 是『把外部資料源接進 Claude』的標準協議——Anthropic 版的 LSP。」
**這一刀的卡點**：MCP server 連不上（server 千萬別印 log 到 stdout，要 stderr）／Discord bot 沒回應（`.env` token + Discord 端開 message intent）。

### H10 Part 11（前半）Plugins 入門 + superpowers（切兩次）

```bash
code ~/claude-code-complete-tutorial/Projects/plugins-from-zero-to-marketplace   # 3 個範例 plugin 從 0 到上架
code ~/claude-code-complete-tutorial/important-plugins/superpowers               # 配 important-plugins/superpowers_walkthrough.md
# 重點看：skills/brainstorming/SKILL.md 的 HARD-GATE + Anti-Pattern 三招設計手法
```
> 釐清誤會：`~/.claude/plugins/` **存在**，是 Claude Code 自動管的安裝區（marketplaces/ data/ cache/），不是手動放東西的地方。
> **教學金句**：「Superpowers 厲害的不是 14 個 skill，是『SKILL.md 怎麼寫才能讓 Claude 不敢偷懶』——HARD-GATE + Anti-Pattern。」
**這一刀的卡點**：`/plugin install` 失敗（先 `/plugin marketplace add <url>`）／裝了沒效果（沒重啟）。

### H11 Part 11（後半）Pomocat 真實案例 + Part 13–17（純 PPT buffer）

```bash
code ~/claude-code-complete-tutorial/important-plugins/project1-superpowers
ls docs/superpowers/specs/ docs/superpowers/plans/   # brainstorming + writing-plans 的真實產出
# 配 important-plugins/superpowers_production_walkthrough.md（120 分鐘版，時間緊只讀 spec/plan 講解）
```
Part 13–17（IDE 整合 / Headless / Permissions / 進階 / GitHub 資源）是 **buffer 段**：時間緊就純 PPT 飛快帶過，Part 17 可開瀏覽器點幾個 repo 連結。
> **教學金句**：「Pomocat 是 superpowers 自己證明自己——四階段（brainstorm→spec→plan→implement）是真的可用，不是教科書理論。」

### H12 Part 18 Context Engineering 實戰 + Part 19 收尾 ⚠️ 高潮段，留最多時間

```bash
code ~/claude-code-complete-tutorial/agent_group_projects/computer-vision-wafer-detection
cat CLAUDE.md INITIAL.md         # 對照 Part 18·1 + 18·2
# 講師可現場跑 /generate-prp 給大家看（PPT 一頁一步驟，IDE 同步操作）
# 替代教材：context-engineering-intro/（coleam00 原 repo 對照）
```
四步驟流程：CLAUDE.md → INITIAL.md → `/generate-prp` → `/execute-prp`。心法集（PPT Part 18·5）5 條快帶。Part 19 學習路徑 5 分鐘收。
> **教學金句**：「Prompt Engineering 是『把問題講清楚』，Context Engineering 是『把工作環境準備好』——後者一勞永逸。」
**這一刀的卡點**：`/generate-prp` 不存在（`context-engineering-intro` 沒 clone）／INITIAL.md 寫太空泛（強迫先跑 brainstorming skill）。

---

## 整合 demo：12h 一條龍的「切換節奏」

整堂課就是這個節奏循環 11 次（H3–H12 每次切 IDE）：

```
PPT 講概念 → footer 出現 ▶ 實戰演練 → 暫停 30 秒讓學員心理切換
   → 切 IDE 開那個資料夾 → 開 README/WALKTHROUGH → 展開 .claude/ 看真實檔
   → 現場跑一次 → 學員自己敲一次（H3/H5 一定要留）→ 回 PPT 下一頁
```

> **教學金句**：「PPT 每頁 footer 的 `▶ 實戰演練：` 就是你的『切 IDE 提示燈』——看到它＝這個 Part 有資料夾可動手；沒看到＝安心留在 PPT。」

---

## 切換 IDE 的標準動作（每次都一樣，背起來）

1. PPT 講到該 Part 概念頁結束（footer 顯示 `▶ 實戰演練：<路徑>`）
2. **暫停 30 秒**讓學員心理切換（別直接切，會有人跟丟）
3. 切 IDE，用 footer 那行路徑開資料夾
4. 開資料夾裡的 `README.md`（或 `WALKTHROUGH.md`），跟著它走
5. 有 `.claude/` 子資料夾的，**一定展開給大家看真實檔案長相**（這是切 IDE 的意義）
6. 講完切回 PPT，從剛那 Part 的下一頁繼續

---

## 時間配置（12h 為主，附短版應急）

| 課程長度 | 怎麼切 |
|---|---|
| **12 小時（本指揮譜主場）** | H1–H12 全帶，每個切換點都進去，學員自己敲。逐分鐘看 [`course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md)。**90% 機率超時 30–60 分**，備一個 Hour 13 buffer 或敢砍 Part 13–17。 |
| **一日（6 小時）** | **照上方 [6 小時時時刻刻作戰表](#6-小時時時刻刻作戰表一日精華版)**——分鐘級時鐘、每段切哪個資料夾、何時休息都列好了。 |
| **一天（7 小時）** | 砍學員自己敲環節、Part 13–17 純 PPT、H6 Wafer 只口頭帶不 live。 |
| **半天（4 小時）** | 只 Part 1–12，每個切換點切但不留練習；Part 13–19 快速帶；Part 18 只講概念不實作。 |
| **2 小時精華** | 只 Part 1–3 + Part 4/8/9 各切一次 + Part 19。其餘跳過。 |
| **只示範 superpowers** | 直接跳 H10–H11（Part 11 superpowers 段）+ 切 `important-plugins/`，配兩份 walkthrough。 |

---

## 應變：時間不夠怎麼砍（優先砍順序）

1. 先砍 **Part 16 進階主題、Part 17 GitHub 資源**——純參考，給連結讓學員自己看
2. 再砍 **Part 14 Headless、Part 15 Permissions**——進階非核心
3. **H6 Wafer / H10–H11 superpowers 的進階案例**只口頭帶過，但**入門範例（recipe-genie、plugins-from-zero）一定留**
4. **Part 18 只講前段概念**，不做完整實作
5. **絕對不能砍**：Part 1（認識）、Part 4（第一次切 IDE 的轉折）、Part 6（Memory，最實用）、Part 9（Hooks，最多人搞混）

---

## FAQ（你帶課當下會被問 / 會自問的）

**Q：學員問「頁碼跟你 PPT 對不上」？**
A：PPT 一直在長（已 338 頁），別跟頁碼較勁。叫學員認 **Part 名稱 + 章節分隔頁 + footer 的 `▶ 實戰演練`**——這三個不漂移。

**Q：某 Hour 嚴重超時，下一個切換點還沒到？**
A：看上面「應變砍順序」，從 Part 16/17 開刀。**不要砍 H3 第一次切換和 H12 高潮**——寧可午休縮短。

**Q：兩份 walkthrough 我到底帶課時看哪份？**
A：**帶課看這份（指揮譜）的全景表 + 各 Part 卡點**；某 Hour 想要逐分鐘腳本/金句逐句，翻 `course_12hr_walkthrough.md` 對應 Hour。備課時兩份都讀過一遍。

**Q：H6 / H12 agent 當場跑爆怎麼辦？**
A：所以 Phase 0 要你**前一晚親手跑過**。當場真爆了：H6 改放 `computer-vision-wafer-detection/WALKTHROUGH.md` 口頭帶（不 live）；H12 改用 `context-engineering-intro/` 靜態講解。

**Q：Project 08 Agent Teams 怎麼當堂跑完？**
A：set 一個 4 人 team（backend/frontend/test/docs），丟 `app/SPEC.md` 讓它從骨架蓋 Kanban，一小時內跑完。backend 先定契約，frontend/test/docs 並行。重點讓學員看到 backend 完成後三個任務同時解鎖那一刻。深講翻 `agent_team_walkthrough.md`。

---

## 卡點對照表 ⭐（12 小時所有切換刀的坑，一張清）

| 卡點 | 出現在 | 真實原因 | 秒救 |
|---|---|---|---|
| `claude` 找不到 | H1 | npm bin 沒進 PATH | `which -a claude` 排查 |
| 認證卡瀏覽器 | H1 | 公司網路擋 Anthropic | 改設 `ANTHROPIC_API_KEY` |
| `@` 補全沒跳 | H2 | 觸發太快 | 多打幾字觸發 fuzzy |
| 自訂 command 沒出現 | H3 | session 沒重啟 | 退出 `claude` 再進 |
| `settings.local.json` 進 git | H4 | `.gitignore` 沒設 | 加進 `.gitignore` |
| Claude 沒呼叫 agent | H5 | description 觸發詞弱 | 加關鍵字 / 明示 `@agent` |
| 按 `e` 後 `/agents` 卡死 | H6 | VS Code 開了 .md tab 沒關 | `Ctrl+C` 救回，永遠按 `s` |
| MPS 不支援某 op | H6 | PyTorch + Apple Silicon | `PYTORCH_ENABLE_MPS_FALLBACK=1` |
| Agent Teams 開不起來 | H6 | 版本 < v2.1.32 / 沒開實驗旗標 | 看 08 的 `.claude/settings.json` |
| skill 沒自動觸發 | H7 | description 沒匹配關鍵字 | 加「Use when X」明確情境 |
| `/hooks` 想加 hook | H8 | 以為 TUI 能編輯 | 改 `settings.json`，TUI 只檢視 |
| MCP server 連不上 | H9 | server 印 log 到 stdout | 改印 stderr |
| `/plugin install` 失敗 | H10 | marketplace 沒加 | 先 `/plugin marketplace add` |
| spec/plan 文件難讀 | H11 | 一次給太多 | 分階段讀，先 spec consensus 再 plan |
| `/generate-prp` 不存在 | H12 | repo 沒 clone | clone `context-engineering-intro` |

---

## 講師私房筆記

### 節奏控制（一個人帶 12h 的求生指南）

- **H1–H3（上午前段）**：學員熱身中。**不要追進度**，寧可砍 Q&A 也要把 H3 第一次切 IDE 做完整——這是「啊原來這就是 Claude Code」的引爆點。
- **H4–H6（上午後段）**：開始高密度切換。**每切一次 IDE 前 PPT 暫停 30 秒**，別直接切，會有人跟丟。
- **H7–H9（下午前段）**：學員開始累。H7 Skills 三站必超時——**寧可砍第 3 站也要把 production skill 講完整**。
- **H10–H12（下午後段）**：高潮段。Pomocat + Context Engineering 不能砍。H11 的 Part 13–17 是 buffer，時間緊純 PPT 飛快帶。

### 故意踩坑（比口頭講有效 10 倍）

- **H3**：故意改完 command 不重啟 → `/cmd` 找不到 → 現場退出再進。「啊原來要重啟」勝過你講十次。
- **H5**：故意把 agent description 寫爛（「處理事情」）→ Claude 不觸發 → 改成明確觸發句 → 秒觸發。對比張力最大。
- **H6**：故意按一次 `e` → Claude Code 卡住 → `Ctrl+C` 救回。學員回家必踩這坑，先讓他看一次。
- **H8**：故意只放 `.claude/hooks/` 不註冊 `settings.json` → 跑沒效果 → 加註冊才 work。

### 不同學員角色推薦（收尾時點名給個人化建議）

| 學員角色 | 對哪段最有共鳴 | 給他的建議 |
|---|---|---|
| 全端工程師 | H3 / H8 / H9 / H12 | 回去把 commit hook、CI auto-review 接上 |
| ML / 資料工程師 | H6 / H12 | wafer-detection + Context Engineering 直接套自己 pipeline |
| 技術 PM | H7 / H10 | Skills + plugins 包 SOP 給團隊用 |
| DevOps / SRE | H8 / H9 | Hooks + Headless + MCP 接內部 infra |
| 講師 / 教學者 | H6 / H11 / H12 | Agent Teams 判準 + Pomocat + Context Engineering 當示範 |

### Kevin 親自驗證的真實狀況

- ✅ 「按 `s` 不要按 `e`」我自己踩過——VS Code 真的會卡，不是傳說。
- ✅ Wafer Roboflow `wm811k v3` 只有 Donut 一類、只有 train split——教學版本不是 bug。
- ✅ MPS `PYTORCH_ENABLE_MPS_FALLBACK=1` 必設，不然某些 op 直接報錯。
- ✅ superpowers 14 招、Context Engineering 整套 repo 我都**親手跑完才寫進 PPT**，不是 paper review。
- ⚠️ 12h 時間表是「全部按表操課」估計，**90% 機率超時 30–60 分**——備 Hour 13 buffer 或敢砍 Part 13–17。
- ⚠️ **H6 跟 H12 最危險**——agent 跑起來常出意外，前一晚務必把這兩段 pipeline 跑過一次。

---

## 一句話總結

> **這份指揮譜給你「12h 的方向感」（19 Part → 12 Hour、何時切 IDE、哪刀會卡）；逐分鐘腳本去 `course_12hr_walkthrough.md`。帶課主看這份，迷路看全景表，卡住看卡點表，超時看砍場順序——一個人也能把 12 小時穩穩交完。**

---

## 進階閱讀

- 🔗 [`docs/walkthroughs/course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md) — **逐小時放大鏡**（Hour 1–12 每小時逐分鐘腳本 + 金句逐句 + 預期 Q&A），備課必讀
- 🔗 [`docs/walkthroughs/agent_team_walkthrough.md`](docs/walkthroughs/agent_team_walkthrough.md) — H6 Agent Teams 蓋 Kanban 看板實戰（60 分鐘）
- 🔗 [`docs/walkthroughs/hook_walkthrough.md`](docs/walkthroughs/hook_walkthrough.md) — H8 Hooks 心智模型
- 🔗 [`docs/walkthroughs/gitnexus_walkthrough.md`](docs/walkthroughs/gitnexus_walkthrough.md) — H9 加碼：GitNexus knowledge graph 工具深入（接 Part 10 MCP 應用 / Part 16 進階）
- 🔗 [`docs/walkthroughs/karpathy_skills_walkthrough.md`](docs/walkthroughs/karpathy_skills_walkthrough.md) — H4 尾 或 H10：Karpathy 4 原則 + 最小 plugin 解剖（接 Part 6 / Part 11）
- 🔗 [`Claude_Code_建構指南.md`](Claude_Code_建構指南.md) — 1559 行完整 reference
- 🔗 [`Projects/README.md`](Projects/README.md) — 8 個 Projects 總覽
- 🔗 [`agent_group_projects/computer-vision-wafer-detection/WALKTHROUGH.md`](agent_group_projects/computer-vision-wafer-detection/WALKTHROUGH.md) — H6 / H12 wafer 案例 20K 字講師版
- 🔗 [`agent_group_projects/new-course-material2presentation-blank/WALKTHROUGH.md`](agent_group_projects/new-course-material2presentation-blank/WALKTHROUGH.md) — H6 進階加菜：Course Factory（主題無關的課程開發 agent 團隊，sub-agent 抽象層級的最高階範例，時間夠才帶）

---

_Last updated: 2026-05-22（新增「6 小時時時刻刻作戰表」一日精華逐分鐘版，Part 11 接上 important-plugins 三大 plugin 安裝+案例）_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材：[docs/walkthroughs/course_12hr_walkthrough.md](docs/walkthroughs/course_12hr_walkthrough.md)（逐小時版）、[docs/walkthroughs/agent_team_walkthrough.md](docs/walkthroughs/agent_team_walkthrough.md)、[docs/walkthroughs/hook_walkthrough.md](docs/walkthroughs/hook_walkthrough.md)、[important-plugins/plugins_install_and_cases_walkthrough.md](important-plugins/plugins_install_and_cases_walkthrough.md)（Part 11 三大 plugin 安裝+案例）_
_對應 PPT：`Claude_Code_完整教學.pptx`（338 頁・19 Part）_
