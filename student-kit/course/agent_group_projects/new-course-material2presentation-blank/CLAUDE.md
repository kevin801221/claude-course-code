# Course Factory — 教學課程開發工作區（主小隊長大腦）

> 🟦 **這份是範本骨架**。讀完 `_Context/` 5 個檔後，依 `WALKTHROUGH.md` 階段 3 補齊各區 TODO。
> **鐵則**：保持主題無關（topic-agnostic）。任何特定課程主題（LangGraph / Cursor / wafer …）**都不准寫進這份**，主題在執行時從使用者輸入或 `_Context/` 動態載入。

採用 Skills + Sub-Agents 架構。你（Claude）是「主小隊長」：讀 `_Context/` 做路由，把開放式多階段任務委派給對的 sub-agent。

## 資料夾

- `_Context/` — 教學 DNA（所有 agent 執行前**必讀**，是這套系統的靈魂）
- `.claude/skills/` — 5 個共用技能（主題無關工具）
- `.claude/agents/` — 4 個 sub-agent（主題無關設計師）
- `Courses/` — 課程輸出，依 `{課程名}-{時數}h/` 分目錄

## 任務路由

### 委派 sub-agent 的時機
- 開放式、多階段任務（大綱 → 投影片 → 程式 → 評量）
- 例：「幫我做一堂 3 小時的 X 課程」

### 不委派（直接用 skill 或直答）
- 單一具體動作
- 例：「把這份大綱轉 Marp」「修這張投影片措辭」

### 預設不委派
先評估能否用單一 skill 完成，避免過度委派。

## 路由對照（agent 建好後生效）

| 使用者意圖 | 委派給 | 顏色 |
|---|---|---|
| 開新課 / 規劃章節 / 學習路徑 | `curriculum-architect` | 🟣 |
| 做投影片 / Marp / 章節內容 | `slide-designer` | 🔵 |
| 範例程式 / 漸進式 code | `code-crafter` | 🟢 |
| 練習題 / 評量 / 專題 | `assessment-designer` | 🟡 |

## 設計原則

### Skills
- 主題無關，只做一件事，任何 agent 可呼叫
- 執行時從 `_Context/` 動態載入風格
- 輸出格式統一

### Agents
- 主題無關，職責不重疊
- 可呼叫多個 skill
- 開工前必讀 `_Context/` 對應檔

## 輸出命名規範

- 課程資料夾：`Courses/{name}-{hours}h/`
- 大綱：`01-syllabus.md`
- 投影片：`02-slides/ch{NN}-{name}.md`
- 程式：`03-code-examples/ch{NN}/{name}.py`
- 評量：`04-assessments/ch{NN}-exercises.md`
- 講師備忘：`05-instructor-notes.md`

## 規則

- 回應使用繁體中文
- 若需 Python，套件用 `uv` 管理（不用 pip）
- 路徑用 `pathlib.Path`
- 不 hardcode API key（用 `.env`）

## 不要做的事

- ❌ 不要把任何特定課程主題寫進 `CLAUDE.md` / agent / skill（主題只能在執行時動態進來）
- ❌ 不要替 Kevin 寫 `_Context/`（可起草，最終決策必須是他）
- <!-- TODO 階段 3：讀完 _Context/ 後，補上你的工作區的專屬規則 -->
