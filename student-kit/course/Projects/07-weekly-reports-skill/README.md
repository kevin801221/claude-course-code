# 小專案 7：drafting-weekly-reports skill — 週報黃金範例

> 套用「AI Skill 實戰架構藍圖」心法，**production-grade** 完整 skill。
> 對照 PPT 「心法 1」第 8 頁 perfect skill 範例做出來的實作。

## 為什麼這個是「黃金範例」

之前的 mini-projects 為了教學簡潔，多數 skill 只有單檔 `SKILL.md`。
這個專案**完整套用 PDF 心法所有原則**：

| 心法原則 | 這個 skill 怎麼做 |
|---|---|
| **Layer 1: Perfect Metadata** | name=動名詞、description 含「做什麼+何時用」+ 6 個自然觸發詞 |
| **Layer 2: Core Methodology (~150 行)** | SKILL.md 給「Why / Attitude / Principles / Workflow」心法 not 步驟 |
| **Layer 3: External Assets (按需載入)** | references/ + scripts/ + examples/ 三類拆好 |
| **客觀操作丟 Scripts** | fetch_commits.sh、classify_commits.py、format_report.py 處理 deterministic 邏輯 |
| **主觀判斷丟 SKILL.md** | 「翻譯成業務語言」「該不該寫」交給 AI 判斷 |
| **Anti-patterns 內建** | references/anti-patterns.md 列 5 個常見錯誤 |
| **多受眾設計** | tone-guide.md 對 CEO / 工程主管 / PM / 客戶 4 種版本 |

## 結構

```
07-weekly-reports-skill/
├── README.md                                ← 你正在看的
└── .claude/skills/drafting-weekly-reports/
    ├── SKILL.md                              (127 行 — 主文件)
    ├── scripts/
    │   ├── fetch_commits.sh                  ← 撈 GitHub commits
    │   ├── classify_commits.py               ← 自動分類 feat/fix/refactor/docs
    │   └── format_report.py                  ← 套版產 markdown
    ├── references/
    │   ├── output-template.md                ← 黃金格式 + 翻譯對照表
    │   ├── tone-guide.md                     ← 4 種讀者語氣指南
    │   └── anti-patterns.md                  ← 5 個反例（教學用）
    └── examples/
        ├── good-output.md                    ← 好的範例輸出
        └── bad-output.md                     ← 壞的範例（對比學習）
```

## 安裝

### 個人層（推薦，所有 repo 都能用）

```bash
mkdir -p ~/.claude/skills
cp -r .claude/skills/drafting-weekly-reports ~/.claude/skills/
```

### 專案層

```bash
cd ~/your-repo
mkdir -p .claude/skills
cp -r /path/to/07-weekly-reports-skill/.claude/skills/drafting-weekly-reports .claude/skills/
git add .claude/skills/drafting-weekly-reports
git commit -m "Add drafting-weekly-reports skill"
```

## 使用

### 方式 1：自動觸發（最自然）

```bash
cd ~/your-repo
claude
> 幫我寫這週的週報
# Claude 看 description 自動載入 skill，跑 workflow
```

### 方式 2：明確呼叫

```bash
> 用 drafting-weekly-reports 幫我整理本週進度
```

### 方式 3：跑特定情境

```bash
> 寫週報，給 CEO 看的版本（不要技術細節）
> 寫週報，包含 PR 跟 issue
> 寫週報，但這週只有 2 個 commits，幫我問我有沒有非 commit 工作
```

## 範例輸出

看 `examples/good-output.md`（好的版本）vs `examples/bad-output.md`（壞的版本）對比學習。

## 設計亮點（教學重點）

### 1. SKILL.md 寫「心法」不寫「步驟」

整份 SKILL.md 只列了 5 個 step，且每 step 一句話帶過。
真正的「智慧」在：
- Why：解釋讀者是誰、要什麼
- Attitude：「翻譯官 not git log dumper」這句心法
- Principles：5 條判斷模糊地帶的優先順序

→ 這樣 AI 在 corner case 知道怎麼做（憑原則判斷，不會卡死）。

### 2. Scripts 處理「客觀邏輯」

撈 commits、分類、套版全交給 Python/Bash。
**為什麼**：這些是 deterministic 操作，AI 用正則容易出錯，且浪費 token。

### 3. References 處理「會膨脹」的內容

輸出範本（500 行）、翻譯對照表（100+ 條）、anti-patterns 全部抽到 references/。
**為什麼**：這些「按需載入」就好，每次都載會塞爆 context。

### 4. Examples 是「最強教材」

`good-output.md` 跟 `bad-output.md` 並排放，AI 一眼看出差異。
**為什麼**：給 AI「正例 + 反例」遠比給 100 條規則有用。

## 客製化

### 改成你公司的格式

編輯 `references/output-template.md` 把範本改成你公司既有格式（讓主管不用適應新格式）。

### 加新的分類規則

編輯 `scripts/classify_commits.py` 的 `PATTERNS` dict，加你公司的 commit prefix（例：`docs(zh)` `feat(api)` 等）。

### 改翻譯對照表

`references/output-template.md` 最下方的對照表 — 加你公司常用的工程術語對應業務語言。

## 故障排除

| 症狀 | 解法 |
|---|---|
| Claude 沒自動觸發 skill | 看 description 是否含你常用的觸發詞，沒有就加 |
| commits 撈不到 | 檢查 `git config user.email` 是否對 |
| 分類常常錯 | 改 `classify_commits.py` 的 PATTERNS，或在 SKILL.md 寫「分類有錯就重判斷」 |
| 報告太長 | SKILL.md 已限制 500 字，AI 還太長就明說「壓在 300 字內」|
| AI 自己編 commits | 在 SKILL.md 「禁止」段加「絕對不准 hallucinate commits」|

## 與其他 mini-projects 的對比

| 專案 | 複雜度 | 特色 |
|---|---|---|
| MP3 youtube-notes | ⭐ | 單檔 SKILL.md（最小例） |
| MP4 pomodoro | ⭐⭐ | hook + script |
| MP6 discord-dm-bot | ⭐⭐⭐ | Agent SDK + 外部服務 |
| **07 weekly-reports** | **⭐⭐⭐⭐ 黃金範例** | **完整心法應用 — 3 層架構 + 多檔分工** |

## 對照教學文件

- PPT 完整版「Part 8 Skills」+「心法 1: AI Skill 實戰架構藍圖」
- `../../Claude_Code_建構指南.md` Part 2 Skills 完整建構指南
