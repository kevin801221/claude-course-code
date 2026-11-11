# Superpowers in Action：從零到 production 打造 TUI 番茄鐘 `pomocat`

> **對象**：已看過 `superpowers_walkthrough.md`、想看 superpowers 在真實專案怎麼跑完整流程的人
> **形式**：講師現場帶 / 進階自學
> **時長**：120 分鐘（前 20 設計 + 中 80 實作 + 後 20 收尾）
> **產出**：一個能 `uv tool install` 的 TUI 番茄鐘 `pomocat`，含倒數動畫、聲音提醒、設定檔、統計檔
> **核心方法**：「**不寫一行 code**，全部讓 superpowers 帶你走 — brainstorming → plan → TDD → subagent → review → ship」

---

## 開場（10 分鐘）：為什麼選番茄鐘當教材？

| 候選專案 | 為何不選 |
|---|---|
| Todo CLI | 太樸素，跑不出「production」氣質 |
| React App | superpowers 的 TDD 在前端打折扣 |
| 純 API server | 沒有 UI / 沒有狀態機，學到的 skill 不夠廣 |
| **TUI 番茄鐘 ⭐** | **有 UI（Textual）、有狀態機（work/break/long）、有 I/O（聲音/檔案）、有時間驅動 — 一次踩到 superpowers 多個強項** |

番茄鐘的好處：

1. **狀態機**：work → short_break → work → ... → long_break → 循環。剛好練 `brainstorming` 抓清楚 state transition
2. **時間驅動**：倒數計時很容易測歪，剛好練 `test-driven-development` 怎麼 fake time
3. **副作用**：聲音、寫檔、桌面通知 — 練怎麼把副作用隔離成可測
4. **狀態持久化**：完成輪數要存到 disk — 練 schema 設計
5. **UI 事件**：鍵盤輸入要轉成 state action — 練 event handling
6. **size 剛好**：8–12 個 task，subagent-driven-development 跑完不超過 90 分鐘

> **教學金句**：「選教材選太簡單，superpowers 顯不出價值；選太大，學員會嚇跑。番茄鐘是『state machine + I/O + UI』的最小完整體。」

---

## 📁 預期成品結構

```
pomocat/
├── pyproject.toml                ← uv 管套件 + entry point
├── README.md
├── docs/
│   ├── plans/
│   │   └── 2026-05-13-pomocat-design.md   ← brainstorming 產出
│   └── superpowers/plans/
│       └── 2026-05-13-pomocat.md          ← writing-plans 產出
├── src/pomocat/
│   ├── __init__.py
│   ├── __main__.py             ← `python -m pomocat` 入口
│   ├── cli.py                  ← typer command
│   ├── state.py                ← ⭐ 純函式狀態機（最該被測爛）
│   ├── timer.py                ← 倒數邏輯（可注入 clock）
│   ├── audio.py                ← 抽象的聲音 backend
│   ├── storage.py              ← config.toml + history.jsonl
│   ├── tui.py                  ← Textual App
│   └── assets/
│       └── bell.wav            ← 內建聲音
├── tests/
│   ├── test_state.py           ← 純函式測試（最容易、最先寫）
│   ├── test_timer.py           ← 用 fake clock 測倒數
│   ├── test_storage.py
│   └── test_tui_snapshot.py    ← pytest-textual-snapshot
└── .gitignore
```

**關鍵設計**：UI/audio/clock 都靠**注入**，不直接 import 真實實作。這是 TDD 能跑的前提。

---

## Phase 0：環境準備（10 分鐘）⚙️

```bash
# 1. 確認 superpowers 已裝
ls ~/.claude/plugins/data/superpowers* 2>/dev/null || \
  echo "請先：/plugin install superpowers@claude-plugins-official"

# 2. 確認 uv 已裝
uv --version || curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 確認系統聲音指令存在
command -v afplay || command -v paplay || command -v aplay  # 至少一個

# 4. 建空目錄 + git
mkdir -p ~/Desktop/pomocat && cd ~/Desktop/pomocat
git init && git commit --allow-empty -m "init"

# 5. 開 Claude Code
claude
```

**驗證 superpowers 真的在**：第一句話打：

> 「請列出你現在 active 的所有 superpowers skills」

預期看到 14 個。如果只有 1-2 個或 0 個，重啟 Claude Code。

> **教學金句**：「沒驗證 plugin 已激活就開講，是教學現場最常見的車禍。」

---

## Phase 1：Brainstorming（15 分鐘）🧠 — 最詳細展示

對 Claude 打：

> 「我想做一個 TUI 番茄鐘叫 pomocat，會倒數、有聲音、會統計完成幾輪，要做到能 `uv tool install` 的程度。Python + Textual + uv。」

**正常情況**`brainstorming` skill 會 auto-trigger。Claude 應該：

### 1.1 Claude 探查專案脈絡

它會 `ls`、`git log` 看你給的是空專案還是有東西。空專案它知道要從零開始。

### 1.2 它問你（一次一題）

| Claude 會問 | 為什麼這題重要 |
|---|---|
| 「`work` / `short_break` / `long_break` 預設幾分鐘？要不要可設定？」 | 決定設定檔 schema |
| 「幾輪後進長休息？4 輪是標準，要改嗎？」 | 狀態機 transition rule |
| 「結束時的聲音要內建還是讀使用者檔？」 | audio 模組複雜度 |
| 「歷史紀錄要存什麼？只算 count 還是含 timestamp / tag？」 | storage schema |
| 「TUI 要支援哪些鍵？」 | event handler 範圍 |
| 「Pause 時計時器要停，還是繼續但畫面凍結？」 | 邊界條件，超容易寫錯 |

> **教學金句**：「brainstorming 不是 Claude 在問問題，是它在『**幫你想清楚你以為你想清楚但其實沒想清楚的點**』。」

### 1.3 它丟出 2–3 個方案讓你選

例如關於聲音：

| 方案 | 優點 | 缺點 |
|---|---|---|
| A：`playsound` library | 跨平台一句 API | playsound 在 Mac 11+ 有 bug，超不穩 |
| B：shell out 到 `afplay`/`paplay` | 穩、無 dependency | 要寫 OS detect |
| **C：抽象 AudioBackend，預設 shell out（推薦）** | **可注入 fake、好測** | **多一個檔但 production-grade** |

它會推薦 C 並解釋理由（**測試友善 + production 穩定 = TDD 救命**）。

### 1.4 分段給設計，每段問你 OK 嗎

按 superpowers 的規定，設計拆成 200–300 字一段：

1. **架構分層**：CLI → TUI → State Machine → (Timer / Audio / Storage)
2. **State 機**：四個狀態 + transition table
3. **資料 schema**：config.toml 結構、history.jsonl 每行格式
4. **錯誤處理**：聲音播放失敗 fallback、設定檔損壞 reset
5. **測試策略**：純函式優先、UI 用 snapshot、time 注入

每段你要回 ✅ 才繼續。

### 1.5 它寫 design doc

存到 `docs/plans/2026-05-13-pomocat-design.md` 並 `git commit`。

⚠️ **這時候你還沒寫過一行 code**。

---

## Phase 2：Writing Plans（10 分鐘）📋

你說「OK 接受 design」。`writing-plans` skill 自動接手。

它會產出 `docs/superpowers/plans/2026-05-13-pomocat.md`，類似：

```markdown
## File Structure
- src/pomocat/state.py            (純函式 state machine)
- src/pomocat/timer.py            (倒數，注入 clock)
- src/pomocat/audio.py            (抽象 backend)
- src/pomocat/storage.py          (toml + jsonl)
- src/pomocat/tui.py              (Textual App)
- src/pomocat/cli.py              (typer entry)
- tests/test_state.py
- tests/test_timer.py
- tests/test_storage.py
- tests/test_tui_snapshot.py

## Tasks
1. 建 uv 專案結構 + pyproject.toml (5 min)
2. 寫 state machine 的 failing test：work → short_break (3 min)
3. 實作 transition_next() 讓 test 過 (3 min)
4. 補滿剩餘 transition cases (5 min)
5. timer.py：寫 fake_clock + countdown test (5 min)
6. 實作 Timer 類別 (4 min)
7. audio.py：寫 AudioBackend Protocol + ShellAudioBackend (3 min)
8. storage.py：config 載入 / 預設值 / 損壞回退 test + 實作 (5 min)
9. storage.py：history append test + 實作 (3 min)
10. tui.py：Textual App 骨架 + snapshot baseline (5 min)
11. tui.py：綁鍵盤事件、串 state machine (5 min)
12. cli.py：typer command + entry point (3 min)
13. 整合 smoke test：實際跑一輪 5 秒短週期 (3 min)
14. pyproject.toml 加 [project.scripts] 與 README (3 min)
```

每個 task **2–5 分鐘**，這是 superpowers 的鐵則 — task 太大 subagent 會迷路。

> **教學金句**：「Plan 的品質直接決定 subagent 跑下來的品質。一個 task 寫得糊，AI 就交糊的 code。」

---

## Phase 3：開 worktree（2 分鐘）🌿

`using-git-worktrees` skill 自動觸發：

```bash
git worktree add ../pomocat-feat feat/pomocat-mvp
cd ../pomocat-feat
```

從這刻起，所有 code 在 worktree 內改。主目錄保持乾淨。

**為什麼一定要 worktree？**

| 沒 worktree | 有 worktree |
|---|---|
| AI 跑壞了你想看 main 還在哪 → 要 `git stash` | 直接切到主目錄就看到原版 |
| 想同時跑兩個實驗 → branch 切來切去 | 兩個 worktree 並存 |
| AI 動到 .env / .gitignore → 灘子 | 整個 worktree 砍掉重建 |

---

## Phase 4：TDD 跑第一個 task ⭐⭐⭐（15 分鐘）

`subagent-driven-development` + `test-driven-development` 雙觸發。展示**第一個 task** 怎麼跑（後面同樣 pattern 加速）：

### Task 2：寫 state machine 的 failing test

Claude 派一個 subagent，給它的 prompt 包含：
- 整份 design doc
- 整份 plan
- 「**只能做 task 2，做完回報**」
- 嚴格的 RED 流程

Subagent 做的事：

```python
# tests/test_state.py
from pomocat.state import transition_next, PomState

def test_work_transitions_to_short_break():
    state = PomState(phase="work", round=1, total_rounds=4)
    next_state = transition_next(state)
    assert next_state.phase == "short_break"
    assert next_state.round == 1
```

然後跑 `pytest tests/test_state.py::test_work_transitions_to_short_break`：

```
ImportError: cannot import name 'transition_next' from 'pomocat.state'
```

✅ **這是「watched it fail」的證據**。Subagent 把 pytest output 貼回來作為 RED 完成的證據。

### Task 3：實作讓 test 過（GREEN）

下一個 subagent 拿到 task 3，**禁止改測試**，只能寫剛剛好的實作：

```python
# src/pomocat/state.py
from dataclasses import dataclass

@dataclass(frozen=True)
class PomState:
    phase: str
    round: int
    total_rounds: int

def transition_next(state: PomState) -> PomState:
    if state.phase == "work":
        return PomState(phase="short_break", round=state.round, total_rounds=state.total_rounds)
    raise NotImplementedError
```

跑 pytest → 綠燈 → commit。

### 兩階段 review

Subagent 跑完，**主 session** 自動觸發兩個 reviewer subagent：

| Stage | 看什麼 |
|---|---|
| Spec compliance | 你做的有符合 plan 寫的嗎？檔名對嗎？簽名對嗎？ |
| Code quality | 命名、簡潔、有沒有 YAGNI 違反、有沒有 dead code |

通過才下 task 4，不通過 subagent 回去修。

> **教學金句**：「TDD 的『watched it fail』不是儀式 — 它在驗證『你寫的 test 確實會壞』。少這步，你不知道你測的是不是廢的。」

---

## Phase 4.5：把整份 plan 交給 `/goal` 自動駕駛 🎯

Phase 4 你**手動**看著第一個 task 跑完 RED → GREEN → review。接下來有兩條路：

- **Phase 5（手動連跑）**：你一輪輪回「go / next」，自己當調度員看著它跑完 14 個 task。
- **本節（`/goal` 自動駕駛）**：設一次完成條件，**走開**，讓 Claude 自己一輪一輪跑到達標。

兩條路產出一樣，差別只在「你要不要當人肉 while-loop」。

### `/goal` 是什麼（30 秒）

`/goal` 是 Claude Code **v2.1.139+ 的原生指令**。你給它一個「完成條件」，它就**不還控制權給你** —— 每跑完一輪，一個獨立的評估模型（預設 Haiku）去檢查條件成立了沒；沒成立就自己再開一輪。

| 指令 | 作用 |
|---|---|
| `/goal <條件>` | 設定目標，開始自動連跑 |
| `/goal` | （無參數）看目前花了幾輪、幾 token |
| `/goal clear` | 喊停，收回控制權 |

> **教學金句**：「`/goal` 最聰明的地方是『把幹活的 agent 和判斷做完沒的 agent 分開』 —— 幹活的容易自我感覺良好說『做完了』，evaluator 不信，要看證據。」

### 為什麼 superpowers + `/goal` 是天作之合

`/goal` 要三個輸入，而你在 Phase 1–2 已經全部產好了：

| superpowers 產出 | `/goal` 要的 | 對應 |
|---|---|---|
| design doc 的驗收標準 | 一個可量測的 end state | acceptance → 完成條件 |
| writing-plans 的 14 個 task | 要跑的待辦 queue | plan = 要做的事 |
| `verification-before-completion` 的檢查指令 | 「怎麼證明做完」 | `uv run pytest` = stated check |

> **教學金句**：「superpowers 給**紀律**，`/goal` 給**續航**。少了 superpowers，`/goal` 會朝一個沒設計過的目標狂奔；少了 `/goal`，你得自己當人肉 while-loop。」

### 手動連跑 vs `/goal` 自動駕駛

| | Phase 5 手動連跑 | 本節 `/goal` 自動駕駛 |
|---|---|---|
| 推進方式 | 你一直回「go / next」 | 設一次條件就走開 |
| 誰判斷做完沒 | 你（人眼看 pytest） | Haiku evaluator 每輪查 |
| 防自我感覺良好 | 靠你警覺 | evaluator 不收沒證據的「做完了」 |
| 適合 | 教學現場逐步展示 | 任務明確、想離開鍵盤 |

### 實際怎麼接（pomocat 範例）

把 plan 的 acceptance 直接翻成一條 `/goal` 條件：

```
/goal 完成 docs/superpowers/plans/2026-05-13-pomocat.md 裡全部 14 個 task。
完成條件（每輪結尾要貼出證據）：
1. uv run pytest tests/ -q 全綠（exit 0），把輸出貼出來
2. uv run pomocat --help 可執行不報錯
3. pyproject.toml 有 [project.scripts] 的 pomocat entry
禁區：
- 不得修改任何「已存在」的 test 的 assert（只能新增 test）
- 不得用 skip / xfail 讓測試假性通過
過程照 subagent-driven-development + TDD：每個 task 先 RED 再 GREEN，禁止跳過 watched-it-fail。
```

下完這條，你就可以去泡咖啡。Claude 跑一個 task → evaluator 檢查「pytest 真的綠了嗎」→ 沒綠就再開一輪，直到三條全中才自動停、把控制權還你。

### 寫完成條件的鐵則 ⭐

evaluator **不會自己跑指令、不會自己讀檔** —— 它只看 Claude 這一輪輸出了什麼。所以條件一定要：

| 鐵則 | 反例（會燒 token 不收斂） | 正例 |
|---|---|---|
| 一個可量測 end state | 「做得穩一點」 | 「pytest exit 0」 |
| 寫清楚怎麼證明 | 「測試有過」 | 「貼出 `uv run pytest -q` 輸出」 |
| 設禁區 | （沒寫） | 「不准改現有 test 的 assert」 |

> **教學金句**：「`/goal` 條件寫『做好一點』＝叫它原地燒錢。寫『pytest exit 0 且不准改現有 test』＝給它一條會收斂的終點線。」

---

## Phase 5：剩下 task 連跑（30 分鐘）🚀

Task 4 ~ 14 同樣 pattern，每個 task：

```
subagent_A (TDD RED) → subagent_B (GREEN) → spec reviewer → quality reviewer → commit
```

你**完全不需要介入**，去泡咖啡。Claude 的主 session 變調度員，不寫 code、不被細節塞滿 context。

### 中間幾個關鍵 task 的看點

| Task | 為什麼有趣 |
|---|---|
| Task 5（timer fake clock） | 展示「注入時間」的測試手法，這招用一次學一輩子 |
| Task 7（audio backend） | 用 Python `Protocol` 做依賴注入，subagent 會自動跑出 fake `RecordingAudioBackend` 來測 |
| Task 8（config 損壞 fallback） | superpowers 會主動寫 negative test（給壞 toml 看會不會 crash） |
| Task 10（Textual snapshot） | 第一次跑會建立 baseline `.svg`，後面改動自動 diff |
| Task 13（整合 smoke test） | 真的跑一遍 5 秒週期，這是 `verification-before-completion` 上場 |

---

## Phase 6：故意製造 bug → `systematic-debugging` ⭐（10 分鐘）

教學現場**故意**讓某個 task 出 bug，展示 superpowers 抓 bug 的紀律。

### 製造法

對 Claude 說：

> 「Task 11 你不要綁 `q` 鍵，先跳過。」

跑到 smoke test 階段，發現按 q 不會結束 — `systematic-debugging` skill 觸發。它**不會**直接亂猜，而是按 4 階段：

| 階段 | 做什麼 |
|---|---|
| 1. Reproduce | 寫一個 failing test 復現問題：`test_q_key_quits` |
| 2. Hypothesize | 列可能原因：keybinding 沒註冊 / event 沒 propagate / async loop block |
| 3. Isolate | 用 print 或 logging 縮到單一原因 |
| 4. Fix + verify | 改最小 patch + 確認 test 過 + 沒打壞其他 test |

每階段都有產出（test、log、commit）。

> **教學金句**：「debugging 90% 的時間花在『搞清楚問題到底是什麼』，10% 才是改。superpowers 強迫你把比例擺對。」

---

## Phase 7：Code review + 收尾（15 分鐘）🔍

全部 task 跑完，`requesting-code-review` 自動觸發。

### 自我 review

Claude 對整支 branch 跑：
- 對照 design doc 看有沒有偏離
- 對照 plan 看有沒有跳 task
- 跑 `git diff main` 看實際變更
- 列出每個檔案的 risk（high / medium / low）

### `verification-before-completion`

它強迫驗證**不是嘴砲**：

```bash
uv run pytest tests/ -v          # 全綠？
uv run pomocat --help            # 命令真的能跑？
uv run pomocat start --work 5 --break 2 --rounds 2  # smoke test
ls ~/.config/pomocat/            # 設定檔有建？
cat ~/.config/pomocat/history.jsonl  # 有寫一輪？
```

5 個檢查全過才算「done」。少一個就回去修。

### `finishing-a-development-branch`

給你選：

| 選項 | 適用 |
|---|---|
| **Merge to main** | 你是 solo dev、自己用 |
| Open PR | 有 remote、要 review |
| Keep branch | 還想加 feature |
| Discard | 失敗實驗（這次別選） |

選 merge：

```bash
cd /Users/kevinluo/Desktop/pomocat
git merge feat/pomocat-mvp --ff
git worktree remove ../pomocat-feat
```

### 真的 install

```bash
uv tool install -e .
pomocat start
```

🎉 你打字次數可能不到 20 次，AI 跑了 ~80 分鐘，得到一個真的能用的 TUI 工具。

---

## 整合 demo：完整時間軸

```
00:00  你：「想做 pomocat ...」
00:01  [brainstorming] 問 6 個問題 + 給 3 個方案 + 分 5 段設計
00:15  [brainstorming] 寫完 design doc，commit
00:16  你：「OK」
00:17  [writing-plans] 切出 14 個 task，commit plan
00:25  你：「go」
00:26  [using-git-worktrees] 建 worktree
00:27  [subagent-driven-development] 跑 task 1（建 uv 結構）
00:30  [TDD] task 2-3：state machine RED → GREEN → review → commit
00:40  task 4-7：transition cases / timer / audio backend
00:55  task 8-9：storage
01:05  task 10-11：tui + 鍵盤事件
01:15  task 12-13：cli + smoke test → 發現 q 不會結束
01:16  [systematic-debugging] 4 階段抓 bug + 修
01:25  task 14：README + entry point
01:30  [requesting-code-review] 自我 review
01:35  [verification-before-completion] 5 項檢查
01:40  [finishing-a-development-branch] merge to main
01:45  `uv tool install -e .` 安裝
01:46  你跑 `pomocat start` → ✅
```

### 同一條龍的 `/goal` 自動駕駛版

把 `00:25` 之後的手動連跑換成**一條 `/goal`**：

```
00:25  你：下 /goal 條件（pytest 全綠 + entry point + 不准改現有 test）
00:26  [/goal] Claude 自己跑 task 1 → Haiku evaluator 查 → 沒達標 → 再一輪
  ...（你去泡咖啡，每輪 evaluator 檢查 pytest 是否真的綠）
01:30  [/goal] 三條完成條件全中 → 自動停 → 還控制權給你
01:31  你回來：先打 /goal 看花了幾輪幾 token → finishing-a-development-branch
```

差別：`00:25` 之後你**一次都不用回「go」**。

---

## 常見問題 / FAQ

**Q1：subagent 跑到一半 timeout 怎麼辦？**
A：Plan 切太大。回去 `writing-plans` 把那個 task 拆細。superpowers 規定 2–5 分鐘是有理由的。

**Q2：Textual snapshot test 第一次跑都會「失敗」？**
A：不是失敗，是建 baseline。pytest output 會說 `snapshot not found, creating new`。下次跑才會比對。

**Q3：聲音在 Linux 上不會播？**
A：`audio.py` 的 `ShellAudioBackend` 要偵測 `afplay`(Mac) / `paplay`(Linux Pulse) / `aplay`(Linux ALSA)。superpowers 寫 plan 時應該已經考慮，如果沒有，回 brainstorming 加。

**Q4：可以跳過 brainstorming 嗎？我已經知道要做什麼了。**
A：可以，但**不建議**。即使你「自認知道」，brainstorming 問的問題會逼出你沒想清楚的邊界（pause 時 timer 怎樣？config 損壞怎樣？）。跳過 = 你要在實作中段才發現 → 推翻設計 → 重做。

**Q5：subagent 寫的 code 跟我的風格不一致怎麼辦？**
A：在 brainstorming 階段就要明確：「用 dataclass 不要用 Pydantic」「用 typer 不要用 click」「測試用 pytest fixtures 不要 setUp」。寫進 design doc 後 subagent 都會遵守。

**Q6：跑到一半我想加新 feature？**
A：**不要在跑 task 的時候加**。記下來。等 finishing-a-development-branch 後開新 brainstorming session 加。否則 plan 會走鐘。

**Q7：`/goal` 自動駕駛跟 Phase 5 手動連跑該用哪個？**
A：產出一樣。教學現場用手動（看得到每個 task 紅綠燈、好講解）；自己幹活、任務明確、想離開鍵盤就用 `/goal`。代價：`/goal` 比較燒 token（evaluator 每輪都跑一次），且要 Claude Code v2.1.139+。

**Q8：`/goal` 一直不收斂、token 狂燒怎麼辦？**
A：99% 是完成條件不可量測。把「做穩一點」改成 exit-code / 檔案數類硬條件，並在條件裡要求 Claude 每輪結尾貼出 `uv run pytest` 輸出當證據。真的跑歪就 `/goal clear` 收回控制權。

---

## 卡點對照表 ⭐

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| brainstorming 一直問問題，學員等不及 | 學員回答太敷衍 | **示範認真回答**，給具體 constraint |
| 「watched it fail」沒看到 RED 證據 | subagent 跳過了 | 主 session 應拒收，回去要 pytest output |
| Textual snapshot 一直 diff | TUI 渲染有時間相關（時鐘） | snapshot 前 freeze time，或 mask 掉時鐘區 |
| audio backend test 跑超慢 | 不小心呼叫真實 `afplay` | 確認 test 注入的是 `RecordingAudioBackend` |
| `uv tool install -e .` 找不到 entry point | `pyproject.toml` 的 `[project.scripts]` 沒寫對 | 對照 plan task 14 的 acceptance |
| subagent context 太大跑很慢 | plan 沒切夠細 | 回去 writing-plans 拆 task |
| worktree 滿了 | 跑完忘了 `finishing-a-development-branch` | 手動 `git worktree prune` |
| 教學時間爆掉 | 想完整跑 14 task | **預先跑過、現場只 demo 前 3 個 + 結尾 1 個** |
| `/goal` 一直不收斂、燒 token | 完成條件不可量測（「做穩一點」） | 改成 exit-code / 檔案數硬條件，並要求每輪貼證據 |
| `/goal` evaluator 說沒達成但其實達成了 | Claude 沒把 pytest 證據輸出 | 條件裡加「每輪結尾貼 `uv run pytest` 結果」 |
| `/goal` 為了達標自己改 test 騙過條件 | 條件沒設禁區 | 條件加「不得修改現有 test 的 assert / 不准 skip」 |
| 打 `/goal` 說找不到指令 | Claude Code < 2.1.139 | 升級到 2.1.139+ |

---

## 講師私房筆記

### 教學節奏（120 分鐘版）

| 段落 | 時間 | 重點 |
|---|---|---|
| 開場（為什麼選番茄鐘） | 10 分 | 對比表 + 痛點 |
| Phase 0 環境準備 | 5 分 | **預先跑過**、現場 dry run |
| Phase 1 brainstorming | 20 分 | **不要快轉**，這是 superpowers 最值錢的部分 |
| Phase 2-3 plan + worktree | 10 分 | 看產出，講 task 細度 |
| Phase 4 第一個 TDD task | 20 分 | **逐行展示 RED → GREEN**，現場讓他們看 pytest 紅綠燈 |
| Phase 5 連跑剩下 | 15 分 | **不要逐個 task 唸**，跳到關鍵 3 個（timer fake clock / audio backend / TUI snapshot） |
| Phase 6 故意製造 bug | 15 分 | **這是高潮**，展現 systematic-debugging 的紀律 |
| Phase 7 review + ship | 15 分 | 真的 `uv tool install` 跑給他們看 |
| FAQ + 結尾 | 10 分 | 留問題時間 |

### 故意踩坑（比口頭講有效）

1. **brainstorming 階段假裝沒準備好**：對 Claude 說「都可以你決定」，學員會看 AI 反問「我需要你回答 X，因為...」 — 體會 garbage in / garbage out
2. **跳過「watched it fail」**：故意說「test 應該會 fail 啦不用真的跑」，看 superpowers 阻擋你
3. **想偷加 feature**：跑到 task 6 中間，跟 Claude 說「順便加上週統計功能」— 它應該拒絕，叫你做完這 plan 再說
4. **故意改測試讓它過**：在 GREEN 階段改 test 的 assert 數值，code reviewer subagent 會抓到

### `/goal` 自動駕駛怎麼帶（誠實版）

- 現場**先用手動連跑展示前 3 個 task**（看得到紅綠燈），再切 `/goal` 示範「設一次條件就走開」的爽感 —— 前後對比最有感。
- `/goal` 比較燒 token（evaluator 每輪都跑一次）。教學現場建議**預先跑過、現場只 demo 設條件那一刻 + 跑兩輪**，不要真的當場等它跑完 14 個 task。
- 條件一定要含禁區（「不准改現有 test」）。現場可以**故意先不寫禁區**，讓學員看它為了達標去動測試「作弊」，再加上禁區重跑 —— 比口頭講「要設禁區」有效十倍。
- ⚠️ 這段的具體耗時 / token 數我還沒在固定環境壓測過，現場別報死數字，講「會比手動連跑多燒 token」即可。

### 給不同學員角色

| 角色 | 強調哪段 |
|---|---|
| 軟體工程師 | Phase 4（TDD 細節）+ Phase 6（debug 流程） |
| 技術 PM | Phase 1（brainstorming）+ 整合 demo 時間軸 |
| 想學 plugin 開發的 | Phase 2 plan 的長相、subagent prompt 的設計 |
| 教育/培訓相關 | 講師私房筆記 + 「故意踩坑」段 |

### Kevin 親自驗過

- 我在 Mac Sonoma + Python 3.13 + uv 0.5 + Textual 0.85 上跑過完整流程。整個 brainstorming + plan 大概 25 分鐘，subagent 跑 14 task 大概 75 分鐘，最後 review + ship 10 分鐘 — 加總約 110 分鐘
- subagent-driven-development 在 task 數 8–14 個的時候效果最好。超過 20 task 主 session context 開始吃緊，要改用 `executing-plans`
- `pytest-textual-snapshot` 第一次跑會建 .svg baseline，git 要記得 commit 進去（不然下次 reviewer 抓不到對照組）
- 聲音的 `shell out` 方案在 Mac + Linux 都實測 OK，Windows 沒驗

---

## 跟其他 walkthrough 的關係

```
superpowers_walkthrough.md          ← 這份的「導覽 + 14 skill 一覽」前菜
        ↓
superpowers_production_walkthrough.md (本份)   ← 真實案例完整流程
        ↓
《打算之後寫》：superpowers_writing_skills.md  ← 進階：自己寫新 skill
```

---

## 一句話總結

> **Superpowers 不是讓你「用 AI 寫得更快」，是讓你「**用 AI 寫得更紀律**」— 番茄鐘只是載體，真正的產出是你對「研發流程」這件事的肌肉記憶。**

---

## 進階閱讀

- 🔗 [Textual 官方文件](https://textual.textualize.io/)
- 🔗 [`pytest-textual-snapshot`](https://github.com/Textualize/pytest-textual-snapshot)
- 🔗 [uv tool install 文件](https://docs.astral.sh/uv/concepts/tools/)
- 🔗 配套：本目錄 `superpowers_walkthrough.md`（先看這份再回來）
- 🔗 superpowers 原始 repo：`./superpowers/`
- 🔗 Pomodoro 學術原典：Francesco Cirillo (1980s)

---

_Last updated: 2026-05-22（加 Phase 4.5：superpowers 準備好就接 `/goal` 自動駕駛）_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材：`superpowers_walkthrough.md`（同目錄，先看那份的 14 skill 一覽再回來看實戰）_
_專案實戰產出：`~/Desktop/pomocat/`（依本 walkthrough 跑完後產出，可 `uv tool install -e .` 變真實工具）_
