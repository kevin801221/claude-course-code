"""Fill a prompt template's {{PLACEHOLDERS}} for the Mac scripts.

Usage:
    python3 render_prompt.py <template.md> [KEY=VALUE ...]

Date placeholders are computed here so the shell script stays simple:
    {{DATE}}        today, YYYY-MM-DD
    {{WEEK_START}}  Monday of this week
    {{WEEK_END}}    Sunday of this week
    {{WEEK_LABEL}}  ISO week, e.g. 2026-W47
    {{MONTH}}       YYYY-MM
Extra KEY=VALUE pairs (REPO_DIR, AUTHOR, TRANSCRIPT, ...) override or add.

Also:
    python3 render_prompt.py --is-month-end   exits 0 on the last day of the month
"""

import datetime as dt
import sys
from pathlib import Path


def date_vars(today: dt.date) -> dict:
    monday = today - dt.timedelta(days=today.weekday())
    iso_year, iso_week, _ = today.isocalendar()
    return {
        "DATE": today.isoformat(),
        "WEEK_START": monday.isoformat(),
        "WEEK_END": (monday + dt.timedelta(days=6)).isoformat(),
        "WEEK_LABEL": f"{iso_year}-W{iso_week:02d}",
        "MONTH": today.strftime("%Y-%m"),
    }


def main(argv: list[str]) -> int:
    today = dt.date.today()
    if argv and argv[0] == "--is-month-end":
        return 0 if (today + dt.timedelta(days=1)).month != today.month else 1
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2

    values = date_vars(today)
    for pair in argv[1:]:
        key, _, value = pair.partition("=")
        values[key] = value

    text = Path(argv[0]).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
