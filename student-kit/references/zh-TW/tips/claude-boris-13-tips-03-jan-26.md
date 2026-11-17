# 我怎麼用 Claude Code —— Boris Cherny 的 13 個技巧

Claude Code 創造者 Boris Cherny（[@bcherny](https://x.com/bcherny)）於 2026 年 1 月 3 日分享的設定技巧摘要。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`tips/claude-boris-13-tips-03-jan-26.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tips/claude-boris-13-tips-03-jan-26.md)

---

## 背景

Boris 分享了他個人的 Claude Code 設定，並說它「意外地很原味」—— Claude Code 開箱即用就很好，所以他沒怎麼客製。使用方式沒有唯一正解：團隊刻意把它做成讓你隨意使用、客製與 hack 的樣子。Claude Code 團隊裡每個人的用法都非常不同。

<a href="https://x.com/bcherny/status/2007179832300581177"><img src="../tips/assets/boris-26-1-3/0.png" alt="Boris Cherny 開場推文" width="50%" /></a>

---

## 1/ 平行跑 5 個 Claude

在終端機中平行跑 5 個 Claude。把分頁編號 1–5，並用系統通知得知哪個 Claude 需要你輸入。

參見：[終端機設定文件](https://code.claude.com/docs/en/terminal)

<a href="https://x.com/bcherny/status/2007179833990885678"><img src="../tips/assets/boris-26-1-3/1.png" alt="平行跑 5 個 Claude" width="50%" /></a>

---

## 2/ 用 claude.ai/code 達到更高的平行度

在 claude.ai/code 上平行跑 5–10 個 Claude，與你本機的 Claude 並行。用 `claude.ai/code` 把本機 session 交接到網頁 session，在 Chrome 中手動啟動 session，並在兩邊之間 teleport。

<a href="https://x.com/bcherny/status/2007179836704600237"><img src="../tips/assets/boris-26-1-3/2.png" alt="claude.ai/code 平行度" width="50%" /></a>

---

## 3/ 所有事情都用帶思考的 Opus

所有事情都用帶 thinking 的 Opus 4.5。這是 Boris 用過最好的寫程式模型 —— 即使它比 Sonnet 更大更慢，但因為你不太需要引導它、而且它工具使用更好，最後幾乎總是比用小模型更快。

<a href="https://x.com/bcherny/status/2007179838864666847"><img src="../tips/assets/boris-26-1-3/3.png" alt="帶思考的 Opus" width="50%" /></a>

---

## 4/ 與團隊共用單一 CLAUDE.md

整個 repo 共用一份 `CLAUDE.md`。把它 commit 進 git，讓整個團隊每週貢獻好幾次。每當 Claude 做錯什麼，就把它加進 `CLAUDE.md`，讓 Claude 下次知道不要那樣做。

<a href="https://x.com/bcherny/status/2007179840848597422"><img src="../tips/assets/boris-26-1-3/4.png" alt="共用的 CLAUDE.md" width="50%" /></a>

---

## 5/ 在 PR 上標記 @claude 以更新 CLAUDE.md

在 code review 時，在同事的 PR 上標記 `@claude`，把某件事當成該 PR 的一部分加進 `CLAUDE.md`。用 Claude Code GitHub action（[install-@hub-action](https://github.com/apps/claude)）做這件事 —— 這是 Boris 版本的 Compounding Engineering（複利工程）。

<a href="https://x.com/bcherny/status/2007179842928947333"><img src="../tips/assets/boris-26-1-3/5.png" alt="在 PR 上標記 @claude" width="50%" /></a>

---

## 6/ 大多數 session 都從 Plan 模式開始

大多數 session 都從 Plan 模式開始（shift+tab 兩次）。如果目標是寫一個 Pull Request，就用 Plan 模式跟 Claude 來回討論，直到你滿意它的計畫。從那裡切到 auto-accept edits 模式，Claude 通常能一次搞定。一個好的計畫真的很重要。

<a href="https://x.com/bcherny/status/2007179845336527000"><img src="../tips/assets/boris-26-1-3/6.png" alt="Plan 模式" width="50%" /></a>

---

## 7/ 用 slash command 處理內迴圈工作流

為每個你一天會做很多次的「內迴圈」工作流建立 slash command。這省下重複打 prompt 的功夫，也讓 Claude 自己也能使用這些工作流。命令會 commit 進 git，放在 `.claude/commands/`。

範例：`/commit-push-pr` —— commit、push 並開一個 PR。

<a href="https://x.com/bcherny/status/2007179847949500714"><img src="../tips/assets/boris-26-1-3/7.png" alt="Slash command" width="50%" /></a>

---

## 8/ 用子代理自動化常見工作流

固定使用幾個子代理：`code-simplifier` 在 Claude 做完後簡化程式碼，`verify-app` 有端到端測試 Claude Code 的詳細指令，諸如此類。把子代理想成「自動化最常見的工作流」—— 跟 slash command 類似。

子代理放在 `.claude/agents/`。

<a href="https://x.com/bcherny/status/2007179850139000872"><img src="../tips/assets/boris-26-1-3/8.png" alt="子代理" width="50%" /></a>

---

## 9/ 用 PostToolUse hook 自動格式化程式碼

用 `PostToolUse` hook 格式化 Claude 的程式碼。Claude 開箱產生的程式碼通常格式就不錯，這個 hook 處理最後 10%，避免之後在 CI 出現格式錯誤。

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [
      {
        "type": "command",
        "command": "bun run format || true"
      }
    ]
  }
]
```

<a href="https://x.com/bcherny/status/2007179852047335529"><img src="../tips/assets/boris-26-1-3/9.png" alt="用 PostToolUse hook 做格式化" width="50%" /></a>

---

## 10/ 預先允許權限，而不是用 --dangerously-skip-permissions

不要用 `--dangerously-skip-permissions`。改用 `/permissions` 預先允許那些你確定在自己環境中安全的常見 bash 命令，以避免不必要的權限提示。這些大多會 commit 進 `.claude/settings.json` 並與團隊共享。

<a href="https://x.com/bcherny/status/2007179854077407667"><img src="../tips/assets/boris-26-1-3/10.png" alt="預先允許權限" width="50%" /></a>

---

## 11/ 透過 MCP 讓 Claude 使用你所有的工具

Claude Code 會使用你所有的工具。它常常搜尋並發文到 Slack（透過 MCP server）、跑 BigQuery 查詢回答分析問題（用 `bq` CLI）、從 Sentry 抓錯誤日誌等等。Slack MCP 設定會 commit 進 `.mcp.json` 並與團隊共享。

<a href="https://x.com/bcherny/status/2007179856266789204"><img src="../tips/assets/boris-26-1-3/11.png" alt="MCP 工具" width="50%" /></a>

---

## 12/ 用背景代理驗證長時間任務

對於非常長時間的任務，可以 (a) 在 prompt 中要 Claude 完成後用背景代理驗證自己的工作、(b) 用代理的 Stop hook 更確定地做這件事，或 (c) 使用 ralph-wiggum 外掛（最初由 @GeoffreyHuntley 發想）。

<a href="https://x.com/bcherny/status/2007179858435281082"><img src="../tips/assets/boris-26-1-3/12.png" alt="長時間任務的驗證" width="50%" /></a>

---

## 13/ 給 Claude 一個驗證自己工作的方法

這大概是從 Claude Code 得到優異成果最重要的一件事 —— 給 Claude 一個驗證自己工作的方法。只要 Claude 有這個回饋迴圈，最終結果的品質會提升 2–3 倍。

Boris 每一筆落地的變更，Claude 都會測試。

<a href="https://x.com/bcherny/status/2007179861115511237"><img src="../tips/assets/boris-26-1-3/13.png" alt="給 Claude 驗證的方法" width="50%" /></a>

---

## 資料來源

- [Boris Cherny (@bcherny) on X — 2026 年 1 月 3 日](https://x.com/bcherny/status/2007179832300581177)
