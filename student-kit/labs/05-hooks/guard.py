#!/usr/bin/env python3
"""PreToolUse 範例：僅阻擋 Write/Edit 的 .env* 與 secrets/ 路徑。"""
import json
from pathlib import PurePosixPath
import sys


def main():
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise ValueError("event 必須是 object")
        if event.get("tool_name") not in {"Write", "Edit"}:
            return 0
        tool_input = event.get("tool_input")
        if not isinstance(tool_input, dict):
            raise ValueError("缺少 tool_input")
        file_path = tool_input.get("file_path")
        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("缺少 file_path")
        path = PurePosixPath(file_path.replace("\\", "/"))
        if path.name.startswith(".env") or "secrets" in path.parts:
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "課堂範例：請勿以 Write/Edit 修改 .env* 或 secrets/。",
            }}, ensure_ascii=False))
        return 0
    except (ValueError, TypeError) as error:
        print("Hook JSON 輸入格式錯誤：" + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
