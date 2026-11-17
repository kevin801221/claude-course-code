# 使用 Claude Code：Session 管理與 1M 脈絡 —— Thariq

Thariq（[@trq212](https://x.com/trq212)）於 2026 年 4 月 16 日分享的 Claude Code session、脈絡視窗與壓縮管理指南。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`tips/claude-thariq-tips-16-apr-26.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tips/claude-thariq-tips-16-apr-26.md)

---

## 背景

有了 1M token 脈絡視窗，Claude Code 能更可靠地處理更長的任務 —— 但如果你不刻意管理 session，它也為脈絡污染打開了大門。Session 管理比以往更重要：何時重新開始、何時壓縮、何時倒回、何時委派給子代理。

<img src="../tips/assets/thariq-26-4-16/1.png" alt="Thariq 開場推文" width="50%" />

<img src="../tips/assets/thariq-26-4-16/2.png" alt="Session 管理開場" width="50%" />

---

## 脈絡、壓縮與脈絡腐敗速覽

脈絡視窗是模型在產生下一個回應時能一次「看見」的所有東西。它包含你的 system prompt、目前為止的對話、每次工具呼叫與其輸出，以及每個讀過的檔案。Claude Code 的脈絡視窗是**一百萬個 token**。

可惜使用脈絡有一點代價 —— **脈絡腐敗（context rot）**。隨著脈絡增長，模型效能會下降，因為注意力被分散到更多 token 上，而較舊、不相關的內容開始干擾當前任務。對 1M 脈絡的模型而言，某種程度的脈絡腐敗大約在 **30-40 萬 token** 出現，但高度依賴任務內容 —— 這不是硬性規則。

脈絡視窗是硬性截斷。當你接近末端時，必須摘要任務並在新的脈絡視窗中繼續 —— 這就是**壓縮（compaction）**。你也可以自己觸發壓縮。

<img src="../tips/assets/thariq-26-4-16/3.png" alt="脈絡視窗圖解" width="50%" />

<img src="../tips/assets/thariq-26-4-16/4.png" alt="脈絡腐敗說明" width="50%" />

---

## 每個回合都是分歧點

Claude 完成一個回合後，你接下來能做的事出乎意料地多：

- **繼續（Continue）** —— 在同一個 session 中再送一則訊息
- **/rewind（esc esc）** —— 跳回先前某則訊息，從那裡重試
- **/clear** —— 開新 session，通常帶著你從剛才學到的東西所提煉出的簡報
- **壓縮（Compact）** —— 摘要目前為止的 session，在摘要之上繼續
- **子代理（Subagents）** —— 把下一塊工作委派給有乾淨脈絡的代理，只把它的結果拉回來

雖然最自然的是直接繼續，但另外四個選項的存在就是為了幫你管理脈絡。

<img src="../tips/assets/thariq-26-4-16/5.png" alt="壓縮與分歧圖解" width="50%" />

<img src="../tips/assets/thariq-26-4-16/6.png" alt="一個回合後的五個選項" width="50%" />

每個選項帶往前走的既有脈絡量不同：

| 全新 session | 壓縮 | 子代理 | 倒回 | 繼續 |
|:---:|:---:|:---:|:---:|:---:|
| 只有你的簡報 | 有損摘要 | 全部 + 結果 | 保留前段、切掉尾巴 | 全部留著 |
| *一點都不留* | | | | *全部都留* |

<img src="../tips/assets/thariq-26-4-16/7.png" alt="脈絡延續光譜" width="50%" />

---

## 何時該開新 session

新的 1M 脈絡視窗代表你現在能更可靠地做更長的任務 —— 例如從零打造一個全端 App。但「模型的脈絡還沒用完」不代表你就不該開新 session。

**一般原則：當你開始一個新任務時，也該開一個新 session。**

灰色地帶是當你要做相關任務、部分脈絡仍然必要但不是全部時。例如，為你剛實作的功能寫文件。雖然你可以開新 session，但 Claude 得重讀那些檔案，較慢也較貴。既然寫文件未必是高度仰賴智慧的任務，多餘的脈絡大概值得換取那個效率。

<img src="../tips/assets/thariq-26-4-16/8.png" alt="何時該開新 session" width="50%" />

---

## 用倒回取代糾正

如果 Thariq 只能挑一個代表良好脈絡管理的習慣，那就是**倒回（rewind）**。

在 Claude Code 中，連按兩下 Esc（或執行 `/rewind`）能讓你跳回任何先前的訊息並從那裡重新下 prompt。那一點之後的訊息會從脈絡中移除。

**糾正**（在嘗試 A 失敗後說「不對，試試 B」）會把失敗的嘗試留在脈絡裡：
> 脈絡 = 檔案讀取 + 2 次失敗嘗試 + 2 次糾正 + 最後的修正

**倒回**（回到失敗嘗試之前，帶著你學到的東西重新下 prompt）更乾淨：
> 脈絡 = 檔案讀取 + 一個充分知情的 prompt + 最後的修正

倒回通常是更好的做法。例如，Claude 讀了五個檔案、試了一個方向，但行不通。你的直覺可能是打「那個沒用，改試 X」。但更好的動作是倒回到剛讀完檔案那一刻，帶著你學到的東西重新下 prompt：「不要用方向 A，foo 模組沒有暴露那個 —— 直接用 B。」

你也可以用 **「summarize from here」** 讓 Claude 摘要它學到的東西並產生一則交接訊息，有點像是「未來的 Claude 寫給過去的自己」的紙條，告訴它試過什麼、結果不行。

<img src="../tips/assets/thariq-26-4-16/9.png" alt="糾正 vs 倒回圖解" width="50%" />

<img src="../tips/assets/thariq-26-4-16/10.png" alt="搭配 summarize from here 的倒回" width="50%" />

---

## 壓縮 vs. 全新 session

一旦 session 變長，你有兩種減重方式：`/compact` 或 `/clear`（重新開始）。它們感覺相似，但行為非常不同。

**壓縮**要求模型摘要目前為止的對話，然後用那份摘要取代歷史。它是有損的 —— 你信任 Claude 去決定什麼重要，但你不必自己動筆寫。Claude 在納入重要學習或檔案時可能更周全。你也可以傳入指示來引導它（`/compact focus on the auth refactor, drop the test debugging`）。

- **任務進行中**，保持動能 —— 細節可以模糊
- 便宜、繼續走

**全新 + 簡報**（`/clear`）代表*由你*寫下什麼重要（「我們在重構 auth middleware，限制是 X，重要的檔案是 A 和 B，我們已排除方向 Y」）然後乾淨開始。這比較費工，但得到的脈絡是*你*認定相關的東西。

- 下一步**事關重大** —— 在 100K 的探索中找到了一個事實
- 更費工、更精確

<img src="../tips/assets/thariq-26-4-16/11.png" alt="壓縮 vs 全新 session" width="50%" />

<img src="../tips/assets/thariq-26-4-16/12.png" alt="壓縮 vs 全新 圖解" width="50%" />

---

## 什麼會造成糟糕的壓縮？

如果你常跑長時間 session，可能注意過某些時候壓縮特別糟。糟糕的壓縮通常發生在模型無法預測你工作方向的時候。

例如，autocompact 在一段長時間除錯後觸發，摘要了整個調查過程。你的下一則訊息是「現在修掉我們在 bar.ts 看到的另一個警告」。但因為這個 session 聚焦在除錯上，那個「另一個警告」可能已經從摘要中被丟掉了。

這特別棘手，因為受脈絡腐敗影響，模型在壓縮當下正處於最不聰明的狀態。有了一百萬脈絡，你有更多時間主動 `/compact`，並附上你接下來想做什麼的說明。

<img src="../tips/assets/thariq-26-4-16/13.png" alt="糟糕壓縮圖解" width="50%" />

<img src="../tips/assets/thariq-26-4-16/14.png" alt="糟糕壓縮說明" width="50%" />

---

## 子代理與全新脈絡視窗

子代理是一種脈絡管理形式，適用於你事先就知道某塊工作會產生大量之後不再需要的中間輸出的情況。

當 Claude 透過 Agent 工具生成子代理時，那個子代理會拿到自己全新的脈絡視窗。它能做任何需要的工作，然後綜整結果，只把最終報告帶回給父代理。

心法測試：**我之後還會需要這些工具輸出，還是只需要結論？**

探索過程的雜訊會在子代理退出時被垃圾回收 —— 20 次檔案讀取、12 次 grep、3 條死路 —— 只有最終報告回到父脈絡。

雖然 Claude Code 會自動呼叫子代理，你可能會想明確要求它這麼做。例如：

- 「開一個子代理，依照下面這份 spec 檔驗證這份工作的結果」
- 「開一個子代理讀過另一個 codebase，摘要它怎麼實作 auth 流程，然後你自己用同樣方式實作」
- 「開一個子代理，根據我的 git 變更為這個功能寫文件」

<img src="../tips/assets/thariq-26-4-16/15.png" alt="子代理脈絡圖解" width="50%" />

<img src="../tips/assets/thariq-26-4-16/16.png" alt="子代理說明" width="50%" />

<img src="../tips/assets/thariq-26-4-16/17.png" alt="何時使用子代理" width="50%" />

---

## 總結

當 Claude 結束一個回合、你正要送出新訊息時，就是一個決策點。久而久之 Claude 會自己處理這件事，但目前這是你引導 Claude 輸出的方式之一。

| 情況 | 該用 | 為什麼 |
|-----------|-----------|-----|
| 同一個任務，脈絡仍然相關 | **繼續** | 視窗裡的一切都還在承重 —— 不要花錢重建它 |
| Claude 走錯方向 | **倒回**（連按兩下 Esc） | 保留有用的檔案讀取，丟掉失敗的嘗試，帶著學到的東西重新下 prompt |
| 任務進行中但 session 被過時的除錯／探索塞爆 | **/compact \<提示\>** | 省力；由 Claude 決定什麼重要。必要時用提示引導它 |
| 開始一個真正的新任務 | **/clear** | 零腐敗；你完全控制什麼被帶過去 |
| 下一步會產生大量輸出，但你只需要結論 | **子代理** | 中間的工具雜訊留在子代理的脈絡裡；只有結果回來 |

<img src="../tips/assets/thariq-26-4-16/18.png" alt="總結" width="50%" />

<img src="../tips/assets/thariq-26-4-16/19.png" alt="決策表" width="50%" />

---

## 資料來源

- [Thariq (@trq212) on X — 2026 年 4 月 16 日](https://x.com/trq212)
