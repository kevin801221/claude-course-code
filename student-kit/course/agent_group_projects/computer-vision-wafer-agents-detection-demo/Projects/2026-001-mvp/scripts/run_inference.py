"""推論腳本：對 test set 跑 YOLOv8 推論並產出視覺化 + summary.md"""
import os
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

import random
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from PIL import Image
from ultralytics import YOLO

PROJECT_ROOT = Path("/Users/kevinluo/claude-code-complete-tutorial/agent_group_projects/computer-vision-wafer-agents-detection-demo")
BEST_PT = PROJECT_ROOT / "Projects/2026-001-mvp/04-experiments/exp001/weights/best.pt"
TEST_DIR = PROJECT_ROOT / "data/processed/images/test"
DATA_YAML = PROJECT_ROOT / "data/processed/data.yaml"
OUT_DIR = PROJECT_ROOT / "Projects/2026-001-mvp/05-results/predictions"
SUMMARY_MD = PROJECT_ROOT / "Projects/2026-001-mvp/05-results/summary.md"

OUT_DIR.mkdir(parents=True, exist_ok=True)

assert BEST_PT.exists(), f"找不到權重 {BEST_PT}"
assert TEST_DIR.exists(), f"找不到 test set {TEST_DIR}"

model = YOLO(str(BEST_PT))

# Step 1: val 模式算 mAP
print("=== 評估 test split ===")
metrics = model.val(data=str(DATA_YAML), split="test", device="mps", verbose=False)
mAP50 = float(metrics.box.map50)
mAP = float(metrics.box.map)
precision = float(metrics.box.mp)
recall = float(metrics.box.mr)
print(f"mAP@0.5: {mAP50:.4f}")
print(f"mAP@0.5:0.95: {mAP:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")

# Step 2: 隨機抽 10 張
random.seed(42)
all_imgs = sorted(list(TEST_DIR.glob("*.jpg")) + list(TEST_DIR.glob("*.png")))
sample = random.sample(all_imgs, min(10, len(all_imgs)))
print(f"\n=== 抽 {len(sample)} 張視覺化 ===")

pred_files = []
for img_path in sample:
    result = model.predict(str(img_path), conf=0.25, device="mps", verbose=False)[0]
    img = Image.open(img_path)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img)
    n_boxes = len(result.boxes)
    if n_boxes == 0:
        ax.set_title(f"{img_path.name} — No prediction")
    else:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls = result.names[int(box.cls[0])]
            conf = float(box.conf[0])
            ax.add_patch(patches.Rectangle(
                (x1, y1), x2 - x1, y2 - y1,
                fill=False, edgecolor="red", linewidth=2,
            ))
            ax.text(
                x1, max(y1 - 5, 0), f"{cls} {conf:.2f}",
                color="white", fontsize=10,
                bbox=dict(facecolor="red", alpha=0.7, pad=2),
            )
        ax.set_title(f"{img_path.name} — {n_boxes} pred")
    ax.axis("off")
    out_path = OUT_DIR / f"pred_{img_path.stem}.png"
    plt.savefig(out_path, dpi=100, bbox_inches="tight")
    plt.close()
    pred_files.append(out_path)
    print(f"  saved: {out_path.name} (boxes={n_boxes})")

# Step 3: summary.md
lines = [
    "# Inference Summary — exp001",
    "",
    f"- 模型：`{BEST_PT.relative_to(PROJECT_ROOT)}`",
    f"- Test set：`{TEST_DIR.relative_to(PROJECT_ROOT)}`（{len(all_imgs)} 張）",
    f"- 裝置：Mac MPS",
    "",
    "## Metrics (test split)",
    "",
    f"- **mAP@0.5**: {mAP50:.4f}",
    f"- **mAP@0.5:0.95**: {mAP:.4f}",
    f"- **Precision**: {precision:.4f}",
    f"- **Recall**: {recall:.4f}",
    "",
    "## 視覺化樣本（10 張）",
    "",
]
for p in pred_files:
    rel = p.relative_to(SUMMARY_MD.parent)
    lines.append(f"![{p.stem}]({rel.as_posix()})")
    lines.append("")

lines += [
    "## 觀察筆記",
    "",
    "- 紅色矩形為模型預測 bbox，左上角顯示 class name 與 confidence。",
    "- 標題顯示 `No prediction` 的圖代表模型在 conf=0.25 門檻下未輸出框。",
    "- 若有大量漏偵測或低 confidence，可嘗試調整 conf 門檻或重新訓練。",
    "",
]
SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")
print(f"\n=== summary 寫入 {SUMMARY_MD} ===")
