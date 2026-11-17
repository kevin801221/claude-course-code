---
name: doc-generator
description: 從原始碼生成全面且準確的 API 文件。適用於建立或更新 API 文件、生成 OpenAPI 規範，或在使用者提到 API 文件、端點或說明時使用。
---

# API 文件生成 Skill

## 可生成內容

- OpenAPI / Swagger 規範
- API 端點文件
- SDK 使用範例
- 整合指南
- 錯誤碼參考
- 認證指南

## 文件結構

### 每個端點的寫法

````markdown
## GET /api/v1/users/:id

### 描述
簡要說明這個端點做什麼

### 引數

| 名稱 | 型別 | 必填 | 說明 |
|------|------|------|------|
| id | string | 是 | 使用者 ID |

### 響應

**200 成功**
```json
{
  "id": "usr_123",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**404 未找到**
```json
{
  "error": "USER_NOT_FOUND",
  "message": "User does not exist"
}
```

### 範例

**cURL**
```bash
curl -X GET "https://api.example.com/api/v1/users/usr_123" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**JavaScript**
```javascript
const user = await fetch('/api/v1/users/usr_123', {
  headers: { 'Authorization': 'Bearer token' }
}).then(r => r.json());
```

**Python**
```python
response = requests.get(
    'https://api.example.com/api/v1/users/usr_123',
    headers={'Authorization': 'Bearer token'}
)
user = response.json()
```
````
