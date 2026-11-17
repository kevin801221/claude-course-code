#!/bin/bash
# PreToolUse: production 寫入保護 + secrets 讀取保護
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# 場景 1：擋 production DB 寫入
if echo "$CMD" | grep -qE 'DATABASE_URL=.*prod|psql.*prod|UPDATE.*production'; then
  echo "BLOCKED: 偵測到 production DB 操作 — 改去 staging 試" >&2
  exit 2
fi

# 場景 2：擋 .env / secrets 讀取
if [ "$TOOL" = "Read" ]; then
  P=$(echo "$INPUT" | jq -r '.tool_input.file_path')
  if echo "$P" | grep -qE '\.env$|secrets/|credentials/'; then
    echo "BLOCKED: 不准讀 secrets 檔" >&2
    exit 2
  fi
fi

exit 0
