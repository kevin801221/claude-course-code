---
name: refactor
description: 依據 Martin Fowler 的方法論進行系統化程式碼重構。使用時機：使用者要求重構程式碼、改善程式碼結構、減少技術債、清理舊有程式碼、消除程式碼異味，或改善程式碼可維護性。這個技能（Skills）會引導完成一套分階段流程，包含研究、規劃與安全的漸進式實作。
---

# 程式碼重構技能

一套依據 Martin Fowler《Refactoring: Improving the Design of Existing Code》（第二版）方法論的系統化重構做法。這個技能強調由測試撐腰的安全漸進式變更。

> 「重構是在不改變軟體系統外部行為的前提下，改善其內部結構的過程。」— Martin Fowler

## 核心原則

1. **行為不變**：外部行為必須維持不變
2. **小步前進**：進行微小、可測試的變更
3. **測試驅動**：測試是安全網
4. **持續進行**：重構是持續進行的事，不是一次性的活動
5. **協作**：每個階段都需要取得使用者核准

## 工作流程總覽

```
第 1 階段：研究與分析
    ↓
第 2 階段：測試涵蓋率評估
    ↓
第 3 階段：程式碼異味辨識
    ↓
第 4 階段：擬定重構計畫
    ↓
第 5 階段：漸進式實作
    ↓
第 6 階段：審閱與反覆修正
```

---

## 第 1 階段：研究與分析

### 目標
- 理解程式碼庫的結構與用途
- 確認重構的範圍
- 蒐集有關業務需求的背景資訊

### 要問使用者的問題
開始之前，先釐清：

1. **範圍**：哪些檔案／模組／函式需要重構？
2. **目標**：想解決什麼問題？（可讀性、效能、可維護性）
3. **限制**：有沒有不應該變動的區域？
4. **時程壓力**：這是不是正在卡住其他工作？
5. **測試狀態**：有測試嗎？測試都通過嗎？

### 動作
- [ ] 讀取並理解目標程式碼
- [ ] 找出相依關係與整合點
- [ ] 記錄目前的架構
- [ ] 記下任何既有的技術債標記（TODO、FIXME）

### 輸出
向使用者呈現：
- 程式碼結構摘要
- 找到的問題區域
- 初步建議
- **請求核准後再繼續**

---

## 第 2 階段：測試涵蓋率評估

### 為什麼測試很重要
> 「沒有測試就重構，就像不繫安全帶開車一樣。」— Martin Fowler

測試是安全重構的**關鍵推手**。沒有測試的話，你就冒著引入 bug 的風險。

### 評估步驟

1. **檢查是否有既有測試**
   ```bash
   # 尋找測試檔案
   find . -name "*test*" -o -name "*spec*" | head -20
   ```

2. **執行既有測試**
   ```bash
   # JavaScript/TypeScript
   npm test

   # Python
   pytest -v

   # Java
   mvn test
   ```

3. **檢查涵蓋率（如果有的話）**
   ```bash
   # JavaScript
   npm run test:coverage

   # Python
   pytest --cov=.
   ```

### 決策點：詢問使用者

**如果測試都存在且通過：**
- 進入第 3 階段

**如果測試缺漏或不完整：**
提出以下選項：
1. 先寫測試（建議做法）
2. 在重構過程中漸進式補上測試
3. 不寫測試直接進行（有風險——需要使用者明確認可）

**如果測試失敗：**
- 停下來。先修好失敗的測試，再進行重構
- 詢問使用者：要先修測試嗎？

### 測試撰寫準則（如果需要）

針對每個要重構的函式，確保測試涵蓋：
- 正常路徑（一般操作）
- 邊界情況（空輸入、null、邊界值）
- 錯誤情境（無效輸入、例外）

使用「red-green-refactor」循環：
1. 寫一個會失敗的測試（red）
2. 讓它通過（green）
3. 重構

---

## 第 3 階段：程式碼異味辨識

### 什麼是程式碼異味？
更深層問題的症狀。它們不是 bug，而是程式碼可以被改善的訊號。

### 要檢查的常見程式碼異味

完整目錄請見 [references/code-smells.md](references/code-smells.md)。

#### 快速參考

| 異味 | 跡象 | 影響 |
|-------|-------|------|
| **Long Method（過長方法）** | 方法超過 30-50 行 | 難以理解、測試、維護 |
| **Duplicated Code（重複程式碼）** | 相同邏輯出現在多處 | 修 bug 要改好幾個地方 |
| **Large Class（過大類別）** | 類別承擔太多職責 | 違反單一職責原則 |
| **Feature Envy（特性依戀）** | 方法過度使用另一個類別的資料 | 封裝不佳 |
| **Primitive Obsession（基本型別偏執）** | 過度使用基本型別而非物件 | 缺少領域概念 |
| **Long Parameter List（過長參數列）** | 方法有 4 個以上參數 | 難以正確呼叫 |
| **Data Clumps（資料泥團）** | 同一組資料項目反覆一起出現 | 缺少抽象化 |
| **Switch Statements（switch 陳述式）** | 複雜的 switch／if-else 鏈 | 難以擴充 |
| **Speculative Generality（投機性泛化）** | 「以防萬一」寫的程式碼 | 不必要的複雜度 |
| **Dead Code（死程式碼）** | 未使用的程式碼 | 造成混淆、增加維護負擔 |

### 分析步驟

1. **自動化分析**（如果有腳本可用）
   ```bash
   python scripts/detect-smells.py <file>
   ```

2. **人工審閱**
   - 有系統地逐步檢視程式碼
   - 記下每個異味的位置與嚴重程度
   - 依影響程度分類（Critical／High／Medium／Low）

3. **排定優先順序**
   優先處理以下異味：
   - 卡住目前開發進度的
   - 會造成 bug 或混淆的
   - 影響最常變動的程式碼路徑的

### 輸出：異味報告

向使用者呈現：
- 已找到的異味清單，附位置資訊
- 各異味的嚴重程度評估
- 建議的優先順序
- **請求對優先順序的核准**

---

## 第 4 階段：擬定重構計畫

### 選擇重構手法

針對每個異味，從目錄中選出適合的重構手法。

完整清單請見 [references/refactoring-catalog.md](references/refactoring-catalog.md)。

#### 異味對應重構手法

| 程式碼異味 | 建議的重構手法 |
|------------|---------------------------|
| Long Method | Extract Method、Replace Temp with Query |
| Duplicated Code | Extract Method、Pull Up Method、Form Template Method |
| Large Class | Extract Class、Extract Subclass |
| Feature Envy | Move Method、Move Field |
| Primitive Obsession | Replace Primitive with Object、Replace Type Code with Class |
| Long Parameter List | Introduce Parameter Object、Preserve Whole Object |
| Data Clumps | Extract Class、Introduce Parameter Object |
| Switch Statements | Replace Conditional with Polymorphism |
| Speculative Generality | Collapse Hierarchy、Inline Class、Remove Dead Code |
| Dead Code | Remove Dead Code |

### 計畫結構

使用 [templates/refactoring-plan.md](templates/refactoring-plan.md) 的範本。

針對每項重構：
1. **目標**：哪段程式碼會變動
2. **異味**：解決什麼問題
3. **重構手法**：套用哪個技巧
4. **步驟**：詳細的微步驟
5. **風險**：可能會出什麼問題
6. **回滾方式**：如果需要，如何還原

### 分階段做法

**關鍵**：分階段漸進式導入重構。

**第 A 階段：快速見效項目**（低風險、高價值）
- 為求清晰而重新命名變數
- 抽取明顯的重複程式碼
- 移除死程式碼

**第 B 階段：結構性改善**（中等風險）
- 從過長函式中抽取方法
- 引入參數物件
- 把方法移到適合的類別中

**第 C 階段：架構性變更**（較高風險）
- 用多型取代條件判斷
- 抽取類別
- 引入設計模式

### 決策點：向使用者呈現計畫

實作之前：
- 展示完整的重構計畫
- 說明每個階段及其風險
- 針對每個階段取得明確核准
- **詢問**：「要開始進行第 A 階段嗎？」

---

## 第 5 階段：漸進式實作

### 黃金原則
> 「變更 → 測試 → 通過了嗎？→ 提交 → 下一步」

### 實作節奏

針對每個重構步驟：

1. **事前檢查**
   - 測試通過（綠燈）
   - 程式碼可以編譯

2. **進行一個小變更**
   - 依照目錄中的操作細節進行
   - 讓變更保持最小

3. **驗證**
   - 立刻執行測試
   - 檢查是否有編譯錯誤

4. **如果測試通過（綠燈）**
   - 提交並附上清楚的說明
   - 進行下一步

5. **如果測試失敗（紅燈）**
   - 立刻停下來
   - 復原變更
   - 分析出了什麼問題
   - 若不確定，詢問使用者

### 提交策略

每個提交都應該：
- **原子性**：只包含一個邏輯變更
- **可回復**：容易還原
- **有描述性**：提交訊息清楚

提交訊息範例：
```
refactor: Extract calculateTotal() from processOrder()
refactor: Rename 'x' to 'customerCount' for clarity
refactor: Remove unused validateOldFormat() method
```

### 進度回報

每個子階段完成後，向使用者回報：
- 做了哪些變更
- 測試是否還在通過
- 遇到什麼問題
- **詢問**：「要繼續下一批嗎？」

---

## 第 6 階段：審閱與反覆修正

### 重構後檢查清單

- [ ] 所有測試都通過
- [ ] 沒有新的警告／錯誤
- [ ] 程式碼可以成功編譯
- [ ] 行為沒有改變（人工驗證）
- [ ] 文件已更新（如果需要）
- [ ] 提交歷史乾淨清楚

### 指標比較

在變更前後執行複雜度分析：
```bash
python scripts/analyze-complexity.py <file>
```

呈現改善結果：
- 程式碼行數變化
- 循環複雜度變化
- 可維護性指數變化

### 使用者審閱

呈現最終結果：
- 所有變更的摘要
- 前後程式碼比較
- 指標改善狀況
- 剩餘的技術債
- **詢問**：「你對這些變更滿意嗎？」

### 下一步

與使用者討論：
- 還有其他異味需要處理嗎？
- 要排程後續的重構嗎？
- 要在其他地方套用類似的變更嗎？

---

## 重要準則

### 何時要停下來詢問

在以下情況務必暫停並徵詢使用者：
- 不確定業務邏輯
- 變更可能影響外部 API
- 測試涵蓋不足
- 需要重大架構決策
- 風險等級升高
- 遇到預期外的複雜度

### 安全規則

1. **絕不在沒有測試的情況下重構**（除非使用者明確認可風險）
2. **絕不進行大幅變更**——拆成微小步驟
3. **絕不跳過**每次變更後的測試執行
4. **絕不在測試失敗時繼續**——先修正或回滾
5. **絕不自行假設**——有疑慮就問

### 不該做的事

- 不要把重構和新增功能混在一起做
- 不要在生產環境緊急事故期間重構
- 不要重構你不理解的程式碼
- 不要過度工程化——保持簡單
- 不要一次重構所有東西

---

## 快速開始範例

### 情境：過長方法且有重複

**重構前：**
```javascript
function processOrder(order) {
  // 150 行程式碼，包含：
  // - 重複的驗證邏輯
  // - 內嵌計算
  // - 混雜的職責
}
```

**重構步驟：**

1. **確認 processOrder() 有測試**
2. **抽取**驗證邏輯到 validateOrder()
3. **測試**——應該要通過
4. **抽取**計算邏輯到 calculateOrderTotal()
5. **測試**——應該要通過
6. **抽取**通知邏輯到 notifyCustomer()
7. **測試**——應該要通過
8. **審閱**——processOrder() 現在協調了 3 個清楚的函式

**重構後：**
```javascript
function processOrder(order) {
  validateOrder(order);
  const total = calculateOrderTotal(order);
  notifyCustomer(order, total);
  return { order, total };
}
```

---

## 參考資料

- [程式碼異味目錄](references/code-smells.md) - 完整的程式碼異味清單
- [重構手法目錄](references/refactoring-catalog.md) - 重構技巧
- [重構計畫範本](templates/refactoring-plan.md) - 規劃範本

## 腳本

- `scripts/analyze-complexity.py` - 分析程式碼複雜度指標
- `scripts/detect-smells.py` - 自動化異味偵測

## 版本歷史

- v1.0.0（2025-01-15）：首次發行，包含 Fowler 方法論、分階段做法、使用者諮詢節點

---

**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/skills
**相容模型**：Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
