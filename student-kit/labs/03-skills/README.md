# Lab 03：Skill 不只是一段 Prompt

講義 Part 10。讀 [.claude/skills/course-check/SKILL.md](../../.claude/skills/course-check/SKILL.md)，理解 description、手動觸發與 allowed-tools。

## 操作

1. 在 Claude 對話跑 `/course-check`，核對實際命令結果與回報。
2. 打開 [doc-generator](../../resources/templates/skills/doc-generator/README.md)。先不用 Claude，照 README 執行 Python 腳本，對照 expected-api.md。
3. 讀 `SKILL.md`、腳本、sample 與預期輸出；指出哪部分是操作流程、哪部分是確定性程式。
4. 若要使用，依 README 手動複製該 Skill 到新練習專案的 `.claude/skills/`，確認未覆蓋同名檔案。
5. 給 sample 新增一個有 docstring 的函式，再產生文件；確認新增內容真的出現。

## 驗收

能不靠模型執行腳本；能說出 AST 文件草稿不等於完整 OpenAPI；能說明哪些產出需人工核對。

`allowed-tools` 是該 Skill 啟動時的權限授予清單，不是整個 session 的工具白名單。更多設計方法見 [精選導讀](../../docs/reading-guide.md)。
