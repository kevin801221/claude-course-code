# 🚀 Claude Code 使用全攻略 (Full Guide to Using Claude Code)

這裡包含了您使用 Claude Code 構建任何內容所需了解的一切！本指南將帶領您從安裝到進階的上下文工程、子代理人 (Subagents)、掛鉤 (Hooks) 和平行代理人工作流。

## 📋 準備工作 (Prerequisites)

- 終端機/命令列訪問權限
- 已安裝 Node.js (用於安裝 Claude Code)
- GitHub 帳號 (用於 GitHub CLI 整合)
- 文字編輯器 (推薦使用 VS Code)

## 🔧 安裝 (Installation)

**macOS/Linux:**
```bash
npm install -g @anthropic-ai/claude-code
```

**Windows (推薦使用 WSL):**
請參閱 [install_claude_code_windows.md](./install_claude_code_windows.md) 中的詳細說明。

**驗證安裝：**
```bash
claude --version
```

---

## ✅ 技巧 1：建立並優化 CLAUDE.md 檔案

設定 Claude 會自動提取到每次對話中的上下文檔案，其中包含專案特定的資訊、命令和指引。

```bash
mkdir your-folder-name && cd your-folder-name
claude
```

使用內建命令：
```
/init
```

或根據此儲存庫中的範本建立您自己的 `CLAUDE.md` 檔案。請參閱 `CLAUDE.md` 以獲取 Python 特定的範例結構，其中包括：
- 專案感知和上下文規則
- 程式碼結構指引
- 測試需求
- 任務完成工作流
- 風格慣例
- 文件標準

### 進階提示技巧 (Advanced Prompting Techniques)

**強力關鍵字 (Power Keywords)**：Claude 會對某些關鍵字做出增強行為的回應 (資訊密集型關鍵字)：
- **IMPORTANT (重要)**：強調不應被忽視的關鍵指示。
- **Proactively (主動地)**：鼓勵 Claude 採取主動並提出改進建議。
- **Ultra-think (深度思考)**：可以觸發更徹底的分析 (請謹慎使用)。

**必備提示工程技巧**：
- 避免要求「生產級 (production-ready)」程式碼 —— 這往往會導致過度工程。
- 提示 Claude 編寫腳本來檢查其工作：「實作後，建立一個驗證腳本」。
- 除非特別需要，否則避免回溯相容性 —— Claude 傾向於不必要地保留舊程式碼。
- 專注於清晰度和具體需求，而不是模糊的品質描述詞。

### 檔案放置策略 (File Placement Strategies)

Claude 會自動從多個位置讀取 `CLAUDE.md` 檔案：

```bash
# 儲存庫根目錄 (最常用)
./CLAUDE.md              # 提交到 git，與團隊共享
./CLAUDE.local.md        # 僅限本地，新增到 .gitignore

# 父目錄 (用於 Monorepos)
root/CLAUDE.md           # 通用專案資訊
root/frontend/CLAUDE.md  # 前端特定上下文
root/backend/CLAUDE.md   # 後端特定上下文

# 引用外部檔案以獲得靈活性
echo "遵循以下最佳實踐： ~/company/engineering-standards.md" > CLAUDE.md
```

**專家提示**：許多團隊保持 `CLAUDE.md` 簡約，並引用共用的標準文件。這使得以下操作變得容易：
- 在不同的 AI 編碼助手之間切換
- 無需更改每個專案即可更新標準
- 在團隊之間共享最佳實踐

*注意：雖然 Claude Code 會自動讀取 CLAUDE.md，但其他 AI 編碼助手也可以使用類似的上下文檔案 (例如 Cursor 的 .cursorrules)*

---

## ✅ 技巧 2：設定權限管理

設定工具允許列表 (Allowlist)，在保持檔案操作和系統命令安全的同時簡化開發。

**方法 1：互動式允許列表**
當 Claude 請求權限時，對常見操作選擇「始終允許 (Always allow)」。

**方法 2：使用 /permissions 命令**
```
/permissions
```
然後新增：
- `Edit` (用於檔案編輯)
- `Bash(git commit:*)` (用於 git 提交)
- `Bash(npm:*)` (用於 npm 命令)
- `Read` (用於讀取檔案)
- `Write` (用於建立檔案)

**方法 3：建立專案設定檔案**
建立 `.claude/settings.local.json`：
```json
{
  "allowedTools": [
    "Edit",
    "Read",
    "Write",
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(npm:*)",
    "Bash(python:*)",
    "Bash(pytest:*)"
  ]
}
```

**安全性最佳實踐**：
- 絕不允許 `Bash(rm -rf:*)` 或類似的破壞性命令。
- 使用特定的命令模式，而不是 `Bash(*)`。
- 定期審查權限。
- 為不同專案使用不同的權限集。

*注意：所有 AI 編碼助手都有權限管理 —— 有些是內建的，有些則需要手動核准每個操作。*

---

## ✅ 技巧 3：掌握自訂斜線命令 (Slash Commands)

斜線命令是將您自己的工作流新增到 Claude Code 中的關鍵。它們位於 `.claude/commands/` 中，使您能夠建立可重用且參數化的工作流。

### 內建命令
- `/init` - 生成初始 CLAUDE.md
- `/permissions` - 管理工具權限
- `/clear` - 清除任務之間的上下文
- `/agents` - 管理子代理人
- `/help` - 獲取 Claude Code 協助

### 自訂命令範例

**儲存庫分析：**
```
/primer
```
對儲存庫進行全面分析，讓 Claude Code 熟悉您的程式碼庫，以便您可以開始實作修復或新功能，且它擁有執行此操作所需的所有必要上下文。

### 建立您自己的命令

1. 在 `.claude/commands/` 中建立一個 Markdown 檔案：
```markdown
# 命令：analyze-performance

分析 $ARGUMENTS 中指定的檔案的效能。

## 步驟：
1. 讀取路徑處的檔案： $ARGUMENTS
2. 識別效能瓶頸
3. 建議優化方案
4. 建立基準測試 (Benchmark) 腳本
```

2. 使用命令：
```
/analyze-performance src/heavy-computation.js
```

命令可以使用 `$ARGUMENTS` 來接收參數，並可以呼叫 Claude 的任何工具。

*注意：其他 AI 編碼助手可以將這些命令作為常規提示使用 —— 只需複製命令內容並連同您的參數一起貼上即可。*

---

## ✅ 技巧 4：整合 MCP 伺服器

將 Claude Code 連接到模型上下文協定 (Model Context Protocol, MCP) 伺服器以增強功能。在 [MCP 說明文件](https://docs.anthropic.com/en/docs/claude-code/mcp) 中了解更多資訊。

**新增 Serena MCP 伺服器** —— 最強大的編碼工具包：

請確保先 [安裝 uvx](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)。在 Windows 的 WSL 中可以這樣做：
```bash
sudo snap install astral-uv --classic
```

然後使用以下命令新增 Serena：
```bash
# 安裝 Serena 以進行語義程式碼檢索和編輯
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project $(pwd)
```

[Serena](https://github.com/oraios/serena) 將 Claude Code 轉變為功能齊全的編碼代理人，具有：
- 語義程式碼檢索與分析
- 使用語言伺服器協定 (LSP) 的進階編輯能力
- 支援 Python, TypeScript/JavaScript, PHP, Go, Rust, C/C++, Java
- 訂閱制編碼助手的免費且開源替代方案

**管理 MCP 伺服器：**
```bash
# 列出所有配置的伺服器
claude mcp list

# 獲取特定伺服器的詳細資訊
claude mcp get serena

# 移除伺服器
claude mcp remove serena
```

**即將推出**：Archon V2 (重大改版) —— AI 編碼助手的全面知識和任務管理骨幹 —— 首次實現真正的程式碼人機協作。

*注意：MCP 已與每個主要的 AI 編碼助手整合，且伺服器的管理方式非常相似。*

---

## ✅ 技巧 5：使用範例進行上下文工程

將您的開發工作流從簡單的提示轉變為全面的上下文工程 —— 為 AI 提供端到端實作所需的所有資訊。

### 快速開始

PRP (產品需求提示，Product Requirements Prompt) 框架是上下文工程的一個簡單 3 步驟策略：

```bash
# 1. 使用範例和上下文定義您的需求
# 編輯 INITIAL.md 以包含範例程式碼和模式

# 2. 生成完整的 PRP
/generate-prp INITIAL.md

# 3. 執行 PRP 以實作您的功能
/execute-prp PRPs/your-feature-name.md
```

### 定義您的需求

您的 `INITIAL.md` 應始終包含：

```markdown
## FEATURE (功能)
構建使用者身分驗證系統

## EXAMPLES (範例)
- 身分驗證流程： `examples/auth-flow.js`
- 類似的 API 端點： `src/api/users.js` 
- 資料庫綱要模式： `src/models/base-model.js`
- 驗證方法： `src/validators/user-validator.js`

## DOCUMENTATION (文件)
- JWT 函式庫文件： https://github.com/auth0/node-jsonwebtoken
- 我們的 API 標準： `docs/api-guidelines.md`

## OTHER CONSIDERATIONS (其他考量)
- 使用現有的錯誤處理模式
- 遵循我們的標準回應格式
- 包含速率限制
```

### 關鍵 PRP 策略

**範例 (Examples)**：最強大的工具 —— 提供程式碼片段、類似功能和要遵循的模式。

**驗證關卡 (Validation Gates)**：確保全面的測試和迭代，直到所有測試通過。

**拒絕憑感覺編碼 (No Vibe Coding)**：在執行前驗證 PRP，並在執行後驗證程式碼！

您提供的具體範例越多，Claude 就能越好地匹配您現有的模式和風格。

*注意：上下文工程適用於任何 AI 編碼助手 —— PRP 框架和範例驅動的方法是通用原則。*

---

## ✅ 技巧 6：利用子代理人 (Subagents) 處理專門任務

子代理人是專門的 AI 助手，在獨立的上下文視窗中運行，具有集中的專業知識。它們使 Claude 能夠將特定任務委派給專家，從而提高品質和效率。

### 瞭解子代理人

每個子代理人：
- 擁有自己的上下文視窗 (不會受到主對話的污染)
- 使用專門的系統提示詞運行
- 可以限制使用特定工具
- 在委派的任務上自主工作

### 本儲存庫中的子代理人範例

**文件管理員 (Documentation Manager)** (`.claude/agents/documentation-manager.md`)：
- 程式碼更改時自動更新文件
- 確保 README 的準確性
- 維護 API 文件
- 建立遷移指南

**驗證關卡 (Validation Gates)** (`.claude/agents/validation-gates.md`)：
- 更改後執行所有測試
- 迭代修復直到測試通過
- 強制執行程式碼品質標準
- 絕不在測試失敗時將任務標記為完成

### 建立您自己的子代理人

1. 使用 `/agents` 命令或在 `.claude/agents/` 中建立一個檔案：

```markdown
---
name: security-auditor
description: "安全性稽核專家。主動審查程式碼中的漏洞並建議改進措施。"
tools: Read, Grep, Glob
---

您是一位安全性稽核專家，專注於識別和預防安全性漏洞...

## 核心職責
1. 針對 OWASP Top 10 漏洞審查程式碼
2. 檢查洩漏的機密或憑證
3. 驗證輸入清理 (Sanitization)
4. 確保正確的身分驗證/授權
...
```

### 子代理人最佳實踐

**1. 專業分工**：每個子代理人應有一個清晰的專長。

**2. 主動描述**：在描述中使用「主動 (proactively)」以便自動調用：
```yaml
description: "程式碼審查員。主動審查所有程式碼更改的品質。"
```

**3. 工具限制**：僅給予子代理人所需的工具：
```yaml
tools: Read, Grep  # 對於僅限審查的代理人，不提供寫入權限
```

**4. 資訊流設計**：瞭解資訊如何從「主代理人 → 子代理人 → 主代理人」流動。子代理人的描述至關重要，因為它告訴您的主 Claude Code 代理人何時以及如何使用它。在描述中包含有關主代理人應如何提示此子代理人的清晰指示。

**5. 一次性上下文 (One-Shot Context)**：子代理人沒有完整的對話歷史 —— 它們接收來自您的主代理人的單個提示。在設計您的子代理人時，請記住這一限制。

在 [子代理人說明文件](https://docs.anthropic.com/en/docs/claude-code/sub-agents) 中了解更多資訊。

*注意：雖然其他 AI 助手沒有正式的子代理人，但您可以透過建立專門的提示並在不同的對話上下文之間切換來實現類似的結果。*

---

## ✅ 技巧 7：使用掛鉤 (Hooks) 實現自動化

掛鉤透過使用者定義的 shell 命令提供對 Claude Code 行為的確定性控制，這些命令在預定義的生命週期事件中執行。

### 可用的掛鉤事件

Claude Code 提供了多個您可以掛鉤的預定義操作：
- **PreToolUse**：在工具執行之前 (可以阻止操作)。
- **PostToolUse**：在工具成功完成之後。
- **UserPromptSubmit**：當使用者提交提示時。
- **SubagentStop**：當子代理人完成任務時。
- **Stop**：當主代理人完成回應時。
- **SessionStart**：在對話初始化時。
- **PreCompact**：在上下文壓縮之前。
- **Notification**：在系統通知期間。

在 [掛鉤說明文件](https://docs.anthropic.com/en/docs/claude-code/hooks) 中了解更多資訊。

### 掛鉤範例：工具使用日誌記錄

本儲存庫在 `.claude/hooks/` 中包含一個簡單的掛鉤範例：

**log-tool-usage.sh** —— 記錄所有工具使用情況以進行追蹤和除錯：
```bash
#!/bin/bash
# 記錄帶有時間戳記的工具使用情況
# 建立 .claude/logs/tool-usage.log
# 無需外部依賴
```

### 設定掛鉤

1. 在 `.claude/hooks/` 中**建立掛鉤腳本**。
2. **使其可執行**：`chmod +x your-hook.sh`
3. **新增至設定**，位於 `.claude/settings.local.json`：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/log-tool-usage.sh"
          }
        ]
      }
    ]
  }
}
```

掛鉤確保某些操作始終發生，而不是依賴 AI 去記住 —— 非常適合日誌記錄、安全性驗證和構建觸發。

*注意：其他 AI 助手沒有掛鉤 (雖然 Kiro 有！)，我幾乎可以保證它們很快就會出現在其他人身上。*

---

## ✅ 技巧 8：GITHUB CLI 整合

設定 GitHub CLI，使 Claude 能夠與 GitHub 進行互動，處理問題 (Issues)、拉取請求 (Pull Requests) 和儲存庫管理。

```bash
# 安裝 GitHub CLI
# 造訪： https://github.com/cli/cli#installation

# 驗證
gh auth login

# 驗證設定
gh repo list
```

### 自訂 GitHub 命令

使用 `/fix-github-issue` 命令進行自動修復：

```
/fix-github-issue 123
```

這將會：
1. 獲取問題詳情
2. 分析問題
3. 搜尋相關程式碼
4. 實作修復
5. 執行測試
6. 建立 PR

*注意：GitHub CLI 適用於任何 AI 編碼助手 —— 只需安裝它，AI 就可以使用 `gh` 命令與您的儲存庫進行互動。*

---

## ✅ 技巧 9：使用開發容器 (Dev Containers) 的安全 YOLO 模式

允許 Claude Code 執行任何操作，同時透過容器化保持安全性。這使得能夠進行快速開發，而不會對您的主機造成破壞性行為。

**前提條件：**
- 安裝 [Docker](https://www.docker.com/) 
- VS Code (或相容的編輯器)

**安全性功能：**
- 帶有允許列表的網路隔離
- 無法訪問主機檔案系統
- 限制外網連線
- 安全的實驗環境

**設定流程：**

1. **在 VS Code 中開啟**並按下 `F1`。
2. **選擇**「Dev Containers: Reopen in Container」。
3. **等待**容器構建。
4. **開啟終端機** (`Ctrl+J`)。
5. 在容器中**對 Claude Code 進行驗證**。
6. **以 YOLO 模式執行**：
   ```bash
   claude --dangerously-skip-permissions
   ```

**為什麼要使用開發容器？**
- 安全地測試危險操作
- 實驗系統更改
- 快速原型開發
- 一致的開發環境
- 無需擔心破壞您的系統

---

## ✅ 技巧 10：使用 GIT 工作樹 (Worktrees) 進行平行開發

使用 Git 工作樹使多個 Claude 實例能夠同時處理獨立任務，或自動執行同一功能的平行實作。

### 手動工作樹設定

```bash
# 為不同的功能建立工作樹
git worktree add ../project-auth feature/auth
git worktree add ../project-api feature/api

# 在每個工作樹中啟動 Claude
cd ../project-auth && claude  # 終端機 1
cd ../project-api && claude   # 終端機 2
```

### 自動化平行代理人

AI 編碼助手是非確定性的。執行多次嘗試可以提高成功機率並提供實作選項。

**設定平行工作樹：**
```bash
/prep-parallel user-system 3
```

**執行平行實作：**
1. 建立一個計畫檔案 (`plan.md`)
2. 執行平行執行：

```bash
/execute-parallel user-system plan.md 3
```

**選擇最佳實作：**
```bash
# 審查結果
cat trees/user-system-*/RESULTS.md

# 測試每個實作
cd trees/user-system-1 && npm test

# 合併最佳的實作
git checkout main
git merge user-system-2
```

### 優點

- **無衝突**：每個實例都在隔離狀態下工作。
- **多種方法**：比較不同的實作。
- **品質關卡**：僅考慮測試通過的實作。
- **易於整合**：合併最佳解決方案。

---

## 🎯 快速命令參考 (Quick Command Reference)

| 命令 | 用途 |
|---------|---------|
| `/init` | 生成初始 CLAUDE.md |
| `/permissions` | 管理工具權限 |
| `/clear` | 清除任務之間的上下文 |
| `/agents` | 建立與管理子代理人 |
| `/primer` | 分析儲存庫結構 |
| `ESC` | 中斷 Claude |
| `Shift+Tab` | 進入計畫模式 |
| `/generate-prp INITIAL.md` | 建立實作藍圖 |
| `/execute-prp PRPs/feature.md` | 根據藍圖實作 |
| `/prep-parallel [feature] [count]` | 設定平行工作樹 |
| `/execute-parallel [feature] [plan] [count]` | 執行平行實作 |
| `/fix-github-issue [number]` | 自動修復 GitHub 問題 |

---

## 📚 額外資源

- [Claude Code 說明文件](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code 最佳實踐](https://www.anthropic.com/engineering/claude-code-best-practices)
- [MCP 伺服器庫](https://github.com/modelcontextprotocol)

---

## 🚀 下一步

1. **從簡單開始**：設定 `CLAUDE.md` 和基本權限。
2. **新增斜線命令**：為您的工作流建立自訂命令。
3. **安裝 MCP 伺服器**：新增 Serena 以增強編碼能力。
4. **實作子代理人**：為您的技術棧新增專家。
5. **配置掛鉤**：自動化重複性任務。
6. **嘗試平行開發**：實驗多種方法。

記住：當您提供清晰的上下文、具體的範例和全面的驗證時，Claude Code 的功能最強大。祝您編碼愉快！ 🎉
