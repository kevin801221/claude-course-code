# Wafer Defect Detection — 課程模板

晶圓瑕疵檢測 YOLO 自動訓練工作區（教學用空白模板）。

## 目標
從零自動完成：抓資料 → 驗證標註 → 訓練 YOLO → 跑推論視覺化

## 資料夾
- `_Context/` — 領域知識與課程指引（必讀）
- `.claude/agents/` — 你會用 `/agents` 建在這裡
- `Projects/` — 訓練結果輸出

## 任務路由（agent 建好後自動生效）
- 抓資料 → `data-hunter`
- 驗證 + 切分 → `bbox-labeler`
- 訓練 YOLO → `training-runner`
- 跑推論 → `inference-runner`

## 規則
- 預設委派 sub-agent
- 訓練前顯示預估時間，等使用者明確說 GO
- Mac 環境（MPS 加速）
- Python 套件用 `uv` 管理（不用 pip）
- 所有路徑用 `pathlib.Path`
- `ROBOFLOW_API_KEY` 從專案根目錄的 `.env` 載入
- 回應使用繁體中文
