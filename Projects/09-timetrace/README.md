# 09. TimeTrace — 五大組件一鏡到底蓋一個 SaaS

> **學什麼**：把 Agents Team × Skills × MCP × Hooks × Claude(Pencil) Design 五件事串成「從接到需求到 demo 跑在瀏覽器」的一條工作流
> **時長**：3 小時（純內容 ~165 min + Q&A 15 min）
> **產出**：一個能跑、有 UI、有資料、有自動化把關的 SaaS scaffold（TimeTrace：時間追蹤 + AI 自動分類）

## 為什麼這個範例存在？

前面 01–08 是「一個 feature 一個範例」散著教。這個範例反過來：**用一個真實產品（TimeTrace），把五大組件各司其職地串成一條工作流**，示範它們不是五個獨立功能，而是「一條 pipeline 的五個齒輪，少一個都不轉」。

對應教學金句：**Agents 解決速度、Skills 解決重複、MCP 解決連線、Hooks 解決信任、Design 解決美感。**

## 狀態：藍圖已就緒，成品待跑

> ⚠️ 這個資料夾目前**只有教案藍圖（`WALKTHROUGH.md`），TimeTrace 成品還沒被蓋出來**。
> 教案的設計就是「現場一鏡到底、從零開始建」，所以成品要照著 `WALKTHROUGH.md` 跑一遍才會長出來。
> 跑完後，這裡會多出 `.claude/agents/`、`.claude/hooks/`、`.claude/mcp.json`、Next.js dashboard 等實際產物。

## 你會用到的 Claude Code 功能

- [x] sub-agents（Module 1：4 個 agent 並行做 spike）
- [x] skills（Module 2：把 spike 流程封裝成可複用 skill）
- [x] MCP（Module 3：接 GitNexus + Postgres + Pencil）
- [x] hooks（Module 4：5 種 hook 把流程焊死）
- [x] Claude/Pencil Design（Module 5：UI 在 .pen 設計 → 切版回 React）

## 起手式

教案是「現場從零建」，建議照 `WALKTHROUGH.md` 在一個乾淨資料夾跑（例如教案內示範的 `~/timetrace/`），把這個資料夾當**藍圖 + 完成後的成品收納處**。

```bash
# 先讀藍圖
open Projects/09-timetrace/WALKTHROUGH.md

# 環境前置（教案 Module 0）
claude --version   # >= 1.0
which uv           # 後端一律 uv，不用 pip
docker --version   # Postgres MCP 要用
```

## 流程（6 個 Module）

1. **M0 開場**（10 min）— 五件事為什麼一起學
2. **M1 Agents Team**（30 min）— 4 個 sub-agent 並行做需求 spike
3. **M2 Skills**（30 min）— 把 spike 流程沉澱成可複用 skill
4. **M3 MCP**（30 min）— 接 GitNexus + Postgres + Pencil
5. **M4 Hooks**（30 min）— 5 種 hook 把流程焊死
6. **M5 Pencil Design**（45 min）— UI 設計 → 切版回 React（整堂高潮）
7. **M6 收尾**（5 min）— 五件事拼成 personal SaaS factory

> 完整逐字稿、每段要打什麼、卡點對照表、講師備課 checklist 都在 `WALKTHROUGH.md`。

## 進階閱讀

- 配套藍圖：[`WALKTHROUGH.md`](./WALKTHROUGH.md)
- 單組件深講：`../../docs/walkthroughs/four_skills_walkthrough.md`、`hook_walkthrough.md`、`gitnexus_walkthrough.md`、`agent_team_walkthrough.md`
