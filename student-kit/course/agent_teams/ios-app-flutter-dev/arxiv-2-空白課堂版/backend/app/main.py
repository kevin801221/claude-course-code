"""FastAPI 進入點 —— arXiv 每日論文閱讀器後端。

端點（照 API 契約 _Context/api-contract.md）：
    GET /health            → {"status": "ok"}
    GET /reports/today     → 今天報告；還沒產出回 404
    GET /reports           → 歷史日期清單（新到舊）
    GET /reports/{date}    → 指定日期報告，查無回 404

啟動：
    uv run uvicorn app.main:app --reload --port 8000

產出今日報告：
    uv run python -m app.generate
"""

from __future__ import annotations

from datetime import date

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# 載入 backend/.env（若有）
load_dotenv()

from app import storage  # noqa: E402（需在 load_dotenv 之後）

app = FastAPI(
    title="arXiv 每日論文閱讀器後端",
    description="提供每日 arXiv 最新科技論文摘要報告",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/reports/today")
def reports_today():
    """回今天的報告。今天還沒產出時回 404。"""
    report = storage.load_report(date.today())
    if report is None:
        raise HTTPException(status_code=404, detail="今日報告尚未產生")
    return JSONResponse(content=report, media_type="application/json; charset=utf-8")


@app.get("/reports")
def reports_list():
    """回歷史報告日期清單（新到舊）。"""
    dates = storage.list_report_dates()
    return JSONResponse(content=dates, media_type="application/json; charset=utf-8")


@app.get("/reports/{report_date}")
def reports_by_date(report_date: str):
    """回指定日期的報告。日期格式 YYYY-MM-DD，查無回 404。"""
    report = storage.load_report_by_str(report_date)
    if report is None:
        raise HTTPException(status_code=404, detail="查無該日期報告")
    return JSONResponse(content=report, media_type="application/json; charset=utf-8")
