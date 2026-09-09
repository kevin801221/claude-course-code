---
name: drafting-weekly-reports
description: |
  Drafts weekly status reports by aggregating GitHub commits, issues,
  and PRs into a structured markdown report for non-technical readers.
  Use when user mentions: "週報", "weekly report", "本週進度", "team
  update", "週五要交的", "review 這週 commits", or asks to summarize
  recent git activity.
---

# 撰寫每週工作報告 (Drafting Weekly Reports)

> ⚠️ 給 AI 的閱讀提示：這份 skill 給的是**心法**，不是步驟。
> 任何模糊地帶請依「核心原則」自行判斷，不要硬問。

---

## 為什麼要做這件事 (Why)

每週要產出給**非技術主管 / 客戶 / 跨部門同事**的進度報告。
這些讀者：
- **不關心**程式技術細節（不要寫 `Refactored AuthMiddleware.parseToken()` 這種）
- **關心**業務影響（用戶能不能登入了？bug 修了嗎？新功能上線了嗎？）
- **時間有限**，預期 2 分鐘看完

報告失敗 = 讀者覺得你「這週沒做什麼」（其實你做了，只是沒翻譯成他們的語言）。

---

## 抱持什麼心態 (Attitude)

你是**翻譯官**，不是 git log dumper。

- **過濾優先於完整**：100 個 commit 翻成 5 個重點，不是 100 個 bullet
- **影響優先於動作**：「修了 N+1 query」→ 寫成「優化 dashboard 載入速度從 3 秒 → 0.5 秒」
- **使用者語言優先於工程術語**：「deploy」→「上線」、「PR」→「功能更新」、「refactor」→「內部優化（使用者無感）」
- **誠實優先於漂亮**：這週沒做啥就誠實寫「下週重點」，不要硬湊 commit 充數

---

## 核心原則 (Guiding Principles)

遇到模糊地帶，依下列優先順序判斷：

1. **「主管會在意這件事嗎？」** — 不會 → 不寫
2. **「客戶會被這個功能影響嗎？」** — 不會 → 歸到「內部優化」一句帶過
3. **「這個 commit message 講人話嗎？」** — 不講 → 看 PR description / 看 diff 重新總結
4. **「沒寫 = 沒做嗎？」** — 是 → 加「進行中 / 下週完成」段落補上
5. **「會議、會談、決策呢？」** — git 看不到 → 主動問使用者「這週有什麼重要的非 commit 工作？」

---

## 工作流程 (Workflow)

### Step 1：收集資料

**用 `scripts/fetch_commits.sh`** 撈 commits（不要自己用 git log，script 處理好 author / 日期 / 格式）。

```bash
bash .claude/skills/drafting-weekly-reports/scripts/fetch_commits.sh \
  --since "7 days ago" --author "$(git config user.email)"
```

如果使用者要包含 PR / issue：
```bash
bash .claude/skills/drafting-weekly-reports/scripts/fetch_commits.sh \
  --include-prs --include-issues
```

### Step 2：分類

**用 `scripts/classify_commits.py`** 把 commits 自動分類成：
- ✨ 新功能 (feat)
- 🐛 Bug 修復 (fix)
- ♻️ 重構 / 內部優化 (refactor / chore / perf)
- 📚 文件 / 測試 (docs / test)

```bash
python3 .claude/skills/drafting-weekly-reports/scripts/classify_commits.py \
  --input /tmp/commits.json
```

如果分類看起來不對，**不要硬調** — 你的判斷比正則更好，自己重新分類。

### Step 3：翻譯成使用者語言

對每個分類，把工程術語翻成業務語言。
參考 `references/output-template.md` 的範例對照。

### Step 4：套版輸出

依照 `references/output-template.md` 的格式產出 markdown。
**不要自創格式** — 主管習慣某個格式很重要。

### Step 5：自我檢查

對照 `references/anti-patterns.md`，確認沒踩到任何反例。

---

## 何時要主動問使用者

不要悶頭做完才發現方向錯。下列情境**先問**：

- 這週 commits < 3 個 → 「這週是不是有非 commit 的重要工作？會議？決策？」
- 看到 commits 都在某個 feature branch → 「這個 feature 上線了嗎？要在週報提嗎？」
- 不確定讀者層級 → 「這份是要給工程主管、產品主管還是 CEO？」

---

## 輸出長度限制

- **總長度：500 字內**（讀者 2 分鐘看完）
- **每個分類：3-5 個 bullet 最多**
- **每個 bullet：1 行寫完，不要跨行說明**

如果 commits 太多 → 合併同主題、刪重複、保留最重要的 5 個。

---

## 詳細參考

- 完整輸出範本 + 翻譯對照表：`references/output-template.md`
- 給不同角色的語氣指南：`references/tone-guide.md`
- 反例（什麼絕對不能寫）：`references/anti-patterns.md`
- 好的範例輸出：`examples/good-output.md`
- 壞的範例（教學用）：`examples/bad-output.md`
