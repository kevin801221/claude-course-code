"""Read a drawing through the optional Windows desktop Visio application."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def inspect_in_visio(path: Path) -> dict:
    """Open a VSDX read-only in a separate Visio instance and query its live model."""
    if sys.platform != "win32":
        raise ValueError("桌面 Visio 驗證需要 Windows。可用 inspect_flowchart 與 verify_manager_review 檢查檔案。")
    powershell = shutil.which("powershell.exe")
    if not powershell:
        raise ValueError("桌面驗證需要 Windows PowerShell 與已安裝的桌面 Visio。")
    script = Path(__file__).with_name("inspect_in_visio.ps1").read_text(encoding="utf-8")
    # The path is data, even when it contains quotes or PowerShell metacharacters.
    try:
        result = subprocess.run(
            [powershell, "-NoProfile", "-NonInteractive", "-STA", "-Command", script],
            env={**os.environ, "VISIO_LAB_DRAWING": str(path.resolve(strict=True))},
            capture_output=True, encoding="utf-8", errors="replace", timeout=75,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValueError("桌面 Visio 未及時回應。請確認已完成首次啟動，或改用檔案層驗證。") from exc
    if result.returncode:
        detail = result.stderr.strip() or "無法啟動 Visio 或開啟圖檔"
        raise ValueError(f"Visio 桌面驗證失敗：{detail}")
    return json.loads(result.stdout)
