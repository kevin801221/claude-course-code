"""下載 WM-811K 晶圓瑕疵資料集 (Roboflow Universe → YOLOv8 格式)。

預設參數:
  Workspace: wm811k-paasr
  Project:   wm811k
  Version:   3
  Format:    yolov8
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# 專案根目錄: scripts/ 的上一層
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
TARGET_DIR = PROJECT_ROOT / "Projects" / "2026-001-mvp" / "01-raw-data"

WORKSPACE = "wm811k-paasr"
PROJECT = "wm811k"
PREFERRED_VERSION = 3
FORMAT = "yolov8"


def load_api_key() -> str:
    if not ENV_PATH.exists():
        raise SystemExit(f"[ERROR] 找不到 .env: {ENV_PATH}")
    load_dotenv(ENV_PATH)
    api_key = os.environ.get("ROBOFLOW_API_KEY")
    if not api_key:
        raise SystemExit("[ERROR] .env 中找不到 ROBOFLOW_API_KEY")
    return api_key


def main() -> int:
    api_key = load_api_key()
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # 延後 import 以便 .env 先讀取
    from roboflow import Roboflow

    try:
        rf = Roboflow(api_key=api_key)
    except Exception as exc:
        raise SystemExit(f"[ERROR] Roboflow 初始化失敗 (API key 可能失效): {exc}")

    # 取得 workspace
    try:
        workspace = rf.workspace(WORKSPACE)
    except Exception as exc:
        raise SystemExit(f"[ERROR] 找不到 workspace '{WORKSPACE}': {exc}")

    # 取得 project；失敗時嘗試列出該 workspace 下的 projects
    try:
        project = workspace.project(PROJECT)
    except Exception as exc:
        print(f"[WARN] 找不到 project '{PROJECT}': {exc}", file=sys.stderr)
        try:
            projects = workspace.projects()  # type: ignore[attr-defined]
            print(f"[INFO] Workspace '{WORKSPACE}' 下的 projects: {projects}")
        except Exception as exc2:
            print(f"[WARN] 列出 projects 失敗: {exc2}", file=sys.stderr)
        raise SystemExit(1)

    # 決定要下載的版本
    target_version = PREFERRED_VERSION
    try:
        versions = project.versions()
        version_ids = []
        for v in versions:
            # Roboflow Version 物件有 .version 屬性 (含 workspace 前綴)
            raw = getattr(v, "version", None) or getattr(v, "id", "")
            # 解析尾端數字
            try:
                vid = int(str(raw).split("/")[-1])
                version_ids.append(vid)
            except Exception:
                continue
        if version_ids:
            print(f"[INFO] 可用版本: {sorted(version_ids)}")
            if PREFERRED_VERSION not in version_ids:
                target_version = max(version_ids)
                print(f"[WARN] v{PREFERRED_VERSION} 不存在，改用最新版 v{target_version}")
    except Exception as exc:
        print(f"[WARN] 列出版本失敗，沿用 v{PREFERRED_VERSION}: {exc}", file=sys.stderr)

    print(
        f"[INFO] 下載 {WORKSPACE}/{PROJECT} v{target_version} "
        f"(format={FORMAT}) → {TARGET_DIR}"
    )

    try:
        dataset = project.version(target_version).download(
            FORMAT, location=str(TARGET_DIR), overwrite=True
        )
    except Exception as exc:
        raise SystemExit(f"[ERROR] 下載失敗: {exc}")

    print(f"[OK] Downloaded to: {dataset.location}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
