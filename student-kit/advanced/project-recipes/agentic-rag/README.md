# AgenticRAG：先看懂路由、評分與停止條件

對應講義附錄 B 的 Agentic RAG、CRAG、Adaptive RAG。講義指名的三份 `.ipynb` 沒有在本次提供的五個來源 Repo 中找到，本包不假裝已收錄那些 notebooks。

本目錄的 `rag-flow.py` 是依講義流程另外寫的離線控制流程教材：沒有 LangGraph、沒有 Claude Agent SDK、沒有向量資料庫，也不會連外。固定規則模擬「相關性判斷」，固定文件模擬檢索結果；它不是 LLM 品質測試。

## 執行

Python 3.9+，標準函式庫，從本 Repo 根目錄：

```bash
python3 advanced/project-recipes/agentic-rag/rag-flow.py hooks
python3 advanced/project-recipes/agentic-rag/rag-flow.py 自動化
python3 advanced/project-recipes/agentic-rag/rag-flow.py 天氣
```

預期分別看見：

1. `retrieve → grade → generate`，答案帶文件 ID。
2. 首次檢索無結果，`rewrite` 成 hooks 後命中；最多重寫一次。
3. 兩次查不到後 `stop`，回覆沒有足夠證據，不自行編造答案。

## 換成真正 AgenticRAG 時的工作

| 本練習 | 真實系統要替換的部分 |
|---|---|
| 固定文件字典 | 切分、embedding、向量檢索與文件版本 |
| 關鍵字命中 | 相關性評分器，需獨立評估漏判/誤判 |
| 固定 rewrite 規則 | 問題重寫模型與最大重試次數 |
| 直接回傳文件內容 | 生成模型、逐項證據引用與答案驗證 |
| 找不到就停止 | 若做 CRAG，可改有來源的 web search fallback |

作業：把三條路徑的 trace 記錄下來，說明為何需要最大迴圈次數。進階再對照講義補齊 LangGraph 節點、結構化評分與成本限制；補到真正 notebook 前，不要宣稱已跑通講義原版。

驗收界線：本包驗證這三條離線控制路徑；模型回答品質、檢索召回率與真實 SDK 整合都待另外驗證。
