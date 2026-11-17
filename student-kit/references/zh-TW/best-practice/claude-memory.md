# Claude Memory（記憶）

透過 CLAUDE.md 檔案提供持久脈絡 —— 怎麼寫，以及在 monorepo 中怎麼載入。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`best-practice/claude-memory.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-memory.md)

---

## 1. 寫出好的 CLAUDE.md

結構良好的 CLAUDE.md 是改善 Claude Code 在你專案上表現最有效的單一手段。Humanlayer 有一篇很棒的指南，涵蓋該放什麼、怎麼組織，以及常見的陷阱。

- [Humanlayer - Writing a good Claude.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

---

## 2. 大型 Monorepo 中的 CLAUDE.md

在 monorepo 中使用 Claude Code 時，理解 CLAUDE.md 如何被載入脈絡，是有效組織專案指令的關鍵。

<p align="center">
  <a href="https://x.com/bcherny/status/2016339448863355206"><img src="../best-practice/assets/claude-memory/claude-memory-monorepo.jpg" alt="monorepo 中的 CLAUDE.md 載入機制" width="600"></a>
</p>

### 兩種載入機制

Claude Code 用兩種不同機制載入 CLAUDE.md：

#### 祖先載入（往目錄樹**上**走）

啟動 Claude Code 時，它會從當前工作目錄**往上**走到檔案系統根目錄，載入沿途找到的每一個 CLAUDE.md。這些檔案在**啟動當下立即載入**。

#### 後代載入（往目錄樹**下**走）

位於當前工作目錄底下子目錄中的 CLAUDE.md **不會在啟動時載入**。它們只有在 session 中 Claude 讀取那些子目錄的檔案時才會被納入。這就是所謂的**延遲載入（lazy loading）**。

### Monorepo 結構範例

想像一個典型的 monorepo，不同元件分在不同目錄：

```
/mymonorepo/
├── CLAUDE.md          # 根層級指令（所有元件共用）
├── frontend/
│   └── CLAUDE.md      # 前端專屬指令
├── backend/
│   └── CLAUDE.md      # 後端專屬指令
└── api/
    └── CLAUDE.md      # API 專屬指令
```

### 情境 1：從根目錄啟動 Claude Code

當你在 `/mymonorepo/` 執行 Claude Code：

```bash
cd /mymonorepo
claude
```

| 檔案 | 啟動時載入？ | 原因 |
|------|-------------------|--------|
| `/mymonorepo/CLAUDE.md` | 是 | 它就是你的當前工作目錄 |
| `/mymonorepo/frontend/CLAUDE.md` | 否 | 只有在你讀／編輯 `frontend/` 裡的檔案時才載入 |
| `/mymonorepo/backend/CLAUDE.md` | 否 | 只有在你讀／編輯 `backend/` 裡的檔案時才載入 |
| `/mymonorepo/api/CLAUDE.md` | 否 | 只有在你讀／編輯 `api/` 裡的檔案時才載入 |

### 情境 2：從元件目錄啟動 Claude Code

當你在 `/mymonorepo/frontend/` 執行 Claude Code：

```bash
cd /mymonorepo/frontend
claude
```

| 檔案 | 啟動時載入？ | 原因 |
|------|-------------------|--------|
| `/mymonorepo/CLAUDE.md` | 是 | 它是祖先目錄 |
| `/mymonorepo/frontend/CLAUDE.md` | 是 | 它就是你的當前工作目錄 |
| `/mymonorepo/backend/CLAUDE.md` | 否 | 位於目錄樹的另一個分支 |
| `/mymonorepo/api/CLAUDE.md` | 否 | 位於目錄樹的另一個分支 |

### 重點整理

1. **祖先一律在啟動時載入** —— Claude 往目錄樹上走，載入找到的所有 CLAUDE.md。這確保你永遠能取得根層級、整個 repo 適用的指令。

2. **後代延遲載入** —— 子目錄的 CLAUDE.md 只有在你操作該子目錄的檔案時才載入。這能避免不相關的脈絡把 session 撐爆。

3. **兄弟目錄永遠不載入** —— 如果你在 `frontend/` 工作，`backend/CLAUDE.md` 或 `api/CLAUDE.md` 不會進入脈絡。

4. **全域 CLAUDE.md** —— 你也可以在家目錄放 `~/.claude/CLAUDE.md`，它會套用到**所有** Claude Code session，不分專案。

### 這個設計為什麼適合 Monorepo

- **共用指令會向下傳播** —— 根層級 CLAUDE.md 放整個 repo 適用的慣例、程式碼標準與共通模式。

- **元件專屬指令保持隔離** —— 前端開發者不需要後端專屬指令來塞爆脈絡，反之亦然。

- **脈絡經過最佳化** —— 透過延遲載入後代 CLAUDE.md，Claude Code 避免在啟動時載入可能高達數百 KB 的無關指令。

### 最佳實踐

1. **共用慣例放根層級 CLAUDE.md** —— 程式碼標準、commit 訊息格式、PR 範本，以及其他整個 repo 適用的準則。

2. **元件專屬指令放元件層級 CLAUDE.md** —— 框架專屬模式、元件架構、該元件獨有的測試慣例。

3. **個人偏好用 CLAUDE.local.md** —— 把它加進 `.gitignore`，放那些不該分享給團隊的指令。

---

## 資料來源

- [Claude Code Documentation - How Claude Looks Up Memories](https://code.claude.com/docs/en/memory#how-claude-looks-up-memories)
- [Boris Cherny on X - Clarification on CLAUDE.md Loading](https://x.com/bcherny/status/2016339448863355206)
- [Humanlayer - Writing a good Claude.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
