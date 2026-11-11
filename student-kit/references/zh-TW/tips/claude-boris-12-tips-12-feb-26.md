# 客製 Claude Code 的 12 種方式 —— 來自 Boris Cherny 的技巧

Claude Code 創造者 Boris Cherny（[@bcherny](https://x.com/bcherny)）於 2026 年 2 月 12 日分享的客製化技巧摘要。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`tips/claude-boris-12-tips-12-feb-26.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tips/claude-boris-12-tips-12-feb-26.md)

---

## 背景

Boris Cherny 指出，可客製性是工程師最愛 Claude Code 的特點之一 —— hooks、外掛、LSP、MCP、skills、effort、自訂代理、狀態列、輸出風格等等。他分享了開發者與團隊客製自己設定的 12 種實用方式。

<a href="https://x.com/bcherny/status/2021699851499798911"><img src="../tips/assets/boris-26-2-12/0.webp" alt="Boris Cherny 開場推文" width="50%" /></a>

---

## 1/ 設定你的終端機

為最佳 Claude Code 體驗設定終端機：

- **主題**：執行 `/config` 設定淺色／深色模式
- **通知**：為 iTerm2 啟用通知，或用自訂通知 hook
- **換行**：若在 IDE 終端機、Apple Terminal、Warp 或 Alacritty 中使用 Claude Code，執行 `/terminal-setup` 以啟用 shift+enter 換行（這樣就不用打 `\`）
- **Vim 模式**：執行 `/vim`

<a href="https://x.com/bcherny/status/2021699859359883608"><img src="../tips/assets/boris-26-2-12/1.webp" alt="設定你的終端機" width="50%" /></a>

---

## 2/ 調整努力等級

執行 `/model` 挑選你偏好的努力等級：

- **Low** —— 較少 token、回應更快
- **Medium** —— 平衡的行為
- **High** —— 較多 token、更高智慧

Boris 的偏好：所有事情都用 High。

<a href="https://x.com/bcherny/status/2021699860869902424"><img src="../tips/assets/boris-26-2-12/2.webp" alt="調整努力等級" width="50%" /></a>

---

## 3/ 安裝外掛、MCP 與 Skills

外掛讓你安裝 LSP（每個主流語言都有）、MCP、skills、代理與自訂 hook。

從官方 Anthropic 外掛市集安裝，或為你的公司建立自己的市集。把 `settings.json` commit 進 codebase 就能為團隊自動加入這些市集。

執行 `/plugin` 開始。

<a href="https://x.com/bcherny/status/2021699862522364149"><img src="../tips/assets/boris-26-2-12/3.webp" alt="安裝外掛、MCP 與 skills" width="50%" /></a>

---

## 4/ 建立自訂代理

在 `.claude/agents` 放 `.md` 檔即可建立自訂代理。每個代理都能有自訂名稱、顏色、工具組、預先允許與預先拒絕的工具、權限模式與模型。

你也可以用 `settings.json` 的 `"agent"` 欄位或 `--agent` 旗標，設定主對話的預設代理。

執行 `/agents` 開始。

<a href="https://x.com/bcherny/status/2021700144039903699"><img src="../tips/assets/boris-26-2-12/4.webp" alt="建立自訂代理" width="50%" /></a>

---

## 5/ 預先核准常見權限

Claude Code 的權限系統結合了 prompt 注入偵測、靜態分析、沙箱與人工監督。

開箱即用時只有一小組安全命令被預先核准。要預先核准更多，執行 `/permissions` 並加進 allow 與 block 清單。把這些 commit 進團隊的 `settings.json`。

完整支援萬用字元語法 —— 例如 `Bash(bun run *)` 或 `Edit(/docs/**)`。

<a href="https://x.com/bcherny/status/2021700332292911228"><img src="../tips/assets/boris-26-2-12/5.webp" alt="預先核准常見權限" width="50%" /></a>

---

## 6/ 啟用沙箱

啟用 Claude Code 的開源沙箱執行期，在減少權限提示的同時提升安全性。

執行 `/sandbox` 啟用。沙箱在你的機器上執行，同時支援檔案與網路隔離。

<a href="https://x.com/bcherny/status/2021700506465579443"><img src="../tips/assets/boris-26-2-12/6.webp" alt="啟用沙箱" width="50%" /></a>

---

## 7/ 加上狀態列

自訂狀態列會顯示在輸入框正下方，呈現模型、目錄、剩餘脈絡、成本，以及任何你工作時想看到的資訊。

每個團隊成員都能有不同的狀態列。用 `/statusline` 讓 Claude 依你的 `.bashrc`/`.zshrc` 產生一個。

<a href="https://x.com/bcherny/status/2021700784019452195"><img src="../tips/assets/boris-26-2-12/7.webp" alt="加上狀態列" width="50%" /></a>

---

## 8/ 客製你的快捷鍵

Claude Code 的每個鍵位綁定都可客製。執行 `/keybindings` 重新對應任何按鍵。設定會即時重載，讓你立刻感受效果。

<a href="https://x.com/bcherny/status/2021700883873165435"><img src="../tips/assets/boris-26-2-12/8.webp" alt="客製你的快捷鍵" width="50%" /></a>

---

## 9/ 設定 Hooks

Hooks 讓你確定性地掛進 Claude 的生命週期：

- 自動把權限請求導向 Slack 或 Opus
- 在 Claude 到達回合結尾時推它繼續（你甚至可以啟動一個代理，或用一個 prompt 來決定 Claude 該不該繼續）
- 對工具呼叫做前處理或後處理，例如加上你自己的日誌

請 Claude 幫你加一個 hook 來開始。

<a href="https://x.com/bcherny/status/2021701059253874861"><img src="../tips/assets/boris-26-2-12/9.webp" alt="設定 hooks" width="50%" /></a>

---

## 10/ 客製你的轉圈動詞

客製轉圈動詞，把預設清單換成或加上你自己的詞。把 `settings.json` commit 進版控就能與團隊共享這些動詞。

<a href="https://x.com/bcherny/status/2021701145023197516"><img src="../tips/assets/boris-26-2-12/10.webp" alt="客製你的轉圈動詞" width="50%" /></a>

---

## 11/ 使用輸出風格

執行 `/config` 設定輸出風格，讓 Claude 用不同的語氣或格式回應。

- **Explanatory** —— 熟悉新 codebase 時推薦，讓 Claude 邊做邊解釋框架與程式碼模式
- **Learning** —— 讓 Claude 指導你完成程式碼變更
- **Custom** —— 建立自訂輸出風格來調整 Claude 的語氣

<a href="https://x.com/bcherny/status/2021701379409273093"><img src="../tips/assets/boris-26-2-12/11.webp" alt="使用輸出風格" width="50%" /></a>

---

## 12/ 把所有東西都客製一遍！

Claude Code 開箱即用就很好，但當你真的要客製時，把 `settings.json` commit 進 git，讓團隊也能受益。設定支援多個層級：

- 為你的 codebase
- 為某個子資料夾
- 只為你自己
- 透過全企業政策

有 37 個設定與 84 個環境變數（用 `settings.json` 的 `"env"` 欄位就不必寫包裝腳本），你想要的任何行為很有機會都能設定出來。

<a href="https://x.com/bcherny/status/2021701636075458648"><img src="../tips/assets/boris-26-2-12/12.webp" alt="把所有東西都客製一遍" width="50%" /></a>

---

## 資料來源

- [Boris Cherny (@bcherny) on X — 2026 年 2 月 12 日](https://x.com/bcherny)
- [Claude Code Terminal Setup Docs](https://code.claude.com/docs/en/terminal)
- [Claude Code Plugins & Discovery Docs](https://code.claude.com/docs/en/discover-plugins)
- [Claude Code Sub-agents Docs](https://code.claude.com/docs/en/sub-agents)
- [Claude Code Permissions Docs](https://code.claude.com/docs/en/permissions)
- [Claude Code Sandbox Docs](https://code.claude.com/docs/en/sandbox)
- [Claude Code Status Line Docs](https://code.claude.com/docs/en/statusline)
- [Claude Code Keyboard Shortcuts Docs](https://code.claude.com/docs/en/keybindings)
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Claude Code Output Styles Docs](https://code.claude.com/docs/en/output-styles)
- [Claude Code Settings Docs](https://code.claude.com/docs/en/settings)
