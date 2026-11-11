# 小專案 1：/weekly-haiku 用 git log 寫俳句

> 週五下班前打 `/weekly-haiku`，30 秒給你一首詩總結這週工作。

## 為什麼做

- ❌ 週五下班前想 review 這週做了啥，但 git log 30 個 commit 看了想睡
- ❌ 寫週報像在交作業
- ✅ 用俳句的形式 review，順便產生可貼 IG 限動的素材

## 用到的 Claude Code feature

- 自訂 slash command (`.claude/commands/weekly-haiku.md`)
- `Bash(git log:*)` 權限 — 讓 Claude 讀 git history

## 安裝

### 方式 A：個人層（所有 repo 都能用）

```bash
mkdir -p ~/.claude/commands
cp .claude/commands/weekly-haiku.md ~/.claude/commands/
```

### 方式 B：專案層（commit 進 git，團隊共用）

```bash
# 在你的 repo 根目錄
mkdir -p .claude/commands
cp /path/to/this-folder/.claude/commands/weekly-haiku.md .claude/commands/
git add .claude/commands/weekly-haiku.md
git commit -m "Add /weekly-haiku slash command"
```

## 使用

```bash
cd ~/your-repo
claude
> /weekly-haiku
```

## 進階變化

- **`/commit-roast`** — 改成吐槽自己（「你這週留了 5 個 console.log」）
- **`/team-sonnet`** — 讀整個 team 的 commit 寫十四行詩
- **情緒分析** — 根據 commit message 判斷這週情緒（焦慮 / 順利 / 摸魚）
- **多語版** — 在 prompt 加「同時給日文 / 英文版」

## 故障排除

| 症狀 | 解法 |
|---|---|
| `command not found: /weekly-haiku` | 確認檔案在對的位置 (`~/.claude/commands/` 或 `.claude/commands/`) |
| Claude 拒絕跑 git log | 確認 frontmatter 有 `allowed-tools: Bash(git log:*)` |
| 俳句字數不對 | prompt 加更明確的「5 字 / 7 字 / 5 字」要求 |
