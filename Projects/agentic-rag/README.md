# Agentic RAG：同一間餐廳，三種查資料的方法

為簡報附錄 B 新寫的三本實作。情境是一間**虛構**餐廳：菜單在本地文件；天氣通常需要外部來源；找不到停車資料就應該拒答。每本都可以單獨開啟，不需要先跑前一本。

| 順序／投影片 | 直接開 Colab | 從哪裡看出方法不同？ |
|---|---|---|
| 1．Agentic RAG | [執行第一本](https://colab.research.google.com/github/kevin801221/claude-course-code/blob/main/Projects/agentic-rag/LangGraph_Agentic%20RAG%20%E7%AF%87.ipynb) | 「你好」直接回答；「幾點打烊」第一次查不到，改寫成「營業時間」再查。 |
| 2．CRAG | [執行第二本](https://colab.research.google.com/github/kevin801221/claude-course-code/blob/main/Projects/agentic-rag/LangGraph-CRAG%20%E7%AF%87.ipynb) | 每題先查本地。菜單命中；天氣找不到，才改寫並轉外部搜尋。 |
| 3．Adaptive RAG | [執行第三本](https://colab.research.google.com/github/kevin801221/claude-course-code/blob/main/Projects/agentic-rag/LangGraph_-Adaptive-RAG%20%E7%AF%87.ipynb) | 入口先選來源；出口分開檢查「證據支持」和「答到問題」，兩種錯誤會走不同的修正路線。 |

**第一輪不需要金鑰。** 在 Colab 選「執行階段 → 全部執行」；第一次需要連網安裝套件。看最後的節點順序、答案、來源 ID，再改一筆文件或題目重跑。本機取得相依套件後亦可離線執行。

### 實作與投影片怎麼對照？

- 圖中的節點、條件邊與迴圈都以真正的 LangGraph 執行。知識庫是數筆資料組成的稀疏向量索引，以餘弦相似度檢索。為讓全班可重現相同分支，預設的決策與評分器使用明示的詞彙規則，並非 LLM。精確引文檢查能抓本實驗設定的錯誤，不能用來宣稱一般文字都沒有幻覺。
- CRAG／Adaptive 的預設 Web Search 是固定外部樣本，**不是即時網路或真實預報**。CRAG 最後一格可選用自己的 Tavily key，切換成真正的網路搜尋；請對照回傳來源。連線若被封鎖或額度不足，關掉該格的開關，其他步驟仍可跑。
- 第一頁講到的 LangChain `model.bind_tools` 是另一種工具綁定介面。本資料夾的真模型版本用 **Claude Agent SDK** 的 `@tool` 與 `create_sdk_mcp_server` 註冊唯讀查詢工具；實際呼叫紀錄與來源引文比對方式見下方。這三本是課程版，不是其他教材的原始 notebook。

### 本機依序執行（Python 3.12）

從 repo 根目錄開始：

```bash
cd Projects/agentic-rag
python3.12 -m venv .venv
source .venv/bin/activate
# Windows PowerShell 改用：.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python verify_notebooks.py
```

看到三行 `PASS` 以及每條實際的節點軌跡。驗收會為每本啟用新 kernel，不寫回輸出或修改 notebook。要逐格操作本機介面：

```bash
python -m pip install jupyterlab==4.6.6
python -m jupyterlab
```

### 選做：讓真正的 Claude 決定要不要查

先跑不連線的自我檢查，確認 SDK、MCP 工具和引文驗證在本機能用：

```bash
python -m pip install -r requirements-live.txt
python live_sdk.py --self-check
```

準備好自己的 Anthropic API key 並透過環境變數 `ANTHROPIC_API_KEY` 提供給程式。**不要**把金鑰寫入 notebook 或提交到 Git。以下會連線、有模型用量；無金鑰不會送出請求。

```bash
python live_sdk.py --live --question "這間餐廳幾點打烊？"
python live_sdk.py --live --question "你好"
```

真人操作時，比較兩輪印出的「實際工具回報的來源」。LangGraph 先進入 SDK 節點，Claude 自行決定是否呼叫資料工具，下一個節點只接受實際取得且逐字匹配的引文；驗證失敗時會拒答。問候則可以直接回答。付費連線不包含在預設驗收中；模型不一定每次都走同一條路線。

延伸文件：[LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)、[Claude Agent SDK Python](https://code.claude.com/docs/en/agent-sdk/python)、[Tavily Search](https://docs.tavily.com/documentation/api-reference/endpoint/search)。
