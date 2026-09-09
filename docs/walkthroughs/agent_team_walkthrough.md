# Agent Team Walkthrough — set 好一個 4 人團隊，丟一個 Kanban 大案子讓它跑完

> **對象**：用過 sub-agent、想學會「怎麼把 agent team set 好並丟一個真案子給它」的工程師
> **形式**：講師現場帶 / 自學
> **時長**：60 分鐘（一小時內當堂跑完整套）
> **產出**：親手 set 一個 4 人 agent team，照 SPEC 從骨架蓋出一個能跑、測試全綠的 Kanban 看板，並當場看到 agent team 的三個好處
> **核心方法**：不講空泛理論。直接 set 一個 backend / frontend / test / docs 四人團隊，丟一個 Kanban 規格給它，當場看「並行、契約對齊、依賴解鎖」三件事發生

---

## 開場（5 分鐘）：為什麼要學 agent team？

你已經會 sub-agent 了。那 agent team 多了什麼？一張表看懂：

| 做法 | 隊友之間 | context | 適合 |
|---|---|---|---|
| 單一 session 序列做 | — | 一份，越做越擠 | 小任務 |
| Sub-agent | **不能直接對話**，只回報主對話 | 各自獨立 | 各做各的、互不相干的子任務 |
| **Agent team** | **共享任務列表 + 直接互相喊話** | 各自獨立 | 要互相對齊契約、有依賴的跨層工作 |

跨層蓋一個功能，前端得知道後端的契約長怎樣。sub-agent 做這件事，前端只能「猜」或「等主對話轉述」；agent team 裡前端**直接問後端**——這就是差別。

> **教學金句**：「sub-agent 是『各自交報告，互不通氣』；agent team 是『同一個專案的隊友，會互相喊話對齊』。需要隊友之間講話，才需要 team。」

---

## 📁 這趟要蓋的東西 + 團隊長相

起點是一個**骨架 + 一份完整規格**（不是空白），團隊照規格把它蓋完：

```
Projects/08-agent-team-review/
├── app/
│   ├── SPEC.md              ← 完整功能規格（丟給 team 的大案子）
│   ├── backend/server.py    ← 空殼：只有 GET /api/health
│   ├── frontend/index.html  ← 空白 + TODO
│   ├── frontend/app.js      ← 空殼 + TODO
│   ├── tests/test_health.py ← smoke test（證明骨架能跑）
│   └── docs/                ← 留給 docs-owner
└── .claude/agents/          ← 4 個 owner 定義（已放好）
        backend-owner / frontend-owner / test-owner / docs-owner
```

團隊與任務依賴：

```
backend-owner（定 cards CRUD 契約 + 實作）   ← 先跑，無依賴
        │
        ├──→ frontend-owner（三欄看板 UI + 串 API）  ┐
        ├──→ test-owner（釘契約 + edge cases）        ├─ 都只依賴 backend → 並行
        └──→ docs-owner（API 文件 + 使用說明）        ┘
```

> **教學金句**：「給骨架 + 明確 SPEC，不是給空白。團隊不用花時間猜你要什麼，一小時才跑得完。規格清楚，並行才有意義。」

---

## ⚙️ Phase 0：環境準備（5 分鐘）

```bash
cd Projects/08-agent-team-review

# 1. 版本（agent teams 需要 v2.1.32+）
claude --version

# 2. 骨架能跑嗎？（應該 1 passed）
uv run --with pytest pytest app/tests/ -v

# 3. 後端 health 活著嗎？
uv run python app/backend/server.py    # 另開終端：curl localhost:8000/api/health → {"status":"ok"}
```

實驗性 flag 已在本資料夾 `.claude/settings.json` 設好：

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

> **教學金句**：「先確認骨架自己會跑，再丟給團隊。骨架是壞的，你會分不清是團隊的問題還是起點的問題。」

---

## 🛠 Phase 1：把團隊 set 好 ⭐ 最關鍵（10 分鐘）

「set 好」的核心是兩件事：**每個 owner 只擁一層、任務有依賴順序**。這兩件事決定團隊會不會亂。

### 四個 owner，各擁一層

| owner | 擁有層 | 為什麼是它 |
|---|---|---|
| backend-owner | `app/backend/` | **契約的源頭** —— 它定 shape，其他人照著串 |
| frontend-owner | `app/frontend/` | 串 UI，依賴 backend 的契約 |
| test-owner | `app/tests/` | 釘契約，依賴 backend 的契約 |
| docs-owner | `app/docs/` | 寫文件，依賴 backend（契約）+ frontend（操作流程） |

定義已經在 `.claude/agents/`，每份都寫死「**只能改自己那層，跨層需求傳訊息**」。

> **教學金句**：「檔案所有權邊界是 agent team 不打架的關鍵。每個隊友只碰一層，兩個人就永遠不會改到同一個檔——零衝突是『設計出來的』，不是『運氣好』。」

### 為什麼是 4 個人，不是 1 個全包？

因為 backend 一完成，**frontend / test / docs 三個同時解鎖、並行做**。這就是你等下會親眼看到的並行價值。一個人全包只能一件一件來。

---

## 📋 Phase 2：丟案子，看依賴鎖住下游（10 分鐘）

在這個資料夾開 `claude`，貼這段（**可直接照跨**）：

```text
這個 app/ 是一個 Kanban 看板的骨架，完整需求寫在 app/SPEC.md。
開一個 agent team，四個隊友各擁一層：
- backend-owner（用 backend-owner agent 定義）擁 app/backend/
- frontend-owner（用 frontend-owner agent 定義）擁 app/frontend/
- test-owner（用 test-owner agent 定義）擁 app/tests/
- docs-owner（用 docs-owner agent 定義）擁 app/docs/

照 app/SPEC.md 把 Kanban 看板蓋完。任務依賴：backend 先定 cards CRUD 契約並實作
→ frontend / test / docs 三個都依賴 backend，backend 完成後並行進行。
隊友只能改自己那層，跨層需求用訊息對齊契約，不要越界改別人的層。
全部完成後 test-owner 跑 uv run --with pytest pytest app/tests/ -v 給我 pass/fail 摘要，然後清理團隊。
```

主管會：建 team → 生 4 個隊友 → 拆出有依賴的任務 → 隊友認領。

**這時去看共享任務列表**：backend 任務是 `in_progress`，frontend / test / docs 三個應該是 `blocked`——它們在等 backend 的契約。

> **教學金句**：「`blocked` 不是卡住，是團隊在自我協調。它知道現在做下游會白做，所以先按住——這是共享任務列表幫你做的事，不用你盯。」

---

## 🚀 Phase 3：看三個好處同時發生 ⭐⭐⭐（25 分鐘）

這是整堂課的價值。盯著三件事看：

### 好處 1：隊友直接對齊契約

backend 還在實作時，frontend-owner 會**直接傳訊息問** backend-owner：「POST /api/cards 的 body 跟 response 長怎樣？」backend 回精確 shape。

用 **Shift+Down** 在隊友間循環，你能看到這段對話。對照 sub-agent：sub-agent 之間沒有這條線，只能各自猜或回報主對話。

> **教學金句**：「frontend 不用猜、不用等你轉述——它直接問 backend。契約在兩個隊友之間一句話對齊，這是 sub-agent 做不到的。」

### 好處 2：依賴解鎖 → 並行起飛

backend 任務一標完成，frontend / test / docs **三個同時從 `blocked` 變 `in_progress`**。三個隊友同時動。

牆鐘時間在這裡被壓縮：一個人要「前端→測試→文件」跑三趟，團隊一趟並行做完。

> **教學金句**：「並行的價值不在『更聰明』，在『同一段牆鐘時間做了三件事』。backend 解鎖那一刻三個人一起動，就是你買 agent team 的理由。」

### 好處 3：各自獨立 context，主對話乾淨

每個 owner 自己一份 context，前端的一堆 CSS 嘗試不會擠進後端的 context，也不會塞爆你的主對話。主管那邊只看到「誰完成了什麼」。

> **教學金句**：「四個隊友四份 context，主對話只收結論。你不會因為前端 debug CSS 半小時，就把後端的 context 也一起污染掉。」

---

## ✅ Phase 4：驗收 + 清理（10 分鐘）

```bash
uv run --with pytest pytest app/tests/ -v   # 全綠，涵蓋 CRUD + edge cases
uv run python app/backend/server.py          # 瀏覽器開 app/frontend/index.html
                                             # 能新增卡片、用 ←/→ 移動、刪除
```

文件檢查：`app/docs/api.md`（每個 endpoint 契約）、`app/docs/usage.md`（怎麼跑）都在。

清理團隊（讓主管收掉，或手動清殘留 tmux）：

```bash
tmux ls                              # 看有沒有殘留
tmux kill-session -t <name>          # 有就清掉
```

> **教學金句**：「驗收看 pytest 全綠 + 瀏覽器真的能操作，不看主管嘴上說『做完了』。沒綠就退回去繼續。」

---

## 整合 demo：一條龍跑完

1. `Phase 0` 確認骨架能跑（1 passed、health 200）
2. 貼 `Phase 2` 的 prompt → team 建立、下游 `blocked`
3. backend 定契約並實作 → frontend 來問契約
4. backend 完成 → 三個隊友並行起飛
5. test-owner 回報 pytest 全綠
6. 瀏覽器操作看板：建卡 → `→` 移到 doing → `→` 移到 done → 刪除
7. 清理 team

一小時內整套跑完。

---

## 常見問題 / FAQ

**Q：agent team 跟 sub-agent 一句話差在哪？**
A：sub-agent 各自回報主對話、彼此不通氣；agent team 隊友直接互相喊話、共享任務列表自我協調。要「隊友之間對齊契約」才需要 team。

**Q：為什麼要給骨架 + SPEC，不直接叫團隊從零想？**
A：從零想需求變數太大，一小時跑不完。骨架 + 明確 SPEC 讓團隊不用猜，把力氣花在實作和對齊，不是花在猜你要什麼。

**Q：4 個 owner 會不會太多？**
A：剛好。backend 是源頭，另外三個並行下游——這個 1→3 的形狀正好讓你看到「依賴解鎖 → 並行起飛」。少一個就少一條並行線。

**Q：跨層開發是 agent team 最強用例嗎？**
A：不是最強，但**最好看到並行價值、最好驗收**（app 能跑、測試綠）。研究、並行審查那類也很適合，但結果是文件、較難當堂驗收。教學選這個是為了「看得到、跑得完」。

**Q：團隊把 app 蓋出來的程式碼，算我們維護的嗎？**
A：不算。這個專案維護的是「骨架 + SPEC + agent 定義 + 教材」。app 是你每次開 team 當場蓋出來的產物，重跑就重蓋。

---

## 卡點對照表 ⭐

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 沒生出隊友 | 版本太舊 / flag 沒開 | `claude --version` ≥ 2.1.32；確認 flag；in-process 模式按 Shift+Down 找隊友 |
| 主管自己動手沒委派 | prompt 沒夠強調委派 | 回：「等你的隊友完成任務再繼續，不要自己做」 |
| 兩個隊友改到同一檔互相覆蓋 | 檔案邊界沒收斂 | 重申硬規則：每個隊友只擁一層，跨層用訊息 |
| 下游一直 `blocked` 不解鎖 | 任務狀態滯後（實驗性已知限制） | 叫主管推 backend-owner 把任務標完成 |
| frontend 自己猜契約沒問 backend | prompt 沒下「對齊契約」 | 回：「frontend-owner 串 API 前先跟 backend-owner 確認 shape」 |
| 權限提示太多 | 沒預批准 | 生隊友前先在 settings 預批准常用操作（隊友權限會冒泡到主管） |
| 主管提前說做完了 | 沒驗收就回報 | 回：「先 pytest 全綠 + 瀏覽器能操作再說，沒綠就繼續」 |
| 結束殘留 tmux session | 清理沒乾淨 | `tmux ls` → `tmux kill-session -t <name>` |

---

## 講師私房筆記

- **Phase 3 是這堂課的命脈，前面都是鋪陳**。一定要當堂用 Shift+Down 切到隊友視角，讓學生親眼看到「frontend 問、backend 回」這段對話，以及 backend 完成那一刻三個任務同時解鎖。看到比講十遍有效。
- **時間分配**：Phase 0–2 控制在 25 分鐘內（環境 + set + 丟案子），把時間留給 Phase 3 看並行。backend 實作那段最久（10–15 分鐘），趁這段講「為什麼下游要 blocked」。
- **故意讓學生先看 `blocked`**：貼完 prompt 馬上去看任務列表，趁三個還是 blocked 時提問「為什麼它們不現在做？」——讓學生自己想出「等契約」，比直接講有效。
- **最容易失控的點**：主管自己動手把四層都做了（尤其小看板，主管覺得自己做更快）。一看到就打斷：「委派給隊友，你只負責協調和綜合。」這正是教學重點——你要的是看團隊協作，不是看主管單幹。
- **給不同角色**：
  - 工程師：重點 Phase 1 的檔案所有權邊界（這是團隊不打架的工程設計）
  - 帶人的：Phase 2 的任務依賴 = 真實專案排程，backend 是 blocker 就先排
  - 想省 token 的：prompt 加「每個隊友用 Sonnet」，主管用 Opus 協調
- **設計考量**：選 Kanban 而非更大的 app，是因為它在「夠大到並行有感」和「一小時跑得完」之間平衡得最好；用按鈕移動卡片而非拖拉，是為了不讓 frontend-owner 卡在 UI 細節吃掉並行時間。

---

## 一句話總結

> **Agent team = 共享任務列表 + 隊友直接喊話。把 4 個 owner 各綁一層、丟一份明確 SPEC，你就能當場看到它的三個好處：隊友直接對齊契約、依賴解鎖後並行起飛、各自獨立 context 不互相污染。**

---

## 進階閱讀

- 🔗 官方文件：協調 Claude Code 工作階段團隊（agent teams）—— 並行審查、競爭假設 debug 的 prompt 結構
- 🔗 sub-agent vs agent team 架構圖（官方 features-overview）
- 🔗 功能規格：`../../Projects/08-agent-team-review/app/SPEC.md`
- 🔗 專案實戰：`../../Projects/08-agent-team-review/README.md`

---

_Last updated: 2026-05-22_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材（同目錄）：hook_walkthrough.md, four_skills_walkthrough.md, anthropics_marketplace_skills_walkthrough.md, course_12hr_walkthrough.md_
_專案實戰案例：../../Projects/08-agent-team-review/README.md_
