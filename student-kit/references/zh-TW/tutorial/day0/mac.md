# macOS 安裝設定

[回到 Day 0](README.md)

> 英文原文：[`tutorial/day0/mac.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tutorial/day0/mac.md)

---

**終端機**
- 開啟 Terminal（按 `Cmd + Space`，輸入 "Terminal"，按 Enter）

**Homebrew**
- 檢查 Homebrew 是否已安裝：
  ```bash
  brew --version
  ```
- 若出現 "command not found"，先安裝 Homebrew：
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

**Claude Code**
- ```bash
  brew install --cask claude-code
  ```

**確認**
- ```bash
  claude --version
  ```

---

接著回到 [README.md](README.md) 進行驗證設定。
