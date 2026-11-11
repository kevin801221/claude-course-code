from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

import graph_builder

TODAY = date.today().isoformat()
WIKI_DIRNAME = "wiki"
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
AUTO_BLOCK_RE = re.compile(
    r"\n<!-- AUTO-INGEST START -->[\s\S]*?<!-- AUTO-INGEST END -->\n?",
    re.MULTILINE,
)
RELATED_RE = re.compile(r"\n## 相關頁面\n[\s\S]*$", re.MULTILINE)

SOURCE_SKIP = {"_cross_summary.json"}

SOURCE_TITLE_OVERRIDES = {
    "2023-10-27_財經_Podcast_財經_Podcast_EPXXX.json": "財經 Podcast EP.XXX",
    "2026-02-12_游庭皓的財經皓角__市場觀察_2026_台灣人如何迎接_少子化海嘯_.json": "市場觀察 2026 台灣人如何迎接少子化海嘯",
    "2026-02-13_游庭皓的財經皓角__市場觀察_2026台灣人如何_迎接AI時代_.json": "市場觀察 2026 台灣人如何迎接AI時代",
}

TICKER_OVERRIDES = {
    "2330.TW": "台積電",
    "TSM": "台積電",
    "2303.TW": "聯電",
    "2376.TW": "技嘉",
    "NVDA": "NVIDIA",
    "NVDA.US": "NVIDIA",
    "AMD": "AMD",
    "AMD.US": "AMD",
    "INTC": "Intel",
    "INTC.US": "Intel",
    "ARM": "Arm",
    "ARM.US": "Arm",
    "AAPL": "Apple",
    "MU": "美光",
    "AVGO": "Broadcom",
    "MRVL": "Marvell",
    "TSLA": "特斯拉",
    "005930.KS": "三星電子",
    "ASTS": "AST SpaceMobile",
    "00631L.TW": "元大台灣50正2",
    "0050.TW": "元大台灣50",
    "0050L.TW": "元大台灣50正2",
}

CONCEPT_CATALOG = {
    "AI 驅動的台灣產業升級": {
        "aliases": ["AI", "AI伺服器", "輝達", "NVIDIA", "Blackwell", "矽光帝國"],
        "tags": ["AI", "台灣經濟", "產業升級", "伺服器"],
        "summary": "這個概念整理目前來源中與 AI 需求、AI 伺服器、供應鏈擴張與台灣產業升級有關的觀察。",
    },
    "Agentic AI 與 CPU 投資主線": {
        "aliases": ["CPU", "x86", "Grace", "Rubin", "Xeon", "Arm CPU"],
        "tags": ["AI", "CPU", "半導體", "投資主線"],
        "summary": "這個概念整理 Agentic AI、CPU 角色提升與相關投資主線的觀察。",
    },
    "地緣政治與市場波動": {
        "aliases": ["川普", "伊朗", "關稅", "戰爭", "石器時代", "荷姆茲海峽", "地緣政治", "Pizza Tracker"],
        "tags": ["地緣政治", "市場波動", "風險"],
        "summary": "這個概念整理川普、伊朗、關稅與戰爭敘事如何影響市場風險偏好與資金流向。",
    },
    "CPO 與矽光子": {
        "aliases": ["CPO", "矽光", "矽光子", "共同封裝光學", "光通訊"],
        "tags": ["CPO", "矽光子", "光通訊", "AI"],
        "summary": "這個概念整理 CPO、矽光子與光通訊供應鏈在 AI 基礎設施中的投資脈絡。",
    },
    "先進封裝與封測供應鏈": {
        "aliases": ["CoWoS", "封測", "封裝", "先進封裝", "日月光", "京元電", "頎邦"],
        "tags": ["先進封裝", "封測", "半導體"],
        "summary": "這個概念整理 CoWoS、先進封裝與封測供應鏈的需求、瓶頸與投資觀察。",
    },
    "記憶體與 HBM 週期": {
        "aliases": ["HBM", "記憶體", "DRAM", "美光", "南亞科", "創見"],
        "tags": ["記憶體", "HBM", "DRAM"],
        "summary": "這個概念整理記憶體、HBM 與 DRAM 景氣循環相關的觀察。",
    },
    "PCB 與 CCL 供應鏈": {
        "aliases": ["PCB", "CCL", "台光電", "台燿", "聯茂", "金像電", "欣興"],
        "tags": ["PCB", "CCL", "供應鏈"],
        "summary": "這個概念整理 PCB、CCL 與相關板材供應鏈的投資脈絡。",
    },
    "低軌衛星與通訊供應鏈": {
        "aliases": ["低軌", "衛星", "AST SpaceMobile", "ASTS", "SpaceX", "昇達科"],
        "tags": ["低軌衛星", "通訊", "供應鏈"],
        "summary": "這個概念整理低軌衛星、衛星通訊與相關供應鏈的投資觀察。",
    },
    "台積電資本支出與設備鏈": {
        "aliases": ["台積電設備", "資本支出", "設備股", "辛耘", "翔名", "旺矽"],
        "tags": ["台積電", "資本支出", "設備鏈"],
        "summary": "這個概念整理台積電資本支出、設備需求與延伸設備鏈的觀察。",
    },
    "合約負債與訂單能見度": {
        "aliases": ["合約負債", "訂單能見度"],
        "tags": ["財務指標", "訂單"],
        "summary": "這個概念整理以合約負債與訂單能見度評估產業需求的觀察。",
    },
    "ETF 資產配置與槓桿策略": {
        "aliases": ["ETF", "0050", "正二", "高股息", "資產配置", "主動式ETF", "00631L", "0050L"],
        "tags": ["ETF", "資產配置", "槓桿"],
        "summary": "這個概念整理 ETF、資產配置、高股息與槓桿策略的觀察。",
    },
    "台股反彈與風險管理": {
        "aliases": ["反彈", "節後", "安心抱", "搶反彈", "不敢買", "不敢追", "先蹲跳更高"],
        "tags": ["台股", "反彈", "風險管理"],
        "summary": "這個概念整理台股反彈行情中的風險控管、節奏判斷與操作框架。",
    },
    "市場輪動與資金風向": {
        "aliases": ["輪動", "外資", "籌碼", "資金", "美元", "費半", "那斯達克", "道瓊"],
        "tags": ["市場輪動", "資金流向", "總體"],
        "summary": "這個概念整理市場輪動、外資籌碼與資金風向的觀察。",
    },
    "事件後應對投資法": {
        "aliases": ["處理", "不要預測", "最低點", "事件發生後", "不預判"],
        "tags": ["投資策略", "方法論", "風險管理"],
        "summary": "這個概念整理不要過度預測、而是強調事件發生後如何應對的投資方法。",
    },
}

FALLBACK_CONCEPTS = {
    "strategy": ["事件後應對投資法"],
    "macro": ["市場輪動與資金風向"],
    "sector": [],
    "stock": [],
    "personal": [],
}

ENTITY_CATALOG = {
    "Gooaye 股癌": {
        "aliases": ["Gooaye 股癌", "股癌"],
        "tags": ["節目", "Podcast", "來源"],
        "summary": "這是目前 wiki 中收錄的 Podcast 來源之一，內容偏向市場觀察、個股與交易心法。",
    },
    "理財達人秀 EBCmoneyshow": {
        "aliases": ["理財達人秀 EBCmoneyshow", "理財達人秀"],
        "tags": ["節目", "財經節目", "來源"],
        "summary": "這是目前 wiki 中收錄的電視財經節目來源，內容常聚焦台股題材、族群輪動與短中線操作。",
    },
    "兆華艾綸說": {
        "aliases": ["兆華艾綸說"],
        "tags": ["節目", "財經節目", "來源"],
        "summary": "這是理財達人秀系列中的主題節目，內容聚焦市場事件、題材輪動與資產配置討論。",
    },
    "川普": {
        "aliases": ["川普", "Trump"],
        "tags": ["人物", "政治"],
        "summary": "這是在目前來源中高頻出現的政治人物，相關言論經常影響關稅、伊朗與市場風險情緒。",
    },
    "黃仁勳": {
        "aliases": ["黃仁勳", "Jensen Huang"],
        "tags": ["人物", "AI", "半導體"],
        "summary": "這是在目前來源中代表 AI 與 NVIDIA 敘事的重要人物。",
    },
    "李兆華": {"aliases": ["李兆華"], "tags": ["人物", "主持人"], "summary": "這是在目前來源中反覆出現的主持人與市場討論者。"},
    "朱家泓": {"aliases": ["朱家泓"], "tags": ["人物", "來賓"], "summary": "這是在目前來源中反覆出現的市場來賓。"},
    "王建文": {"aliases": ["王建文"], "tags": ["人物", "來賓"], "summary": "這是在目前來源中反覆出現的市場來賓。"},
    "黃豐凱": {"aliases": ["黃豐凱"], "tags": ["人物", "來賓"], "summary": "這是在目前來源中反覆出現的市場來賓。"},
    "陳唯泰": {"aliases": ["陳唯泰"], "tags": ["人物", "來賓"], "summary": "這是在目前來源中反覆出現的市場來賓。"},
    "陳威良": {"aliases": ["陳威良"], "tags": ["人物", "來賓"], "summary": "這是在目前來源中反覆出現的市場來賓。"},
    "紀緯明": {"aliases": ["紀緯明"], "tags": ["人物", "來賓"], "summary": "這是在目前來源中反覆出現的市場來賓。"},
    "曲建仲": {"aliases": ["曲建仲", "曲博"], "tags": ["人物", "來賓"], "summary": "這是在目前來源中反覆出現的技術分析與科技產業來賓。"},
    "艾綸": {"aliases": ["艾綸"], "tags": ["人物", "來賓"], "summary": "這是在目前來源中反覆出現的市場來賓。"},
    "股魚": {"aliases": ["股魚"], "tags": ["人物", "來賓"], "summary": "這是在目前來源中反覆出現的市場來賓。"},
    "CPO": {"aliases": ["CPO"], "tags": ["技術", "光通訊"], "summary": "這是在目前來源中高頻出現的技術關鍵字，通常與 AI 網通和光通訊投資主線相關。"},
    "CoWoS": {"aliases": ["CoWoS"], "tags": ["技術", "先進封裝"], "summary": "這是在目前來源中高頻出現的先進封裝技術節點，通常與 AI 晶片產能與瓶頸相關。"},
    "HBM": {"aliases": ["HBM"], "tags": ["技術", "記憶體"], "summary": "這是在目前來源中高頻出現的高頻寬記憶體技術節點。"},
    "PCB": {"aliases": ["PCB"], "tags": ["技術", "供應鏈"], "summary": "這是在目前來源中高頻出現的供應鏈技術關鍵字。"},
    "低軌衛星": {"aliases": ["低軌", "低軌衛星"], "tags": ["技術", "通訊"], "summary": "這是在目前來源中高頻出現的衛星通訊題材。"},
    "矽光子": {"aliases": ["矽光子", "矽光"], "tags": ["技術", "光通訊"], "summary": "這是在目前來源中高頻出現的光通訊與 AI 網通技術關鍵字。"},
    "川普關稅": {"aliases": ["川普關稅", "關稅戰", "對等關稅"], "tags": ["事件", "關稅"], "summary": "這是在目前來源中反覆出現的事件型節點，常被用來討論市場風險與資金配置。"},
    "美伊衝突": {"aliases": ["美伊", "伊朗", "石器時代"], "tags": ["事件", "地緣政治"], "summary": "這是在目前來源中高頻出現的地緣政治事件節點。"},
    "荷姆茲海峽": {"aliases": ["荷姆茲海峽"], "tags": ["事件", "地緣政治"], "summary": "這是在目前來源中與油價、戰爭與風險情緒相連的地緣政治節點。"},
}

STOP_NAME_PREFIXES = (
    "並指出",
    "主持人提及",
    "主持人認為",
    "講者澄清",
    "他以",
    "若",
    "包括",
    "近期",
    "但",
    "和",
    "與",
    "是因為",
    "旗下的",
    "建議關注",
    "儘管",
    "而",
    "可留意其合作夥伴",
    "概念股中的",
)

BAD_NAME_SUBSTRINGS = (
    "主持人",
    "講者",
    "外資",
    "概念股",
    "族群",
    "本週",
    "近期",
    "包括",
    "以及",
    "和",
    "與",
    "如",
    "的",
    "給予",
    "模組廠",
    "供應商",
)

TICKER_NAME_RE = re.compile(r"([A-Za-z\u4e00-\u9fff0-9・\-]{2,20})[（(]([0-9A-Z.]{3,12})[）)]")
PARTICIPANT_RE = re.compile(r"[\u4e00-\u9fff]{2,4}|股魚|艾綸")


def parse_frontmatter(text: str) -> dict[str, object]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}

    data: dict[str, object] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        value = raw_value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip() for item in value[1:-1].split(",") if item.strip()]
            data[key.strip()] = items
        else:
            data[key.strip()] = value
    return data


def strip_frontmatter(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return text
    return text[match.end():]


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def truncate(text: str, limit: int = 180) -> str:
    text = normalize_space(text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def sanitize_filename(name: str) -> str:
    return name.replace("/", "／").replace(":", "：")


def read_existing_sources(root_dir: Path) -> set[str]:
    sources: set[str] = set()
    for path in (root_dir / WIKI_DIRNAME).rglob("*.md"):
        if path.name in {"index.md", "log.md"}:
            continue
        frontmatter = parse_frontmatter(path.read_text())
        for source in frontmatter.get("sources", []):
            if isinstance(source, str):
                sources.add(source)
    return sources


def discover_pending_raw_files(root_dir: Path, processed: set[str] | None = None) -> list[Path]:
    processed = processed if processed is not None else read_existing_sources(root_dir)
    pending = []
    for path in sorted((root_dir / "raw").glob("*.json")):
        if path.name in SOURCE_SKIP or path.name in processed:
            continue
        pending.append(path)
    return pending


def clean_ticker_name(name: str) -> str:
    cleaned = name.strip(" -｜|：:")
    for prefix in STOP_NAME_PREFIXES:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix) :].strip(" -｜|：:")
    if len(cleaned) < 2:
        return ""
    if any(token in cleaned for token in BAD_NAME_SUBSTRINGS):
        return ""
    if re.fullmatch(r"[\u4e00-\u9fff]+", cleaned) and len(cleaned) > 5:
        return ""
    return cleaned


def extract_ticker_name_map(text: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for name, ticker in TICKER_NAME_RE.findall(text):
        cleaned = clean_ticker_name(name)
        if cleaned:
            mapping.setdefault(ticker, cleaned)
    return mapping


def infer_entity_from_ticker(ticker: str, text: str) -> str:
    if ticker in TICKER_OVERRIDES:
        return TICKER_OVERRIDES[ticker]
    mapping = extract_ticker_name_map(text)
    if ticker in mapping:
        return mapping[ticker]
    return ticker


def extract_participants(title: str) -> set[str]:
    participants: set[str] = set()
    if "｜" not in title:
        return participants
    for segment in title.split("｜")[1:]:
        if any(token in segment for token in ("2026", "2025", "#")):
            segment = segment.split("202", 1)[0]
            segment = segment.split("#", 1)[0]
        for candidate in PARTICIPANT_RE.findall(segment):
            if candidate not in {"理財達人秀", "市場觀察"}:
                participants.add(candidate)
    return participants


def extract_entities_and_concepts(title: str, insight: dict[str, object]) -> tuple[set[str], set[str]]:
    content = str(insight.get("content", ""))
    key_points = " ".join(str(point) for point in insight.get("key_points", []) or [])
    combined = f"{title} {content} {key_points}"

    entities = set(extract_participants(title))
    concepts: set[str] = set()

    podcast_match = re.search(r"【([^】]+)】", title)
    if podcast_match:
        label = podcast_match.group(1)
        if label == "兆華艾綸說":
            entities.add("兆華艾綸說")

    for ticker in insight.get("tickers", []) or []:
        entities.add(infer_entity_from_ticker(str(ticker), combined))

    for title_name, meta in ENTITY_CATALOG.items():
        if any(alias in combined for alias in meta["aliases"]):
            entities.add(title_name)

    for concept_name, meta in CONCEPT_CATALOG.items():
        if any(alias in combined for alias in meta["aliases"]):
            concepts.add(concept_name)

    for concept_name in FALLBACK_CONCEPTS.get(str(insight.get("type", "")), []):
        concepts.add(concept_name)

    return entities, concepts


def build_source_record(file_name: str, payload: dict[str, object]) -> dict[str, object]:
    insights = payload.get("insights", []) or []
    first_content = ""
    if insights and isinstance(insights[0], dict):
        first_content = str(insights[0].get("content", ""))
    summary = truncate(
        "｜".join(
            filter(
                None,
                [
                    str(payload.get("episode", "")).strip(),
                    str(payload.get("podcast_name", "")).strip(),
                    str(payload.get("date", "")).strip(),
                    first_content.strip(),
                ],
            )
        ),
        limit=320,
    )
    return {
        "title": SOURCE_TITLE_OVERRIDES.get(file_name, str(payload.get("episode", file_name)).strip()),
        "podcast_name": str(payload.get("podcast_name", "")).strip(),
        "date": str(payload.get("date", TODAY)).strip(),
        "summary": summary,
        "sources": [file_name],
    }


def format_frontmatter(data: dict[str, object]) -> str:
    lines = ["---"]
    for key in ("title", "type", "tags", "created", "updated", "sources"):
        value = data[key]
        if isinstance(value, list):
            formatted = ", ".join(str(item) for item in value)
            lines.append(f"{key}: [{formatted}]")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def build_source_filename(file_name: str) -> str:
    return sanitize_filename(Path(file_name).stem) + ".md"


def get_page_path(root_dir: Path, page_type: str, title: str, source_file: str | None = None) -> Path:
    if page_type == "source" and source_file:
        return root_dir / WIKI_DIRNAME / "sources" / build_source_filename(source_file)
    folder_map = {
        "concept": "concepts",
        "entity": "entities",
        "source": "sources",
        "synthesis": "synthesis",
    }
    folder = folder_map.get(page_type, page_type + "s") if page_type != "overview" else ""
    if page_type == "overview":
        return root_dir / WIKI_DIRNAME / "overview.md"
    return root_dir / WIKI_DIRNAME / folder / f"{sanitize_filename(title)}.md"


def strip_auto_sections(body: str) -> str:
    body = AUTO_BLOCK_RE.sub("\n", body)
    body = RELATED_RE.sub("", body)
    return body.strip()


def read_existing_page(path: Path) -> tuple[dict[str, object], str]:
    if not path.exists():
        return {}, ""
    text = path.read_text()
    frontmatter = parse_frontmatter(text)
    body = strip_frontmatter(text)
    return frontmatter, strip_auto_sections(body)


def ensure_heading(body: str, title: str) -> str:
    stripped = body.strip()
    if not stripped:
        return f"# {title}"
    if stripped.startswith("# "):
        return stripped
    return f"# {title}\n\n{stripped}"


def merge_lists(existing: list[str] | object, new_items: list[str]) -> list[str]:
    merged = []
    for item in list(existing or []) + new_items:
        text = str(item).strip()
        if text and text not in merged:
            merged.append(text)
    return merged


def build_related_section(related_titles: list[str]) -> str:
    unique = []
    for title in related_titles:
        if title and title not in unique:
            unique.append(title)
    lines = ["## 相關頁面"]
    for title in unique[:18]:
        lines.append(f"- [[{title}]]")
    return "\n".join(lines)


def build_auto_block(title: str, notes: list[str], related_titles: list[str]) -> str:
    lines = ["<!-- AUTO-INGEST START -->", "## 來源補充"]
    if notes:
        lines.extend(f"- {note}" for note in notes[:18])
    else:
        lines.append("- 目前尚無自動補充內容。")
    lines.append("")
    lines.append(build_related_section(related_titles))
    lines.append("<!-- AUTO-INGEST END -->")
    return "\n".join(lines)


def infer_entity_summary(title: str, tags: list[str], notes: list[str]) -> str:
    if title in ENTITY_CATALOG:
        return ENTITY_CATALOG[title]["summary"]
    if "人物" in tags:
        return f"這是在目前來源中出現的人物節點，與「{title}」相關的觀點會持續整理在此頁。"
    if "技術" in tags:
        return f"這是在目前來源中反覆出現的技術節點，與「{title}」相關的觀點會持續整理在此頁。"
    if "事件" in tags:
        return f"這是在目前來源中反覆出現的事件節點，與「{title}」相關的觀點會持續整理在此頁。"
    if notes:
        return f"這是在目前來源中反覆被提及的實體節點。{normalize_space(notes[0].split('：', 1)[-1])}"
    return f"這是在目前來源中反覆被提及的實體節點，與「{title}」相關的觀點會持續整理在此頁。"


def infer_concept_summary(title: str, notes: list[str]) -> str:
    if title in CONCEPT_CATALOG:
        return CONCEPT_CATALOG[title]["summary"]
    if notes:
        return f"這個概念整理目前來源中與「{title}」相關的觀察。{normalize_space(notes[0].split('：', 1)[-1])}"
    return f"這個概念整理目前來源中與「{title}」相關的觀察。"


def write_page(
    path: Path,
    page_type: str,
    title: str,
    tags: list[str],
    sources: list[str],
    manual_intro: str,
    notes: list[str],
    related_titles: list[str],
) -> None:
    existing_frontmatter, existing_body = read_existing_page(path)
    created = str(existing_frontmatter.get("created", TODAY))
    merged_tags = merge_lists(existing_frontmatter.get("tags", []), tags)
    merged_sources = merge_lists(existing_frontmatter.get("sources", []), sources)

    manual_body = existing_body if existing_body else ensure_heading(manual_intro, title)
    content = "\n\n".join(
        [
            format_frontmatter(
                {
                    "title": title,
                    "type": page_type,
                    "tags": merged_tags,
                    "created": created,
                    "updated": TODAY,
                    "sources": merged_sources,
                }
            ),
            manual_body.strip(),
            build_auto_block(title, notes, related_titles),
        ]
    ).strip() + "\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def render_source_page(record: dict[str, object]) -> str:
    title = str(record["title"])
    concepts = list(record["concepts"])
    entities = list(record["entities"])
    bullets = list(record["bullets"])
    lines = [
        format_frontmatter(
            {
                "title": title,
                "type": "source",
                "tags": merge_lists([], list(record["tags"])),
                "created": TODAY,
                "updated": TODAY,
                "sources": list(record["sources"]),
            }
        ),
        f"# {title}",
        "",
        str(record["summary"]),
        "",
        "## 文件重點",
    ]
    lines.extend(f"- {bullet}" for bullet in bullets[:8])
    lines.extend(["", "## 核心概念"])
    lines.extend(f"- [[{name}]]" for name in concepts[:10])
    lines.extend(["", "## 核心實體"])
    lines.extend(f"- [[{name}]]" for name in entities[:12])
    lines.extend(["", build_related_section(concepts[:8] + entities[:8])])
    return "\n".join(lines).strip() + "\n"


def build_source_output(file_name: str, payload: dict[str, object]) -> tuple[dict[str, object], dict[str, list[str]], dict[str, list[str]]]:
    source = build_source_record(file_name, payload)
    title = str(source["title"])
    podcast_name = str(source["podcast_name"])
    concepts: set[str] = set()
    entities: set[str] = {podcast_name} if podcast_name else set()
    entities |= extract_participants(title)
    if podcast_name in {"理財達人秀 EBCmoneyshow", "Gooaye 股癌"}:
        entities.add(podcast_name)
    if "兆華艾綸說" in title:
        entities.add("兆華艾綸說")

    bullets: list[str] = []
    concept_notes: dict[str, list[str]] = defaultdict(list)
    entity_notes: dict[str, list[str]] = defaultdict(list)

    for insight in payload.get("insights", []) or []:
        if not isinstance(insight, dict):
            continue
        matched_entities, matched_concepts = extract_entities_and_concepts(title, insight)
        entities |= matched_entities
        concepts |= matched_concepts
        insight_summary = truncate(str(insight.get("content", "")), limit=150)

        concept_links = "、".join(f"[[{name}]]" for name in sorted(matched_concepts)[:3])
        entity_links = "、".join(f"[[{name}]]" for name in sorted(matched_entities)[:3])
        bullet_parts = [insight_summary]
        if concept_links:
            bullet_parts.append(f"概念：{concept_links}")
        if entity_links:
            bullet_parts.append(f"實體：{entity_links}")
        bullets.append("｜".join(part for part in bullet_parts if part))

        for concept in matched_concepts:
            note = f"[[{title}]]：{insight_summary}"
            if note not in concept_notes[concept]:
                concept_notes[concept].append(note)
        for entity in matched_entities:
            note = f"[[{title}]]：{insight_summary}"
            if note not in entity_notes[entity]:
                entity_notes[entity].append(note)

    source["concepts"] = sorted(concepts)
    source["entities"] = sorted(entities)
    source["bullets"] = bullets
    source["tags"] = merge_lists([], [podcast_name, "來源摘要"] + sorted(list(concepts))[:3])
    return source, concept_notes, entity_notes


def build_index_entry(path: Path) -> tuple[str, str, list[str], str]:
    frontmatter = parse_frontmatter(path.read_text())
    title = str(frontmatter.get("title", path.stem))
    page_type = str(frontmatter.get("type", path.parent.name.rstrip("s")))
    sources = [str(item) for item in frontmatter.get("sources", [])]
    summary = graph_builder.extract_markdown_summary(path.read_text())
    return title, page_type, sources, summary


def collect_unique_page_paths(wiki_dir: Path) -> dict[str, Path]:
    candidates = [wiki_dir / "overview.md"]
    for folder in ("concepts", "entities", "sources", "synthesis"):
        candidates.extend(sorted((wiki_dir / folder).glob("*.md")))

    chosen: dict[str, Path] = {}
    for path in candidates:
        if not path.exists():
            continue
        title = str(parse_frontmatter(path.read_text()).get("title", path.stem))
        existing = chosen.get(title)
        if existing is None or len(path.name) < len(existing.name):
            chosen[title] = path
    return chosen


def rebuild_index(root_dir: Path) -> None:
    wiki_dir = root_dir / WIKI_DIRNAME
    buckets: dict[str, list[tuple[str, list[str], str]]] = defaultdict(list)
    page_count = 0

    for path in collect_unique_page_paths(wiki_dir).values():
        title, page_type, sources, summary = build_index_entry(path)
        if page_type == "overview":
            buckets["overview"].append((title, sources, summary))
        else:
            buckets[page_type].append((title, sources, summary))
        page_count += 1

    lines = ["# Wiki Index", "", f"最後更新：{TODAY}｜共 {page_count} 頁", "", "## 總覽（overview）", ""]
    for title, sources, summary in buckets.get("overview", []):
        lines.append(f"- [[{title}]] — {truncate(summary, 40)}")

    section_map = [
        ("concept", "概念（concepts/）"),
        ("entity", "實體（entities/）"),
        ("source", "文件摘要（sources/）"),
        ("synthesis", "分析與洞察（synthesis/）"),
    ]
    for key, header in section_map:
        lines.extend(["", f"## {header}", ""])
        items = sorted(buckets.get(key, []), key=lambda item: item[0])
        if not items:
            lines.append("（尚無頁面）")
            continue
        for title, sources, summary in items:
            if key == "source":
                lines.append(f"- [[{title}]] — {TODAY} ingest")
            elif key == "synthesis":
                lines.append(f"- [[{title}]] — {TODAY}，來自 batch ingest")
            elif key == "concept":
                lines.append(f"- [[{title}]] — {truncate(summary, 38)}（來自 {len(sources)} 份來源）")
            else:
                lines.append(f"- [[{title}]] — {truncate(summary, 38)}")

    (wiki_dir / "index.md").write_text("\n".join(lines).strip() + "\n")


def rebuild_overview(root_dir: Path) -> None:
    wiki_dir = root_dir / WIKI_DIRNAME
    unique_pages = collect_unique_page_paths(wiki_dir)
    source_pages = [path for path in unique_pages.values() if parse_frontmatter(path.read_text()).get("type") == "source"]
    concept_pages = [path for path in unique_pages.values() if parse_frontmatter(path.read_text()).get("type") == "concept"]
    entity_pages = [path for path in unique_pages.values() if parse_frontmatter(path.read_text()).get("type") == "entity"]
    synthesis_pages = [path for path in unique_pages.values() if parse_frontmatter(path.read_text()).get("type") == "synthesis"]
    pending = discover_pending_raw_files(root_dir)

    lines = [
        format_frontmatter(
            {
                "title": "整體知識摘要",
                "type": "overview",
                "tags": ["總覽"],
                "created": TODAY,
                "updated": TODAY,
                "sources": [],
            }
        ),
        "# 整體知識摘要",
        "",
        f"本 wiki 已批量整理來源，目前完成 {len(source_pages)} 份來源摘要、{len(concept_pages)} 個概念頁、{len(entity_pages)} 個實體頁與 {len(synthesis_pages)} 個 synthesis 頁。",
        "",
        "## 目前狀態",
        "",
        f"- `raw/` 尚未處理檔案：{len(pending)} 份",
        f"- 主要概念焦點：{ '、'.join(f'[[{parse_frontmatter(path.read_text()).get('title', path.stem)}]]' for path in concept_pages[:10]) }",
        f"- 主要來源節目：[[Gooaye 股癌]]、[[理財達人秀 EBCmoneyshow]]、[[游庭皓的財經皓角]]",
        "",
        build_related_section(
            [parse_frontmatter(path.read_text()).get("title", path.stem) for path in synthesis_pages[:3]]
            + [parse_frontmatter(path.read_text()).get("title", path.stem) for path in source_pages[:6]]
        ),
    ]
    (wiki_dir / "overview.md").write_text("\n".join(lines).strip() + "\n")


def append_log_entries(root_dir: Path, log_entries: list[str]) -> None:
    log_path = root_dir / WIKI_DIRNAME / "log.md"
    existing = log_path.read_text() if log_path.exists() else "# Wiki Log\n"
    existing_headers = set(re.findall(r"^## \[[^\]]+\] .+$", existing, re.MULTILINE))
    filtered_entries = []
    for entry in log_entries:
        stripped = entry.strip()
        if not stripped:
            continue
        header = stripped.splitlines()[0]
        if header in existing_headers:
            continue
        filtered_entries.append(stripped)
    if not filtered_entries:
        return
    append_text = "\n\n".join(filtered_entries)
    log_path.write_text(existing.rstrip() + "\n\n" + append_text.strip() + "\n")


def create_synthesis_pages(root_dir: Path, source_records: list[dict[str, object]]) -> list[str]:
    wiki_dir = root_dir / WIKI_DIRNAME
    source_titles = [record["title"] for record in source_records]

    pages = {
        "AI供應鏈投資脈絡": {
            "tags": ["AI", "半導體", "供應鏈", "synthesis"],
            "sources": sorted(
                {
                    source
                    for path in (wiki_dir / "concepts").glob("*.md")
                    if parse_frontmatter(path.read_text()).get("title") in {
                        "AI 驅動的台灣產業升級",
                        "CPO 與矽光子",
                        "先進封裝與封測供應鏈",
                        "記憶體與 HBM 週期",
                        "台積電資本支出與設備鏈",
                        "PCB 與 CCL 供應鏈",
                    }
                    for source in parse_frontmatter(path.read_text()).get("sources", [])
                }
            ),
            "body": [
                "# AI供應鏈投資脈絡",
                "",
                "這頁把目前 wiki 中與 AI 供應鏈相關的概念串成一條脈絡，從需求端、晶片與先進封裝，到光通訊、PCB、記憶體與設備鏈。",
                "",
                "## 核心鏈條",
                "",
                "- 需求起點：[[AI 驅動的台灣產業升級]]",
                "- 算力與平台：[[Agentic AI 與 CPU 投資主線]]、[[NVIDIA]]、[[台積電]]",
                "- 產能瓶頸：[[先進封裝與封測供應鏈]]、[[CoWoS]]",
                "- 高速互連：[[CPO 與矽光子]]、[[矽光子]]",
                "- 板材與基板：[[PCB 與 CCL 供應鏈]]、[[PCB]]",
                "- 記憶體支撐：[[記憶體與 HBM 週期]]、[[HBM]]",
                "- 資本支出外溢：[[台積電資本支出與設備鏈]]",
                "",
                "## 關鍵觀察",
                "",
                "- 多個來源都把 [[台積電]] 放在供應鏈核心位置，差別在於各自更看重封裝、設備、記憶體還是網通。",
                "- [[CPO]]、[[CoWoS]]、[[HBM]] 與 [[PCB]] 常一起出現，代表市場已經從單一 AI 晶片敘事走向整體基礎設施敘事。",
                "- 部分節目強調題材仍未走完，另一些節目則提醒評價、節奏與地緣政治風險，這些分歧會直接影響進場方式。",
                "",
                build_related_section(
                    [
                        "AI 驅動的台灣產業升級",
                        "CPO 與矽光子",
                        "先進封裝與封測供應鏈",
                        "記憶體與 HBM 週期",
                        "PCB 與 CCL 供應鏈",
                        "台積電資本支出與設備鏈",
                    ]
                    + source_titles[:8]
                ),
            ],
        },
        "2026Q1市場共識與分歧": {
            "tags": ["市場共識", "Podcast", "synthesis"],
            "sources": sorted({source for record in source_records for source in record["sources"]}),
            "body": [
                "# 2026Q1市場共識與分歧",
                "",
                "這頁綜合 2026 年第一季目前已整理的 Podcast 與節目來源，整理彼此之間的共識與分歧。",
                "",
                "## 市場共識",
                "",
                "- AI 供應鏈仍是 2026Q1 最強主線，尤其是 [[台積電]]、[[CPO]]、[[CoWoS]]、[[HBM]] 與 [[PCB]]。",
                "- 地緣政治與 [[川普關稅]] 是短期市場波動的重要來源，投資上需要更重視節奏與風險管理。",
                "- 多數節目都不鼓勵盲目追價或預設最低點，而是強調 [[事件後應對投資法]] 與部位管理。",
                "",
                "## 市場分歧",
                "",
                "- 有些來源認為台股與 AI 題材仍有反彈空間，另一些來源則偏向先看籌碼與外部事件落地。",
                "- 對 [[ETF 資產配置與槓桿策略]] 的態度不同，有人強調正二可納入長期配置，也有人主張只適合條件明確時使用。",
                "- 對各族群節奏也有差異：有的來源偏好 [[CPO 與矽光子]]，有的偏好 [[記憶體與 HBM 週期]] 或 [[低軌衛星與通訊供應鏈]]。",
                "",
                build_related_section(
                    [
                        "AI 驅動的台灣產業升級",
                        "地緣政治與市場波動",
                        "ETF 資產配置與槓桿策略",
                        "台股反彈與風險管理",
                    ]
                    + source_titles[:10]
                ),
            ],
        },
        "交易心法彙整": {
            "tags": ["交易心法", "strategy", "synthesis"],
            "sources": sorted({source for record in source_records for source in record["sources"]}),
            "body": [
                "# 交易心法彙整",
                "",
                "這頁把目前來源中 `strategy` 類型的觀點做去重與合併，保留可重複使用的操作框架。",
                "",
                "## 核心心法",
                "",
                "- 先處理、後預測：[[事件後應對投資法]] 仍是目前最穩定的共識。",
                "- 題材再強也要分辨節奏：[[台股反彈與風險管理]] 強調反彈不等於全面追價。",
                "- 供需比故事重要：不論個股還是產業，最後仍要回到訂單、產能、價格與籌碼。",
                "- 風險要配工具：當波動加大時，ETF、現金比重與槓桿工具使用方式比單純方向判斷更重要。",
                "",
                "## 常見分歧",
                "",
                "- 是否可以長期持有正二",
                "- 反彈盤應該分批佈局還是等待確認",
                "- 地緣政治利空該視為短空還是趨勢反轉",
                "",
                build_related_section(
                    [
                        "事件後應對投資法",
                        "ETF 資產配置與槓桿策略",
                        "台股反彈與風險管理",
                        "市場輪動與資金風向",
                    ]
                    + source_titles[:10]
                ),
            ],
        },
    }

    log_entries = []
    for title, data in pages.items():
        path = wiki_dir / "synthesis" / f"{sanitize_filename(title)}.md"
        text = "\n".join(
            [
                format_frontmatter(
                    {
                        "title": title,
                        "type": "synthesis",
                        "tags": data["tags"],
                        "created": TODAY,
                        "updated": TODAY,
                        "sources": data["sources"],
                    }
                )
            ]
            + data["body"]
        ).strip() + "\n"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        log_entries.append(
            "\n".join(
                [
                    f"## [{TODAY}] synthesis | {title}",
                    f"- 新增 wiki/synthesis/{sanitize_filename(title)}.md",
                    f"- 串聯 {len(data['sources'])} 份來源，整理跨節目觀點",
                ]
            )
        )
    return log_entries


def main() -> None:
    root_dir = Path(__file__).parent.parent
    pending_files = discover_pending_raw_files(root_dir)
    target_files = pending_files or sorted(
        path for path in (root_dir / "raw").glob("*.json") if path.name not in SOURCE_SKIP
    )
    wiki_dir = root_dir / WIKI_DIRNAME

    source_records: list[dict[str, object]] = []
    concept_agg: dict[str, dict[str, object]] = defaultdict(lambda: {"sources": set(), "tags": set(), "notes": [], "related": set()})
    entity_agg: dict[str, dict[str, object]] = defaultdict(lambda: {"sources": set(), "tags": set(), "notes": [], "related": set()})
    log_entries: list[str] = []

    for raw_path in target_files:
        payload = json.loads(raw_path.read_text())
        source_record, concept_notes, entity_notes = build_source_output(raw_path.name, payload)
        source_records.append(source_record)

        source_path = get_page_path(root_dir, "source", str(source_record["title"]), raw_path.name)
        source_path.write_text(render_source_page(source_record))

        for concept, notes in concept_notes.items():
            concept_agg[concept]["sources"].add(raw_path.name)
            concept_agg[concept]["tags"].update(CONCEPT_CATALOG.get(concept, {}).get("tags", ["概念"]))
            concept_agg[concept]["notes"].extend(note for note in notes if note not in concept_agg[concept]["notes"])
            concept_agg[concept]["related"].update(source_record["entities"])
            concept_agg[concept]["related"].add(source_record["title"])

        for entity, notes in entity_notes.items():
            entity_agg[entity]["sources"].add(raw_path.name)
            if entity in ENTITY_CATALOG:
                entity_agg[entity]["tags"].update(ENTITY_CATALOG[entity]["tags"])
            elif entity.endswith(".TW") or entity.endswith(".US") or entity.isupper():
                entity_agg[entity]["tags"].update(["公司", "股票代號"])
            else:
                entity_agg[entity]["tags"].update(["公司", "標的"])
            entity_agg[entity]["notes"].extend(note for note in notes if note not in entity_agg[entity]["notes"])
            entity_agg[entity]["related"].update(source_record["concepts"])
            entity_agg[entity]["related"].add(source_record["title"])

        concept_pages = sorted(source_record["concepts"])[:6]
        entity_pages = sorted(source_record["entities"])[:8]
        log_entries.append(
            "\n".join(
                [
                    f"## [{TODAY}] ingest | {source_record['title']}",
                    f"- 新增 sources/{source_path.name}",
                    f"- 更新概念頁：{ '、'.join(f'[[{name}]]' for name in concept_pages) if concept_pages else '無' }",
                    f"- 更新實體頁：{ '、'.join(f'[[{name}]]' for name in entity_pages) if entity_pages else '無' }",
                ]
            )
        )

    for title, data in concept_agg.items():
        path = get_page_path(root_dir, "concept", title)
        intro = "\n\n".join([f"# {title}", "", infer_concept_summary(title, data["notes"])])
        related = sorted(set(data["related"]) | {"整體知識摘要"})
        write_page(
            path=path,
            page_type="concept",
            title=title,
            tags=sorted(data["tags"]) or ["概念"],
            sources=sorted(data["sources"]),
            manual_intro=intro,
            notes=data["notes"],
            related_titles=related,
        )

    for title, data in entity_agg.items():
        path = get_page_path(root_dir, "entity", title)
        tags = sorted(data["tags"]) or ["實體"]
        intro = "\n\n".join([f"# {title}", "", infer_entity_summary(title, tags, data["notes"])])
        related = sorted(set(data["related"]) | {"整體知識摘要"})
        write_page(
            path=path,
            page_type="entity",
            title=title,
            tags=tags,
            sources=sorted(data["sources"]),
            manual_intro=intro,
            notes=data["notes"],
            related_titles=related,
        )

    synthesis_log_entries = create_synthesis_pages(root_dir, source_records)
    log_entries.extend(synthesis_log_entries)
    rebuild_overview(root_dir)
    rebuild_index(root_dir)
    append_log_entries(root_dir, log_entries)

    print(f"processed {len(target_files)} raw files")
    print(f"created_or_updated_sources {len(source_records)}")
    print(f"created_or_updated_concepts {len(concept_agg)}")
    print(f"created_or_updated_entities {len(entity_agg)}")
    print(f"synthesis_pages 3")


if __name__ == "__main__":
    main()
