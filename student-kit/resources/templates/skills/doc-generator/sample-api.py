"""純靜態文件練習；沒有啟動 HTTP 服務。"""

def get_lesson(lesson_id: str) -> dict:
    """依課程 ID 取得課程資訊。"""
    return {"id": lesson_id, "title": "Claude Code 入門"}


def post_enrollment(name: str, lesson_id: str) -> dict:
    """建立課程報名；這是教學函式，不會呼叫外部 API。"""
    return {"name": name, "lesson_id": lesson_id}


async def get_async_lesson(lesson_id: str) -> dict:
    """此 async 函式不會被現有腳本擷取。"""
    return {"id": lesson_id}
