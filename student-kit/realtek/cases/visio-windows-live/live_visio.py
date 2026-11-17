"""Start the public Visio MCP tools in a separate, visible classroom window."""

import argparse
from datetime import datetime
from pathlib import Path
import sys
from uuid import uuid4


ROOT = Path(__file__).resolve().parent


def new_file(label):
    suffix = f"{datetime.now():%Y%m%d-%H%M%S}-{uuid4().hex[:6]}"
    return ROOT / "output" / f"{label}-{suffix}.vsdx"


def print_prompts():
    output = new_file("claude-mcp-visio")
    print(f"""
① 在 Claude Code 貼上第一段，等 Visio 出現後，把兩個視窗並排。

請使用 visio-live 的 create_visio_file 新建空白圖，save_path 請完整使用
{output}
後續操作都在這個檔案上。請先停在空白畫布，回覆實際儲存路徑。

② 看著右邊畫布，貼上第二段。

請只用 visio-live，在剛才的圖從左至右放三個 Rectangle。每個寬 1.5 英吋、高 0.8 英吋，
左下座標依序為 (0.6, 4)、(3.0, 4)、(5.4, 4)。每次 add_shape 都讀取傳回的形狀 ID，
立刻用 add_text 寫上對應文字「Claude Code」、「MCP Server」、「Visio」。三個都完成後停下來。

③ 確認三個標籤後，貼上第三段。

請依上一步實際取得的 ID，用 visio-live 的 connect_shapes 和 Dynamic 連接器，
從 Claude Code 連到 MCP Server，再從 MCP Server 連到 Visio。
用 list_shapes 確認結果，回報三個標籤及 .vsdx 路徑，保留視窗讓我拖動中間的方塊。
""".strip())


def new_visible_app():
    import win32com.client

    # Visio.InvisibleApp creates an independent instance. Reveal it immediately
    # instead of attaching the upstream tool to the student's existing document.
    app = win32com.client.DispatchEx("Visio.InvisibleApp")
    app.Visible = True
    return app


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preflight", action="store_true", help="open a separate Visio instance and read its version")
    mode.add_argument("--prompts", action="store_true", help="print classroom prompts with a new absolute output path")
    args = parser.parse_args()
    if args.prompts:
        print_prompts()
        return
    if sys.platform != "win32":
        parser.exit(2, "This live lab requires Windows and the Microsoft Visio desktop application.\n")
    if args.preflight:
        try:
            app = new_visible_app()
            try:
                print(f"Visio desktop COM OK: version {app.Version}, visible = {bool(app.Visible)}")
            finally:
                app.Quit()
        except Exception as error:
            parser.exit(1, f"Could not start desktop Visio. Open and activate Visio once, then retry.\n{error}\n")
        return

    from visio_mcp_server import visio_server

    def get_classroom_app():
        if visio_server.visio_app is None:
            visio_server.visio_app = new_visible_app()
        return visio_server.visio_app

    # The published tool implementations are registered on this server. Delay
    # COM activation so /mcp and tools/list work before the first drawing call.
    visio_server.get_visio_app = get_classroom_app
    visio_server.mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
