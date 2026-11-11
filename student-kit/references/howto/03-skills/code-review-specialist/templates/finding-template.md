# 程式碼審查問題記錄模板

使用這個模板來記錄程式碼審查中發現的每一個問題。

---

## 問題：[標題]

### 嚴重性
- [ ] Critical（阻塞釋出）
- [ ] High（合併前應修復）
- [ ] Medium（儘快修復）
- [ ] Low（可選最佳化）

### 類別
- [ ] Security
- [ ] Performance
- [ ] Code Quality
- [ ] Maintainability
- [ ] Testing
- [ ] Design Pattern
- [ ] Documentation

### 位置
**檔案：** `src/components/UserCard.tsx`

**行號：** 45-52

**函式 / 方法：** `renderUserDetails()`

### 問題描述

**是什麼：** 描述這個問題是什麼。

**為什麼重要：** 說明影響，以及為什麼需要修復。

**當前行為：** 展示有問題的程式碼或行為。

**期望行為：** 描述理想情況下應該發生什麼。

### 程式碼範例

#### 當前（有問題）

```typescript
// 這裡展示了 N+1 查詢問題
const users = fetchUsers();
users.forEach(user => {
  const posts = fetchUserPosts(user.id); // 每個使用者都發一次查詢！
  renderUserPosts(posts);
});
```

#### 建議修復

```typescript
// 使用 JOIN 查詢進行最佳化
const usersWithPosts = fetchUsersWithPosts();
usersWithPosts.forEach(({ user, posts }) => {
  renderUserPosts(posts);
});
```

### 影響分析

| 方面 | 影響 | 嚴重性 |
|--------|--------|--------|
| 效能 | 20 個使用者就會產生 100+ 次查詢 | High |
| 使用者體驗 | 頁面載入緩慢 | High |
| 可擴充套件性 | 規模變大後會失效 | Critical |
| 可維護性 | 難以排查問題 | Medium |

### 相關問題

- `AdminUserList.tsx` 第 120 行有類似問題
- 相關 PR：#456
- 相關 issue：#789

### 額外資源

- [N+1 Query Problem](https://en.wikipedia.org/wiki/N%2B1_problem)
- [Database Join Documentation](https://docs.example.com/joins)

### 審查者備註

- 這是這個程式碼庫裡常見的模式
- 可以考慮把它加入程式碼風格指南
- 也許值得提取一個輔助函式

### 作者回復（供回饋）

*由程式碼作者填寫：*

- [ ] 已在提交 `abc123` 中修復
- [ ] 修復狀態：Complete / In Progress / Needs Discussion
- [ ] 問題或疑慮：（描述）

---

## 統計資訊（供審查者使用）

在審查多個問題時，請記錄：

- **發現問題總數：** X
- **Critical：** X
- **High：** X
- **Medium：** X
- **Low：** X

**建議：** ✅ Approve / ⚠️ Request Changes / 🔄 Needs Discussion

**整體程式碼品質：** 1-5 星
