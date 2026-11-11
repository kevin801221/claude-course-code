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

## 開發規範

### 程式碼風格
- 使用 Prettier 格式化
- 使用帶 airbnb 設定的 ESLint
- 最大行長度：100 字元
- 使用 2 空格縮排

### 命名規範
- **檔案**：kebab-case（`user-controller.js`）
- **類**：PascalCase（`UserService`）
- **函式 / 變數**：camelCase（`getUserById`）
- **常量**：UPPER_SNAKE_CASE（`API_BASE_URL`）
- **資料庫表**：snake_case（`user_accounts`）

### Git 工作流程
- 分支命名：`feature/description` 或 `fix/description`
- 提交資訊：遵循 conventional commits
- 合併前必須有 PR
- 所有 CI/CD 檢查都必須通過
- 至少需要 1 個 approval

### 測試要求
- 最低 80% 程式碼覆蓋率
- 所有關鍵路徑都必須有測試
- 單元測試使用 Jest
- E2E 測試使用 Cypress
- 測試檔名：`*.test.ts` 或 `*.spec.ts`

### API 規範
- 只允許 RESTful 端點
- 請求 / 響應都使用 JSON
- 正確使用 HTTP 狀態碼
- API 版本路徑：`/api/v1/`
- 所有端點都要帶範例文件

### 資料庫
- schema 變更使用 migrations
- 絕不硬編碼憑據
- 使用連線池
- 開發環境啟用查詢日誌
- 需要定期備份

### 部署
- 基於 Docker 的部署
- 使用 Kubernetes 編排
- 藍綠部署策略
- 失敗時自動回滾
- 部署前先執行資料庫遷移

## 常用命令

| 命令 | 作用 |
|---------|---------|
| `npm run dev` | 啟動開發伺服器 |
| `npm test` | 執行測試套件 |
| `npm run lint` | 檢查程式碼風格 |
| `npm run build` | 建置生產版本 |
| `npm run migrate` | 執行資料庫遷移 |

## 團隊聯絡人
- 技術負責人：Sarah Chen（@sarah.chen）
- 產品經理：Mike Johnson（@mike.j）
- 運維：Alex Kim（@alex.k）

## 已知問題與解決方案
- PostgreSQL 連線池在高峰期限制為 20
- 解決方法：實現查詢排隊
- Safari 14 對 async generator 的相容性有問題
- 解決方法：使用 Babel 轉譯器

## 關聯專案
- 分析儀表盤：`/projects/analytics`
- 移動端 App：`/projects/mobile`
- 管理後臺：`/projects/admin`
