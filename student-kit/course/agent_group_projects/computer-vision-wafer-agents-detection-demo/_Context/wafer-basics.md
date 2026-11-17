# 晶圓檢測基礎

## WM-811K 是什麼

台積電前晶圓廠在 wafer map 上標記的瑕疵資料集，9 種 pattern：

| ID | Pattern | 說明 |
|---|---|---|
| 0 | Center | 中心區域瑕疵 |
| 1 | Donut | 環狀分佈 |
| 2 | Edge-Loc | 邊緣局部 |
| 3 | Edge-Ring | 邊緣環狀 |
| 4 | Loc | 局部 |
| 5 | Random | 隨機（雜訊，通常排除） |
| 6 | Scratch | 刮痕 |
| 7 | Near-full | 接近全瑕疵 |
| 8 | None | 無瑕疵 |

## 課程用版本

本課程用 Roboflow Universe `wm811k-paasr/wm811k` v3：
- 409 張圖
- 只有 1 類（Donut）
- 沒有切 train/val/test split

**這跟原始 WM-811K 不同**，是別人做過子集 + 簡化的版本，適合教學快速跑通。

如果想要完整版，可去 Kaggle 找 `WM-811K wafer map dataset`（172k 張）。

## 為什麼用 YOLO 而不是分類

WM-811K 原始任務是 **wafer map 分類**（整張圖 9 類）。
但本課程做的是 **bbox 物件偵測**，目標是：
1. 教 YOLO pipeline（業界更常用）
2. 產出可視化結果（bbox 比分類結果更直觀）

所以我們不直接用 WM-811K 原始檔，而用 Roboflow 上已轉成 YOLO bbox 格式的子集。

## Mac 訓練建議

| 項目 | 建議值 | 原因 |
|---|---|---|
| 模型 | `yolov8n.pt` | 最小，本機可跑 |
| imgsz | 416 | 平衡速度與精度 |
| batch | 8 | Mac MPS 記憶體常見上限 |
| device | `mps` | Apple Silicon GPU |
| epochs | 50 | 小資料集 50 足夠看趨勢 |

## 評估目標（MVP）

**跑通 pipeline > 高 mAP**

能輸出 10 張帶 bbox 的視覺化 PNG = 成功。
mAP 數字是 nice-to-have，不是核心 KPI。
