"""YOLOv8 training script for wafer defect detection (MPS on Mac)."""
import os
import time
from pathlib import Path

os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

from ultralytics import YOLO

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_YAML = PROJECT_ROOT / "Projects/2026-001-mvp/02-dataset/data.yaml"
EXP_DIR = PROJECT_ROOT / "Projects/2026-001-mvp/04-experiments"


def main() -> None:
    assert DATA_YAML.exists(), f"data.yaml not found: {DATA_YAML}"

    model = YOLO("yolov8n.pt")
    t0 = time.time()
    results = model.train(
        data=str(DATA_YAML),
        epochs=50,
        batch=8,
        imgsz=416,
        device="mps",
        project=str(EXP_DIR),
        name="exp001",
        exist_ok=True,
        verbose=True,
    )
    elapsed = time.time() - t0
    print(f"\n=== TRAINING DONE in {elapsed/60:.2f} min ===")
    print(f"best.pt: {Path(results.save_dir) / 'weights' / 'best.pt'}")


if __name__ == "__main__":
    main()
