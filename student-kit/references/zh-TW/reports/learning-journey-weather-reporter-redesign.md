# 學習旅程 —— 天氣播報員改版計畫

← 回到 [README](../README.md)

> 英文原文：[`reports/learning-journey-weather-reporter-redesign.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/reports/learning-journey-weather-reporter-redesign.md)

## 概觀

把第 7 張之後的所有投影片，圍繞單一貫穿範例重新設計：**天氣播報員代理（weather reporter agent）**。敘事弧線對應目錄的可見順序（Agents → Skills → Context → CLAUDE.md → Commands+Workflow），讓聽眾先認識這位天氣播報員，再理解他們知道什麼、怎麼思考、遵守什麼規則，最後是如何用一個命令觸發他們。

---

## 1. 現有 → 新章節對照

| 現有章節 | 現有投影片 | 動作 | 新位置 |
|---|---|---|---|
| Topic 1: Context | 7-11（章節頁在 7） | 移到 Topic 3 | 投影片 17-21 |
| Topic 2: CLAUDE.md | 12-17（章節頁在 12） | 移到 Topic 4 | 投影片 22-27 |
| Topic 3: Agents | 18-23（章節頁在 18） | 移到 Topic 1 | 投影片 7-12 |
| Topic 4: Skills | 24-29（章節頁在 24） | 移到 Topic 2 | 投影片 13-18 |
| Topic 5: Commands | 30-32（章節頁在 30） | 與 Workflow 合併成 Topic 5 | 投影片 28-32 |
| Topic 6: Workflow | 33-36（章節頁在 33） | 併入 Commands 章節 | （不另設章節頁） |
| 結尾投影片 | 37 | 保留，更新副標 | 投影片 33 |

**新總數：33 張**（等於現有 37 張扣掉 Workflow 章節頁與併入 Commands 章節的 3 張 Workflow 內容頁，而 Commands 章節則增加那 3 張）。

等等 —— 讓我重算：

現有：投影片 7-37 = 31 張。
- Agents 章節：6 張（18-23）→ 變成 Topic 1（7-12）
- Skills 章節：6 張（24-29）→ 變成 Topic 2（13-18）
- Context 章節：5 張（7-11）→ 變成 Topic 3（19-23）
- CLAUDE.md 章節：6 張（12-17）→ 變成 Topic 4（24-29）
- Commands+Workflow 合併：3 + 1 章節頁 + 4 內容頁 = Commands（3）+ Workflow（1 章節頁 + 3 內容頁）= 7 張 → 變成 Topic 5（30-36）
- 結尾：1 張（37）

**新總數：37 張。**（沒有投影片被刪除；Workflow 章節頁成為合併後 Commands+Workflow 章節的一部分 —— 我們把它保留為子章節，或拿掉它的 `data-level` 以避免出現第二個章節分隔。）

**決定**：保留全部 37 張。拿掉舊 Workflow 章節分隔頁（投影片 33）的 `data-level`，讓它被視為內容頁而非章節分隔。Commands 章節涵蓋 30-36。Workflow 章節分隔變成 Commands 章節內部的視覺「章節標題」。

其實更簡單：把 Workflow 章節分隔保留為沒有 `data-level` 的內容頁。旅程列維持在 `commands` 層級。章節編號文字從「Topic 6」改成純粹的子標題。

---

## 2. 新的 LEVELS 對照表（鍵與顏色皆不變）

新章節順序為：**Agents → Skills → Context → CLAUDE.md → Commands**。`workflow` 這個層級鍵不再用於 `data-level`（章節分隔頁失去 `data-level`）。`LEVELS` 對照表仍保留 `workflow` 供旅程列的歷史顯示，但沒有投影片會觸發它。

**修正後的做法**：既然沒有投影片帶 `data-level="workflow"`，就把 `workflow` 層級從 LEVELS 對照表中完全拿掉。旅程列最高停在 `commands`（83%）。這樣也行 —— Workflow 章節是作為 Commands 章節*內部*的高潮呈現，而非獨立主題。

不過旅程列在結尾章節只填到 83% 而非 100%，感覺不夠完整。更好的計畫：**把 Commands+Workflow 合併成單一章節「Commands & Workflow」**，帶 `data-level="commands"`。在 LEVELS 中保留 `workflow` 為 100%，並把 `data-level="workflow"` 指派給*舊的* workflow 章節分隔頁 —— 它成為 Commands 章節內的視覺轉場。這樣旅程列就能在 workflow 那幾張填滿到 100%。

**最終決定**：LEVELS 中同時保留 `commands`（83%）與 `workflow`（100%）。把 `data-level="commands"` 指派給 Commands 章節分隔頁，`data-level="workflow"` 指派給 Workflow 子章節頁。旅程刻度維持原樣。這與現有結構完全一致 —— 只是內容頁重新排序。

---

## 3. 逐張投影片內容大綱

### 投影片 1-6（不變）

投影片 1（標題）、2（Boris GIF）、3（Vibe→Agentic）、4（什麼是 Vibe Coding）、5（好 vs 壞的 Prompt）、6（目錄 —— 只更新 goToSlide 目標）。

**投影片 6 的目錄更新：**
- Agents 列：`goToSlide(7)`（原為 18）
- Skills 列：`goToSlide(13)`（原為 24）
- Context 列：`goToSlide(19)`（原為 7）
- CLAUDE.md 列：`goToSlide(25)`（原為 12）
- Commands 列：`goToSlide(30)`（原為 30 —— 不變）

---

### 第 1 章：Agents（投影片 7-12）——「這個人」

**投影片 7** —— 章節分隔（`data-level="agents"`，Topic 1）
- 標題：「Agents —— 天氣播報員」
- 說明：「代理就是 Claude 扮演某個特定角色。來認識這位天氣播報員 —— 一位受雇來抓取並播報杜拜天氣資料的專家。」

**投影片 8** ——「餐廳廚房」（現有投影片 19）
- 內容：同樣的類比（純 prompt = 對著隨便一間廚房大喊；代理 = 特定專家）
- 把代理範例全面改用「天氣播報員」的框架
- 保留比較純 prompt 與 weather-agent 的雙欄卡片

**投影片 9** ——「Prompt vs. 代理 —— 並排比較」（現有投影片 20）
- 表格完整保留。它已經很好地使用了天氣範例。

**投影片 10** ——「代理有自己的大腦」（現有投影片 21）
- 保留 Thariq 的技巧。把它連到：「天氣播報員在自己的大腦裡工作 —— 所有抓網頁的動作都不會進到你的大腦。」

**投影片 11** ——「如何建立你自己的代理」（現有投影片 22）
- 保留 `/agents` 的操作模式
- 更新程式碼區塊以顯示真實的 `weather-agent.md` 路徑

**投影片 12** ——「代理設定欄位」（現有投影片 23）
- 保留欄位表。加上一個標註框，在脈絡中展示 `skills: [weather-fetcher]` 欄位。

---

### 第 2 章：Skills（投影片 13-18）——「播報員知道什麼」

**投影片 13** —— 章節分隔（`data-level="skills"`，Topic 2）
- 標題：「Skills —— 天氣播報員知道什麼」
- 說明：「Skills 是播報員被訓練過的具體能力。我們的播報員有兩項：抓資料，以及把它畫成卡片。」

**投影片 14** ——「訓練手冊」（現有投影片 25）
- 重新框定：天氣播報員有兩項 skill：weather-fetcher（去拿溫度）與 weather-svg-creator（做出視覺卡片）。
- 把「Shayan」範例換成天氣播報員的這兩項 skill。

**投影片 15** ——「什麼時候該把某件事變成 Skill」（現有投影片 26）
- 保留 Boris 的技巧。把 weather-fetcher 與 weather-svg-creator 加進範例。

**投影片 16** ——「為什麼要把代理和 Skills 分開？」（現有投影片 27）
- 保留雙欄。更新以強調：weather-agent = 那個人，weather-fetcher = 他們受過的訓練。

**投影片 17** ——「如何建立你自己的 Skill」（現有投影片 28）
- 保留。程式碼區塊已經展示真實的 `weather-fetcher` SKILL.md 內容 —— 完美。

**投影片 18** ——「Skill 設定欄位」（現有投影片 29）
- 保留。加註：weather-fetcher 設了 `user-invocable: false`，因為它只給代理用。

---

### 第 3 章：Context（投影片 19-23）——「播報員的大腦」

**投影片 19** —— 章節分隔（`data-level="context"`，Topic 3）
- 標題：「Context —— 播報員的大腦」
- 說明：「既然你已經認識播報員也知道他們的 skills，接著來理解他們一次能真正記住多少東西。」

**投影片 20** ——「Claude 的大腦」（現有投影片 8）
- 保留。加一句連到天氣播報員：「當 weather-agent 被派出時，它會拿到自己全新的大腦 —— 而 weather-fetcher 在啟動時就被釘進去了。」
- 保留兩張圖（context-window.jpeg 留在這裡）。

**投影片 21** ——「Session 開始時載入什麼」（現有投影片 9）
- 保留。連到天氣播報員：「啟動時，Claude 只知道 weather-fetcher 的*存在*（僅 description）。當命令執行時，完整的 skill 內容才載入代理的大腦。」
- context.jpg 留在這裡。

**投影片 22** ——「保持大腦清晰」（現有投影片 10）
- 保留分歧點表格。

**投影片 23** ——「如何管理你的脈絡」（現有投影片 11）
- 保留 `/context`、`/compact`、`/clear` 的操作說明。

---

### 第 4 章：CLAUDE.md（投影片 24-29）——「隨身規則手冊」

**投影片 24** —— 章節分隔（`data-level="claude-md"`，Topic 4）
- 標題：「CLAUDE.md —— 播報員的隨身規則手冊」
- 說明：「播報員每次上班前都會翻一下 —— 即使他們的大腦每晚都會重置。」

**投影片 25** ——「員工手冊」（現有投影片 13）
- 保留。改成天氣播報員的框架：CLAUDE.md 是播報員上播前要讀的規則手冊 ——「除非被要求，一律用攝氏播報；一律註明資料來源。」

**投影片 26** ——「如何建立你的 CLAUDE.md」（現有投影片 14）
- 保留 `/init` 的操作說明。

**投影片 27** ——「每犯一次錯就讓 CLAUDE.md 長大」（現有投影片 15）
- 保留 Boris 的技巧。

**投影片 28** ——「CLAUDE.md 裡該放什麼」（現有投影片 16）
- 保留程式碼區塊。天氣播報員元素：加一段註解展示天氣專屬規則。

**投影片 29** ——「CLAUDE.md 如何載入」（現有投影片 17）
- 保留。

---

### 第 5 章：Commands + Workflow（投影片 30-36）——「扳機」

**投影片 30** —— 章節分隔（`data-level="commands"`，Topic 5）
- 標題：「Commands —— 扳機」
- 說明：「一個詞啟動整條鏈。`/weather-orchestrator` → 代理 → skill → SVG 卡片。」

**投影片 31** ——「Commands —— 進入點」（現有投影片 31）
- 保留。很好的開場，已經提到 weather-orchestrator。

**投影片 32** ——「如何建立你自己的命令」（現有投影片 32）
- 保留。程式碼區塊已經展示 weather-orchestrator.md。

**投影片 33** —— Workflow 子章節（原投影片 33，`data-level="workflow"`）
- 把章節編號文字從「Topic 6」改成「把全部串起來」
- 保留 `data-level="workflow"` 讓進度列填滿到 100%。
- 標題更新為：「Workflow —— 五個部件一起運作」
- 說明：「看天氣播報員範例如何從一次按鍵跑到 SVG 卡片輸出。」

**投影片 34** ——「Command → Agent → Skill」（現有投影片 34）
- 保留程式碼區塊的流程圖。已經很完美。

**投影片 35** ——「Skills 的兩種使用方式」（現有投影片 35）
- 保留比較預載與直接呼叫的雙欄。

**投影片 36** ——「如何接起你自己的 Workflow」（現有投影片 36）
- 保留。已經用天氣 workflow 當範例。

**投影片 37** —— 結尾（現有投影片 37）
- 保留。副標更新為：「五個概念，一個貫穿範例」
- 更新內文以呼應天氣播報員的敘事弧線。

---

## 4. 素材重用清單

| 素材 | 現有位置 | 新位置 | 動作 |
|---|---|---|---|
| `context-window.jpeg` | 投影片 8（Claude 的大腦） | 投影片 20（內容相同，重新編號） | 保留 —— 不需更動 |
| `context.jpg` | 投影片 9（Session 開始時載入什麼） | 投影片 21（內容相同，重新編號） | 保留 —— 不需更動 |
| `../../!/claude-jumping.svg` | 投影片 1、頁首 | 不變 | 無動作 |
| `../../!/root/boris-slider.gif` | 投影片 2 | 不變 | 無動作 |

兩張脈絡圖都完整保留在原位 —— 含有它們的投影片只是重新編號（8→20、9→21）。

---

## 5. 帳務性影響

### 新的章節分隔位置與 `data-level` 指派

| 投影片 | 主題 | `data-level` |
|---|---|---|
| 7 | Agents | `agents` |
| 13 | Skills | `skills` |
| 19 | Context | `context` |
| 25 | CLAUDE.md | `claude-md` |
| 30 | Commands | `commands` |
| 33 | Workflow 子章節 | `workflow` |

### 投影片 6 的目錄 `goToSlide` 目標

| 列 | 主題 | 舊目標 | 新目標 |
|---|---|---|---|
| 第 1 列 | Agents | 18 | 7 |
| 第 2 列 | Skills | 24 | 13 |
| 第 3 列 | Context | 7 | 19 |
| 第 4 列 | CLAUDE.md | 12 | 25 |
| 第 5 列 | Commands | 30 | 30 |

### 旅程刻度（不變）

旅程刻度軌已經由上到下排為：Workflow、Commands、Skills、Agents、CLAUDE.md、Context。這是敘事順序的*反向*（最上 = 最高層級 = 最後達成）。不需更動。

### LEVELS 對照表（不變）

全部 6 個層級鍵（`context`、`claude-md`、`agents`、`skills`、`commands`、`workflow`）都保留。沒有新增或移除。

---

## 6. 實作方式

HTML 是一個大檔。投影片順序與新的敘事弧線不符。最乾淨的實作方式是：

1. 剪下投影片 div 並依新順序貼上（7-12 = 舊 18-23，13-18 = 舊 24-29，19-23 = 舊 7-11，24-29 = 舊 12-17，30-37 不變）。
2. 把所有 `data-slide` 屬性依序重新編號。
3. 更新章節投影片的 `data-level` 屬性。
4. 更新章節分隔頁的章節編號文字與 h1。
5. 更新投影片 6 的目錄 `goToSlide` 目標。
6. 更新 Workflow 章節頁（舊 33）的章節編號文字。
7. 在需要處做針對性的內容編輯，改成天氣播報員的框架。

投影片總數：**37**（不變）。

---

## 7. 模糊之處 —— 沒有關鍵性的

所有模糊之處都已在上面解決。直接進入實作。
