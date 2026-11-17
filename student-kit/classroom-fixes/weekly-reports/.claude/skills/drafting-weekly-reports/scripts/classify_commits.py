#!/usr/bin/env python3
"""
分類 commits 成 feat/fix/refactor/docs/other。
讀 stdin 或 --input FILE 的 JSON，輸出分類後的 JSON 到 stdout。

外包確定性操作 — 不要讓 AI 自己用正則分類，這個 script 處理好。
"""
import argparse
import json
import re
import sys
from collections import defaultdict

# 簡單 conventional commit detector
PATTERNS = {
    "feat":     re.compile(r"^(feat|feature|新增|加上|增加)[:(]", re.I),
    "fix":      re.compile(r"^(fix|bug|hotfix|修|解決)", re.I),
    "refactor": re.compile(r"^(refactor|chore|perf|重構|優化|改寫)", re.I),
    "docs":     re.compile(r"^(docs?|test|文件|測試)", re.I),
}

def classify(subject: str) -> str:
    s = subject.strip()
    for cat, pat in PATTERNS.items():
        if pat.search(s):
            return cat
    return "other"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="-", help="JSON file (or - for stdin)")
    args = ap.parse_args()

    src = sys.stdin if args.input == "-" else open(args.input)
    data = json.load(src)

    grouped = defaultdict(list)
    for c in data.get("commits", []):
        cat = classify(c["subject"])
        grouped[cat].append({
            "sha": c["sha"][:7],
            "subject": c["subject"],
            "date": c["date"][:10],
        })

    out = {
        "period": data.get("period"),
        "author": data.get("author"),
        "totals": {k: len(v) for k, v in grouped.items()},
        "by_category": dict(grouped),
    }
    if "prs" in data:
        out["prs"] = data["prs"]
    if "issues" in data:
        out["issues"] = data["issues"]

    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
