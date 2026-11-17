"""測試共用：以子程序呼叫 CLI；B run 只跑一次並快取（所有輸出都在暫存目錄，不寫 outputs/）。"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
HAS_CMAKE = bool(shutil.which("cmake") and shutil.which("ctest"))
needs_cmake = unittest.skipUnless(HAS_CMAKE, "需要 cmake/ctest 與 C++17 編譯器")
_TMP = tempfile.TemporaryDirectory(prefix="workshop-tests-")
_B: dict = {}


def tmpdir() -> Path:
    return Path(tempfile.mkdtemp(dir=_TMP.name))


def cli(*args) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "workshop", *map(str, args)], cwd=REPO,
                          capture_output=True, text=True, encoding="utf-8")


def b_run() -> Path:
    """回傳一次成功 B run 的目錄（快取）。"""
    if "dir" not in _B:
        out = tmpdir() / "b"
        p = cli("b", "run", "--offline", "--out", out)
        assert p.returncode == 0, p.stdout + p.stderr
        _B["dir"] = out
    return _B["dir"]


def copy_b_run() -> Path:
    dst = tmpdir() / "b"
    shutil.copytree(b_run(), dst)
    return dst


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, obj) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reseal(project: Path) -> None:
    """模擬「有人改了 JSON 也同步改了版本雜湊」，讓檢核聚焦在內容規則本身。"""
    from workshop.c_draft import load_version, version_sha
    pj = read_json(project / "project.json")
    v = pj["current_version"]
    pj["versions"][v]["sha256"] = version_sha(load_version(project, v))
    write_json(project / "project.json", pj)
