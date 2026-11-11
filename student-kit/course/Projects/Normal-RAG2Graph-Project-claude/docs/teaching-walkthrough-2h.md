# 互動教學 Walkthrough（進階版）

> **講師使用方式**：
> - 「🧑‍🎓 學生動手」= 學生跟著做，講師等
> - 「🎤 講師講述」= 學生停下來，講師講概念（已附逐字參考稿）
> - 「💬 互動提問」= 講師丟問題、收答案、引導討論
>
> **總時長**：約 120 分鐘
> **前置**：學生需有 Python 3.11+、Node 18+、`uv`、`GOOGLE_API_KEY`、git clone 好專案

---

## 🕐 段落 0｜開場與環境檢查（10 分鐘）

### 🎤 講師講述（5 min）

> 「今天我們不從零開始寫，這個專案已經寫好了，你們的任務是**跑起來、玩壞它、看出設計取捨**。
>
> 我們會跑兩個版本——main 分支是『土炮版 GraphRAG』，feature/semantic-graphrag 是『LangChain 標準版』。同一份 PDF 餵兩邊，你們會親眼看到差異在哪。
>
> 重點不是哪個比較好，是讓你們學會**從成品反推設計決策**——這才是工程師讀 codebase 該有的能力。」

### 🧑‍🎓 學生動手（5 min）

```bash
# 學生執行
cd Normal-RAG2Graph-Project
git checkout main
git pull
cd backend && uv sync
cd ../frontend && npm install
echo $GOOGLE_API_KEY  # 確認有值
```

**講師說**：「跑完跟我說 OK，我們等大家。」

---

## 🕐 段落 1｜跑起 naive 版 + 講 RAG 基礎（30 分鐘）

### 🧑‍🎓 學生動手（10 min）

```bash
# Terminal 1
cd backend
uv run uvicorn app.main:app --reload

# Terminal 2
cd frontend
npm run dev

# 瀏覽器打開 http://localhost:3000
# 上傳一份 PDF（建議用講師提供的同一份）
```

**講師說**：「上傳完、看到文件出現在列表，舉手讓我知道。等大家都好我才繼續。」

### 🎤 講師講述：什麼是 RAG（10 min）

> 「趁大家上傳的時候，我先講 RAG 是什麼。
>
> **RAG = Retrieval-Augmented Generation**，三個字拆開：
> - **Generation**：LLM 生答案。但 LLM 有兩個致命傷——一是訓練資料有 cutoff，二是會幻覺。
> - **Retrieval**：在生答案前，先從你的私有文件撈相關片段出來。
> - **Augmented**：把撈到的片段塞進 prompt，當作 LLM 的『開卷考試小抄』。
>
> 所以 RAG 的本質是『把 LLM 從閉卷考改成開卷考』。
>
> 那『相關片段』怎麼撈？這裡有個關鍵技術叫 **embedding**——把每段文字轉成一個高維向量（你們現在用的 Gemini embedding 是 768 維）。語意相近的文字，向量在空間裡會靠在一起。
>
> 撈的時候算 **cosine similarity**，找跟 query 向量最近的 top-K 個 chunk。
>
> **三個步驟記起來**：
> 1. **Ingestion**：文件 → 切 chunk → embedding → 存 Vector DB
> 2. **Retrieval**：query → embedding → 算相似度 → top-K chunks
> 3. **Generation**：top-K chunks + query → 塞給 LLM → 回答
>
> 你們現在跑的 `backend/app/rag_engine.py` 就是這三步。等下我們會打開來看。」

### 💬 互動提問（5 min）

> 「先問你們一題：如果 query 是『公司的財務長是誰』，文件裡寫『CFO 由 John 兼任』——向量檢索找得到嗎？」

**預期答案**：可能找不到，因為「財務長」跟「CFO」雖然語意接近但不一定夠近，要看 embedding 模型品質。

> 「再問一題：如果 query 是『A 跟 B 的關係』，向量檢索能告訴你『A 投資了 B』嗎？」

**引導學生發現**：向量檢索撈的是『**包含 A 和 B 的段落**』，但**關係本身**沒被結構化。這就是 GraphRAG 要解決的痛點。

### 🧑‍🎓 學生動手（5 min）

```
在 Chat 試問三個問題：
1. 「這份文件在講什麼？」（概覽型 → RAG 強項）
2. 「X 跟 Y 是什麼關係？」（關係型 → RAG 弱項）
3. 「這份文件的作者是誰？」（metadata 型 → 陷阱題）
```

**講師說**：「先把答案截圖存下來，等下對照組要比較。」

---

## 🕐 段落 2｜打開 code 看 naive GraphRAG 怎麼做（25 分鐘）

### 🎤 講師講述：為什麼要 GraphRAG（5 min）

> 「剛剛你們應該發現，第二題答案很爛。為什麼？因為 LLM 拿到的 chunk 裡，A 跟 B 各自被提到，但**關係**沒被明確抓出來。
>
> GraphRAG 的核心觀念是：在 ingestion 階段，**多做一步『實體與關係抽取』**，把『A —投資→ B』這種結構化資訊存到 Graph DB。
>
> Query 時就變成：
> 1. 向量檢索撈 top-K chunks（跟原本一樣）
> 2. **反查這些 chunks 裡有哪些 entity**
> 3. **把 entity 跟它的 relations 一起塞進 prompt**
>
> LLM 就有了『我在哪個 chunk』+『這個 chunk 裡有什麼實體跟關係』兩種視角。」

### 🧑‍🎓 學生動手（5 min）

```bash
# 學生用編輯器打開這 4 個檔案
backend/app/rag_engine.py        # naive 版引擎
backend/app/graph_db.py          # SQLite schema
backend/app/main.py              # FastAPI 路由
frontend/components/GraphView.tsx # 前端 force graph
```

**講師說**：「不要讀全部，等我帶大家看重點。」

### 🎤 講師講述：rag_engine.py 拆解（10 min）

> 「打開 `backend/app/rag_engine.py`，看三個關鍵段落：
>
> **第一段：Chunking**
> ```python
> RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
> ```
> 這是『**土炮切法**』——按字數硬切，不管語意。
> 一個完整的句子可能被攔腰斬斷。為什麼還要用？因為**簡單、可預測、便宜**。production 系統很多還在用這個。
>
> **第二段：Entity 抽取**
> ```python
> prompt = '請從以下文字抽出實體和關係...'
> response = gemini.generate(prompt)
> ```
> 這是『自寫 prompt』讓 LLM 抽 entity。問題：
> - entity type 全是字串自由發揮 → 後來都標成 'Unknown'
> - relation 是中文自由文字 → 沒辦法 query graph
> - 同一個 entity 在不同 chunk 出現，名稱可能不一樣 → 沒去重
>
> **第三段：存進 SQLite**
> 看 `graph_db.py` 的 5 張表：
> - `documents`：原始文件
> - `chunks`：切好的片段 + 它的 embedding ID
> - `entities`：抽出來的實體
> - `links`：實體之間的關係
> - `entity_chunks`：**關鍵的關聯表**——某個 entity 出現在哪些 chunk
>
> Query 時就靠 `entity_chunks` 從 chunk 反查 entity。這是 vector 跟 graph 兩個世界的橋樑。」

### 💬 互動提問（5 min）

> 「現在問你們：如果要把 SQLite 換成 Neo4j，這 4 個檔案哪幾個要改？」

**引導**：只有 `graph_db.py` 跟 `rag_engine.py` 裡寫 SQL 的部分要改。`main.py`（API 層）跟前端**完全不用動**——這就是好的抽象邊界。

> 「再問：entity type 全是 'Unknown' 有什麼壞處？」

**引導**：
- 前端沒辦法依 type 著色 → 視覺資訊量低
- 沒辦法做『只查 Person 類 entity』這種過濾
- 會跟 schema-based 的 Graph DB（如 Neo4j label）整合困難

---

## 🕐 段落 3｜切到對照組看 LangChain 怎麼做（30 分鐘）

### 🧑‍🎓 學生動手（5 min）

```bash
# 切分支
git checkout feature/semantic-graphrag

# 重啟後端（檔案不一樣了）
# Ctrl+C 停掉原本的 uvicorn，重跑
cd backend
uv sync  # 可能多了 langchain 等依賴
uv run uvicorn app.main:app --reload

# 前端不用動，refresh 瀏覽器
# 重新上傳同一份 PDF
```

**講師說**：「上傳中我來講 LangChain 在做什麼。」

### 🎤 講師講述：LangChain 標準堆疊（10 min）

> 「打開 `backend/app/semantic_rag_engine.py`，這版用 LangChain 兩個關鍵元件：
>
> **元件 1：SemanticChunker**
> ```python
> from langchain_experimental.text_splitter import SemanticChunker
> ```
> 切法不是按字數，是**按語意距離**：
> 1. 先把文章切成句子
> 2. 每個句子算 embedding
> 3. 相鄰句子算 cosine 距離
> 4. 距離大於 threshold 的地方 → 切點
>
> 結果：chunk 邊界落在『語意轉換』的地方，不會把一個完整概念切爛。
>
> **代價**：慢、貴（每句都要 embedding）、threshold 難調。
>
> **元件 2：LLMGraphTransformer**
> ```python
> LLMGraphTransformer(
>     llm=llm,
>     allowed_nodes=['Person', 'Organization', 'Concept', 'Event', 'Location', 'Document'],
>     allowed_relationships=['RELATES_TO', 'PART_OF', 'MENTIONS', ...]
> )
> ```
> 這叫 **schema-constrained extraction**——強迫 LLM 只能輸出 schema 裡有的 type。
>
> 為什麼重要？
> - entity type 不再是 'Unknown' → 前端可以依 type 著色
> - relation 不再是自由中文 → 可以做 graph traversal
> - 跨 chunk 的同名 entity 會被 merge → 自動去重
>
> 這就是『**有 schema 就有後續**』。沒 schema 等於只是把資料堆在那邊。」

### 🧑‍🎓 學生動手（10 min）

```
1. 上傳完成後，看右邊 graph：
   - 節點現在有顏色了（Person 藍、Org 橘、Concept 綠...）
   - 右下角看到 Legend
2. 試問段落 1 那三個問題（同一份 PDF、同樣問題）
3. 截圖三題答案
4. 把兩個版本的截圖並排，看差在哪
```

**講師說**：「跑完比較好兩邊差異，等下我們一起討論。」

### 💬 互動提問（5 min）

> 「跟 main 版比，哪題答案明顯變好？哪題沒變？」

**預期觀察**：
- 第 2 題（關係型）變好——因為 entity 跟 relation 都被結構化了
- 第 1 題（概覽型）差不多——因為這題本來向量檢索就夠
- 第 3 題（作者）兩邊都還是爛——這是下一段要講的彩蛋

> 「為什麼節點現在能著色？前端做了什麼？還是後端做了什麼？」

**引導**：前端只是收 `node.type` 然後 mapping 顏色。是**後端 schema-constrained extraction** 讓 type 變成有意義的值。**前端的好看，常常來自後端的結構化**。

---

## 🕐 段落 4｜SemanticChunker 失效 Case Study（20 分鐘）

### 🎤 講師講述：沒有銀彈（10 min）

> 「現在回到第 3 題——『這份文件的作者是誰？』兩個版本都答不好，為什麼？
>
> 想像一份論文 PDF：
> - 第一頁有 title、author、affiliation、abstract
> - 第二頁開始是 introduction
>
> **SemanticChunker 會怎麼切？**
> Title 跟 author 是名詞片段，跟 abstract 的句子語意距離很遠，**會被切成獨立 chunk**。
>
> 但這個獨立 chunk 太短、語意不完整，有兩個問題：
> 1. **embedding 品質差**：『John Smith, MIT, 2024』這種 chunk 的向量沒什麼語意可言
> 2. **LLMGraphTransformer 抓不到關係**：因為沒有上下文說明 John Smith 是『作者』，只是個名字
>
> 結果就是：query『作者是誰』→ 向量檢索撈不到 author chunk → LLM 沒小抄 → 瞎答。
>
> **這是教學重點**：
> - LangChain 標準堆疊**不是銀彈**
> - 越『聰明』的 chunking 策略，越容易在 metadata 類資料失效
> - 真正的 production RAG 系統要做 **specialized extractors**：
>   - PDF metadata 用 PyPDF2 直接抓
>   - Title / author 用 regex 或 LLM 單獨抽
>   - 表格用 table parser
>   - 然後**併入 main 索引**
>
> 一句話總結：**chunking 策略要看資料形態挑，沒有一種 chunking 適合所有資料**。」

### 💬 互動討論（10 min）

開放討論題：

1. **「你們公司/工作上的文件是哪一種？適合 naive 還是 semantic？」**
   - 合約 → 條款結構固定，naive 切法 + section 偵測可能更好
   - 技術文件 → semantic 適合
   - 財報 → 表格多，兩者都不夠，要 specialized parser
   - 客服 FAQ → 短文居多，naive 就夠

2. **「如果讓你修這個 codebase 讓它能答『作者是誰』，你會怎麼改？」**
   - 加 PDF metadata extractor
   - 第一頁強制獨立處理
   - 加一個 'document_metadata' entity type

3. **「你會選哪個版本上 production？為什麼？」**
   - 沒有標準答案，重點是讓學生說出 trade-off

---

## 🕐 段落 5｜架構回顧 + 3 個 Takeaway（10 分鐘）

### 🎤 講師講述（10 min）

> 「最後 10 分鐘做總整理。
>
> **回顧這 2 小時你們學了什麼**：
>
> 1. **RAG 三步驟**：Ingestion → Retrieval → Generation
> 2. **GraphRAG = RAG + 多做一步 entity/relation 抽取**
> 3. **vector DB 跟 graph DB 怎麼黏起來**：靠 entity_chunks 關聯表
> 4. **chunking 策略決定一切**：naive vs semantic 各有適用場景
> 5. **schema-constrained extraction 的價值**：不是約束 LLM，是讓下游能用
> 6. **沒有銀彈**：每個技術選擇都有它的失效模式
>
> **帶走這 3 個觀念，今天就值了**：
>
> 🎯 **Takeaway 1：GraphRAG 不是新的 DB，是兩個 DB 的整合架構**
> 不要被名字騙了，去拆它的資料流。
>
> 🎯 **Takeaway 2：Chunking 是 RAG 系統最被低估的設計決策**
> 90% 的 RAG 品質問題，根源在 chunking 沒選對。
>
> 🎯 **Takeaway 3：讀 codebase 要從『失效模式』反推設計**
> 看一個系統不是看它做對什麼，是看它**故意不做什麼**——那才是設計者的取捨。
>
> **回家作業（自選）**：
> - 換一份你工作上的真實文件，跑兩個版本，看哪個適合
> - 試著修 code 讓它能答 metadata 類問題
> - 把 SQLite 換成 Neo4j（會發現要改的東西比想像少）
>
> 有問題嗎？」

---

## 📋 講師備課 Checklist

### 前一晚準備
- [ ] 確認兩個分支都能跑（main + feature/semantic-graphrag）
- [ ] 準備一份 PDF 給所有學生用（建議：論文、技術文件，**有 metadata** 的）
- [ ] 預先 ingest 一遍，存截圖當備案（萬一現場 LLM 卡住）
- [ ] 準備 3 個示範問題，自己先跑過確認結果

### 現場開場前
- [ ] 確認所有學生都能 git clone、`uv sync`、`npm install`
- [ ] 把 PDF 用 AirDrop / USB / 雲端發給學生
- [ ] 白板/投影幕準備好，待會要畫資料流圖

### 救場彈藥（學生卡住時）
- [ ] `uv sync` 失敗 → `uv cache clean` 重來
- [ ] Chroma 錯誤 → `rm -rf backend/local_chromadb` 重新上傳
- [ ] CORS 錯 → 確認 backend `allow_origins=['*']`
- [ ] LLM 沒回應 → 確認 `GOOGLE_API_KEY`、檢查 quota

---

## 🕐 時間表總覽

| 段落 | 時長 | 內容 | 學生狀態 |
|---|---|---|---|
| 0 | 10 min | 開場 + 環境檢查 | 動手 setup |
| 1 | 30 min | 跑 naive 版 + 講 RAG 基礎 | 動手 + 聽講 |
| 2 | 25 min | 拆解 naive code | 看 code + 聽講 |
| 3 | 30 min | 切對照組 + 講 LangChain | 動手 + 聽講 |
| 4 | 20 min | SemanticChunker 失效討論 | 聽講 + 討論 |
| 5 | 10 min | 總結 + Takeaway | 聽講 + Q&A |
| **總計** | **125 min** | | |

> 留 5 分鐘 buffer 給現場意外。實際走完約 2 小時。
