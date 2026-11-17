# Matt Pocock AI PM 技能體系 Walkthrough — 28 萬星 Spec 驅動開發、證據 PR 與閉環復盤

> **對象**：技術 PM、團隊 Tech Lead、架構師，以及厭倦了 AI 程式碼「Vibe Coding（盲寫）」與 PR 審查地獄的資深工程師
> **形式**：講師現場教學 / 團隊工程規範導入 / 自學
> **時長**：60 分鐘（精華版 40 分鐘 + 實戰 20 分鐘）
> **產出**：
> 1. 理解並掌握 Matt Pocock 突破 28 萬星開源技能庫（`mattpocock/skills` v1.3）的底層設計邏輯
> 2. 實裝三大核心技能：`/implement-spec`（相依感知並行派工）、`/pr`（證據導向 PR）、`/retro`（修環境復盤）
> 3. 學會專案領域建模升級：將舊版 `CONTEXT.md` 無痛升級至 `GLOSSARY.md`
> **核心方法**：打破「把 AI 當打字員一張張派工」的舊模式，建立「**Ticket Graph 並行施工 ＋ 三層防線審查 ＋ 修環境不修程式**」的現代 AI PM 工作流
> **參考來源**：[Gary Chen 拆解影片（YouTube: QqhyqMvdx5Q）](https://www.youtube.com/watch?v=QqhyqMvdx5Q) 與 Matt Pocock 原生規範

---

## 開場（5 分鐘）：AI 時代 PM 與工程主管的兩大絕症

當團隊開始全面引進 Claude Code 或 AI Coding Agent，通常不到一個月就會撞上兩堵大牆：

1. **實作瓶頸（單兵效率上限）**：PM 寫好詳細規格，AI 卻只能「一張工單做完才做下一張」，遇到 10 個無相依性的任務還是排隊循序進行，人類成了在終端前按 Enter 的無情開車員。
2. **PR 審查地獄（Review Hell）**：AI 產能無限廉價，一天提交 30 個 PR，每個 PR 幾百行。人類審查者根本看不完，只能粗暴 Approve，導致暗藏架構債的「垃圾代碼」迅速腐化 codebase。
3. **金魚腦反覆犯錯**：AI 踩過的坑，下次 session 忘得一乾二淨。工程師習慣在 prompt 裡加一句「不要重複錯誤」，結果提示詞越來越冗長，AI 依然故我。

| 傳統 Vibe Coding 模式 | Matt Pocock AI PM 方案（v1.3） | 解決的根本問題 |
|---|---|---|
| 單工單串行作業，人盯著螢幕點確認 | **`/implement-spec`** 讀 Ticket Graph 並行派工 | 把「順序等候」變成「多 Sub-agent 並行開工」 |
| PR 寫得籠統，缺乏驗證證據 | **`/pr`** 證據導向 ＋ 單向門/雙向門分級 | 建立三層防線，人類只把專注力放在高風險決策 |
| 踩坑後只在對話口頭罵 AI | **`/retro`** 閉環復盤，修環境不修程式 | 將教訓固化為 `rules`、`hooks` 或 `GLOSSARY.md` |
| 專案術語定義混亂易與上下文搞混 | **`GLOSSARY.md`** 領域統一語言（Breaking Change） | 建立人類與 Agent 共用的領域模型 |

> **教學金句**：「**在 AI 產能無限廉價的時代，好的 PM 方案不是讓 AI 寫更多代碼，而是『約束 AI 怎麼施工、證明它沒寫爛、並把經驗沉澱進環境』。**」

---

## 📁 AI PM 工作流核心架構

```
需求發想 / 訪談
       │
       ▼
【GLOSSARY.md】 ─── 統一領域名詞（禁止模糊代名詞）
       │
       ▼
【SPEC.md 規格書】 ─── 包含任務清單與相依性關係（Ticket Graph）
       │
       ▼
【/implement-spec】 ─── 解析 Unblocked 任務，多 Sub-agents 並行施工
       │
       ▼
【/pr】 ─── 生成架構圖 + 前後對比證據 + 單向門/雙向門風險分級
       │
       ▼
【/retro】 ─── 復盤 Token 與效率瓶頸，把規則沉澱回專案設定與 Hook
```

---

## Phase 0：環境準備與 Breaking Change 遷移（10 分鐘）

### 1. 關鍵破壞性變更（Breaking Change）：`CONTEXT.md` → `GLOSSARY.md`

Matt Pocock 在 v1.3 正式將原本的 `CONTEXT.md` 更名為 `GLOSSARY.md`（詞彙辭典），並將領域對照圖命名為 `GLOSSARY-MAP.md`。

* **為什麼要改名？** 「Context」在 LLM 領域通常指「上下文窗口（Context Window）」，容易產生概念混淆。改為「Glossary」明確代表領域驅動設計（DDD）中的「通用語言（Ubiquitous Language）」。
* **舊專案遷移指令**：
  ```bash
  # 如果你的專案過去有 CONTEXT.md，請立即更名：
  git mv CONTEXT.md GLOSSARY.md
  # 若有地圖文件：
  git mv CONTEXT-MAP.md GLOSSARY-MAP.md 2>/dev/null || true
  ```

### 2. 安裝與啟用 Matt Pocock 專屬技能庫（三種方式）

Matt Pocock 提供了正式的專屬技能庫（GitHub: `mattpocock/skills`），支援以下三種安裝方式：

#### 途徑 A：透過 Agent Skills CLI（推薦，一鍵安裝至專案）
```bash
# 直接將 Matt Pocock 的完整技能庫加入專案 .agents/skills/ 或 .claude/skills/
npx skills@latest add mattpocock/skills
```

#### 途徑 B：透過 Claude Code Plugin 體系
```bash
# 在 Claude Code 終端中執行安裝
/plugin install mattpocock-skills
```

#### 途徑 C：本教學專案內建版（無需聯網即可使用）
本教學 Repo 已直接在 `.claude/skills/` 內建核心技能：
- `.claude/skills/ask-matt/`：技能總管與情境導航路由
- `.claude/skills/to-spec/`：無痛訪談轉 PRD 規格
- `.claude/skills/to-tickets/`：垂直切片與相依圖 Ticket 拆解
- `.claude/skills/implement-spec/`：相依感知多 Agent 並行實作
- `.claude/skills/pr/`：架構圖 ＋ 證據 ＋ 單向門/雙向門評估
- `.claude/skills/retro/`：工作階段復盤與環境處方


---

## Phase 1：`/implement-spec` ⭐ 帶相依感知的並行施工隊

### 心智模型：誰來當這個 `for` 迴圈？
以前開發者面對 10 個任務，需要手動對 Claude 說：「現在做 Task 1」、「現在做 Task 2」。  
`/implement-spec` 讓 Claude 自主讀取 `SPEC.md` 中的 Task 相依關係（DAG），找出**所有未被前置任務卡住的獨立工作（Unblocked Tasks）**，同時喚起多個 Sub-agents 並行處理！

### 實戰示範 SPEC 格式
在專案根目錄建立 `SPEC.md`：

```markdown
# 功能規格：使用者導覽模組

## 任務清單與相依性
- [ ] Task 1: 定義導覽列資料模型與 TypeScript 介面 (Blocked by: None)
- [ ] Task 2: 實作後端 API /api/nav (Blocked by: Task 1)
- [ ] Task 3: 前端 Navbar 靜態 UI 切版 (Blocked by: Task 1)
- [ ] Task 4: 編寫單元測試用例 (Blocked by: Task 1)
- [ ] Task 5: 前後端資料整合與 E2E 驗證 (Blocked by: Task 2, Task 3)
```

### 執行過程
終端輸入：
```bash
> /implement-spec SPEC.md
```

1. Claude 讀取任務圖，判定 Task 1 是唯一前置。
2. Task 1 完成後，Claude 立即偵測到 Task 2、Task 3、Task 4 同時解除鎖定（Unblocked）。
3. Claude 自動生成 3 個 Sub-agents 並行施工，各自擁有獨立上下文，避免單一對話 token 爆炸。
4. 當 Task 2 與 Task 3 回報完成，自動解鎖 Task 5 進行收斂。

> **教學金句**：「`/implement-spec` 把工程師從『點單員』提升為『工頭』——你定義好施工圖與相依性，Claude 調度並行工班自己把地基打完。」

---

## Phase 2：`/pr` ⭐ 證據導向 PR 與風險分級

### 痛點：AI 產能爆發後的「PR 塞車地獄」
過去 AI 寫 PR 描述：「Updated navigation and added tests.」審查者根本不知道哪裡有危險。

`/pr` 強制要求產出三大塊結構化證據：

```markdown
# PR: 新增使用者導覽系統

## 1. 架構摘要圖（Diagram）
```mermaid
graph LR
  User -->|Request| NavbarUI
  NavbarUI -->|Fetch| ApiNav[/api/nav]
  ApiNav --> DB[(User Prefs)]
```

## 2. 變更證據（Evidence）
- [x] 單元測試全綠：`uv run pytest tests/test_nav.py`（9 passed in 0.42s）
- [x] 實際終端輸出證據：
  ```text
  GET /api/nav 200 OK - 14ms
  ```
- [x] 前後效能對比：LCP 由 1.4s 微降至 1.35s，無記憶體洩漏。

## 3. 風險分級（門的類型）
- 🚪 **雙向門（Two-Way Door）**：UI 樣式與按鈕排列（隨時可透過 CSS 調整回滾）。
- 🚨 **單向門（One-Way Door）**：DB Schema 新增 `nav_preferences` 欄位（不可逆遷移，請資深架構師重點審查此處）。
```

### 三層防線架構
1. **第一層（機械防線）**：CI / Pre-commit Hook / Linter 自動通過。
2. **第二層（AI 預審）**：Claude 根據 SPEC 與 Diff 自我檢查邊界情況。
3. **第三層（人工審查）**：人類 Reviewer **只看單向門（One-Way Door）與 Evidence 區塊**，3 分鐘內做出關鍵決策！

> **教學金句**：「別讓人類 Reviewer 去數括號或看瑣碎 code。告訴他哪扇門是單向門，把人類的智慧留給不可逆的架構決策。」

---

## Phase 3：`/retro` ⭐ 閉環復盤：修環境，不修程式

### 心智模型：為什麼不要在 Prompt 裡空喊？
當 AI 在開發時把資料庫連線搞砸了 3 次，一般人的做法是在下一次 prompt 補一句：「請記住千萬別弄錯連線」。這是無效的，只會讓 Prompt 肥大。

Matt Pocock 的哲學：**「修環境，不修程式（Fix the environment, not the code）」**。

### 執行復盤
```bash
> /retro
```

Claude 會分析本次 Session 的對話日誌：
1. **Token 浪費點**：哪次搜尋撈了整個 `node_modules` 或 `build/`？
2. **無效迴圈**：哪個測試失敗了 4 次才改對？
3. **環境處方**：
   - 「建議在 `.gitignore` 補上快取目錄」
   - 「建議在 `.claude/hooks/guard-secrets.sh` 加上攔截規則」
   - 「建議在 `GLOSSARY.md` 明確定義 `TenantID` 與 `OrgID` 的差別」

執行 `/retro` 後，Claude 會直接產出規則修訂方案，確認後直接寫入專案環境設定！

---

## 整合 Demo：一個需求從規格到落地的完整 20 分鐘演練

```bash
# 1. 建立或檢查領域術語
cat GLOSSARY.md

# 2. 撰寫需求與相依圖 SPEC.md
cat SPEC.md

# 3. 啟動並行施工
claude
> /implement-spec SPEC.md

# 4. 驗收完成後產出高信任度 PR
> /pr

# 5. 開發收尾，沉澱環境規則
> /retro
```

---

## 卡點對照表 ⭐

| 卡點 | 真實原因 | 現場秒救方案 |
|---|---|---|
| 找不到 `CONTEXT.md` | v1.3 已正式更名為 `GLOSSARY.md` | 執行 `git mv CONTEXT.md GLOSSARY.md` 即可相容 |
| `/implement-spec` 依然一個一個做 | `SPEC.md` 中沒有明確標註 `Blocked by: ...` | 檢查 Task 列表，確保每項都有明確的相依性標記 |
| Sub-agents 互相覆寫檔案 | 並行任務修改了同一個檔案的重疊區域 | 拆分 Task 邊界，讓並行任務分別負責獨立模組或資料夾 |
| `/pr` 輸出的 Evidence 太空泛 | 提示詞未強制要求貼上終端執行指令與 output | 在 command 樣板中設定 HARD-GATE：必須附上測試指令與成功 exit code |
| `/retro` 沒有給出具體改進建議 | 工作階段太短或未發生顯著摩擦 | 在大規模重構或跨模組開發後執行，效果最顯著 |

---

## 講師私房筆記

### 1. 教學對象心理掌握
- **技術 PM 與主管**：他們不關心語法細節，最關心的是「專案會不會失控」、「人類審查會不會崩潰」。展示 `/pr` 的**單向門/雙向門**分類，他們會立刻明白這套方案的商業價值。
- **資深工程師**：他們最討厭「Vibe Coding 寫出屎山」。重點強調 Matt Pocock 的原則是「小而可組合、由規格與測試焊死邊界」，展示與 Clean Code 的完美契合。

### 2. 故意踩坑設計
- 現場故意在 `SPEC.md` 把所有任務都標為 `Blocked by: Task 1`，讓學員看見 Task 1 完成那一瞬間，終端同時開出 3 個 sub-agents 並行推進的震撼畫面。
- 故意不寫 `GLOSSARY.md`，讓 AI 把專案中的「客戶」與「使用者」混淆，再補上詞彙辭典看 Claude 瞬間對齊術語。

---

## 一句話總結

> **Matt Pocock 的 AI PM 方案不是為了加速打字，而是建立一套「相依感知派工、證據標定風險、復盤固化環境」的工業級防護體系，讓團隊在 AI 爆發期既有極速產能、又有穩健架構。**

---

## 配套教材與進階閱讀

- 🔗 [Gary Chen YouTube 拆解影片：28 萬星的 Matt Pocock skill 更新拆解！](https://www.youtube.com/watch?v=QqhyqMvdx5Q)
- 🔗 [`docs/walkthroughs/course_12hr_walkthrough.md`](course_12hr_walkthrough.md) — 12 小時完整課帶課教案
- 🔗 [`docs/walkthroughs/karpathy_skills_walkthrough.md`](karpathy_skills_walkthrough.md) — Karpathy 4 原則行為規範
- 🔗 [`Projects/09-timetrace/WALKTHROUGH.md`](../../Projects/09-timetrace/WALKTHROUGH.md) — 全組件一鏡到底 SaaS 實戰
- 🔗 [Matt Pocock GitHub 技能庫官方存儲庫](https://github.com/mattpocock/skills)

---

_Last updated: 2026-10-24（整合 Matt Pocock v1.3 核心技能更新與 Gary Chen 影片架構精華）_  
_Maintainer: Kevin ([@kevin801221](https://github.com/kevin801221))_
