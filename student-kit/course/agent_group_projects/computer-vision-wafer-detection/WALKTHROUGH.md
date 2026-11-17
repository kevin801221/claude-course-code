# Wafer Defect Detection — 講師 Walkthrough

> **對象**：用過 Claude Code、不會寫 sub-agent 的工程師
> **形式**：講師本人現場帶
> **時長**：90 分鐘（Phase 1）+ 60 分鐘（Phase 2-4 demo）
> **產出**：一個 4-agent 團隊跑通 YOLO 訓練 → 推論 pipeline，並理解如何往「自動優化」進化

---

## 開場（5 分鐘）

### 講師說
> 「今天我們不教 YOLO 怎麼運作，也不教 wafer 領域知識。
> 我們教**怎麼用 Claude Code 把一個 ML pipeline 拆成 4 個專業 agent 互相協作**。
> 90 分鐘後，你會擁有一個可以對客戶 demo 的『自動化晶圓瑕疵偵測 AI 團隊』。」

### 為什麼這個案例好教
- ML pipeline 天然有階段（資料→標註→訓練→推論），分工很清楚
- 真實會卡的點都會卡到（API key、MPS、資料格式、時間估算）
- 結束有可視化的成果（10 張 bbox 預測圖）

### 教學分層（先講清楚層次）
| Phase | 內容 | 今天教 |
|---|---|---|
| 1 | 4-agent baseline 跑通 | ✅ 90 分鐘 |
| 2 | + evaluator agent（自動分析訓練結果） | ✅ Demo 20 分鐘 |
| 3 | + hyper-tuner agent（自動 HPO） | ✅ Demo 20 分鐘 |
| 4 | + orchestrator（自我改進迴圈） | ✅ 概念 20 分鐘 |

---

## Phase 1：4-Agent Baseline（90 分鐘）

### Step 0：環境準備（5 分鐘，課前必做）

**檢查清單貼黑板上**：
```bash
node --version          # 需要 18+
claude --version        # 需要有 Claude Code
uv --version            # 需要 uv (https://docs.astral.sh/uv/)
python3 --version       # 3.11+
```

**還要做**：
1. 去 https://app.roboflow.com 註冊（免費，Google 登入最快）
2. Settings → API → 複製 Private API Key

> 💡 講師提示：課前 1 天請學生先做，現場別花時間在註冊。

---

### Step 1：建工作區骨架（10 分鐘）

#### 講師說
> 「Claude Code 對資料夾結構有約定。我們先把骨架立起來，後面 Claude 自己會認得。」

#### 操作

```bash
mkdir -p computer-vision-wafer-detection/{.claude/agents,.claude/skills,_Context,Projects}
cd computer-vision-wafer-detection
```

**結構長這樣**：
```
.claude/agents/   ← Claude Code 自動掃描的 sub-agent 目錄
_Context/         ← 領域知識（讓 agent 引用，但不污染主 prompt）
Projects/         ← 實際產出
```

#### 教學要點（必講）
1. **為什麼 `.claude/agents/` 是約定？**
   - Claude Code 啟動會掃這個目錄，每個 `.md` 自動註冊成 agent
   - 學生會問：「那 `.claude/skills/` 呢？」→ 那是進階用，今天不碰
2. **為什麼有 `_Context/`？**
   - CLAUDE.md 是「永遠載入」，太多東西會佔 context window
   - `_Context/*.md` 是「按需讀」，agent 主動 grep/read 才載入

---

### Step 2：寫 CLAUDE.md（10 分鐘）

#### 講師說
> 「CLAUDE.md 是這個專案的『常駐 system prompt』。每次跟 Claude 對話，它都會自動讀。
> 規則就是：**只寫永遠成立的東西**，不寫具體任務細節。」

#### 內容（學生跟著打）

```markdown
# Wafer Defect Detection AI Team

晶圓瑕疵檢測 YOLO 自動訓練工作區。

## 目標
從零自動完成: 抓資料 → 標註 bbox → 訓練 YOLO → 跑推論

## 資料夾
- _Context/ — 領域知識(必讀)
- .claude/agents/ — Sub-agents
- Projects/ — 專案輸出

## 任務路由
- 抓資料 → data-hunter
- 自動畫 bbox → bbox-labeler
- 訓練 YOLO → training-runner
- 跑推論 → inference-runner

## 規則
- 預設委派 sub-agent
- 訓練前顯示預估時間,等使用者 GO
- Mac 環境(MPS 加速)
- Python 套件用 uv 管理 (不用 pip)
- ROBOFLOW_API_KEY 從 .env 載入
```

#### 教學要點
- 「任務路由」這段是讓 Claude 知道何時要叫哪個 agent
- 「訓練前要使用者 GO」這條是**人類在 loop 裡**的關鍵 → 訓練很貴，不能讓 agent 自己跑

#### 延伸提問（給工程師同行）
- Q：CLAUDE.md vs. system prompt 差在哪？
- A：CLAUDE.md 是 user-level 的常駐 context，可以 git commit、可以 team share；system prompt 是平台層的，你改不到。

---

### Step 3：寫 .env + .gitignore（3 分鐘）

```bash
echo "ROBOFLOW_API_KEY=你的key" > .env
echo ".env" > .gitignore
echo "Projects/" >> .gitignore
echo "*.pt" >> .gitignore
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
```

#### 教學要點（**講師大聲講**）
- **API key 永遠不進 git**，這是底線
- 課堂上有人會不小心 `git add .` 把 key 推上去 → 提早預防
- 用 `python-dotenv` 在程式裡 `load_dotenv()` 載

---

### Step 4：寫第一個 agent（data-hunter）（20 分鐘）⭐ 核心

#### 講師說
> 「現在進入今天最重要的 20 分鐘。寫一個 sub-agent 的 anatomy（解剖學）。」

#### Agent 檔案結構（畫在黑板上）

```markdown
---
name: data-hunter              # ← 唯一 ID，Claude 用這個叫你
description: 何時要叫我          # ← 自動路由的關鍵
tools: Read, Write, Bash, Glob # ← 安全邊界
---

你是 XXX 專員...                # ← System prompt 開始

## 任務
...

## 執行步驟
1. ...
2. ...

## 完成標準
...

## 錯誤處理
...
```

#### 為什麼這 4 個區塊？
| 區塊 | 用途 | 不寫的後果 |
|---|---|---|
| name + description | 路由 | Claude 不知道何時叫你 |
| tools | 安全 | agent 亂用 Bash 砍檔案 |
| 任務 | 聚焦 | agent 範圍蔓延 |
| 執行步驟 | 可重現 | 每次跑出不同結果 |
| 完成標準 | 驗收 | agent 自說自話「我跑完了」 |
| 錯誤處理 | 韌性 | 卡住就停在那 |

#### 完整 data-hunter.md（學生抄）

> 📄 直接看 `.claude/agents/data-hunter.md` 全文

#### 講師現場示範
1. 開檔案，逐行解釋每個區塊在做什麼
2. 特別講 `description` 的寫法 → **「當使用者要 X、要 Y、要 Z 時使用」這個句式很重要**，Claude 用 description 做路由

#### 學生練習（5 分鐘）
讓學生自己改 `description`，看 Claude 會不會還是路由給 data-hunter。
- 改成 `description: 下載資料` → Claude 可能找不到
- 改回完整描述 → Claude 找得到
- **這個對比要學生親眼看到**

---

### Step 5：寫剩下 3 個 agents（15 分鐘，加速）

#### 講師策略
- 不要再逐行解釋，直接展示成品（`bbox-labeler.md`, `training-runner.md`, `inference-runner.md`）
- 重點講**每個 agent 的職責邊界**：
  - bbox-labeler **不重新生 bbox**（信任 Roboflow）
  - training-runner **強制要使用者 GO**（人類在 loop）
  - inference-runner **產出視覺化**（讓老闆看得懂）

#### 教學要點：職責邊界（畫在黑板上）

```
┌──────────────┐  下載  ┌──────────────┐  驗證  ┌──────────────┐  訓練  ┌──────────────┐
│ data-hunter  │ ───→  │ bbox-labeler │ ───→  │training-runner│ ───→  │inference-runn│
└──────────────┘        └──────────────┘        └──────────────┘        └──────────────┘
     ↓                       ↓                       ↓                       ↓
  raw data              clean dataset            best.pt              預測 PNG + mAP
  + data.yaml           + data.yaml              + mAP                + summary.md
```

**為什麼分 4 個而不寫成 1 個大 agent？**
1. **上下文乾淨**：每個 agent 的 context window 只放自己的事
2. **可重用**：data-hunter 換個 workspace 就能下載別的資料
3. **可暫停**：train 跑一半中斷，可以從 inference 那段重啟
4. **失敗隔離**：bbox-labeler 出 bug 不會炸到下游

---

### Step 6：執行 data-hunter（10 分鐘）

#### 講師說
> 「現在我們不寫程式，直接跟 Claude 說『去抓資料』，看它怎麼自己找到 data-hunter。」

#### 操作
在 Claude Code 裡輸入：
> 幫我抓 Roboflow 的 wm811k 資料集到 Projects/2026-001-mvp/01-raw-data/

#### 學生會看到
1. Claude 自動呼叫 data-hunter agent
2. data-hunter 跑 `uv init` → `uv add roboflow python-dotenv`
3. 寫 `scripts/download_dataset.py`
4. 執行下載

#### 預期結果
- 409 張圖（**Roboflow 這個版本只有 1 類 Donut 且沒切 val/test**）
- ⚠️ **這是學員會卡住的真實狀況** → 接 Step 7

#### 教學要點（**這個故事一定要講**）
> 「現實世界你拿到的資料**永遠**跟教學範例不一樣。
> 我們原本以為有 6 類，結果只有 1 類；以為有 train/val/test，結果只有 train。
> Agent 不會替你決定要不要繼續，**它會把問題回報給你，由你決策**。」

---

### Step 7：執行 bbox-labeler（5 分鐘）

#### 講師說
> 「現在請 bbox-labeler 處理這個狀況：只有 1 類、沒有 val/test。」

#### 操作
> 用 bbox-labeler 把 01-raw-data 的 409 張切成 70/20/10 的 train/val/test，輸出到 02-dataset

#### 預期結果
| Split | 圖片 | bbox |
|---|---|---|
| train | 286 | 290 |
| val | 81 | 81 |
| test | 42 | 42 |

#### 教學要點
- bbox-labeler 不是「畫 bbox」的 → 它是「驗證 + 切分 + 組裝」
- agent 名字取「-labeler」其實有點 misleading，**真正在做的是 dataset prep**
- 學生會問：「那為什麼叫 labeler？」→ 因為原本計劃要用 OpenCV 自動畫 bbox，後來資料已有 bbox 就改驗證
- **這就是 agent 命名的真實困境**：一開始不知道最終職責

---

### Step 8：執行 training-runner（停下來等使用者）（20 分鐘）

#### 講師說
> 「最關鍵的一步：訓練。
> 我們在 agent 寫了一條規則：**訓練前要顯示預估時間並等使用者 GO**。
> 看看 Claude 會不會遵守。」

#### 操作
> 開始訓練

#### 預期看到（學生會驚訝）
```
📊 訓練預估
- dataset: 286 張 train
- epochs: 50, batch: 8 → iterations ≈ 1800
- 預估時間: 約 6–10 分鐘
- 輸出: Projects/2026-001-mvp/04-experiments/exp001/

要開始嗎？(請回 GO)
```

**Claude 停下來了。** 👈 這就是「人類在 loop」的具體表現。

#### 學生回 GO → 訓練開始

訓練過程中講師補充：
- 看 epoch 1 → epoch 50 的 loss/mAP 變化
- 解釋 `box_loss / cls_loss / dfl_loss` 是什麼
- 第一個 epoch 很慢（build MPS graph），後面穩定

#### 訓練完成（約 6–10 分鐘）
- best.pt 路徑
- 最終 mAP@0.5（單類 Donut，預期 0.7–0.95）

---

### Step 9：執行 inference-runner（10 分鐘）

#### 操作
> 用 inference-runner 跑 test set 推論，產出視覺化

#### 學生會看到
- 10 張 PNG，每張畫了預測 bbox + class + confidence
- 終端印出 test mAP
- `summary.md` 寫了觀察筆記

#### 教學收尾
> 「恭喜，你剛剛**沒寫一行 ML code**，完成了從資料下載到模型推論的完整 pipeline。
> 你寫的只是 4 個 markdown 檔，描述每個 agent 是誰、要做什麼。
> **這就是 sub-agent 的威力：你在指揮，agent 在執行。**」

---

### Phase 1 收尾（5 分鐘）

#### 回顧今天做了什麼
1. 建工作區骨架（CLAUDE.md + .claude/agents/）
2. 寫 4 個 sub-agent（每個 50 行 markdown）
3. Claude 自動路由 + 依序執行
4. 在訓練前停下來等人類確認
5. 產出可 demo 的結果

#### 學生會問的 3 個問題
**Q1：agent 之間怎麼傳資料？**
A：透過**檔案系統**。data-hunter 寫到 `01-raw-data/`，bbox-labeler 讀進去再寫到 `02-dataset/`。沒有 in-memory pipeline，這樣才能跨 session 接續。

**Q2：agent 可以平行跑嗎？**
A：可以，用 `dispatching-parallel-agents`。但今天的 4 個是**有依賴關係**的（要先有資料才能訓練），不能平行。

**Q3：怎麼 debug agent？**
A：看 agent 的回報訊息 + 看它寫的 script。記住 agent **不是黑箱**，它做的每件事都是檔案+指令。

---

## Phase 2：加入 evaluator agent（20 分鐘 demo）

### 講師說
> 「Phase 1 結束你有一個能跑的 pipeline，但**還不能自我改進**。
> 第一步：加一個 evaluator，自動分析訓練結果寫人話 report。」

### evaluator 的職責
讀 `04-experiments/exp001/`，產出 `evaluation.md`：
1. **訓練曲線健康度**（看 `results.csv`）
   - 是否 overfit（train loss ↓ 但 val mAP 停滯）
   - 是否還能 train 更多 epoch
2. **失敗案例**（看 confusion matrix）
   - 哪一類預測差？
   - 哪些 confidence 低？
3. **下一輪建議**（人話）
   - 「val mAP 在 epoch 30 就飽和，建議 epochs=30」
   - 「Donut 類別 small bbox 預測差，建議 imgsz=640」

### evaluator.md 骨架（現場寫）

```markdown
---
name: evaluator
description: 訓練完讀 results.csv + confusion matrix,寫一份「下一輪該怎麼改」的人話 report
tools: Read, Bash, Write, Glob
---

你是訓練分析師...

## 任務
讀 Projects/2026-001-mvp/04-experiments/exp001/,
產出 Projects/2026-001-mvp/04-experiments/exp001/evaluation.md

## 分析項目
1. 訓練曲線 (讀 results.csv)
2. 過擬合檢測 (train vs val mAP gap)
3. 失敗類別 (confusion matrix)
4. 下一輪建議 (3 條具體可執行)
```

### 教學重點
- evaluator **不訓練、不推論**，只讀 + 寫
- 它的輸出是給**人類**或**下一個 agent**（orchestrator）讀的
- 這是「**從工具型 agent → 分析型 agent**」的跳躍

---

## Phase 3：加入 hyper-tuner（20 分鐘 demo）

### 講師說
> 「現在我們讓 agent 自己跑多組實驗找最佳參數。
> 不再是『跑 1 次』而是『跑 N 次比一比』。」

### hyper-tuner 的職責
1. 讀 evaluator 的建議
2. 定義 search space（例如 lr ∈ [1e-4, 1e-2], imgsz ∈ {416, 640}）
3. 用 **Ultralytics 內建** `model.tune()` 或 **Optuna** 跑 N 個 trial
4. 每個 trial 跑短訓（10 epochs）
5. 挑最好的參數，回報

### 兩種實作法（講師選一個 demo）

**法 1：Ultralytics 內建 tune（最快上手）**
```python
model = YOLO("yolov8n.pt")
model.tune(data="data.yaml", epochs=10, iterations=10, optimizer="AdamW")
```

**法 2：Optuna（更彈性）**
```python
import optuna
def objective(trial):
    lr = trial.suggest_float("lr", 1e-4, 1e-2, log=True)
    imgsz = trial.suggest_categorical("imgsz", [416, 640])
    model = YOLO("yolov8n.pt")
    results = model.train(data=..., lr0=lr, imgsz=imgsz, epochs=10)
    return results.box.map50

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=10)
```

### hyper-tuner.md 骨架

```markdown
---
name: hyper-tuner
description: 跑超參數搜尋(HPO),找最佳 lr/imgsz/batch 組合
tools: Read, Write, Bash, Glob
---

## 任務
1. 讀 evaluator 的 evaluation.md
2. 從建議生成 search space
3. 跑 N 個 trial (每個 10 epochs)
4. 挑最好的,輸出 best_params.json

## 重要
- 跑 HPO 前**必須**讓使用者確認 (這會跑很久)
- 每個 trial 結果要寫進 experiments.md
```

### 教學重點
- HPO 是「Phase 2 → Phase 3 的質變」：從 1 次訓練變多次
- **token 成本和時間成本都會跳一級**，所以要使用者確認
- 學生會問：「那要跑幾個 trial？」→ Pareto 原則：先 5-10 個看趨勢，覺得有戲再加

---

## Phase 4：Orchestrator + 自我改進迴圈（20 分鐘概念）

### 講師說
> 「最後一個 phase 不一定要實作，但**一定要懂**。
> 這是『agent 團隊』vs.『agent 自我演化』的分水嶺。」

### Orchestrator 的職責
```
┌──────────────────────────────────────────────┐
│  orchestrator (大腦)                           │
│  - 讀 experiments.md (記憶所有過去 run)         │
│  - 決定下一步: 收資料? 換模型? 再 tune? 收手?   │
└──────────────────────────────────────────────┘
                  │
       ┌──────────┼─────────┬──────────┐
       ▼          ▼         ▼          ▼
   data-hunter  trainer  evaluator  hyper-tuner
       │          │         │          │
       └──────────┴────┬────┴──────────┘
                       ▼
              ┌─────────────────┐
              │ experiments.md  │  ← 唯一真相來源
              └─────────────────┘
```

### experiments.md（記憶 schema）

```markdown
# Experiment Log

## exp001 — 2026-05-12
- params: yolov8n, lr=0.01, imgsz=416, epochs=50
- mAP@0.5: 0.85
- 觀察: val 在 epoch 30 飽和
- 下一步: 減 epochs, 試 imgsz=640

## exp002 — 2026-05-12 (orchestrator 決策)
- params: yolov8n, lr=0.01, imgsz=640, epochs=30
- mAP@0.5: 0.88 ⬆️
- 觀察: small bbox 召回變好
- 下一步: 試 yolov8s 看是否更好

## exp003 — ...
```

### 自我改進迴圈的本質

```python
while not converged:
    plan = orchestrator.read(experiments_md).decide_next()
    if plan.action == "train": result = trainer(plan.params)
    if plan.action == "tune":  result = hyper_tuner(plan.search_space)
    if plan.action == "audit": result = evaluator(latest_exp)
    if plan.action == "stop":  break
    write_to(experiments_md, result)
```

### 教學重點
- **記憶（experiments.md）是核心**，沒有記憶就沒有自我改進
- Orchestrator **本身就是一個 agent**，只是它的 tools 是「呼叫別的 agent」
- 真實世界 Claude Code 還沒原生支援 agent-call-agent，需要用**外部 driver script** 或 **workflow tool**（如 LangGraph、Vercel Workflow）來驅動

### 進階提問（給工程師同行）
- Q：這跟 AutoML（如 Google Vertex AI AutoML）差在哪？
- A：AutoML 是黑箱、固定 search space。Agent 團隊是**可解釋、可干預、可擴展**。你可以隨時插一個「-看一下這次的圖」agent。

- Q：成本怎麼控制？
- A：Phase 4 跑起來很燒 token。實務上 orchestrator 應該有 budget cap，跑超過就停。

---

## 課程後續（給學生帶走）

### 作業（選一個做）
1. **改資料源**：找 Roboflow 上另一個多類別 wafer 資料集，重跑 4-agent
2. **加 evaluator**：自己寫 evaluator.md 並產 evaluation.md
3. **加一個 deploy-agent**：把 best.pt 包成 FastAPI 服務
4. **改領域**：把 4-agent 改成「PCB 瑕疵偵測」或「醫療影像分類」

### 進階閱讀
- Anthropic 官方 sub-agent 文件
- Ultralytics YOLOv8 tune 文件
- Optuna 文件
- 真實世界 ML pipeline 工具：MLflow、Weights & Biases、ClearML

---

## 講師備忘錄（常見卡點）

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `ROBOFLOW_API_KEY unauthorized` | key 沒設或設錯位置 | 檢查 `.env` 位置與內容，`load_dotenv()` 是否載到 |
| `roboflow project not found` | workspace/project name 拼錯 | 用 SDK 列 workspace 下所有 project |
| MPS 不支援某 op | PyTorch + Apple Silicon 限制 | `export PYTORCH_ENABLE_MPS_FALLBACK=1` |
| 訓練爆 RAM | batch 太大 | batch 8 → 4 |
| Roboflow 下載卡在 0% | overwrite=False + 資料夾已存在 | `Version.download(..., overwrite=True)` |
| `uv run` 找不到套件 | uv 隔離環境 vs. .venv 衝突 | 統一用 `uv add`（會更新 pyproject.toml） |
| Claude 沒呼叫 sub-agent | description 寫太短或太籠統 | 改成「當使用者要 X、要 Y、要 Z 時使用」 |
| Sub-agent 跑到一半停 | tools 不夠或卡在權限確認 | 檢查 frontmatter `tools:` 區段 |

---

## 教學節奏建議

| 時間 | 內容 | 重點 |
|---|---|---|
| 0–5 | 開場 + 分層說明 | 讓學生知道今天會走到哪 |
| 5–15 | Step 1-3 環境 | 別花太久，課前準備好 |
| 15–35 | Step 4 第一個 agent ⭐ | 全課最重要 20 分鐘 |
| 35–50 | Step 5 剩下 3 個 agents | 加速、講邊界 |
| 50–55 | Step 6 data-hunter 執行 | 故意讓學生看到「真實資料的混亂」 |
| 55–60 | Step 7 bbox-labeler | 講 agent 命名的真實困境 |
| 60–80 | Step 8 訓練 + 等使用者 GO | 講「人類在 loop」 |
| 80–90 | Step 9 推論 + 收尾 | 看 10 張 PNG 收尾 |
| 90–110 | Phase 2 evaluator demo | |
| 110–130 | Phase 3 hyper-tuner demo | |
| 130–150 | Phase 4 orchestrator 概念 | |

---

## 一句話總結

> **Sub-agent 不是讓 AI 變更聰明，是讓你把複雜任務拆得夠細，AI 才有能力一塊一塊把它做完。**

---

_Last updated: 2026-05-12_
_Maintainer: Kevin (kevin@legalsign.ai)_
