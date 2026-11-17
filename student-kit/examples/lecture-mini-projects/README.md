# 講義指名的小專案原碼

三個直接出現在講義課堂演練的例子，各只保留少量核心檔與操作說明。
所有範本位於 `source/` 或明確標示的示例目錄，不會在本精華 Repo 自動啟用。

| 例子 | 原始碼 | 講義位置 | 開始 |
|---|---|---|---|
| weekly-haiku | legacy command；另附新版 Skill 改寫 | Part 04，85–86 | [README](weekly-haiku/README.md) |
| recipe-genie | 只允許搜尋的 sub-agent | Part 11，256–257 | [README](recipe-genie/README.md) |
| pomodoro | PostToolUse Bash hook + 設定 | Part 12，324–326 | [README](pomodoro/README.md) |

表中為投影片印出的頁碼；原 PDF 的實體頁少一頁，個別 README 另列對照。
原碼與改寫有清楚區分，原始授權沿用 `claude-course-code` 的 MIT。
最小可執行離線檢查是 pomodoro 的 `smoke-test.py`；Claude 的提示詞輸出與真人互動須另在課堂驗收。
