# Agent Team — 看到「多個 Claude 互相證偽」的強大 Walkthrough

> **對象**：用過 sub-agent、但沒開過 agent team 的工程師
> **形式**：講師現場帶、學生跟著做
> **時長**：75 分鐘
> **產出**：一個會穩定復現的「多嫌疑 bug」sample + 一份「何時該開 team、怎麼下 prompt 讓隊友互相證偽」的可複用心法
> **核心方法**：用「同一個 bug，單一 agent 會錨定就停 vs agent team 互相證偽才收斂」的對打，讓你**親眼**看到差別，而不是聽我說它很強

---

## 為什麼要寫這份 walkthrough？

你已經會 sub-agent 了。最常見的誤解是：

> 「agent team 不就是一次開很多 sub-agent 嗎？」

**不是。** 差別就一句話：

| | Sub-agent | Agent team |
|---|---|---|
| Context | 各自獨立 | 各自獨立 |
| 溝通 | **只能回報給主對話** | **隊友彼此直接喊話** |
| 協調 | 主代理指揮全部 | 共享任務列表、自我協調 |
| 最適合 | 只有結論重要的專注任務 | **需要互相辯論、彼此推翻** 的複雜工作 |

> **教學金句**：「sub-agent 是『各自交報告』，agent team 是『開會吵架』。會吵架，才查得出單一 agent 會錯過的真兇。」

這份不教你跑跨層開發那個弱 demo（`08-agent-team-review/app/` 那個會卡在檔案邊界）。我們直接上 agent team **最強的場景**：**競爭假設 debug**。

---

## 🧠 30 秒釘穩心智模型（讀不下去全文，至少看這節）

### 單一 agent debug 的致命弱點：錨定

一個 agent 查 bug，會做這件事：

1. 看 code → 想到一個「看起來很合理」的原因
2. 講得頭頭是道 → **停手**
3. 你照著修 → 沒好，或「好像好了」其實沒解到本質

這叫**錨定（anchoring）**：找到第一個說得通的解釋就不找了。

### Agent team 怎麼破解錨定

開 5 個隊友，**每人認領一個假設**，然後下一個關鍵指令：

> 「互相試著推翻對方的理論，像科學辯論。」

辯論結構是關鍵機制：當每個隊友的工作不只是查自己的理論、**還要積極證偽別人的**，那個「被大家圍攻還活下來」的理論，才更可能是真兇。

> **教學金句**：「不要叫隊友『各查一個原因』，要叫他們『互相證偽』。前者是 5 份獨立報告，後者才是收斂。」

---

## 📁 這份會用到的東西

```
Projects/08-agent-team-review/
├── .claude/
│   ├── settings.json          ← CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1（已設好）
│   └── agents/                ← 三個 sub-agent 定義（這份用不到，給跨層 demo 用）
└── debug-sample/
    └── chat_server.py         ← ⭐ 本份主角：藏了一個多嫌疑 bug 的聊天 server
```

`chat_server.py` 的症狀：**連上、送第一則訊息、收到 echo —— 停頓一下再送第二則就被斷線。**

裡面**明寫了 4 個嫌疑點**（A/B/C/D 註解標好），真兇只有一個，另外三個是「看起來超可疑但其實沒問題」的誘餌。這就是為什麼它是 agent team 的完美教材。

---

## Phase 0：環境準備（5 分鐘）

```bash
# 1. agent teams 需要 v2.1.32+
claude --version

# 2. 進這個資料夾（settings.json 已幫你開好實驗性 flag）
cd Projects/08-agent-team-review

# 3. 親眼看症狀復現 —— 不要跳過這步
uv run python debug-sample/chat_server.py
```

你應該看到：

```
echo: hello 0
DISCONNECTED at round 1: server closed connection
```

> **教學金句**：「debug 第一件事永遠是『先讓 bug 在你面前穩定復現』。沒復現就開 team，是叫五個人去查一個不存在的鬼。」

⚠️ 如果你看到 `OK: 連線撐過三輪` —— 你的機器跑太快或 timeout 行為不同，把 `chat_server.py` 的 `USER_THINK_TIME` 調大到 5.0 再試。

---

## Phase 1：先看「單一 agent」會怎麼錯 ⭐（15 分鐘）

**先不要開 team。** 這步是對照組，沒有它，後面的「哇」會打折。

開 `claude`，貼：

```text
debug-sample/chat_server.py 有個 bug：使用者送第一則訊息收到 echo，
停頓一下送第二則就被斷線。幫我找出原因並修好。
```

觀察 Claude 會怎麼做（**90% 會這樣**）：

- 它讀 code、看到 `HEARTBEAT_TIMEOUT = 2.0`
- 講一個很合理的故事：「timeout 太短，使用者還沒打字就逾時了，把它調大」
- 改 `HEARTBEAT_TIMEOUT`，跑一下「看起來好了」

**這就是錨定。** 它找到嫌疑 A 就停了。問題是：

> 把 timeout 調大只是**讓症狀不容易出現**，沒解到本質——
> 真正的 bug 是 `except socket.timeout: break` 把「使用者還在打字」
> 誤判成「連線該關」。timeout 設多久都一樣，使用者只要想久一點就斷。

把這個「半對的答案」記下來。等等 agent team 會自己戳破它。

> **教學金句**：「最危險的不是錯答案，是『半對的答案』——它能跑、能解釋、還掩蓋症狀，讓你以為解決了。單一 agent 最容易停在這。」

---

## Phase 2：開 agent team，下「互相證偽」指令 ⭐⭐⭐（30 分鐘）

開**新的** `claude`（不要接續 Phase 1 的對話，要乾淨對照），貼這段——**逐字照貼，這個 prompt 是這份的精華**：

```text
debug-sample/chat_server.py 有個 bug：使用者連上、送第一則訊息收到
echo，停頓幾秒再送第二則就被伺服器斷線。

開一個 agent team，5 個隊友，每人認領一個假設去調查：
- 隊友 1：HEARTBEAT_TIMEOUT 太短造成的
- 隊友 2：RECV_BUFFER 只有 16 bytes，訊息被截斷造成的
- 隊友 3：except socket.timeout 的處理邏輯有問題
- 隊友 4：收到資料沒更新 last_seen，心跳邏輯失效
- 隊友 5：以上都不是，是 client/server 握手或 threading 的問題

關鍵：讓他們互相喊話，積極試著推翻彼此的理論，像科學辯論。
每個人都要拿「最小可驗證實驗」證明或反駁，不要只用嘴講。
最後在對話裡給我：哪個理論被推翻、為什麼，倖存的真兇是什麼，
以及最小修法。然後清理團隊。
```

**接下來盯著看這幾件事**（這才是這堂課的價值，不是看它修好）：

| 觀察點 | 怎麼看 | 為什麼重要 |
|---|---|---|
| 隊友互相喊話 | in-process 模式按 **Shift+Down** 在隊友間循環 | 看到「隊友 3 證偽隊友 1」這種訊息，就是 sub-agent 做不到的事 |
| 誘餌被戳破 | 看隊友 2/4 的結論 | 隊友 2 會發現 `hello 0` 才 7 bytes 根本沒到 16；隊友 4 會發現那段 code 在 `break` 後到不了（dead code） |
| 半對答案被推翻 | 看隊友 1 vs 隊友 3 的辯論 | 隊友 1 主張「調大 timeout」，隊友 3 會用實驗打臉：timeout 設多大，使用者想久一點還是斷 |
| 收斂到真兇 | 主管最後的綜合 | `except socket.timeout: break` 把「還在等訊息」當「斷線」——這是唯一改了就真的好的地方 |

> **教學金句**：「你不是在看它修 bug。你是在看『隊友 3 拿實驗把隊友 1 的合理故事打死』——這一刻就是 agent team 的全部價值。」

### 真兇與三個誘餌（講師對答案用，不要先給學生看）

| 嫌疑 | 是不是真兇 | 為什麼 |
|---|---|---|
| A `HEARTBEAT_TIMEOUT` 太短 | ❌ 半對誘餌（最毒） | 調大只是讓症狀變難復現，使用者想久一點照斷 |
| B `RECV_BUFFER=16` 截斷 | ❌ 純誘餌 | `hello 0` 只有 7 bytes，根本沒碰到邊界 |
| C `except socket.timeout: break` | ✅ **真兇** | 把「使用者還沒打字」誤判成「連線該關」，唯一改了就真的好 |
| D `last_seen` 沒更新 | ❌ dead code 誘餌 | 那段在 `break` 之後永遠到不了，改了也沒用 |

最小修法：`except socket.timeout` 不要 `break`，應該 `continue`（逾時只代表這輪沒訊息，不代表連線斷）。

---

## 整合 demo：一條龍對照（10 分鐘）

把 Phase 1 和 Phase 2 的結果並排講給學生看：

| | Phase 1 單一 agent | Phase 2 agent team |
|---|---|---|
| 找到的原因 | 嫌疑 A（timeout 太短） | 嫌疑 C（except 邏輯錯） |
| 對不對 | 半對：症狀掩蓋了，本質沒解 | 對：唯一改了就真的好 |
| 怎麼得到的 | 第一個合理解釋就停 | 4 個假設互相證偽後倖存 |
| token 成本 | 低 | 高（5 個獨立 context） |
| 什麼時候值得 | 簡單 bug、原因明顯 | **原因不明、有多個合理解釋** |

> **教學金句**：「agent team 不是『更強的 sub-agent』，是『花更多 token 買掉錨定風險』。bug 越曖昧、錯了代價越高，這筆 token 越值得花。」

---

## 常見問題 / FAQ

**Q：為什麼不直接用 08 那個跨層開發沙盒？**
A：跨層開發是 agent team **最弱**的展示——隊友卡在檔案邊界、序列依賴，並行優勢被吃掉。官方文件自己也說最強用例是研究/審查/競爭假設 debug。要「看到強大」就要用對場景。

**Q：一定要 5 個隊友嗎？**
A：3–5 個是甜蜜點。這個 bug 剛好 4 個嫌疑 + 1 個「都不是」的兜底，所以 5。假設少就少開，不要為了多而多。

**Q：隊友沒出現？**
A：`claude --version` 要 ≥ 2.1.32；確認在 `08-agent-team-review/` 裡（settings.json 才生效）；in-process 模式按 Shift+Down 找隊友。

**Q：主管自己動手沒委派？**
A：回它「等隊友完成再繼續，不要自己做」。

**Q：可以用在真實工作的 bug 嗎？**
A：可以，而且這才是重點。把 prompt 模板的「假設清單」換成你自己列的 3–5 個可能原因即可。心法不變：**每人一個假設 + 互相證偽 + 拿實驗不要用嘴**。

---

## 卡點對照表 ⭐

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 跑 sample 看到 `OK: 連線撐過三輪`，bug 沒復現 | 機器跑太快，停頓沒超過 timeout | 把 `USER_THINK_TIME` 調大到 5.0 |
| 開了 team 但隊友只各交報告、沒互相喊話 | prompt 沒下「互相證偽」指令 | 一定要有「積極試著推翻彼此、像科學辯論」這句，這是收斂的開關 |
| 隊友都同意「調大 timeout」就結案 | 連 team 也被半對答案帶跑了 | 追問：「timeout 設成 1 小時，使用者想 2 小時還會斷嗎？用實驗證明」 |
| 主管提前說「修好了」 | 它信了某隊友沒驗證 | 回：「跑 `uv run python debug-sample/chat_server.py`，要看到三輪 echo 才算」 |
| token 燒很快很心痛 | 5 個獨立 context 本來就貴 | 這是 agent team 的本質成本，prompt 加「每個隊友用 Sonnet」省一半 |
| 結束後殘留 tmux session | 清理沒乾淨 | `tmux ls` → `tmux kill-session -t <name>` |

---

## 講師私房筆記

- **節奏**：Phase 1（單一 agent 翻車）只給 15 分鐘，但**絕對不能跳**。學生要先親眼看到「它停在半對答案」，Phase 2 的「哇」才成立。我實測過：直接跳 Phase 2 的班，課後問卷「我覺得 sub-agent 也能做到」的比例高一倍。
- **故意踩坑**：讓學生 Phase 1 真的照著「調大 timeout」改，然後當場把 `USER_THINK_TIME` 調更大再跑——又斷了。這個打臉比你講十句「這是半對答案」都有效。
- **真兇藏在 C 不是 A 是刻意的**：A 是最「順手」的解釋，放最前面當錨。學生（和單一 agent）幾乎都會先抓 A。這個設計就是要示範錨定。
- **誘餌 D 是 dead code**：這個最有教育意義——它「看起來是個 bug」（少更新 last_seen），但在 `break` 之後根本到不了。會有隊友想修 D，看哪個隊友能指出「這段根本沒被執行」，那個隊友的 reasoning 最值得拿出來講。
- **給不同角色**：
  - 後端工程師：重點放「半對答案掩蓋本質」的危險，他們最有共鳴
  - PM / 帶人的：重點放「錨定 = 團隊 review 為什麼要找不同立場的人」，這是組織隱喻
  - 想省錢的：重點放整合 demo 那張 token 成本表，講清楚「什麼時候不該開 team」
- **Kevin 親自驗過**：這個 sample 在我的 Mac（Darwin 25.0）上穩定第 1 輪 OK、第 2 輪斷。`uv run python debug-sample/chat_server.py` 直接會復現，不需要手動連 socket。

---

## 一句話總結

> **agent team 的強大不在「更多 agent」，在「隊友會互相證偽」——它買掉的是單一 agent 最致命的錨定風險。下 prompt 時，『互相推翻對方』這句話，比『各查一個原因』值錢一百倍。**

---

## 進階閱讀

- 🔗 官方文件：協調 Claude Code 工作階段團隊（agent teams）
- 🔗 sub-agent vs agent team 架構圖（官方 features-overview）
- 🔗 同目錄 `hook_walkthrough.md` —— 想用 `TaskCompleted` hook 加品質閘門看這份
- 🔗 跨層開發弱 demo（對照用）：`../../Projects/08-agent-team-review/README.md`

---

_Last updated: 2026-05-15_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材（同目錄）：hook_walkthrough.md, four_skills_walkthrough.md, anthropics_marketplace_skills_walkthrough.md, course_12hr_walkthrough.md_
_專案實戰案例：../../Projects/08-agent-team-review/README.md_
