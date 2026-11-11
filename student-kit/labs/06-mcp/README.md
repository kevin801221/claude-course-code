# Lab 06：本機只讀 MCP，先不碰金鑰

講義 Part 13。這個 [lesson-server.py](lesson-server.py) 用 Python 標準函式庫實作 stdio JSON-RPC 教學子集，只搜尋同目錄的 [課程索引](lessons.json)。不連網、不寫資料、不需要 npx 安裝。

## 操作

1. 從根目錄跑 `npm test`，測試會啟動真實子程序，檢查 initialize、tools/list、tools/call 與錯誤輸入。
2. 讀 [mcp.example.json](mcp.example.json)。`command` 啟動程序，`args` 的相對路徑要求從本 Repo 根目錄啟動。
3. 於根目錄執行：

```bash
claude --permission-mode manual --mcp-config labs/06-mcp/mcp.example.json --strict-mcp-config
```

4. 在對話用 `/mcp` 檢查連線，再說「請用 course-lessons 的 search_lessons 查 Hooks，回報 Part 與 Lab。」
5. 試 `不存在的主題`，應回傳空陣列；不應虛構課程。

## 驗收

你能指出工具名稱、JSON schema、傳回內容與來源資料。確認 Claude 真的呼叫 MCP 工具，而非只靠自己讀 README 回答。

這份程式只做教學需要的協定子集，宣告 `2024-11-05`，並非完整 MCP SDK；未提供 HTTP、OAuth、資源、分頁與取消。stdio 每行一份 JSON；stdout 不可混入 debug log。正式產品應採用 [官方 SDK](https://modelcontextprotocol.io/docs/sdk)。

`--strict-mcp-config` 限定此次 MCP 來源，不是對整個 Claude session 做沙箱隔離。結束 session 後無須清除全域 MCP 註冊，因為本練習沒有新增全域設定。
