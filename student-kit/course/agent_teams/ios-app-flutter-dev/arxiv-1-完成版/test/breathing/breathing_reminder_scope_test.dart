import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:arxiv_reader/breathing/breathing_overlay.dart';
import 'package:arxiv_reader/breathing/breathing_reminder_scope.dart';

void main() {
  Widget host(Widget child) => MaterialApp(home: Scaffold(body: child));

  testWidgets('門檻 0(關閉)時永遠只顯示閱讀內容,不跳呼吸 overlay', (tester) async {
    await tester.pumpWidget(host(
      const BreathingReminderScope(
        threshold: Duration.zero,
        child: Text('閱讀內容'),
      ),
    ));
    await tester.pump(const Duration(seconds: 2));

    expect(find.text('閱讀內容'), findsOneWidget);
    expect(find.byType(BreathingOverlay), findsNothing);
  });

  testWidgets('累積達門檻後疊出呼吸 overlay', (tester) async {
    await tester.pumpWidget(host(
      const BreathingReminderScope(
        threshold: Duration(seconds: 2),
        // 真實 App 的 child 是滿版的 ReaderHomePage(Scaffold);測試用滿版盒模擬。
        child: SizedBox.expand(child: Center(child: Text('閱讀內容'))),
      ),
    ));
    expect(find.byType(BreathingOverlay), findsNothing);

    // 推進超過門檻 → overlay 出現,顯示階段文字。
    await tester.pump(const Duration(seconds: 3));
    expect(find.byType(BreathingOverlay), findsOneWidget);
    expect(find.text('吸氣'), findsOneWidget);

    // 點「略過」→ overlay 消失,回到閱讀。
    await tester.tap(find.text('略過,繼續閱讀'));
    await tester.pump();
    expect(find.byType(BreathingOverlay), findsNothing);
    expect(find.text('閱讀內容'), findsOneWidget);

    // 收掉殘留的計時 timer,避免測試結束時報 pending timer。
    await tester.pumpWidget(host(const SizedBox.shrink()));
  });

  testWidgets('呼吸 overlay 顯示時攔截背景觸控,不穿透到 reader', (tester) async {
    var bgTaps = 0;
    await tester.pumpWidget(host(
      BreathingReminderScope(
        threshold: const Duration(seconds: 2),
        // 背景閱讀內容:可被點擊。呼吸進行中點背景不該觸發它。
        child: GestureDetector(
          onTap: () => bgTaps++,
          behavior: HitTestBehavior.opaque,
          child: const SizedBox.expand(child: Center(child: Text('閱讀內容'))),
        ),
      ),
    ));

    // overlay 未出現前,點背景會觸發。
    await tester.tapAt(const Offset(20, 20));
    expect(bgTaps, 1);

    // 累積達門檻 → overlay 出現。
    await tester.pump(const Duration(seconds: 3));
    expect(find.byType(BreathingOverlay), findsOneWidget);

    // overlay 顯示中點背景空白區(非按鈕)→ 被 modal barrier 吃掉,不穿透。
    await tester.tapAt(const Offset(20, 20));
    expect(bgTaps, 1);

    // 收掉殘留計時 timer。
    await tester.pumpWidget(host(const SizedBox.shrink()));
  });

  testWidgets('呼吸動畫跑完(onDone)會自動移除 overlay', (tester) async {
    var done = false;
    await tester.pumpWidget(host(
      BreathingOverlay(
        totalDuration: const Duration(seconds: 16),
        onDone: () => done = true,
      ),
    ));

    expect(find.byType(BreathingOverlay), findsOneWidget);
    // 一輪 16 秒(吸4停4吐4停4)跑完;多 pump 一幀讓 completed 狀態確實觸發。
    await tester.pump(const Duration(seconds: 16));
    await tester.pump(const Duration(milliseconds: 1));
    expect(done, isTrue);
  });
}
