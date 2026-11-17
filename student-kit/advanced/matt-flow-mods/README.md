# matt-flow：進階 Mods 原始碼閱讀包

這份精選保留 matt-flow `0.7.0` 的核心原碼、原測試、型別與開發檢查腳本，另加學生導讀。先讀 [STUDENT-GUIDE.md](STUDENT-GUIDE.md)，課堂操作見 [Lab 11](../../labs/11-mods/README.md)。

來源是 `kevin801221/matt-flow-mods` 的固定快照：[`70b50bc1b822eb18d770f8f75588b3b01f77cc27`](https://github.com/kevin801221/matt-flow-mods/tree/70b50bc1b822eb18d770f8f75588b3b01f77cc27)。所附來源檔逐字保留，採 [MIT 授權](LICENSE)。原作者的完整安裝與功能說明請看[該快照 README](https://github.com/kevin801221/matt-flow-mods/blob/70b50bc1b822eb18d770f8f75588b3b01f77cc27/README.md)。

此包適合研究「如何把開發流程做成狀態機與事件關卡」。它依賴特定 Claude Code Mods 執行環境，不能用一般 Node.js 直接啟動，也不能把 `hooks/hooks.json` 當成傳統 `.claude/settings.json` 的 Hooks 設定。放在 `advanced/` 下不會替學生安裝或啟用外掛。

整理時已使用 Claude Code `2.1.319` 的 `claude plugin test` 實跑原測試：**76 pass / 0 fail**，約 1.96 秒。測試採隔離的 `CLAUDE_CONFIG_DIR`，沒有開互動 session、呼叫模型或變更使用者的 history／trust。這驗證引擎測試工具中的事件與狀態規則；真實 UI、完整型別編譯，以及外部 Matt Skills 的完整互動尚未驗證。重跑方式見[學生導讀](STUDENT-GUIDE.md)。

排除項目包含 `.git/`、`.scratch/` 歷史工作資料、圖片、上游專案的 `CLAUDE.md` 與文件；完整原專案可由上面的固定快照取回。本資料夾的 `README.md` 與 `STUDENT-GUIDE.md` 是精華包新增的說明。
