# 在週末內精通 Claude Code 完整教學

> 🚀 從基礎到高階：結合 10 大系統化理論模組、多 Agent 協作產線、原生 Agent Teams 與真實工業級專案的旗艦級教學庫。
> 
> 由 [@kevin801221](https://github.com/kevin801221) 精心打造與繁體中文化整理

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.263-brightgreen)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-2.1+-purple)](https://code.claude.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

從輸入 `claude` 開始，到能協調代理、Hooks、技能（Skills）與 MCP 伺服器——搭配視覺化教學、可直接複製貼上的範本，以及豐富的實戰專案工廠。

**[15 分鐘快速上手](#15-分鐘快速上手)** | **[找到你的等級](#不知道從哪裡開始)** | **[實戰專案工廠](#實戰專案工廠-projects)** | **[瀏覽功能目錄](CATALOG.md)**


---

## 目錄

- [問題在哪裡](#問題在哪裡)
- [Claude Code 完整教學 如何解決](#claude-how-to-如何解決)
- [運作原理](#運作原理)
- [不知道從哪裡開始？](#不知道從哪裡開始)
- [15 分鐘快速上手](#15-分鐘快速上手)
- [你能用它做什麼？](#你能用它做什麼)
- [常見問題](#常見問題)
- [參與貢獻](#參與貢獻)
- [授權條款](#授權條款)

---

## 問題在哪裡

你安裝了 Claude Code，也跑了幾個提示詞。然後呢？

- **官方文件只描述功能，卻沒告訴你怎麼把它們組合起來。** 你知道斜線指令（Slash Commands）的存在，但不知道怎麼把它跟 Hooks、記憶（Memory）、子代理（Subagents）串起來，變成真正能省下大把時間的工作流程。
- **沒有清楚的學習路徑。** 該先學 MCP 還是先學 Hooks？先學技能還是先學子代理？結果什麼都碰過一點，卻沒有一項真正精通。
- **範例太基礎。** 一個「hello world」等級的斜線指令，沒辦法幫你打造出會用到記憶、委派給專業代理、自動執行安全性掃描的生產級程式碼審查管線。

你放著 Claude Code 九成的威力沒用——而且你根本不知道自己不知道什麼。

---

## Claude Code 完整教學 如何解決

這不是又一份功能參考文件，而是一份**有結構、視覺化、以範例為導向的教學**，教你使用每一項 Claude Code 功能，並提供你今天就能複製進專案的實戰範本。

| | 官方文件 | 本教學 |
|--|---------------|------------|
| **格式** | 參考文件 | 搭配 Mermaid 圖表的視覺化教學 |
| **深度** | 功能描述 | 底層運作原理 |
| **範例** | 基礎程式碼片段 | 可立即使用的生產級範本 |
| **結構** | 依功能分類 | 漸進式學習路徑（初階到進階） |
| **入門方式** | 自行摸索 | 附時間估計的引導路線圖 |
| **自我評量** | 沒有 | 互動測驗，找出弱點並建立個人化路徑 |

### 你會得到什麼：

- **10 個教學模組**，涵蓋每一項 Claude Code 功能——從斜線指令到自訂代理團隊（Agent Teams）
- **可直接複製貼上的設定**——斜線指令、CLAUDE.md 範本、hook 腳本、MCP 設定、子代理定義，以及完整的外掛（Plugins）套件
- **Mermaid 圖表**，展示每項功能內部的運作方式，讓你不只知道「怎麼做」，還懂「為什麼」
- **有引導的學習路徑**，讓你在 11 到 13 小時內從新手變成高手
- **內建自我評量**——直接在 Claude Code 中執行 `/self-assessment` 或 `/lesson-quiz hooks`，找出自己的弱點

**[開始學習路徑 ->](LEARNING-ROADMAP.md)**

---

## 運作原理

### 1. 找到你的等級

做這份[自我評量測驗](LEARNING-ROADMAP.md#-找到你的等級)，或在 Claude Code 中執行 `/self-assessment`。根據你已經會的東西，取得個人化的路線圖。

### 2. 依照引導路徑進行

依序完成 10 個模組——每一個都建立在前一個的基礎上。邊學邊把範本直接複製進你的專案。

### 3. 把功能組合成工作流程

真正的威力在於把功能組合起來。學習把斜線指令 + 記憶 + 子代理 + Hooks 串接成自動化管線，處理程式碼審查、部署與文件產生。

### 4. 測試你的理解

每完成一個模組，就執行 `/lesson-quiz [topic]`。測驗會精準指出你漏掉的地方，讓你快速補齊。

**[15 分鐘快速上手](#15-分鐘快速上手)**

---

## 深受開發者信賴

- **GitHub 星星數**，來自每天使用 Claude Code 的開發者
- **Fork 數**，來自把這份教學改成自己工作流程的團隊
- **積極維護中**——與每次 Claude Code 發行同步（最新版本：v2.1.263，2026 年 9 月）
- **社群驅動**——來自分享真實世界設定的開發者貢獻


---

## 不知道從哪裡開始？

做自我評量，或直接挑選你的等級：

| 等級 | 你會…… | 從這裡開始 | 時間 |
|-------|-----------|------------|------|
| **初階** | 啟動 Claude Code 並對話 | [斜線指令](01-slash-commands/) | 約 2.5 小時 |
| **中階** | 使用 CLAUDE.md 與自訂指令 | [技能](03-skills/) | 約 3.5 小時 |
| **進階** | 設定 MCP 伺服器與 Hooks | [進階功能](09-advanced-features/) | 約 5 小時 |

**包含全部 10 個模組的完整學習路徑：**

| 順序 | 模組 | 等級 | 時間 |
|-------|--------|-------|------|
| 1 | [斜線指令](01-slash-commands/) | 初階 | 30 分鐘 |
| 2 | [記憶](02-memory/) | 初階+ | 45 分鐘 |
| 3 | [檢查點（Checkpoints）](08-checkpoints/) | 中階 | 45 分鐘 |
| 4 | [CLI 基礎](10-cli/) | 初階+ | 30 分鐘 |
| 5 | [技能](03-skills/) | 中階 | 1 小時 |
| 6 | [Hooks](06-hooks/) | 中階 | 1 小時 |
| 7 | [MCP](05-mcp/) | 中階+ | 1 小時 |
| 8 | [子代理](04-subagents/) | 中階+ | 1.5 小時 |
| 9 | [進階功能](09-advanced-features/) | 進階 | 2-3 小時 |
| 10 | [外掛](07-plugins/) | 進階 | 2 小時 |

**[完整學習路線圖 ->](LEARNING-ROADMAP.md)**

---

## 15 分鐘快速上手

> **安裝提醒**：從 v2.1.113 開始，Claude Code 以各平台原生執行檔的形式發行（macOS/Linux/Windows）。`npm install -g @anthropic-ai/claude-code` 仍然可用——原生執行檔會在第一次使用時以選用相依套件的方式下載。從 v2.1.116 起，下載來源是 `https://downloads.claude.ai/claude-code-releases`——企業代理伺服器必須將此主機加入允許清單。

```bash
# 1. 複製這份教學
git clone https://github.com/kevin801221/claude-new-course.git
cd claude-code-tutorial

# 2. 複製你的第一個斜線指令
mkdir -p /path/to/your-project/.claude/commands
cp 01-slash-commands/optimize.md /path/to/your-project/.claude/commands/

# 3. 試試看——在 Claude Code 裡輸入：
# /optimize

# 4. 準備好進階內容了嗎？設定專案記憶：
cp 02-memory/project-CLAUDE.md /path/to/your-project/CLAUDE.md

# 5. 安裝一個技能：
cp -r 03-skills/code-review-specialist ~/.claude/skills/
```

想要完整設定嗎？以下是 **1 小時的必要設定**：

```bash
# 斜線指令（15 分鐘）
cp 01-slash-commands/*.md .claude/commands/

# 專案記憶（15 分鐘）
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 安裝一個技能（15 分鐘）
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 週末目標：加入 Hooks、子代理、MCP 與外掛
# 依照學習路徑進行有引導的設定
```

**[查看完整的安裝參考](#15-分鐘快速上手)**

---

## 你能用它做什麼？

| 使用情境 | 你會組合的功能 |
|----------|------------------------|
| **自動化程式碼審查** | 斜線指令 + 子代理 + 記憶 + MCP |
| **團隊導入** | 記憶 + 斜線指令 + 外掛 |
| **CI/CD 自動化** | CLI 參考 + Hooks + 背景任務 |
| **文件產生** | 技能 + 子代理 + 外掛 |
| **安全性稽核** | 子代理 + 技能 + Hooks（唯讀模式） |
| **DevOps 管線** | 外掛 + MCP + Hooks + 背景任務 |
| **複雜重構** | 檢查點 + 規劃模式（Planning Mode） + Hooks |

---


---

## 實戰專案工廠 (Projects)

除了 10 大系統化理論模組之外，本教學庫提供了 **9 大從輕量到生產級的實戰 Mini-projects**，以及真實世界 RAG 知識庫：

| 專案 | 目錄 | 特色與涵蓋技術 |
|---|---|---|
| **01-weekly-haiku** | [`Projects/haiku/`](Projects/haiku/) | Slash Command 實戰，定時彙整與生成團隊日報/週報 |
| **02-recipe-genie** | [`Projects/02-recipe-genie/`](Projects/02-recipe-genie/) | 料理推薦 Sub-agent 實戰，帶有完整 GitHub Actions 流程 |
| **03-youtube-notes** | [`Projects/03-youtube-notes/`](Projects/03-youtube-notes/) | 語音/逐字稿筆記抽取，大綱總結自動化管線 |
| **04-pomodoro** | [`Projects/04-pomodoro/`](Projects/04-pomodoro/) | Hook 實戰：利用 Stop hook 驅動自動化番茄鐘循環與聲音通知 |
| **05-organize-downloads**| [`Projects/05-organize-downloads/`](Projects/05-organize-downloads/) | 自動整理檔案系統，CLI 批次自動化分類 |
| **06-discord-dm-bot** | [`Projects/06-discord-dm-bot/`](Projects/06-discord-dm-bot/) | 外部 API 串接：Discord Bot 自動化私訊通知機器人 |
| **07-weekly-reports** | [`Projects/07-weekly-reports-skill/`](Projects/07-weekly-reports-skill/) | 自建複合式 Skill，自動抓取 Git Log 生成週報 |
| **08-agent-team-review**| [`Projects/08-agent-team-review/`](Projects/08-agent-team-review/) | 多 Agent 審查系統：Backend / Frontend / Test 專業 Agent 盲評審查 |
| **09-timetrace** | [`Projects/09-timetrace/`](Projects/09-timetrace/) | 現代 CLI 工具開發（Typer + Rich） |
| **Normal-RAG2Graph** | [`Projects/Normal-RAG2Graph-Project-claude/`](Projects/Normal-RAG2Graph-Project-claude/) | 知識圖譜 + Hybrid RAG 智慧問答全端架構（FastAPI + Next.js） |

---

## 多 Agent 協作生產線 (Agent Group Projects)

展示「一個大任務拆解給多個專業 Agent 分階段或平行協作」的完整工業級案例：

| 專案目錄 | 模式與特色 | 涵蓋技術 |
|---|---|---|
| [`agent_group_projects/computer-vision-wafer-detection/`](agent_group_projects/computer-vision-wafer-detection/) | **4-agent 晶圓瑕疵 YOLO 檢測全自動管線**（完成版） | 資料探勘 → 標註 → 訓練 → 推論 |
| [`agent_group_projects/computer-vision-wafer-template/`](agent_group_projects/computer-vision-wafer-template/) | **晶圓檢測空白練習版**（學生練習專用） | 親手使用 `/agents` 建立專業 Sub-agents |
| [`agent_group_projects/stock-groups-skills/`](agent_group_projects/stock-groups-skills/) | **多視角股票分析智囊團** | 基本面 + 技術面 + 新聞情緒 3 Agent 平行研析與收斂 |
| [`agent_group_projects/new-course-material2presentation-blank/`](agent_group_projects/new-course-material2presentation-blank/) | **自動化課程內容生產工廠** | 投影片大綱、教學碼與教材全自動生成 |

---

## 原生 Agent Teams 協同開發 (Agent Teams)

使用 Claude Code 原生實驗功能 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`，展示 Team Lead 協調多個獨立 Claude 實例：

| 專案目錄 | 案例內容 | 亮點 |
|---|---|---|
| [`agent_teams/ios-app-flutter-dev/`](agent_teams/ios-app-flutter-dev/) | **Flutter 冥想 App 全端開發** | 共享任務板 (Task List) + 實例互通信箱 (Mailbox)，平行跨模組開發 |

---

## 大師心法、出版書籍與帶課演練手冊

- **高階架構 Blueprint**（收錄於 [`心法/`](心法/)）：
  - 📄 `AI_Skill_Architecture_Blueprints.pdf` (AI 技能架構藍圖)
  - 📄 `Agentic_AI_Systems_Blueprint.pdf` (自主 Agent 系統工程藍圖)
  - 📄 `Claude_Design_Decoded.pdf` (Claude Code 設計哲學拆解)
  - 📄 `Unshackling_Advanced_AI.pdf` (進階 AI 生產力解放手冊)
- **書籍出版大綱**（收錄於 [`book/`](book/)）：
  - 📖 `Claude_Code_完全攻略_書籍大綱_v1.pdf` 與第 01 章書稿範本
- **12 小時帶課演練手冊**：
  - 📑 [`docs/walkthroughs/course_12hr_walkthrough.md`](docs/walkthroughs/course_12hr_walkthrough.md)（講師手冊，含 6 大階段 120 分鐘極限演練與踩坑排錯）

## 常見問題

**這是免費的嗎？**
是的。採用 MIT 授權，永久免費。可以用在個人專案、工作、團隊中——除了附上授權聲明之外沒有其他限制。

**這份教學有在維護嗎？**
積極維護中。這份教學會跟著每次 Claude Code 發行同步更新。目前版本：v2.1.263（2026 年 9 月），相容於 Claude Code 2.1 以上版本。

**這跟官方文件有什麼不同？**
官方文件是功能參考。這份教學則是搭配圖表、生產級範本與漸進式學習路徑的教學。兩者互補——先在這裡學習，需要查細節時再去看官方文件。

**要花多久才能學完全部內容？**
完整路徑大約需要 11 到 13 小時。但 15 分鐘內你就能得到立即的成效——只要複製一個斜線指令範本並試試看。

**可以搭配 Claude Sonnet / Haiku / Opus 使用嗎？**
可以。所有範本都適用於 Claude Fable 5.1、Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8 與 Claude Haiku 4.5。

**我可以貢獻嗎？**
當然可以。指南請見 [CONTRIBUTING.md](CONTRIBUTING.md)。我們歡迎新範例、錯誤修正、文件改進與社群範本。

**可以離線閱讀嗎？**
可以。執行 `uv run scripts/build_epub.py`，就能產生包含所有內容與渲染後圖表的 EPUB 電子書。

---

## 今天就開始精通 Claude Code

你已經安裝好 Claude Code 了。你跟 10 倍生產力之間，只差知道怎麼用它而已。這份教學提供你有結構的路徑、視覺化的說明，以及可以直接複製貼上的範本，帶你走到那一步。

MIT 授權，永久免費。複製它、fork 它，變成你自己的東西。

**[開始學習路徑 ->](LEARNING-ROADMAP.md)** | **[瀏覽功能目錄](CATALOG.md)** | **[15 分鐘快速上手](#15-分鐘快速上手)**

---

<details>
<summary>快速導覽——所有功能</summary>

| 功能 | 說明 | 資料夾 |
|---------|-------------|--------|
| **功能目錄** | 含安裝指令的完整參考 | [CATALOG.md](CATALOG.md) |
| **斜線指令** | 使用者手動觸發的捷徑 | [01-slash-commands/](01-slash-commands/) |
| **記憶** | 持久化上下文 | [02-memory/](02-memory/) |
| **技能** | 可重複使用的能力 | [03-skills/](03-skills/) |
| **子代理** | 專業的 AI 助理 | [04-subagents/](04-subagents/) |
| **MCP 協定** | 存取外部工具 | [05-mcp/](05-mcp/) |
| **Hooks** | 事件驅動的自動化 | [06-hooks/](06-hooks/) |
| **外掛** | 打包好的功能 | [07-plugins/](07-plugins/) |
| **檢查點** | 工作階段（session）快照與回溯 | [08-checkpoints/](08-checkpoints/) |
| **進階功能** | 規劃、思考、背景任務 | [09-advanced-features/](09-advanced-features/) |
| **CLI 參考** | 指令、旗標與選項 | [10-cli/](10-cli/) |
| **部落格文章** | 真實世界的使用範例 | [部落格文章](https://medium.com/@kevin801221) |

</details>

<details>
<summary>功能比較</summary>

| 功能 | 觸發方式 | 持久性 | 最適合 |
|---------|-----------|------------|----------|
| **斜線指令** | 手動（`/cmd`） | 僅限工作階段 | 快速捷徑 |
| **記憶** | 自動載入 | 跨工作階段 | 長期學習 |
| **技能** | 自動觸發 | 檔案系統 | 自動化工作流程 |
| **子代理** | 自動委派 | 獨立上下文 | 任務分派 |
| **MCP 協定** | 自動查詢 | 即時 | 即時資料存取 |
| **Hooks** | 事件觸發 | 依設定而定 | 自動化與驗證 |
| **外掛** | 一個指令 | 所有功能 | 完整解決方案 |
| **檢查點** | 手動／自動 | 依工作階段 | 安全實驗 |
| **規劃模式** | 手動／自動 | 規劃階段 | 複雜實作 |
| **背景任務** | 手動 | 任務持續期間 | 長時間執行的操作 |
| **CLI 參考** | 終端機指令 | 工作階段／腳本 | 自動化與腳本編寫 |

</details>

<details>
<summary>安裝快速參考</summary>

```bash
# 斜線指令
cp 01-slash-commands/*.md .claude/commands/

# 記憶
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 技能
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 子代理
cp 04-subagents/*.md .claude/agents/

# MCP
export GITHUB_TOKEN="token"
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Hooks
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 外掛
/plugin install pr-review

# 檢查點（自動啟用，於設定中調整）
# 參見 08-checkpoints/README.md

# 進階功能（於設定中調整）
# 參見 09-advanced-features/config-examples.json

# CLI 參考（不需安裝）
# 參見 10-cli/README.md 取得使用範例
```

</details>

<details>
<summary>01. 斜線指令</summary>

**位置**：[01-slash-commands/](01-slash-commands/)

**說明**：使用者手動觸發、以 Markdown 檔案儲存的捷徑

**範例**：
- `optimize.md` - 程式碼最佳化分析
- `pr.md` - Pull Request 準備
- `generate-api-docs.md` - API 文件產生器

**安裝**：
```bash
cp 01-slash-commands/*.md /path/to/project/.claude/commands/
```

**用法**：
```
/optimize
/pr
/generate-api-docs
```

**深入了解**：[探索 Claude Code 斜線指令](https://medium.com/@kevin801221/discovering-claude-code-slash-commands-cdc17f0dfb29)

</details>

<details>
<summary>02. 記憶</summary>

**位置**：[02-memory/](02-memory/)

**說明**：跨工作階段的持久化上下文

**範例**：
- `project-CLAUDE.md` - 團隊共用的專案標準
- `directory-api-CLAUDE.md` - 特定目錄的規則
- `personal-CLAUDE.md` - 個人偏好設定

**安裝**：
```bash
# 專案記憶
cp 02-memory/project-CLAUDE.md /path/to/project/CLAUDE.md

# 目錄記憶
cp 02-memory/directory-api-CLAUDE.md /path/to/project/src/api/CLAUDE.md

# 個人記憶
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

**用法**：由 Claude 自動載入

</details>

<details>
<summary>03. 技能</summary>

**位置**：[03-skills/](03-skills/)

**說明**：可重複使用、自動觸發的能力，包含指示與腳本

**範例**：
- `code-review-specialist/` - 搭配腳本的完整程式碼審查
- `brand-voice/` - 品牌語氣一致性檢查器
- `doc-generator/` - API 文件產生器

**安裝**：
```bash
# 個人技能
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 專案技能
cp -r 03-skills/code-review-specialist /path/to/project/.claude/skills/
```

**用法**：相關時自動觸發

</details>

<details>
<summary>04. 子代理</summary>

**位置**：[04-subagents/](04-subagents/)

**說明**：具備獨立上下文與自訂提示詞的專業 AI 助理

**範例**：
- `code-reviewer.md` - 完整的程式碼品質分析
- `test-engineer.md` - 測試策略與涵蓋率
- `documentation-writer.md` - 技術文件
- `secure-reviewer.md` - 專注安全性的審查（唯讀）
- `implementation-agent.md` - 完整功能實作

**安裝**：
```bash
cp 04-subagents/*.md /path/to/project/.claude/agents/
```

**用法**：由主代理自動委派

</details>

<details>
<summary>05. MCP 協定</summary>

**位置**：[05-mcp/](05-mcp/)

**說明**：用於存取外部工具與 API 的 Model Context Protocol

**範例**：
- `github-mcp.json` - GitHub 整合
- `database-mcp.json` - 資料庫查詢
- `filesystem-mcp.json` - 檔案操作
- `multi-mcp.json` - 多個 MCP 伺服器

**安裝**：
```bash
# 設定環境變數
export GITHUB_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# 透過 CLI 新增 MCP 伺服器
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# 或手動加入專案的 .mcp.json（範例請見 05-mcp/）
```

**用法**：設定完成後，Claude 會自動可以使用 MCP 工具

</details>

<details>
<summary>06. Hooks</summary>

**位置**：[06-hooks/](06-hooks/)

**說明**：由事件觸發的 shell 指令，會在 Claude Code 事件發生時自動執行

**範例**：
- `format-code.sh` - 寫入前自動格式化程式碼
- `pre-commit.sh` - 提交前執行測試
- `security-scan.sh` - 掃描安全性問題
- `log-bash.sh` - 記錄所有 bash 指令
- `validate-prompt.sh` - 驗證使用者提示詞
- `notify-team.sh` - 事件發生時傳送通知

**安裝**：
```bash
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

在 `~/.claude/settings.json` 中設定 hooks：
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write",
      "hooks": ["~/.claude/hooks/format-code.sh"]
    }],
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": ["~/.claude/hooks/security-scan.sh"]
    }]
  }
}
```

**用法**：Hooks 會在事件發生時自動執行

**Hook 類型**（5 種）：`command`、`http`、`prompt`、`mcp_tool`、`agent`——決定 hook 如何執行。

**Hook 事件**（33 個，分 4 類）——決定何時執行：
- **工具 Hooks**：`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PostToolBatch`、`PermissionRequest`、`PermissionDenied`
- **工作階段 Hooks**：`SessionStart`、`Setup`、`SessionEnd`、`Stop`、`StopFailure`、`SubagentStart`、`SubagentStop`
- **任務 Hooks**：`UserPromptSubmit`、`UserPromptExpansion`、`MessageDisplay`、`TaskCompleted`、`TaskCreated`、`TeammateIdle`——`TaskCompleted` 與 `TaskCreated` 只有在啟用 todo 工具時才會觸發，而 Opus 4.8、Sonnet 5、Fable 5、Mythos 5 及更新版本預設關閉此功能（設定 `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` 可恢復）
- **生命週期 Hooks**：`ConfigChange`、`CwdChanged`、`DirectoryAdded`、`FileChanged`、`PreCompact`、`PostCompact`、`PreModelSwitch`、`PostModelSwitch`、`WorktreeCreate`、`WorktreeRemove`、`Notification`、`InstructionsLoaded`、`Elicitation`、`ElicitationResult`

</details>

<details>
<summary>07. 外掛</summary>

**位置**：[07-plugins/](07-plugins/)

**說明**：整合指令、代理、MCP 與 hooks 的套件組合

**範例**：
- `pr-review/` - 完整的 PR 審查工作流程
- `devops-automation/` - 部署與監控
- `documentation/` - 文件產生

**安裝**：
```bash
/plugin install pr-review
/plugin install devops-automation
/plugin install documentation
```

**用法**：使用套件內建的斜線指令與功能

</details>

<details>
<summary>08. 檢查點與回溯</summary>

**位置**：[08-checkpoints/](08-checkpoints/)

**說明**：儲存對話狀態，並回溯到先前的時間點以嘗試不同做法

**核心概念**：
- **檢查點**：對話狀態的快照
- **回溯**：回到先前的檢查點
- **分支點**：從同一個檢查點嘗試多種做法

**用法**：
```
# 每次使用者輸入提示詞時，都會自動建立檢查點
# 若要回溯，按兩次 Esc，或使用：
/rewind

# 接著從五個選項中選擇：
# 1. 還原程式碼與對話
# 2. 還原對話
# 3. 還原程式碼
# 4. 從這裡開始摘要
# 5. 取消
```

**使用情境**：
- 嘗試不同的實作做法
- 從錯誤中復原
- 安全地實驗
- 比較替代方案
- 對不同設計進行 A/B 測試

</details>

<details>
<summary>09. 進階功能</summary>

**位置**：[09-advanced-features/](09-advanced-features/)

**說明**：用於複雜工作流程與自動化的進階能力

**包含**：
- **規劃模式**——在寫程式前建立詳細的實作計畫
- **延伸思考（Extended Thinking）**——針對複雜問題進行深度推理（用 `Alt+T` / `Option+T` 切換）
- **背景任務**——在不阻塞的情況下執行長時間操作
- **權限模式**——`manual`（舊稱 `default`，`default` 目前仍可使用）、`acceptEdits`、`plan`、`auto`、`dontAsk`、`bypassPermissions`
- **無介面模式（headless）**——在 CI/CD 中執行 Claude Code：`claude -p "執行測試並產生報告"`
- **工作階段管理**——`/resume`、`/rename`、`/fork`、`/branch`、`claude -c`、`claude -r`
- **設定**——在 `~/.claude/settings.json` 中自訂行為

完整設定請見 [config-examples.json](09-advanced-features/config-examples.json)。

</details>

<details>
<summary>10. CLI 參考</summary>

**位置**：[10-cli/](10-cli/)

**說明**：Claude Code 完整的命令列介面參考

**快速範例**：
```bash
# 互動模式
claude "解釋這個專案"

# 列印模式（非互動）
claude -p "審查這段程式碼"

# 處理檔案內容
cat error.log | claude -p "解釋這個錯誤"

# 給腳本用的 JSON 輸出
claude -p --output-format json "列出函式"

# 繼續工作階段
claude -r "feature-auth" "繼續實作"
```

**使用情境**：CI/CD 管線整合、腳本自動化、批次處理、多工作階段工作流程、自訂代理設定

</details>

<details>
<summary>範例工作流程</summary>

### 完整的程式碼審查工作流程

```markdown
# 使用：斜線指令 + 子代理 + 記憶 + MCP

User: /review-pr

Claude:
1. 載入專案記憶（程式碼規範）
2. 透過 GitHub MCP 取得 PR
3. 委派給 code-reviewer 子代理
4. 委派給 test-engineer 子代理
5. 統整發現
6. 提供完整審查
```

### 自動化文件產生

```markdown
# 使用：技能 + 子代理 + 記憶

User: "產生 auth 模組的 API 文件"

Claude:
1. 載入專案記憶（文件規範）
2. 偵測到文件產生請求
3. 自動觸發 doc-generator 技能
4. 委派給 api-documenter 子代理
5. 建立包含範例的完整文件
```

### DevOps 部署

```markdown
# 使用：外掛 + MCP + Hooks

User: /deploy production

Claude:
1. 執行 pre-deploy hook（驗證環境）
2. 委派給 deployment-specialist 子代理
3. 透過 Kubernetes MCP 執行部署
4. 監控進度
5. 執行 post-deploy hook（健康檢查）
6. 回報狀態
```

</details>

<details>
<summary>目錄結構</summary>

```
├── 01-slash-commands/
│   ├── optimize.md
│   ├── pr.md
│   ├── generate-api-docs.md
│   └── README.md
├── 02-memory/
│   ├── project-CLAUDE.md
│   ├── directory-api-CLAUDE.md
│   ├── personal-CLAUDE.md
│   └── README.md
├── 03-skills/
│   ├── code-review-specialist/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── templates/
│   ├── brand-voice/
│   │   ├── SKILL.md
│   │   └── templates/
│   ├── doc-generator/
│   │   ├── SKILL.md
│   │   └── generate-docs.py
│   └── README.md
├── 04-subagents/
│   ├── code-reviewer.md
│   ├── test-engineer.md
│   ├── documentation-writer.md
│   ├── secure-reviewer.md
│   ├── implementation-agent.md
│   └── README.md
├── 05-mcp/
│   ├── github-mcp.json
│   ├── database-mcp.json
│   ├── filesystem-mcp.json
│   ├── multi-mcp.json
│   └── README.md
├── 06-hooks/
│   ├── format-code.sh
│   ├── pre-commit.sh
│   ├── security-scan.sh
│   ├── log-bash.sh
│   ├── validate-prompt.sh
│   ├── notify-team.sh
│   └── README.md
├── 07-plugins/
│   ├── pr-review/
│   ├── devops-automation/
│   ├── documentation/
│   └── README.md
├── 08-checkpoints/
│   ├── checkpoint-examples.md
│   └── README.md
├── 09-advanced-features/
│   ├── config-examples.json
│   ├── planning-mode-examples.md
│   └── README.md
├── 10-cli/
│   └── README.md
└── README.md（本檔案）
```

</details>

<details>
<summary>最佳實踐</summary>

### 建議做法
- 從簡單的斜線指令開始
- 逐步加入功能
- 用記憶儲存團隊規範
- 先在本機測試設定
- 記錄自訂實作
- 對專案設定進行版本控制
- 與團隊分享外掛

### 避免做法
- 不要建立重複的功能
- 不要寫死憑證
- 不要略過文件
- 不要把簡單的任務複雜化
- 不要忽視安全性最佳實踐
- 不要提交敏感資料

</details>

<details>
<summary>疑難排解</summary>

### 功能未載入
1. 檢查檔案位置與命名
2. 確認 YAML frontmatter 語法
3. 檢查檔案權限
4. 檢查 Claude Code 版本相容性

### MCP 連線失敗
1. 確認環境變數
2. 檢查 MCP 伺服器安裝
3. 測試憑證
4. 檢查網路連線

### 子代理未委派
1. 檢查工具權限
2. 確認代理描述是否清楚
3. 檢視任務複雜度
4. 單獨測試代理

</details>

<details>
<summary>測試</summary>

這個專案包含完整的自動化測試：

- **單元測試**：使用 pytest 的 Python 測試（Python 3.10、3.11、3.12）
- **程式碼品質**：用 Ruff 進行 lint 與格式化
- **安全性**：用 Bandit 進行漏洞掃描
- **型別檢查**：用 mypy 進行靜態型別分析
- **建置驗證**：EPUB 產生測試
- **涵蓋率追蹤**：整合 Codecov

```bash
# 安裝開發相依套件
uv pip install -r requirements-dev.txt

# 執行所有單元測試
pytest scripts/tests/ -v

# 執行測試並產生涵蓋率報告
pytest scripts/tests/ -v --cov=scripts --cov-report=html

# 執行程式碼品質檢查
ruff check scripts/
ruff format --check scripts/

# 執行安全性掃描
bandit -c pyproject.toml -r scripts/ --exclude scripts/tests/

# 執行型別檢查
mypy scripts/ --ignore-missing-imports
```

每次推送到 `main`／`develop`，以及每個對 `main` 的 PR，都會自動執行測試。詳細資訊請見 [TESTING.md](.github/TESTING.md)。

</details>

<details>
<summary>EPUB 產生</summary>

想離線閱讀這份教學嗎？產生一份 EPUB 電子書：

```bash
uv run scripts/build_epub.py
```

這會產生 `claude-code-tutorial-guide.epub`，內含所有內容，包括渲染後的 Mermaid 圖表。

更多選項請見 [scripts/README.md](scripts/README.md)。

</details>

<details>
<summary>參與貢獻</summary>

發現問題，或想貢獻一個範例？歡迎加入！

**詳細指南請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md)，內容包括：**
- 貢獻類型（範例、文件、功能、錯誤回報、意見回饋）
- 如何設定開發環境
- 目錄結構與新增內容的方式
- 撰寫準則與最佳實踐
- 提交與 PR 流程

**我們的社群規範：**
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - 我們如何彼此對待
- [SECURITY.md](SECURITY.md) - 安全性政策與漏洞回報

### 回報安全性問題

如果你發現安全性漏洞，請負責任地回報：

1. **使用 GitHub 私密漏洞回報功能**：https://github.com/kevin801221/claude-new-course/security/advisories
2. **或閱讀** [.github/SECURITY_REPORTING.md](.github/SECURITY_REPORTING.md) 取得詳細說明
3. **請勿**針對安全性漏洞開公開 issue

快速開始：
1. Fork 並複製這個儲存庫
2. 建立有描述性的分支（`add/feature-name`、`fix/bug`、`docs/improvement`）
3. 依照指南進行修改
4. 提交描述清楚的 Pull Request

**需要協助**？開一個 issue 或討論串，我們會引導你完成整個流程。

</details>

<details>
<summary>延伸資源</summary>

- [Claude Code 文件](https://code.claude.com/docs/en/overview)
- [MCP 協定規格](https://modelcontextprotocol.io)
- [技能儲存庫](https://github.com/kevin801221/skills) - 現成技能的合輯
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Boris Cherny 的 Claude Code 工作流程](https://x.com/bcherny/status/2007179832300581177) - Claude Code 的創作者分享他系統化的工作流程：平行代理、共用的 CLAUDE.md、規劃模式、斜線指令、子代理，以及用於自動化長時間工作階段的驗證 hooks。

</details>

---

## 參與貢獻

我們歡迎貢獻！詳細的開始方式請見我們的[貢獻指南](CONTRIBUTING.md)。

---

## 授權條款

MIT 授權——詳見 [LICENSE](LICENSE)。可自由使用、修改與散布，唯一的要求是附上授權聲明。

---

**最後更新**：2026 年 9 月 6 日
**Claude Code 版本**：2.1.263
**資料來源**：
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/changelog
- https://code.claude.com/docs/en/permission-modes
- https://platform.claude.com/docs/en/about-claude/models/overview
- https://github.com/anthropics/claude-code/releases
- https://github.com/anthropics/claude-code/releases/tag/v2.1.154
- https://code.claude.com/docs/en/model-config
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
**相容模型**：Claude Fable 5.1、Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
