"""下載官方文件：LangChain／LangGraph／Deep Agents（langchain-ai/docs repo）與 Claude Agent SDK（code.claude.com）。"""
from __future__ import annotations

import io
import re
import tarfile
import urllib.request
from datetime import date

from lab.common import CORPUS, DOCS_JSON, FRAMEWORKS, load_json, save_json, sha256

LC_TARBALL = "https://codeload.github.com/langchain-ai/docs/tar.gz/main"
LC_FRAMEWORKS = {"deepagents", "langchain", "langgraph"}
SDK_INDEX = "https://code.claude.com/docs/llms.txt"
SDK_LINK = re.compile(r"\((https://code\.claude\.com/docs/en/agent-sdk/[a-z0-9/-]+\.md)\)")
SDK_PAGE = "https://code.claude.com/docs/en/agent-sdk/{slug}.md"
# Agent SDK 每頁開頭都有一段固定的「Documentation Index」引言，把它去掉
DOC_INDEX_BANNER = re.compile(r"\A(?:> .*\n)+\n?")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "retrieval-lab"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def title_of(body: str, fallback: str) -> str:
    """標題：優先用 frontmatter 的 title，其次用第一個 # 標題。"""
    fm = re.match(r"---\n(.*?)\n---", body, re.S)
    if fm and (m := re.search(r"^title:\s*(.+)$", fm.group(1), re.M)):
        return m.group(1).strip().strip("\"'")
    if m := re.search(r"^# (.+)$", body, re.M):
        return m.group(1).strip()
    return fallback


def clean_body(body: str) -> str:
    """換行統一成 LF、去掉頭尾空白並以換行結尾。git 的 autocrlf 才不會事後改動內文，讓 sha 對不上。"""
    return body.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n"


def langchain_pages(wanted: set[str]) -> list[tuple[str, str, str]]:
    """回傳 (框架, 頁面路徑, 內文)。"""
    pages = []
    with tarfile.open(fileobj=io.BytesIO(fetch(LC_TARBALL)), mode="r:gz") as tar:
        for member in tar.getmembers():
            parts = member.name.split("/")   # docs-main/src/oss/<框架>/.../<頁>.mdx
            if (member.isfile() and member.name.endswith(".mdx") and len(parts) > 4
                    and parts[1:3] == ["src", "oss"] and parts[3] in wanted):
                slug = "/".join(parts[4:])[: -len(".mdx")]
                pages.append((parts[3], slug, tar.extractfile(member).read().decode("utf-8")))
    return pages


def sdk_page(slug: str) -> str:
    return DOC_INDEX_BANNER.sub("", fetch(SDK_PAGE.format(slug=slug)).decode("utf-8"), count=1)


def sdk_pages() -> list[tuple[str, str, str]]:
    urls = sorted(set(SDK_LINK.findall(fetch(SDK_INDEX).decode("utf-8"))))
    slugs = [url.split("/agent-sdk/", 1)[1][: -len(".md")] for url in urls]
    return [("agent-sdk", slug, sdk_page(slug)) for slug in slugs]


def collect_missing() -> list[str]:
    """補下載 docs.json 列了、但 world/corpus/ 裡沒有的 Agent SDK 文件（公開 repo 沒附全文）。
    不動 docs.json 和其他文件。回傳內容和當初 sha 不同的文件 id。"""
    world = load_json(DOCS_JSON)
    missing = [d for d in world["docs"] if not (CORPUS / f"{d['id']}.md").exists()]
    if other := [d["id"] for d in missing if d["category"] != "agent-sdk"]:
        raise SystemExit(f"缺少 {len(other)} 份不是 Agent SDK 的文件（例如 {other[0]}），請改用 lab collect --force 重新下載全部")
    changed = []
    for d in missing:
        body = clean_body(sdk_page(d["slug"]))
        path = CORPUS / f"{d['id']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        if sha256(body) != d["sha"]:
            changed.append(d["id"])
    print(f"補下載 {len(missing)} 份 Agent SDK 文件。")
    if changed:
        print(f"其中 {len(changed)} 份和 {world['collected_at']} 下載的版本不同（官方之後改過），"
              f"重跑的結果可能和 results/ 不完全一樣：" + "、".join(changed))
    return changed


def collect(only: list[str] | None = None, force: bool = False) -> None:
    if DOCS_JSON.exists() and not force:
        raise SystemExit("world/docs.json 已經存在。要重新下載請加 --force（舊結果會因 world_id 不同，自動不納入統計）")
    wanted = set(only or FRAMEWORKS)
    pages: list[tuple[str, str, str]] = []
    if wanted & LC_FRAMEWORKS:
        print("下載 langchain-ai/docs …")
        pages += langchain_pages(wanted & LC_FRAMEWORKS)
    if "agent-sdk" in wanted:
        print("下載 Claude Agent SDK 文件 …")
        pages += sdk_pages()
    pages.sort(key=lambda p: (p[0], p[1]))
    if CORPUS.exists():
        for old in CORPUS.rglob("*.md"):
            old.unlink()
    docs = []
    for category, slug, body in pages:
        doc_id = f"{category}/{slug}"
        body = clean_body(body)
        path = CORPUS / f"{doc_id}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        docs.append({"id": doc_id, "title": title_of(body, slug), "category": category, "slug": slug,
                     "chars": len(body), "sha": sha256(body)})
    save_json(DOCS_JSON, {"collected_at": date.today().isoformat(), "docs": docs})
    counts = {f: sum(1 for d in docs if d["category"] == f) for f in sorted(wanted)}
    print(f"完成：{len(docs)} 頁（" + "、".join(f"{f} {n}" for f, n in counts.items()) + "）")
