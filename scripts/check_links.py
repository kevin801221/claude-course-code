#!/usr/bin/env python3
"""Check external URLs in Markdown files are reachable."""

import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote, urldefrag, urlsplit, urlunsplit

from check_markdown_prose import (
    MARKDOWN_TARGET,
    frozen_student_snapshot,
    markdown_prose,
)

IGNORE_DIRS = {
    ".venv",
    "node_modules",
    ".git",
    "blog-posts",
    "openspec",
    "prompts",
    ".agents",
    ".claude",
}
TIMEOUT = 10
# Domains/patterns to skip: badges, placeholders, and bot-blocking hosts
SKIP_DOMAINS = {
    "shields.io",
    "img.shields.io",
    "star-history.com",
    "api.star-history.com",
    "example.com",
    "localhost",
    "127.0.0.1",
    "my-webhook.example.com",
    "git.internal",
    # Wikipedia blocks HEAD requests — GET also unreliable in CI without network
    "en.wikipedia.org",
    "wikipedia.org",
    # GitHub API requires auth — unauthenticated requests return 404 for protected endpoints
    "api.github.com",
    # Claude Code native-binary download host — directory listing returns 404, artifacts are
    # fetched programmatically by the installer via the full filename path
    "downloads.claude.ai",
}
SKIP_DOMAIN_SUFFIXES = (".example.com", ".example.org", ".internal")
# Placeholder/template URLs that are intentionally non-resolvable
SKIP_URL_PATTERNS = {
    "github.com/org/",
    "github.com/user/",
    "github.com/your-org/",
    "docs.example.com",
}

URL_RE = re.compile(r"https?://[a-zA-Z0-9][a-zA-Z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+")


def is_skipped(url: str) -> bool:
    try:
        domain = url.split("/", 3)[2].split(":", 1)[0]
    except IndexError:
        return True  # malformed URL
    if any(skip == domain or domain.endswith("." + skip) for skip in SKIP_DOMAINS):
        return True
    if any(domain.endswith(suffix) for suffix in SKIP_DOMAIN_SUFFIXES):
        return True
    return any(pattern in url for pattern in SKIP_URL_PATTERNS)


# These two published source references are instructor-only. The runnable student
# materials and public download are checked separately with all other public URLs.
PRIVATE_SOURCES = {
    "https://github.com/kevin801221/autosearch-PRD-claudecode",
    "https://github.com/kevin801221/autosearch-PRD-claudecode/tree/f0e10cef442c46cef9eebda4831225374cc4fbd7",
}


def external_urls(text: str) -> set[str]:
    prose, _ = markdown_prose(text)
    urls = {m[1] or m[2] for m in MARKDOWN_TARGET.finditer(prose)}
    # Also check bare student-facing URLs. Extract Markdown targets first to
    # preserve Unicode paths and legit trailing underscores in repository names.
    for candidate in URL_RE.findall(MARKDOWN_TARGET.sub(" ", prose)):
        raw = candidate.rstrip(">*`':.,;")
        while raw.endswith(")") and raw.count(")") > raw.count("("):
            raw = raw[:-1]
        urls.add(raw)
    result = set()
    for value in urls:
        if not value.startswith(("https://", "http://")):
            continue
        parts = urlsplit(urldefrag(value)[0])
        if not parts.hostname or "." not in parts.hostname:
            continue
        result.add(
            urlunsplit(
                (
                    parts.scheme,
                    parts.netloc,
                    quote(parts.path, safe="/%:@!$&'()*+,;=-._~"),
                    quote(parts.query, safe="=&%:@!$'()*+,;/?-._~"),
                    "",
                )
            )
        )
    return result


def check_url(url: str) -> tuple[str, bool, str]:
    if is_skipped(url):
        return url, True, "skipped"
    method = "HEAD"
    for attempt in range(3):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            if method == "GET":
                headers["Range"] = "bytes=0-0"
            req = urllib.request.Request(url, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=TIMEOUT):  # nosec B310
                return url, True, "ok"
        except urllib.error.HTTPError as error:
            if error.code in (401, 403) or (error.code == 429 and attempt == 2):
                return url, True, "access restricted"
            reason = f"HTTP {error.code}"
            if method == "HEAD" and error.code in (404, 405):
                method = "GET"
            elif error.code not in (408, 429, 500, 502, 503, 504):
                break
        except (OSError, ValueError) as error:
            reason = str(error)
        if attempt < 2:
            time.sleep(attempt + 1)
    return url, False, reason


def main(strict: bool = False) -> int:
    urls: dict[str, list[str]] = {}  # url -> [file, ...]

    private_references = set()
    md_files = [
        f
        for f in Path().rglob("*.md")
        if not any(part in IGNORE_DIRS for part in f.parts)
        and not frozen_student_snapshot(f)
    ]

    for file_path in md_files:
        content = file_path.read_text()
        for url in external_urls(content):
            if url in PRIVATE_SOURCES:
                private_references.add(url)
                continue
            urls.setdefault(url, []).append(str(file_path))

    if private_references:
        print("Access required for these instructor-only sources:")
        for private_url in sorted(private_references):
            print(f"  - {private_url}")
    if not urls:
        print("✅ No external URLs found")
        return 0

    errors: list[str] = []
    statuses: Counter[str] = Counter()
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(check_url, url): url for url in urls}
        for future in as_completed(futures):
            url, ok, reason = future.result()
            statuses[reason] += 1
            if not ok:
                errors.extend(f"{f}: dead link → {url} ({reason})" for f in urls[url])

    if errors:
        print("❌ Dead links found:")
        for e in sorted(errors):
            print(f"  - {e}")
        # In non-strict mode (pre-commit), report but don't block the commit.
        # Set LINK_CHECK_STRICT=1 (as CI does) to enforce failures.
        return 1 if strict else 0

    print(
        f"✅ No broken public links found: {statuses['ok']} reachable, "
        f"{statuses['access restricted']} access/rate-limited, {statuses['skipped']} configured exclusions."
    )
    return 0


if __name__ == "__main__":
    import os

    sys.exit(main(strict=os.environ.get("LINK_CHECK_STRICT") == "1"))
