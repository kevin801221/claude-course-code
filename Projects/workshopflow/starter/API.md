# 共用 HTTP 契約

在本機 127.0.0.1 的教學服務上，每次請求以 `X-Participant: i1` 等種子 ID 選擇操作身分。這是身分模擬，不要對外開放。API 必須依伺服器種子角色／擁有權決定授權；不接受「我是 HR」的 JSON 欄位。所有回應均為 JSON；錯誤有可讀的 `error`。ID 均為字串。日期採 ISO 8601；FIFO 使用伺服器單調序號，不按日期排序。

| 操作 | 路徑 | 契約 |
|---|---|---|
| GET | /api/participants | 種子身分陣列，每筆 id、kind |
| GET | /api/sessions | 場次陣列：id、title、description、starts、capacity、open（0/1）、remaining |
| GET | /api/sessions/:sid | 同上，加 mine（當事人的報名或 null） |
| GET | /api/mine | 當事人所有報名，含已取消 |
| GET | /api/registrations | 僅 HR：所有報名 |
| POST | /api/sessions | 僅 HR：title、description、starts、capacity；回新場次，201 |
| PATCH | /api/sessions/:sid | 僅 HR：可提供正整數 capacity、布林 open 或兩者；回更新場次 |
| POST | /api/sessions/:sid/enroll | 僅學員，回本人唯一報名 |
| POST | /api/sessions/:sid/cancel/:uid | 僅該學員能取消自己的報名，回同一筆報名 |

報名：`{sessionId, participantId, status, queue}`。confirmed／cancelled 的 queue 為 null；waitlisted 為正遞增整數。重送有效報名回 2xx 與原結果。未知身分 401、角色或擁有權不符 403、無此資源 404、欄位錯誤 400、非允許的狀態或容量衝突 409。資料庫路徑可由 `WORKSHOP_DB` 設定；HTTP 連接埠由 `PORT` 設定，0 應由系統分配。啟動完成印出 `READY http://127.0.0.1:<port>` 供公共驗收器連接。持久資料不可在啟動時重置。

**瀏覽器共用介面契約：**讓學生與測試都能用語意找控件。四視圖：場次列表、詳情、我的報名、HR 管理。使用標示「目前身分」的選單；每場以標題超連結開詳情；「我的報名」「HR 管理」為連結；詳情顯示「我的狀態：正取／候補／已取消」與「報名」按鈕；HR 每場使用 article 包覆名稱標題、標為「容量」的 input 和「更新容量」按鈕。場次摘要顯示「開放 · 剩餘 X / Y」或「已截止 · 剩餘 X / Y」，錯誤使用 role=alert。畫面狀態應來自 API。
