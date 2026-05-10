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
- **Claude Code 完整教學**：見 `../../Claude_Code_完整教學.pptx`
- **Claude Code 建構指南**：見 `../../Claude_Code_建構指南.md`
