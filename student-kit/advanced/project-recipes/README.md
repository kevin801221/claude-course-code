# 進階專案：先學工作流，再裝大型環境

這三份配方對應講義 Part 11、18 與附錄 B。它們是課後選修，請先完成基礎 Labs。

| 配方 | 本包包含 | 需要額外準備 |
|---|---|---|
| [4-Agent 晶圓 pipeline](wafer/README.md) | 原始四個 agents、階段契約、空跑提示 | 真訓練需要資料集、Python/uv、Ultralytics 與運算時間 |
| [原生 Agent Teams](agent-teams/README.md) | 原始 API 契約、檔案分工、最小演練 | Claude 版本/功能可用；完整 App 需要 Flutter/後端環境 |
| [AgenticRAG 概念練習](agentic-rag/README.md) | 離線且可執行的控制流程示範 | 完整實作需另補講義指名 notebooks 與實際模型依賴 |

本包不包含資料集、權重、Flutter 完整 App。原始檔以固定 commit 連回來源，避免學生拿錯版本。
AgenticRAG 的三份指定 `.ipynb` 在本次五個來源 Repo 找不到；不要把其他 RAG 專案說成同一份範例。
