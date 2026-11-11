# B-agent-teams

以下貼入互動式 Claude Code：

現在採用 B：Agent Teams 完成前一則 P2 的 WorkshopFlow 任務。
先確認目前版本與帳號支援，並且 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 對此 session 生效；核對實際 teammate 模式與訊息能力。不可用就回報未執行，不能用普通 subagents 冒充。
你擔任 lead／資深顧問，建立最多 3 位隊友：前端、後端／資料、QA。所有人讀相同 PRD 和契約。先列檔案責任，避免多人同時修改同一檔；Agent Teams 不會自動替你完成工作樹隔離。
請隊友直接就 API 回傳、候補狀態、交易競態、錯誤畫面與驗收案例交換訊息；遇到矛盾要提出證據和建議。lead 將共識寫入 decision-log 與契約，明確標出未決問題及負責人。有 Task 工具的隊友使用共享任務清單；沒有時明確回報限制。
不用為討論而討論；已有明確契約就各自實作。QA 針對跨層情境核對 UI/API/資料庫，lead 整合並跑共同驗收。遵守 P2 的相同預算與最多 2 輪修復，不加派隱藏隊友。
保留真實 teammate 訊息、任務流轉、決策、測試、等待和重工紀錄，不能只用角色扮演回答。完成 v1 保存版本與證據，等待 CR-01。
