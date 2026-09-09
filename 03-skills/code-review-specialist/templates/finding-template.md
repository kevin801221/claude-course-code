# 程式碼審查發現範本

記錄程式碼審查中發現的每個問題時，請使用這份範本。

---

## 問題：[標題]

### 嚴重程度
- [ ] Critical（阻擋部署）
- [ ] High（合併前應該修正）
- [ ] Medium（應該盡快修正）
- [ ] Low（有做更好）

### 類別
- [ ] 安全性
- [ ] 效能
- [ ] 程式碼品質
- [ ] 可維護性
- [ ] 測試
- [ ] 設計模式
- [ ] 文件

### 位置
**檔案：** `src/components/UserCard.tsx`

**行數：** 45-52

**函式／方法：** `renderUserDetails()`

### 問題說明

**是什麼**：描述問題是什麼。

**為什麼重要**：說明影響範圍，以及為什麼需要修正。

**目前行為**：呈現有問題的程式碼或行為。

**預期行為**：描述應該要發生什麼事。

### 程式碼範例

#### 目前（有問題）

```typescript
// 展示 N+1 查詢問題
const users = fetchUsers();
users.forEach(user => {
  const posts = fetchUserPosts(user.id); // 每個使用者都要查一次！
  renderUserPosts(posts);
});
```

#### 建議修正

```typescript
// 使用 JOIN 查詢最佳化
const usersWithPosts = fetchUsersWithPosts();
usersWithPosts.forEach(({ user, posts }) => {
  renderUserPosts(posts);
});
```

### 影響分析

| 面向 | 影響 | 嚴重程度 |
|--------|--------|----------|
| 效能 | 20 位使用者就要跑 100+ 次查詢 | High |
| 使用者體驗 | 頁面載入緩慢 | High |
| 擴充性 | 規模一大就會壞掉 | Critical |
| 可維護性 | 難以除錯 | Medium |

### 相關問題

- `AdminUserList.tsx` 第 120 行有類似問題
- 相關 PR：#456
- 相關 Issue：#789

### 延伸資源

- [N+1 查詢問題](https://en.wikipedia.org/wiki/N%2B1_problem)
- [資料庫 Join 文件](https://docs.example.com/joins)

### 審查者備註

- 這是這個程式碼庫中常見的模式
- 可以考慮把它加進程式碼風格指南
- 或許值得建立一個輔助函式

### 作者回覆（供回饋使用）

*由程式碼作者填寫：*

- [ ] 修正已於此提交實作：`abc123`
- [ ] 修正狀態：完成／進行中／需要討論
- [ ] 問題或疑慮：（描述）

---

## 發現統計（供審查者使用）

審查多個發現時，追蹤以下項目：

- **發現的問題總數：** X
- **Critical：** X
- **High：** X
- **Medium：** X
- **Low：** X

**建議：** ✅ 核准 / ⚠️ 要求修改 / 🔄 需要討論

**整體程式碼品質：** 1-5 顆星

---

**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/skills
**相容模型**：Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
