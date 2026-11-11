# WorkshopFlow 共同起點

需 Node 22.13 以上的 22.x 或 Node 24（內建 node:sqlite）、npm。先讀 [PRD-v1.md](PRD-v1.md) 和 [API.md](API.md)，再貼講師發給你的 P2 和一種模式 Prompt。請只在自己的工作目錄操作。

    npm ci
    npm run build
    npm start

開啟終端機印出的網址（預設 http://127.0.0.1:4100）。在尚未實作業務規則的起點，只會看到簡單說明和三場 seed；這是預期結果。改過前端後重跑 build；改過 server 後重啟。先關掉服務才執行 `npm run reset`；只重設目前工作目錄的教學資料庫。勿指定實際業務資料庫。

    npm test
    npx playwright install chromium
    node --test tests/ui.test.mjs

測試使用各自的暫時 SQLite 和系統分配的連接埠，不改手上的資料庫。初始版第一個 seed 檢查可通過；報名規則等測試應失敗，三組的任務就是實作同一份契約。未裝瀏覽器不要把 UI 標為通過；可指定 CHROME_PATH 使用已裝 Chrome 可執行檔。每次記錄輸出、程式版本和仍未完成項目。課堂模擬身分，沒有正式登入、Email、金流、雲端服務。
