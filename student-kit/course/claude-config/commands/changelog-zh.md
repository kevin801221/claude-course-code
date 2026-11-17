---
description: 依 git log 自動更新 CHANGELOG.md（繁體中文，分類歸納）
argument-hint: <since-tag-or-date>（選填，預設最近 30 天）
allowed-tools: Read, Write, Edit, Bash(git log:*), Bash(git tag:*), Bash(date:*)
---

# Changelog 生成（繁體中文）

依 git history 自動寫一段 changelog，附加到 `CHANGELOG.md` 最上方。

## 步驟

1. **決定起始點**
   - 若 `$1` 有值：用 `$1` 當起點（可以是 tag、commit hash、或日期，例如 `v0.2.0`、`2026-04-01`）。
   - 若 `$1` 為空：先試 `git describe --tags --abbrev=0`；如果連一個 tag 都沒有，fallback 到最近 30 天 (`--since="30 days ago"`)。

2. **撈 commits**

   ```bash
   git log <起點>..HEAD --pretty=format:"%h|%s|%an|%ad" --date=short --no-merges
   ```

3. **分類歸納**（按 commit message 前綴 + 內容語意）：
   - ✨ 新增功能
   - 🐛 修正
   - 📚 文件 / 教學
   - 🔧 重構 / 維護
   - 🎨 範例 / Demo
   - 其他

   每條 commit 寫成一句**讓非工程師也看得懂**的繁體中文（不要照抄 commit message），結尾標註 `(<hash>)`。

4. **抓版本號**
   - 看根目錄有沒有 `package.json` / `pyproject.toml` 取版本；沒有就用日期 `YYYY-MM-DD`。

5. **寫入 CHANGELOG.md**
   - 若檔案不存在就建，加開頭：

     ```markdown
     # Changelog

     > 用「給人讀」而不是「給機器讀」的方式記錄這個 repo 的演進。
     ```

   - 新增段落塞在標題之後、其他版本之前：

     ```markdown
     ## <版本 / 日期>

     ### ✨ 新增功能
     - ...

     ### 🐛 修正
     - ...
     ```

   - **不要刪掉舊紀錄**，只新增。

## 注意事項

- commit author 不是 kevin801221 / kevin@legalsign.ai 的，仍要列入但不要強調。
- 不要在 changelog 中提到 "Claude Code"、"AI 生成" 之類字眼。
- 寫完後告訴使用者：「新增了 N 條紀錄到 CHANGELOG.md，跨 X 個 commit」。
