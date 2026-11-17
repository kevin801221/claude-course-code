"""共用設定與小工具。"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unicodedata
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORLD = ROOT / "world"
DOCS_JSON = WORLD / "docs.json"
QUESTIONS_JSON = WORLD / "questions.json"
CORPUS = WORLD / "corpus"
INDEX_CACHE = WORLD / "index_rows.json"
WIKI = WORLD / "wiki"   # D 組：Antigravity 產出的 LLM wiki（用 lab wiki-import 匯入）
MAPPING = ROOT / "build" / "mapping.json"
RESULTS = ROOT / "results"
RESULTS_JSONL = RESULTS / "results.jsonl"
RUNS = ROOT / "runs"

CONDS = ["A-messy", "B-organized", "C-indexed", "D-wiki"]
CLOSED = "Z-closed"
COND_LABELS = {"A-messy": "A 雜亂", "B-organized": "B 整理", "C-indexed": "C 索引", "D-wiki": "D wiki",
               CLOSED: "閉卷"}
FRAMEWORKS = ["agent-sdk", "deepagents", "langchain", "langgraph"]
QTYPES = ["lookup", "paraphrase", "version", "multi_doc", "unanswerable", "aggregate", "confusable", "near_miss"]
QTYPE_LABELS = {"lookup": "直接查找", "paraphrase": "換句話說", "version": "新舊版本",
                "multi_doc": "跨文件", "unanswerable": "題庫裡沒有",
                "aggregate": "彙整", "confusable": "易混淆", "near_miss": "近似陷阱"}
MULTI_DOC_TYPES = {"multi_doc", "aggregate"}           # 答案分散在多份文件，檢索要全部碰到
UNANSWERABLE_TYPES = {"unanswerable", "near_miss"}     # 文件沒有答案，應回答找不到

# 不載入使用者設定、MCP、技能，也不留對話紀錄（設計第 3 節）
ISOLATION = ["--strict-mcp-config", "--setting-sources", "project",
             "--disable-slash-commands", "--no-session-persistence"]
# Claude Code 會從工作目錄往上層找、並當成指示載入的檔案
INSTRUCTION_FILES = ["CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", ".claude/CLAUDE.md"]
# Read 工具一次讀到約 3.3 萬字元就會截斷（truncatedByTokenCap）；入口檔（C 的 INDEX.md、D 的 wiki/index.md）要一次讀得完
INDEX_BUDGET = 28_000


def fit_budget(render: Callable[[int], str], most: int, budget: int = INDEX_BUDGET) -> str:
    """render(n)：每筆只放前 n 個關鍵字。回傳放得進 budget 的最大 n 的結果。"""
    for n in range(most, 0, -1):
        if len(text := render(n)) <= budget:
            return text
    raise ValueError(f"每筆只放 1 個關鍵字仍超過 {budget} 字元")


def stage_root() -> Path:
    return Path(os.environ.get("LAB_STAGE", "/Users/Shared/retrieval-lab-stage"))


def norm(s: str) -> str:
    """全形轉半形、轉小寫、去掉空白與逗號，用於答案比對。"""
    s = unicodedata.normalize("NFKC", s).lower()
    return "".join(ch for ch in s if not ch.isspace() and ch != ",")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_world() -> dict:
    """回傳 {"docs": [...], "questions": [...]}；還沒出題時 questions 是空清單。"""
    docs = load_json(DOCS_JSON)["docs"]
    questions = load_json(QUESTIONS_JSON) if QUESTIONS_JSON.exists() else []
    return {"docs": docs, "questions": questions}


def load_bodies(world: dict) -> dict[str, str]:
    return {d["id"]: (CORPUS / f"{d['id']}.md").read_text(encoding="utf-8") for d in world["docs"]}


def world_id() -> str:
    """文件清單、題目與 wiki 的指紋：任何一項改變就換一個 id，舊結果自動不納入統計。
    設了 LAB_WORLD_ID 就直接用它：公開 repo 少了 7 頁 wiki，要重算 repo 裡的既有結果時用。"""
    if wid := os.environ.get("LAB_WORLD_ID"):
        return wid
    questions =QUESTIONS_JSON.read_text(encoding="utf-8") if QUESTIONS_JSON.exists() else ""
    wiki = "".join(f"{p.relative_to(WIKI)}\n{p.read_text(encoding='utf-8')}" for p in sorted(WIKI.rglob("*.md")))
    return sha256(DOCS_JSON.read_text(encoding="utf-8") + questions + wiki)[:12]


def read_rows() -> list[dict]:
    """讀取 results/results.jsonl 的所有列。"""
    if not RESULTS_JSONL.exists():
        return []
    lines = RESULTS_JSONL.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def is_under_home(path: Path, home: Path | None = None) -> bool:
    home = (home or Path.home()).resolve()
    p = path.resolve()
    return p == home or home in p.parents


def leaking_ancestors(path: Path) -> list[Path]:
    """path 本身與所有上層資料夾裡，會被 Claude Code 當成指示載入的檔案。"""
    p = path.resolve()
    return [d / name for d in (p, *p.parents) for name in INSTRUCTION_FILES if (d / name).exists()]


def claude_json(prompt: str, schema: dict, model: str, timeout: int = 900) -> dict:
    """一次性的結構化呼叫（盲建索引用）：不開任何工具，在家目錄外的暫存資料夾執行。"""
    with tempfile.TemporaryDirectory() as tmp:
        if is_under_home(Path(tmp)):
            raise RuntimeError(f"暫存資料夾在家目錄底下（{tmp}），請把 TMPDIR 設到家目錄外")
        proc = subprocess.run(
            ["claude", "-p", prompt, "--model", model, "--output-format", "json", "--tools", "",
             "--json-schema", json.dumps(schema, ensure_ascii=False), *ISOLATION],
            cwd=tmp, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout,
        )
    if proc.returncode != 0:
        raise RuntimeError(f"claude -p 失敗（exit {proc.returncode}）：{proc.stderr[-500:]}")
    out = json.loads(proc.stdout)
    if out.get("is_error") or not isinstance(out.get("structured_output"), dict):
        raise RuntimeError(f"claude -p 沒有回傳結構化結果：{str(out.get('result'))[:500]}")
    return out["structured_output"]
