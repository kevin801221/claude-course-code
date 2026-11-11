# 程式碼異味目錄

這是基於 Martin Fowler《Refactoring》（第 2 版）的程式碼異味參考目錄。程式碼異味是更深層問題的表面症狀，它們說明程式碼設計可能出了問題。

> “程式碼異味通常是系統中更深層問題的表面訊號。” — Martin Fowler

---

## 過度膨脹類異味

表示物件或函式已經大到不再好用。

### 長函式

**跡象：**
- 函式超過 30-50 行
- 需要滾動才能看完整個函式
- 巢狀層級很多
- 需要註解來解釋區域性邏輯

**為什麼不好：**
- 難理解
- 難單獨測試
- 改動容易波及其他邏輯
- 重複邏輯容易藏在裡面

**可用重構：**
- Extract Method
- Replace Temp with Query
- Introduce Parameter Object
- Replace Method with Method Object
- Decompose Conditional

**範例（重構前）：**
```javascript
function processOrder(order) {
  // Validate order (20 lines)
  if (!order.items) throw new Error('No items');
  if (order.items.length === 0) throw new Error('Empty order');
  // ... more validation

  // Calculate totals (30 lines)
  let subtotal = 0;
  for (const item of order.items) {
    subtotal += item.price * item.quantity;
  }
  // ... tax, shipping, discounts

  // Send notifications (20 lines)
  // ... email logic
}
```

**範例（重構後）：**
```javascript
function processOrder(order) {
  validateOrder(order);
  const totals = calculateOrderTotals(order);
  sendOrderNotifications(order, totals);
  return { order, totals };
}
```

---

### 大類

**跡象：**
- 例項變數很多（>7-10）
- 方法很多（>15-20）
- 類名含糊（Manager、Handler、Processor）
- 方法沒有用到全部欄位

**為什麼不好：**
- 違反單一職責原則
- 難測試
- 改動會波及無關功能
- 難以複用區域性能力

**可用重構：**
- Extract Class
- Extract Subclass
- Extract Interface

**檢測參考：**
```text
程式碼行數 > 300
方法數量 > 15
欄位數量 > 10
```

---

### 基礎型別沉迷

**跡象：**
- 用基礎型別表達領域概念（用 string 表示郵箱、用 int 表示金額）
- 使用基礎型別陣列，而不是物件
- 用字串常量表示型別碼
- 大量 magic number / magic string

**為什麼不好：**
- 型別層面沒有驗證
- 邏輯散落在整個程式碼庫裡
- 容易傳錯值
- 缺少領域物件

**可用重構：**
- Replace Primitive with Object
- Replace Type Code with Class
- Replace Type Code with Subclasses
- Replace Type Code with State/Strategy

**範例（重構前）：**
```javascript
const user = {
  email: 'john@example.com',     // 只是字串
  phone: '1234567890',           // 只是字串
  status: 'active',              // 魔法字串
  balance: 10050                 // 以分為單位的整數
};
```

**範例（重構後）：**
```javascript
const user = {
  email: new Email('john@example.com'),
  phone: new PhoneNumber('1234567890'),
  status: UserStatus.ACTIVE,
  balance: Money.cents(10050)
};
```

---

### 長引數列表

**跡象：**
- 方法引數超過 4 個
- 一些引數總是一起出現
- 布林引數改變方法行為
- 經常傳 null / undefined

**為什麼不好：**
- 難正確呼叫
- 引數順序容易搞混
- 暗示方法做了太多事
- 難以增加新引數

**可用重構：**
- Introduce Parameter Object
- Preserve Whole Object
- Replace Parameter with Method Call
- Remove Flag Argument

**範例（重構前）：**
```javascript
function createUser(firstName, lastName, email, phone,
                    street, city, state, zip,
                    isAdmin, isActive, createdBy) {
  // ...
}
```

**範例（重構後）：**
```javascript
function createUser(personalInfo, address, options) {
  // personalInfo: { firstName, lastName, email, phone }
  // address: { street, city, state, zip }
  // options: { isAdmin, isActive, createdBy }
}
```

---

### 資料泥團

**跡象：**
- 同樣的 3 個以上欄位反覆一起出現
- 引數總是成對或成組傳遞
- 類中的欄位子集總是一起使用

**為什麼不好：**
- 邏輯重複
- 缺少抽象
- 難擴充套件
- 暗示隱藏的類應該存在

**可用重構：**
- Extract Class
- Introduce Parameter Object
- Preserve Whole Object

**範例：**
```javascript
// 資料泥團：座標 (x, y, z)
function movePoint(x, y, z, dx, dy, dz) { }
function scalePoint(x, y, z, factor) { }
function distanceBetween(x1, y1, z1, x2, y2, z2) { }

// 提取 Point3D 類
class Point3D {
  constructor(x, y, z) { }
  move(delta) { }
  scale(factor) { }
  distanceTo(other) { }
}
```

---

## 物件導向濫用類異味

表示 OOP 原則沒有被正確使用。

### switch 語句

**跡象：**
- 長 switch/case 或 if/else 鏈
- 多處出現相同 switch
- 按型別碼分支
- 新增 case 時需要改很多地方

**為什麼不好：**
- 違反開放 / 封閉原則
- 改動會擴散到所有 switch 位置
- 難擴充套件
- 往往說明缺少多型

**可用重構：**
- Replace Conditional with Polymorphism
- Replace Type Code with Subclasses
- Replace Type Code with State/Strategy

**範例（重構前）：**
```javascript
function calculatePay(employee) {
  switch (employee.type) {
    case 'hourly':
      return employee.hours * employee.rate;
    case 'salaried':
      return employee.salary / 12;
    case 'commissioned':
      return employee.sales * employee.commission;
  }
}
```

**範例（重構後）：**
```javascript
class HourlyEmployee {
  calculatePay() {
    return this.hours * this.rate;
  }
}

class SalariedEmployee {
  calculatePay() {
    return this.salary / 12;
  }
}
```

---

### 臨時欄位

**跡象：**
- 例項變數只在部分方法中使用
- 欄位只在某些條件下設定
- 某些情況初始化過程很複雜

**為什麼不好：**
- 容易混淆：欄位存在但可能為 null
- 物件狀態難理解
- 說明條件邏輯被隱藏了

**可用重構：**
- Extract Class
- Introduce Null Object
- Replace Temp Field with Local

---

### 拒絕遺贈

**跡象：**
- 子類沒有用到繼承來的方法 / 資料
- 子類重寫方法只是為了不做事
- 繼承被當成程式碼複用，而不是真正的 IS-A

**為什麼不好：**
- 抽象不對
- 違反里氏替換原則
- 繼承層次誤導人

**可用重構：**
- Push Down Method / Field
- Replace Subclass with Delegate
- Replace Inheritance with Delegation

---

### 不同介面的相似類

**跡象：**
- 兩個類做的事情差不多
- 同一個概念卻用了不同方法名
- 理論上可以互換使用

**為什麼不好：**
- 重複實現
- 沒有公共介面
- 難切換

**可用重構：**
- Rename Method
- Move Method
- Extract Superclass
- Extract Interface

---

## 變更阻礙類異味

這類異味會讓改動變得困難，一次改動需要波及很多地方。

### 發散式變化

**跡象：**
- 一個類因為很多不同原因而被修改
- 不同區域的變更都會觸發同一個類的編輯
- 類變成了“上帝類”

**為什麼不好：**
- 違反單一職責原則
- 變更頻率高
- 容易產生合併衝突

**可用重構：**
- Extract Class
- Extract Superclass
- Extract Subclass

**範例：**
一個 `User` 類同時因為這些原因變化：
- 身份驗證變化
- 個人資料變化
- 計費變化
- 通知變化

→ 可以拆成：`AuthService`、`ProfileService`、`BillingService`、`NotificationService`

---

### 散彈式修改

**跡象：**
- 一個改動需要編輯很多類
- 一個小功能要觸碰 10+ 個檔案
- 改動分散，難以一次找全

**為什麼不好：**
- 很容易漏改
- 耦合高
- 容易出錯

**可用重構：**
- Move Method
- Move Field
- Inline Class

**檢測參考：**
如果新增一個欄位需要改 5 個以上檔案，就要警惕。

---

### 平行繼承體系

**跡象：**
- 在一個繼承體系中建立子類，另一個體系也得跟著建立
- 類字首相似（如 `DatabaseOrder`、`DatabaseProduct`）

**為什麼不好：**
- 維護成本翻倍
- 兩個層次之間耦合
- 容易漏掉一邊

**可用重構：**
- Move Method
- Move Field
- 消除其中一個層次

---

## 可捨棄類異味

表示有些東西已經不必要了，應該移除。

### 註解過多

**跡象：**
- 註解在解釋程式碼“做了什麼”
- 註解掉的程式碼
- 長期存在的 TODO / FIXME
- 註解裡帶道歉語氣

**為什麼不好：**
- 註解會過時
- 程式碼本身應該能自解釋
- 死程式碼會造成混亂

**可用重構：**
- Extract Method（讓方法名解釋意圖）
- Rename（透過命名提升清晰度）
- 刪除註解掉的程式碼
- Introduce Assertion

**好與壞的註解：**
```javascript
// BAD: 解釋做了什麼
// 遍歷使用者並檢查是否活躍
for (const user of users) {
  if (user.status === 'active') { }
}

// GOOD: 解釋為什麼
// 只保留活躍使用者，未活躍使用者由清理任務處理
const activeUsers = users.filter(u => u.isActive);
```

---

### 重複程式碼

**跡象：**
- 多處出現相同程式碼
- 只有少量差異的相似程式碼
- 複製貼上模式

**為什麼不好：**
- 修復要改多處
- 容易不一致
- 程式碼庫臃腫

**可用重構：**
- Extract Method
- Extract Class
- Pull Up Method（在繼承層次中）
- Form Template Method

**檢測規則：**
任何重複 3 次以上的程式碼都應該考慮提取。

---

### 惰性類

**跡象：**
- 類做的事情不足以支撐它的存在
- 只是一個沒有增值的包裝器
- 過度設計的產物

**為什麼不好：**
- 增加維護開銷
- 多了一層沒必要的間接
- 有複雜度但沒收益

**可用重構：**
- Inline Class
- Collapse Hierarchy

---

### 死程式碼

**跡象：**
- 無法到達的程式碼
- 未使用的變數 / 方法 / 類
- 註解掉的程式碼
- 位於不可能條件分支後的程式碼

**為什麼不好：**
- 造成困惑
- 增加維護負擔
- 降低理解速度

**可用重構：**
- Remove Dead Code
- Safe Delete

**檢測：**
```bash
# 查詢未使用的匯出
# 查詢未引用的函式
# IDE 的“unused”警告
```

---

### 臆想泛化

**跡象：**
- 只有一個子類的抽象類
- 為“未來可能需要”而加的未使用引數
- 只是轉發的函式
- 為一個用例設計的“框架”

**為什麼不好：**
- 複雜度沒有收益
- 違背 YAGNI
- 更難理解

**可用重構：**
- Collapse Hierarchy
- Inline Class
- Remove Parameter
- Rename Method

---

## 耦合類異味

表示類之間耦合過強。

### Feature Envy

**跡象：**
- 一個方法使用別的類的資料比自己更多
- 對另一個物件呼叫很多 getter
- 資料和行為分離

**為什麼不好：**
- 行為放錯地方了
- 封裝性差
- 難維護

**可用重構：**
- Move Method
- Move Field
- Extract Method（然後移動）

**範例（重構前）：**
```javascript
class Order {
  getDiscountedPrice(customer) {
    // 這裡大量使用 customer 資料
    if (customer.loyaltyYears > 5) {
      return this.price * customer.discountRate;
    }
    return this.price;
  }
}
```

**範例（重構後）：**
```javascript
class Customer {
  getDiscountedPriceFor(price) {
    if (this.loyaltyYears > 5) {
      return price * this.discountRate;
    }
    return price;
  }
}
```

---

### 不恰當的親密

**跡象：**
- 類之間互相訪問私有細節
- 雙向引用很多
- 子類知道父類太多細節

**為什麼不好：**
- 耦合高
- 改一邊會連帶另一邊
- 難單獨修改

**可用重構：**
- Move Method
- Move Field
- Change Bidirectional to Unidirectional
- Extract Class
- Hide Delegate

---

### 訊息鏈

**跡象：**
- 方法呼叫鏈很長：`a.getB().getC().getD().getValue()`
- 用戶端依賴導航結構
- “火車殘骸”式程式碼

**為什麼不好：**
- 很脆弱，任何一層變動都會壞
- 違反迪米特法則
- 繫結到物件結構

**可用重構：**
- Hide Delegate
- Extract Method
- Move Method

**範例：**
```javascript
// 差：訊息鏈
const managerName = employee.getDepartment().getManager().getName();

// 更好：隱藏委派
const managerName = employee.getManagerName();
```

---

### 中間人

**跡象：**
- 類只是把呼叫轉發給另一個類
- 一半以上的方法都是委派
- 沒有額外價值

**為什麼不好：**
- 多了一層沒必要的間接
- 維護成本更高
- 架構令人困惑

**可用重構：**
- Remove Middle Man
- Inline Method

---

## 嚴重性指南

| 嚴重性 | 說明 | 處理方式 |
|--------|------|---------|
| **Critical** | 阻塞開發，導致 bug | 立刻修復 |
| **High** | 明顯增加維護負擔 | 本迭代修復 |
| **Medium** | 有問題但還能接受 | 近期計劃修復 |
| **Low** | 小問題 | 視情況順手修 |

---

## 快速檢測清單

掃描程式碼時使用這個清單：

- [ ] 有沒有超過 30 行的函式？
- [ ] 有沒有超過 300 行的類？
- [ ] 有沒有引數超過 4 個的函式？
- [ ] 有沒有重複程式碼區塊？
- [ ] 有沒有按型別碼分支的 switch/case？
- [ ] 有沒有未使用的程式碼？
- [ ] 有沒有大量使用其他類資料的方法？
- [ ] 有沒有很長的方法呼叫鏈？
- [ ] 有沒有解釋“是什麼”而不是“為什麼”的註解？
- [ ] 有沒有應該封裝成物件的基礎型別？

---

## 延伸閱讀

- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.)
- Kerievsky, J. (2004). *Refactoring to Patterns*
- Feathers, M. (2004). *Working Effectively with Legacy Code*
