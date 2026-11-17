# Batch Wiki Ingest Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 批量 ingest `raw/` 中尚未處理的 23 份 JSON，更新 `wiki/` 的 sources、concepts、entities、synthesis、index、log、overview 與 graph。

**Architecture:** 以 Python 腳本批次解析 `raw/*.json`，從 `episode/podcast_name/date/insights[]` 萃取來源頁、概念頁、實體頁與 synthesis 所需資料。既有頁面不整頁覆蓋，而是保留原有內容、合併 frontmatter `sources`，並刷新自動生成的補充與相關頁面區塊。

**Tech Stack:** Python 3、標準函式庫、Markdown frontmatter parsing、自訂規則式 entity/concept 萃取、既有 `wiki/graph_builder.py`

### Task 1: 批次 ingest 腳本與測試

**Files:**
- Create: `wiki/batch_ingest.py`
- Create: `wiki/test_batch_ingest.py`

**Step 1: 寫待處理檔案與抽取規則測試**

驗證：
- 排除已處理的 3 份來源與 `_cross_summary.json`
- 實際待 ingest 檔案數為 23
- 代表性內容能正確對應到 canonical concept/entity

**Step 2: 跑測試確認失敗**

Run: `python3 -m unittest wiki/test_batch_ingest.py -v`

**Step 3: 寫最小批次 ingest 實作**

包含：
- 發現 pending raw 檔案
- 解析 `insights[]`
- 生成 source/concept/entity/synthesis 資料模型
- 合併既有 frontmatter `sources`

**Step 4: 跑測試確認通過**

Run: `python3 -m unittest wiki/test_batch_ingest.py -v`

### Task 2: 寫入 wiki 頁面與索引

**Files:**
- Modify: `wiki/index.md`
- Modify: `wiki/log.md`
- Modify: `wiki/overview.md`
- Modify/Create: `wiki/sources/*.md`
- Modify/Create: `wiki/concepts/*.md`
- Modify/Create: `wiki/entities/*.md`
- Create: `wiki/synthesis/AI供應鏈投資脈絡.md`
- Create: `wiki/synthesis/2026Q1市場共識與分歧.md`
- Create: `wiki/synthesis/交易心法彙整.md`

**Step 1: 先用腳本在工作目錄產生完整結果**

Run: `python3 wiki/batch_ingest.py`

**Step 2: 檢查新增與更新頁面是否符合 CLAUDE.md**

檢查：
- frontmatter 欄位齊全
- `[[頁面名稱]]` 交叉連結存在
- log 為 append-only
- index 頁數與實際頁數一致

### Task 3: 驗證 graph 與最終結果

**Files:**
- Modify: `wiki/graph.html`

**Step 1: 重新生成 graph**

Run: `python3 wiki/graph_builder.py`

**Step 2: 驗證測試與關鍵輸出**

Run:
- `python3 -m unittest wiki/test_graph_builder.py -v`
- `python3 -m unittest wiki/test_batch_ingest.py -v`

**Step 3: 驗證重點檔案**

檢查：
- `wiki/index.md`
- `wiki/log.md`
- `wiki/overview.md`
- 三份 synthesis 頁
- `wiki/graph.html`
