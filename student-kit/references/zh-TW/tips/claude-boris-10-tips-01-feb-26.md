# 使用 Claude Code 的 10 個技巧 —— 來自 Claude Code 團隊

Claude Code 創造者 Boris Cherny（[@bcherny](https://x.com/bcherny)）於 2026 年 2 月 1 日分享的團隊技巧摘要。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`tips/claude-boris-10-tips-01-feb-26.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tips/claude-boris-10-tips-01-feb-26.md)

---

## 背景

Boris 分享了直接來自 Claude Code 團隊的使用技巧。團隊的用法跟 Boris 個人的用法不同。記住：使用 Claude Code 沒有唯一正解 —— 每個人的設定都不一樣。你應該多實驗，找出適合自己的方式！

<a href="https://x.com/bcherny/status/2017742741636321619"><img src="../tips/assets/boris-26-2-1/0.png" alt="Boris Cherny 開場推文" width="50%" /></a>

---

## 1/ 更多事情平行做

一次開 3–5 個 git worktree，每個跑自己的 Claude session 平行進行。這是最大的單一生產力解鎖，也是團隊票選第一的技巧。Boris 個人用多個 git checkout，但 Claude Code 團隊多數人偏好 worktree —— 這正是 `@amorisscode` 把原生 worktree 支援做進 Claude 桌面 App 的原因！

有些人還會為 worktree 命名並設定 shell 別名（`2a`、`2b`、`2c`），這樣一次按鍵就能跳換。也有人專門留一個「分析」worktree，只用來讀日誌與跑 BigQuery。

參見：[Worktrees 文件](https://code.claude.com/docs/en/common...)

<a href="https://x.com/bcherny/status/2017742743125299476"><img src="../tips/assets/boris-26-2-1/1.png" alt="更多事情平行做" width="50%" /></a>

---

## 2/ 每個複雜任務都從 Plan 模式開始

把你的精力灌注在計畫上，好讓 Claude 能一次搞定實作。

有人讓一個 Claude 寫計畫，再開第二個 Claude 以資深工程師的角度審查它。

另一個人說，只要事情開始走偏，他們就切回 plan 模式重新規劃。不要硬推。他們也會明確要 Claude 為「驗證步驟」進入 plan 模式，不只是為了開發。

<a href="https://x.com/bcherny/status/2017742745365057733"><img src="../tips/assets/boris-26-2-1/2.png" alt="每個複雜任務都從 plan 模式開始" width="50%" /></a>

---

## 3/ 投資你的 CLAUDE.md

每次糾正之後，以這句話收尾：「更新你的 CLAUDE.md，這樣你就不會再犯同樣的錯。」Claude 寫規則給自己的能力好得有點詭異。

隨時間無情地編修你的 `CLAUDE.md`。持續迭代，直到 Claude 的出錯率明顯下降。

有位工程師要 Claude 為每個任務／專案維護一個筆記目錄，每個 PR 之後更新。然後他們在 `CLAUDE.md` 指向那個目錄。

<a href="https://x.com/bcherny/status/2017742747067945390"><img src="../tips/assets/boris-26-2-1/3.png" alt="投資你的 CLAUDE.md" width="50%" /></a>

---

## 4/ 建立自己的 Skills 並 commit 進 git

在每個專案間重複使用。來自團隊的技巧：

- 如果某件事你一天做超過一次，就把它變成 skill 或命令
- 建一個 `/techdebt` slash command，在每個 session 結束時執行，找出並消滅重複的程式碼
- 設定一個 slash command，把 7 天份的 Slack、GDrive、Asana 與 GitHub 同步成一份脈絡傾印
- 打造分析工程師風格的代理，讓它寫 dbt 模型、審查程式碼、在 dev 環境測試變更

參見：[Extend Claude with Skills — Claude Code Docs](https://code.claude.com/docs/en/skills)

<a href="https://x.com/bcherny/status/2017742748984742078"><img src="../tips/assets/boris-26-2-1/4.png" alt="建立自己的 skills" width="50%" /></a>

---

## 5/ 大多數 bug Claude 自己會修

團隊的做法是：

啟用 Slack MCP，把 Slack 上的 bug 討論串貼進 Claude，然後只說「fix」。完全不需切換脈絡。

或者，直接說「去修好失敗的 CI 測試」。不要微管理它怎麼做。

把 Claude 指向 docker 日誌來排查分散式系統問題 —— 它在這方面的能力好得出乎意料。

<a href="https://x.com/bcherny/status/2017742750473720121"><img src="../tips/assets/boris-26-2-1/5.png" alt="大多數 bug Claude 自己會修" width="50%" /></a>

---

## 6/ 升級你的 prompt 功力

a. **挑戰 Claude。** 說「把這些變更拿來質問我，在我通過你的測試前不要開 PR。」讓 Claude 當你的審查者。或者說「證明給我看這能動」，讓 Claude 比較 main 與你功能分支之間的行為差異。

b. **在一個平庸的修正之後**，說：「以你現在知道的全部，把這個丟掉，實作那個優雅的解法。」

c. **寫詳細的規格**，在交付工作前降低歧義。你越具體，輸出越好。

<a href="https://x.com/bcherny/status/2017742752566632544"><img src="../tips/assets/boris-26-2-1/6.png" alt="升級你的 prompt 功力" width="50%" /></a>

---

## 7/ 終端機與環境設定

團隊很愛 Ghostty！好幾個人喜歡它的同步繪製、24 位元色彩與正確的 unicode 支援。

為了更好地同時駕馭多個 Claude，用 `/statusline` 客製狀態列，讓它永遠顯示脈絡用量與當前 git 分支。許多人也會為終端機分頁上色與命名，有時搭配 tmux —— 一個分頁對一個任務／worktree。

使用語音聽寫。你說話比打字快 3 倍，而且 prompt 因此詳細得多。（macOS 上按 fn 兩下）

參見：[終端機設定文件](https://code.claude.com/docs/en/termin...)

<a href="https://x.com/bcherny/status/2017742753971769626"><img src="../tips/assets/boris-26-2-1/7.png" alt="終端機與環境設定" width="50%" /></a>

---

## 8/ 使用子代理

a. 在任何你希望 Claude 投入更多運算的請求後面加上「use subagents」。

b. 把個別任務卸載給子代理，讓主代理的脈絡視窗保持乾淨聚焦。

c. 透過 hook 把權限請求導向 Opus 4.5 —— 讓它掃描攻擊並自動核准安全的那些。參見：[Hooks 文件](https://code.claude.com/docs/en/hooks#...)

<a href="https://x.com/bcherny/status/2017742755737555434"><img src="../tips/assets/boris-26-2-1/8.png" alt="使用子代理" width="50%" /></a>

---

## 9/ 用 Claude 做資料與分析

請 Claude Code 用 "bq" CLI 即時拉取並分析指標。團隊有一個 BigQuery skill commit 在 codebase 裡，大家都直接在 Claude Code 裡用它做分析查詢。Boris 個人已經 6 個多月沒寫過一行 SQL。

任何有 CLI、MCP 或 API 的資料庫都適用。

<a href="https://x.com/bcherny/status/2017742757666902374"><img src="../tips/assets/boris-26-2-1/9.png" alt="用 Claude 做資料與分析" width="50%" /></a>

---

## 10/ 用 Claude 學習

幾個來自團隊、用 Claude Code 學習的技巧：

a. 在 `/config` 啟用 "Explanatory" 或 "Learning" 輸出風格，讓 Claude 解釋它所做變更背後的「為什麼」。

b. 讓 Claude 產生視覺化的 HTML 簡報來解釋你不熟的程式碼。它做出來的投影片好得出乎意料！

c. 請 Claude 為新協定與 codebase 畫 ASCII 圖，幫助你理解它們。

d. 打造一個間隔重複學習的 skill：你說明自己的理解，Claude 追問以補上缺口，並把結果存起來。

<a href="https://x.com/bcherny/status/2017742759218794768"><img src="../tips/assets/boris-26-2-1/10.png" alt="用 Claude 學習" width="50%" /></a>

---

## 資料來源

- [Boris Cherny (@bcherny) on X — 2026 年 2 月 1 日](https://x.com/bcherny/status/2017742741636321619)
