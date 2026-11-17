#!/usr/bin/env python3
"""Export schemaVersion 1 diagram layouts as individually editable PPTX objects.

Requires python-pptx. No browser, model API, raster image, or cloud service is used.
Coordinates and input font sizes are SVG pixels; one uniform geometry transform
per page converts them to points. Font sizes in the report are the explicit
DrawingML font sizes, not estimates of a viewer's substituted font metrics.
"""

import argparse
import json
import math
from pathlib import Path
import re
import sys
import tempfile
import unicodedata

try:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
    from pptx.oxml.xmlchemy import OxmlElement
    from pptx.util import Inches, Pt
except ImportError as exc:
    raise SystemExit("native_pptx requires python-pptx; install it in the Python environment running this script.") from exc


class LayoutError(ValueError):
    """An unsupported or unreadable layout; no output should be committed."""


SIZES = {"landscape": (40 / 3, 7.5), "portrait": (10, 40 / 3)}
MARGIN = 28.8  # points, 0.4 inch
KINDS = {"rect": MSO_SHAPE.RECTANGLE, "roundRect": MSO_SHAPE.ROUNDED_RECTANGLE,
         "ellipse": MSO_SHAPE.OVAL, "diamond": MSO_SHAPE.DIAMOND}


def number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise LayoutError(f"{name} must be a finite number")
    if positive and value <= 0:
        raise LayoutError(f"{name} must be positive")
    return float(value)


def validate(layout, source):
    if not isinstance(layout, dict) or layout.get("schemaVersion") != 1:
        raise LayoutError(f"{source}: expected layout schemaVersion 1")
    if not isinstance(layout.get("title"), str):
        raise LayoutError(f"{source}: title must be text")
    for collection in ("nodes", "edges", "groups"):
        if not isinstance(layout.get(collection), list):
            raise LayoutError(f"{source}: {collection} must be an array")
    all_ids = set()
    for item in layout["nodes"] + layout["groups"]:
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in all_ids:
            raise LayoutError(f"{source}: node/group id is missing or duplicated: {identifier!r}")
        all_ids.add(identifier)
    groups = {g["id"]: g for g in layout["groups"]}
    for item in [layout.get("viewBox", {})] + layout["nodes"] + layout["groups"]:
        for key in ("x", "y", "width", "height"):
            number(item.get(key), f"{source}: {item.get('id', 'viewBox')}.{key}", key in ("width", "height"))
        if item.get("fontSize") is not None:
            number(item["fontSize"], "fontSize", True)
    for group in layout["groups"]:
        visited = {group["id"]}
        parent = group.get("parentId")
        while parent is not None:
            if parent not in groups:
                raise LayoutError(f"{source}: unknown parent group {parent}")
            if parent in visited:
                raise LayoutError(f"{source}: group hierarchy contains a cycle at {parent}")
            visited.add(parent)
            parent = groups[parent].get("parentId")
    for node in layout["nodes"]:
        if node.get("kind") not in {*KINDS, "polygon", "path"}:
            raise LayoutError(f"{source}: unsupported node kind {node.get('kind')!r}")
        if not isinstance(node.get("text"), str):
            raise LayoutError(f"{source}: node {node['id']} text must be a string")
        if not isinstance(node.get("groupIds", []), list):
            raise LayoutError(f"{source}: node {node['id']} groupIds must be an array")
        for group_id in node.get("groupIds", []):
            if group_id not in groups:
                raise LayoutError(f"{source}: node {node['id']} references unknown group {group_id}")
        if node["kind"] in ("polygon", "path"):
            validate_points(node.get("points"), f"{source}: node {node['id']}", 3)
    edge_ids = set()
    for edge in layout["edges"]:
        identifier = edge.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in edge_ids:
            raise LayoutError(f"{source}: missing or duplicate edge id {identifier!r}")
        edge_ids.add(identifier)
        for endpoint in ("source", "target"):
            if edge.get(endpoint) not in all_ids:
                raise LayoutError(f"{source}: edge {identifier} has unknown {endpoint} {edge.get(endpoint)!r}")
        validate_points(edge.get("points"), f"{source}: edge {identifier}", 2)
        if edge.get("label") is not None:
            label = edge["label"]
            if not isinstance(label.get("text"), str):
                raise LayoutError(f"{source}: edge {identifier} label text must be a string")
            for key in ("x", "y", "width", "height", "fontSize"):
                number(label.get(key), f"{source}: edge {identifier} label {key}", key in ("width", "height", "fontSize"))
    for item in layout["nodes"] + layout["groups"] + layout["edges"] + [e["label"] for e in layout["edges"] if e.get("label")]:
        for key in ("fill", "stroke", "color"):
            value = item.get(key)
            if value is not None and value != "transparent":
                try:
                    valid = len(value) == 7 and value.startswith("#") and int(value[1:], 16) >= 0
                except (ValueError, TypeError, AttributeError):
                    valid = False
                if not valid:
                    raise LayoutError(f"{source}: {key} must be #RRGGBB or transparent")
        if "strokeWidth" in item:
            number(item["strokeWidth"], "strokeWidth")
            if item["strokeWidth"] < 0:
                raise LayoutError(f"{source}: strokeWidth must not be negative")


def validate_points(points, description, minimum):
    if not isinstance(points, list) or len(points) < minimum:
        raise LayoutError(f"{description} needs at least {minimum} sampled points")
    for point in points:
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise LayoutError(f"{description} points must be [x, y] pairs")
        number(point[0], description + " point x")
        number(point[1], description + " point y")


def rect(item):
    return item["x"], item["y"], item["x"] + item["width"], item["y"] + item["height"]


def bounds(page, whole=False):
    layout = page["layout"]
    boxes = [rect(layout["viewBox"])] if whole else []
    boxes += [rect(item) for item in page["nodes"] + page["groups"]]
    for node in page["nodes"]:
        if node.get("points"):
            xs, ys = zip(*node["points"])
            boxes.append((min(xs), min(ys), max(xs), max(ys)))
    for edge in page["internalEdges"]:
        xs, ys = zip(*edge["points"])
        boxes.append((min(xs), min(ys), max(xs), max(ys)))
        if edge.get("label"):
            boxes.append(rect(edge["label"]))
    if not boxes:
        boxes = [rect(layout["viewBox"])]
    return min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)


def wrap_text(text, width_pt, size_pt):
    """Wrap without deleting text; conservative CJK/Latin width allowance."""
    capacity = max(1, (width_pt - 8) / size_pt)
    lines = []
    for paragraph in text.split("\n"):
        current, used = "", 0.0
        for token in re.findall(r"[A-Za-z0-9]+|.", paragraph):
            units = sum(1.05 if unicodedata.east_asian_width(char) in ("W", "F") else 0.66 for char in token)
            if units <= capacity:
                if current and used + units > capacity:
                    lines.append(current)
                    current, used = "", 0.0
                current += token
                used += units
            else:
                for char in token:
                    if current and used + 0.66 > capacity:
                        lines.append(current)
                        current, used = "", 0.0
                    current += char
                    used += 0.66
        lines.append(current)
    return "\n".join(lines)


def font_values(page):
    values = [n.get("fontSize", 16) for n in page["nodes"] if n["text"]]
    values += [g.get("fontSize", 16) for g in page["groups"] if g.get("title")]
    values += [e["label"].get("fontSize", 16) for e in page["internalEdges"] if e.get("label") and e["label"]["text"]]
    return values


def make_page(layout, source, input_index, nodes, groups, title, group_id=None, whole=False):
    entities = {item["id"] for item in nodes + groups}
    return {"layout": layout, "source": source, "inputIndex": input_index,
            "nodes": nodes, "groups": groups, "entities": entities,
            "title": title, "groupId": group_id, "whole": whole,
            "internalEdges": [e for e in layout["edges"] if e["source"] in entities and e["target"] in entities],
            "continuations": []}


def measure(page, size, min_font):
    width, height = (v * 72 for v in size)
    inner_width = width - 2 * MARGIN
    title_font = max(22, min_font)
    page["titleText"] = wrap_text(page["title"], inner_width, title_font)
    page["titleHeight"] = len(page["titleText"].split("\n")) * title_font * 1.25
    page["continuationHeight"] = 0
    for continuation in page["continuations"]:
        continuation["wrappedText"] = wrap_text(continuation["text"], inner_width - 12, min_font)
        continuation["height"] = len(continuation["wrappedText"].split("\n")) * min_font * 1.25 + 10
        page["continuationHeight"] += continuation["height"] + 5
    top = MARGIN + page["titleHeight"] + 10
    available = height - top - MARGIN - page["continuationHeight"]
    if page["continuations"]:
        available -= 10
    box = bounds(page, page["whole"])
    if available <= 0:
        page.update(scale=0, minimumFontPt=0, bounds=box)
        return
    scale = min(inner_width / max(1, box[2] - box[0]), available / max(1, box[3] - box[1]))
    page["bounds"] = box
    page["scale"] = scale
    page["origin"] = (MARGIN + (inner_width - (box[2] - box[0]) * scale) / 2,
                      top + (available - (box[3] - box[1]) * scale) / 2)
    fonts = [round(value * scale, 2) for value in font_values(page)]
    fonts.append(title_font)
    if page["continuations"]:
        fonts.append(min_font)
    page["minimumFontPt"] = min(fonts)


def plan_orientation(layouts, sources, mode, orientation, min_font):
    size = SIZES[orientation]
    pages, warnings = [], []
    for index, (layout, source) in enumerate(zip(layouts, sources)):
        whole = make_page(layout, source, index, layout["nodes"], layout["groups"], layout["title"], whole=True)
        measure(whole, size, min_font)
        split = mode == "groups" or (mode == "auto" and whole["minimumFontPt"] < min_font)
        roots = [g for g in layout["groups"] if g.get("parentId") is None]
        if not split or not roots:
            pages.append(whole)
            if mode == "groups" and not roots:
                warnings.append(f"{source}: no top-level groups; retained the complete diagram on one slide.")
            continue
        group_map = {g["id"]: g for g in layout["groups"]}

        def root_id(identifier):
            while group_map[identifier].get("parentId") is not None:
                identifier = group_map[identifier]["parentId"]
            return identifier

        assigned = set()
        for root in roots:
            groups = [g for g in layout["groups"] if root_id(g["id"]) == root["id"]]
            selected = {g["id"] for g in groups}
            nodes = [n for n in layout["nodes"] if selected.intersection(n.get("groupIds", []))]
            assigned.update(n["id"] for n in nodes)
            pages.append(make_page(layout, source, index, nodes, groups,
                                   layout["title"] + " — " + root.get("title", root["id"]), root["id"]))
        loose = [n for n in layout["nodes"] if n["id"] not in assigned]
        if loose:
            pages.append(make_page(layout, source, index, loose, [], layout["title"] + " — Ungrouped nodes"))
            warnings.append(f"{source}: ungrouped nodes preserved on an additional slide: " + ", ".join(n["id"] for n in loose))
    for number_, page in enumerate(pages, 1):
        page["number"] = number_
    for page in pages:
        layout = page["layout"]
        peers = [p for p in pages if p["inputIndex"] == page["inputIndex"]]
        names = {n["id"]: n["text"] for n in layout["nodes"]}
        names.update({g["id"]: g.get("title", g["id"]) for g in layout["groups"]})
        for edge in layout["edges"]:
            source_here, target_here = edge["source"] in page["entities"], edge["target"] in page["entities"]
            if source_here == target_here:
                continue
            other_endpoint = edge["target"] if source_here else edge["source"]
            related = [p["number"] for p in peers if p is not page and other_endpoint in p["entities"]]
            direction = "outgoing" if source_here else "incoming"
            label = edge["label"]["text"] if edge.get("label") else ""
            endpoint_text = lambda key: names.get(key) or key
            arrow = "↔" if edge.get("arrowStart") and edge.get("arrowEnd") else "←" if edge.get("arrowStart") else "→" if edge.get("arrowEnd") else "—"
            text = f"{'前往' if source_here else '承接'}第 " + "、".join(map(str, related)) + " 頁："
            text += f"{endpoint_text(edge['source'])} {arrow} {endpoint_text(edge['target'])}"
            if label:
                text += "\n條件：" + label
            page["continuations"].append({"edgeId": edge["id"], "source": edge["source"], "target": edge["target"],
                                          "label": label, "direction": direction, "relatedSlides": related, "text": text})
        measure(page, size, min_font)
    for page in pages:
        if page["minimumFontPt"] < min_font:
            warnings.append(f"{page['source']}: {page['title']}: minimum font {page['minimumFontPt']:.2f}pt is below {min_font:g}pt" + ("; --pages single explicitly forces one slide." if mode == "single" else "."))
    return {"pages": pages, "warnings": warnings, "orientation": orientation,
            "score": min(p["minimumFontPt"] for p in pages)}


def set_fill(fill, color):
    if color == "transparent":
        fill.background()
    else:
        fill.solid()
        fill.fore_color.rgb = RGBColor.from_string(color.lstrip("#"))


def style_shape(shape, item, scale):
    # An explicit empty effect list overrides the template's inherited shadow.
    shape._element.spPr.append(OxmlElement("a:effectLst"))
    for effect_ref in shape._element.xpath("./p:style/a:effectRef"):
        effect_ref.set("idx", "0")
    if hasattr(shape, "fill"):
        set_fill(shape.fill, item.get("fill", "transparent"))
    stroke = item.get("stroke", "#43638B")
    if stroke == "transparent" or item.get("strokeWidth", 1) == 0:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = RGBColor.from_string(stroke.lstrip("#"))
        shape.line.width = Pt(item.get("strokeWidth", 1) * scale)
    if item.get("dash"):
        shape.line.dash_style = MSO_LINE_DASH_STYLE.DASH


def put_text(shape, text, size, color="#172B4D", family="Arial", align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE):
    frame = shape.text_frame
    frame.clear()
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    frame.word_wrap = False
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.vertical_anchor = anchor
    family = family.split(",")[0].strip().strip("\"'") or "Arial"
    for i, line in enumerate(text.split("\n")):
        paragraph = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        paragraph.alignment = align
        paragraph.line_spacing = 1.0
        paragraph.space_before = paragraph.space_after = Pt(0)
        run = paragraph.add_run()
        run.text = line
        run.font.size = Pt(max(0.01, round(size, 2)))
        run.font.name = family
        if color == "transparent":
            run.font.fill.background()
        else:
            run.font.color.rgb = RGBColor.from_string(color.lstrip("#"))
        properties = run._r.get_or_add_rPr()
        east_asian = OxmlElement("a:ea")
        east_asian.set("typeface", family)
        properties.append(east_asian)


def transform(page, x, y):
    left, top, _, _ = page["bounds"]
    ox, oy = page["origin"]
    return Pt(ox + (x - left) * page["scale"]), Pt(oy + (y - top) * page["scale"])


def freeform(slide, points, close):
    builder = slide.shapes.build_freeform(*points[0])
    builder.add_line_segments(points[1:], close=close)
    return builder.convert_to_shape()


def add_arrows(shape, edge):
    line = shape._element.spPr.get_or_add_ln()
    for key, tag in (("arrowStart", "a:headEnd"), ("arrowEnd", "a:tailEnd")):
        if edge.get(key):
            arrow = OxmlElement(tag)
            arrow.set("type", "triangle")
            arrow.set("w", "med")
            arrow.set("len", "med")
            line.append(arrow)


def add_textbox(slide, name, x, y, width, height, text, size, **kwargs):
    shape = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(width), Pt(height))
    shape.name = name
    put_text(shape, text, size, **kwargs)
    return shape


def render_page(deck, page, min_font):
    slide = deck.slides.add_slide(deck.slide_layouts[6])
    scale = page["scale"]
    font_nodes = page["nodes"] or page["layout"]["nodes"]
    page_font = font_nodes[0].get("fontFamily", "Arial") if font_nodes else "Arial"
    for group in sorted(page["groups"], key=lambda g: g["width"] * g["height"], reverse=True):
        x, y = transform(page, group["x"], group["y"])
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Pt(group["width"] * scale), Pt(group["height"] * scale))
        shape.name = "group:" + group["id"]
        style_shape(shape, group, scale)
        if group.get("title"):
            font = group.get("fontSize", 16) * scale
            add_textbox(slide, "group-title:" + group["id"], x.pt + 5 * scale, y.pt + 4 * scale,
                        max(1, (group["width"] - 10) * scale), font * 1.4,
                        group["title"], font, family=page_font, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)
    for edge in page["internalEdges"]:
        points = [transform(page, *point) for point in edge["points"]]
        if len(points) == 2:
            shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, *points[0], *points[-1])
        else:
            shape = freeform(slide, points, close=False)
        shape.name = "edge:" + edge["id"]
        style_shape(shape, edge, scale)
        add_arrows(shape, edge)
    for node in page["nodes"]:
        x, y = transform(page, node["x"], node["y"])
        if node["kind"] in KINDS:
            shape = slide.shapes.add_shape(KINDS[node["kind"]], x, y, Pt(node["width"] * scale), Pt(node["height"] * scale))
        else:
            shape = freeform(slide, [transform(page, *p) for p in node["points"]], close=True)
        shape.name = "node:" + node["id"]
        style_shape(shape, node, scale)
        put_text(shape, node["text"], node.get("fontSize", 16) * scale,
                 node.get("color", "#172B4D"), node.get("fontFamily", "Arial"))
    for edge in page["internalEdges"]:
        label = edge.get("label")
        if not label or not label["text"]:
            continue
        x, y = transform(page, label["x"], label["y"])
        shape = add_textbox(slide, "label:" + edge["id"], x.pt, y.pt,
                            label["width"] * scale, label["height"] * scale,
                            label["text"], label.get("fontSize", 16) * scale,
                            color=label.get("color", "#172B4D"), family=label.get("fontFamily", page_font))
        set_fill(shape.fill, label.get("fill", "transparent"))
    add_textbox(slide, "slide-title", MARGIN, MARGIN, deck.slide_width.pt - 2 * MARGIN,
                page["titleHeight"], page["titleText"], max(22, min_font),
                family=page_font, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)
    y = deck.slide_height.pt - MARGIN - page["continuationHeight"]
    for continuation in page["continuations"]:
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(MARGIN), Pt(y),
                                       Pt(deck.slide_width.pt - 2 * MARGIN), Pt(continuation["height"]))
        shape.name = "edge:" + continuation["edgeId"] + ":continuation"
        style_shape(shape, {"fill": "#EFF5FC", "stroke": "#A4B9D1", "strokeWidth": 0.6}, 1)
        put_text(shape, continuation["wrappedText"], min_font, family=page_font, align=PP_ALIGN.LEFT)
        shape.text_frame.margin_left = shape.text_frame.margin_right = Pt(6)
        y += continuation["height"] + 5
    return slide


def coverage(layouts, pages, key):
    by_input = []
    for index, layout in enumerate(layouts):
        expected = {item["id"] for item in layout[key]}
        covered = set()
        for page in pages:
            if page["inputIndex"] != index:
                continue
            if key == "nodes":
                covered.update(n["id"] for n in page["nodes"])
            else:
                covered.update(e["id"] for e in page["internalEdges"])
                covered.update(c["edgeId"] for c in page["continuations"])
        by_input.append({"inputIndex": index, "total": len(expected), "covered": len(expected & covered),
                         "missingIds": sorted(expected - covered)})
    return {"total": sum(i["total"] for i in by_input), "covered": sum(i["covered"] for i in by_input),
            "complete": all(not i["missingIds"] for i in by_input),
            "missingIds": [f"{i['inputIndex']}:{identifier}" for i in by_input for identifier in i["missingIds"]],
            "byInput": by_input}


def export_layouts(input_paths, output_path, pages="auto", orientation="auto", min_font=14):
    """Write a deck plus `<deck>.report.json`; return its JSON-compatible report."""
    output = Path(output_path)
    if output.suffix.lower() != ".pptx":
        raise LayoutError("Output must use the .pptx extension; legacy binary .ppt is not supported.")
    if pages not in ("auto", "single", "groups") or orientation not in ("auto", *SIZES):
        raise LayoutError("Unsupported pages or orientation option")
    min_font = number(min_font, "min-font", True)
    if not input_paths:
        raise LayoutError("At least one layout JSON is required")
    sources, layouts = [], []
    for input_path in input_paths:
        source = str(input_path)
        try:
            layout = json.loads(Path(input_path).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise LayoutError(f"Cannot read {source}: {exc}") from exc
        validate(layout, source)
        sources.append(source)
        layouts.append(layout)
    choices = list(SIZES) if orientation == "auto" else [orientation]
    plans = [plan_orientation(layouts, sources, pages, choice, min_font) for choice in choices]
    plan = max(plans, key=lambda candidate: (candidate["score"], -len(candidate["pages"])))
    if plan["score"] < min_font and pages != "single":
        failing = min(plan["pages"], key=lambda page: page["minimumFontPt"])
        raise LayoutError(f"{failing['title']}: minimum font would be {failing['minimumFontPt']:.2f}pt, below {min_font:g}pt. "
                          "Please split the Mermaid diagram into smaller semantic groups/diagrams before exporting. "
                          "No automatic clipping or flow truncation was performed. Use --pages single only to explicitly accept smaller text.")
    deck = Presentation()
    width, height = SIZES[plan["orientation"]]
    deck.slide_width, deck.slide_height = Inches(width), Inches(height)
    deck.core_properties.title = layouts[0]["title"] if len(layouts) == 1 else "Mermaid diagrams"
    deck.core_properties.subject = "Native editable diagram shapes, text, and connectors"
    report = {"schemaVersion": 1, "format": "pptx", "nativeEditable": True,
              "orientation": plan["orientation"], "slideSizeInches": {"width": width, "height": height},
              "requestedMinimumFontPt": min_font, "pages": pages, "inputs": sources,
              "warnings": plan["warnings"], "slides": [],
              "nodeCoverage": coverage(layouts, plan["pages"], "nodes"),
              "edgeCoverage": coverage(layouts, plan["pages"], "edges"),
              "limitations": ["Fonts are referenced, not embedded; installed fonts affect glyph metrics.",
                              "Sampled curves are native editable polylines, not original Bezier handles.",
                              "Cross-page edges are represented by visible continuation cards on each endpoint page.",
                              "OOXML editability checks do not replace visual inspection in the target presentation application."]}
    if not report["nodeCoverage"]["complete"] or not report["edgeCoverage"]["complete"]:
        raise LayoutError("Internal pagination error: a node or edge has no representation")
    for page in plan["pages"]:
        slide = render_page(deck, page, min_font)
        actual_fonts = [run.font.size.pt for shape in slide.shapes if shape.has_text_frame
                        for paragraph in shape.text_frame.paragraphs for run in paragraph.runs if run.text]
        report["slides"].append({"number": page["number"], "title": page["title"],
                                  "source": page["source"], "inputIndex": page["inputIndex"], "groupId": page["groupId"],
                                  "nodeIds": [n["id"] for n in page["nodes"]],
                                  "edgeIds": [e["id"] for e in page["internalEdges"]] + [c["edgeId"] for c in page["continuations"]],
                                  "continuations": [{k: v for k, v in c.items() if k not in ("height", "wrappedText")}
                                                    for c in page["continuations"]],
                                  "minimumFontPt": min(actual_fonts) if actual_fonts else None,
                                  "nativeShapeCount": len(slide.shapes)})
    report["nativeShapeCount"] = sum(s["nativeShapeCount"] for s in report["slides"])
    output.parent.mkdir(parents=True, exist_ok=True)
    # Stage both artifacts only after all diagrams validate and all pages build.
    with tempfile.TemporaryDirectory(prefix="native-pptx-", dir=output.parent) as temporary:
        staged = Path(temporary) / "deck.pptx"
        deck.save(staged)
        reopened = Presentation(staged)
        if len(reopened.slides) != len(report["slides"]):
            raise LayoutError("PowerPoint round-trip failed: slide count changed")
        staged_report = Path(temporary) / "report.json"
        staged_report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        staged.replace(output)
        staged_report.replace(Path(str(output) + ".report.json"))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("layouts", nargs="+", help="schemaVersion 1 layout JSON files, one task per deck")
    parser.add_argument("--out", required=True, help="output .pptx file; also writes .pptx.report.json")
    parser.add_argument("--pages", choices=("auto", "single", "groups"), default="auto")
    parser.add_argument("--orientation", choices=("auto", "landscape", "portrait"), default="auto",
                        help="auto chooses the most readable shared deck orientation")
    parser.add_argument("--min-font", type=float, default=14, help="minimum final font size in points (default 14)")
    args = parser.parse_args(argv)
    try:
        report = export_layouts(args.layouts, args.out, args.pages, args.orientation, args.min_font)
    except (LayoutError, OSError, KeyError, TypeError) as exc:
        print(f"native_pptx: {exc}", file=sys.stderr)
        return 1
    for warning in report["warnings"]:
        print("Warning: " + warning, file=sys.stderr)
    print(f"Wrote {args.out}: {len(report['slides'])} slides, {report['nativeShapeCount']} native shapes ({report['orientation']}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
