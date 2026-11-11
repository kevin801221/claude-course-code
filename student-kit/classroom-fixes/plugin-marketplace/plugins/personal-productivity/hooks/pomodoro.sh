#!/bin/bash
# 番茄鐘 hook — 每 50 個 tool call 提醒喝水
STATE_DIR="${CLAUDE_PROJECT_DIR:-$PWD}/.outputs/plugin-demo"
mkdir -p "$STATE_DIR"
COUNTER_FILE="$STATE_DIR/pomodoro-count"
N=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
case "$N" in ""|*[!0-9]*) echo "pomodoro: invalid counter; inspect the project-local state" >&2; exit 1 ;; esac
N=$((N + 1))
echo "$N" > "$COUNTER_FILE"

if [ $((N % 50)) -eq 0 ]; then
  osascript -e 'display notification "該休息囉～去喝水 🫗" \
    with title "Claude 番茄鐘" sound name "Glass"' 2>/dev/null
  command -v notify-send >/dev/null && \
    notify-send "Claude 番茄鐘" "該休息囉～去喝水 🫗"
fi
exit 0
