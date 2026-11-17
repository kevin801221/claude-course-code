"""Shared Markdown handling for document checks that should not scan code examples."""

import json
import re
from functools import lru_cache
from pathlib import Path

FENCE_START = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.+?)\1(?!`)")
# Accept URL-encoded and Unicode destinations, including balanced path parentheses.
MARKDOWN_TARGET = re.compile(
    r"\]\(\s*(?:<([^>\n]+)>|((?:[^()\s]|\([^()\n]*\))+))"
    r"(?:\s+[\"'][^\n]*?[\"'])?\s*\)"
)


@lru_cache(maxsize=4)
def _student_sources(kit: Path) -> set[str]:
    destinations = set()
    for name in ("manifest.json", "full-manifest.json"):
        manifest = json.loads((kit / "sources" / name).read_text(encoding="utf-8"))
        for item in manifest["files"] + manifest.get("supplemental_files", []):
            destinations.add(item["destination"])
    return destinations


def frozen_student_snapshot(path: Path) -> bool:
    """The kit checks hashes for these specific upstream source files in CI."""
    if path.parts[:2] not in {("student-kit", "course"), ("student-kit", "references")}:
        return False
    return path.relative_to("student-kit").as_posix() in _student_sources(
        Path("student-kit").resolve()
    )


def markdown_prose(text: str) -> tuple[str, bool]:
    """Return text outside fenced/inline examples and whether a fence was left open."""
    lines = []
    marker = ""
    for line in text.splitlines():
        boundary = FENCE_START.match(line)
        if marker:
            if boundary and boundary[1].startswith(marker) and not boundary[2].strip():
                marker = ""
        elif boundary:
            marker = boundary[1]
        else:
            lines.append(INLINE_CODE.sub("", line))
    return "\n".join(lines), bool(marker)
