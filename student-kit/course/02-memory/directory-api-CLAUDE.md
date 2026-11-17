# API 模組標準

此檔案是根目錄 CLAUDE.md 在 /src/api/ 底下所有內容的補充。記憶（Memory）檔案是串接而非覆蓋——根目錄的 CLAUDE.md 仍然適用，Claude Code 會在讀取這個子目錄下的檔案時，依需要載入這份檔案。

## API 專屬標準

### 請求驗證
- 使用 Zod 做結構描述驗證（schema validation）
- 一律驗證輸入內容
- 驗證失敗時回傳 400 與驗證錯誤
- 附上欄位層級的錯誤細節

### 身分驗證
- 所有端點都需要 JWT token
- Token 放在 Authorization 標頭
- Token 在 24 小時後過期
- 實作 refresh token 機制

### 回應格式

所有回應都必須遵循以下結構：

```json
{
  "success": true,
  "data": { /* 實際資料 */ },
  "timestamp": "2025-11-06T10:30:00Z",
  "version": "1.0"
}
```

錯誤回應：
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "使用者訊息",
    "details": { /* 欄位錯誤 */ }
  },
  "timestamp": "2025-11-06T10:30:00Z"
}
```

### 分頁
- 使用以游標（cursor）為基礎的分頁（而非 offset）
- 附上 `hasMore` 布林值
- 單頁最大筆數限制為 100
- 預設單頁筆數：20

### 速率限制
- 已驗證使用者每小時 1000 次請求
- 公開端點每小時 100 次請求
- 超過限制時回傳 429
- 附上 retry-after 標頭

### 快取
- 使用 Redis 做工作階段（session）快取
- 快取時間：預設 5 分鐘
- 寫入操作時使該快取失效
- 用資源類型標記快取鍵值

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/memory
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
