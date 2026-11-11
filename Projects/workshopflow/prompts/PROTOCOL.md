# 公平實驗操作協定（講師）

【講師操作協定】
1. 共用準備：一次 PM 訪談，人工確認 PRD v1；建立 React TS/Vite + Express/SQLite starter、lockfile、共同驗收與 seed/reset。每組拿相同 baseline，測試由統一驗收者執行。開發開始後的協調成本與 workflow 建立時間都計時，不能只計 workflow 最後那次執行。
2. 同樣模型、effort、工具權限、網路與機器資源、最多 3 位 worker + 1 位協調者。先記錄確切版本與時間／token 或費用上限，若某模式不支援相同模型／額度，標為條件不同，不把結果混成公平排行。
3. 三組各自資料夾、session 和 SQLite，不能互看程式與修復答案。A 禁用 Agent Teams，確認真正使用普通 subagents；B 依官方文件以 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 啟用並確認 teammate；不要只看模型自述。C 核對 workflow 功能可用，用 /workflow-authoring 與 /workflows，依當前文件將 CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS 設為 3。功能不可用就記為未執行，不可偷偷改成另一種方法。
4. 各組先貼 P2，再貼其方法 prompt。v1 60 分鐘到期保存版本與證據。評分者給相同格式的失敗輸出，最多 2 輪修復，修復時間算在同一上限內。然後每組收到相同 CR-01，另給 15 分鐘與最多 2 輪修復。時間是教學示範設定，實際可事前統一調整。
5. 訪談與人類確認在 workflow 執行前完成；CR 是下一次執行的新輸入，不能要求 workflow 在執行中停下來訪談 PM。
6. 共同觀察面板僅讀資料，不幫某組修正答案。$.agent.list() 不保證包含所有 workflow agent 或跨 session 工作者；C 用 /workflows 與結構化結果補證據。狀態未知就標未知。
7. 實際紀錄總 elapsed time、setup/orchestration time、tokens／費用（取不到寫 N/A）、人類干預次數與分鐘、重工檔案與測試失敗。不要把不同欄位換算成沒有依據的單一效率分。
8. 若要研究結論，至少每種方法重跑 3 次、交換順序、對 App 產物匿名評分，報中位數與範圍。一次課堂 demo 只代表這次條件下的結果。
