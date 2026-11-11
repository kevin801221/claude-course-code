import 'package:flutter_test/flutter_test.dart';

import 'package:arxiv_reader/breathing/reading_timer.dart';

void main() {
  group('ReadingTimer 計時觸發邏輯', () {
    test('累積未達門檻不觸發', () {
      var fired = 0;
      final timer = ReadingTimer(
        threshold: const Duration(minutes: 10),
        onThresholdReached: () => fired++,
      );
      timer.advance(const Duration(minutes: 9));
      expect(fired, 0);
      expect(timer.hasFired, isFalse);
      timer.dispose();
    });

    test('累積達門檻觸發一次,且不重複觸發', () {
      var fired = 0;
      final timer = ReadingTimer(
        threshold: const Duration(minutes: 10),
        onThresholdReached: () => fired++,
      );
      timer.advance(const Duration(minutes: 10));
      expect(fired, 1);
      expect(timer.hasFired, isTrue);
      // 觸發後再推進不應再觸發。
      timer.advance(const Duration(minutes: 5));
      expect(fired, 1);
      timer.dispose();
    });

    test('reset 後可再次計時並再次觸發', () {
      var fired = 0;
      final timer = ReadingTimer(
        threshold: const Duration(seconds: 30),
        onThresholdReached: () => fired++,
      );
      timer.advance(const Duration(seconds: 30));
      expect(fired, 1);

      timer.reset();
      expect(timer.accumulated, Duration.zero);
      expect(timer.hasFired, isFalse);

      timer.advance(const Duration(seconds: 30));
      expect(fired, 2);
      timer.dispose();
    });

    test('門檻 <= 0 視為關閉,start 不啟動且永不觸發', () {
      var fired = 0;
      final timer = ReadingTimer(
        threshold: Duration.zero,
        onThresholdReached: () => fired++,
      );
      expect(timer.isDisabled, isTrue);
      timer.start();
      expect(timer.isRunning, isFalse);
      timer.advance(const Duration(minutes: 10));
      expect(fired, 0);
      timer.dispose();
    });

    test('periodic timer 會累積時間並在門檻觸發', () async {
      var fired = 0;
      final timer = ReadingTimer(
        threshold: const Duration(milliseconds: 30),
        onThresholdReached: () => fired++,
        tick: const Duration(milliseconds: 10),
      );
      timer.start();
      expect(timer.isRunning, isTrue);

      await Future<void>.delayed(const Duration(milliseconds: 80));
      expect(fired, 1);
      // 觸發後自動暫停,不再跑。
      expect(timer.isRunning, isFalse);
      timer.dispose();
    });
  });
}
