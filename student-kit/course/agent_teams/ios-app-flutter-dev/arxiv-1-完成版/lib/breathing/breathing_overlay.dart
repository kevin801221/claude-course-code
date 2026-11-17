import 'package:flutter/material.dart';

/// Box Breathing 的四個階段。
enum BreathPhase {
  inhale, // 吸氣:圓圈放大
  holdFull, // 停(滿):維持放大
  exhale, // 吐氣:圓圈縮小
  holdEmpty; // 停(空):維持縮小

  /// 階段顯示文案(中性、不宣稱療效)。
  String get label {
    switch (this) {
      case BreathPhase.inhale:
        return '吸氣';
      case BreathPhase.holdFull:
        return '停';
      case BreathPhase.exhale:
        return '吐氣';
      case BreathPhase.holdEmpty:
        return '停';
    }
  }
}

/// 60 秒 Box Breathing(4-4-4-4)呼吸動畫 overlay。
///
/// 圓圈:放大=吸氣、維持=停、縮小=吐氣(用 [AnimationController] 驅動)。
/// 一輪 16 秒(吸4→停4→吐4→停4),依 [totalDuration] 換算輪數
/// (60 秒 → 約 4 輪 ≈ 64 秒,對齊 app-spec)。
///
/// 提示溫和、可略過,不強迫、不宣稱療效。做完或使用者略過都會呼叫 [onDone]。
class BreathingOverlay extends StatefulWidget {
  const BreathingOverlay({
    super.key,
    required this.onDone,
    this.totalDuration = const Duration(seconds: 60),
    this.phaseDuration = const Duration(seconds: 4),
  });

  /// 呼吸結束或使用者略過時呼叫(回到閱讀並重置計時)。
  final VoidCallback onDone;

  /// 動畫總時長(會換算成最接近的整數輪)。
  final Duration totalDuration;

  /// 單一階段時長(Box Breathing 四階段等長,預設 4 秒)。
  final Duration phaseDuration;

  @override
  State<BreathingOverlay> createState() => _BreathingOverlayState();
}

class _BreathingOverlayState extends State<BreathingOverlay>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _scale;
  late final int _rounds;
  late final int _phaseSeconds;
  late final int _totalSeconds;

  // 圓圈縮放範圍:吐到底 0.5、吸到滿 1.0。
  static const double _minScale = 0.5;
  static const double _maxScale = 1.0;

  @override
  void initState() {
    super.initState();
    _phaseSeconds = widget.phaseDuration.inSeconds.clamp(1, 60);
    final roundSeconds = _phaseSeconds * 4;
    // 由總時長換算輪數,至少 1 輪。60s / 16s ≈ 3.75 → 4 輪 ≈ 64s。
    _rounds = (widget.totalDuration.inSeconds / roundSeconds).round().clamp(
      1,
      99,
    );
    _totalSeconds = _rounds * roundSeconds;

    _controller = AnimationController(
      vsync: this,
      duration: Duration(seconds: _totalSeconds),
    );

    _scale = _buildScaleSequence().animate(_controller);

    _controller.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        widget.onDone();
      }
    });

    _controller.forward();
  }

  /// 把「吸→停→吐→停」重複 [_rounds] 輪,串成一條 scale 動畫。
  TweenSequence<double> _buildScaleSequence() {
    final items = <TweenSequenceItem<double>>[];
    for (var i = 0; i < _rounds; i++) {
      items.addAll([
        // 吸:放大
        TweenSequenceItem(
          tween: Tween(
            begin: _minScale,
            end: _maxScale,
          ).chain(CurveTween(curve: Curves.easeInOut)),
          weight: 1,
        ),
        // 停(滿):維持
        TweenSequenceItem(tween: ConstantTween(_maxScale), weight: 1),
        // 吐:縮小
        TweenSequenceItem(
          tween: Tween(
            begin: _maxScale,
            end: _minScale,
          ).chain(CurveTween(curve: Curves.easeInOut)),
          weight: 1,
        ),
        // 停(空):維持
        TweenSequenceItem(tween: ConstantTween(_minScale), weight: 1),
      ]);
    }
    return TweenSequence(items);
  }

  /// 依目前進度算出 (第幾輪, 當前階段)。
  ({int round, BreathPhase phase}) _progress() {
    final elapsed = _controller.value * _totalSeconds;
    var phaseIndex = (elapsed / _phaseSeconds).floor();
    final maxPhase = _rounds * 4 - 1;
    if (phaseIndex > maxPhase) phaseIndex = maxPhase;
    final round = (phaseIndex ~/ 4) + 1;
    final phase = BreathPhase.values[phaseIndex % 4];
    return (round: round, phase: phase);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      // 半透明深色底,蓋住閱讀內容、聚焦呼吸。
      color: const Color(0xF21E2761),
      child: Stack(
        children: [
          // 全螢幕 modal barrier:呼吸進行中吃掉所有背景觸控,
          // 不讓長按 / 點擊穿透到背景 reader 的 SelectableText(避免誤觸跳選單)。
          // 只有上層的「略過」按鈕可互動。
          const ModalBarrier(dismissible: false, color: Colors.transparent),
          SafeArea(
            child: AnimatedBuilder(
              animation: _controller,
              builder: (context, _) {
                final p = _progress();
                return Column(
                  children: [
                    const Spacer(),
                    Text(
                      '休息一下,跟著呼吸',
                      style: TextStyle(
                        color: Colors.white.withValues(alpha: 0.92),
                        fontSize: 20,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '第 ${p.round} / $_rounds 輪',
                      style: TextStyle(
                        color: Colors.white.withValues(alpha: 0.6),
                        fontSize: 14,
                      ),
                    ),
                    const Spacer(),
                    // 呼吸圓圈:放大=吸、維持=停、縮小=吐。
                    SizedBox(
                      width: 240,
                      height: 240,
                      child: Center(
                        child: Transform.scale(
                          scale: _scale.value,
                          child: Container(
                            width: 200,
                            height: 200,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              gradient: RadialGradient(
                                colors: [
                                  const Color(
                                    0xFFD97757,
                                  ).withValues(alpha: 0.95),
                                  const Color(
                                    0xFFD97757,
                                  ).withValues(alpha: 0.45),
                                ],
                              ),
                            ),
                            alignment: Alignment.center,
                            child: Text(
                              p.phase.label,
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 28,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                    const Spacer(),
                    Text(
                      '溫和提醒你抬頭休息一下',
                      style: TextStyle(
                        color: Colors.white.withValues(alpha: 0.55),
                        fontSize: 13,
                      ),
                    ),
                    const SizedBox(height: 16),
                    // 可略過,不強迫。
                    TextButton(
                      onPressed: widget.onDone,
                      style: TextButton.styleFrom(
                        foregroundColor: Colors.white,
                        backgroundColor: Colors.white.withValues(alpha: 0.14),
                        padding: const EdgeInsets.symmetric(
                          horizontal: 28,
                          vertical: 12,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(24),
                        ),
                      ),
                      child: const Text('略過,繼續閱讀'),
                    ),
                    const SizedBox(height: 32),
                  ],
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
