## 在 Windows 上安裝 Claude Code (使用 WSL)

Claude Code 預設僅支援 Linux 和 MacOS。若要在 Windows 上使用 Claude Code，您可以使用 WSL (Windows Subsystem for Linux)。

1. 開啟 Microsoft Store。

2. 搜尋並安裝 **Ubuntu WSL**。

3. 在終端機中開啟 WSL。

4. 執行以下指令 (此流程遵循安全性最佳實踐)：

```bash
# 首先，儲存您現有的全域套件列表，以便日後遷移
npm list -g --depth=0 > ~/npm-global-packages.txt

# 為您的全域套件建立目錄
mkdir -p ~/.npm-global

# 配置 npm 使用新的目錄路徑
npm config set prefix ~/.npm-global

# 注意：請根據您使用的 Shell，將 ~/.bashrc 替換為 ~/.zshrc、~/.profile 或其他相應檔案
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc

# 套用新的 PATH 設定
source ~/.bashrc

# 現在於新位置重新安裝 Claude Code
npm install -g @anthropic-ai/claude-code
```

5. 現在，在您的 IDE 中，您可以透過 `Ctrl + J` 開啟終端機 (同樣使用此快捷鍵來關閉)，並點擊「+」號旁邊的向下箭頭，開啟 **Ubuntu (WSL)** 終端機。在此處執行 `claude` 指令即可啟動 Claude Code。
