"""驗證 YOLO 標註並切分 train/val/test (70/20/10)。"""
from __future__ import annotations

import random
import shutil
from collections import Counter
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
SRC_IMG_DIR = RAW_DIR / "train" / "images"
SRC_LBL_DIR = RAW_DIR / "train" / "labels"
RAW_YAML = RAW_DIR / "data.yaml"

OUT_DIR = PROJECT_ROOT / "data" / "processed"
SEED = 42
RATIOS = {"train": 0.7, "val": 0.2, "test": 0.1}
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


def main() -> None:
    raw_cfg = yaml.safe_load(RAW_YAML.read_text())
    names = raw_cfg["names"]
    nc = raw_cfg["nc"]

    images = sorted(p for p in SRC_IMG_DIR.iterdir() if p.suffix.lower() in IMG_EXTS)
    print(f"圖片總數: {len(images)}")

    all_errors: list[str] = []
    class_counter: Counter[int] = Counter()
    total_bbox = 0
    empty_labels = 0
    paired: list[tuple[Path, Path]] = []

    for img in images:
        lbl = SRC_LBL_DIR / f"{img.stem}.txt"
        errors, cids, bcount = validate_label_file(lbl)
        all_errors.extend(errors)
        class_counter.update(cids)
        total_bbox += bcount
        if bcount == 0:
            empty_labels += 1
        if lbl.exists():
            paired.append((img, lbl))

    print(f"label 配對成功: {len(paired)}")
    print(f"bbox 總數: {total_bbox}")
    print(f"空 label 數: {empty_labels}")
    print(f"類別分佈: {dict(class_counter)}")
    print(f"異常行數: {len(all_errors)}")
    if all_errors[:5]:
        print("前 5 條異常:")
        for e in all_errors[:5]:
            print(f"  - {e}")

    err_ratio = len(all_errors) / max(total_bbox, 1)
    if err_ratio > 0.1:
        raise SystemExit(f"格式錯誤比例 {err_ratio:.1%} > 10%，中止")
    if empty_labels / max(len(images), 1) > 0.3:
        print("警告: 空 label 比例 > 30%")

    rng = random.Random(SEED)
    shuffled = paired.copy()
    rng.shuffle(shuffled)
    n = len(shuffled)
    n_train = int(n * RATIOS["train"])
    n_val = int(n * RATIOS["val"])
    splits = {
        "train": shuffled[:n_train],
        "val": shuffled[n_train : n_train + n_val],
        "test": shuffled[n_train + n_val :],
    }

    for split in splits:
        (OUT_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)

    for split, items in splits.items():
        for img, lbl in items:
            shutil.copy2(img, OUT_DIR / "images" / split / img.name)
            shutil.copy2(lbl, OUT_DIR / "labels" / split / lbl.name)
        print(f"{split}: {len(items)} 張")

    out_yaml = {
        "path": str(OUT_DIR.resolve()),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "nc": nc,
        "names": {i: n for i, n in enumerate(names)} if isinstance(names, list) else names,
    }
    yaml_path = OUT_DIR / "data.yaml"
    yaml_path.write_text(yaml.safe_dump(out_yaml, sort_keys=False, allow_unicode=True))
    print(f"data.yaml -> {yaml_path}")


if __name__ == "__main__":
    main()
