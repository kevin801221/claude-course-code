# 專案設定

## 專案總覽
- **名稱**：電商平台
- **技術堆疊**：Node.js、PostgreSQL、React 18、Docker
- **團隊規模**：5 位開發者
- **截止日期**：2025 年第 4 季

## 架構
@docs/architecture.md
@docs/api-standards.md
@docs/database-schema.md

## 開發標準

### 程式碼風格
- 使用 Prettier 做格式化
- 使用 ESLint，搭配 airbnb 設定
- 每行最多 100 字元
- 使用 2 個空格縮排

### 命名慣例
- **檔案**：kebab-case（user-controller.js）
- **類別**：PascalCase（UserService）
- **函式 / 變數**：camelCase（getUserById）
- **常數**：UPPER_SNAKE_CASE（API_BASE_URL）
- **資料庫資料表**：snake_case（user_accounts）

### Git 工作流程
- 分支命名：`feature/description` 或 `fix/description`
- 提交訊息：遵循 conventional commits
- 合併前需要 PR
- 所有 CI/CD 檢查都必須通過
- 至少需要 1 個人核准

### 測試需求
- 最低 80% 程式碼涵蓋率
- 所有關鍵路徑都必須有測試
- 單元測試使用 Jest
- E2E 測試使用 Cypress
- 測試檔名：`*.test.ts` 或 `*.spec.ts`

### API 標準
- 只使用 RESTful 端點
- JSON 格式的請求 / 回應
- 正確使用 HTTP 狀態碼
- 為 API 端點加上版本號：`/api/v1/`
- 每個端點都要附上範例文件

### 資料庫
- 用 migration 處理 schema 變更
- 絕不寫死憑證
- 使用連線池
- 開發環境啟用查詢日誌
- 需要定期備份

### 部署
- 以 Docker 為基礎的部署
- Kubernetes 協調
- 藍綠部署策略
- 失敗時自動回滾
- 部署前先執行資料庫遷移

## 常用指令

| 指令 | 用途 |
|---------|---------|
| `npm run dev` | 啟動開發伺服器 |
| `npm test` | 執行測試套件 |
| `npm run lint` | 檢查程式碼風格 |
| `npm run build` | 建置生產版本 |
| `npm run migrate` | 執行資料庫遷移 |

## 團隊聯絡人
- 技術主管：Sarah Chen（@sarah.chen）
- 產品經理：Mike Johnson (@mike.j)
- DevOps：Alex Kim (@alex.k)

## 已知問題與因應方式
- PostgreSQL 連線池在尖峰時段限制為 20 個連線
- 因應方式：實作查詢佇列
- Safari 14 對 async generator 有相容性問題
- 因應方式：使用 Babel 轉譯

## 相關專案
- 分析儀表板：`/projects/analytics`
- 行動應用：`/projects/mobile`
- 管理後台：`/projects/admin`

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/memory
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
