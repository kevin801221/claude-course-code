"""List tool schemas from this lab's MCP server and read its bundled Visio file."""
import asyncio
import json
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    root = Path(__file__).resolve().parent
    settings = json.loads((root / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]["visio-lab"]
    server = StdioServerParameters(command=settings["command"], args=settings["args"], cwd=root)
    async with stdio_client(server) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            tools = {tool.name: tool for tool in (await session.list_tools()).tools}
            inspector = tools["inspect_flowchart"]
            print("tools/list:", inspector.name, "required =", inspector.inputSchema["required"])
            result = await session.call_tool(inspector.name, {"path": "fixtures/starter.vsdx"})
            if result.isError:
                raise SystemExit(f"MCP read failed: {result.content}")
            flow = result.structuredContent
            print("page:", flow["page"])
            for node in flow["nodes"]:
                print(f'{node["id"]} {node["text"]}')
            for edge in flow["edges"]:
                print(f'{edge["id"]}: {edge["from_id"]} -> {edge["to_id"]}')


if __name__ == "__main__":
    asyncio.run(main())
