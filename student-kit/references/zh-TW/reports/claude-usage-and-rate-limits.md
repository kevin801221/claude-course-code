# Claude Code：用量、速率限制與額外用量

理解 Claude Code 的用量上限怎麼運作，以及碰到上限時如何繼續工作。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`reports/claude-usage-and-rate-limits.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/reports/claude-usage-and-rate-limits.md)

---

## 概觀

訂閱方案（Pro、Max 5x、Max 20x）的 Claude Code 有用量上限，以滾動視窗重設。三個內建 slash command 可以幫你監控與管理用量：

| 命令 | 說明 | 適用對象 |
|---------|-------------|--------------|
| `/usage` | 查看方案上限與速率限制狀態 | Pro、Max 5x、Max 20x |
| `/extra-usage` | 設定碰到上限時的隨用隨付溢流 | Pro、Max 5x、Max 20x |
| `/cost` | 顯示當前 session 的 token 用量與花費 | API key 使用者 |

---

## `/usage` —— 查看你的上限

顯示你當前方案的用量上限與速率限制狀態。在碰到上限前查看還剩多少容量很有用。

---

## `/extra-usage` —— 超出上限後繼續工作

`/extra-usage` 命令設定**隨用隨付的溢流計費**，讓 Claude Code 在你碰到方案速率限制時能無縫繼續工作，而不是把你擋下來。

### 運作方式

1. 你碰到方案的速率限制（上限每 5 小時重設）
2. 若已啟用額外用量且有可用資金，Claude Code 會不中斷地繼續
3. 溢流的 token 以**標準 API 費率**計費，與你的訂閱費分開

### 設定方式

CLI 中的 `/extra-usage` 命令會帶你完成設定。你也可以在 claude.ai 網頁的 **Settings > Usage** 設定：

1. 啟用額外用量
2. 新增付款方式
3. 設定**每月消費上限**（或選擇無上限）
4. 可選擇性加入**預付資金**，餘額低於門檻時自動儲值

### 重點細節

| 項目 | 值 |
|--------|-------|
| 每日兌換上限 | $2,000／天 |
| 計費 | 與訂閱分開，依標準 API 費率 |
| 上限重設視窗 | 每 5 小時 |

### 已知問題

截至 2026 年 2 月，`/extra-usage` CLI 命令[未被正式文件記載](https://github.com/anthropics/claude-code/issues/12396)，且可能開啟一個沒有明確設定選項的登入視窗。目前透過 **claude.ai 網頁介面**設定是比較可靠的路徑。

---

## `/cost` —— Session 花費（API 使用者）

對用 API key 驗證（而非訂閱方案）的使用者，`/cost` 顯示：

- 當前 session 的總成本
- API 時長與實際經過時間
- token 用量細目
- 做過的程式碼變更

這個命令與 Pro／Max 訂閱使用者無關。

---

## Fast 模式與額外用量

Fast 模式（`/fast`）使用 Claude Opus 4.6 並加快輸出。它與額外用量有特殊的計費關係：

- Fast 模式的用量**從第一個 token 起就一律計入額外用量**
- 即使你的訂閱方案還有剩餘用量也一樣
- Fast 模式不會消耗你方案內含的速率限制

這表示你必須啟用並儲值額外用量才能使用 `/fast`。

---

## CLI 啟動旗標

兩個與用量預算相關的啟動旗標（僅 API key 使用者，print 模式）：

| 旗標 | 說明 |
|------|-------------|
| `--max-budget-usd <AMOUNT>` | API 呼叫在停止前的最大美元金額 |
| `--max-turns <NUMBER>` | 限制代理回合數 |

完整清單見 [CLI 啟動旗標參考](../best-practice/claude-cli-startup-flags.md)。

---

## 資料來源

- [Extra usage for paid Claude plans — Claude Help Center](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)
- [Using Claude Code with your Pro or Max plan — Claude Help Center](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan)
- [/extra-usage slash command is undocumented — GitHub Issue #12396](https://github.com/anthropics/claude-code/issues/12396)
- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
