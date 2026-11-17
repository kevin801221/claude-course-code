# Squash Merge 與 PR 大小分布 —— 來自 Boris Cherny 的技巧

Claude Code 創造者 Boris Cherny（[@bcherny](https://x.com/bcherny)）於 2026 年 3 月 25 日分享的洞察摘要。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`tips/claude-boris-2-tips-25-mar-26.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tips/claude-boris-2-tips-25-mar-26.md)

---

## 1/ 單日 266 次貢獻 —— 一律 squash

Boris 分享了他的 GitHub 貢獻圖，顯示 **3 月 24 日有 266 次貢獻** —— 來自 **141 個 PR，全部 squash**，每個 PR 的中位數是 **118 行**。

- Squash merge 把分支上所有 commit 合併成目標分支上的單一 commit —— 保持歷史乾淨且線性
- 每個 PR = 一個 commit，讓整個功能容易被 revert，也簡化了 `git bisect`
- 在高速的 AI 輔助工作流下（每天 141 個 PR），squash 是務實的選擇 —— 分支內那些「fix lint」、「try this」的個別 commit 都是雜訊

<a href="https://x.com/bcherny/status/2038552880018538749"><img src="../tips/assets/boris-26-3-25/1.png" alt="Boris Cherny —— 266 次貢獻，一律 squash" width="50%" /></a>

---

## 2/ PR 大小分布 —— 讓 PR 保持小

Boris 分享了那 141 個 PR 的大小分布，總計 **45,032 行變更**（新增 + 刪除）：

| 指標 | 行數（新增+刪除） | 意義 |
|--------|---------------:|---------|
| **p50** | **118** | PR 大小中位數 —— 一半的 PR 在 118 行以內 |
| p90 | 498 | 90% 的 PR 在 500 行以下 |
| **p99** | **2,978** | 只有約 1 個 PR 超過 3K 行 |
| 最小 | 2 | 最小的 PR —— 一個 2 行的快速修正 |
| 最大 | 10,459 | 最大的單一 PR —— 很可能是遷移或產生出來的程式碼 |

- **中位數 118 行**代表大多數 PR 聚焦且好審，即使每天 141 個 PR 也一樣
- 分布嚴重右偏 —— 偶爾出現的大 PR 無可避免（大量重新命名、遷移），但常態是很緊湊的
- 小 PR 降低合併衝突風險、較易審查，且與 squash merge 完美搭配，revert 時很乾淨

<a href="https://x.com/bcherny/status/2038552880018538749"><img src="../tips/assets/boris-26-3-25/2.png" alt="Boris Cherny —— PR 大小分布表" width="50%" /></a>

---

## 資料來源

- [Boris Cherny (@bcherny) on X — 2026 年 3 月 25 日](https://x.com/bcherny)
