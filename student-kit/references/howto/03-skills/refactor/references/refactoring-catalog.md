# 重構目錄

這是 Martin Fowler《Refactoring》（第 2 版）中的一份精選重構目錄。每個重構都包含動機、操作步驟和範例。

> “重構由它的操作步驟來定義，也就是你執行這個變化時遵循的精確過程。” — Martin Fowler

---

## 如何使用這個目錄

1. **識別異味**：先用程式碼異味目錄定位問題
2. **找到對應重構**：在這裡查詢匹配的手法
3. **按步驟執行**：一步一步來
4. **每步都測試**：確保行為不變

**黃金法則**：如果某一步超過 10 分鐘，就把它拆得更小。

---

## 最常見的重構

### Extract Method

**何時使用**：長函式、重複程式碼、需要為概念命名

**動機**：把一段程式碼抽成一個名字能說明意圖的方法。

**步驟**：
1. 建立一個新方法，名字應描述“做什麼”而不是“怎麼做”
2. 把程式碼片段複製到新方法裡
3. 檢查片段裡用了哪些區域性變數
4. 把區域性變數作為引數傳入，或在方法內宣告
5. 正確處理返回值
6. 用新方法呼叫替換原始片段
7. 測試

**前：**
```javascript
function printOwing(invoice) {
  let outstanding = 0;

  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");

  // Calculate outstanding
  for (const order of invoice.orders) {
    outstanding += order.amount;
  }

  // Print details
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

**後：**
```javascript
function printOwing(invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice, outstanding);
}

function printBanner() {
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
}

function calculateOutstanding(invoice) {
  return invoice.orders.reduce((sum, order) => sum + order.amount, 0);
}

function printDetails(invoice, outstanding) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

---

### Inline Method

**何時使用**：方法體和名字一樣清楚，或者只是多餘轉發

**動機**：當方法沒有額外價值時，去掉不必要的間接層。

**步驟**：
1. 確認這個方法不是多型方法
2. 找到所有呼叫點
3. 用方法體替換每個呼叫
4. 每替換一次就測試一次
5. 刪除方法定義

**前：**
```javascript
function getRating(driver) {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}

function moreThanFiveLateDeliveries(driver) {
  return driver.numberOfLateDeliveries > 5;
}
```

**後：**
```javascript
function getRating(driver) {
  return driver.numberOfLateDeliveries > 5 ? 2 : 1;
}
```

---

### Extract Variable

**何時使用**：複雜表示式難以理解

**動機**：給複雜表示式的一部分起名字。

**步驟**：
1. 確保表示式沒有副作用
2. 宣告一個不可變變數
3. 將表示式結果賦給變數
4. 用變數替換原表示式
5. 測試

**前：**
```javascript
return order.quantity * order.itemPrice -
  Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
  Math.min(order.quantity * order.itemPrice * 0.1, 100);
```

**後：**
```javascript
const basePrice = order.quantity * order.itemPrice;
const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
const shipping = Math.min(basePrice * 0.1, 100);
return basePrice - quantityDiscount + shipping;
```

---

### Inline Variable

**何時使用**：變數名沒有比表示式更清楚

**動機**：移除沒必要的間接層。

**步驟**：
1. 檢查右側表示式沒有副作用
2. 如果變數不是不可變的，先改成不可變並測試
3. 找到第一次引用並替換成表示式
4. 測試
5. 對所有引用重複
6. 刪除變數宣告和賦值
7. 測試

---

### Rename Variable

**何時使用**：名字沒有清楚表達用途

**動機**：好名字是清晰程式碼的基礎。

**步驟**：
1. 如果變數使用範圍很廣，先考慮封裝
2. 找到所有引用
3. 逐個修改引用
4. 測試

**提示**：
- 使用能體現意圖的名字
- 避免縮寫
- 使用領域術語

```javascript
// Bad
const d = 30;
const x = users.filter(u => u.a);

// Good
const daysSinceLastLogin = 30;
const activeUsers = users.filter(user => user.isActive);
```

---

### Change Function Declaration

**何時使用**：函式名不能清楚說明用途，引數也需要變化

**動機**：好函式名能讓程式碼自解釋。

**步驟（簡單情況）**：
1. 刪除不需要的引數
2. 修改函式名
3. 新增需要的引數
4. 測試

**步驟（遷移式，適用於複雜改動）**：
1. 如果要刪除引數，確保它沒有被使用
2. 建立一個新函式，宣告符合新設計
3. 讓舊函式呼叫新函式
4. 測試
5. 讓呼叫方逐步改用新函式
6. 每改一個呼叫點就測試
7. 刪除舊函式

**前：**
```javascript
function circum(radius) {
  return 2 * Math.PI * radius;
}
```

**後：**
```javascript
function circumference(radius) {
  return 2 * Math.PI * radius;
}
```

---

### Encapsulate Variable

**何時使用**：多個地方直接訪問某個資料

**動機**：為資料訪問提供明確入口。

**步驟**：
1. 建立 getter 和 setter
2. 找到所有引用
3. 用 getter 替換讀取
4. 用 setter 替換寫入
5. 每次改動後測試
6. 降低變數可見性

**前：**
```javascript
let defaultOwner = { firstName: "Martin", lastName: "Fowler" };

// Used in many places
spaceship.owner = defaultOwner;
```

**後：**
```javascript
let defaultOwnerData = { firstName: "Martin", lastName: "Fowler" };

function defaultOwner() { return defaultOwnerData; }
function setDefaultOwner(arg) { defaultOwnerData = arg; }

spaceship.owner = defaultOwner();
```

---

### Introduce Parameter Object

**何時使用**：一組引數經常一起出現

**動機**：把自然屬於一起的資料打包起來。

**步驟**：
1. 為這組引數建立一個新類 / 結構
2. 測試
3. 用 Change Function Declaration 引入新物件
4. 測試
5. 逐個移除引數，改用物件欄位
6. 每次移除後測試

**前：**
```javascript
function amountInvoiced(startDate, endDate) { ... }
function amountReceived(startDate, endDate) { ... }
function amountOverdue(startDate, endDate) { ... }
```

**後：**
```javascript
class DateRange {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }
}

function amountInvoiced(dateRange) { ... }
function amountReceived(dateRange) { ... }
function amountOverdue(dateRange) { ... }
```

---

### Combine Functions into Class

**何時使用**：多個函式操作同一份資料

**動機**：把函式和它操作的資料放到一起。

**步驟**：
1. 對公共資料先做 Encapsulate Record
2. 把每個函式移動到類裡
3. 每移動一次就測試
4. 用類欄位替代資料引數

**前：**
```javascript
function base(reading) { ... }
function taxableCharge(reading) { ... }
function calculateBaseCharge(reading) { ... }
```

**後：**
```javascript
class Reading {
  constructor(data) { this._data = data; }

  get base() { ... }
  get taxableCharge() { ... }
  get calculateBaseCharge() { ... }
}
```

---

### Split Phase

**何時使用**：程式碼在處理兩件不同的事

**動機**：把程式碼拆成邊界清晰的兩個階段。

**步驟**：
1. 為第二階段建立新函式
2. 測試
3. 在兩個階段之間引入中間資料結構
4. 測試
5. 把第一階段提取成獨立函式
6. 測試

**前：**
```javascript
function priceOrder(product, quantity, shippingMethod) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0)
    * product.basePrice * product.discountRate;
  const shippingPerCase = (basePrice > shippingMethod.discountThreshold)
    ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = quantity * shippingPerCase;
  return basePrice - discount + shippingCost;
}
```

**後：**
```javascript
function priceOrder(product, quantity, shippingMethod) {
  const priceData = calculatePricingData(product, quantity);
  return applyShipping(priceData, shippingMethod);
}

function calculatePricingData(product, quantity) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0)
    * product.basePrice * product.discountRate;
  return { basePrice, quantity, discount };
}

function applyShipping(priceData, shippingMethod) {
  const shippingPerCase = (priceData.basePrice > shippingMethod.discountThreshold)
    ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = priceData.quantity * shippingPerCase;
  return priceData.basePrice - priceData.discount + shippingCost;
}
```

---

## 移動特性

### Move Method

**何時使用**：方法更依賴另一個類的資料而不是自己類的資料

**動機**：把函式放到它最依賴的資料所在的類裡。

**步驟**：
1. 檢查方法使用到的所有程式元素
2. 確認方法不是多型的
3. 把方法複製到目標類
4. 調整上下文
5. 讓原方法委託給目標方法
6. 測試
7. 視情況刪除原方法

---

### Move Field

**何時使用**：欄位更多被另一個類使用

**動機**：讓資料和使用它的函式靠在一起。

**步驟**：
1. 如果還沒有，先封裝欄位
2. 測試
3. 在目標類中建立欄位
4. 把引用改成使用目標欄位
5. 測試
6. 刪除原欄位

---

### Move Statements into Function

**何時使用**：相同程式碼總是跟著函式呼叫一起出現

**動機**：把重複語句移入函式，去掉重複。

**步驟**：
1. 如果還沒有，先把重複程式碼提取成函式
2. 把語句移入函式
3. 測試
4. 如果呼叫方不再需要獨立語句，就刪除它們

---

### Move Statements to Callers

**何時使用**：不同呼叫方需要不同的行為

**動機**：當行為需要差異化時，把它從函式裡移出去。

**步驟**：
1. 先對要移動的程式碼做 Extract Method
2. 再對原函式做 Inline Method
3. 刪除被內聯後的呼叫
4. 把提取出的程式碼移到各個呼叫方
5. 測試

---

## 資料組織

### Replace Primitive with Object

**何時使用**：資料項需要的不只是簡單值

**動機**：把資料和行為封裝在一起。

**步驟**：
1. 先做 Encapsulate Variable
2. 建立一個簡單值物件
3. 修改 setter，讓它建立新例項
4. 修改 getter，讓它返回值
5. 測試
6. 給新類增加更豐富的行為

**前：**
```javascript
class Order {
  constructor(data) {
    this.priority = data.priority; // string: "high", "rush", etc.
  }
}

// Usage
if (order.priority === "high" || order.priority === "rush") { ... }
```

**後：**
```javascript
class Priority {
  constructor(value) {
    if (!Priority.legalValues().includes(value))
      throw new Error(`Invalid priority: ${value}`);
    this._value = value;
  }

  static legalValues() { return ['low', 'normal', 'high', 'rush']; }
  get value() { return this._value; }

  higherThan(other) {
    return Priority.legalValues().indexOf(this._value) >
           Priority.legalValues().indexOf(other._value);
  }
}

// Usage
if (order.priority.higherThan(new Priority("normal"))) { ... }
```

---

### Replace Temp with Query

**何時使用**：臨時變數儲存的是一個表示式結果

**動機**：把表示式提取成函式，讓程式碼更清晰。

**步驟**：
1. 確保變數只被賦值一次
2. 把賦值右側提取成一個方法
3. 用方法呼叫替換臨時變數引用
4. 測試
5. 刪除臨時變數宣告和賦值

**前：**
```javascript
const basePrice = this._quantity * this._itemPrice;
if (basePrice > 1000) {
  return basePrice * 0.95;
} else {
  return basePrice * 0.98;
}
```

**後：**
```javascript
get basePrice() {
  return this._quantity * this._itemPrice;
}

// In the method
if (this.basePrice > 1000) {
  return this.basePrice * 0.95;
} else {
  return this.basePrice * 0.98;
}
```

---

## 簡化條件邏輯

### Decompose Conditional

**何時使用**：複雜條件語句

**動機**：把條件和分支動作分別提取出來，讓意圖更清楚。

**步驟**：
1. 對條件做 Extract Method
2. 對 then 分支做 Extract Method
3. 對 else 分支也做 Extract Method（如果有）

**前：**
```javascript
if (!aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd)) {
  charge = quantity * plan.summerRate;
} else {
  charge = quantity * plan.regularRate + plan.regularServiceCharge;
}
```

**後：**
```javascript
if (isSummer(aDate, plan)) {
  charge = summerCharge(quantity, plan);
} else {
  charge = regularCharge(quantity, plan);
}

function isSummer(date, plan) {
  return !date.isBefore(plan.summerStart) && !date.isAfter(plan.summerEnd);
}

function summerCharge(quantity, plan) {
  return quantity * plan.summerRate;
}

function regularCharge(quantity, plan) {
  return quantity * plan.regularRate + plan.regularServiceCharge;
}
```

---

### Consolidate Conditional Expression

**何時使用**：多個條件最後都返回同一個結果

**動機**：讓人一眼看出這些條件其實是一道檢查。

**步驟**：
1. 確認條件沒有副作用
2. 用 and / or 合併條件
3. 視情況對合並後的條件做 Extract Method

**前：**
```javascript
if (employee.seniority < 2) return 0;
if (employee.monthsDisabled > 12) return 0;
if (employee.isPartTime) return 0;
```

**後：**
```javascript
if (isNotEligibleForDisability(employee)) return 0;

function isNotEligibleForDisability(employee) {
  return employee.seniority < 2 ||
         employee.monthsDisabled > 12 ||
         employee.isPartTime;
}
```

---

### Replace Nested Conditional with Guard Clauses

**何時使用**：深層巢狀條件讓流程難以追蹤

**動機**：用 guard clause 提前返回，讓正常流程更清楚。

**步驟**：
1. 找出特殊情況
2. 用提前返回的 guard clause 替換它們
3. 每改一步就測試

**前：**
```javascript
function payAmount(employee) {
  let result;
  if (employee.isSeparated) {
    result = { amount: 0, reasonCode: "SEP" };
  } else {
    if (employee.isRetired) {
      result = { amount: 0, reasonCode: "RET" };
    } else {
      result = calculateNormalPay(employee);
    }
  }
  return result;
}
```

**後：**
```javascript
function payAmount(employee) {
  if (employee.isSeparated) return { amount: 0, reasonCode: "SEP" };
  if (employee.isRetired) return { amount: 0, reasonCode: "RET" };
  return calculateNormalPay(employee);
}
```

---

### Replace Conditional with Polymorphism

**何時使用**：按型別分支的 switch / 條件邏輯

**動機**：讓物件自己處理自己的行為。

**步驟**：
1. 建立類層次（如果還沒有）
2. 用 Factory Function 建立物件
3. 把條件邏輯移到超類方法裡
4. 給每種情況建立子類方法
5. 刪除原條件

**前：**
```javascript
function plumages(birds) {
  return birds.map(b => plumage(b));
}

function plumage(bird) {
  switch (bird.type) {
    case 'EuropeanSwallow':
      return "average";
    case 'AfricanSwallow':
      return (bird.numberOfCoconuts > 2) ? "tired" : "average";
    case 'NorwegianBlueParrot':
      return (bird.voltage > 100) ? "scorched" : "beautiful";
    default:
      return "unknown";
  }
}
```

**後：**
```javascript
class Bird {
  get plumage() { return "unknown"; }
}

class EuropeanSwallow extends Bird {
  get plumage() { return "average"; }
}

class AfricanSwallow extends Bird {
  get plumage() {
    return (this.numberOfCoconuts > 2) ? "tired" : "average";
  }
}

class NorwegianBlueParrot extends Bird {
  get plumage() {
    return (this.voltage > 100) ? "scorched" : "beautiful";
  }
}

function createBird(data) {
  switch (data.type) {
    case 'EuropeanSwallow': return new EuropeanSwallow(data);
    case 'AfricanSwallow': return new AfricanSwallow(data);
    case 'NorwegianBlueParrot': return new NorwegianBlueParrot(data);
    default: return new Bird(data);
  }
}
```

---

### Introduce Special Case (Null Object)

**何時使用**：重複出現 null 檢查

**動機**：返回一個特殊物件來處理特殊情況。

**步驟**：
1. 建立一個具備預期介面的特殊情況類
2. 增加 isSpecialCase 檢查
3. 引入工廠方法
4. 用特殊物件替換 null 檢查
5. 測試

**前：**
```javascript
const customer = site.customer;
// ... many places checking
if (customer === "unknown") {
  customerName = "occupant";
} else {
  customerName = customer.name;
}
```

**後：**
```javascript
class UnknownCustomer {
  get name() { return "occupant"; }
  get billingPlan() { return registry.defaultPlan; }
}

// Factory method
function customer(site) {
  return site.customer === "unknown"
    ? new UnknownCustomer()
    : site.customer;
}

// Usage - no null checks needed
const customerName = customer.name;
```

---

## 重構 API

### Separate Query from Modifier

**何時使用**：函式既返回值又有副作用

**動機**：明確哪些操作會產生副作用。

**步驟**：
1. 建立新的查詢函式
2. 複製原函式的返回邏輯
3. 修改原函式，讓它只負責副作用
4. 替換依賴返回值的呼叫點
5. 測試

**前：**
```javascript
function alertForMiscreant(people) {
  for (const p of people) {
    if (p === "Don") {
      setOffAlarms();
      return "Don";
    }
    if (p === "John") {
      setOffAlarms();
      return "John";
    }
  }
  return "";
}
```

**後：**
```javascript
function findMiscreant(people) {
  for (const p of people) {
    if (p === "Don") return "Don";
    if (p === "John") return "John";
  }
  return "";
}

function alertForMiscreant(people) {
  if (findMiscreant(people) !== "") setOffAlarms();
}
```

---

### Parameterize Function

**何時使用**：有多個做類似事情但數值不同的函式

**動機**：透過引數化減少重複。

**步驟**：
1. 選擇一個函式
2. 為變化的字面值增加引數
3. 修改函式體使用該引數
4. 測試
5. 讓呼叫方改用引數化版本
6. 刪除不再使用的舊函式

**前：**
```javascript
function tenPercentRaise(person) {
  person.salary = person.salary * 1.10;
}

function fivePercentRaise(person) {
  person.salary = person.salary * 1.05;
}
```

**後：**
```javascript
function raise(person, factor) {
  person.salary = person.salary * (1 + factor);
}

// Usage
raise(person, 0.10);
raise(person, 0.05);
```

---

### Remove Flag Argument

**何時使用**：布林引數改變函式行為

**動機**：透過拆分成明確函式，讓行為更清楚。

**步驟**：
1. 針對不同旗標值建立顯式函式
2. 替換每個呼叫點
3. 每次改動後測試
4. 刪除原函式

**前：**
```javascript
function bookConcert(customer, isPremium) {
  if (isPremium) {
    // premium booking logic
  } else {
    // regular booking logic
  }
}

bookConcert(customer, true);
bookConcert(customer, false);
```

**後：**
```javascript
function bookPremiumConcert(customer) {
  // premium booking logic
}

function bookRegularConcert(customer) {
  // regular booking logic
}

bookPremiumConcert(customer);
bookRegularConcert(customer);
```

---

## 繼承相關

### Pull Up Method

**何時使用**：多個子類裡有相同方法

**動機**：去掉類層次中的重複。

**步驟**：
1. 檢查方法是否完全相同
2. 確認簽名一致
3. 在超類中新建方法
4. 從一個子類複製實現
5. 刪除一個子類中的方法並測試
6. 刪除其他子類中的方法並測試

---

### Push Down Method

**何時使用**：某個行為只適用於部分子類

**動機**：把方法放到真正使用它的地方。

**步驟**：
1. 把方法複製到需要它的子類
2. 從超類刪除方法
3. 測試
4. 刪除不需要該方法的子類副本
5. 測試

---

### Replace Subclass with Delegate

**何時使用**：繼承用得不對，需要更靈活

**動機**：在合適的地方更偏向組合而不是繼承。

**步驟**：
1. 建立一個空的委託類
2. 在宿主類中加一個持有委託的欄位
3. 在宿主類構造委託
4. 把功能遷移到委託類
5. 每次遷移後測試
6. 用委託替代繼承

---

## Extract Class

**何時使用**：大類裡有多個職責

**動機**：拆分類以維持單一職責。

**步驟**：
1. 決定如何拆分職責
2. 建立新類
3. 把欄位從原類移到新類
4. 測試
5. 把方法從原類移到新類
6. 每次移動後測試
7. 重新檢查並命名兩個類
8. 決定如何暴露新類

**前：**
```javascript
class Person {
  get name() { return this._name; }
  set name(arg) { this._name = arg; }
  get officeAreaCode() { return this._officeAreaCode; }
  set officeAreaCode(arg) { this._officeAreaCode = arg; }
  get officeNumber() { return this._officeNumber; }
  set officeNumber(arg) { this._officeNumber = arg; }

  get telephoneNumber() {
    return `(${this._officeAreaCode}) ${this._officeNumber}`;
  }
}
```

**後：**
```javascript
class Person {
  constructor() {
    this._telephoneNumber = new TelephoneNumber();
  }
  get name() { return this._name; }
  set name(arg) { this._name = arg; }
  get telephoneNumber() { return this._telephoneNumber.toString(); }
  get officeAreaCode() { return this._telephoneNumber.areaCode; }
  set officeAreaCode(arg) { this._telephoneNumber.areaCode = arg; }
}

class TelephoneNumber {
  get areaCode() { return this._areaCode; }
  set areaCode(arg) { this._areaCode = arg; }
  get number() { return this._number; }
  set number(arg) { this._number = arg; }
  toString() { return `(${this._areaCode}) ${this._number}`; }
}
```

---

## 快速參考：異味到重構

| 程式碼異味 | 主要重構 | 備選方案 |
|----------|---------|---------|
| 長函式 | Extract Method | Replace Temp with Query |
| 重複程式碼 | Extract Method | Pull Up Method |
| 大類 | Extract Class | Extract Subclass |
| 長引數列表 | Introduce Parameter Object | Preserve Whole Object |
| Feature Envy | Move Method | Extract Method + Move |
| 資料泥團 | Extract Class | Introduce Parameter Object |
| 基礎型別沉迷 | Replace Primitive with Object | Replace Type Code |
| switch 語句 | Replace Conditional with Polymorphism | Replace Type Code |
| 臨時欄位 | Extract Class | Introduce Null Object |
| 訊息鏈 | Hide Delegate | Extract Method |
| 中間人 | Remove Middle Man | Inline Method |
| 發散式變化 | Extract Class | Split Phase |
| 散彈式修改 | Move Method | Inline Class |
| 死程式碼 | Remove Dead Code | - |
| 臆想泛化 | Collapse Hierarchy | Inline Class |

---

## 延伸閱讀

- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (第 2 版)
- 線上目錄：https://refactoring.com/catalog/
