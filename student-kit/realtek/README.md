# 瑞昱課後問題與實作

上課從 [簡報第 177 頁的問題總覽](https://docs.google.com/presentation/d/10ShW-Ij-aOjli2i4BnXB5YZFQ-RzLgJHL3jCUuvpc1c/edit#slide=id.realtek_questions_start) 選題。自己練習時，點下表的問題，就能在解壓後的教材裡找到起始檔、操作指令和驗收方式。表中的「解答」會開啟原簡報對應頁。

| 題目 | 學生操作手冊 | 完成時要能做到什麼 | 原簡報與來源 |
| --- | --- | --- | --- |
| Q1 | [Claude Code 怎麼接上 Visio MCP？](cases/visio-mcp/STUDENT.md) | 讓 Claude 自己選工具讀出三個圖形和兩支箭頭。 | [解答](https://docs.google.com/presentation/d/10ShW-Ij-aOjli2i4BnXB5YZFQ-RzLgJHL3jCUuvpc1c/edit#slide=id.realtek_visio_mcp) · [claude-course-code](https://github.com/kevin801221/claude-course-code/tree/main/Projects/visio-mcp-lab) |
| Q2 | [怎麼從工作紀錄整理個人和主管的日週報？](cases/claude-mem/Q2.md) | 從一筆日報追回來源，再確認主管週報涵蓋哪些人。 | [解答](https://docs.google.com/presentation/d/10ShW-Ij-aOjli2i4BnXB5YZFQ-RzLgJHL3jCUuvpc1c/edit#slide=id.realtek_report_lab) · [claude-mem-application_](https://github.com/kevin801221/claude-mem-application_) |
| Q3 | [上百份 Markdown，該先讀哪份？](cases/md-retrieval/STUDENT.md) | 用同一道題比較資料夾、索引和 Wiki，指出支撐答案的原文。 | [解答](https://docs.google.com/presentation/d/10ShW-Ij-aOjli2i4BnXB5YZFQ-RzLgJHL3jCUuvpc1c/edit#slide=id.realtek_md_retrieval) · [compare-claudecode-retrieval-methods](https://github.com/kevin801221/compare-claudecode-retrieval-methods) |
| Q4 | [開新對話後，怎麼找回上次的修法？](cases/claude-mem/Q4.md) | 用 observation ID 找到完整紀錄，對照當時的測試證據。 | [解答](https://docs.google.com/presentation/d/10ShW-Ij-aOjli2i4BnXB5YZFQ-RzLgJHL3jCUuvpc1c/edit#slide=id.realtek_memory_lab) · [claude-mem-application_](https://github.com/kevin801221/claude-mem-application_) |
| Q5 | [怎麼讓不同專案畫出一致的 Mermaid 圖？](cases/mermaid-design/STUDENT.md) | 套用團隊風格，沿箭頭確認補件後會重新檢查。 | [解答](https://docs.google.com/presentation/d/10ShW-Ij-aOjli2i4BnXB5YZFQ-RzLgJHL3jCUuvpc1c/edit#slide=id.realtek_mermaid_skill) · [mermaid-design](https://github.com/kevin801221/mermaid-design) |
| 延伸 A | [怎麼讓 Mac 複製英文後貼出繁中？](cases/clip-translate/STUDENT.md) | 啟動監聽、複製英文、貼出繁中，最後停止監聽。 | [解答](https://docs.google.com/presentation/d/10ShW-Ij-aOjli2i4BnXB5YZFQ-RzLgJHL3jCUuvpc1c/edit#slide=id.realtek_clip_demo) · [clip-translate](https://github.com/kevin801221/clip-translate) |
| 延伸 B | [實驗測到 5 秒，PM 可以寫進 PRD 嗎？](cases/autosearch-prd/STUDENT.md) | 離線跑研究與測試，從 PRD 追到原始數據，核對變更仍待人工決定。 | [解答](https://docs.google.com/presentation/d/10ShW-Ij-aOjli2i4BnXB5YZFQ-RzLgJHL3jCUuvpc1c/edit#slide=id.realtek_bc_run) · [autosearch-PRD-claudecode（私有）](https://github.com/kevin801221/autosearch-PRD-claudecode) |

## 從哪裡執行

先開啟解壓後的 `claude-code-student-kit/`。每份手冊的第一步會指向自己的實驗資料夾。Q2 與 Q4 共用 `cases/claude-mem/`，前者做報表，後者練習保存與檢索。

延伸 B 的合成資料、編譯來源、文件模板與測試都在包內。準備好 Python 3.10 以上、CMake 3.20 以上與 C++17 編譯器即可離線完成 CLI 實驗。Visio 與剪貼簿的 Claude 示範需要已登入的 Claude Code，剪貼簿腳本還需要 macOS。其他案例的離線步驟與外部工具需求列在各自手冊。

[來源版本與收錄範圍](../SOURCES.md#realtek-sources)
