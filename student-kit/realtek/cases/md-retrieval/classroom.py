"""用公開實驗的版面配置與索引函式，產生四組同題、同文本的檔案。"""
import argparse
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "upstream/src"))
from lab.build import GUIDES, SETTINGS, layout, render_index


def material():
    data = json.loads((ROOT / "fixtures/documents.json").read_text(encoding="utf-8"))
    question = json.loads((ROOT / "fixtures/question.json").read_text(encoding="utf-8"))
    return data, question


def write(target, text):
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def prepare(dest, world, question):
    if dest.exists() or dest.is_symlink():
        raise SystemExit(f"目的目錄已存在。請指定另一個練習目錄：{dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=dest.parent) as tmp:
        stage = Path(tmp) / "groups"
        for name, paths in layout(world).items():
            group = stage / name
            for doc in world["docs"]:
                write(group / paths[doc["id"]], doc["body"])
            write(group / ".claude/settings.json", json.dumps(SETTINGS, indent=2) + "\n")
            if name in GUIDES:
                write(group / "CLAUDE.md", GUIDES[name])
            if name == "C-indexed":
                rows = {doc["id"]: doc["index"] for doc in world["docs"]}
                write(group / "INDEX.md", render_index(world, paths, rows))
            if name == "D-wiki":
                write(group / "wiki/index.md", "# 主題導覽\n\n"
                      "- 節點快取與快取時效 → [[concepts/node-caching]]\n"
                      "- 對話與跨執行記憶 → [[concepts/persistence]]\n")
                excerpt = (ROOT / "fixtures/wiki-excerpt.txt").read_text(encoding="utf-8")
                source = paths[question["gold_docs"][0]]
                write(group / "wiki/concepts/node-caching.md",
                      f"# 節點快取\n\n{excerpt}\n## 出處\n\n{source}\n")
                write(group / "wiki/concepts/persistence.md",
                      "# 短期記憶與保存\n\n單一對話與多次執行的背景資料可由這兩篇著手。\n\n"
                      "## 出處\n\ndocs/langchain/short-term-memory.md\ndocs/langgraph/persistence.md\n")
        stage.rename(dest)
    print(question["question"])


def verify(dest, world, question):
    for group, mapping in layout(world).items():
        for doc in world["docs"]:
            target = dest / group / mapping[doc["id"]]
            if target.read_text(encoding="utf-8") != doc["body"]:
                raise SystemExit(f"來源內容有異動：{target}")
        gold_path = mapping[question["gold_docs"][0]]
        source = (dest / group / gold_path).read_text(encoding="utf-8")
        if not all(term in source for term in question["must_include"]):
            raise SystemExit(f"{gold_path} 找不到所需證據")
        if group in GUIDES:
            guide = "INDEX.md" if group == "C-indexed" else "wiki/concepts/node-caching.md"
            if gold_path not in (dest / group / guide).read_text(encoding="utf-8"):
                raise SystemExit(f"{group}/{guide} 找不到來源路徑")
        print(f"{group}：{gold_path} → key_func、ttl")
    print("四組各 3 份摘錄一致，索引與 wiki 可回到同一份原文。")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "verify"))
    parser.add_argument("--out", type=Path, default=Path("practice"))
    args = parser.parse_args()
    world, question = material()
    if args.command == "prepare":
        prepare(args.out, world, question)
    else:
        verify(args.out, world, question)


if __name__ == "__main__":
    main()
