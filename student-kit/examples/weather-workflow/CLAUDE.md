# Weather workflow lab

這是一個獨立的 Command → Agent → Skill 示範。用繁體中文回覆。

- 入口：`/weather-orchestrator celsius` 或 `/weather-orchestrator fahrenheit`。
- 讀數必須來自本次 Open-Meteo API 回應；範例讀數僅供排版參考。
- API 抓取交給 `weather-agent`，主對話使用 `weather-svg-creator` 寫出 SVG 與摘要。
- 沒有真實讀數時停止並描述錯誤，不補假資料。
- 不需要 API key，不修改全域 Claude 設定，不加入音效 hooks。
