---
description: 對本程式碼庫進行全面驗證
---

# 驗證程式碼庫 (Validate Codebase)

> **針對 React + FastAPI + PostgreSQL 應用程式生成的驗證指令範例**

## 第一階段：Lint 檢查 (Linting)
!`cd frontend && npm run lint`
!`cd backend && ruff check src/`

## 第二階段：型別檢查 (Type Checking)
!`cd frontend && npx tsc --noEmit`
!`cd backend && mypy src/`

## 第三階段：風格檢查 (Style Checking)
!`cd frontend && npm run format:check`
!`cd backend && black --check src/`

## 第四階段：單元測試 (Unit Testing)
!`cd frontend && npm test -- --coverage`
!`cd backend && pytest tests/unit -v --cov=src`

## 第五階段：端到端測試 (End-to-End Testing)

### 設定 (Setup)
!`docker-compose up -d`
!`timeout 60 bash -c 'until curl -f http://localhost:8000/health; do sleep 2; done'`

### 前端 E2E (Playwright)
!`cd frontend && npx playwright test`

**測試項目：**
- 使用者註冊 → 電子郵件驗證 → 登入
- 建立項目 → 編輯項目 → 刪除項目
- 搜尋與過濾功能
- 錯誤處理與驗證
- 所有主要的使用者工作流

### 後端 E2E (API + 資料庫)

**測試所有 API 端點：**
!`curl -X POST http://localhost:8000/api/auth/register -d '{"email":"test@test.com","password":"Test123!"}'`
!`TOKEN=$(curl -X POST http://localhost:8000/api/auth/login -d '{"email":"test@test.com","password":"Test123!"}' | jq -r '.token')`
!`curl http://localhost:8000/api/items -H "Authorization: Bearer $TOKEN"`
!`curl -X POST http://localhost:8000/api/items -H "Authorization: Bearer $TOKEN" -d '{"name":"Test"}'`

**驗證資料庫：**
!`docker exec postgres psql -U user -d db -c "SELECT COUNT(*) FROM users;"`
!`docker exec postgres psql -U user -d db -c "SELECT * FROM items WHERE name='Test';"`

**測試錯誤處理：**
!`curl -w "%{http_code}" http://localhost:8000/api/items/invalid-id` # 應為 404
!`curl -w "%{http_code}" http://localhost:8000/api/admin -H "Authorization: Bearer $TOKEN"` # 應為 403

### 清理 (Cleanup)
!`docker-compose down -v`

## 總結 (Summary)
所有驗證皆已通過！準備好進行部署。
