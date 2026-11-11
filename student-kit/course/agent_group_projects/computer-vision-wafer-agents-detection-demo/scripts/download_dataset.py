"""Download WM-811K wafer defect dataset from Roboflow Universe to data/raw/."""
from pathlib import Path
import os
from dotenv import load_dotenv
from roboflow import Roboflow

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("ROBOFLOW_API_KEY")
if not api_key:
    raise RuntimeError("ROBOFLOW_API_KEY 未設定，請於 .env 設定後重試")

dest = PROJECT_ROOT / "data" / "raw"
dest.mkdir(parents=True, exist_ok=True)

rf = Roboflow(api_key=api_key)
project = rf.workspace("wm811k-paasr").project("wm811k")
dataset = project.version(3).download("yolov8", location=str(dest), overwrite=True)
print(f"DOWNLOAD_OK: {dataset.location}")
