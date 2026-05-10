# LLM Wiki Graph README

這份 README 是這個專案目前實際運作流程的完整重建說明。
目標不是解釋理想狀態，而是把「這個 repo 是怎麼被建立、怎麼 ingest、怎麼長出 graph、怎麼維護」全部寫清楚，讓之後可以照著重做。

## 1. 專案目的

這個 repo 的核心目標是：

- 把 `raw/` 裡的原始 JSON 文件整理成可累積的 wiki
- 把知識拆成 `source / concept / entity / synthesis`
- 用 `[[頁面名稱]]` 交叉連結形成知識圖
- 再把這些圖元素輸出成可互動的 `wiki/graph.html`

資料流方向是固定的：

`raw/*.json` → `wiki/sources/*.md` → `wiki/concepts/*.md`、`wiki/entities/*.md`、`wiki/synthesis/*.md` → `wiki/index.md`、`wiki/overview.md`、`wiki/log.md` → `wiki/graph.html`

## 2. 必須遵守的規則

這些規則來自 [CLAUDE.md](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/CLAUDE.md)，目前整個 repo 都照這個 schema 在跑：

- 只能寫 `wiki/`
- 永遠不修改 `raw/`
- 所有內容一律使用繁體中文
- 每個 wiki 頁面都必須有 YAML frontmatter
- frontmatter 欄位固定為：

```yaml
---
title: 頁面標題
type: concept | entity | source | overview | synthesis
tags: [標籤1, 標籤2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [來源檔名1, 來源檔名2]
---
```

- 內文交叉連結一律用 `[[頁面名稱]]`
- 每頁最後都要有 `## 相關頁面`
- `wiki/log.md` 是 append-only，不能回頭改舊紀錄

## 3. 目前目錄結構

```text
llm-wiki-graph/
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── raw/
│   ├── *.json
│   └── _cross_summary.json
├── docs/
│   └── plans/
└── wiki/
    ├── index.md
    ├── log.md
    ├── overview.md
    ├── batch_ingest.py
    ├── graph_builder.py
    ├── test_batch_ingest.py
    ├── test_graph_builder.py
    ├── graph.html
    ├── concepts/
    ├── entities/
    ├── sources/
    └── synthesis/
```

## 4. `raw/` JSON 格式

目前 ingest 腳本假設每份原始文件長這樣：

```json
{
  "episode": "節目標題",
  "podcast_name": "節目名稱",
  "date": "YYYY-MM-DD",
  "insights": [
    {
      "type": "strategy | macro | sector | stock | personal",
      "content": "重點敘述",
      "tickers": ["2330.TW", "NVDA"],
      "key_points": ["補充重點1", "補充重點2"]
    }
  ]
}
```

目前腳本會特別跳過：

- `_cross_summary.json`

## 4.1 Python 與套件管理

這個 repo 現在已統一改成用 `uv` 啟動與維護 Python 環境。

目前設定檔是：

- [pyproject.toml](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/pyproject.toml)

目前專案本身沒有額外第三方依賴，主要使用 Python 標準函式庫，但之後如果要加套件，也一律用 `uv` 管理。

第一次進 repo 時，先跑：

```bash
uv sync
```

如果之後需要安裝新套件：

```bash
uv add 套件名
```

如果要移除套件：

```bash
uv remove 套件名
```

如果只是臨時跑某個 Python 指令或腳本，一律用：

```bash
uv run python ...
```

## 5. 一開始怎麼初始化 wiki

最初初始化的實際步驟如下：

1. 先讀 [CLAUDE.md](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/CLAUDE.md)，確認 schema 和 SOP。
2. 確認 `raw/` 存在。
3. 建立 `wiki/` 與子目錄：
   - `wiki/concepts/`
   - `wiki/entities/`
   - `wiki/sources/`
   - `wiki/synthesis/`
4. 建立基本頁面：
   - `wiki/index.md`
   - `wiki/log.md`
   - `wiki/overview.md`
5. 建一個示範概念頁，確認 frontmatter、標題、摘要、相關頁面格式正確。

如果你要從零重做一份空 wiki，可以用這個概念初始化：

```bash
uv run python - <<'PY'
from pathlib import Path
for path in ["wiki/concepts", "wiki/entities", "wiki/sources", "wiki/synthesis"]:
    Path(path).mkdir(parents=True, exist_ok=True)
PY
```

然後再依 CLAUDE schema 建 `index.md`、`log.md`、`overview.md`。如果是新環境，請先跑一次 `uv sync`。

## 6. 單份 ingest 的原始流程

最前面 3 份來源是半手動 ingest，流程如下：

1. 先讀指定的 `raw/*.json`
2. 從 `insights` 摘出 2 到 3 個主軸
3. 先和使用者確認主軸方向
4. 建 `wiki/sources/` 的摘要頁
5. 補或更新對應的 `wiki/concepts/`
6. 補或更新對應的 `wiki/entities/`
7. 更新 `wiki/index.md`
8. 在 `wiki/log.md` 追加 ingest 紀錄
9. 更新 `wiki/overview.md`

這 3 份已處理來源是：

- `2023-10-27_財經_Podcast_財經_Podcast_EPXXX.json`
- `2026-02-12_游庭皓的財經皓角__市場觀察_2026_台灣人如何迎接_少子化海嘯_.json`
- `2026-02-13_游庭皓的財經皓角__市場觀察_2026台灣人如何_迎接AI時代_.json`

## 7. 為什麼後來做成批次 ingest

CLAUDE.md 的 SOP 預設是一次 ingest 一份，但後來因為使用者明確要求批量 ingest，所以把流程腳本化，整理成 [wiki/batch_ingest.py](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/batch_ingest.py)。

這支腳本做的事不是單純新增檔案，而是「全量更新 wiki 的知識狀態」。

## 8. `batch_ingest.py` 的實際工作內容

`batch_ingest.py` 目前的流程是：

1. 掃描 `raw/*.json`
2. 跳過 `_cross_summary.json`
3. 讀出每份已處理 wiki 頁面的 `sources:` frontmatter
4. 找出尚未 ingest 的 raw 檔案
5. 如果有 pending，就只 ingest pending
6. 如果沒有 pending，就退回全量重建模式，掃描全部 raw 檔
7. 對每份 raw：
   - 讀 JSON
   - 建 source record
   - 提取概念與實體
   - 寫 source page
   - 聚合 concept notes / entity notes
8. 寫回 concept pages
9. 寫回 entity pages
10. 自動建立 3 個 synthesis pages
11. 重建 `overview.md`
12. 重建 `index.md`
13. append `log.md`

## 9. `batch_ingest.py` 的關鍵內部規則

### 9.1 Pending 判定

腳本不是靠檔名比對目錄，而是靠所有 wiki 頁面 frontmatter 裡的 `sources:` 來判斷某份 raw 是否已經被處理過。

對應函式：

- `read_existing_sources(...)`
- `discover_pending_raw_files(...)`

### 9.2 Source title override

因為前 3 份來源是先手動建立的，後來批次腳本為了避免標題漂移，加入了固定標題覆寫：

- `財經 Podcast EP.XXX`
- `市場觀察 2026 台灣人如何迎接少子化海嘯`
- `市場觀察 2026 台灣人如何迎接AI時代`

對應常數：

- `SOURCE_TITLE_OVERRIDES`

### 9.3 Entity 抽取邏輯

實體不是只建公司，也會建：

- 人物
- 技術
- 事件
- 節目
- 股票代號

來源包括：

- `insight["tickers"]`
- 標題中的來賓名稱
- 文字中出現的已知別名
- ticker 對應名稱覆寫

對應規則：

- `TICKER_OVERRIDES`
- `ENTITY_CATALOG`
- `extract_participants(...)`
- `extract_entities_and_concepts(...)`

### 9.4 Concept 抽取邏輯

概念頁不是每個 insight 各建一頁，而是透過一份概念目錄把相近敘事收斂到同一頁。

例如：

- `AI 驅動的台灣產業升級`
- `CPO 與矽光子`
- `先進封裝與封測供應鏈`
- `台股反彈與風險管理`
- `事件後應對投資法`

對應規則：

- `CONCEPT_CATALOG`
- `FALLBACK_CONCEPTS`

### 9.5 已存在頁面是更新，不是覆蓋

`write_page(...)` 的策略是：

- 保留舊頁的 `created`
- 合併 `tags`
- 合併 `sources`
- 保留手動編輯內容
- 自動更新 `updated`
- 自動重寫 `來源補充`
- 自動重寫 `## 相關頁面`

對應的關鍵設計：

- 用 `<!-- AUTO-INGEST START -->` / `<!-- AUTO-INGEST END -->` 包住自動區塊
- 手動區塊與自動區塊分離

### 9.6 Source page 命名

source page 的檔名預設來自 raw 檔名，而不是 title。

對應函式：

- `build_source_filename(...)`
- `get_page_path(...)`

這樣做的好處是：

- 同名標題不容易覆蓋
- 可以穩定回指原始檔案

### 9.7 Index / Overview 重建

`index.md` 與 `overview.md` 不是手工維護，而是由腳本重建：

- `rebuild_index(...)`
- `rebuild_overview(...)`

重建時會：

- 掃描 `concepts/ entities/ sources/ synthesis/ overview.md`
- 以 frontmatter `title` 去重
- 用頁面摘要生成索引簡述

### 9.8 Synthesis 頁面

每次完整 batch ingest 後，腳本會產出 3 個 synthesis 頁面：

- [AI供應鏈投資脈絡.md](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/synthesis/AI供應鏈投資脈絡.md)
- [2026Q1市場共識與分歧.md](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/synthesis/2026Q1市場共識與分歧.md)
- [交易心法彙整.md](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/synthesis/交易心法彙整.md)

這部分對應：

- `create_synthesis_pages(...)`

## 10. 目前實際用來重建 wiki 的指令

### 10.1 批次 ingest 尚未處理的 raw

```bash
uv run python wiki/batch_ingest.py
```

這支腳本會：

- ingest pending raw
- 更新 concepts / entities / sources
- 重建 synthesis / overview / index / log

### 10.2 重新生成 graph

```bash
uv run python wiki/graph_builder.py
```

這支腳本會輸出：

- [wiki/graph.html](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/graph.html)

### 10.3 跑測試

```bash
uv run python -m unittest wiki/test_batch_ingest.py -v
uv run python -m unittest wiki/test_graph_builder.py -v
```

## 11. `graph_builder.py` 是怎麼長出 graph 的

[wiki/graph_builder.py](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/graph_builder.py) 目前做的事有：

1. 掃描這些頁面：
   - `wiki/overview.md`
   - `wiki/concepts/*.md`
   - `wiki/entities/*.md`
   - `wiki/sources/*.md`
   - `wiki/synthesis/*.md`
2. 解析 frontmatter
3. 抓正文中的 `[[頁面名稱]]`
4. 建立 graph nodes
5. 建立 graph links
6. 額外把 `raw/*.json` 也做成 raw nodes
7. 用 wiki 頁面的 `sources:` frontmatter 把 raw 連回對應頁面
8. 從 markdown 第一段擷取 `summary`
9. 產出單檔 HTML

## 12. `graph.html` 目前有哪些互動能力

目前的 [wiki/graph.html](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/graph.html) 已經有這些功能：

- 點節點看摘要卡片
- 卡片顯示：
  - `summary`
  - `type`
  - `path`
  - `tags`
  - `neighbors`
- 可以搜尋節點
- 可以拖曳節點
- 可以拖曳空白處平移
- 可以滾輪縮放
- 可以重置
- 可以顯示或隱藏 `raw` 節點
- 可以用 `間距` 滑桿把群組拉開
- 可以 `暫停 / 啟動`
- 可以 `重新排版`

## 13. 為什麼 graph 一開始會亂動，後來怎麼修

一開始的 graph 問題是：

- 所有節點同時進 force simulation
- `raw + source + concept + entity + synthesis` 全擠在一起
- 沒有明確收斂停止條件

後來修成現在這樣：

1. `raw` 預設隱藏
2. simulation 會自動收斂後停止
3. 不同 type 先分群擺位
4. 群內半徑放大
5. 加入節點碰撞推開
6. 加入間距滑桿

## 14. 這個 repo 曾經踩過的坑

### 14.1 曾經誤建 `wiki/entitys/`

早期批次腳本一度把 entity 寫到錯誤的 `wiki/entitys/`。
後來已修正路徑邏輯，正式目錄只保留：

- [wiki/entities](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/entities)

錯誤目錄已清除。

### 14.2 Source title 與 source filename 不同

這不是 bug，是刻意的：

- title 用來當 wiki 頁面名稱
- filename 用來穩定對應 raw 檔案

所以 `wiki/sources/` 裡可能同時看到：

- 標題比較漂亮的頁面名稱
- 檔名還保留 raw stem 的來源頁

索引與 graph 會以 frontmatter `title` 做去重與展示。

## 15. 如果要從現在這個 repo 重新跑一次完整流程

建議順序：

1. 確認 [CLAUDE.md](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/CLAUDE.md)
2. 確認 `raw/` 裡的 JSON 是你要 ingest 的集合
3. 執行：

```bash
uv run python wiki/batch_ingest.py
```

4. 再執行：

```bash
uv run python wiki/graph_builder.py
```

5. 驗證：

```bash
uv run python -m unittest wiki/test_batch_ingest.py -v
uv run python -m unittest wiki/test_graph_builder.py -v
```

6. 打開：
   - [wiki/index.md](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/index.md)
   - [wiki/overview.md](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/overview.md)
   - [wiki/log.md](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/log.md)
   - [wiki/graph.html](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/graph.html)

## 16. 如果要新增下一批 raw，正確順序是什麼

1. 把新 JSON 放進 `raw/`
2. 不要改舊的 `wiki/` 頁面
3. 跑：

```bash
uv run python wiki/batch_ingest.py
uv run python wiki/graph_builder.py
```

4. 檢查 `index.md`、`overview.md`、`log.md`
5. 跑測試
6. 再打開 graph 看節點是否正常連上

## 17. 如果要手動修改 wiki 頁面，什麼可以改、什麼不要改

可以改：

- `# 標題` 下方的人手摘要
- 補充說明段落
- 你自己想加入的分析內容

不要手改：

- frontmatter 基本結構
- `sources:` 裡已存在的來源紀錄
- `<!-- AUTO-INGEST START --> ... <!-- AUTO-INGEST END -->`
- `log.md` 舊紀錄

因為下次 batch ingest 時，自動區塊會被重寫。

## 18. 目前這個 repo 的核心腳本

- [wiki/batch_ingest.py](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/batch_ingest.py)
- [wiki/graph_builder.py](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/graph_builder.py)
- [wiki/test_batch_ingest.py](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/test_batch_ingest.py)
- [wiki/test_graph_builder.py](/Users/kevinluo/google-agent-ecosystem/llm-wiki-graph/wiki/test_graph_builder.py)

## 19. 一句話版本

如果你之後又忘記，最短版就是：

1. `raw/` 放原始 JSON
2. `uv sync`
3. `uv run python wiki/batch_ingest.py`
4. `uv run python wiki/graph_builder.py`
5. 看 `wiki/index.md`、`wiki/overview.md`、`wiki/log.md`、`wiki/graph.html`
6. 跑兩個 unittest

這就是目前整個 LLM Wiki Graph 的可重建流程。
