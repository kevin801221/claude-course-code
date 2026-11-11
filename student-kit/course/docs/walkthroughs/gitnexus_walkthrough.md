# GitNexus Walkthrough — 讓 AI 真的「看懂整個 codebase 架構」

> **對象**：用過 Claude Code 基礎、受夠「AI 改一個 function 不知道 47 個地方在 call 它」的工程師
> **形式**：講師現場帶 / 自學
> **時長**：75 分鐘
> **產出**：能把任何 repo 一鍵建成 knowledge graph，用 16 個 MCP tool 做「改之前先算爆炸半徑」「沿 call chain 追 bug」「跨檔安全 rename」「跨 repo 契約檢查」
> **核心方法**：先讓 AI 在「沒有架構知識」下改壞一段 code（故意踩坑）→ 建 graph → 同一題用 `impact` / `context` 工具，當場看它秒答出剛剛漏掉的依賴
> **跟現有教材的關係**：本 repo 已有 [`Projects/build-gitnexus-skill-commandline/`](../../Projects/build-gitnexus-skill-commandline/README.md)——那份教「**怎麼把 gitnexus 包成 `/gitnexus` 一鍵指令**」；**這份教「gitnexus 這個工具本身怎麼運作、16 個 MCP tool 怎麼用、能解什麼真實問題」**。兩份分工：要 demo 一鍵體驗看 Project，要懂原理跟工具看這份。課程位置：**Part 10 MCP 的進階應用** ＋ **Part 16 進階主題**。

---

## 開場（5 分鐘）：為什麼 AI 改 code 老是改壞？

AI coding 助手最大的盲點不是「不會寫」，是「**沒有架構意識**」。你叫它改一個 function 的回傳型別，它改了——但它不知道有 47 個地方依賴這個型別，於是悄悄弄壞了一片。

它為什麼會這樣？因為它只能**邊讀邊猜**：開幾個檔、grep 幾個字、推測關係。檔一多就漏。

| 做法 | AI 怎麼拿到「誰呼叫誰」 | 問題 |
|---|---|---|
| 純 LLM（grep + 讀檔） | 現場一個個探索 | 檔多必漏，越大越不準 |
| RAG（向量檢索片段） | 找「字面像」的片段 | 找得到相似的，找不到「誰真的 call 誰」 |
| **GitNexus（knowledge graph）** | **建 graph 時就把依賴算完**，查詢一次回完整 | 一次查詢拿到完整爆炸半徑 |

> **教學金句**：「RAG 是『找出長得像的片段』，knowledge graph 是『早就把誰依賴誰算清楚了』——前者像關鍵字搜尋，後者像有人先幫你畫好整張架構圖。」

GitNexus 做的事：**索引時就把整個 codebase 算成一張圖**（誰呼叫誰、誰繼承誰、誰屬於哪個模組、哪條執行流程經過哪些 function），再透過 16 個 MCP tool 餵給 Claude。Claude 不用再瞎猜。

---

## 📁 GitNexus 的心智模型（一張圖看懂）

```
你的 repo
  │
  │  npx gitnexus analyze   ← 6 階段 pipeline
  ▼
┌─────────────── Knowledge Graph ───────────────┐
│  節點 = 符號（function / class / method）       │
│  邊   = 關係：CALLS / IMPORTS / EXTENDS /       │
│              IMPLEMENTS / MEMBER_OF             │
│  每條邊有 confidence 分數 (0.0–1.0)             │
│  自動偵測「執行流程」(LoginFlow / 結帳流程…)     │
│  Leiden 演算法把相關符號分群成 community         │
└────────────────────────────────────────────────┘
  │                                  │
  │  gitnexus mcp (stdio)            │  gitnexus serve
  ▼                                  ▼
Claude Code / Cursor / Codex     瀏覽器視覺化
  ← 16 個 MCP tool 查圖            gitnexus.vercel.app (WebGL)
```

**兩種跑法**：
1. **CLI + MCP**（主力）：本機 `analyze` 建圖，跑 `mcp` 當 server 餵給 AI agent
2. **Web UI**：瀏覽器版（WASM），免 server，看視覺化，但受瀏覽器記憶體限制（~5k 檔）

---

## 🔌 Phase 0：環境準備（5 分鐘）

```bash
# 1. 全域安裝（Node.js 環境）
npm install -g gitnexus

# 2. 進到你要分析的 repo 根目錄
cd ~/your-project

# 3. 接到 Claude Code（macOS / Linux）
claude mcp add gitnexus -- npx -y gitnexus@latest mcp
#   Windows 要包 cmd /c：
#   claude mcp add gitnexus -- cmd /c npx -y gitnexus@latest mcp
```

> 💡 **教學現場省事招**：本 repo 已有 [`/gitnexus`](../../Projects/build-gitnexus-skill-commandline/README.md) 一鍵指令，把上面三步包成一個 slash command。**Part 10 帶課時先用 `/gitnexus` 給體感，這份 walkthrough 再拆開講背後在跑什麼。**

> ⚠️ `npx gitnexus` 第一次會下載 Tree-sitter / LadybugDB 原生套件，**前一晚先在示範 repo 跑過一次**，不要當場第一次跑等下載。

---

## 🧠 Phase 1：建第一個 graph ⭐ 最詳細——`analyze` 在做什麼

```bash
# 從 repo 根目錄跑（這就是建圖）
npx gitnexus analyze

# 常用變體
npx gitnexus analyze --force            # 強制全量重建
npx gitnexus analyze --skills           # 順便產生 repo 專屬 skills
npx gitnexus analyze --skip-embeddings  # 跳過 embedding，求快
```

`analyze` 不是隨便掃一掃——它跑 **6 階段 pipeline**，這是這個工具的精華，帶課一定要拆給學員看：

| # | 階段 | 在做什麼 | 為什麼需要 |
|---|---|---|---|
| 1 | **Structure** | 走檔案樹，建資料夾/檔案關係 | 先有骨架 |
| 2 | **Parsing** | Tree-sitter 抽 function / class / method | 拿到「符號」這層 |
| 3 | **Resolution** | 解析 import、call、繼承、constructor、`self`/`this` 接收者 | **這步決定準不準**——「A 真的 call B」要解析才知道 |
| 4 | **Clustering** | Leiden 社群偵測，把相關符號分群 | 自動找出「這是認證模組」「這是金流模組」 |
| 5 | **Processes** | 從進入點（main / HTTP handler / constructor）往下追 call chain | 產出「LoginFlow」這種**有名字的執行流程** |
| 6 | **Search** | 建 BM25 + semantic 混合索引 | 查詢時又快又準 |

> **教學金句**：「`analyze` 最關鍵的是第 3 步 Resolution——RAG 跳過這步所以只會『找相似』；GitNexus 做這步，所以能回答『誰真的呼叫了它』。」

跑完你會得到一張圖：**節點是符號、邊是關係**。每種邊有意義、每條邊有 `confidence`：

| 邊型別 | 意思 |
|---|---|
| `CALLS` | function/method 呼叫 |
| `IMPORTS` | 模組依賴 |
| `EXTENDS` / `IMPLEMENTS` | 類別繼承 / 介面實作 |
| `MEMBER_OF` | 這個符號屬於哪個 community（模組群） |

> 💡 `confidence`（0.0–1.0）= 解析的確定度。動態語言（Python/JS）的某些 call 解析不到 100%，查詢時可以用 `minConfidence` 過濾雜訊——這是進階技巧，學員問再講。

**支援 14 種語言**（TS/JS/Python/Java/Kotlin/C#/Go/Rust/PHP/Ruby/Swift/C/C++/Dart），且懂框架慣例（Rails / Spring / Django / Express 的路由與 handler）。

---

## 🛠 Phase 2：16 個 MCP Tool（按「你想幹嘛」分群記）

別叫學員背 16 個工具名。按**意圖**分四群就記得住：

### 群 A：搞懂這份 code（探索）

| Tool | 你問的問題 | 回什麼 |
|---|---|---|
| `list_repos` | 我索引過哪些 repo？ | 清單 |
| `query({query})` | 「登入流程在哪？」 | 符號**依執行流程分組**回（不是一堆散檔） |
| `context({name})` | 「`createUser` 這函式 360 度長怎樣？」 | 定義 + 誰呼叫它 + 它呼叫誰 + 參與哪些流程 |

### 群 B：改之前先算風險（影響分析）⭐ 最殺的賣點

| Tool | 你問的問題 | 回什麼 |
|---|---|---|
| `impact({target, direction})` | 「我改這個會炸到誰？」 | **爆炸半徑**：upstream/downstream 依賴，按深度分層 |
| `detect_changes({scope:"staged"})` | 「我這次 commit 動到哪些流程？」 | 把 git diff 的行對到受影響的執行流程（**commit 前跑**） |

### 群 C：安全改（重構）

| Tool | 你問的問題 | 回什麼 |
|---|---|---|
| `rename({symbol_name, new_name, dry_run:true})` | 「把這個改名，跨檔幫我對齊」 | graph + 文字雙重比對的改名清單，`dry_run` 先看不動手 |

### 群 D：進階 / 跨 repo

| Tool | 用途 |
|---|---|
| `cypher({query})` | 直接對圖下 Cypher，做任意 pattern 比對 |
| `group_list` / `group_sync` / `group_contracts` / `group_query` / `group_status` | **多 repo**：抽契約、跨 repo 比對、跨服務查執行流程 |

> **教學金句**：「`impact` 是 GitNexus 的招牌——『改這行會炸到誰』這個問題，純 LLM 永遠在賭，GitNexus 是用算的。」

也有 MCP resources（`gitnexus://repo/{name}/processes`、`/clusters`、`/schema`）讓 AI 自己拿圖的 schema 來組 Cypher。

---

## 📝 Phase 3：四個真實應用劇本（這段最有共鳴）

帶課時不要逐工具講，講「**遇到什麼情境用哪招**」：

### 劇本 1：改 API 前先算爆炸半徑

```
你：我想把 getUserProfile 的回傳改成包 email
Claude（接 gitnexus）：先 impact({target:"getUserProfile", direction:"upstream"})
  → 回：12 個 caller，跨 3 個 community，其中 2 個 confidence 0.6（要人工確認）
你：先看那 12 個再決定
```
**價值**：把「改完才發現炸了」變成「改之前就知道會炸哪」。

### 劇本 2：沿 call chain 追 bug

```
你：登入有時候會 500，幫我追
Claude：query({query:"login flow"}) → 拿到 LoginFlow 的完整 call chain
  → context({name:"verifyToken"}) → 看到它 call 了一個 confidence 低的外部解析
```
**價值**：不是 grep "login"，是**沿著真實執行流程**走。

### 劇本 3：安全 rename

```
你：把 calc_tax 改名 compute_tax
Claude：rename({symbol_name:"calc_tax", new_name:"compute_tax", dry_run:true})
  → 列出 8 處（6 處 graph 高信心、2 處字串疑似），你確認再 dry_run:false
```
**價值**：跨檔改名不靠「全域取代」賭運氣。

### 劇本 4：跨 repo 契約檢查（微服務）

```
group_sync → 抽出 service-A 對外契約
group_query({query:"checkout flow"}) → 跨 3 個 repo 追同一條結帳流程
```
**價值**：單 repo 工具看不到的「服務間斷掉的契約」。

加碼：`gitnexus wiki` 用圖生出文件、`gitnexus analyze --skills` 產 repo 專屬 skill（描述每個功能區的進入點與流程）。

---

## 整合 demo：一條龍跑完（10 分鐘現場）

```bash
cd ~/demo-repo
npx gitnexus analyze                              # ① 建圖（前一晚先跑過）
claude
> 用 gitnexus 找出這個 repo 的主要執行流程         # ② query
> getUserProfile 這個函式的 360 度關係            # ③ context
> 我想改它的回傳值，先算 upstream 影響            # ④ impact
> 把它改名成 fetchUserProfile，先 dry run        # ⑤ rename dry_run
> 我 stage 了一些改動，這次 commit 動到哪些流程？  # ⑥ detect_changes
```

跑完學員就懂：**①建圖一次 → ②③④⑤⑥ 都是查同一張圖**，不是每次重新探索。

---

## 常見問題 / FAQ

**Q：跟 RAG / embedding 檢索差在哪？**
A：RAG 找「字面/語意相似的片段」，回答不了「誰真的 call 誰」。GitNexus 在 `analyze` 時就把關係算成圖，`impact` 這種問題是用圖算的、不是猜的。

**Q：跟 LSP（語言伺服器）差在哪？**
A：LSP 是單檔/即時、跟著編輯器。GitNexus 是**全 repo 預先算好整張關係圖 + 跨 repo + 餵給 AI agent**，定位不同。

**Q：要一直重新 analyze 嗎？**
A：目前**不支援增量索引**，所有分析都基於完整索引。改動大就 `--force` 重建。這是已知限制。

**Q：大 repo 跑得動嗎？**
A：CLI 模式靠 worker threads，可以撐大 repo。**Web UI 受瀏覽器記憶體限制（~5k 檔）**，超過要用 backend 模式。

**Q：免費嗎？**
A：開源 CLI/MCP 免費。另有商用 SaaS（akonlabs.com）多了 PR review、自動重索引、多 repo 統一圖等。

---

## 卡點對照表 ⭐（真的會踩，不是想像的）

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `analyze` 卡在某個檔 timeout | 大檔/奇怪檔案 worker 超時 | `--worker-timeout 60` 或設 `GITNEXUS_WORKER_SUB_BATCH_TIMEOUT_MS` |
| Dart / Proto 解析報錯 | 選用 grammar 需要 C++ toolchain | `export GITNEXUS_SKIP_OPTIONAL_GRAMMARS=1` 跳過 |
| MCP 接上但 Claude 收不到 | server 的 log 印到 stdout 汙染 stdio | gitnexus 自身沒問題，但**自寫 MCP 同理**：log 一律走 stderr |
| 改了 code 但查詢結果還是舊的 | 沒重新 analyze（不支援增量） | `npx gitnexus analyze --force` |
| Web UI 開超大 repo 卡死 | 瀏覽器記憶體 ~5k 檔上限 | 改用 CLI + MCP（backend）模式 |
| `impact` 結果一堆雜訊 | 動態語言低 confidence 邊 | 查詢加 `minConfidence: 0.8` 過濾 |
| 第一次 `npx` 等很久 | 下載原生 binding | 前一晚先跑過、別現場第一次跑 |

---

## 講師私房筆記

### 教學順序心法

- **先用 `/gitnexus` 給體感（Part 10），再用這份拆原理（Part 16）**。順序反了學員會被 6 階段 pipeline 嚇到。
- Phase 1 的 6 階段表是這堂的脊椎——**花 10 分鐘講透「第 3 步 Resolution 才是跟 RAG 的分水嶺」**，其他階段帶過。
- Phase 3 四劇本比 Phase 2 工具表重要。學員記得住「改之前先 impact」，記不住 16 個工具名。

### 故意踩坑（比口頭講有效）

- **開場**：先不開 gitnexus，叫 Claude「把 `getX` 回傳值加個欄位」，它改完很開心 → 再問「有幾個地方 call 它你查過嗎？」它支吾 → **這時才 analyze + impact**，當場列出 12 個 caller。痛點瞬間具體化。
- **rename**：故意先 `dry_run:false` 直接改（嚇一下）再退回講「永遠先 `dry_run:true`」。

### 不同學員角色推薦

| 角色 | 對哪段最有共鳴 | 給他的建議 |
|---|---|---|
| 接手舊專案的工程師 | Phase 3 劇本 1/2 | 進新 repo 第一件事先 `analyze` 再問 query |
| 做微服務的後端 | Phase 2 群 D | `group_*` 跨 repo 契約檢查 |
| Tech Lead / Reviewer | `detect_changes` | 接 pre-commit / PR，自動標「這次動到哪些流程」 |
| 重構控 | `impact` + `rename` | 重構前先算爆炸半徑，別憑感覺 |

### Kevin 親自驗證的真實狀況

- ✅ `/gitnexus` 一鍵指令我自己包過，本 repo `Projects/build-gitnexus-skill-commandline/` 就是。
- ✅ 本 session 的 `mcp__gitnexus__*` 工具就是這套 MCP 接上來的——是真的可用，不是 paper。
- ⚠️ 「不支援增量索引」這條最容易讓學員誤會「為什麼我改完它沒變」——務必講清楚要 `--force`。
- ⚠️ 大 repo 第一次 `analyze` 可能數分鐘，**現場 demo 一定要用已 analyze 過的 repo**，或前一晚先跑。

---

## 一句話總結

> **GitNexus = 在 AI 改你的 code 之前，先把「誰依賴誰」算成一張圖。RAG 找相似、LSP 管單檔，它管的是「全 repo 架構意識」——招牌是 `impact`：改這行會炸到誰，用算的不用賭。**

---

## 進階閱讀

- 🔗 [`Projects/build-gitnexus-skill-commandline/README.md`](../../Projects/build-gitnexus-skill-commandline/README.md) — 把 gitnexus 包成 `/gitnexus` 一鍵指令（體感版，先看這個）
- 🔗 [`Projects/build-gitnexus-skill-commandline/examples/workflow-example.md`](../../Projects/build-gitnexus-skill-commandline/examples/workflow-example.md) — 完整對話紀錄範例
- 🔗 GitHub: `github.com/abhigyanpatwari/GitNexus` — 上游原始碼
- 🔗 Web UI: `gitnexus.vercel.app` — 免安裝瀏覽器視覺化
- 🔗 [`hook_walkthrough.md`](hook_walkthrough.md) — 把 `detect_changes` 接 pre-commit hook 的延伸玩法

---

_Last updated: 2026-05-16_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材（同目錄）：karpathy_skills_walkthrough.md、hook_walkthrough.md、course_12hr_walkthrough.md_
_專案實戰：[../../Projects/build-gitnexus-skill-commandline/README.md](../../Projects/build-gitnexus-skill-commandline/README.md)_
_對應 PPT：Part 10 MCP（應用）＋ Part 16 進階主題_
