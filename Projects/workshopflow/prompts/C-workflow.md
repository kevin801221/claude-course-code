# C-workflow

以下貼入互動式 Claude Code：

現在採用 C：真正的 Dynamic workflow 完成前一則 P2 的 WorkshopFlow 任務。
先載入 /workflow-authoring 並核對當前官方 runtime、結構化回傳與 agent 呼叫方式。若此版本或帳號沒有該能力，停止回報未執行，不得用一般主代理對話或外部 shell 排程冒充。
請使用 dynamic workflow（可依官方方式用 ultracode: 指示）建立可保存的協調腳本。限制最多 3 位 worker 同時工作，確認當前支援的 CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS=3 設定。模型、effort、工具與 P2 其他組相同。
流程：讀凍結 PRD並整理契約 → 平行前端、後端、QA 測試設計 → 整合 → 跑共同驗收 → 根據結構化失敗報告，僅交辦相關責任的修復 → 再驗證。最多 2 輪修復、不可弱化測試。若失敗超限，輸出未完成與阻塞原因。
每階段回傳有明確 schema 的狀態、檔案、契約版本、實際測試與風險，腳本核對回傳後決定分支，不用自由文字假裝成功。保存腳本、輸入與執行摘要，讓下一次能使用同一套協調邏輯；不保證模型產物位元相同。
遵守 runtime 邊界：工作流腳本負責協調，檔案讀寫、執行命令與測試交由 agent 工具完成；不要在腳本直接使用未支援的檔案／shell／動態 import 或非決定性 API。請依當前文件實作，不猜 API。
PM 訪談已完成；執行中不要設計人類問答節點。v1 結束保存版本，CR-01 到來後作為另一輪輸入。用 /workflows 與實際腳本／結果證明機制；agent-board 清單未必涵蓋所有 workflow agent。
把建立腳本與修正流程的時間也算入 P2 預算。回報啟用證據、流程、條件分支、測試與未決項目。
