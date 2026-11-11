# 發行前驗證紀錄

日期：2026-11-11。環境：macOS、Node.js 22.x、Python 3.14.3、Claude Code 2.1.319。根專案預期支援 Node.js 22+、Python 3.10+；未另在 Windows、舊 Python 或不同 CLI 版本驗證。

本頁保留首次製作的驗證紀錄。分享前已於 Claude Code 2.1.322、Node.js 22.13.0、Python 3.13.1 再次檢查，並修正下載入口及 Mods 暫存路徑，詳見 [分享檢查紀錄](share-review.md)。

## 已執行

| 命令 / 檢查 | 結果 | 證明範圍 |
|---|---|---|
| `npm test` | 9 pass，0 fail | 真實程序的任務 CRUD、錯誤資料保留、Hook 決策、MCP 初始化與工具呼叫 |
| `npm run check` | 通過 | 12 Labs、JSON/Python 語法、本地 Markdown 連結、frontmatter、49 項來源紀錄與雜湊 |
| doc-generator sample 與 expected-api.md 比對 | 一致 | AST 產生器的範例輸出 |
| rag-flow.py 的 hooks / 自動化 / 天氣 | 三種 trace 符合 | 直接命中、重寫後命中、上限停止 |
| `bash -n scripts/summarize.sh` | 通過 | Shell 語法；未呼叫模型 |
| `claude plugin validate .claude` | Validation passed | 根擴充元件結構 |
| `claude plugin validate labs/07-plugins/course-review` | Validation passed | 本機 Plugin 結構；未做 marketplace 發布認證 |
| `CLAUDE_CONFIG_DIR=/private/tmp/claude-course-kit-validation claude plugin test advanced/matt-flow-mods` | 76 pass，0 fail | CLI 測試工具中的模擬事件、狀態與 gates；未呼叫模型 |
| `python3 examples/lecture-mini-projects/pomodoro/smoke-test.py` | 通過 | 隔離測試計數 1/50 與通知命令分支，不發真通知 |
| 五個來源 Git 快照與 LICENSE | 全部存在 | 來源固定 commit，26 檔 copy 原樣，12 項 adapted，11 項導讀參考 |

本包 CLI、Hook 與 MCP 的測試先於其實作撰寫；最初因功能尚未實作而失敗，再補上實作使行為通過。新增後另有只讀審查，抓到舊 `default` 權限旗標，已修正為本機支援的 `manual`。

`npm run check` 的來源 hash 針對發行版教材精選檔；學生刻意改動精選教材時會提醒差異。根層 src/bin 的課堂作業不在此固定來源 hash 範圍。

## 未執行，須課堂再驗

- 真人 Claude 的自然語言規劃、委派、Skill 自動探索與所有端到端互動。
- 在真實 Claude session 中掛載並操作 Hook、MCP、本機 review Plugin。
- 天氣 API 的實際網路讀取與產圖。
- Headless 的模型呼叫、計費行為及雲端 CI 執行。
- Mods 真人面板、外部 Matt Skills、完整 SDK 型別編譯；沒有把可能回傳 skipped 的腳本當作通過。
- ML 資料下載/模型訓練、原生 Agent Teams，以及講義未找到的 AgenticRAG notebooks。

這些限制已列在各 Lab；離線測試通過不會被描述為上述整合已完成。
