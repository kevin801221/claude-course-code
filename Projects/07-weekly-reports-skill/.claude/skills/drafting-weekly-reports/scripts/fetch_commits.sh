#!/bin/bash
# 撈 GitHub commits（外包確定性操作 — 不要讓 AI 自己 git log）
#
# Usage:
#   fetch_commits.sh --since "7 days ago" --author "kevin@example.com"
#   fetch_commits.sh --include-prs --include-issues
#
# Output: JSON 到 stdout（或 --output FILE）

set -euo pipefail

SINCE="7 days ago"
AUTHOR=""
INCLUDE_PRS=false
INCLUDE_ISSUES=false
OUTPUT="/dev/stdout"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --since) SINCE="$2"; shift 2 ;;
    --author) AUTHOR="$2"; shift 2 ;;
    --include-prs) INCLUDE_PRS=true; shift ;;
    --include-issues) INCLUDE_ISSUES=true; shift ;;
    --output) OUTPUT="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

[[ -z "$AUTHOR" ]] && AUTHOR=$(git config user.email)

# 撈 commits（用 JSON 友善的 separator）
COMMITS=$(git log --since="$SINCE" --author="$AUTHOR" \
  --pretty=format:'{"sha":"%H","date":"%aI","subject":"%s","body":"%b"}' \
  | sed 's/}$/},/' | sed '$ s/,$//')

# 產 JSON array
echo "{" > "$OUTPUT"
echo "  \"period\": \"$SINCE\"," >> "$OUTPUT"
echo "  \"author\": \"$AUTHOR\"," >> "$OUTPUT"
echo "  \"commits\": [" >> "$OUTPUT"
echo "$COMMITS" >> "$OUTPUT"
echo "  ]" >> "$OUTPUT"

# 撈 PRs (gh CLI)
if [[ "$INCLUDE_PRS" == true ]] && command -v gh >/dev/null; then
  echo "  ,\"prs\": $(gh pr list --author @me --state all \
    --json number,title,state,mergedAt --limit 20)" >> "$OUTPUT"
fi

# 撈 issues
if [[ "$INCLUDE_ISSUES" == true ]] && command -v gh >/dev/null; then
  echo "  ,\"issues\": $(gh issue list --author @me --state all \
    --json number,title,state --limit 20)" >> "$OUTPUT"
fi

echo "}" >> "$OUTPUT"
