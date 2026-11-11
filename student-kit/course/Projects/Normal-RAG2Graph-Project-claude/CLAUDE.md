# Project Rules — Hybrid GraphRAG（Claude Code 版）

> 這份 `CLAUDE.md` 是 Claude Code 在這個專案內**自動讀取**的剛性規則。Claude Code IDE Extension（IDE 內寫 code 的 agent）跟 Claude Code CLI（終端機跑 review / commit / `/sync`）兩邊都吃這份。

## 語言
- 所有回應、commit message、註解一律繁體中文。
- 變數/函式名維持英文。

## 技術棧（鎖死）
- Backend: Python 3.10+、FastAPI、uv 管理依賴（禁用 pip/poetry）。
- Vector: ChromaDB（本地 persistent）。
- LLM: Google Gemini（生成：`gemini-2.5-flash`。向量 Embedding **極度強制寫死：`"models/gemini-embedding-001"`**，任何 Agent 絕對禁止私自替換成 text-embedding-004 等！）。
- Frontend: Next.js App Router + TypeScript + TailwindCSS。
- 圖譜視覺化: `react-force-graph-2d`。

## 工作流程
1. 動手寫 code 前，先產出 / 更新 `spec/spec.md` 與 `spec/PRD.md`。
2. 每完成一個 milestone，必須 `git commit`，訊息由 Claude Code CLI 跑 `/sync` 產生。
3. 禁止引入 Celery/Redis/Neo4j，背景工作只用 FastAPI BackgroundTasks。
4. 前後端透過 `chunk_id` 強綁定，Graph 與 Vector 不可分離。
5. **雙 Agent 協作**：每次完成階段性任務，IDE Extension 必須自動讀寫並更新專案根目錄的 `.collab-sync.md` 檔案，記錄完成項目、後續任務與狀態，再交由 Claude Code CLI 端跑 `/sync` 進行 Review 與 Commit。

## 禁忌
- 不要 mock 資料庫。
- 不要自行 npm install 未列在 Rules 的套件，先問。
- 不要動 `.env`、不要 commit API key。

## Skill 自動載入
專案內 `.claude/skills/` 提供以下 skills，Claude Code 會根據對話內容自動 invoke：

| Skill | 觸發時機 |
|---|---|
| `fastapi-uv-setup` | 建後端、跑 uv init、初始化 Python 專案 |
| `rag-pipeline` | 建 RAG 管線、parse/chunk/embed/Chroma |
| `graph-extraction` | 從 chunk 抽 entity-relation 寫 SQLite |
| `force-graph-ui` | 前端圖譜視覺化、節點高亮 |
| `cli-extension-sync` | 兩個 Claude（Extension ↔ CLI）之間的 sync 協議 |

**不要手動 `/skill xxx`**——Claude Code 會自己判斷。如果發現它沒載入該載的 skill，直接在對話中提到關鍵字（例如「建立 RAG 後端」「knowledge graph extraction」）即可觸發。

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **Normal-RAG2Graph-Project-claude** (554 symbols, 618 relationships, 3 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/Normal-RAG2Graph-Project-claude/context` | Codebase overview, check index freshness |
| `gitnexus://repo/Normal-RAG2Graph-Project-claude/clusters` | All functional areas |
| `gitnexus://repo/Normal-RAG2Graph-Project-claude/processes` | All execution flows |
| `gitnexus://repo/Normal-RAG2Graph-Project-claude/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
