---
description: 為本程式碼庫生成全面的驗證命令
---

# 生成終極驗證命令 (Generate Ultimate Validation Command)

深度分析本程式碼庫，並建立一個能全面驗證所有內容的 `.claude/commands/validate.md` 檔案。

## 步驟 0：探索真實使用者工作流 (Discover Real User Workflows)

**在分析工具之前，請先了解使用者「實際」在做什麼：**

1. 閱讀工作流文件：
   - README.md —— 尋找「使用方式 (Usage)」、「快速開始 (Quickstart)」、「範例 (Examples)」等章節。
   - CLAUDE.md/AGENTS.md 或類似檔案 —— 尋找工作流模式。
   - docs/ 資料夾 —— 使用者指南、教學。

2. 識別外部整合：
   - 應用程式使用了哪些 CLI？ (檢查 Dockerfile 以了解已安裝的工具)
   - 呼叫了哪些外部 API？ (Telegram, Slack, GitHub 等)
   - 與哪些服務進行互動？

3. 從文件中提取完整的使用者旅程 (User Journeys)：
   - 尋找類似「修復問題 (GitHub)：」或「使用者執行 X → 然後 Y → 然後 Z」的範例。
   - 每個工作流都應成為一個端到端 (E2E) 測試場景。

**重要：您的 E2E 測試應該鏡像文件中的實際工作流，而不僅僅是測試內部 API。**

## 步驟 1：深度程式碼庫分析

探索程式碼庫以了解：

**現有哪些驗證工具：**
- Lint 檢查配置： `.eslintrc*`, `.pylintrc`, `ruff.toml` 等。
- 型別檢查： `tsconfig.json`, `mypy.ini` 等。
- 風格/格式化： `.prettierrc*`, `black`, `.editorconfig`。
- 單元測試： `jest.config.*`, `pytest.ini`, 測試目錄。
- 套件管理員腳本： `package.json` 腳本, `Makefile`, `pyproject.toml` 工具。

**應用程式的功能：**
- 前端：路由、頁面、組件、使用者流程。
- 後端：API 端點、身分驗證、資料庫操作。
- 資料庫：Schema、遷移 (Migrations)、模型。
- 基礎設施：Docker 服務、依賴項。

**目前是如何測試的：**
- 現有的測試檔案與模式。
- CI/CD 工作流 (`.github/workflows/` 等)。
- `package.json` 或腳本中的測試命令。

## 步驟 2：生成 validate.md

建立包含以下階段的 `.claude/commands/validate.md` (僅包含程式碼庫中存在的階段)：

### 第一階段：Lint 檢查 (Linting)
執行專案中找到的實際 Linter 指令 (例如： `npm run lint`, `ruff check` 等)。

### 第二階段：型別檢查 (Type Checking)
執行找到的實際型別檢查指令 (例如： `tsc --noEmit`, `mypy .` 等)。

### 第三階段：風格檢查 (Style Checking)
執行找到的實際格式化檢查指令 (例如： `prettier --check`, `black --check` 等)。

### 第四階段：單元測試 (Unit Testing)
執行找到的實際測試指令 (例如： `npm test`, `pytest` 等)。

### 第五階段：端到端測試 (End-to-End Testing) (請發揮創意並保持全面性)

測試文件中完整的使用者工作流，而不僅僅是內部 API。

**E2E 測試的三個層級：**

1. **內部 API** (您自然會測試的部分)：
   - 測試適配器 (Adapter) 端點是否正常。
   - 資料庫查詢是否成功。
   - 指令是否能執行。

2. **外部整合** (您「必須」測試的部分)：
   - CLI 操作 (GitHub CLI 建立 Issue/PR 等)。
   - 平台 API (發送 Telegram 訊息、在 Slack 發文)。
   - 應用程式依賴的任何外部服務。

3. **完整使用者旅程** (能提供 100% 置信度的部分)：
   - 從頭到尾遵循文件中的工作流。
   - 範例：「使用者要求機器人修復 GitHub 問題」→ 機器人複製儲存庫 → 進行變更 → 建立 PR → 在問題下留言。
   - 像使用者在生產環境中實際使用應用程式那樣進行測試。

**優秀 vs 差勁 E2E 測試範例：**
- ❌ 差勁：測試 `/clone` 指令是否將資料儲存在資料庫中。
- ✅ 優秀：複製儲存庫 → 載入指令 → 執行指令 → 驗證 Git Commit 已建立。
- ✅ 極佳：建立 GitHub Issue → 機器人接收 Webhook → 分析問題 → 建立 PR → 在問題下留言並附上 PR 連結。

**處理方式：**
- 使用 Docker 進行隔離、可重複的測試。
- 根據需要建立測試數據/儲存庫/問題。
- 在外部系統 (GitHub, 資料庫, 檔案系統) 中驗證結果。
- 測試結束後進行清理。

## 重要：不遺餘力，直到一切都經過驗證

**您的任務是建立一個面面俱到的驗證命令。**

- 文件中的每個使用者工作流都應經過端到端測試。
- 每個外部整合都應經過演練 (GitHub CLI, API 等)。
- 每個 API 端點都應被觸及。
- 每個錯誤情況都應經過驗證。
- 應確認資料庫完整性。
- 驗證應如此徹底，以至於手動測試變得完全沒必要。

如果 `/validate` 通過，使用者應能 100% 確信其應用程式在生產環境中能正常運作。不要滿足於部分覆蓋 —— 請使其全面、具備創意且完整。

## 輸出

將生成的驗證命令寫入 `.claude/commands/validate.md`。

該命令應該是可執行的、實用的，並能提供對程式碼庫的完整信心。
