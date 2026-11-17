# Claude Code 的 15 個隱藏與未被善用的功能 —— 來自 Boris Cherny

Claude Code 創造者 Boris Cherny（[@bcherny](https://x.com/bcherny)）於 2026 年 3 月 30 日分享的技巧摘要。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`tips/claude-boris-15-tips-30-mar-26.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tips/claude-boris-15-tips-30-mar-26.md)

---

## 背景

Boris 分享了一批他最愛的 Claude Code 隱藏與未被善用功能，聚焦在他最常用的那些。

<a href="https://x.com/bcherny/status/2038454336355999749"><img src="../tips/assets/boris-26-3-30/0.png" alt="Boris Cherny 開場推文" width="50%" /></a>

---

## 1/ Claude Code 有行動 App

你知道 Claude Code 有行動 App 嗎？Boris 很多程式碼是從 iOS App 寫的 —— 這是不用開筆電就能做變更的便利方式。

- 下載 iOS／Android 版 Claude App
- 切到左側的 **Code** 分頁
- 你可以直接在手機上審查變更、核准 PR 並寫程式

<a href="https://x.com/bcherny/status/2038454337811386436"><img src="../tips/assets/boris-26-3-30/1.png" alt="Claude Code 行動 App" width="50%" /></a>

---

## 2/ 在行動／網頁／桌面與終端機之間搬動 session

執行 `claude --teleport` 或 `/teleport` 把雲端 session 接續到你的機器上。或執行 `/remote-control` 從手機／網頁控制本機執行中的 session。

- **Teleport**：把雲端 session 拉到你的本機終端機
- **Remote Control**：讓你從任何裝置控制本機 session
- Boris 在他的 `/config` 中設定了 **「Enable Remote Control for all sessions」**

<a href="https://x.com/bcherny/status/2038454339933548804"><img src="../tips/assets/boris-26-3-30/2.png" alt="Teleport 與 Remote Control" width="50%" /></a>

---

## 3/ /loop 與 /schedule —— 最強大的兩個功能

用它們排程 Claude 以固定間隔自動執行，一次最長可達一週。Boris 在本機跑著一堆 loop：

- `/loop 5m /babysit` —— 自動處理 code review、自動 rebase，把 PR 一路護送到 production
- `/loop 30m /slack-feedback` —— 每 30 分鐘自動為 Slack 回饋開 PR
- `/loop /post-merge-sweeper` —— 為他漏掉的 code review 留言開 PR
- `/loop 1h /pr-pruner` —— 關掉過期與不再需要的 PR
- ……還有很多！

試著把工作流變成 skill + loop。這很強大。

<a href="https://x.com/bcherny/status/2038454341884154269"><img src="../tips/assets/boris-26-3-30/3.png" alt="/loop 與 /schedule" width="50%" /></a>

---

## 4/ 用 Hooks 確定性地執行邏輯

用 hooks 把邏輯接進代理的生命週期。例如：

- 每次啟動 Claude 時**動態載入**脈絡（`SessionStart`）
- **記錄模型執行的每個 bash 命令**（`PreToolUse`）
- 把**權限提示導向 WhatsApp** 讓你核准／拒絕（`PermissionRequest`）
- 每當 Claude 停下來就**推它一把**讓它繼續（`Stop`）

<a href="https://x.com/bcherny/status/2038454343519932844"><img src="../tips/assets/boris-26-3-30/4.png" alt="使用 hooks" width="50%" /></a>

---

## 5/ Cowork Dispatch

Boris 每天都用 Dispatch 處理 Slack 與 email、管理檔案，以及在不在電腦前時操作他的筆電。他不寫程式的時候就在 dispatch。

- Dispatch 是 Claude 桌面 App 的**安全遠端控制**
- 在你許可下，它能使用你的 MCP、瀏覽器與電腦
- 把它想成「從任何地方把非寫程式的任務委派給 Claude」的方法

<a href="https://x.com/bcherny/status/2038454345419936040"><img src="../tips/assets/boris-26-3-30/5.png" alt="Cowork Dispatch" width="50%" /></a>

---

## 6/ 前端工作請用 Chrome 擴充套件

使用 Claude Code 最重要的技巧：**給 Claude 一個驗證輸出的方法。** 一旦做到，Claude 就會持續迭代直到結果很好。

- 把它想成：你請人做一個網站，但不准他用瀏覽器 —— 結果大概不會好看
- 給 Claude 一個瀏覽器，它就會寫程式並迭代到好看為止
- Boris 每次處理網頁程式碼都用 Chrome 擴充套件 —— 它通常比其他類似的 MCP 更可靠

<a href="https://x.com/bcherny/status/2038454347156398333"><img src="../tips/assets/boris-26-3-30/6.png" alt="前端用 Chrome 擴充套件" width="50%" /></a>

---

## 7/ 用 Claude 桌面 App 自動啟動與測試 web server

同樣的脈絡下，桌面 App 內建了讓 Claude **自動執行你的 web server、甚至在內建瀏覽器中測試它**的能力。

- 你也可以用 Chrome 擴充套件在 CLI 或 VSCode 中做類似設定
- 或者直接用桌面 App 享受整合體驗

<a href="https://x.com/bcherny/status/2038454348804714642"><img src="../tips/assets/boris-26-3-30/7.png" alt="桌面 App 的 web server 測試" width="50%" /></a>

---

## 8/ Fork 你的 session

常有人問怎麼 fork 既有的 session。兩種方式：

1. 在 session 中執行 `/branch`
2. 從 CLI 執行 `claude --resume <session-id> --fork-session`

`/branch` 會建立一個分支對話 —— 你現在就在那個分支裡。要回到原本的，用 `claude -r <original-session-id>`。

<a href="https://x.com/bcherny/status/2038454350214041740"><img src="../tips/assets/boris-26-3-30/8.png" alt="Fork 你的 session" width="50%" /></a>

---

## 9/ 用 /btw 問支線問題

Boris 一直在用這個，在代理工作時回答快速問題。`/btw` 讓你問個支線問題而不打斷代理當前的任務。

範例：
```
/btw how do I spell dachshund?
> dachshund — German for "badger dog" (dachs + badger, hund + dog).
↑/↓ to scroll · Space, Enter, or Escape to dismiss
```

<a href="https://x.com/bcherny/status/2038454351849787485"><img src="../tips/assets/boris-26-3-30/9.png" alt="用 /btw 問支線問題" width="50%" /></a>

---

## 10/ 使用 Git Worktrees

Claude Code 內建對 git worktree 的深度支援。要在同一個 repository 做大量平行工作，worktree 不可或缺。Boris **隨時有數十個 Claude 在跑**，就是靠這個。

- 用 `claude -w` 在 worktree 中開新 session
- 或在 Claude 桌面 App 勾選 **「worktree」核取方塊**
- 非 git 版控的使用者，可用 `WorktreeCreate` hook 加入你自己的 worktree 建立邏輯

<a href="https://x.com/bcherny/status/2038454353787519164"><img src="../tips/assets/boris-26-3-30/10.png" alt="Git worktrees" width="50%" /></a>

---

## 11/ 用 /batch 扇出大規模變更

`/batch` 會先訪談你，然後讓 Claude 把工作扇出給需要的任意數量**worktree 代理**（數十、數百、甚至數千個）來完成。

- 適用於大型程式碼遷移與其他可平行化的工作
- 每個 worktree 代理在自己的 codebase 副本上獨立工作

<a href="https://x.com/bcherny/status/2038454355469484142"><img src="../tips/assets/boris-26-3-30/11.png" alt="用 /batch 處理大規模變更" width="50%" /></a>

---

## 12/ 用 --bare 把 SDK 啟動加速最多 10 倍

預設情況下，當你執行 `claude -p`（或 TypeScript／Python SDK）時，Claude 會搜尋本機的 CLAUDE.md、設定與 MCP。但對非互動用途而言，多數時候你會想透過 `--system-prompt`、`--mcp-config`、`--settings` 等明確指定要載入什麼。

- 這是 SDK 最初建構時的設計疏失
- 未來版本會把預設翻轉為 `--bare`
- 目前請用這個旗標主動啟用，可獲得**最多 10 倍的啟動加速**

```bash
claude -p "summarize this codebase" \
    --output-format=stream-json \
    --verbose \
    --bare
```

<a href="https://x.com/bcherny/status/2038454357088457168"><img src="../tips/assets/boris-26-3-30/12.png" alt="--bare 旗標加速 SDK 啟動" width="50%" /></a>

---

## 13/ 用 --add-dir 讓 Claude 存取更多資料夾

跨多個 repository 工作時，Boris 通常在其中一個 repo 啟動 Claude，再用 `--add-dir`（或 `/add-dir`）讓 Claude 看到另一個 repo。

- 這不只是告訴 Claude 有這個 repo，同時也**給它在該 repo 工作的權限**
- 或者在團隊的 `settings.json` 加上 `"additionalDirectories"`，讓 Claude Code 啟動時永遠載入額外資料夾

<a href="https://x.com/bcherny/status/2038454359047156203"><img src="../tips/assets/boris-26-3-30/13.png" alt="--add-dir 用於多個 repo" width="50%" /></a>

---

## 14/ 用 --agent 給 Claude Code 自訂的 System Prompt 與工具

自訂代理是個強大但常被忽略的原語。要用它，只要在 `.claude/agents/` 定義一個新代理，然後執行：

```bash
claude --agent=<your agent's name>
```

- 代理可以有受限的工具、自訂描述與指定模型
- 很適合用來建立唯讀代理、專門的審查代理，或領域專屬工具

<a href="https://x.com/bcherny/status/2038454360418787764"><img src="../tips/assets/boris-26-3-30/14.png" alt="--agent 自訂 system prompt" width="50%" /></a>

---

## 15/ 用 /voice 啟用語音輸入

有趣的事實：Boris 大部分的程式是用「說」給 Claude 聽，而不是打字。

- 在 CLI 執行 `/voice`，然後按住空白鍵說話
- 在桌面版按語音按鈕
- 或在 iOS 設定中啟用聽寫

<a href="https://x.com/bcherny/status/2038454362226467112"><img src="../tips/assets/boris-26-3-30/15.png" alt="/voice 語音輸入" width="50%" /></a>

---

## 資料來源

- [Boris Cherny (@bcherny) on X — 2026 年 3 月 30 日](https://x.com/bcherny/status/2038454336355999749)
