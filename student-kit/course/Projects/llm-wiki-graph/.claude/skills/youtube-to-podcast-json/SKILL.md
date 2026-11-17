---
name: youtube-to-podcast-json
description: 把 YouTube URL 轉成符合本 wiki repo schema 的 podcast JSON，再倒進 raw/ 由 batch_ingest.py 寫成 wiki/sources/ 頁面。Use when the user wants to ingest YouTube content, or says「ingest YouTube」「下載 podcast」「YouTube to wiki」「把這支影片整理進 wiki」.
---

# YouTube → Podcast JSON → Wiki Sources

這個 skill 是 **llm-wiki-graph 接 YouTube 內容的入口**。完整 pipeline 已實作在 `~/google-agent-ecosystem/stockclaw-backend/app/podcast.py`，本 skill 教 Claude Code 怎麼**用它**而不是重新實作。

## 完整概念跟工具鏈

詳細教學見：
**`~/google-agent-ecosystem/Antigravity-work/Normal-RAG2Graph-Project-claude/docs/YOUTUBE-PODCAST-PIPELINE.md`**

包含：
- youtube-transcript-api（字幕首選）vs yt-dlp + Whisper（音訊備援）的設計
- yt-dlp 反爬 player_client 設定
- ffmpeg `-c copy` 切片不 re-encode 的關鍵
- Groq vs OpenAI Whisper 權衡
- Gemini JSON mode 萃取 prompt 設計
- JSON schema 完整定義

第一次接這套 pipeline，**先讀那份文件**再動手。

## 在本 repo 的工作流程

### 0. 啟動後端服務

```bash
cd ~/google-agent-ecosystem/stockclaw-backend
./run.sh
# 確認 http://localhost:8088 起來
```

### 1. 健康檢查

```bash
curl -s http://localhost:8088/api/podcast/youtube_health | jq
```

確認 `ready: true`、所需 API key 都設好。**重點檢查項**：

| 欄位 | 期望 | 沒有時 |
|---|---|---|
| `youtube_transcript_api` | true | `uv add youtube-transcript-api` |
| `yt_dlp` | true | `uv add yt-dlp` |
| `ffmpeg` | true | `brew install ffmpeg`（>30min 影片必要） |
| `groq_api_key_set` 或 `openai_api_key_set` | true | 設環境變數 |
| `gemini_api_key_set` | true | 設 `GOOGLE_API_KEY` |

### 2. Ingest YouTube URL

```bash
curl -X POST http://localhost:8088/api/podcast/ingest_youtube \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtu.be/<video_id>",
    "podcast_name": "（覆寫節目名）",
    "episode": "（覆寫集數標題）",
    "use_gemini": true
  }' | jq
```

回應會有：
- `saved_to`: 寫到 `~/google-agent-ecosystem/stockclaw-backend/data/podcasts/<date>_<slug>.json`
- `extraction_mode`: `"gemini"` 或 `"fallback"`
- `summary`、`main_topics`、`tickers`、`sectors`

### 3. 把 JSON 倒進本 wiki repo 的 raw/

```bash
cp ~/google-agent-ecosystem/stockclaw-backend/data/podcasts/<date>_<slug>.json \
   ~/google-agent-ecosystem/llm-wiki-graph/raw/
```

或一次倒所有新檔（rsync）：

```bash
rsync -av --update \
  ~/google-agent-ecosystem/stockclaw-backend/data/podcasts/ \
  ~/google-agent-ecosystem/llm-wiki-graph/raw/
```

### 4. 跑本 repo 的 batch_ingest.py 整理成 wiki 頁

```bash
cd ~/google-agent-ecosystem/llm-wiki-graph
uv run python wiki/batch_ingest.py
```

它會：
- 對每份 `raw/*.json` 確認 `wiki/sources/` 有沒有對應頁
- 沒有就用 LLM 寫一頁 markdown 摘要、含 frontmatter
- 同步更新 `wiki/index.md` 跟 `wiki/log.md`
- 涉及到的 entity / concept 頁面也會被建立或更新

### 5.（選用）跑 graph_builder.py 重生 graph.html

```bash
uv run python wiki/graph_builder.py
# 開 wiki/graph.html 看 wiki-link 網絡圖
```

## JSON Schema（產出）

跟本 repo `raw/*.json` 既有 schema 一致：

```json
{
  "podcast_name": "...",
  "episode": "...",
  "date": "YYYY-MM-DD",
  "note": "（一句話節目重點）",
  "summary": "...",
  "main_topics": ["..."],
  "insights": [
    {
      "type": "stock | sector | macro | event | strategy",
      "content": "...",
      "tickers": ["2330", "NVDA"],
      "sectors": ["AI 伺服器"],
      "key_points": ["..."]
    }
  ],
  "_video_id": "...",
  "_video_url": "...",
  "_transcript_language": "zh-TW",
  "_transcript_chars": 12345,
  "_ingested_at": "...",
  "_extraction_mode": "gemini"
}
```

## 一鍵 alias（進階）

如果你常做這套流程，可以加 shell alias：

```bash
# ~/.zshrc 或 ~/.bashrc
youtube-to-wiki() {
  curl -sX POST http://localhost:8088/api/podcast/ingest_youtube \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"$1\"}" | jq -r .saved_to | xargs -I {} cp {} \
    ~/google-agent-ecosystem/llm-wiki-graph/raw/
  cd ~/google-agent-ecosystem/llm-wiki-graph
  uv run python wiki/batch_ingest.py
}
```

用：`youtube-to-wiki "https://youtu.be/xxx"`

## 環境變數（快速 reference）

| 變數 | 必要？ | 用途 |
|---|---|---|
| `GROQ_API_KEY` | 推薦 | Whisper（字幕 fallback） |
| `OPENAI_API_KEY` | Groq 替代 | Whisper |
| `GOOGLE_API_KEY` | 推薦 | Gemini 萃取 + batch_ingest 寫 wiki |

申請：
- Groq: https://console.groq.com/keys（免費 + 快 10x）
- Gemini: https://aistudio.google.com/apikey
- OpenAI: https://platform.openai.com/api-keys

## 常見錯誤

| 症狀 | 解法 |
|---|---|
| `yt-dlp 下載失敗：Sign in to confirm` | `uv add yt-dlp@latest` 升版 |
| `Whisper API 失敗：rate_limit` | Groq 額度用完，等一小時或切 OpenAI |
| `Gemini 回應非合法 JSON` | 已有 sanitize；持續發生重啟 service |
| `音檔超過 25MB 上限需切片，但找不到 ffmpeg` | `brew install ffmpeg` |

## 對應 code（debug 時看）

- 主入口：`stockclaw-backend/app/podcast.py:688` (`ingest_youtube`)
- 字幕路徑：`podcast.py:288` (`_fetch_via_subtitles`)
- 音訊路徑：`podcast.py:567` (`_fetch_via_whisper`)
- Gemini 萃取：`podcast.py:634` (`_gemini_extract`)
- Wiki 整理：`llm-wiki-graph/wiki/batch_ingest.py`

## 設計哲學

「**先試免費快慢精度低的路徑（字幕）、失敗才走貴慢精度高（音訊+Whisper）**」是這套 pipeline 的核心設計，也是任何 LLM agentic pipeline 應該採用的「cost-tier」哲學。詳見 PIPELINE 文件最後一節。
