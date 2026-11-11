// 共用層 + App 啟動 smoke test。
// 各模組(reader / breathing)的測試由各自隊友放在 test/reader/、test/breathing/。

import 'package:flutter_test/flutter_test.dart';

import 'package:arxiv_reader/main.dart';
import 'package:arxiv_reader/shared/models.dart';
import 'package:arxiv_reader/shared/app_config.dart';

void main() {
  testWidgets('App 啟動顯示標題', (WidgetTester tester) async {
    await tester.pumpWidget(const ArxivReaderApp());
    expect(find.text('arXiv 每日論文閱讀器'), findsWidgets);
  });

  test('Report.fromJson 解析契約結構', () {
    final report = Report.fromJson({
      'date': '2026-05-23',
      'title': 'arXiv 每日科技論文摘要 · 2026-05-23',
      'markdownBody': '## 今日綜述\n...',
      'papers': [
        {
          'title': 'A Paper',
          'authors': ['Alice', 'Bob'],
          'arxivId': '2505.12345',
          'link': 'https://arxiv.org/abs/2505.12345',
          'summary': '一段摘要',
        },
      ],
    });
    expect(report.date, '2026-05-23');
    expect(report.papers, hasLength(1));
    expect(report.papers.first.authorsLine, 'Alice, Bob');
  });

  test('凍結的呼吸節奏常數', () {
    expect(AppConfig.breathingRounds, 3);
    expect(AppConfig.breathingPhaseDuration, const Duration(seconds: 4));
    expect(AppConfig.readingReminderThreshold, const Duration(minutes: 20));
  });
}
