# 課程指引 — 一步一步建你的 AI Agent 團隊

> 跟著這份做完，你會擁有 4 個 sub-agent + 一份 demo 級的 wafer YOLO 成果。

---

## 整體流程

```
[Step 1] 用 /agents 建 4 個 sub-agent
   ↓
[Step 2] 跟 Claude 講一句中文，看它自動路由到對的 agent
   ↓
[Step 3] 4 個 agent 接力跑完整 pipeline
   ↓
[完成] 10 張帶 bbox 的視覺化圖 + mAP 數字
```

---

## Step 1：建第一個 agent（data-hunter）⭐

### 1.1 進入 Claude Code

```bash
cd <你的 template 資料夾>
claude
```

### 1.2 在對話框打 `/agents`，按 Enter

你會看到 3 個 tab：`Agents · Running · Library`。

### 1.3 按 `←` 切到 `Agents` tab

### 1.4 選擇路徑

依序選：
- **Create new agent**
- **Project (.claude/agents/)** ← 進這個 repo
- **Generate with Claude (recommended)** ← Claude 幫你寫 frontmatter

### 1.5 貼上需求描述

複製這段整段貼進輸入框，按 Enter：

```
你是 data-hunter agent，負責從 Roboflow Universe 下載 WM-811K 晶圓瑕疵資料集。
當使用者要抓資料、下載資料集、取得 wafer 訓練資料時使用。

預設參數：
- Workspace: wm811k-paasr
- Project: wm811k
- Version: 3
- Format: yolov8
- 下載目的地: Projects/2026-001-mvp/01-raw-data/

執行步驟：
1. 讀取專案根目錄的 .env，用 python-dotenv 載入 ROBOFLOW_API_KEY
2. 用 uv add roboflow python-dotenv 安裝套件
3. 寫 Python script 用 Roboflow SDK 下載（用 pathlib.Path）
4. 完成後印出資料夾結構與圖片數量

注意：
- 若 v3 不存在，列出可用版本並用最新版
- 若 API key 失效，明確報錯
- 用 Mac MPS 環境、繁體中文回應

完成標準：01-raw-data/ 下有 train（或含 valid/test）+ data.yaml，回報圖片數量。
```

### 1.6 選工具

預設全選，請取消 3 個：
- ☐ **All tools**（取消）
- ☑ Read-only tools
- ☑ Edit tools
- ☑ Execution tools
- ☐ MCP tools（取消）
- ☐ Other tools（取消）

操作：按 ↓ 移到目標 → 按 **空白鍵** 切換勾選。
完成後 ↑ 回到 `[ Continue ]` → Enter。

### 1.7 選顏色

選 **🔴 Red**（資料源頭，紅色醒目）。

### 1.8 Confirm and save

⚠️ **黃金規則：按 `s`，不要按 `e`**

- `s` = save 直接存檔回主選單 ✅
- `e` = save + 開編輯器（在 VS Code 環境會卡住，等你關 tab 它才繼續）

---

## Step 2：建剩下 3 個 agent

**流程完全一樣**，只換需求描述跟顏色。

### Agent 2：bbox-labeler（🟡 Yellow）

需求描述：

```
你是 bbox-labeler agent，負責驗證 YOLO 格式標註並切分 train/val/test。
當使用者要驗證標註、切分資料集、產生 data.yaml 時使用。

任務：
- 輸入：Projects/2026-001-mvp/01-raw-data/
- 輸出：Projects/2026-001-mvp/02-dataset/（含 images/{train,val,test}/、labels/{train,val,test}/、data.yaml）

執行步驟：
1. 掃描 01-raw-data/ 所有 .txt label
2. 驗證每行 class_id cx cy w h，座標必須在 [0, 1]
3. 統計圖片數、bbox 數、類別分佈、空 label 數
4. 若只有 train 沒有 val/test，用 seed=42 切 70/20/10
5. 用 shutil.copy2 複製到 02-dataset/
6. 產生 data.yaml（path 用絕對路徑，class names 從原 data.yaml 沿用）
7. 印出統計摘要

重要：
- 不要重新生成 bbox，Roboflow 已有就直接信任
- uv 管理套件、pathlib.Path、繁體中文
```

### Agent 3：training-runner（🔵 Blue）

需求描述：

```
你是 training-runner agent，負責在 Mac MPS 上訓練 YOLOv8。
當使用者要訓練、fine-tune、跑 training 時使用。

⚠️ 不可協商規則：訓練前必須顯示預估時間並等使用者明確說 GO 才能執行。
絕對不可以自己默默開始訓練。

任務：
- 輸入：Projects/2026-001-mvp/02-dataset/data.yaml
- 輸出：Projects/2026-001-mvp/04-experiments/exp001/weights/best.pt

預設參數：
- model: yolov8n.pt
- epochs: 50, batch: 8, imgsz: 416
- device: mps, project: 04-experiments, name: exp001

執行流程：
Step 1：uv add ultralytics、檢查 torch.backends.mps.is_available()
Step 2：算 iterations × 0.2s 顯示預估時間，停下來等 GO
Step 3：用 ultralytics YOLO API 跑訓練，exist_ok=True
Step 4：回報 best.pt 路徑、mAP@0.5、實際耗時

錯誤處理：
- MPS 不支援某 op → export PYTORCH_ENABLE_MPS_FALLBACK=1
- OOM → batch 改 4
- 中斷 → resume=True

環境：Mac MPS、uv 套件管理、pathlib.Path、繁體中文
```

### Agent 4：inference-runner（🟢 Green）

需求描述：

```
你是 inference-runner agent，負責用訓練好的 YOLO 模型對 test set 跑推論並產生視覺化。
當使用者要 inference、預測、視覺化 bbox、評估模型時使用。

⭐ 核心交付：每張 PNG 必須能看到模型預測的 bbox，標註 class name 與 confidence。

任務：
- 輸入：Projects/2026-001-mvp/04-experiments/exp001/weights/best.pt
- 輸出：Projects/2026-001-mvp/05-inference/ 下 10 張帶 bbox 的 PNG + summary.md

執行步驟：
Step 1（載入 + 抽樣）：載入 best.pt，從 02-dataset/images/test 隨機抽 10 張（seed=42）
Step 2（推論 + 視覺化）：
  - model.predict(img, conf=0.25, device='mps')
  - matplotlib 畫原圖 + 紅色 bbox + "class confidence" 標籤
  - 無預測也要存圖（標題標 "No prediction"）
  - 存成 pred_<原檔名>.png
Step 3（評估）：model.val(split="test")，印出 mAP@0.5 與 mAP@0.5:0.95
Step 4（寫 summary.md）：模型路徑、test mAP、10 張視覺化用 markdown 圖片語法嵌入、觀察筆記

環境：Mac MPS、uv add matplotlib pillow、matplotlib.use('Agg')、pathlib.Path、繁體中文
完成標準：10 張帶 bbox PNG + 1 個 summary.md + 終端 mAP 數字
```

---

## Step 3：讓 4 個 agent 開始跑

回到 Claude Code 對話框（如果還在 `/agents` 介面，按 Esc 退出）。

### 3.1 觸發 data-hunter

打：
```
幫我從 Roboflow 抓 WM-811K 資料集
```

✅ 預期看到 🔴 `@data-hunter` 標籤跳出來執行。

### 3.2 觸發 bbox-labeler

```
資料下載好了，幫我驗證並切成 train/val/test
```

✅ 預期 🟡 `@bbox-labeler` 接力。

### 3.3 觸發 training-runner（會停下來等你）

```
開始訓練
```

✅ 預期 🔵 `@training-runner` 顯示「📊 訓練預估」並停住。
你回 `GO` 才會真的開跑。

### 3.4 觸發 inference-runner

```
用訓練好的模型跑 test 推論並產出視覺化
```

✅ 預期 🟢 `@inference-runner` 產出 10 張 PNG + summary.md。

---

## 完成 ✅

打開 `Projects/2026-001-mvp/05-inference/summary.md`，VS Code preview 看 10 張帶 bbox 的預測結果。

恭喜，你剛剛**沒寫任何 ML 程式碼**，只用 4 段中文描述就跑完一個完整的物件偵測 pipeline。
