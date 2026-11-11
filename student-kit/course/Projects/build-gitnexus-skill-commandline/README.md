# /gitnexus — 一鍵建構 codebase 知識圖譜

> 進到任何 repo，打 `claude` 啟動，輸入 `/gitnexus` —— Claude 會問你要建構哪種等級，然後幫你建好 + 自動開瀏覽器看視覺化。

```
你 → /gitnexus
Claude → 你要 quick / deep / full？
你 → 2
Claude → ✓ 確認 gitnexus 已裝
        → 跑 npx gitnexus analyze... (5 分鐘)
        → 註冊 MCP
        → 啟動 bridge server
        → 自動開啟 https://gitnexus.vercel.app/ 🌐
        → 完成！下面是建構統計 + 怎麼跟 graph 對話的範例
```

> ⚠️ **這個資料夾裡只有「**讓 Claude Code 會用 GitNexus 的 skill + slash command**」，並不是 GitNexus 本體。**先讀下面「GitNexus 是什麼」搞清楚要裝兩個東西。**

---

## GitNexus 是什麼？（先讀這段再動手）

**GitNexus** 是一個開源工具（GitHub：[`abhigyanpatwari/GitNexus`](https://github.com/abhigyanpatwari/GitNexus)），它的核心能力是：

> **把任何 codebase 解析成一張「**程式碼知識圖譜（knowledge graph）**」**——每個 file、class、function、import、call chain 都變成 graph 裡的節點與邊。

### 它解決什麼問題？

LLM 寫程式碼最大的盲點：**它看不到整個 repo 的依賴關係**。你叫它改 `UserService`，它不知道有 12 個檔案 import 這個 class、有 3 個測試會壞掉。

```
沒有 GitNexus：
  Claude → grep 找關鍵字 → 看到的是「字串配對」，會漏會錯

有 GitNexus：
  Claude → 查 graph：「誰 import UserService？」
        → graph 回：12 個檔案、5 條 call chain、3 個測試
        → Claude 知道改動的完整 blast radius
```

### 它產出什麼？

- **Knowledge graph**：節點（檔案/類別/函式）+ 邊（import/call/inherit）
- **Web UI 視覺化**：[`gitnexus.vercel.app`](https://gitnexus.vercel.app/)，可以滑鼠拖、放大、搜尋
- **MCP server**：給 Claude Code / Cursor / Codex 用的 16 種 query tool（找 caller、找循環依賴、影響分析…）
- **14 種語言支援**：TypeScript / Python / Java / C# / Go / Rust / Ruby / Swift / C / C++ / Dart / PHP / Kotlin / JavaScript

### 跟普通的 `grep` / IDE 「find references」差在哪？

| 方法 | 能找什麼 | 限制 |
|---|---|---|
| `grep` | 字串配對 | 同名變數會誤判、抓不到動態 import |
| IDE find references | 單一語言、單一 repo | 跨語言/跨 repo 失靈 |
| **GitNexus graph** | 跨語言、跨檔案的真正關係 | 第一次建 graph 要 5–30 分鐘 |

> **教學金句**：「**LLM 不是看不懂 codebase，是『看不見』。**GitNexus 是把 codebase 攤平給 LLM 看的眼鏡。」

---

## 🎤 金句牆（講課直接念、簡報直接抄）

> 把這些貼在 PPT 章節分隔頁、或寫在白板開場——學員會記得住。

### 🔹 關於「看見」

> **「沒裝 GitNexus 的 Claude 是『近視眼工程師』——看得到眼前那一行，看不到整個 repo。」**

> **「GitNexus 讓 Claude Code 從『看到字串』升級成『看到關係』——一個是讀者，一個是工程師。」**

> **「LLM 不是看不懂 codebase，是『看不見』。GitNexus 是把 codebase 攤平給 LLM 看的眼鏡。」**

> **「沒有 graph 的 LLM 是缸中之腦；有 graph 的 LLM 是有 GPS 的工程師。」**

### 🔹 關於「grep vs graph」

> **「`grep` 找的是『這個字串出現在哪』，GitNexus 找的是『這個概念跟誰有關』——一個是配對，一個是理解。」**

> **「你不會每次寫 SQL 都 sequential scan——為什麼要讓 LLM 每次都重讀整個 codebase？GitNexus 是 codebase 的 B-tree index。」**

> **「Claude Code 沒裝 GitNexus，像 IDE 沒裝 LSP——能用，但你不知道自己錯過多少。」**

### 🔹 關於「重構與安全」

> **「LLM 寫程式不會出大事是運氣好；**會**出大事的時候，永遠是它沒看到的那條 call chain。**GitNexus 就是讓它『看見』。」**

> **「重構最怕『漏改』。GitNexus 把『漏改』這件事從『不可預測』變成『可預測』——它直接列給你看誰會壞。」**

> **「『我不確定改這個會壞什麼』——這句話以後說不出口，因為 graph 直接告訴你會壞什麼。」**

### 🔹 關於「跨語言」

> **「IDE 的 find references 跨不過語言邊界——Python 呼叫 TypeScript、Go 呼叫 C，IDE 就投降了。**GitNexus 不在乎你用什麼語言，graph 是同一張。**」**

### 🔹 關於「onboarding 與生產力」

> **「Junior 上手新 repo 要兩週，LLM + GitNexus 上手新 repo 要兩分鐘——這不是取代 junior，是讓所有人一上來就是 senior 視角。」**

> **「Codebase 大到一定程度，人也記不住、LLM 也讀不完——這時你需要的不是更大的 context window，是更聰明的 index。GitNexus 就是那個 index。」**

### 🔹 一句話總結（簡報封面那種）

> **「GitNexus 給 Claude 賦予『更快抓到專案全脈絡』的能力——它不會讓模型更聰明，它讓模型看得更遠。」**

---

## 你要裝**兩個東西**（順序不能反）

```
Step 1: 先裝 GitNexus 本體                ← 真正做 graph 解析的引擎
Step 2: 再裝這個資料夾的 skill + command  ← 教 Claude Code 怎麼指揮引擎
```

### Step 1：裝 GitNexus 本體

**選項 A：npm 全域安裝（推薦，最快）**

```bash
# 需要 Node.js 18+ (建議 v20 LTS)
npm install -g gitnexus

# 驗證
gitnexus --version
```

**選項 B：git clone 跑 source（適合想看原始碼 / 想改它 / 想 contribute 的人）**

```bash
# clone 到你想放的地方
cd ~/code
git clone https://github.com/abhigyanpatwari/GitNexus.git
cd GitNexus

# 安裝依賴 + build
npm install
npm run build

# 接成全域 command（讓 `gitnexus` 指到這份 source）
npm link

# 驗證
gitnexus --version
which gitnexus    # 應該指到 ~/code/GitNexus 那邊
```

> **什麼時候要選 B**：① 你想客製化它的 parser；② 公司不允許裝全域 npm 套件；③ 你想跟著它 main branch 拿最新功能；④ 你想對它發 PR。
> **其他人選 A 就好。**

**選項 B 的好處**：之後要拉新版只要 `cd ~/code/GitNexus && git pull && npm run build`，不用重新 `npm install -g`。

### Step 1.5：第一次跑 GitNexus（驗證裝對了）

進到**任何**一個你熟的 repo 試跑：

```bash
cd ~/some-project
gitnexus analyze         # 預設快速模式，1-3 分鐘
gitnexus serve           # 啟動 bridge server 給 web UI 用
```

開瀏覽器去 `https://gitnexus.vercel.app/`，應該能看到你 repo 的 graph。看到了→ GitNexus 本體裝成功，可以進 Step 2。

> 看不到？先看本文末「疑難排解」，**不要急著裝 skill，本體沒通的話 skill 也沒用**。

### Step 2：裝這份 skill + command（讓 Claude Code 學會用 GitNexus）

往下看「兩種安裝方式」那段。

---

## 這個工具包包含什麼

```
build-gitnexus-skill-commandline/
├── README.md              ← 你正在看的這份
├── INSTALL.md             ← 怎麼安裝到你的 repo / global
├── .claude/
│   ├── commands/
│   │   └── gitnexus.md    ← /gitnexus slash command 本體
│   └── skills/
│       └── gitnexus-helper/
│           ├── SKILL.md   ← 自動觸發的 helper skill
│           └── reference/
│               └── cli-reference.md   ← gitnexus CLI 完整選項
└── examples/
    └── workflow-example.md   ← 完整使用範例（含對話紀錄）
```

---

## 兩種安裝方式（任選一個）

### 方法 A：放在「個人層」（推薦）—— 所有 repo 都能用

複製到 `~/.claude/`：

```bash
cd /Users/kevinluo/claude-code-complete-tutorial/Projects/build-gitnexus-skill-commandline

# 複製 commands
cp .claude/commands/gitnexus.md ~/.claude/commands/

# 複製 skills（整個資料夾）
cp -r .claude/skills/gitnexus-helper ~/.claude/skills/
```

之後你進**任何** repo 跑 `claude`，都能用 `/gitnexus`。

### 方法 B：放在「專案層」—— 只在這個 repo 用

複製到 `<your-repo>/.claude/`（commit 進 git，團隊共用）：

```bash
# 假設你要裝在 ~/my-project
cd ~/my-project
mkdir -p .claude/commands .claude/skills

cp /Users/kevinluo/claude-code-complete-tutorial/Projects/build-gitnexus-skill-commandline/.claude/commands/gitnexus.md \
   .claude/commands/

cp -r /Users/kevinluo/claude-code-complete-tutorial/Projects/build-gitnexus-skill-commandline/.claude/skills/gitnexus-helper \
      .claude/skills/
```

---

## 使用流程（完整版）

### 第一次

```bash
# 1. cd 到任何你想分析的 repo
cd ~/my-project

# 2. 啟動 Claude Code
claude

# 3. 在 REPL 內打：
> /gitnexus

# 4. Claude 會問你模式：
   選 1（快速）/ 2（詳細）/ 3（完整 + embeddings）

# 5. 等 Claude 跑完（會即時顯示進度）

# 6. 完成後瀏覽器自動開 https://gitnexus.vercel.app/
   你的 repo graph 已經在裡面
```

### 之後（已經建過 graph）

直接打 `/gitnexus` 一樣的流程，Claude 會自動 incremental update（不會從零重建）。

### 想跟 graph 對話（不用打開網頁）

在 Claude Code 直接問：

```
> 用 gitnexus 看 src/auth/ 被哪些檔案 import
> 我要重構 UserService，列出所有受影響的測試
> @gitnexus 找 PaymentController 的所有 caller
> 哪些 module 互相依賴形成循環？
```

Claude 會透過 MCP 查 graph，回給你結構化答案。

---

## 三種模式比較

| | Quick (1) | Deep (2) | Full (3) |
|---|---|---|---|
| **時間** | 1-3 分 | 5-15 分 | 10-30 分 |
| **內容** | 檔案 + class + function + import | + dependency / call chain / type system | + semantic embeddings |
| **適合** | 第一次試 / 小 repo | 想跟 Claude 對話 codebase | semantic search / production |
| **記憶體** | 低 | 中 | 高（embeddings 吃 RAM）|

> **建議**：第一次先選 1（quick），等覺得有用再升 3（full）。

---

## 想客製化？

### 改建構模式選項

編輯 `.claude/commands/gitnexus.md` 的 **Step 2** 段，加你自己的模式（例如「only-frontend」「only-backend」），再對應到 Step 4 的指令表。

### 改視覺化網站

如果你跑了 enterprise self-hosted 版，把 `gitnexus.md` 的 Step 7 中
`https://gitnexus.vercel.app/` 換成你內部的網址。

### 加完成通知

在 Step 8 結尾加：
```bash
osascript -e 'display notification "Graph 建好了 🎉" with title "GitNexus"'
```

---

## 疑難排解

| 症狀 | 解法 |
|---|---|
| 安裝 npm 套件超慢 | 加 `GITNEXUS_SKIP_OPTIONAL_GRAMMARS=1` |
| 網頁顯示 No connection | `gitnexus serve` 沒在跑，重跑一次 |
| MCP 連不上 | `claude mcp remove gitnexus && npx gitnexus setup` |
| `analyze` OOM | 用 `--embeddings 5000` 限制節點數 |
| Graph 過時 | `/gitnexus` 再跑一次（會 incremental update）；或直接 `gitnexus analyze --force` |

---

## 相關資源

- **GitNexus 官方 repo**：https://github.com/abhigyanpatwari/GitNexus
- **完整 CLI 文件**：見 `.claude/skills/gitnexus-helper/reference/cli-reference.md`
- **使用範例**：見 `examples/workflow-example.md`
- **A/B 測試協議（用數字證明它有沒有用）**：見 [`examples/ab-test-protocol.md`](examples/ab-test-protocol.md)
- **Claude Code 完整教學**：見 `../../Claude_Code_完整教學.pptx`
- **Claude Code 建構指南**：見 `../../Claude_Code_建構指南.md`
