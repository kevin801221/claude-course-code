# API 契約與對接簽章（team lead 凍結 🔒）

> 這份是前後端 + 三個模組的**共同地基**。由 team lead 凍結，隊友照這份做。
> 要改任何一條，先用 mailbox 問 team lead、等批准，**不可自己改**。
> 凍結時間：2026-05-23。

## 1. 後端 HTTP 契約（backend-owner 照這份提供）

所有回應 `Content-Type: application/json; charset=utf-8`。

### GET /reports/today
回今天那份報告。

```json
{
  "date": "2026-05-23",
  "title": "arXiv 每日科技論文摘要 · 2026-05-23",
  "markdownBody": "## 今日綜述\n...(整份 markdown 報告)...",
  "papers": [
    {
      "title": "論文標題",
      "authors": ["First Author", "Second Author"],
      "arxivId": "2505.12345",
      "link": "https://arxiv.org/abs/2505.12345",
      "summary": "Gemini 整理的單篇摘要(數句)"
    }
  ]
}
```
- `papers` 固定 5 篇(抓不到 5 篇時回實際篇數)。
- 今天還沒產出報告時：回 `404`，body `{ "detail": "今日報告尚未產生" }`。
- `date` 一律 `YYYY-MM-DD`。

### GET /reports
歷史報告日期清單，新到舊。

```json
["2026-05-23", "2026-05-22", "2026-05-21"]
```

### GET /reports/{date}
指定日期報告，結構同 `/reports/today`。查無該日期回 `404`。

### GET /health（驗收方便）
`GET /health` → `{ "status": "ok" }`

---

## 2. 共用層 Dart 介面（team lead 已實作於 lib/shared/，前端隊友直接用）

- **`Paper` / `Report`**（`lib/shared/models.dart`）：對應上面 JSON，有 `fromJson` / `toJson`；`Paper.authorsLine` 給顯示用。
- **`ReportApiClient`**（`lib/shared/report_api_client.dart`）：
  - `Future<Report> today()`
  - `Future<List<String>> list()`
  - `Future<Report> byDate(String date)`
  - 失敗拋 `ReportApiException`(含 `statusCode`，連不上時為 null)。
  - 建構可注入 `http.Client`(測試用 mock client)。
- **`AppConfig`**（`lib/shared/app_config.dart`）：
  - `backendBaseUrl`（可用 `--dart-define=BACKEND_BASE_URL=...` 覆寫）
  - `effectiveReadingThreshold`（demo 模式 20 秒、正式 20 分鐘；用 `--dart-define=DEMO=true` 切 demo）
  - `breathingDuration`(60s)、`breathingPhaseDuration`(4s)、`breathingRounds`(3)

> 前端**只透過 `ReportApiClient` 拿資料**，不要自己寫 http / jsonDecode。
> 閱讀門檻、呼吸節奏**只從 `AppConfig` 讀**，不要自己寫 magic number。

---

## 3. Widget 層交接介面（整合用，reader / breathing 照這份 export）

整合階段 team lead 會在 `lib/main.dart` 這樣組裝：
```dart
home: BreathingReminderScope(child: ReaderHomePage())
```
所以兩個前端隊友各自要 export 一個進入點 widget：

### reader-owner → `lib/reader/reader_home_page.dart`
- `class ReaderHomePage extends StatelessWidget`(或 Stateful)，**無必填建構參數**。
- 內部用 `ReportApiClient().today()` 拉今日報告，render `markdownBody` + 列 5 篇 papers，提供歷史回看(用 `list()` / `byDate()`)。

### breathing-owner → `lib/breathing/breathing_reminder_scope.dart`
- `class BreathingReminderScope extends StatefulWidget`，建構：`const BreathingReminderScope({required this.child})`。
- 包住 child，內部累積「閱讀時間」達 `AppConfig.effectiveReadingThreshold` → 蓋一層 60 秒 Box Breathing 動畫 overlay → 做完(或使用者略過)移除 overlay 回到 child。
- 對外提供一個可讓 reader 通知「使用者正在閱讀」的機制(見下)，但**不可改 reader 的檔案**。

### 跨模組依賴：閱讀計時誰來餵？
- breathing 的計時需要知道「使用者正在閱讀」。MVP 約定：**只要 App 在前景且停在閱讀畫面就算在閱讀**，由 `BreathingReminderScope` 自己用 `Ticker`/`Timer` 累積即可，**不需要 reader 主動回報**(降低耦合)。
- 若 breathing-owner 想要更精準(例如捲動才算閱讀)，**先 mailbox 問 team lead**，由 team lead 決定是否在 shared 加一個 `ReadingActivityNotifier`，不要自己去改 reader。

---

## 4. 安全紅線（全員）
- `GEMINI_API_KEY` 只從環境變數讀；`.env` 進 `.gitignore`，repo 只留 `.env.example`。
- 任何隊友不准把 key 寫進程式碼或 commit。
- 後端沒 key 時走 mock/sample 報告 fallback，讓前端與 pipeline 仍可驗收。

---

## 5. 目錄擁有權（不重疊，平行不撞檔）
| 範圍 | 擁有者 |
|---|---|
| `lib/shared/`、`lib/main.dart`、`pubspec.yaml`、本契約 | team lead |
| `backend/` | backend-owner |
| `lib/reader/`、`test/reader/` | reader-owner |
| `lib/breathing/`、`test/breathing/` | breathing-owner |
