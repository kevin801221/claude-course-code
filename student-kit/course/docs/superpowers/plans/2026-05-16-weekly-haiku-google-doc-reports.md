# 01-weekly-haiku 加 Google Doc 日報/週報 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `Projects/01-weekly-haiku/` 新增 `/daily-report`、`/weekly-report` 兩個 slash command，讀 git log 加手動補充的非程式工作，透過 Google Drive MCP 建檔，MCP 失敗則落地本地草稿。

**Architecture:** 兩個獨立的 slash command markdown 檔（prompt 即實作），共用「讀 git log → 合成結構化報告 → create_file 建檔 → 失敗 fallback Write 本地」流程。檔名帶日期/ISO 週數。不動 PPT。

**Tech Stack:** Claude Code custom slash commands（`.claude/commands/*.md`）、Bash(git log/git config/date)、claude_ai Google Drive MCP（create_file / search_files）。

> 注意：slash command 是 prompt 檔不是可單元測試的程式碼。本計畫的「測試」是手動驗證情境（spec 定義的四種情境），每個 command 建檔後立刻跑一次驗證。

---

### Task 1: 建 `/daily-report` command

**Files:**
- Create: `Projects/01-weekly-haiku/.claude/commands/daily-report.md`

- [ ] **Step 1: 寫 command 檔**

寫入 `Projects/01-weekly-haiku/.claude/commands/daily-report.md`，完整內容如下：

````markdown
---
description: 讀今日 git log 加手動補充，產結構化日報並建到 Google Drive
allowed-tools: Bash(git log:*), Bash(git config:*), Bash(date:*), mcp__claude_ai_Google_Drive__create_file, mcp__claude_ai_Google_Drive__search_files
argument-hint: [非程式工作補充，選填，例：今天開了產品會、跟設計師對齊 UI]
---

請依以下步驟產出今日日報並寫進 Google Drive：

1. 取今日日期：跑 `date +%Y-%m-%d`
2. 抓今日程式工作：跑
   `git log --since="6am" --pretty=format:"%s" --author="$(git config user.email)"`
3. 讀 `$ARGUMENTS` 作為使用者補充的「非程式工作」（開會 / 溝通 / 規劃）。
   若 `$ARGUMENTS` 為空，這段略過、只用 git log。
4. 合成結構化日報，固定三段（沒內容的段落寫「（無）」，不要刪段）：
   - `## 今日完成` — 已交付的 commit 與非程式成果
   - `## 進行中` — 開了頭但還沒完
   - `## 阻塞與待辦` — 卡住的事、明天要接的事
5. 用 `mcp__claude_ai_Google_Drive__create_file` 建檔：
   - name：`日報 <YYYY-MM-DD>`（用步驟 1 的日期）
   - content：步驟 4 的日報全文（Markdown）
6. 回傳給使用者：Google Doc 連結 + 日報全文（讓他當場校對）。

## 失敗時（fallback）

若步驟 5 的 MCP 工具不存在或建檔失敗：
- 不要中斷。改用 Write 把日報存成本地檔：
  `Projects/01-weekly-haiku/日報 <YYYY-MM-DD>.md`
- 明確告訴使用者：「Google Drive MCP 未啟用，已存本地草稿到 <path>，
  你可手動貼到 Google Doc」。

## 範例輸出

```
## 今日完成
- 修好 bbox-labeler 切分比例計算錯誤
- 跟設計師對齊新版 UI 規格（非程式）

## 進行中
- inference-runner agent：推論跑通，視覺化還沒接

## 阻塞與待辦
- 等 PM 確認 test set 範圍才能跑 mAP
```

注意事項：
- 零 commit 且無 `$ARGUMENTS` 也照寫，誠實寫「今日無 commit」，不要硬編
- 不寫 git log / `$ARGUMENTS` 沒提到的事
- 段落順序固定，方便日報之間比對
````

- [ ] **Step 2: 手動驗證情境（spec 四情境的日報版）**

在本 repo 根目錄跑 `claude`，依序測：

1. `/daily-report`（無補充）→ 報告只反映今日 commit；零 commit 時誠實寫「今日無 commit」，三段都在。
2. `/daily-report 今天開了產品會、跟設計師對齊 UI`（有補充）→ 補充出現在對應段落。
3. 確認檔名為 `日報 2026-05-16` 形式（日期 = `date +%Y-%m-%d` 輸出）。
4. 模擬 MCP 失敗（無 Google Drive 整合的環境）→ 落地 `Projects/01-weekly-haiku/日報 <date>.md` 並印出提示字串。

Expected：四情境輸出都符合；三段（今日完成/進行中/阻塞與待辦）恆在；fallback 有本地檔 + 提示。

- [ ] **Step 3: 清掉驗證產生的本地草稿（若有）**

Run: `rm -f Projects/01-weekly-haiku/日報\ *.md`
Expected：無殘留草稿（不要把測試產物 commit 進 repo）。

- [ ] **Step 4: Commit**

```bash
git add Projects/01-weekly-haiku/.claude/commands/daily-report.md
git commit -m "$(cat <<'EOF'
01-weekly-haiku 加 /daily-report：今日 git log + 補充 → Google Doc

讀 date +%Y-%m-%d 與今日 commit，合手動補充的非程式工作成
三段結構化日報，用 Google Drive MCP create_file 建檔，
MCP 不可用則 fallback 落地本地 Markdown 草稿。
EOF
)"
```

---

### Task 2: 建 `/weekly-report` command

**Files:**
- Create: `Projects/01-weekly-haiku/.claude/commands/weekly-report.md`

- [ ] **Step 1: 寫 command 檔**

寫入 `Projects/01-weekly-haiku/.claude/commands/weekly-report.md`，完整內容如下：

````markdown
---
description: 讀本週 git log 加手動補充，產結構化週報並建到 Google Drive
allowed-tools: Bash(git log:*), Bash(git config:*), Bash(date:*), mcp__claude_ai_Google_Drive__create_file, mcp__claude_ai_Google_Drive__search_files
argument-hint: [非程式工作補充，選填，例：本週帶新人、跑了兩場需求訪談]
---

請依以下步驟產出本週週報並寫進 Google Drive：

1. 取本週 ISO 週數：跑 `date +%G-W%V`（例 `2026-W20`）
2. 抓本週程式工作：跑
   `git log --since="7 days ago" --pretty=format:"%s" --author="$(git config user.email)"`
3. 讀 `$ARGUMENTS` 作為使用者補充的「非程式工作」。空則略過。
4. 合成結構化週報，固定四段（沒內容寫「（無）」，不要刪段）：
   - `## 本週重點成果` — 對外可講的交付與里程碑
   - `## 數據` — commit 數（數步驟 2 的輸出行數）、主要動到的模組 / 資料夾
   - `## 下週計畫` — 接下來要做的
   - `## 風險` — 卡點、依賴、需要協助的
5. 用 `mcp__claude_ai_Google_Drive__create_file` 建檔：
   - name：`週報 <YYYY-Www>`（用步驟 1 的週數）
   - content：步驟 4 的週報全文（Markdown）
6. 回傳：Google Doc 連結 + 週報全文。

## 失敗時（fallback）

若步驟 5 MCP 工具不存在或失敗：不中斷，改用 Write 存
`Projects/01-weekly-haiku/週報 <YYYY-Www>.md`，並提示使用者已存本地草稿、可手動貼到 Google Doc。

## 範例輸出

```
## 本週重點成果
- inference-runner 上線，mAP@0.5 0.991
- 帶完新人上手 Claude Code（非程式）

## 數據
- 共 23 個 commit，主要動 Projects/01-weekly-haiku、agent_group_projects

## 下週計畫
- 接視覺化 dashboard
- 跑第二輪需求訪談

## 風險
- test set 範圍還沒拍板，可能影響下週排程
```

注意事項：
- 零 commit 且無 `$ARGUMENTS` 也照寫，誠實寫「本週無 commit」
- `## 數據` 的 commit 數直接數步驟 2 的輸出行數，不要另外跑指令
- 不寫 log / `$ARGUMENTS` 沒提到的事
````

- [ ] **Step 2: 手動驗證情境（spec 四情境的週報版）**

在本 repo 根目錄跑 `claude`，依序測：

1. `/weekly-report`（無補充）→ 只反映本週 commit；四段恆在。
2. `/weekly-report 本週帶新人、跑了兩場需求訪談`（有補充）→ 補充進對應段落。
3. 確認檔名為 `週報 2026-W20` 形式（週數 = `date +%G-W%V` 輸出）。
4. 模擬 MCP 失敗 → 落地 `Projects/01-weekly-haiku/週報 <YYYY-Www>.md` + 提示。

Expected：四情境符合；四段（本週重點成果/數據/下週計畫/風險）恆在；fallback 正常。

- [ ] **Step 3: 清掉驗證產生的本地草稿（若有）**

Run: `rm -f Projects/01-weekly-haiku/週報\ *.md`
Expected：無殘留草稿。

- [ ] **Step 4: Commit**

```bash
git add Projects/01-weekly-haiku/.claude/commands/weekly-report.md
git commit -m "$(cat <<'EOF'
01-weekly-haiku 加 /weekly-report：本週 git log + 補充 → Google Doc

讀 date +%G-W%V 與本週 commit，合手動補充的非程式工作成
四段結構化週報（重點成果/數據/下週計畫/風險），用 Google
Drive MCP create_file 建檔，MCP 不可用則 fallback 本地草稿。
EOF
)"
```

---

### Task 3: 更新 README

**Files:**
- Modify: `Projects/01-weekly-haiku/README.md`（全檔替換）

- [ ] **Step 1: 全檔覆寫 README**

把 `Projects/01-weekly-haiku/README.md` 整檔替換為以下內容：

````markdown
# 小專案 1：/weekly-haiku ＋ Google Doc 日報/週報

> 同樣讀 git log，一個寫詩、一個寫正式報告寫進雲端。
> 週五 `/weekly-haiku` 給你一首詩；每天 `/daily-report`、週末 `/weekly-report`
> 自動把工作整理成結構化報告，建進 Google Drive。

## 為什麼做

- ❌ 週五下班前想 review 這週做了啥，但 git log 30 個 commit 看了想睡
- ❌ 寫日報/週報像在交作業，每天重複勞動
- ✅ 用俳句的形式 review，順便產生可貼 IG 限動的素材（/weekly-haiku）
- ✅ git log + 一句話補充非程式工作 → 結構化報告直接進 Google Doc（/daily-report、/weekly-report）

## 用到的 Claude Code feature

| Command | Feature | 資料來源 | 輸出 |
|---|---|---|---|
| `/weekly-haiku` | 自訂 slash command + `Bash(git log:*)` | 本週 git log | 俳句（終端） |
| `/daily-report` | slash command + `$ARGUMENTS` + Google Drive MCP | 今日 git log + 手動補充 | Google Doc「日報 YYYY-MM-DD」 |
| `/weekly-report` | slash command + `$ARGUMENTS` + Google Drive MCP | 本週 git log + 手動補充 | Google Doc「週報 YYYY-Www」 |

> 教學重點：三個 command 同源（git log）不同形，示範「一個 command 一件事」＋ `$ARGUMENTS` 傳參 ＋ MCP 外部整合。

## 安裝

### 方式 A：個人層（所有 repo 都能用）

```bash
mkdir -p ~/.claude/commands
cp .claude/commands/weekly-haiku.md ~/.claude/commands/
cp .claude/commands/daily-report.md ~/.claude/commands/
cp .claude/commands/weekly-report.md ~/.claude/commands/
```

### 方式 B：專案層（commit 進 git，團隊共用）

```bash
mkdir -p .claude/commands
cp /path/to/this-folder/.claude/commands/*.md .claude/commands/
git add .claude/commands/
git commit -m "Add weekly-haiku / daily-report / weekly-report commands"
```

### Google Doc 報告的前置（只有 /daily-report、/weekly-report 需要）

`/daily-report`、`/weekly-report` 需要 Google Drive MCP。本教學用 Claude 內建的
claude_ai Google Drive 整合（首次用會跳授權）。**沒有 MCP 也能用** —
會自動 fallback 存一份 Markdown 草稿到專案目錄，再手動貼到 Google Doc。

## 使用

```bash
cd ~/your-repo
claude

> /weekly-haiku
> /daily-report 今天開了產品會、跟設計師對齊 UI
> /weekly-report 本週帶新人、跑了兩場需求訪談
```

`$ARGUMENTS`（後面那串）是選填的非程式工作補充；只想用 git log 就直接 `/daily-report`。

## 進階變化

- **`/commit-roast`** — 改成吐槽自己（「你這週留了 5 個 console.log」）
- **`/team-sonnet`** — 讀整個 team 的 commit 寫十四行詩
- **月報累積** — 用 search_files 找本月日報、讀出來拼接（注意 MCP 無 append，要覆寫）
- **指定資料夾** — create_file 指定 parent，把報告收進 Google Drive 的「工作日誌」資料夾
- **多語版** — prompt 加「同時給英文版」給跨國團隊

## 故障排除

| 症狀 | 解法 |
|---|---|
| `command not found: /daily-report` | 確認檔案在 `~/.claude/commands/` 或 `.claude/commands/` |
| Claude 拒絕跑 git log | 確認 frontmatter 有 `allowed-tools: Bash(git log:*)` |
| 俳句字數不對 | prompt 加更明確的「5 字 / 7 字 / 5 字」要求 |
| 「Google Drive MCP 未啟用，已存本地草稿」 | 正常 fallback；要真的寫進 Google Doc 需先啟用 Google Drive 整合並完成授權 |
| Google Doc 沒出現 | 到 Google Drive 根目錄搜尋「日報」/「週報」；MCP 預設建在根目錄 |
| 報告抓不到今日 commit | 確認 commit 作者 email = `git config user.email`；`/daily-report` 用 `--since="6am"`，凌晨跑可能抓不到 |
````

- [ ] **Step 2: 驗證 README 與實作一致**

人工核對清單：
- 三個 command 檔名與 README 表格一致（`weekly-haiku.md` / `daily-report.md` / `weekly-report.md`）。
- README 提到的 `allowed-tools`、`$ARGUMENTS`、fallback 字串與 Task 1/2 command 檔內容一致。
- 故障排除表的「Google Drive MCP 未啟用，已存本地草稿」與 command 檔 fallback 提示字串一致。

Expected：無不一致。

- [ ] **Step 3: Commit**

```bash
git add Projects/01-weekly-haiku/README.md
git commit -m "$(cat <<'EOF'
01-weekly-haiku README 擴成三 command 對照

加 /daily-report、/weekly-report 的安裝/使用/故障排除，
新增三 command 同源不同形對照表，補 Google Drive MCP
前置與 fallback 說明。
EOF
)"
```

---

## Self-Review

**1. Spec coverage：**

| Spec 要求 | 對應 Task |
|---|---|
| 兩個獨立 command `/daily-report` `/weekly-report` | Task 1、Task 2 |
| frontmatter（allowed-tools + argument-hint） | Task 1/2 Step 1 |
| `/daily-report` 三段、`date +%Y-%m-%d`、`--since="6am"` | Task 1 Step 1 |
| `/weekly-report` 四段、`date +%G-W%V`、`--since="7 days ago"` | Task 2 Step 1 |
| 手動補充走 `$ARGUMENTS` 不互動追問 | Task 1/2 Step 1（步驟 3） |
| MCP 失敗落地本地草稿 + 提示 | Task 1/2 Step 1（fallback 段） |
| 零 commit 且無補充也照寫 | Task 1/2 Step 1（注意事項） |
| 四種測試情境 | Task 1/2 Step 2 |
| README 故障排除表涵蓋 command not found / 拒跑 git log / MCP 未啟用 / Doc 沒出現 | Task 3 Step 1 |
| 不動 PPT、不做月報累積/互動追問/資料夾分類 | 全計畫未含這些 Task；README 進階變化僅列為延伸 |

無缺漏。

**2. Placeholder scan：** command 檔內 `<YYYY-MM-DD>` / `<YYYY-Www>` / `<path>` 是執行期值（非計畫 placeholder），command prompt 已說明取值來源。計畫步驟皆含完整內容，無 TBD/TODO。

**3. Type consistency：** fallback 提示字串「Google Drive MCP 未啟用，已存本地草稿」在 Task 1、Task 2、Task 3（故障排除表）三處一致；檔名格式 `日報 YYYY-MM-DD` / `週報 YYYY-Www` 三處一致；MCP 工具名 `mcp__claude_ai_Google_Drive__create_file` 全計畫一致。
