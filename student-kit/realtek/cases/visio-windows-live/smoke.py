"""Exercise the published tools over stdio and read back a real Visio drawing."""

import argparse
import asyncio
from collections import defaultdict
from datetime import timedelta
import json
from pathlib import Path
import re
import sys
from xml.etree import ElementTree
from zipfile import ZipFile

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from live_visio import ROOT, new_file


LABELS = ("Claude Code", "MCP Server", "Visio")
TOOLS = {"create_visio_file", "open_visio_file", "add_shape", "add_text",
         "connect_shapes", "list_shapes", "close_document"}


def verify_saved_drawing(path):
    """Independently read the saved, one-page VSDX and check both glued endpoints."""
    namespace = {"v": "http://schemas.microsoft.com/office/visio/2012/main"}
    with ZipFile(path) as archive:
        page = ElementTree.fromstring(archive.read("visio/pages/page1.xml"))
    labels = {}
    for shape in page.findall("v:Shapes/v:Shape", namespace):
        text = shape.find("v:Text", namespace)
        if text is not None:
            label = "".join(text.itertext()).strip()
            if label in LABELS:
                if label in labels.values():
                    raise ValueError(f"Duplicate node label: {label}")
                labels[shape.attrib["ID"]] = label
    if set(labels.values()) != set(LABELS):
        raise ValueError(f"Saved node labels do not match: {labels}")
    ends = defaultdict(dict)
    for edge in page.findall("v:Connects/v:Connect", namespace):
        ends[edge.attrib["FromSheet"]][edge.attrib["FromCell"]] = edge.attrib["ToSheet"]
    pairs = sorted(
        (labels.get(cells.get("BeginX")), labels.get(cells.get("EndX")))
        for cells in ends.values() if {"BeginX", "EndX"} <= cells.keys()
    )
    if pairs != sorted(zip(LABELS, LABELS[1:])):
        raise ValueError(f"Saved connector endpoints do not match: {pairs}")


async def call(session, name, **args):
    result = await session.call_tool(name, args)
    response = "\n".join(c.text for c in result.content if c.type == "text")
    if result.isError or not response or response.startswith(("Error", "Cannot")):
        raise RuntimeError(f"{name} failed: {response}")
    print(f"{name} OK", flush=True)
    return response


async def run(list_only):
    config = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]["visio-live"]
    server = StdioServerParameters(command=config["command"], args=config["args"],
                                  env=config.get("env"), cwd=str(ROOT))
    async with stdio_client(server) as (incoming, outgoing):
        async with ClientSession(incoming, outgoing, read_timeout_seconds=timedelta(seconds=120)) as session:
            await session.initialize()
            tools = {t.name: t.inputSchema for t in (await session.list_tools()).tools}
            if tools.keys() != TOOLS or "shape1_id" not in tools["connect_shapes"]["required"]:
                raise RuntimeError(f"Unexpected Visio MCP tools: {sorted(tools)}")
            print("PASS tools/list:", ", ".join(sorted(tools)), flush=True)
            if list_only:
                return
            output = new_file("smoke")
            print(f"Drawing in a separate Visio window: {output}", flush=True)
            await call(session, "create_visio_file", save_path=str(output))
            ids = []
            for label, x in zip(LABELS, (0.6, 3.0, 5.4)):
                result = await call(session, "add_shape", file_path=str(output), shape_type="Rectangle",
                                    x=x, y=4.0, width=1.5, height=0.8)
                match = re.search(r"\bID (\d+)\b", result)
                if not match:
                    raise ValueError(f"Missing shape ID: {result}")
                ids.append(int(match[1]))
                await call(session, "add_text", file_path=str(output), shape_id=ids[-1], text=label)
            for source, target in zip(ids, ids[1:]):
                await call(session, "connect_shapes", file_path=str(output),
                           shape1_id=source, shape2_id=target, connector_type="Dynamic")
            listed = json.loads(await call(session, "list_shapes", file_path=str(output)))
            by_id = {int(shape["ID"]): shape["Text"] for shape in listed}
            if [by_id.get(i) for i in ids] != list(LABELS):
                raise ValueError(f"Live Visio labels do not match: {by_id}")
            await call(session, "close_document", file_path=str(output), save_changes=True)
    verify_saved_drawing(output)
    print(f"PASS .vsdx: 3 named nodes, 2 glued connectors. Open the saved file: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-only", action="store_true", help="verify tool discovery without launching Visio")
    args = parser.parse_args()
    if sys.platform != "win32":
        parser.exit(2, "Run this check on Windows. The full drawing check requires desktop Visio.\n")
    asyncio.run(run(args.list_only))
