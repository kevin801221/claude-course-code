# Code Review 與測試時運算 —— 來自 Boris Cherny 的技巧

Claude Code 創造者 Boris Cherny（[@bcherny](https://x.com/bcherny)）於 2026 年 3 月 10 日分享的洞察摘要。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`tips/claude-boris-2-tips-10-mar-26.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tips/claude-boris-2-tips-10-mar-26.md)

---

## 1/ 介紹 Code Review

Claude Code 新功能：**Code Review**。一組代理團隊會對每個 PR 做深度檢視。

- 先為 Anthropic 自己的團隊打造 —— 今年每位工程師的程式碼產出量成長 **200%**，而 code review 成了瓶頸
- Boris 已用了幾週，發現它抓到許多他原本不會注意到的真實 bug
- PR 一開啟，Claude 就派出一組代理團隊去獵 bug

<a href="https://x.com/bcherny/status/2031089411820228645"><img src="../tips/assets/boris-26-3-10/0.png" alt="Boris Cherny 宣布 Code Review" width="50%" /></a>

---

## 2/ 測試時運算與多重脈絡視窗

大致上，你丟給一個寫程式問題的 token 越多，結果就越好。Boris 稱之為**測試時運算（test time compute）**。

- 使用**獨立的脈絡視窗**能讓結果更好 —— 這就是子代理能運作的原因，也是為什麼一個代理會造出 bug，而另一個（用完全相同的模型）能找到它
- 這類似工程團隊：如果 Boris 造出一個 bug，他的同事在審查程式碼時可能比他自己更可靠地找出來
- 極限上，代理最終大概能寫出完美無 bug 的程式碼 —— 在那之前，**多個互不相關的脈絡視窗**往往是個好做法

<a href="https://x.com/bcherny/status/2031151689219321886"><img src="../tips/assets/boris-26-3-10/1.png" alt="Boris Cherny 談測試時運算" width="50%" /></a>

---

## 資料來源

- [Boris Cherny (@bcherny) on X — 2026 年 3 月 10 日](https://x.com/bcherny)
