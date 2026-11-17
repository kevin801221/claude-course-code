import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:arxiv_reader/breathing/breathing_reminder_scope.dart';
import 'package:arxiv_reader/breathing/breathing_overlay.dart';

/// 建立包住 [child] 的標準 MaterialApp，供測試掛載用。
Widget _app(Widget child) =>
    MaterialApp(home: Scaffold(body: child));

/// 快轉 [rounds] 輪 Box Breathing（每輪 4 相）所需時間。
///
/// 每相 pump 一次（phaseDuration + 10ms 緩衝），讓 AnimationController
/// 確實完成並觸發 addStatusListener。
Future<void> _pumpBreathingRounds(
  WidgetTester tester, {
  required int rounds,
  required Duration phaseDuration,
}) async {
  final phasesTotal = rounds * 4;
  final tick = phaseDuration + const Duration(milliseconds: 10);
  for (var i = 0; i < phasesTotal; i++) {
    await tester.pump(tick);
  }
  await tester.pump(); // 最後 setState 重建
}

void main() {
  // ── BreathingReminderScope 測試 ──────────────────────────────────────────

  group('BreathingReminderScope', () {
    testWidgets('未達門檻時不顯示 overlay', (tester) async {
      const threshold = Duration(seconds: 5);

      await tester.pumpWidget(
        _app(
          BreathingReminderScope(
            readingThreshold: threshold,
            breathingPhaseDuration: const Duration(milliseconds: 100),
            breathingRounds: 1,
            child: const Text('閱讀內容'),
          ),
        ),
      );

      // 快轉 4 秒（還未到門檻）
      for (var i = 0; i < 4; i++) {
        await tester.pump(const Duration(seconds: 1));
      }

      expect(find.byType(BreathingOverlay), findsNothing);
      expect(find.text('閱讀內容'), findsOneWidget);
    });

    testWidgets('達到門檻後顯示 overlay', (tester) async {
      const threshold = Duration(seconds: 3);

      await tester.pumpWidget(
        _app(
          BreathingReminderScope(
            readingThreshold: threshold,
            breathingPhaseDuration: const Duration(milliseconds: 50),
            breathingRounds: 1,
            child: const Text('閱讀內容'),
          ),
        ),
      );

      // 每秒 tick 一次，超過 3 秒門檻
      for (var i = 0; i < 4; i++) {
        await tester.pump(const Duration(seconds: 1));
      }
      await tester.pump();

      expect(find.byType(BreathingOverlay), findsOneWidget);
    });

    testWidgets('點略過後 overlay 消失並重置計時', (tester) async {
      const threshold = Duration(seconds: 2);

      await tester.pumpWidget(
        _app(
          BreathingReminderScope(
            readingThreshold: threshold,
            breathingPhaseDuration: const Duration(milliseconds: 50),
            breathingRounds: 1,
            child: const Text('閱讀內容'),
          ),
        ),
      );

      // 快轉到 overlay 出現
      for (var i = 0; i < 3; i++) {
        await tester.pump(const Duration(seconds: 1));
      }
      await tester.pump();
      expect(find.byType(BreathingOverlay), findsOneWidget);

      // 點「略過 / 我好了」（已在頂部列，確保在螢幕內）
      await tester.tap(find.byKey(const Key('skip_button')));
      await tester.pump();

      expect(find.byType(BreathingOverlay), findsNothing);
      expect(find.text('閱讀內容'), findsOneWidget);
    });

    testWidgets('略過後重置計時，再次達門檻時再次顯示 overlay', (tester) async {
      const threshold = Duration(seconds: 2);

      await tester.pumpWidget(
        _app(
          BreathingReminderScope(
            readingThreshold: threshold,
            breathingPhaseDuration: const Duration(milliseconds: 50),
            breathingRounds: 1,
            child: const Text('閱讀內容'),
          ),
        ),
      );

      // 第一次觸發
      for (var i = 0; i < 3; i++) {
        await tester.pump(const Duration(seconds: 1));
      }
      await tester.pump();
      expect(find.byType(BreathingOverlay), findsOneWidget);

      // 略過 → 重置
      await tester.tap(find.byKey(const Key('skip_button')));
      await tester.pump();

      // 重新計時，再次到達門檻
      for (var i = 0; i < 3; i++) {
        await tester.pump(const Duration(seconds: 1));
      }
      await tester.pump();

      expect(find.byType(BreathingOverlay), findsOneWidget);
    });
  });

  // ── BreathingOverlay 測試 ────────────────────────────────────────────────

  group('BreathingOverlay', () {
    testWidgets('顯示初始吸氣相位', (tester) async {
      await tester.pumpWidget(
        _app(
          BreathingOverlay(
            onDone: () {},
            phaseDuration: const Duration(milliseconds: 100),
            rounds: 1,
          ),
        ),
      );

      expect(find.text('吸氣'), findsOneWidget);
      expect(find.byKey(const Key('skip_button')), findsOneWidget);
    });

    testWidgets('做完所有輪次後顯示完成畫面', (tester) async {
      const phase = Duration(milliseconds: 50);
      const rounds = 1;

      await tester.pumpWidget(
        _app(
          BreathingOverlay(
            onDone: () {},
            phaseDuration: phase,
            rounds: rounds,
          ),
        ),
      );

      // 逐相快轉（1 輪 × 4 相 × 50ms）
      await _pumpBreathingRounds(tester, rounds: rounds, phaseDuration: phase);

      expect(find.text('很好！繼續閱讀吧'), findsOneWidget);
      expect(find.byKey(const Key('continue_button')), findsOneWidget);
    });

    testWidgets('點繼續閱讀按鈕呼叫 onDone', (tester) async {
      var doneCalled = false;
      const phase = Duration(milliseconds: 50);

      await tester.pumpWidget(
        _app(
          BreathingOverlay(
            onDone: () => doneCalled = true,
            phaseDuration: phase,
            rounds: 1,
          ),
        ),
      );

      await _pumpBreathingRounds(tester, rounds: 1, phaseDuration: phase);

      await tester.tap(find.byKey(const Key('continue_button')));
      await tester.pump();

      expect(doneCalled, isTrue);
    });

    testWidgets('顯示免責聲明文字', (tester) async {
      await tester.pumpWidget(
        _app(
          BreathingOverlay(
            onDone: () {},
            phaseDuration: const Duration(milliseconds: 100),
            rounds: 1,
          ),
        ),
      );

      expect(find.text('僅供休息提醒，非醫療建議'), findsOneWidget);
    });

    testWidgets('顯示輪次資訊', (tester) async {
      await tester.pumpWidget(
        _app(
          BreathingOverlay(
            onDone: () {},
            phaseDuration: const Duration(milliseconds: 100),
            rounds: 3,
          ),
        ),
      );

      expect(find.text('第 1 / 3 輪'), findsOneWidget);
    });
  });
}
