# OpenCode 專用的 Superpowers 指南

這是配合 [OpenCode.ai](https://opencode.ai) 使用 Superpowers 的完整指南。

## 安裝方式

將 `superpowers` 加到你 `opencode.json`（全局或專案層級皆可）的 `plugin` 陣列中：

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git"]
}
```

重新啟動 OpenCode。該插件會透過 OpenCode 的插件管理器進行安裝並註冊所有技能。

你可以透過提問來驗證安裝是否成功：「告訴我關於你的超能力（Tell me about your superpowers）」

OpenCode 使用其特有的插件安裝機制。如果你同時使用 Claude Code、Codex 或其他環境，請為每個環境單獨安裝 Superpowers。

### 從舊版基於軟連結（Symlink）的安裝進行遷移

如果你之前是使用 `git clone` 與軟連結來安裝 Superpowers，請移除舊的設定：

```bash
# 移除舊的軟連結
rm -f ~/.config/opencode/plugins/superpowers.js
rm -rf ~/.config/opencode/skills/superpowers

# （可選）移除克隆的儲存庫
rm -rf ~/.config/opencode/superpowers

# 如果你曾為 superpowers 增加過 skills.paths，請將其從 opencode.json 中移除
```

然後按照上述步驟重新安裝。

## 使用方法

### 尋找技能

使用 OpenCode 原生的 `skill` 工具來列出所有可用技能：

```
use skill tool to list skills
```

### 載入技能

```
use skill tool to load superpowers/brainstorming
```

### 個人技能

在 `~/.config/opencode/skills/` 目錄中建立你自己的技能：

```bash
mkdir -p ~/.config/opencode/skills/my-skill
```

建立 `~/.config/opencode/skills/my-skill/SKILL.md` 檔案：

```markdown
---
name: my-skill
description: Use when [condition] - [what it does]
---

# My Skill

[Your skill content here]
```

### 專案技能

在你的專案目錄下的 `.opencode/skills/` 內建立特定於該專案的技能。

**技能優先順序：** 專案技能 > 個人技能 > Superpowers 技能

## 升級更新

OpenCode 會透過以 Git 為基礎的套件規格來安裝 Superpowers。某些 OpenCode 和 Bun 版本會在 Lockfile 或快取中鎖定已解析的 Git 依賴項，因此重新啟動可能無法獲取最新的 Superpowers 提交。如果沒有出現更新，請清除 OpenCode 的套件快取或重新安裝插件。

若要鎖定特定版本，請使用分支或標籤：

```json
{
  "plugin": ["superpowers@git+https://github.com/obra/superpowers.git#v5.0.3"]
}
```

## 運作原理

此插件主要執行兩項任務：

1. **注入引導上下文：** 透過 `experimental.chat.system.transform` 鉤子，為每次對話注入超能力意識。
2. **註冊技能目錄：** 透過 `config` 鉤子，讓 OpenCode 能自動發現所有 Superpowers 技能，而無需手動設定或建立軟連結。

### 工具映射對應

為 Claude Code 撰寫的技能會自動適配並映射至 OpenCode 的等效工具：

- `TodoWrite` → `todowrite`
- 使用 Subagents 的 `Task` → OpenCode 的 `@mention` 系統
- `Skill` 工具 → OpenCode 原生的 `skill` 工具
- 檔案操作 → OpenCode 原生的檔案工具

## 常見問題與排查

### 插件無法載入

1. 檢查 OpenCode 日誌：`opencode run --print-logs "hello" 2>&1 | grep -i superpowers`
2. 驗證你的 `opencode.json` 中插件那一行設定是否正確
3. 確保你運行的是較新版本的 OpenCode

### Windows 上的安裝問題

某些 Windows OpenCode 版本在處理以 Git 為基礎的插件規格時，其上游安裝程序存在問題（包括 `git+https` 網址的快取路徑，以及 Bun 即使在正常終端機下運作也找不到 `git.exe` 等問題）。如果 OpenCode 無法自動安裝插件，請嘗試使用系統的 `npm` 安裝，然後讓 OpenCode 指向該本地套件路徑：

```powershell
npm install superpowers@git+https://github.com/obra/superpowers.git --prefix "$HOME\.config\opencode"
```

然後在 `opencode.json` 中使用安裝好的套件路徑：

```json
{
  "plugin": ["~/.config/opencode/node_modules/superpowers"]
}
```

### 找不到技能

1. 使用 OpenCode 的 `skill` 工具列出所有可用技能
2. 檢查插件是否已成功載入（見上述步驟）
3. 確保每個技能都包含一個帶有有效 YAML frontmatter 的 `SKILL.md` 檔案

### 引導提示詞（Bootstrap）未出現

1. 檢查你的 OpenCode 版本是否支援 `experimental.chat.system.transform` 鉤子
2. 修改設定後重新啟動 OpenCode

## 尋求幫助

- 回報問題 (Issues): https://github.com/obra/superpowers/issues
- 主要說明文件: https://github.com/obra/superpowers
- OpenCode 官方文件: https://opencode.ai/docs/
