# 三大 Plugin 安裝 + 實戰 Walkthrough

> **對象**:想實際把 superpowers / ralph-wiggum / pr-review-toolkit 裝起來、跑一遍真實案例的人
> **形式**:講師現場帶 / 自學照做
> **時長**:90 分鐘(安裝 20 + 三個案例各 ~20)
> **產出**:三個 plugin 都裝好、各跑通一個真實案例,並拿到「案例怎麼成案」的逐步 prompt
> **核心方法**:先把 plugin 系統的三個指令講成肌肉記憶,再一支一支裝、一支一支跑
>
> 指令與 marketplace 來源都對著官方 repo 的 `marketplace.json` / command 原始碼查證過(2026-05-22)。

---

## 開場:plugin 系統只有三個指令(先建肌肉記憶)

學生最常卡在「marketplace、plugin、install 到底誰是誰」。先講清楚這三個指令,後面全部都是它們的組合:

| 指令 | 做什麼 | 比喻 |
|---|---|---|
| `/plugin marketplace add <owner/repo>` | 把一個「商店」加進來 | 在手機上**新增一個 App Store** |
| `/plugin install <plugin>@<marketplace>` | 從某商店裝某個 plugin | 在那個 store **裝某個 App** |
| `/plugin` | 開 TUI,瀏覽 / Discover / 管理 | 打開**商店逛街**、管理已裝 App |

> **教學金句**:「marketplace 是商店、plugin 是商品、install 是結帳。`@` 後面那串就是『去哪間店買』。」

⚠️ **安全提醒**(照官方目錄 README 講):裝任何 plugin 前先確認你信任它。Anthropic 不控制第三方 plugin 內含的 MCP server / 檔案,也不保證它不會變。官方兩支(ralph-wiggum、pr-review-toolkit)是 Anthropic 自己維護的,相對安全。

---

## Part A:加 marketplace(商店)

這三支會用到三個 marketplace。**只需要 add 一次**,之後裝什麼都從這幾間店挑。

| Marketplace 名稱 | add 指令 | 裡面有 |
|---|---|---|
| `claude-plugins-official` | `/plugin marketplace add anthropics/claude-plugins-official` | 官方精選目錄(superpowers、pr-review-toolkit…上千個) |
| `claude-code-plugins` | `/plugin marketplace add anthropics/claude-code` | Claude Code 內建官方 plugin(ralph-wiggum、pr-review-toolkit、feature-dev…) |
| `superpowers-marketplace` | `/plugin marketplace add obra/superpowers-marketplace` | superpowers 作者自家商店(superpowers + 周邊) |

> 三個案例其實**最少只要 add 兩間**:`claude-plugins-official`(裝 superpowers + pr-review-toolkit)+ `claude-code-plugins`(裝 ralph-wiggum)。superpowers 自家商店是備援。

加完用 `/plugin` 開 TUI,進 **Discover** 就能看到這些店裡的 plugin 列表。

---

## Part B:裝 plugin(結帳)

裝好直接記這三行就夠:

```bash
# 1) superpowers —— 從官方精選目錄裝(最穩)
/plugin install superpowers@claude-plugins-official
#   備援:/plugin install superpowers@superpowers-marketplace

# 2) ralph-wiggum —— 只在 claude-code-plugins 這間店(官方精選目錄沒有它)
/plugin install ralph-wiggum@claude-code-plugins

# 3) pr-review-toolkit —— 兩間店都有,挑一個
/plugin install pr-review-toolkit@claude-plugins-official
#   或:/plugin install pr-review-toolkit@claude-code-plugins
```

裝完通常要**重啟 / reload** session 讓 command 與 agent 生效。

### 怎麼確認裝好了
- `/plugin` → 看 **Installed / Manage** 清單有沒有它們
- `/help` 或輸入 `/` → 看 slash command 有沒有冒出來(例 `/ralph-loop`、`/pr-review-toolkit:review-pr`)
- `/agents` → 看 pr-review-toolkit 的 6 個 agent 有沒有在列表裡

> 團隊共用:也能在專案 `.claude/settings.json` 設定要啟用的 marketplace / plugin,commit 進 git 全隊一致。語法見官方文件 https://code.claude.com/docs/en/plugins 。

---

## Part C 案例一:superpowers —— 一句話開場,它帶你走完整套開發

**裝的是 Skills**,所以**沒有指令要記** —— skill 會自動觸發。你只要開始講「我要做什麼」,它就接管。

### 案例:做一個「長網址轉短網址」的小 API

**案例怎麼成案(逐步 prompt 與會發生的事):**

1. **你開場(觸發 brainstorming skill)**
   ```text
   我想做一個把長網址縮短的小服務(REST API)。
   ```
   → superpowers 的 `brainstorming` skill 自動啟動,而且有 **HARD-GATE:設計沒被你核准前,它一行 code 都不准寫**。它會先看專案脈絡、**一次問你一個**澄清問題(要不要自訂短碼?要不要統計點擊?存哪?),再提 2-3 個方案 + 推薦,分段把設計給你看。

2. **你逐段核准設計**
   ```text
   方案 B 可以。設計我看過了,OK,進下一步。
   ```
   → 觸發 `writing-plans` skill,產出實作計畫,存到 `docs/superpowers/plans/YYYY-MM-DD-url-shortener.md`,內容是「假設工程師對你的 codebase 零認識」的 bite-sized 任務,強調 TDD / YAGNI / DRY / 頻繁 commit。

3. **你說 go(觸發執行)**
   ```text
   go,照計畫做,用 TDD。
   ```
   → 觸發 `subagent-driven-development`:**每個任務派一個全新的 subagent**(乾淨 context),做完先做「規格合規」審查、再做「程式品質」審查,然後接下一個任務,**中途不會一直問你「要繼續嗎」**。全程 `test-driven-development`:先寫測試、看它紅、再寫最小實作。

4.(可選)**顯式叫 skill**:正常不用,但你可以說「用 superpowers 的 brainstorming」或在 `/plugin` 看它掛了哪些 skill。

> **教學金句**:「superpowers 的 prompt 步驟不是『下指令』,是『被逼著先想清楚再動手』—— 它把資深工程師的紀律(先規格、後計畫、再 TDD 執行)變成自動觸發的 skill。」

**驗收**:`docs/superpowers/plans/` 出現計畫檔、測試先紅後綠、功能照計畫一個個長出來。

---

## Part C 案例二:ralph-wiggum —— 一個 Stop hook 讓它自己跑到完成

**裝的是 Hook + 兩個 command**。核心是 `/ralph-loop`:Stop hook 攔截退出、把同一個 prompt 餵回去,直到你設的完成字串出現或迭代上限到。

### 案例:讓它自動把一個 todo REST API 寫到測試全綠

**前置**:在一個有 `git` 的(最好是空的)專案資料夾裡開 `claude`。

**案例怎麼成案(就這一行 prompt):**
```text
/ralph-loop "用 TDD 做一個 todo REST API:需求是 CRUD、輸入驗證、測試覆蓋率 > 80%、附 README。每一輪:跑測試 → 看哪裡失敗 → 修 → 重跑。等全部需求達成且測試全綠,才輸出 <promise>COMPLETE</promise>。" --completion-promise "COMPLETE" --max-iterations 30
```

**接著會發生什麼:**
1. Claude 開始實作 → 跑測試 → 看到失敗
2. 它想結束 → **Stop hook 攔下,把上面那段 prompt 原封不動再餵一次**
3. 它看得到自己上一輪改的檔案 + git 歷史 → 針對失敗修正
4. 反覆,直到所有需求達成、測試全綠 → 輸出 `COMPLETE`
5. Stop hook 比對到 `COMPLETE` 字串(或到 30 次上限)→ 才放它真正結束

**中途想喊停:**
```text
/cancel-ralph
```

**兩個鐵則(來自 command 原始碼):**
- `--max-iterations` 是**保險絲**,一定要設,避免不可能的任務無限跑爆 API 成本。
- completion-promise **只能在任務真的 100% 完成時輸出** —— command 明文規定不准為了逃出迴圈而謊報完成。

> **教學金句**:「Ralph 的 prompt 設計三要素:**明確完成標準 + 可自動驗證(測試)+ 完成才喊 promise**。少一個,它就會繞圈或提早落跑。」

**什麼任務適合**:有明確完成標準、能被測試/linter 自動判對錯的(greenfield 最佳)。**不適合**:要人做設計判斷、一次性操作、標準模糊、線上 production debug。

---

## Part C 案例三:pr-review-toolkit —— 一隊 review agent 幫你過 PR

**裝的是 6 個 sub-agent + 一個調度 command**。兩種用法:自然語言觸發個別 agent,或 `/pr-review-toolkit:review-pr` 一鍵調度。

### 案例:開 PR 前,對改動做多角度審查

**前置**:在一個**有改動**的 repo(`git diff` 有東西,最好已在一條 feature branch)。

**用法一:自然語言,讓它自動派對的 agent(靠 description 路由)**
```text
幫我看這次改動的測試夠不夠、有沒有漏掉邊界情況。     → 觸發 pr-test-analyzer
檢查這次的錯誤處理,有沒有 catch 了卻吞掉的靜默失敗。  → 觸發 silent-failure-hunter
我新加的註解跟程式一致嗎?有沒有過時註解?           → 觸發 comment-analyzer
我新加的這個型別設計得好不好?                       → 觸發 type-design-analyzer
幫我做一般品質審查,看符不符合 CLAUDE.md。           → 觸發 code-reviewer
這段能用但很繞,幫我簡化(不要改功能)。             → 觸發 code-simplifier
```

**用法二:一鍵調度 command**
```text
/pr-review-toolkit:review-pr                 # 全跑(預設,依改動自動挑適用的 agent)
/pr-review-toolkit:review-pr tests errors    # 只看測試覆蓋 + 錯誤處理
/pr-review-toolkit:review-pr all parallel    # 全部 agent 平行跑(較快)
```

**它會回給你(結構化、可行動):**
- **Critical Issues**(merge 前必修)/ **Important**(該修)/ **Suggestions**(加分)/ **Strengths**(做得好的)
- 每條都帶 `file:line` 與「為什麼是問題 + 建議怎麼改」
- 注意:它**只給建議、不會自動改你的 code**,採不採納你決定

**建議工作流(來自 command 原始碼):**
```text
寫 code → /pr-review-toolkit:review-pr code errors → 修 critical → commit
開 PR 前 → /pr-review-toolkit:review-pr all → 修完 critical/important → 再跑一次驗證 → 開 PR
過了 review → /pr-review-toolkit:review-pr simplify(最後拋光)
```

> **教學金句**:「同一招『鏡頭隔離』,你自己在 stock/wafer 範例手刻過;pr-review-toolkit 是官方把它做成『裝上就有一整隊 + 自動路由』。路由準不準,全看 agent 的 description 寫得夠不夠精準。」

---

## 卡點對照表（安裝 / 使用最常卡的點）

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `/plugin install superpowers@claude-code-plugins` 找不到 | superpowers 不在那間店 | superpowers 用 `@claude-plugins-official` 或 `@superpowers-marketplace` |
| `/plugin install ralph-wiggum@claude-plugins-official` 找不到 | ralph-wiggum 只在 `claude-code-plugins` | 先 `add anthropics/claude-code`,再 `@claude-code-plugins` |
| 裝了但 `/ralph-loop` 沒出現 | 沒重啟 / reload | 重開 session;`/plugin` 確認 Installed |
| `/review-pr` 打不出來 | command 有 namespace | 正確是 `/pr-review-toolkit:review-pr` |
| superpowers 一直問問題不寫 code | 正常 —— brainstorming 的 HARD-GATE | 把設計逐段核准,它才會進實作 |
| Ralph 迴圈停不下來 | 沒設 max-iterations / 完成字串沒被輸出 | 一律帶 `--max-iterations`;prompt 明確要求輸出 promise |
| Ralph 一直繞同樣的錯 | 任務沒有自動驗證,它看不到自己錯 | 換成有測試/linter 能自動判對錯的任務 |
| review agent 沒被觸發 | 請求太籠統 | 講明面向(「測試覆蓋」)或用 `/pr-review-toolkit:review-pr` 點名 |

---

## 講師私房筆記

- **先把三個指令講死再開裝**:90% 的卡關都是 marketplace / plugin / `@` 三者搞混。Part A 那張「商店/商品/結帳」表先講透,後面超順。
- **裝的順序**:先裝 ralph-wiggum(最小、最快有成就感)→ 再 pr-review-toolkit(看一隊 agent)→ 最後 superpowers(最大、最改變行為)。
- **superpowers 要先打預防針**:它「問東問西不寫 code」是設計(HARD-GATE),不是壞掉。沒先講,學生會以為當機。
- **Ralph 一定現場設好保險絲再跑**:故意拿一個很小的任務、把 max-iterations 設小,讓學生看它跑幾輪就收,體感「迴圈是被 hook 控制的」。
- **pr-review-toolkit 對照自家範例教**:跟 `agent_group_projects/stock-groups-skills`、`wafer-detection` 一起講,「鏡頭隔離」這招就立體了 —— 你手刻 vs 官方產品化。
- **誠實邊界**:這三支都不會「自己把事情全做完還保證對」。Ralph 要能自動驗證、review 只給建議、superpowers 要你核准設計。把邊界講清楚,學生才不會神化它們。

---

## 一句話總結

> **plugin 系統就三個指令:`marketplace add`(開店)、`install …@店名`(結帳)、`/plugin`(逛街)。裝好之後 —— superpowers 用一句話開場就接管整套開發、ralph-wiggum 用一行 `/ralph-loop` 自己跑到測試全綠、pr-review-toolkit 用自然語言或 `/pr-review-toolkit:review-pr` 派出一隊 reviewer。**

---

## 進階閱讀

- 🔗 三支 plugin 的逐支拆解:[`ralph_wiggum_walkthrough.md`](ralph_wiggum_walkthrough.md) ・ [`pr_review_toolkit_walkthrough.md`](pr_review_toolkit_walkthrough.md) ・ [`superpowers_walkthrough.md`](superpowers_walkthrough.md)
- 🔗 用 superpowers 做到 production 的實例:[`superpowers_production_walkthrough.md`](superpowers_production_walkthrough.md)(成品 pomocat 見 [`project1-superpowers/`](project1-superpowers/README.md))
- 🔗 plugin 索引與出處/授權:[`README.md`](README.md)
- 🔗 官方 plugin 文件:https://code.claude.com/docs/en/plugins
- 🔗 官方精選目錄:https://github.com/anthropics/claude-plugins-official ・ Claude Code 內建 plugin:https://github.com/anthropics/claude-code/tree/main/plugins

---

_Last updated: 2026-05-22_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材(同目錄):README.md、superpowers_walkthrough.md、ralph_wiggum_walkthrough.md、pr_review_toolkit_walkthrough.md_
