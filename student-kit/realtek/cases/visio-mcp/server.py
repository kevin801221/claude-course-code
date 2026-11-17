"""Claude Code MCP tools for the editable Visio review-flow lab."""

from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from visio_flow import add_supervisor_review, inspect_flow, verify_supervisor_review


LAB_DIR = Path(__file__).resolve().parent
READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=False)
mcp = FastMCP(
    "visio-lab",
    instructions=(
        "Inspect the original .vsdx first. Use the page name and shape IDs it returns "
        "to edit a copy in output/, then verify that file. Paths are relative to this lab."
    ),
)


def lab_file(value: str, *, for_output: bool = False) -> Path:
    relative = Path(value)
    if relative.anchor or relative.suffix.lower() != ".vsdx" or ":" in value:
        raise ValueError("Supply a lab-relative .vsdx path, for example fixtures/starter.vsdx.")
    if ".." in relative.parts:
        raise ValueError("Use a path inside the lab without '..'.")
    path = (LAB_DIR / relative).resolve()
    allowed = LAB_DIR / "output" if for_output else LAB_DIR
    if not path.is_relative_to(allowed):
        raise ValueError("The resolved path must stay inside " + ("output/." if for_output else "the lab."))
    if not for_output and not path.is_file():
        raise ValueError(f"Visio file not found: {value}")
    return path


@mcp.tool(annotations=READ_ONLY)
def inspect_flowchart(path: str, page_name: str | None = None) -> dict[str, Any]:
    """Read an editable .vsdx and list its pages, shape IDs, labels and directed connections."""
    return inspect_flow(lab_file(path), page_name=page_name)


@mcp.tool(annotations=ToolAnnotations(destructiveHint=False, idempotentHint=True, openWorldHint=False))
def add_manager_review(
    source: str,
    submit_id: int,
    complete_id: int,
    output: str = "output/reviewed.vsdx",
    page_name: str | None = None,
) -> dict[str, Any]:
    """Insert supervisor review on the selected submit→complete edge, with approval and return-for-supplement paths.

    Pass the existing submission and completion shape IDs from inspect_flowchart. The source stays intact.
    Repeating the same request reuses its output. An unrelated existing destination is refused.
    """
    original = lab_file(source)
    destination = lab_file(output, for_output=True)
    if original == destination:
        raise ValueError("Choose an output path different from the source.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    result = add_supervisor_review(
        original, destination, page_name=page_name, submit_id=submit_id, complete_id=complete_id
    )
    return {**result, "output": destination.relative_to(LAB_DIR).as_posix()}


@mcp.tool(annotations=READ_ONLY)
def verify_manager_review(
    path: str, submit_id: int, complete_id: int, page_name: str | None = None
) -> dict[str, Any]:
    """Reopen the saved .vsdx and check the supervisor approval path and correction loop."""
    return verify_supervisor_review(
        lab_file(path), page_name=page_name, submit_id=submit_id, complete_id=complete_id
    )


@mcp.tool(annotations=READ_ONLY)
def inspect_in_visio(path: str) -> dict[str, Any]:
    """On Windows with desktop Microsoft Visio, open the file read-only and inspect it through Visio itself."""
    from desktop_visio import inspect_in_visio as inspect_desktop

    return inspect_desktop(lab_file(path))


if __name__ == "__main__":
    mcp.run(transport="stdio")
