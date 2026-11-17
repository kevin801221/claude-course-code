"""每日報告儲存:一天一份 JSON 存在 backend/data/(已 gitignore),保留歷史。

檔名格式:data/report-YYYY-MM-DD.json,內容即 Report 的 JSON。
"""

from __future__ import annotations

import re
from datetime import date as date_cls
from pathlib import Path

from . import config
from .models import Report

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_FILENAME_RE = re.compile(r"^report-(\d{4}-\d{2}-\d{2})\.json$")


def today_str() -> str:
    """今天日期 YYYY-MM-DD。"""
    return date_cls.today().isoformat()


def _data_dir() -> Path:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    return config.DATA_DIR


def _path_for(date: str) -> Path:
    return _data_dir() / f"report-{date}.json"


def is_valid_date(date: str) -> bool:
    return bool(_DATE_RE.match(date))


def save(report: Report) -> Path:
    """存一份報告(覆蓋同日舊檔)。回傳寫入路徑。"""
    path = _path_for(report.date)
    path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return path


def load(date: str) -> Report | None:
    """讀指定日期報告;不存在回 None。"""
    if not is_valid_date(date):
        return None
    path = _path_for(date)
    if not path.exists():
        return None
    return Report.model_validate_json(path.read_text(encoding="utf-8"))


def list_dates() -> list[str]:
    """列出所有已存報告日期,新到舊。"""
    dates: list[str] = []
    for f in _data_dir().glob("report-*.json"):
        m = _FILENAME_RE.match(f.name)
        if m:
            dates.append(m.group(1))
    return sorted(dates, reverse=True)
