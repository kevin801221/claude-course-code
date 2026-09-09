<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 範例——快速參考卡

## 🚀 安裝快速指令

### 斜線指令
```bash
# 全部安裝
cp 01-slash-commands/*.md .claude/commands/

# 安裝特定指令
cp 01-slash-commands/optimize.md .claude/commands/
```

### 記憶
```bash
# 專案記憶
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 個人記憶
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

### 技能
```bash
# 個人技能
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 專案技能
cp -r 03-skills/code-review-specialist .claude/skills/
```

### 子代理
```bash
# 全部安裝
cp 04-subagents/*.md .claude/agents/

# 安裝特定代理
cp 04-subagents/code-reviewer.md .claude/agents/
```

### MCP
```bash
# 設定憑證
export GITHUB_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# 安裝設定（專案範圍）
cp 05-mcp/github-mcp.json .mcp.json

# 或個人範圍：加入 ~/.claude.json
```

### Hooks
```bash
# 安裝 Hooks
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 在設定中設定（~/.claude/settings.json）
```

### 外掛
```bash
# 從範例安裝（若已發布）
/plugin install pr-review
/plugin install devops-automation
/plugin install documentation
```

### 檢查點
```bash
# 每次使用者送出提示都會自動建立檢查點
# 若要回溯，按兩下 Esc 或使用：
/rewind

# 接著選擇：Restore code and conversation、Restore conversation、
# Restore code、Summarize from here 或 Never mind
```

### 進階功能
```bash
# 在設定中設定（.claude/settings.json）
# 見 09-advanced-features/config-examples.json

# 規劃模式
/plan 任務描述

# 權限模式（使用 --permission-mode 旗標）
# manual         - 每個動作都要求核准（原名 "default"；"default" 仍可作為別名使用）
# acceptEdits    - 自動接受檔案編輯，其他動作仍會詢問
# plan           - 唯讀分析，不做任何修改
# auto           - 由背景分類器自動決定權限
# dontAsk        - 只執行已預先核准的工具；其他一律拒絕
# bypassPermissions - 接受所有動作（需要 --dangerously-skip-permissions）

# 工作階段管理
/resume                # 恢復先前的對話（不帶參數 = 過往工作階段選擇器）
/rename "name"         # 為目前的工作階段命名
/fork <directive>      # 派生一個繼承對話內容的背景子代理
/branch [name]         # 切換到對話的副本，並保留原始對話
claude -c              # 繼續最近的對話
claude -r "session"    # 依名稱／ID 恢復工作階段
```

---

## 📋 功能速查表

| 功能 | 安裝路徑 | 用法 |
|---------|-------------|-------|
| **斜線指令（Slash Commands）（60+）** | `.claude/commands/*.md` | `/command-name` |
| **記憶（Memory）** | `./CLAUDE.md` | 自動載入 |
| **技能（Skills）** | `.claude/skills/*/SKILL.md` | 自動呼叫 |
| **子代理（Subagents）** | `.claude/agents/*.md` | 自動委派 |
| **MCP** | `.mcp.json`（專案）或 `~/.claude.json`（個人） | `/mcp__server__action` |
| **Hooks（33 個事件）** | `~/.claude/hooks/*.sh` | 事件觸發（5 種類型） |
| **外掛（Plugins）** | 透過 `/plugin install` | 整合所有功能 |
| **檢查點（Checkpoints）** | 內建 | `Esc+Esc` 或 `/rewind` |
| **規劃模式（Planning Mode）** | 內建 | `/plan <task>` |
| **權限模式（6 種）** | 內建 | `--allowedTools`、`--permission-mode` |
| **工作階段（session）** | 內建 | `/session <command>` |
| **背景任務** | 內建 | 在背景執行 |
| **遠端控制** | 內建 | WebSocket API |
| **網頁工作階段** | 內建 | `claude web` |
| **Git Worktree** | 內建 | `/worktree` |
| **自動記憶** | 內建 | 自動儲存到 CLAUDE.md |
| **任務清單** | 內建 | `/task list` |
| **內建技能（10 個）** | 內建 | `/batch`、`/claude-api`、`/code-review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [pr#\|branch\|path]` *(自 v2.1.215 起僅能明確呼叫——Claude 不會自行觸發；未指定等級時會沿用你上次輸入的等級，v2.1.223)*、`/simplify` *(僅做整理性的審查；自 v2.1.154 起再度獨立於 `/code-review`)*、`/debug`、`/fewer-permission-prompts`、`/loop`、`/run` *(v2.1.145+)*、`/run-skill-generator` *(v2.1.145+)*、`/verify` *(v2.1.145+；自 v2.1.215 起僅能明確呼叫——Claude 不會自行觸發)* |

---

## 🎯 常見使用情境

### 程式碼審查
```bash
# 方法 1：斜線指令
cp 01-slash-commands/optimize.md .claude/commands/
# 用法：/optimize

# 方法 2：子代理
cp 04-subagents/code-reviewer.md .claude/agents/
# 用法：自動委派

# 方法 3：技能
cp -r 03-skills/code-review-specialist ~/.claude/skills/
# 用法：自動呼叫

# 方法 4：外掛（最佳）
/plugin install pr-review
# 用法：/review-pr
```

### 文件
```bash
# 斜線指令
cp 01-slash-commands/generate-api-docs.md .claude/commands/

# 子代理
cp 04-subagents/documentation-writer.md .claude/agents/

# 技能
cp -r 03-skills/doc-generator ~/.claude/skills/

# 外掛（完整解決方案）
/plugin install documentation
```

### DevOps
```bash
# 完整外掛
/plugin install devops-automation

# 指令：/deploy、/rollback、/status、/incident
```

### 團隊標準
```bash
# 專案記憶
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 為你的團隊編輯
vim CLAUDE.md
```

### 自動化與 Hooks
```bash
# 安裝 Hooks（33 個事件、5 種類型：command、http、mcp_tool、prompt、agent）
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 範例：
# - Pre-commit 測試：pre-commit.sh
# - 自動格式化程式碼：format-code.sh
# - 安全性掃描：security-scan.sh

# 使用自動模式實現完全自主的工作流程
claude --permission-mode auto -p "重構並測試驗證模組"
# 或按 Shift+Tab 互動式切換模式
```

### 安全重構
```bash
# 每次提示前都會自動建立檢查點
# 嘗試重構
# 若成功：繼續
# 若失敗：按 Esc+Esc 或使用 /rewind 回到之前的狀態
```

### 複雜實作
```bash
# 使用規劃模式
/plan 實作使用者驗證系統

# Claude 建立詳細計畫
# 檢視並核准
# Claude 有系統地實作
```

### CI/CD 整合
```bash
# 以無介面模式執行（非互動式）
claude -p "執行所有測試並產生報告"

# 搭配 CI 專用的權限模式
claude -p "執行測試" --permission-mode dontAsk

# 搭配自動模式，實現完全自主的 CI 任務
claude --permission-mode auto -p "執行測試並修正失敗"

# 搭配 Hooks 實現自動化
# 見 09-advanced-features/README.md
```

### 學習與實驗
```bash
# 使用規劃模式進行安全分析
claude --permission-mode plan

# 安全地實驗——系統會自動建立檢查點
# 若需要回溯：按 Esc+Esc 或使用 /rewind
```

### 代理團隊（Agent Teams）
```bash
# 啟用 agent teams
export CLAUDE_AGENT_TEAMS=1

# 或在 settings.json 中設定
{ "agentTeams": { "enabled": true } }

# 開始方式：「用團隊合作的方式實作功能 X」
```

### 排程任務
```bash
# 每 5 分鐘執行一次指令
/loop 5m /check-status

# 一次性提醒
/loop 30m "提醒我檢查部署"
```

---

## 📁 檔案位置參考

```
你的專案/
├── .claude/
│   ├── commands/              # 斜線指令放這裡
│   ├── agents/                # 子代理放這裡
│   ├── skills/                # 專案技能放這裡
│   └── settings.json          # 專案設定（Hooks 等）
├── .mcp.json                  # MCP 設定（專案範圍）
├── CLAUDE.md                  # 專案記憶
└── src/
    └── api/
        └── CLAUDE.md          # 目錄專屬記憶

使用者家目錄/
├── .claude/
│   ├── commands/              # 個人指令
│   ├── agents/                # 個人代理
│   ├── skills/                # 個人技能
│   ├── hooks/                 # Hook 腳本
│   ├── settings.json          # 個人設定
│   ├── managed-settings.d/    # 受管設定（企業／組織）
│   └── CLAUDE.md              # 個人記憶
└── .claude.json               # 個人 MCP 設定（個人範圍）
```

---

## 🔍 尋找範例

### 依類別
- **斜線指令**：`01-slash-commands/`
- **記憶**：`02-memory/`
- **技能**：`03-skills/`
- **子代理**：`04-subagents/`
- **MCP**：`05-mcp/`
- **Hooks**：`06-hooks/`
- **外掛**：`07-plugins/`
- **檢查點**：`08-checkpoints/`
- **進階功能**：`09-advanced-features/`
- **CLI**：`10-cli/`

### 依使用情境
- **效能**：`01-slash-commands/optimize.md`
- **安全性**：`04-subagents/secure-reviewer.md`
- **測試**：`04-subagents/test-engineer.md`
- **文件**：`03-skills/doc-generator/`
- **DevOps**：`07-plugins/devops-automation/`

### 依複雜度
- **簡單**：斜線指令
- **中等**：子代理、記憶
- **進階**：技能、Hooks
- **完整**：外掛

---

## 🎓 學習路徑

### 第 1 天
```bash
# 閱讀總覽
cat README.md

# 安裝一個指令
cp 01-slash-commands/optimize.md .claude/commands/

# 試試看
/optimize
```

### 第 2-3 天
```bash
# 設定記憶
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
vim CLAUDE.md

# 安裝子代理
cp 04-subagents/code-reviewer.md .claude/agents/
```

### 第 4-5 天
```bash
# 設定 MCP
export GITHUB_TOKEN="your_token"
cp 05-mcp/github-mcp.json .mcp.json

# 試試 MCP 指令
/mcp__github__list_prs
```

### 第 2 週
```bash
# 安裝技能
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 讓它自動呼叫
# 只要說：「審查這段程式碼有沒有問題」
```

### 第 3 週以後
```bash
# 安裝完整外掛
/plugin install pr-review

# 使用內建功能
/review-pr
/check-security
/check-tests
```

---

## 功能亮點

| 功能 | 說明 | 用法 |
|---------|-------------|-------|
| **自動模式** | 由背景分類器把關的完全自主運作；自 v2.1.207 起在 Bedrock/Vertex/Foundry 上預設可用 | 按 `Shift+Tab` 切換模式，或使用 `--permission-mode auto` |
| **頻道** | Discord 與 Telegram 整合 | `--channels` 旗標、Discord/Telegram 機器人 |
| **語音輸入** | 用語音向 Claude 說出指令與上下文 | `/voice` 指令 |
| **輸出樣式** | 變更 Claude 的角色、語氣與預設回應格式 | `/config` → Output style，或 `outputStyle` 設定。內建選項：Default、Proactive、Explanatory、Learning、Concise |
| **狀態列** | 由指令產生的自訂工作階段底部狀態列 | `/statusline`，或 `statusLine` 設定；指令會在 stdin 收到工作階段／模型／費用／上下文的 JSON |
| **Hooks（33 個事件）** | 支援 5 種類型的擴充 Hook 系統 | command、http、mcp_tool、prompt、agent 等 Hook 類型 |
| **MCP Elicitation** | MCP 伺服器可在執行期間請求使用者輸入 | 伺服器需要澄清時會自動提示 |
| **Plugin LSP** | 外掛支援 Language Server Protocol | `userConfig`、`${CLAUDE_PLUGIN_DATA}` 變數 |
| **遠端控制** | 透過 WebSocket API 控制 Claude Code | `claude --remote` 供外部整合使用 |
| **網頁工作階段** | 瀏覽器介面的 Claude Code | `claude web` 啟動 |
| **Desktop App** | 原生桌面應用程式 | 從 claude.ai/download 下載 |
| **任務清單** | 管理背景任務 | `/task list`、`/task status <id>` |
| **自動記憶** | 從對話中自動儲存記憶 | Claude 會自動將重要上下文存入 CLAUDE.md |
| **Git Worktree** | 用於平行開發的獨立工作區 | `/worktree` 建立獨立工作區 |
| **Model Selection** | 在 Fable 5.1、Fable 5、Opus 5、Sonnet 5、Sonnet 4.6、Opus 4.8 與 Haiku 4.5 之間切換 | `/model`——自 v2.1.153 起，選擇的模型會存為新工作階段的預設值；按 `s` 則僅套用於本次工作階段 |
| **代理團隊（Agent Teams）** | 協調多個代理處理任務 | 用環境變數 `CLAUDE_AGENT_TEAMS=1` 啟用 |
| **Dynamic Workflows** *(v2.1.154)* | 確定性的多代理協調；自 v2.1.219 起預設規模準則為中等（目標少於 15 個代理） | `/workflows` 檢視執行紀錄；請 Claude 建立一個；可在 `/config` 的 **Dynamic workflow size** 中變更規模 |
| **排程任務** | 用 `/loop` 設定週期性任務 | `/loop 5m /command` 或 CronCreate 工具 |
| **Chrome Integration** | 瀏覽器自動化 | `--chrome` 旗標或 `/chrome` 指令 |
| **鍵盤快捷鍵自訂** | 自訂鍵盤綁定 | `/keybindings` 指令 |
| **/usage-credits** | 設定額外使用額度（v2.1.144 由 `/extra-usage` 更名而來；舊名稱仍可作為別名使用） | `/usage-credits` |
| **/run** *(v2.1.145+)* | 啟動此專案的應用程式，查看變更執行情形 | `/run` |
| **/verify** *(v2.1.145+)* | 建置、執行並觀察應用程式，以確認修正是否有效（自 v2.1.215 起僅能明確呼叫——Claude 不會自行觸發） | `/verify` |
| **/run-skill-generator** *(v2.1.145+)* | 教導 `/run`／`/verify` 如何處理特定專案 | `/run-skill-generator` |
| **Subagent Output Scanning** *(v2.1.210+)* | 掃描子代理回報內容中的提示詞注入樣式並加以化解 | 預設啟用，無法關閉 |
| **WebSearch Cap and Subagent Fan-Out Limits** *(v2.1.212，於 v2.1.219 擴充)* | 每個工作階段 200 次 WebSearch 呼叫上限；v2.1.217 新增並行子代理上限（預設 20）；自 v2.1.219 起子代理預設可巢狀派生子代理，最多**深度 3**（v2.1.217 曾停用巢狀派生）。每個工作階段 200 個子代理的派生上限已於 **v2.1.224 移除**——目前工作階段中子代理總數不再有任何限制 | `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`（預設 200；`/clear` 會重置）、`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`（預設 20）、`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`（預設 3；設為 1 可停用） |
| **Screen Reader Mode** *(v2.1.208)* | 供螢幕報讀軟體使用的純文字渲染模式 | `--ax-screen-reader` 旗標、`CLAUDE_AX_SCREEN_READER=1`，或設定中的 `"axScreenReader": true` |
| **Restricted Mode** *(v2.1.248+)* | 移除會執行指令或程式碼的內建工具（Bash、PowerShell、REPL）及 WebFetch，除非 `--tools` 有指名它們；忽略個人、專案與本機設定（受管設定與 `--settings` 仍會套用）；將檔案工具限制在工作目錄內；拒絕 `bypassPermissions` 與雲端工作階段 | `claude --restricted`，或設定 `CLAUDE_CODE_RESTRICTED=1` |
| **Subagent Cache TTL** *(v2.1.248+)* | 代理 frontmatter 的 `experimental.cacheTtl` 欄位可設定子代理提示詞快取的存活時間 | 在代理的 frontmatter 中加入 `experimental:`，並設定 `cacheTtl: "5m"`（或 `"1h"`）。見 [子代理](04-subagents/README.md) |
| **Forced Subagent Model** *(v2.1.257+)* | `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` 讓 `CLAUDE_CODE_SUBAGENT_MODEL` 覆寫代理 frontmatter。自 v2.1.251 起，環境變數預設不再優先——frontmatter（包含 `model: inherit`）會優先套用，除非設定此變數 | `CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 claude` |

---

## 小技巧

### 自訂
- 先照原樣使用範例
- 依你的需求修改
- 分享給團隊前先測試
- 用版本控制管理你的設定

### 最佳實踐
- 用記憶維護團隊標準
- 用外掛實現完整工作流程
- 用子代理處理複雜任務
- 用斜線指令處理快速任務

### 疑難排解
```bash
# 檢查檔案位置
ls -la .claude/commands/
ls -la .claude/agents/

# 驗證 YAML 語法
head -20 .claude/agents/code-reviewer.md

# 測試 MCP 連線
echo $GITHUB_TOKEN
```

---

## 📊 功能矩陣

| 需求 | 使用這個 | 範例 |
|------|----------|---------|
| 快速捷徑 | 斜線指令（60+） | `01-slash-commands/optimize.md` |
| 團隊標準 | 記憶 | `02-memory/project-CLAUDE.md` |
| 自動工作流程 | 技能 | `03-skills/code-review-specialist/` |
| 專門任務 | 子代理 | `04-subagents/code-reviewer.md` |
| 外部資料 | MCP（+ Elicitation） | `05-mcp/github-mcp.json` |
| 事件自動化 | Hook（33 個事件、5 種類型） | `06-hooks/pre-commit.sh` |
| 完整解決方案 | 外掛（+ LSP 支援） | `07-plugins/pr-review/` |
| 安全實驗 | 檢查點 | `08-checkpoints/checkpoint-examples.md` |
| 完全自主 | 自動模式 | `--permission-mode auto` 或 `Shift+Tab` |
| 聊天整合 | 頻道 | `--channels`（Discord、Telegram） |
| CI/CD 管線 | CLI | `10-cli/README.md` |

---

## 🔗 快速連結

- **主要指南**：`README.md`
- **完整索引**：`INDEX.md`
- **原始指南**：`claude_concepts_guide.md`

---

## 📞 常見問題

**問：我該用哪一個？**
答：先從斜線指令開始，再視需要加入其他功能。

**問：可以混用多種功能嗎？**
答：可以！它們可以搭配使用。記憶 + 指令 + MCP = 強大威力。

**問：如何分享給團隊？**
答：把 `.claude/` 目錄提交到 git。

**問：機密資訊怎麼處理？**
答：使用環境變數，絕不寫死在程式碼中。

**問：可以修改範例嗎？**
答：當然可以！它們就是給你自訂的範本。

---

## ✅ 檢查清單

新手入門檢查清單：

- [ ] 閱讀 `README.md`
- [ ] 安裝 1 個斜線指令
- [ ] 試用該指令
- [ ] 建立專案 `CLAUDE.md`
- [ ] 安裝 1 個子代理
- [ ] 設定 1 個 MCP 整合
- [ ] 安裝 1 個技能
- [ ] 試用一個完整外掛
- [ ] 依需求自訂
- [ ] 分享給團隊

---

**快速開始**：`cat README.md`

**完整索引**：`cat INDEX.md`

**這張速查卡**：隨手保留，方便快速參考！

---

**最後更新**：2026 年 9 月 2 日
**Claude Code 版本**：2.1.257
**資料來源**：
- https://code.claude.com/docs/en/changelog
- https://code.claude.com/docs/en/cli-reference
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/hooks
**相容模型**：Claude Fable 5.1、Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
