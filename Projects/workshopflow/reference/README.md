# WorkshopFlow 完整參考解

這是已完成的課堂參考解，並非三組協作的實測結果。在獨立的 reference 副本、用 Node.js 22.13+ (22.x) 或 24 執行：

    npm ci
    npm run build
    npm start

開啟終端顯示的網址，選擇 i1／i2 報名「最後一席」，取消 i1 的正取後應看到 i2 遞補。按 Ctrl+C，再以同一個資料夾執行 `WORKSHOP_PHASE=cr npm start`，用 e1 送新報名，再切換 HR 核准。PowerShell 可先執行 `$env:WORKSHOP_PHASE='cr'`。要重新開始時先停止服務，再 `npm run reset`。

完整驗收需要真實瀏覽器：

    npx playwright install chromium
    node --test tests/*.test.mjs

有可用 Chrome 時，也可將 CHROME_PATH 設為安裝後的可執行檔路徑。API 測試可單獨執行：`node --test tests/api.test.mjs tests/cr.test.mjs`。測試使用臨時資料庫；其他操作的預設 DB 是 data/workshop.sqlite。若更新前端，請重新 build。

決策與取捨：

- 同一個人、一場次共用一筆紀錄；取消後重新排隊會由伺服器分配新序號。不接受客戶端時間決定候補順序。
- 登記、遞補與核准讀取名額後立即寫回，同一 SQLite 交易維持容量以及隊伍順序。單一 Node 行程＋SQLite 適合教室本機；這不是分散式壓力測試成績。
- v1 和 CR-01 共享 schema，CR 只改新外部報名的轉換條件。重新啟動以保留舊資料，不能拿 reset 當「遷移」。
- X-Participant 從本機種子識別角色與操作者，後端檢查權限。這是模擬身分，不是正式登入；無金流、通知或部署設定。

四頁 UI 在 src/main.tsx；共用契約見 API.md、PRD-v1.md，增量契約在 CR-api.md。
