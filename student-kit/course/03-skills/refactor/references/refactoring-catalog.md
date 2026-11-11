# 重構手法目錄

這是根據 Martin Fowler 的《Refactoring》（第 2 版）整理的重構手法目錄，每個重構手法都包含動機、逐步操作步驟與範例。

> 「重構的定義在於它的操作步驟——也就是你為了完成這項改變所依循的精確步驟序列。」——Martin Fowler

---

## 如何使用本目錄

1. **找出程式碼異味**：參考程式碼異味目錄
2. **在本目錄中找到對應的重構手法**
3. **依序照著步驟做**
4. **每個步驟後都要測試**，確保行為沒有改變

**黃金法則**：如果任何一個步驟耗時超過 10 分鐘，就把它拆成更小的步驟。

---

## 最常見的重構手法

### 提取方法（Extract Method）

**適用時機**：方法過長、有重複程式碼、需要為某個概念命名

**動機**：把一段程式碼變成一個方法，用方法名稱來說明用途。

**步驟**：
1. 建立一個新方法，名稱要說明「做什麼」（而不是「怎麼做」）
2. 把這段程式碼複製到新方法裡
3. 掃描這段程式碼中用到的區域變數
4. 把區域變數當作參數傳入（或直接在方法中宣告）
5. 適當處理回傳值
6. 把原本的程式碼片段換成對新方法的呼叫
7. 測試

**修改前**：
```javascript
function printOwing(invoice) {
  let outstanding = 0;

  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");

  // 計算未付金額
  for (const order of invoice.orders) {
    outstanding += order.amount;
  }

  // 印出明細
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

**修改後**：
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

### 內聯方法（Inline Method）

**適用時機**：方法本身跟名稱一樣清楚易懂、有過度的委派轉呼叫

**動機**：當方法沒有增加價值時，移除不必要的間接層。

**步驟**：
1. 確認這個方法不是多型方法
2. 找出所有呼叫這個方法的地方
3. 把每個呼叫換成方法本體
4. 每次替換後都要測試
5. 移除方法定義

**修改前**：
```javascript
function getRating(driver) {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}

function moreThanFiveLateDeliveries(driver) {
  return driver.numberOfLateDeliveries > 5;
}
```

**修改後**：
```javascript
function getRating(driver) {
  return driver.numberOfLateDeliveries > 5 ? 2 : 1;
}
```

---

### 提取變數（Extract Variable）

**適用時機**：複雜的運算式難以理解

**動機**：為複雜運算式的某一部分取個名字。

**步驟**：
1. 確認這個運算式沒有副作用
2. 宣告一個不可變的變數
3. 把它設成該運算式（或其中一部分）的結果
4. 把原本的運算式換成這個變數
5. 測試

**修改前**：
```javascript
return order.quantity * order.itemPrice -
  Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
  Math.min(order.quantity * order.itemPrice * 0.1, 100);
```

**修改後**：
```javascript
const basePrice = order.quantity * order.itemPrice;
const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
const shipping = Math.min(basePrice * 0.1, 100);
return basePrice - quantityDiscount + shipping;
```

---

### 內聯變數（Inline Variable）

**適用時機**：變數名稱沒有比運算式本身傳達更多資訊

**動機**：移除不必要的間接層。

**步驟**：
1. 確認等號右邊沒有副作用
2. 如果變數不是不可變的，先讓它變成不可變並測試
3. 找到第一個參照，換成該運算式
4. 測試
5. 對其他所有參照重複這個步驟
6. 移除變數宣告與賦值
7. 測試

---

### 重新命名變數（Rename Variable）

**適用時機**：名稱沒有清楚表達用途

**動機**：好的命名對乾淨的程式碼至關重要。

**步驟**：
1. 如果變數被廣泛使用，考慮先封裝它
2. 找出所有參照
3. 逐一修改每個參照
4. 測試

**小提示**：
- 用能表達意圖的名稱
- 避免縮寫
- 使用領域術語

```javascript
// 不好
const d = 30;
const x = users.filter(u => u.a);

// 好
const daysSinceLastLogin = 30;
const activeUsers = users.filter(user => user.isActive);
```

---

### 變更函式宣告（Change Function Declaration）

**適用時機**：函式名稱沒有說明用途、參數需要調整

**動機**：好的函式名稱能讓程式碼自我說明。

**步驟（簡單版）**：
1. 移除不需要的參數
2. 修改名稱
3. 新增需要的參數
4. 測試

**步驟（遷移版——用於複雜的變更）**：
1. 如果要移除參數，先確認它沒有被用到
2. 用想要的宣告方式建立新函式
3. 讓舊函式呼叫新函式
4. 測試
5. 把呼叫端改成呼叫新函式
6. 每次修改後都要測試
7. 移除舊函式

**修改前**：
```javascript
function circum(radius) {
  return 2 * Math.PI * radius;
}
```

**修改後**：
```javascript
function circumference(radius) {
  return 2 * Math.PI * radius;
}
```

---

### 封裝變數（Encapsulate Variable）

**適用時機**：資料在多處被直接存取

**動機**：為資料操作提供一個清楚的存取點。

**步驟**：
1. 建立 getter 與 setter 函式
2. 找出所有參照
3. 把讀取換成 getter
4. 把寫入換成 setter
5. 每次修改後都要測試
6. 限制該變數的可見範圍

**修改前**：
```javascript
let defaultOwner = { firstName: "Martin", lastName: "Fowler" };

// 在很多地方被使用
spaceship.owner = defaultOwner;
```

**修改後**：
```javascript
let defaultOwnerData = { firstName: "Martin", lastName: "Fowler" };

function defaultOwner() { return defaultOwnerData; }
function setDefaultOwner(arg) { defaultOwnerData = arg; }

spaceship.owner = defaultOwner();
```

---

### 引入參數物件（Introduce Parameter Object）

**適用時機**：好幾個參數經常一起出現

**動機**：把天生就該歸在一起的資料分組。

**步驟**：
1. 為這組參數建立一個新的類別／結構
2. 測試
3. 使用變更函式宣告來新增這個新物件
4. 測試
5. 針對這組裡的每個參數，把它從函式中移除，改用新物件
6. 每次修改後都要測試

**修改前**：
```javascript
function amountInvoiced(startDate, endDate) { ... }
function amountReceived(startDate, endDate) { ... }
function amountOverdue(startDate, endDate) { ... }
```

**修改後**：
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

### 將函式組合成類別（Combine Functions into Class）

**適用時機**：好幾個函式都在操作同一份資料

**動機**：把函式跟它們所操作的資料組合在一起。

**步驟**：
1. 對共用資料套用封裝記錄（Encapsulate Record）
2. 把每個函式搬進類別
3. 每次搬移後都要測試
4. 把資料引數替換成類別欄位的使用

**修改前**：
```javascript
function base(reading) { ... }
function taxableCharge(reading) { ... }
function calculateBaseCharge(reading) { ... }
```

**修改後**：
```javascript
class Reading {
  constructor(data) { this._data = data; }

  get base() { ... }
  get taxableCharge() { ... }
  get calculateBaseCharge() { ... }
}
```

---

### 拆分階段（Split Phase）

**適用時機**：程式碼處理著兩件不同的事

**動機**：把程式碼拆成邊界清楚的不同階段。

**步驟**：
1. 為第二階段建立一個函式
2. 測試
3. 在兩個階段之間引入一個中介資料結構
4. 測試
5. 把第一階段提取成獨立函式
6. 測試

**修改前**：
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

**修改後**：
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

## 搬移功能

### 搬移方法（Move Method）

**適用時機**：方法用到另一個類別的功能，比用到自己的還多

**動機**：把函式放在它最常用到的資料旁邊。

**步驟**：
1. 檢查這個方法在自己類別裡用到的所有程式元素
2. 確認這個方法是不是多型方法
3. 把方法複製到目標類別
4. 因應新環境做調整
5. 讓原本的方法轉呼叫目標方法
6. 測試
7. 考慮移除原本的方法

---

### 搬移欄位（Move Field）

**適用時機**：欄位被另一個類別用得更多

**動機**：讓資料跟使用它的函式放在一起。

**步驟**：
1. 如果還沒封裝這個欄位，先封裝它
2. 測試
3. 在目標類別中建立欄位
4. 把參照改成使用目標欄位
5. 測試
6. 移除原本的欄位

---

### 將陳述式搬入函式（Move Statements into Function）

**適用時機**：同樣的程式碼總是伴隨著某個函式呼叫出現

**動機**：把重複的程式碼搬進函式裡，消除重複。

**步驟**：
1. 如果重複的程式碼還沒被提取成函式，先提取它
2. 把陳述式搬進那個函式
3. 測試
4. 如果呼叫端不再需要獨立的陳述式，就移除它們

---

### 將陳述式搬到呼叫端（Move Statements to Callers）

**適用時機**：共用行為在不同呼叫端之間出現差異

**動機**：當行為需要因呼叫端而異時，把它搬出函式外。

**步驟**：
1. 對要搬移的程式碼使用提取方法
2. 對原本的函式使用內聯方法
3. 移除已經被內聯的呼叫
4. 把提取出來的程式碼搬到每個呼叫端
5. 測試

---

## 整理資料

### 以物件取代基本型別（Replace Primitive with Object）

**適用時機**：資料項目需要比單純數值更多的行為

**動機**：把資料跟它的行為封裝在一起。

**步驟**：
1. 套用封裝變數
2. 建立一個簡單的值物件類別
3. 把 setter 改成建立一個新實例
4. 把 getter 改成回傳這個值
5. 測試
6. 為新類別加上更豐富的行為

**修改前**：
```javascript
class Order {
  constructor(data) {
    this.priority = data.priority; // 字串："high"、"rush" 等
  }
}

// 用法
if (order.priority === "high" || order.priority === "rush") { ... }
```

**修改後**：
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

// 用法
if (order.priority.higherThan(new Priority("normal"))) { ... }
```

---

### 以查詢取代暫存變數（Replace Temp with Query）

**適用時機**：暫存變數保存著某個運算式的結果

**動機**：把運算式提取成函式，讓程式碼更清楚。

**步驟**：
1. 確認這個變數只被賦值一次
2. 把賦值等號右邊的內容提取成方法
3. 把對暫存變數的參照換成呼叫這個方法
4. 測試
5. 移除暫存變數的宣告與賦值

**修改前**：
```javascript
const basePrice = this._quantity * this._itemPrice;
if (basePrice > 1000) {
  return basePrice * 0.95;
} else {
  return basePrice * 0.98;
}
```

**修改後**：
```javascript
get basePrice() {
  return this._quantity * this._itemPrice;
}

// 在方法內
if (this.basePrice > 1000) {
  return this.basePrice * 0.95;
} else {
  return this.basePrice * 0.98;
}
```

---

## 簡化條件邏輯

### 分解條件式（Decompose Conditional）

**適用時機**：複雜的條件式（if-then-else）陳述式

**動機**：把條件與動作提取出來，讓意圖更清楚。

**步驟**：
1. 對條件套用提取方法
2. 對 then 分支套用提取方法
3. 對 else 分支（如果有的話）套用提取方法

**修改前**：
```javascript
if (!aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd)) {
  charge = quantity * plan.summerRate;
} else {
  charge = quantity * plan.regularRate + plan.regularServiceCharge;
}
```

**修改後**：
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

### 合併條件式（Consolidate Conditional Expression）

**適用時機**：多個條件卻導向相同的結果

**動機**：讓「這些條件其實是同一個檢查」這件事變得清楚。

**步驟**：
1. 確認條件裡沒有副作用
2. 用 `and` 或 `or` 把條件合併起來
3. 考慮對合併後的條件套用提取方法

**修改前**：
```javascript
if (employee.seniority < 2) return 0;
if (employee.monthsDisabled > 12) return 0;
if (employee.isPartTime) return 0;
```

**修改後**：
```javascript
if (isNotEligibleForDisability(employee)) return 0;

function isNotEligibleForDisability(employee) {
  return employee.seniority < 2 ||
         employee.monthsDisabled > 12 ||
         employee.isPartTime;
}
```

---

### 以衛式子句取代巢狀條件式（Replace Nested Conditional with Guard Clauses）

**適用時機**：深層巢狀的條件式讓流程難以追蹤

**動機**：用衛式子句處理特殊情況，讓正常流程保持清楚。

**步驟**：
1. 找出特殊情況的條件
2. 把它們換成會提早回傳的衛式子句
3. 每次修改後都要測試

**修改前**：
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

**修改後**：
```javascript
function payAmount(employee) {
  if (employee.isSeparated) return { amount: 0, reasonCode: "SEP" };
  if (employee.isRetired) return { amount: 0, reasonCode: "RET" };
  return calculateNormalPay(employee);
}
```

---

### 以多型取代條件式（Replace Conditional with Polymorphism）

**適用時機**：根據型別做的 switch/case、隨型別而異的條件邏輯

**動機**：讓物件自己處理自己的行為。

**步驟**：
1. 建立類別階層（如果還沒有的話）
2. 使用工廠函式（Factory Function）建立物件
3. 把條件邏輯搬進父類別的方法
4. 為每種情況建立子類別方法
5. 移除原本的條件式

**修改前**：
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

**修改後**：
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

### 引入特例（Introduce Special Case，Null Object）

**適用時機**：對特殊情況重複做 null 檢查

**動機**：回傳一個能自己處理特殊情況的特例物件。

**步驟**：
1. 建立具備預期介面的特例類別
2. 加上 isSpecialCase 檢查
3. 引入工廠方法
4. 把 null 檢查換成使用特例物件
5. 測試

**修改前**：
```javascript
const customer = site.customer;
// ……很多地方都在檢查
if (customer === "unknown") {
  customerName = "occupant";
} else {
  customerName = customer.name;
}
```

**修改後**：
```javascript
class UnknownCustomer {
  get name() { return "occupant"; }
  get billingPlan() { return registry.defaultPlan; }
}

// 工廠方法
function customer(site) {
  return site.customer === "unknown"
    ? new UnknownCustomer()
    : site.customer;
}

// 用法——不需要做 null 檢查
const customerName = customer.name;
```

---

## 重構 API

### 將查詢與修改函式分離（Separate Query from Modifier）

**適用時機**：函式既回傳值又帶有副作用

**動機**：讓「哪些操作有副作用」這件事變得清楚。

**步驟**：
1. 建立一個新的查詢函式
2. 複製原本函式的回傳邏輯
3. 把原本的函式改成回傳 void
4. 把用到回傳值的呼叫端換掉
5. 測試

**修改前**：
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

**修改後**：
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

### 參數化函式（Parameterize Function）

**適用時機**：好幾個函式做著類似的事，只是數值不同

**動機**：加一個參數來消除重複。

**步驟**：
1. 挑一個函式
2. 為變動的字面值加上參數
3. 把函式本體改成使用這個參數
4. 測試
5. 把呼叫端改成使用參數化後的版本
6. 移除不再使用的函式

**修改前**：
```javascript
function tenPercentRaise(person) {
  person.salary = person.salary * 1.10;
}

function fivePercentRaise(person) {
  person.salary = person.salary * 1.05;
}
```

**修改後**：
```javascript
function raise(person, factor) {
  person.salary = person.salary * (1 + factor);
}

// 用法
raise(person, 0.10);
raise(person, 0.05);
```

---

### 移除旗標引數（Remove Flag Argument）

**適用時機**：布林參數會改變函式行為

**動機**：透過拆成獨立函式，讓行為變得明確。

**步驟**：
1. 為每個旗標值建立明確的函式
2. 把每個呼叫換成對應的新函式
3. 每次修改後都要測試
4. 移除原本的函式

**修改前**：
```javascript
function bookConcert(customer, isPremium) {
  if (isPremium) {
    // 高級訂票邏輯
  } else {
    // 一般訂票邏輯
  }
}

bookConcert(customer, true);
bookConcert(customer, false);
```

**修改後**：
```javascript
function bookPremiumConcert(customer) {
  // 高級訂票邏輯
}

function bookRegularConcert(customer) {
  // 一般訂票邏輯
}

bookPremiumConcert(customer);
bookRegularConcert(customer);
```

---

## 處理繼承

### 上移方法（Pull Up Method）

**適用時機**：多個子類別有相同的方法

**動機**：消除類別階層中的重複。

**步驟**：
1. 檢查這些方法是否完全相同
2. 確認方法簽章是否一致
3. 在父類別中建立新方法
4. 從其中一個子類別複製方法本體
5. 刪除其中一個子類別的方法，測試
6. 刪除其他子類別的方法，逐一測試

---

### 下移方法（Push Down Method）

**適用時機**：某個行為只跟部分子類別有關

**動機**：把方法放在用得到它的地方。

**步驟**：
1. 把方法複製到每個需要它的子類別
2. 從父類別移除該方法
3. 測試
4. 從不需要它的子類別中移除
5. 測試

---

### 以委派取代子類別（Replace Subclass with Delegate）

**適用時機**：繼承被誤用，需要更多彈性

**動機**：適當的情況下，優先選用組合而非繼承。

**步驟**：
1. 建立一個空的委派類別
2. 在宿主類別加上一個欄位持有這個委派物件
3. 為委派物件建立建構子，由宿主類別呼叫
4. 把功能搬到委派物件
5. 每次搬移後都要測試
6. 把繼承改成委派

---

## 提取類別（Extract Class）

**適用時機**：大型類別身兼多種職責

**動機**：拆分類別，維持單一職責。

**步驟**：
1. 決定要怎麼拆分職責
2. 建立新類別
3. 把欄位從原本的類別搬到新類別
4. 測試
5. 把方法從原本的類別搬到新類別
6. 每次搬移後都要測試
7. 檢視並重新命名兩個類別
8. 決定要怎麼公開新類別

**修改前**：
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

**修改後**：
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

## 快速參考：程式碼異味對應重構手法

| 程式碼異味 | 主要重構手法 | 替代方案 |
|------------|-------------------|-------------|
| 過長方法（Long Method） | 提取方法 | 以查詢取代暫存變數 |
| 重複程式碼（Duplicate Code） | 提取方法 | 上移方法 |
| 過大類別（Large Class） | 提取類別 | 提取子類別 |
| 過長參數列（Long Parameter List） | 引入參數物件 | 保留完整物件（Preserve Whole Object） |
| 依戀情結（Feature Envy） | 搬移方法 | 提取方法+搬移 |
| 資料泥團（Data Clumps） | 提取類別 | 引入參數物件 |
| 基本型別偏執（Primitive Obsession） | 以物件取代基本型別 | 取代型別碼（Replace Type Code） |
| Switch 陳述式（Switch Statements） | 以多型取代條件式 | 取代型別碼（Replace Type Code） |
| 暫時欄位（Temporary Field） | 提取類別 | 引入 Null 物件（Introduce Null Object） |
| 訊息鏈（Message Chains） | 隱藏委派（Hide Delegate） | 提取方法 |
| 中間人（Middle Man） | 移除中間人（Remove Middle Man） | 內聯方法 |
| 發散式變化（Divergent Change） | 提取類別 | 拆分階段 |
| 霰彈式修改（Shotgun Surgery） | 搬移方法 | 內聯類別（Inline Class） |
| 無用程式碼（Dead Code） | 移除無用程式碼（Remove Dead Code） | - |
| 投機性泛化（Speculative Generality） | 折疊繼承體系（Collapse Hierarchy） | 內聯類別（Inline Class） |

---

## 延伸閱讀

- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.)
- Online catalog: https://refactoring.com/catalog/

---

**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/skills
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
