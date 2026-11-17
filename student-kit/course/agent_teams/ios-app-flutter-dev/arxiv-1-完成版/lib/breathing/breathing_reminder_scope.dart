import 'package:flutter/material.dart';

import '../shared/app_config.dart';
import 'breathing_overlay.dart';
import 'reading_timer.dart';

/// 呼吸提醒範圍(模組 C,breathing-owner 擁有)。
///
/// 包住 [child](閱讀內容),內部用 [ReadingTimer] 累積閱讀時間;
/// 達門檻時疊一層 60 秒 [BreathingOverlay](Box Breathing 4-4-4-4),
/// 做完或使用者略過後移除 overlay、重置計時、繼續閱讀。
///
/// public 入口簽章維持 `required Widget child`(main.dart 用
/// `BreathingReminderScope(child: ReaderHomePage())`);
/// [threshold] 是**向後相容的可選參數**,給 demo / 測試 override 門檻,
/// 不傳時用 `AppConfig.readingReminderThreshold`(預設 10 分鐘)。
/// 門檻 <= 0 視為關閉提醒(尊重使用者,可調 / 可關)。
///
/// 提示溫和、可略過,不強迫、不宣稱療效。
class BreathingReminderScope extends StatefulWidget {
  final Widget child;

  /// override 觸發門檻;null → 用 [AppConfig.readingReminderThreshold]。
  final Duration? threshold;

  const BreathingReminderScope({
    super.key,
    required this.child,
    this.threshold,
  });

  @override
  State<BreathingReminderScope> createState() => _BreathingReminderScopeState();
}

class _BreathingReminderScopeState extends State<BreathingReminderScope> {
  late final ReadingTimer _timer;
  bool _showBreathing = false;

  Duration get _threshold =>
      widget.threshold ?? AppConfig.readingReminderThreshold;

  @override
  void initState() {
    super.initState();
    _timer = ReadingTimer(
      threshold: _threshold,
      onThresholdReached: _onThresholdReached,
    );
    _timer.start();
  }

  void _onThresholdReached() {
    if (!mounted) return;
    setState(() => _showBreathing = true);
  }

  /// 呼吸做完或使用者略過 → 移除 overlay、重置並重新計時。
  void _onBreathingDone() {
    if (!mounted) return;
    setState(() => _showBreathing = false);
    _timer.reset();
    _timer.start();
  }

  @override
  void dispose() {
    _timer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        widget.child,
        if (_showBreathing)
          Positioned.fill(
            child: BreathingOverlay(
              totalDuration: AppConfig.breathingDuration,
              onDone: _onBreathingDone,
            ),
          ),
      ],
    );
  }
}
