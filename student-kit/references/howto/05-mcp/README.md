<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# MCP（Model Context Protocol）

## 概覽

MCP 是 Claude Code 訪問外部工具、服務和 API 的標準協議。你可以把 GitHub、資料庫、檔案系統、聊天系統等都接到 Claude 裡。

## MCP 架構

MCP 通常由三部分構成：

1. Claude Code
2. MCP server
3. 外部工具或資料來源

Claude 會透過 MCP 協議向 server 發起工具呼叫，並把結果帶回當前會話。

## MCP 生態

- GitHub 整合
- 資料庫整合
- 檔案系統整合
- 組織內部工具
- 第三方服務

## 安裝方式

### HTTP 傳輸（推薦）

```bash
# Basic HTTP connection

# HTTP with authentication header
```

### Stdio 傳輸（本地）

```bash
# Local Node.js server

# With environment variables
```

### SSE 傳輸（已棄用）

舊版本中可能仍能見到 SSE 方式，但新設定一般優先考慮 HTTP 或 stdio。

### WebSocket 傳輸

適用於需要實時雙向通訊的場景。

### Windows 說明

在 Windows 上設定本地 server 時，要注意 shell、環境變數和路徑寫法。

### OAuth 2.0 認證

對於支援 OAuth 的 MCP server，Claude 可以透過互動式流程或預設定憑據完成認證。

## MCP 設定流程

1. 確認你要接入的服務
2. 選擇 transport
3. 設定環境變數或認證
4. 在 Claude Code 中新增 server
5. 驗證工具是否可用

## MCP 工具搜尋

Claude 會根據當前上下文自動查詢可用工具。

## 動態工具更新

當 MCP server 增加或移除工具時，Claude 可以在執行時感知變化。

## MCP 提示補充（Elicitation）

有些 MCP server 會在需要使用者補充資訊時觸發 elicitation，Claude 再把問題轉給使用者。

## 工具描述與指令上限

每個 MCP 工具都應該有清晰的描述，幫助 Claude 選擇正確的工具。

## 把 MCP Prompts 暴露成 Slash Commands

```text
/mcp__<server-name>__<prompt-name> [arguments]
```

例如：

```bash
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug title" high
```

## Server 去重

如果多個設定都指向同一個 server，Claude 會盡量避免重複載入。

## 透過 `@` 提及使用 MCP 資源

你可以把某些資源當作引用物件，在 prompt 中直接提及。

## MCP 作用域

MCP 設定通常有不同作用域，例如專案級和使用者級。

### 使用專案作用域

適合把團隊共享的 server 設定寫進專案內。

## MCP 設定管理

### 新增 MCP server

```bash
# Add HTTP-based server

# Add local stdio server

# List all MCP servers

# Get details on specific server

# Remove an MCP server

# Reset project-specific approval choices

# Import from Claude Desktop
```

## 可用 MCP Server 表

你可以在設定中維護一張 server 清單，記錄用途、認證方式和安裝命令。

## 實戰範例

### 範例 1：GitHub MCP 設定

你可以用 GitHub MCP 做這些事：

- PR 管理
- Issue 管理
- 儲存庫資訊查詢
- commit 操作

### 環境變數展開

在設定中可以使用環境變數，讓同一份設定適配不同環境。

### 範例 2：資料庫 MCP

```bash
# Using MCP database tool:

# Results:
```

### 範例 3：多 MCP 工作流程

適合日常報告、跨系統同步和自動化文件生成。

### 範例 4：檔案系統 MCP 操作

可用於讀寫檔案、批次整理、生成報告或匯出結果。

## MCP vs Memory：決策矩陣

- **Memory**：適合長期規則、偏好和上下文
- **MCP**：適合實時工具訪問和外部資料

## 請求 / 響應模式

MCP 一般遵循：

1. Claude 發起請求
2. Server 處理
3. 返回結構化結果

## 環境變數

常見環境變數包括：

- API token
- 資料庫地址
- 服務埠
- 認證資訊

## Claude 作為 MCP Server（`claude mcp serve`）

```bash
# Start Claude Code as an MCP server on stdio
```

## 受管 MCP 設定（企業）

企業可透過受管設定統一分發 MCP 設定。

## 外掛提供的 MCP Servers

外掛可以把自己的 MCP server 一起打包分發。

## Subagent 作用域 MCP

某些 MCP 只允許特定 subagent 使用。

## MCP 輸出限制

如果輸出過大，可以限制 token 數或分頁獲取。

### 增大最大輸出

```bash
# Increase the max output to 50,000 tokens
```

## 用程式碼執行解決上下文膨脹

當重複把大量資料回傳給 Claude 會浪費 token 時，可以把 MCP 當作程式碼 API 來用，減少來回傳輸。

### 問題

- 兩個資訊源都在耗 token
- 大資料集不適合全量塞進上下文

### 方案

- 用 MCP 工具做實時查詢
- 只把必要結果傳給 Claude

#### 工作方式

Claude 透過工具呼叫從外部系統取回需要的資料，而不是把所有資料先寫進上下文。

### 好處

- 更少 token 浪費
- 更清晰的資料邊界
- 更適合大規模查詢

#### 範例：過濾大資料集

#### 範例：迴圈而不做 round-trip

### 取捨

- 實現複雜度更高
- 需要維護 server
- 但擴充套件性更好

### MCPorter：MCP 工具組合執行時

這是更高階的工具編排思路，可以把多個 MCP 工具串成一個流程。

## 最佳實踐

### 安全注意事項

#### 應該做的

- 只授權必要的工具
- 優先使用最小許可權
- 檢查輸出是否可信

#### 不要做的

- 不要把高風險 token 寫死在儲存庫裡
- 不要預設開放所有工具
- 不要忽視網路和認證風險

### 設定建議

- 給每個 server 寫清楚用途
- 用環境變數存認證資訊
- 把專案級設定版本化

### 效能建議

- 避免一次性拉回過多資料
- 優先做過濾和分頁
- 只返回 Claude 真正需要的結果

## 安裝說明

### 前置條件

- Claude Code
- 對應的 MCP server
- 必要的認證資訊

### 分步設定

1. 安裝 server
2. 設定環境變數
3. 新增到 Claude
4. 測試工具

### 特定服務的安裝

不同服務會有不同的安裝命令和認證方式。

## 故障排查

### 找不到 MCP Server

- 檢查是否安裝
- 檢查路徑
- 檢查設定是否正確

### 認證失敗

- 檢查環境變數是否設定
- 確認 token 許可權正確
- 重新匯出變數後再試

### 連線超時

- 檢查網路
- 檢查 server 是否可用

### MCP Server 崩潰

- 檢視 server 日誌
- 降低併發
- 簡化請求

## 相關概念

- [Memory 中文指南](../02-memory/README.md)
- [Subagents 中文參考](../04-subagents/README.md)
- [Plugins 中文指南](../07-plugins/README.md)

## 更多資源

- [根目錄中文指南](../README.md)
- [MCP 規範](https://modelcontextprotocol.io)
