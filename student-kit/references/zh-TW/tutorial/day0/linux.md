# Linux 安裝設定

[回到 Day 0](README.md)

> 英文原文：[`tutorial/day0/linux.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tutorial/day0/linux.md)

## 先決條件

你需要 **Node.js v18 或更高版本**與 **npm**。

## 步驟 1：安裝 Node.js

### 選項 A：透過 nodejs.org 下載頁搭配 fnm（推薦）

**fnm**（Fast Node Manager）是 Node.js 官方推薦的工具。它快速、輕量，且日後需要時能輕鬆切換 Node 版本。

1. 開啟瀏覽器前往 [nodejs.org/en/download](https://nodejs.org/en/download)。

2. 你會看到一列下拉選單寫著：**"Get Node.js® vXX.XX.X (LTS) for __ using __ with __"**。請如下設定：

   | 下拉選單 | 選擇 |
   |----------|--------|
   | Version | **vXX.XX.X (LTS)** —— 保持預設的 LTS 版本，不要改 |
   | OS | **Linux** |
   | Package Manager | **fnm**（在 "Recommended (Official)" 底下） |
   | Package Format | **npm** —— 保持預設 |

3. 頁面會顯示你該執行的確切命令。打開終端機複製貼上。它們大致長這樣：

   ```bash
   # 步驟 1 —— 安裝 fnm
   curl -fsSL https://fnm.vercel.app/install | bash

   # 步驟 2 —— 重啟終端機或重新載入 shell profile
   source ~/.bashrc   # 或：source ~/.zshrc（若你用 zsh）

   # 步驟 3 —— 安裝 Node.js
   fnm install 24   # 頁面會顯示確切的版本號
   ```

   > 版本號可能與上面不同 —— 一律以網站顯示的為準。

4. **關掉再重開終端機**（或執行上面的 `source` 命令），讓 `fnm`、`node` 與 `npm` 可用。

> **為什麼用 fnm？** 它在 Node.js 下載頁上屬於「Recommended (Official)」類別。跟 nvm 一樣，它把 Node 裝在你的家目錄，所以 npm 全域安裝永遠不需要 `sudo` —— 但 fnm 明顯更快（用 Rust 寫的），而且在 Windows、macOS 與 Linux 上行為一致。

### 選項 B：使用你發行版的套件管理器

這比較快，但可能裝到較舊版本的 Node.js。**安裝後請檢查版本** —— 若低於 v18，請改用選項 A。

**Ubuntu / Debian：**

```bash
sudo apt update
sudo apt install -y nodejs npm

# 檢查版本
node --version   # 必須是 v18 或更高
```

**Fedora：**

```bash
sudo dnf install -y nodejs npm
```

**Arch Linux：**

```bash
sudo pacman -S nodejs npm
```

### 選項 C：NodeSource（透過 apt 取得最新 LTS，不用 nvm）

適合想要最新 LTS 又不想用 nvm 的 Ubuntu/Debian 使用者：

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

## 步驟 2：確認 Node.js

```bash
node --version
npm --version
```

兩者都應印出版本號。`node --version` 必須顯示 v18.x 或更高。

## 步驟 3：安裝 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

> **權限錯誤？**
> - 若你用 **fnm** 或 **nvm**：不該發生。檢查它是否生效（`which node` 應指向你家目錄內的路徑，而非 `/usr/...`）。
> - 若你用系統安裝：可用 `sudo npm install -g @anthropic-ai/claude-code`，或修正 npm 全域目錄的權限：
>   ```bash
>   mkdir -p ~/.npm-global
>   npm config set prefix '~/.npm-global'
>   echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
>   source ~/.bashrc
>   ```

## 步驟 4：確認 Claude Code

```bash
claude --version
```

你應該會看到印出 Claude Code 版本。接著回到 [README.md](README.md) 進行驗證設定。

---

## 補充

- **WSL（Windows Subsystem for Linux）：** 本指南在 WSL 內也適用。只要在 WSL 終端機中照做即可。
- **PATH 問題：** 若安裝後找不到 `claude`，請確認 npm 的全域 bin 在你的 PATH 中。執行 `npm config get prefix` —— 該路徑下的 `bin/` 子目錄需要在 PATH 裡。
