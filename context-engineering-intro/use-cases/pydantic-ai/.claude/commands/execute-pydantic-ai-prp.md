# 執行 Pydantic AI 代理人 PRP (Execute Pydantic AI Agent PRP)

使用 PRP 檔案實作 Pydantic AI 代理人。

## PRP 檔案：$ARGUMENTS

## 執行流程 (Execution Process)

1. **載入 PRP (Load PRP)**
   - 讀取指定的 Pydantic AI PRP 檔案。
   - 理解所有代理人需求和研究發現。
   - 遵循 PRP 中的所有說明，並在需要時擴展研究。
   - 審查 `main_agent_reference` 模式以獲取實作指引。
   - 根據需要進行更多的網頁搜尋和 Pydantic AI 文件審查。

2. **深度思考 (ULTRATHINK)**
   - 在執行代理人實作計畫前深入思考。
   - 使用您的待辦事項 (Todos) 工具將代理人開發分解為更小的步驟。
   - 使用 `TodoWrite` 工具建立並追蹤您的代理人實作計畫。
   - 遵循 `main_agent_reference` 的配置和結構模式。
   - 規劃 `agent.py`, `tools.py`, `dependencies.py` 以及測試方法。

3. **執行計畫 (Execute the plan)**
   - 遵循 PRP 實作 Pydantic AI 代理人。
   - 建立具備基於環境配置的代理人 (`settings.py`, `providers.py`)。
   - 預設使用字串輸出 (除非需要結構化輸出，否則不使用 `result_type`)。
   - 使用 `@agent.tool` 裝飾器和正確的錯誤處理實作工具。
   - 新增包含 `TestModel` 和 `FunctionModel` 的全面測試。

4. **驗證 (Validate)**
   - 測試代理人的匯入與實例化。
   - 執行 `TestModel` 驗證以進行快速開發測試。
   - 測試工具註冊與功能。
   - 執行建立的 `pytest` 測試套件。
   - 驗證代理人是否遵循 `main_agent_reference` 模式。

5. **完成 (Complete)**
   - 確保完成所有 PRP 檢查表項目。
   - 使用範例查詢測試代理人。
   - 驗證安全模式 (環境變數、錯誤處理)。
   - 報告完成狀態。
   - 再次閱讀 PRP 以確保實作完整。

6. **參考 PRP (Reference the PRP)**
   - 如果需要，您可以隨時再次參考 PRP。

## 應遵循的 Pydantic AI 特定模式

- **配置**：使用類似 `main_agent_reference` 的基於環境的設定。
- **輸出**：預設為字串輸出，僅在需要驗證時使用 `result_type`。
- **工具**：使用 `@agent.tool` 配合 `RunContext` 進行依賴注入。
- **測試**：包含用於開發的 `TestModel` 驗證。
- **安全性**：為 API 金鑰使用環境變數，進行正確的錯誤處理。

注意：如果驗證失敗，請使用 PRP 中的錯誤模式進行修復並重試。遵循 `main_agent_reference` 以獲取經過驗證的 Pydantic AI 實作模式。
