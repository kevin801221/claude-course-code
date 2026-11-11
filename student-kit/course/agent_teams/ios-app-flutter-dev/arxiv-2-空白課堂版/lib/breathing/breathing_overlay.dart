import 'package:flutter/material.dart';
import '../shared/app_config.dart';

/// Box Breathing 動畫相位。
enum BreathingPhase { inhale, holdIn, exhale, holdOut }

extension BreathingPhaseLabel on BreathingPhase {
  String get label {
    switch (this) {
      case BreathingPhase.inhale:
        return '吸氣';
      case BreathingPhase.holdIn:
        return '屏息';
      case BreathingPhase.exhale:
        return '吐氣';
      case BreathingPhase.holdOut:
        return '屏息';
    }
  }

  /// 動畫目標縮放比例。
  double get targetScale {
    switch (this) {
      case BreathingPhase.inhale:
        return 1.4;
      case BreathingPhase.holdIn:
        return 1.4;
      case BreathingPhase.exhale:
        return 0.7;
      case BreathingPhase.holdOut:
        return 0.7;
    }
  }
}

/// 60 秒 Box Breathing 動畫 overlay。
///
/// 建構參數可注入 [phaseDuration] 與 [rounds] 以便測試快轉；
/// 不傳則從 [AppConfig] 讀預設值。
///
/// 做完（或使用者點「略過 / 我好了」）呼叫 [onDone]。
class BreathingOverlay extends StatefulWidget {
  const BreathingOverlay({
    super.key,
    required this.onDone,
    Duration? phaseDuration,
    int? rounds,
  })  : phaseDuration = phaseDuration ?? AppConfig.breathingPhaseDuration,
        rounds = rounds ?? AppConfig.breathingRounds;

  final VoidCallback onDone;
  final Duration phaseDuration;
  final int rounds;

  @override
  State<BreathingOverlay> createState() => _BreathingOverlayState();
}

class _BreathingOverlayState extends State<BreathingOverlay>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnim;

  int _currentRound = 0;
  int _phaseIndex = 0;

  static const List<BreathingPhase> _phases = [
    BreathingPhase.inhale,
    BreathingPhase.holdIn,
    BreathingPhase.exhale,
    BreathingPhase.holdOut,
  ];

  bool _finished = false;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: widget.phaseDuration,
    );
    _startPhase();
    _controller.addStatusListener(_onAnimStatus);
  }

  void _startPhase() {
    final begin = _phaseIndex == 0
        ? BreathingPhase.holdOut.targetScale
        : _phases[_phaseIndex - 1].targetScale;
    final end = _phases[_phaseIndex].targetScale;

    _scaleAnim = Tween<double>(begin: begin, end: end).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );

    _controller
      ..reset()
      ..forward();
  }

  BreathingPhase get _currentPhase => _phases[_phaseIndex];

  void _onAnimStatus(AnimationStatus status) {
    if (status != AnimationStatus.completed || _finished) return;

    final nextPhaseIndex = (_phaseIndex + 1) % 4;
    final nextRound = nextPhaseIndex == 0 ? _currentRound + 1 : _currentRound;

    if (nextRound >= widget.rounds) {
      setState(() => _finished = true);
    } else {
      setState(() {
        _phaseIndex = nextPhaseIndex;
        _currentRound = nextRound;
      });
      _startPhase();
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox.expand(
      child: Material(
      color: Colors.black.withValues(alpha: 0.85),
      child: SafeArea(
        child: Column(
          children: [
            // ── 頂部列：標題 + 略過按鈕（永遠在視窗內）──────────────────
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 16, 8, 0),
              child: Row(
                children: [
                  const Expanded(
                    child: Text(
                      '休息一下，跟著呼吸',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  if (!_finished)
                    TextButton(
                      key: const Key('skip_button'),
                      onPressed: widget.onDone,
                      child: const Text(
                        '略過 / 我好了',
                        style: TextStyle(color: Colors.white54, fontSize: 13),
                      ),
                    ),
                ],
              ),
            ),

            // ── 中段：呼吸動畫（可捲動，避免小螢幕截斷）─────────────────
            Expanded(
              child: Center(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 32),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      // 輪次
                      Text(
                        '第 ${_currentRound + 1} / ${widget.rounds} 輪',
                        style: const TextStyle(
                          color: Colors.white70,
                          fontSize: 14,
                        ),
                      ),
                      const SizedBox(height: 32),
                      // 圓圈動畫或完成圖示
                      _finished ? _buildFinished() : _buildCircle(),
                    ],
                  ),
                ),
              ),
            ),

            // ── 底部：免責聲明 ─────────────────────────────────────────
            const Padding(
              padding: EdgeInsets.only(bottom: 16),
              child: Text(
                '僅供休息提醒，非醫療建議',
                style: TextStyle(color: Colors.white38, fontSize: 11),
                textAlign: TextAlign.center,
              ),
            ),
          ],
        ),
      ),
    ), // Material
    ); // SizedBox.expand
  }

  Widget _buildCircle() {
    return AnimatedBuilder(
      animation: _scaleAnim,
      builder: (context, _) => Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Transform.scale(
            scale: _scaleAnim.value,
            child: Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.teal.withValues(alpha: 0.3),
                border: Border.all(color: Colors.tealAccent, width: 3),
              ),
            ),
          ),
          const SizedBox(height: 20),
          Text(
            _currentPhase.label,
            style: const TextStyle(
              color: Colors.tealAccent,
              fontSize: 26,
              fontWeight: FontWeight.w700,
              letterSpacing: 2,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFinished() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 100,
          height: 100,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: Colors.teal.withValues(alpha: 0.4),
            border: Border.all(color: Colors.tealAccent, width: 3),
          ),
          child: const Icon(Icons.check, color: Colors.tealAccent, size: 50),
        ),
        const SizedBox(height: 20),
        const Text(
          '很好！繼續閱讀吧',
          style: TextStyle(
            color: Colors.tealAccent,
            fontSize: 20,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 24),
        ElevatedButton(
          key: const Key('continue_button'),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.tealAccent,
            foregroundColor: Colors.black,
            minimumSize: const Size(180, 46),
          ),
          onPressed: widget.onDone,
          child: const Text('繼續閱讀', style: TextStyle(fontSize: 15)),
        ),
      ],
    );
  }
}
