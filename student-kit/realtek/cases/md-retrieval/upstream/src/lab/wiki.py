"""D 組（LLM wiki）：準備 Antigravity 的工作資料夾，匯入並檢查它產出的 wiki。check_wiki 是純函式。"""
from __future__ import annotations

import re
import shutil
from collections import Counter
from pathlib import Path

from lab.collect import clean_body
from lab.common import CORPUS, INDEX_BUDGET, ROOT, WIKI, fit_budget, load_world

DOC_REF = re.compile(r"docs/[a-z-]+/[A-Za-z0-9_/.-]+\.md")
WIKI_LINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
LOCAL_PATH = re.compile(r"/Users/|/private/")   # 本機（macOS）路徑；/home/... 是文件裡沙盒的範例路徑，不算
SPECIAL = {"index.md", "log.md"}
TASK = ROOT / "docs" / "antigravity-wiki.md"
CATEGORIES = {"concepts": "概念", "entities": "API 與設定", "guides": "操作指南", "versions": "版本與遷移",
              "comparisons": "比較"}


def check_wiki(files: dict[str, str], doc_paths: set[str]) -> tuple[list[str], list[str], dict]:
    """files：wiki 內的相對路徑 → 內容；doc_paths：D 組文件路徑（docs/...）。回傳 (問題, 提醒, 統計)。"""
    problems: list[str] = []
    warnings: list[str] = []
    if "index.md" not in files:
        problems.append("缺少 index.md")
    elif len(files["index.md"]) > INDEX_BUDGET:
        problems.append(f"index.md 有 {len(files['index.md'])} 字元，超過 {INDEX_BUDGET}，Claude 一次讀不完"
                        "（可以用 lab wiki-index 重建）")
    pages = {p: t for p, t in files.items() if p not in SPECIAL}
    cited: set[str] = set()
    broken: list[str] = []
    links = 0
    for path, text in sorted(files.items()):
        if LOCAL_PATH.search(text):
            problems.append(f"{path}：出現本機路徑")
        refs = set(DOC_REF.findall(text))
        cited |= refs & doc_paths
        for ref in sorted(refs - doc_paths):
            problems.append(f"{path}：出處不存在 {ref}")
        for target in WIKI_LINK.findall(text):
            links += 1
            if target.strip().removesuffix(".md") + ".md" not in files:
                broken.append(f"{path} → [[{target.strip()}]]")
        if path in pages and not re.search(r"^## 出處", text, re.M):
            problems.append(f"{path}：缺少「## 出處」")
    if broken:
        warnings.append(f"{len(broken)} 個連結找不到頁面，例如：{'；'.join(broken[:5])}")
    if uncited := sorted(doc_paths - cited):
        warnings.append(f"{len(uncited)} 份文件沒有被任何頁面引用，例如：{'、'.join(uncited[:5])}")
    stats = {"pages": len(pages),
             "by_category": dict(Counter(p.split("/")[0] if "/" in p else "(根目錄)" for p in pages)),
             "links": links, "cited_docs": len(cited), "chars": sum(len(t) for t in files.values())}
    return problems, warnings, stats


def render_wiki_index(files: dict[str, str]) -> str:
    """依分類列出每一頁：[[分類/檔名]] — 摘要第一句。關鍵詞：前 n 個別名（n 取放得進 INDEX_BUDGET 的最大值）。
    給 Antigravity 沒寫完 index.md 時用；內容全部取自各頁，不加入人工判斷。"""
    entries: dict[str, list[tuple[str, str, list[str]]]] = {}
    for path, text in sorted(files.items()):
        if path in SPECIAL:
            continue
        alias = re.search(r"^別名：(.+)$", text, re.M)
        summary = re.search(r"^## 摘要\n+(.+?)(?:。|\n)", text, re.M | re.S)
        if not (alias and summary):
            raise SystemExit(f"{path}：缺少「別名：」或「## 摘要」，無法放進 index")
        cat = path.split("/")[0]
        entries.setdefault(cat, []).append((path.removesuffix(".md"), summary.group(1).strip(),
                                            alias.group(1).strip().split("、")))
    cats = [c for c in CATEGORIES if c in entries] + sorted(set(entries) - set(CATEGORIES))

    def render(n: int) -> str:
        lines = ["# Wiki 目錄", ""]
        for cat in cats:
            lines.append(f"## {CATEGORIES.get(cat, cat)}（{cat}）")
            lines += [f"- [[{link}]] — {s}。關鍵詞：{'、'.join(a[:n])}" for link, s, a in entries[cat]]
            lines.append("")
        return "\n".join(lines)

    return fit_budget(render, max(len(a) for es in entries.values() for _, _, a in es))


def wiki_index(src: Path) -> None:
    """重建 Antigravity 工作資料夾裡的 wiki/index.md（會覆寫）。"""
    text = render_wiki_index(load_wiki(src / "wiki"))
    (src / "wiki" / "index.md").write_text(text, encoding="utf-8")
    print(f"完成：{src / 'wiki' / 'index.md'}（{len(text)} 字元）")


def doc_paths() -> set[str]:
    return {f"docs/{d['id']}.md" for d in load_world()["docs"]}


def load_wiki(root: Path) -> dict[str, str]:
    """讀取 root 底下所有 .md（相對路徑 → 內容），換行統一成 LF。"""
    return {str(p.relative_to(root)): clean_body(p.read_text(encoding="utf-8")) for p in sorted(root.rglob("*.md"))}


def _report(files: dict[str, str]) -> None:
    problems, warnings, stats = check_wiki(files, doc_paths())
    cats = "、".join(f"{k} {v}" for k, v in sorted(stats["by_category"].items()))
    print(f"wiki：{stats['pages']} 頁（{cats}），連結 {stats['links']} 個，"
          f"引用 {stats['cited_docs']} 份文件，共 {stats['chars']} 字元")
    for w in warnings:
        print(f"  提醒：{w}")
    for p in problems:
        print(f"  問題：{p}")
    if problems:
        raise SystemExit(f"有 {len(problems)} 個問題要修正")
    print("沒有問題" + (f"（有 {len(warnings)} 個提醒）" if warnings else ""))


def wiki_export(dst: Path) -> None:
    """建立給 Antigravity 的工作資料夾：只放文件副本（唯讀）和任務說明，不放題目。"""
    dst = dst.resolve()
    if dst == ROOT or ROOT in dst.parents:
        raise SystemExit("工作資料夾不能放在 repo 裡，因為 repo 裡有題目")
    if dst.exists():
        raise SystemExit(f"{dst} 已經存在，請換個位置，或先把它移走")
    shutil.copytree(CORPUS, dst / "docs")
    for p in sorted((dst / "docs").rglob("*"), reverse=True) + [dst / "docs"]:
        p.chmod(p.stat().st_mode & ~0o222)   # 唯讀，避免文件被改動
    (dst / "wiki").mkdir()
    shutil.copy(TASK, dst / "WIKI_TASK.md")
    print(f"完成：{dst}（請在 Antigravity 開啟這個資料夾，依照 WIKI_TASK.md 建立 wiki）")


def wiki_import(src: Path) -> None:
    """把 Antigravity 工作資料夾裡的 wiki/ 匯入 world/wiki/（只匯入 .md 檔），再做檢查。"""
    if not (src / "wiki").is_dir():
        raise SystemExit(f"找不到 {src / 'wiki'}")
    files = load_wiki(src / "wiki")
    if WIKI.exists():
        shutil.rmtree(WIKI)
    for rel, text in files.items():
        target = WIKI / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    print(f"已匯入 {len(files)} 個檔案到 world/wiki/")
    _report(files)


def wiki_check() -> None:
    if not WIKI.exists():
        raise SystemExit("還沒有 world/wiki/，請先執行 lab wiki-import <Antigravity 的資料夾>")
    _report(load_wiki(WIKI))
