#!/usr/bin/env python3
"""與原 fetch_commits.sh 相同的參數；可靠地輸出 UTF-8 JSON。"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", default="7 days ago")
    parser.add_argument("--author", default="")
    parser.add_argument("--include-prs", action="store_true")
    parser.add_argument("--include-issues", action="store_true")
    parser.add_argument("--output", default="-", help="JSON 檔案；- 或 /dev/stdout 輸出到 stdout")
    args = parser.parse_args()

    author = args.author
    if not author:
        configured = subprocess.run(
            ["git", "config", "user.email"], capture_output=True, text=True, encoding="utf-8",
        )
        author = configured.stdout.strip()
        if not author:
            parser.error("請提供 --author，或在目標 Git repo 設定 user.email。")

    # Git commit message 不能含 NUL。-z 加上欄位間的 NUL 可保留引號、反斜線與 body 換行。
    result = subprocess.run(
        ["git", "-c", "i18n.logOutputEncoding=UTF-8", "log", "-z",
         "--since=" + args.since, "--author=" + author,
         "--pretty=format:%H%x00%aI%x00%s%x00%b"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    fields = result.stdout.split("\0") if result.stdout else []
    if len(fields) % 4:
        raise ValueError("Git log 欄位數異常，未產生或覆寫輸出檔。")
    commits = [dict(zip(("sha", "date", "subject", "body"), fields[i:i + 4]))
               for i in range(0, len(fields), 4)]
    payload = {"period": args.since, "author": author, "commits": commits}

    for enabled, field, command in [
        (args.include_prs, "prs", ["gh", "pr", "list", "--author", "@me", "--state", "all",
                                  "--json", "number,title,state,mergedAt", "--limit", "20"]),
        (args.include_issues, "issues", ["gh", "issue", "list", "--author", "@me", "--state", "all",
                                        "--json", "number,title,state", "--limit", "20"]),
    ]:
        if not enabled:
            continue
        if not shutil.which("gh"):
            print("未找到 gh，略過 " + field + "；commits 仍正常輸出。", file=sys.stderr)
            continue
        response = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=True)
        payload[field] = json.loads(response.stdout)

    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output in {"-", "/dev/stdout"}:
        sys.stdout.write(rendered)
    else:
        # 先收齊並成功解析全部資料，才寫入檔案；上游命令失敗不覆寫既有輸出。
        Path(args.output).write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print((error.stderr or str(error)).strip(), file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
