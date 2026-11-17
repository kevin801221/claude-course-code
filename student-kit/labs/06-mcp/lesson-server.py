#!/usr/bin/env python3
"""MCP stdio 教學子集；標準函式庫、只讀資料、每行一份 JSON-RPC。"""
import json
from pathlib import Path
import sys

LESSONS = json.loads(Path(__file__).with_name("lessons.json").read_text(encoding="utf-8"))
PROTOCOL = "2024-11-05"
TOOL = {
    "name": "search_lessons",
    "description": "搜尋課堂本機課程索引，只讀、不連外。",
    "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"], "additionalProperties": False},
}


def tool_result(text, error=False):
    return {"content": [{"type": "text", "text": text}], "isError": error}


def respond(request):
    if not isinstance(request, dict) or request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}
    if "id" not in request:
        return None
    reply = {"jsonrpc": "2.0", "id": request["id"]}
    method = request["method"]
    params = request.get("params") or {}
    if not isinstance(params, dict):
        return {**reply, "error": {"code": -32602, "message": "Invalid params"}}
    if method == "initialize":
        result = {"protocolVersion": PROTOCOL, "capabilities": {"tools": {}}, "serverInfo": {"name": "course-lessons", "version": "1.0.0"}}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": [TOOL]}
    elif method == "tools/call":
        arguments = params.get("arguments") or {}
        if params.get("name") != TOOL["name"]:
            result = tool_result("未知工具", True)
        elif not isinstance(arguments, dict) or not isinstance(arguments.get("query"), str) or set(arguments) != {"query"}:
            result = tool_result("query 必須是字串，且不可含其他參數", True)
        else:
            query = arguments["query"].casefold()
            matches = [row for row in LESSONS if query in json.dumps(row, ensure_ascii=False).casefold()]
            result = tool_result(json.dumps(matches, ensure_ascii=False))
    else:
        return {**reply, "error": {"code": -32601, "message": "Method not found"}}
    return {**reply, "result": result}


if __name__ == "__main__":
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            response = respond(json.loads(line))
        except json.JSONDecodeError:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)
