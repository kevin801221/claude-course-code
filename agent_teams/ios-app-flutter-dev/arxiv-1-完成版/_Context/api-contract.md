# API 契約與對接簽章(team lead 凍結 🔒)

> 這份是前後端 + 三個模組的**共同地基**。由 team lead 凍結,隊友照這份做。
> 要改任何一條,先用 mailbox 問 team lead、等批准,**不可自己改**。

## 1. 後端 HTTP 契約(backend-owner 照這份提供)

所有回應 `Content-Type: application/json; charset=utf-8`。

### GET /reports/today
回今天那份報告。

```json
{
  "date": "2026-05-22",
  "title": "arXiv 每日科技論文摘要 · 2026-05-22",
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
- 今天還沒產出報告時:回 `404`,body `{ "detail": "今日報告尚未產生" }`。

### GET /reports
歷史報告日期清單,新到舊。

```json
["2026-05-22", "2026-05-21", "2026-05-20"]
```

### GET /reports/{date}
指定日期報告,結構同 `/reports/today`。查無該日期回 `404`。

### 健康檢查(選配,驗收方便)
`GET /health` → `{ "status": "ok" }`

---

## 2. 共用層介面(team lead 已實作於 lib/shared/,前端隊友直接用)

- `Report` / `Paper`(`lib/shared/models.dart`):對應上面 JSON,有 `fromJson` / `toJson`。
- `ReportApiClient`(`lib/shared/report_api_client.dart`):
  - `Future<Report> today()`
  - `Future<List<String>> list()`
  - `Future<Report> byDate(String date)`
  - 失敗拋 `ReportApiException`(含 `statusCode`)。
- `AppConfig`(`lib/shared/app_config.dart`):`backendBaseUrl`、`readingReminderThreshold`、`breathingDuration`。

> 前端**只透過 `ReportApiClient` 拿資料**,不要自己寫 http / jsonDecode。

---

## 3. 前端模組對接簽章(team lead 凍結,main.dart 靠這兩個 public 入口)

team lead 在 `lib/reader/` 與 `lib/breathing/` 各放了一個 **stub**,定義 public 入口的簽章。
隊友把 stub 換成真實作,**可以在自己目錄新增任意檔案**,但**保持下面這兩個 public 入口的名稱與簽章不變**(main.dart 靠它們組裝);要改簽章先 mailbox 問 team lead。

### reader-owner 暴露(`lib/reader/reader_home_page.dart`)
```dart
class ReaderHomePage extends StatelessWidget {
  const ReaderHomePage({super.key});
}
```
- App 首頁主體。內部用 `ReportApiClient` 拉今日報告 + 歷史清單,render `markdownBody`、列出 5 篇 papers(標題/作者/arXiv 連結),提供歷史回看。

### breathing-owner 暴露(`lib/breathing/breathing_reminder_scope.dart`)
```dart
class BreathingReminderScope extends StatefulWidget {
  final Widget child;
  const BreathingReminderScope({super.key, required this.child});
}
```
- 包住閱讀內容(`child`)。內部累積閱讀時間,達 `AppConfig.readingReminderThreshold`(預設 10 分鐘)時,疊一層 60 秒呼吸動畫 overlay(跟著圓圈吸/吐),做完或使用者略過後回到閱讀並重置計時。
- 提示溫和、可略過,不強迫、不宣稱療效。

### main.dart 組裝(team lead 擁有)
```dart
home: const BreathingReminderScope(child: ReaderHomePage()),
```

---

## 4. 安全紅線(全員)
- Gemini API key **只從環境變數 `GEMINI_API_KEY` 讀**;`.env` 進 `.gitignore`,repo 只留 `.env.example`。
- 任何人不准把 key 寫進程式碼或 commit 進 repo。

_凍結時間:研究收斂後由 team lead 確認。研究結論的具體數值(arXiv 領域與排序、閱讀間隔、呼吸節奏)見 `app-spec.md` 的「研究結論」。_
