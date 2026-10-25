---
description: 復盤工作階段（Retro），分析效率瓶頸與 Token 浪費，提供「修環境不修程式」的具體配置升級方案
allowed-tools: Bash, Read, Write
---

請依據 Matt Pocock 的「修環境，不修程式（Fix the environment, not the code）」哲學，復盤本次工作階段（Session）：

1. **工作階段回顧**：
   - 檢視本次對話中的痛點：是否有重複試錯的測試？是否有搜尋範圍過大導致 Token 暴增？是否有概念理解偏差？
   - 識別 AI 在開發過程中所做的未經驗證假設。

2. **產出 Retro 分析報告**：
   - **痛點與摩擦力（Frictions Encountered）**：具體列出 2–3 個拉低效率的環節。
   - **Token 浪費點（Token / Context Waste）**：是否有讀取不必要的二進位檔、快取檔或過大的日誌？

3. **環境處方簽（Actionable Environmental Fixes）**：
   不要只給抽象建議，具體輸出可落地的環境變更：
   - **Git 忽略**：需要在 `.gitignore` 加入哪些忽略路徑？
   - **行為防護欄**：是否需要新增 Hook 腳本（放在 `.claude/hooks/`）阻擋特定危險操作？
   - **領域術語**：是否有概念歧義需要補進 `GLOSSARY.md`？
   - **專案規範**：需要在 `CLAUDE.md` 補上哪一條明確的不可協商規則？
