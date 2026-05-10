# Claude Code 完整教學

> 從零到能自建 Skills、Sub-agents、Slash Commands、Hooks、MCP Server 的一站式教學 repo。

by [@kevin801221](https://github.com/kevin801221) · 2026

---

## 這個 repo 是什麼

把 [Claude Code](https://claude.com/claude-code) 的核心概念拆成 10 個可以照著做的章節，每章一個資料夾、一份 README、一組可複製的範例。

讀完之後你會：

- 知道 `CLAUDE.md`、`.claude/` 三層架構（個人 / 專案 / Plugin）到底在做什麼
- 會自己寫 Slash Commands、Skills、Sub-agents、Hooks
- 會用 Python（uv 管理）做一個自己的 MCP Server
- 看得懂三者怎麼搭配解真實場景

---

## 適合誰

| 你是… | 從哪一章開始 |
|---|---|
| 完全沒裝過 Claude Code | [Ch 01 安裝](./docs/01-installation/) |
| 用過但只會 chat，沒寫過設定檔 | [Ch 02 CLAUDE.md 與 .claude/](./docs/02-claude-md/) |
| 會用基本功能，想自訂指令 | [Ch 03 Slash Commands](./docs/03-slash-commands/) |
| 想做可重用的能力包 | [Ch 04 Skills](./docs/04-skills/) |
| 想做特化代理 | [Ch 05 Sub-agents](./docs/05-subagents/) |
| 想串外部工具 | [Ch 07 MCP Server](./docs/07-mcp-server/) |

---

## 章節大綱

| # | 章節 | 重點 |
|---|---|---|
| 00 | [序章：Claude Code vs 其他 AI 工具](./docs/00-intro/) | 設計哲學、為什麼要寫 `CLAUDE.md` |
| 01 | [安裝與第一次跑 Claude Code](./docs/01-installation/) | 安裝、登入、hello world |
| 02 | [CLAUDE.md 與 .claude/ 目錄結構](./docs/02-claude-md/) | 個人層 / 專案層 / Plugin 三層 |
| 03 | [Slash Commands 自訂指令](./docs/03-slash-commands/) | 寫一個 `/translate`、`/weekly-haiku` |
| 04 | [Skills 完整建構](./docs/04-skills/) | SKILL.md 格式、scripts、references |
| 05 | [Sub-agents 特化代理](./docs/05-subagents/) | code-reviewer、recipe-genie |
| 06 | [Hooks 事件鉤子](./docs/06-hooks/) | PreToolUse / PostToolUse / SessionStart |
| 07 | [MCP Server 自建](./docs/07-mcp-server/) | 用 Python（uv）做一個天氣 MCP |
| 08 | [三者搭配的真實場景](./docs/08-real-world/) | Skill + Sub-agent + MCP 怎麼湊 |
| 09 | [速查表 + FAQ](./docs/09-cheatsheet/) | 一頁速查、常見問題 |

---

## 怎麼用這個 repo

```bash
git clone git@github-personal:kevin801221/claude-code-complete-tutorial.git
cd claude-code-complete-tutorial

# 從第一章開始讀
open docs/01-installation/README.md
```

每章資料夾結構：

```
docs/0X-章節名/
├── README.md       # 這章在講什麼、怎麼做
└── examples/       # 可以直接複製到 ~/.claude/ 或專案 .claude/ 的範例
```

---

## 學習路徑建議

```
新手路徑：00 → 01 → 02 → 03 → 09
進階路徑：04 → 05 → 06 → 07 → 08
```

每章結尾都有「下一步」連結，跟著走就好。

---

## 環境需求

- macOS / Linux / Windows（WSL）
- Node.js 20+（裝 Claude Code CLI 用）
- Python 3.11+ 與 [uv](https://github.com/astral-sh/uv)（Ch 07 MCP server 才用得到）
- Claude 帳號（[claude.ai](https://claude.ai) 註冊）

---

## License

MIT
