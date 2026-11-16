"""Exercise the same stdio server Claude Code starts, without a model or an account."""

import asyncio
import hashlib
import json
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


LAB_DIR = Path(__file__).resolve().parent
SOURCE = "fixtures/starter.vsdx"


async def test_round_trip(session: ClientSession, scratch: Path) -> None:
    async def call(name: str, **arguments):
        response = await session.call_tool(name, arguments)
        assert not response.isError, response.content
        return response.structuredContent

    tools = {tool.name for tool in (await session.list_tools()).tools}
    assert {"inspect_flowchart", "add_manager_review", "verify_manager_review", "inspect_in_visio"} <= tools
    original = LAB_DIR / SOURCE
    original_hash = hashlib.sha256(original.read_bytes()).digest()
    initial = await call("inspect_flowchart", path=SOURCE)
    ids = {node["text"]: node["id"] for node in initial["nodes"]}
    edge = {"page_name": initial["page"], "submit_id": ids["送出申請"], "complete_id": ids["完成登記"]}
    output = (scratch / "reviewed.vsdx").relative_to(LAB_DIR).as_posix()
    created = await call("add_manager_review", source=SOURCE, output=output, **edge)
    assert created["valid"] and created["output"] == output
    confirmed = await call("verify_manager_review", path=output, **edge)
    assert confirmed["valid"], confirmed

    revised = await call("inspect_flowchart", path=output, page_name=initial["page"])
    original_nodes = {(node["id"], node["text"]) for node in initial["nodes"]}
    revised_nodes = {(node["id"], node["text"]) for node in revised["nodes"]}
    assert original_nodes <= revised_nodes
    connections = {(item["from_id"], item["to_id"]) for item in revised["edges"]}
    assert (ids["填寫申請"], ids["送出申請"]) in connections
    assert (ids["送出申請"], ids["完成登記"]) not in connections
    review, supplement = confirmed["review_id"], confirmed["supplement_id"]
    directed_edges = {(item["from_id"], item["to_id"], item["label"]) for item in revised["edges"]}
    assert {
        (ids["送出申請"], review, ""), (review, ids["完成登記"], "通過"),
        (review, supplement, "退回"), (supplement, review, "重新送審"),
    } <= directed_edges

    first = (LAB_DIR / output).read_bytes()
    again = await call("add_manager_review", source=SOURCE, output=output, **edge)
    assert again["status"] == "unchanged_output"
    assert (LAB_DIR / output).read_bytes() == first
    assert hashlib.sha256(original.read_bytes()).digest() == original_hash

    forged_output = (scratch / "existing.vsdx").relative_to(LAB_DIR).as_posix()
    shutil.copyfile(original, LAB_DIR / forged_output)
    refused = await session.call_tool("add_manager_review", {"source": SOURCE, "output": forged_output, **edge})
    assert refused.isError and (LAB_DIR / forged_output).read_bytes() == original.read_bytes()
    escaped = await session.call_tool("inspect_flowchart", {"path": "../outside.vsdx"})
    assert escaped.isError

    with TemporaryDirectory() as outside:
        linked = scratch / "linked.vsdx"
        external_file = Path(outside) / "external.vsdx"
        shutil.copyfile(original, external_file)
        try:
            linked.symlink_to(external_file)
        except OSError:
            # Some Windows accounts cannot create symbolic links.
            pass
        else:
            alias = linked.relative_to(LAB_DIR).as_posix()
            assert (await session.call_tool("inspect_flowchart", {"path": alias})).isError
            assert (await session.call_tool("add_manager_review", {"source": SOURCE, "output": alias, **edge})).isError
            assert external_file.read_bytes() == original.read_bytes()

    print("PASS: stdio discovery, editable flow, verified edges, repeat run, original and existing file preserved.")


async def main() -> None:
    config = json.loads((LAB_DIR / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]["visio-lab"]
    server = StdioServerParameters(command=config["command"], args=config["args"], cwd=LAB_DIR)
    output_dir = LAB_DIR / "output"
    output_dir.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=output_dir) as scratch:
        async with stdio_client(server) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                await test_round_trip(session, Path(scratch))


if __name__ == "__main__":
    asyncio.run(main())
