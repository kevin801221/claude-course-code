# Day 0 —— Claude Code 安裝設定

本指南帶你在自己的機器上安裝 Claude Code 並完成驗證，就能開始使用。

> 英文原文：[`tutorial/day0/README.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tutorial/day0/README.md)

## 步驟 1：安裝 Claude Code

選擇你的作業系統：

| 作業系統 | 指南 |
|----|-------|
| Windows | [windows.md](windows.md) |
| Linux | [linux.md](linux.md) |
| macOS | [mac.md](mac.md) |

依你的作業系統照著做，完成後回到這裡進行驗證設定。

---

## 步驟 2：確認安裝

照著你作業系統的指南做完後，確認一切正常：

```bash
node --version    # 應顯示 v18.x 或更高
claude --version  # 應顯示已安裝的 Claude Code 版本
```

---

## 步驟 3：登入

<img src="../../tutorial/day0/assets/login.png" alt="Claude Code 登入畫面" width="50%">

在終端機執行 `claude`。首次啟動時，它會請你選擇登入方式。

### 方式 1：訂閱（Claude Pro / Max）

- 選擇 **Claude.ai account**
- 瀏覽器會開啟 —— 登入並授權
- 回到終端機，你就登入好了

### 方式 2a：API Key（團隊邀請）

你的團隊管理員從 Anthropic 後台邀請你。

- 你會收到一封**邀請信** —— 接受邀請並建立你的 Anthropic 帳號
- 在終端機執行 `claude`
- 選擇 **Anthropic API Key**
- 你的 key 會在後台**自動產生** —— 不需手動設定
- Claude Code 立刻就能運作

### 方式 2b：API Key（你已經有 key）

如果有人把 key 分享給你（透過 Slack、email 等），或你自己建立了一個：

- 在終端機執行 `claude`
- 選擇 **Anthropic API Key**
- 貼上你的 key（以 `sk-ant-` 開頭）
- key 會被**永久儲存** —— 之後不會再問你

---
