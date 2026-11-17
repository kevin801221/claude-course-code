# 函式：`functionName`

## 說明
簡短說明此函式的用途。

## 簽章
```typescript
function functionName(param1: Type1, param2: Type2): ReturnType
```

## 參數

| 參數 | 型別 | 是否必填 | 說明 |
|-----------|------|----------|-------------|
| param1 | Type1 | 是 | param1 的說明 |
| param2 | Type2 | 否 | param2 的說明 |

## 回傳值
**型別**：`ReturnType`

說明回傳的內容。

## 拋出例外
- `Error`：提供無效輸入時
- `TypeError`：傳入錯誤型別時

## 範例

### 基本用法
```typescript
const result = functionName('value1', 'value2');
console.log(result);
```

### 進階用法
```typescript
const result = functionName(
  complexParam1,
  { option: true }
);
```

## 備註
- 其他備註或注意事項
- 效能考量
- 最佳實踐

## 另請參閱
- [相關函式](#)
- [API 文件](#)

---

**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/plugins
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
