"""Optional: LangGraph orchestrates a real Claude Agent SDK turn with one read-only MCP tool."""
import argparse
import asyncio
import json
import os
from tempfile import TemporaryDirectory
from typing import TypedDict

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, ResultMessage, create_sdk_mcp_server, tool
from langgraph.graph import StateGraph, START, END

DOCS = {"menu": "素食菜單有絲瓜蒸餃。", "hours": "教學餐廳的營業時間為 11:00–20:00。"}
class State(TypedDict, total=False):
    question: str
    observed: list[str]
    answer: str


def toolset():
    seen = []
    @tool("look_up", "查虛構餐廳資料，topic 僅支援 menu（菜單）或 hours（營業時間）", {"topic": str})
    async def look_up(args):
        key = args.get("topic")
        if key not in DOCS:
            return {"content": [{"type": "text", "text": "沒有此項來源"}]}
        seen.append(key)
        return {"content": [{"type":"text", "text": json.dumps({"id":key,"text":DOCS[key]},ensure_ascii=False)}]}
    return seen, look_up, create_sdk_mcp_server(name="restaurant",tools=[look_up])


async def sdk_turn(s: State):
    seen, _, server = toolset()
    with TemporaryDirectory() as workspace:
        options=ClaudeAgentOptions(
            cwd=workspace, tools=[], setting_sources=[], max_turns=4,
            mcp_servers={"restaurant":server}, allowed_tools=["mcp__restaurant__look_up"],
            permission_mode="dontAsk",
            system_prompt=("這是虛構餐廳練習。問候可直接回應；問資料時請使用 look_up。"
                           "有資料只輸出原句再加空格和 [id]；沒有資料就說「目前沒有足夠來源回答。」"),
        )
        async with ClaudeSDKClient(options=options) as client:
            await client.query(s["question"])
            async for m in client.receive_response():
                if isinstance(m,ResultMessage):
                    if m.is_error:
                        raise RuntimeError("SDK 未成功完成。請檢查 API key、帳戶用量及網路。")
                    return {"answer":(m.result or "").strip(), "observed":list(seen)}
    raise RuntimeError("SDK 沒有回傳完成訊息。")


def check(s: State):
    # Do not treat a made-up ID as retrieval. Check the content against actual tool calls.
    if s["question"].strip() not in {"你好","嗨"}:
        if not any(s["answer"] == DOCS[k]+" ["+k+"]" for k in s["observed"]):
            return {"answer":"目前沒有足夠來源回答。"}
    return {}


def build_graph():
    builder=StateGraph(State)
    builder.add_node("Claude Agent SDK", sdk_turn)
    builder.add_node("Verify observed evidence", check)
    builder.add_edge(START,"Claude Agent SDK"); builder.add_edge("Claude Agent SDK","Verify observed evidence")
    builder.add_edge("Verify observed evidence",END)
    return builder.compile()


async def self_check():
    seen, lookup, server = toolset()
    assert server["type"] == "sdk"
    sample = await lookup.handler({"topic":"hours"})
    assert json.loads(sample["content"][0]["text"]) == {"id":"hours","text":DOCS["hours"]}
    assert seen == ["hours"]
    assert check({"question":"營業時間？","answer":"24 小時。 [hours]","observed":seen})["answer"].startswith("目前沒有")
    assert check({"question":"營業時間？","answer":DOCS["hours"]+" [hours]","observed":seen}) == {}
    assert check({"question":"營業時間？","answer":DOCS["hours"]+" [hours]","observed":[]})["answer"].startswith("目前沒有")
    build_graph()
    print("PASS：已載入真實 SDK、註冊及呼叫自訂工具、編譯 LangGraph，並驗證引用；沒有連線到模型。")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-check",action="store_true")
    mode.add_argument("--live",action="store_true")
    parser.add_argument("--question",default="餐廳的營業時間？")
    args=parser.parse_args()
    if args.self_check:
        asyncio.run(self_check())
    elif not os.getenv("ANTHROPIC_API_KEY"):
        parser.error("--live 需要 ANTHROPIC_API_KEY。未設定金鑰，未發出請求。")
    else:
        result=asyncio.run(build_graph().ainvoke({"question":args.question}))
        print("實際工具回報的來源：",result.get("observed",[]))
        print("驗證後的回答：",result["answer"])
