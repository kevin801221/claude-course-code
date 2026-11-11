"""FastAPI 服務:照凍結契約(_Context/api-contract.md 第 1 節)對外提供報告。

端點:
- GET /reports/today      今日報告(無則 404 {"detail": "今日報告尚未產生"})
- GET /reports            歷史日期清單(新到舊)
- GET /reports/{date}     指定日期報告(查無 404)
- GET /health             健康檢查

所有回應 Content-Type: application/json; charset=utf-8。
啟動:uv run uvicorn app.main:app --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from . import storage
from .models import Report


class UTF8JSONResponse(JSONResponse):
    """強制契約要求的 charset=utf-8。"""

    media_type = "application/json; charset=utf-8"


app = FastAPI(
    title="arXiv 每日論文閱讀器 —— 後端",
    version="0.1.0",
    default_response_class=UTF8JSONResponse,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/reports/today", response_model=Report)
def reports_today() -> Report:
    report = storage.load(storage.today_str())
    if report is None:
        raise HTTPException(status_code=404, detail="今日報告尚未產生")
    return report


@app.get("/reports", response_model=list[str])
def reports_list() -> list[str]:
    return storage.list_dates()


@app.get("/reports/{date}", response_model=Report)
def reports_by_date(date: str) -> Report:
    if not storage.is_valid_date(date):
        raise HTTPException(status_code=404, detail="日期格式須為 YYYY-MM-DD")
    report = storage.load(date)
    if report is None:
        raise HTTPException(status_code=404, detail="查無該日期報告")
    return report
