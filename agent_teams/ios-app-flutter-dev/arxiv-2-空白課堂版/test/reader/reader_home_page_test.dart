/// reader-owner 的 widget 測試 —— 只測 lib/reader/ 範圍。
///
/// 透過注入 mock http.Client 的 ReportApiClient 測試：
///   1. 成功渲染今日報告（markdownBody + 5 篇 papers）
///   2. 404 / 連線失敗時顯示友善錯誤訊息
///   3. 歷史日期清單能取得並顯示（list()）
library;

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

import 'package:arxiv_reader/shared/models.dart';
import 'package:arxiv_reader/shared/report_api_client.dart';
import 'package:arxiv_reader/reader/reader_home_page.dart';

// ── 測試用 fixture 資料 ──────────────────────────────────────

const _testDate = '2026-05-23';

final _testPapers = List.generate(
  5,
  (i) => {
    'title': 'Paper Title $i',
    'authors': ['Author A$i', 'Author B$i'],
    'arxivId': '2505.0000$i',
    'link': 'https://arxiv.org/abs/2505.0000$i',
    'summary': 'Summary of paper $i.',
  },
);

final _testReportJson = {
  'date': _testDate,
  'title': 'arXiv 每日科技論文摘要 · $_testDate',
  'markdownBody': '## 今日綜述\n這是測試報告的 markdown 內容。\n\n### 論文亮點\n- 項目一\n- 項目二',
  'papers': _testPapers,
};

// ── helper：建立注入 mock client 的 ReportApiClient ──────────

ReportApiClient _makeClient(MockClientHandler handler) {
  return ReportApiClient(client: MockClient(handler));
}

/// 回傳 200 今日報告的 mock client。
ReportApiClient _successClient() {
  return _makeClient((request) async {
    if (request.url.path == '/reports/today') {
      return http.Response(
        jsonEncode(_testReportJson),
        200,
        headers: {'content-type': 'application/json; charset=utf-8'},
      );
    }
    if (request.url.path == '/reports') {
      return http.Response(
        jsonEncode([_testDate, '2026-05-22', '2026-05-21']),
        200,
        headers: {'content-type': 'application/json; charset=utf-8'},
      );
    }
    return http.Response('Not Found', 404);
  });
}

/// 今日報告回 404 的 mock client。
ReportApiClient _notFoundClient() {
  return _makeClient((request) async {
    return http.Response(
      jsonEncode({'detail': '今日報告尚未產生'}),
      404,
      headers: {'content-type': 'application/json; charset=utf-8'},
    );
  });
}

/// 後端不可用的 mock client（回 503 模擬連線/伺服器錯誤）。
ReportApiClient _networkErrorClient() {
  return _makeClient((request) async {
    return http.Response(
      '{"error": "Service Unavailable"}',
      503,
      headers: {'content-type': 'application/json; charset=utf-8'},
    );
  });
}

// ── helper：pump ReaderHomePage ──────────────────────────────

Future<void> _pumpPage(
  WidgetTester tester, {
  required ReportApiClient client,
}) async {
  await tester.pumpWidget(
    MaterialApp(
      home: ReaderHomePage(client: client),
    ),
  );
}

// ── 測試群組 ─────────────────────────────────────────────────

void main() {
  group('ReaderHomePage —— 成功載入今日報告', () {
    testWidgets('載入中顯示 CircularProgressIndicator', (tester) async {
      final client = _successClient();
      await _pumpPage(tester, client: client);

      // 第一次 pump：async future 尚未完成，應顯示 loading
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('報告標題顯示在 AppBar', (tester) async {
      final client = _successClient();
      await _pumpPage(tester, client: client);
      await tester.pumpAndSettle();

      // AppBar title 應顯示日期
      expect(find.text(_testDate), findsWidgets);
    });

    testWidgets('markdownBody 的文字內容被渲染', (tester) async {
      final client = _successClient();
      await _pumpPage(tester, client: client);
      await tester.pumpAndSettle();

      // flutter_markdown 會把 ## 轉成 Text widget，找關鍵字
      expect(find.textContaining('今日綜述'), findsWidgets);
    });

    testWidgets('5 篇 papers 標題都出現在畫面', (tester) async {
      final client = _successClient();
      await _pumpPage(tester, client: client);
      await tester.pumpAndSettle();

      for (var i = 0; i < 5; i++) {
        expect(find.textContaining('Paper Title $i'), findsWidgets);
      }
    });

    testWidgets('papers 的作者顯示 authorsLine 格式', (tester) async {
      final client = _successClient();
      await _pumpPage(tester, client: client);
      await tester.pumpAndSettle();

      // 第一篇作者應顯示 "Author A0, Author B0"
      expect(find.textContaining('Author A0, Author B0'), findsWidgets);
    });

    testWidgets('papers 的 arXiv 連結有出現', (tester) async {
      final client = _successClient();
      await _pumpPage(tester, client: client);
      await tester.pumpAndSettle();

      expect(
        find.textContaining('arxiv.org/abs/2505.00000'),
        findsWidgets,
      );
    });

    testWidgets('顯示 AppBar 歷史 icon', (tester) async {
      final client = _successClient();
      await _pumpPage(tester, client: client);
      await tester.pumpAndSettle();

      expect(find.byIcon(Icons.history), findsOneWidget);
    });
  });

  group('ReaderHomePage —— 錯誤態', () {
    testWidgets('後端 404 時顯示「今日報告尚未產生」友善訊息', (tester) async {
      final client = _notFoundClient();
      await _pumpPage(tester, client: client);
      await tester.pumpAndSettle();

      expect(find.textContaining('今日報告尚未產生'), findsOneWidget);
      // 確認沒有 crash（無 CircularProgressIndicator 遮住整個畫面）
      expect(find.byType(CircularProgressIndicator), findsNothing);
    });

    testWidgets('404 時顯示「重新載入」按鈕', (tester) async {
      final client = _notFoundClient();
      await _pumpPage(tester, client: client);
      await tester.pumpAndSettle();

      expect(find.textContaining('重新載入'), findsOneWidget);
    });

    testWidgets('後端 503 時顯示連線錯誤友善訊息（不 crash）', (tester) async {
      final client = _networkErrorClient();
      await _pumpPage(tester, client: client);
      await tester.pumpAndSettle();

      // 後端不可用應顯示通用友善錯誤，不 crash
      expect(find.byType(CircularProgressIndicator), findsNothing);
      // 錯誤訊息包含「無法取得今日報告」
      expect(find.textContaining('無法取得今日報告'), findsOneWidget);
    });
  });

  group('ReaderHomePage —— Report model', () {
    test('Report.fromJson 正確解析 papers', () {
      final report = Report.fromJson(_testReportJson);
      expect(report.date, _testDate);
      expect(report.papers.length, 5);
      expect(report.papers[0].title, 'Paper Title 0');
      expect(report.papers[0].authorsLine, 'Author A0, Author B0');
      expect(report.papers[0].link, 'https://arxiv.org/abs/2505.00000');
    });

    test('Paper.authorsLine 正確拼接多位作者', () {
      const paper = Paper(
        title: 'Test',
        authors: ['Alice', 'Bob', 'Charlie'],
        arxivId: '0000.00000',
        link: 'https://arxiv.org/abs/0000.00000',
        summary: 'Test summary.',
      );
      expect(paper.authorsLine, 'Alice, Bob, Charlie');
    });
  });

  group('ReaderHomePage —— 歷史清單', () {
    testWidgets('點歷史 icon 開啟 bottom sheet', (tester) async {
      final client = _successClient();
      await _pumpPage(tester, client: client);
      await tester.pumpAndSettle();

      // 點擊歷史按鈕
      await tester.tap(find.byIcon(Icons.history));
      await tester.pumpAndSettle();

      // bottom sheet 出現，且包含日期清單
      expect(find.text('選擇歷史日期'), findsOneWidget);
      expect(find.textContaining('2026-05-22'), findsOneWidget);
    });
  });
}
