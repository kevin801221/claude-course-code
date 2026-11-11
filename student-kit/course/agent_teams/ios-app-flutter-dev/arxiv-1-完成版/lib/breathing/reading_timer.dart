import 'dart:async';

import 'package:flutter/foundation.dart';

/// 閱讀計時器(模組 C 的核心邏輯,刻意抽成可單獨測試的 class)。
///
/// 累積「使用者正在閱讀」的時間,達 [threshold] 時呼叫 [onThresholdReached] 一次。
/// 計時與呼吸動畫無關 —— 把純邏輯隔離出來,方便寫 test、也方便 demo override 門檻。
///
/// 設計重點:
/// - [advance] 是真正推進累積時間的入口,內部 periodic timer 與測試都呼叫它,
///   所以 test 不必真的等 10 分鐘,直接 `advance(threshold)` 即可驗證觸發。
/// - 門檻 <= 0 視為「關閉提醒」([start] 不會啟動,永不觸發),呼應「可調 / 可關」。
class ReadingTimer {
  ReadingTimer({
    required this.threshold,
    required this.onThresholdReached,
    this.tick = const Duration(seconds: 1),
  });

  /// 累積多久觸發一次呼吸提醒。<= 0 表示關閉。
  final Duration threshold;

  /// 達門檻時呼叫(每個計時週期只呼叫一次,直到 [reset])。
  final VoidCallback onThresholdReached;

  /// 內部 periodic timer 的取樣間隔(預設 1 秒)。
  final Duration tick;

  Timer? _ticker;
  Duration _accumulated = Duration.zero;
  bool _fired = false;

  /// 是否已關閉(門檻 <= 0)。
  bool get isDisabled => threshold <= Duration.zero;

  /// 目前累積的閱讀時間。
  Duration get accumulated => _accumulated;

  /// periodic timer 是否正在跑。
  bool get isRunning => _ticker != null;

  /// 本週期是否已觸發過提醒(觸發後到 [reset] 前不會重複觸發)。
  bool get hasFired => _fired;

  /// 開始(或繼續)累積閱讀時間。已關閉、已觸發、已在跑則為 no-op。
  void start() {
    if (isDisabled || _fired || _ticker != null) return;
    _ticker = Timer.periodic(tick, (_) => advance(tick));
  }

  /// 暫停累積(例如呼吸 overlay 顯示中、App 進背景),保留已累積時間。
  void pause() {
    _ticker?.cancel();
    _ticker = null;
  }

  /// 推進累積時間 [delta]。達門檻則觸發一次 [onThresholdReached] 並自動暫停。
  ///
  /// 內部 periodic timer 與測試都走這個入口。
  void advance(Duration delta) {
    if (isDisabled || _fired) return;
    _accumulated += delta;
    if (_accumulated >= threshold) {
      _fired = true;
      pause();
      onThresholdReached();
    }
  }

  /// 重置累積與觸發狀態(呼吸做完或略過後回到閱讀時呼叫)。不會自動重新 [start]。
  void reset() {
    pause();
    _accumulated = Duration.zero;
    _fired = false;
  }

  /// 釋放資源(State.dispose 時呼叫)。
  void dispose() {
    pause();
  }
}
