# backend — arXiv 抓取 + Gemini 摘要 + FastAPI

team lead 建的 uv 骨架。**backend-owner 擁有此目錄**，照 `../_Context/api-contract.md` 實作。

## 啟動

```bash
cd backend
uv sync                  # 建 .venv、裝依賴
cp .env.example .env     # 填 GEMINI_API_KEY（沒 key 也能跑，走 mock fallback）
uv run uvicorn app.main:app --reload --port 8000
```

## 驗收

```bash
curl http://127.0.0.1:8000/health          # {"status":"ok"}
curl http://127.0.0.1:8000/reports/today   # 產報告後回今日報告（papers 5 篇 + markdownBody）
uv run pytest                              # 測試綠
```

## 安全紅線
`GEMINI_API_KEY` 只從環境變數讀；`.env` 不 commit，repo 只留 `.env.example`。
