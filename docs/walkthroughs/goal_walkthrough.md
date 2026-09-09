# `/goal` Walkthrough — 設一個「完成條件」，讓 Claude 自己跨輪做到達標

> **對象**：用過 Claude Code、跑長任務時受夠「每輪結束都要再打一次『繼續』」的工程師
> **形式**：講師現場帶 / 自學
> **時長**：50 分鐘
> **產出**：能用 `/goal` 設一個可驗證的完成條件，讓 Claude 不用你每輪 prompt 就一直做到達標；會寫「評估模型判得了」的條件；分得清 `/goal` vs `/loop` vs Stop hook vs auto mode 各該用哪個
> **核心方法**：先讓學員手動敲三次「繼續」感受痛點 → 設一條會自動收斂的 `/goal` → 故意寫一條 evaluator 判不了的爛條件，當場看它無限空轉，再修好
> **跟現有教材的關係**：[`hook_walkthrough.md`](hook_walkthrough.md) 講 Stop hook 的原理；**`/goal` 本質就是「一個 session 範圍的 prompt-based Stop hook 的快捷包裝」**——這份接在 Hook 那章之後講最順。課程位置：**Part 9 Hooks 延伸** ＋ **Part 16 進階主題（自主工作流）**。需要 **Claude Code v2.1.139 以上**。

---

## 開場（5 分鐘）：為什麼要學這個？

跑大任務時最煩的不是 Claude 不會做，是**它每做完一輪就把控制權還你**，你得一直打「繼續」「對，往下」「還沒好，再做」。一個搬 API 的工作可能要你手動催二十次。

有三種機制都能「讓這個 session 在你不開口時自己跑下一輪」，差別在**誰決定下一輪何時開始、何時該停**：

| 機制 | 下一輪何時開始 | 何時停 | 寫在哪 / 範圍 |
|---|---|---|---|
| **`/goal`** ⭐ | 上一輪一結束就接著跑 | **一個小快模型確認條件達成** | 你打的指令，**只這個 session** |
| `/loop` | 一個時間間隔到了 | 你喊停，或 Claude 自己判斷做完了 | slash 指令，這個 session |
| Stop hook | 上一輪一結束 | 你自己的腳本或 prompt 說了算 | `settings.json`，該 scope 的**每個** session |
| auto mode | （不啟動新一輪，只在同一輪內自動批工具） | Claude 自己判斷做完 | 設定檔 |

> **教學金句**：「`/loop` 是『每隔 N 分鐘戳一下』，`/goal` 是『達標前我不還你方向盤』——前者看時鐘，後者看終點線。」

`/goal` 跟 Stop hook 都是「**每輪結束都評估一次**」，但 `/goal` 是 session 級的快捷：打一句就生效，`/clear` 或結束就沒了，不污染 `settings.json`。auto mode 跟它**互補不衝突**——auto mode 去掉「每個工具都要你按同意」，`/goal` 去掉「每輪都要你打繼續」，兩個一起開才是真正無人值守。

---

## 📁 心智模型（一張圖看懂 `/goal` 在幹嘛）

```
你打：/goal <完成條件>
      │
      │  立刻啟動一輪（條件本身就是指令，不用再 prompt）
      ▼
┌──── Claude 做一輪 ────┐
│  跑測試 / 改檔 / commit │
│  結果都留在對話裡       │
└───────────┬───────────┘
            │  這輪一結束
            ▼
   ┌─────────────────────────┐
   │  小快模型（預設 Haiku）  │   ← 只讀「對話到目前為止」
   │  條件達成了嗎？          │   ← 不跑指令、不讀檔、不開工具
   └───────────┬─────────────┘
        ┌──────┴──────┐
       是              否（附一句 reason）
        │              │
        ▼              ▼
  清掉 goal，      把 reason 當下一輪的
  記一筆 achieved   方向，再跑一輪 ──┐
        │                          │
        ▼          └───────────────┘ 迴圈
   方向盤還你
```

**三個必須釘住的點**：

1. **設了就立刻跑**——`/goal ...` 不用再送第二句 prompt，條件本身就是第一輪的指令。
2. **評估的是「對話」，不是「真實世界」**——那個小模型不會去跑 `npm test`、不會去讀檔，它只看 Claude 在對話裡**秀出來**了什麼。這句話是整份 walkthrough 的脊椎，Phase 2 全在講它。
3. **每輪都有一句 reason**——「為什麼還沒達成」會出現在狀態列和 transcript，也是下一輪的指引。

---

## ⚙️ Phase 0：環境準備（5 分鐘）

跑之前先確認四件事，少一件 `/goal` 會直接告訴你為什麼不能用（不會默默裝死）：

| 檢查 | 為什麼 | 不過會怎樣 |
|---|---|---|
| Claude Code **≥ v2.1.139** | `/goal` 是這版才有 | 指令不存在 |
| 這個 workspace **接受過 trust 對話框** | evaluator 屬於 hooks 系統 | `/goal` 拒跑並說原因 |
| 沒有任何層級設 `disableAllHooks` | 同上，hook 全關它也不能跑 | 拒跑並說原因 |
| managed settings 沒設 `allowManagedHooksOnly` | 它是 session 級 hook，不是 managed 的 | 拒跑並說原因 |

> 💡 **強烈建議搭 auto mode 一起開**：`/goal` 幫你省掉「每輪打繼續」，但每一輪裡 Claude 還是會被「這個工具要你同意嗎」打斷。兩個一起開，才是「設了就走開喝咖啡」。auto mode 設定見 [`auto-mode-config`](https://code.claude.com/docs/en/auto-mode-config)。

---

## 🧠 Phase 1：設第一個 goal ⭐ 最詳細

同一個 `/goal` 指令，靠參數決定它是**設定 / 查狀態 / 清除**。一個 session 同時只能有一個 goal，再設一個會蓋掉舊的。

### 設定

```text
/goal all tests in test/auth pass and the lint step is clean
```

打下去**馬上開跑**，不用再送 prompt。goal 活著的時候，畫面會有個 `◎ /goal active` 指示器顯示它跑多久了。每輪結束評估模型回一句 reason，最新那句會出現在狀態檢視和 transcript，你隨時看得到 Claude 正在朝什麼修。

> **教學金句**：「`/goal` 設下去那一刻就是第一輪的開工槍——別再手賤補一句『開始吧』，那只是浪費一輪。」

### 它會一直跑——直到達成或你喊停

goal 不會自己累了就停。**只有兩種結束**：評估模型說達成了、或你 `/goal clear`。所以「**怎麼寫條件**」直接決定它是 30 秒收斂還是空轉一整晚——這就是 Phase 2。

---

## 📝 Phase 2：寫一條 evaluator 判得了的條件 ⭐⭐⭐（全篇最重要）

這是學員 100% 會踩、而且踩了還不知道自己踩了的坑。

**核心事實**：評估模型**不跑指令、不讀檔、不開工具**。它只讀「Claude 到目前為止在對話裡秀了什麼」。所以你的條件必須是「**Claude 自己的輸出能證明**」的東西。

| 你寫的條件 | evaluator 判得了嗎 | 為什麼 |
|---|---|---|
| `all tests in test/auth pass` | ✅ 判得了 | Claude 會跑測試，結果落在 transcript，模型讀得到 |
| `npm test exits 0 and git status is clean` | ✅ 判得了 | 有明確的證明方式，Claude 跑了就看得到 |
| `the code is correct and well-designed` | ❌ 永遠判不了 | 「correct」沒有對話裡的證據可看 → **無限空轉** |
| `the bug is fixed` | ❌ 很危險 | 沒說「怎麼算修好」，模型只能猜 |

一條撐得過很多輪的好條件，通常有三件事：

1. **一個可量測的終態**：測試結果、build exit code、檔案數、佇列空了
2. **一個講明的驗證方式**：`npm test exits 0`、`git status is clean`、`ls shows 5 files`
3. **路上不能動到的約束**：例如「不准改其他 test 檔」

> **教學金句**：「evaluator 是個沒手沒腳、只會讀對話的人。你的條件如果不能被『Claude 講出來的話』證明，它就只能一直回『還沒喔』——然後你的帳單一直跑。」

### 一定要加個剎車

條件可以到 4,000 字。**務必塞一句回合/時間上限**，否則寫爛了就燒一整晚：

```text
/goal every call site of fetchUser() compiles and the test suite passes,
or stop after 20 turns
```

Claude 每輪會對著「or stop after 20 turns」報進度，evaluator 也會從對話判這條。**這是現場 demo 的安全帶，帶課一定要先示範這個再放學員自己試。**

---

## 🛠 Phase 3：查狀態 / 清除 / 續跑 / 非互動

### 查狀態

```text
/goal
```

沒帶參數就是看現況。有 active goal 會顯示：條件、跑了多久、評估過幾輪、目前 token 花費、evaluator 最新那句 reason。沒 active 但這個 session 早先達成過，會顯示那條已達成的條件 + 它的時長/輪數/花費。

### 清除

```text
/goal clear
```

`stop`、`off`、`reset`、`none`、`cancel` 都是 `clear` 的別名。`/clear` 開新對話也會順手把 active goal 清掉。

### 續跑（resume 的行為要講清楚）

session 結束時還活著的 goal，用 `--resume` / `--continue` 回來會被還原——但**只有條件留著，輪數、計時器、token 花費基準全部歸零**。已達成或已清掉的 goal 不會還原。

### 非互動 / headless

`-p` 模式、桌面 app、Remote Control 都能用。`-p` 會把整個迴圈一次跑到達成：

```bash
claude -p "/goal CHANGELOG.md has an entry for every PR merged this week"
```

要中途喊停就 `Ctrl+C`。

---

## 整合 demo：一條龍跑完（10 分鐘現場）

```bash
# 前置：開 auto mode（少掉每輪的工具同意）
# 場景：把一個小模組從舊 API 搬到新 API

> /goal every call site of the old getUser() is migrated to fetchUser(),
  the project compiles, and all tests pass — or stop after 15 turns

# ↑ 打完就走開。觀察：
#   - ◎ /goal active 指示器開始跑
#   - 每輪結束自動接下一輪，你完全沒打字
#   - 狀態列那句 reason 一直在變（"還有 3 個 call site 沒搬"…）

> /goal          # ← 中途插一句查進度（不會打斷迴圈）

# 達成那刻：goal 自動清掉、transcript 記一筆 achieved、方向盤還你
```

跑完學員就懂：**設一次條件 → 後面每一輪都是 Claude 自己接的 → 達標自動收手**。對照「沒有 `/goal` 時你要手動催十五次」，痛點瞬間具體。

---

## 常見問題 / FAQ

**Q：跟 `/loop` 到底差在哪？我兩個都會 confuse。**
A：`/loop` 看**時鐘**（每隔 N 分鐘再跑），停在「你喊停或 Claude 覺得做完」。`/goal` 看**終點線**（上一輪一結束就接），停在「一個獨立小模型確認條件達成」。要「一直做到 X 為止」用 `/goal`；要「每 5 分鐘檢查一次部署」用 `/loop`。

**Q：evaluator 會自己去跑測試確認嗎？**
A：**不會**。它不開任何工具，只讀對話。所以條件要寫成「Claude 跑了測試、結果秀在對話裡」這種模型讀得到的形式。這是最常被誤會的點。

**Q：evaluator 的 token 很貴嗎？**
A：跑在你 provider 設的「小快模型」（預設 Haiku），相對主回合的花費通常可忽略。

**Q：它跟 auto mode 二選一嗎？**
A：不是，互補。auto mode 去掉 per-tool 的同意，`/goal` 去掉 per-turn 的 prompt。長任務無人值守是兩個一起開。

**Q：為什麼說它「就是個 Stop hook」？**
A：`/goal` 底層就是一個 session 範圍的 prompt-based Stop hook。差別是它是打指令臨時掛、`/clear` 就沒；真正寫進 `settings.json` 的 Stop hook 對每個 session 生效、還能跑腳本做確定性檢查。要自訂評估邏輯就自己寫 Stop hook（見 [`hook_walkthrough.md`](hook_walkthrough.md)）。

---

## 卡點對照表 ⭐（真的會踩，不是想像的）

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `/goal` 指令根本不存在 | Claude Code 版本太舊 | 升到 **≥ v2.1.139** |
| 打了 `/goal` 它說不能用 | 沒接受 trust 對話框 / `disableAllHooks` / `allowManagedHooksOnly` | 照它印的原因處理；信任這個 workspace |
| goal 跑了一整晚沒停、token 爆 | 條件 evaluator 判不了（寫了「正確」「設計良好」這種主觀詞） | 改成可量測 + 講明驗證方式；**永遠加 `or stop after N turns`** |
| 每輪都被工具同意打斷，跑很慢 | 沒開 auto mode | 搭 auto mode 一起開 |
| resume 回來輪數歸零、以為它重跑了 | 設計如此：續跑只留條件，計時/輪數/token 基準 reset | 正常行為，別誤判 |
| 設完又補一句 prompt，浪費一輪 | 不知道「設了就立刻開跑」 | 設定參數就是第一輪指令，別補話 |
| 達成了但我沒看到它停 | goal 達成會自動清、記一筆 achieved 在 transcript | `/goal`（無參數）查 achieved 紀錄 |
| `/clear` 之後 goal 不見了 | `/clear` 會順手清掉 active goal（設計如此） | 要保留就別 `/clear`，用 `/goal` 查狀態即可 |

---

## 講師私房筆記

### 教學節奏心法

- **開場別先講 `/goal`**：先叫學員用一般方式做一個三步任務，逼他手動打三次「繼續」，**讓他煩**。煩了再放 `/goal`，反差最大。
- Phase 2（寫條件）花最多時間，至少 15 分鐘。Phase 1/3 是操作，看一次就會；**Phase 2 是觀念，不講透學員回去一定踩**。
- 接在 [`hook_walkthrough.md`](hook_walkthrough.md) 的 Stop hook 那節之後講最順——一句「`/goal` 就是 Stop hook 的 session 版快捷」學員秒懂定位。

### 故意踩坑（比口頭講有效）

- **當場寫一條爛條件**：`/goal the code is clean and correct`。讓全班看它跑兩三輪每次 reason 都在掙扎、永遠不收斂。然後問：「那個評估模型怎麼知道『clean』？它看得到檔案嗎？」——**不行，它只讀對話**。再當場改成 `npm run lint exits 0 and npm test passes, or stop after 10 turns`，立刻收斂。這一段勝過講十分鐘理論。
- **故意不加剎車**讓它跑，跑兩輪就 `/goal clear` 喊停，順勢講「沒加 `or stop after N turns` 就是這樣，帳單會跑」。

### 不同學員角色推薦

| 角色 | 對哪段最有共鳴 | 給他的建議 |
|---|---|---|
| 跑大型重構的工程師 | 整合 demo（搬 API） | 條件寫「所有 call site 編譯過 + 測試綠」 |
| 照 design doc 實作的人 | Phase 2 | 把 acceptance criteria 逐條塞進條件 |
| 做 CI / 自動化的 | FAQ「就是個 Stop hook」 | 要跨 session、要跑腳本就寫真正的 Stop hook，不要用 `/goal` |
| 想無人值守過夜的 | Phase 0 + 整合 demo | `/goal` + auto mode + `or stop after N turns` 三件套缺一不可 |

### Kevin 親自驗證的真實狀況

- ✅ 「設了就立刻跑」是真的——別再習慣性補一句 prompt，那真的浪費一輪。
- ⚠️ 「evaluator 不讀檔只讀對話」這條最反直覺，學員 90% 第一次都會寫出判不了的條件。**這是這堂課唯一的必考題。**
- ⚠️ 沒加回合上限 + 條件寫爛 = 過夜燒 token 的經典組合。現場 demo 一定先示範剎車再放手。
- 💡 它跟本 repo `.claude/settings.json` 已掛的 `notify-done.sh`（Stop hook）是同一個事件家族——可以順帶呼應 [`hook_walkthrough.md`](hook_walkthrough.md) 的 Phase 3。

---

## 一句話總結

> **`/goal <可驗證的完成條件>` = 設一次終點線，Claude 每輪結束自己接下一輪，直到一個獨立小模型從對話裡確認達標才還你方向盤。關鍵只有一句：那個模型只讀對話、不讀檔不跑指令，所以條件必須是「Claude 講得出來的證據」能證明的——再加一句 `or stop after N turns` 當剎車。**

---

## 進階閱讀

- 🔗 [`hook_walkthrough.md`](hook_walkthrough.md) — Stop hook 原理；`/goal` 就是它的 session 版快捷，要自訂評估邏輯看這份
- 🔗 [Run a prompt repeatedly with `/loop`](https://code.claude.com/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop) — 按時間間隔重跑，跟 `/goal` 互為對照
- 🔗 [Auto mode](https://code.claude.com/docs/en/auto-mode-config) — 自動批工具，跟 `/goal` 搭著開才是真無人值守
- 🔗 [Prompt-based hooks](https://code.claude.com/docs/en/hooks-guide#prompt-based-hooks) — 自己寫 Stop hook
- 🔗 [Scheduling comparison](https://code.claude.com/docs/en/scheduled-tasks#compare-scheduling-options) — 要獨立於 session 的排程（夜跑測試、晨間 triage）看這
- 🔗 文件索引：`https://code.claude.com/docs/llms.txt` — 先抓這份找出所有可用頁面再深入

---

_Last updated: 2026-05-17_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材（同目錄）：hook_walkthrough.md、course_12hr_walkthrough.md、gitnexus_walkthrough.md_
_對應 PPT：Part 9 Hooks（延伸）＋ Part 16 進階主題（自主工作流）_
