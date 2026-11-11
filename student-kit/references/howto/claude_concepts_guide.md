<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Concepts 完整指南

這是一份全面的參考指南，覆蓋 Slash Commands、Subagents、Memory、MCP Protocol、Agent Skills、Plugins、Hooks、Checkpoints、Advanced Features 等 Claude Code 核心概念，並配有表格、圖示和實踐範例。

---

## 目錄

1. [Slash Commands](#slash-commands)
2. [Subagents](#subagents)
3. [Memory](#memory)
4. [MCP Protocol](#mcp-protocol)
5. [Agent Skills](#agent-skills)
6. [Plugins](#claude-code-plugins)
7. [Hooks](#hooks)
8. [Checkpoints and Rewind](#checkpoints-and-rewind)
9. [Advanced Features](#advanced-features)
10. [Comparison & Integration](#comparison--integration)

---

## Slash Commands

### 概覽

Slash commands 是由使用者手動觸發的快捷命令，以 Markdown 檔案形式儲存，Claude Code 可以讀取並執行。它們非常適合把高頻提示詞與工作流程標準化，方便團隊複用。

### 架構

```mermaid
graph TD
    A["使用者輸入: /command-name"] -->|觸發| B["搜尋 .claude/commands/"]
    B -->|找到| C["command-name.md"]
    C -->|載入| D["Markdown 內容"]
    D -->|執行| E["Claude 處理提示"]
    E -->|返回| F["上下文中的結果"]
```

### 檔案結構

```mermaid
graph LR
    A["專案根目錄"] -->|包含| B[".claude/commands/"]
    B -->|包含| C["optimize.md"]
    B -->|包含| D["test.md"]
    B -->|包含| E["docs/"]
    E -->|包含| F["generate-api-docs.md"]
    E -->|包含| G["generate-readme.md"]
```

### 命令組織表

| 位置 | 作用域 | 可用範圍 | 適用場景 | Git 跟蹤 |
|------|--------|----------|----------|-----------|
| `.claude/commands/` | 專案級 | 團隊成員 | 團隊工作流程、共享標準 | ✅ 是 |
| `~/.claude/commands/` | 個人級 | 當前使用者 | 跨專案的個人快捷命令 | ❌ 否 |
| 子目錄 | 名稱空間 | 取決於父目錄 | 按類別組織命令 | ✅ 是 |

### 功能與能力

| 功能 | 範例 | 是否支援 |
|------|------|----------|
| Shell 指令碼執行 | `bash scripts/deploy.sh` | ✅ 是 |
| 檔案引用 | `@path/to/file.js` | ✅ 是 |
| Bash 整合 | `$(git log --oneline)` | ✅ 是 |
| 引數 | `/pr --verbose` | ✅ 是 |
| MCP 命令 | `/mcp__github__list_prs` | ✅ 是 |

### 實踐範例

#### 範例 1：程式碼最佳化命令

**檔案：** `.claude/commands/optimize.md`

```markdown
---
name: 程式碼最佳化
description: 分析程式碼中的效能問題並給出最佳化建議
tags: performance, analysis
---

# 程式碼最佳化

請按以下優先順序順序審查給定程式碼中的問題：

1. **效能瓶頸** - 識別 O(n²) 操作、低效迴圈
2. **記憶體洩漏** - 查詢未釋放資源、迴圈引用
3. **演算法改進** - 建議更優演算法或資料結構
4. **快取機會** - 識別重複計算
5. **併發問題** - 查詢競態條件或執行緒問題

請按以下格式輸出：
- 問題嚴重級別（Critical/High/Medium/Low）
- 程式碼位置
- 解釋說明
- 帶程式碼範例的修復建議
```

**使用方式：**
```bash
# 使用者在 Claude Code 中輸入
/optimize

# Claude 載入提示並等待程式碼輸入
```

#### 範例 2：Pull Request 輔助命令

**檔案：** `.claude/commands/pr.md`

```markdown
---
name: 準備 Pull Request
description: 清理程式碼、暫存改動並準備一個 Pull Request
tags: git, workflow
---

# Pull Request 準備清單

在建立 PR 前，執行以下步驟：

1. 執行 lint：`prettier --write .`
2. 執行測試：`npm test`
3. 檢視 git diff：`git diff HEAD`
4. 暫存改動：`git add .`
5. 按 conventional commits 規則編寫提交資訊：
   - `fix:` 用於 bug 修復
   - `feat:` 用於新功能
   - `docs:` 用於文件更新
   - `refactor:` 用於程式碼重構
   - `test:` 用於補充測試
   - `chore:` 用於維護性工作

6. 生成 PR 摘要，包括：
   - 改了什麼
   - 為什麼改
   - 做了哪些測試
   - 可能的影響
```

**使用方式：**
```bash
/pr

# Claude 按清單逐項檢查並準備 PR
```

#### 範例 3：分層式文件生成器

**檔案：** `.claude/commands/docs/generate-api-docs.md`

```markdown
---
name: 生成 API 文件
description: 基於原始碼生成完整 API 文件
tags: documentation, api
---

# API 文件生成器

透過以下步驟生成 API 文件：

1. 掃描 `/src/api/` 下的所有檔案
2. 提取函式簽名和 JSDoc 註解
3. 按 endpoint / module 組織結構
4. 生成帶範例的 Markdown
5. 包含請求 / 響應 schema
6. 補充錯誤文件

輸出格式：
- 輸出 Markdown 檔案到 `/docs/api.md`
- 為所有端點包含 curl 範例
- 補充 TypeScript 型別
```

### 命令生命週期圖

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant FS as File System
    participant CLI as Shell/Bash

    User->>Claude: 輸入 /optimize
    Claude->>FS: 搜尋 .claude/commands/
    FS-->>Claude: 返回 optimize.md
    Claude->>Claude: 載入 Markdown 內容
    Claude->>User: 顯示提示上下文
    User->>Claude: 提供待分析程式碼
    Claude->>CLI: （可能執行指令碼）
    CLI-->>Claude: 返回結果
    Claude->>User: 輸出分析
```

### 最佳實踐

| ✅ 建議 | ❌ 不建議 |
|------|---------|
| 使用清晰、面向動作的命名 | 為一次性任務建立命令 |
| 在描述中寫清觸發場景 | 在命令裡堆複雜邏輯 |
| 保持命令聚焦單一任務 | 建立重複命令 |
| 將專案命令納入版本控制 | 硬編碼敏感資訊 |
| 使用子目錄組織分類 | 做過長的命令列表 |
| 使用簡單、可讀的提示詞 | 使用晦澀或過度縮寫的措辭 |

---

## Subagents

### 概覽

Subagents 是帶有隔離上下文視窗和自訂系統提示詞的專門化 AI 助手。它們讓 Claude 能夠把複雜任務拆分並委派出去，同時保持關注點清晰分離。

### 架構圖

```mermaid
graph TB
    User["👤 使用者"]
    Main["🎯 主 Agent<br/>(協調者)"]
    Reviewer["🔍 程式碼審查<br/>Subagent"]
    Tester["✅ 測試工程師<br/>Subagent"]
    Docs["📝 文件編寫<br/>Subagent"]

    User -->|提出請求| Main
    Main -->|委派| Reviewer
    Main -->|委派| Tester
    Main -->|委派| Docs
    Reviewer -->|返回結果| Main
    Tester -->|返回結果| Main
    Docs -->|返回結果| Main
    Main -->|彙總| User
```

### Subagent 生命週期

```mermaid
sequenceDiagram
    participant User
    participant MainAgent as 主 Agent
    participant CodeReviewer as 程式碼審查<br/>Subagent
    participant Context as 獨立的<br/>上下文視窗

    User->>MainAgent: “建置新的認證功能”
    MainAgent->>MainAgent: 分析任務
    MainAgent->>CodeReviewer: “審查這段程式碼”
    CodeReviewer->>Context: 初始化乾淨上下文
    Context->>CodeReviewer: 載入審查規則
    CodeReviewer->>CodeReviewer: 執行審查
    CodeReviewer-->>MainAgent: 返回發現
    MainAgent->>MainAgent: 融合結果
    MainAgent-->>User: 輸出綜合結論
```

### Subagent 設定表

| 設定項 | 型別 | 作用 | 範例 |
|--------|------|------|------|
| `name` | String | Agent 識別符號 | `code-reviewer` |
| `description` | String | 用途與觸發詞 | `Comprehensive code quality analysis` |
| `tools` | List/String | 允許的工具 | `Read, Grep, Glob, Bash` |
| *（Markdown 正文）* | Markdown | 系統提示詞 / 行為指令 | 自訂規範 |

### 工具訪問層級

```mermaid
graph TD
    A["Subagent 設定"] -->|選項 1| B["繼承主執行緒的全部工具"]
    A -->|選項 2| C["顯式指定工具"]
    B -->|包含| B1["檔案操作"]
    B -->|包含| B2["Shell 命令"]
    B -->|包含| B3["MCP 工具"]
    C -->|顯式列表| C1["read, grep, diff"]
    C -->|顯式列表| C2["Bash(npm:*), Bash(test:*)"]
```

### 實踐範例

#### 範例 1：完整 Subagent 設定

**檔案：** `.claude/agents/code-reviewer.md`

```yaml
---
name: code-reviewer
description: Comprehensive code quality and maintainability analysis
tools: Read, Grep, Glob, Bash
---

# Code Reviewer Agent

You are an expert code reviewer specializing in:
- Performance optimization
- Security vulnerabilities
- Code maintainability
- Testing coverage
- Design patterns

## Review Priorities (in order)

1. **Security Issues** - Authentication, authorization, data exposure
2. **Performance Problems** - O(n²) operations, memory leaks, inefficient queries
3. **Code Quality** - Readability, naming, documentation
4. **Test Coverage** - Missing tests, edge cases
5. **Design Patterns** - SOLID principles, architecture

## Review Output Format

針對每個問題：
- **Severity**: Critical / High / Medium / Low
- **Category**: Security / Performance / Quality / Testing / Design
- **Location**: File path and line number
- **Issue Description**: What's wrong and why
- **Suggested Fix**: Code example
- **Impact**: How this affects the system
```

**檔案：** `.claude/agents/test-engineer.md`

```yaml
---
name: test-engineer
description: Test strategy, coverage analysis, and automated testing
tools: read, write, bash, grep
---

# Test Engineer Agent

You are expert at:
- Writing comprehensive test suites
- Ensuring high code coverage (>80%)
- Testing edge cases and error scenarios
- Performance benchmarking
- Integration testing
```

**檔案：** `.claude/agents/documentation-writer.md`

```yaml
---
name: documentation-writer
description: Technical documentation, API docs, and user guides
tools: read, write, grep
---

# Documentation Writer Agent

You create:
- API documentation with examples
- User guides and tutorials
- Architecture documentation
- Changelog entries
- Code comment improvements
```

#### 範例 2：Subagent 委派流程

```markdown
# 場景：建置支付功能

## 使用者請求
"建置一個與 Stripe 整合的安全支付處理功能"

## 主 Agent 工作流程

1. **規劃階段**
   - 理解需求
   - 確定所需任務
   - 規劃架構

2. **委派給 Code Reviewer Subagent**
   - 任務："審查支付處理實現中的安全問題"
   - 上下文：認證、API 金鑰、token 處理
   - 重點：SQL 注入、金鑰洩露、HTTPS 強制

3. **委派給 Test Engineer Subagent**
   - 任務："為支付流程建立完整測試"
   - 上下文：成功場景、失敗場景、邊界情況
   - 輸出：有效支付、拒付、網路故障、webhook 測試

4. **委派給 Documentation Writer Subagent**
   - 任務："為支付 API 端點編寫文件"
   - 上下文：請求 / 響應 schema
   - 產出：帶 curl 範例和錯誤碼的 API 文件

5. **綜合**
   - 主 Agent 彙總所有輸出
   - 整合發現
   - 返回完整方案給使用者
```

#### 範例 3：工具許可權範圍

**受限設定：只允許特定能力**

```yaml
---
name: secure-reviewer
description: Security-focused code review with minimal permissions
tools: read, grep
---

# Secure Code Reviewer

Reviews code for security vulnerabilities only.
```

**擴充套件設定：為實現任務開放全部工具**

```yaml
---
name: implementation-agent
description: Full implementation capabilities for feature development
tools: read, write, bash, grep, edit, glob
---

# Implementation Agent

Builds features from specifications.
```

### Subagent 上下文管理

```mermaid
graph TB
    A["主 Agent 上下文<br/>50,000 tokens"]
    B["Subagent 1 上下文<br/>20,000 tokens"]
    C["Subagent 2 上下文<br/>20,000 tokens"]
    D["Subagent 3 上下文<br/>20,000 tokens"]

    A -->|乾淨上下文| B
    A -->|乾淨上下文| C
    A -->|乾淨上下文| D

    B -->|僅返回結果| A
    C -->|僅返回結果| A
    D -->|僅返回結果| A

    style A fill:#e1f5ff
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#fff9c4
```

### 何時使用 Subagents

| 場景 | 是否使用 Subagent | 原因 |
|------|------------------|------|
| 多步驟複雜功能 | ✅ 是 | 分離關注點，防止上下文汙染 |
| 快速程式碼審查 | ❌ 否 | 開銷不值得 |
| 並行任務執行 | ✅ 是 | 每個 subagent 都有自己的上下文 |
| 需要專業化角色 | ✅ 是 | 可以用自訂系統提示詞 |
| 長時間分析任務 | ✅ 是 | 防止主上下文耗盡 |
| 單一步驟任務 | ❌ 否 | 只會增加延遲 |

### Agent Teams

Agent Teams 用於協調多個 agent 圍繞一個共同目標協作。與一次只委派一個 subagent 不同，Agent Teams 允許主 agent 編排一組協作代理，在共享中間結果的同時並行推進大任務，例如由前端 agent、後端 agent、測試 agent 一起完成一個全棧功能。

---

## Memory

### 概覽

Memory 讓 Claude 能夠在不同會話和對話之間保留上下文。它主要有兩種形態：Claude Web/Desktop 中的自動記憶綜合，以及 Claude Code 中基於檔案系統的 `CLAUDE.md`。

### Memory 架構

```mermaid
graph TB
    A["Claude 會話"]
    B["使用者輸入"]
    C["記憶系統"]
    D["記憶儲存"]

    B -->|使用者提供資訊| C
    C -->|每 24 小時綜合| D
    D -->|自動載入| A
    A -->|使用上下文| C
```

### Claude Code 中的 7 層記憶層級

Claude Code 會載入 7 層記憶。CLAUDE.md 檔案不會互相覆蓋，而是拼接進上下文，並按 managed → user → project → local 的順序載入（越具體的檔案越晚讀取）：

```mermaid
graph TD
    A["1. Managed Policy<br/>企業管理員策略"] --> B["2. Project Memory<br/>./CLAUDE.md"]
    B --> C["3. Project Rules<br/>.claude/rules/*.md"]
    C --> D["4. User Memory<br/>~/.claude/CLAUDE.md"]
    D --> E["5. User Rules<br/>~/.claude/rules/*.md"]
    E --> F["6. Local Memory<br/>./CLAUDE.local.md"]
    F --> G["7. Auto Memory<br/>自動捕獲的偏好"]
```

### Memory 位置表

| 層級 | 位置 | 作用域 | 優先順序 | 是否共享 | 最適合 |
|------|------|--------|--------|----------|--------|
| 1. Managed Policy | 企業管理員 | 組織級 | 最高 | 全組織使用者 | 合規、安全策略 |
| 2. Project | `./CLAUDE.md` | 專案級 | 高 | 團隊（Git） | 團隊標準、架構 |
| 3. Project Rules | `.claude/rules/*.md` | 專案級 | 高 | 團隊（Git） | 模組化專案約定 |
| 4. User | `~/.claude/CLAUDE.md` | 個人級 | 中 | 個人 | 個人偏好 |
| 5. User Rules | `~/.claude/rules/*.md` | 個人級 | 中 | 個人 | 個人規則模組 |
| 6. Local | `./CLAUDE.local.md` | 本地 | 低 | 不共享 | 機器相關設定 |
| 7. Auto Memory | 自動生成 | 儲存庫級 | 最低 | 個人 | 學到的偏好與模式 |

### Auto Memory

Auto Memory 會在會話中自動捕獲使用者偏好與行為模式。Claude 會記住：

- 程式碼風格偏好
- 你常做的糾正
- 框架和工具選擇
- 溝通方式偏好

它在後臺工作，不需要手動設定。

### Memory 更新生命週期

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Editor as File System
    participant Memory as CLAUDE.md

    User->>Claude: “記住：統一使用 async/await”
    Claude->>User: “寫入哪個記憶檔案？”
    User->>Claude: “專案記憶”
    Claude->>Editor: 開啟 ~/.claude/settings.json
    Claude->>Memory: 寫入 ./CLAUDE.md
    Memory-->>Claude: 檔案已儲存
    Claude->>Claude: 重新載入記憶
    Claude-->>User: “記憶已儲存！”
```

### 實踐範例

#### 範例 1：專案級記憶結構

**檔案：** `./CLAUDE.md`

```markdown
# 專案設定

## 專案概覽
- **名稱**：電商平臺
- **技術棧**：Node.js、PostgreSQL、React 18、Docker
- **團隊規模**：5 名開發者
- **截止時間**：2025 年第 4 季度

## 架構
@docs/architecture.md
@docs/api-standards.md
@docs/database-schema.md

## 開發標準

### Code Style
- 使用 Prettier 格式化
- 使用 ESLint + airbnb config
- 最大行寬 100 字元
- 使用 2 空格縮排

### Naming Conventions
- **檔案**：kebab-case
- **類**：PascalCase
- **函式/變數**：camelCase
- **常量**：UPPER_SNAKE_CASE
- **資料庫表**：snake_case
```

#### 範例 2：目錄級記憶

**檔案：** `./src/api/CLAUDE.md`

~~~~markdown
# API 模組標準

該檔案會覆蓋根目錄 `CLAUDE.md` 中對 `/src/api/` 的規則。

## API 專屬標準

### Request Validation
- 使用 Zod 做 schema 校驗
- 所有輸入都必須校驗
- 校驗失敗時返回 400
- 包含欄位級錯誤詳情

### Authentication
- 所有端點都要求 JWT token
- Token 透過 Authorization header 傳遞
- Token 24 小時過期
- 實現 refresh token 機制
~~~~

#### 範例 3：個人記憶

**檔案：** `~/.claude/CLAUDE.md`

~~~~markdown
# 我的開發偏好

## About Me
- **經驗水平**：8 年全棧開發
- **偏好語言**：TypeScript、Python
- **溝通風格**：直接、配範例
- **學習風格**：喜歡圖示和程式碼配合

## Code Preferences

### Error Handling
我偏好顯式的 try-catch 和清晰的錯誤資訊。
避免泛化錯誤，除錯時始終記錄日誌。
~~~~

#### 範例 4：會話中更新記憶

```markdown
User: 記住：所有新元件都優先使用 React hooks，不用 class components。

Claude: 我會把它加入記憶。你希望寫入哪個記憶檔案？
        1. 專案記憶（./CLAUDE.md）
        2. 個人記憶（~/.claude/CLAUDE.md）

User: 專案記憶

Claude: ✅ 記憶已儲存！
```

### Claude Web/Desktop 中的記憶綜合

#### 記憶綜合時間線

```mermaid
graph LR
    A["第 1 天：使用者對話"] -->|24 小時| B["第 2 天：記憶綜合"]
    B -->|自動| C["記憶更新並摘要化"]
    C -->|載入到| D["第 2-N 天：新對話"]
```

### Memory 功能對比

| 功能 | Claude Web/Desktop | Claude Code (`CLAUDE.md`) |
|------|--------------------|---------------------------|
| 自動綜合 | ✅ 每 24 小時 | ❌ 手動 |
| 跨專案 | ✅ 共享 | ❌ 專案級 |
| 團隊訪問 | ✅ 共享專案 | ✅ Git 跟蹤 |
| 可搜尋 | ✅ 內建 | ✅ 透過 `/memory` |
| 可編輯 | ✅ 聊天中 | ✅ 直接改檔案 |
| 匯入/匯出 | ✅ 支援 | ✅ 複製貼上 |
| 永續性 | ✅ 24h+ | ✅ 長期 |

---

## MCP Protocol

### 概覽

MCP（Model Context Protocol）是 Claude 訪問外部工具、API 與實時資料來源的標準方式。與 Memory 不同，MCP 提供的是對持續變化資料的實時訪問。

### MCP 架構

```mermaid
graph TB
    A["Claude"]
    B["MCP Server"]
    C["外部服務"]

    A -->|請求| B
    B -->|查詢| C
    C -->|資料| B
    B -->|響應| A
```

### MCP 生態

```mermaid
graph TB
    A["Claude"] -->|MCP| B["Filesystem<br/>MCP Server"]
    A -->|MCP| C["GitHub<br/>MCP Server"]
    A -->|MCP| D["Database<br/>MCP Server"]
    A -->|MCP| E["Slack<br/>MCP Server"]
    A -->|MCP| F["Google Docs<br/>MCP Server"]
```

### MCP 設定流程

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Config as 設定檔案
    participant Service as 外部服務

    User->>Claude: 輸入 /mcp
    Claude->>Claude: 列出可用 MCP server
    Claude->>User: 展示選項
    User->>Claude: 選擇 GitHub MCP
    Claude->>Config: 更新設定
    Config->>Claude: 啟用連線
    Claude->>Service: 測試連線
    Service-->>Claude: 認證成功
    Claude->>User: ✅ MCP 已連線
```

### 可用 MCP Server 表

| MCP Server | 用途 | 常見工具 | 認證 | 實時 |
|------------|------|----------|------|------|
| Filesystem | 檔案操作 | read, write, delete | 作業系統許可權 | ✅ 是 |
| GitHub | 儲存庫管理 | list_prs, create_issue, push | OAuth | ✅ 是 |
| Slack | 團隊溝通 | send_message, list_channels | Token | ✅ 是 |
| Database | SQL 查詢 | query, insert, update | 憑據 | ✅ 是 |
| Google Docs | 文件訪問 | read, write, share | OAuth | ✅ 是 |
| Asana | 專案管理 | create_task, update_status | API Key | ✅ 是 |
| Stripe | 支付資料 | list_charges, create_invoice | API Key | ✅ 是 |
| Memory | 持久記憶 | store, retrieve, delete | Local | ❌ 否 |

### 實踐範例

#### 範例 1：GitHub MCP 設定

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

#### 範例 2：多 MCP 工作流程

```markdown
# 使用多個 MCP 的日報工作流程

## 設定
1. GitHub MCP - 獲取 PR 指標
2. Database MCP - 查詢銷售資料
3. Slack MCP - 傳送報告
4. Filesystem MCP - 儲存報告
```

#### 範例 3：Filesystem MCP 操作

| 操作 | 命令 | 作用 |
|------|------|------|
| 列出檔案 | `ls ~/projects` | 檢視目錄內容 |
| 讀取檔案 | `cat src/main.ts` | 讀取檔案內容 |
| 寫入檔案 | `create docs/api.md` | 建立新檔案 |
| 編輯檔案 | `edit src/app.ts` | 修改檔案 |
| 搜尋 | `grep "async function"` | 在檔案中搜尋 |
| 刪除 | `rm old-file.js` | 刪除檔案 |

### MCP vs Memory：決策矩陣

```mermaid
graph TD
    A["需要外部資料嗎？"]
    A -->|否| B["使用 Memory"]
    A -->|是| C["資料是否頻繁變化？"]
    C -->|否/很少| B
    C -->|是/經常| D["使用 MCP"]
```

### 請求 / 響應模式

```mermaid
sequenceDiagram
    participant App as Claude
    participant MCP as MCP Server
    participant DB as Database

    App->>MCP: Request: "SELECT * FROM users WHERE id=1"
    MCP->>DB: Execute query
    DB-->>MCP: Result set
    MCP-->>App: Return parsed data
```

---

## Agent Skills

### 概覽

Agent Skills 是可複用、由模型自動呼叫的能力包。它們以目錄形式存在，通常包含說明、指令碼和資原始檔。Claude 會在合適時自動發現並使用它們。

### Skill 架構

```mermaid
graph TB
    A["Skill 目錄"]
    B["SKILL.md"]
    C["YAML 後設資料"]
    D["說明"]
    E["指令碼"]
    F["模板"]

    A --> B
    B --> C
    B --> D
    E --> A
    F --> A
```

### Skill 載入流程

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude
    participant System as System
    participant Skill as Skill

    User->>Claude: "Create Excel report"
    Claude->>System: Scan available skills
    System->>System: Load skill metadata
    Claude->>Claude: Match user request to skills
    Claude->>Skill: Load xlsx skill SKILL.md
    Skill-->>Claude: Return instructions + tools
    Claude->>Claude: Execute skill
    Claude->>User: Generate Excel file
```

### Skill 型別與位置

| 型別 | 位置 | 作用域 | 是否共享 | 同步方式 | 最適合 |
|------|------|--------|----------|----------|--------|
| 內建 | Built-in | 全域性 | 全部使用者 | 自動 | 文件生成 |
| 個人 | `~/.claude/skills/` | 個人 | 否 | 手動 | 個人自動化 |
| 專案 | `.claude/skills/` | 團隊 | 是 | Git | 團隊標準 |
| 外掛 | 透過 plugin 安裝 | 視情況而定 | 視情況而定 | 自動 | 整合能力 |

### 預建置 Skills

Claude Code 內建了一些 bundled skills，可直接使用，包括：

| Skill | 命令 | 用途 |
|-------|------|------|
| Simplify | `/simplify` | 簡化複雜程式碼或解釋 |
| Batch | `/batch` | 批次對多個檔案或物件執行操作 |
| Debug | `/debug` | 為當前會話開啟除錯日誌，並透過讀取該日誌排查問題 |
| Loop | `/loop` | 按定時計劃重複執行任務 |
| Claude API | `/claude-api` | 按專案語言載入 Claude API 和 Managed Agents 參考資料；程式碼匯入 `anthropic` 或 `@anthropic-ai/sdk` 時自動啟用 |

### 實踐範例

#### 範例 1：自訂程式碼審查 Skill

**目錄結構：**

```text
~/.claude/skills/code-review/
├── SKILL.md
├── templates/
│   ├── review-checklist.md
│   └── finding-template.md
└── scripts/
    ├── analyze-metrics.py
    └── compare-complexity.py
```

**檔案：** `~/.claude/skills/code-review/SKILL.md`

```yaml
---
name: Code Review Specialist
description: Comprehensive code review with security, performance, and quality analysis
version: "1.0.0"
tags:
  - code-review
  - quality
  - security
when_to_use: 當使用者希望審查程式碼、分析程式碼品質或評估 pull request 時
effort: high
shell: bash
---

# 程式碼審查 Skill

這個 skill 提供全面的程式碼審查能力，重點關注：

1. **安全分析**
2. **效能審查**
3. **程式碼品質**
4. **可維護性**
```

相關 Python 指令碼和模板可直接沿用原始實現；指令碼邏輯本身無需翻譯即可使用。

#### 範例 2：Brand Voice Skill

這個 skill 用於統一品牌語氣、用詞風格和外部溝通表達。它通常包含品牌使命、價值觀、推薦用詞、避免用詞，以及郵件 / 社交媒體等模板。

#### 範例 3：Documentation Generator Skill

這個 skill 用於從原始碼生成 API 文件，常見產物包括：

- OpenAPI/Swagger 規範
- API 端點文件
- SDK 使用範例
- 整合指南
- 錯誤碼說明
- 認證說明

### Skill 發現與呼叫

```mermaid
graph TD
    A["使用者請求"] --> B["Claude 分析"]
    B -->|掃描| C["可用 Skills"]
    C -->|後設資料匹配| D["Skill 描述是否匹配？"]
    D -->|是| E["載入 SKILL.md"]
    D -->|否| F["嘗試下一個 Skill"]
    E --> H["提取指令"]
    H --> I["執行 Skill"]
    I --> J["返回結果"]
```

### Skill 與其他功能的區別

```mermaid
graph TB
    A["擴充套件 Claude"]
    B["Slash Commands"]
    C["Subagents"]
    D["Memory"]
    E["MCP"]
    F["Skills"]

    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
```

---

## Claude Code Plugins

### 概覽

Claude Code Plugins 是把多種能力打包在一起的一體化擴充套件機制，通常包含 slash commands、subagents、MCP servers、hooks 以及相關設定。它們可以透過一條命令完成安裝。

### 架構

```mermaid
graph TB
    A["Plugin"]
    B["Slash Commands"]
    C["Subagents"]
    D["MCP Servers"]
    E["Hooks"]
    F["Configuration"]

    A -->|打包| B
    A -->|打包| C
    A -->|打包| D
    A -->|打包| E
    A -->|打包| F
```

### Plugin 載入流程

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Plugin as Plugin Marketplace
    participant Install as Installation
    participant SlashCmds as Slash Commands
    participant Subagents
    participant MCPServers as MCP Servers
    participant Hooks

    User->>Claude: claude --plugin-dir ./07-plugins/pr-review
    Claude->>Plugin: 下載外掛清單
    Plugin-->>Claude: 返回外掛定義
    Claude->>Install: 解包元件
    Install->>SlashCmds: 設定
    Install->>Subagents: 設定
    Install->>MCPServers: 設定
    Install->>Hooks: 設定
```

### Plugin 型別與分發

| 型別 | 作用域 | 是否共享 | 權威來源 | 範例 |
|------|--------|----------|----------|------|
| Official | 全域性 | 全部使用者 | Anthropic | PR Review、Security Guidance |
| Community | 公開 | 全部使用者 | 社群 | DevOps、Data Science |
| Organization | 內部 | 團隊成員 | 公司 | 內部標準、工具 |
| Personal | 個人 | 單使用者 | 開發者 | 自訂工作流程 |

### Plugin 定義結構

清單是位於 `.claude-plugin/plugin.json` 的 JSON 檔案。只有 `name` 是必填項，無法識別的頂層鍵會被移除：

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What this plugin does"
}
```

### Plugin 結構

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
├── agents/
├── skills/
├── hooks/
├── .mcp.json
├── bin/
├── templates/
├── scripts/
├── docs/
└── tests/
```

### 實踐範例

#### 範例 1：PR Review Plugin

```json
{
  "name": "pr-review",
  "version": "1.0.0",
  "description": "Complete PR review workflow with security, testing, and docs"
}
```

#### 範例 2：DevOps Plugin

```text
devops-automation/
├── commands/
├── agents/
├── mcp/
├── hooks/
└── scripts/
```

#### 範例 3：Documentation Plugin

```text
documentation/
├── commands/
├── agents/
├── mcp/
└── templates/
```

### Plugin Marketplace

```mermaid
graph TB
    A["Plugin Marketplace"]
    B["Official"]
    C["Community"]
    D["Enterprise"]
```

### Plugin 安裝與生命週期

```mermaid
graph LR
    A["發現"] --> B["瀏覽 Marketplace"]
    B --> C["檢視外掛頁"]
    C --> D["檢視元件"]
    D --> E["/plugin install"]
    E --> F["設定"]
    F --> G["啟用"]
```

### Plugin 功能對比

| 功能 | Slash Command | Skill | Subagent | Plugin |
|------|---------------|-------|----------|--------|
| 安裝 | 手動複製 | 手動複製 | 手動設定 | 一條命令 |
| 搭建時間 | 5 分鐘 | 10 分鐘 | 15 分鐘 | 2 分鐘 |
| 打包能力 | 單檔案 | 單檔案 | 單檔案 | 多元件 |
| 團隊共享 | 複製檔案 | 複製檔案 | 複製檔案 | 透過安裝 ID |
| 更新方式 | 手動 | 手動 | 手動 | 市場可用 / 更易分發 |

### 何時建立 Plugin

- 當你需要一次分發多個命令、subagents、MCP servers 或 hooks 時
- 當這是團隊級工作流程，需要統一安裝和複製時
- 當你希望自動化設定過程並減少手工步驟時

### 釋出 Plugin

1. 建立完整的外掛結構
2. 編寫 `.claude-plugin/plugin.json`
3. 編寫 `README.md`
4. 本地測試
5. 提交到 marketplace
6. 稽核透過
7. 釋出

### Plugin vs 手動設定

**手動設定：**
- 一個個複製 slash commands
- 單獨建立 subagents
- 分別設定 MCP
- 手動設定 hooks

**使用 Plugin：**
```bash
claude --plugin-dir ./07-plugins/pr-review
# ✅ 一次安裝完成
# ✅ 即刻可用
# ✅ 團隊可復現
```

---

## Comparison & Integration

### 功能對比矩陣

| 功能 | 呼叫方式 | 永續性 | 作用域 | 適用場景 |
|------|----------|--------|--------|----------|
| Slash Commands | 手動 (`/cmd`) | 僅當前會話 | 單個命令 | 快捷操作 |
| Subagents | 自動委派 | 隔離上下文 | 專門任務 | 任務拆分 |
| Memory | 自動載入 | 跨會話 | 使用者 / 團隊上下文 | 長期記憶 |
| MCP Protocol | 自動查詢 | 實時外部資料 | 動態訪問 | 外部資料接入 |
| Skills | 自動觸發 | 檔案系統級 | 可複用專長 | 自動化工作流程 |
| Plugins | 一鍵安裝 | 全套組合 | 團隊 / 市場分發 | 完整方案打包 |

### 互動時間線

```mermaid
graph LR
    A["Session Start"] -->|Load| B["Memory (CLAUDE.md)"]
    B -->|Discover| C["Available Skills"]
    C -->|Register| D["Slash Commands"]
    D -->|Connect| E["MCP Servers"]
    E -->|Ready| F["User Interaction"]
```

### 整合範例：客戶支援自動化

#### 架構

```mermaid
graph TB
    User["客戶郵件"] -->|進入| Router["支援路由器"]
    Router -->|分析| Memory["Memory<br/>客戶歷史"]
    Router -->|查詢| MCP1["MCP: 客戶資料庫"]
    Router -->|檢查| MCP2["MCP: Slack"]
    Router -->|複雜問題| Sub1["Subagent: 技術支援"]
    Router -->|簡單問題| Sub2["Subagent: 計費支援"]
```

#### 請求流

```markdown
1. 使用者發來報錯郵件
2. 讀取記憶和歷史上下文
3. 透過多個 MCP 查詢系統狀態
4. 自動識別適合的 Skill
5. 委派給對應 Subagent
6. Subagent 處理問題
7. Skill 負責按統一語氣生成回覆
8. MCP 將結果同步到外部系統
9. 返回給客戶
```

### 完整功能編排

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Memory as Memory
    participant MCP as MCP Servers
    participant Skills as Skills
    participant SubAgent as Subagents

    User->>Claude: "Build auth system"
    Claude->>Memory: 載入專案標準
    Claude->>MCP: 查詢相似實現
    Claude->>Skills: 檢測匹配 Skill
    Claude->>SubAgent: 委派實現
```

### 何時使用哪種功能

```mermaid
graph TD
    A["新任務"] --> B{任務型別？}

    B -->|重複工作流程| C["Slash Command"]
    B -->|需要實時資料| D["MCP Protocol"]
    B -->|希望下次記住| E["Memory"]
    B -->|需要專業子任務| F["Subagent"]
    B -->|領域型自動化| G["Skill"]
```

### 選擇決策樹

```mermaid
graph TD
    Start["需要擴充套件 Claude 嗎？"]
    Start -->|快速重複任務| A{"手動還是自動？"}
    A -->|手動| B["Slash Command"]
    A -->|自動| C["Skill"]
    Start -->|需要外部資料| D{"是否實時？"}
    D -->|是| E["MCP Protocol"]
    D -->|否| F["Memory"]
    Start -->|複雜專案| G{"是否多角色協作？"}
    G -->|是| H["Subagents"]
```

---

## Summary Table

| 維度 | Slash Commands | Subagents | Memory | MCP | Skills | Plugins |
|------|----------------|-----------|--------|-----|--------|---------|
| 搭建難度 | 簡單 | 中等 | 簡單 | 中等 | 中等 | 簡單 |
| 學習曲線 | 低 | 中 | 低 | 中 | 中 | 低 |
| 團隊價值 | 高 | 高 | 中 | 高 | 高 | 很高 |
| 自動化程度 | 低 | 高 | 中 | 高 | 高 | 很高 |
| 上下文管理 | 單會話 | 隔離 | 持久 | 實時 | 持久 | 全部整合 |
| 可擴充套件性 | 好 | 極佳 | 好 | 極佳 | 極佳 | 極佳 |
| 共享性 | 一般 | 一般 | 好 | 好 | 好 | 極佳 |
| 安裝方式 | 手動複製 | 手動設定 | N/A | 手動設定 | 手動複製 | 一條命令 |

---

## Quick Start Guide

### 第 1 周：先從簡單的開始
- 為常見任務做 2-3 個 slash commands
- 在設定裡開啟 Memory
- 在 `CLAUDE.md` 裡寫明團隊標準

### 第 2 周：接入實時資料
- 先設定 1 個 MCP（GitHub 或 Database）
- 透過 `/mcp` 設定
- 在工作流程中查詢實時資料

### 第 3 周：分發工作
- 建立第一個針對角色的 Subagent
- 讓 Claude 建立，或新增 `.claude/agents/<name>.md` 檔案（`/agents` 嚮導已移除）
- 用簡單任務測試委派

### 第 4 周：全面自動化
- 建立第一個 Skill
- 使用市場裡的 Skill 或自建
- 組合多個功能做完整工作流程

### 持續最佳化
- 每月回顧並更新 Memory
- 當重複模式出現時新增 Skill
- 最佳化 MCP 查詢
- 持續打磨 Subagent 提示詞

---

## Hooks

### 概覽

Hooks 是事件驅動的 shell 命令，會在 Claude Code 的特定事件發生時自動執行，可用於自動化、校驗、通知和自訂工作流程。

### Hook 事件

Claude Code 支援 **33 個 hook 事件**，分佈在四類鉤子中：

| Hook 事件 | 觸發時機 | 常見用途 |
|-----------|----------|----------|
| SessionStart | 會話開始 / 恢復 / 清空 / compact | 環境初始化 |
| InstructionsLoaded | 載入 `CLAUDE.md` 或 rules | 校驗、增強 |
| UserPromptSubmit | 使用者提交提示詞 | 輸入校驗 |
| PreToolUse | 工具執行前 | 審批、校驗、日誌 |
| PermissionRequest | 彈出許可權請求時 | 自動批准 / 拒絕 |
| PostToolUse | 工具執行成功後 | 自動格式化、通知、清理 |
| PostToolUseFailure | 工具失敗後 | 錯誤處理 |
| Notification | 通知傳送時 | 外部聯動 |
| SubagentStart | 啟動 subagent 時 | 注入上下文 |
| SubagentStop | subagent 結束時 | 結果校驗 |
| Stop | Claude 響應完成時 | 總結、清理 |
| SessionEnd | 會話結束時 | 收尾處理 |

### 常見 Hook 設定

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

### Hook 環境變數

- Hook 輸入以 JSON 形式透過 stdin 傳入（`session_id`、`tool_name`、`tool_input.file_path` 等），可用 `jq` 讀取
- `$CLAUDE_CODE_SESSION_ID`：當前會話 ID
- `$CLAUDE_PROJECT_DIR`：專案目錄路徑

### 最佳實踐

✅ 建議：
- 讓 hooks 儘量快（最好 < 1 秒）
- 用 hooks 做校驗和自動化
- 優雅處理錯誤
- 使用絕對路徑

❌ 不建議：
- 讓 hooks 進入互動式流程
- 把長時間任務放在 hooks 裡
- 硬編碼憑據

**詳見：** [06-hooks/README.md](06-hooks/README.md)

---

## Checkpoints and Rewind

### 概覽

Checkpoints 可以儲存會話狀態，並在需要時回退到之前的節點，從而安全地嘗試不同方案。

### 核心概念

| 概念 | 說明 |
|------|------|
| Checkpoint | 對訊息、檔案和上下文的快照 |
| Rewind | 回到某個歷史 checkpoint，並丟棄之後的變化 |
| Branch Point | 從同一個 checkpoint 分叉出多種方案 |

### 如何訪問 Checkpoints

```bash
# 按兩次 Esc 開啟 checkpoint 瀏覽器
Esc + Esc

# 或使用 /rewind
/rewind
```

選擇 checkpoint 後有六個選項：
1. 恢復程式碼和對話
2. 恢復對話
3. 恢復程式碼
4. 從這裡開始總結
5. 總結到這裡為止
6. 取消

### 常見場景

| 場景 | 工作流程 |
|------|--------|
| 探索不同方案 | 儲存 → 嘗試 A → 儲存 → 回退 → 嘗試 B |
| 安全重構 | 儲存 → 重構 → 測試 → 失敗就回退 |
| A/B 測試 | 儲存 → 設計 A → 儲存 → 回退 → 設計 B |
| 誤操作恢復 | 發現問題 → 回退到最近穩定狀態 |

### 設定

Checkpoint 預設開啟，由 `fileCheckpointingEnabled` 控制：

```json
{
  "fileCheckpointingEnabled": true
}
```

**詳見：** [08-checkpoints/README.md](08-checkpoints/README.md)

---

## Advanced Features

### Planning Mode

在編碼前先生成詳細實現計劃。

```bash
/plan Implement user authentication system
```

優勢：
- 清晰路線圖
- 時間預估
- 風險評估
- 可審查、可修改

### Extended Thinking

適合複雜問題的深度推理。

Opus 4.7+、Sonnet 5+、Haiku 5.5 和 Fable 始終使用自適應推理，固定的 `MAX_THINKING_TOKENS` 預算對它們不適用；用 `/effort` 控制推理深度。

```bash
# 用 effort 級別控制推理深度
/effort high
```

### Background Tasks

後臺執行長任務而不阻塞當前對話。

```bash
/tasks               # 檢視和管理後臺工作（別名：/bashes）
```

### Permission Modes

| 模式 | 說明 | 適用場景 |
|------|------|----------|
| `default` | 標準許可權模式 | 通用開發 |
| `acceptEdits` | 自動接受檔案編輯 | 信任編輯工作流程 |
| `plan` | 只分析不改檔案 | 審查、規劃 |
| `auto` | 自動批准安全操作 | 平衡自治與安全 |
| `dontAsk` | 只執行預先批准的工具，其餘一律自動拒絕 | 資深使用者 / 自動化 |
| `bypassPermissions` | 完全不受限 | CI/CD、可信指令碼 |

### Headless Mode（Print Mode）

使用 `-p` 標誌在無互動模式下執行 Claude Code，適合自動化和 CI/CD。

```bash
claude -p "Run all tests" --permission-mode auto
cat error.log | claude -p "explain this error"
claude -p --output-format json "list all functions in src/"
```

### Scheduled Tasks

透過 `/loop` 按計劃週期性執行任務：

```bash
/loop every 30m "Run tests and report failures"
/loop every 2h "Check for dependency updates"
/loop every 1d "Generate daily summary of code changes"
```

### Chrome Integration

Claude Code 可以與 Chrome 瀏覽器整合，用於網頁自動化，如導航頁面、填寫表單、截圖和提取頁面資料。

### Session Management

```bash
/resume
/rename "Feature"
/fork
claude -c
claude -r "Feature"
```

### Interactive Features

- `Ctrl + R`：搜尋命令歷史
- `Tab`：自動補全
- `↑ / ↓`：瀏覽歷史
- `Ctrl + L`：清屏

### 設定

```json
{
  "permissions": {
    "defaultMode": "manual"
  }
}
```

`settings.json` 中沒有後臺任務設定塊 —— 該功能由環境變數 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 控制，併發數由 `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`（預設 `20`）決定。

**詳見：** [09-advanced-features/README.md](09-advanced-features/README.md)

---

## Resources

- [Claude Code Documentation](https://code.claude.com/docs/en/overview)
- [Anthropic Documentation](https://docs.anthropic.com)
- [MCP GitHub Servers](https://github.com/modelcontextprotocol/servers)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

---

*適用於 Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5*
*現已覆蓋：Hooks、Checkpoints、Planning Mode、Extended Thinking、Background Tasks、Permission Modes、Headless Mode、Session Management、Auto Memory、Agent Teams、Scheduled Tasks、Chrome Integration、Bundled Skills 等概念。*

**最後更新**：2026 年 10 月 26 日
**Claude Code 版本**：2.1.310
**來源**：
- https://code.claude.com/docs/en/plugins/manifest-reference
- https://code.claude.com/docs/en/plugins/install
- https://code.claude.com/docs/en/settings-reference
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/checkpointing
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/headless#auto-approve-tools
- https://code.claude.com/docs/en/permission-modes#which-mode-a-non-interactive-run-starts-in
