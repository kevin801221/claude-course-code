# Windows 安裝設定

[回到 Day 0](README.md)

> 英文原文：[`tutorial/day0/windows.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tutorial/day0/windows.md)

---

**Node.js**
- 前往 [nodejs.org](https://nodejs.org)
- 點 **「Download Node.js (LTS)」** 按鈕 —— 這會下載 `.msi` 安裝程式
- 執行 `.msi` 檔，在精靈中一路按 **Next**
- 接受預設值，點 **Install**，等它跑完

**確認 Node.js**
- 開啟**新的**終端機（PowerShell 或 Windows Terminal）並執行：
  ```powershell
  node --version
  npm --version
  ```

**Claude Code**
- ```powershell
  npm install -g @anthropic-ai/claude-code
  ```
- 若出現權限錯誤，請以**系統管理員**身分執行終端機（右鍵 > 以系統管理員身分執行）

**確認**
- ```powershell
  claude --version
  ```

---

接著回到 [README.md](README.md) 進行驗證設定。
