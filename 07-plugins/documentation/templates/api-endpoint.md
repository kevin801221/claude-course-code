# [METHOD] /api/v1/[endpoint]

## 說明
簡短說明此端點的用途。

## 身分驗證
所需的身分驗證方式（例如 Bearer token）。

## 參數

### 路徑參數
| 名稱 | 型別 | 是否必填 | 說明 |
|------|------|----------|-------------|
| id | string | 是 | 資源 ID |

### 查詢參數
| 名稱 | 型別 | 是否必填 | 說明 |
|------|------|----------|-------------|
| page | integer | 否 | 頁碼（預設值：1） |
| limit | integer | 否 | 每頁項目數（預設值：20） |

### 請求主體
```json
{
  "field": "value"
}
```

## 回應

### 200 OK
```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "Example"
  }
}
```

### 400 Bad Request
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input"
  }
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

## 範例

### cURL
```bash
curl -X GET "https://api.example.com/api/v1/endpoint" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### JavaScript
```javascript
const response = await fetch('/api/v1/endpoint', {
  headers: {
    'Authorization': 'Bearer token',
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
```

### Python
```python
import requests

response = requests.get(
    'https://api.example.com/api/v1/endpoint',
    headers={'Authorization': 'Bearer token'}
)
data = response.json()
```

## 速率限制
- 已驗證使用者：每小時 1000 次請求
- 公開端點：每小時 100 次請求

## 相關端點
- [GET /api/v1/related](#)
- [POST /api/v1/related](#)

---

**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/plugins
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
