#!/usr/bin/env bash
# Install (or remove) the launchd jobs that run the reports on a schedule (Mac).
#
# Usage:
#   scripts/mac/install-schedule.sh            # personal: daily, weekly, monthly
#   scripts/mac/install-schedule.sh --team     # also manager: team-daily, team-weekly
#   scripts/mac/install-schedule.sh --uninstall
#
# Times (local time, change below if needed):
#   daily        Mon-Fri 19:00
#   weekly       Fri     19:30
#   monthly      every day 20:00, but the script only acts on the last day of the month
#   team-daily   Mon-Fri 20:00
#   team-weekly  Fri     21:00
#
# The Mac must be awake at those times; launchd runs a missed job when it wakes.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="$SCRIPT_DIR/run-report.sh"
AGENTS_DIR="$HOME/Library/LaunchAgents"
PREFIX="com.claude-mem-daily-report"
UID_NUM="$(id -u)"

ALL_JOBS=(daily weekly monthly team-daily team-weekly)

unload_job() {
  local label="$PREFIX.$1" plist="$AGENTS_DIR/$PREFIX.$1.plist"
  launchctl bootout "gui/$UID_NUM/$label" 2>/dev/null || true
  rm -f "$plist"
}

# $1 = job name, $2 = hour, $3 = minute, $4 = space-separated weekdays (1=Mon ... 5=Fri), empty = every day
write_job() {
  local name="$1" hour="$2" minute="$3" days="$4"
  local label="$PREFIX.$name" plist="$AGENTS_DIR/$PREFIX.$name.plist"
  local intervals=""
  if [[ -z "$days" ]]; then
    intervals="<dict><key>Hour</key><integer>$hour</integer><key>Minute</key><integer>$minute</integer></dict>"
  else
    for d in $days; do
      intervals+="<dict><key>Weekday</key><integer>$d</integer><key>Hour</key><integer>$hour</integer><key>Minute</key><integer>$minute</integer></dict>"
    done
  fi

  cat >"$plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$label</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$RUNNER</string>
    <string>$name</string>
  </array>
  <key>StartCalendarInterval</key>
  <array>$intervals</array>
  <key>RunAtLoad</key><false/>
</dict>
</plist>
EOF
  launchctl bootout "gui/$UID_NUM/$label" 2>/dev/null || true
  launchctl bootstrap "gui/$UID_NUM" "$plist"
  echo "installed $label"
}

mkdir -p "$AGENTS_DIR"
chmod +x "$RUNNER"

case "${1:-}" in
  --uninstall)
    for job in "${ALL_JOBS[@]}"; do unload_job "$job"; done
    echo "removed all report jobs"
    ;;
  ""|--team)
    write_job daily   19 0  "1 2 3 4 5"
    write_job weekly  19 30 "5"
    write_job monthly 20 0  ""
    if [[ "${1:-}" == "--team" ]]; then
      write_job team-daily  20 0 "1 2 3 4 5"
      write_job team-weekly 21 0 "5"
    fi
    echo "check with: launchctl list | grep $PREFIX"
    echo "test now:   bash $RUNNER daily && tail -n 30 \"$(cd "$SCRIPT_DIR/../.." && pwd)/logs/\$(date +%Y-%m-%d)-daily.log\""
    ;;
  *)
    echo "Usage: $0 [--team | --uninstall]"
    exit 2
    ;;
esac
