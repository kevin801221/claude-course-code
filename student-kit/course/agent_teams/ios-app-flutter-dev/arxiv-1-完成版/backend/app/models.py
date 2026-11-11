"""資料模型,對齊凍結的 API 契約(_Context/api-contract.md 第 1 節)。

Paper / Report 直接是 FastAPI 回應 schema,也是存檔的 JSON 結構。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Paper(BaseModel):
    """單篇論文(對應契約 papers[] 元素)。"""

    title: str
    authors: list[str] = Field(default_factory=list)
    arxivId: str  # noqa: N815 —— 契約欄位名,前端依賴,不可改成 snake_case
    link: str
    summary: str


class Report(BaseModel):
    """一份每日報告(對應契約 GET /reports/today 回應)。"""

    date: str  # YYYY-MM-DD
    title: str
    markdownBody: str  # noqa: N815 —— 契約欄位名
    papers: list[Paper] = Field(default_factory=list)
