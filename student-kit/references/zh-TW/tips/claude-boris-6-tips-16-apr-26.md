# 讓 Opus 4.7 發揮更多的 6 個技巧 —— 來自 Boris Cherny

Claude Code 創造者 Boris Cherny（[@bcherny](https://x.com/bcherny)）於 2026 年 4 月 16 日分享的技巧串 —— 在他自用 Opus 4.7 幾週之後。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`tips/claude-boris-6-tips-16-apr-26.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tips/claude-boris-6-tips-16-apr-26.md)

---

## 背景

自用 Opus 4.7 幾週後，Boris 覺得自己「生產力高得不可思議」，於是分享了六種榨出新模型更多價值的方法 —— 從權限自動化、努力等級調校，到驗證模式。

<a href="https://x.com/bcherny"><img src="../tips/assets/boris-26-4-16/0.png" alt="Boris Cherny 開場推文 —— 自用 Opus 4.7" width="50%" /></a>

---

## 1/ Auto 模式 —— 不再有權限提示

Opus 4.7 很愛做複雜的長時間任務：深度研究、重構程式碼、打造複雜功能、反覆迭代直到打中效能基準。過去你要嘛得在模型做這類長任務時盯著它，要嘛就用 `--dangerously-skip-permissions`。

Anthropic 最近推出 **auto 模式**作為更安全的替代方案。在這個模式下，權限提示會被導向一個模型驅動的分類器，由它判斷命令是否安全：

- 若安全，自動核准
- 若有風險，暫停並詢問

這代表模型執行時不用再盯著。更重要的是，你可以平行跑更多 Claude —— 若安全，你就能把注意力切到下一個 Claude。

Auto 模式現已對 Max、Teams 與 Enterprise 使用者的 Opus 4.7 開放。在 CLI 中按 **Shift+Tab** 可循環切換 `Ask permissions` → `Plan mode` → `Auto mode`，或在 Desktop 與 VS Code 的下拉選單中選取。

<a href="https://x.com/bcherny"><img src="../tips/assets/boris-26-4-16/1.png" alt="Boris Cherny 談 auto 模式" width="50%" /></a>

---

## 2/ 新的 /fewer-permission-prompts Skill

Anthropic 推出了新的 `/fewer-permission-prompts` skill。它會掃描你的 session 歷史，找出那些安全但反覆跳權限提示的常見 bash 與 MCP 命令，然後建議一份該加進權限白名單的命令清單。

用它來調校你的權限、避免不必要的權限提示，尤其是在你不使用 auto 模式的情況下。

<a href="https://x.com/bcherny"><img src="../tips/assets/boris-26-4-16/2.png" alt="Boris Cherny 談 /fewer-permission-prompts skill" width="50%" /></a>

---

## 3/ Recaps（回顧）

Anthropic 在本週稍早推出 **recaps**，為 Opus 4.7 做準備。Recaps 是代理做了什麼、接下來要做什麼的簡短摘要。

在離開幾分鐘或幾小時後回到長時間執行的 session 時非常有用：

```
* Cogitated for 6m 27s

* recap: Fixing the post-submit transcript shift bug. The styling-flash
  part is shipped as PR #29869 (auto-merge on, posted to stamps). Next:
  I need a screen recording of the remaining horizontal rewrap on `cc -c`
  to target that separate cause. (disable recaps in /config)
```

不想要的話可在 `/config` 中停用 recaps。

<a href="https://x.com/bcherny"><img src="../tips/assets/boris-26-4-16/3.png" alt="Boris Cherny 談 recaps" width="50%" /></a>

---

## 4/ Focus 模式

Boris 非常喜歡 CLI 中新的 **focus 模式**，它會隱藏所有中間過程，只聚焦在最終結果。模型已經到了他普遍信任它會執行正確命令、做出正確編輯的程度。他只看最終結果。

用 `/focus` 開關。

<a href="https://x.com/bcherny"><img src="../tips/assets/boris-26-4-16/4.png" alt="Boris Cherny 談 focus 模式" width="50%" /></a>

---

## 5/ 設定你的努力等級

Opus 4.7 使用**自適應思考（adaptive thinking）**取代思考預算。要調整模型多想或少想，就調 effort。

- **較低 effort** —— 回應更快、token 用量更低
- **較高 effort** —— 最高的智慧與能力

滑桿有五個等級：`low` · `medium` · `high` · `xhigh` · `max` —— 左邊是速度，右邊是智慧。

<a href="https://x.com/bcherny"><img src="../tips/assets/boris-26-4-16/5.png" alt="Boris Cherny 談努力等級" width="50%" /></a>

---

## 6/ 給 Claude 一個驗證自己工作的方法

最後，確保 Claude 有辦法驗證自己的工作。這一向很重要 —— 現在 4.7 能讓你從 Claude 拿到 2-3 倍的產出，所以比以往更重要。

驗證的樣貌依任務而不同：

- **後端工作** —— 讓 Claude 跑你的 server/service 做端到端測試
- **前端工作** —— 用 [Claude Chromium 擴充套件](https://code.claude.com/docs/en/chrome)給 Claude 操控瀏覽器的方法
- **桌面 App** —— 用 Computer Use

Boris 現在的 prompt 長得像 `Claude do blah blah /go`，其中 `/go` 是一個會做以下三件事的 skill：

1. 用 bash、瀏覽器或 computer use 對自己做端到端測試
2. 執行 `/simplify`
3. 開一個 PR

對長時間執行的工作，驗證更加重要 —— 當你回到任務時，你知道程式碼是能動的。

<a href="https://x.com/bcherny"><img src="../tips/assets/boris-26-4-16/6.png" alt="Boris Cherny 談驗證" width="50%" /></a>

---

## 資料來源

- [Boris Cherny (@bcherny) on X — 2026 年 4 月 16 日](https://x.com/bcherny)
