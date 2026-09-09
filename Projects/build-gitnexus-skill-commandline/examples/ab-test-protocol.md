# A/B 測試：有 GitNexus vs. 沒 GitNexus 的 Claude Code

> **目的**：用**數字**證明 GitNexus 到底有沒有用，而不是靠「感覺起來比較聰明」。
> **適用**：上課現場 demo（最有衝擊力）、自己評估要不要長期用、寫部落格 / 內部報告佐證。

---

## 為什麼 A/B 測 LLM 工具很容易測錯？

先講三個**新手必踩的坑**，不避開的話你測出來的數字沒意義：

| 坑 | 為什麼錯 | 怎麼避開 |
|---|---|---|
| **只跑一次就下結論** | LLM 有隨機性，同一題跑兩次答案可能不同 | **每題每組各跑 3–5 次**，看平均 |
| **沒有標準答案** | 你不知道「正確答案」就無法判對錯 | **先人工建 ground truth**（見下） |
| **兩組 prompt 不一樣** | 變數沒控制，比的是 prompt 不是工具 | **逐字一模一樣的 prompt** |
| **context 污染** | 同一個 session 問第二題時已經被第一題影響 | **每題開新 session**（`/clear` 或重開 `claude`） |
| **只看『答得對不對』** | 漏掉成本面 | 同時記 **tool 呼叫次數、花的時間、token** |

> **教學金句**：「測 LLM 工具跟做藥物試驗一樣——**沒有對照組、沒有重複、沒有盲測，得到的數字都是安慰劑。**」

---

## Step 0：選一個「graph 才答得好」的 repo

不是每個 repo 都測得出差異。**小到一眼看完的 repo，有沒有 GitNexus 都一樣**。要挑：

- **中大型**：至少 50+ 檔案、跨多層目錄
- **有跨檔案/跨語言依賴**：例如前端呼叫後端 API、service 被多處 import
- **你（或助教）熟**：因為你要當「裁判」，必須知道正確答案

> 建議：用你公司一個真實的中型 repo，或拿這個 tutorial 的 `context-engineering-intro/`、`agent_group_projects/` 之類。

---

## Step 1：先建「標準答案」（ground truth）

A/B 測的靈魂。**沒有標準答案，後面全是空談。**

挑 **5 道有客觀正解的題目**，先用人工 + IDE 查出正確答案寫下來。推薦這 5 類（都是 graph 的強項）：

| # | 題型 | 範例題目 | 標準答案長怎樣 |
|---|---|---|---|
| Q1 | **找所有 caller** | 「`UserService` 這個 class 被哪些檔案 import / 使用？」 | 一份完整檔案清單（例：12 個檔案） |
| Q2 | **影響分析** | 「如果我改 `parsePayment()` 的簽名，哪些檔案＋哪些測試會壞？」 | 受影響檔案 + 測試清單 |
| Q3 | **死碼偵測** | 「`legacyExport()` 這個函式現在還有人用嗎？」 | Yes/No + 證據 |
| Q4 | **循環依賴** | 「專案裡有哪些 module 互相 import 形成循環？」 | 循環清單（或「無」） |
| Q5 | **跨層追蹤** | 「前端按下『送出訂單』，一路會呼叫到後端哪個 function？」 | 完整 call chain |

**建 ground truth 的方法**（人工這側）：
```bash
# Q1 用 IDE 的 "Find All References"，或：
grep -rn "UserService" --include="*.ts" . | grep -i import
# 但注意 grep 會漏掉 re-export、alias import —— 這正是要凸顯的點
# 所以 ground truth 要用 IDE LSP 或人工確認，別只信 grep
```

把 5 題的正確答案寫成一張表存好，**測試時遮住、最後才對答案**。

---

## Step 2：設定「對照組（A）」與「實驗組（B）」

### 實驗組 B：有 GitNexus（完整能力）

```bash
cd <你的 repo>
gitnexus analyze           # 先把 graph 建好
claude                     # 確認 .claude/mcp.json 有 gitnexus
/mcp                       # 應該看到 gitnexus server 在線
```

### 對照組 A：沒 GitNexus（只剩 grep / read）

**兩種做法，選一個**：

**做法 1（乾淨，推薦）**：暫時拔掉 MCP，開乾淨 session
```bash
# 暫時把 gitnexus 從 mcp.json 移掉（或備份整個 mcp.json）
mv .claude/mcp.json .claude/mcp.json.bak
claude
/mcp        # 應該看不到 gitnexus
# 測完記得 mv 回來
```

**做法 2（快速，但要靠自律）**：MCP 還在，但 prompt 明令禁用
> 在對照組每題前面加一句：「**只准用 grep / Read / Glob，禁止使用任何 gitnexus / mcp 工具。**」
>
> ⚠️ 缺點：Claude 偶爾會偷用，所以做法 1 比較嚴謹。**上課 demo 用做法 1**。

---

## Step 3：跑測試（嚴格照流程）

**鐵律**：
1. 每題開**新 session**（`claude` 重開，或 `/clear`）
2. 兩組用**逐字相同**的 prompt
3. 每題每組跑 **3 次**（時間夠就 5 次）
4. 每次都記錄四個數字（見計分表）

**範例 — Q1 的 prompt（A、B 兩組一字不差）**：
```
列出所有 import 或使用 UserService 這個 class 的檔案，給我完整清單（含路徑）。
最後用一行總結：總共幾個檔案。
```

每跑完一次，記下：
- **找對幾個**（對照 ground truth）→ 算 Recall
- **亂報幾個**（ground truth 沒有的）→ 算 Precision
- **花幾次 tool call**（看 Claude 的工具呼叫次數）
- **花多久 / 燒多少 token**

---

## Step 4：計分表（直接印出來填）

每題一張，A 組 B 組各跑 3 次：

```
題號：Q1（找所有 caller）
標準答案總數：12 個檔案

┌─────────┬──────┬──────────┬──────────┬───────────┬──────────┐
│  組別   │ 第幾 │ 找對(命中)│ 亂報(誤報)│ tool 次數 │ 花費秒數 │
├─────────┼──────┼──────────┼──────────┼───────────┼──────────┤
│ A 無GN  │  1   │   7/12   │    1     │    9      │   45s    │
│ A 無GN  │  2   │   8/12   │    0     │   11      │   52s    │
│ A 無GN  │  3   │   6/12   │    2     │    8      │   40s    │
├─────────┼──────┼──────────┼──────────┼───────────┼──────────┤
│ B 有GN  │  1   │  12/12   │    0     │    2      │   12s    │
│ B 有GN  │  2   │  12/12   │    0     │    2      │   11s    │
│ B 有GN  │  3   │  11/12   │    0     │    3      │   14s    │
└─────────┴──────┴──────────┴──────────┴───────────┴──────────┘

A 組平均 Recall = (7+8+6)/3 / 12 = 58%
B 組平均 Recall = (12+12+11)/3 / 12 = 97%
A 組平均 tool call = 9.3 次   B 組 = 2.3 次
A 組平均耗時 = 46s            B 組 = 12s
```

> 上面是**示意數字**，不是保證——但 graph 強項題（Q1/Q2/Q5）通常會看到這種量級的差距。

---

## Step 5：算四個關鍵指標

| 指標 | 公式 | 意義 | 哪組會贏 |
|---|---|---|---|
| **Recall（召回率）** | 找對的 / 標準答案總數 | 有沒有「漏掉」 | **B（graph 不漏）** |
| **Precision（精確率）** | 找對的 / 它總共報的 | 有沒有「亂講」 | B（grep 容易誤報同名） |
| **Efficiency（效率）** | tool call 次數、耗時 | 多快得到答案 | B（一次 query vs. 反覆 grep） |
| **Cost（成本）** | token 用量 | 燒多少錢 | 通常 B（少讀檔案省 context）|

**重點看 Recall。** 因為漏掉一個 caller = 重構時漏改一個檔案 = 線上炸掉。**這是 GitNexus 最值錢的地方。**

---

## 預期結果（講師心裡要有底）

| 題型 | 預期差距 | 原因 |
|---|---|---|
| Q1 找 caller | **B 大勝** | grep 抓不到 re-export / alias / 動態 import |
| Q2 影響分析 | **B 大勝** | 要跨 call chain，grep 根本做不到 |
| Q3 死碼 | **B 勝** | 要確認「全 repo 都沒人用」，grep 容易漏 |
| Q4 循環依賴 | **B 完勝** | grep 本質上做不到，B 一個 query 解決 |
| Q5 跨層追蹤 | **B 大勝** | 跨語言 call chain 是 graph 的主場 |
| （加碼）改單一檔案的小 bug | **平手** | 小範圍任務 grep 就夠，graph 沒優勢 |

> **誠實提醒**：別假裝 GitNexus 萬能。**小範圍、單檔案的任務它沒明顯優勢**——把這個也測出來、誠實呈現，你的 A/B 才有公信力。**「知道工具什麼時候沒用」跟「知道它什麼時候有用」一樣重要。**

---

## 上課 demo 的精簡版（時間不夠時）

3 小時課裡沒那麼多時間跑 5 題 × 2 組 × 3 次。**現場只 demo 1 題、各跑 1 次**就夠震撼：

1. 挑 **Q4 循環依賴** 或 **Q1 找 caller**（差距最明顯）
2. 左邊終端跑 A 組（無 GitNexus），右邊跑 B 組（有）
3. 同一題、同時敲下去，**讓學員看兩邊 tool call 數量爆炸性差異**
4. A 組 grep 來 grep 去 10 次還漏；B 組 2 次 query 就完整命中
5. 收尾金句👇

> **教學金句**：「**這不是模型變強，是模型『看得見』了。**同一個 Claude、同一題、同一秒——差別只在它手上有沒有那張 graph。」

---

## 進階：把它變成可重複的自動化評測（給想認真評估的人）

如果要長期追蹤（例如比較不同版本 GitNexus、或寫進團隊採購評估）：

1. 把 5 題寫成 `eval/tasks.jsonl`，每題含 `prompt` + `ground_truth`
2. 寫個 script 用 `claude -p "<prompt>"`（非互動模式）各跑 N 次
3. 自動 parse 輸出比對 ground truth，算 Recall / Precision
4. 輸出 CSV，畫成 bar chart

```bash
# 非互動模式跑單題（headless），方便寫迴圈
claude -p "列出所有 import UserService 的檔案，最後一行給總數" \
  --output-format json > result_B_run1.json
```

> 這部分可以再開一堂「**LLM 工具評測方法論**」的進階課，這裡先點到。

---

## 一頁總結

```
要證明 GitNexus 有用，不能靠感覺，要靠 A/B：
  1. 選中大型 repo（小 repo 測不出差異）
  2. 先建 5 題的標準答案（ground truth）—— 這是靈魂
  3. A 組拔掉 GitNexus、B 組有，prompt 逐字相同
  4. 每題每組跑 3 次、每次開新 session
  5. 比四個數字：Recall / Precision / tool次數 / 耗時
  6. 重點看 Recall —— 漏一個 caller = 重構炸一次

結論通常是：
  graph 強項題（找 caller / 影響分析 / 循環依賴）→ B 大勝
  小範圍單檔任務 → 平手（誠實講出來，A/B 才可信）
```
