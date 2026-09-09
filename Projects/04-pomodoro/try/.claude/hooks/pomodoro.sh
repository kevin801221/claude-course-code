#!/bin/bash
# 番茄鐘 hook — Claude 用了 50 個 tool call 後彈通知喝水

COUNTER_FILE="$HOME/.claude/.pomodoro-count"
N=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
N=$((N + 1))
echo "$N" > "$COUNTER_FILE"

# 每 50 個 tool call 提醒一次
if [ $((N % 50)) -eq 0 ]; then
  TITLE="Claude 番茄鐘"
  MSG="該休息囉～去喝水 🫗"

  if command -v terminal-notifier >/dev/null; then
    # macOS 首選：terminal-notifier（權限好設、必跳）
    terminal-notifier -title "$TITLE" -message "$MSG" -sound Glass
  elif command -v osascript >/dev/null; then
    # macOS fallback：osascript（部分機器通知權限會被擋）
    osascript -e "display notification \"$MSG\" with title \"$TITLE\" sound name \"Glass\"" 2>/dev/null
  elif command -v notify-send >/dev/null; then
    # Linux
    notify-send "$TITLE" "$MSG"
  fi
fi

exit 0
