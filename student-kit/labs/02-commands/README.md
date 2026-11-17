# Lab 02：把重複提示變成 Command

講義 Part 04。先讀 [.claude/commands/course-plan.md](../../.claude/commands/course-plan.md)。

## 操作

在根目錄啟動 Claude，在互動對話輸入：

```text
/course-plan 新增 list --pending，只顯示未完成任務，其他行為保持相容
```

1. 對照 `$ARGUMENTS` 被替換後的需求是否完整。
2. 計畫應指出 `bin/tasks.mjs`、資料操作與真實測試，不只列抽象步驟。
3. 複製成你自己的 `/course-handoff`，讓它依交接模板產出摘要；先在練習 Repo 試用。
4. 比較 [兩個精選 commands](../../resources/templates/commands/README.md)，選一份改成自己專案的指令。

## 驗收

同一 command 換需求仍會先讀相關檔案；規劃階段未改程式；計畫包含失敗案例與可執行命令。

`.claude/commands/` 是保留相容的寫法；新建可重用流程也可使用 `.claude/skills/<name>/SKILL.md`。同名時要先處理衝突，兩者不必重複安裝。

講義同題原碼：[weekly-haiku](../../examples/lecture-mini-projects/weekly-haiku/README.md)，同時保留原 command 與新版 Skill 選用版。
