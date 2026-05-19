# 設計文件：autocv ui 視覺駕駛艙

> 日期：2026-05-19
> 作者：羅子嘉（with Claude）
> 狀態：已 approve，待轉實作計畫
> 目標 repo：`/Users/kevinluo/auto-cv-train-inference-optimization`（GitHub: kevin801221/auto-cv-train-optimization-claude_code）

## 1. 目標

替既有 `autocv` 通用 CV 模板加一個**本機視覺駕駛艙**：一個指令 `autocv ui` 開瀏覽器，選 config、按 Run，看 5 階段 pipeline 真實接力、訓練曲線即時長出、跑完展示成果圖。兌現 README 對「無碼視覺駕駛艙」的懸念，且**是真的能跑，不是假動畫**。

## 2. 定位與誠實原則

「5 個 agent 接力」= 真實 pipeline 5 階段（data→split→train→optimize→infer），每階段一個狀態燈。不偽造任何進度或結果。誠實是這個 repo 的品牌核心（呼應「不偷燒 GPU」的 GO-gate）。

## 3. 鎖定決策

| 決策 | 結論 |
|---|---|
| 是否要做 | 要，做真的（非假 demo） |
| 前端路線 | FastAPI 後端 + 自刻單頁前端（零建置，深色 cockpit 質感） |
| 範圍 | 本機單人、一次一條 pipeline；無登入/雲端/DB/多工 |
| 驅動方式 | 後端直接 import autocv 函式，背景 thread 執行，事件經 queue→WebSocket |
| GO-gate | 保留並在 UI 強制：train/optimize 前彈預估時間 modal，需點確認 |
| CLI | 新增 `autocv ui` 子命令（起 uvicorn + 開瀏覽器） |

## 4. 架構

```
瀏覽器 (單頁自刻 UI, 深色)
   │  WebSocket /ws  (即時事件: stage / log / metric / result / await_confirm)
   │  REST           (GET /configs, POST /run, POST /confirm, GET /)
   ▼
FastAPI (uvicorn, 由 `autocv ui` 啟動)
   │  背景 thread: runner 依序跑 autocv.data/split/train/optimize/infer
   │  事件 queue → WebSocket 廣播
   └  train/optimize: 讀 YOLO 寫的 runs/<name>/results.csv → 推曲線點
```

- backend 不開 shell 亂跑；直接呼叫套件函式，stage 邊界由 runner 控制。
- 訓練/優化的 GO-gate：runner 跑到該階段先發 `await_confirm`（含預估時間），暫停在 `threading.Event`，等前端 `POST /confirm` 才繼續。
- 一次只允許一個 job（單人本機）；重複啟動回 409。

## 5. 元件邊界

| 檔 | 職責 | 介面 |
|---|---|---|
| `src/autocv/server/__init__.py` | package marker | — |
| `src/autocv/server/app.py` | FastAPI app：REST + WebSocket，掛載 static | `create_app() -> FastAPI` |
| `src/autocv/server/runner.py` | 背景 thread 跑 pipeline，發事件，管 GO-gate confirm | `PipelineRunner`（`start(cfg,root,stages)`, `confirm()`, `events` queue, `status`） |
| `src/autocv/server/events.py` | 事件資料結構（dataclass）與型別常數 | `Event`（kind, stage, payload） |
| `src/autocv/server/static/index.html` | 單頁 UI：5 階段燈、log、曲線(canvas)、成果圖廊、GO-gate modal。HTML/CSS/JS 內聯，零建置 | — |
| `src/autocv/cli.py`（改） | 加 `ui` 子命令：起 uvicorn + webbrowser 開頁 | `autocv ui [--config] [--host] [--port] [--no-browser]` |
| `tests/test_server.py` | TestClient 測 REST + 事件協定 + GO-gate；不跑真訓練 | — |

## 6. 事件協定（WebSocket，JSON）

| kind | 何時 | payload |
|---|---|---|
| `stage` | 階段狀態變更 | `{name, status: pending\|running\|done\|error\|skipped}` |
| `log` | 有新輸出行 | `{line}` |
| `metric` | 訓練/優化每讀到一列 results.csv | `{epoch, map50, map, loss}` |
| `await_confirm` | train/optimize 啟動前 | `{stage, estimate_min, detail}` |
| `result` | infer 完成 | `{images: [url...], map50, map, summary_md}` |
| `done` | 全 pipeline 結束 | `{ok, error?}` |

前端對 `await_confirm` 跳 modal，使用者按「開始」→ `POST /confirm {stage}` → runner 放行。

## 7. 資料流

`GET /configs` 列 `configs/*.yaml` → 使用者選 → `POST /run {config, optimize:bool}` 起 runner thread → WebSocket 串 stage/log/metric → train/optimize 前 `await_confirm` 暫停 → 確認後續跑 → infer 後 `result`（成果圖用 `GET /runs/infer/<png>` 靜態服務）→ `done`。

## 8. 測試策略

- `TestClient`：`GET /configs` 回現有 yaml 清單；`POST /run` 回 job 並進 running；重複 `POST /run` 回 409。
- runner 注入假 stage 函式（不 import ultralytics）：驗證事件序 `stage(pending→running→done)` + `log` + `done`。
- GO-gate：含 train 的流程會發 `await_confirm` 且在未 `confirm` 前不前進；`confirm` 後才 `done`。
- 不在 CI 跑真實下載/訓練（需 key+GPU）。CI 加跑 `test_server.py`。

## 9. 風險與緩解

| 風險 | 緩解 |
|---|---|
| 長時間訓練阻塞 server | 背景 thread + queue，WebSocket 只推播；event loop 不被卡 |
| 截圖不夠「爆款」 | 深色儀表板配色 + canvas 即時曲線動畫，視覺為投資重點 |
| 假 agent 被識破 | 不偽造，映射真實 5 階段，誠實接住品牌 |
| 範圍膨脹成 SaaS | 明文 YAGNI：無登入/雲端/DB/多工，留作 README 下一輪懸念 |
| 前端建置鏈污染 uv-only | 單一 index.html 內聯 JS/CSS，零 npm/build |
| GO-gate 被繞過 | runner 端 `threading.Event` 阻塞，不靠前端自律；未 confirm 物理上不進訓練 |

## 10. 完成標準

- `uv run autocv ui` 起服務並開瀏覽器，列得到 `configs/wafer.yaml`
- 假資料/小設定下能看到 5 階段燈依序變、log 串流、`done`
- train 階段一定先跳 GO-gate modal，不確認不訓練
- `tests/test_server.py` 全綠，既有 10 測試不破，ruff 乾淨
- README 🔒 區塊把「無碼視覺駕駛艙」那條改成已實作 + 截圖（實作後另行更新）
- 公開 repo commit 訊息全程純技術，無行銷字眼
