# GitNexus CLI Reference (整理自 v1.x)

## 安裝

```bash
# 標準安裝
npm install -g gitnexus

# 跳過原生 grammar 編譯（快很多，但少了 dart/proto 支援）
GITNEXUS_SKIP_OPTIONAL_GRAMMARS=1 npm install -g gitnexus
```

## 主要指令

### `gitnexus analyze [path]`
索引 repo 成 knowledge graph。

| Flag | 用途 |
|---|---|
| `-f, --force` | 強制重建（即使已是最新版） |
| `--embeddings [limit]` | 啟用 semantic embeddings（預設關）；`[limit]` 限制節點數，`0` = 無限 |
| `--drop-embeddings` | 重建時順便刪掉舊 embeddings |

**預設行為**：增量更新（只 reparse 改動過的檔案）。

### `gitnexus setup`
自動偵測你裝了哪些 AI editor，幫你寫 MCP config（global 設定）。

**支援的 editor**：
- Claude Code（Full：MCP + Skills + Hooks）
- Cursor（MCP + Skills）
- Codex（MCP + Skills）
- Windsurf（MCP）
- OpenCode（MCP + Skills）

### `gitnexus serve`
Bridge mode — 讓網頁版（gitnexus.vercel.app）自動偵測你本地的 graph。

```bash
gitnexus serve              # foreground
gitnexus serve &            # background
nohup gitnexus serve > /tmp/gn.log 2>&1 &   # 完全 detach
```

### `gitnexus status`
看當前 repo 的 index 狀態（檔案數、node 數、最後更新時間）。

### `gitnexus list`
列出所有已 index 過的 repo（在你電腦上）。

### `gitnexus clean`
清除特定 repo 的 index。

| Flag | 用途 |
|---|---|
| `-f, --force` | 跳過確認 |
| `--all` | 清掉所有 repo |

### `gitnexus remove [path]`
從 registry 移除某個 repo（不刪 graph 檔，只取消註冊）。

### `gitnexus doctor`
診斷工具：node 版本、依賴、MCP 連線、graph 完整性。

### `gitnexus wiki`
產生 codebase wiki 文件。

| Flag | 用途 |
|---|---|
| `-f, --force` | 強制重產 |
| `--provider <name>` | LLM provider: `openai` / `cursor` |
| `--model <name>` | 指定模型 |

### `gitnexus mcp`
啟動 MCP server（給 AI editor 連的）。通常透過 `gitnexus setup` 設好就會自動跑，不用手動呼叫。

### `gitnexus publish`
發佈到 cloud（enterprise 功能）。

## 環境變數

| 變數 | 用途 |
|---|---|
| `GITNEXUS_SKIP_OPTIONAL_GRAMMARS=1` | 安裝時跳過 dart/proto 原生編譯 |
| `GITNEXUS_EMBEDDING_THREADS=N` | 限制本地 ONNX CPU threads |
| `GITNEXUS_SEMANTIC_EXACT_SCAN_LIMIT=N` | 語意 exact-scan fallback 上限（預設 10000）|

## .gitnexusignore

支援 `.gitignore` 風格，可以用 `!pattern` 反向 include。

範例：
```
node_modules/
dist/
*.test.ts
!critical/*.test.ts   # 但這個 critical 的測試還是要 index
```

## 常見問題

**Q: 第一次裝很慢怎辦？**
A: 用 `GITNEXUS_SKIP_OPTIONAL_GRAMMARS=1` 跳過原生 build。

**Q: graph 怎麼存？**
A: 用 LadybugDB（CLI 版是 native，web 版是 WASM）。檔案存在 `~/.gitnexus/`。

**Q: 隱私？**
A: CLI 完全 local，no network。Web 版完全在 browser 跑，no server。

**Q: enterprise vs OSS 差別？**
A: enterprise 有 PR review、auto-update wiki、auto-reindex、multi-repo。OSS 含基本 wiki + analyze + serve。
