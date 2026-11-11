#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")/.."
command -v claude >/dev/null || { echo '請先安裝並登入 Claude Code。' >&2; exit 1; }
mkdir -p .outputs
temporary=$(mktemp .outputs/summary.XXXXXX)
trap 'rm -f -- "$temporary"' EXIT
claude -p '閱讀 CLAUDE.md、src/ 與 bin/，用繁體中文列出目前支援的 CLI 行為與兩個已知限制。不執行 shell、不修改檔案，沒測試就寫未測試。' \
  --output-format json \
  --tools 'Read,Glob,Grep' \
  --allowedTools 'Read,Glob,Grep' \
  --setting-sources project \
  --mcp-config labs/09-automation/no-mcp.json \
  --strict-mcp-config \
  --max-budget-usd 0.25 \
  --no-session-persistence > "$temporary"
mv -- "$temporary" .outputs/summary.json
echo '模型回應已儲存於 .outputs/summary.json；請檢查 result、is_error 與成本欄位。'
