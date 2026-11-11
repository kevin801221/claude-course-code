# Lab 04：分工要有契約

講義 Part 11。先讀根層 [.claude/agents/course-reviewer.md](../../.claude/agents/course-reviewer.md)；它只具 Read、Glob、Grep，不會修改程式或執行 shell。

## 操作

在 Claude 對話用 `/agents` 確認代理可見，再說：

```text
請委派 course-reviewer，讀取 bin/tasks.mjs、src/task-board.mjs 與對應測試。
檢查 list --pending 目前是否支援。交付觸發情境、程式位置與需要補的驗收。
這是行為盤點，不修改程式。不要說自己跑過測試。
```

接著比較 [三種精選 agents](../../resources/templates/agents/README.md)。請主對話整理 reviewer 與 test engineer 的結果，指出兩者可平行的部分、需要等待相同規格的部分。

## 驗收

- 每個子任務都有明確輸入、輸出、成功條件。
- 主對話能回收結論和證據；代理沒有提供的資訊不補成事實。
- 分工不等於讓兩個代理同時覆寫同一檔案。

課後看 [Agent Teams 契約](../../advanced/project-recipes/agent-teams/README.md)。單一對話的 subagent 與多 session 的 Teams，不應混稱同一種平行方式。

講義同題原碼：[recipe-genie](../../examples/lecture-mini-projects/recipe-genie/README.md)，用一個小代理觀察工具與回報契約。
