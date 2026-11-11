# 分享前複檢

日期：2026-11-11。檢查環境：Claude Code 2.1.322、Node.js 22.13.0、Python 3.13.1。

## Standards

獨立只讀審查未發現需要阻擋分享的程式或規範問題。核心 9 項、教材檢查與額外 CLI/MCP 錯誤情境均符合本包宣告；Headless 腳本語法與 Plugin/元件靜態驗證通過。

## Spec

獨立只讀審查找到兩項 P2，已修正：

1. **下載入口**：GitHub 放在大 Repo 的子目錄，原說明容易讓學生下載整個分支後找錯路徑，或在父 Repo 內啟動並繼承額外設定。README 現在優先連到學生專用 ZIP，要求獨立解壓。
2. **跨平台暫存路徑**：Mods 學生操作原用 macOS 的 `/private/tmp`；現在用 `mktemp -d` 建立新的暫存目錄，適用 macOS/Linux/WSL。固定舊路徑僅保留在歷史驗證紀錄。

五個來源的精選素材、缺失 notebooks 的揭露、真人整合的驗證界線均符合原教學包需求；未發現其他阻擋分享的 Spec 問題。

## 實際複檢

- 核心程序測試：9 pass、0 fail。
- Mods 原始事件測試：76 pass、0 fail；沒有呼叫模型。
- pomodoro 的隔離計數/通知分支測試通過；未發送真實通知。
- 文件產生器與預期輸出一致；RAG 的直接命中、重寫命中、停止三條流程通過。
- 教材 JSON、Python 語法、本地連結、frontmatter、49 項來源紀錄與五份原始授權檢查通過。
- Git 歷史檔案掃描未發現常見 Anthropic/GitHub/Google 金鑰、AWS access key、JWT 或私鑰格式；這是模式掃描結果，不是完整安全性保證。
- 以未帶認證的公開 GitHub ZIP 連結下載原發布檔，位元組與本機原包一致，ZIP CRC 正確。修正後亦需重新下載及解壓測試，確認交付的就是最新內容。

## 分享方式與限制

分享 README 首頁或其「學生專用 ZIP」連結；GitHub Repo/分支是公開的。Google Drive 原檔沿用私人權限，分享 Google Drive 時仍須由講師設定收件者或檢視權限。

可以進行教材與離線實作；真人 Claude 委派、真實 Hook/MCP 掛載、天氣 API、Headless 計費、Mods 真人面板、Teams 與 ML 訓練仍未做完整端到端驗證。這些不是核心離線測試的覆蓋範圍。
