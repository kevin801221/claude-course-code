# Superpowers Plugin Walkthrough

> **對象**：已會用 Claude Code 基礎（slash command / sub-agent / skill），想把 AI Coding 從「對話式」升級成「工程式」的人
> **形式**：講師現場帶 / 自學皆可
> **時長**：90 分鐘（30 分鐘 repo 導覽 + 60 分鐘實戰專案）
> **產出**：跑完一個 `todo-cli`（Python + uv）小專案，從 brainstorming → design doc → plan → worktree → TDD → subagent 執行 → code review → merge，全程靠 superpowers 跑
> **核心方法**：「先看懂 14 個 skill 是哪 14 個齒輪 → 親手讓齒輪轉一圈」

---

## 開場（5 分鐘）：為什麼需要 superpowers？

一般人用 Claude Code 都是「丟一句話 → AI 寫一坨 code」。問題是：

| 一般用法 | 用 superpowers |
|---|---|
| 沒設計就動手 | brainstorming 強制先把 spec 釐清 |
| 沒計畫就寫 code | writing-plans 切成 2–5 分鐘小任務 |
| 先寫實作再補測試 | test-driven-development 強制 RED → GREEN → REFACTOR |
| 一個 session 寫到底，context 越滾越爛 | subagent-driven-development 每個任務開新 subagent |
| 寫完不 review 直接 merge | requesting-code-review 卡在 PR 前 |
| 一條 branch 改到底 | using-git-worktrees 隔離工作區 |

> **教學金句**：「Superpowers 不是給你新工具，是給你**一條紀律**。它把你從『跟 AI 對話』升級成『跟 AI 一起跑研發流程』。」

這個 plugin 是 Jesse Vincent（Anthropic 顧問）寫的，現在在 Anthropic 官方 marketplace 上架（`@claude-plugins-official`）。

---

## 📁 Repo 結構速覽

```
superpowers/
├── README.md                       ← 安裝 + 哲學
├── CLAUDE.md                       ← 給 contributor 的（94% PR 退件率，重要警告）
├── AGENTS.md / GEMINI.md           ← 其他 harness 的指引
├── .claude-plugin/plugin.json      ← Claude Code 認得的 plugin manifest
├── hooks/
│   ├── hooks.json                  ← SessionStart hook 設定
│   └── session-start               ← bash 腳本：每次開 session 注入 using-superpowers
├── skills/                         ← ⭐ 心臟，14 個 skill
│   ├── using-superpowers/          ← 開場必載入，教 AI「如何使用其他 skill」
│   ├── brainstorming/              ← 設計階段
│   ├── writing-plans/              ← 寫計畫
│   ├── executing-plans/            ← 跨 session 執行
│   ├── subagent-driven-development/← 同 session 用 subagent 跑
│   ├── test-driven-development/    ← TDD 鐵則
│   ├── systematic-debugging/       ← 4 階段抓 bug
│   ├── verification-before-completion/
│   ├── requesting-code-review/
│   ├── receiving-code-review/
│   ├── using-git-worktrees/
│   ├── finishing-a-development-branch/
│   ├── dispatching-parallel-agents/
│   └── writing-skills/             ← meta：教你寫新 skill
├── docs/
│   ├── plans/                      ← 範例計畫
│   ├── superpowers/specs/          ← 範例設計文件
│   └── windows/                    ← Windows 安裝補丁
├── tests/                          ← skill 觸發的 eval 集
└── scripts/                        ← 維護用（bump-version, sync to codex）
```

每個 skill 是 1 個資料夾，裡面至少有 `SKILL.md`（YAML frontmatter + 內容），有些還有 supporting prompts（`*-prompt.md`）給 subagent 用。

---

## Phase 0：安裝與檢查（5 分鐘）⚙️

### 安裝（任選一）

| 方式 | 指令 | 適用 |
|---|---|---|
| 官方 marketplace（**推薦**） | `/plugin install superpowers@claude-plugins-official` | 大部分人 |
| Jesse 自己的 marketplace | `/plugin marketplace add obra/superpowers-marketplace` 然後 `/plugin install superpowers@superpowers-marketplace` | 想拿最新 dev 版 |
| 本地 clone（這個 repo 就是） | 不裝，直接讀 — 但 skills 不會 auto-trigger | 教學 / 改 skill 用 |

### 驗證安裝成功

```bash
# 1. 看 plugin 是否在
ls ~/.claude/plugins/data/superpowers* 2>/dev/null || \
  ls ~/.claude/plugins/marketplaces/

# 2. 開 Claude Code，第一句話打：
#    "list all the superpowers skills you have"
# 應該回你 14 個 skill 名稱（brainstorming / writing-plans / TDD / ...）

# 3. 終極驗證（acceptance test，README 寫的）：
#    開新 session 打："Let's make a react todo list"
# 應該自動觸發 brainstorming skill，而不是直接寫 code。
```

> **教學金句**：「驗證一個 skill plugin 有沒有真的裝好，不是看 `/plugin list`，是看『該觸發的時候有沒有觸發』。」

### ⚠️ 常見裝完不會動

| 症狀 | 原因 | 處理 |
|---|---|---|
| 打「做個 todo list」直接寫 code | SessionStart hook 沒跑 | 重啟 Claude Code、`/hooks` 看狀態 |
| skills 列出但不會自動用 | `using-superpowers` skill 沒注入 | 重啟 / `claude --debug` 看啟動 log |
| 安裝指令找不到 marketplace | 沒先 `add` | 跑 `/plugin marketplace add` |

---

## Phase 1：14 個 Skill 一覽 ⭐ 最關鍵（15 分鐘）

按「**何時會觸發**」分組，這比照字母排序好記。

### 🧠 設計階段（在動手前）

| Skill | 何時觸發 | 做什麼 |
|---|---|---|
| `using-superpowers` | SessionStart 自動 | 教 AI「碰到創意任務先檢查有沒有 skill 適用」 |
| `brainstorming` | 你說「想做 X」 | 蘇格拉底式問你，逼出真實需求；產出 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` |
| `writing-plans` | spec 拿到後 | 把 spec 切成 2–5 分鐘一塊的 task；產出 `docs/superpowers/plans/YYYY-MM-DD-<feature>.md` |

### 🛠 執行階段（動手了）

| Skill | 何時觸發 | 做什麼 |
|---|---|---|
| `using-git-worktrees` | 確認要動工前 | 建 git worktree 隔離工作區，避免污染主分支 |
| `subagent-driven-development` | plan 寫好，當 session 內跑 | 每個 task 開新 subagent 跑（context 不污染） |
| `executing-plans` | plan 寫好，要跨 session | 同上但用 batch + checkpoint |
| `test-driven-development` | 每個 task 內 | RED → GREEN → REFACTOR 鐵則 |
| `dispatching-parallel-agents` | 多個獨立任務 | 一次派多個 subagent 平行跑 |

### 🔍 收尾階段

| Skill | 何時觸發 | 做什麼 |
|---|---|---|
| `systematic-debugging` | 任何 bug / 測試失敗 | 4 階段抓根本原因（不要瞎猜） |
| `verification-before-completion` | 宣稱「做完了」前 | 強制驗證不是嘴砲 |
| `requesting-code-review` | task 完成 | 對著 plan 自我 review |
| `receiving-code-review` | 收到 reviewer 回饋 | 怎麼回應、怎麼修 |
| `finishing-a-development-branch` | 全部 task 完 | 給你 merge / PR / 留著 / 丟掉 四選一 |

### 🧰 Meta

| Skill | 何時觸發 | 做什麼 |
|---|---|---|
| `writing-skills` | 你想新增 skill 時 | 教你怎麼寫一個會 auto-trigger 的 skill |

> **教學金句**：「Skill 不是 menu，是**反射神經**。Claude 不會問你『要不要用 X』，它看到觸發條件就跳了。」

---

## Phase 2：心臟剖開——讀懂一個 SKILL.md（10 分鐘）📄

打開 `skills/brainstorming/SKILL.md`，看前 20 行：

```yaml
---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---

# Brainstorming Ideas Into Designs
...
<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it.
</HARD-GATE>
```

3 個關鍵設計：

| 設計 | 為什麼 |
|---|---|
| `description` 用「**You MUST use this before any creative work**」 | trigger 越強烈、AI 越認真檢查 |
| `<HARD-GATE>` 區塊 | 給 AI 設絕對禁區，不准跨越 |
| Anti-Pattern 段：「This Is Too Simple To Need A Design」 | 預防 AI 自我合理化（「這個太簡單不用 design」） |

> **教學金句**：「寫 skill 的核心不是『告訴 AI 怎麼做』，是『**預先擋掉它會偷懶的藉口**』。」

---

## Phase 3：實戰專案——`todo-cli`（60 分鐘）⭐⭐⭐

我們要做：一個 Python CLI，可以 `add` / `list` / `done` Markdown 格式的 todo。用 uv 管套件、pytest 測試。

整個流程**只用嘴**操作 Claude Code，不自己手動 `git checkout -b`、不自己 `mkdir`、不自己想結構——讓 superpowers 帶你走。

### Step 1：建工作目錄（30 秒）

```bash
mkdir -p ~/Desktop/todo-cli-demo && cd ~/Desktop/todo-cli-demo
git init && git commit --allow-empty -m "init"
claude  # 開 Claude Code
```

### Step 2：丟出需求（brainstorming 階段）

對 Claude 打：

> 我想做一個 CLI 工具叫 todo-cli，可以加待辦、列出來、標記完成。用 Python + uv，資料存 Markdown 檔。

**預期觸發**：`brainstorming` skill。Claude 應該：
1. ✅ 不直接寫 code
2. 先問你：「Markdown 檔放哪？固定路徑還是 flag？」「`done` 是刪掉還是劃線？」「要不要 due date？」
3. 提出 2–3 個方案（CLI library 用 `click` 還是 `typer`？）
4. 把設計分段給你看，每段等你確認
5. 寫設計文件存 `docs/superpowers/specs/2026-05-13-todo-cli-design.md`

**你要做的事**：認真回答、別敷衍「都可以」。superpowers 的價值就在這逼問。

> **教學金句**：「『隨便都好』是 AI Coding 慘案的開頭。superpowers 不讓你跳這步。」

### Step 3：產生計畫（writing-plans）

設計文件你看過後跟 Claude 說「OK」。它會自動接 `writing-plans`：
- 列出要動哪些檔案（`pyproject.toml`、`todo_cli/__init__.py`、`todo_cli/cli.py`、`tests/test_cli.py`...）
- 把工作切成 2–5 分鐘小任務（「建 uv 專案結構」「寫 add 命令的 failing test」「實作 add 命令」...）
- 存到 `docs/superpowers/plans/2026-05-13-todo-cli.md`

### Step 4：開 worktree（using-git-worktrees）

Claude 自動開：

```bash
git worktree add ../todo-cli-demo-feat feat/todo-cli
```

從此寫 code 都在 worktree 內，主目錄不會被污染。

### Step 5：開跑（subagent-driven-development + TDD）

你說「go」。接下來 Claude 會：

1. 派一個 subagent 處理 task 1：先寫測試（會 fail）
2. 派一個 subagent 處理 task 2：寫剛好讓測試 pass 的實作
3. 兩階段 review：spec 合規 → code quality
4. 通過 → commit → 下一個 task
5. 一路自動跑完（不會中間問你「要繼續嗎？」）

> **教學金句**：「subagent-driven-development 的核心是『**每個 task 開新 context**』。你的主 session 只負責調度，不被細節塞滿。」

### Step 6：finish branch

跑完所有 task，`finishing-a-development-branch` 自動觸發。給你選：

| 選項 | 何時選 |
|---|---|
| Merge to main | 你是 solo dev、本地專案 |
| Open PR | 有 GitHub remote、要 review |
| Keep branch | 還沒測夠 |
| Discard | 失敗實驗 |

---

## 整合 demo：一條龍跑完（5 分鐘）

把 Phase 3 從頭跑到尾應該長這樣：

```
你：「我想做 todo-cli ...」
[brainstorming 觸發] → 問你 3 個問題 → 給你設計分 3 段 → 寫 design doc
你：「OK 接受」
[writing-plans 觸發] → 列 8 個 task → 寫 plan doc
你：「go」
[using-git-worktrees 觸發] → 建 worktree
[subagent-driven-development 觸發] → 跑 task 1
  ├─ subagent A: 寫 test_add → 確認失敗 ✅
  ├─ subagent B: 寫 add 實作 → 確認 pass ✅
  ├─ spec review ✅ / code quality review ✅
  └─ commit
[繼續 task 2 ~ task 8]
[finishing-a-development-branch 觸發] → 「要 merge / PR / 留著 / 丟掉？」
你：「merge」
完成。
```

整個過程你打字次數可能不到 15 次。

---

## Phase 4：升級——用 `/goal` 讓它自己跑完整個 plan 🎯

Phase 3 你靠「go」一路手動推到 merge。其實**最後那段連跑可以交給 Claude 自己**。

`/goal` 是 Claude Code **v2.1.139+ 的原生指令**：你給一個「完成條件」，它就一輪一輪自己跑到達標才停，每輪由一個獨立評估模型（預設 Haiku）檢查條件成立了沒 —— 把「幹活的 agent」和「判斷做完沒的 agent」分開。

**關鍵洞察**：superpowers 在 brainstorming + writing-plans 階段，剛好把 `/goal` 要的三樣東西都產好了：

| superpowers 產出 | `/goal` 要的 |
|---|---|
| design doc 的驗收標準 | 可量測的完成條件 |
| writing-plans 的 task 清單 | 要跑的待辦 queue |
| `verification-before-completion` 的檢查指令 | 「怎麼證明做完」 |

所以 plan 一寫好，你可以不喊「go」，改下一條 `/goal`：

```
/goal 完成 docs/superpowers/plans/2026-05-13-todo-cli.md 全部 task。
完成條件（每輪結尾貼證據）：uv run pytest -q 全綠（exit 0）+ todo-cli add/list/done 都能跑。
禁區：不得修改現有 test 的 assert、不准 skip。
過程照 TDD：每個 task 先 RED 再 GREEN。
```

然後走開。Claude 跑一個 task → evaluator 查 pytest 是否真的綠 → 沒綠就再開一輪，直到達標自動停。

> **教學金句**：「superpowers 給**紀律**，`/goal` 給**續航**。少了 superpowers，`/goal` 會朝沒設計過的目標狂奔；少了 `/goal`，你得自己當人肉 while-loop。」

📌 完整操作（手動連跑 vs `/goal` 對比表、寫完成條件的鐵則、卡點對照）看同目錄 **`superpowers_production_walkthrough.md` 的 Phase 4.5**。

---

## 常見問題 / FAQ

**Q1：我打了「做 todo list」但沒觸發 brainstorming？**
A：檢查 (1) plugin 真的裝了嗎？(2) 重啟過 Claude Code 嗎？(3) `/hooks` 看 SessionStart hook 在跑嗎？

**Q2：subagent-driven-development 跟 executing-plans 差在哪？**
A：前者**同一個 session 內**派 subagent；後者跨 session 用 batch + 人類 checkpoint。短專案用前者，長專案 / 要中斷恢復用後者。

**Q3：我不想用 TDD，可以跳過嗎？**
A：可以，但 `test-driven-development` 的 description 寫「Use when implementing any feature or bugfix」——你不主動關掉它就會跳。要跳就在 CLAUDE.md 加「don't use TDD」，superpowers 自己的優先級規定 user instruction > skill。

**Q4：worktree 滿了硬碟怎麼辦？**
A：跑完用 `finishing-a-development-branch`，它會清。或手動 `git worktree remove <path>`。

**Q5：我想改 skill 內容，PR 上去會被收嗎？**
A：**幾乎不會**。看 `CLAUDE.md`——94% PR 退件率，contributor guide 講得很白。要改就 fork 自己用。

**Q6：plan 寫好後一定要手動「go」嗎？**
A：不用。下一條 `/goal`（完成條件＝`uv run pytest` 全綠 + 不准改現有 test）就能讓它自己跑完，要 Claude Code v2.1.139+。完整接法見 `superpowers_production_walkthrough.md` 的 Phase 4.5。

---

## 卡點對照表 ⭐

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 安裝完打話沒效果 | SessionStart hook 沒注入 | 重啟 Claude Code，或 `/hooks` 看 |
| brainstorming 問太久很煩 | 你回答太敷衍它就一直問 | 認真給 constraint：時長、技術棧、限制 |
| TDD 跑到一半測試環境壞掉 | uv venv 沒建好 | 退到 Phase 0 重做 `uv init` |
| subagent 寫的 code 風格不一致 | 你沒在 design 階段定 style | 之後在 CLAUDE.md 加 style guide |
| `finishing-a-development-branch` 顯示「testsfailing」 | 真的有測試壞掉 | 別 merge，回去跑 `systematic-debugging` |
| Claude 跳過 brainstorming 直接寫 code | description 沒被讀到 | 開 `/skill` 看列表，或 `using-superpowers` 沒注入 |
| 教學現場 plugin 還沒裝 | 沒先準備好 | **提前裝**，現場 demo 不裝 |
| `/goal` 一直不收斂、燒 token | 完成條件不可量測（「做好一點」） | 改成 `pytest exit 0` 類硬條件，並要求每輪貼證據 |

---

## 講師私房筆記

### 教學節奏

| 段落 | 建議時間 | 重點 |
|---|---|---|
| 開場 + 痛點 | 5 分鐘 | 對比一般用法 vs superpowers，挑起痛 |
| Phase 0 安裝 | 5 分鐘 | **現場別裝**，提前裝；不然會卡 |
| Phase 1 14 skill | 15 分鐘 | 看表格、講 trigger 時機，**不要逐個唸完整 SKILL.md** |
| Phase 2 SKILL.md 剖開 | 10 分鐘 | 只展 1 個（brainstorming），講「HARD-GATE」與「Anti-Pattern」設計巧思 |
| Phase 3 實戰 | 50 分鐘 | 真的 demo 跑一次 todo-cli，**不要打 cheat sheet**，現場讓觀眾看 AI 怎麼問問題 |
| FAQ + 收尾 | 5 分鐘 | 留時間問問題 |

### 故意踩坑（比口頭講有效）

1. **brainstorming 階段故意敷衍**：對 Claude 說「都可以你決定」。觀眾會看到 AI 反問「我需要你決定 X，因為...」——讓他們體會「你不認真給 spec，AI 就是垃圾進垃圾出」。
2. **故意跳過 TDD**：對 Claude 說「直接寫實作就好」。它會跳出來說「TDD skill 規定先測後寫」——觀眾會看到 skill 的「強制力」。
3. **故意在 worktree 外改檔**：觀眾會看到 superpowers 對 git 狀態的清潔強迫症。

### 給不同角色的推薦

| 角色 | 講重點 |
|---|---|
| 軟體工程師 | Phase 2 + 3，重點在「工程紀律」怎麼變成 skill 強制力 |
| 技術 PM / TPM | Phase 1 表格 + 整合 demo，看「AI 怎麼跑研發流程」 |
| 教 AI 工具的講師 | Phase 2 + writing-skills，學「怎麼寫會 trigger 的 skill」 |
| 開源 contributor | **重點講 CLAUDE.md 的 94% 退件率**，不要傻傻丟 PR |

### Kevin 親自驗過

- 我在 Mac Sonoma + Claude Code 上實測過 acceptance test「Let's make a react todo list」會自動觸發 brainstorming。✅
- subagent-driven-development 在中型 task（30 分鐘量）效果最好，超過 1 小時的還是建議 `executing-plans`（跨 session）比較不會出包。
- 「**superpowers + uv + Mac MPS**」是我目前認為最順的本機開發三件套（uv 取代 pip、MPS 取代 CUDA）。

---

## 一句話總結

> **Superpowers 把「跟 AI 對話」升級成「跟 AI 跑研發流程」——你失去的是想到哪做到哪的自由，得到的是不再被 AI 幻覺浪費時間的紀律。**

---

## 進階閱讀

- 🔗 [Superpowers 官方 README](https://github.com/obra/superpowers)
- 🔗 [Jesse Vincent 的釋出文 (2025-10-09)](https://blog.fsck.com/2025/10/09/superpowers/)
- 🔗 [Anthropic 官方 plugin marketplace](https://claude.com/plugins/superpowers)
- 🔗 [Discord 社群](https://discord.gg/35wsABTejz)
- 🔗 本機 repo：`/Users/kevinluo/claude-code-complete-tutorial/important-plugins/superpowers/`

---

_Last updated: 2026-05-22（加 Phase 4：plan 寫好接 `/goal` 自動跑完）_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材：`../Projects/plugins-from-zero-to-marketplace/`（plugin 從零到 marketplace 上架的三件式範例）_
_專案實戰案例：`~/Desktop/todo-cli-demo/`（依本 walkthrough Phase 3 跑完後會產出）_
