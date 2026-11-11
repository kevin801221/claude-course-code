import 'dart:async';
import 'package:flutter/material.dart';
import '../shared/app_config.dart';
import 'breathing_overlay.dart';

/// 包住整個 App 的閱讀計時 scope。
///
/// App 在前景就累積閱讀時間；達到 [readingThreshold]（預設從
/// [AppConfig.effectiveReadingThreshold] 讀）時，蓋一層
/// [BreathingOverlay]；做完（或使用者略過）後移除 overlay 並重置計時。
///
/// 建構參數 [readingThreshold]、[breathingPhaseDuration]、[breathingRounds]
/// 可由外部注入，方便測試快轉時間，不傳則使用 [AppConfig] 預設值。
///
/// 整合時 team lead 在 [main.dart] 這樣用：
/// ```dart
/// home: BreathingReminderScope(child: ReaderHomePage())
/// ```
class BreathingReminderScope extends StatefulWidget {
  /// [readingThreshold]、[breathingPhaseDuration]、[breathingRounds] 若未傳
  /// 則由 State 在初始化時從 [AppConfig] 讀取，方便測試注入短時間值。
  const BreathingReminderScope({
    super.key,
    required this.child,
    this.readingThreshold,
    this.breathingPhaseDuration,
    this.breathingRounds,
  });

  final Widget child;

  /// 累積閱讀多久後觸發呼吸提醒（null → 用 AppConfig.effectiveReadingThreshold）。
  final Duration? readingThreshold;

  /// Box Breathing 每一相的秒數（null → 用 AppConfig.breathingPhaseDuration）。
  final Duration? breathingPhaseDuration;

  /// 呼吸動畫輪數（null → 用 AppConfig.breathingRounds）。
  final int? breathingRounds;

  @override
  State<BreathingReminderScope> createState() => _BreathingReminderScopeState();
}

class _BreathingReminderScopeState extends State<BreathingReminderScope>
    with WidgetsBindingObserver {
  Timer? _timer;
  Duration _accumulated = Duration.zero;
  bool _overlayVisible = false;

  static const _tickInterval = Duration(seconds: 1);

  // 實際生效值（widget 參數 ?? AppConfig 預設）
  late final Duration _readingThreshold;
  late final Duration _breathingPhaseDuration;
  late final int _breathingRounds;

  @override
  void initState() {
    super.initState();
    _readingThreshold =
        widget.readingThreshold ?? AppConfig.effectiveReadingThreshold;
    _breathingPhaseDuration =
        widget.breathingPhaseDuration ?? AppConfig.breathingPhaseDuration;
    _breathingRounds = widget.breathingRounds ?? AppConfig.breathingRounds;
    WidgetsBinding.instance.addObserver(this);
    _startTicking();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _timer?.cancel();
    super.dispose();
  }

  // ── App 生命週期：進前景繼續計時，進背景暫停 ──────────────────────────────

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      _startTicking();
    } else if (state == AppLifecycleState.paused ||
        state == AppLifecycleState.detached) {
      _stopTicking();
    }
  }

  // ── Timer ────────────────────────────────────────────────────────────────

  void _startTicking() {
    if (_timer?.isActive == true) return;
    _timer = Timer.periodic(_tickInterval, _onTick);
  }

  void _stopTicking() {
    _timer?.cancel();
    _timer = null;
  }

  void _onTick(Timer timer) {
    if (_overlayVisible) return; // overlay 顯示中不累積

    setState(() {
      _accumulated += _tickInterval;
    });

    if (_accumulated >= _readingThreshold) {
      _showOverlay();
    }
  }

  // ── Overlay 控制 ─────────────────────────────────────────────────────────

  void _showOverlay() {
    if (_overlayVisible) return;
    setState(() => _overlayVisible = true);
  }

  void _dismissOverlay() {
    setState(() {
      _overlayVisible = false;
      _accumulated = Duration.zero; // 重置計時
    });
  }

  // ── Build ─────────────────────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    return Stack(
      fit: StackFit.expand,
      children: [
        widget.child,
        if (_overlayVisible)
          Positioned.fill(
            child: BreathingOverlay(
              onDone: _dismissOverlay,
              phaseDuration: _breathingPhaseDuration,
              rounds: _breathingRounds,
            ),
          ),
      ],
    );
  }
}
