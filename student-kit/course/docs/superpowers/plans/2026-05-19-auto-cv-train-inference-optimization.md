# auto-cv-train-inference-optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把現有 wafer 4-agent 教學 demo 重構成通用 CV 自動訓練模板 `auto-cv-train-inference-optimization`，建成獨立 repo 並 push 到 `kevin801221` 個人 GitHub（public）。

**Architecture:** src-layout Python 套件 `autocv`，typer CLI 五子命令（data/split/train/optimize/infer + all），config.yaml 驅動，5 個 Claude Code agent 為第二介面。新 repo 建在教學 repo 外，獨立 git 歷史。

**Tech Stack:** Python 3.11, uv, typer, ultralytics(YOLOv8), roboflow, pyyaml, torch(MPS), matplotlib, pytest, ruff, GitHub Actions, gh CLI。

---

## 重要常數

- **來源資料夾**（讀取舊檔）：`/Users/kevinluo/claude-code-complete-tutorial/agent_group_projects/computer-vision-wafer-agents-detection-demo`（以下簡稱 `$SRC`）
- **新 repo 根目錄**：`/Users/kevinluo/auto-cv-train-inference-optimization`（以下簡稱 `$REPO`）
- **GitHub**：`kevin801221/auto-cv-train-inference-optimization`，public，remote `git@github-personal:kevin801221/auto-cv-train-inference-optimization.git`
- **git 身分**：`user.name=kevin801221`、`user.email=kevin801221@users.noreply.github.com`，commit 不署名 AI、繁中訊息
- 所有 `autocv` 指令在 `$REPO` 根目錄執行；專案路徑 = `Path.cwd()`

## File Structure

```
$REPO/
├── pyproject.toml              套件 metadata + [project.scripts] autocv
├── .python-version             3.11
├── .gitignore                  排除 .env .venv data/ runs/ *.pt 等
├── .env.example                ROBOFLOW_API_KEY=
├── LICENSE                     MIT
├── README.md                   中英雙語同頁
├── CLAUDE.md                   通用模板 Claude Code 指南
├── configs/
│   ├── wafer.yaml              showcase 設定
│   └── template.yaml           空白範本（逐行註解）
├── src/autocv/
│   ├── __init__.py             版本字串
│   ├── __main__.py             python -m autocv
│   ├── config.py               dataclass + load_config + 驗證
│   ├── device.py               pick_device
│   ├── data.py                 download
│   ├── split.py                validate_label_file + split
│   ├── train.py                train
│   ├── optimize.py             optimize
│   ├── infer.py                infer
│   └── cli.py                  typer app
├── tests/
│   ├── test_config.py
│   ├── test_device.py
│   ├── test_split_validate.py
│   └── test_cli.py
├── .claude/agents/             5 個 agent .md
│   ├── data-hunter.md
│   ├── bbox-labeler.md
│   ├── training-runner.md
│   ├── hp-optimizer.md
│   └── inference-runner.md
├── docs/
│   ├── architecture.md
│   └── results/                10 張 pred_*.png + summary.md
├── examples/wafer/README.md
└── .github/workflows/ci.yml
```

---

### Task 1: 建立 repo 骨架與 git

**Files:**
- Create: `$REPO/` 目錄樹、`.python-version`、`.gitignore`、`.env.example`

- [ ] **Step 1: 建目錄結構**

```bash
mkdir -p /Users/kevinluo/auto-cv-train-inference-optimization/{src/autocv,tests,configs,.claude/agents,docs/results,examples/wafer,.github/workflows}
cd /Users/kevinluo/auto-cv-train-inference-optimization
```

- [ ] **Step 2: git init + 身分**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git init -b main
git config user.name "kevin801221"
git config user.email "kevin801221@users.noreply.github.com"
```

- [ ] **Step 3: 寫 `.python-version`**

檔案 `$REPO/.python-version` 內容（單行）：

```
3.11
```

- [ ] **Step 4: 寫 `.gitignore`**

檔案 `$REPO/.gitignore`：

```gitignore
# secrets
.env
*.pem
credentials.json

# python
__pycache__/
*.py[cod]
.venv/
*.egg-info/
.pytest_cache/
.ruff_cache/

# ML artifacts
data/
runs/
*.pt
*.onnx

# os
.DS_Store
```

- [ ] **Step 5: 寫 `.env.example`**

檔案 `$REPO/.env.example`：

```
# Roboflow API key — 從 https://app.roboflow.com/settings/api 取得
ROBOFLOW_API_KEY=
```

- [ ] **Step 6: Commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git add .python-version .gitignore .env.example
git commit -m "初始化 repo 骨架與 .gitignore"
```

---

### Task 2: pyproject.toml 與套件 metadata

**Files:**
- Create: `$REPO/pyproject.toml`, `$REPO/src/autocv/__init__.py`

- [ ] **Step 1: 寫 `pyproject.toml`**

檔案 `$REPO/pyproject.toml`：

```toml
[project]
name = "auto-cv-train-inference-optimization"
version = "0.1.0"
description = "改一個 YAML，一行指令把任何 Roboflow 資料集自動跑完 下載→驗證切分→訓練→超參優化→推論視覺化。"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [{ name = "Kevin Luo" }]
dependencies = [
    "typer>=0.15.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "roboflow>=1.3.8",
    "ultralytics>=8.4.48",
    "matplotlib>=3.8",
    "pillow>=10.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.6"]

[project.scripts]
autocv = "autocv.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/autocv"]

[tool.ruff]
line-length = 100
target-version = "py311"
```

- [ ] **Step 2: 寫 `src/autocv/__init__.py`**

檔案 `$REPO/src/autocv/__init__.py`：

```python
"""auto-cv-train-inference-optimization: 通用 CV 自動訓練模板。"""

__version__ = "0.1.0"
```

- [ ] **Step 3: 建立環境並驗證可裝**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
uv venv --python 3.11
uv pip install -e ".[dev]"
```

Expected: 安裝成功，無錯誤。

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml src/autocv/__init__.py
git commit -m "加 pyproject 套件設定與 autocv console script"
```

---

### Task 3: config.py（TDD）

**Files:**
- Create: `$REPO/src/autocv/config.py`, `$REPO/tests/test_config.py`, `$REPO/configs/wafer.yaml`

- [ ] **Step 1: 寫 `configs/wafer.yaml`（測試需要）**

檔案 `$REPO/configs/wafer.yaml`：

```yaml
roboflow:
  workspace: wm811k-paasr
  project: wm811k
  version: 3
  format: yolov8
  api_key_env: ROBOFLOW_API_KEY

paths:
  raw: data/raw
  processed: data/processed
  runs: runs

dataset:
  split: [0.7, 0.2, 0.1]
  seed: 42

train:
  model: yolov8n.pt
  epochs: 50
  batch: 8
  imgsz: 416
  device: auto

optimize:
  iterations: 20
  epochs: 15

infer:
  conf: 0.25
  num_samples: 10
```

- [ ] **Step 2: 寫失敗測試 `tests/test_config.py`**

```python
from pathlib import Path

import pytest

from autocv.config import Config, load_config

WAFER = Path("configs/wafer.yaml")


def test_load_wafer_config():
    cfg = load_config(WAFER)
    assert isinstance(cfg, Config)
    assert cfg.roboflow.workspace == "wm811k-paasr"
    assert cfg.roboflow.version == 3
    assert cfg.dataset.split == [0.7, 0.2, 0.1]
    assert cfg.train.model == "yolov8n.pt"
    assert cfg.optimize.iterations == 20
    assert cfg.infer.num_samples == 10
    assert cfg.paths.raw == "data/raw"


def test_split_must_sum_to_one():
    with pytest.raises(ValueError, match="split"):
        Config.from_dict(
            {
                "roboflow": {"workspace": "w", "project": "p", "version": 1},
                "dataset": {"split": [0.5, 0.2, 0.1]},
            }
        )


def test_missing_roboflow_section_raises():
    with pytest.raises(ValueError, match="roboflow"):
        Config.from_dict({"dataset": {"split": [0.7, 0.2, 0.1]}})
```

- [ ] **Step 3: 跑測試確認失敗**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_config.py -v`
Expected: FAIL（`ModuleNotFoundError: autocv.config`）

- [ ] **Step 4: 實作 `src/autocv/config.py`**

```python
"""載入並驗證 config.yaml。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class RoboflowCfg:
    workspace: str
    project: str
    version: int
    format: str = "yolov8"
    api_key_env: str = "ROBOFLOW_API_KEY"


@dataclass
class PathsCfg:
    raw: str = "data/raw"
    processed: str = "data/processed"
    runs: str = "runs"


@dataclass
class DatasetCfg:
    split: list[float] = field(default_factory=lambda: [0.7, 0.2, 0.1])
    seed: int = 42


@dataclass
class TrainCfg:
    model: str = "yolov8n.pt"
    epochs: int = 50
    batch: int = 8
    imgsz: int = 416
    device: str = "auto"


@dataclass
class OptimizeCfg:
    iterations: int = 20
    epochs: int = 15


@dataclass
class InferCfg:
    conf: float = 0.25
    num_samples: int = 10


@dataclass
class Config:
    roboflow: RoboflowCfg
    paths: PathsCfg = field(default_factory=PathsCfg)
    dataset: DatasetCfg = field(default_factory=DatasetCfg)
    train: TrainCfg = field(default_factory=TrainCfg)
    optimize: OptimizeCfg = field(default_factory=OptimizeCfg)
    infer: InferCfg = field(default_factory=InferCfg)

    @classmethod
    def from_dict(cls, raw: dict) -> Config:
        if "roboflow" not in raw:
            raise ValueError("config 缺少 roboflow 區塊")
        rf = RoboflowCfg(**raw["roboflow"])
        dataset = DatasetCfg(**raw.get("dataset", {}))
        if abs(sum(dataset.split) - 1.0) > 1e-6 or len(dataset.split) != 3:
            raise ValueError("dataset.split 必須是 3 個和為 1 的比例")
        return cls(
            roboflow=rf,
            paths=PathsCfg(**raw.get("paths", {})),
            dataset=dataset,
            train=TrainCfg(**raw.get("train", {})),
            optimize=OptimizeCfg(**raw.get("optimize", {})),
            infer=InferCfg(**raw.get("infer", {})),
        )


def load_config(path: str | Path) -> Config:
    """讀 YAML 檔並回傳驗證過的 Config。"""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"找不到 config: {path}")
    return Config.from_dict(yaml.safe_load(path.read_text()))
```

- [ ] **Step 5: 跑測試確認通過**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_config.py -v`
Expected: 3 passed

- [ ] **Step 6: Commit**

```bash
git add src/autocv/config.py tests/test_config.py configs/wafer.yaml
git commit -m "加 config 模組：dataclass 載入與驗證 + wafer showcase 設定"
```

---

### Task 4: device.py（TDD）

**Files:**
- Create: `$REPO/src/autocv/device.py`, `$REPO/tests/test_device.py`

- [ ] **Step 1: 寫失敗測試 `tests/test_device.py`**

```python
from autocv.device import pick_device


def test_explicit_device_passthrough():
    assert pick_device("cpu") == "cpu"
    assert pick_device("mps") == "mps"


def test_auto_returns_valid_device(monkeypatch):
    import autocv.device as d

    monkeypatch.setattr(d, "_mps_available", lambda: False)
    monkeypatch.setattr(d, "_cuda_available", lambda: False)
    assert pick_device("auto") == "cpu"

    monkeypatch.setattr(d, "_mps_available", lambda: True)
    assert pick_device("auto") == "mps"
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_device.py -v`
Expected: FAIL（`ModuleNotFoundError: autocv.device`）

- [ ] **Step 3: 實作 `src/autocv/device.py`**

```python
"""自動挑選運算裝置：auto → mps → cuda → cpu。"""

from __future__ import annotations

import os


def _mps_available() -> bool:
    try:
        import torch

        return torch.backends.mps.is_available()
    except Exception:
        return False


def _cuda_available() -> bool:
    try:
        import torch

        return torch.cuda.is_available()
    except Exception:
        return False


def pick_device(pref: str = "auto") -> str:
    """pref 非 auto 時原樣回傳；auto 時 mps→cuda→cpu 依序挑。"""
    if pref != "auto":
        return pref
    if _mps_available():
        os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
        return "mps"
    if _cuda_available():
        return "cuda"
    return "cpu"
```

- [ ] **Step 4: 跑測試確認通過**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_device.py -v`
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add src/autocv/device.py tests/test_device.py
git commit -m "加 device 模組：auto 自動挑 mps/cuda/cpu"
```

---

### Task 5: split.py 標註驗證邏輯（TDD）

**Files:**
- Create: `$REPO/src/autocv/split.py`, `$REPO/tests/test_split_validate.py`

- [ ] **Step 1: 寫失敗測試 `tests/test_split_validate.py`**

```python
from autocv.split import validate_label_file


def test_valid_label(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("0 0.5 0.5 0.2 0.2\n1 0.1 0.1 0.05 0.05\n")
    errors, cids, n = validate_label_file(f)
    assert errors == []
    assert cids == [0, 1]
    assert n == 2


def test_missing_file(tmp_path):
    errors, cids, n = validate_label_file(tmp_path / "nope.txt")
    assert len(errors) == 1
    assert n == 0


def test_out_of_range_and_bad_fields(tmp_path):
    f = tmp_path / "b.txt"
    f.write_text("0 1.5 0.5 0.2 0.2\n0 0.5 0.5\n-1 0.5 0.5 0.2 0.2\n")
    errors, cids, n = validate_label_file(f)
    assert any("超出" in e for e in errors)
    assert any("欄位數" in e for e in errors)
    assert any("為負" in e for e in errors)
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_split_validate.py -v`
Expected: FAIL（`ModuleNotFoundError: autocv.split`）

- [ ] **Step 3: 實作 `src/autocv/split.py`**

```python
"""驗證 YOLO 標註並切分 train/val/test，產生 data.yaml。"""

from __future__ import annotations

import random
import shutil
from collections import Counter
from pathlib import Path

import yaml

from autocv.config import Config

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def validate_label_file(label_path: Path) -> tuple[list[str], list[int], int]:
    """回傳 (errors, class_ids, bbox_count)。"""
    errors: list[str] = []
    class_ids: list[int] = []
    bbox_count = 0
    if not label_path.exists():
        return [f"{label_path.name}: 缺少 label 檔"], class_ids, 0
    for lineno, raw in enumerate(label_path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 5:
            errors.append(f"{label_path.name}:L{lineno} 欄位數 != 5")
            continue
        try:
            cid = int(parts[0])
            cx, cy, w, h = (float(x) for x in parts[1:])
        except ValueError:
            errors.append(f"{label_path.name}:L{lineno} 解析失敗")
            continue
        if cid < 0:
            errors.append(f"{label_path.name}:L{lineno} class_id 為負")
        for name, val in (("cx", cx), ("cy", cy), ("w", w), ("h", h)):
            if not (0.0 <= val <= 1.0):
                errors.append(f"{label_path.name}:L{lineno} {name}={val} 超出 [0,1]")
        class_ids.append(cid)
        bbox_count += 1
    return errors, class_ids, bbox_count


def _find_src(raw_dir: Path) -> tuple[Path, Path, Path]:
    """找出 raw 下的 images / labels / data.yaml（相容 train/ 子層）。"""
    for base in (raw_dir, raw_dir / "train"):
        img_dir = base / "images"
        lbl_dir = base / "labels"
        if img_dir.is_dir() and lbl_dir.is_dir():
            yaml_path = raw_dir / "data.yaml"
            return img_dir, lbl_dir, yaml_path
    raise FileNotFoundError(f"{raw_dir} 下找不到 images/ 與 labels/，請先跑 autocv data")


def split(cfg: Config, root: Path) -> Path:
    """執行驗證 + 切分，回傳 processed/data.yaml 路徑。"""
    raw_dir = root / cfg.paths.raw
    out_dir = root / cfg.paths.processed
    img_dir, lbl_dir, raw_yaml = _find_src(raw_dir)

    raw_cfg = yaml.safe_load(raw_yaml.read_text())
    names = raw_cfg["names"]
    nc = raw_cfg["nc"]

    images = sorted(p for p in img_dir.iterdir() if p.suffix.lower() in IMG_EXTS)
    print(f"圖片總數: {len(images)}")

    all_errors: list[str] = []
    class_counter: Counter[int] = Counter()
    total_bbox = 0
    empty_labels = 0
    paired: list[tuple[Path, Path]] = []
    for img in images:
        lbl = lbl_dir / f"{img.stem}.txt"
        errors, cids, bcount = validate_label_file(lbl)
        all_errors.extend(errors)
        class_counter.update(cids)
        total_bbox += bcount
        if bcount == 0:
            empty_labels += 1
        if lbl.exists():
            paired.append((img, lbl))

    print(f"label 配對成功: {len(paired)}  bbox 總數: {total_bbox}  空 label: {empty_labels}")
    print(f"類別分佈: {dict(class_counter)}  異常行數: {len(all_errors)}")
    for e in all_errors[:5]:
        print(f"  - {e}")

    if total_bbox and len(all_errors) / total_bbox > 0.1:
        raise SystemExit(f"格式錯誤比例 > 10%（{len(all_errors)}/{total_bbox}），中止")

    rng = random.Random(cfg.dataset.seed)
    shuffled = paired.copy()
    rng.shuffle(shuffled)
    n = len(shuffled)
    n_train = int(n * cfg.dataset.split[0])
    n_val = int(n * cfg.dataset.split[1])
    splits = {
        "train": shuffled[:n_train],
        "val": shuffled[n_train : n_train + n_val],
        "test": shuffled[n_train + n_val :],
    }
    for s in splits:
        (out_dir / "images" / s).mkdir(parents=True, exist_ok=True)
        (out_dir / "labels" / s).mkdir(parents=True, exist_ok=True)
    for s, items in splits.items():
        for img, lbl in items:
            shutil.copy2(img, out_dir / "images" / s / img.name)
            shutil.copy2(lbl, out_dir / "labels" / s / lbl.name)
        print(f"{s}: {len(items)} 張")

    out_yaml = {
        "path": str(out_dir.resolve()),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "nc": nc,
        "names": {i: nm for i, nm in enumerate(names)} if isinstance(names, list) else names,
    }
    yaml_path = out_dir / "data.yaml"
    yaml_path.write_text(yaml.safe_dump(out_yaml, sort_keys=False, allow_unicode=True))
    print(f"data.yaml -> {yaml_path}")
    return yaml_path
```

- [ ] **Step 4: 跑測試確認通過**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_split_validate.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add src/autocv/split.py tests/test_split_validate.py
git commit -m "加 split 模組：標註驗證 + config 驅動切分"
```

---

### Task 6: data.py（Roboflow 下載）

**Files:**
- Create: `$REPO/src/autocv/data.py`

- [ ] **Step 1: 實作 `src/autocv/data.py`**

```python
"""從 Roboflow Universe 下載資料集到 paths.raw。"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from autocv.config import Config


def download(cfg: Config, root: Path) -> Path:
    """下載資料集，回傳下載目錄。"""
    load_dotenv(root / ".env")
    api_key = os.getenv(cfg.roboflow.api_key_env)
    if not api_key:
        raise RuntimeError(
            f"{cfg.roboflow.api_key_env} 未設定，請複製 .env.example 成 .env 並填入"
        )

    from roboflow import Roboflow

    dest = root / cfg.paths.raw
    dest.mkdir(parents=True, exist_ok=True)
    rf = Roboflow(api_key=api_key)
    project = rf.workspace(cfg.roboflow.workspace).project(cfg.roboflow.project)
    dataset = project.version(cfg.roboflow.version).download(
        cfg.roboflow.format, location=str(dest), overwrite=True
    )
    print(f"DOWNLOAD_OK: {dataset.location}")
    return Path(dataset.location)
```

- [ ] **Step 2: 驗證可 import**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run python -c "from autocv.data import download; print('ok')"`
Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add src/autocv/data.py
git commit -m "加 data 模組：config 驅動 Roboflow 下載"
```

---

### Task 7: train.py（含 GO-gate）

**Files:**
- Create: `$REPO/src/autocv/train.py`

- [ ] **Step 1: 實作 `src/autocv/train.py`**

```python
"""YOLOv8 訓練，預設先報預估時間並等使用者確認。"""

from __future__ import annotations

import math
import time
from pathlib import Path

import typer

from autocv.config import Config
from autocv.device import pick_device


def _count_train_imgs(processed: Path) -> int:
    d = processed / "images" / "train"
    if not d.is_dir():
        return 0
    return sum(1 for _ in d.iterdir())


def _estimate_minutes(n_imgs: int, epochs: int, batch: int) -> float:
    iters = math.ceil(max(n_imgs, 1) / batch) * epochs
    return iters * 0.2 / 60.0


def train(cfg: Config, root: Path, yes: bool = False) -> Path:
    """訓練並回傳 best.pt 路徑。"""
    data_yaml = root / cfg.paths.processed / "data.yaml"
    if not data_yaml.exists():
        raise SystemExit(f"找不到 {data_yaml}，請先跑 autocv split")

    device = pick_device(cfg.train.device)
    n_imgs = _count_train_imgs(root / cfg.paths.processed)
    est = _estimate_minutes(n_imgs, cfg.train.epochs, cfg.train.batch)
    typer.echo(
        f"📊 訓練預估\n"
        f"- train 圖片: {n_imgs}\n"
        f"- epochs={cfg.train.epochs} batch={cfg.train.batch} device={device}\n"
        f"- 預估時間: 約 {est:.1f} 分鐘\n"
        f"- 輸出: {root / cfg.paths.runs}/train/"
    )
    if not yes and not typer.confirm("要開始訓練嗎？"):
        raise typer.Abort()

    from ultralytics import YOLO

    t0 = time.time()
    model = YOLO(cfg.train.model)
    results = model.train(
        data=str(data_yaml),
        epochs=cfg.train.epochs,
        batch=cfg.train.batch,
        imgsz=cfg.train.imgsz,
        device=device,
        project=str(root / cfg.paths.runs),
        name="train",
        exist_ok=True,
    )
    best = Path(results.save_dir) / "weights" / "best.pt"
    typer.echo(f"耗時 {(time.time() - t0) / 60:.2f} 分鐘  best.pt -> {best}")
    return best
```

- [ ] **Step 2: 驗證可 import**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run python -c "from autocv.train import train; print('ok')"`
Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add src/autocv/train.py
git commit -m "加 train 模組：MPS 預設 + 預估時間 GO-gate"
```

---

### Task 8: optimize.py（超參搜尋）

**Files:**
- Create: `$REPO/src/autocv/optimize.py`

- [ ] **Step 1: 實作 `src/autocv/optimize.py`**

```python
"""Ultralytics 內建 tuner 做超參搜尋，回傳最佳結果目錄。"""

from __future__ import annotations

import time
from pathlib import Path

import typer

from autocv.config import Config
from autocv.device import pick_device


def optimize(cfg: Config, root: Path, yes: bool = False) -> Path:
    """跑超參搜尋並回傳 tune 結果目錄。"""
    data_yaml = root / cfg.paths.processed / "data.yaml"
    if not data_yaml.exists():
        raise SystemExit(f"找不到 {data_yaml}，請先跑 autocv split")

    device = pick_device(cfg.train.device)
    typer.echo(
        f"🔧 超參優化預估\n"
        f"- iterations={cfg.optimize.iterations} 每輪 epochs={cfg.optimize.epochs}\n"
        f"- device={device}（每輪都是一次短訓，總時間 ≈ iterations × 單輪）\n"
        f"- 輸出: {root / cfg.paths.runs}/tune/"
    )
    if not yes and not typer.confirm("要開始超參搜尋嗎？（很耗時）"):
        raise typer.Abort()

    from ultralytics import YOLO

    t0 = time.time()
    model = YOLO(cfg.train.model)
    model.tune(
        data=str(data_yaml),
        epochs=cfg.optimize.epochs,
        iterations=cfg.optimize.iterations,
        imgsz=cfg.train.imgsz,
        batch=cfg.train.batch,
        device=device,
        project=str(root / cfg.paths.runs),
        name="tune",
        exist_ok=True,
    )
    tune_dir = root / cfg.paths.runs / "tune"
    typer.echo(
        f"耗時 {(time.time() - t0) / 60:.2f} 分鐘\n"
        f"最佳超參 -> {tune_dir / 'best_hyperparameters.yaml'}"
    )
    return tune_dir
```

- [ ] **Step 2: 驗證可 import**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run python -c "from autocv.optimize import optimize; print('ok')"`
Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add src/autocv/optimize.py
git commit -m "加 optimize 模組：Ultralytics tuner 超參搜尋"
```

---

### Task 9: infer.py（推論 + 視覺化 + summary）

**Files:**
- Create: `$REPO/src/autocv/infer.py`

- [ ] **Step 1: 實作 `src/autocv/infer.py`**

```python
"""推論並產出帶 bbox 的視覺化 PNG 與 summary.md。"""

from __future__ import annotations

import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as patches  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

from autocv.config import Config  # noqa: E402
from autocv.device import pick_device  # noqa: E402


def _latest_best(runs: Path) -> Path:
    cands = sorted(runs.glob("*/weights/best.pt"), key=lambda p: p.stat().st_mtime)
    if not cands:
        raise SystemExit(f"{runs} 下找不到 best.pt，請先跑 autocv train 或 optimize")
    return cands[-1]


def infer(cfg: Config, root: Path) -> Path:
    """推論 + 視覺化，回傳輸出目錄。"""
    runs = root / cfg.paths.runs
    best = _latest_best(runs)
    processed = root / cfg.paths.processed
    test_dir = processed / "images" / "test"
    if not test_dir.is_dir() or not any(test_dir.iterdir()):
        test_dir = processed / "images" / "val"
        print("test/ 不存在或為空，改用 val/")

    out_dir = runs / "infer"
    out_dir.mkdir(parents=True, exist_ok=True)
    device = pick_device(cfg.train.device)

    from ultralytics import YOLO

    model = YOLO(str(best))
    random.seed(cfg.dataset.seed)
    imgs = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png"))
    sample = random.sample(imgs, min(cfg.infer.num_samples, len(imgs)))

    lines: list[str] = ["# Inference Summary\n", f"- 模型：`{best}`\n"]
    for img_path in sample:
        result = model.predict(str(img_path), conf=cfg.infer.conf, device=device)[0]
        img = Image.open(img_path)
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(img)
        if len(result.boxes) == 0:
            ax.set_title(f"{img_path.name} — No prediction")
        else:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cls = result.names[int(box.cls[0])]
                conf = float(box.conf[0])
                ax.add_patch(
                    patches.Rectangle(
                        (x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor="red", linewidth=2
                    )
                )
                ax.text(
                    x1,
                    y1 - 5,
                    f"{cls} {conf:.2f}",
                    color="white",
                    bbox=dict(facecolor="red", alpha=0.7),
                )
            ax.set_title(img_path.name)
        ax.axis("off")
        out_png = out_dir / f"pred_{img_path.name}.png"
        plt.savefig(out_png, dpi=100, bbox_inches="tight")
        plt.close()
        lines.append(f"![{out_png.stem}]({out_png.name})\n")

    data_yaml = processed / "data.yaml"
    try:
        metrics = model.val(data=str(data_yaml), split="test")
    except Exception:
        metrics = model.val(data=str(data_yaml), split="val")
    lines.insert(
        2,
        f"- mAP@0.5: {metrics.box.map50:.4f}  mAP@0.5:0.95: {metrics.box.map:.4f}\n",
    )
    (out_dir / "summary.md").write_text("\n".join(lines))
    print(f"summary.md -> {out_dir / 'summary.md'}")
    print(f"mAP@0.5: {metrics.box.map50:.4f}  mAP@0.5:0.95: {metrics.box.map:.4f}")
    return out_dir
```

- [ ] **Step 2: 驗證可 import**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run python -c "from autocv.infer import infer; print('ok')"`
Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add src/autocv/infer.py
git commit -m "加 infer 模組：推論 + bbox 視覺化 + summary"
```

---

### Task 10: cli.py + __main__.py（typer app）

**Files:**
- Create: `$REPO/src/autocv/cli.py`, `$REPO/src/autocv/__main__.py`

- [ ] **Step 1: 實作 `src/autocv/cli.py`**

```python
"""autocv CLI：data / split / train / optimize / infer / all。"""

from __future__ import annotations

from pathlib import Path

import typer

from autocv import __version__
from autocv.config import load_config

app = typer.Typer(
    add_completion=False,
    help="改一個 YAML，一行指令跑完整 CV pipeline：data→split→train→optimize→infer。",
)

ConfigOpt = typer.Option("configs/wafer.yaml", "-c", "--config", help="config.yaml 路徑")
YesOpt = typer.Option(False, "--yes", "-y", help="跳過訓練前確認")


def _ctx(config: str) -> tuple:
    root = Path.cwd()
    return load_config(config), root


@app.command()
def version() -> None:
    """印出版本。"""
    typer.echo(f"autocv {__version__}")


@app.command()
def data(config: str = ConfigOpt) -> None:
    """從 Roboflow 下載資料集。"""
    from autocv.data import download

    cfg, root = _ctx(config)
    download(cfg, root)


@app.command()
def split(config: str = ConfigOpt) -> None:
    """驗證標註並切分 train/val/test。"""
    from autocv.split import split as do_split

    cfg, root = _ctx(config)
    do_split(cfg, root)


@app.command()
def train(config: str = ConfigOpt, yes: bool = YesOpt) -> None:
    """訓練 YOLOv8 模型。"""
    from autocv.train import train as do_train

    cfg, root = _ctx(config)
    do_train(cfg, root, yes=yes)


@app.command()
def optimize(config: str = ConfigOpt, yes: bool = YesOpt) -> None:
    """超參搜尋（很耗時）。"""
    from autocv.optimize import optimize as do_opt

    cfg, root = _ctx(config)
    do_opt(cfg, root, yes=yes)


@app.command()
def infer(config: str = ConfigOpt) -> None:
    """推論並產出視覺化 + summary。"""
    from autocv.infer import infer as do_infer

    cfg, root = _ctx(config)
    do_infer(cfg, root)


@app.command()
def all(
    config: str = ConfigOpt,
    yes: bool = YesOpt,
    optimize_step: bool = typer.Option(
        False, "--optimize", help="用 optimize 取代 train"
    ),
) -> None:
    """一條龍：data→split→(train|optimize)→infer。"""
    from autocv.data import download
    from autocv.infer import infer as do_infer
    from autocv.optimize import optimize as do_opt
    from autocv.split import split as do_split
    from autocv.train import train as do_train

    cfg, root = _ctx(config)
    download(cfg, root)
    do_split(cfg, root)
    if optimize_step:
        do_opt(cfg, root, yes=yes)
    else:
        do_train(cfg, root, yes=yes)
    do_infer(cfg, root)


if __name__ == "__main__":
    app()
```

- [ ] **Step 2: 實作 `src/autocv/__main__.py`**

```python
from autocv.cli import app

if __name__ == "__main__":
    app()
```

- [ ] **Step 3: 驗證 CLI 可跑**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run autocv --help && uv run autocv version`
Expected: 顯示子命令列表 + `autocv 0.1.0`

- [ ] **Step 4: Commit**

```bash
git add src/autocv/cli.py src/autocv/__main__.py
git commit -m "加 typer CLI：五子命令 + all 一條龍"
```

---

### Task 11: CLI smoke 測試

**Files:**
- Create: `$REPO/tests/test_cli.py`

- [ ] **Step 1: 寫測試 `tests/test_cli.py`**

```python
from typer.testing import CliRunner

from autocv.cli import app

runner = CliRunner()


def test_help():
    r = runner.invoke(app, ["--help"])
    assert r.exit_code == 0
    for cmd in ("data", "split", "train", "optimize", "infer", "all"):
        assert cmd in r.output


def test_version():
    r = runner.invoke(app, ["version"])
    assert r.exit_code == 0
    assert "autocv" in r.output
```

- [ ] **Step 2: 跑全部測試確認通過**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest -v`
Expected: 全部 passed（config 3 + device 2 + split 3 + cli 2）

- [ ] **Step 3: Commit**

```bash
git add tests/test_cli.py
git commit -m "加 CLI smoke 測試"
```

---

### Task 12: configs/template.yaml

**Files:**
- Create: `$REPO/configs/template.yaml`

- [ ] **Step 1: 寫 `configs/template.yaml`（逐行註解的空白範本）**

```yaml
# ---- 複製這份改成你自己的 config ----
roboflow:
  workspace: YOUR_WORKSPACE   # Roboflow workspace slug
  project: YOUR_PROJECT       # Roboflow project slug
  version: 1                  # dataset version 號
  format: yolov8              # 下載格式（YOLOv8）
  api_key_env: ROBOFLOW_API_KEY  # 從哪個環境變數讀 API key

paths:
  raw: data/raw               # 原始下載目錄
  processed: data/processed   # 切分後目錄
  runs: runs                  # 訓練/推論輸出

dataset:
  split: [0.7, 0.2, 0.1]      # train/val/test，和需為 1（原始已切分則沿用）
  seed: 42

train:
  model: yolov8n.pt           # 起始權重（n/s/m/l/x）
  epochs: 50
  batch: 8
  imgsz: 416
  device: auto                # auto → mps→cuda→cpu

optimize:
  iterations: 20              # 超參搜尋輪數
  epochs: 15                  # 每輪短訓 epochs

infer:
  conf: 0.25                  # 推論信心門檻
  num_samples: 10             # 產出幾張視覺化
```

- [ ] **Step 2: Commit**

```bash
git add configs/template.yaml
git commit -m "加 template.yaml 空白範本（逐行註解）"
```

---

### Task 13: 改寫 5 個 Claude Code agent

**Files:**
- Create: `$REPO/.claude/agents/{data-hunter,bbox-labeler,training-runner,hp-optimizer,inference-runner}.md`

來源參考：`$SRC/.claude/agents/*.md`（4 個）。改寫原則：去 wafer 寫死、去 `Projects/2026-001-mvp` 路徑、改成「呼叫對應 `autocv` 子命令並讀 `configs/*.yaml`」。

- [ ] **Step 1: 寫 `data-hunter.md`**

```markdown
---
name: "data-hunter"
description: "從 Roboflow Universe 下載資料集到 data/raw/。當使用者要抓資料、下載資料集時使用。\n\n<example>\nContext: 開始一個 CV 專案需要原始資料。\nuser: \"幫我下載資料集\"\nassistant: \"我用 data-hunter 跑 autocv data 下載\"\n<commentary>下載資料集是 data-hunter 的核心職責。</commentary>\n</example>"
tools: Bash, Read, Write
model: opus
color: red
---

你是 **data-hunter**，只負責從 Roboflow 下載原始資料。下載完立刻交棒。

## 流程
1. 確認專案根目錄有 `.env` 含 config 指定的 API key 變數（預設 `ROBOFLOW_API_KEY`）；沒有就請使用者複製 `.env.example`
2. 確認 `configs/` 下有要用的 config（預設 `configs/wafer.yaml`）
3. 跑 `uv run autocv data -c configs/<name>.yaml`
4. 回報下載路徑、train/valid/test 圖片數、`data.yaml` 前 20 行

## 完成標準
- `data/raw/` 下有 images/labels + data.yaml
- 不做切分、不訓練、不推論
```

- [ ] **Step 2: 寫 `bbox-labeler.md`**

```markdown
---
name: "bbox-labeler"
description: "驗證 YOLO 標註並切分 train/val/test，產生 data.yaml。當使用者要驗證標註、切分資料集時使用。\n\n<example>\nContext: 資料剛下載完。\nuser: \"驗證並切分資料\"\nassistant: \"我用 bbox-labeler 跑 autocv split\"\n<commentary>驗證 + 切分是 bbox-labeler 的核心職責。</commentary>\n</example>"
tools: Bash, Read, Write
model: opus
color: yellow
---

你是 **bbox-labeler**，把 raw data 整理成標準 YOLO 訓練格式。

## 流程
1. 確認 `data/raw/` 存在（否則請使用者先跑 data-hunter）
2. 跑 `uv run autocv split -c configs/<name>.yaml`
3. 回報三個 split 圖片數、bbox 總數、類別分佈、標註異常清單
4. 確認 `data/processed/data.yaml` 可被 ultralytics 讀取

## 邊界
- 不重新生成 bbox，信任既有標註
- 格式錯誤 > 10% 會由 CLI 中止，回報並請使用者確認
```

- [ ] **Step 3: 寫 `training-runner.md`**

```markdown
---
name: "training-runner"
description: "訓練 YOLOv8 模型。當使用者要訓練、fine-tune 時使用。⚠️ 訓練前必須顯示預估時間並等使用者明確說 GO。\n\n<example>\nContext: dataset 準備好了。\nuser: \"開始訓練\"\nassistant: \"我用 training-runner 跑 autocv train，會先報預估時間等你 GO\"\n<commentary>訓練前要先預估並等 GO。</commentary>\n</example>"
tools: Bash, Read, Write
model: opus
color: blue
---

你是 **training-runner**，負責訓練。

## 不可協商硬規則
跑 `uv run autocv train -c configs/<name>.yaml`（**不要**加 `--yes`），CLI 會印出預估時間並停下來等確認。把預估時間原樣轉述給使用者，**等使用者回「GO/開始/繼續」才在 confirm 輸入 y**。絕不可自己默默開始。

## 流程
1. 確認 `data/processed/data.yaml` 存在（否則請先跑 bbox-labeler）
2. 跑 `uv run autocv train -c configs/<name>.yaml`
3. 轉述預估時間，等使用者 GO
4. 回報 best.pt 路徑、mAP、實際耗時

## 錯誤處理
- 找不到 data.yaml → 請使用者先跑 bbox-labeler
- OOM → 建議調小 config 的 train.batch 後重跑
```

- [ ] **Step 4: 寫 `hp-optimizer.md`**

```markdown
---
name: "hp-optimizer"
description: "用 Ultralytics tuner 做超參搜尋，找 mAP 最高的超參。當使用者要調參、優化模型表現、hyperparameter tuning 時使用。\n\n<example>\nContext: 基線模型訓練完想再壓榨效能。\nuser: \"幫我調參數讓 mAP 更高\"\nassistant: \"我用 hp-optimizer 跑 autocv optimize 做超參搜尋\"\n<commentary>超參搜尋是 hp-optimizer 的核心職責。</commentary>\n</example>"
tools: Bash, Read, Write
model: opus
color: magenta
---

你是 **hp-optimizer**，負責超參搜尋。

## 不可協商硬規則
跑 `uv run autocv optimize -c configs/<name>.yaml`（**不要**加 `--yes`），CLI 會印出預估並停下來。轉述給使用者，**等回 GO 才確認**。超參搜尋很耗時（iterations × 單輪訓練），務必讓使用者知道。

## 流程
1. 確認 `data/processed/data.yaml` 存在
2. 跑 `uv run autocv optimize -c configs/<name>.yaml`
3. 轉述預估時間，等使用者 GO
4. 回報 `runs/tune/best_hyperparameters.yaml` 路徑與最佳指標
5. 建議使用者把最佳超參填回 config 的 train 區塊再跑一次 training-runner
```

- [ ] **Step 5: 寫 `inference-runner.md`**

```markdown
---
name: "inference-runner"
description: "用訓練好的模型跑推論，產出帶 bbox 的視覺化與 summary.md。當使用者要 inference、預測、視覺化、評估 mAP 時使用。\n\n<example>\nContext: 訓練完成想看結果。\nuser: \"跑 test set 看結果\"\nassistant: \"我用 inference-runner 跑 autocv infer 產出 bbox 視覺化\"\n<commentary>推論 + 視覺化是 inference-runner 的核心交付。</commentary>\n</example>"
tools: Bash, Read, Write
model: opus
color: green
---

你是 **inference-runner**，負責推論與視覺化。

## 核心交付
每張 PNG 必須能看到預測 bbox 與 class name + confidence，並產出 `summary.md` 含 mAP。

## 流程
1. 確認 `runs/` 下有 best.pt（否則請先跑 training-runner 或 hp-optimizer）
2. 跑 `uv run autocv infer -c configs/<name>.yaml`
3. 回報 `runs/infer/` 下 PNG 數量、mAP@0.5、mAP@0.5:0.95
4. 把 summary.md 重點轉述給使用者

## 錯誤處理
- 找不到 best.pt → 請使用者先跑 training-runner
- test/ 不存在 → CLI 會自動 fallback 到 val/，回報時註明
```

- [ ] **Step 6: Commit**

```bash
git add .claude/agents/
git commit -m "加 5 個 config 驅動 agent（新增 hp-optimizer）"
```

---

### Task 14: CLAUDE.md（通用模板指南）

**Files:**
- Create: `$REPO/CLAUDE.md`

- [ ] **Step 1: 寫 `CLAUDE.md`**

```markdown
# auto-cv-train-inference-optimization

通用 CV 自動訓練模板。改一個 `configs/*.yaml`，一行指令或跟 Claude Code 對話即可跑完整 pipeline。

## Pipeline
`data → split → train → optimize → infer`

兩種介面：
1. **CLI**：`uv run autocv all -c configs/wafer.yaml`
2. **Claude Code agents**：跟 Claude 說「下載並訓練」，5 個 agent 自動接力

## 規則
- Python 套件用 `uv` 管理（禁止 pip）
- 所有路徑用 `pathlib.Path`
- Mac 預設 MPS（`device: auto`）
- 訓練/優化前一定先報預估時間並等使用者確認（agent 不可加 `--yes`）
- 換資料集只改 config，不改程式碼

## 不要 commit 的東西
`.env`、`data/`、`runs/`、`*.pt` 已在 `.gitignore`。
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "加通用模板 CLAUDE.md"
```

---

### Task 15: 搬 showcase 成果圖與 docs

**Files:**
- Create: `$REPO/docs/results/` (10 PNG + summary.md)、`$REPO/docs/architecture.md`、`$REPO/examples/wafer/README.md`

- [ ] **Step 1: 複製 wafer 成果圖**

```bash
cp /Users/kevinluo/claude-code-complete-tutorial/agent_group_projects/computer-vision-wafer-agents-detection-demo/Projects/2026-001-mvp/05-results/predictions/*.png /Users/kevinluo/auto-cv-train-inference-optimization/docs/results/
cp /Users/kevinluo/claude-code-complete-tutorial/agent_group_projects/computer-vision-wafer-agents-detection-demo/Projects/2026-001-mvp/05-results/summary.md /Users/kevinluo/auto-cv-train-inference-optimization/docs/results/summary.md
ls /Users/kevinluo/auto-cv-train-inference-optimization/docs/results/*.png | wc -l
```

Expected: `10`

- [ ] **Step 2: 修 `docs/results/summary.md` 圖片路徑**

把 summary.md 內 `![...](predictions/pred_xxx.png)` 改成 `![...](pred_xxx.png)`（圖已平鋪在同層）。用 sed：

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization/docs/results
sed -i '' 's|(predictions/|(|g' summary.md
grep -c '](pred_' summary.md
```

Expected: `10`

- [ ] **Step 3: 寫 `docs/architecture.md`**

```markdown
# 架構

## Pipeline

```
configs/*.yaml ──┐
                 ▼
ROBOFLOW_API_KEY → data  → data/raw/
                            │
                            ▼
                 split → data/processed/{images,labels}/{train,val,test}/ + data.yaml
                            │
              ┌─────────────┴──────────────┐
              ▼                             ▼
           train                       optimize
      runs/train/weights/best.pt   runs/tune/ + best_hyperparameters.yaml
              └─────────────┬──────────────┘
                            ▼
                         infer → runs/infer/pred_*.png + summary.md
```

## 模組職責

| 模組 | 職責 |
|---|---|
| `config.py` | 載入+驗證 YAML |
| `device.py` | auto 挑 mps/cuda/cpu |
| `data.py` | Roboflow 下載 |
| `split.py` | 標註驗證 + 切分 + data.yaml |
| `train.py` | 單次訓練（GO-gate） |
| `optimize.py` | 超參搜尋 |
| `infer.py` | 推論 + 視覺化 + summary |
| `cli.py` | typer 指令路由 |

## 安全設計

`train` / `optimize` 預設先印預估時間並等 `typer.confirm`，`--yes` 才跳過。Claude Code agent 規定不可加 `--yes`，確保不會偷偷燒運算資源。
```

- [ ] **Step 4: 寫 `examples/wafer/README.md`**

```markdown
# Wafer Showcase

內建範例：半導體晶圓圖瑕疵偵測（WM-811K，YOLOv8n，Mac MPS）。

## 重現

```bash
cp .env.example .env   # 填入 ROBOFLOW_API_KEY
uv run autocv all -c configs/wafer.yaml --yes
```

## 已達成績（見 docs/results/）

| 指標 | 數值 |
|---|---|
| mAP@0.5 | 0.9913 |
| mAP@0.5:0.95 | 0.7633 |
| Precision | 0.9331 |
| Recall | 0.9968 |

成果視覺化見 [`docs/results/summary.md`](../../docs/results/summary.md)。
```

- [ ] **Step 5: Commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git add docs/ examples/
git commit -m "加 wafer showcase 成果圖、架構文件與範例說明"
```

---

### Task 16: README.md（中英雙語同頁）

**Files:**
- Create: `$REPO/README.md`

- [ ] **Step 1: 寫 `README.md`**

````markdown
# auto-cv-train-inference-optimization

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/kevin801221/auto-cv-train-inference-optimization/actions/workflows/ci.yml/badge.svg)](https://github.com/kevin801221/auto-cv-train-inference-optimization/actions)

> **EN** — Change one YAML, run one command: auto-pipeline any Roboflow dataset through **download → validate/split → train → hyperparameter-optimize → inference visualization**. Or just talk to Claude Code — 5 specialist agents run the whole pipeline for you.
>
> **中** — 改一個 YAML，一行指令把任何 Roboflow 資料集自動跑完「下載 → 驗證切分 → 訓練 → 超參優化 → 推論視覺化」；或者直接跟 Claude Code 對話，5 個專家 agent 自動接力做完。

半導體晶圓瑕疵偵測（WM-811K）內建 showcase：**mAP@0.5 = 0.9913**。

---

## 30-second quickstart / 30 秒上手

```bash
git clone git@github.com:kevin801221/auto-cv-train-inference-optimization.git
cd auto-cv-train-inference-optimization
uv venv --python 3.11 && uv pip install -e .
cp .env.example .env          # fill in ROBOFLOW_API_KEY / 填入 Roboflow API key
uv run autocv all -c configs/wafer.yaml --yes
```

## Two interfaces / 兩種介面

**1. CLI**

| Command | Does |
|---|---|
| `autocv data -c configs/wafer.yaml` | download from Roboflow / 下載 |
| `autocv split -c ...` | validate labels + split 70/20/10 / 驗證切分 |
| `autocv train -c ...` | train YOLOv8 (asks before burning GPU) / 訓練（先問再燒卡） |
| `autocv optimize -c ...` | hyperparameter search / 超參搜尋 |
| `autocv infer -c ...` | inference + bbox PNGs + summary / 推論視覺化 |
| `autocv all -c ... [--optimize]` | full pipeline / 一條龍 |

**2. Claude Code agents** — open this repo in Claude Code and say *"download and train this dataset"*. Five agents (data-hunter → bbox-labeler → training-runner → hp-optimizer → inference-runner) hand off automatically. 用 Claude Code 打開本 repo，說「下載並訓練」，5 個 agent 自動接力。

## Bring your own dataset / 換你自己的資料集

Copy `configs/template.yaml`, change `roboflow.workspace/project/version`. No code change. 複製 `configs/template.yaml` 改 workspace/project/version 即可，不用改任何程式碼。

## Showcase results / 成果展示

| Metric | Value |
|---|---|
| mAP@0.5 | 0.9913 |
| mAP@0.5:0.95 | 0.7633 |
| Precision | 0.9331 |
| Recall | 0.9968 |

See [`docs/results/summary.md`](docs/results/summary.md) for 10 bbox visualizations. 10 張帶 bbox 視覺化見該檔。

## Responsible training / 負責任訓練

`train` and `optimize` print a time estimate and **wait for your confirmation** before consuming GPU/electricity. Agents are forbidden from using `--yes`. 訓練/優化前一定先報預估時間並等你確認，agent 不准跳過。

## Architecture / 架構

See [`docs/architecture.md`](docs/architecture.md).

## License

MIT
````

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "加中英雙語 README（badges + quickstart + 成果展示）"
```

---

### Task 17: LICENSE + CI

**Files:**
- Create: `$REPO/LICENSE`, `$REPO/.github/workflows/ci.yml`

- [ ] **Step 1: 寫 `LICENSE`（MIT）**

```
MIT License

Copyright (c) 2026 Kevin Luo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: 寫 `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v5
      - name: Set up Python
        run: uv venv --python 3.11
      - name: Install
        run: uv pip install -e ".[dev]"
      - name: Lint
        run: uv run ruff check src tests
      - name: Smoke
        run: uv run autocv --help
      - name: Tests
        run: uv run pytest -v
```

- [ ] **Step 3: 本地驗證 ruff + 測試全綠**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run ruff check src tests && uv run pytest -v`
Expected: ruff 無錯、所有測試 passed

- [ ] **Step 4: Commit**

```bash
git add LICENSE .github/workflows/ci.yml
git commit -m "加 MIT LICENSE 與 GitHub Actions CI"
```

---

### Task 18: 安全掃描與最終檢查

**Files:** 無（驗證）

- [ ] **Step 1: 確認沒有 .env / 權重 / 大資料被追蹤**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git ls-files | grep -E '\.env$|\.pt$|^data/|^runs/' && echo "❌ 有不該追蹤的檔" || echo "✅ 乾淨"
```

Expected: `✅ 乾淨`

- [ ] **Step 2: grep 掃描有無 API key 字串外洩**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git grep -nE '[A-Za-z0-9]{20,}' -- '*.py' '*.yaml' '*.md' | grep -iv badge | grep -iv shields || echo "✅ 無疑似 key"
```

Expected: `✅ 無疑似 key`（或人工確認列出的都是無害字串）

- [ ] **Step 3: 確認檔案樹符合設計**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git ls-files | sort
```

Expected: 含 pyproject/README/LICENSE/CLAUDE.md/configs(2)/src/autocv(9 py)/tests(4)/.claude/agents(5)/docs(architecture+results 11)/examples/.github/ci，**不含** .env/.venv/data/runs/*.pt

- [ ] **Step 4: 更新 uv.lock 並 commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
uv lock
git add uv.lock
git commit -m "鎖定相依版本（uv.lock）"
```

---

### Task 19: 建 GitHub repo 並 push

**Files:** 無（git/gh 操作）

- [ ] **Step 1: 用 gh 建 public repo**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
gh repo create kevin801221/auto-cv-train-inference-optimization --public --source . --remote origin --description "改一個 YAML 一行指令跑完整 CV pipeline：下載→切分→訓練→超參優化→推論。或跟 Claude Code 對話讓 5 個 agent 接力。"
```

若 gh 預設帳號非 kevin801221，先 `gh auth status` 確認；必要時 `gh auth switch`。

- [ ] **Step 2: 把 remote 改成個人 SSH alias**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git remote set-url origin git@github-personal:kevin801221/auto-cv-train-inference-optimization.git
git remote -v
```

Expected: origin 指向 `git@github-personal:...`

- [ ] **Step 2.5: 在 push 前停下來等使用者確認**

向使用者回報：repo 將以 **public** 推送到 `kevin801221/auto-cv-train-inference-optimization`，列出 `git ls-files` 摘要與 commit 數，**等使用者回「push / GO」才執行 Step 3**（建立公開 repo 是對外、難回退動作）。

- [ ] **Step 3: push**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git push -u origin main
```

- [ ] **Step 4: 驗證**

```bash
gh repo view kevin801221/auto-cv-train-inference-optimization --web
```

Expected: 瀏覽器開啟 repo，README 正常渲染、CI 開始跑、無 .env/權重/大資料。

---

## Self-Review

**Spec coverage：**

- 通用 CV 模板定位 → Task 16 README、Task 14 CLAUDE.md ✅
- 中英雙語 README → Task 16 ✅
- 附成果圖不附權重 → Task 15（複製 PNG）、.gitignore 排除 *.pt（Task 1）✅
- 完整 CLI 深重構 → Task 2 套件化、Task 3-10 模組、Task 10 typer CLI ✅
- typer 框架 → Task 2 依賴、Task 10 ✅
- repo 名 auto-cv-train-inference-optimization + 個人 public → Task 19 ✅
- optimization 階段（Ultralytics tuner）→ Task 8 optimize.py、Task 10 CLI、Task 13 hp-optimizer agent ✅
- 5 階段 pipeline → Task 10 `all` ✅
- 5 個 config 驅動 agent → Task 13 ✅
- GO-gate 升級 → Task 7/8（typer.confirm）、Task 13 agent 規定不可加 --yes ✅
- 上傳/排除清單 → Task 1 .gitignore、Task 18 掃描 ✅
- 新 repo 建教學 repo 外、獨立 git → Task 1 ✅
- 測試策略（config/device/split/cli + CI 不跑真實訓練）→ Task 3/4/5/11/17 ✅
- 安全（.env 排除 + push 前掃描 + push 前確認）→ Task 1/18/19 ✅

無遺漏。

**Placeholder scan：** 各 step 皆含完整檔案內容或精確指令，無 TBD/TODO/「類似上面」。✅

**Type consistency：** `Config`/`load_config`/`Config.from_dict` 跨 Task 3-10 一致；各模組對外函式 `download(cfg, root)`、`split(cfg, root)`、`train(cfg, root, yes)`、`optimize(cfg, root, yes)`、`infer(cfg, root)`、`validate_label_file(path)`、`pick_device(pref)`、`_mps_available`/`_cuda_available`（test 有 monkeypatch 對應）、cli `app` 與 `[project.scripts]` 一致。✅
