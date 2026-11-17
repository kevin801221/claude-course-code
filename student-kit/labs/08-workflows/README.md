# Lab 08：從零件到完整工作流

講義 Part 04、10、11。這堂直接使用 [天氣工作流](../../examples/weather-workflow/README.md)。先依該 README 啟動，不要把散落的 `.claude` 檔混進根層。

## 任務

1. 畫出 Command → Agent → 預載 Skill → 主對話產圖 Skill 的順序。
2. 跑 Celsius，再跑 Fahrenheit；核對 API URL、資料時間、數值與 SVG。
3. 模擬查詢失敗，觀察流程能否停止，沒有引用範本的示意數字冒充真實資料。
4. 改成 Taipei / Dubai 可選；先把城市座標、資料來源與驗收寫進任務卡。

## 驗收

交出 `weather.svg`、`output.md`、本次 API URL、資料時間，以及一次失敗處理紀錄。沒有網路或模型額度時可做原碼導讀，但請把執行結果記為未驗證。

整合練習的價值在資料如何交接與驗收，不在開了幾個 agents。若只需查一個資料，先問自己是否真的需要代理隔離。
