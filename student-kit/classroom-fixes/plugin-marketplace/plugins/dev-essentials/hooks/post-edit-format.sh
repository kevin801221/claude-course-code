#!/bin/bash
# PostToolUse: 自動格式化編輯過的檔案
command -v jq >/dev/null 2>&1 || { echo "post-edit-format: skipped (jq is required)" >&2; exit 0; }
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

case "$FILE" in
  *.py)              command -v black >/dev/null && black "$FILE" 2>/dev/null ;;
  *.js|*.ts|*.tsx)   command -v prettier >/dev/null && prettier --write "$FILE" 2>/dev/null ;;
  *.go)              command -v gofmt >/dev/null && gofmt -w "$FILE" 2>/dev/null ;;
  *.rs)              command -v rustfmt >/dev/null && rustfmt "$FILE" 2>/dev/null ;;
esac

# log 編輯紀錄
LOG_DIR="${CLAUDE_PROJECT_DIR:-$PWD}/.outputs/plugin-demo"
mkdir -p "$LOG_DIR"
printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$FILE" >> "$LOG_DIR/edits.log"

exit 0
