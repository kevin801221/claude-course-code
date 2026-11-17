"""共用小工具：雜湊、JSON、輸出目錄守衛、安全路徑、極簡 schema 驗證。"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCHEMAS = REPO / "schemas"


class WorkshopError(Exception):
    """可預期的錯誤：訊息給操作者看，code 為 CLI 結束碼。"""

    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_run_id(prefix: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{stamp}-{secrets.token_hex(2)}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def read_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj) -> None:
    write_text(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def write_text(path: Path, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def prepare_out_dir(path: Path) -> Path:
    """不覆蓋既有結果：目錄已存在就拒絕。"""
    path = Path(path)
    if path.exists():
        raise WorkshopError(f"輸出目錄已存在：{path}。為保留既有結果，請改用新的 --out 路徑。", code=2)
    path.mkdir(parents=True)
    return path


def warn(msg: str) -> None:
    print(f"[警示] {msg}", file=sys.stderr)


def safe_child(root: Path, rel: str) -> Path:
    """rel 必須是 root 底下的相對路徑，不得越界或經過符號連結。"""
    if not isinstance(rel, str) or not rel or "\\" in rel or rel.startswith("/") or os.path.isabs(rel):
        raise WorkshopError(f"路徑不是安全的相對路徑：{rel!r}")
    parts = Path(rel).parts
    if any(p in ("..", "") for p in parts):
        raise WorkshopError(f"路徑含越界片段：{rel!r}")
    root = Path(root).resolve()
    cur = root
    for p in parts:
        cur = cur / p
        if cur.is_symlink():
            raise WorkshopError(f"路徑經過符號連結：{rel!r}")
    if not cur.resolve().is_relative_to(root):
        raise WorkshopError(f"路徑越界：{rel!r}")
    return cur


# ---- 極簡 JSON Schema 子集：type / required / properties / items / enum ----
_TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "number": (int, float), "integer": int, "null": type(None),
}


def _is_type(v, t: str) -> bool:
    if t in ("number", "integer") and isinstance(v, bool):
        return False
    return isinstance(v, _TYPES[t])


def validate(inst, schema: dict, where: str = "$") -> list[str]:
    errs: list[str] = []
    t = schema.get("type")
    if t is not None:
        ts = t if isinstance(t, list) else [t]
        if not any(_is_type(inst, x) for x in ts):
            return [f"{where}：型別應為 {t}"]
    if "enum" in schema and inst not in schema["enum"]:
        errs.append(f"{where}：值 {inst!r} 不在 {schema['enum']}")
    if isinstance(inst, dict):
        for k in schema.get("required", []):
            if k not in inst:
                errs.append(f"{where}：缺少欄位 {k}")
        for k, sub in schema.get("properties", {}).items():
            if k in inst:
                errs += validate(inst[k], sub, f"{where}.{k}")
    if isinstance(inst, list) and "items" in schema:
        for i, item in enumerate(inst):
            errs += validate(item, schema["items"], f"{where}[{i}]")
    return errs


def check_schema(inst, name: str) -> list[str]:
    return validate(inst, read_json(SCHEMAS / f"{name}.schema.json"))
