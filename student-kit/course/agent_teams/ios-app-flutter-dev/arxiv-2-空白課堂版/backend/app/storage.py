"""報告本地 JSON 儲存模組。

每日一份，保留歷史。
檔案路徑：backend/data/YYYY-MM-DD.json
內容結構：與 API 契約的 Report 結構完全一致。
"""

from __future__ import annotations

import json
import os
import logging
from datetime import date
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# DATA_DIR 預設為 backend/data/，可由環境變數覆寫
_DEFAULT_DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR = Path(os.getenv("DATA_DIR", str(_DEFAULT_DATA_DIR)))


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _date_to_filename(report_date: date) -> Path:
    return DATA_DIR / f"{report_date.isoformat()}.json"


def save_report(report: dict[str, Any]) -> None:
    """把 report dict 寫入 DATA_DIR/<date>.json。"""
    _ensure_data_dir()
    report_date = report["date"]  # 字串 YYYY-MM-DD
    path = DATA_DIR / f"{report_date}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("報告已儲存：%s", path)


def load_report(report_date: date) -> dict[str, Any] | None:
    """載入指定日期報告，不存在回 None。"""
    path = _date_to_filename(report_date)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.error("讀取報告失敗 %s：%s", path, exc)
        return None


def load_report_by_str(date_str: str) -> dict[str, Any] | None:
    """載入指定日期字串（YYYY-MM-DD）的報告，不存在或格式錯誤回 None。"""
    try:
        d = date.fromisoformat(date_str)
    except ValueError:
        return None
    return load_report(d)


def list_report_dates() -> list[str]:
    """回傳所有已存在的報告日期字串清單（新到舊）。"""
    _ensure_data_dir()
    dates: list[str] = []
    for path in DATA_DIR.glob("????-??-??.json"):
        dates.append(path.stem)
    return sorted(dates, reverse=True)


def today_report_exists() -> bool:
    return _date_to_filename(date.today()).exists()
