<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-code-tutorial-logo-dark.svg">
  <img alt="Claude Code 完整教學" src="resources/logos/claude-code-tutorial-logo.svg">
</picture>

# Claude Code 範例 - 完整索引

本文件提供依功能類型分類的完整範例檔案索引。

## 統計摘要

- **檔案總數**：100+ 個檔案
- **分類**：10 個功能分類
- **外掛（Plugins）**：3 個完整外掛
- **技能（Skills）**：6 個完整技能
- **Hooks**：11 個範例 hook
- **可直接使用**：所有範例

---

## 01. 斜線指令（10 個檔案）

用於常見工作流程的使用者觸發捷徑。

| 檔案 | 說明 | 使用情境 |
|------|-------------|----------|
| `optimize.md` | 程式碼最佳化分析器 | 找出效能問題 |
| `pr.md` | Pull Request 準備 | PR 工作流程自動化 |
| `generate-api-docs.md` | API 文件產生器 | 產生 API 文件 |
| `commit.md` | 提交訊息小幫手 | 標準化提交 |
| `setup-ci-cd.md` | CI/CD 管線設定 | DevOps 自動化 |
| `push-all.md` | 推送所有變更 | 快速推送工作流程 |
| `unit-test-expand.md` | 擴充單元測試涵蓋率 | 測試自動化 |
| `doc-refactor.md` | 文件重構 | 文件改進 |
| `pr-slash-command.png` | 截圖範例 | 視覺參考 |
| `README.md` | 文件 | 安裝與使用指南 |

**安裝路徑**：`.claude/commands/`

**用法**：`/optimize`、`/pr`、`/generate-api-docs`、`/commit`、`/setup-ci-cd`、`/push-all`、`/unit-test-expand`、`/doc-refactor`

---

## 02. 記憶（6 個檔案）

持久化上下文與專案標準。

| 檔案 | 說明 | 範圍 | 位置 |
|------|-------------|-------|----------|
| `project-CLAUDE.md` | 團隊專案標準 | 整個專案 | `./CLAUDE.md` |
| `directory-api-CLAUDE.md` | API 專屬規則 | 目錄 | `./src/api/CLAUDE.md` |
| `personal-CLAUDE.md` | 個人偏好設定 | 使用者 | `~/.claude/CLAUDE.md` |
| `memory-saved.png` | 截圖：記憶（Memory）已儲存 | - | 視覺參考 |
| `memory-ask-claude.png` | 截圖：詢問 Claude | - | 視覺參考 |
| `README.md` | 文件 | - | 參考 |

**安裝**：複製到適當的位置

**用法**：由 Claude 自動載入

---

## 03. 技能（23 個檔案）

自動觸發的能力，包含腳本與範本。

### 程式碼審查技能（5 個檔案）
```
code-review-specialist/
├── SKILL.md                          # 技能定義
├── scripts/
│   ├── analyze-metrics.py            # 程式碼指標分析器
│   └── compare-complexity.py         # 複雜度比較
└── templates/
    ├── review-checklist.md           # 審查檢查清單
    └── finding-template.md           # 發現項目文件
```

**用途**：完整的程式碼審查，包含安全性、效能與品質分析

**自動觸發時機**：審查程式碼時

---

### 品牌語氣技能（4 個檔案）
```
brand-voice/
├── SKILL.md                          # 技能定義
├── templates/
│   ├── email-template.txt            # Email 格式
│   └── social-post-template.txt      # 社群媒體格式
└── tone-examples.md                  # 範例訊息
```

**用途**：確保溝通內容的品牌語氣一致

**自動觸發時機**：撰寫行銷文案時

---

### 文件產生器技能（2 個檔案）
```
doc-generator/
├── SKILL.md                          # 技能定義
└── generate-docs.py                  # Python 文件擷取器
```

**用途**：從原始碼產生完整的 API 文件

**自動觸發時機**：建立／更新 API 文件時

---

### 重構技能（5 個檔案）
```
refactor/
├── SKILL.md                          # 技能定義
├── scripts/
│   ├── analyze-complexity.py         # 複雜度分析器
│   └── detect-smells.py              # 程式碼異味偵測器
├── references/
│   ├── code-smells.md                # 程式碼異味目錄
│   └── refactoring-catalog.md        # 重構模式
└── templates/
    └── refactoring-plan.md           # 重構計畫範本
```

**用途**：搭配複雜度分析的系統化程式碼重構

**自動觸發時機**：重構程式碼時

---

### Claude MD 技能（1 個檔案）
```
claude-md/
└── SKILL.md                          # 技能定義
```

**用途**：管理與最佳化 CLAUDE.md 檔案

---

### 部落格草稿技能（3 個檔案）
```
blog-draft/
├── SKILL.md                          # 技能定義
└── templates/
    ├── draft-template.md             # 部落格草稿範本
    └── outline-template.md           # 部落格大綱範本
```

**用途**：以一致的結構起草部落格文章

**另外還有**：`README.md` - 技能總覽與使用指南

**安裝路徑**：`~/.claude/skills/` 或 `.claude/skills/`

---

## 04. 子代理（10 個檔案）

具備自訂能力的專業 AI 助理。

| 檔案 | 說明 | 工具 | 使用情境 |
|------|-------------|-------|----------|
| `code-reviewer.md` | 程式碼品質分析 | Read, Grep, Glob, Bash | 完整審查 |
| `test-engineer.md` | 測試涵蓋率分析 | Read, Write, Bash, Grep | 測試自動化 |
| `documentation-writer.md` | 文件撰寫 | Read, Write, Grep | 文件產生 |
| `secure-reviewer.md` | 安全性審查（唯讀） | Read, Grep | 安全性稽核 |
| `implementation-agent.md` | 完整實作 | Read, Write, Edit, Bash, Grep, Glob | 功能開發 |
| `debugger.md` | 除錯專家 | Read, Edit, Bash, Grep, Glob | 錯誤調查 |
| `data-scientist.md` | 資料分析專家 | Bash, Read, Write | 資料工作流程 |
| `clean-code-reviewer.md` | 簡潔程式碼標準 | Read, Grep, Glob, Bash | 程式碼品質 |
| `performance-optimizer.md` | 效能瓶頸分析 | Read, Edit, Bash, Grep, Glob | 最佳化工作 |
| `README.md` | 文件 | - | 安裝與使用指南 |

**安裝路徑**：`.claude/agents/`

**用法**：由主代理自動委派

---

## 05. MCP 協定（5 個檔案）

外部工具與 API 整合。

| 檔案 | 說明 | 整合對象 | 使用情境 |
|------|-------------|-----------------|----------|
| `github-mcp.json` | GitHub 整合 | GitHub API | PR／issue 管理 |
| `database-mcp.json` | 資料庫查詢 | PostgreSQL/MySQL | 即時資料查詢 |
| `filesystem-mcp.json` | 檔案操作 | 本機檔案系統 | 檔案管理 |
| `multi-mcp.json` | 多個伺服器 | GitHub + DB + Slack | 完整整合 |
| `README.md` | 文件 | - | 安裝與使用指南 |

**安裝路徑**：`.mcp.json`（專案範圍）或 `~/.claude.json`（使用者範圍）

**用法**：`/mcp__github__list_prs` 等

---

## 06. Hooks（12 個檔案）

會自動執行的事件驅動自動化腳本。

| 檔案 | 說明 | 事件 | 使用情境 |
|------|-------------|-------|----------|
| `format-code.sh` | 自動格式化程式碼 | PostToolUse（matcher：Write） | 程式碼格式化 |
| `pre-commit.sh` | 提交前執行測試 | PreToolUse（matcher：Bash） | 測試自動化 |
| `pre-tool-check.sh` | 在指令執行前驗證與稽核 | PreToolUse（matcher：Bash） | 防護機制、稽核日誌 |
| `security-scan.sh` | 安全性掃描 | PostToolUse（matcher：Write） | 安全性檢查 |
| `dependency-check.sh` | 掃描相依套件清單中的漏洞 | PostToolUse（matcher：Write） | 供應鏈檢查 |
| `log-bash.sh` | 記錄 bash 指令 | PostToolUse（matcher：Bash） | 指令記錄 |
| `notify-team.sh` | 傳送通知 | PostToolUse（matcher：Bash） | 團隊通知 |
| `validate-prompt.sh` | 驗證提示詞 | UserPromptSubmit | 輸入驗證 |
| `session-end.sh` | 工作階段（session）結束時記錄進度 | SessionEnd | 進度追蹤 |
| `context-tracker.py` | 追蹤上下文視窗使用量 | UserPromptSubmit, Stop | 上下文監控 |
| `context-tracker-tiktoken.py` | 以 token 為單位追蹤上下文 | UserPromptSubmit, Stop | 精確計算 token |
| `README.md` | 文件 | - | 安裝與使用指南 |

**安裝路徑**：於 `~/.claude/settings.json` 中設定

**用法**：於設定中設定，自動執行

**Hook 類型**（5 種）：`command`、`http`、`prompt`、`mcp_tool`、`agent`——決定 hook 如何執行。

**Hook 事件**（33 個，分 4 類）——決定何時執行：
- 工具 Hooks：PreToolUse、PostToolUse、PostToolUseFailure、PostToolBatch、PermissionRequest、PermissionDenied
- 工作階段 Hooks：SessionStart、Setup、SessionEnd、Stop、StopFailure、SubagentStart、SubagentStop
- 任務 Hooks：UserPromptSubmit、UserPromptExpansion、MessageDisplay、TaskCompleted、TaskCreated、TeammateIdle（TaskCompleted／TaskCreated 只有在啟用 todo 工具時才會觸發——Opus 4.8、Sonnet 5、Fable 5、Mythos 5 及更新版本預設關閉）
- 生命週期 Hooks：ConfigChange、CwdChanged、DirectoryAdded、FileChanged、PreCompact、PostCompact、PreModelSwitch、PostModelSwitch、WorktreeCreate、WorktreeRemove、Notification、InstructionsLoaded、Elicitation、ElicitationResult

---

## 07. 外掛（3 個完整外掛，共 39 個檔案）

打包好的功能組合。

### PR 審查外掛（10 個檔案）
```
pr-review/
├── .claude-plugin/
│   └── plugin.json                   # 外掛清單
├── commands/
│   ├── review-pr.md                  # 完整審查
│   ├── check-security.md             # 安全性檢查
│   └── check-tests.md                # 測試涵蓋率檢查
├── agents/
│   ├── security-reviewer.md          # 安全性專家
│   ├── test-checker.md               # 測試專家
│   └── performance-analyzer.md       # 效能專家
├── mcp/
│   └── github-config.json            # GitHub 整合
├── hooks/
│   └── pre-review.js                 # 審查前驗證
└── README.md                         # 外掛文件
```

**功能**：安全性分析、測試涵蓋率、效能影響

**指令**：`/review-pr`、`/check-security`、`/check-tests`

**安裝**：`/plugin install pr-review`

---

### DevOps 自動化外掛（15 個檔案）
```
devops-automation/
├── .claude-plugin/
│   └── plugin.json                   # 外掛清單
├── commands/
│   ├── deploy.md                     # 部署
│   ├── rollback.md                   # 回滾
│   ├── status.md                     # 系統狀態
│   └── incident.md                   # 事件應變
├── agents/
│   ├── deployment-specialist.md      # 部署專家
│   ├── incident-commander.md         # 事件協調者
│   └── alert-analyzer.md             # 警示分析器
├── mcp/
│   └── kubernetes-config.json        # Kubernetes 整合
├── hooks/
│   ├── pre-deploy.js                 # 部署前檢查
│   └── post-deploy.js                # 部署後任務
├── scripts/
│   ├── deploy.sh                     # 部署自動化
│   ├── rollback.sh                   # 回滾自動化
│   └── health-check.sh               # 健康檢查
└── README.md                         # 外掛文件
```

**功能**：Kubernetes 部署、回滾、監控、事件應變

**指令**：`/deploy`、`/rollback`、`/status`、`/incident`

**安裝**：`/plugin install devops-automation`

---

### 文件外掛（14 個檔案）
```
documentation/
├── .claude-plugin/
│   └── plugin.json                   # 外掛清單
├── commands/
│   ├── generate-api-docs.md          # API 文件產生
│   ├── generate-readme.md            # README 建立
│   ├── sync-docs.md                  # 文件同步
│   └── validate-docs.md              # 文件驗證
├── agents/
│   ├── api-documenter.md             # API 文件專家
│   ├── code-commentator.md           # 程式碼註解專家
│   └── example-generator.md          # 範例產生器
├── mcp/
│   └── github-docs-config.json       # GitHub 整合
├── templates/
│   ├── api-endpoint.md               # API 端點範本
│   ├── function-docs.md              # 函式文件範本
│   └── adr-template.md               # ADR 範本
└── README.md                         # 外掛文件
```

**功能**：API 文件、README 產生、文件同步、驗證

**指令**：`/generate-api-docs`、`/generate-readme`、`/sync-docs`、`/validate-docs`

**安裝**：`/plugin install documentation`

**另外還有**：`README.md` - 外掛總覽與使用指南

---

## 08. 檢查點與回溯（2 個檔案）

儲存對話狀態，探索不同的做法。

| 檔案 | 說明 | 內容 |
|------|-------------|---------|
| `README.md` | 文件 | 完整的檢查點（Checkpoints）指南 |
| `checkpoint-examples.md` | 真實範例 | 資料庫遷移、效能最佳化、UI 迭代、除錯 |
| | | |

**核心概念**：
- **檢查點**：對話狀態的快照
- **回溯**：回到先前的檢查點
- **分支點**：嘗試多種做法

**用法**：
```
# 每次使用者輸入提示詞時，都會自動建立檢查點
# 若要回溯，按兩次 Esc，或使用：
/rewind
# 接著選擇：還原程式碼與對話、還原對話、
# 還原程式碼、從這裡開始摘要，或取消
```

**使用情境**：
- 嘗試不同的實作
- 從錯誤中復原
- 安全地實驗
- 比較解決方案
- A/B 測試

---

## 09. 進階功能（4 個檔案）

用於複雜工作流程的進階能力。

| 檔案 | 說明 | 功能 |
|------|-------------|----------|
| `README.md` | 完整指南 | 所有進階功能的文件 |
| `config-examples.json` | 設定範例 | 10+ 個特定使用情境的設定 |
| `planning-mode-examples.md` | 規劃範例 | REST API、資料庫遷移、重構 |
| `setup-auto-mode-permissions.py` | 為自動模式建立初始 `permissions.allow` | 冪等、`--dry-run` 與選用旗標 |
| 動態工作流程 | 透過 `/workflows` 進行確定性的多代理協調（v2.1.154） | 完整稽核、遷移、擴展 |
| 排程任務 | 用 `/loop` 與 cron 工具執行週期性任務 | 自動化週期性工作流程 |
| Chrome 整合 | 透過無介面 Chromium 進行瀏覽器自動化 | 網頁測試與擷取 |
| 遠端控制（擴充） | 連線方式、安全性、比較表、裝置卡片 | 遠端工作階段管理（已不再是研究預覽） |
| 跨工作階段訊息 | `SendMessage` / `ListAgents`，包含 `notify_when_idle`（v2.1.236） | 協調同一台機器上的工作階段 |
| 鍵盤自訂 | 自訂按鍵綁定、和弦支援、情境 | 個人化捷徑 |
| 桌面應用程式（擴充） | 連接器、launch.json、企業功能 | 桌面整合 |
| | | |

**涵蓋的進階功能**：

### 規劃模式
- 建立詳細的實作計畫
- 時間估計與風險評估
- 系統化的任務拆解

### 延伸思考
- 針對複雜問題進行深度推理
- 架構決策分析
- 取捨評估

### 背景任務
- 不阻塞的長時間操作
- 平行開發工作流程
- 任務管理與監控

### 動態工作流程（v2.1.154）
- 確定性地協調數十到數百個背景子代理（Subagents）
- 用扇出／管線／平行階段達成完整涵蓋
- 用 `/workflows` 檢視執行紀錄；`ultracode` `/effort` 會為工作階段啟用它
- 自 v2.1.219 起，預設規模準則為中等（目標少於 15 個代理）——可在 `/config` 中用**動態工作流程規模**變更

### 權限模式
- **manual**：對有風險的操作要求核准（v2.1.200 由 `default` 改名而來，`default` 仍可使用）
- **acceptEdits**：自動接受檔案編輯，其他操作仍會詢問
- **plan**：唯讀分析，不做任何修改
- **auto**：全部自動執行，並搭配背景安全性檢查——會用分類器審查指令與受保護目錄的寫入（透過 `autoMode` 設定物件調整）
- **dontAsk**：只執行預先核准的工具——會自動拒絕所有原本需要詢問的呼叫。Claude 只會執行符合 `permissions.allow` 的項目、唯讀的 Bash 指令，以及經 `PreToolUse` hook 核准的呼叫
- **bypassPermissions**：全部接受（需要 `--dangerously-skip-permissions`）

### 無介面模式（`claude -p`）
- CI/CD 整合
- 自動化任務執行
- 批次處理

### 工作階段管理
- 多個工作階段
- 工作階段切換與儲存
- 工作階段持久化

### 互動功能
- 鍵盤快捷鍵
- 指令歷史紀錄
- Tab 自動完成
- 多行輸入

### 設定
- 完整的設定管理
- 依環境而異的設定
- 依專案自訂

### 排程任務
- 用 `/loop` 指令執行週期性任務
- Cron 工具：CronCreate、CronList、CronDelete
- 自動化週期性工作流程

### Chrome 整合
- 透過無介面 Chromium 進行瀏覽器自動化
- 網頁測試與擷取能力
- 頁面互動與資料擷取

### 遠端控制（擴充）
- 連線方式與協定
- 安全性考量與最佳實踐
- 遠端存取選項的比較表
- 已脫離研究預覽階段——執行 `claude remote-control` 的機器會在 Claude app 的 Code 分頁中顯示為裝置卡片

### 跨工作階段訊息
- 在同一台機器的工作階段之間使用 `SendMessage`
- `notify_when_idle`——當另一個工作階段下次閒置時傳送一則選用通知（v2.1.236）
- `ListAgents` 會回報自己工作階段的名稱，並列出線上的隊友（v2.1.239）

### 鍵盤自訂
- 自訂按鍵綁定設定
- 支援多鍵和弦快捷鍵
- 依情境啟用按鍵綁定

### 桌面應用程式（擴充）
- 用於 IDE 整合的連接器
- launch.json 設定
- 企業功能與部署

---

## 10. CLI 用法（1 個檔案）

命令列介面的使用模式與參考。

| 檔案 | 說明 | 內容 |
|------|-------------|---------|
| `README.md` | CLI 文件 | 旗標、選項與使用模式 |

**主要 CLI 功能**：
- `claude` - 啟動互動式工作階段
- `claude -p "prompt"` - 無介面／非互動模式
- `claude web` - 啟動網頁工作階段
- `claude --model` - 選擇模型（Opus 5、Sonnet 5、Sonnet 4.6、Opus 4.8、Haiku 4.5）
- `claude --permission-mode` - 設定權限模式
- `claude --remote` - 透過 WebSocket 啟用遠端控制

---

## 文件檔案（13 個檔案）

| 檔案 | 位置 | 說明 |
|------|----------|-------------|
| `README.md` | `/` | 主要範例總覽 |
| `INDEX.md` | `/` | 這份完整索引 |
| `QUICK_REFERENCE.md` | `/` | 快速參考卡 |
| `README.md` | `/01-slash-commands/` | 斜線指令（Slash Commands）指南 |
| `README.md` | `/02-memory/` | 記憶指南 |
| `README.md` | `/03-skills/` | 技能指南 |
| `README.md` | `/04-subagents/` | 子代理指南 |
| `README.md` | `/05-mcp/` | MCP 指南 |
| `README.md` | `/06-hooks/` | Hooks 指南 |
| `README.md` | `/07-plugins/` | 外掛指南 |
| `README.md` | `/08-checkpoints/` | 檢查點指南 |
| `README.md` | `/09-advanced-features/` | 進階功能指南 |
| `README.md` | `/10-cli/` | CLI 指南 |

---

## 完整檔案樹

```
claude-code-tutorial/
├── README.md                                    # 主要總覽
├── INDEX.md                                     # 本檔案
├── QUICK_REFERENCE.md                           # 快速參考卡
├── claude_concepts_guide.md                     # 原始指南
│
├── 01-slash-commands/                           # 斜線指令
│   ├── optimize.md
│   ├── pr.md
│   ├── generate-api-docs.md
│   ├── commit.md
│   ├── setup-ci-cd.md
│   ├── push-all.md
│   ├── unit-test-expand.md
│   ├── doc-refactor.md
│   ├── pr-slash-command.png
│   └── README.md
│
├── 02-memory/                                   # 記憶
│   ├── project-CLAUDE.md
│   ├── directory-api-CLAUDE.md
│   ├── personal-CLAUDE.md
│   ├── memory-saved.png
│   ├── memory-ask-claude.png
│   └── README.md
│
├── 03-skills/                                   # 技能
│   ├── code-review-specialist/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── analyze-metrics.py
│   │   │   └── compare-complexity.py
│   │   └── templates/
│   │       ├── review-checklist.md
│   │       └── finding-template.md
│   ├── brand-voice/
│   │   ├── SKILL.md
│   │   ├── templates/
│   │   │   ├── email-template.txt
│   │   │   └── social-post-template.txt
│   │   └── tone-examples.md
│   ├── doc-generator/
│   │   ├── SKILL.md
│   │   └── generate-docs.py
│   ├── refactor/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── analyze-complexity.py
│   │   │   └── detect-smells.py
│   │   ├── references/
│   │   │   ├── code-smells.md
│   │   │   └── refactoring-catalog.md
│   │   └── templates/
│   │       └── refactoring-plan.md
│   ├── claude-md/
│   │   └── SKILL.md
│   ├── blog-draft/
│   │   ├── SKILL.md
│   │   └── templates/
│   │       ├── draft-template.md
│   │       └── outline-template.md
│   └── README.md
│
├── 04-subagents/                                # 子代理
│   ├── code-reviewer.md
│   ├── test-engineer.md
│   ├── documentation-writer.md
│   ├── secure-reviewer.md
│   ├── implementation-agent.md
│   ├── debugger.md
│   ├── data-scientist.md
│   ├── clean-code-reviewer.md
│   └── README.md
│
├── 05-mcp/                                      # MCP 協定
│   ├── github-mcp.json
│   ├── database-mcp.json
│   ├── filesystem-mcp.json
│   ├── multi-mcp.json
│   └── README.md
│
├── 06-hooks/                                    # Hooks
│   ├── format-code.sh
│   ├── pre-commit.sh
│   ├── security-scan.sh
│   ├── log-bash.sh
│   ├── validate-prompt.sh
│   ├── notify-team.sh
│   ├── context-tracker.py
│   ├── context-tracker-tiktoken.py
│   └── README.md
│
├── 07-plugins/                                  # 外掛
│   ├── pr-review/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   │   ├── review-pr.md
│   │   │   ├── check-security.md
│   │   │   └── check-tests.md
│   │   ├── agents/
│   │   │   ├── security-reviewer.md
│   │   │   ├── test-checker.md
│   │   │   └── performance-analyzer.md
│   │   ├── mcp/
│   │   │   └── github-config.json
│   │   ├── hooks/
│   │   │   └── pre-review.js
│   │   └── README.md
│   ├── devops-automation/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   │   ├── deploy.md
│   │   │   ├── rollback.md
│   │   │   ├── status.md
│   │   │   └── incident.md
│   │   ├── agents/
│   │   │   ├── deployment-specialist.md
│   │   │   ├── incident-commander.md
│   │   │   └── alert-analyzer.md
│   │   ├── mcp/
│   │   │   └── kubernetes-config.json
│   │   ├── hooks/
│   │   │   ├── pre-deploy.js
│   │   │   └── post-deploy.js
│   │   ├── scripts/
│   │   │   ├── deploy.sh
│   │   │   ├── rollback.sh
│   │   │   └── health-check.sh
│   │   └── README.md
│   ├── documentation/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   │   ├── generate-api-docs.md
│   │   │   ├── generate-readme.md
│   │   │   ├── sync-docs.md
│   │   │   └── validate-docs.md
│   │   ├── agents/
│   │   │   ├── api-documenter.md
│   │   │   ├── code-commentator.md
│   │   │   └── example-generator.md
│   │   ├── mcp/
│   │   │   └── github-docs-config.json
│   │   ├── templates/
│   │   │   ├── api-endpoint.md
│   │   │   ├── function-docs.md
│   │   │   └── adr-template.md
│   │   └── README.md
│   └── README.md
│
├── 08-checkpoints/                              # 檢查點
│   ├── checkpoint-examples.md
│   └── README.md
│
├── 09-advanced-features/                        # 進階功能
│   ├── config-examples.json
│   ├── planning-mode-examples.md
│   └── README.md
│
└── 10-cli/                                      # CLI 用法
    └── README.md
```

---

## 依使用情境快速開始

### 程式碼品質與審查
```bash
# 安裝斜線指令
cp 01-slash-commands/optimize.md .claude/commands/

# 安裝子代理
cp 04-subagents/code-reviewer.md .claude/agents/

# 安裝技能
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 或安裝完整外掛
/plugin install pr-review
```

### DevOps 與部署
```bash
# 安裝外掛（包含所有功能）
/plugin install devops-automation
```

### 文件
```bash
# 安裝斜線指令
cp 01-slash-commands/generate-api-docs.md .claude/commands/

# 安裝子代理
cp 04-subagents/documentation-writer.md .claude/agents/

# 安裝技能
cp -r 03-skills/doc-generator ~/.claude/skills/

# 或安裝完整外掛
/plugin install documentation
```

### 團隊標準
```bash
# 設定專案記憶
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 編輯以符合你團隊的標準
```

### 外部整合
```bash
# 設定環境變數
export GITHUB_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# 安裝 MCP 設定（專案範圍）
cp 05-mcp/multi-mcp.json .mcp.json
```

### 自動化與驗證
```bash
# 安裝 hooks
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 在設定中設定 hooks（~/.claude/settings.json）
# 參見 06-hooks/README.md
```

### 安全實驗
```bash
# 每次使用者輸入提示詞時，都會自動建立檢查點
# 若要回溯：按 Esc+Esc 或使用 /rewind
# 接著從回溯選單中選擇要還原的內容

# 範例請參見 08-checkpoints/README.md
```

### 進階工作流程
```bash
# 設定進階功能
# 參見 09-advanced-features/config-examples.json

# 使用規劃模式
/plan 實作功能 X

# 使用權限模式
claude --permission-mode plan          # 用於程式碼審查（唯讀）
claude --permission-mode acceptEdits   # 自動接受編輯
claude --permission-mode auto          # 自動核准安全的操作

# 以無介面模式在 CI/CD 中執行
claude -p "執行測試並回報結果"

# 執行背景任務
在背景執行測試

# 完整指南請參見 09-advanced-features/README.md
```

---

## 功能涵蓋矩陣

| 分類 | 指令 | 代理 | MCP | Hooks | 腳本 | 範本 | 文件 | 圖片 | 總計 |
|----------|----------|--------|-----|-------|---------|-----------|------|--------|-------|
| **01 斜線指令** | 8 | - | - | - | - | - | 1 | 1 | **10** |
| **02 記憶** | - | - | - | - | - | 3 | 1 | 2 | **6** |
| **03 技能** | - | - | - | - | 5 | 7 | 11 | - | **23** |
| **04 子代理** | - | 9 | - | - | - | - | 1 | - | **10** |
| **05 MCP** | - | - | 4 | - | - | - | 1 | - | **5** |
| **06 Hooks** | - | - | - | 11 | - | - | 1 | - | **12** |
| **07 外掛** | 11 | 9 | 3 | 3 | 3 | 3 | 7 | - | **39** |
| **08 檢查點** | - | - | - | - | - | - | 1 | 1 | **2** |
| **09 進階** | - | - | - | - | 1 | 1 | 2 | - | **4** |
| **10 CLI** | - | - | - | - | - | - | 1 | - | **1** |

---

## 學習路徑

### 初階（第 1 週）
1. ✅ 閱讀 `README.md`
2. ✅ 安裝 1-2 個斜線指令
3. ✅ 建立專案記憶檔案
4. ✅ 試試基本指令

### 中階（第 2-3 週）
1. ✅ 設定 GitHub MCP
2. ✅ 安裝一個子代理
3. ✅ 試試委派任務
4. ✅ 安裝一個技能

### 進階（第 4 週以後）
1. ✅ 安裝完整外掛
2. ✅ 建立自訂斜線指令
3. ✅ 建立自訂子代理
4. ✅ 建立自訂技能
5. ✅ 打造自己的外掛

### 專家（第 5 週以後）
1. ✅ 設定 hooks 進行自動化
2. ✅ 用檢查點進行實驗
3. ✅ 設定規劃模式（Planning Mode）
4. ✅ 有效運用權限模式
5. ✅ 為 CI/CD 設定無介面模式
6. ✅ 精通工作階段管理

---

## 依關鍵字搜尋

### 效能
- `01-slash-commands/optimize.md` - 效能分析
- `04-subagents/code-reviewer.md` - 效能審查
- `03-skills/code-review-specialist/` - 效能指標
- `07-plugins/pr-review/agents/performance-analyzer.md` - 效能專家

### 安全性
- `04-subagents/secure-reviewer.md` - 安全性審查
- `03-skills/code-review-specialist/` - 安全性分析
- `07-plugins/pr-review/` - 安全性檢查

### 測試
- `04-subagents/test-engineer.md` - 測試工程師
- `07-plugins/pr-review/commands/check-tests.md` - 測試涵蓋率

### 文件
- `01-slash-commands/generate-api-docs.md` - API 文件指令
- `04-subagents/documentation-writer.md` - 文件撰寫代理
- `03-skills/doc-generator/` - 文件產生器技能
- `07-plugins/documentation/` - 完整文件外掛

### 部署
- `07-plugins/devops-automation/` - 完整 DevOps 解決方案

### 自動化
- `06-hooks/` - 事件驅動的自動化
- `06-hooks/pre-commit.sh` - 提交前自動化
- `06-hooks/format-code.sh` - 自動格式化
- `09-advanced-features/` - CI/CD 用無介面模式

### 驗證
- `06-hooks/security-scan.sh` - 安全性驗證
- `06-hooks/validate-prompt.sh` - 提示詞驗證

### 實驗
- `08-checkpoints/` - 用回溯進行安全實驗
- `08-checkpoints/checkpoint-examples.md` - 真實範例

### 規劃
- `09-advanced-features/planning-mode-examples.md` - 規劃模式範例
- `09-advanced-features/README.md` - 延伸思考（Extended Thinking）

### 設定
- `09-advanced-features/config-examples.json` - 設定範例

---

## 備註

- 所有範例都可直接使用
- 可依你的需求修改
- 範例遵循 Claude Code 最佳實踐
- 每個分類都有自己的 README，內含詳細說明
- 腳本包含適當的錯誤處理
- 範本可自訂

---

## 參與貢獻

想新增更多範例嗎？請依照以下結構：
1. 建立適當的子目錄
2. 附上包含用法的 README.md
3. 遵循命名慣例
4. 徹底測試
5. 更新這份索引

---

**最後更新**：2026 年 8 月 25 日
**Claude Code 版本**：2.1.245
**資料來源**：
- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/permission-modes
- https://github.com/anthropics/claude-code/releases/tag/v2.1.153
- https://github.com/anthropics/claude-code/releases/tag/v2.1.154
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/en/model-config
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
**範例總數**：100+ 個檔案
**分類**：10 個功能
**Hooks**：11 個自動化腳本
**設定範例**：10+ 個情境
**可直接使用**：所有範例
