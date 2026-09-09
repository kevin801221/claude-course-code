<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-code-tutorial-logo-dark.svg">
  <img alt="Claude Code 完整教學" src="../resources/logos/claude-code-tutorial-logo.svg">
</picture>

# MCP (Model Context Protocol)

這個資料夾包含完整的文件與範例，說明如何在 Claude Code 中設定與使用 MCP 伺服器。

## 總覽

MCP（Model Context Protocol）是 Claude 存取外部工具、API 與即時資料來源的標準化方式。與記憶（Memory）不同，MCP 能即時存取會變動的資料。

主要特性：
- 即時存取外部服務
- 即時資料同步
- 可擴充架構
- 安全的身分驗證
- 以工具為基礎的互動

## MCP 架構

```mermaid
graph TB
    A["Claude"]
    B["MCP 伺服器"]
    C["外部服務"]

    A -->|請求：list_issues| B
    B -->|查詢| C
    C -->|資料| B
    B -->|回應| A

    A -->|請求：create_issue| B
    B -->|動作| C
    C -->|結果| B
    B -->|回應| A

    style A fill:#e1f5fe,stroke:#333,color:#333
    style B fill:#f3e5f5,stroke:#333,color:#333
    style C fill:#e8f5e9,stroke:#333,color:#333
```

## MCP 生態系

```mermaid
graph TB
    A["Claude"] -->|MCP| B["檔案系統<br/>MCP 伺服器"]
    A -->|MCP| C["GitHub<br/>MCP 伺服器"]
    A -->|MCP| D["資料庫<br/>MCP 伺服器"]
    A -->|MCP| E["Slack<br/>MCP 伺服器"]
    A -->|MCP| F["Google Docs<br/>MCP 伺服器"]

    B -->|檔案讀寫| G["本機檔案"]
    C -->|API| H["GitHub 儲存庫"]
    D -->|查詢| I["PostgreSQL/MySQL"]
    E -->|訊息| J["Slack 工作空間"]
    F -->|文件| K["Google Drive"]

    style A fill:#e1f5fe,stroke:#333,color:#333
    style B fill:#f3e5f5,stroke:#333,color:#333
    style C fill:#f3e5f5,stroke:#333,color:#333
    style D fill:#f3e5f5,stroke:#333,color:#333
    style E fill:#f3e5f5,stroke:#333,color:#333
    style F fill:#f3e5f5,stroke:#333,color:#333
    style G fill:#e8f5e9,stroke:#333,color:#333
    style H fill:#e8f5e9,stroke:#333,color:#333
    style I fill:#e8f5e9,stroke:#333,color:#333
    style J fill:#e8f5e9,stroke:#333,color:#333
    style K fill:#e8f5e9,stroke:#333,color:#333
```

## MCP 安裝方式

Claude Code 支援多種傳輸協定來連接 MCP 伺服器：

### HTTP 傳輸（建議）

```bash
# 基本 HTTP 連線
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 附帶身分驗證標頭的 HTTP
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Stdio 傳輸（本機）

適用於在本機執行的 MCP 伺服器：

```bash
# 本機 Node.js 伺服器
claude mcp add --transport stdio myserver -- npx @myorg/mcp-server

# 附帶環境變數
claude mcp add --transport stdio myserver --env KEY=value -- npx server
```

#### stdio 伺服器的 `CLAUDE_PROJECT_DIR`（v2.1.139+）

每個 MCP stdio 伺服器啟動時，環境變數中都已設定 `CLAUDE_PROJECT_DIR=<儲存庫根目錄的絕對路徑>`——與 Hooks 使用的慣例相同。外掛（Plugins）與專案的 `.mcp.json` 檔案可以在 `command`、`args` 與 `env` 值中參照 `${CLAUDE_PROJECT_DIR}`，替換會在 `execve()` 之前完成：

```json
{
  "mcpServers": {
    "repo-tools": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PROJECT_DIR}/.claude/mcp/repo-tools.js"],
      "env": {
        "REPO_ROOT": "${CLAUDE_PROJECT_DIR}"
      }
    }
  }
}
```

當你的 stdio 伺服器需要讀取相對於專案根目錄的檔案，而不論 Claude Code 從哪裡啟動時，就可以使用這個方式。

stdio MCP 伺服器也會收到 `CLAUDE_CODE_SESSION_ID`（與傳給 Hooks 及 Bash 的值相同），即使工作階段（session）是以 `--resume` 恢復的也一樣（v2.1.163+）。

### SSE 傳輸（已棄用）

Server-Sent Events 傳輸已棄用，建議改用 `http`，但目前仍支援：

```bash
claude mcp add --transport sse legacy-server https://example.com/sse
```

### WebSocket 傳輸（`ws`）

WebSocket 伺服器會維持一個持久的雙向連線，適合用在遠端 MCP 伺服器需要主動（未經請求）推送事件給 Claude 的情境。如果你的伺服器只會回應請求，改用 HTTP 會更合適，因為 HTTP 支援 OAuth 與 `claude mcp add --transport` 旗標，而 WebSocket 兩者都不支援。

由於 `--transport` 不接受 `ws`，你需要在 `.mcp.json` 中設定，或透過 `claude mcp add-json` 設定：

```json
{
  "type": "ws",
  "url": "wss://mcp.example.com/socket",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN"
  }
}
```

`type: "ws"` 項目接受與 `http` 相同的 `url`、`headers`、`headersHelper`、`timeout` 與 `alwaysLoad` 欄位。身分驗證**僅支援標頭方式**——WebSocket 伺服器沒有 OAuth 流程。

> **備註**：WebSocket 伺服器不會出現在 `claude mcp list` 的輸出中。請用 `claude mcp get <name>` 或 `/mcp` 面板來檢查它們。

與 HTTP 及 SSE 一樣，WebSocket 連線採用 5 分鐘的閒置視窗；stdio 與 WebSocket 都沒有單次請求的計時器。若 `url` 項目沒有指定 `type`，會回報錯誤並列出 `"http"`、`"sse"`、`"ws"` 為有效值。

### 工作階段的工作目錄（roots/list）

MCP 伺服器可以得知工作階段的工作目錄：啟動目錄加上所有 `--add-dir`／`additionalDirectories` 項目，都會透過 MCP 的 `roots/list` 請求回傳；當這組目錄有變動時，也會送出 `notifications/roots/list_changed` 通知（v2.1.203）。閒置逾時現在也適用於 stdio 伺服器（30 分鐘），並以各伺服器的 `timeout` 作為閒置下限（v2.1.203）。

### Windows 專屬注意事項

在原生 Windows（非 WSL）上，npx 指令請使用 `cmd /c`：

```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

### OAuth 2.0 身分驗證

Claude Code 對需要 OAuth 2.0 的 MCP 伺服器提供支援。連線到啟用 OAuth 的伺服器時，Claude Code 會處理整個身分驗證流程：

```bash
# 連線到啟用 OAuth 的 MCP 伺服器（互動式流程）
claude mcp add --transport http my-service https://my-service.example.com/mcp

# 預先設定 OAuth 憑證以進行非互動式設定
claude mcp add --transport http my-service https://my-service.example.com/mcp \
  --client-id "your-client-id" \
  --client-secret "your-client-secret" \
  --callback-port 8080
```

| 功能 | 說明 |
|---------|-------------|
| **互動式 OAuth** | 使用 `/mcp` 觸發以瀏覽器進行的 OAuth 流程 |
| **預先設定的 OAuth 客戶端** | 內建常見服務（如 Notion、Stripe 等）的 OAuth 客戶端（v2.1.30+） |
| **預先設定憑證** | 用於自動化設定的 `--client-id`、`--client-secret`、`--callback-port` 旗標 |
| **Token 儲存** | Token 會安全地儲存在你系統的金鑰鏈中 |
| **升級驗證（step-up auth）** | 支援針對特權操作的升級身分驗證 |
| **探索結果快取** | OAuth 探索中繼資料會被快取，加快重新連線速度 |
| **中繼資料覆寫** | 在 `.mcp.json` 中設定 `oauth.authServerMetadataUrl`，可覆寫預設的 OAuth 中繼資料探索 |

#### 覆寫 OAuth 中繼資料探索

如果你的 MCP 伺服器在標準 OAuth 中繼資料端點（`/.well-known/oauth-authorization-server`）上會回傳錯誤，但有一個可正常運作的 OIDC 端點，你可以指示 Claude Code 從特定 URL 取得 OAuth 中繼資料。在伺服器設定的 `oauth` 物件中設定 `authServerMetadataUrl`：

```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

URL 必須使用 `https://`。此選項需要 Claude Code v2.1.64 以上版本。

#### 啟動時的身分驗證提示與動態標頭刷新（v2.1.193）

- **啟動時的驗證提示（v2.1.193+）**：啟動時，Claude Code 會顯示一則提示，列出所有仍需要身分驗證的 MCP 伺服器，避免需要登入的伺服器在無聲無息中無法運作。
- **`headersHelper` 自動刷新（v2.1.193+）**：如果你透過 `headersHelper` 提供自訂身分驗證，當伺服器回傳 HTTP 401 或 403 時，這個 helper 會自動被重新呼叫。憑證會即時刷新，不需要手動重新連線。詳見[為自訂身分驗證使用動態標頭](https://code.claude.com/docs/en/mcp)。

> **警告**（v2.1.238）：專案 `.mcp.json` 中的 `headersHelper`，以及專案或 `--add-dir` 代理檔案中內嵌的 MCP 伺服器，現在都需要該資料夾的信任對話框已被接受——即使在 `claude -p` 底下也一樣。這類 helper 執行時**不會繼承憑證環境變數**；使用者、受管、claude.ai 範圍的 helper 則改為從 Claude 設定目錄執行。若某個專案設定原本仰賴繼承的憑證，或仰賴在未信任狀態下執行，將會停止運作，直到你接受信任對話框，並以其他方式提供憑證為止。

### Claude.ai MCP 連接器

在你的 Claude.ai 帳號中設定的 MCP 伺服器，會自動在 Claude Code 中可用。這代表你透過 Claude.ai 網頁介面設定的任何 MCP 連線，都不需要額外設定就能使用。

Claude.ai 的 MCP 連接器在 `--print` 模式下也可使用（v2.1.83+），讓非互動式與腳本化的使用方式成為可能。

> **啟動說明（v2.1.117+）：** 當同時設定了本機與 claude.ai 的 MCP 伺服器時，預設會採用並行連線（先前為序列連線），在使用多個伺服器時可降低啟動延遲。

若要在 Claude Code 中停用 Claude.ai 的 MCP 伺服器，請將環境變數 `ENABLE_CLAUDEAI_MCP_SERVERS` 設為 `false`：

```bash
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

> **注意：** 此功能僅適用於以 Claude.ai 帳號登入的使用者。

## MCP 設定流程

```mermaid
sequenceDiagram
    participant User as 使用者
    participant Claude as Claude Code
    participant Config as 設定檔
    participant Service as 外部服務

    User->>Claude: 輸入 /mcp
    Claude->>Claude: 列出可用的 MCP 伺服器
    Claude->>User: 顯示選項
    User->>Claude: 選擇 GitHub MCP
    Claude->>Config: 更新設定
    Config->>Claude: 啟用連線
    Claude->>Service: 測試連線
    Service-->>Claude: 身分驗證成功
    Claude->>User: ✅ MCP 已連線！
```

### `/mcp` 指令

在工作階段中輸入 `/mcp`，即可列出已連線的伺服器、觸發 OAuth 流程，並檢視連線狀態。

- 自 **v2.1.121** 起，MCP 遇到暫時性錯誤時，初始連線最多會重試 3 次。
- 自 **v2.1.128** 起，`/mcp` 會顯示每個已連線伺服器的**工具數量**，並以視覺方式標示回報**0 個工具**的伺服器，讓設定錯誤的伺服器一眼就能看出來。

## MCP 工具搜尋

當 MCP 工具說明超過上下文視窗的 10% 時，Claude Code 會自動啟用工具搜尋，以有效率地選出正確的工具，避免塞爆模型的上下文。

| 設定 | 值 | 說明 |
|---------|-------|-------------|
| `ENABLE_TOOL_SEARCH` | `auto`（預設） | 當工具說明超過上下文的 10% 時自動啟用 |
| `ENABLE_TOOL_SEARCH` | `auto:<N>` | 在自訂的 `N` 個工具門檻時自動啟用 |
| `ENABLE_TOOL_SEARCH` | `true` | 不論工具數量一律啟用 |
| `ENABLE_TOOL_SEARCH` | `false` | 停用；一律完整傳送所有工具說明 |

> **注意：** 工具搜尋需要 Sonnet 4 以上或 Opus 4 以上的模型。Haiku 模型不支援工具搜尋。

### 逐伺服器略過工具搜尋（v2.1.121+）

如果某個特定 MCP 伺服器的工具每一輪都需要用到，可以在它的
設定中加上 `"alwaysLoad": true`，跳過工具搜尋的延後載入機制，
讓它的工具始終保持可用：

```json
{
  "mcpServers": {
    "always-on-tool": {
      "command": "node",
      "args": ["./tools/always.js"],
      "alwaysLoad": true
    }
  }
}
```

請謹慎使用——每個一律載入的工具都會消耗原本可用於工具搜尋、
藉此呈現更相關工具的上下文。

## 動態工具更新

Claude Code 支援 MCP 的 `list_changed` 通知。當 MCP 伺服器動態新增、移除或修改其可用工具時，Claude Code 會收到更新，並自動調整其工具清單——不需要重新連線或重新啟動。

## MCP Apps

MCP Apps 是第一個官方 MCP 擴充功能，讓 MCP 工具呼叫可以回傳直接顯示在聊天介面中的互動式 UI 元件。MCP 伺服器不再只能回傳純文字回應，而是可以提供豐富的儀表板、表單、資料視覺化與多步驟工作流程——全部都以內嵌方式顯示，不需要離開對話。

## MCP Elicitation

MCP 伺服器可以透過互動式對話框，向使用者請求結構化輸入（v2.1.49+）。這讓 MCP 伺服器可以在工作流程進行到一半時要求額外資訊——例如要求確認、從選項清單中選擇，或填寫必填欄位——為 MCP 伺服器的互動增添互動性。

## 工具說明與指示上限

自 v2.1.84 起，Claude Code 對每個 MCP 伺服器的工具說明與指示強制施加 **2 KB 上限**。這可避免個別伺服器因為過於冗長的工具定義而佔用過多上下文，減少上下文膨脹，並讓互動維持高效率。

## 以斜線指令形式呈現的 MCP 提示詞

MCP 伺服器可以公開提示詞，這些提示詞會以斜線指令（Slash Commands）的形式出現在 Claude Code 中。提示詞可用以下命名慣例存取：

```
/mcp__<server>__<prompt>
```

舉例來說，如果一個名為 `github` 的伺服器公開了一個叫做 `review` 的提示詞，你可以用 `/mcp__github__review` 來呼叫它。

## 重複伺服器的去除

當同一個 MCP 伺服器在多個範圍（本機、專案、使用者）中都有定義時，本機設定的優先權最高。這讓你可以用本機的自訂設定，覆寫專案層級或使用者層級的 MCP 設定，而不會產生衝突。

## 近期的生命週期修正（v2.1.136）

v2.1.136 修正了兩個存在已久的 MCP 生命週期臭蟲——如果你使用多伺服器設定，值得升級：

- **MCP 伺服器在 `/clear` 之後仍會保留**：透過 `.mcp.json`、外掛或 claude.ai 連接器設定的伺服器，在 VS Code、JetBrains 或 Agent SDK 中執行 `/clear` 後不再消失。舊版本會默默地把它們丟掉，需要重新啟動才能恢復。
- **OAuth 更新權杖並行刷新修正**：多伺服器 OAuth 設定，在多個伺服器同時搶著刷新時，不再遺失更新權杖（refresh token）。這解決了「每天早上都要重新驗證」的問題，此問題原本會影響設有多個受 OAuth 保護的 MCP 伺服器的環境。

## 透過 @ 提及使用 MCP 資源

你可以在提示詞中用 `@` 提及語法，直接參照 MCP 資源：

```
@server-name:protocol://resource/path
```

舉例來說，要參照特定的資料庫資源：

```
@database:postgres://mydb/users
```

這讓 Claude 可以擷取 MCP 資源內容，並將其內嵌納入對話的上下文中。

## MCP 範圍

MCP 設定可以儲存在不同的範圍，各自有不同程度的共享方式：

| 範圍 | 旗標 | 位置 | 說明 | 共享對象 | 需要核准 |
|-------|------|----------|-------------|-------------|------------------|
| **本機**（預設） | `--scope local` | `~/.claude.json`（位於專案路徑底下） | 僅限目前使用者、目前專案私用（舊版本稱為 `project`） | 只有你自己 | 否 |
| **專案** | `--scope project` | `.mcp.json` | 提交進 git 儲存庫 | 團隊成員 | 是（首次使用時） |
| **使用者** | `--scope user` | `~/.claude.json` | 可在所有專案間使用（舊版本稱為 `global`） | 只有你自己 | 否 |

在新增伺服器時可用 `--scope`（縮寫 `-s`）選擇範圍。若省略，
Claude Code 會使用 `local`：

```bash
# 專案範圍——寫入 .mcp.json，讓團隊共享
claude mcp add --scope project --transport http github https://api.github.com/mcp

# 使用者範圍——在每個專案中都可用
claude mcp add --scope user --transport stdio memory -- npx @modelcontextprotocol/server-memory
```

### 使用專案範圍

將專案專屬的 MCP 設定儲存在 `.mcp.json` 中：

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.github.com/mcp"
    }
  }
}
```

團隊成員第一次使用專案 MCP 時，會看到核准提示。在未受信任的工作區中，透過已提交的 `.claude/settings.json` 由儲存庫自行核准的伺服器，**不會**被 `claude mcp list`／`get` 自動啟動——它們會顯示 `⏸ Pending approval`，直到你接受信任對話框為止；而在未受信任的資料夾中，`enableAllProjectMcpServers` 會被忽略（v2.1.196）。

## MCP 設定管理

### 新增 MCP 伺服器

```bash
# 新增以 HTTP 為基礎的伺服器
claude mcp add --transport http github https://api.github.com/mcp

# 新增本機 stdio 伺服器
claude mcp add --transport stdio database -- npx @company/db-server

# 列出所有 MCP 伺服器
claude mcp list

# 取得特定伺服器的詳細資訊
claude mcp get github

# 移除 MCP 伺服器
claude mcp remove github

# 重設專案專屬的核准選擇
claude mcp reset-project-choices

# 從 CLI 對 MCP 伺服器進行身分驗證（v2.1.186+）
claude mcp login github

# 登出 MCP 伺服器（v2.1.186+）
claude mcp logout github

# 從 Claude Desktop 匯入
claude mcp add-from-claude-desktop

# 用 JSON 內容新增伺服器（適合腳本化設定）
claude mcp add-json events-server '{"type":"stdio","command":"npx","args":["@modelcontextprotocol/server-events"]}'
```

> **備註**：在 JSON 設定中——`.mcp.json`、`~/.claude.json`，或 `claude mcp add-json`——`type` 欄位接受 `streamable-http` 作為 `http` 的別名。MCP 規格對這種傳輸方式使用 `streamable-http` 這個名稱，所以從伺服器自身文件複製過來的設定不需修改就能使用。

自 v2.1.238 起，`claude mcp list` 與 `claude mcp get` 會將已停用的伺服器顯示為 `⊘ Disabled`，而不會為了健康檢查去連線。

`claude mcp login <name>` ／ `claude mcp logout <name>` 是 `/mcp` 選單中 OAuth 流程的非互動式對應指令——不需要開啟選單就能進行身分驗證或登出。在 `login` 加上 `--no-browser`，即可透過 SSH 或在無介面工作階段中完成 OAuth（它會透過 stdin 重新導向該流程）。

## 可用的 MCP 伺服器一覽表

| MCP 伺服器 | 用途 | 常見工具 | 驗證方式 | 即時 |
|------------|---------|--------------|------|-----------|
| **Filesystem** | 檔案操作 | read, write, delete | OS 權限 | ✅ 是 |
| **GitHub** | 儲存庫管理 | list_prs, create_issue, push | OAuth | ✅ 是 |
| **Slack** | 團隊溝通 | send_message, list_channels | Token | ✅ 是 |
| **Database** | SQL 查詢 | query, insert, update | 憑證 | ✅ 是 |
| **Google Docs** | 文件存取 | read, write, share | OAuth | ✅ 是 |
| **Asana** | 專案管理 | create_task, update_status | API 金鑰 | ✅ 是 |
| **Stripe** | 付款資料 | list_charges, create_invoice | API 金鑰 | ✅ 是 |
| **Memory** | 持久記憶 | store, retrieve, delete | 本機 | ❌ 否 |

## 實際範例

### 範例 1：GitHub MCP 設定

**檔案：** `.mcp.json`（專案根目錄）

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

**可用的 GitHub MCP 工具：**

#### Pull Request 管理
- `list_prs` - 列出儲存庫中的所有 PR
- `get_pr` - 取得 PR 詳細資訊，包含 diff
- `create_pr` - 建立新的 PR
- `update_pr` - 更新 PR 的描述／標題
- `merge_pr` - 將 PR 合併到主分支
- `review_pr` - 加入審查意見

**範例請求：**
```
/mcp__github__get_pr 456

# 回傳：
Title: 新增深色模式支援
Author: @alice
Description: 使用 CSS 變數實作深色主題
Status: OPEN
Reviewers: @bob, @charlie
```

#### Issue 管理
- `list_issues` - 列出所有 Issue
- `get_issue` - 取得 Issue 詳細資訊
- `create_issue` - 建立新的 Issue
- `close_issue` - 關閉 Issue
- `add_comment` - 為 Issue 新增留言

#### 儲存庫資訊
- `get_repo_info` - 儲存庫詳細資訊
- `list_files` - 檔案樹狀結構
- `get_file_content` - 讀取檔案內容
- `search_code` - 跨程式碼庫搜尋

#### Commit 操作
- `list_commits` - 提交歷史紀錄
- `get_commit` - 特定 Commit 的詳細資訊
- `create_commit` - 建立新的 Commit

**設定**：
```bash
export GITHUB_TOKEN="your_github_token"
# 或直接用 CLI 新增：
claude mcp add --transport stdio github -- npx @modelcontextprotocol/server-github
```

### 設定中的環境變數展開

MCP 設定支援環境變數展開，並可搭配預設值當作備援。`${VAR}` 與 `${VAR:-default}` 語法適用於以下欄位：`command`、`args`、`env`、`url`、`headers`。

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}",
        "X-Custom-Header": "${CUSTOM_HEADER:-default-value}"
      }
    },
    "local-server": {
      "command": "${MCP_BIN_PATH:-npx}",
      "args": ["${MCP_PACKAGE:-@company/mcp-server}"],
      "env": {
        "DB_URL": "${DATABASE_URL:-postgresql://localhost/dev}"
      }
    }
  }
}
```

變數會在執行期展開：
- `${VAR}` - 使用環境變數，若未設定則回報錯誤
- `${VAR:-default}` - 使用環境變數，若未設定則使用預設值

### 範例 2：資料庫 MCP 設定

**設定：**

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-database"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

**使用範例：**

```markdown
User: 找出所有訂單數超過 10 筆的使用者

Claude: 我會查詢你的資料庫來找出這項資訊。

# 使用 MCP 資料庫工具：
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
HAVING COUNT(o.id) > 10
ORDER BY order_count DESC;

# 結果：
- Alice：15 筆訂單
- Bob：12 筆訂單
- Charlie：11 筆訂單
```

**設定**：
```bash
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
# 或直接用 CLI 新增：
claude mcp add --transport stdio database -- npx @modelcontextprotocol/server-database
```

### 範例 3：多 MCP 工作流程

**情境：每日報告產出**

```markdown
# 使用多個 MCP 的每日報告工作流程

## 設定
1. GitHub MCP - 取得 PR 指標
2. Database MCP - 查詢銷售資料
3. Slack MCP - 發布報告
4. Filesystem MCP - 儲存報告

## 工作流程

### 步驟 1：取得 GitHub 資料
/mcp__github__list_prs completed:true last:7days

輸出：
- 總 PR 數：42
- 平均合併時間：2.3 小時
- 審查回覆時間：1.1 小時

### 步驟 2：查詢資料庫
SELECT COUNT(*) as sales, SUM(amount) as revenue
FROM orders
WHERE created_at > NOW() - INTERVAL '1 day'

輸出：
- 銷售量：247
- 營收：$12,450

### 步驟 3：產生報告
把資料整合成 HTML 報告

### 步驟 4：儲存到檔案系統
將 report.html 寫入 /reports/

### 步驟 5：發布到 Slack
將摘要傳送到 #daily-reports 頻道

最終輸出：
✅ 報告已產生並發布
📊 本週合併了 47 個 PR
💰 每日銷售額 $12,450
```

**設定**：
```bash
export GITHUB_TOKEN="your_github_token"
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
export SLACK_TOKEN="your_slack_token"
# 透過 CLI 新增每個 MCP 伺服器，或在 .mcp.json 中設定它們
```

### 範例 4：Filesystem MCP 操作

**設定：**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    }
  }
}
```

**可用操作：**

| 操作 | 指令 | 用途 |
|-----------|---------|---------|
| 列出檔案 | `ls ~/projects` | 顯示目錄內容 |
| 讀取檔案 | `cat src/main.ts` | 讀取檔案內容 |
| 寫入檔案 | `create docs/api.md` | 建立新檔案 |
| 編輯檔案 | `edit src/app.ts` | 修改檔案 |
| 搜尋 | `grep "async function"` | 在檔案中搜尋 |
| 刪除 | `rm old-file.js` | 刪除檔案 |

**設定**：
```bash
# 直接用 CLI 新增：
claude mcp add --transport stdio filesystem -- npx @modelcontextprotocol/server-filesystem /home/user/projects
```

## MCP 與記憶（Memory）的決策矩陣

```mermaid
graph TD
    A["需要外部資料？"]
    A -->|否| B["使用記憶"]
    A -->|是| C["資料會頻繁變動嗎？"]
    C -->|否／很少| B
    C -->|是／經常| D["使用 MCP"]

    B -->|儲存| E["偏好設定<br/>上下文<br/>歷史紀錄"]
    D -->|存取| F["即時 API<br/>資料庫<br/>服務"]

    style A fill:#fff3e0,stroke:#333,color:#333
    style B fill:#e1f5fe,stroke:#333,color:#333
    style C fill:#fff3e0,stroke:#333,color:#333
    style D fill:#f3e5f5,stroke:#333,color:#333
    style E fill:#e8f5e9,stroke:#333,color:#333
    style F fill:#e8f5e9,stroke:#333,color:#333
```

## 請求／回應模式

```mermaid
sequenceDiagram
    participant App as Claude
    participant MCP as MCP 伺服器
    participant DB as 資料庫

    App->>MCP: 請求："SELECT * FROM users WHERE id=1"
    MCP->>DB: 執行查詢
    DB-->>MCP: 結果集
    MCP-->>App: 回傳解析後的資料
    App->>App: 處理結果
    App->>App: 繼續任務

    Note over MCP,DB: 即時存取<br/>不使用快取
```

## 環境變數

把敏感憑證儲存在環境變數中：

```bash
# ~/.bashrc 或 ~/.zshrc
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
export SLACK_TOKEN="xoxb-xxxxxxxxxxxxx"
```

接著在 MCP 設定中參照它們：

```json
{
  "env": {
    "GITHUB_TOKEN": "${GITHUB_TOKEN}"
  }
}
```

## Claude 作為 MCP 伺服器（`claude mcp serve`）

Claude Code 本身也可以扮演 MCP 伺服器的角色，供其他應用程式使用。這讓外部工具、編輯器與自動化系統，能透過標準 MCP 協定運用 Claude 的能力。

```bash
# 以 stdio 啟動 Claude Code 作為 MCP 伺服器
claude mcp serve
```

其他應用程式接著就能像連接任何以 stdio 為基礎的 MCP 伺服器一樣連接這個伺服器。舉例來說，要在另一個 Claude Code 實例中把 Claude Code 加為 MCP 伺服器：

```bash
claude mcp add --transport stdio claude-agent -- claude mcp serve
```

這對建構多代理工作流程很有用，可以讓一個 Claude 實例協調另一個。

## 受管的 MCP 設定（企業版）

在企業部署中，IT 管理員透過兩種各自獨立的機制來強制執行 MCP 伺服器政策：一是 `managed-mcp.json` 檔案，用來部署一組固定且具排他控制權的伺服器；二是 `allowedMcpServers` ／ `deniedMcpServers` 設定鍵，用來篩選哪些已設定的伺服器可以載入。

**位置：**
- macOS：`/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux 與 WSL：`/etc/claude-code/managed-mcp.json`
- Windows：`C:\Program Files\ClaudeCode\managed-mcp.json`

`managed-mcp.json` 使用與專案 `.mcp.json` 相同的格式——一個頂層的 `mcpServers` 對照表。它負責部署伺服器，而不負責篩選：

```json
{
  "mcpServers": {
    "example-remote": {
      "type": "http",
      "url": "https://mcp.example.com/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"]
    }
  }
}
```

機器上的任何使用者都能讀取這個檔案，所以絕對不要把憑證放在 `env` 區塊裡。請改用 `${VAR}` 展開、OAuth 或 `headersHelper`。

**篩選：允許清單與封鎖清單**

`allowedMcpServers`、`deniedMcpServers` 與 `allowAllClaudeAiMcps` 是**設定鍵，而不是 `managed-mcp.json` 的欄位**。要讓它們可被強制執行，必須放進受管設定來源——伺服器端受管設定、`managed-settings.json`、MDM 設定檔，或登錄檔：

- `allowedMcpServers`——允許的伺服器清單。請在同一個受管來源中一併設定 `allowManagedMcpServersOnly: true`，否則允許清單會從各個範圍合併，使用者就能擴大你的清單。
- `deniedMcpServers`——封鎖的伺服器清單。無論如何都會從各個範圍合併。
- `allowAllClaudeAiMcps`——在部署 `managed-mcp.json` 的同時載入 claude.ai 雲端連接器（v2.1.149+）。只能從管理員控制的政策層級讀取。

每個項目都是只有**單一**鍵的物件：

| 鍵 | 比對對象 |
|-----|---------|
| `serverUrl` | 遠端伺服器 URL，可精確比對或用 `*` 萬用字元 |
| `serverCommand` | 啟動 stdio 伺服器的確切指令與引數，以陣列表示——依序列出每個引數 |
| `serverName` | 使用者指定的標籤。**僅限完全比對；不會展開萬用字元** |

**設定範例：**

```json
{
  "allowedMcpServers": [
    { "serverUrl": "https://mcp.example.com/*" },
    { "serverCommand": ["/usr/local/bin/company-mcp-server", "--config", "/etc/company/mcp-config.json"] }
  ],
  "deniedMcpServers": [
    { "serverName": "untrusted-server" },
    { "serverUrl": "http://*" }
  ],
  "allowManagedMcpServersOnly": true
}
```

第三個受管設定 `managedMcpServers`（v2.1.259+），讓組織可以為每個使用者提供 HTTP／SSE MCP 伺服器。項目的結構與 `.mcp.json` 相同；若項目指定了要執行的指令，則會被略過。

> **注意：** 當 `allowedMcpServers` 與 `deniedMcpServers` 同時比對到同一個伺服器時，以封鎖規則為準。

## 外掛提供的 MCP 伺服器

外掛可以搭載自己的 MCP 伺服器，並在外掛安裝時自動提供這些伺服器。外掛提供的 MCP 伺服器可以用兩種方式定義：

1. **獨立的 `.mcp.json`**——在外掛根目錄放一個 `.mcp.json` 檔案
2. **內嵌在 `plugin.json` 中**——直接在外掛清單中定義 MCP 伺服器

使用 `${CLAUDE_PLUGIN_ROOT}` 變數來參照相對於外掛安裝目錄的路徑：

```json
{
  "mcpServers": {
    "plugin-tools": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/dist/mcp-server.js"],
      "env": {
        "CONFIG_PATH": "${CLAUDE_PLUGIN_ROOT}/config.json"
      }
    }
  }
}
```

## 子代理範圍的 MCP

可以用 `mcpServers:` 鍵，在代理的 frontmatter 中內嵌定義 MCP 伺服器，讓它們的範圍侷限在特定子代理（Subagents），而非整個專案。當某個代理需要存取工作流程中其他代理不需要的特定 MCP 伺服器時，這個做法很有用。

```yaml
---
mcpServers:
  my-tool:
    type: http
    url: https://my-tool.example.com/mcp
---

You are an agent with access to my-tool for specialized operations.
```

子代理範圍的 MCP 伺服器僅在該代理的執行情境中可用，不會與父代理或同層代理共享。

## MCP 輸出上限

Claude Code 對 MCP 工具輸出強制施加上限，以避免上下文溢位：

| 上限 | 門檻 | 行為 |
|-------|-----------|----------|
| **警告** | 10,000 個 token | 顯示輸出過大的警告 |
| **預設上限** | 25,000 個 token | 超過此上限的輸出會被截斷 |
| **磁碟持久化** | 50,000 個字元 | 超過 50K 字元的工具結果會被持久化到磁碟 |

最大輸出上限可以透過環境變數 `MAX_MCP_OUTPUT_TOKENS` 設定：

```bash
# 將最大輸出提高到 50,000 個 token
export MAX_MCP_OUTPUT_TOKENS=50000
```

## 長時間執行的工具呼叫自動轉為背景任務（v2.1.212）

執行時間超過 2 分鐘的 MCP 工具呼叫，現在會自動轉為背景任務，讓工作階段保持可用，不會因為速度慢的工具而卡住。這個門檻可以透過 `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` 設定，行為也可以被調整或停用：

```bash
# 把自動轉為背景任務的門檻改為 5 分鐘（300,000ms）
export CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS=300000
```

## 用程式碼執行解決上下文膨脹

隨著 MCP 的採用規模擴大，連接到數十個伺服器、上百甚至上千個工具，會帶來一項重大挑戰：**上下文膨脹**。這可說是 MCP 在大規模使用時最大的問題，而 Anthropic 的工程團隊提出了一個優雅的解決方案——用程式碼執行取代直接的工具呼叫。

> **來源**：[Code Execution with MCP: Building More Efficient Agents](https://www.anthropic.com/engineering/code-execution-with-mcp) —— Anthropic Engineering Blog

### 問題所在：兩種 token 浪費的來源

**1. 工具定義塞爆上下文視窗**

大多數 MCP 客戶端會預先載入所有工具定義。當連接到上千個工具時，模型甚至在讀到使用者的請求之前，就得先處理數十萬個 token。

**2. 中間結果消耗額外的 token**

每一個中間工具結果都會經過模型的上下文。想像把一份會議逐字稿從 Google Drive 搬到 Salesforce——完整的逐字稿會**兩次**流經上下文：一次是讀取時，另一次是寫入目的地時。一份 2 小時的會議逐字稿，可能就代表多出 50,000 個以上的 token。

```mermaid
graph LR
    A["模型"] -->|"工具呼叫：getDocument"| B["MCP 伺服器"]
    B -->|"完整逐字稿（5 萬個 token）"| A
    A -->|"工具呼叫：updateRecord<br/>（重新傳送完整逐字稿）"| B
    B -->|"確認"| A

    style A fill:#ffcdd2,stroke:#333,color:#333
    style B fill:#f3e5f5,stroke:#333,color:#333
```

### 解決方案：把 MCP 工具當成程式碼 API

代理不再把工具定義與結果傳遞經過上下文視窗，而是**撰寫程式碼**，把 MCP 工具當成 API 來呼叫。這段程式碼會在沙箱化的執行環境中執行，只有最終結果會回傳給模型。

```mermaid
graph LR
    A["模型"] -->|"撰寫程式碼"| B["程式碼執行環境"]
    B -->|"直接呼叫工具"| C["MCP 伺服器"]
    C -->|"資料留在<br/>執行環境中"| B
    B -->|"只回傳最終結果<br/>（極少 token）"| A

    style A fill:#c8e6c9,stroke:#333,color:#333
    style B fill:#e1f5fe,stroke:#333,color:#333
    style C fill:#f3e5f5,stroke:#333,color:#333
```

#### 運作原理

MCP 工具會以帶型別函式的檔案樹狀結構呈現：

```
servers/
├── google-drive/
│   ├── getDocument.ts
│   └── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   └── index.ts
└── ...
```

每個工具檔案都包含一個帶型別的包裝函式：

```typescript
// ./servers/google-drive/getDocument.ts
import { callMCPTool } from "../../../client.js";

interface GetDocumentInput {
  documentId: string;
}

interface GetDocumentResponse {
  content: string;
}

export async function getDocument(
  input: GetDocumentInput
): Promise<GetDocumentResponse> {
  return callMCPTool<GetDocumentResponse>(
    'google_drive__get_document', input
  );
}
```

接著代理撰寫程式碼來協調這些工具：

```typescript
import * as gdrive from './servers/google-drive';
import * as salesforce from './servers/salesforce';

// 資料直接在工具之間流動——完全不經過模型
const transcript = (
  await gdrive.getDocument({ documentId: 'abc123' })
).content;

await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: transcript }
});
```

**結果：token 用量從約 150,000 降到約 2,000——減少了 98.7%。**

### 主要好處

| 好處 | 說明 |
|---------|-------------|
| **漸進式揭露（Progressive Disclosure）** | 代理瀏覽檔案系統，只載入它需要的工具定義，而非一開始就載入全部工具 |
| **上下文高效的結果** | 資料在回傳給模型之前，先在執行環境中篩選／轉換 |
| **強大的控制流程** | 迴圈、條件判斷與錯誤處理都在程式碼中執行，不需來回經過模型 |
| **隱私保護** | 中間資料（個資、機密紀錄）留在執行環境中，永遠不會進入模型的上下文 |
| **狀態持久化** | 代理可以把中間結果存成檔案，並建立可重複使用的技能（Skills）函式 |

#### 範例：篩選大型資料集

```typescript
// 不使用程式碼執行——全部 10,000 列資料都會流經上下文
// 工具呼叫：gdrive.getSheet(sheetId: 'abc123')
//   -> 回傳的 10,000 列資料進入上下文

// 使用程式碼執行——在執行環境中篩選
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
const pendingOrders = allRows.filter(
  row => row["Status"] === 'pending'
);
console.log(`Found ${pendingOrders.length} pending orders`);
console.log(pendingOrders.slice(0, 5)); // 只有 5 列資料進入模型
```

#### 範例：不需來回呼叫的迴圈

```typescript
// 輪詢部署通知——完全在程式碼中執行
let found = false;
while (!found) {
  const messages = await slack.getChannelHistory({
    channel: 'C123456'
  });
  found = messages.some(
    m => m.text.includes('deployment complete')
  );
  if (!found) await new Promise(r => setTimeout(r, 5000));
}
console.log('Deployment notification received');
```

### 需要考量的取捨

程式碼執行也帶來自己的複雜度。執行代理產生的程式碼需要：

- 具備適當資源限制的**安全沙箱執行環境**
- 對執行的程式碼進行**監控與記錄**
- 相較於直接工具呼叫，會有額外的**基礎設施成本**

好處——降低 token 成本、降低延遲、改善工具組合方式——應該與這些實作成本互相權衡。對只有少數幾個 MCP 伺服器的代理來說，直接工具呼叫或許更簡單。對規模較大的代理（數十個伺服器、上百個工具）來說，程式碼執行是顯著的改善。

### MCPorter：一個用於組合 MCP 工具的執行期環境

[MCPorter](https://github.com/steipete/mcporter) 是一個 TypeScript 執行期環境與 CLI 工具組，讓呼叫 MCP 伺服器不需要樣板程式碼就能實際運用——並透過選擇性工具公開與帶型別的包裝函式，協助減少上下文膨脹。

**它解決的問題：** MCPorter 不會預先載入所有 MCP 伺服器的全部工具定義，而是讓你依需求探索、檢視並呼叫特定工具——讓你的上下文保持精簡。

**主要功能：**

| 功能 | 說明 |
|---------|-------------|
| **零設定探索** | 自動從 Cursor、Claude、Codex 或本機設定中探索 MCP 伺服器 |
| **帶型別的工具客戶端** | `mcporter emit-ts` 會產生 `.d.ts` 介面與可直接執行的包裝函式 |
| **可組合的 API** | `createServerProxy()` 會把工具以駝峰命名法（camelCase）的方法公開，並附帶 `.text()`、`.json()`、`.markdown()` 輔助方法 |
| **CLI 產生** | `mcporter generate-cli` 可以把任何 MCP 伺服器轉換成獨立的 CLI，並支援 `--include-tools` ／ `--exclude-tools` 篩選 |
| **參數隱藏** | 選用參數預設會保持隱藏，減少 schema 的冗長程度 |

**安裝：**

```bash
npx mcporter list          # 不需安裝——立即探索伺服器
pnpm add mcporter          # 加入專案
brew install steipete/tap/mcporter  # 在 macOS 上透過 Homebrew 安裝
```

**範例——用 TypeScript 組合工具：**

```typescript
import { createRuntime, createServerProxy } from "mcporter";

const runtime = await createRuntime();
const gdrive = createServerProxy(runtime, "google-drive");
const salesforce = createServerProxy(runtime, "salesforce");

// 資料在工具之間流動，不經過模型的上下文
const doc = await gdrive.getDocument({ documentId: "abc123" });
await salesforce.updateRecord({
  objectType: "SalesMeeting",
  recordId: "00Q5f000001abcXYZ",
  data: { Notes: doc.text() }
});
```

**範例——CLI 工具呼叫：**

```bash
# 直接呼叫特定工具
npx mcporter call linear.create_comment issueId:ENG-123 body:'Looks good!'

# 列出可用的伺服器與工具
npx mcporter list
```

MCPorter 補足了上述程式碼執行方法，提供把 MCP 工具當成帶型別 API 呼叫所需的執行期基礎設施——讓中間資料不進入模型上下文變得輕而易舉。

## 最佳實踐

### 安全性考量

#### 建議做法 ✅
- 所有憑證都使用環境變數
- 定期輪換 token 與 API 金鑰（建議每月一次）
- 盡可能使用唯讀 token
- 把 MCP 伺服器的存取範圍限制在所需的最小程度
- 監控 MCP 伺服器的使用與存取記錄
- 有提供 OAuth 時就對外部服務使用 OAuth
- 對 MCP 請求實作速率限制
- 在正式上線前先測試 MCP 連線
- 記錄所有作用中的 MCP 連線
- 保持 MCP 伺服器套件為最新版本

#### 避免做法 ❌
- 不要把憑證寫死在設定檔中
- 不要把 token 或機密資料提交到 git
- 不要在團隊聊天室或電子郵件中分享 token
- 不要用個人 token 執行團隊專案
- 不要授予不必要的權限
- 不要忽略身分驗證錯誤
- 不要把 MCP 端點公開對外
- 不要以 root／管理員權限執行 MCP 伺服器
- 不要在記錄檔中快取敏感資料
- 不要停用身分驗證機制

### 設定最佳實踐

1. **版本控制**：把 `.mcp.json` 放進 git，但機密資料要用環境變數
2. **最小權限**：只授予每個 MCP 伺服器所需的最少權限
3. **隔離**：盡可能讓不同的 MCP 伺服器在各自獨立的程序中執行
4. **監控**：記錄所有 MCP 請求與錯誤，以利稽核追蹤
5. **測試**：在部署到正式環境之前，測試所有 MCP 設定

### 效能提示

- 在應用程式層快取常用的資料
- 使用精確的 MCP 查詢以減少資料傳輸量
- 監控 MCP 操作的回應時間
- 考慮對外部 API 實作速率限制
- 執行多項操作時使用批次處理

## 安裝說明

### 先備知識
- 已安裝 Node.js 與 npm
- 已安裝 Claude Code CLI
- 具備外部服務的 API token／憑證

### 逐步設定

1. 用 CLI **新增你的第一個 MCP 伺服器**（範例：GitHub）：
```bash
claude mcp add --transport stdio github -- npx @modelcontextprotocol/server-github
```

   或在你的專案根目錄建立一個 `.mcp.json` 檔案：
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

2. **設定環境變數：**
```bash
export GITHUB_TOKEN="your_github_personal_access_token"
```

3. **測試連線：**
```bash
claude /mcp
```

4. **使用 MCP 工具：**
```bash
/mcp__github__list_prs
/mcp__github__create_issue "Title" "Description"
```

### 特定服務的安裝方式

**GitHub MCP：**
```bash
npm install -g @modelcontextprotocol/server-github
```

**Database MCP：**
```bash
npm install -g @modelcontextprotocol/server-database
```

**Filesystem MCP：**
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Slack MCP：**
```bash
npm install -g @modelcontextprotocol/server-slack
```

## 疑難排解

### 先看錯誤輸出（v2.1.219+）

如果某個伺服器無法連線，先執行 `claude mcp list`（或在工作階段中輸入 `/mcp`），再開始改動任何東西。Claude Code 現在會在失敗的伺服器旁印出 **HTTP 狀態碼與該伺服器的錯誤文字**，因此你會看到 `401 Unauthorized` 或 `404 Not Found`，而不是一般籠統的「連線失敗」：

```bash
# 顯示連線狀態，以及失敗時的 HTTP 狀態碼與錯誤文字
claude mcp list
```

先看狀態碼——它會告訴你該套用哪種修法：

- `401` / `403` → 憑證錯誤或已過期；用 `claude mcp login <name>` 重新驗證
- `404` → URL 錯誤（常見原因是少了 `/mcp` 或 `/sse` 這樣的路徑後綴）
- `5xx` / 逾時 → 遠端伺服器故障；參見[連線逾時](#連線逾時)

### 設定值中隱藏的空白字元（v2.1.219+）

當 MCP 設定值前後有**多餘空白**時，Claude Code 會發出警告。這是造成驗證失敗、卻很難察覺的常見原因：從瀏覽器或聊天訊息複製貼上的 token，經常會多帶一個尾隨空白或換行字元，這會原封不動地送進 `Authorization` 標頭，並因憑證無效而失敗。

如果你看到這個警告，請重新檢查 `.mcp.json` 中的值（或它所展開的環境變數），並將其修剪乾淨：

```bash
# 顯示分隔符號之間隱藏的前導／尾隨空白
printf '[%s]\n' "$GITHUB_TOKEN"
```

### 無介面執行時被略過的伺服器（v2.1.219+）

透過 `--mcp-config` 傳入、卻未通過設定驗證的伺服器會被**略過**，而不是中止整個執行，所以無介面腳本可能看起來正常運作，實際上卻少了一半的工具。Claude Code 現在會回報哪些伺服器被丟棄：

- **無介面／`-p` 執行**：stream-json 的 `init` 事件會帶有一個 `mcp_server_errors` 欄位，列出每個被略過的項目。在信任執行結果之前先檢查它。
- **互動式終端機執行**：同樣的問題會在工作階段開始時，以啟動警告的形式印出。

```bash
# 檢視無介面執行中被略過的 --mcp-config 項目
claude -p "列出我的工具" --mcp-config ./servers.json \
  --output-format stream-json --verbose \
  | jq -r 'select(.type == "system" and .subtype == "init") | .mcp_server_errors'
```

### 找不到 MCP 伺服器
```bash
# 確認 MCP 伺服器已安裝
npm list -g @modelcontextprotocol/server-github

# 若缺少則安裝
npm install -g @modelcontextprotocol/server-github
```

### 身分驗證失敗
```bash
# 確認環境變數已設定
echo $GITHUB_TOKEN

# 若需要則重新 export
export GITHUB_TOKEN="your_token"

# 確認 token 有正確的權限
# 到這裡檢查 GitHub token 的權限範圍：https://github.com/settings/tokens
```

### 連線逾時
- 檢查網路連線：`ping api.github.com`
- 確認 API 端點可以存取
- 檢查 API 的速率限制
- 嘗試在設定中提高逾時時間
- 檢查防火牆或代理伺服器的問題

### MCP 伺服器當機
- 檢查 MCP 伺服器記錄：`~/.claude/logs/`
- 確認所有環境變數都已設定
- 確保檔案權限正確
- 嘗試重新安裝 MCP 伺服器套件
- 檢查同一個連接埠上是否有衝突的行程

## 相關概念

### 記憶（Memory）與 MCP 的比較
- **記憶（Memory）**：儲存持久、不會變動的資料（偏好設定、上下文、歷史紀錄）
- **MCP**：存取即時、會變動的資料（API、資料庫、即時服務）

### 各自適用的時機
- **使用記憶（Memory）** 適用於：使用者偏好設定、對話歷史、已學到的上下文
- **使用 MCP** 適用於：目前的 GitHub Issue、即時資料庫查詢、即時資料

### 與 Claude 其他功能整合
- 結合 MCP 與記憶（Memory）以取得豐富的上下文
- 在提示詞中使用 MCP 工具以獲得更好的推理能力
- 運用多個 MCP 來處理複雜的工作流程

## 延伸資源

- [官方 MCP 文件](https://code.claude.com/docs/en/mcp)
- [MCP 協定規格](https://modelcontextprotocol.io/specification)
- [MCP GitHub 儲存庫](https://github.com/modelcontextprotocol/servers)
- [可用的 MCP 伺服器](https://github.com/modelcontextprotocol/servers)
- [MCPorter](https://github.com/steipete/mcporter) —— 用於呼叫 MCP 伺服器、免樣板程式碼的 TypeScript 執行期環境與 CLI
- [用 MCP 執行程式碼](https://www.anthropic.com/engineering/code-execution-with-mcp) —— Anthropic 工程部落格談解決上下文膨脹的問題
- [Claude Code CLI 參考](https://code.claude.com/docs/en/cli-reference)
- [Claude API 文件](https://docs.anthropic.com)

---

**最後更新**：2026 年 9 月 6 日
**Claude Code 版本**：2.1.263
**資料來源**：
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/managed-mcp
- https://code.claude.com/docs/en/changelog
- https://github.com/anthropics/claude-code/releases/tag/v2.1.117
- https://github.com/anthropics/claude-code/releases/tag/v2.1.139
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/en/model-config
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
