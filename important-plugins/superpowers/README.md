# Superpowers (超能力)

Superpowers 是一套專為你的 AI 程式開發助理（Coding Agents）設計的完整軟體開發方法論。它建立在一組可組合的技能（Composable Skills）和一些初始化指令之上，能確保你的 AI 助理在開發過程中切實使用這些技能。

## 快速入門

賦予你的 AI 助理超能力：[Claude Code](#claude-code)、[Codex CLI](#codex-cli)、[Codex App](#codex-app)、[Factory Droid](#factory-droid)、[Gemini CLI](#gemini-cli)、[OpenCode](#opencode)、[Cursor](#cursor)、[GitHub Copilot CLI](#github-copilot-cli)。

## 運作原理

超能力在啟動 AI 助理的那一刻就開始發揮作用。一旦它發現你準備開始構建某些東西，它*不會*直接開始動手寫程式碼，而是會退後一步，詢問你真正想要實現的目標是什麼。

一旦它從對話中提煉出明確的規格說明書（Spec），它會將其拆分成足夠短小、易於閱讀和理解的模塊，展示給你進行驗證。

當你批准了這個設計方案後，你的助理會整理出一份實作計畫（Implementation Plan）。這份計畫非常清晰詳盡，甚至連缺乏經驗、沒有專案背景、不懂得測試且審美欠佳的初級工程師都能輕鬆照著做。它高度強調真正的「紅燈-綠燈（Red/Green）測試驅動開發（TDD）」、YAGNI（You Aren't Gonna Need It，你不會需要它）以及 DRY（Don't Repeat Yourself，不要重複你自己）原則。

接著，一旦你發出「執行」的指令，它就會啟動「子代理驅動開發（Subagent-Driven-Development）」的流程。這會指派獨立的 Subagents 來完成每個工程任務，並對它們的工作進行嚴格的檢查與評審。在這種模式下，Claude 往往能夠自主運作數個小時，完全不會偏離你們當初共同制定的計畫。

此外還有許多細節，但這就是整個系統的核心。因為這些技能會自動觸發，所以你不需要進行任何特殊的設定。你的 AI 助理自然而然就擁有了「Superpowers」。


## 贊助

如果 Superpowers 曾幫助你完成了能帶來商業價值的專案，且你也樂意支持，我會非常感激你考慮[贊助我的開源工作](https://github.com/sponsors/obra)。

謝謝！

- Jesse


## 安裝方式

不同的執行環境（Harness）安裝方式會有所不同。如果你使用多個環境，請分別為每個環境安裝 Superpowers。

### Claude Code

Superpowers 可透過 [Claude 官方插件市場](https://claude.com/plugins/superpowers)取得。

#### 官方市場安裝

- 從 Anthropic 官方市場安裝此插件：

  ```bash
  /plugin install superpowers@claude-plugins-official
  ```

#### Superpowers 社群市場安裝

Superpowers 社群市場為 Claude Code 提供了 Superpowers 及其它相關插件。

- 註冊該插件市場：

  ```bash
  /plugin marketplace add obra/superpowers-marketplace
  ```

- 從此市場安裝插件：

  ```bash
  /plugin install superpowers@superpowers-marketplace
  ```

### Codex CLI

Superpowers 可透過 [Codex 官方插件市場](https://github.com/openai/plugins)取得。

- 開啟插件搜尋介面：

  ```bash
  /plugins
  ```

- 搜尋 Superpowers：

  ```bash
  superpowers
  ```

- 選擇 `Install Plugin`（安裝插件）。

### Codex App

Superpowers 可透過 [Codex 官方插件市場](https://github.com/openai/plugins)取得。

- 在 Codex 應用程式中，點擊側邊欄的 「Plugins」（插件）。
- 你應該會在 「Coding」 部分看到 `Superpowers`。
- 點擊 Superpowers 旁邊的 `+` 並按照提示進行操作。

### Factory Droid

- 註冊插件市場：

  ```bash
  droid plugin marketplace add https://github.com/obra/superpowers
  ```

- 安裝插件：

  ```bash
  droid plugin install superpowers@superpowers
  ```

### Gemini CLI

- 安裝擴充功能：

  ```bash
  gemini extensions install https://github.com/obra/superpowers
  ```

- 稍後更新：

  ```bash
  gemini extensions update superpowers
  ```

### OpenCode

OpenCode 使用其特有的插件安裝機制；即使你已經在其他環境中使用過，也請為 OpenCode 獨立安裝。

- 告訴 OpenCode：

  ```
  Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
  ```

- 詳細文件請見：[docs/README.opencode.md](docs/README.opencode.md)

### Cursor

- 在 Cursor Agent 聊天視窗中，從市場安裝：

  ```text
  /add-plugin superpowers
  ```

- 或者在插件市場中搜尋 "superpowers"。

### GitHub Copilot CLI

- 註冊插件市場：

  ```bash
  copilot plugin marketplace add obra/superpowers-marketplace
  ```

- 安裝插件：

  ```bash
  copilot plugin install superpowers@superpowers-marketplace
  ```


## 基本工作流程

1. **腦力激盪 (brainstorming)** - 在寫程式碼之前啟用。透過提問來淬煉粗略的想法、探索替代方案，並分段呈現設計以供驗證。最後保存設計文件（Design Document）。

2. **使用 Git 工作樹 (using-git-worktrees)** - 在設計批准後啟用。在新的分支上建立隔離的工作空間，執行專案設定，並驗證測試基線是否乾淨。

3. **撰寫實作計畫 (writing-plans)** - 在設計獲得批准後啟用。將工作拆分為小巧的任務（每個任務約 2-5 分鐘）。每個任務都必須有確切的檔案路徑、完整的程式碼和驗證步驟。

4. **子代理驅動開發 (subagent-driven-development)** 或 **執行計畫 (executing-plans)** - 在實作計畫制定後啟用。為每個任務分派全新的子代理（Subagent），並進行兩階段審查（首先是規格合規性，然後是程式碼品質）；或者以人類檢查點進行批次執行。

5. **測試驅動開發 (test-driven-development)** - 在實作過程中啟用。強制執行「紅燈-綠燈-重構（RED-GREEN-REFACTOR）」循環：先寫一個會失敗的測試，親眼看著它失敗，接著寫最少量的程式碼，看著它通過，然後提交。自動刪除在測試之前撰寫的程式碼。

6. **請求程式碼評審 (requesting-code-review)** - 在任務之間啟用。根據實作計畫進行評審，並按嚴重程度報告問題。嚴重問題會阻止後續的進度。

7. **完成開發分支 (finishing-a-development-branch)** - 在任務全部完成後啟用。驗證所有測試，提供合併（Merge）、PR、保留或捨棄等選項，最後清理工作樹（Worktree）。

**AI 助理會在執行任何任務之前，先檢查是否有適用的技能。** 這些是強制性的工作流程，而非僅僅是建議。


## 目錄架構與技能庫

### 技能庫 (Skills Library)

**測試 (Testing)**
- **test-driven-development** - 紅燈-綠燈-重構（RED-GREEN-REFACTOR）循環（包含測試反模式參考指南）

**除錯 (Debugging)**
- **systematic-debugging** - 四階段根因分析法（包含根因追踪 root-cause-tracing、深度防禦 defense-in-depth、以及條件式等待 condition-based-waiting 技術）
- **verification-before-completion** - 確保問題確實已被修復

**協作 (Collaboration)** 
- **brainstorming** - 蘇格拉底式的設計細化流程
- **writing-plans** - 詳細的實作計畫撰寫
- **executing-plans** - 帶有檢查點的批次計畫執行
- **dispatching-parallel-agents** - 同時執行的並行子代理工作流
- **requesting-code-review** - 提交程式碼評審前的自我檢查清單
- **receiving-code-review** - 如何應對並回應反饋意見
- **using-git-worktrees** - 並行開發分支的管理
- **finishing-a-development-branch** - 合併或 PR 的決策與分支清理工作流
- **subagent-driven-development** - 帶有兩階段審查（規格合規性與程式碼品質）的快速迭代開發

**元技能 (Meta)**
- **writing-skills** - 遵循最佳實踐創建新技能（包含測試方法論）
- **using-superpowers** - 技能系統的入門與使用說明


## 核心哲學

- **測試驅動開發 (TDD)** - 永遠先寫測試
- **系統化勝過臨時起意** - 流程重於盲目猜測
- **降低複雜度** - 以簡潔作為核心目標
- **事實勝於雄辯** - 在宣稱成功之前必須先進行驗證

閱讀[最初的發布公告](https://blog.fsck.com/2025/10/09/superpowers/)。


## 參與貢獻

Superpowers 的一般貢獻流程如下。請注意，我們通常不接受新增技能的貢獻，且任何對現有技能的更新都必須相容於我們所支援的所有 AI 助理開發環境。

1. Fork 本儲存庫
2. 切換到 `dev` 分支
3. 為你的工作建立一個新分支
4. 遵循 `writing-skills` 技能來建立和測試全新或修改過的技能
5. 提交 PR，並確保完整填寫 Pull Request 範本。

完整指南請參閱 `skills/writing-skills/SKILL.md`。


## 升級更新

Superpowers 的更新在一定程度上取決於你所使用的 AI 助理環境，但通常是自動完成的。


## 開源授權

MIT 授權條款 - 詳情請參閱 LICENSE 檔案。


## 社群與支援

Superpowers 由 [Jesse Vincent](https://blog.fsck.com) 及 [Prime Radiant](https://primeradiant.com) 團隊共同打造。

- **Discord**: [加入我們](https://discord.gg/35wsABTejz) 以獲得社群支援、提問或分享你用 Superpowers 構建的成果。
- **問題回報 (Issues)**: https://github.com/obra/superpowers/issues
- **版本公告**: [訂閱郵件](https://primeradiant.com/superpowers/) 以接收新版本通知。
