# arXiv 每日論文閱讀器 —— 後端(模組 A)

抓 arXiv 最新 5 篇科技論文 → Gemini(gemini-3.5-flash)整理成 markdown 報告 → 每日存檔 → FastAPI 對外提供。
前後端靠 team lead 凍結的 API 契約對接(`_Context/api-contract.md`)。

## 技術
- Python 3.12,**套件一律用 [uv](https://docs.astral.sh/uv/) 管理(禁止 pip)**
- FastAPI + uvicorn、httpx、feedparser、google-genai、python-dotenv

## 安裝

```bash
cd backend
uv sync          # 依 pyproject.toml / uv.lock 建立 .venv 並安裝依賴
```

## 設定 Gemini API key(可選,沒設也能跑)

key **只從環境變數讀**,絕不寫進程式碼或 commit。

**`GEMINI_API_KEY` 放在「專案根目錄」`.env`**(`arxiv-1-完成版/.env`,跨前後端共用):

```bash
# 在專案根目錄(backend 的上一層)
cp .env.example .env   # 專案根目錄那份 .env.example
# 編輯 .env,把 GEMINI_API_KEY 換成 https://aistudio.google.com/apikey 申請的真 key
```

後端載入順序:**先讀專案根目錄 `.env`(優先)→ 再讀 `backend/.env`(fallback,放後端專屬調參如 `ARXIV_*`)**。
`backend/.env` 不需要再放 key。

- **有 key** → 真呼叫 Gemini,markdown 報告為 AI 整理的中文綜述 + 各篇白話摘要。
- **沒 key** → 自動 fallback:報告開頭標示「[未設 GEMINI_API_KEY,以下為佔位摘要]」,
  各篇用 arXiv 原始 abstract 拼成。`GET /reports/today` 在沒 key 時仍回完整結構,方便自測 / 驗收。

所有 `.env` 已進 `.gitignore`,repo 只保留 `.env.example`。

## 手動觸發抓取(產生今日報告)

```bash
uv run python -m app.fetch
```

會抓最新論文、去重截前 5 篇、產出 markdown 報告,存到 `data/report-YYYY-MM-DD.json`(`data/` 已 gitignore)。

## 啟動 API 服務

```bash
uv run uvicorn app.main:app --port 8000
# 開發時可加 --reload
```

### API 契約端點

| Method | Path | 說明 |
|---|---|---|
| GET | `/reports/today` | 今日報告;無則 `404 {"detail": "今日報告尚未產生"}` |
| GET | `/reports` | 歷史報告日期清單(新到舊) |
| GET | `/reports/{date}` | 指定日期報告(`YYYY-MM-DD`),查無 `404` |
| GET | `/health` | 健康檢查 `{"status": "ok"}` |

所有回應 `Content-Type: application/json; charset=utf-8`。

`GET /reports/today` 回應結構:

```json
{
  "date": "2026-05-22",
  "title": "arXiv 每日科技論文摘要 · 2026-05-22",
  "markdownBody": "## 今日綜述\n...",
  "papers": [
    {
      "title": "...",
      "authors": ["..."],
      "arxivId": "2505.12345",
      "link": "https://arxiv.org/abs/2505.12345",
      "summary": "..."
    }
  ]
}
```

### 快速自測

```bash
uv run python -m app.fetch                   # 先產生今日報告
uv run uvicorn app.main:app --port 8000 &    # 起服務
curl http://127.0.0.1:8000/reports/today     # 應回 5 篇 + markdownBody
```

## 每日排程(cron 範例)

每天早上 06:00 自動抓取(請把路徑換成你的實際路徑):

```cron
0 6 * * * cd /path/to/arxiv-1-完成版/backend && /Users/you/.local/bin/uv run python -m app.fetch >> data/fetch.log 2>&1
```

> 提醒:`uv` 需用絕對路徑(cron 環境 PATH 較精簡);`which uv` 可查。

## 測試

```bash
uv run pytest          # 解析 / 去重 / 儲存 / fallback 單元測試(不碰網路)
```

## 設計依據(來自 `_Context/`)

- **arXiv 抓取**:端點 `export.arxiv.org/api/query`,`search_query=cat:cs.AI OR cat:cs.LG OR cat:cs.CL`,
  `sortBy=submittedDate&sortOrder=descending`;**多抓 15 篇 → 依 arxivId 去重 → 截最新 5 篇**
  (一篇可掛多分類會重複命中)。回傳是 Atom XML,用 feedparser 解析。
- **arXiv ToU**:連續請求自帶 ≥3 秒間隔、單一連線、follow http→https 導向。
- **可調環境變數**:`ARXIV_CATEGORIES`(逗號分隔)、`ARXIV_FETCH_SIZE`、`ARXIV_TOP_N`、
  `ARXIV_REQUEST_INTERVAL_SEC`、`GEMINI_MODEL`、`DATA_DIR`、`PORT`。

## 目錄結構

```
backend/
├── app/
│   ├── config.py     設定(讀 .env / 環境變數)
│   ├── models.py     Paper / Report(對齊 API 契約)
│   ├── arxiv.py      抓取 + Atom 解析 + 去重(純邏輯可測)
│   ├── gemini.py     Gemini 摘要 + 無 key fallback
│   ├── storage.py    每日 JSON 存取
│   ├── report.py     編排:抓取→摘要→存檔
│   ├── fetch.py      手動觸發 CLI(python -m app.fetch)
│   └── main.py       FastAPI app(uvicorn app.main:app)
├── tests/            單元測試
├── data/             每日報告 JSON(gitignore)
├── .env.example      環境變數範本(repo 只留這份)
└── pyproject.toml
```
