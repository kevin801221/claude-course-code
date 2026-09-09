# 一鏡到底：用 Agents Team × Skills × MCP × Hooks × Claude Design 蓋一個 SaaS
> 從接到需求那一刻，到 demo 跑在瀏覽器上的完整工作流

> **對象**：已經會用 Claude Code 跑基本對話、但還沒把「五大組件」串起來的工程師 / PM / 設計師
> **時長**：3 小時 ±15 min（純內容 ~165 min + Q&A buffer 15 min）
> **形式**：講師一邊講一邊打，學員跟著敲。**全程一個專案、一鏡到底、絕不換 demo**
> **產出**：學員下課時手上有一個能跑、有 UI、有資料、有自動化把關的 SaaS scaffold
> **核心心法**：**「五件事不是五個功能，是一條工作流的五個齒輪。少一個都不轉。」**

---

## 為什麼是這五件事，而且要這個順序？

很多人學 Claude Code 是「散著學」——今天看 sub-agent、明天玩 hook、後天裝 MCP——學完還是不會在「真的接到需求」時用上。這份教材的目標是：**示範一個產品從 idea 到 demo 的完整一條路徑，五件事各司其職、不可替代**。

| 階段 | 真實痛點 | 對應的 Claude Code 能力 | 它解決的事 |
|---|---|---|---|
| 1. 接到需求要快速摸清 | 需要同時搞清楚競品、技術選型、資料模型——一個人慢 | **Agents Team**（多 sub-agent 並行） | 把「順序作業」變成「並行作業」 |
| 2. 流程要可複用 | 第二個專案再來一遍很煩 | **Skills** | 把方法論沉澱成可被別的 session 載入的指引 |
| 3. 要接外部世界 | LLM 不能直接打 DB / 設計工具 / GitHub API | **MCP** | 給 LLM 長手手 |
| 4. 流程要可信任 | Agent 會偷懶、會跳步、會 commit 不該 commit 的東西 | **Hooks** | 用程式碼強制 LLM 守規矩 |
| 5. 要有像樣的前端 | LLM 寫的 UI 通常很醜 | **Claude（or Pencil MCP）設計再回流** | 讓設計這件事也能融進 agent loop |

> **教學金句 #1**：「**Agents 解決速度、Skills 解決重複、MCP 解決連線、Hooks 解決信任、Design 解決美感。**這五件事每一件單獨拿出來都只是個玩具，串起來才是工程。」

---

## 全景儀表板（一張表看完 3 小時）

| 時段 | Module | 主題 | 切 IDE？ | 學員打哪些東西 | 收什麼 |
|---|---|---|---|---|---|
| 0:00–0:10 | M0 | 開場 + 五件事為什麼一起學 | ❌ 純講 | — | 心智模型 |
| 0:10–0:40 | **M1** | **Agents Team**：用 4 個 sub-agent 並行做需求 spike | ✅ | `claude` + `@market-scout` 等 | `docs/spike/` 4 份報告 |
| 0:40–1:10 | **M2** | **Skills**：把 spike 流程封裝成可複用 skill | ✅ | 寫 `~/.claude/skills/product-spike/SKILL.md` | 一個 personal skill |
| 1:10–1:40 | **M3** | **MCP**：接 GitNexus + Postgres + Pencil | ✅ | 改 `.claude/mcp.json`，跑 query | 三個活的 MCP server |
| 1:40–2:10 | **M4** | **Hooks**：5 種 hook 把流程焊死 | ✅ | 寫 `pre-commit` / `pre-tool-use` 等 | 一組會擋人的 hooks |
| 2:10–2:55 | **M5** | **Pencil Design 回流**：UI 在 .pen 設計 → 切版回 React | ✅ | 跟 pencil MCP 對話 + 切版 | 真的能跑的 dashboard |
| 2:55–3:00 | M6 | 收尾：把五件事拼成 personal SaaS factory | ❌ | — | 帶回家的 checklist |

> ⚠️ **最容易踩雷的兩段**：M3（MCP server 連線權限）跟 M5（Pencil 切版到 React 的格式轉換）。前一晚務必親手跑一遍。

---

# 📚 Module 0 ｜開場（10 min）

## 0.1 講師開場：先別動 IDE，先講故事（5 min）

開場第一句不要講「今天教 agents、skills、MCP、hooks」——學員會睡著。

**改講這個情境**：

> 「假設我下週要 demo 給投資人一個叫 TimeTrace 的 SaaS——簡單來說是 Toggl 的競品，但加了 AI 自動分類。我只有一個下午。
> 
> 過去你會怎麼做？打開 Notion 寫需求？開 Figma 畫圖？clone 一個 Next.js template？
> 
> 今天我要示範另一條路：**讓 Claude Code 同時派 4 個 agent 並行幫我做 spike，把流程沉澱成 skill，連到 GitNexus 跟 Postgres 抓真實資料、用 hooks 擋我 commit 錯東西、最後用 Pencil 設計 UI 再切版回來。**一個下午做完。」

> **教學金句 #2**：「不是 LLM 變強，是你**指揮 LLM 的方式**變了。」

## 0.2 環境檢查（5 min）

學員跟著做：

```bash
# 確認版本
claude --version                  # 必須 ≥ 1.0
which claude && which uv          # uv 沒裝 → 後面 Python 部分會死

# 建 demo 資料夾
mkdir -p ~/timetrace && cd ~/timetrace
git init && uv init               # 用 uv，不要用 pip（這是專案規矩）

# 開 Claude Code
claude
```

如果學員 `uv` 沒裝：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> **講師注意**：這段不要超過 5 分鐘。學員裝環境出問題的，請助教旁邊處理，不要全班等。

---

# 📚 Module 1 ｜Agents Team：四個 agent 並行做需求 spike（30 min）

## 1.1 觀念：為什麼要多 agent（5 min）

畫一張對比圖在白板上：

```
單 agent 模式 (順序)：
  Claude → 查競品 (5 min) → 想技術 (5 min) → 寫資料模型 (5 min) → 規劃 sprint (5 min)
  總時間 = 20 min，且後面查資料的記憶會被前面吃掉 context

多 agent 模式 (並行)：
  Claude (orchestrator)
    ├─ market-scout   查競品          ┐
    ├─ tech-architect 想技術選型      │  全部並行
    ├─ data-modeler   設計 schema     │  總時間 ≈ 6 min
    └─ sprint-planner 切 milestone    ┘  且每個 agent 各自獨立 context
```

**核心概念三句話**：
1. Sub-agent 是「**獨立 context 的 LLM 實例**」，不會把垃圾資訊帶回主對話
2. 主 agent 看到的只是 sub-agent 的「**最終報告**」，省 token 又省雜訊
3. **並行**是用一句話派多個 sub-agent 同時做事，這是 Claude Code 的隱藏殺手鐧

> **教學金句 #3**：「Sub-agent 不是『叫 AI 做事』，是『**把不該污染主對話的雜活外包出去**』。」

## 1.2 動手：定義四個 agent（10 min）

在 `~/timetrace/` 下建 4 個 agent 定義：

```bash
mkdir -p .claude/agents
```

**`.claude/agents/market-scout.md`**：
```markdown
---
name: market-scout
description: 競品分析專家。當使用者要做 product spike、找市場上類似產品時 MUST BE USED。回傳一份 markdown 報告，包含 3 個直接競品、各自的差異化、定價、技術 stack 推測。
tools: WebSearch, WebFetch, Write
---

你是資深的產品市調分析師。收到產品名稱或 idea 時：

1. WebSearch 找出 3-5 個直接競品（不要找 me-too 列表，找有差異化的）
2. 對每個競品用 WebFetch 抓 pricing page
3. 推測他們的技術 stack（從 careers page、tech blog、HTTP header）
4. 把報告寫到 docs/spike/market.md，分這四節：
   - TL;DR（3 句話）
   - 競品矩陣表（feature × 競品）
   - 定價區間
   - 技術 stack 推測 + 我們可以怎麼繞過他們

**禁止**：不要憑空編造數字、不要寫「綜合來說」這種廢話、報告控制在 400 字內。
```

**`.claude/agents/tech-architect.md`**：
```markdown
---
name: tech-architect
description: 技術選型架構師。當需要決定 frontend / backend / database / auth / hosting 技術 stack 時 MUST BE USED。
tools: WebFetch, Write, Read
---

你是有 10 年經驗的全端架構師，今天的任務是給「個人開發者 + 一週要 ship MVP」做技術選型。

選型原則（不可違反）：
- 後端優先 Python (FastAPI) 或 Next.js API routes，不要碰 Java/Spring
- 前端只用 Next.js 14 + Tailwind + shadcn/ui
- DB 用 Postgres (Supabase or Neon)，不要碰 Mongo
- 部署用 Vercel + Supabase，不要碰 AWS

把選擇 + 理由寫到 docs/spike/tech.md，每個選擇附「為什麼不選 X」一句話。
```

**`.claude/agents/data-modeler.md`**：
```markdown
---
name: data-modeler
description: 資料模型專家。當需要設計資料表、ER 圖、初始 schema 時 MUST BE USED。產出 SQL DDL + ER 描述。
tools: Write, Read
---

你是熟 Postgres 的資料模型專家。針對使用者描述的產品：

1. 找出核心 entity (3-5 個，不要超過)
2. 寫 PostgreSQL DDL 到 docs/spike/schema.sql
3. 寫 ER 描述（用 Mermaid 語法）到 docs/spike/schema.md
4. 每張表必須有 created_at, updated_at, deleted_at (soft delete)
5. 主鍵一律用 uuid，不要用 auto-increment int
```

**`.claude/agents/sprint-planner.md`**：
```markdown
---
name: sprint-planner
description: Sprint 規劃師。當需要把產品需求拆成可執行的 milestone 時 MUST BE USED。產出 5 天可 ship 的 roadmap。
tools: Write
---

你是精實創業的 sprint planner，原則是「**每天結束都要能 demo**」。

任務：把產品拆成 5 天，每天一個 milestone，寫到 docs/spike/sprint.md：

Day 1: 能跑起來的空殼 + 路由
Day 2: 跑得通的一條 happy path
Day 3: 加 auth + DB persist
Day 4: AI 自動分類功能
Day 5: polish UI + deploy

每個 day 列「完成判定條件」(3 條 checklist)。不要列「研究 X」這種非交付項目。
```

## 1.3 動手：一句話派四個 agent 並行（10 min）

回到 `claude` 對話視窗，學員打：

```
我要做一個叫 TimeTrace 的 SaaS——時間追蹤 + AI 自動分類，類似 Toggl 但加 AI。
請同時派 market-scout、tech-architect、data-modeler、sprint-planner 四個 agent
並行做 spike，分別產出 docs/spike/ 下的四份報告。
```

**講師現場示範重點**：

1. 等 Claude 回應後**指出畫面上的關鍵字**：「**parallel**」「**4 agents dispatched**」——這是並行的證據
2. 4 個 agent 跑完大約 5-7 分鐘，**這段不要乾等**，趁機講下面這段觀念
3. 跑完後 `ls docs/spike/` 學員應該看到 4 個檔案

**等待時講的觀念**：「為什麼這比『我自己一個一個問 Claude』快？」

```
你自己分 4 次問：
  問 #1 → Claude 回 (含背景知識 + 答案) → 你看完 → 問 #2 → ...
  context 累積、你的注意力被切碎

派 4 個 agent：
  Claude 一次派完 → 各 agent 獨立做 → 你只看 4 份報告
  context 不會互相污染、你只需要 review 最終產出
```

## 1.4 卡點預警（5 min）

| 卡點 | 症狀 | 救法 |
|---|---|---|
| Agent 不被 dispatch | Claude 回「我幫你做」自己動手 | 描述要更強硬：「**用 Task tool 派 sub-agent**，不要自己做」 |
| 報告品質差 | 寫得很空泛 | agent 定義裡 `description` 太鬆，加「**禁止**」條款 |
| 沒並行而是順序 | 一個跑完才跑下一個 | 一個 message 裡要明確說「**parallel / 同時**」 |
| `tools:` 限制錯 | Agent 想用 Bash 但定義沒給 | agent 定義裡的 `tools:` 是白名單，要寫進去 |

> **教學金句 #4**：「Sub-agent 寫得好不好，看 **description 寫得夠不夠狠**。description 是給主 Claude 看的『**什麼時候該派我**』，越具體越會被叫到。」

## 1.5 課堂練習（5 min）

學員自己加一個第 5 個 agent：`pricing-strategist`，要它做 SaaS 定價建議。寫完用 `@pricing-strategist 幫 TimeTrace 想定價` 觸發。

**驗收**：Claude 應該明確說「dispatch pricing-strategist agent」。

---

# 📚 Module 2 ｜Skills：把 spike 流程沉澱成可複用方法（30 min）

## 2.1 觀念：Skill 跟 Agent 有什麼不同？（5 min）

這是學員最容易搞混的地方。在白板上畫：

```
Agent：
  「一個獨立 context 的 LLM 實例」
  我「派人」去做事
  跑完就消失，不留下方法論

Skill：
  「給主 Claude 看的『遇到 X 情境，請用這個方法做』」
  我「教 Claude」做事的方式
  常駐，下次遇到同樣場景自動觸發

CLAUDE.md：
  「給主 Claude 看的『這個專案的規矩』」
  專案級別，僅這 repo

Slash command：
  「給人類用的快捷鍵」
  /foo → 觸發某段 prompt

差別：
  Agent  = 外包員工
  Skill  = 公司內部 SOP
  CLAUDE = 公司文化
  Slash  = 老闆按鈕
```

> **教學金句 #5**：「Agent 是『**我派誰去做**』，Skill 是『**遇到這種事用什麼方法做**』。」

## 2.2 動手：把 spike 流程封裝成 skill（10 min）

剛才 M1 學員用了 4 個 agent 做 spike。現在的問題是：**下次做另一個產品，要再寫一次 prompt 嗎？** 不要，封裝成 skill。

```bash
mkdir -p ~/.claude/skills/product-spike
```

**`~/.claude/skills/product-spike/SKILL.md`**：

```markdown
---
name: product-spike
description: Use when the user describes a new product idea (SaaS, app, MVP) and needs rapid technical/market exploration. Triggers on phrases like "I want to build X", "我想做一個", "幫我看看可行性", "做個 spike". Dispatches 4 parallel sub-agents to produce a complete spike report in docs/spike/.
---

# Product Spike Skill

When the user describes a new product idea, do NOT start coding immediately.
Instead, run this 4-step parallel spike:

## Step 1: Verify sub-agents exist

Check `.claude/agents/` for these 4 agents:
- market-scout
- tech-architect
- data-modeler
- sprint-planner

If any is missing, ask the user to install them first (point to ~/.claude/skills/product-spike/agents/ for templates).

## Step 2: Dispatch in parallel

In ONE message, dispatch all 4 agents with the Task tool. They must run in parallel, not serial.

The product context passed to each agent should include:
- Product name
- One-sentence pitch
- Target user (個人 / SMB / Enterprise)
- Budget tier (free / freemium / paid)

## Step 3: Wait, then synthesize

After all 4 reports land in docs/spike/, write a TL;DR synthesis to docs/spike/README.md:
- 1 paragraph: should we build this?
- 3 bullet points: biggest risks
- 1 sentence: recommended next action

## Step 4: Hand off

End by asking the user: "要我用 Day 1 的 sprint plan 開始實作嗎？"

## Anti-patterns (do NOT do)

- Do NOT start coding before all 4 reports are done
- Do NOT skip market-scout because "I know the market"
- Do NOT write the synthesis before reading all 4 reports
- Do NOT promise timelines longer than what sprint-planner says
```

**`~/.claude/skills/product-spike/agents/`** 放 4 個 agent template（從剛才 M1 複製過去）：

```bash
cp -r ~/timetrace/.claude/agents ~/.claude/skills/product-spike/agents
```

## 2.3 動手：測 skill 真的會被觸發（10 min）

**開新對話**（重要！skill 觸發要在乾淨 context）：

```bash
cd ~/timetrace && claude
```

學員打：

```
我想做一個叫 FoodMood 的 app——記錄吃什麼然後 AI 分析心情關聯。
```

**講師現場觀察**：Claude 應該主動說「I'll use the **product-spike** skill」並開始派 4 個 agent。如果沒有：
- 檢查 SKILL.md 的 frontmatter `description` 是否包含觸發詞（"want to build", "我想做"）
- 檢查 `~/.claude/skills/product-spike/SKILL.md` 路徑對不對

## 2.4 Skill 的高階用法：parameterize（5 min）

進階：skill 可以吃參數。改 `description`：

```markdown
description: ... Accepts optional args: --depth (quick|deep), --skip-market.
```

然後在 SKILL.md 內讀 `$ARGS`。

**示範**：學員打 `/product-spike --skip-market FoodMood` 應該只跑 3 個 agent。

> **教學金句 #6**：「**Skill 的價值不是『讓 Claude 多會一招』，是『讓你的方法論可以跨 session、跨專案、跨團隊複用』。**寫 skill 等於寫 SOP。」

---

# 📚 Module 3 ｜MCP：給 LLM 長手手連外部世界（30 min）

## 3.1 觀念：MCP 到底在解什麼問題？（5 min）

白板畫一張：

```
沒有 MCP 的 Claude Code：
  Claude ─→ Bash / Read / Write / Edit / WebFetch ─→ 你的電腦
                     ↑ 只能做這些

有 MCP 的 Claude Code：
  Claude ─→ Bash / ... 
       ─→ MCP server (Postgres) ──→ DB
       ─→ MCP server (GitNexus) ──→ codebase graph
       ─→ MCP server (Pencil)   ──→ 設計檔
       ─→ MCP server (Figma)    ──→ Figma 檔
       ─→ MCP server (你寫的)   ──→ 任何 API
```

**核心三句**：
1. MCP = **Model Context Protocol**，是 Anthropic 推的「LLM 跟外部工具溝通的標準」
2. 一個 MCP server 對 Claude 來說就是「**多了一組工具**」（多了一堆 `mcp__xxx__yyy` tool）
3. **要用一個工具前，先確認該 server 有跑起來**

> **教學金句 #7**：「**MCP 不是『讓 LLM 變聰明』，是『讓 LLM 能摸到原本摸不到的東西』。**沒有 MCP 的 LLM 是缸中之腦。」

## 3.2 動手：裝三個 MCP server（15 min）

**TimeTrace 真實需要的三個 MCP**：
- **GitNexus**：把 codebase 變成 knowledge graph，問 "什麼 import 了 X"
- **Postgres**：直接讀寫 DB
- **Pencil**：等下 M5 要設計 UI 用

**`.claude/mcp.json`**（在 `~/timetrace/` 下建）：

```json
{
  "mcpServers": {
    "gitnexus": {
      "command": "uvx",
      "args": ["gitnexus-mcp@latest"],
      "env": {}
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres",
               "postgresql://timetrace:dev@localhost:5432/timetrace"],
      "env": {}
    },
    "pencil": {
      "command": "npx",
      "args": ["-y", "@pencil/mcp@latest"],
      "env": {
        "PENCIL_API_KEY": "${PENCIL_API_KEY}"
      }
    }
  }
}
```

**啟動 Postgres**（學員可能沒有，提供 docker 方案）：

```bash
docker run -d --name timetrace-pg \
  -e POSTGRES_USER=timetrace \
  -e POSTGRES_PASSWORD=dev \
  -e POSTGRES_DB=timetrace \
  -p 5432:5432 \
  postgres:16
```

**重啟 Claude Code** 讓它讀新的 `mcp.json`：

```bash
# 退出再進入
exit
claude
```

**驗證 MCP 跑起來**：

```
/mcp
```

應該看到三個 server 列出。

## 3.3 動手：用 MCP 跑真實任務（10 min）

**任務 1：把剛才 data-modeler 的 schema 套到真實 DB**

學員打：
```
讀 docs/spike/schema.sql，用 postgres MCP 把 schema 套到 DB，然後用 mcp__postgres__query 列出建好的 table。
```

**任務 2：用 GitNexus 看 codebase 結構**

```
用 gitnexus 把這個 repo 建一次 graph，然後告訴我有哪些 entry point。
```

（這個 repo 還沒有 code，跑出來會很乾淨——這是好事，剛開始就建 graph）

**任務 3：先預習 Pencil**

```
用 pencil MCP 開一個新檔，叫 timetrace-dashboard.pen。
```

## 3.4 卡點預警（5 min）

| 卡點 | 症狀 | 救法 |
|---|---|---|
| `/mcp` 看不到 server | 沒重啟 Claude Code | 退出再進入 |
| Postgres 連不上 | docker 沒起來 / port 衝突 | `docker ps`，5432 換成 5433 |
| `PENCIL_API_KEY` 沒設 | 報 auth error | `export PENCIL_API_KEY=xxx` 或進 .env |
| MCP tool 不被叫 | Claude 用 Bash 自己連 DB | 明確說「**用 mcp__postgres__**」 |

> **教學金句 #8**：「**MCP server 的安全模型 = 你電腦的安全模型。**Postgres MCP 拿到的是 DB 連線，跟你 `psql` 同等權限。**正式環境千萬別塞 prod DB 進 mcp.json**。」

---

# 📚 Module 4 ｜Hooks：用程式碼焊死流程（30 min）

## 4.1 觀念：Hook 不是「自動化」，是「強制執行」（5 min）

學員最常見的誤解：「hook 不就是 git hook 嗎？」不是。

```
Git hook  = 在 git 操作前後跑 shell
Claude hook = 在 LLM 動作前後跑 shell
            ↑ 對象是 LLM，不是 git
```

**6 種 hook 時機**（這是現在 Claude Code 支援的）：

| Hook 名稱 | 什麼時候觸發 | 拿來做什麼 |
|---|---|---|
| `SessionStart` | 開新 session | 自動 inject 公司資訊、檢查環境 |
| `UserPromptSubmit` | 使用者送出 prompt 前 | 改寫 prompt、檢查敏感字 |
| `PreToolUse` | LLM 要呼叫某 tool 前 | **擋下危險操作**、要使用者確認 |
| `PostToolUse` | tool 跑完後 | 自動 lint、自動 test |
| `Notification` | 系統有事要通知時 | 推到 Slack |
| `Stop` | LLM 結束回應時 | 自動 commit、自動 push、發 telegram |

> **教學金句 #9**：「**Hook 是把『要這樣做』從 prompt 升級成『不這樣做就跑不下去』。**Prompt 可以被 LLM 偷懶忽略，hook 不行——它是 shell。」

## 4.2 動手：5 個 hook 把 TimeTrace 焊死（20 min）

**`.claude/settings.json`** 加 hooks 段（在 `~/timetrace/`）：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/session-start.sh" }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/block-dangerous-bash.sh" }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/no-secrets.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/auto-format.sh" }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/auto-commit.sh" }
        ]
      }
    ]
  }
}
```

### Hook 1：SessionStart — 自動報專案狀態

**`.claude/hooks/session-start.sh`**：

```bash
#!/usr/bin/env bash
# 開 session 自動告訴 Claude 目前專案狀態
cat <<EOF
=== TimeTrace 專案現況 ===
Branch: $(git branch --show-current 2>/dev/null || echo "(no git)")
Uncommitted files: $(git status -s 2>/dev/null | wc -l | tr -d ' ')
Latest commit: $(git log -1 --oneline 2>/dev/null || echo "no commits yet")
DB status: $(docker ps --filter name=timetrace-pg --format '{{.Status}}' 2>/dev/null || echo "down")
EOF
```

```bash
chmod +x .claude/hooks/session-start.sh
```

### Hook 2：擋危險的 Bash

**`.claude/hooks/block-dangerous-bash.sh`**：

```bash
#!/usr/bin/env bash
# 讀 stdin 拿到 LLM 想跑的 command
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# 黑名單
if echo "$CMD" | grep -qE 'rm -rf /|git push --force|drop database|drop table'; then
  echo "BLOCKED: 危險指令 → $CMD" >&2
  exit 2  # exit code 2 = 擋下這次 tool call
fi
```

### Hook 3：擋 commit 含 secret

**`.claude/hooks/no-secrets.sh`**：

```bash
#!/usr/bin/env bash
INPUT=$(cat)
CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // ""')

if echo "$CONTENT" | grep -qE 'sk-[a-zA-Z0-9]{32,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36}'; then
  echo "BLOCKED: 內容疑似含 API key 或 token" >&2
  exit 2
fi
```

### Hook 4：寫完 .py / .tsx 自動 format

**`.claude/hooks/auto-format.sh`**：

```bash
#!/usr/bin/env bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

case "$FILE" in
  *.py)  uv run ruff format "$FILE" 2>/dev/null ;;
  *.ts|*.tsx|*.js|*.jsx) npx prettier --write "$FILE" 2>/dev/null ;;
esac
```

### Hook 5：Stop 後自動 commit（小心使用）

**`.claude/hooks/auto-commit.sh`**：

```bash
#!/usr/bin/env bash
# 只在有 staged changes 時 commit
if ! git diff --cached --quiet 2>/dev/null; then
  git commit -m "auto: claude code session $(date +%Y%m%d-%H%M)" \
    --author="kevin801221 <kevin801221@users.noreply.github.com>" \
    2>/dev/null || true
fi
```

```bash
chmod +x .claude/hooks/*.sh
```

## 4.3 動手：實測 hook 真的會擋（5 min）

學員打：

```
跑 rm -rf /
```

Claude 應該被 hook 擋下，回報 "BLOCKED"。

學員打：

```
寫一個檔 secret.txt 內容是 sk-proj-abcdefg1234567890abcdefg1234567890abc
```

也應該被擋下。

## 4.4 卡點預警

| 卡點 | 症狀 | 救法 |
|---|---|---|
| hook 沒被觸發 | command 跑了但沒擋 | `chmod +x`、檢查 `.claude/settings.json` 路徑 |
| hook 一直 exit 1 | tool call 都被擋 | 看 stderr：`claude --debug` |
| auto-commit 把 .env 也 commit | 災難 | hook 改成 `git diff --cached --name-only \| grep -v env` |

> **教學金句 #10**：「Hook 像家裡的瓦斯防爆閥——**99% 的時候你忘記它存在，1% 救你一命**。寫的時候請當作 production code，不是 demo script。」

---

# 📚 Module 5 ｜Claude Design with Pencil：UI 設計 → 切版回流（45 min）

> **這是整堂課的高潮**。前面 4 個 module 都是後端 / 流程，這個 module 把美感拉進來。
> **講師注意**：這段最容易拖時間，記得控速。

## 5.1 觀念：為什麼要把 design tool 接進 LLM 工作流？（5 min）

```
傳統流程：
  PM 寫 Notion → 設計師畫 Figma → 工程師切版 → 來回 review 3 輪
  痛點：每一步都是「換工具 + 換人」

接 Design MCP 後：
  跟 Claude 對話 ─┬─→ 派 agent 想需求
                  ├─→ 用 pencil MCP 在 .pen 設計
                  ├─→ 用 Claude design 跟你來回改
                  └─→ 切版回 React 落到 Next.js
  痛點消失：一個視窗、一個 LLM、一條 thread
```

**Pencil MCP 的特點**：
- `.pen` 檔是加密的，只能透過 MCP tool 讀寫（不能用 Read 直接看）
- 有 `batch_get` / `batch_design` 兩個核心工具
- 可以 export 成 PNG / 切成 React component

> **教學金句 #11**：「**設計不應該是 LLM 工作流的外掛，應該是內建步驟。**接上 Pencil MCP，等於請了一個永遠不會煩的設計師。」

## 5.2 動手：先想清楚 UI 要什麼（5 min）

學員打：

```
派 ui-planner agent 幫我規劃 TimeTrace dashboard 的主畫面。
要點：
- 左 sidebar: 專案列表
- 中間: 今天的 time entries (timeline)
- 右上: 在跑的 timer (大字, 紅色點)
- 右下: 今天的 AI 自動分類 summary

請產出 docs/design/dashboard-spec.md，包含元件樹 + 互動描述。
```

（讓 Claude 生規格，我們等下對著規格設計）

## 5.3 動手：開 Pencil 設計（15 min）

學員打：

```
用 pencil MCP 開一個新檔 timetrace-dashboard.pen。
然後根據 docs/design/dashboard-spec.md 設計這個畫面。
規範：
- 用 Tailwind 風格的色 (slate-900 背景, indigo-500 強調)
- Inter 字型
- 圓角 12px
- 卡片有 subtle shadow
```

**講師現場示範**：

1. Claude 會呼叫 `mcp__pencil__open_document`
2. 然後呼叫 `mcp__pencil__batch_design` 一次插入多個 node
3. **重點 demo**：截 screenshot 給學員看 `mcp__pencil__get_screenshot`

**講師可以做的對話式 iteration**：

```
sidebar 太寬，縮到 240px
今天 timeline 的時間 block 改成漸層 (indigo-400 → indigo-600)
右上 timer 字太小，改 48px
```

**每一次改完截一張圖給學員看「畫面真的變了」**——這是最有衝擊力的 demo moment。

## 5.4 動手：切版回 React（15 min）

設計完了，要落地。

```
讀 timetrace-dashboard.pen，把它切成 Next.js 14 + Tailwind 的 page.tsx。
規則：
- 用 shadcn/ui 的 Card、Button、Avatar 元件
- 拆成 3 個 component: <Sidebar/> <Timeline/> <TimerWidget/>
- 寫到 app/dashboard/page.tsx 跟 components/dashboard/
- 假資料寫到 lib/mock-data.ts
```

Claude 會：
1. `mcp__pencil__batch_get` 把 .pen 內容讀出來
2. 分析元件樹
3. 對應到 shadcn 元件
4. 寫出 React code

**講師現場跑起來**：

```bash
# 學員打開新 terminal
cd ~/timetrace
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
npx shadcn@latest init
npx shadcn@latest add card button avatar
npm run dev
```

開 `http://localhost:3000/dashboard`——**畫面應該跟 Pencil 設計的長得一樣**。

> **這個瞬間是整堂課的高潮**。學員會看到：design tool 裡的圖 → 一句話 → 真的在瀏覽器跑起來。

## 5.5 動手：design 回流改 code（5 min）

最後示範「設計回頭改」的 round-trip：

```
我覺得右上 timer 太大了，回 .pen 改成 32px，然後把 page.tsx 同步更新。
```

Claude 應該：
1. `mcp__pencil__batch_design` 改 .pen
2. Edit `components/dashboard/TimerWidget.tsx` 同步改

**這個雙向同步是 design system 的聖杯**——示範完跟學員強調這件事。

> **教學金句 #12**：「**設計跟程式碼一直是兩條平行線，現在 LLM 是橋。**改 design 自動改 code、改 code 也可以反推 design——這是過去 10 年設計工程界沒解決的事。」

## 5.6 卡點預警

| 卡點 | 症狀 | 救法 |
|---|---|---|
| Pencil MCP 沒裝 | `mcp__pencil__*` tool 不存在 | 回 M3 檢查 `mcp.json` |
| .pen 檔讀不到 | 用 Read 想看 .pen → 失敗 | 一定要用 `batch_get`，.pen 是加密的 |
| shadcn 元件對不上 | 切版生出來樣式怪 | prompt 加「**對應到 shadcn/ui 的 X 元件**」 |
| Tailwind class 不生效 | 樣式跑掉 | `tailwind.config.ts` 沒包到 components/，加路徑 |

---

# 📚 Module 6 ｜收尾：五件事拼成 personal SaaS factory（5 min）

## 6.1 把今天串起來

最後一張白板畫：

```
     ┌─ Agents Team  ──┐ 並行探索
     │                  │
     ├─ Skills ─────────┤ 沉澱方法
     │                  │
     ├─ MCP ────────────┤ 連外部世界
     │                  │
     ├─ Hooks ──────────┤ 強制流程
     │                  │
     └─ Pencil Design ──┘ 美感落地
              │
              ▼
        TimeTrace（demo 跑在瀏覽器）
```

## 6.2 帶回家的 5 件事

1. **下一個 idea**：開 `claude` 第一句先講 idea，**讓 product-spike skill 自動觸發**
2. **下一個 repo**：第一件事是建 `.claude/agents/`、`.claude/hooks/`、`.claude/mcp.json` 三件套
3. **下一次設計**：別再切到 Figma，**直接 Pencil MCP 在對話裡設計**
4. **下一次 commit**：讓 Stop hook 幫你 commit、別自己 commit
5. **下一個 skill**：每完成一個專案，問自己「**這個流程下次能不能用？**」能就抽成 skill

## 6.3 最後一句

> **教學金句 #13**：「3 年前你用 LLM 寫程式碼，1 年前你用 LLM 寫測試，現在你用 LLM **跑整條工作流**——明年呢？**自己想清楚這題，或是被想清楚的人取代。**」

---

# 附錄 A：講師備課 checklist（前一晚做）

```bash
# 環境
[ ] claude --version ≥ 1.0
[ ] uv 裝好
[ ] docker 可跑 postgres
[ ] PENCIL_API_KEY 拿到並 export

# 預跑（避免現場炸）
[ ] 把 M1 的 4 個 agent 跑過一次，確認 docs/spike/ 都生得出來
[ ] 把 M3 的 mcp.json 跑過 /mcp 確認 3 個 server 都 up
[ ] 把 M4 的 hook 用 rm -rf / 測過會擋
[ ] 把 M5 整條跑過一次（最容易出意外的就這段）

# 備援
[ ] M1 跑掛的話備一份 docs/spike/ 截圖 PNG 直接展示
[ ] M3 Postgres 連不上的話備一份 sqlite fallback config
[ ] M5 Pencil 連不上的話備一份預錄影片 60s
```

# 附錄 B：學員端前一晚發給他們的訊息

```
明天 3 小時 Claude Code 進階課，請預先：

1. 裝 Claude Code (>= 1.0)：https://claude.com/code
2. 裝 uv：curl -LsSf https://astral.sh/uv/install.sh | sh
3. 裝 Docker Desktop 並確認可跑容器
4. 申請 Pencil API key（如要做 M5 設計段）
5. 確認 ~/.claude/ 資料夾存在（沒有的話 mkdir 一下）

當天會做的事：
- 從 0 蓋一個叫 TimeTrace 的 SaaS（時間追蹤 + AI 分類）
- 不需要事先 clone repo，當天會在 ~/timetrace/ 建

請帶筆電 + 充電線。
```

# 附錄 C：常見學員問題（FAQ）

**Q1: Agent 跟 Skill 我永遠搞不清楚**
A: 一句話：Agent 是「**派誰**」，Skill 是「**怎麼派**」。一個 skill 通常會調用多個 agent。

**Q2: MCP server 會偷我資料嗎？**
A: 會。**MCP server 是有完整存取權的本地程式**。只裝你信任作者的、開源的、你能看 source 的。

**Q3: Hooks 跟 git hooks 衝突嗎？**
A: 不衝突，**作用對象不同**。Claude hook 攔 LLM 的動作、git hook 攔 git 的動作。可以同時存在。

**Q4: 為什麼非要 uv 不用 pip？**
A: uv 比 pip 快 10-100 倍、自動管 virtualenv、lock file 比 requirements.txt 可靠。這是專案規矩。

**Q5: Pencil 一定要付費嗎？有免費替代嗎？**
A: 可以用 Claude.ai artifact + 對話設計，再貼回 Claude Code。流程一樣，只是少了「持久化設計檔」這層。

**Q6: 3 小時學完我就會了嗎？**
A: 你會「**看過完整流程一次**」，這不等於「會用」。**回家挑一個自己的小專案重跑這條 pipeline**——跑完才算學會。

---

# 附錄 D：延伸閱讀

- **Anthropic 官方 sub-agent doc**：https://docs.claude.com/en/docs/claude-code/sub-agents
- **MCP 規範**：https://modelcontextprotocol.io/
- **Pencil MCP**：（裝完後 `npx @pencil/mcp@latest --help`）
- **Hook 完整 spec**：https://docs.claude.com/en/docs/claude-code/hooks
- **Skills 系統設計**：https://docs.claude.com/en/docs/claude-code/skills

---

# 附錄 E：本教材的 3 個進階變體（下次開更深的課用）

1. **6 小時版**：每個 module 加「**自己改 + 課堂展示**」環節，學員當場展示自己客製化的成果
2. **2 天工作坊**：第一天照本教案走完 TimeTrace；第二天每組挑自己的真實 idea 用同套 pipeline 重跑
3. **企業內訓版**：M3 的 MCP 換成接公司內部系統（Jira / 自家 DB / 公司 wiki），其他不變

---

**完。**

> 如果你帶這份教材帶得順，學員會在 M5 結束時鼓掌；如果學員只是默默點頭，**通常是 M3 卡到、後面就沒入戲**——下次帶課時 M3 要更仔細顧。
