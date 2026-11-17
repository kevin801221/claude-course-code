# MCP 伺服器建構者 —— 上下文工程用例 (MCP Server Builder - Context Engineering Use Case)

此用例演示了如何使用「**上下文工程 (Context Engineering)**」和「**PRP (產品需求提示) 流程**」來構建生產級的型別模型上下文協定 (Model Context Protocol, MCP) 伺服器。它為建立具備 GitHub OAuth 身分驗證、資料庫整合和 Cloudflare Workers 部署功能的 MCP 伺服器提供了一個經過驗證的範本和工作流。

> PRP 是「PRD + 精選的程式碼庫情報 + 代理人/執行指南」—— 這是 AI 在第一次嘗試時就可能交付生產級程式碼所需的最小可行資訊包。

## 🚀 快速開始

### 前提條件

- 已安裝 Node.js 和 npm。
- Cloudflare 帳戶 (免費層即可)。
- 用於 OAuth 的 GitHub 帳戶。
- PostgreSQL 資料庫 (本地或託管)。

### 步驟 1：設定您的專案

```bash
# 複製上下文工程儲存庫
git clone https://github.com/coleam00/Context-Engineering-Intro.git
cd Context-Engineering-Intro/use-cases/mcp-server

# 將範本複製到您的新專案目錄
python copy_template.py my-mcp-server-project

# 導航至您的新專案
cd my-mcp-server-project

# 安裝依賴項
npm install

# 全域安裝 Wrangler CLI
npm install -g wrangler

# 向 Cloudflare 進行驗證
wrangler login
```

**copy_template.py 的作用：**
- 複製除構建產物以外的所有範本檔案 (遵循 .gitignore)。
- 將 README.md 重新命名為 README_TEMPLATE.md (以便您可以建立自己的 README)。
- 包含所有原始碼、範例、測試和配置檔案。
- 保留完整的上下文工程設定。

## 🎯 您將學到什麼

此用例教導您如何：

- **使用 PRP 流程**系統地構建複雜的 MCP 伺服器。
- **利用專門的上下文工程**進行 MCP 開發。
- **遵循經過驗證的模式**，源自生產級 MCP 伺服器範本。
- **實作安全的身分驗證**，結合 GitHub OAuth 和基於角色的存取。
- **部署到 Cloudflare Workers**，並具備監控和錯誤處理功能。

## 📋 運作方式 —— MCP 伺服器的 PRP 流程

> **步驟 1 是上述的快速開始設定** —— 克隆儲存庫、複製範本、安裝依賴項、設定 Wrangler。

### 步驟 2：定義您的 MCP 伺服器

編輯 `PRPs/INITIAL.md` 來描述您的特定 MCP 伺服器需求：

```markdown
## FEATURE (功能)：
我們想要建立一個天氣 MCP 伺服器，提供即時天氣數據，
並具備快取和速率限制功能。

## ADDITIONAL FEATURES (額外功能)：
- 與 OpenWeatherMap API 整合
- 使用 Redis 快取以提升效能
- 針對每個使用者進行速率限制
- 歷史天氣數據存取
- 地點搜尋和自動完成

## OTHER CONSIDERATIONS (其他考量)：
- 外部服務的 API 金鑰管理
- API 失敗的正確錯誤處理
- 地點查詢的座標驗證
```

### 步驟 3：生成您的 PRP

使用專門的 MCP PRP 命令來建立全面的實作計畫：

```bash
/prp-mcp-create INITIAL.md
```

**此命令的作用：**
- 讀取您的功能請求。
- 研究現有的 MCP 程式碼庫模式。
- 研究身分驗證和資料庫整合模式。
- 在 `PRPs/your-server-name.md` 中建立完整的 PRP。
- 包含所有上下文、驗證迴圈和逐步任務。

> 在生成 PRP 後，務必驗證所有內容！在 PRP 框架下，您應該參與此流程以確保所有上下文的品質。執行的效果取決於您的 PRP 質量。請使用 `/prp-mcp-create` 作為堅實的起點。

### 步驟 4：執行您的 PRP

使用專門的 MCP 執行命令來構建您的伺服器：

```bash
/prp-mcp-execute PRPs/your-server-name.md
```

**此命令的作用：**
- 載入包含所有上下文的完整 PRP。
- 使用 `TodoWrite` 建立詳細的實作計畫。
- 遵循經過驗證的模式實作每個組件。
- 執行全面的驗證 (TypeScript, 測試, 部署)。
- 確保您的 MCP 伺服器端到端正常運作。

### 步驟 5：配置環境

```bash
# 建立環境檔案
cp .dev.vars.example .dev.vars

# 使用您的憑證編輯 .dev.vars
# - GitHub OAuth 應用程式憑證
# - 資料庫連線字串
# - Cookie 加密金鑰
```

### 步驟 6：測試與部署

```bash
# 本地測試
wrangler dev --config <您的 wrangler 配置 (.jsonc)>

# 使用 MCP 檢查器 (Inspector) 進行測試
npx @modelcontextprotocol/inspector@latest
# 連線至： http://localhost:8792/mcp

# 部署到生產環境
wrangler deploy
```

## 🏗️ MCP 特定的上下文工程

此用例包含了專為 MCP 伺服器開發設計的專門上下文工程組件：

### 專門的斜線命令

位於 `.claude/commands/`：

- **`/prp-mcp-create`** —— 專門為 MCP 伺服器生成 PRP。
- **`/prp-mcp-execute`** —— 執行具備全面驗證的 MCP PRP。

這些是根目錄中 `.claude/commands/` 通用命令的專門版本，針對 MCP 開發模式進行了調整。

### 專門的 PRP 範本

範本 `PRPs/templates/prp_mcp_base.md` 包括：

- 用於工具註冊和身分驗證的 **MCP 特定模式**。
- 用於部署的 **Cloudflare Workers 配置**。
- **GitHub OAuth 整合**模式。
- **資料庫安全**和 SQL 注入防護。
- 從 TypeScript 到生產環境的**全面驗證迴圈**。

### AI 說明文件

`PRPs/ai_docs/` 資料夾包含：

- **`mcp_patterns.md`** —— 核心 MCP 開發模式和安全實務。
- **`claude_api_usage.md`** —— 如何整合 Anthropic 的 API 以實現由 LLM 驅動的功能。

## 🔧 範本架構

此範本提供了一個完整的、生產級的 MCP 伺服器，具備：

### 核心組件

```
src/
├── index.ts                 # 主要的已認證 MCP 伺服器
├── index_sentry.ts         # 具備 Sentry 監控的版本
├── simple-math.ts          # 基本的 MCP 範例 (無認證)
├── github-handler.ts       # 完整的 GitHub OAuth 實作
├── database.ts             # 具備安全模式的 PostgreSQL
├── utils.ts                # OAuth 輔助工具和公用程式
├── workers-oauth-utils.ts  # HMAC 簽名的 Cookie 系統
└── tools/                  # 模組化工具註冊系統
    └── register-tools.ts   # 中央工具註冊處
```

### 範例工具

`examples/` 資料夾展示了如何建立 MCP 工具：

- **`database-tools.ts`** —— 具備正確模式的資料庫工具範例。
- **`database-tools-sentry.ts`** —— 具備 Sentry 監控的相同工具。

### 關鍵特點

- **🔐 GitHub OAuth** —— 具備基於角色存取的完整驗證流程。
- **🗄️ 資料庫整合** —— 具備連線池和安全性的 PostgreSQL。
- **🛠️ 模組化工具** —— 透過中央註冊實現清晰的關注點分離。
- **☁️ Cloudflare Workers** —— 使用 Durable Objects 進行全球邊緣部署。
- **📊 監控** —— 用於生產環境的可選 Sentry 整合。
- **🧪 測試** —— 從 TypeScript 到部署的全面驗證。

## 🔍 需要理解的關鍵檔案

要充分理解此用例，請檢視以下檔案：

### 上下文工程組件

- **`PRPs/templates/prp_mcp_base.md`** —— 專門的 MCP PRP 範本。
- **`.claude/commands/prp-mcp-create.md`** —— MCP 特定的 PRP 生成。
- **`.claude/commands/prp-mcp-execute.md`** —— MCP 特定的執行。

### 實作模式

- **`src/index.ts`** —— 具備身分驗證的完整 MCP 伺服器。
- **`examples/database-tools.ts`** —— 工具建立和註冊模式。
- **`src/tools/register-tools.ts`** —— 模組化工具註冊系統。

### 配置與部署

- **`wrangler.jsonc`** —— Cloudflare Workers 配置。
- **`.dev.vars.example`** —— 環境變數範本。
- **`CLAUDE.md`** —— 實作指引和模式。

## 📈 成功指標

當您成功使用此流程時，您將獲得：

- **快速實作** —— 透過極少的迭代快速擁有一個 MCP 伺服器。
- **生產就緒** —— 安全的身分驗證、監控和錯誤處理。
- **可擴展架構** —— 清晰的關注點分離和模組化設計。
- **全面測試** —— 從 TypeScript 到生產部署的驗證。

## 🤝 貢獻

此用例展示了上下文工程在複雜軟體開發中的強大力量。要改進它：

1. **新增新的 MCP 伺服器範例**以展示不同的模式。
2. **增強 PRP 範本**，提供更全面的上下文。
3. **改進驗證迴圈**，以實現更好的錯誤檢測。
4. **記錄邊緣情況**和常見陷阱。

目標是透過全面的上下文工程使 MCP 伺服器開發變得可預測且成功。

---

**準備好構建您的 MCP 伺服器了嗎？** 遵循上述完整流程：使用複製範本設定您的專案，配置您的環境，在 `PRPs/INITIAL.md` 中定義您的需求，然後生成並執行您的 PRP 以構建生產就緒的 MCP 伺服器。
