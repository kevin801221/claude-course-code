# Wafer Defect Detection AI Team

晶圓瑕疵檢測 YOLO 自動訓練工作區。

## 目標
從零自動完成: 抓資料 → 標註 bbox → 訓練 YOLO → 跑推論

## 資料夾
- _Context/ — 領域知識(必讀)
- .claude/skills/ — 共用技能
- .claude/agents/ — Sub-agents
- Projects/ — 專案輸出
- .claude/rule 要讀取基本規則
## 任務路由
- 抓資料 → data-hunter
- 自動畫 bbox → bbox-labeler
- 訓練 YOLO → training-runner
- 跑推論 → inference-runner

## 規則
- 預設委派 sub-agent
- 訓練前顯示預估時間,等使用者 GO
- 用 Mac 環境(MPS 加速,小資料本機跑)
- 資料少沒關係,目標是端到端跑通
- 所有路徑用 pathlib.Path,不要硬編碼
- Python 套件用 uv 管理 (不用 pip)
- ROBOFLOW_API_KEY 從專案根目錄的 .env 載入
