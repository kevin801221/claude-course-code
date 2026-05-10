# 完整使用流程範例（含真實對話）

> 假設你進到一個 React + Express 的 monorepo，第一次想用 GitNexus

## 場景

```
~/projects/my-saas/
├── frontend/   (React + TypeScript)
├── backend/    (Express + Prisma)
└── shared/     (共用 type)
```

你想：
1. 看 codebase 整體架構
2. 之後跟 Claude 對話時，它能精準回答「X 被誰用到」這種問題
3. 想可視化看一下 dependency 圖

## 步驟（真實對話）

### 1. cd 進 repo + 啟動 Claude

```bash
cd ~/projects/my-saas
claude
```

### 2. 觸發 /gitnexus

```
> /gitnexus
```

### 3. Claude 開始問你

```
Claude:
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

### 4. 你選 2

```
> 2
```

### 5. Claude 開始執行（你會即時看到輸出）

```
Claude:
✓ 確認當前資料夾：~/projects/my-saas
✓ 檢查 gitnexus...
   找到了：v1.x.x

正在執行 npx gitnexus analyze...

[gitnexus] Indexing 234 TypeScript files...
[gitnexus] Building dependency graph...
[gitnexus] Resolving type system... (this takes a moment)
[gitnexus] Done in 7m 23s
[gitnexus] Indexed: 234 files, 1,892 nodes, 5,617 edges

✓ 索引完成！
✓ 確認 MCP 連線...
   未連線，正在跑 npx gitnexus setup...
   ✓ Claude Code: configured
   ✓ Cursor: configured (順便)
✓ 啟動 bridge server (背景)...
   PID: 87432
✓ 開啟視覺化網站...
```

### 6. 瀏覽器自動開了 https://gitnexus.vercel.app/

網站偵測到你本地的 `gitnexus serve`，列出剛剛的 my-saas repo，
你點進去看到完整的 graph：
- 中間是 frontend / backend / shared 三大叢集
- 連線顯示哪些檔案 import 哪些
- 你發現 `frontend/components/Auth.tsx` 直接 import 了 `backend/services/db.ts`
  → 違反了 monorepo 規範！這是個 bug

### 7. Claude 給你結尾訊息

```
Claude:
✅ GitNexus 建構完成！

📊 已開啟視覺化網站：https://gitnexus.vercel.app/
   → 網站會自動偵測你本地的 gitnexus serve
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

### 8. 接著你開始問 Claude（不用切視窗）

```
> @gitnexus 找出所有 frontend/ 直接 import backend/ 的檔案

Claude:
查到 3 個違反規範的 import：

| Frontend 檔案 | 違規 import |
|---|---|
| frontend/components/Auth.tsx | backend/services/db.ts |
| frontend/utils/email.ts | backend/lib/sendgrid.ts |
| frontend/hooks/useUser.ts | backend/types/User.ts |

建議：
- Auth.tsx → 改用 backend 暴露的 API
- email.ts → 移到 shared/ 或建 frontend/services/
- useUser.ts 的 type 應該移到 shared/types/

要我幫你開始修嗎？

> 好，從最簡單的 useUser.ts 開始

Claude:
[執行 refactor]
[跑測試]
[commit]
✓ 完成。useUser.ts 改 import shared/types/User.ts，已 commit。
```

## 隔天再進來

```bash
cd ~/projects/my-saas
claude
```

```
> @gitnexus 昨天我重構了 useUser.ts，現在還有哪些檔案違規？
```

Claude 會用 graph 即時查（graph 已經 stale 但 hooks 會偵測，提醒你重跑或自動 incremental update）。

---

## 觀察重點

從這個範例看到 GitNexus + Claude Code 的威力：

1. **發現結構問題**：靠 graph 視覺化看出 frontend → backend 的違規 import
2. **精準回答問題**：「找出所有 X」這種問題，graph 比 grep 準
3. **影響範圍分析**：「我要改 X，誰會壞」graph 直接告訴你
4. **架構級重構**：不再是「改一個檔忘記改另外 5 個」
