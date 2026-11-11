# 為什麼 Harness 很重要

為什麼 Claude Code 的功能不是「換湯不換藥的 prompt」—— 以及為什麼 harness 才是真正把玩具輸出與生產級工程工作區分開來的東西。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`reports/why-harness-is-important.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/reports/why-harness-is-important.md)

---

## 摘要

有經驗的 Claude Code 使用者常有一種化約說法：*「skills、commands、subagents、hooks —— 它們最終都變成送給模型的 prompt，所以一個夠強的 prompt 就等價了。」*

在模型最終推論呼叫那一層，這技術上是對的。模型看到的永遠只有 token。

但在其他每一層 —— 也就是真正發生軟體工程的那一層 —— **這個化約就崩潰了。** harness 不是一個 prompt 遞送系統，而是一個 **prompt 建構系統、確定性執行系統，以及脈絡架構系統** —— 這些能力無法靠更好的措辭取代。

本報告說明這個化約哪裡對、哪裡失效，以及為什麼把「模型看到什麼」和「系統做了什麼」混為一談，會讓實務工作者錯過 Claude Code 真正帶來槓桿的那些功能。

---

## 聽起來很對的化約

對於**單次原子任務** —— 「幫我寫一個遞迴 Fibonacci 函式」—— harness 對輸出品質沒有任何貢獻。把同樣的 token 餵給同樣的模型，無論它是透過 skill、command 還是純 prompt 抵達的，你得到的輸出分布都一樣。

在這個狹窄的範圍內，化約是成立的：

> 輸出品質 ≈ prompt 品質

這正是 Claude Code 相較於普通聊天機器人幾乎沒有加值的範圍。這也是那個化約隱含假設的範圍 —— 而真正的工程工作恰恰不在這個範圍裡。

---

## 化約在哪裡失效

harness 有十項架構層級的能力，運作在 prompt 無法觸及的層次。

| # | 能力 | 它做什麼 | 為什麼 prompt 無法複製 |
|---|------------|--------------|-------------------------------|
| 1 | **脈絡隔離** | 子代理在獨立的脈絡視窗中執行 | 一個 prompt 只能填滿一個視窗。N 個平行子代理提供約 N 倍的有效脈絡。 |
| 2 | **harness 強制的工具限制** | `allowed-tools` / `disallowedTools` 在模型能使用工具之前就擋下 | prompt 指令只是勸告；模型可以忽略。deny 規則無法被忽略。 |
| 3 | **延遲載入的規則與記憶** | `paths:` frontmatter 與後代 `CLAUDE.md` 只在 Claude 碰到符合的路徑時載入 | prompt 是靜態的 —— 它無法依執行期讀取哪些檔案而有條件地載入。 |
| 4 | **Hooks：確定性的程式碼執行** | shell 命令在生命週期事件（PreToolUse、PostToolUse、Stop 等）執行，而且可以**阻擋**工具呼叫 | prompt 無法攔截自己的工具呼叫。即使模型「不想要」，hook 照樣執行。 |
| 5 | **模型路由** | `model: haiku` 或 `model: opus` 把呼叫導向不同的模型端點 | prompt 裡沒有任何 token 能改變由哪個模型回答。 |
| 6 | **平行性** | 多個子代理同時執行 | prompt 是循序的。harness 負責排程並收集平行行程的結果。 |
| 7 | **跨 session 持久性** | 記憶系統與設定階層跨對話保存 | prompt 在 session 結束時就死了。 |
| 8 | **模組化 system prompt** | CLI 依啟用的功能有條件地載入 110+ 個 system prompt 片段 | 使用者無法手寫或抽換 CLI 的內部 prompt 片段。 |
| 9 | **Skill 預載** | `skills:` 欄位把 skill 的完整內容注入子代理的起始脈絡 | 使用者無法預先塞滿另一個代理的脈絡 —— 只有 harness 的載入器可以。 |
| 10 | **權限分類** | `auto` 權限模式用背景分類器預先核准或阻擋工具呼叫 | prompt 無法為自己加上一層執行前的安全層。 |

每一列都是「措辭夠強」在範疇上無法替代的面向。

---

## 「Prompt」這個詞的兩種用法

這個化約靠的是一個語意偷換。*prompt* 這個詞被用來指兩件很不一樣的事：

| 意思 | 誰控制 | 大小 |
|---------|-----------------|------|
| (a) 使用者打進去的東西 | 使用者 | 約 6–60 tokens |
| (b) 模型在推論時看到的東西 | harness | 約 5,000–50,000+ tokens |

在聊天機器人裡，(a) 和 (b) 是同一件事。
在 Claude Code 裡，兩者天差地遠。

harness 的工作正是讓 (b) 遠比 (a) 豐富：

```
使用者打：「write a recursive flatten function」      ← (a) 約 6 tokens

模型在推論時實際看到的：                                ← (b) 約 15,000 tokens
  ├── CLAUDE.md（專案慣例）
  ├── 符合的 .claude/rules/*.md（透過 paths: frontmatter 載入）
  ├── 模組化 system prompt 片段
  ├── 工具定義
  ├── 環境脈絡（cwd、git status、平台）
  ├── 先前回合歷史
  ├── 模型透過 Read/Grep 工具讀到的檔案
  └── 使用者那 6 個 token 的請求
```

**輸出品質是 (b) 的函數，不是 (a) 的。** harness 建構 (b)。「單靠一個強 prompt」無法重現 (b)，因為其中大部分根本不是使用者寫的。

---

## 就算只看輸出品質，harness 也在做事

考慮同一個 prompt —— 「write a recursive flatten function」—— 在三種環境下：

| 環境 | 模型看到什麼 | 典型結果 |
|-------------|---------------------|----------------|
| 聊天機器人，無工具 | 那句話 | 教科書式遞迴，通用風格 |
| Claude Code，不讀檔 | 那句話 + CLAUDE.md | 符合宣告過的專案慣例 |
| Claude Code，agentic 迴圈 | 那句話 + CLAUDE.md + 讀相鄰檔案 + 跑測試 | 符合實際 codebase 模式、通過測試、處理既有程式碼有處理的邊界情況 |

同樣的模型。同樣的使用者 prompt。**三種不同的輸出品質。** 差別在 harness —— 具體來說，是它組裝出的有效脈絡，以及它啟用的迭代迴圈。

對於非瑣碎的任務，輸出品質是以下的函數：

```
輸出品質 = f(有效脈絡, 模型能力, 迭代迴圈)
```

使用者只控制了*有效脈絡*的一小片（他們打的 prompt）。harness 控制其餘的 —— 而迭代迴圈則完全由它掌握。

---

## 這個化約對在哪、錯在哪

| 主張 | 判定 |
|-------|---------|
| 「推論時模型只看到 token。」 | ✅ 正確 |
| 「skills、commands 與子代理 prompt 都只是對某個脈絡貢獻 token。」 | ✅ 正確 |
| 「對真空中的原子任務而言，prompt 品質主導輸出品質。」 | ✅ 正確 |
| 「所以一個強 prompt 等同於使用那些功能。」 | ❌ 錯誤 |
| 「所以 harness 對輸出品質不重要。」 | ❌ 在真實工程任務上錯誤 |

前三句是準確的觀察。跳到第四句才是推理失敗之處：它把模型跟包覆它的系統混為一談，也把原子任務跟真實工程工作混為一談。

---

## 正確的心智模型

> **Prompt 控制模型被要求做什麼。**
> **harness 控制系統在模型搆不到的層次做了什麼** —— 在 token 抵達之前、在 token 產生之後、跨 session、跨脈絡、跨行程。

功能不是「多繞幾步的 prompt」。它們是 **harness 層級的原語** —— 確定性執行、脈絡架構與基礎設施路由 —— 運作在模型沒有發言權的層次。

一個有用的類比：

| 層次 | 聊天機器人 | Claude Code |
|-------|---------|-------------|
| 食譜 | 使用者的訊息 | 使用者的訊息 + harness 組裝的脈絡 |
| 廚房 | 沒有 —— 只有一個學生 | 工具、hooks、記憶、平行工作者、生命週期事件 |

你可以寫出世界上最好的食譜。沒有廚房，你無法規模化地做菜。

---

## 給實務工作者的重點

1. **對原子問題而言，prompt 品質幾乎就是一切。** harness 不相關。如果你只需要這個，用聊天機器人就好。
2. **對真實的 codebase 工作而言，harness 在默默扛重活。** 推論時的有效 prompt 大部分是 harness 建構的，不是使用者打的。
3. **把功能用在 prompt 範疇上做不到的事：** 確定性（hooks）、隔離（子代理）、延遲載入（帶 `paths:` 的規則）、持久性（記憶）、路由（各代理的 `model:`），以及平行性。
4. **強 prompt 是必要條件，但不充分。** 功能給你 prompt 無法提供的確定性、隔離與組合能力。兩者互補，不是互相取代。

---

## 資料來源

- [Agents vs Commands vs Skills](claude-agent-command-skill.md) —— 展示各功能在脈絡隔離、模型覆寫與工具限制上的差異
- [Claude Agent SDK 與 CLI System Prompts](claude-agent-sdk-vs-cli-system-prompts.md) —— 記錄了 110+ 個模組化 system prompt 片段
- [Claude Agent Memory](claude-agent-memory.md) —— 透過 `memory:` 範圍達成跨 session 持久性
- [Claude Memory 最佳實踐](../best-practice/claude-memory.md) —— 延遲載入的後代 `CLAUDE.md`
- [Claude 子代理最佳實踐](../best-practice/claude-subagents.md) —— harness 強制能力的 frontmatter 參考
- [Claude 設定最佳實踐（英文原檔）](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-settings.md) —— 權限規則評估與 `auto` 模式分類器
- [Orchestration Workflow](https://github.com/kevin801221/claude-code-best-practice/blob/main/orchestration-workflow/orchestration-workflow.md) —— 具體展示這個化約為何失效
