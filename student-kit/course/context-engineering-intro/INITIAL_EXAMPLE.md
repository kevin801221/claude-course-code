## FEATURE (功能)：

- 一個 Pydantic AI 代理人 (Agent)，它將另一個 Pydantic AI 代理人作為工具。
- 主代理人為「研究代理人 (Research Agent)」，子代理人為「郵件草稿代理人 (Email Draft Agent)」。
- 用於與代理人互動的 CLI。
- 郵件草稿代理人使用 Gmail，研究代理人使用 Brave API。

## EXAMPLES (範例)：

在 `examples/` 資料夾中，有一個 README 供您閱讀，以了解該範例的全部內容，以及在為上述功能建立文件時如何構建自己的 README。

- `examples/cli.py` - 將此作為建立 CLI 的範本。
- `examples/agent/` - 通讀此處的所有檔案，了解建立支援不同提供者和 LLM、處理代理人依賴關係以及向代理人新增工具的 Pydantic AI 代理人的最佳實踐。

請勿直接複製這些範例中的任何內容，它們完全屬於另一個專案。但請將其作為靈感和最佳實踐的參考。

## DOCUMENTATION (文件)：

Pydantic AI 官方文件：https://ai.pydantic.dev/

## OTHER CONSIDERATIONS (其他考量)：

- 包含 `.env.example`，以及包含設定說明的 `README` (包括如何設定 Gmail 和 Brave)。
- 在 `README` 中包含專案結構。
- 虛擬環境已經設定好，並包含必要的依賴項。
- 使用 `python_dotenv` 和 `load_env()` 來處理環境變數。
