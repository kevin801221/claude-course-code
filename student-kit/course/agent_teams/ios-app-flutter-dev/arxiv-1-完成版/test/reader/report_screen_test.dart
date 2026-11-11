import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:arxiv_reader/reader/report_screen.dart';
import 'package:arxiv_reader/shared/models.dart';
import 'package:arxiv_reader/shared/report_api_client.dart';

/// 注入用的假 client:不打網路,回傳預先準備好的資料或丟錯誤。
class _FakeReportApiClient extends ReportApiClient {
  final Report? report;
  final int? throwStatusCode;

  _FakeReportApiClient({
    this.report,
    this.throwStatusCode,
  }) : super(baseUrl: 'http://test.local');

  @override
  Future<Report> today() async {
    if (throwStatusCode != null) {
      throw ReportApiException('fake', statusCode: throwStatusCode);
    }
    return report!;
  }

  @override
  Future<Report> byDate(String date) => today();

  @override
  Future<List<String>> list() async => const ['2026-05-22', '2026-05-21'];
}

Report _sampleReport() => const Report(
      date: '2026-05-22',
      title: 'arXiv 每日科技論文摘要 · 2026-05-22',
      markdownBody: '## 今日綜述\n這是測試用的綜述內容。',
      papers: [
        Paper(
          title: '測試論文一',
          authors: ['Alice', 'Bob'],
          arxivId: '2505.00001',
          link: 'https://arxiv.org/abs/2505.00001',
          summary: '第一篇摘要。',
        ),
        Paper(
          title: '測試論文二',
          authors: ['Carol'],
          arxivId: '2505.00002',
          link: 'https://arxiv.org/abs/2505.00002',
          summary: '第二篇摘要。',
        ),
      ],
    );

void main() {
  Widget wrap(ReportApiClient client) =>
      MaterialApp(home: ReportScreen(client: client));

  testWidgets('成功載入時顯示報告標題與論文清單', (tester) async {
    await tester.pumpWidget(wrap(_FakeReportApiClient(report: _sampleReport())));
    await tester.pumpAndSettle();

    expect(find.text('arXiv 每日科技論文摘要 · 2026-05-22'), findsOneWidget);
    expect(find.text('測試論文一'), findsOneWidget);
    expect(find.text('測試論文二'), findsOneWidget);
    expect(find.text('今日 2 篇論文'), findsOneWidget);
    // 明確結尾,不無限滑。
    expect(find.text('— 今天讀完了,明天見 —'), findsOneWidget);
  });

  testWidgets('今日報告尚未產生(404)顯示友善空狀態 + 重新整理', (tester) async {
    await tester.pumpWidget(wrap(_FakeReportApiClient(throwStatusCode: 404)));
    await tester.pumpAndSettle();

    expect(find.textContaining('今日報告尚未產生'), findsOneWidget);
    expect(find.text('重新整理'), findsOneWidget);
  });

  testWidgets('後端錯誤(500)顯示錯誤狀態 + 重試', (tester) async {
    await tester.pumpWidget(wrap(_FakeReportApiClient(throwStatusCode: 500)));
    await tester.pumpAndSettle();

    expect(find.textContaining('讀取報告失敗'), findsOneWidget);
    expect(find.text('重試'), findsOneWidget);
  });
}
