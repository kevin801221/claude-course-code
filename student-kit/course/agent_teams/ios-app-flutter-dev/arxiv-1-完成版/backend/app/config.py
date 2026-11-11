"""集中設定:從環境變數 / backend/.env 讀,沒設就用合理預設。

安全紅線:GEMINI_API_KEY 只從環境變數讀,絕不寫進程式碼或 commit 進 repo。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# backend/ 根目錄(本檔在 backend/app/config.py → 上兩層)
BACKEND_DIR = Path(__file__).resolve().parent.parent
# 專案根目錄(backend 的上一層,arxiv-1-完成版/)
PROJECT_ROOT = BACKEND_DIR.parent

# 載入 .env(load_dotenv 預設不覆蓋已存在的環境變數):
# 1) 先讀「專案根目錄 .env」(跨層共用,使用者把真 GEMINI_API_KEY 放這)→ 優先生效
# 2) 再讀「backend/.env」作 fallback(後端專屬調參 ARXIV_* 等)
# 用絕對路徑往上找,不寫死脆弱相對路徑。
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(BACKEND_DIR / ".env")

# --- arXiv 抓取設定(依 research-findings 第 1 節) ---
# 預設收 cs.AI / cs.LG / cs.CL;可用環境變數覆蓋(逗號分隔)。
ARXIV_CATEGORIES: list[str] = [
    c.strip()
    for c in os.getenv("ARXIV_CATEGORIES", "cs.AI,cs.LG,cs.CL").split(",")
    if c.strip()
]
ARXIV_API_URL = "http://export.arxiv.org/api/query"
# 多抓一點 → 依 arxivId 去重 → 截最新 N 篇,避免去重後不足。
ARXIV_FETCH_SIZE = int(os.getenv("ARXIV_FETCH_SIZE", "15"))
ARXIV_TOP_N = int(os.getenv("ARXIV_TOP_N", "5"))
# arXiv ToU:連續請求至少間隔 3 秒、單一連線。
ARXIV_REQUEST_INTERVAL_SEC = float(os.getenv("ARXIV_REQUEST_INTERVAL_SEC", "3"))
ARXIV_TIMEOUT_SEC = float(os.getenv("ARXIV_TIMEOUT_SEC", "30"))

# --- Gemini 摘要設定 ---
# key 只從環境變數讀;沒設 → fallback 佔位摘要(讓 API 沒 key 也能跑)。
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()

# --- 儲存設定 ---
DATA_DIR = Path(os.getenv("DATA_DIR", str(BACKEND_DIR / "data")))

# --- FastAPI 服務 ---
PORT = int(os.getenv("PORT", "8000"))


def has_gemini_key() -> bool:
    """是否設了可用的 Gemini API key(決定真呼叫 or fallback)。"""
    return bool(GEMINI_API_KEY) and GEMINI_API_KEY != "your-gemini-api-key-here"
