# MCP 課堂修正版：只整理兩個匿名檔案

對應講義 Part 13；依 `Projects/05-organize-downloads/` 改寫。原例在 settings.json 放 MCP 設定，且授權真實 Downloads；此版把設定獨立放在 **`.mcp.json`**，只將本目錄的 `sample-files/` 提供給 filesystem server。

## 先看資料，再連線

本包只有兩個匿名樣本：`meeting-notes.txt` 與 `course-tasks.csv`。不要把真實 Downloads 複製進來，也不要把授權路徑改成家目錄或 `/`。

需要 Node.js/npx、可用的 Claude Code 帳號。`npx -y` 會執行所解析到的 `@modelcontextprotocol/server-filesystem` 套件；首次執行或本機無快取時需要網路，可能寫入 npm 快取。此包未內附該 MCP server，未鎖其套件版本，也沒有代你執行下載/安裝。模型使用另外依你的帳號計費。

從精華包根目錄執行：

```bash
cd classroom-fixes/mcp-sandbox
COURSE_MCP_SANDBOX_DIR="$PWD/sample-files" claude --permission-mode manual --mcp-config .mcp.json --strict-mcp-config
```

這個環境變數只給此次命令使用，讓 `.mcp.json` 的 `${COURSE_MCP_SANDBOX_DIR}` 展開成目前樣本目錄的絕對路徑。不會註冊全域 MCP，不會修改 `~/.claude/settings.json`。macOS/Linux/WSL 可用上述語法；原生 PowerShell 的環境變數語法不同。

在互動對話中用 `/mcp` 檢查 `fs` 的連線狀態，接著分兩輪：

```text
第一輪：只用 fs MCP 列出授權目錄的兩個檔案，依副檔名提出 dry-run 清單。
清單需有目前路徑、擬建資料夾、目標路徑與理由。先不要建資料夾、搬移或刪除。
```

預期計畫：`meeting-notes.txt → notes/meeting-notes.txt`，`course-tasks.csv → tables/course-tasks.csv`。第一輪結束後，兩個檔案仍在原位。

```text
第二輪：只依我剛確認的兩筆計畫建立 notes/、tables/ 並搬移這兩個匿名檔案。
遇到同名目標、來源缺失或任何授權外的路徑就停止並回報，不刪除、不覆蓋、不擴大範圍。
```

## 驗收與復原

- 工具紀錄應真的使用 filesystem MCP，而非只憑 README 作答。
- dry-run 前後檔案不變；確認後只有兩筆預期搬移，內容不變。
- 再執行時應先查看現況，不能假設原路徑仍存在；中斷不保證可以盲目重跑或自動 undo。
- 要重做，可從原 ZIP 重新取出這個目錄的兩個匿名樣本。

filesystem server 在授權目錄內具讀寫能力；`manual`、提示詞與 `--strict-mcp-config` 都不等同於整個 session 的作業系統沙箱。此練習沒有要求刪檔，也沒有自動化全域或排程安裝。

**本次驗證：**JSON、樣本與環境變數佔位結構已檢查。未執行 npx、未連線真實 MCP/Claude、未使用模型、未觸碰真實 Downloads。
