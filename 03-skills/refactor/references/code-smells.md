# 程式碼異味目錄

這是根據 Martin Fowler 的《Refactoring》（第 2 版）整理的完整程式碼異味參考。程式碼異味是更深層問題的徵兆——它們代表你的程式碼設計可能有問題。

> 「程式碼異味是一種表面徵兆，通常對應著系統中更深層的問題。」——Martin Fowler

---

## 膨脹型（Bloaters）

代表某樣東西長得太大、難以有效處理的程式碼異味。

### 過長方法（Long Method）

**徵兆：**
- 方法超過 30-50 行
- 需要捲動才能看完整個方法
- 多層巢狀結構
- 用註解說明各段落在做什麼

**為什麼不好：**
- 難以理解
- 難以獨立測試
- 修改容易產生非預期的後果
- 內部藏著重複邏輯

**對應重構手法：**
- 提取方法（Extract Method）
- 以查詢取代暫存變數（Replace Temp with Query）
- 引入參數物件（Introduce Parameter Object）
- 以方法物件取代方法（Replace Method with Method Object）
- 分解條件式（Decompose Conditional）

**範例（修改前）：**
```javascript
function processOrder(order) {
  // 驗證訂單（20 行）
  if (!order.items) throw new Error('No items');
  if (order.items.length === 0) throw new Error('Empty order');
  // ...更多驗證

  // 計算總計（30 行）
  let subtotal = 0;
  for (const item of order.items) {
    subtotal += item.price * item.quantity;
  }
  // ...稅金、運費、折扣

  // 發送通知（20 行）
  // ...寄信邏輯
}
```

**範例（修改後）：**
```javascript
function processOrder(order) {
  validateOrder(order);
  const totals = calculateOrderTotals(order);
  sendOrderNotifications(order, totals);
  return { order, totals };
}
```

---

### 過大類別（Large Class）

**徵兆：**
- 類別有很多實例變數（超過 7-10 個）
- 類別有很多方法（超過 15-20 個）
- 類別名稱含糊不清（例如 Manager、Handler、Processor）
- 方法沒有用到所有的實例變數

**為什麼不好：**
- 違反單一職責原則
- 難以測試
- 修改會擴散影響到不相關的功能
- 難以重複使用其中的部分

**對應重構手法：**
- 提取類別（Extract Class）
- 提取子類別（Extract Subclass）
- 提取介面（Extract Interface）

**偵測方式：**
```
程式碼行數 > 300
方法數量 > 15
欄位數量 > 10
```

---

### 基本型別偏執（Primitive Obsession）

**徵兆：**
- 用基本型別表示領域概念（用字串表示 email、用整數表示金額）
- 用基本型別陣列取代物件
- 用字串常數表示型別碼
- 魔術數字／魔術字串

**為什麼不好：**
- 型別層級沒有驗證
- 邏輯散落在整個程式碼庫
- 容易傳入錯誤的值
- 缺少領域概念

**對應重構手法：**
- 以物件取代基本型別（Replace Primitive with Object）
- 以類別取代型別碼（Replace Type Code with Class）
- 以子類別取代型別碼（Replace Type Code with Subclasses）
- 以 State/Strategy 取代型別碼（Replace Type Code with State/Strategy）

**範例（修改前）：**
```javascript
const user = {
  email: 'john@example.com',     // 只是個字串
  phone: '1234567890',           // 只是個字串
  status: 'active',              // 魔術字串
  balance: 10050                 // 用整數表示的分（cents）
};
```

**範例（修改後）：**
```javascript
const user = {
  email: new Email('john@example.com'),
  phone: new PhoneNumber('1234567890'),
  status: UserStatus.ACTIVE,
  balance: Money.cents(10050)
};
```

---

### 過長參數列（Long Parameter List）

**徵兆：**
- 方法有 4 個以上的參數
- 總是一起出現的參數
- 布林旗標改變方法行為
- 常常傳入 null／undefined

**為什麼不好：**
- 難以正確呼叫
- 參數順序容易搞混
- 代表方法做的事情太多
- 難以新增參數

**對應重構手法：**
- 引入參數物件（Introduce Parameter Object）
- 保留完整物件（Preserve Whole Object）
- 以方法呼叫取代參數（Replace Parameter with Method Call）
- 移除旗標引數（Remove Flag Argument）

**範例（修改前）：**
```javascript
function createUser(firstName, lastName, email, phone,
                    street, city, state, zip,
                    isAdmin, isActive, createdBy) {
  // ...
}
```

**範例（修改後）：**
```javascript
function createUser(personalInfo, address, options) {
  // personalInfo: { firstName, lastName, email, phone }
  // address: { street, city, state, zip }
  // options: { isAdmin, isActive, createdBy }
}
```

---

### 資料泥團（Data Clumps）

**徵兆：**
- 同樣的 3 個以上欄位一再一起出現
- 總是一起傳遞的參數
- 類別裡有應該歸在一起的欄位子集

**為什麼不好：**
- 重複的處理邏輯
- 缺少抽象
- 難以擴充
- 代表隱藏了一個類別

**對應重構手法：**
- 提取類別（Extract Class）
- 引入參數物件（Introduce Parameter Object）
- 保留完整物件（Preserve Whole Object）

**範例：**
```javascript
// 資料泥團：(x, y, z) 座標
function movePoint(x, y, z, dx, dy, dz) { }
function scalePoint(x, y, z, factor) { }
function distanceBetween(x1, y1, z1, x2, y2, z2) { }

// 提取 Point3D 類別
class Point3D {
  constructor(x, y, z) { }
  move(delta) { }
  scale(factor) { }
  distanceTo(other) { }
}
```

---

## 物件導向濫用（Object-Orientation Abusers）

代表不完整或錯誤運用物件導向原則的異味。

### Switch 陳述式（Switch Statements）

**徵兆：**
- 很長的 switch/case 或 if/else 鏈
- 同樣的 switch 出現在多個地方
- 針對型別碼做 switch
- 新增一個 case 就要到處修改

**為什麼不好：**
- 違反開放封閉原則
- 修改會擴散到所有 switch 出現的地方
- 難以擴充
- 通常代表缺少多型

**對應重構手法：**
- 以多型取代條件式（Replace Conditional with Polymorphism）
- 以子類別取代型別碼（Replace Type Code with Subclasses）
- 以 State/Strategy 取代型別碼（Replace Type Code with State/Strategy）

**範例（修改前）：**
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

**範例（修改後）：**
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

### 暫時欄位（Temporary Field）

**徵兆：**
- 實例變數只在部分方法中用到
- 欄位是有條件才設定的
- 特定情況需要複雜的初始化

**為什麼不好：**
- 令人困惑——欄位存在卻可能是 null
- 難以理解物件狀態
- 代表藏著條件邏輯

**對應重構手法：**
- 提取類別（Extract Class）
- 引入 Null 物件（Introduce Null Object）
- 以區域變數取代暫存欄位（Replace Temp Field with Local）

---

### 拒絕遺贈（Refused Bequest）

**徵兆：**
- 子類別沒有用到繼承來的方法／資料
- 子類別覆寫方法卻不做任何事
- 繼承只是為了重複使用程式碼，而不是 IS-A 關係

**為什麼不好：**
- 抽象方式錯誤
- 違反里氏替換原則
- 誤導性的階層結構

**對應重構手法：**
- 下移方法／欄位（Push Down Method/Field）
- 以委派取代子類別（Replace Subclass with Delegate）
- 以委派取代繼承（Replace Inheritance with Delegation）

---

### 異曲同工的類別（Alternative Classes with Different Interfaces）

**徵兆：**
- 兩個類別做類似的事
- 同一個概念用不同的方法名稱
- 可以互換使用

**為什麼不好：**
- 重複的實作
- 沒有共同介面
- 難以互相切換

**對應重構手法：**
- 重新命名方法（Rename Method）
- 搬移方法（Move Method）
- 提取父類別（Extract Superclass）
- 提取介面（Extract Interface）

---

## 修改阻礙者（Change Preventers）

讓修改變得困難的異味——改一個東西就要跟著改一堆其他東西。

### 發散式變化（Divergent Change）

**徵兆：**
- 一個類別因為多種不同原因而被修改
- 不同領域的變化都會觸發同一個類別的修改
- 類別成了「上帝類別」

**為什麼不好：**
- 違反單一職責原則
- 修改頻率高
- 容易產生合併衝突

**對應重構手法：**
- 提取類別（Extract Class）
- 提取父類別（Extract Superclass）
- 提取子類別（Extract Subclass）

**範例：**
`User` 類別因為以下原因而修改：
- 身分驗證邏輯變動
- 個人資料變動
- 帳務邏輯變動
- 通知邏輯變動

→ 提取出：`AuthService`、`ProfileService`、`BillingService`、`NotificationService`

---

### 霰彈式修改（Shotgun Surgery）

**徵兆：**
- 一個修改需要編輯很多個類別
- 一個小功能需要動到 10 個以上的檔案
- 修改分散各處，難以找齊

**為什麼不好：**
- 容易漏掉某個地方
- 高度耦合
- 修改容易出錯

**對應重構手法：**
- 搬移方法（Move Method）
- 搬移欄位（Move Field）
- 內聯類別（Inline Class）

**偵測方式：**
留意：新增一個欄位需要修改 5 個以上的檔案。

---

### 平行繼承體系（Parallel Inheritance Hierarchies）

**徵兆：**
- 在一個繼承體系新增子類別，就要在另一個繼承體系也新增子類別
- 類別名稱前綴相符（例如 `DatabaseOrder`、`DatabaseProduct`）

**為什麼不好：**
- 維護成本加倍
- 兩個繼承體系互相耦合
- 容易漏掉其中一邊

**對應重構手法：**
- 搬移方法（Move Method）
- 搬移欄位（Move Field）
- 消除其中一個繼承體系

---

## 冗餘元素（Dispensables）

不必要、應該移除的東西。

### 過多的註解（Excessive Comments）

**徵兆：**
- 用註解解釋程式碼在做什麼
- 被註解掉的程式碼
- 永遠停留在那裡的 TODO/FIXME
- 註解裡的道歉

**為什麼不好：**
- 註解會說謊（跟程式碼脫節）
- 程式碼本身應該要能自我說明
- 死程式碼造成困惑

**對應重構手法：**
- 提取方法（好名字自己會說明用途）
- 重新命名（不靠註解也能清楚表達）
- 移除被註解掉的程式碼
- 引入斷言（Introduce Assertion）

**好與壞的註解對比：**
```javascript
// 不好：解釋「做了什麼」
// 遍歷使用者並檢查是否啟用
for (const user of users) {
  if (user.status === 'active') { }
}

// 好：解釋「為什麼」
// 只取啟用中的使用者——停用的由清理工作處理
const activeUsers = users.filter(u => u.isActive);
```

---

### 重複程式碼（Duplicate Code）

**徵兆：**
- 同樣的程式碼出現在多個地方
- 有些微差異的類似程式碼
- 複製貼上的痕跡

**為什麼不好：**
- 修 bug 要改很多地方
- 有不一致的風險
- 程式碼庫變得臃腫

**對應重構手法：**
- 提取方法（Extract Method）
- 提取類別（Extract Class）
- 上移方法（Pull Up Method，用於繼承體系中）
- 塑造模板方法（Form Template Method）

**偵測規則：**
任何重複 3 次以上的程式碼都應該被提取出來。

---

### 冗贅類別（Lazy Class）

**徵兆：**
- 類別做的事情不足以撐起它存在的理由
- 沒有附加價值的包裝
- 過度設計的產物

**為什麼不好：**
- 維護成本
- 不必要的間接層
- 增加複雜度卻沒有好處

**對應重構手法：**
- 內聯類別（Inline Class）
- 折疊繼承體系（Collapse Hierarchy）

---

### 無用程式碼（Dead Code）

**徵兆：**
- 永遠不會執行到的程式碼
- 沒用到的變數／方法／類別
- 被註解掉的程式碼
- 藏在不可能成立的條件後面的程式碼

**為什麼不好：**
- 造成困惑
- 增加維護負擔
- 拖慢理解速度

**對應重構手法：**
- 移除無用程式碼（Remove Dead Code）
- 安全刪除（Safe Delete）

**偵測方式：**
```bash
# 找出未使用的匯出
# 找出沒被參照的函式
# IDE 顯示的「unused」警告
```

---

### 投機性泛化（Speculative Generality）

**徵兆：**
- 只有一個子類別的抽象類別
- 「為了未來使用」而留著的未用參數
- 只做轉呼叫的方法
- 只為了一個使用情境而做的「框架」

**為什麼不好：**
- 增加複雜度卻沒有好處
- 違反 YAGNI（You Ain't Gonna Need It，你不會需要它）
- 更難理解

**對應重構手法：**
- 折疊繼承體系（Collapse Hierarchy）
- 內聯類別（Inline Class）
- 移除參數（Remove Parameter）
- 重新命名方法（Rename Method）

---

## 過度耦合（Couplers）

代表類別之間耦合過度的異味。

### 依戀情結（Feature Envy）

**徵兆：**
- 方法用到另一個類別的資料，比用自己的資料還多
- 對另一個物件呼叫了很多 getter
- 資料與行為被分開

**為什麼不好：**
- 行為放錯了位置
- 封裝性差
- 難以維護

**對應重構手法：**
- 搬移方法（Move Method）
- 搬移欄位（Move Field）
- 提取方法（Extract Method，之後搬移）

**範例（修改前）：**
```javascript
class Order {
  getDiscountedPrice(customer) {
    // 大量使用 customer 的資料
    if (customer.loyaltyYears > 5) {
      return this.price * customer.discountRate;
    }
    return this.price;
  }
}
```

**範例（修改後）：**
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

### 過度親密（Inappropriate Intimacy）

**徵兆：**
- 類別互相存取對方的私有部分
- 雙向參照
- 子類別對父類別知道太多

**為什麼不好：**
- 高度耦合
- 修改會連鎖擴散
- 難以只修改其中一個而不動到另一個

**對應重構手法：**
- 搬移方法（Move Method）
- 搬移欄位（Move Field）
- 將雙向關聯改為單向關聯（Change Bidirectional to Unidirectional）
- 提取類別（Extract Class）
- 隱藏委派（Hide Delegate）

---

### 訊息鏈（Message Chains）

**徵兆：**
- 一長串的方法呼叫：`a.getB().getC().getD().getValue()`
- 呼叫端依賴著導覽結構
- 「連環車禍」式的程式碼

**為什麼不好：**
- 很脆弱——任何一個環節改變都會斷掉整條鏈
- 違反迪米特法則
- 耦合到內部結構

**對應重構手法：**
- 隱藏委派（Hide Delegate）
- 提取方法（Extract Method）
- 搬移方法（Move Method）

**範例：**
```javascript
// 不好：訊息鏈
const managerName = employee.getDepartment().getManager().getName();

// 更好：隱藏委派
const managerName = employee.getManagerName();
```

---

### 中間人（Middle Man）

**徵兆：**
- 類別只是把工作轉呼叫給另一個類別
- 有一半的方法都是轉呼叫
- 沒有附加價值

**為什麼不好：**
- 不必要的間接層
- 維護成本
- 架構令人困惑

**對應重構手法：**
- 移除中介者（Remove Middle Man）
- 內聯方法（Inline Method）

---

## 異味嚴重程度指南

| 嚴重程度 | 說明 | 處理方式 |
|----------|------|----------|
| **嚴重** | 阻礙開發、導致錯誤 | 立即修正 |
| **高** | 造成顯著維護負擔 | 在目前的 sprint 中修正 |
| **中** | 明顯但可控管 | 排入近期計畫 |
| **低** | 輕微不便 | 有機會就順手修正 |

---

## 快速偵測檢查清單

掃描程式碼時可以用這份檢查清單：

- [ ] 有沒有方法超過 30 行？
- [ ] 有沒有類別超過 300 行？
- [ ] 有沒有方法的參數超過 4 個？
- [ ] 有沒有重複的程式碼區塊？
- [ ] 有沒有針對型別碼做的 switch/case？
- [ ] 有沒有沒用到的程式碼？
- [ ] 有沒有方法大量使用另一個類別的資料？
- [ ] 有沒有很長的方法呼叫鏈？
- [ ] 有沒有註解在解釋「做了什麼」而不是「為什麼」？
- [ ] 有沒有應該用物件表示、卻用了基本型別的地方？

---

## 延伸閱讀

- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.)
- Kerievsky, J. (2004). *Refactoring to Patterns*
- Feathers, M. (2004). *Working Effectively with Legacy Code*

---

**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/skills
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
