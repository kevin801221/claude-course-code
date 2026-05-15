# Projects — Claude Code 小專案實戰集

> 對應「Claude Code 完整教學 PPT」中的 6 個 mini-projects + GitNexus 工具包。
> 每個資料夾都是獨立可用的範例，含 `.claude/` 設定 + 詳細 README。

## 📦 8 個 Mini-Projects

| # | 資料夾 | Feature | 場景 |
|---|---|---|---|
| 1 | [`01-weekly-haiku/`](01-weekly-haiku/README.md) | Slash command | 用本週 git log 寫俳句 |
| 2 | [`02-recipe-genie/`](02-recipe-genie/README.md) | Sub-agent | 冰箱食譜助手 |
| 3 | [`03-youtube-notes/`](03-youtube-notes/README.md) | Skill | YouTube 連結變學習筆記 |
| 4 | [`04-pomodoro/`](04-pomodoro/README.md) | Hook | 番茄鐘提醒喝水 |
| 5 | [`05-organize-downloads/`](05-organize-downloads/README.md) | MCP server | 整理 Downloads 資料夾 |
| 6 | [`06-discord-dm-bot/`](06-discord-dm-bot/README.md) | Agent SDK | Discord 文字冒險 bot |
| 7 | [`07-weekly-reports-skill/`](07-weekly-reports-skill/README.md) | Production skill | GitHub commit 變週報 |
| 8 | [`08-agent-team-review/`](08-agent-team-review/README.md) | Agent teams | 3 人團隊跨層補完便利貼板 |

## 🛠 額外工具包

| 資料夾 | 內容 |
|---|---|
| [`build-gitnexus-skill-commandline/`](build-gitnexus-skill-commandline/README.md) | `/gitnexus` slash command + helper skill + 完整教學 |

## 🚀 快速使用流程

### 對於 slash command / agent / skill / hook：

```bash
# 1. 進到該專案資料夾
cd 01-weekly-haiku/

# 2. 看 README 學怎麼用
cat README.md

# 3. 安裝到個人層（所有 repo 都能用）
cp -r .claude/* ~/.claude/

# 或安裝到專案層（commit 進 git，團隊共用）
cp -r .claude/* /path/to/your/repo/.claude/
```

### 對於 MCP server (MP5)：

```bash
# 用 claude mcp add 一行裝完
claude mcp add fs npx -y @modelcontextprotocol/server-filesystem ~/Downloads
```

### 對於 SDK bot (MP6)：

```bash
cd 06-discord-dm-bot
pip install -r requirements.txt
cp .env.example .env  # 編輯填入 token
python discord_dm_bot.py
```

## 📚 對應教學文件

| 想看 | 看哪 |
|---|---|
| 概念 + 為什麼這樣設計 | `../Claude_Code_完整教學.pptx` |
| 完整建構指南（Hooks / Plugins / MCP / Skills 怎麼建） | `../Claude_Code_建構指南.md` |
| 簡化版 PPT（給混合 audience） | `../Claude_Code_教學版.pptx` |
| 想自己改 PPT | `../build_ppt_完整版.js` |

## 🎓 推薦學習順序

1. **MP1 weekly-haiku** — 最簡單，5 分鐘上手 slash command
2. **MP4 pomodoro** — 學 hook 機制，順便有實用價值
3. **MP3 youtube-notes** — 學 skill 結構（資料夾形式）
4. **MP2 recipe-genie** — 學 sub-agent，understanding 委派
5. **MP5 organize-downloads** — 學 MCP，接外部資料源
6. **MP6 discord-dm-bot** — 學 SDK，最進階
7. **MP8 agent-team-review** — 學 agent teams，多 Claude 實例並行協作（接在 sub-agent 之後學）

每個專案都可以**獨立完成**，照 README 跑即可。

## 📝 授權

這些範例皆為教學用途，可自由 fork / 修改 / 商用。
