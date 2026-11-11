# Gemini CLI 與 Antigravity 協作指南 (Collaboration Guide)

本文檔說明了 Gemini CLI 如何透過自訂 Skill 與 Antigravity (例如在 Cursor 或 Windsurf 中運行的 AI Agent) 進行無縫協作。

## 1. 協作的核心機制

為了讓兩個獨立運作的 AI Agent 能夠互相溝通與交接工作，我們建立了一個共享的狀態檔案：`.antigravity_sync.md`。

這個檔案必須位於專案的根目錄。雙方都會透過讀寫這個檔案來：
* 了解目前的專案進度。
* 確認誰完成了哪些任務。
* 留下 Code Review 的反饋。
* 規劃下一步的行動清單。

## 2. Gemini CLI 端的設置 (Skill)

為了讓 Gemini CLI 了解如何進行協作，我們開發並全域安裝了一個專屬技能 (Skill)：`antigravity-collaboration`。

### 技能的安裝方式
這個技能已經透過 Gemini CLI 的內建指令全域安裝在系統中：
```bash
gemini skills install /path/to/antigravity-collaboration.skill --scope user --consent
```
安裝在 `user` scope 意味著，只要你在這台電腦上啟動 Gemini CLI，它都會具備「追蹤 Antigravity 進度與協助 Git Commit」的專業知識。

### 技能的作用
當使用者告訴 Gemini CLI：「Antigravity 完成了某個任務」，Gemini CLI 會：
1. 自動讀取 `.antigravity_sync.md` 確認狀態。
2. 使用 `git status` 與 `git diff` 檢查 Antigravity 修改的程式碼。
3. 根據專案規範 (`.agents/rules.md` 或 `GEMINI.md`) 進行 Code Review。
4. 若無問題，自動產生符合 Conventional Commits 格式的 Git Commit。
5. 更新 `.antigravity_sync.md`，將任務移至「已完成」，並列出下一步。

## 3. Antigravity 端的設置

Antigravity 無法主動得知 Gemini CLI 已經安裝了特定的 Skill。為了確保 Antigravity 也遵循這套協作流程，我們將規則寫入到 Antigravity 必定會讀取的專案設定檔中。

### 修改 `.agents/rules.md`
在專案的 `.agents/rules.md` 中的「工作流程」區塊，我們加入了以下強制規定：

> **與 Gemini CLI 的協作**：每次完成階段性任務，必須自動讀寫並更新專案根目錄的 `.antigravity_sync.md` 檔案，記錄你完成的項目、後續任務與狀態，並交由 Gemini CLI 進行 Review 與 Commit。

透過這條規則，Antigravity 就會知道它必須將進度與狀態寫入 `.antigravity_sync.md` 中，並等待 Gemini CLI 的接手。

## 4. 啟動協作的標準流程

1. **使用者啟動 Antigravity 時**，可以輸入以下指令來建立初步的共識：
   > 「請先閱讀 `.agents/rules.md` 的最新規則，並建立/更新 `.antigravity_sync.md`，然後開始我們今天的工作。」
2. **Antigravity 完成程式碼編寫後**，它會依照規則更新 `.antigravity_sync.md`。
3. **使用者通知 Gemini CLI**：
   > 「Antigravity 完成了 API 端點的開發，請幫忙 Review 並 Commit。」
4. **Gemini CLI 執行驗證與提交**，然後更新 `.antigravity_sync.md` 狀態，並規劃下一步給 Antigravity。
5. 反覆執行步驟 2 到 4，直到專案完成。