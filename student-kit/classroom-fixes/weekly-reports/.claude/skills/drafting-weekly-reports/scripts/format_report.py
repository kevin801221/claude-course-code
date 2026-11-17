#!/usr/bin/env python3
"""
把分類後的 JSON 套成 markdown 週報。

⚠️ 注意：這個 script 只負責「機械式套版」。
   真正「翻譯成使用者語言」的工作要交給 AI（看 SKILL.md workflow）。
"""
import json
import sys
from datetime import datetime

EMOJI = {
    "feat":     "✨",
    "fix":      "🐛",
    "refactor": "♻️",
    "docs":     "📚",
    "other":    "🔧",
}

LABELS = {
    "feat":     "新功能",
    "fix":      "Bug 修復",
    "refactor": "內部優化",
    "docs":     "文件 / 測試",
    "other":    "其他",
}

def main():
    data = json.load(sys.stdin)
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"# 📅 週報 — {today}")
    print(f"> 期間：{data['period']} · 作者：{data['author']}")
    print()

    for cat in ["feat", "fix", "refactor", "docs", "other"]:
        items = data["by_category"].get(cat, [])
        if not items:
            continue
        print(f"## {EMOJI[cat]} {LABELS[cat]}")
        for c in items[:5]:  # 每類最多 5 條
            print(f"- `{c['sha']}` {c['subject']} _(({c['date']}))_")
        if len(items) > 5:
            print(f"- ... 另 {len(items) - 5} 個")
        print()

    print("---")
    print("> 💡 上面是機械分類，請接著翻譯成「業務語言」並加上影響說明。")

if __name__ == "__main__":
    main()
