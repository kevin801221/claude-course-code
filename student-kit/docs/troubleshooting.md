# 同學卡住時先看這裡

| 現象 | 先確認 | 最小處理 |
|---|---|---|
| npm 找不到 package.json | 目前是否在 Repo 根目錄 | `cd claude-code-student-kit` 再跑 |
| python3 找不到 | Python 是否安裝、PATH 是否正確 | 安裝 Python 3.10+；同步修改所有 command 名稱 |
| `npm test` 失敗 | 第一個失敗案例、stdout/stderr | 保留完整錯誤；不要先重裝無關套件 |
| `npm run check` 報 hash 不同 | 是否改到教材精選檔 | 課堂作業先改根層 src/bin；若刻意改教材，另留自己的版本與新來源紀錄 |
| command/skill 不見 | cwd、隱藏 `.claude/`、同名技能 | 從正確目錄開新 session，用 `/help` 檢查 |
| agent 不見 | `.claude/agents/` 與 frontmatter | 用 `/agents` 查載入，不把 agent 檔放 skills |
| MCP 連不上 | cwd、python3、JSON 是否乾淨 | 從根目錄啟動；stderr 才能放 debug log |
| Hook 完全沒執行 | 是否載入 Lab settings、事件名稱、路徑 | 先獨立 pipe JSON，再查 Claude hook debug |
| Hook exit 0 卻拒絕 | 是否輸出 deny JSON | exit 0 代表程式成功，工具決策在 JSON 內 |
| Plugin 看不到 skill | manifest 與 skills 的位置 | `skills/` 放 Plugin 根層，使用 namespaced command |
| Mods script 說 skipped | 是否有 CLI 提供的型別/測試環境 | skipped 不是 passed；看 Lab 11，先用 CLI plugin test |
| tasks.json 損壞 | 是否為合法任務陣列 | 保留原檔，手動修復；不要讓 agent 覆蓋成空陣列 |
| 天氣數字一直一樣 | 是否真實呼叫 API、資料時間 | 不能把 examples.md 示意數字當作當下天氣 |
| 模型/功能不能用 | 自己帳號與 CLI 的實際能力 | `/model`、`/help`；別為練習改成繞過權限 |

回報問題請附：Lab 編號、版本、目前目錄、完整命令、預期/實際、已嘗試的最小重現。請遮蔽金鑰與個人資料。
