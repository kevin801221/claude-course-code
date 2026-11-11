# dev-essentials：審查與事件護欄練習

先準備 `jq`；沒有 jq 時 guard 會拒絕該次 Read/Bash，格式化 Hook 則明確回報 skipped，不把 skipped 當成通過。套件安裝由同學自行決定，本包不代裝。

從精華包根目錄啟動：

```bash
claude --permission-mode manual --plugin-dir ./classroom-fixes/plugin-marketplace/plugins/dev-essentials
```

此 Plugin 含 `code-reviewer`，請主對話委派它盤點練習 Repo 的 diff。agents 沒有獨立 slash command；使用實際代理清單確認是否載入。模型改為 `inherit`。

`hooks/hooks.json` 註冊 PreToolUse 的 Bash/Read guard，以及 PostToolUse 的 Write/Edit 格式化。guard 只做字串/路徑比對，涵蓋列出的 production 與 secret 示意模式，不是完整命令解析、權限隔離或防外洩系統。

格式化會在 formatter 存在時修改剛編輯的檔案：Python→black、JS/TS→prettier、Go→gofmt、Rust→rustfmt。沒有 formatter 就略過。編輯紀錄寫入目前專案 `.outputs/plugin-demo/edits.log`，不再寫 HOME；會記錄檔案路徑，不記錄檔案內容。

只在可丟棄的練習 Repo 載入；先讀腳本，勿拿真實正式環境資料測 guard。完整流程見 [工作坊首頁](../../README.md)。

**驗證範圍：**靜態 Plugin validation、Shell 語法與臨時專案 Hook 分支；formatter 使用替身，驗證了呼叫與日誌，未呼叫模型、正式 DB 或修改真實檔案格式。
