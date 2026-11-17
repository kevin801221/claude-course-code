# 怎麼用這份中文文件學到進階的 Claude Code

<table width="100%">
<tr>
<td><a href="README.md">← 回到中文版索引</a></td>
<td align="right"><img src="!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 這份文件不是翻譯，是**讀法**。這個 repo 有 48 份文件、約 10,000 行，照目錄順序讀會迷路。
> 下面是一條有先後順序的路線，每一關都有「讀什麼 → 做什麼 → 怎麼知道自己過關了」。

---

## 先搞清楚：「進階」到底是什麼意思

大部分人卡住的地方，不是不知道某個指令，而是**心智模型停在第 1 層**。

| 層級 | 心智模型 | 典型行為 | 卡住的症狀 |
|------|---------|---------|-----------|
| **L1 聊天** | Claude 是會寫程式的聊天機器人 | 貼程式碼、問問題、複製答案 | 「它不懂我的專案」 |
| **L2 代理** | Claude 會自己讀檔、執行、修正 | 給任務、讓它跑、review diff | 「跑久了就開始變笨」 |
| **L3 harness** | 我在設計 Claude 的工作環境 | 寫 CLAUDE.md、skills、hooks | 「我寫的 skill 它不觸發」 |
| **L4 脈絡工程** | 我在管理一個會腐壞的資源：脈絡 | 切 session、分子代理、設計壓縮點 | 「怎麼平行跑五個還不打架」 |
| **L5 編排** | 我在經營一支代理團隊 | worktree、agent teams、workflows | —— |

**進階 = L3 以上。** 這份 repo 的價值幾乎全在 L3–L5，而 L3 的入口只有一個觀念：

> 功能不是「換湯不換藥的 prompt」。skills、subagents、hooks 是**真正不同的執行機制**，
> 選錯機制，prompt 寫得再好也救不回來。

這句話的完整論證在 [`reports/why-harness-is-important.md`](reports/why-harness-is-important.md)。**如果你只讀一份，讀那份。**

---

## 路線圖

```
L0 裝起來 ──► L1 三原語 ──► L2 選對機制 ──► L3 脈絡工程 ──► L4 編排 ──► L5 心法
   1 小時        1 週          1 週            2 週           2 週      持續
```

---

## L0 ── 把環境裝對（1 小時）

| 讀 | 為什麼 |
|----|--------|
| [`tutorial/day0/README.md`](tutorial/day0/README.md) → 你的 OS（[mac](tutorial/day0/mac.md) / [windows](tutorial/day0/windows.md) / [linux](tutorial/day0/linux.md)） | 安裝、驗證 |
| [`tutorial/day1/README.md`](tutorial/day1/README.md) | 第一個真實任務 |
| [`best-practice/claude-cli-startup-flags.md`](best-practice/claude-cli-startup-flags.md) | 只掃過，知道有哪些旗標就好 |

**做**：在你自己的 repo 跑 `claude`，叫它 `/init` 產生 CLAUDE.md，然後**自己讀一遍並刪掉一半**。

**過關**：你知道 `claude -p`、`--worktree`、`/doctor` 分別做什麼。

---

## L1 ── 三個原語（1 週）

這是 Claude Code 全部擴充能力的地基。**不要跳過，也不要一次讀完三份。**

| 第幾天 | 讀 | 做 |
|-------|----|----|
| 1–2 | [`best-practice/claude-memory.md`](best-practice/claude-memory.md) | 把 `/init` 產的 CLAUDE.md 重寫成 200 行以內，只留「Claude 猜不到的事」 |
| 3–4 | [`best-practice/claude-commands.md`](best-practice/claude-commands.md) | 寫一個 `/` 指令，把你每天手動打的那串 prompt 封裝起來 |
| 5–7 | [`best-practice/claude-skills.md`](best-practice/claude-skills.md) | 寫第一個 skill，放進 `.claude/skills/<name>/SKILL.md` |

**最容易踩的坑**：skill 寫好了不觸發。原因 99% 是 `description` 寫得太像標題。
`description` 是 Claude 決定要不要載入的**唯一依據**，要寫成「什麼情況下用我」，而且把使用者會講的詞寫進去。
這條的深入說明看 [`tips/claude-thariq-tips-17-mar-26.md`](tips/claude-thariq-tips-17-mar-26.md)（官方 Thariq 的 9 種 skill 類型 + 9 個撰寫技巧）。

**過關**：你的 skill 在你**沒有打 `/`** 的情況下被自動觸發過至少一次。

---

## L2 ── 選對機制（1 週）← 這裡才真正進入進階

L1 教你「怎麼寫」，L2 教你「什麼時候該寫哪一種」。

| 順序 | 讀 | 核心問題 |
|------|----|---------|
| 1 | [`reports/why-harness-is-important.md`](reports/why-harness-is-important.md) | 為什麼不能全部塞 prompt |
| 2 | [`reports/claude-agent-command-skill.md`](reports/claude-agent-command-skill.md) | agent / command / skill 三選一的決策樹 |
| 3 | [`best-practice/claude-subagents.md`](best-practice/claude-subagents.md) | 16 個 frontmatter 欄位 —— 特別看 `context`、`model`、`skills` |
| 4 | [`reports/claude-skills-for-larger-mono-repos.md`](reports/claude-skills-for-larger-mono-repos.md) | 漸進式揭露：怎麼讓 50 個 skill 不塞爆脈絡 |

**決策的一句話版本**（細節在上面第 2 份）：

| 你想要 | 用 |
|-------|-----|
| 我主動觸發的固定流程 | **command**（`.claude/commands/`） |
| Claude 自己判斷該不該用的知識 | **skill**（`.claude/skills/`） |
| 要**獨立脈絡視窗**跑、不污染主對話 | **subagent**（`.claude/agents/`） |
| 每次工具呼叫都要發生的事（格式化、音效、擋危險指令） | **hook**（`.claude/settings.json`） |

**做**：挑一個你已經寫成 command 的東西，問自己「它需要獨立脈絡嗎？」如果需要，改寫成 subagent，比較差異。
本 repo 的 `/weather-orchestrator` 就是這個模式的最小範例（Command → Agent → Skill），
流程圖在 [`orchestration-workflow/orchestration-workflow.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/orchestration-workflow/orchestration-workflow.md)。

**過關**：有人問你「這要用 skill 還 agent」，你能在 10 秒內給出理由，而不是「都可以」。

---

## L3 ── 脈絡工程（2 週）← 真正的分水嶺

到這裡你會的東西已經比 90% 的人多了。但你還是會遇到「跑久了它就開始亂」。
**那不是模型變笨，是脈絡腐壞（context rot）。**

| 順序 | 讀 | 你會拿到什麼 |
|------|----|------------|
| 1 | [`videos/claude-dex-mlops-community-24-mar-26.md`](videos/claude-dex-mlops-community-24-mar-26.md) | 「聰明區 vs 笨蛋區」—— 脈絡用量與品質的關係曲線 |
| 2 | [`reports/llm-day-to-day-degradation.md`](reports/llm-day-to-day-degradation.md) | 權重凍結 ≠ 行為凍結；什麼情況下「今天比較笨」是真的 |
| 3 | [`tips/claude-boris-2-tips-10-mar-26.md`](tips/claude-boris-2-tips-10-mar-26.md) | 多重脈絡視窗：為什麼不相關的脈絡要分開跑 |
| 4 | [`reports/claude-advanced-tool-use.md`](reports/claude-advanced-tool-use.md) | Tool Search、動態過濾、PTC —— 工具本身也佔脈絡 |
| 5 | [`videos/claude-matt-pocock-24-apr-26.md`](videos/claude-matt-pocock-24-apr-26.md) | RPI 方法論、垂直切片、指令預算（~150–200 條） |

**可以立刻改變你每天工作方式的三件事**：

1. **約 50% 脈絡時手動 `/compact`**，不要等它自動壓縮。自動壓縮發生時你沒得選要保留什麼。
2. **換任務就 `/clear`**，不要讓上一個任務的殘渣留在脈絡裡。省下的不是錢，是品質。
3. **走錯路用 rewind，不要用「不對，重來」**。後者把錯誤答案永久留在脈絡裡當成範例。

**做**：連續一週，每次 session 結束前記一筆：脈絡用到幾 %、品質在哪個點開始掉。
你會親眼看到那條曲線。

**過關**：你會為了「脈絡乾淨」而主動開新 session，而不是覺得那樣很麻煩。

---

## L4 ── 編排（2 週）

一次只跑一個 Claude 的時代結束了。

| 讀 | 主題 |
|----|------|
| [`tips/claude-boris-15-tips-30-mar-26.md`](tips/claude-boris-15-tips-30-mar-26.md) | `/loop`、`/batch`、`--bare`、`/btw`、worktree —— 隱藏功能大補帖 |
| [`reports/claude-global-vs-project-settings.md`](reports/claude-global-vs-project-settings.md) | 設定階層、Tasks 系統、Agent Teams |
| [`implementation/claude-agent-teams-implementation.md`](implementation/claude-agent-teams-implementation.md) | 多個完整 session 透過共享任務清單協調 |
| [`implementation/claude-subagents-implementation.md`](implementation/claude-subagents-implementation.md) | 子代理實作細節 |
| [`implementation/claude-scheduled-tasks-implementation.md`](implementation/claude-scheduled-tasks-implementation.md) | `/loop`、`/schedule` |
| [`implementation/claude-goal-implementation.md`](implementation/claude-goal-implementation.md) | `/goal` 跨回合持續工作 |
| [`reports/claude-agent-memory.md`](reports/claude-agent-memory.md) | 子代理的持久記憶（`memory: user/project/local`） |
| [`best-practice/claude-mcp.md`](best-practice/claude-mcp.md) | MCP server、三種範圍、權限規則 |

**平行工作的關鍵不是「開很多視窗」，是 worktree。**
`git worktree` 讓每個 Claude 有自己的工作目錄，彼此不會互相覆寫檔案。
`claude --worktree`（或 `-w`）一行搞定。

**做**：用 worktree 同時跑兩個 Claude 做兩個不相關的小功能，從頭到 PR。

**過關**：你能說出「什麼任務適合平行、什麼任務不行」—— 提示：共享狀態。

---

## L5 ── 心法（持續）

這一層沒有技巧，只有判斷力。這些是 Claude Code 團隊自己的思考方式。

| 讀 | 一句話 |
|----|-------|
| [`videos/claude-boris-lennys-podcast-19-feb-26.md`](videos/claude-boris-lennys-podcast-19-feb-26.md) | 「永遠不要賭模型不會進步」—— 為模型 6 個月後的樣子打造 |
| [`videos/claude-boris-pragmatic-engineer-04-mar-26.md`](videos/claude-boris-pragmatic-engineer-04-mar-26.md) | Claude Code 自己是怎麼被 Claude Code 做出來的 |
| [`videos/claude-cat-every-29-oct-25.md`](videos/claude-cat-every-29-oct-25.md) | 原型文化、紅色 diff、「不要有新使用者體驗」 |
| [`videos/claude-karpathy-ai-engineer-02-may-26.md`](videos/claude-karpathy-ai-engineer-02-may-26.md) | Karpathy 視角：這件事在歷史上的位置 |
| [`videos/claude-boris-y-combinator-17-feb-26.md`](videos/claude-boris-y-combinator-17-feb-26.md) | 潛在需求（latent demand）—— 產品判斷的核心 |
| [`videos/claude-boris-ryan-peterman-15-dec-25.md`](videos/claude-boris-ryan-peterman-15-dec-25.md) | 工程師的角色怎麼變 |

**最反直覺、但最重要的一條**：
> 不要為了繞過模型今天的弱點而蓋複雜的鷹架。那個弱點下一版就補掉了，你的鷹架會變成技術債。
> 要蓋的是**模型變強時會跟著變強**的東西。

---

## 四週速成表（每天 30–60 分鐘）

| 週 | 讀 | 動手產出 |
|----|----|---------|
| 1 | L0 + L1 | 一份精簡 CLAUDE.md、一個 command、一個會自動觸發的 skill |
| 2 | L2 | 把一個 command 改寫成 subagent，寫出你自己的決策樹 |
| 3 | L3 | 一週的脈絡用量紀錄 + 改掉三個習慣 |
| 4 | L4 | 用 worktree 平行跑兩個任務到 PR |

L5 不排進度，當睡前讀物，每週一份。

---

## 三個最常見的反模式

| 反模式 | 為什麼錯 | 改成 |
|-------|---------|------|
| CLAUDE.md 寫成 500 行百科全書 | 超過約 200 行後遵守率明顯下滑，而且每次 session 都吃脈絡 | 200 行內，只寫「Claude 猜不到的」；其他放 `.claude/rules/*.md` 加 `paths:` 讓它按需載入 |
| 什麼都塞進 prompt | 一次性、無法複用、每次都得重打 | 固定流程 → command；判斷性知識 → skill；每次都要發生 → hook |
| 一個 session 跑到底 | 脈絡腐壞，後半段品質斷崖式下滑 | 任務切小到 50% 脈絡內能做完，換任務就 `/clear` |

---

## 一個加速技巧：讓 Claude 當你的讀書教練

這些文件本來就是給 Claude 讀的格式。與其自己啃，不如：

```
# 在這個 repo 裡開 claude，然後：
請讀 @reports/why-harness-is-important.md，
用我的專案（@CLAUDE.md）當例子，告訴我我現在哪裡做錯了，列出三個具體可以改的地方。
```

或者更進一步 —— **去讀一份真正會動的 harness**。
[英文原 repo](https://github.com/kevin801221/claude-code-best-practice) 的 `.claude/` 底下有可運作的 skills、agents、commands、hooks：

- [`.claude/agents/weather-agent.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/.claude/agents/weather-agent.md) —— 子代理定義
- [`.claude/skills/weather-fetcher/SKILL.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/.claude/skills/weather-fetcher/SKILL.md) —— 被預載進代理的 skill
- [`.claude/commands/weather-orchestrator.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/.claude/commands/weather-orchestrator.md) —— Command → Agent → Skill 的入口

讀完 L2 之後，拿這三個檔案對照 [`best-practice/claude-subagents.md`](best-practice/claude-subagents.md) 的欄位表看，比讀十篇文章有用。

> 注意：`.claude/` 底下的檔案**刻意沒有翻譯**。
> 那些 `description` 欄位是 Claude 做語意比對的依據，翻成中文會讓英文 prompt 的觸發率下降。
> 你讀的是中文文件，Claude 讀的是英文定義 —— 這個分工是故意的。

---

## 查詢型文件（不用照順序讀，用到再翻）

| 文件 | 什麼時候翻 |
|------|-----------|
| [`best-practice/claude-commands.md`](best-practice/claude-commands.md) | 想知道某個 `/` 指令存不存在（96 個官方指令） |
| [`best-practice/claude-power-ups.md`](best-practice/claude-power-ups.md) | 想用 `/powerup` 的 10 堂互動課 |
| [`reports/claude-usage-and-rate-limits.md`](reports/claude-usage-and-rate-limits.md) | 撞到額度上限、想搞懂 fast 模式計費 |
| [`reports/claude-in-chrome-v-chrome-devtools-mcp.md`](reports/claude-in-chrome-v-chrome-devtools-mcp.md) | 要選瀏覽器自動化方案 |
| [`reports/claude-agent-sdk-vs-cli-system-prompts.md`](reports/claude-agent-sdk-vs-cli-system-prompts.md) | 要用 Agent SDK 自己蓋代理 |
| [`reports/claude-spinner-verbs-and-tips.md`](reports/claude-spinner-verbs-and-tips.md) | 好奇轉圈時那些字 / 想看 42 條內建提示 |
| [`best-practice/claude-settings.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md)（英文） | 要查某個 settings.json 欄位 |

---

<table width="100%">
<tr>
<td><a href="README.md">← 回到中文版索引</a></td>
<td align="right"><a href="../../README.md">英文原 README →</a></td>
</tr>
</table>
