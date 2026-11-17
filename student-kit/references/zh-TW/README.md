# claude-code 中文筆記

Claude Code 最佳實踐的繁體中文（台灣）版 —— 從 vibe coding 到 agentic engineering

> **這是 [`shanraisshan/claude-code-best-practice`](https://github.com/shanraisshan/claude-code-best-practice) 的繁體中文翻譯。**
> 原作以 MIT 授權釋出，本翻譯同樣採用 MIT（見 [`LICENSE`](LICENSE)）。
>
> 功能名稱、指令、檔案路徑、frontmatter 欄位一律保留原文，方便你對照官方文件查找。
> 文中指向英文原檔的連結，會連到 [`kevin801221/claude-code-best-practice`](https://github.com/kevin801221/claude-code-best-practice)（上游的 fork）。

<p align="center">
  <img src="!/claude-jumping.svg" alt="Claude Code 吉祥物" width="120" height="100">
</p>

> [!TIP]
> 想完整發揮這個 repo 的價值，請看最下面的 [**怎麼用這份中文文件學習**](#怎麼用這份中文文件學習) 一節。

---

## 📖 中文版文件索引

### best-practice/ —— 核心參考（frontmatter 欄位、官方清單）

| 文件 | 內容 |
|------|------|
| [Skills 最佳實踐](best-practice/claude-skills.md) | 20 個 frontmatter 欄位 + 25 個官方內建 skills |
| [子代理最佳實踐](best-practice/claude-subagents.md) | 16 個 frontmatter 欄位 + 5 個官方代理類型 |
| [Commands 最佳實踐](best-practice/claude-commands.md) | 20 個 frontmatter 欄位 + 96 個官方 slash command |
| [MCP Servers 最佳實踐](best-practice/claude-mcp.md) | 日常推薦 server、設定、權限規則、三種範圍 |
| [Claude Memory](best-practice/claude-memory.md) | CLAUDE.md 怎麼寫、monorepo 的載入機制 |
| [CLI 啟動旗標](best-practice/claude-cli-startup-flags.md) | 所有啟動旗標、子命令、啟動環境變數 |
| [Power-ups](best-practice/claude-power-ups.md) | `/powerup` 的 10 堂互動課程 |

### reports/ —— 深度分析（為什麼這樣設計）

| 文件 | 內容 |
|------|------|
| [為什麼 Harness 很重要](reports/why-harness-is-important.md) | ★ 進階必讀：功能不是「換湯不換藥的 prompt」 |
| [Agents vs Commands vs Skills](reports/claude-agent-command-skill.md) | ★ 三種擴充機制的完整對照與解析順序 |
| [Agent Memory Frontmatter](reports/claude-agent-memory.md) | 子代理的持久記憶、三種範圍 |
| [全域 vs 專案層級功能](reports/claude-global-vs-project-settings.md) | 設定階層、Tasks 系統、Agent Teams |
| [Monorepo 中的 Skills 探索](reports/claude-skills-for-larger-mono-repos.md) | 巢狀 skill 的按需探索機制 |
| [Agent SDK vs CLI System Prompts](reports/claude-agent-sdk-vs-cli-system-prompts.md) | 模組化 system prompt、輸出一致性 |
| [進階工具使用模式](reports/claude-advanced-tool-use.md) | PTC、動態過濾、Tool Search、工具使用範例 |
| [LLM 每日品質波動](reports/llm-day-to-day-degradation.md) | 凍結權重 ≠ 凍結行為，完整推論堆疊 |
| [瀏覽器自動化 MCP 比較](reports/claude-in-chrome-v-chrome-devtools-mcp.md) | Chrome DevTools vs Claude in Chrome vs Playwright |
| [用量、速率限制與額外用量](reports/claude-usage-and-rate-limits.md) | `/usage`、`/extra-usage`、fast 模式計費 |
| [轉圈動畫與提示](reports/claude-spinner-verbs-and-tips.md) | 179 個動詞 + 42 條內建提示的中譯 |
| [天氣播報員改版計畫](reports/learning-journey-weather-reporter-redesign.md) | 一份真實的 Claude 規劃文件範例 |

### tips/ —— 官方人員放出的技巧

| 文件 | 內容 |
|------|------|
| [Boris：13 個技巧](tips/claude-boris-13-tips-03-jan-26.md) | 2026-01-03：平行 5 個 Claude、共用 CLAUDE.md、PostToolUse hook |
| [Claude Code 團隊：10 個技巧](tips/claude-boris-10-tips-01-feb-26.md) | 2026-02-01：worktree、plan 模式、prompt 功力、用 Claude 學習 |
| [Boris：12 種客製方式](tips/claude-boris-12-tips-12-feb-26.md) | 2026-02-12：終端機、effort、外掛、沙箱、hooks、輸出風格 |
| [Boris：2 個技巧](tips/claude-boris-2-tips-10-mar-26.md) | 2026-03-10：Code Review、測試時運算與多重脈絡視窗 |
| [Thariq：我們怎麼用 Skills](tips/claude-thariq-tips-17-mar-26.md) | ★ 2026-03-17：9 種 skill 類型 + 9 個撰寫技巧 |
| [Boris：2 個技巧](tips/claude-boris-2-tips-25-mar-26.md) | 2026-03-25：squash merge 與 PR 大小分布 |
| [Boris：15 個隱藏功能](tips/claude-boris-15-tips-30-mar-26.md) | ★ 2026-03-30：`/loop`、`/batch`、`--bare`、`/btw`、worktree |
| [Boris：Opus 4.7 的 6 個技巧](tips/claude-boris-6-tips-16-apr-26.md) | 2026-04-16：auto 模式、recaps、focus、effort、驗證 |
| [Thariq：Session 管理與 1M 脈絡](tips/claude-thariq-tips-16-apr-26.md) | ★ 2026-04-16：脈絡腐敗、倒回 vs 糾正、壓縮 vs 全新 |

### implementation/ —— 這個 repo 的實際實作

| 文件 | 內容 |
|------|------|
| [Commands 實作](implementation/claude-commands-implementation.md) | `/weather-orchestrator` 作為編排進入點 |
| [子代理實作](implementation/claude-subagents-implementation.md) | `weather-agent` 與預載 skill |
| [Skills 實作](implementation/claude-skills-implementation.md) | 兩種 skill 模式的具體對照 |
| [Agent Teams 實作](implementation/claude-agent-teams-implementation.md) | 用 tmux 分割窗格跑多個協調 session |
| [排程任務實作](implementation/claude-scheduled-tasks-implementation.md) | `/loop` 的 cron 機制與示範 |
| [Goal 實作](implementation/claude-goal-implementation.md) | `/goal` 與社群的 prompt 技巧 |

### videos/ —— 訪談逐字稿

| 文件 | 內容 |
|------|------|
| [Karpathy：從 Vibe Coding 到 Agentic Engineering](videos/claude-karpathy-ai-engineer-02-may-26.md) | ★ Software 3.0、可驗證性、鋸齒狀智慧 |
| [Boris × Ryan Peterman](videos/claude-boris-ryan-peterman-15-dec-25.md) | Claude Code 的誕生故事與職涯心法 |
| [Boris × Lenny's Podcast](videos/claude-boris-lennys-podcast-19-feb-26.md) | 產品視角的 Claude Code |
| [Boris × Pragmatic Engineer](videos/claude-boris-pragmatic-engineer-04-mar-26.md) | 工程實務視角 |
| [Boris × Y Combinator](videos/claude-boris-y-combinator-17-feb-26.md) | 新創視角 |
| [Matt Pocock](videos/claude-matt-pocock-24-apr-26.md) | TypeScript 社群視角 |
| [Cat × Every](videos/claude-cat-every-29-oct-25.md) | Anthropic 內部使用實況 |
| [Dex × MLOps Community](videos/claude-dex-mlops-community-24-mar-26.md) | 脈絡工程與 agent 設計 |

### tutorial/ —— 新手入門

| 文件 | 內容 |
|------|------|
| [Day 0：安裝設定](tutorial/day0/README.md) | 安裝 + 登入（[macOS](tutorial/day0/mac.md) · [Windows](tutorial/day0/windows.md) · [Linux](tutorial/day0/linux.md)） |
| [Day 1：第一次對話](tutorial/day1/README.md) | Prompting → Agents → Skills 的三層遞進 |

---

## 🧠 核心概念速查

這張表對應英文版 README 的 CONCEPTS 區塊。功能名稱保留原文，連結指向官方文件與本中文版文件。

| 功能 | 位置 | 中文說明 |
|---------|----------|-------------|
| [**Subagents**](https://code.claude.com/docs/en/sub-agents) | `.claude/agents/<name>.md` | 有獨立脈絡視窗的子代理 → [最佳實踐](best-practice/claude-subagents.md) · [實作](implementation/claude-subagents-implementation.md) |
| [**Commands**](https://code.claude.com/docs/en/commands) | `.claude/commands/<name>.md` | 使用者觸發的 slash command → [最佳實踐](best-practice/claude-commands.md) · [實作](implementation/claude-commands-implementation.md) |
| [**Skills**](https://code.claude.com/docs/en/skills) | `.claude/skills/<name>/SKILL.md` | 可重用的程序性知識 → [最佳實踐](best-practice/claude-skills.md) · [實作](implementation/claude-skills-implementation.md) · [Monorepo 探索機制](reports/claude-skills-for-larger-mono-repos.md) |
| [**Workflows**](https://code.claude.com/docs/en/common-workflows) | `.claude/commands/weather-orchestrator.md` | Command → Agent → Skill 的編排模式 → [流程圖](https://github.com/kevin801221/claude-code-best-practice/blob/main/orchestration-workflow/orchestration-workflow.md) |
| [**Hooks**](https://code.claude.com/docs/en/hooks) | `.claude/hooks/` | 生命週期事件的確定性程式碼執行 → [hooks repo](https://github.com/shanraisshan/claude-code-hooks) |
| [**MCP Servers**](https://code.claude.com/docs/en/mcp) | `.claude/settings.json`、`.mcp.json` | 連接外部工具與資料來源 → [最佳實踐](best-practice/claude-mcp.md) |
| [**Plugins**](https://code.claude.com/docs/en/plugins/overview) | 可散佈的套件 | 打包 skills/agents/hooks/MCP → [市集](https://code.claude.com/docs/en/plugins/anthropic-marketplaces) |
| [**Settings**](https://code.claude.com/docs/en/settings) | `.claude/settings.json` | 設定階層與權限 → [英文參考](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md)（1,451 行查詢型大表，未翻譯） |
| [**Status Line**](https://code.claude.com/docs/en/statusline) | `.claude/settings.json` | 自訂狀態列 → [status-line repo](https://github.com/shanraisshan/claude-code-status-line) |
| [**Memory**](https://code.claude.com/docs/en/memory) | `CLAUDE.md`、`.claude/rules/` | 持久脈絡 → [最佳實踐](best-practice/claude-memory.md) · [Agent Memory 深入](reports/claude-agent-memory.md) |
| [**Checkpointing**](https://code.claude.com/docs/en/checkpointing) | 自動（檔案編輯追蹤） | `/rewind`、`Esc Esc` 倒回 |
| [**Sessions**](https://code.claude.com/docs/en/sessions) | `--resume`、`--continue`、`/resume`、`/branch` | Session 接續與分支 |
| [**Context Window**](https://code.claude.com/docs/en/context-window) | `/compact`、`/clear`、`/context` | 脈絡管理 → [Thariq 的脈絡管理指南](tips/claude-thariq-tips-16-apr-26.md) |
| [**CLI Startup Flags**](https://code.claude.com/docs/en/cli-reference) | `claude [flags]` | 啟動旗標 → [最佳實踐](best-practice/claude-cli-startup-flags.md) |

### 🔥 值得注意的新功能

| 功能 | 位置 | 中文說明 |
|---------|----------|-------------|
| [**Ultrareview**](https://code.claude.com/docs/en/ultrareview) | `/code-review ultra` | 雲端沙箱中的多代理深度 code review |
| [**Auto Mode**](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode) | `--permission-mode auto`、`Shift+Tab` | 用模型分類器決定權限，取代盯著看 |
| [**Power-ups**](best-practice/claude-power-ups.md) | `/powerup` | 10 堂互動課程教你被忽略的功能 |
| [**Fast Mode**](https://code.claude.com/docs/en/fast-mode) | `/fast`、`"fastMode": true` | Opus 加速輸出（計入額外用量） |
| [**Advisor**](https://code.claude.com/docs/en/advisor) | `/advisor`、`advisorModel` | 在關鍵時刻諮詢第二個模型 |
| [**Agent SDK**](https://code.claude.com/docs/en/agent-sdk/overview) | `npm` / `pip` 套件 | 用 SDK 打造自己的代理 |
| [**Chrome**](https://code.claude.com/docs/en/chrome) | `--chrome`、擴充套件 | 讓 Claude 驗證前端工作 → [比較報告](reports/claude-in-chrome-v-chrome-devtools-mcp.md) |
| [**Code Review**](https://code.claude.com/docs/en/code-review) | GitHub App | 每個 PR 派出代理團隊獵 bug |
| [**Remote Control**](https://code.claude.com/docs/en/remote-control) | `/remote-control`、`/rc` | 從手機控制本機 session |
| [**Dynamic Workflows**](https://code.claude.com/docs/en/workflows) | `/workflows`、`ultracode` | 腳本化地編排數十個代理 |
| [**Agent Teams**](https://code.claude.com/docs/en/agent-teams) | 環境變數啟用 | 多個完整 session 透過共享任務清單協調 → [實作](implementation/claude-agent-teams-implementation.md) |
| [**Cross-Session Messaging**](https://code.claude.com/docs/en/cross-session-messaging) | `SendMessage`、`/list-agents` | session 之間互相傳訊 |
| [**Scheduled Tasks**](https://code.claude.com/docs/en/scheduled-tasks) | `/loop`、`/schedule` | 排程重複任務 → [實作](implementation/claude-scheduled-tasks-implementation.md) |
| [**Tasks**](reports/claude-global-vs-project-settings.md) | `/tasks`、`~/.claude/tasks/` | 跨 session 的持久任務清單 |
| [**Goal**](https://code.claude.com/docs/en/goal) | `/goal <condition>` | 跨回合持續工作直到條件滿足 → [實作](implementation/claude-goal-implementation.md) |
| [**Voice Dictation**](https://code.claude.com/docs/en/voice-dictation) | `/voice` | 說話比打字快 3 倍 |
| [**Git Worktrees**](https://code.claude.com/docs/en/worktrees) | `--worktree`/`-w` | 平行工作的基礎設施 |

---

## 📌 未翻譯的部分（以及為什麼）

| 目錄 | 原因 |
|------|------|
| `changelog/` | 由 `/workflows:best-practice:*` 自動產生的 drift log，翻了下次跑過就被覆蓋 |
| `.claude/` | skill / agent / command 定義是**給 Claude 讀的**，`description` 欄位是語意比對的依據，翻譯會降低英文 prompt 的觸發率 |
| `presentation/` | HTML 投影片 |
| `best-practice/claude-settings.md` | 1,451 行的查詢型設定大表，查的時候直接看[英文原檔](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md)更即時 |
| README 的外部連結清單 | TIPS AND TRICKS（83 條）、STARTUPS、SUBSCRIBE 等區塊是外部連結索引，請直接看[英文原 README](https://github.com/kevin801221/claude-code-best-practice/blob/main/README.md) |

---

## 怎麼用這份中文文件學習

見 [`LEARNING-PATH.md`](LEARNING-PATH.md)。
