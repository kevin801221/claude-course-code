# [方法] /api/v1/[endpoint]

## 描述
簡要說明這個端點的作用。

## 身份驗證
所需的身份驗證方式，例如 Bearer token。

## 引數

### 路徑引數
| 名稱 | 型別 | 必填 | 描述 |
|------|------|------|------|
| id | string | 是 | 資源 ID |

### 查詢引數
| 名稱 | 型別 | 必填 | 描述 |
|------|------|------|------|
| page | integer | 否 | 頁碼（預設：1） |
| limit | integer | 否 | 每頁條數（預設：20） |

### 請求體
```json
{
  "field": "value"
}
```

## 響應

### 200 OK
```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "範例"
  }
}
```

### 400 Bad Request
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "無效輸入"
  }
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "資源未找到"
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

## 限流
- 已認證使用者每小時 1000 次請求
- 公開端點每小時 100 次請求

## 相關端點
- [GET /api/v1/related](#)
- [POST /api/v1/related](#)
