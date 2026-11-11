# API 模組規範

本檔案是對根目錄 `CLAUDE.md` 的補充，作用於 `/src/api/` 下的所有內容。memory 檔案是拼接（concatenate）而不是覆蓋 — 根目錄 `CLAUDE.md` 依然生效，Claude Code 會在讀取、寫入或編輯該子目錄下的檔案時按需載入本檔案。

## API 專屬規範

### 請求校驗
- 使用 Zod 做 schema 校驗
- 始終校驗輸入
- 校驗失敗時返回 400
- 提供欄位級別的錯誤詳情

### 認證
- 所有端點都需要 JWT token
- token 放在 `Authorization` header 中
- token 24 小時後過期
- 實現 refresh token 機制

### 響應格式

所有響應都必須遵循下面的結構：

```json
{
  "success": true,
  "data": { /* 實際資料 */ },
  "timestamp": "2025-11-06T10:30:00Z",
  "version": "1.0"
}
```

錯誤響應：

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "使用者可讀訊息",
    "details": { /* 欄位錯誤 */ }
  },
  "timestamp": "2025-11-06T10:30:00Z"
}
```

### 分頁
- 使用基於 cursor 的分頁，而不是 offset
- 包含 `hasMore` 布林值
- 單頁最大數量限制為 100
- 預設頁大小：20

### 限流
- 已認證使用者每小時 1000 次請求
- 公開端點每小時 100 次請求
- 超出時返回 429
- 包含 `retry-after` header

### 快取
- 使用 Redis 做會話快取
- 快取時長預設 5 分鐘
- 寫操作時失效快取
- 用資源型別給快取鍵打標籤

---

**最後更新**: 2026 年 10 月 10 日
**Claude Code 版本**: 2.1.296
**來源**:
- https://code.claude.com/docs/en/memory
- https://github.com/anthropics/claude-code/releases/tag/v2.1.288
- https://github.com/anthropics/claude-code/releases/tag/v2.1.293
