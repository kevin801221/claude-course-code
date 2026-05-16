# 設計：01-weekly-haiku 加 Google Doc 日報/週報

- 日期：2026-05-16
- 範圍：只動 `Projects/01-weekly-haiku/` 專案，不動 PPT
- 機制：session 內建的 claude_ai Google Drive MCP

## 目標

在現有「純 slash command 教學專案」01-weekly-haiku 上，新增兩個 slash command，
讀 git log（+ 手動補充的非程式工作）合成結構化日報/週報，透過 Google Drive MCP
建檔到 Google Drive，並回傳連結與全文給使用者校對。

和現有 `/weekly-haiku` 形成教學對照：同樣讀 git log，一個寫俳句（純本地），
一個寫正式報告（外部整合）。教學上同時示範「slash command + MCP + `$ARGUMENTS`」。

## 做法選擇

採 **Approach A：兩個獨立 slash command**（`/daily-report`、`/weekly-report`）。

- 否決 B（單一參數化 command）：一個 prompt 塞兩種流程，教學拆解較糊。
- 否決 C（改用 skill）：與 `Projects/07-weekly-reports-skill/` 功能重疊，
  且破壞 01 作為 slash command 教學專案的定位。

## 新增/異動檔案

```
Projects/01-weekly-haiku/.claude/commands/daily-report.md   (新增)
Projects/01-weekly-haiku/.claude/commands/weekly-report.md  (新增)
Projects/01-weekly-haiku/README.md                          (更新)
```

## Command 設計

### 共用 frontmatter

```yaml
---
description: <逐 command 不同>
allowed-tools: Bash(git log:*), Bash(git config:*), Bash(date:*),
  mcp__claude_ai_Google_Drive__create_file,
  mcp__claude_ai_Google_Drive__search_files
argument-hint: [非程式工作補充，選填]
---
```

### `/daily-report` 流程

1. 跑 `git log --since="6am" --pretty=format:"%s" --author="$(git config user.email)"`
   抓今日 commit（程式工作）。
2. 讀 `$ARGUMENTS` 作為使用者補充的非程式工作（開會/溝通/規劃）；空白則只用 git log。
3. 合成結構化日報，段落固定：
   - `## 今日完成`
   - `## 進行中`
   - `## 阻塞與待辦`
4. 用 `mcp__claude_ai_Google_Drive__create_file` 建檔，檔名 `日報 YYYY-MM-DD`
   （日期取自 `date +%Y-%m-%d`）。
5. 回傳 Google Doc 連結 + 日報全文（讓使用者當場校對）。

### `/weekly-report` 流程

同 `/daily-report`，差異：

- git log 改 `--since="7 days ago"`。
- 檔名 `週報 YYYY-Www`，週數取 `date +%G-W%V`（ISO 週數，例 `2026-W20`）。
- 段落改：
  - `## 本週重點成果`
  - `## 數據`（commit 數、主要模組）
  - `## 下週計畫`
  - `## 風險`

## 錯誤處理

- **MCP 未連上 / 建檔失敗**：不中斷流程。改落地一份 Markdown 草稿到
  `Projects/01-weekly-haiku/` 目錄（檔名同上 + `.md`），並明確提示
  「Google Drive MCP 未啟用，已存本地草稿到 <path>」。
- **零 commit 且無 `$ARGUMENTS`**：仍產出報告，誠實寫「今日（本週）無 commit」，
  對齊 `/weekly-haiku` 的「失敗也照寫」精神。
- **手動補充輸入方式**：一律走 `$ARGUMENTS`，不互動追問（確認過）。

## 測試（README 故障排除表 + 手動驗證情境）

四種情境各跑一次，確認輸出合理：

1. 有 commit、無補充 → 報告只反映 commit。
2. 無 commit、有補充 → 報告只反映補充。
3. 有 commit、有補充 → 兩者合併。
4. MCP 未啟用 → 落地本地草稿並提示。

README 故障排除表至少涵蓋：command not found、Claude 拒絕跑 git log、
MCP 未啟用、Google Doc 沒出現。

## 不做（YAGNI）

- 不做累積到同一份月報（MCP 無 append，覆寫有風險）。
- 不做互動追問補充內容。
- 不做資料夾分類（不指定 parent，建在 Drive 根目錄）。
- 不動 PPT。
