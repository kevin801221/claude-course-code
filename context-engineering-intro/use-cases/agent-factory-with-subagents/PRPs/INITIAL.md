## FEATURE (功能)：

[請將方括號中的內容替換為您自己的上下文]
[提供您想要構建的代理人概覽。細節越多越好！]
[過於簡單的範例：使用 Pydantic AI 構建一個簡單的研究代理人，它可以透過 Brave API 研究主題，並使用 Gmail 起草電子郵件以分享見解。]

## TOOLS (工具)：

[描述您希望代理人擁有的工具 —— 功能、參數、回傳內容等。請盡可能具體 —— 越具體越好。]

## DEPENDENCIES (依賴項)：

[描述代理人工具所需的依賴項 (用於 Pydantic AI 的 RunContext) —— 例如 API 金鑰、資料庫連線、HTTP 用戶端等。]

## SYSTEM PROMPT(S) (系統提示詞)：

[在此描述給代理人的指令 —— 您可以建立完整的系統提示詞，或者提供一般性描述來引導編碼助手。]

## EXAMPLES (範例)：

[將過去專案或在線資源中的任何其他代理人/工具實作範例新增至 `examples/` 資料夾，並在此處引用它們。]
[此範本已包含以下 Pydantic AI 內容：]

- examples/basic_chat_agent —— 具備對話記憶的基礎對話代理人
- examples/tool_enabled_agent —— 具備網頁搜尋能力的工具化代理人
- examples/structured_output_agent —— 用於資料驗證的結構化輸出代理人
- examples/testing_examples —— 使用 TestModel 和 FunctionModel 的測試範例
- examples/main_agent_reference —— 構建 Pydantic AI 代理人的最佳實踐

## DOCUMENTATION (文件)：

[新增您希望它參考的任何額外文件 —— 這可以是您放在 `PRPs/ai_docs` 中的精選文件、網址等。]

- Pydantic AI 官方文件： https://ai.pydantic.dev/
- 代理人建立指南： https://ai.pydantic.dev/agents/
- 工具整合： https://ai.pydantic.dev/tools/
- 測試模式： https://ai.pydantic.dev/testing/
- 模型提供者： https://ai.pydantic.dev/models/

## OTHER CONSIDERATIONS (其他考量)：

- 使用環境變數進行 API 金鑰配置，而非硬編碼模型字串。
- 保持代理人簡單 —— 除非明確需要結構化輸出，否則預設使用字串輸出。
- 遵循 `main_agent_reference` 中的配置與提供者模式。
- 務必包含使用 TestModel 進行開發的全面測試。

[為編碼助手新增任何額外考量，特別是您希望它記住的「陷阱 (Gotchas)」。]
