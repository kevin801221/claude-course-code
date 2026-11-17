#!/usr/bin/env bash
# Run one report with Claude Code in headless mode (Mac).
#
# Usage:
#   scripts/mac/run-report.sh daily          # meetings + personal daily report
#   scripts/mac/run-report.sh weekly
#   scripts/mac/run-report.sh monthly        # only runs on the last day of the month
#   scripts/mac/run-report.sh monthly --force
#   scripts/mac/run-report.sh team-daily     # manager side
#   scripts/mac/run-report.sh team-weekly    # manager side
#
# launchd starts jobs with a minimal environment, so PATH is set here.

set -euo pipefail

TYPE="${1:-}"
FORCE="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

# Settings (AUTHOR, ALLOWED_TOOLS, ...). Missing file is fine: defaults below.
if [[ -f "$REPO_DIR/config/report.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$REPO_DIR/config/report.env"
  set +a
fi
AUTHOR="${AUTHOR:-$(id -un)}"
ALLOWED_TOOLS="${ALLOWED_TOOLS:-Read,Write,Edit,Glob,Grep}"
TEAM_REPORTS_DIR="${TEAM_REPORTS_DIR:-$REPO_DIR/team-reports}"
REPORT_DESTINATION="${REPORT_DESTINATION:-}"
NOTION_REPORT_DB="${NOTION_REPORT_DB:-}"
JIRA_ISSUE="${JIRA_ISSUE:-}"

LOG_DIR="$REPO_DIR/logs"
mkdir -p "$LOG_DIR" "$REPO_DIR"/reports/{daily,weekly,monthly,team} "$REPO_DIR/meetings"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d)-${TYPE:-none}.log"
exec >>"$LOG_FILE" 2>&1
echo "=== $(date '+%Y-%m-%d %H:%M:%S') start $TYPE ==="

if ! command -v claude >/dev/null 2>&1; then
  echo "[error] claude command not found on PATH: $PATH"
  exit 1
fi

render() {
  python3 "$SCRIPT_DIR/render_prompt.py" "$REPO_DIR/prompts/$1" \
    "REPO_DIR=$REPO_DIR" "AUTHOR=$AUTHOR" "TEAM_REPORTS_DIR=$TEAM_REPORTS_DIR" \
    "REPORT_DESTINATION=$REPORT_DESTINATION" "NOTION_REPORT_DB=$NOTION_REPORT_DB" \
    "JIRA_ISSUE=$JIRA_ISSUE" "${@:2}"
}

run_claude() {
  # Run from the repo so Write stays inside it under acceptEdits.
  (cd "$REPO_DIR" && claude -p "$1" \
    --allowedTools "$ALLOWED_TOOLS" \
    --permission-mode acceptEdits)
}

transcribe_and_minutes() {
  local py="python3"
  # Prefer a dedicated virtualenv if the user created one for WhisperX.
  [[ -x "$REPO_DIR/.venv-whisper/bin/python" ]] && py="$REPO_DIR/.venv-whisper/bin/python"
  if ! "$py" -c "import whisperx" >/dev/null 2>&1; then
    echo "[info] whisperx not installed; skipping meeting transcription"
    return 0
  fi
  local transcripts
  transcripts="$("$py" "$REPO_DIR/scripts/transcribe/transcribe.py" \
    --recordings "$REPO_DIR/recordings" --out "$REPO_DIR/meetings")" || {
    echo "[warn] transcription reported errors; continuing with what succeeded"
  }
  local t out
  while IFS= read -r t; do
    [[ -z "$t" ]] && continue
    out="${t%.transcript.md}.md"
    echo "[info] writing minutes for $(basename "$t")"
    run_claude "$(render meeting-minutes.md "TRANSCRIPT=$t" "OUTPUT=$out")"
  done <<<"$transcripts"
}

case "$TYPE" in
  daily)
    transcribe_and_minutes
    run_claude "$(render daily-report.md)"
    ;;
  weekly)
    run_claude "$(render weekly-report.md)"
    ;;
  monthly)
    if [[ "$FORCE" != "--force" ]] && ! python3 "$SCRIPT_DIR/render_prompt.py" --is-month-end; then
      echo "[info] not the last day of the month; skipping"
      exit 0
    fi
    run_claude "$(render monthly-report.md)"
    ;;
  team-daily)
    run_claude "$(render team-daily.md)"
    ;;
  team-weekly)
    run_claude "$(render team-weekly.md)"
    ;;
  *)
    echo "Usage: $0 {daily|weekly|monthly [--force]|team-daily|team-weekly}"
    exit 2
    ;;
esac

echo "=== $(date '+%Y-%m-%d %H:%M:%S') done $TYPE ==="
