# Course Factory — 教學課程開發 AI 團隊建構 Walkthrough

> **本份是什麼**：用 AI Agent 團隊自動產出教學課程（大綱／投影片／程式碼／評量／講師備忘）的完整建構指引。
> **對象**：Kevin（課程開發者）、或任何想複製這套系統的講師。
> **特色**：**自我增生版** —— 這套系統產出的第一堂課，就是「**教別人怎麼建這套系統**」。
> **產出**：4 個 sub-agent + 5 個 skill + 完整 `_Context/` 教學 DNA。

---

## 為什麼這份 walkthrough 跟 wafer 那份不一樣？

你已經跑過 [wafer-agents 範例](../computer-vision-wafer-agents-detection-demo/WALKTHROUGH.md)。
那份示範的是「**特定領域**的 agent 團隊」（晶圓瑕疵偵測，只能做這件事）。

這份完全不同：

| | Wafer Agents | Course Factory |
|---|---|---|
| 範圍 | 一個 ML pipeline | **任何**教學課程主題 |
| Agent 職責 | 寫死流程（抓資料→訓練→推論） | 主題無關（topic-agnostic） |
| Context 角色 | 領域知識（wafer pattern） | **教學 DNA**（哲學/受眾/風格） |
| 重用性 | 只能做 wafer | 換 `_Context/` 就能換主題 |
| 抽象層級 | 工具型 agent | **設計型 agent** |

**核心心法**：
> Wafer 的 agent 是「**做某件事**」的工具；
> Course Factory 的 agent 是「**用某種哲學做事**」的設計師。
> 後者更接近真實工程化 AI 團隊。

---

## 🧬 自我增生（Self-Replicating）是什麼意思？

不是「AI 自動寫課人類不做事」——這做不到也不該追求。

**真正的自我增生**：
1. 你用這套系統開發**第一堂課**：「給 PM 看的 LangGraph 入門」
2. 第二堂課可以是：「**怎麼用 Claude Code 建一套課程開發 AI 團隊**」← 教學內容就是這份 walkthrough 本身
3. 第三堂課：你過去 36 小時三部曲的任何一章，丟主題給 agent 直接產出
4. 第 N 堂課：學生學完用同一套系統建他自己的教學工作區，**系統開始繁殖**

這就是「**教材自我增生**」：
- 工具產出內容
- 內容教人用工具
- 學生用工具產出新內容
- 新內容繼續教人

---

## 📐 整體架構藍圖

```
                  ┌──────────────────────┐
                  │   你（課程總設計）    │
                  └──────────┬───────────┘
                             │ 單點互動（不用同時應付 4 個 agent）
                             ▼
                  ┌──────────────────────┐
                  │  主小隊長 (CLAUDE.md) │
                  │  讀 _Context/ 做路由  │
                  └──────────┬───────────┘
                             │ 委派
      ┌──────────────┬───────┴───────┬──────────────┐
      ▼              ▼               ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│curriculum│   │ slide-   │   │  code-   │   │assessment│
│-architect│   │ designer │   │ crafter  │   │-designer │
│   🟣      │   │    🔵     │   │    🟢     │   │    🟡     │
│ 大綱目標 │   │ 投影片   │   │ 範例程式 │   │ 練習評量 │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
      │              │               │              │
      └──────────────┴───────┬───────┴──────────────┘
                             │ 共用底層
                             ▼
                  ┌──────────────────────┐
                  │      Skills 層       │
                  │  outline-design      │
                  │  slide-content       │
                  │  code-example        │
                  │  exercise-gen        │
                  │  marp-render         │
                  └──────────┬───────────┘
                             │ 動態載入
                             ▼
                  ┌──────────────────────┐
                  │   _Context/ 教學 DNA  │
                  │  teaching-philosophy │
                  │  audience-profiles   │
                  │  slide-design-rules  │
                  │  code-style-guide    │
                  │  assessment-philosophy│
                  └──────────────────────┘
```

### 設計核心 3 條原則

1. **Agent 主題無關**：`curriculum-architect.md` 裡**不應該**出現「LangGraph」「Cursor」「wafer」這類字眼
2. **Skill 工具屬性**：每個 skill 只做一件事，任何 agent 都能呼叫
3. **Context 是靈魂**：所有「風格／品味／受眾感受」全部寫進 `_Context/`，未來換語言、換受眾只改這裡

---

## 📁 資料夾結構

```
new-course-material2presentation-blank/
├── CLAUDE.md                          # 主小隊長的大腦
├── README.md                          # 學生 / 你自己的入口
├── WALKTHROUGH.md                     # 你正在看的這份
├── .env.example                       # （如果 skill 要呼外部 API 才需要）
├── .gitignore
│
├── _Context/                          # 教學 DNA（你親自寫，不交給 AI）
│   ├── teaching-philosophy.md         # 你的教學風格與信念
│   ├── audience-profiles.md           # 不同受眾的描繪
│   ├── slide-design-rules.md          # 投影片設計準則
│   ├── code-style-guide.md            # 範例程式風格
│   └── assessment-philosophy.md       # 評量設計原則
│
├── .claude/
│   ├── agents/                        # 4 個 sub-agent（用 /agents 建）
│   │   ├── curriculum-architect.md
│   │   ├── slide-designer.md
│   │   ├── code-crafter.md
│   │   └── assessment-designer.md
│   └── skills/                        # 5 個 skill
│       ├── outline-design/
│       │   └── SKILL.md
│       ├── slide-content/
│       │   └── SKILL.md
│       ├── code-example/
│       │   └── SKILL.md
│       ├── exercise-gen/
│       │   └── SKILL.md
│       └── marp-render/
│           └── SKILL.md
│
└── Courses/                           # 輸出資料夾
    └── {課程名稱}-{時數}h/
        ├── 01-syllabus.md             # 大綱
        ├── 02-slides/                 # Marp 投影片
        │   ├── ch01-*.md
        │   └── ch02-*.md
        ├── 03-code-examples/          # 範例程式
        │   ├── ch01/
        │   └── ch02/
        ├── 04-assessments/            # 練習評量
        │   ├── ch01-exercises.md
        │   └── ch02-exercises.md
        └── 05-instructor-notes.md     # 講師備忘
```

---

## 🚀 七階段建構流程

每個階段都有「**你做什麼**」「**Claude 做什麼**」「**驗收標準**」。

預計總時間：**首次建構 4-6 小時**（含寫 `_Context/`），之後每堂新課 **1.5 小時內**。

---

### 階段 1：搭骨架（5 分鐘）

#### 你要做的事

```bash
cd /Users/kevinluo/claude-code-complete-tutorial/agent_group_projects/new-course-material2presentation-blank

mkdir -p _Context
mkdir -p .claude/agents
mkdir -p .claude/skills/{outline-design,slide-content,code-example,exercise-gen,marp-render}
mkdir -p Courses

touch .claude/agents/.gitkeep Courses/.gitkeep
```

#### 為什麼

- `.claude/agents/` 是 Claude Code 自動掃描的目錄
- `.claude/skills/` 每個技能一個資料夾（之後可放範本、輔助腳本）
- `_Context/` 放教學 DNA，所有 agent 執行前都會讀

#### 驗收

```bash
find . -type d | sort
```

預期看到 11 個資料夾。

---

### 階段 2：寫 `_Context/` 教學 DNA（30-60 分鐘）⭐ 最重要

> ⚠️ **這 5 個檔案 Kevin 你要親自寫，不要交給 AI**。
> 這是你的教學品味、判斷、風格的數位化。AI 可以幫你**起草**，但**最終決策必須是你**。

5 個檔案分工：

| 檔案 | 內容 | 為什麼 |
|---|---|---|
| `teaching-philosophy.md` | 你的教學信念、節奏、語言風格 | 決定 agent 怎麼「**說話**」 |
| `audience-profiles.md` | 不同受眾畫像（企業/學生/自學） | 決定 agent 怎麼「**選詞**」 |
| `slide-design-rules.md` | 投影片設計規則 | 決定 slide-designer 怎麼「**排版**」 |
| `code-style-guide.md` | 程式碼風格 | 決定 code-crafter 怎麼「**寫 code**」 |
| `assessment-philosophy.md` | 評量設計原則 | 決定 assessment-designer 怎麼「**出題**」 |

#### 寫作建議

不要從零寫。最快的方法是：
1. **找你過去最得意的一堂課**（投影片、講義都行）
2. **告訴 Claude**：「分析這堂課，幫我萃取教學風格規則」
3. **拿到草稿後親自審稿、改、加你的個人判斷**

#### `_Context/teaching-philosophy.md` 範本

```markdown
# 教學哲學

## 核心信念
- 先建立直覺，再講細節 — 永遠用「為什麼會這樣」開頭
- 一堂課 = 一個能帶走的能力，不是一堆知識點
- 學員寧可少學三個概念，也要把一個概念吃透

## 節奏偏好
- 每 15 分鐘必須有一個動手練習或互動點
- 概念講解 : 示範 : 練習 = 3 : 4 : 3
- 開頭 5 分鐘必須回答：為什麼今天要學這個？

## 不做的事
- 不用「很簡單」「顯然」這類詞
- 不直接貼官方文件
- 不假設學員有先備知識，除非開頭明確說了

## 語言風格
- 主要繁體中文，技術術語保留英文
- 比喻優先於定義
```

#### `_Context/audience-profiles.md` 範本

```markdown
# 受眾畫像

## Profile A：企業學員（Deloitte、Nike、和泰）
- 主管或資深 IC，30-45 歲
- 普遍能讀 Python 但不熟工程實踐
- 關注：能不能帶回公司用？ROI 怎麼算？
- 策略：商業案例先行，技術細節點到為止

## Profile B：學校學生（清大、北商大）
- 大三到研究生
- 學術強、工程弱
- 關注：履歷、面試
- 策略：底層原理講透，給 GitHub repo 練手

## Profile C：自學者
- 各種背景
- 關注：跟不跟得上
- 策略：節奏慢、多檢核點
```

#### 其他 3 個檔案

範本見 Kevin 的原始藍圖（slide-design-rules.md / code-style-guide.md / assessment-philosophy.md），這份 walkthrough 不重複。

#### 驗收

```bash
ls _Context/
wc -l _Context/*.md
```

預期看到 5 個檔案、每個檔案 30-80 行（不要太長，agent 每次都要讀）。

---

### 階段 3：寫 `CLAUDE.md`（主小隊長的大腦，15 分鐘）

#### 你做什麼

在 Claude Code 對話框打：

```
請讀 _Context/ 下所有檔案，然後幫我建立 CLAUDE.md，內容包含：
1. 工作區概述
2. 資料夾結構說明
3. 任務路由規則（何時委派、何時不委派）
4. Skills 與 Agents 設計原則（保持主題無關性）
5. 輸出檔案命名規範

⚠️ 重要：保持 agnostic — 不要把任何特定課程主題寫進去。
所有主題細節在執行時從使用者輸入或 _Context 動態載入。
```

#### Claude 會做什麼

讀 5 個 `_Context/*.md`，產出 `CLAUDE.md` 草稿。

#### 你要驗收什麼

打開 `CLAUDE.md` 檢查：
- [ ] **沒有**「LangGraph」「Cursor」「wafer」等特定主題字眼
- [ ] 有任務路由規則（什麼時候委派、什麼時候不委派）
- [ ] 有命名規範（`Courses/{name}-{hours}h/`）
- [ ] 有「預設不委派，先評估能否用單一 Skill 完成」這條原則

#### 範本（如果 Claude 給你的不滿意）

```markdown
# Course Factory — 教學課程開發工作區

採用 Skills + Sub-Agents 架構。

## 資料夾
- _Context/ — 教學 DNA（所有 agents 執行前必讀）
- .claude/skills/ — 共用技能
- .claude/agents/ — Sub-agents
- Courses/ — 課程輸出，依課程名稱分目錄

## 任務路由

### 委派 sub-agent 的時機
- 開放式多階段任務（大綱→投影片→程式→評量）
- 範例：「幫我做一堂 3 小時的 X 課程」

### 不委派的時機（直接用 skill 或直答）
- 單一具體動作
- 範例：「把這份大綱轉 Marp」「修這張投影片措辭」

### 預設不委派
先評估能否用單一 skill 完成，避免過度委派。

## 設計原則

### Skills
- 主題無關
- 執行時從 _Context/ 動態載入
- 輸出格式統一

### Agents
- 主題無關，職責不重疊
- 可呼叫多個 skills

## 輸出命名
- 課程資料夾：Courses/{name}-{hours}h/
- 大綱：01-syllabus.md
- 投影片：02-slides/ch{NN}-{name}.md
- 程式：03-code-examples/ch{NN}/{name}.py
- 評量：04-assessments/ch{NN}-exercises.md
- 講師備忘：05-instructor-notes.md

## 規則
- 回應使用繁體中文
- 套件管理用 uv（如需 Python）
- 路徑用 pathlib.Path
```

---

### 階段 4：建第一個 Skill（10 分鐘）

從最常用的 `outline-design` 開始。

#### 你做什麼

在 Claude Code 打：

```
幫我建立 .claude/skills/outline-design/SKILL.md。

觸發時機：使用者要求設計課程大綱、章節結構、學習目標。

輸入：課程主題、總時數、目標受眾（從使用者問或從 _Context/audience-profiles.md 選）。

工作流程：
1. 讀 _Context/teaching-philosophy.md 與 audience-profiles.md
2. 與使用者確認三件事：主題範圍、受眾、時數
3. 產出三層結構：
   - 課程級學習目標
   - 章節級目標
   - 單元級目標
4. 每章節標註預估時數、主要產出物、評量方式
5. 輸出存到 Courses/{課程名}-{時數}h/01-syllabus.md

要求：保持主題無關，所有教學風格從 _Context 載入。
```

#### 驗收

```bash
cat .claude/skills/outline-design/SKILL.md | head -30
```

檢查：
- [ ] 有 YAML frontmatter（`name`, `description`）
- [ ] 內容**沒有**特定主題字眼
- [ ] 明確說「執行時讀 _Context/」

---

### 階段 5：建第一個 Sub-Agent（10 分鐘）⭐ 用 `/agents` 互動式建

#### 你做什麼

```
/agents
```

走 9 個畫面（流程參考 [wafer walkthrough](../computer-vision-wafer-agents-detection-demo/WALKTHROUGH.md)）：

1. ← 切到 Agents tab
2. Create new agent
3. **Project (.claude/agents/)**
4. **Generate with Claude (recommended)**
5. 貼上需求描述（下方）
6. 選工具：Read-only / Edit / Execution（不勾 All / MCP / Other）
7. 選顏色：**🟣 Purple**（架構規劃 = 思考紫）
8. Confirm 預覽
9. ⚠️ **按 `s` 不要按 `e`**

#### 需求描述

```
你是 curriculum-architect agent — 課程架構師。
當使用者要開新課程、規劃章節結構、設計學習路徑時使用。

⚠️ 你只負責「規劃」，不要嘗試做投影片、程式碼、評量 — 那是其他 sub-agent 的工作。

工作職責：
1. 開工前必須先讀 _Context/teaching-philosophy.md 與 _Context/audience-profiles.md
2. 用對話確認三件事：主題範圍、受眾 profile、總時數
3. 呼叫 outline-design skill 產出三層大綱
4. 在 Courses/{課程名}-{時數}h/ 建立後續資料夾骨架：
   - 02-slides/
   - 03-code-examples/
   - 04-assessments/
5. 產出「下一步建議」：告訴使用者下一步該找哪個 sub-agent

輸出位置：Courses/{課程名}-{時數}h/01-syllabus.md

完成標準：
- 01-syllabus.md 包含三層學習目標
- 每章節標註預估時數、產出物、評量方式
- 後續資料夾骨架已建好
- 回報「下一步可以叫 slide-designer 開始做投影片」

環境：繁體中文回應、保持主題無關（不寫死任何特定領域）
```

#### 驗收

```bash
ls .claude/agents/
cat .claude/agents/curriculum-architect.md | head -10
```

檢查 frontmatter 有 `color: purple`、tools 不含過多東西。

---

### 階段 6：第一次完整跑通（測試，30 分鐘）

#### 你做什麼

在 Claude Code 對話框打：

```
我要開一堂新課：「給 PM 看的 LangGraph 入門」，3 小時。
受眾是 Profile A 企業學員。請開發課程。
```

#### 預期流程

1. 主小隊長判斷這是開放式多階段任務 → 委派 🟣 `@curriculum-architect`
2. agent 先讀 `_Context/`
3. 用對話確認細節（你可能要回答 1-2 個問題）
4. 產出 `Courses/PM-LangGraph-3h/01-syllabus.md`
5. 建好 02-slides/、03-code-examples/、04-assessments/ 空資料夾
6. 回報你「下一步可叫 slide-designer」

#### 驗收

打開產出的 `01-syllabus.md`，**檢查它有沒有用上你的教學哲學**：
- [ ] 開頭 5 分鐘有「為什麼今天學這個」
- [ ] 每 15 分鐘有互動點
- [ ] 沒有「很簡單」「顯然」這類詞
- [ ] 比喻優先於定義

#### 如果不對怎麼辦

**不要去改 agent 本身**，回去調：
1. `_Context/teaching-philosophy.md`（風格沒被用上）
2. `.claude/skills/outline-design/SKILL.md`（流程不對）

這個分離很重要：**agent 是骨架、context 是靈魂**。

---

### 階段 7：擴充其他 3 個 Sub-Agent + 4 個 Skill

按這個順序建（**每建一個立刻測試一輪，不要四個都建完才測**）：

| 順序 | Sub-Agent | 顏色 | 必用 Skill | 為什麼這個順序 |
|---|---|---|---|---|
| 1 | curriculum-architect | 🟣 Purple | outline-design | 沒大綱什麼都做不了 |
| 2 | slide-designer | 🔵 Blue | slide-content, marp-render | 投影片是課程骨架 |
| 3 | code-crafter | 🟢 Green | code-example | 投影片會引用程式 |
| 4 | assessment-designer | 🟡 Yellow | exercise-gen | 評量最後做，可參照前三者 |

#### 各 sub-agent 需求描述範本

##### slide-designer（🔵 Blue）

```
你是 slide-designer agent — 投影片內容設計師。
當使用者要做投影片、Marp、簡報、章節內容時使用。

⚠️ 前置條件：必須先有 01-syllabus.md（curriculum-architect 的產出）。
若沒有，請使用者先呼叫 curriculum-architect。

職責：
1. 讀 _Context/teaching-philosophy.md, slide-design-rules.md, audience-profiles.md
2. 讀目標課程的 01-syllabus.md
3. 對使用者指定的章節，呼叫 slide-content skill 產出內容
4. 呼叫 marp-render skill 轉成 Marp 格式
5. 輸出到 Courses/{課程名}/02-slides/ch{NN}-{name}.md

規則：
- 每張投影片只承載一個概念
- 文字 ≤ 30 字/頁
- 每張必有 speaker notes
- 程式碼片段 ≤ 15 行

繁體中文、保持主題無關
```

##### code-crafter（🟢 Green）

```
你是 code-crafter agent — 範例程式工匠。
當使用者要範例程式、程式碼示範、漸進式範例時使用。

職責：
1. 讀 _Context/code-style-guide.md
2. 對指定章節呼叫 code-example skill
3. 產出三版本：minimal (10 行) → practical (30 行) → production (含錯誤處理)
4. 輸出到 Courses/{課程名}/03-code-examples/ch{NN}/

規則：
- Python 3.10+，用 type hints
- 不寫死 API key，用 os.getenv()
- 註解寫「為什麼」不寫「做什麼」
- 每檔開頭三行說明：目的、執行方式、預期輸出
- 關鍵行用 # ← 這裡 標示講解重點

繁體中文、保持主題無關
```

##### assessment-designer（🟡 Yellow）

```
你是 assessment-designer agent — 練習評量設計師。
當使用者要練習題、評量、檢核題、專題時使用。

職責：
1. 讀 _Context/assessment-philosophy.md
2. 讀目標章節的 syllabus 與已產出的 slides
3. 呼叫 exercise-gen skill 出三層題目
4. 輸出到 Courses/{課程名}/04-assessments/ch{NN}-exercises.md

三層題目結構：
- 檢核題（concept check）— 1 分鐘可答
- 練習題（practice）— 15-30 分鐘可完成
- 專題（capstone）— 整章結束的整合應用

難度分布：70% 基礎 / 20% 進階 / 10% 挑戰（⭐⭐⭐）

繁體中文、保持主題無關
```

#### 5 個 Skill 設計重點（簡述）

| Skill | 核心職責 | 輸出 |
|---|---|---|
| outline-design | 三層學習目標生成 | 01-syllabus.md |
| slide-content | 投影片內容撰寫（純文字） | 中間態 markdown |
| marp-render | 中間態 → Marp 格式 | 02-slides/*.md |
| code-example | 三版本漸進範例 | 03-code-examples/*/ |
| exercise-gen | 三層題目（檢核/練習/專題） | 04-assessments/*.md |

每個 skill 的詳細 SKILL.md 由 Claude 根據你的描述生成，不在這份 walkthrough 重複。

---

## ⏱️ 時間節省（量化）

以一堂 3 小時新課為例：

| 階段 | 純手動 | AI 團隊輔助 | 你需要做的事 |
|---|---|---|---|
| 大綱設計 | 90 分 | 5 分 | 確認受眾、調大綱 |
| 投影片開發 | 300 分 | 30 分 | 審內容、調用詞 |
| 範例程式 | 200 分 | 20 分 | 跑一遍確認 |
| 評量設計 | 120 分 | 15 分 | 挑題、改情境 |
| 講師備忘 | 80 分 | 10 分 | 補你的口語化梗 |
| **單堂 3h 課** | **~13 小時** | **~1.5 小時** | — |

每堂課省 **11.5 小時**。下一個 36 小時三部曲省 **130+ 小時**。

---

## ✅ 完整驗收清單

跑完整套後檢查：

### 結構
- [ ] `_Context/` 5 個檔案，每個 30-80 行
- [ ] `CLAUDE.md` 無特定主題字眼
- [ ] `.claude/agents/` 有 4 個 .md
- [ ] `.claude/skills/` 有 5 個資料夾，每個有 SKILL.md

### 功能
- [ ] 打「幫我開一堂 X 課」會自動路由到 🟣 curriculum-architect
- [ ] 打「做章節 1 的投影片」會路由到 🔵 slide-designer
- [ ] 產出的內容**有用上你 _Context 的風格**（不是 Claude 預設口吻）

### 主題無關性
- [ ] 隨便換一個主題（例：「Rust 入門」「品酒學」）都能跑
- [ ] 沒有任何 agent / skill 寫死特定領域

---

## 🧬 自我增生：第一個遞迴課程

**建議的第一堂課**：用這套系統開「**怎麼用 Claude Code 建一套課程開發 AI 團隊**」。

為什麼這是好的第一堂課？

1. **你最熟**（你剛建完，所有細節都在腦子裡）
2. **內容＝過程**（教材就是這份 walkthrough）
3. **驗證系統可用性**（如果系統做不出這堂課，表示系統有問題）
4. **學生學完馬上能用**（他們可以複製你的 template，建自己的 Course Factory）

執行：

```
我要開一堂課：「用 Claude Code 建構教學課程開發 AI 團隊」，
3 小時，受眾是 Profile B 學校學生（清大資工大三大四）。
請開發課程。
```

看 4 個 agent 接力，產出完整課程包。產出之後：
1. 拿這份產出跟我的這份 walkthrough 對比
2. 補上系統沒抓到的點 → 改進 `_Context/`
3. 再跑一次 → 拿到更好的版本
4. 這就是「**用 AI 開發課程的課程**」

---

## 🚨 常見卡點對照

| 卡點 | 原因 | 處理 |
|---|---|---|
| Agent 沒讀 `_Context/` | description 沒強調 | 在需求描述加「**開工前必須讀 _Context/**」 |
| 產出帶特定主題字眼 | agent 內容寫死 | 改 agent.md，把主題字眼搬到 _Context |
| Claude 沒委派 agent | description 觸發句不夠強 | 加更多觸發關鍵字（「開課」「規劃」「大綱」等） |
| 投影片風格不對 | _Context 沒寫清楚 | 補 slide-design-rules.md（給 3-5 個 do/don't 範例） |
| 程式碼風格不對 | code-style-guide 太抽象 | 補實際 code snippet 範例 |
| `/agents` 按 `e` 卡住 | VS Code tab 沒關 | 永遠按 `s` |

---

## 🎯 立即可做的下一步

選一個：

### A. **今天就開始寫 _Context/**（30-60 分鐘）
- 找你最得意的一堂課（投影片或講義）
- 跟 Claude Code 說：「分析這堂課，萃取教學風格規則寫進 _Context/teaching-philosophy.md」
- 拿到草稿親自改、補

### B. **用 Claude 起 `_Context/` 草稿**（10 分鐘）
- 直接打：「根據我過去做過 LangGraph 20h、Cursor 三部曲、Deloitte 企業課的經驗，幫我起 _Context/ 五個檔案的草稿」
- 拿到後親自審稿（**這步不能省**）

### C. **先跑階段 1**（5 分鐘）
- 建好資料夾骨架
- 確認結構對，再決定下一步

### D. **跳到最有趣的：自我增生實驗**
- 跳過階段 2-7
- 直接讓 Claude 跑「**做一堂課教別人建這套系統**」
- 看會出什麼東西
- 對照產出修正 _Context

我個人推 **B → C → A**：用 AI 加速草稿 → 把骨架建起來 → 再花時間打磨 `_Context/`。
但如果你想感受「**從零到有**」的體驗，**C → A → B** 也很好。

---

## 🧠 設計哲學總結

> **Wafer agents 教你怎麼用 Claude Code 「做某件事」。
> Course Factory 教你怎麼用 Claude Code 「**做做事的方法**」。**

這個抽象層級的跳躍，是從「使用者」變成「**系統設計者**」的分水嶺。
跑完這份 walkthrough，你會擁有的不是「一個課程」，而是「**無限產出課程的工廠**」。

---

_Last updated: 2026-05-12_
_Maintainer: Kevin (kevin@legalsign.ai)_
_本份 walkthrough 本身就是 Course Factory 第一個遞迴實驗的素材_
