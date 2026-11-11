# Wafer Defect Detection — /agents Demo

教學用乾淨資料夾。
用 `/agents` slash command 建構 4 個 sub-agent，目標是教學示範，不是要真的跑完訓練。

## 目標 agent 清單
1. data-hunter — 從 Roboflow 下載資料
2. bbox-labeler — 驗證 bbox 並切分 train/val/test
3. training-runner — 訓練 YOLO（必須要使用者 GO 才能跑）
4. inference-runner — 推論並產出視覺化

## 規則
- 預設委派 sub-agent
- Python 套件用 uv 管理
- Mac 環境（MPS）
- 所有路徑用 pathlib.Path
