"""離線報表與記憶檢索教學。從合成 observation 建立獨立的 SQLite 檔。"""
import argparse
import datetime as dt
import json
import sqlite3
from collections import defaultdict
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COLUMNS = ("id", "date", "author", "kind", "subject", "detail", "evidence")
PRIORITIES = {"eng": ("完成", "待查", "決議", "初報"), "pm": ("待查", "決議", "完成", "初報")}


def load(database):
    database.parent.mkdir(parents=True, exist_ok=True)
    records = json.loads((ROOT / "fixtures/observations.json").read_text(encoding="utf-8"))
    with closing(sqlite3.connect(database)) as connection, connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS observations "
            "(id INTEGER PRIMARY KEY, date TEXT, author TEXT, kind TEXT, "
            "subject TEXT, detail TEXT, evidence TEXT)"
        )
        connection.executemany(
            "INSERT OR REPLACE INTO observations VALUES (?, ?, ?, ?, ?, ?, ?)",
            [tuple(record[key] for key in COLUMNS) for record in records],
        )
        count = connection.execute("SELECT count(*) FROM observations").fetchone()[0]
    print(f"資料庫有 {count} 筆 observation。")


def week(day):
    year, number, _ = dt.date.fromisoformat(day).isocalendar()
    return f"{year}-W{number:02d}"


def make_report(folder, title, period, records, priorities):
    folder.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}｜{period}", ""]
    for kind in priorities:
        entries = [r for r in records if r["kind"] == kind]
        if entries:
            lines.extend([f"## {kind}", ""])
            for r in entries:
                lines.append(f"- {r['author']} · {r['subject']}：{r['detail']} "
                             f"〔#{r['id']} · {r['evidence']}〕")
            lines.append("")
    path = folder / f"{period}.md"
    path.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")
    print(path)


def reports(rows, output):
    by_period = defaultdict(list)
    for r in rows:
        for period in [r["date"], week(r["date"])]:
            by_period[(r["author"], period)].append(r)
            by_period[("team", period)].append(r)
    for (who, period), records in sorted(by_period.items()):
        cadence = "weekly" if "-W" in period else "daily"
        folder = output / "team" if who == "team" else output / "members" / who
        priorities = PRIORITIES.get(who, ("待查", "決議", "完成", "初報"))
        title = "團隊" if who == "team" else who
        make_report(folder / cadence, title, period, records, priorities)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("practice/memory.sqlite3"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("save")
    search = commands.add_parser("search")
    search.add_argument("term")
    for name in ["timeline", "get"]:
        commands.add_parser(name).add_argument("id", type=int)
    commands.add_parser("reports").add_argument("--out", type=Path, default=Path("practice/reports"))
    args = parser.parse_args()
    if args.command == "save":
        load(args.db)
        return
    if not args.db.is_file():
        parser.error("請先執行 save 建立練習資料庫。")
    with closing(sqlite3.connect(args.db.resolve().as_uri() + "?mode=ro", uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        rows = list(connection.execute("SELECT * FROM observations ORDER BY date, id"))
    if args.command == "reports":
        reports(rows, args.out)
    elif args.command == "search":
        matches = [r for r in rows if any(args.term.casefold() in r[key].casefold()
                                         for key in ("subject", "detail", "evidence"))]
        for r in matches:
            print(f"#{r['id']} | {r['date']} | {r['subject']} | {r['kind']}")
        if not matches:
            print("查無這個詞的記憶。")
    else:
        row = next((r for r in rows if r["id"] == args.id), None)
        if row is None:
            parser.error(f"沒有 observation #{args.id}")
        if args.command == "get":
            print(json.dumps(dict(row), ensure_ascii=False, indent=2))
        else:
            for r in rows:
                if r["subject"] == row["subject"]:
                    print(f"{r['date']} | #{r['id']} | {r['kind']} | {r['detail']}")


if __name__ == "__main__":
    main()
