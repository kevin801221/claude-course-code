#!/usr/bin/env python3
"""離線檢查教材：結構、語法、相對連結、來源快照與精選檔雜湊。"""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []
files = [p for p in ROOT.rglob("*") if p.is_file() and not any(x in {".git", "node_modules", ".outputs", "__pycache__"} for x in p.relative_to(ROOT).parts) and p.name != "tasks.json"]


def fail(path, message):
    errors.append(f"{path.relative_to(ROOT)}: {message}")


for path in files:
    if path.is_symlink():
        fail(path, "教材不應包含符號連結")
    # Source snapshots retain upstream schemas, example snippets and old links.
    # Their bytes and completeness are checked by check-full-course.py instead.
    if path.relative_to(ROOT).parts[0] in {"course", "references"} and path.relative_to(ROOT).as_posix() != "references/english-workflows/README.md":
        continue
    if path.suffix == ".json":
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError) as error:
            fail(path, f"JSON 無法解析：{error}")
    if path.suffix == ".py":
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as error:
            fail(path, f"Python 語法錯誤：{error}")
    if path.suffix == ".md":
        inside = False
        fence = ""
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.lstrip()
            if stripped.startswith(("```", "~~~")):
                marker = stripped[:3]
                if not inside:
                    inside, fence = True, marker
                elif marker == fence:
                    inside = False
                continue
            if inside:
                continue
            for match in re.finditer(r"\[[^\]\n]*\]\(([^)\n]+)\)", line):
                target = match.group(1).strip().strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith(("#", "//")):
                    continue
                local = (path.parent / unquote(parsed.path)).resolve()
                if not local.is_relative_to(ROOT) or not local.exists():
                    fail(path, f"本地連結不存在：{target}")
    if path.name == "SKILL.md" or (path.suffix == ".md" and path.name != "README.md" and path.parent.name == "agents"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            fail(path, "缺少 YAML frontmatter 邊界")

expected_labs = ["00-cli", "01-memory", "02-commands", "03-skills", "04-agents", "05-hooks", "06-mcp", "07-plugins", "08-workflows", "09-automation", "10-projects", "11-mods"]
for lab in expected_labs:
    if not (ROOT / "labs" / lab / "README.md").is_file():
        fail(ROOT / "labs" / lab, "缺少 Lab README")

manifest_path = ROOT / "sources/manifest.json"
try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for row in manifest["files"]:
        destination = ROOT / row["destination"]
        if not destination.is_file():
            fail(manifest_path, f"精選檔不存在：{row['destination']}")
            continue
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        if digest != row["destination_sha256"]:
            fail(destination, "與發行版來源 manifest 的 hash 不符；若刻意改教材，請另記新版本")
        if row["kind"] == "copy" and digest != row["source_sha256"]:
            fail(destination, "原樣複製檔與來源 hash 不符")
    for snapshot in manifest["snapshots"]:
        license_path = ROOT / snapshot["license_file"]
        if not license_path.is_file() or hashlib.sha256(license_path.read_bytes()).hexdigest() != snapshot["license_sha256"]:
            fail(manifest_path, f"授權缺失或變動：{snapshot['name']}")
except (ValueError, OSError, KeyError) as error:
    fail(manifest_path, f"來源 manifest 無法驗證：{error}")

secret_pattern = re.compile(rb"(?:sk-ant-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)")
for path in files:
    if secret_pattern.search(path.read_bytes()):
        fail(path, "疑似憑證；請檢查內容，不要發布")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"教材檢查通過：{len(files)} 個檔案、{len(expected_labs)} 個 Labs、{len(manifest['files'])} 項來源紀錄。")
print("已檢查本包編寫檔案的 JSON、Python 語法、本地連結、frontmatter 與精選來源雜湊。")
print("course/、references/ 的來源快照由完整課堂檢查器驗證；不宣稱所有上游程式皆可直接執行。")
print("此命令不呼叫模型，不驗證外部網站或真人 Claude 端到端行為。")
