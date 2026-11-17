"""文件 → A/B/C/D 四個 Claude Code 專案（放在家目錄外的 stage 資料夾）。"""
from __future__ import annotations

import json
import random
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from lab.common import (CONDS, INDEX_CACHE, MAPPING, WIKI, claude_json, fit_budget, is_under_home,
                        leaking_ancestors, load_bodies, load_json, load_world, save_json, sha256, stage_root)
from lab.wiki import check_wiki, load_wiki

SETTINGS = {"permissions": {"deny": ["Bash", "Edit", "Write", "NotebookEdit", "WebFetch", "WebSearch"]}}

CLAUDE_MD = """# 資料查找指引
- 先讀 INDEX.md，依關鍵字找出候選文件，再打開文件確認內容。
- 同一主題有多個版本時，以日期最新的為準。
"""

CLAUDE_MD_WIKI = """# 資料查找指引
- 先讀 wiki/index.md 找出相關頁面，再順著頁面裡的 [[連結]] 往下找（[[分類/檔名]] 對應 wiki/分類/檔名.md）。
- 回答前，依頁面「## 出處」打開 docs/ 裡的原始文件確認內容。
- 同一主題有多個版本時，以日期最新的為準。
"""

# 每一組除了 docs/ 和 .claude/ 之外，還應該有的東西
EXTRAS = {"A-messy": set(), "B-organized": set(), "C-indexed": {"CLAUDE.md", "INDEX.md"},
          "D-wiki": {"CLAUDE.md", "wiki"}}
GUIDES = {"C-indexed": CLAUDE_MD, "D-wiki": CLAUDE_MD_WIKI}

INDEX_PROMPT = """你是技術文件管理員。下面每一份文件只附上開頭和所有標題。請替每份文件寫一列索引：
- summary：一句繁體中文（40 字以內），說明這份文件在講什麼。
- keywords：8–12 個關鍵字，包含文件裡重要的英文名詞（類別、函式、參數、功能名稱），以及對應的繁體中文說法、同義詞和口語說法。
- path：原樣照抄文件標籤上的 path。
只根據提供的內容撰寫，不要編造。

"""

INDEX_SCHEMA = {
    "type": "object",
    "properties": {"rows": {"type": "array", "items": {
        "type": "object",
        "properties": {"path": {"type": "string"}, "summary": {"type": "string"},
                       "keywords": {"type": "array", "items": {"type": "string"}}},
        "required": ["path", "summary", "keywords"],
    }}},
    "required": ["rows"],
}


def layout(world: dict, seed: int = 42) -> dict[str, dict[str, str]]:
    """每一組的 doc_id → 相對路徑。A 用固定種子打亂編號；B、C、D 用「框架/頁面路徑」。"""
    ids = [d["id"] for d in world["docs"]]
    shuffled = ids[:]
    random.Random(seed).shuffle(shuffled)
    messy = {doc_id: f"docs/doc_{i:03d}.md" for i, doc_id in enumerate(shuffled, 1)}
    organized = {d["id"]: f"docs/{d['category']}/{d['slug']}.md" for d in world["docs"]}
    if len(set(organized.values())) != len(organized):
        raise ValueError("B 組有重複的檔案路徑")
    return {"A-messy": messy, "B-organized": organized, "C-indexed": dict(organized), "D-wiki": dict(organized)}


def _cell(text: str) -> str:
    return text.replace("|", "／").replace("\n", " ").strip()


def render_index(world: dict, paths: dict[str, str], rows: dict[str, dict]) -> str:
    """每份文件一列：路徑、摘要、前 n 個關鍵字（n 取放得進 INDEX_BUDGET 的最大值；不放標題，省空間）。"""
    docs = sorted(world["docs"], key=lambda d: paths[d["id"]])

    def render(n: int) -> str:
        lines = ["# 文件索引", "", "| 路徑 | 摘要 | 關鍵字 |", "|---|---|---|"]
        lines += [f"| {paths[d['id']]} | {_cell(rows[d['id']]['summary'])} | "
                  f"{_cell('、'.join(rows[d['id']]['keywords'][:n]))} |" for d in docs]
        return "\n".join(lines) + "\n"

    return fit_budget(render, max(len(rows[d["id"]]["keywords"]) for d in docs))


def digest(body: str, limit: int = 3000) -> str:
    """索引用的材料：開頭 1500 字元，加上所有標題行。整頁太長，不直接丟給模型。"""
    heads = [line for line in body.splitlines() if line.startswith("#")]
    return (body[:1500] + "\n…\n" + "\n".join(heads))[:limit]


def index_rows(world: dict, bodies: dict[str, str], paths: dict[str, str], model: str,
               batch: int = 10, workers: int = 4) -> dict[str, dict]:
    """盲建索引：每一批只給文件的開頭和標題，完全不給題目。結果快取在 world/index_rows.json。"""
    cache = load_json(INDEX_CACHE) if INDEX_CACHE.exists() else {}

    def stale(doc_id: str) -> bool:
        return cache.get(doc_id, {}).get("sha") != sha256(bodies[doc_id])

    todo = [d["id"] for d in world["docs"] if stale(d["id"])]
    lock = threading.Lock()

    def work(ids: list[str]) -> None:
        docs = "\n\n".join(f'<document path="{paths[i]}">\n{digest(bodies[i])}\n</document>' for i in ids)
        try:
            out = claude_json(INDEX_PROMPT + docs, INDEX_SCHEMA, model)
        except Exception as e:  # noqa: BLE001
            print(f"  索引批次失敗（{', '.join(ids)}）：{e}")
            return
        by_path = {r["path"]: r for r in out["rows"]}
        with lock:
            for i in ids:
                if r := by_path.get(paths[i]):
                    cache[i] = {"sha": sha256(bodies[i]), "summary": r["summary"], "keywords": r["keywords"]}
            save_json(INDEX_CACHE, cache)

    if todo:
        print(f"盲建索引：{len(todo)} 份文件 …")
        with ThreadPoolExecutor(workers) as pool:
            list(pool.map(work, [todo[i:i + batch] for i in range(0, len(todo), batch)]))
    missing = [d["id"] for d in world["docs"] if stale(d["id"])]
    if missing:
        raise SystemExit(f"這些文件沒有索引，請重跑 lab build：{', '.join(missing)}")
    return cache


def stage_problems(root: Path, maps: dict, bodies: dict[str, str], wiki: dict[str, str] | None = None) -> list[str]:
    """檢查 stage：位置、上層指示檔、各組內文逐字相同、設定一致、各組只有該有的額外檔案，以及 D 組的 wiki 跟 world/wiki 相同。"""
    problems = []
    if is_under_home(root):
        problems.append(f"stage 資料夾在家目錄底下：{root}")
    problems += [f"上層資料夾有指示檔：{p}" for p in leaking_ancestors(root)]
    for cond in CONDS:
        cdir = root / cond
        settings = cdir / ".claude" / "settings.json"
        if not settings.exists() or json.loads(settings.read_text(encoding="utf-8")) != SETTINGS:
            problems.append(f"{cond} 的 .claude/settings.json 不符")
        for name in ("CLAUDE.md", "INDEX.md", "wiki"):
            if (cdir / name).exists() != (name in EXTRAS[cond]):
                problems.append(f"{cond} 的 {name} 狀態不符")
        guide = cdir / "CLAUDE.md"
        if cond in GUIDES and guide.exists() and guide.read_text(encoding="utf-8") != GUIDES[cond]:
            problems.append(f"{cond} 的 CLAUDE.md 內容不符")
        for doc_id, rel in maps[cond].items():
            f = cdir / rel
            if not f.exists() or sha256(f.read_text(encoding="utf-8")) != sha256(bodies[doc_id]):
                problems.append(f"{cond}/{rel} 內文與標準正文不同")
    staged_wiki = root / "D-wiki" / "wiki"
    if wiki is not None and staged_wiki.exists() and load_wiki(staged_wiki) != wiki:
        problems.append("D-wiki 的 wiki/ 與 world/wiki/ 不同")
    return problems


def build(model: str = "sonnet") -> None:
    world = load_world()
    bodies = load_bodies(world)
    root = stage_root()
    if is_under_home(root):
        raise SystemExit(f"stage 資料夾不能在家目錄底下：{root}（用 LAB_STAGE 換位置）")
    maps = layout(world)
    if not WIKI.exists():
        raise SystemExit("D 組需要 world/wiki/：請先用 Antigravity 建好 wiki，再執行 lab wiki-import <資料夾>")
    wiki = load_wiki(WIKI)
    if check_wiki(wiki, set(maps["D-wiki"].values()))[0]:
        raise SystemExit("world/wiki/ 還有問題，請先執行 lab wiki-check")
    rows = index_rows(world, bodies, maps["C-indexed"], model)
    for cond in CONDS:
        cdir = root / cond
        if cdir.exists():
            shutil.rmtree(cdir)
        for doc_id, rel in maps[cond].items():
            target = cdir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(bodies[doc_id], encoding="utf-8")
        save_json(cdir / ".claude" / "settings.json", SETTINGS)
    (root / "C-indexed" / "CLAUDE.md").write_text(CLAUDE_MD, encoding="utf-8")
    (root / "C-indexed" / "INDEX.md").write_text(render_index(world, maps["C-indexed"], rows), encoding="utf-8")
    (root / "D-wiki" / "CLAUDE.md").write_text(CLAUDE_MD_WIKI, encoding="utf-8")
    for rel, text in wiki.items():
        target = root / "D-wiki" / "wiki" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    save_json(MAPPING, maps)
    if problems := stage_problems(root, maps, bodies, wiki):
        raise SystemExit("建置後檢查失敗：\n" + "\n".join(f"- {p}" for p in problems))
    print(f"完成：{root}（{len(world['docs'])} 份文件 × {len(CONDS)} 組，wiki {len(wiki)} 個檔案）")
