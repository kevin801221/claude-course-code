// 共用層 smoke test(team lead 維護)。
// reader-owner / breathing-owner 各自的模組測試放自己目錄下。

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:arxiv_reader/main.dart';

void main() {
  testWidgets('App 能起來且渲染出首頁 Scaffold', (WidgetTester tester) async {
    await tester.pumpWidget(const ArxivReaderApp());
    await tester.pump();

    // BreathingReminderScope 包住 ReaderHomePage,首頁主體可見即通過 smoke。
    expect(find.byType(MaterialApp), findsOneWidget);
    expect(find.byType(Scaffold), findsWidgets);
  });
}
