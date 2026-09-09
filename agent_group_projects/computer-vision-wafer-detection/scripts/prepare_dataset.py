"""
Prepare YOLO dataset：將 01-raw-data/train 切分為 train/val/test (70/20/10)。

輸出：Projects/2026-001-mvp/02-dataset/{images,labels}/{train,val,test} + data.yaml
"""

from __future__ import annotations

import random
import shutil
from collections import Counter
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "Projects" / "2026-001-mvp" / "01-raw-data" / "train"
OUT_DIR = PROJECT_ROOT / "Projects" / "2026-001-mvp" / "02-dataset"

RAW_IMAGES = RAW_DIR / "images"
RAW_LABELS = RAW_DIR / "labels"

SEED = 42
SPLIT_RATIO = {"train": 0.70, "val": 0.20, "test": 0.10}
CLASS_NAMES = {0: "Donut"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def validate_labels(image_files: list[Path]) -> dict:
    """掃描所有 label，回傳統計與異常清單。"""
    stats = {
        "total_images": len(image_files),
        "total_labels": 0,
        "empty_labels": 0,
        "total_bboxes": 0,
        "class_counter": Counter(),
        "invalid": [],  # list of (label_path, line_no, reason)
        "missing_labels": [],
    }

    for img in image_files:
        label_path = RAW_LABELS / f"{img.stem}.txt"
        if not label_path.exists():
            stats["missing_labels"].append(str(label_path))
            continue

        stats["total_labels"] += 1
        lines = label_path.read_text(encoding="utf-8").splitlines()
        non_empty = [ln for ln in lines if ln.strip()]
        if not non_empty:
            stats["empty_labels"] += 1
            continue

        for i, line in enumerate(non_empty, start=1):
            parts = line.strip().split()
            if len(parts) != 5:
                stats["invalid"].append((str(label_path), i, f"expect 5 fields, got {len(parts)}"))
                continue
            try:
                cls = int(parts[0])
                cx, cy, w, h = (float(x) for x in parts[1:])
            except ValueError as e:
                stats["invalid"].append((str(label_path), i, f"parse error: {e}"))
                continue
            if cls < 0:
                stats["invalid"].append((str(label_path), i, f"class_id<0: {cls}"))
                continue
            if not all(0.0 <= v <= 1.0 for v in (cx, cy, w, h)):
                stats["invalid"].append((str(label_path), i, f"coord out of [0,1]: {(cx, cy, w, h)}"))
                continue
            stats["total_bboxes"] += 1
            stats["class_counter"][cls] += 1

    return stats


def split_files(image_files: list[Path]) -> dict[str, list[Path]]:
    """隨機切分 70/20/10。"""
    rng = random.Random(SEED)
    shuffled = image_files[:]
    rng.shuffle(shuffled)

    n = len(shuffled)
    n_train = int(n * SPLIT_RATIO["train"])
    n_val = int(n * SPLIT_RATIO["val"])
    # test 拿剩下的，確保總和不漏
    splits = {
        "train": shuffled[:n_train],
        "val": shuffled[n_train : n_train + n_val],
        "test": shuffled[n_train + n_val :],
    }
    return splits


def prepare_output_dirs() -> None:
    """建立 02-dataset 目錄結構（若存在則清掉）。"""
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    for sub in ("images", "labels"):
        for split in ("train", "val", "test"):
            (OUT_DIR / sub / split).mkdir(parents=True, exist_ok=True)


def copy_split(name: str, files: list[Path]) -> dict:
    """複製 images + labels，回傳該 split 的統計。"""
    bbox_count = 0
    class_counter: Counter[int] = Counter()
    for img in files:
        dst_img = OUT_DIR / "images" / name / img.name
        shutil.copy2(img, dst_img)
        src_label = RAW_LABELS / f"{img.stem}.txt"
        dst_label = OUT_DIR / "labels" / name / f"{img.stem}.txt"
        if src_label.exists():
            shutil.copy2(src_label, dst_label)
            for line in src_label.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) == 5:
                    try:
                        cls = int(parts[0])
                        class_counter[cls] += 1
                        bbox_count += 1
                    except ValueError:
                        pass
        else:
            # 沒對應 label 就建空檔（YOLO 視為 background）
            dst_label.write_text("", encoding="utf-8")
    return {
        "images": len(files),
        "bboxes": bbox_count,
        "classes": dict(class_counter),
    }


def write_data_yaml() -> Path:
    data = {
        "path": str(OUT_DIR.resolve()),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "nc": len(CLASS_NAMES),
        "names": {k: v for k, v in CLASS_NAMES.items()},
    }
    out = OUT_DIR / "data.yaml"
    with out.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    return out


def main() -> None:
    print("=" * 60)
    print("Step 1: 驗證標註")
    print("=" * 60)
    image_files = sorted(p for p in RAW_IMAGES.iterdir() if p.suffix.lower() in IMAGE_EXTS)
    stats = validate_labels(image_files)
    print(f"  total_images : {stats['total_images']}")
    print(f"  total_labels : {stats['total_labels']}")
    print(f"  empty_labels : {stats['empty_labels']}")
    print(f"  total_bboxes : {stats['total_bboxes']}")
    print(f"  class_dist   : {dict(stats['class_counter'])}")
    print(f"  missing_labels: {len(stats['missing_labels'])}")
    print(f"  invalid_lines : {len(stats['invalid'])}")
    if stats["invalid"]:
        print("  -- 異常清單 (最多顯示 20 筆) --")
        for item in stats["invalid"][:20]:
            print(f"    {item}")

    print()
    print("=" * 60)
    print("Step 2-3: 切分 + 複製檔案 (seed=42, 70/20/10)")
    print("=" * 60)
    splits = split_files(image_files)
    prepare_output_dirs()
    split_stats: dict[str, dict] = {}
    for name, files in splits.items():
        split_stats[name] = copy_split(name, files)
        print(f"  {name:5s}: {len(files)} images copied")

    print()
    print("=" * 60)
    print("Step 4: 寫出 data.yaml")
    print("=" * 60)
    yaml_path = write_data_yaml()
    print(f"  寫出 {yaml_path}")
    print("  內容：")
    print("  " + yaml_path.read_text(encoding="utf-8").replace("\n", "\n  "))

    print()
    print("=" * 60)
    print("Step 5: 摘要")
    print("=" * 60)
    print(f"  {'split':<6}{'images':>8}{'bboxes':>8}  classes")
    for name in ("train", "val", "test"):
        s = split_stats[name]
        print(f"  {name:<6}{s['images']:>8}{s['bboxes']:>8}  {s['classes']}")
    total_imgs = sum(s["images"] for s in split_stats.values())
    total_bbox = sum(s["bboxes"] for s in split_stats.values())
    print(f"  {'TOTAL':<6}{total_imgs:>8}{total_bbox:>8}")

    # 對齊檢查
    print()
    print("  -- 檔案數對齊檢查 --")
    for name in ("train", "val", "test"):
        n_img = len(list((OUT_DIR / "images" / name).iterdir()))
        n_lbl = len(list((OUT_DIR / "labels" / name).iterdir()))
        flag = "OK" if n_img == n_lbl else "MISMATCH"
        print(f"    {name}: images={n_img}, labels={n_lbl}  [{flag}]")


if __name__ == "__main__":
    main()
