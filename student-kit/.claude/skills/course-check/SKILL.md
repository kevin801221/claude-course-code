---
name: course-check
description: 執行課堂共用專案測試，回報可追溯證據
disable-model-invocation: true
allowed-tools: Read, Bash(npm test), Bash(npm run check)
---

1. 確認 cwd 是有 package.json 的學生精華 Repo 根目錄。
2. 執行 `npm test` 與 `npm run check`，保存退出碼與失敗情境。
3. 若失敗，先歸納能重現的行為；這個 skill 不自動改程式。
4. 用「命令／觀察結果／限制／下一步」回報。
5. 本機測試沒有呼叫 Claude 模型，也沒有驗證真人 Claude 對話、Mods 或天氣 API。

`allowed-tools` 是這個 skill 的免詢問清單；不應把它描述成對整個 session 的工具隔離。
