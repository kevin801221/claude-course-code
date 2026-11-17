<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Checkpoints 與 Rewind

Checkpoints 可以讓你儲存對話狀態，並在 Claude Code 會話中回退到之前的時間點。無論你是在探索不同方案、修復錯誤，還是比較多個實現路徑，這個能力都非常有用。

## 概覽

Checkpoints 會儲存會話狀態，讓你可以安全地試驗和探索多種方案。它們本質上是當前對話狀態的快照，包含：
- 所有已交換的訊息
- 已做出的檔案修改
- 工具使用歷史
- 當前會話上下文

當你在嘗試不同實現方式、從錯誤中恢復，或比較替代方案時，這個功能尤其好用。

## 核心概念

| 概念 | 說明 |
|---------|-------------|
| **Checkpoint** | 儲存訊息、檔案和上下文的對話快照 |
| **Rewind** | 回到之前的 checkpoint，並丟棄之後的更改 |
| **Branch Point** | 從同一個 checkpoint 出發，探索多個方案 |

## 訪問 Checkpoints

你可以透過兩種主要方式訪問和管理 checkpoints：

### 使用鍵盤快捷鍵

按兩次 `Esc`（`Esc` + `Esc`）開啟 checkpoint 介面並瀏覽已儲存的 checkpoints。

### 使用 Slash Command

使用 `/rewind` 命令（別名：`/checkpoint`、`/undo`）快速進入：

```bash
# 開啟 rewind 介面
/rewind

# 或者使用別名
/checkpoint
```

## Rewind 選項

回退時，你會看到一個包含五個選項的選單：

1. **恢復程式碼和對話** - 把檔案和訊息都恢復到那個 checkpoint
2. **恢復對話** - 只回退訊息，保留當前程式碼不變
3. **恢復程式碼** - 只回退檔案修改，保留完整對話歷史
4. **從這裡開始總結** - 把從這裡往後的對話壓縮成 AI 生成的摘要，而不是直接丟棄。原始訊息仍會保留在記錄中。你也可以額外指定摘要應聚焦哪些主題。
5. **算了** - 取消並返回當前狀態

## 自動 Checkpoints

Claude Code 會自動為你建立 checkpoints：

- **每次使用者提示** - 每次使用者輸入都會建立一個新 checkpoint
- **持久儲存** - checkpoints 隨對話一起儲存，因此恢復會話後仍可使用 `/rewind`
- **自動清理** - 30 天後自動清理舊 checkpoints

這意味著你隨時都可以回到之前的任意節點，從幾分鐘前到幾天前都可以。

## 使用場景

| 場景 | 工作流程 |
|----------|----------|
| **探索不同方案** | 儲存 → 試方案 A → 儲存 → Rewind → 試方案 B → 比較 |
| **安全重構** | 儲存 → 重構 → 測試 → 如果失敗：Rewind |
| **A/B 測試** | 儲存 → 設計 A → 儲存 → Rewind → 設計 B → 比較 |
| **錯誤恢復** | 發現問題 → Rewind 到最後一個正常狀態 |

## 如何使用 Checkpoints

### 檢視和回退

按兩次 `Esc`，或者使用 `/rewind` 開啟 checkpoint 瀏覽器。你會看到一個帶時間戳的可用 checkpoint 列表。選擇任意一個 checkpoint，即可回退到該狀態。

### Checkpoint 詳情

每個 checkpoint 會顯示：
- 建立時間
- 被修改的檔案
- 對話中的訊息數量
- 使用過的工具

## 實戰範例

更多可直接參考的中文範例見 [checkpoint-examples.md](checkpoint-examples.md)。

### 範例 1：探索不同方案

```text
User: 我們給 API 加一個快取層吧

Claude: 我會為你的 API 端點新增 Redis 快取……
[在 checkpoint A 處做出修改]

User: 其實我們先試試記憶體快取

Claude: 我會 rewind 回去，探索另一種方案……
[使用者按下 Esc+Esc 並回退到 checkpoint A]
[在 checkpoint B 處實現記憶體快取]

User: 現在我可以比較兩種方案了
```

### 範例 2：從錯誤中恢復

```text
User: 把認證模組重構成 JWT

Claude: 我會重構認證模組……
[做出大量修改]

User: 等等，這把 OAuth 整合弄壞了。我們回去。

Claude: 我來幫你回退到重構之前……
[使用者按下 Esc+Esc，並選擇重構前的 checkpoint]

User: 這次我們試一個更保守的方案
```

### 範例 3：安全試驗

```text
User: 我們試著把它改寫成函式式風格
[在實驗前建立 checkpoint]

Claude: [執行實驗性修改]

User: 測試失敗了。我們回退吧。
[使用者按下 Esc+Esc 並回退到 checkpoint]

Claude: 我已經回退這些更改了。我們試另一個方案。
```

### 範例 4：分支式探索

```text
User: 我想比較兩種資料庫設計
[記下 checkpoint，命名為 "Start"]

Claude: 我先實現第一種設計……
[實現 Schema A]

User: 現在讓我回去試第二種方案
[使用者按下 Esc+Esc 並回退到 "Start"]

Claude: 現在我實現 Schema B……
[實現 Schema B]

User: 太好了，我現在有兩個 schema 可以選擇
```

## Checkpoint 保留策略

Claude Code 會自動管理你的 checkpoints：

- 每次使用者輸入都會自動建立 checkpoint
- 舊 checkpoint 最多保留 30 天
- 系統會自動清理，避免儲存無限增長

## 工作流程模式

### 探索時的分支策略

當你在探索多個方案時：

```text
1. 從初始實現開始 → Checkpoint A
2. 嘗試方案 1 → Checkpoint B
3. 回退到 Checkpoint A
4. 嘗試方案 2 → Checkpoint C
5. 比較 B 和 C 的結果
6. 選擇最佳方案並繼續
```

### 安全重構模式

當你在做大改動時：

```text
1. 當前狀態 → Checkpoint（自動）
2. 開始重構
3. 執行測試
4. 如果測試透過 → 繼續
5. 如果測試失敗 → Rewind 並嘗試別的方案
```

## 最佳實踐

因為 checkpoints 是自動建立的，所以你可以專注於工作，而不用擔心手動儲存狀態。不過，下面這些習慣仍然很重要：

### 如何高效使用 Checkpoints

✅ **應該做：**
- 回退前先看清楚可用的 checkpoints
- 當你想嘗試不同方向時使用 rewind
- 保留 checkpoints 方便比較不同方案
- 理解每個 rewind 選項的作用（恢復程式碼和對話、恢復對話、恢復程式碼、或總結）

❌ **不要做：**
- 只依賴 checkpoints 來儲存程式碼
- 指望 checkpoints 跟蹤外部檔案系統變化
- 把 checkpoints 當成 git commit 的替代品

## 設定

你可以在設定中開啟或關閉自動 checkpoints：

```json
{
  "fileCheckpointingEnabled": true
}
```

- `fileCheckpointingEnabled`：是否在每次編輯前為檔案建立快照，以便用 `/rewind` 恢復（預設：`true`）

## 侷限性

Checkpoints 很適合會話級回退，但它不是版本控制系統。對於需要長期儲存、可審計、可共享的改動，仍然應該使用 git。

## 故障排查

### 找不到 Checkpoints

- 檢查你是否在支援該功能的 Claude Code 版本中
- 確認自動 checkpoint 沒有被關閉
- 重新開啟會話再試一次

### Rewind 失敗

- 確認你選擇了一個有效的 checkpoint
- 檢視是否存在與檔案系統或許可權相關的限制
- 嘗試先分別恢復程式碼或對話，再決定是否同時恢復兩者

## 與 Git 的整合

Checkpoints 和 git 是互補關係：

- Checkpoints 用於會話內探索和安全試驗
- Git 用於永久儲存程式碼歷史
- 你可以先用 checkpoints 快速試錯，再把最終方案提交到 git

## 快速開始

### 基本工作流程

```text
1. 開始修改前自動建立 checkpoint
2. 嘗試某個方案
3. 如果結果不理想，按 Esc 兩次
4. 選擇合適的 rewind 選項
5. 繼續探索或提交最終方案
```

### 鍵盤快捷鍵

- `Esc` + `Esc`：開啟 checkpoint 瀏覽器
- `/rewind`：透過命令進入回退介面
- `/checkpoint`、`/undo`：`/rewind` 的別名

## 什麼時候該 rewind：上下文監控

如果你發現這些訊號，通常就該回退了：

- 當前方案開始變複雜，而且你還沒確定方向
- 測試剛失敗，問題可能就是最近一兩步引入的
- 你想比較兩種實現方式
- 你想保留一個“乾淨起點”繼續探索

## 相關概念

- **Memory**：跨會話的長期上下文，見 [02-memory/README.md](../02-memory/README.md)
- **Hooks**：事件驅動自動化，見 [06-hooks/README.md](../06-hooks/README.md)
- **Plugins**：打包功能集合，見 [07-plugins/README.md](../07-plugins/README.md)
- **Advanced Features**：包括 planning mode 和背景任務，見 [09-advanced-features/README.md](../09-advanced-features/README.md)

## 更多資源

- [根目錄中文指南](../README.md)
- [Claude Code 官方檢查點文件](https://code.claude.com/docs/en/checkpointing)
- [Claude Code 高階功能指南](../09-advanced-features/README.md)

## 總結

Checkpoints 的價值在於讓你敢於試錯。它讓“先試再說”和“試錯後立刻回退”變得安全，從而幫你更快找到正確方案。

---

**最後更新**: 2026 年 10 月 18 日
**Claude Code 版本**: 2.1.302
**來源**:
- https://code.claude.com/docs/en/checkpointing
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/settings-reference
