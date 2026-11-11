# 09. TimeTrace — Claude 規則

教學用範例：用五大組件（Agents Team / Skills / MCP / Hooks / Pencil Design）一鏡到底蓋一個 SaaS。

## 目標

照 `WALKTHROUGH.md` 的 6 個 Module，把 TimeTrace（時間追蹤 + AI 自動分類）從零蓋到 demo 跑在瀏覽器。

## 現況

- 這個資料夾目前**只有藍圖 `WALKTHROUGH.md`**，成品尚未產出。
- 要實作時，照教案逐 Module 跑，產物（`.claude/agents/`、`.claude/hooks/`、`.claude/mcp.json`、Next.js app）落在這個資料夾。

## 規則

- 後端 Python 套件一律用 **uv** 管理，禁止 pip
- 前端用 Next.js 14 + Tailwind + shadcn/ui（教案技術選型）
- DB 用 Postgres，主鍵 uuid、每張表帶 created_at/updated_at/deleted_at（soft delete）
- 路徑用 `pathlib.Path`
- 回覆繁體中文
- commit 走 Kevin 個人帳號 `kevin801221`，不署名 Claude Code

## 不要做的事

- **不要動 `WALKTHROUGH.md` 的教學內容**（那是定稿藍圖，要改先問）
- 不要 hardcode API key / DB 密碼，用 `.env`（教案有 `no-secrets` hook 會擋）
- 不要把 prod DB 連線塞進 `mcp.json`（教案金句 #8）
- 不要用 Read 直接讀 `.pen`（加密，只能透過 Pencil MCP 的 batch_get）
