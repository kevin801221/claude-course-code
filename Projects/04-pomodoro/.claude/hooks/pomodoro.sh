#!/bin/bash
# 番茄鐘 hook — Claude 用了 50 個 tool call 後彈通知喝水

COUNTER_FILE="$HOME/.claude/.pomodoro-count"
N=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
N=$((N + 1))
echo "$N" > "$COUNTER_FILE"

# 每 50 個 tool call 提醒一次
if [ $((N % 50)) -eq 0 ]; then
  # macOS
  osascript -e 'display notification "該休息囉～去喝水 🫗" \
    with title "Claude 番茄鐘" sound name "Glass"' 2>/dev/null

  # Linux 替代（如果上面 osascript 失敗）
  command -v notify-send >/dev/null && \
    notify-send "Claude 番茄鐘" "該休息囉～去喝水 🫗"
fi

exit 0
