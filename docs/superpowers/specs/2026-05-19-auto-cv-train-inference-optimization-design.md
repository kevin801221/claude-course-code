# 設計文件：auto-cv-train-inference-optimization

> 日期：2026-05-19
> 作者：Kevin（with Claude）
> 狀態：待 review

## 1. 目標與定位

把現有的「wafer 瑕疵偵測 4-agent 教學 demo」重構成一個**通用 CV 自動訓練模板**，上傳到個人 GitHub（`kevin801221`，public）做為爆款開源模板。

一句話定位：

> **auto-cv-train-inference-optimization** — 改一個 YAML，一行指令把任何 Roboflow 資料集自動跑完「下載 → 驗證切分 → 訓練 → 超參優化 → 推論視覺化」；或者直接跟 Claude Code 對話，5 個專家 agent 自動接力做完。半導體晶圓瑕疵偵測（mAP@0.5 = 0.99）當內建 showcase。

爆款鉤子 = **雙介面**：純 CLI 一條龍 + 跟 AI agent 對話兩種都能跑完整 ML pipeline。

## 2. 鎖定決策（brainstorming 結論）

| 決策點 | 結論 |
|---|---|
| 定位 | 通用 CV 自動訓練模板（wafer 當 showcase） |
| README 語言 | 中英雙語同頁 |
| 成果展示 | 附 10 張推論成果圖 + mAP 數字，**不附**權重 |
| 通用化深度 | 完整 CLI 深重構（套件化） |
| CLI 框架 | typer |
| Repo 名稱 | `auto-cv-train-inference-optimization`（個人帳號 public） |
| optimization 含意 | 真實階段：超參優化（Ultralytics tuner） |

## 3. 系統架構

### 3.1 套件結構（src-layout）

```
auto-cv-train-inference-optimization/   ← 全新獨立 repo（教學 repo git 外）
├── README.md                  雙語同頁：badges + 30秒 quickstart + 成果展示 + 架構圖 + BYO dataset
├── LICENSE                    MIT（著作權人：Kevin Luo）
├── pyproject.toml             套件化 + console_scripts: autocv = "autocv.cli:app"
├── uv.lock
├── .python-version            3.11
├── .env.example               ROBOFLOW_API_KEY=
├── .gitignore                 .env .venv/ data/ runs/ *.pt __pycache__ .DS_Store
├── configs/
│   ├── wafer.yaml             內建 showcase 設定（指向 WM-811K v3）
│   └── template.yaml          空白範本（逐行註解，使用者複製改）
├── src/autocv/
│   ├── __init__.py
│   ├── __main__.py            python -m autocv → cli.app()
│   ├── cli.py                 typer app：data / split / train / optimize / infer / all
│   ├── config.py              dataclass 載入 + 驗證 YAML
│   ├── device.py              device: auto → mps → cuda → cpu 自動挑
│   ├── data.py                Roboflow 下載（由 download_dataset.py 通用化）
│   ├── split.py               驗證標註 + 切 70/20/10 + 產 data.yaml（由 split_dataset.py 通用化）
│   ├── train.py               YOLO 訓練（MPS 預設、預估時間 GO-gate、--yes 跳過）
│   ├── optimize.py            Ultralytics model.tune() 超參搜尋 → 最佳超參 + 最終模型
│   └── infer.py               推論 + N 張 bbox PNG + summary.md
├── .claude/agents/            5 個 agent（讀 config、非 wafer 寫死）
│   ├── data-hunter.md
│   ├── bbox-labeler.md
│   ├── training-runner.md
│   ├── hp-optimizer.md        ← 新增
│   └── inference-runner.md
├── CLAUDE.md                  通用模板的 Claude Code 指南（無 wafer/公開課字樣）
├── docs/
│   ├── architecture.md        pipeline 圖 + 資料流 + 設計理念
│   └── results/               showcase：10 張預測 PNG + summary.md（wafer，~3MB）
├── examples/wafer/            showcase 說明（如何重現 0.99 mAP）
└── .github/workflows/ci.yml   ruff lint + autocv --help smoke test（綠勾 badge）
```

### 3.2 CLI 指令介面

| 指令 | 行為 | 對應 agent |
|---|---|---|
| `autocv data -c configs/wafer.yaml` | 從 Roboflow 下載到 `data/raw/` | data-hunter |
| `autocv split -c ...` | 驗證標註 + 切 70/20/10 + 產 `data/processed/data.yaml` | bbox-labeler |
| `autocv train -c ...` | 單次 YOLO 訓練（預設報預估時間等確認，`--yes` 跳過） | training-runner |
| `autocv optimize -c ... [--iterations N]` | Ultralytics tuner 跨 lr/momentum/augment 等搜尋 → 輸出最佳超參 + 用最佳超參訓練最終模型 | hp-optimizer |
| `autocv infer -c ...` | 推論 + N 張 bbox PNG + `summary.md` | inference-runner |
| `autocv all -c ... [--optimize] [--yes]` | 一條龍：data→split→train→infer；加 `--optimize` 則用 optimize 取代 train | — |

設計原則：`optimize` 很貴（跑 N 輪訓練），預設**不**進 `all`，要顯式 `--optimize`。`train` 與 `optimize` 互斥（兩者都產出 `runs/<name>/weights/best.pt` 給 infer 用）。

### 3.3 config.yaml 結構

```yaml
roboflow:
  workspace: wm811k-paasr      # Roboflow workspace slug
  project: wm811k              # Roboflow project slug
  version: 3                   # dataset version
  format: yolov8               # 下載格式
  api_key_env: ROBOFLOW_API_KEY  # 從哪個環境變數讀 key

dataset:
  split: [0.7, 0.2, 0.1]       # train/val/test 比例（原始已切分則沿用）
  seed: 42

train:
  model: yolov8n.pt
  epochs: 50
  batch: 8
  imgsz: 416
  device: auto                 # auto → mps→cuda→cpu

optimize:
  iterations: 20               # tuner 搜尋輪數
  epochs: 15                   # 每輪短訓 epochs

infer:
  conf: 0.25
  num_samples: 10
```

換資料集 = 只改 `configs/template.yaml` 複製一份。所有路徑用 `pathlib.Path`，相對於 repo root。

### 3.4 資料流

```
configs/*.yaml ──┐
                 ▼
ROBOFLOW_API_KEY → [data]  → data/raw/
                              │
                              ▼
                   [split] → data/processed/{images,labels}/{train,val,test}/ + data.yaml
                              │
                ┌─────────────┴──────────────┐
                ▼                             ▼
          [train]                      [optimize]
       runs/exp/weights/best.pt    runs/tune/weights/best.pt + best_hyperparameters.yaml
                └─────────────┬──────────────┘
                              ▼
                          [infer] → runs/infer/pred_*.png ×N + summary.md
```

### 3.5 安全設計（保留並升級 GO-gate）

`train` 與 `optimize` 預設先印出預估時間並停下來等使用者輸入確認（typer `confirm`），`--yes` 跳過。README 主打「不會偷偷燒你的 GPU/電費」這個負責任 AI 訓練設計，做為差異化賣點。

## 4. 元件職責（單一職責、可獨立測試）

| 模組 | 職責 | 依賴 | 介面 |
|---|---|---|---|
| `config.py` | 載入+驗證 YAML，回傳 typed config 物件 | pyyaml | `load_config(path) -> Config` |
| `device.py` | 自動挑 device，設 MPS fallback env | torch | `pick_device(pref) -> str` |
| `data.py` | Roboflow 下載 | roboflow, config | `download(cfg) -> Path` |
| `split.py` | 驗證標註 + 切分 + 產 data.yaml | pyyaml, config | `split(cfg) -> Path` |
| `train.py` | 單次訓練 | ultralytics, config, device | `train(cfg, yes) -> Path` |
| `optimize.py` | 超參搜尋 + 最終訓練 | ultralytics, config, device | `optimize(cfg, yes) -> Path` |
| `infer.py` | 推論 + 視覺化 + summary | ultralytics, matplotlib, config | `infer(cfg) -> Path` |
| `cli.py` | typer 指令路由 | 上述全部 | `app` |

每個模組可獨立 import 測試，不靠全域狀態，路徑全來自 config。

## 5. 上傳 / 排除清單

**上傳**：全部 `src/`、`configs/`、`.claude/agents/`（5 個）、`CLAUDE.md`（改寫）、`README.md`、`LICENSE`、`.env.example`、`.gitignore`、`pyproject.toml`、`uv.lock`、`.python-version`、`docs/`（含 10 張成果 PNG + summary）、`examples/wafer/`、`.github/workflows/ci.yml`

**排除**：`.env`、`.venv/`、`data/`（21MB wafer 原圖）、`*.pt` 權重（5.9MB×2）、`runs/`、`__pycache__/`、`.DS_Store`、教學專用 `WALKTHROUGH.md`、`_Context/`、原 `main.py`、`Projects/2026-001-mvp/`（除 `05-results/` 的 10 張預測 PNG + summary.md → 複製進 `docs/results/`）

## 6. Git 與上傳流程

1. 新 repo 建在教學 repo **外面**：`/Users/kevinluo/auto-cv-train-inference-optimization/`（獨立 git，不污染教學 repo 歷史）
2. `git init`、`git config user.name/email` 走個人帳號 `kevin801221`
3. `gh repo create kevin801221/auto-cv-train-inference-optimization --public`
4. remote 用 SSH alias：`git@github-personal:kevin801221/auto-cv-train-inference-optimization.git`
5. 首 commit（繁中、commit-zh 風格、不署名 Claude Code）後 push `main`

## 7. 測試策略

- `tests/test_config.py`：載入 wafer.yaml / template.yaml 不報錯，缺欄位有明確錯誤
- `tests/test_device.py`：`pick_device("auto")` 在無 GPU 時回 `cpu`，不崩
- `tests/test_split_validate.py`：餵合法 / 非法 YOLO label 行，驗證錯誤偵測正確（沿用現有 `validate_label_file` 邏輯）
- CI：`ruff check` + `autocv --help` + pytest（不含需 GPU/網路的 data/train/infer）
- 不在 CI 跑真實下載/訓練（需 API key + GPU + 時間）

## 8. 已知限制（YAGNI 邊界）

- 只支援 YOLOv8（Ultralytics）+ Roboflow 來源；不做多框架抽象層
- `optimize` 用 Ultralytics 內建 tuner，不自建 Optuna/Ray 整合
- 不做模型匯出/量化（CoreML/ONNX）—— 留待未來，本版不含
- 不做 web UI / dashboard
- CI 不跑真實訓練

## 9. 風險與緩解

| 風險 | 緩解 |
|---|---|
| 誤把教學 repo 整包 push | 新 repo 建在教學 repo 外，獨立 git init |
| .env 含 API key 外洩 | .gitignore 第一條排除 + push 前 grep 掃描確認無 key |
| 成果圖讓 repo 過大 | 僅 10 張 PNG ~3MB，可接受；不附 5.9MB 權重 |
| 帳號搞錯（個人/工作） | 已確認個人 `kevin801221` + SSH alias `git@github-personal:` |
| Roboflow workspace 失效讓 quickstart 跑不動 | README 標明「showcase 用公開 WM-811K，BYO dataset 改 config」並附 mAP 佐證 |
