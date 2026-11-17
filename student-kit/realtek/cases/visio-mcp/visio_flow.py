"""Read and patch one page of an editable, unencrypted Visio drawing.

The lab edits a single, unlabeled, glued edge between two unrotated, top-level
flowchart shapes with explicit geometry. It does not run macros or launch Visio.
"""
import filecmp
import math
import os
import posixpath
import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile

from lxml import etree as ET

V = "{http://schemas.microsoft.com/office/visio/2012/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
VIS_REL = "http://schemas.microsoft.com/visio/2010/relationships/"
REVIEW, SUPPLEMENT = "主管審核", "補件"


def _xml(archive, name):
    return ET.fromstring(archive.read(name), ET.XMLParser(resolve_entities=False, no_network=True))


def _related(archive, part, role, rel_id=None):
    directory, name = posixpath.split(part)
    links = _xml(archive, posixpath.join(directory, "_rels", name + ".rels"))
    targets = [r.get("Target") for r in links
               if r.get("Type") == VIS_REL + role and r.get("TargetMode") != "External"
               and (rel_id is None or r.get("Id") == rel_id)]
    if len(targets) != 1:
        raise ValueError(f"Expected a single internal {role} relationship in {part or 'package'}.")
    return posixpath.normpath(posixpath.join(directory, targets[0])).lstrip("/")


def _page(archive, name):
    doc = _related(archive, "", "document")
    index = _related(archive, doc, "pages")
    page_index = _xml(archive, index)
    if page_index.tag != V + "Pages":
        raise ValueError("Expected a Visio 2013+ .vsdx drawing with the 2012/main namespace.")
    pages = page_index.findall(V + "Page")
    names = [p.get("Name") or p.get("NameU") for p in pages]
    if name is None:
        if len(pages) != 1:
            raise ValueError(f"Specify a page name. Available pages: {names}")
        name = names[0]
    if names.count(name) != 1:
        raise ValueError(f"Unknown or ambiguous page {name!r}. Available pages: {names}")
    page = pages[names.index(name)]
    part = _related(archive, index, "page", page.find(V + "Rel").get(R + "id"))
    return names, name, part, page.find(V + "PageSheet"), _xml(archive, part)


def _text(shape):
    text = shape.find(V + "Text")
    return "".join(text.itertext()).strip() if text is not None else ""


def _shapes(root):
    return {int(s.get("ID")): s for s in root.findall(f"{V}Shapes/{V}Shape")}


def _edges(root):
    shapes, endpoints = _shapes(root), {}
    for c in root.findall(f"{V}Connects/{V}Connect"):
        if c.get("FromCell") in ("BeginX", "EndX"):
            ends = endpoints.setdefault(int(c.get("FromSheet")), {})
            key = c.get("FromCell")
            if key in ends:
                raise ValueError("A connector endpoint is glued more than once.")
            ends[key] = int(c.get("ToSheet"))
    return [{"id": k, "from_id": v["BeginX"], "to_id": v["EndX"], "label": _text(shapes[k])}
            for k, v in endpoints.items() if k in shapes and "BeginX" in v and "EndX" in v]


def inspect_flow(path: Path, page_name: str | None = None) -> dict:
    with ZipFile(path) as archive:
        names, selected, _, _, root = _page(archive, page_name)
        edges = _edges(root)
        connectors = {e["id"] for e in edges}
        nodes = [{"id": k, "text": _text(s)} for k, s in _shapes(root).items()
                 if k not in connectors and s.find(f"{V}Cell[@N='BeginX']") is None]
        return {"pages": names, "page": selected, "nodes": nodes, "edges": edges}


def _branch_names(submit_id, complete_id):
    prefix = f"LabApproval_{submit_id}_{complete_id}_"
    return prefix + "Review", prefix + "Supplement"


def _static_glue(shapes, connector, link):
    """Check both stored endpoint formulas and their referenced native port."""
    target = shapes.get(int(link.get("ToSheet")))
    if target is None:
        return False
    port = link.get("ToCell", "")
    end = {"BeginX": "Begin", "EndX": "End"}.get(link.get("FromCell"))
    row_number = port.removeprefix("Connections.X")
    if not end or port == row_number or not row_number.isdigit():
        return False
    index = int(row_number) - 1
    row = target.find(f"{V}Section[@N='Connection']/{V}Row[@IX='{index}']")
    if row is None or link.get("ToPart") != str(100 + index):
        return False
    ref = f"Sheet.{target.get('ID')}!Connections."
    formula = f"PAR(PNT({ref}X{index+1},{ref}Y{index+1}))"
    for axis in ("X", "Y"):
        endpoint = connector.find(f"{V}Cell[@N='{end}{axis}']")
        if row.find(f"{V}Cell[@N='{axis}']") is None or endpoint is None or endpoint.get("F") != formula:
            return False
    return True


def _report(root, submit_id, complete_id):
    shapes = _shapes(root)
    review_name, supplement_name = _branch_names(submit_id, complete_id)
    def role(name):
        matches = [k for k, s in shapes.items() if s.get("NameU") == name]
        if len(matches) > 1:
            raise ValueError(f"Duplicate diagram role {name}")
        return next(iter(matches), None)
    review, supplement = role(review_name), role(supplement_name)
    required = [(submit_id, review, ""), (review, complete_id, "通過"),
                (review, supplement, "退回"), (supplement, review, "重新送審")]
    edges = _edges(root)
    actual = [(e["from_id"], e["to_id"], e["label"]) for e in edges]
    valid = (review is not None and supplement is not None and _text(shapes[review]) == REVIEW
             and _text(shapes[supplement]) == SUPPLEMENT and submit_id in shapes and complete_id in shapes
             and all(actual.count(route) == 1 for route in required)
             and not any(a == submit_id and b == complete_id for a, b, _ in actual))
    if valid:
        route_ids = {e["id"] for e in edges if (e["from_id"], e["to_id"], e["label"]) in required}
        links = [link for link in root.findall(f"{V}Connects/{V}Connect")
                 if int(link.get("FromSheet")) in route_ids and link.get("FromCell") in ("BeginX", "EndX")]
        valid = len(links) == 8 and all(_static_glue(shapes, shapes[int(link.get("FromSheet"))], link)
                                        for link in links)
    nodes = [{"id": node, "text": _text(shapes[node])}
             for node in (submit_id, review, supplement, complete_id) if node in shapes]
    return {"valid": valid, "review_id": review, "supplement_id": supplement,
            "nodes": nodes, "edges": edges}


def verify_supervisor_review(path: Path, *, page_name: str | None = None,
                             submit_id: int, complete_id: int) -> dict:
    with ZipFile(path) as archive:
        _, _, _, _, root = _page(archive, page_name)
        return _report(root, submit_id, complete_id)


def _number(sheet, name, default=None):
    cell = sheet.find(f"{V}Cell[@N='{name}']")
    if cell is None:
        if default is not None:
            return default
        raise ValueError(f"Missing explicit geometry cell {name}; use an ungrouped flowchart.")
    value = float(cell.get("V"))
    if not math.isfinite(value):
        raise ValueError(f"Invalid {name} geometry.")
    return value


def _cell(parent, name, value, formula=None):
    attrs = {"N": name, "V": format(value, ".12g") if isinstance(value, float) else str(value)}
    if formula is not None:
        attrs["F"] = formula
    return ET.SubElement(parent, V + "Cell", **attrs)


def _section(shape, name, **attrs):
    section = ET.Element(V + "Section", N=name, **attrs)
    end = next((child for child in shape if child.tag in (V + "Text", V + "Shapes", V + "ForeignData")), None)
    if end is None:
        shape.append(section)
    else:
        shape.insert(shape.index(end), section)
    return section


def _geometry(shape, points, width, height):
    geom = _section(shape, "Geometry", IX="0")
    for i, (x, y) in enumerate(points, 1):
        row = ET.SubElement(geom, V + "Row", T="MoveTo" if i == 1 else "LineTo", IX=str(i))
        _cell(row, "X", x * width, f"Width*{x}")
        _cell(row, "Y", y * height, f"Height*{y}")


def _caption(shape, text, size, fill):
    # Visio stores Character.Size in inches, including point-tagged cells.
    row = ET.SubElement(_section(shape, "Character"), V + "Row", IX="0")
    _cell(row, "Size", size / 72)
    _cell(row, "Color", fill)
    para = ET.SubElement(_section(shape, "Paragraph"), V + "Row", IX="0")
    _cell(para, "HorzAlign", 1)
    ET.SubElement(shape, V + "Text").text = text


def _node(shapes, identifier, name, label, x, y, w, h):
    shape = ET.SubElement(shapes, V + "Shape", ID=str(identifier), NameU=name,
                          Type="Shape", LineStyle="0", FillStyle="0", TextStyle="0")
    for key, value in [("PinX", x), ("PinY", y), ("Width", w), ("Height", h)]:
        _cell(shape, key, value)
    _cell(shape, "LocPinX", w / 2, "Width*0.5")
    _cell(shape, "LocPinY", h / 2, "Height*0.5")
    _cell(shape, "LineColor", "#395472")
    _cell(shape, "LinePattern", 1)
    _cell(shape, "LineWeight", 1.2 / 72)
    _cell(shape, "FillPattern", 1)
    _cell(shape, "FillForegnd", "#DBEBFA" if label == REVIEW else "#FFF1D9")
    _geometry(shape, [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], w, h)
    _caption(shape, label, 14, "#182C46")
    return shape


def _box(shape):
    w, h = _number(shape, "Width"), _number(shape, "Height")
    x = _number(shape, "PinX") - _number(shape, "LocPinX", w / 2)
    y = _number(shape, "PinY") - _number(shape, "LocPinY", h / 2)
    return x, y, w, h


def _port(shape, fx, fy):
    # Named connection points on existing masters require master inheritance
    # resolution. The lab operates on standalone, explicit-geometry nodes.
    x, y, w, h = _box(shape)
    section = shape.find(f"{V}Section[@N='Connection']")
    if section is None:
        section = _section(shape, "Connection")
    rows = section.findall(V + "Row")
    ix = max((int(r.get("IX", "0")) for r in rows), default=-1) + 1
    row = ET.SubElement(section, V + "Row", IX=str(ix), T="Connection")
    _cell(row, "X", fx * w, f"Width*{fx}")
    _cell(row, "Y", fy * h, f"Height*{fy}")
    _cell(row, "DirX", 0)
    _cell(row, "DirY", 0)
    _cell(row, "Type", 0)
    return int(shape.get("ID")), ix, x + fx * w, y + fy * h


def _edge(shapes, connects, identifier, start, finish, label):
    a, b = start, finish
    x, y, dx, dy = a[2], a[3], b[2]-a[2], b[3]-a[3]
    shape = ET.SubElement(shapes, V + "Shape", ID=str(identifier), NameU=f"LabLink.{identifier}",
                          Type="Shape", LineStyle="0", FillStyle="0", TextStyle="0")
    for name, value, formula in [
        ("PinX", x + dx / 2, "(BeginX+EndX)/2"), ("PinY", y + dy / 2, "(BeginY+EndY)/2"),
        ("Width", dx, "EndX-BeginX"), ("Height", dy, "EndY-BeginY"),
        ("LocPinX", dx / 2, "Width*0.5"), ("LocPinY", dy / 2, "Height*0.5"),
        ("Angle", 0, "GUARD(0DA)")]:
        _cell(shape, name, value, formula)
    for end, (sid, ix, px, py), part in [("Begin", a, 9), ("End", b, 12)]:
        # PAR(PNT(...)) transforms a named shape's local port to page space.
        # Both endpoint cells use it, so the glued line follows a moved node.
        ref = f"Sheet.{sid}!Connections."
        formula = f"PAR(PNT({ref}X{ix+1},{ref}Y{ix+1}))"
        _cell(shape, end+"X", px, formula)
        _cell(shape, end+"Y", py, formula)
        ET.SubElement(connects, V+"Connect", FromSheet=str(identifier), FromCell=end+"X",
                      FromPart=str(part), ToSheet=str(sid), ToCell=f"Connections.X{ix+1}", ToPart=str(100+ix))
    for key, value in [("EndArrow", 4), ("EndArrowSize", 2), ("LinePattern", 1),
                       ("LineColor", "#405773"), ("LineWeight", 1.25/72), ("FillPattern", 0),
                       ("TxtWidth", 0.82), ("TxtHeight", 0.24), ("TxtAngle", 0),
                       ("TextBkgnd", "#FFFFFF"), ("TextBkgndTrans", 0)]:
        _cell(shape, key, value)
    _cell(shape, "TxtPinX", dx / 2, "Width*0.5")
    _cell(shape, "TxtPinY", dy / 2, "Height*0.5")
    _cell(shape, "TxtLocPinX", 0.41, "TxtWidth*0.5")
    _cell(shape, "TxtLocPinY", 0.12, "TxtHeight*0.5")
    _geometry(shape, [(0, 0), (1, 1)], dx, dy)
    if label:
        _caption(shape, label, 10, "#243B57")


def _patch(root, sheet, submit_id, complete_id):
    report = _report(root, submit_id, complete_id)
    if report["valid"]:
        return False
    if report["review_id"] is not None or report["supplement_id"] is not None:
        raise ValueError("This review block already exists but its nodes or routes have changed.")
    shapes = _shapes(root)
    if submit_id == complete_id or submit_id not in shapes or complete_id not in shapes:
        raise ValueError("Select two different, existing top-level node IDs.")
    src, dst = shapes[submit_id], shapes[complete_id]
    for s in (src, dst):
        if (s.get("Type") != "Shape" or s.get("Master") or s.find(f"{V}Cell[@N='BeginX']") is not None
            or _number(s, "Angle", 0) != 0 or _number(s, "FlipX", 0) or _number(s, "FlipY", 0)):
            raise ValueError("Editing requires two unrotated, ungrouped, masterless 2-D nodes.")
        if any(r.get("N") for r in s.findall(f"{V}Section[@N='Connection']/{V}Row")):
            raise ValueError("Selected nodes must use numbered connection points.")
    direct = [e for e in report["edges"] if (e["from_id"], e["to_id"]) == (submit_id, complete_id)]
    if len(direct) != 1 or direct[0]["label"]:
        raise ValueError("Select the ends of exactly one unlabeled, forward, glued connector.")
    old = direct[0]["id"]
    source_box, dest_box = _box(src), _box(dst)
    sx, sy, sw, sh = source_box
    ex, ey, ew, eh = dest_box
    ax, ay, bx, by = sx+sw/2, sy+sh/2, ex+ew/2, ey+eh/2
    horizontal = abs(bx-ax) > abs(by-ay)
    rx, ry = (ax+bx)/2, (ay+by)/2
    w, h = 1.84, 0.68
    pw, ph = _number(sheet, "PageWidth"), _number(sheet, "PageHeight")
    if horizontal:
        placements = [(rx, ry-2.25), (rx, ry+2.25)]
    else:
        placements = [(rx+2.75, ry), (rx-2.75, ry)]
    obstacles = [_box(s) for s in shapes.values() if s.find(f"{V}Cell[@N='BeginX']") is None
                 and s.find(f"{V}Cell[@N='Width']") is not None and s.find(f"{V}Cell[@N='Height']") is not None]
    def fits(x, y):
        lx, ly = x-w/2, y-h/2
        return (0.08 <= lx and lx+w <= pw-0.08 and 0.08 <= ly and ly+h <= ph-0.08
                and all(lx+w+.10 <= ox or ox+ow+.10 <= lx or ly+h+.10 <= oy or oy+oh+.10 <= ly
                        for ox, oy, ow, oh in obstacles))
    supplement_center = next(((x, y) for x, y in placements if fits(x,y)), None)
    if not fits(rx, ry) or supplement_center is None:
        raise ValueError("Leave space between the selected nodes and beside the path for the review loop.")
    # Reserve IDs across nested groups as well, not just visible top-level shapes.
    new = max(int(s.get("ID")) for s in root.iter(V+"Shape")) + 1
    parent = src.getparent()
    old_shape = shapes[old]
    links = root.find(V+"Connects")
    for link in list(links):
        if link.get("ToSheet") == str(old):
            raise ValueError("The selected connector is itself the target of another connection.")
        if link.get("FromSheet") == str(old):
            links.remove(link)
    parent.remove(old_shape)
    rname, sname = _branch_names(submit_id, complete_id)
    review = _node(parent, new, rname, REVIEW, rx, ry, w, h)
    cx, cy = supplement_center
    supplement = _node(parent, new+1, sname, SUPPLEMENT, cx, cy, w, h)
    if horizontal:
        side = float(bx > ax)
        outport, inport = (side, 0.5), (1-side, 0.5)
        near, far = float(cy > ry), float(cy < ry)
        reject_r, reject_s, retry_s, retry_r = (.20,near), (.20,far), (.80,far), (.80,near)
    else:
        side = float(by > ay)
        outport, inport = (0.5, side), (0.5, 1-side)
        near, far = float(cx > rx), float(cx < rx)
        reject_r, reject_s, retry_s, retry_r = (near,.20), (far,.20), (far,.80), (near,.80)
    for sid, a, ap, b, bp, label in [
        (old, src, outport, review, inport, ""),
        (new+2, review, outport, dst, inport, "通過"),
        (new+3, review, reject_r, supplement, reject_s, "退回"),
        (new+4, supplement, retry_s, review, retry_r, "重新送審")]:
        _edge(parent, links, sid, _port(a, *ap), _port(b, *bp), label)
    return True


def add_supervisor_review(source: Path, output: Path, *, page_name: str | None = None,
                          submit_id: int, complete_id: int) -> dict:
    source, output = Path(source), Path(output)
    if source.resolve() == output.resolve() or source.suffix.lower() != ".vsdx" or output.suffix.lower() != ".vsdx":
        raise ValueError("Choose separate .vsdx source and output files.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        staged = Path(tmp) / "review.vsdx"
        with ZipFile(source) as archive:
            if len(archive.infolist()) != len(set(archive.namelist())) or any(
                part.lower().startswith("_xmlsignatures/") for part in archive.namelist()
            ):
                raise ValueError("Signed drawings and duplicate package parts are unsupported.")
            _, name, part, sheet, root = _page(archive, page_name)
            changed = _patch(root, sheet, submit_id, complete_id)
            if changed:
                xml = ET.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
                with ZipFile(staged, "w") as result:
                    result.comment = archive.comment
                    for item in archive.infolist():
                        result.writestr(item, xml if item.filename == part else archive.read(item.filename))
            else:
                shutil.copyfile(source, staged)
        verified = verify_supervisor_review(staged, page_name=name, submit_id=submit_id, complete_id=complete_id)
        if not verified["valid"]:
            raise ValueError("Saved output did not pass review-loop verification.")
        status = "applied" if changed else "already_applied"
        try:
            # Publish the complete verified file atomically; a concurrent writer wins intact.
            os.link(staged, output)
        except FileExistsError:
            if not filecmp.cmp(staged, output, shallow=False):
                raise FileExistsError(f"Choose a new output name; {output.name} already exists.") from None
            status = "unchanged_output"
        return {"page": name, "status": status, **verified}
