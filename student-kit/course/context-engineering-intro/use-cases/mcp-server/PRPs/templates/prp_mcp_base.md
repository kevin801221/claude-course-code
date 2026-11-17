---
name: "MCP 伺服器 PRP 範本 (MCP Server PRP Template)"
description: 此範本旨在利用本程式碼庫中經過驗證的模式，提供一個生產就緒的模型上下文協定 (Model Context Protocol, MCP) 伺服器。
---

## 目的 (Purpose)

針對 AI 代理人優化的範本，用於實作具備 GitHub OAuth 身分驗證、資料庫整合和 Cloudflare Workers 部署功能的生產級模型上下文協定 (MCP) 伺服器，並使用本程式碼庫中經過驗證的模式。

## 核心原則 (Core Principles)

1. **上下文至上 (Context is King)**：包含所有必要的 MCP 模式、身分驗證流程和部署配置。
2. **驗證迴圈 (Validation Loops)**：提供從 TypeScript 編譯到生產部署的可執行測試。
3. **安全性優先 (Security First)**：內建身分驗證、授權和 SQL 注入防護。
4. **生產就緒 (Production Ready)**：包含監控、錯誤處理和部署自動化。

---

## 目標 (Goal)

構建一個生產級的 MCP (模型上下文協定) 伺服器，具備：

- [具體 MCP 功能] —— 描述要實作的特定工具和資源。
- 具備角色型存取控制 (RBAC) 的 GitHub OAuth 身分驗證。
- 具備監控功能的 Cloudflare Workers 部署。
- [額外功能] —— 基礎身分驗證/資料庫之外的任何特定功能。

## 為什麼 (Why)

- **開發人員效率**：讓 AI 助手能安全地存取 [特定數據/操作]。
- **企業級安全**：具備細粒度權限系統的 GitHub OAuth。
- **可擴展性**：Cloudflare Workers 全球邊緣部署。
- **整合**：[這如何與現有系統配合]。
- **使用者價值**：[對終端使用者的具體好處]。

## 內容 (What)

### MCP 伺服器特點

**核心 MCP 工具：**

- 工具被組織在模組化檔案中，並透過 `src/tools/register-tools.ts` 進行註冊。
- 每個功能/領域都有自己的工具註冊檔案 (例如 `database-tools.ts`, `analytics-tools.ts`)。
- [列出特定工具] —— 例如 "queryDatabase", "listTables", "executeOperations"。
- 使用者身分驗證與權限驗證在工具註冊期間進行。
- 全面的錯誤處理與記錄。
- [領域特定工具] —— 針對您的用例的特定工具。

**身分驗證與授權：**

- 具備已簽署 Cookie 核准系統的 GitHub OAuth 2.0 整合。
- 角色型存取控制 (唯讀 vs 特權使用者)。
- 使用者上下文傳播至所有 MCP 工具。
- 使用 HMAC 簽署 Cookie 的安全對話 (Session) 管理。

**資料庫整合：**

- 具備自動清理功能的 PostgreSQL 連線池。
- SQL 注入防護與查詢驗證。
- 根據使用者權限分離讀取/寫入操作。
- 錯誤清理以防止資訊外洩。

**部署與監控：**

- 使用 Durable Objects 進行狀態管理的 Cloudflare Workers。
- 選用的 Sentry 整合，用於錯誤追蹤與效能監控。
- 基於環境的配置 (開發 vs 生產)。
- 即時記錄與告警。

### 成功準則 (Success Criteria)

- [ ] MCP 伺服器通過 MCP Inspector 的驗證。
- [ ] GitHub OAuth 流程端到端運作正常 (授權 → 回呼 → MCP 存取)。
- [ ] TypeScript 編譯成功且無錯誤。
- [ ] 本地開發伺服器啟動並正確回應。
- [ ] 成功部署到 Cloudflare Workers。
- [ ] 身分驗證可防止未經授權存取敏感操作。
- [ ] 錯誤處理提供友善的使用者訊息，且不洩露系統細節。
- [ ] [領域特定成功準則]。

## 所有需要的上下文 (All Needed Context)

### 說明文件與參考資料 (必讀)

```yaml
# 關鍵 MCP 模式 —— 請先閱讀這些
- docfile: PRPs/ai_docs/mcp_patterns.md
  why: 核心 MCP 開發模式、安全實務與錯誤處理

# 關鍵程式碼範例
- docfile: PRPs/ai_docs/claude_api_usage.md
  why: 如何使用 Anthropic API 從 LLM 獲取回應

# 工具註冊系統 —— 了解模組化方法
- file: src/tools/register-tools.ts
  why: 中央註冊處，展示所有工具如何匯入與註冊 —— 學習此模式

# 範例 MCP 工具 —— 查看此處以了解如何建立與註冊新工具
- file: examples/database-tools.ts
  why: Postgres MCP 伺服器的範例工具，展示工具建立與註冊的最佳實踐

- file: examples/database-tools-sentry.ts
  why: 同樣是 Postgres MCP 伺服器範例，但包含生產監控的 Sentry 整合

# 現有程式碼庫模式 —— 學習這些實作
- file: src/index.ts
  why: 具備身分驗證、資料庫與工具的完整 MCP 伺服器 —— 鏡像此模式

- file: src/github-handler.ts
  why: OAuth 流程實作 —— 務必使用此確切模式進行身分驗證

- file: src/database.ts
  why: 資料庫安全、連線池、SQL 驗證 —— 遵循這些模式

- file: wrangler.jsonc
  why: Cloudflare Workers 配置 —— 複製此模式進行部署

# 官方 MCP 說明文件
- url: https://modelcontextprotocol.io/docs/concepts/tools
  why: MCP 工具註冊與 Schema 定義模式

- url: https://modelcontextprotocol.io/docs/concepts/resources
  why: 如果需要，實作 MCP 資源 (Resources)

# 根據需要新增與使用者用例相關的文件如下
```

### 目前程式碼庫樹狀圖 (在專案根目錄執行 `tree -I node_modules`)

```bash
# 在此處插入實際的 TREE 輸出
/
├── src/
│   ├── index.ts                 # 主要的已認證 MCP 伺服器 ← 學習此檔案
│   ├── index_sentry.ts         # Sentry 監控版本
│   ├── simple-math.ts          # 基礎 MCP 範例 ← 良好的起點
│   ├── github-handler.ts       # OAuth 實作 ← 使用此模式
│   ├── database.ts             # 資料庫公用程式 ← 安全模式
│   ├── utils.ts                # OAuth 輔助工具
│   ├── workers-oauth-utils.ts  # Cookie 安全系統
│   └── tools/                  # 工具註冊系統
│       └── register-tools.ts   # 中央工具註冊處 ← 理解此檔案
├── PRPs/
│   ├── templates/prp_mcp_base.md  # 本範本
│   └── ai_docs/                   # 實作指南 ← 全部閱讀
├── examples/                   # 範例工具實作
│   ├── database-tools.ts       # 資料庫工具範例 ← 遵循模式
│   └── database-tools-sentry.ts # 具備 Sentry 監控
├── wrangler.jsonc              # Cloudflare 配置 ← 複製模式
├── package.json                # 依賴項
└── tsconfig.json               # TypeScript 配置
```

### 期望的程式碼庫樹狀圖 (視使用者用例需要新增/修改檔案)

```bash

```

### 已知陷阱與關鍵 MCP/Cloudflare 模式

```typescript
// 重要：Cloudflare Workers 要求特定模式
// 1. 務必為 Durable Objects 實作清理 (Cleanup)
export class YourMCP extends McpAgent<Env, Record<string, never>, Props> {
  async cleanup(): Promise<void> {
    await closeDb(); // 重要：關閉資料庫連線
  }

  async alarm(): Promise<void> {
    await this.cleanup(); // 重要：處理 Durable Object 警報
  }
}

// 2. 務必驗證 SQL 以防止注入 (使用現有模式)
const validation = validateSqlQuery(sql); // 來自 src/database.ts
if (!validation.isValid) {
  return createErrorResponse(validation.error);
}

// 3. 務必在執行敏感操作前檢查權限
const ALLOWED_USERNAMES = new Set(["admin1", "admin2"]);
if (!ALLOWED_USERNAMES.has(this.props.login)) {
  return createErrorResponse("權限不足");
}

// 4. 務必使用 withDatabase 包裝器進行連線管理
return await withDatabase(this.env.DATABASE_URL, async (db) => {
  // 在此進行資料庫操作
});

// 5. 務必使用 Zod 進行輸入驗證
import { z } from "zod";
const schema = z.object({
  param: z.string().min(1).max(100),
});

// 6. TypeScript 編譯要求介面完全匹配
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // 在此處新增您的環境變數
}
```

## 實作藍圖 (Implementation Blueprint)

### 資料模型與型別

定義 TypeScript 介面與 Zod Schemas 以確保型別安全與驗證。

```typescript
// 使用者身分驗證屬性 (繼承自 OAuth)
type Props = {
  login: string; // GitHub 使用者名稱
  name: string; // 顯示名稱
  email: string; // 電子郵件地址
  accessToken: string; // GitHub 存取權杖
};

// MCP 工具輸入 Schemas (根據您的工具自訂)
const YourToolSchema = z.object({
  param1: z.string().min(1, "參數不可為空"),
  param2: z.number().int().positive().optional(),
  options: z.object({}).optional(),
});

// 環境介面 (新增您的變數)
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // YOUR_SPECIFIC_ENV_VAR: string;
}

// 權限等級 (根據您的用例自訂)
enum Permission {
  READ = "read",
  WRITE = "write",
  ADMIN = "admin",
}
```

### 任務列表 (請依序完成)

```yaml
任務 1 —— 專案設定：
  將 wrangler.jsonc 複製為 wrangler-[伺服器名稱].jsonc：
    - 將 name 欄位修改為 "[伺服器名稱]"
    - 在 vars 章節新增任何新的環境變數
    - 保留現有的 OAuth 與資料庫配置

  建立 .dev.vars 檔案 (如果不存在)：
    - 新增 GITHUB_CLIENT_ID=您的用戶端ID
    - 新增 GITHUB_CLIENT_SECRET=您的用戶端密鑰
    - 新增 DATABASE_URL=postgresql://...
    - 新增 COOKIE_ENCRYPTION_KEY=您的32位元金鑰
    - 新增任何領域特定的環境變數

任務 2 —— GitHub OAuth 應用程式：
  建立新的 GitHub OAuth 應用程式：
    - 設定 Homepage URL: https://您的Worker.workers.dev
    - 設定 Callback URL: https://您的Worker.workers.dev/callback
    - 將 Client ID 與 Secret 複製到 .dev.vars

  或者重用現有的 OAuth 應用程式：
    - 如果使用不同子網域，請更新 Callback URL
    - 驗證環境中的 Client ID 與 Secret

任務 3 —— MCP 伺服器實作：
  建立 src/[伺服器名稱].ts 或修改 src/index.ts：
    - 複製 src/index.ts 的類別結構
    - 在 McpServer 建構函式中修改伺服器名稱與版本
    - 在 init() 方法中呼叫 registerAllTools(server, env, props)
    - 保持身分驗證與資料庫模式完全一致

  建立工具模組：
    - 遵循 examples/database-tools.ts 模式建立新的工具檔案
    - 導出接受 (server, env, props) 的註冊函式
    - 使用 Zod Schemas 進行輸入驗證
    - 使用 createErrorResponse 實作正確的錯誤處理
    - 在工具註冊期間新增權限檢查

  更新工具註冊表：
    - 修改 src/tools/register-tools.ts 以匯入您的新工具
    - 在 registerAllTools() 中新增您的註冊函式呼叫

任務 4 —— 資料庫整合 (如果需要)：
  使用來自 src/database.ts 的現有資料庫模式：
    - 匯入 withDatabase, validateSqlQuery, isWriteOperation
    - 實作具備安全驗證的資料庫操作
    - 根據使用者權限分離讀取與寫入操作
    - 使用 formatDatabaseError 顯示友善的錯誤訊息

任務 5 —— 環境配置：
  設定 Cloudflare KV 命名空間：
    - 執行： wrangler kv namespace create "OAUTH_KV"
    - 將回傳的命名空間 ID 更新至 wrangler.jsonc

  設定生產環境機密 (Secrets)：
    - 執行： wrangler secret put GITHUB_CLIENT_ID
    - 執行： wrangler secret put GITHUB_CLIENT_SECRET
    - 執行： wrangler secret put DATABASE_URL
    - 執行： wrangler secret put COOKIE_ENCRYPTION_KEY

任務 6 —— 本地測試：
  測試基本功能：
    - 執行： wrangler dev
    - 驗證伺服器啟動無誤
    - 測試 OAuth 流程： http://localhost:8792/authorize
    - 驗證 MCP 端點： http://localhost:8792/mcp

任務 7 —— 生產部署：
  部署到 Cloudflare Workers：
    - 執行： wrangler deploy
    - 驗證部署成功
    - 測試生產環境 OAuth 流程
    - 驗證 MCP 端點的可存取性
```

### 各項任務實作細節

```typescript
// 任務 3 —— MCP 伺服器實作模式
export class YourMCP extends McpAgent<Env, Record<string, never>, Props> {
  server = new McpServer({
    name: "您的 MCP 伺服器名稱",
    version: "1.0.0",
  });

  // 重要：務必實作清理
  async cleanup(): Promise<void> {
    try {
      await closeDb();
      console.log("資料庫連線已成功關閉");
    } catch (error) {
      console.error("資料庫清理期間發生錯誤：", error);
    }
  }

  async alarm(): Promise<void> {
    await this.cleanup();
  }

  async init() {
    // 模式：使用集中式工具註冊
    registerAllTools(this.server, this.env, this.props);
  }
}

// 任務 3 —— 工具模組模式 (例如 src/tools/your-feature-tools.ts)
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Props } from "../types";
import { z } from "zod";

const PRIVILEGED_USERS = new Set(["admin1", "admin2"]);

export function registerYourFeatureTools(server: McpServer, env: Env, props: Props) {
  // 工具 1：對所有已驗證使用者可用
  server.tool(
    "yourBasicTool",
    "您的基礎工具描述",
    YourToolSchema, // Zod 驗證 Schema
    async ({ param1, param2, options }) => {
      try {
        // 模式：具備錯誤處理的工具實作
        const result = await performOperation(param1, param2, options);

        return {
          content: [
            {
              type: "text",
              text: `**成功**\n\n操作已完成\n\n**結果：**\n\`\`\`json\n${JSON.stringify(result, null, 2)}\n\`\`\``,
            },
          ],
        };
      } catch (error) {
        return createErrorResponse(`操作失敗：${error.message}`);
      }
    },
  );

  // 工具 2：僅對特權使用者可用
  if (PRIVILEGED_USERS.has(props.login)) {
    server.tool(
      "privilegedTool",
      "供特權使用者使用的管理工具",
      { action: z.string() },
      async ({ action }) => {
        // 實作內容
        return {
          content: [
            {
              type: "text",
              text: `管理員動作 '${action}' 已由 ${props.login} 執行`,
            },
          ],
        };
      },
    );
  }
}

// 任務 3 —— 更新工具註冊表 (src/tools/register-tools.ts)
import { registerYourFeatureTools } from "./your-feature-tools";

export function registerAllTools(server: McpServer, env: Env, props: Props) {
  // 現有的註冊
  registerDatabaseTools(server, env, props);
  
  // 新增您的註冊
  registerYourFeatureTools(server, env, props);
}

// 模式：導出具備 MCP 端點的 OAuth 提供者
export default new OAuthProvider({
  apiHandlers: {
    "/sse": YourMCP.serveSSE("/sse") as any,
    "/mcp": YourMCP.serve("/mcp") as any,
  },
  authorizeEndpoint: "/authorize",
  clientRegistrationEndpoint: "/register",
  defaultHandler: GitHubHandler as any,
  tokenEndpoint: "/token",
});
```

### 整合點 (Integration Points)

```yaml
CLOUDFLARE_WORKERS:
  - wrangler.jsonc：更新名稱、環境變數、KV 綁定
  - 環境機密 (Secrets)：GitHub OAuth 憑證、資料庫 URL、加密金鑰
  - Durable Objects：配置 MCP 代理人綁定以實現狀態持久化

GITHUB_OAUTH:
  - GitHub App：建立 Callback URL，需與您的 Workers 網域相匹配
  - 用戶端憑證：儲存為 Cloudflare Workers 機密
  - Callback URL：必須完全匹配： https://您的Worker.workers.dev/callback

DATABASE:
  - PostgreSQL 連線：使用現有的連線池模式
  - 環境變數：包含完整連線字串的 DATABASE_URL
  - 安全性：對所有 SQL 使用 validateSqlQuery 與 isWriteOperation

環境變數：
  - 開發環境：用於本地測試的 .dev.vars 檔案
  - 生產環境：用於部署的 Cloudflare Workers 機密
  - 必要項：GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, DATABASE_URL, COOKIE_ENCRYPTION_KEY

KV 存儲：
  - OAuth 狀態：由 OAuth 提供者用於狀態管理
  - 命名空間：使用 `wrangler kv namespace create "OAUTH_KV"` 建立
  - 配置：將命名空間 ID 新增至 wrangler.jsonc 綁定中
```

## 驗證關卡 (Validation Gate)

### 第一層：TypeScript 與配置

```bash
# 重要：請先執行這些 —— 在繼續之前修復任何錯誤
npm run type-check                 # TypeScript 編譯
wrangler types                     # 生成 Cloudflare Workers 型別

# 預期：無 TypeScript 錯誤
# 若有錯誤：修復型別問題、缺失的介面、匯入問題
```

### 第二層：本地開發測試

```bash
# 啟動本地開發伺服器
wrangler dev

# 測試 OAuth 流程 (應重新導向至 GitHub)
curl -v http://localhost:8792/authorize

# 測試 MCP 端點 (應回傳伺服器資訊)
curl -v http://localhost:8792/mcp

# 預期：伺服器啟動，OAuth 導向至 GitHub，MCP 回傳伺服器資訊
# 若有錯誤：檢查控制台輸出，驗證環境變數，修復配置
```

### 第三層：為每個功能、函式和檔案編寫單元測試，遵循現有的測試模式 (如有)。

```bash
npm run test
```

執行上述指令 (Vitest) 以確保所有功能運作正常。

### 第四層：資料庫整合測試 (如適用)

```bash
# 測試資料庫連線
curl -X POST http://localhost:8792/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "listTables", "arguments": {}}}'

# 測試權限驗證
# 測試 SQL 注入防護與其他安全性 (如適用)
# 測試資料庫失敗的錯誤處理

# 預期：資料庫操作正常，權限強制執行，錯誤處理優雅等
# 若有錯誤：檢查 DATABASE_URL, 連線設定, 權限邏輯
```

## 最終驗證檢查表 (Final Validation Checklist)

### 核心功能

- [ ] TypeScript 編譯： `npm run type-check` 通過。
- [ ] 單元測試： `npm run test` 通過。
- [ ] 本地伺服器啟動： `wrangler dev` 執行無誤。
- [ ] MCP 端點回應： `curl http://localhost:8792/mcp` 回傳伺服器資訊。
- [ ] OAuth 流程正常：身分驗證重新導向並成功完成。

---

## 應避免的反模式 (Anti-Patterns to Avoid)

### MCP 特定

- ❌ 不要跳過 Zod 輸入驗證 —— 務必驗證工具參數。
- ❌ 不要忘記為 Durable Objects 實作 `cleanup()` 方法。
- ❌ 不要硬編碼使用者權限 —— 使用可配置的權限系統。

### 開發流程

- ❌ 不要跳過驗證迴圈 —— 每一層級都會捕捉不同的問題。
- ❌ 不要對 OAuth 配置胡亂猜測 —— 測試完整的流程。
- ❌ 不要未經監控就部署 —— 實作記錄與錯誤追蹤。
- ❌ 不要忽略 TypeScript 錯誤 —— 在部署前修復所有型別問題。
