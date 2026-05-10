---
description: 為當前 repo 建 codebase knowledge graph，並開啟 GitNexus 視覺化網站
allowed-tools: Bash(npx:*), Bash(npm:*), Bash(open:*), Bash(xdg-open:*), Bash(start:*), Bash(gitnexus:*), Bash(which:*), Bash(claude:*), Bash(uname:*), Bash(pwd), Bash(ls), Read, Glob
---

# /gitnexus — 一鍵建構 codebase 知識圖譜

請依照以下步驟，**邊做邊報告進度**給使用者：

---

## Step 1：先確認當前在哪個 repo

跑 `pwd` 確認位置。如果 cwd 不是某個專案 root（例如沒有 `.git` 或 `package.json` 之類的標誌檔），先問使用者：「你想為哪個專案建構？請給我 repo 路徑，或先 `cd` 進去再叫我。」

---

## Step 2：問使用者要哪種建構模式

**直接把以下選單顯示給使用者**，等他回應再繼續：

```
要為這個 repo 建構哪種等級的 codebase graph？

1. 🚀 快速 (Quick)
   只索引主要結構（檔案、類別、函式、import）
   時間：1-3 分鐘（依 repo 大小）
   適合：小到中型 repo / 第一次試用

2. 🔍 詳細 (Deep)
   完整索引 + dependency graph + call chains + type system
   時間：5-15 分鐘
   適合：要深度分析 / 想跟 Claude 對話 codebase

3. 🌐 完整 + Embeddings (Full)
   詳細模式 + semantic embeddings（可以用語意搜尋）
   時間：10-30 分鐘
   適合：production / 大型 repo / 想要最強體驗

請輸入 1 / 2 / 3，或直接打 quick / deep / full。
```

等使用者回應再進行 Step 3。**不要自己選**。

---

## Step 3：確認 GitNexus 已安裝

```bash
which gitnexus || npm list -g gitnexus 2>/dev/null
```

**沒裝就裝**：

```bash
npm install -g gitnexus
```

如果安裝過程很慢（>2 分鐘），告訴使用者：「Node grammar 編譯需要時間，你可以先去喝水。」並提供加速選項：

```bash
GITNEXUS_SKIP_OPTIONAL_GRAMMARS=1 npm install -g gitnexus
# 跳過 dart/proto 的原生編譯，30 秒裝完
# 但 Dart/Proto 檔案不會被 parse
```

---

## Step 4：依使用者選擇執行對應指令

| 模式 | 指令 |
|---|---|
| Quick (1) | `npx gitnexus analyze` |
| Deep (2) | `npx gitnexus analyze` （目前同 Quick，但會帶入 type system；未來版本可能拆分） |
| Full (3) | `npx gitnexus analyze --embeddings` |

**執行時**：
- 用 Bash 跑，不要丟到背景，讓使用者看到進度
- 過程中如果有 warning / error 就**翻譯成人話**給使用者
- 完成後給一個摘要：「索引了 X 個檔案、Y 個 nodes、Z 個 edges」

如果這個 repo 之前已經 analyze 過、想強制重建：加 `--force` flag。

---

## Step 5：確認 MCP 連線（讓 Claude Code 之後能查 graph）

檢查是否已註冊：

```bash
claude mcp list 2>/dev/null | grep -i gitnexus || echo "NOT_REGISTERED"
```

**沒註冊就跑**：

```bash
npx gitnexus setup
```

這會自動偵測你裝了哪些 AI editor (Claude Code / Cursor / Codex / Windsurf / OpenCode) 並一次設定好。

---

## Step 6：啟動 bridge server（讓網頁版可以連到本地 graph）

跑：

```bash
gitnexus serve &
```

（背景執行，如果使用者用 macOS 也可以 `nohup gitnexus serve > /tmp/gitnexus-serve.log 2>&1 &`）

告訴使用者：「Bridge server 已啟動，網頁會自動偵測。」

---

## Step 7：開啟視覺化網站

依作業系統開瀏覽器：

```bash
# 偵測 OS
case "$(uname -s)" in
  Darwin)  open https://gitnexus.vercel.app/ ;;
  Linux)   xdg-open https://gitnexus.vercel.app/ ;;
  *)       echo "請手動開啟 https://gitnexus.vercel.app/" ;;
esac
```

---

## Step 8：完成提示（給使用者看）

執行完成後，**用以下訊息收尾**：

```
✅ GitNexus 建構完成！

📊 已開啟視覺化網站：https://gitnexus.vercel.app/
   → 網站會自動偵測你本地的 gitnexus serve（bridge mode）
   → 你可以在網站上瀏覽 graph、查 dependency、找 call chain

💬 在 Claude Code 跟 graph 對話：
   > 用 gitnexus 看 src/auth/ 被哪些檔案 import
   > 我要重構 X 模組，列出所有受影響的測試
   > @gitnexus 找 UserService 的所有 caller

🔄 之後 commit 後想重建：
   > /gitnexus
   選同樣的模式即可（會自動 incremental update）

🛠 想停 bridge server：
   pkill -f "gitnexus serve"
```

---

## 錯誤處理

- **`npx gitnexus analyze` 跑超過 30 分鐘**：可能 repo 太大，問使用者要不要中斷改用 `--quick` 風格
- **MCP 連線失敗**：先 `claude mcp remove gitnexus` 再重跑 `gitnexus setup`
- **網頁無法偵測本地 server**：確認 `gitnexus serve` 還在跑（`ps aux | grep gitnexus`）
- **Embeddings 模式 OOM**：建議改用 `--embeddings 5000` 限制節點數
