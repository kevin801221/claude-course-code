# 版本與執行環境

本包整理日期：2026-11-11。講義內容標示 2026-10，更新頁提到 CLI v2.1.311；本機實際可用版本是 **Claude Code 2.1.319**。本包避免固定模型 ID、方案預設值與 context 容量，代理優先用 `inherit`。

分享前再次檢查的環境為 **Claude Code 2.1.322、Node.js 22.13.0、Python 3.13.1**；核心 9 項與 Mods 76 項測試再次通過。下表的 2.1.319 是首次製作的歷史驗證，最新結果見 [分享檢查紀錄](share-review.md)。

| 元件 | 本包驗證範圍 | 你還需要什麼 |
|---|---|---|
| 任務 CLI | Node.js 標準函式庫、真實程序測試 | Node.js 22+ |
| Hook、MCP、文件產生器、離線 RAG | Python 標準函式庫、程序測試/範例比對 | Python 3.10+，命令名為 python3 |
| 根層 Commands / Skills / Agents | 結構、路徑、官方欄位與靜態 validator | Claude Code 登入後互動驗收 |
| 本機 Plugin | `claude plugin validate` | 支援 `--plugin-dir` 的版本 |
| Matt Mods | 2.1.319 的 `claude plugin test`，76/76 | 真實使用需 Mods、相依 skills 與自己的 session |
| 天氣工作流 | 依賴與來源檢查 | 模型額度與 Open-Meteo 網路 |
| ML / Agent Teams | 契約與原碼閱讀 | 專案環境、功能權限、資料與訓練資源 |

macOS/Linux 可直接照終端機例子執行；Windows 建議 WSL。若 Python 命令不同，需同步修改 npm 測試、Hook、MCP 設定中的 command。根專案沒有 npm 外部套件，沒有必要為它下載 lockfile 所列依賴。

## 舊講義與目前 CLI 的差異

2.1.319 的 `--permission-mode` 清單使用 `manual`，沒有舊講義的 `default`；本包的根設定與操作例子統一用 `manual`。若你用較早版本，只在 `claude --help` 明確列出 `default` 時使用舊名稱，並同步調整 `.claude/settings.json`。這也是為何要先核對本機 help。

## 使用前核對

```bash
claude --version
claude --help
claude plugin --help
node --version
python3 --version
```

在互動對話用 `/help`、`/permissions`、`/agents`、`/mcp` 確認實際可用功能。不要把講義的版本號、模型名、未出現在自己 help 中的旗標直接套用。

## 本次查證的官方契約

- [Skills](https://code.claude.com/docs/en/skills)：Skill 目錄、手動觸發與 allowed-tools。
- [Hooks](https://code.claude.com/docs/en/hooks)：PreToolUse stdin JSON 與 permissionDecision。
- [MCP](https://code.claude.com/docs/en/mcp)：stdio 設定與 session 載入。
- [Plugins](https://code.claude.com/docs/en/plugins)：manifest 與元件目錄。
- [MCP stdio 規格 2024-11-05](https://modelcontextprotocol.io/specification/2024-11-05/basic/transports)：每行 JSON-RPC 與 stdout 約定。

CLI help 與這些文件可確認旗標/欄位契約，不能代替真人對話驗證。本包的實際測試紀錄另見 [verification.md](verification.md)。
