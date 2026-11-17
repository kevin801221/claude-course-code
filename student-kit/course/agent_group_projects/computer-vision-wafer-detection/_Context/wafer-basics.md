# 晶圓檢測基礎

## WM-811K 9 種 Pattern
0: Center | 1: Donut | 2: Edge-Loc | 3: Edge-Ring
4: Loc | 5: Random | 6: Scratch | 7: Near-full | 8: None

## 訓練用 6 類 (排除 Random/None/Near-full)
0: center | 1: donut | 2: edge-loc | 3: edge-ring | 4: loc | 5: scratch

## bbox 自動生成原則
- Center/Loc: 最大連通分量外接 bbox
- Donut: 中環區域(30%-80% radius)bbox
- Edge-Loc: 邊緣局部最大分量
- Edge-Ring: 整個外圈
- Scratch: PCA 主軸 + 擴大 bbox
- Random/None: 不畫 bbox,跳過

## 資料源
- Roboflow Universe: https://universe.roboflow.com/wm811k-paasr/wm811k (409 張,已有 bbox,快速驗證)
- Kaggle WM-811K: 完整 172k 張(之後再用)

## Mac 訓練建議
- yolov8n 或 yolov8s (小模型本機可跑)
- imgsz=416 或 640
- batch=8-16
- device='mps'

## 評估目標(MVP)
- 跑通 pipeline > 高 mAP
- 能輸出 inference 結果視覺化 = 成功
