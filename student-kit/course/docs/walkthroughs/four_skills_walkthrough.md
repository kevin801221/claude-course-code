# 四個 Skill 完整工作流 Walkthrough
## `brainstorming` × `writing-plans` × `subagent-driven-development` × `docx`

> **對象**：用過 Claude Code、想升級到「結構化開發」的工程師
> **形式**：講師現場帶、學生跟著做
> **時長**：120 分鐘
> **產出**：用這 4 個 skill 完整跑過 1 個 feature 的全流程，最後產出客戶可看的 .docx 報告
> **核心方法**：4 個 skill 不是各自獨立，是**一條接力路徑**——前 3 個是 superpowers 的工作流 SOP，最後 1 個是 document-skills 的交付格式

---

## 開場：這 4 個是什麼？為什麼要連在一起？

| Skill | 出處 | 一句話 | 在工作流的位置 |
|---|---|---|---|
| 🧠 `brainstorming` | superpowers | 寫程式前先把意圖、需求、設計搞清楚 | **第 1 棒** 探索期 |
| 📋 `writing-plans` | superpowers | 把搞清楚的東西變成可執行的多步驟計畫 | **第 2 棒** 規劃期 |
| ⚙️ `subagent-driven-development` | superpowers | 把計畫拆給多個 subagent 平行執行 | **第 3 棒** 執行期 |
| 📝 `docx` | document-skills | 用 Word 格式產正式交付文件 | **第 4 棒** 交付期 |

> **教學金句**：「Vibe coding 是『想到啥做啥』，這 4 個 skill 是『工程化的紀律』。**從一團 idea → 正式 deliverable，剛好一條路走完**。」

🔗 全部來自：https://github.com/obra/superpowers + https://github.com/anthropics/skills

---

## 📁 為什麼這條路重要？（5 分鐘黑板時間）

大部分人寫程式的流程：

```
模糊需求 → 「我先寫個 prototype」→ 寫到一半發現需求錯 → 砍掉重來
```

這 4 個 skill 強制你走：

```
模糊需求
  → 🧠 brainstorming（問清楚意圖）
  → 📋 writing-plans（寫成可審 plan）
  → ⚙️ subagent-driven-development（平行做）
  → 📝 docx（交付）
```

**每一棒都有檢查點，每一棒都可以打回**。這是「Vibe Coding 升級成 Disciplined Coding」的核心方法論。

---

## Phase 0：環境準備（5 分鐘）

### 確認 4 個 skill 都裝了

```
/help
```

或在對話打：

```
列出我裝了的 skill，含 superpowers:* 跟 document-skills:* 開頭的
```

預期看到：
```
- superpowers:brainstorming
- superpowers:writing-plans
- superpowers:subagent-driven-development
- document-skills:docx
```

### 沒有？兩條指令補裝

```
/plugin marketplace add obra/superpowers
/plugin install superpowers@superpowers

/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

重啟 Claude Code。

---

## 🧠 Skill 1: `brainstorming`（25 分鐘，全程最重要）

🔗 https://github.com/obra/superpowers/tree/main/superpowers/skills/brainstorming

### 是什麼？

一個**強制 Claude 在動手寫程式前**先跟你來回對話 7–12 輪、把意圖跟需求挖出來的 skill。

> 從 description 看：「You MUST use this before any creative work — creating features, building components, adding functionality, or modifying behavior.」

**「MUST」這個字眼是關鍵**——這是 superpowers 的鐵則：**任何要產出新東西的對話、開頭都應該 brainstorm**。

---

### 為什麼要用？

未經 brainstorm 的開發 = Claude 自己幻想需求 = 你拿到不要的東西

| 場景 | 不 brainstorm | brainstorm 後 |
|---|---|---|
| 「幫我蓋一個登入頁」 | Claude 出標準 email/password 表單 | Claude 問你：要 SSO 嗎？要 magic link 嗎？密碼規則？要不要 OAuth？ |
| 「加個 dark mode」 | Claude 加 toggle + 改 CSS | Claude 問：跟 system 連動嗎？只首頁還是全站？localStorage 還是 cookie？ |

> **教學金句**：「Brainstorming 不是浪費時間——**它把『重做一次』的成本攤到對話前面**。」

---

### 使用流程（一步一步）

#### Step 1：對 Claude 表達你要做什麼

別寫太細，就丟個 idea。

```
我想加一個 wafer prediction 的歷史紀錄頁面
```

#### Step 2：Claude 會主動引用 `brainstorming` skill

你會看到：
```
Using brainstorming to explore user intent and requirements
```

#### Step 3：Claude 開始問問題（這是核心）

典型 7–12 輪會問：
1. **誰會用這頁？**（工程師除錯 / PM 看趨勢 / 客戶查詢）
2. **「歷史」的時間範圍多久？**（1 天 / 1 週 / 永久）
3. **每筆紀錄要顯示什麼？**（image / bbox / confidence / mAP）
4. **可以篩選嗎？**（按日期 / 信心度 / 類別）
5. **要分頁還是無限滾動？**
6. **資料從哪來？**（資料庫 / log 檔 / API）
7. **要可匯出嗎？**（CSV / PDF）
8. **行動裝置要 work 嗎？**
9. **資料量預估**（10 筆 / 1k 筆 / 1M 筆）
10. **未來會延伸出什麼？**（誰可能想要新功能）

每題你回 1–2 句。

> ⚠️ **必踩坑**：很多人嫌煩想跳過，回「你都決定就好」。**這會讓 brainstorm 失去意義**。乖乖回答。

#### Step 4：Claude 產出 brainstorm 摘要

對話 7–12 輪後，Claude 會輸出類似：

```markdown
## Brainstorm 摘要

### 目標
做給 PM 看趨勢用的歷史頁。

### 範圍
- 過去 30 天
- 顯示縮圖 + confidence + 預測類別
- 可按日期 / 信心度 filter
- 分頁，每頁 20 筆
- 桌面為主、手機可看

### 不在範圍
- 不需要匯出 CSV（PM 用截圖就好）
- 不需要編輯 / 刪除（read-only）
- 不需要登入

### 假設與風險
- 假設資料量 < 10k 筆（先不分區）
- 風險：縮圖一次 20 張可能慢 → 用 lazy load
```

#### Step 5：你決定下一步

3 條路：
- ✅ **方向對** → 進 `writing-plans`
- 🔄 **某些需求要改** → 直接說，Claude 再 brainstorm 一輪
- ❌ **整個方向不對** → 重來

---

### 範例 prompt（你可以直接複製測）

```
用 brainstorming skill 幫我搞清楚：
我想加一個「wafer detection 歷史紀錄」頁面到 demo dashboard。
我自己也只有個模糊概念，請帶我釐清需求。
```

---

### 常見錯誤

| 錯誤 | 後果 | 正確做法 |
|---|---|---|
| 跳過 brainstorm 直接寫程式 | 寫錯方向 | 強制自己跑這 skill |
| 問題敷衍回答 | brainstorm 失去意義 | 認真想，回不知道也要回「不知道」 |
| brainstorm 完馬上叫 Claude 寫 code | 跳過 `writing-plans` 棒 | 強制接 `writing-plans` |

---

## 📋 Skill 2: `writing-plans`（25 分鐘）

🔗 https://github.com/obra/superpowers/tree/main/superpowers/skills/writing-plans

### 是什麼？

把 brainstorm 出來的「需求」**翻成結構化、可審查、可執行**的多步驟 plan。

> description：「Use when you have a spec or requirements for a multi-step task, before touching code」

關鍵字：**before touching code**。

---

### 它跟一般的 TodoList 差在哪？

| | TodoList | writing-plans 產的 plan |
|---|---|---|
| 內容 | 「做 X」、「做 Y」 | 每步含**做什麼 / 為什麼 / 怎麼驗證 / 哪些檔案會動** |
| 用途 | 給自己看 | 給人類 review、給 subagent 接手 |
| 格式 | 隨意 | 固定結構（spec 級） |
| 進入下一步 | 跳就跳 | **建議 checkpoint，每步做完 review** |

---

### 使用流程

#### Step 1：接 brainstorm 的結果

```
Brainstorm 出來的需求看起來對了，用 writing-plans skill 寫成計畫
```

#### Step 2：Claude 引用 `writing-plans`，產出 plan.md

典型輸出（簡化版）：

```markdown
# Plan: Wafer Detection History Page

## Goal
給 PM 看趨勢的歷史頁。

## Architecture overview
- Next.js page at `/history`
- 資料來源：`Projects/.../05-results/predictions/*.json`
- 用 server-side pagination

## Step 1: 定義資料 schema
- 看現有 inference 輸出格式
- 確認欄位：image_path, bbox, confidence, class, ts
- **驗證**：手動 cat 一個 .json 確認

## Step 2: 寫 API endpoint
- File: `app/api/predictions/route.ts`
- GET /api/predictions?from=&to=&conf_min=&page=
- **驗證**：curl 一次拿到 JSON

## Step 3: 寫 UI 頁面
- File: `app/history/page.tsx`
- 用 shadcn/ui Table + Pagination
- 縮圖用 next/image lazy load
- **驗證**：跑 localhost:3000/history 看畫面

## Step 4: 加 filter
- 日期 picker + confidence slider
- URL state 同步（用 nuqs 或自己處理）
- **驗證**：filter 一次、reload 還在

## Step 5: 寫 tests
- API route test（vitest）
- 一個 e2e（webapp-testing skill）
- **驗證**：CI green

## Open questions
- [ ] 縮圖放 public/ 還是 S3？
- [ ] 30 天前的資料要保留嗎？

## Out of scope
- 編輯/刪除
- 匯出 CSV
- 登入
```

#### Step 3：你 review 這份 plan

這就是「**人類在 loop**」的位置：
- 哪步邏輯不對？
- 哪步遺漏？
- 哪步可以平行？

#### Step 4：plan 通過 → 進下一棒

---

### 為什麼這份 plan 這麼有威力？

因為 `subagent-driven-development` 直接吃它。**每個 Step 可以變成一個 subagent 的任務**。

> **教學金句**：「Plan 寫得好不好，下一棒 subagent 就有沒有命。**這份 plan = subagent 的合約。**」

---

### 範例 prompt

```
brainstorm 的結論我已經確認。用 writing-plans skill 寫成詳細計畫，
存到 _Plans/history_page_plan.md。
```

---

## ⚙️ Skill 3: `subagent-driven-development`（30 分鐘，本場高潮）

🔗 https://github.com/obra/superpowers/tree/main/superpowers/skills/subagent-driven-development

### 是什麼？

把 `writing-plans` 產的計畫，**找出可平行的步驟**、**派給多個 subagent 同時做**，主對話只負責協調。

> description：「Use when executing implementation plans with independent tasks in the current session」

關鍵字：**independent tasks**（彼此沒依賴的任務）。

---

### 跟 sub-agent（`/agents`）差在哪？

容易混！

| | sub-agent（`/agents` 蓋的） | subagent-driven-development |
|---|---|---|
| 是什麼 | 一個**有名字、可重用**的 AI 角色（如 data-hunter） | 一個**執行策略**（讓 Claude 平行派任務） |
| 何時建立 | 開發前一次性建好 | 執行 plan 當下動態派 |
| 數量 | 固定（4 個、5 個...） | 看 plan 有幾個獨立任務 |
| 持久 | `.claude/agents/*.md` | 跑完就消失 |

> **教學金句**：「`/agents` 是『建立分身』，`subagent-driven-development` 是『派分身一起做』。**前者是名詞，後者是動詞**。」

---

### 使用流程

#### Step 1：拿著 plan 引用 skill

```
plan 已經 review 過。用 subagent-driven-development skill 執行，
能平行的就平行。
```

#### Step 2：Claude 引用 skill，產出**執行藍圖**

Claude 會說：
```markdown
## 執行計畫

### 平行批次 1（彼此獨立，3 個 subagent 同時跑）
- subagent A: Step 1 定義 schema
- subagent B: Step 2 寫 API endpoint
- subagent C: Step 3 寫 UI 骨架（先用 mock data）

### 平行批次 2（等批次 1 跑完）
- subagent D: 接 B+C，整合 API 到 UI
- subagent E: Step 4 加 filter（看完整 UI 後加）

### 序列：Step 5 寫 tests（全部 done 之後）

確認執行？(y/n)
```

#### Step 3：你確認 → Claude 真的派出 3 個 subagent 平行跑

你會看到對話分頁式顯示，每個 subagent 進度不同。

> 💡 **這跟你用 sub-agent 平行跑訓練實驗的概念一樣**——只是這裡 subagent 是動態派的。

#### Step 4：每批跑完，Claude 收成結果繼續下一批

#### Step 5：全部跑完，Claude 給你 summary

```markdown
## 執行結果

✅ Step 1: schema 定義完成（app/types/prediction.ts）
✅ Step 2: API endpoint 完成（app/api/predictions/route.ts）
✅ Step 3: UI 骨架完成（app/history/page.tsx）
✅ Step 4: filter 加上（含 URL state）
✅ Step 5: tests 全 pass

📊 平行化效益：
- 序列估算: 60 分鐘
- 實際: 25 分鐘（節省 58%）

## 下一步
建議：用 webapp-testing skill 跑一次 e2e
```

---

### 何時不該用？

| 場景 | 建議 |
|---|---|
| 任務都有強依賴（A 要先 → B 才能 → C 才能） | 序列做就好，別 forced 平行 |
| 任務超小（< 5 分鐘各） | 派 subagent 的開銷比執行還貴 |
| 任務涉及 shared state（同一個檔案多人改） | 序列做，避免 conflict |

---

### 範例 prompt

```
這份 _Plans/history_page_plan.md 已經 review 完。
用 subagent-driven-development 執行，列出平行批次後跟我確認再跑。
```

---

### 注意事項

1. **不要對「需要互動」的任務用** — subagent 不會問你問題，缺資訊就會卡或猜
2. **每個 subagent 任務描述要自含** — 它看不到主對話脈絡
3. **批次間要有 checkpoint** — 第 1 批跑完先 review 再進第 2 批

---

## 📝 Skill 4: `docx`（25 分鐘）

🔗 https://github.com/anthropics/skills/tree/main/skills/docx

### 是什麼？

完整的 .docx 工具包——生成、編輯、保留格式、tracked changes、註解、文字抽取。

> description：「Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction」

關鍵字：**formatting preservation**——這是 docx skill 最值錢的功能。

---

### 為什麼放在工作流最後？

因為：「**寫程式的人最不會做的事就是寫 deliverable 文件給非工程同事看**。」

當你跑完 brainstorm → plan → 平行執行，你會有：
- 一份完整 plan.md
- 一個能 work 的 feature
- 一些測試結果

**但 PM / 老闆 / 客戶要的不是 .md，是 .docx**（要有公司格式、字型、頁碼、表格）。docx skill 補這個 gap。

---

### 使用流程

#### Step 1：給 Claude 你的原料 + 模板（可選）

```
請用 docx skill 把以下內容變成正式報告：

## 內容（從 plan 跟結果摘出）
- Feature: History page
- Tech stack: Next.js, shadcn/ui
- 開發時間: 25 分鐘（用 subagent-driven-development 平行）
- Test coverage: 85%
- 截圖：[3 張 PNG attach]

## 公司模板
internal_report_template.docx（保留封面、頁眉頁尾、配色）
```

#### Step 2：Claude 引用 `docx`，寫 python-docx 腳本

預期看到 Claude 跑：
- 讀模板抽 style（heading 1 / heading 2 / 表格樣式）
- 用 python-docx 填入內容
- 圖片插入並調整尺寸
- 產出 `report_v1.docx`

#### Step 3：Word 打開驗一次

- 樣式跟模板一致？
- 表格沒亂掉？
- 圖片解析度夠？
- 頁碼正確？

#### Step 4：要老闆改？加 tracked changes 或 comments

```
docx skill 在現有 report_v1.docx 加 tracked changes：
- 把「25 分鐘」改成「23 分鐘」
- 在「Test coverage」段加 comment：「想加 1 個 e2e」
存 report_v2.docx
```

老闆用 Word 「審閱」可以接受/拒絕你的改。

---

### 範例 prompt

```
用 docx skill 把這次 history page 的開發成果寫成正式 deliverable：
- 引用模板 templates/proposal_template.docx
- 章節：背景、需求（從 brainstorm 摘）、設計（從 plan 摘）、實作、測試、下一步
- 加 3 張截圖（assets/sc_1.png, sc_2.png, sc_3.png）
- 表格：開發時程（plan 的 Step 1–5 + 預計/實際時間）
- 存 deliverables/history_page_report.docx
```

---

### docx 的潛規則（必講）

1. **不要從零生 .docx**——永遠基於模板，否則樣式很醜
2. **圖片插入要明說尺寸**——python-docx 預設原始大小，常常超頁
3. **表格 style 要套既有的**（`'Light Grid Accent 1'` 等），不要自己畫
4. **tracked changes 要先 enable**——`document.settings.track_revisions = True`
5. **不要編輯後重存覆蓋**——存到新檔，留 backup

---

## 🎬 整合 demo：4 個 skill 接力跑完 1 個 feature（30 分鐘）

### 場景

「PM 說：『加個 wafer detection 歷史頁讓我看趨勢』」

### Step 1：開場 brainstorming

```
PM 要一個 wafer detection 歷史頁。用 brainstorming skill 帶我釐清需求。
```

→ 10 輪對話 → brainstorm 摘要產出

### Step 2：寫成 plan

```
brainstorm 確認。用 writing-plans 寫成 _Plans/history_page_plan.md。
```

→ 5 個 Step plan，每個都標可平行或序列

### Step 3：平行執行

```
plan review 完。用 subagent-driven-development 執行。
```

→ 派 3 個 subagent 平行做 Step 1–3，Step 4 序列接，Step 5 收尾

### Step 4：產 deliverable

```
用 docx skill 把這次的成果寫成 PM 報告：
- 模板 templates/internal_report.docx
- 章節：需求 / 設計 / 結果 / 截圖
存 deliverables/history_page_v1.docx
```

### 預期時間
- brainstorm: 15 分鐘
- writing-plans: 10 分鐘
- subagent-driven-development: 30 分鐘（平行省一半）
- docx: 10 分鐘
- **總計：65 分鐘從 idea 到 deliverable**

對比未用 skill 的隨意做法：通常要 3–4 小時，而且方向會錯一次重做。

---

## 卡點對照表

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| Claude 沒主動引用 `brainstorming` | 你直接叫它「寫程式」太快了 | 明說「用 brainstorming skill 釐清」 |
| brainstorm 問題太多想跳過 | 你以為自己想清楚了 | **乖乖回答**，第 8 題以後常常爆出你沒想到的 |
| `writing-plans` 出來的 plan 太抽象 | brainstorm 沒做夠 | 回上一棒再 brainstorm 一輪 |
| `subagent-driven-development` 把序列任務硬平行 | 你 plan 沒標清楚依賴 | 明寫「Step 2 要 Step 1 完成才能做」 |
| subagent 跑到一半問問題沒人回 | subagent 不能跟主對話互動 | 任務描述要含所有資訊 |
| `docx` 出來的格式爛 | 沒給模板 | **永遠基於模板**，不要從零 |
| `docx` 圖片爆出邊界 | python-docx 預設原始尺寸 | 明說「圖片寬度 6 inches」 |
| 4 個 skill 都沒裝 | 沒裝 superpowers / document-skills marketplace | 看 Phase 0 |
| 用 `subagent-driven-development` 反而更慢 | 任務太小 / 依賴太強 | 短任務序列做，別硬塞平行 |

---

## 講師私房筆記

### 1. 教學順序的心法

| 順序 | 為什麼 |
|---|---|
| brainstorming 第一 | 沒這步，後面全錯 |
| writing-plans 第二 | 沒 plan 沒辦法 subagent |
| subagent-driven-development 第三 | 高潮表演，最有感 |
| docx 收尾 | 學生看到 deliverable 出來會驚 |

### 2. 故意踩坑

**踩坑 1**：跳過 brainstorm 直接寫
- Claude 出個版本
- 故意說「啊我其實要 X 不是 Y」
- 重做一次
- 帶學生算：「剛剛白做 15 分鐘 = 你少 brainstorm 5 分鐘的代價」

**踩坑 2**：plan 寫太抽象
- 故意只寫「Step 1: 做 UI」
- subagent-driven-development 派出去 → subagent 不知道要做啥
- 「看到沒？plan 的細節是合約」

### 3. 給不同學員的選擇建議

| 學員背景 | 一定要學 |
|---|---|
| 新手工程師 | brainstorming + writing-plans（最缺紀律） |
| 資深工程師 | subagent-driven-development（最缺平行思維） |
| PM/設計師 | brainstorming + docx（最缺工程結構 / 最需要 deliverable） |
| 自由接案 | 4 個都要（從 brief 到交付一條龍） |

### 4. 真實工作上一定會發生的事

- **brainstorm 中途客戶改需求** → 重 brainstorm，不是繼續硬寫
- **plan 半路發現有大遺漏** → 回 writing-plans 補，不是邊寫邊塞
- **subagent 平行做出衝突** → 主對話收成時做 merge，不是讓 subagent 互相讓
- **docx 給老闆改回來** → 用 tracked changes 接受/拒絕，不是手動再貼

### 5. Kevin 私房用法

- 我幾乎**所有功能開發**都用這條路
- 例外：「改 1 個 typo」、「rename 1 個 var」——這種不需要 brainstorm
- 標準：**任何要動 3 個檔案以上的，都跑全套**

---

## 一句話總結

> **這 4 個 skill 是「Vibe Coding → 工程化開發」的 4 個閘門：
> 🧠 想清楚 → 📋 寫清楚 → ⚙️ 做有效率 → 📝 交付給人類。
> 每個閘門都可以打回，但**絕不省略**。**

---

## 進階閱讀

- 🔗 [Superpowers GitHub](https://github.com/obra/superpowers)
- 🔗 [Anthropic Skills GitHub](https://github.com/anthropics/skills)
- 🔗 brainstorming skill 原始檔：https://github.com/obra/superpowers/tree/main/superpowers/skills/brainstorming
- 🔗 writing-plans skill 原始檔：https://github.com/obra/superpowers/tree/main/superpowers/skills/writing-plans
- 🔗 subagent-driven-development 原始檔：https://github.com/obra/superpowers/tree/main/superpowers/skills/subagent-driven-development
- 🔗 docx skill 原始檔：https://github.com/anthropics/skills/tree/main/skills/docx

---

_Last updated: 2026-05-12_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材（同目錄）：`hook_walkthrough.md`（hooks）+ `anthropics_marketplace_skills_walkthrough.md`（skills marketplace）_
_專案實戰案例：`../../agent_group_projects/computer-vision-wafer-agents-detection-demo/WALKTHROUGH.md`（sub-agents）_
