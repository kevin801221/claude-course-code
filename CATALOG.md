<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 功能目錄

> Claude Code 所有功能的快速參考指南：指令、代理、技能（Skills）、外掛（Plugins）與 Hooks。

**導覽**：[指令](#斜線指令) | [權限模式](#權限模式) | [子代理（Subagents）](#子代理) | [技能](#技能) | [外掛](#外掛) | [MCP 伺服器](#mcp-伺服器) | [Hooks](#hooks) | [記憶（Memory）](#記憶檔案) | [新功能](#新功能)

---

## 摘要

| 功能 | 內建 | 範例 | 總計 | 參考資料 |
|---------|----------|----------|-------|-----------|
| **斜線指令** | 60+ | 8 | 68+ | [01-slash-commands/](01-slash-commands/) |
| **子代理** | 6 | 9 | 15 | [04-subagents/](04-subagents/) |
| **技能** | 10 個內建 | 6 | 16 | [03-skills/](03-skills/) |
| **外掛** | - | 3 | 3 | [07-plugins/](07-plugins/) |
| **MCP 伺服器** | 1 | 4 | 5 | [05-mcp/](05-mcp/) |
| **Hooks** | 33 個事件 | 11 | 44 | [06-hooks/](06-hooks/) |
| **記憶** | 7 種類型 | 3 | 10 | [02-memory/](02-memory/) |
| **總計** | **117** | **44** | **161** | |

---

## 斜線指令

指令是使用者手動觸發、執行特定動作的捷徑。

### 內建指令

| 指令 | 說明 | 使用時機 |
|---------|-------------|-------------|
| `/help` | 顯示說明資訊 | 開始使用、學習指令 |
| `/btw` | 暫時性的旁支問題——不會污染主要上下文 | 快速的離題問題 |
| `/chrome` | 設定 Chrome 整合 | 瀏覽器自動化 |
| `/clear` | 清除對話紀錄 | 重新開始、減少上下文 |
| `/diff` | 互動式差異檢視器。在全螢幕 TUI（v2.1.260+）中，它會在對話旁開啟一個差異面板，此面板會保持開啟，並在 Claude 每次編輯檔案或執行指令時重新整理；傳統渲染器則會以檢視器取代提示列 | 檢視變更 |
| `/config` | 檢視／編輯設定 | 自訂行為 |
| `/status` | 顯示工作階段（session）狀態 | 檢查目前狀態 |
| `/agents` | 列出可用的代理 | 查看委派選項 |
| `/skills` | 列出可用的技能 | 查看自動呼叫能力 |
| `/hooks` | 列出已設定的 Hooks | 除錯自動化流程 |
| `/insights` | 分析工作階段模式 | 工作階段最佳化 |
| `/install-slack-app` | 安裝 Claude Slack 應用程式 | Slack 整合 |
| `/keybindings` | 自訂鍵盤快捷鍵 | 按鍵自訂 |
| `/mcp` | 列出 MCP 伺服器 | 檢查外部整合 |
| `/memory` | 檢視已載入的記憶檔案 | 除錯上下文載入 |
| `/mobile` | 產生行動裝置 QR code | 行動裝置存取 |
| `/passes` | 檢視使用方案 | 訂閱資訊 |
| `/plugin` | 管理外掛 | 安裝／移除擴充功能 |
| `/plan` | 進入規劃模式（Planning Mode） | 複雜的實作 |
| `/proactive` | `/loop` 的別名（v2.1.105） | 與 `/loop` 相同 |
| `/recap` | 回到工作階段時顯示摘要 | 離開後回來，快速掌握先前的進度 |
| `/rewind` | 回溯到檢查點（Checkpoints） | 復原變更、探索其他做法 |
| `/checkpoint` | 管理檢查點 | 儲存／還原狀態 |
| `/cost` | 開啟 `/usage` 費用分頁的捷徑別名（v2.1.118+） | 監控花費 |
| `/context` | 顯示上下文視窗使用量 | 管理對話長度 |
| `/export` | 匯出對話 | 儲存供日後參考 |
| `/usage-credits` | 設定額外使用額度（v2.1.144 由 `/extra-usage` 更名而來；舊名稱仍可作為別名使用） | 速率限制管理 |
| `/feedback` | 提交意見回饋或錯誤回報 | 回報問題 |
| `/login` | 使用 Anthropic 帳號驗證 | 存取功能 |
| `/logout` | 登出 | 切換帳號 |
| `/sandbox` | 切換沙箱模式 | 安全地執行指令 |
| `/doctor` | 執行診斷 | 疑難排解 |
| `/reload-plugins` | 重新載入已安裝的外掛。自 v2.1.221 起，大多數安裝會立即生效；只有在安裝摘要顯示 `Run /reload-plugins to activate.` 時才需要執行。自 v2.1.260+ 起可在無介面工作階段（headless）中使用，因此也會出現在 Claude Code Desktop 與 SDK 的指令清單中 | 外掛管理 |
| `/reload-skills` | 不重新啟動即可重新掃描技能目錄（v2.1.152） | 技能管理 |
| `/workflows` | 檢視執行中與已完成的動態工作流程（v2.1.154） | 多代理協調 |
| `/release-notes` | 顯示發行說明 | 查看新功能 |
| `/remote-control` | 啟用遠端控制 | 遠端存取 |
| `/permissions` | 管理權限 | 控制存取權 |
| `/session` | 管理工作階段 | 多工作階段工作流程 |
| `/rename` | 重新命名目前的工作階段 | 整理工作階段 |
| `/resume` | 恢復先前的工作階段 | 繼續工作 |
| `/todo` | 檢視／管理待辦清單 | 追蹤任務 |
| `/tui` | 切換全螢幕 TUI（文字使用者介面）模式 | 在全螢幕或 tmux 中無閃爍渲染 |
| `/tasks` | 檢視背景任務 | 監控非同步作業 |
| `/copy` | 將最後一則回應複製到剪貼簿 | 快速分享輸出 |
| `/teleport`（別名 `/tp`） | 在此終端機中恢復 Claude Code on the web 工作階段；會開啟選擇器。需要 claude.ai 訂閱 | 遠端繼續工作 |
| `/desktop` | 開啟 Claude Desktop 應用程式 | 切換到桌面介面 |
| `/theme` | 變更色彩主題；v2.1.118 新增可透過 `~/.claude/themes/<name>.json` 自訂具名主題（外掛也可以附帶 `themes/` 目錄） | 自訂外觀 |
| `/usage` | 用量／費用／統計的正式指令——將 `/cost` 與 `/stats` 合併為單一分頁檢視（v2.1.118）；自 v2.1.149 起，費用檢視會依類別（技能、子代理、外掛、各 MCP 伺服器）拆解花費。在 **VSCode 擴充功能**（v2.1.174）中，`/usage`（帳號與用量）對話框新增了歸因明細——快取未命中、長上下文成本、子代理，以及 24 小時與 7 天期間內各技能／代理／外掛／MCP 的用量 | 監控額度與費用 |
| `/focus` | 切換專注檢視（無干擾的輸出顯示） | 減少長時間任務中的視覺雜訊 |
| `/fork` | 將對話複製到新的獨立背景工作階段（v2.1.212+） | 平行探索其他做法 |
| `/subtask` | 派生一個繼承對話內容並回報結果的分支子代理（v2.1.212+） | 委派旁支任務又不失去目前進度 |
| `/stats` | 開啟 `/usage` 統計分頁的捷徑別名（v2.1.118+） | 檢視工作階段指標 |
| `/statusline` | 設定狀態列 | 自訂狀態顯示 |
| `/stickers` | 檢視工作階段貼紙 | 有趣的獎勵 |
| `/fast` | 切換快速輸出模式；適用於 **Opus 5 與 Opus 4.8**（v2.1.219） | 加快回應速度 |
| `/terminal-setup` | 設定終端機整合 | 設定終端機功能 |
| `/undo` | **已不再列於文件中**——於 v2.1.108 新增作為 `/rewind` 的別名，但官方指令參考中已不再出現 | 請改用 `/rewind`（或 `Esc Esc`） |
| `/upgrade` | 檢查更新 | 版本管理 |
| `/team-onboarding` | 根據此專案的 Claude Code 使用方式產生隊友上手指南 | 協助新隊友上手（v2.1.101） |
| `/code-review ultra` | 對目前的變更執行雲端多代理程式碼審查。`/ultrareview` 仍保留為別名；建議使用 `/code-review ultra` 呼叫。Pro 與 Max 方案含 3 次免費執行，之後需要使用額度 | 合併前由多個代理進行深度審查（v2.1.112） |
| `/fewer-permission-prompts` | 掃描逐字稿，為常見的唯讀工具提出優先順序允許清單 | 減少專案中重複出現的權限提示（v2.1.112） |
| `/skill-doctor` | 顯示哪些已載入的技能未被使用，以及它們佔用多少上下文成本。會在 `/plugin` 管理器的 **Stats** 分頁中開啟；在 `-p` 模式下以文字輸出 | 移除不再需要的技能（v2.1.252+） |

### 自訂指令（範例）

| 指令 | 說明 | 使用時機 | 範圍 | 安裝方式 |
|---------|-------------|-------------|-------|--------------|
| `/optimize` | 分析程式碼以進行最佳化 | 效能改善 | 專案 | `cp 01-slash-commands/optimize.md .claude/commands/` |
| `/pr` | 準備 Pull Request | 提交 PR 之前 | 專案 | `cp 01-slash-commands/pr.md .claude/commands/` |
| `/generate-api-docs` | 產生 API 文件 | 記錄 API | 專案 | `cp 01-slash-commands/generate-api-docs.md .claude/commands/` |
| `/commit` | 建立含上下文的 git commit | 提交變更 | 個人 | `cp 01-slash-commands/commit.md .claude/commands/` |
| `/push-all` | 加入暫存、提交並推送 | 快速部署 | 個人 | `cp 01-slash-commands/push-all.md .claude/commands/` |
| `/doc-refactor` | 重新調整文件結構 | 改善文件 | 專案 | `cp 01-slash-commands/doc-refactor.md .claude/commands/` |
| `/setup-ci-cd` | 設定 CI/CD 管線 | 新專案 | 專案 | `cp 01-slash-commands/setup-ci-cd.md .claude/commands/` |
| `/unit-test-expand` | 擴大測試涵蓋率 | 改善測試 | 專案 | `cp 01-slash-commands/unit-test-expand.md .claude/commands/` |

> **範圍**：`個人` = 個人工作流程（`~/.claude/commands/`）、`專案` = 團隊共用（`.claude/commands/`）

**參考資料**：[01-slash-commands/](01-slash-commands/) | [官方文件](https://code.claude.com/docs/en/interactive-mode)

**快速安裝（所有自訂指令）**：
```bash
cp 01-slash-commands/*.md .claude/commands/
```

---

## 權限模式

Claude Code 支援 6 種權限模式，用來控制工具使用的授權方式。

| 模式 | 說明 | 使用時機 |
|------|-------------|-------------|
| `manual` | 每次工具呼叫都會詢問 | 標準互動式使用（v2.1.200 由 `default` 更名而來；`default` 仍可使用） |
| `acceptEdits` | 自動接受檔案編輯，其他動作仍會詢問 | 可信任的編輯工作流程 |
| `plan` | 僅唯讀工具，不寫入 | 規劃與探索 |
| `auto` | 所有動作皆可執行，並由背景安全分類器檢查 | 長時間任務，降低提示疲勞 |
| `bypassPermissions` | 略過所有權限檢查 | CI/CD、無介面環境 |
| `dontAsk` | 略過需要權限的工具 | 非互動式指令腳本 |

> **備註**：`auto` 模式需要符合資格的方案、模型與供應商——見 [09-advanced-features/](09-advanced-features/#自動模式)。請只在可信任的沙箱環境中使用 `bypassPermissions`。

**參考資料**：[官方文件](https://code.claude.com/docs/en/permissions)

---

## 子代理

針對特定任務、擁有獨立上下文的專門 AI 助理。

> **預設會開啟巢狀派生，深度為 3（v2.1.219）**：子代理可以派生自己的子代理，最多可在主對話下延伸三層。設定 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` 可變更此限制，設為 `1` 則停用巢狀派生。（沿革：v2.1.172–v2.1.216 預設巢狀最多 5 層且無法變更；v2.1.217 將巢狀派生改為選擇性啟用，深度為 1；v2.1.219 將預設值改為 3。）關於限制某個子代理可派生哪些子代理的 `Agent(agent_type)` 語法，請見 [04-subagents/README.md](04-subagents/README.md#限制可派生的子代理)。

### 內建子代理

| 代理 | 說明 | 工具 | 模型 | 使用時機 |
|-------|-------------|-------|-------|-------------|
| **general-purpose** | 多步驟任務、研究 | 所有工具 | 繼承模型 | 複雜研究、多檔案任務 |
| **Plan** | 實作規劃 | Read, Glob, Grep, Bash | 繼承模型 | 架構設計、規劃 |
| **Explore** | 探索程式碼庫 | Read, Glob, Grep | 繼承（上限為 Opus） | 快速搜尋、理解程式碼 |
| **claude** | 適合不屬於特定專門代理的任務的通用選項 | 所有工具 | 繼承模型 | 沒有專門代理的任務；背景工作階段派送時的預設代理 |
| **statusline-setup** | 狀態列設定 | Bash, Read, Write | Sonnet 4.6 | 設定狀態列顯示 |
| **claude-code-guide** | 說明與文件 | Read, Glob, Grep | Haiku 4.5 | 取得協助、學習功能 |

### 子代理設定欄位

| 欄位 | 型別 | 說明 |
|-------|------|-------------|
| `name` | string | 代理識別碼 |
| `description` | string | 代理的功能說明 |
| `model` | string | 覆寫使用的模型（例如 `haiku-4.5`） |
| `tools` | array | 允許使用的工具清單 |
| `effort` | string | 推理投入程度（`low`、`medium`、`high`） |
| `initialPrompt` | string | 代理啟動時注入的系統提示詞 |
| `disallowedTools` | array | 明確禁止此代理使用的工具 |

### 自訂子代理（範例）

| 代理 | 說明 | 使用時機 | 範圍 | 安裝方式 |
|-------|-------------|-------------|-------|--------------|
| `code-reviewer` | 全面的程式碼品質檢查 | 程式碼審查工作階段 | 專案 | `cp 04-subagents/code-reviewer.md .claude/agents/` |
| `clean-code-reviewer` | 依 Clean Code 原則審查 | 可維護性審查 | 專案 | `cp 04-subagents/clean-code-reviewer.md .claude/agents/` |
| `test-engineer` | 測試策略與涵蓋率 | 測試規劃 | 專案 | `cp 04-subagents/test-engineer.md .claude/agents/` |
| `documentation-writer` | 技術文件撰寫 | API 文件、指南 | 專案 | `cp 04-subagents/documentation-writer.md .claude/agents/` |
| `secure-reviewer` | 著重安全性的審查 | 安全稽核 | 專案 | `cp 04-subagents/secure-reviewer.md .claude/agents/` |
| `implementation-agent` | 完整功能實作 | 功能開發 | 專案 | `cp 04-subagents/implementation-agent.md .claude/agents/` |
| `debugger` | 根因分析 | 錯誤調查 | 個人 | `cp 04-subagents/debugger.md .claude/agents/` |
| `data-scientist` | SQL 查詢、資料分析 | 資料相關任務 | 個人 | `cp 04-subagents/data-scientist.md .claude/agents/` |
| `performance-optimizer` | 效能剖析與調校 | 瓶頸調查 | 專案 | `cp 04-subagents/performance-optimizer.md .claude/agents/` |

> **範圍**：`個人` = 個人使用（`~/.claude/agents/`）、`專案` = 團隊共用（`.claude/agents/`）

**參考資料**：[04-subagents/](04-subagents/) | [官方文件](https://code.claude.com/docs/en/sub-agents)

**快速安裝（所有自訂代理）**：
```bash
cp 04-subagents/*.md .claude/agents/
```

---

## 技能

透過指示、腳本與範本自動呼叫的能力。

### 範例技能

| 技能 | 說明 | 自動呼叫時機 | 範圍 | 安裝方式 |
|-------|-------------|-------------------|-------|--------------|
| `code-review-specialist` | 全面的程式碼審查 | 「審查這段程式碼」、「檢查品質」 | 專案 | `cp -r 03-skills/code-review-specialist .claude/skills/` |
| `brand-voice` | 品牌一致性檢查工具 | 撰寫行銷文案時 | 專案 | `cp -r 03-skills/brand-voice .claude/skills/` |
| `doc-generator` | API 文件產生器 | 「產生文件」、「記錄 API」 | 專案 | `cp -r 03-skills/doc-generator .claude/skills/` |
| `refactor` | 系統化的程式碼重構（依 Martin Fowler 的方法） | 「重構這段程式碼」、「整理程式碼」 | 個人 | `cp -r 03-skills/refactor ~/.claude/skills/` |
| `claude-md` | 建立或更新 CLAUDE.md 檔案 | 「建立 CLAUDE.md」、「稽核 CLAUDE.md」 | 專案 | `cp -r 03-skills/claude-md .claude/skills/` |
| `blog-draft` | 根據想法與資料草擬部落格文章 | 「寫一篇部落格文章」、「草擬一篇文章」 | 個人 | `cp -r 03-skills/blog-draft ~/.claude/skills/` |

> **範圍**：`個人` = 個人使用（`~/.claude/skills/`）、`專案` = 團隊共用（`.claude/skills/`）

### 技能結構

```
~/.claude/skills/skill-name/
├── SKILL.md          # 技能定義與指示
├── scripts/          # 輔助腳本
└── templates/        # 輸出範本
```

### 技能 Frontmatter 欄位

技能可在 `SKILL.md` 中使用 YAML frontmatter 進行設定：

| 欄位 | 型別 | 說明 |
|-------|------|-------------|
| `name` | string | 技能顯示名稱 |
| `description` | string | 技能的功能說明 |
| `autoInvoke` | array | 觸發自動呼叫的用語 |
| `effort` | string | 推理投入程度（`low`、`medium`、`high`） |
| `shell` | string | 腳本使用的 shell（`bash`、`zsh`、`sh`） |

**參考資料**：[03-skills/](03-skills/) | [官方文件](https://code.claude.com/docs/en/skills)

**快速安裝（所有技能）**：
```bash
cp -r 03-skills/* ~/.claude/skills/
```

### 內建技能

| 技能 | 說明 | 自動呼叫時機 |
|-------|-------------|-------------------|
| `/batch` | 對多個檔案執行提示詞 | 批次作業 |
| `/claude-api` | 使用 Claude API 建置應用程式 | API 開發 |
| `/debug` | 除錯失敗的測試／錯誤 | 除錯工作階段 |
| `/design` *(研究預覽版，v2.1.233+)* | 建立多畫板設計畫布——UI 模型、畫面流程、到達頁面、海報——以視覺方式而非撰寫程式碼來調整。適用於 Pro／Max／Team／Enterprise | 想用手動調整而非撰寫 HTML 來設計畫面或頁面時 |
| `/fewer-permission-prompts` | 掃描逐字稿並提出優先順序允許清單 | 減少重複出現的權限提示 |
| `/loop` | 定時執行提示詞 | 週期性任務 |
| `/run` *(v2.1.145+)* | 啟動此專案的應用程式，查看變更執行情形 | 在實際應用程式中驗證變更 |
| `/run-skill-generator` *(v2.1.145+)* | 教導 `/run`／`/verify` 如何處理特定專案 | 首次為專案設定 `/run` |
| `/code-review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [pr#\|branch\|path]` | 審查目前的差異——或指定 PR、分支或路徑——找出正確性方面的錯誤。`--fix` 會直接套用審查結果的修正，`--comment` 會以行內留言貼到 PR 上。未指定等級時會沿用你上次輸入的等級（v2.1.223）。較低的投入等級已在 v2.1.218 移到**背景子代理**執行；`high`、`xhigh`、`max` 也在 v2.1.232 跟進，因此審查輸出不再佔滿對話內容 | 寫完程式碼後、送出 PR 之前 |
| `/simplify` *(自 v2.1.154 起再度獨立)* | 僅做整理性的審查（重用／簡化／效率／視角），並直接套用修正；不找錯誤 | 只想整理程式碼、不找錯誤時 |
| `/verify` *(v2.1.145+)* | 建置、執行並觀察應用程式，以確認修正是否有效 | 端對端驗證修正結果 |

---

## 外掛

整合指令、代理、MCP 伺服器與 Hooks 的組合包。

### 範例外掛

| 外掛 | 說明 | 組成 | 使用時機 | 範圍 | 安裝方式 |
|--------|-------------|------------|-------------|-------|--------------|
| `pr-review` | PR 審查工作流程 | 3 個指令、3 個代理、GitHub MCP | 程式碼審查 | 專案 | `/plugin install pr-review` |
| `devops-automation` | 部署與監控 | 4 個指令、3 個代理、K8s MCP | DevOps 任務 | 專案 | `/plugin install devops-automation` |
| `documentation` | 文件產生套件 | 4 個指令、3 個代理、範本 | 文件 | 專案 | `/plugin install documentation` |

> **範圍**：`專案` = 團隊共用、`個人` = 個人工作流程

### 外掛結構

```
.claude-plugin/
├── plugin.json       # 資訊清單檔
├── commands/         # 斜線指令
├── agents/           # 子代理
├── skills/           # 技能
├── mcp/              # MCP 設定
├── hooks/            # Hook 腳本
└── scripts/          # 工具腳本
```

**參考資料**：[07-plugins/](07-plugins/) | [官方文件](https://code.claude.com/docs/en/plugins)

**外掛管理指令**：
```bash
/plugin list              # 列出已安裝的外掛
/plugin install <name>    # 安裝外掛
/plugin remove <name>     # 移除外掛
claude plugin update <name>   # 更新外掛（CLI；文字說明中提到的 /plugin update 斜線形式並未列在指令參考中）
```

---

## MCP 伺服器

用於存取外部工具與 API 的 Model Context Protocol 伺服器。

### 常見的 MCP 伺服器

| 伺服器 | 說明 | 使用時機 | 範圍 | 安裝方式 |
|--------|-------------|-------------|-------|--------------|
| **GitHub** | PR 管理、Issue、程式碼 | GitHub 工作流程 | 專案 | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` |
| **Database** | SQL 查詢、資料存取 | 資料庫操作 | 專案 | `claude mcp add db -- npx -y @modelcontextprotocol/server-postgres` |
| **Filesystem** | 進階檔案操作 | 複雜的檔案任務 | 個人 | `claude mcp add fs -- npx -y @modelcontextprotocol/server-filesystem` |
| **Slack** | 團隊溝通 | 通知、更新 | 專案 | 在設定中設定 |
| **Google Docs** | 文件存取 | 文件編輯、審閱 | 專案 | 在設定中設定 |
| **Asana** | 專案管理 | 任務追蹤 | 專案 | 在設定中設定 |
| **Stripe** | 付款資料 | 財務分析 | 專案 | 在設定中設定 |
| **Memory** | 持久記憶 | 跨工作階段回憶 | 個人 | 在設定中設定 |
| **Context7** | 函式庫文件 | 查詢最新文件 | 內建 | 內建 |

> **範圍**：`專案` = 團隊（`.mcp.json`）、`個人` = 個人（`~/.claude.json`）、`內建` = 預先安裝

### MCP 設定範例

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**參考資料**：[05-mcp/](05-mcp/) | [MCP 協定文件](https://modelcontextprotocol.io)

**快速安裝（GitHub MCP）**：
```bash
export GITHUB_TOKEN="your_token" && claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

---

## Hooks

根據 Claude Code 事件執行 shell 指令的事件驅動自動化。

### Hook 事件

| 事件 | 說明 | 觸發時機 | 使用情境 |
|-------|-------------|----------------|-----------|
| `SessionStart` | 工作階段開始／恢復 | 工作階段初始化 | 設定作業 |
| `Setup` | 初次環境設定（每個工作階段一次） | 工作階段首次啟動 | 佈建工具、安裝相依套件 |
| `InstructionsLoaded` | 已載入指示 | 載入 CLAUDE.md 或規則檔 | 自訂指示處理 |
| `UserPromptSubmit` | 提示詞處理之前 | 使用者送出訊息 | 輸入驗證 |
| `UserPromptExpansion` | 使用者提示詞展開（解析 @ 提及、斜線指令） | 展開之後、送出之前 | 轉換或檢查展開後的提示詞 |
| `PreToolUse` | 工具執行之前 | 任何工具執行前 | 驗證、記錄 |
| `PermissionRequest` | 顯示權限對話框 | 敏感動作之前 | 自訂核准流程 |
| `PermissionDenied` | 使用者拒絕權限提示 | 拒絕權限之後 | 記錄、分析、政策強制執行 |
| `PostToolUse` | 工具成功之後 | 任何工具完成後 | 格式化、通知 |
| `PostToolUseFailure` | 工具執行失敗 | 工具發生錯誤後 | 錯誤處理、記錄 |
| `PostToolBatch` | 一批工具呼叫完成之後 | 一批工具結束時 | 彙整報告、批次驗證 |
| `Notification` | 已送出通知 | Claude 送出通知時 | 外部警示 |
| `MessageDisplay` | 顯示助理訊息文字 | 訊息渲染期間 | 轉換或隱藏顯示的文字 |
| `SubagentStart` | 已派生子代理 | 子代理任務開始 | 初始化子代理上下文 |
| `SubagentStop` | 子代理完成 | 子代理任務完成 | 串接後續動作 |
| `Stop` | Claude 完成回應 | 回應完成 | 清理、回報 |
| `StopFailure` | API 錯誤導致回合結束 | 發生 API 錯誤時 | 錯誤復原、記錄 |
| `TeammateIdle` | 隊友代理閒置 | 代理團隊（Agent Teams）協調 | 分派工作 |
| `TaskCompleted` | 任務標記為完成（僅在待辦事項工具啟用時觸發——見 [Hooks](06-hooks/README.md#hook-事件)） | 任務完成 | 任務後處理 |
| `TaskCreated` | 透過 TaskCreate 建立任務（僅在待辦事項工具啟用時觸發——見 [Hooks](06-hooks/README.md#hook-事件)） | 建立新任務 | 任務追蹤、記錄 |
| `ConfigChange` | 設定已更新 | 設定被修改 | 因應設定變更 |
| `CwdChanged` | 工作目錄變更 | 目錄變更時 | 目錄專屬設定 |
| `DirectoryAdded` | 工作階段中途註冊新的工作目錄 | `/add-dir` 或 SDK 的 `register_repo_root` | 為新目錄設定工具 |
| `FileChanged` | 監看的檔案發生變更 | 檔案被修改 | 檔案監控、重新建置 |
| `PreCompact` | 壓縮（compact）操作之前 | 上下文壓縮 | 保存狀態 |
| `PostCompact` | 壓縮完成之後 | 壓縮完成 | 壓縮後動作 |
| `PreModelSwitch` | 套用所請求的模型切換之前 | 請求切換模型時 | 攔截或否決模型變更 |
| `PostModelSwitch` | 工作階段模型變更之後 | 模型切換完成 | 記錄或因應模型變更 |
| `WorktreeCreate` | 正在建立 worktree | 已建立 Git worktree | 設定 worktree 環境 |
| `WorktreeRemove` | 正在移除 worktree | 已移除 Git worktree | 清理 worktree 資源 |
| `Elicitation` | MCP 伺服器請求輸入 | MCP elicitation | 輸入驗證 |
| `ElicitationResult` | 使用者回應 elicitation 請求 | 使用者回應 | 回應處理 |
| `SessionEnd` | 工作階段終止 | 工作階段結束 | 清理、儲存狀態 |

### 範例 Hooks

| Hook | 說明 | 事件 | 範圍 | 安裝方式 |
|------|-------------|-------|-------|--------------|
| `pre-tool-check.sh` | 封鎖／警告有風險的 Bash 指令 | PreToolUse:Bash | 個人 | `cp 06-hooks/pre-tool-check.sh ~/.claude/hooks/` |
| `security-scan.sh` | 安全性掃描 | PostToolUse:Write | 專案 | `cp 06-hooks/security-scan.sh .claude/hooks/` |
| `format-code.sh` | 自動格式化 | PostToolUse:Write | 個人 | `cp 06-hooks/format-code.sh ~/.claude/hooks/` |
| `validate-prompt.sh` | 提示詞驗證 | UserPromptSubmit | 專案 | `cp 06-hooks/validate-prompt.sh .claude/hooks/` |
| `context-tracker.py` | Token 使用量追蹤 | UserPromptSubmit, Stop | 個人 | `cp 06-hooks/context-tracker.py ~/.claude/hooks/` |
| `context-tracker-tiktoken.py` | Token 使用量追蹤（tiktoken，準確率約 90–95%） | UserPromptSubmit, Stop | 個人 | `cp 06-hooks/context-tracker-tiktoken.py ~/.claude/hooks/` |
| `pre-commit.sh` | Pre-commit 驗證 | PreToolUse:Bash | 專案 | `cp 06-hooks/pre-commit.sh .claude/hooks/` |
| `log-bash.sh` | 指令記錄 | PostToolUse:Bash | 個人 | `cp 06-hooks/log-bash.sh ~/.claude/hooks/` |
| `dependency-check.sh` | 資訊清單變更時掃描漏洞 | PostToolUse:Write | 專案 | `cp 06-hooks/dependency-check.sh .claude/hooks/` |
| `notify-team.sh` | git push 時通知團隊 | PostToolUse:Bash | 專案 | `cp 06-hooks/notify-team.sh .claude/hooks/` |
| `session-end.sh` | 工作階段結束時擷取進度 | SessionEnd | 個人 | `cp 06-hooks/session-end.sh ~/.claude/hooks/` |

> **範圍**：`專案` = 團隊（`.claude/settings.json`）、`個人` = 個人（`~/.claude/settings.json`）

### Hook 設定

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "~/.claude/hooks/pre-tool-check.sh"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "~/.claude/hooks/format-code.sh"
      }
    ]
  }
}
```

**參考資料**：[06-hooks/](06-hooks/) | [官方文件](https://code.claude.com/docs/en/hooks)

**快速安裝（所有 Hooks）**：
```bash
mkdir -p ~/.claude/hooks && cp 06-hooks/*.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.sh
```

---

## 記憶檔案

跨工作階段自動載入的持久上下文。

### 記憶類型

| 類型 | 位置 | 範圍 | 使用時機 |
|------|----------|-------|-------------|
| **Managed Policy** | 組織管理的政策 | 組織 | 強制執行組織層級標準 |
| **Project** | `./CLAUDE.md` | 專案（團隊） | 團隊標準、專案上下文 |
| **Project Rules** | `.claude/rules/` | 專案（團隊） | 模組化的專案規則 |
| **User** | `~/.claude/CLAUDE.md` | 個人 | 個人偏好設定 |
| **User Rules** | `~/.claude/rules/` | 個人 | 模組化的個人規則 |
| **Local** | `./CLAUDE.local.md` | 本機（git 已忽略） | 機器專屬的本機覆寫設定（已加入 gitignore）。https://code.claude.com/docs/en/memory 已將此列為官方支援的每位開發者覆寫檔案。 |
| **自動記憶** | 自動 | 工作階段 | 自動擷取的洞見與修正 |

> **範圍**：`組織` = 由管理員管理、`專案` = 透過 git 與團隊共用、`個人` = 個人偏好設定、`本機` = 不會提交、`工作階段` = 自動管理

**參考資料**：[02-memory/](02-memory/) | [官方文件](https://code.claude.com/docs/en/memory)

**快速安裝**：
```bash
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

---

## 新功能

| 功能 | 說明 | 使用方式 |
|---------|-------------|------------|
| **/focus** | 切換無干擾輸出顯示的專注檢視（v2.1.110） | 執行 `/focus` 以減少長時間任務的視覺雜訊 |
| **/proactive** | `/loop` 的別名——行為與週期性任務相同（v2.1.105） | `/proactive` 可與 `/loop` 互換使用 |
| **/recap** | 回到既有工作階段時顯示摘要（v2.1.108） | 離開後回來時執行 `/recap`，快速掌握先前的進度 |
| **/tui** | 切換全螢幕 TUI（文字使用者介面）模式以無閃爍渲染（v2.1.110） | 在全螢幕終端機或 tmux 中使用 `/tui` |
| **/undo** | **已不再列於文件中**——於 v2.1.108 新增作為 `/rewind` 的別名，但官方指令參考中已不再出現 | 請改用 `/rewind`（或 `Esc Esc`） |
| **Monitor Tool** | 監看背景指令的 stdout 串流並依事件反應，取代輪詢（v2.1.98+） | 透過 [進階功能](09-advanced-features/) 使用 Monitor 工具 |
| **輸出樣式** | 透過系統提示詞變更 Claude 的角色、語氣與預設回應格式。內建選項：Default、Proactive、Explanatory、Learning、Concise | `/config` → Output style，或設定 `outputStyle`。`/output-style` 指令已在 v2.1.91 移除。見 [進階功能](09-advanced-features/#輸出樣式) |
| **狀態列** | 透過指令算繪自訂狀態列，指令會在 stdin 收到工作階段、模型、費用與上下文的 JSON | `/statusline` 或 `statusLine` 設定。見 [進階功能](09-advanced-features/#狀態列) |
| **Community Marketplace** | 通過 Anthropic 自動驗證的第三方外掛，每個都釘選到特定的 commit SHA | `/plugin marketplace add anthropics/claude-plugins-community`，接著 `/plugin install <name>@claude-community` |
| **/team-onboarding** | 根據專案的 Claude Code 設定自動產生隊友上手指南（v2.1.101） | 在專案中執行 `/team-onboarding` |
| **遠端控制** | 透過 API 遠端控制 Claude Code 工作階段。**已不再是研究預覽版**——任何執行 `claude remote-control` 的機器都會在 Claude app 的 Code 分頁中顯示為裝置卡片，因此可以從手機上啟動該機器的工作階段 | 在該機器上執行 `claude remote-control`，接著在 Claude app 中選擇該裝置卡片。見 [進階功能](09-advanced-features/README.md) |
| **網頁工作階段** | 在瀏覽器環境中執行 Claude Code | 透過 `claude web` 或 Anthropic Console 存取 |
| **Desktop App** | Claude Code 的原生桌面應用程式 | 使用 `/desktop`，或從 Anthropic 網站下載 |
| **Cross-Session Messaging** | 工作階段之間可以互相傳訊息——包括你的其他機器與雲端工作階段——可透過 `ListAgents` 探索（v2.1.224+，macOS/Linux） | 見 [進階功能](09-advanced-features/README.md#跨工作階段訊息)；用 `crossSessionInbound` 控制傳入訊息 |
| **Self-Hosted Runner** | 在自己的機器或容器上執行 Claude Code 的 web、行動裝置與桌面工作階段（v2.1.224+，Team/Enterprise） | `claude self-hosted-runner setup`；見 [CLI](10-cli/README.md) |
| **`archive` 外掛來源** | 從 HTTPS zip 安裝外掛，可選擇以 `sha256` 釘選版本（v2.1.224+） | 見 [外掛](07-plugins/README.md#archive-來源v21224) |
| **`command` 外掛來源** | 由本機安裝的工具印出外掛目錄路徑（v2.1.229+） | 見 [外掛](07-plugins/README.md#command-來源v21229) |
| **市集擁有者萬用字元** | `"owner/*"` 可允許或封鎖某個 GitHub 擁有者底下的所有市集儲存庫——僅適用於 `strictKnownMarketplaces` 與 `blockedMarketplaces`（v2.1.223+） | 見 [外掛](07-plugins/README.md#市集設定) |
| **沙箱憑證遮罩** | 沙箱化的指令讀到的是哨兵值，代理伺服器會在對外傳送時替換成真正的機密（v2.1.221+，Linux/WSL） | 見 [進階功能](09-advanced-features/README.md#憑證遮罩v21221v21224) |
| **代理團隊** | 協調多個代理處理相關任務 | 設定會協作並共用上下文的隊友代理 |
| **任務清單** | 背景任務管理與監控 | 使用 `/tasks` 檢視並管理背景作業 |
| **Prompt Suggestions** | 依上下文提供指令建議 | 建議會依目前上下文自動顯示 |
| **Git Worktree** | 用於平行開發的獨立 git worktree | 使用 worktree 相關指令安全地進行平行分支作業 |
| **沙箱** | 為安全性提供的獨立執行環境 | 使用 `/sandbox` 切換；在受限環境中執行指令 |
| **MCP OAuth** | MCP 伺服器的 OAuth 驗證 | 在 MCP 伺服器設定中設定 OAuth 憑證以安全存取 |
| **MCP Tool Search** | 動態搜尋與探索 MCP 工具 | 使用工具搜尋，在已連線的伺服器中找到可用的 MCP 工具 |
| **排程任務** | 用 `/loop` 與 cron 工具設定週期性任務 | 使用 `/loop 5m /command` 或 CronCreate 工具 |
| **Chrome Integration** | 以無介面 Chromium 進行瀏覽器自動化 | 使用 `--chrome` 旗標或 `/chrome` 指令 |
| **鍵盤快捷鍵自訂** | 自訂鍵盤綁定，支援組合鍵 | 使用 `/keybindings`，或編輯 `~/.claude/keybindings.json` |
| **自動模式** | 全自動運作，並由背景安全分類器把關 | 按 `Shift+Tab` 切換至此模式，或使用 `--permission-mode auto` |
| **頻道** | 多頻道通訊（Telegram、Slack 等）（研究預覽版） | 設定頻道外掛；2026 年 3 月 |
| **語音輸入** | 以語音輸入提示詞 | 使用麥克風圖示或語音快捷鍵 |
| **Agent Hook Type** | 派生子代理而非執行 shell 指令的 Hook | 在 Hook 設定中設為 `"type": "agent"` |
| **Prompt Hook Type** | 將提示詞文字注入對話的 Hook | 在 Hook 設定中設為 `"type": "prompt"` |
| **MCP Elicitation** | MCP 伺服器可在工具執行期間請求使用者輸入 | 透過 `Elicitation` 與 `ElicitationResult` Hook 事件處理 |
| **Plugin LSP Support** | 透過外掛整合 Language Server Protocol | 在 `plugin.json` 中設定 LSP 伺服器以提供編輯器功能 |
| **Managed Drop-ins** | 由組織管理的直接套用設定（v2.1.83） | 由管理員透過受管政策設定；自動套用給所有使用者 |
| **`claude plugin init`** | 在 `.claude/skills` 中建立新外掛的骨架；此類外掛無需市集即可自動載入（v2.1.157） | 執行 `claude plugin init <name>` |
| **第三方供應商上的自動模式** | 於 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry，以及已登入的 Claude app 閘道工作階段中預設可用，支援的模型為 Claude Sonnet 5、Opus 4.7 或更新版本（包含 Opus 5），以及 Fable 5（v2.1.158–v2.1.206 需選擇啟用；v2.1.207 移除此限制——`CLAUDE_CODE_ENABLE_AUTO_MODE` 仍可接受但已無作用） | 按 `Shift+Tab` 切換至此模式，或使用 `--permission-mode auto` |
| **即時對話框指令** | Claude 工作時可開啟 `/permissions`（規則變更會套用到本回合剩餘部分），而 `/add-dir`、`/autocompact`、`/theme`、`/help`、`/config` 與 `/advisor` 的對話框會在**全螢幕 TUI** 中於回合進行中直接開啟，而不是排入佇列、等到 Claude 回應完成才處理（`/bug` 自 v2.1.232 起已是如此）（v2.1.234） | 在 Claude 工作時執行以上任一指令。見 [斜線指令](01-slash-commands/README.md) |
| **`CLAUDE_CODE_PROJECT_DIR_NAME`** | 控制各專案逐字稿目錄命名方式的環境變數（v2.1.234） | 在啟動 Claude Code 前於 shell／環境變數中設定。見 [CLI](10-cli/README.md) |
| **目標簽到門檻** | 當 `/goal` 進行中，若背景任務 30 分鐘以上沒有進展，Claude 會回報狀態更新，而不是默默繼續；可用 `CLAUDE_CODE_GOAL_CHECKIN_MINUTES` 調整，設為 `0` 則停用（v2.1.234） | 在有 `/goal` 進行中時設定 `CLAUDE_CODE_GOAL_CHECKIN_MINUTES=<n>`。見 [斜線指令](01-slash-commands/README.md) |
| **使用額度自動接續** | 若工作階段因 claude.ai 使用額度受阻，額度重置時 Claude Code 會自動接續（v2.1.234） | 預設啟用；可在 `/config` → "Continue automatically at usage limit" 關閉。見 [進階功能](09-advanced-features/) |
| **`spellcheck` setting** | 使用 `PATH` 上可用的 aspell、hunspell 或 ispell，為提示詞輸入中的拼字錯誤加底線；預設關閉（v2.1.235） | 安裝拼字檢查工具，然後在 `~/.claude/settings.json` 中設定 `"spellcheck": { "enabled": true }`。僅適用於個人設定、`--settings` 與受管設定——專案設定中會被忽略。見 [進階功能](09-advanced-features/) |
| **代理團隊預設模型** | `/config` 中的「Default teammate model」設定已移除；隊友現在預設會繼承隊長的模型，除非派生時明確指定（v2.1.234） | 見 [子代理——代理團隊](04-subagents/README.md#代理團隊實驗性) |
| **`/design`** | 設計畫布——以 artifact 為基礎、可視覺方式而非撰寫程式碼調整的多畫板視覺設計（UI 模型、畫面流程、到達頁面、海報）。研究預覽版；需要 v2.1.233+；Pro／Max／Team／Enterprise | 在 CLI 或 Desktop app 中執行 `/design`。見 [斜線指令](01-slash-commands/README.md) |
| **`notify_when_idle`** | 跨工作階段 `SendMessage` 的輸入參數，要求同一台機器上的另一個工作階段在下次閒置時發出一次通知——選擇性啟用、只觸發一次、不輪詢（v2.1.236）。相關：`ListAgents` 會回報工作階段自己的名稱並列出上線中的隊友，Windows 也新增了跨工作階段訊息功能（v2.1.239） | 在呼叫 `SendMessage` 時傳入 `notify_when_idle`。見 [進階功能](09-advanced-features/README.md#跨工作階段訊息) |
| **外掛資訊清單欄位** | `plugin.json` 支援 `workflows`、`channels`、`dependencies`（semver）、`outputStyles`、`keywords`、`metadata`、`lspServers`，以及 `experimental.themes`／`experimental.monitors`。CLI 新增了 `claude plugin new`、`remove`／`rm`、`prune`／`autoremove`，以及旗標 `--with`、`-f`／`--force`、`--available`、`--push`、`--dry-run` | 見 [外掛](07-plugins/README.md) |
| **Restricted Mode** | 移除會執行指令或程式碼的內建工具（Bash、PowerShell、REPL）及 WebFetch，除非 `--tools` 有指名它們；忽略個人、專案與本機設定（受管設定與 `--settings` 仍會套用）；將檔案工具限制在工作目錄內；拒絕 `bypassPermissions`；並拒絕建立雲端工作階段（v2.1.248+） | `claude --restricted`，或設定 `CLAUDE_CODE_RESTRICTED=1`。見 [CLI](10-cli/README.md) |
| **`/advisor` 文字指令形式** | `/advisor`、`/advisor <model>`、`/advisor off` 現在可作為文字指令，在桌面 app、遠端控制 與其他無介面（`-p` ／ Agent SDK）工作階段中使用，不再只是對話框（v2.1.260+） | 在無介面工作階段中輸入 `/advisor off`。見 [斜線指令](01-slash-commands/README.md) |

---

## 快速參考矩陣

### 功能選擇指南

| 需求 | 建議功能 | 原因 |
|------|---------------------|-----|
| 快速捷徑 | 斜線指令 | 手動、即時 |
| 持久上下文 | 記憶 | 自動載入 |
| 複雜自動化 | 技能 | 自動呼叫 |
| 專門任務 | 子代理 | 獨立上下文 |
| 外部資料 | MCP 伺服器 | 即時存取 |
| 事件自動化 | Hook | 事件觸發 |
| 完整解決方案 | 外掛 | 一應俱全的組合包 |

### 安裝優先順序

| 優先順序 | 功能 | 指令 |
|----------|---------|---------|
| 1. 必要 | 記憶 | `cp 02-memory/project-CLAUDE.md ./CLAUDE.md` |
| 2. 日常使用 | 斜線指令 | `cp 01-slash-commands/*.md .claude/commands/` |
| 3. 品質 | 子代理 | `cp 04-subagents/*.md .claude/agents/` |
| 4. 自動化 | Hooks | `cp 06-hooks/*.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.sh` |
| 5. 外部整合 | MCP | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` |
| 6. 進階 | 技能 | `cp -r 03-skills/* ~/.claude/skills/` |
| 7. 完整 | 外掛 | `/plugin install pr-review` |

---

## 一鍵完整安裝

安裝此儲存庫中的所有範例：

```bash
# 建立目錄
mkdir -p .claude/{commands,agents,skills} ~/.claude/{hooks,skills}

# 安裝所有功能
cp 01-slash-commands/*.md .claude/commands/ && \
cp 02-memory/project-CLAUDE.md ./CLAUDE.md && \
cp -r 03-skills/* ~/.claude/skills/ && \
cp 04-subagents/*.md .claude/agents/ && \
cp 06-hooks/*.sh ~/.claude/hooks/ && \
chmod +x ~/.claude/hooks/*.sh
```

---

## 延伸資源

- [官方 Claude Code 文件](https://code.claude.com/docs/en/overview)
- [MCP 協定規格](https://modelcontextprotocol.io)
- [學習路線圖](LEARNING-ROADMAP.md)
- [主要 README](README.md)

---

**最後更新**：2026 年 9 月 6 日
**Claude Code 版本**：2.1.263
**資料來源**：
- https://code.claude.com/docs/en/sub-agents
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/permission-modes
- https://code.claude.com/docs/en/changelog#2-1-172
- https://code.claude.com/docs/en/changelog#2-1-174
- https://github.com/anthropics/claude-code/releases/tag/v2.1.145
- https://github.com/anthropics/claude-code/releases/tag/v2.1.154
- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/cli-reference
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/plugin-marketplaces
- https://code.claude.com/docs/en/discover-plugins
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/slash-commands
**相容模型**：Claude Fable 5.1、Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
