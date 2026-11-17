# 排程任務實作

![Last Updated](https://img.shields.io/badge/Last_Updated-Mar_10%2C_2026-white?style=flat&labelColor=555)

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`implementation/claude-scheduled-tasks-implementation.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/implementation/claude-scheduled-tasks-implementation.md)

---

<a href="#loop-示範"><img src="../!/tags/implemented-hd.svg" alt="Implemented"></a>

`/loop` skill 用來以 cron 間隔排程重複任務。下面是 `/loop 1m "tell current time"` 的示範 —— 一個每分鐘觸發一次的簡單重複任務。

---

## Loop 示範

### 1. 排定任務

<p align="center">
  <img src="../implementation/assets/impl-loop-1.png" alt="/loop 1m tell current time —— 排程與 cron 設定" width="100%">
</p>

`/loop 1m "tell current time"` 會解析間隔（`1m` → 每 1 分鐘）、建立 cron job，並確認排程。重點：

- Cron 的最小粒度是 **1 分鐘** —— `1m` 對應到 `*/1 * * * *`
- 重複任務在 **3 天後自動過期**
- Job 是 **session 範圍的** —— 只存在記憶體中，Claude 結束時就停止
- 隨時可用 `cron cancel <job-id>` 取消

---

### 2. Loop 實際運作

<p align="center">
  <img src="../implementation/assets/impl-loop-2.png" alt="重複任務每分鐘觸發" width="100%">
</p>

任務每分鐘觸發一次，執行 `date` 並回報當前時間。每次迭代都會觸發非同步的 **UserPromptSubmit** 與 **Stop** hook —— 就是這個 repo 中用於音效通知的同一套 hook 系統。

---

## ![How to Use](../%21/tags/how-to-use.svg)

```bash
$ claude
> /loop 1m "tell current time"
> /loop 5m /simplify
> /loop 10m "check deploy status"
```

---

## ![How to Implement](../%21/tags/how-to-implement.svg)

`/loop` 是 Claude Code 的內建 skill —— 不需任何設定。它底層使用 cron 工具（`CronCreate`、`CronList`、`CronDelete`）來管理重複排程。
