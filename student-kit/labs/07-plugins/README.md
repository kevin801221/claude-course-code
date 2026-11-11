# Lab 07：把一個 Skill 包成 Plugin

講義 Part 14。先讀 [plugin manifest](course-review/.claude-plugin/plugin.json) 與 [review Skill](course-review/skills/review/SKILL.md)。

從 Repo 根目錄執行：

```bash
claude plugin validate labs/07-plugins/course-review
claude --permission-mode manual --plugin-dir ./labs/07-plugins/course-review
```

互動對話輸入：

```text
/course-review:review bin/tasks.mjs 與 src/task-board.mjs 的錯誤處理
```

## 驗收

- 命名空間是 `/course-review:review`；根層的 `/course-check` 仍是獨立 Skill。
- manifest 在 `.claude-plugin/`，`skills/` 放 Plugin 根層，兩者別放反。
- 靜態 validator 結果與真人端到端執行分開記錄。

這是本機載入練習，未發布 marketplace，也不會自動安裝到同學的全域環境。若自己的版本沒有 `--plugin-dir`，先查 `claude --help` 與 [版本說明](../../docs/compatibility.md)。Mods 是另一個進階主題，見 Lab 11。
