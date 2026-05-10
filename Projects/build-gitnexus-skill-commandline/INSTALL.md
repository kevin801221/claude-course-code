# 安裝指南（30 秒搞定）

> 一鍵把 `/gitnexus` 裝到你電腦，所有 repo 都能用。

## 前置要求

- macOS / Linux / Windows (WSL)
- Node.js 18+（推薦 v20 LTS 或 v22）
- 已裝 Claude Code（`claude --version` 跑得出來）

## 一鍵裝（個人層，所有 repo 都能用）

打開 terminal，貼這段：

```bash
# 從 build-gitnexus-skill-commandline 複製到你的 ~/.claude/
SOURCE=/Users/kevinluo/claude-code-complete-tutorial/Projects/build-gitnexus-skill-commandline

mkdir -p ~/.claude/commands ~/.claude/skills

cp "$SOURCE/.claude/commands/gitnexus.md" ~/.claude/commands/
cp -r "$SOURCE/.claude/skills/gitnexus-helper" ~/.claude/skills/

echo "✅ /gitnexus 已裝！"
```

驗證：

```bash
ls ~/.claude/commands/gitnexus.md     # 應該存在
ls ~/.claude/skills/gitnexus-helper/  # 應該有 SKILL.md + reference/
```

## 第一次使用

```bash
# 進到任何 repo
cd ~/some-project

# 啟動 Claude Code
claude

# 在 REPL 內：
> /gitnexus
```

第一次 Claude 會：
1. 檢查 `gitnexus` 是否已裝（沒裝會自動 `npm install -g gitnexus`，要 1-3 分鐘）
2. 問你要哪種模式
3. 跑 analyze
4. 設定 MCP
5. 開瀏覽器

之後就每個 repo 進去都能直接用。

## 移除

```bash
rm ~/.claude/commands/gitnexus.md
rm -rf ~/.claude/skills/gitnexus-helper

# 順便移除 gitnexus 本體（選擇性）
npm uninstall -g gitnexus
claude mcp remove gitnexus
```

## 改放專案層（限定一個 repo）

如果只想在某個 repo 裡用（例如只在公司 repo 用、不想 pollute 個人）：

```bash
cd ~/your-repo
mkdir -p .claude/commands .claude/skills

SOURCE=/Users/kevinluo/claude-code-complete-tutorial/Projects/build-gitnexus-skill-commandline
cp "$SOURCE/.claude/commands/gitnexus.md" .claude/commands/
cp -r "$SOURCE/.claude/skills/gitnexus-helper" .claude/skills/

# Commit 進 git，團隊共用
git add .claude/
git commit -m "Add /gitnexus slash command + helper skill"
```
