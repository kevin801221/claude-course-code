# YouTube Podcast → JSON → Wiki 完整流水線教學

> 從 YouTube URL 一路到 LLM-wiki-graph 風格的 wiki/sources/ 頁面，完整工具鏈解釋、權衡與真實 code 對位。

## 為什麼要關心這條 pipeline？

你想累積一份**自動長大**的 podcast 知識庫——每集 ingest 進來時：

1. 自動抓 transcript（字幕優先、音訊備援）
2. 自動萃取結構化 insights（含股票代號、產業、key points）
3. 寫成 JSON 進 raw/
4. 由 wiki agent 整理成 markdown 頁進 wiki/sources/
5. 跨 episode 綜合分析（共識 / 矛盾 / 時間軸）

整套已經實作在 `~/google-agent-ecosystem/stockclaw-backend/app/podcast.py`，提供 4 個 endpoint：

```
POST /api/podcast/ingest_youtube  ← 主入口（YouTube URL → JSON）
POST /api/podcast/ingest          手動貼 transcript
POST /api/podcast/synthesis       跨集綜合分析（Gemini）
GET  /api/podcast/youtube_health  環境檢查
```

這份文件把 pipeline 拆解成可獨立理解的步驟，讓你能：
- **複用**到別的專案（llm-wiki-graph、Kmoney-news-stock-graph 等）
- **debug** 卡住時知道是哪一段
- **擴充** 加新的 fallback 路徑（例如自架 Whisper）

---

## 整體流程

```
                          YouTube URL
                                │
                                ▼
                       _extract_video_id()
                       ├─ youtu.be/<id>
                       ├─ youtube.com/watch?v=<id>
                       ├─ youtube.com/shorts/<id>
                       ├─ youtube.com/live/<id>
                       └─ <id> (直接給 11 字)
                                │
                                ▼ video_id (11 字)
                       _fetch_transcript()
                                │
              ┌─────────────────┴─────────────────┐
              ▼ 字幕路徑                          ▼ 音訊路徑（fallback）
        _fetch_via_subtitles()             _fetch_via_whisper()
              │                                   │
        youtube-transcript-api          yt-dlp 下載 m4a / 360p
        ├─ 試 zh-TW > zh-Hant > zh > en        │
        └─ 拿到字幕 → text                ffmpeg 切片（>24MB）
              │                                   │
              │                          Whisper API (Groq / OpenAI)
              │                                   │
              │                                   ▼
              └────────────┬────────────  transcript text
                           ▼
                   _gemini_extract()
                   ├─ Gemini 2.5 Flash JSON mode
                   ├─ prompt: 抽 summary / topics / insights
                   └─ fallback: rule-based regex（沒 GOOGLE_API_KEY 時）
                           │
                           ▼
                   ${PODCAST_DATA_DIR}/{date}_{slug}.json
                           │
                           ▼
                   wiki agent (batch_ingest.py)
                           │
                           ▼
                   wiki/sources/<slug>.md
                   wiki/entities/...md
                   wiki/concepts/...md
                   wiki/log.md
```

---

## 工具鏈逐一解釋

### 1️⃣ `youtube-transcript-api`（字幕首選）

**為什麼是首選**：
- 免費、零延遲、零 token 成本
- 直接拿 YouTube 自動字幕或作者上傳字幕
- 失敗時 graceful fallback 到音訊路徑

**權衡**：
- ❌ 沒字幕的影片打不到（直播、純音樂、被作者關閉字幕）
- ❌ 自動字幕標點符號很差（中文尤其慘），不過拿來餵 LLM 萃取 insights 沒差

**實作要點**（`podcast.py:269-318`）：

```python
def _list_transcripts_compat(video_id: str):
    """兼容 youtube-transcript-api <1.0（classmethod）vs 1.0+（instance .list()）"""
    try:
        ytt = YouTubeTranscriptApi()
        if hasattr(ytt, "list"):
            return ytt.list(video_id)
    except TypeError:
        pass
    if hasattr(YouTubeTranscriptApi, "list_transcripts"):
        return YouTubeTranscriptApi.list_transcripts(video_id)
    raise RuntimeError("API 版本不支援")
```

> ⚠️ **這個版本相容很重要**：`youtube-transcript-api` 在 1.0 大改 API（class method → instance method），舊 code 直接斷掉。Pipeline 兩種都接得到。

**語言優先序**：

```python
languages = body.languages or ["zh-TW", "zh-Hant", "zh", "en"]
```

優先繁中、再簡中、再 generic 中文、最後英文。對應台灣 podcast 通常上傳繁中或自動產生 zh 字幕的實況。

---

### 2️⃣ `yt-dlp`（音訊備援）

**何時走音訊路徑**：字幕 API 拋 `TranscriptsDisabled`、`NoTranscriptFound`，或整個 API 掛掉。

**為什麼選 yt-dlp 不選 youtube-dl**：
- youtube-dl 已經半死狀態（更新頻率低）
- yt-dlp 是 fork，每天都在處理 YouTube 反爬

**反爬技巧**（`podcast.py:343-354`）：

```python
ydl_opts = {
    "format": fmt,
    "outtmpl": out_template,
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "extractor_args": {
        "youtube": {"player_client": ["android", "web", "ios"]},
    },
    "postprocessors": [],   # 不依賴 ffmpeg post-process
}
```

**`player_client` 為何要寫 `["android", "web", "ios"]`**：
- YouTube 有時會擋 default web client，但 android client 還能下
- 三個輪流試，第一個能下的勝出
- 不寫的話常會中「Sign in to confirm」reCAPTCHA-style 阻擋

**format selector 的層層 fallback**（`podcast.py:336-342`）：

```python
fmt = (
    "bestaudio[ext=m4a]/"        # 1️⃣ 最理想：m4a 純音訊（Whisper 直接吃）
    "bestaudio/"                  # 2️⃣ 任何純音訊（webm 也行）
    "worst[acodec!=none][height<=360]/"  # 3️⃣ 360p 含音訊影片（檔小、Whisper 仍能吃）
    "best[height<=360]/"          # 4️⃣ 含音訊影片（保證有 match）
    "worst"                       # 5️⃣ 最差（保證下得到東西）
)
```

**`postprocessors: []` 為何重要**：
- 預設 yt-dlp 會用 ffmpeg 把音訊轉 mp3（後處理）
- 但用戶不一定有 ffmpeg
- Whisper API 吃 m4a / mp4 / webm 都可以，**不必轉**

**錯誤訊息升級**（`podcast.py:362-375`）：

```python
if "Requested format is not available" in msg:
    hint = "（影片格式特殊，可能要升級 yt-dlp）"
elif "Sign in to confirm" in msg or "age" in msg.lower():
    hint = "（影片要登入或年齡驗證）"
elif "Private video" in msg or "unavailable" in msg.lower():
    hint = "（影片不公開或已下架）"
```

讓使用者一眼看出是哪種失敗，不用看 stack trace。

---

### 3️⃣ `ffmpeg`（大檔切片）

**何時用**：音訊檔 > 24 MB（Whisper API 限 25 MB）。

**為什麼非得切片**：

| Whisper API | 限制 |
|---|---|
| OpenAI `whisper-1` | 25 MB / file |
| Groq `whisper-large-v3` | 25 MB / file |

50 分鐘的 m4a 大概 30-50 MB，一定要切。

**切片不 re-encode 是關鍵**（`podcast.py:443-457`）：

```python
cmd = [
    "ffmpeg", "-y",
    "-i", str(audio_path),
    "-f", "segment",
    "-segment_time", str(chunk_seconds),
    "-c", "copy",          # ← 關鍵：copy 不 re-encode
    "-loglevel", "error",
    str(output_pattern),
]
```

**`-c copy` 為何快**：
- 不 re-encode → CPU 幾乎不動，純 I/O
- 50 分鐘音訊 ~ 5 秒切完
- re-encode 同樣檔可能要 1-2 分鐘

**切多大**（`podcast.py:430-438`）：

```python
size_mb = audio_path.stat().st_size / 1024 / 1024
duration = _audio_duration_seconds(audio_path)  # ffprobe
n_chunks = max(2, int(size_mb / target_mb) + 1)
chunk_seconds = max(60, int(duration / n_chunks) + 5)
```

目標每片 ~20 MB（target_mb=20），預留 buffer 給 Whisper API 25 MB 上限。

**罕見邊角案例**：cut 不平均導致某片仍 > 24.5 MB → 遞迴切一次（target_mb 砍半）：

```python
for c in chunks:
    c_mb = c.stat().st_size / 1024 / 1024
    if c_mb > 24.5:
        for x in chunks: x.unlink(missing_ok=True)
        return _split_audio_for_whisper(audio_path, target_mb=target_mb / 2)
```

---

### 4️⃣ Whisper API（音訊轉文字）

**Groq vs OpenAI 權衡**：

| 維度 | Groq (`whisper-large-v3`) | OpenAI (`whisper-1`) |
|---|---|---|
| **價格** | 完全免費（rate limit 內） | $0.006 / 分鐘 |
| **速度** | 快 10x（自家 LPU 推論） | 中等 |
| **精度** | large-v3，比 whisper-1 強 | 較舊 |
| **中文** | 不錯 | 不錯 |
| **rate limit** | RPD 較嚴 | 較寬 |

**設計：Groq 優先、自動 fallback**（`podcast.py:489-499`）：

```python
groq_key = os.environ.get("GROQ_API_KEY", "").strip()
openai_key = os.environ.get("OPENAI_API_KEY", "").strip()

if groq_key:
    client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
    model = "whisper-large-v3"
    provider = "groq"
else:
    client = OpenAI(api_key=openai_key)
    model = "whisper-1"
    provider = "openai"
```

> 💡 **巧思**：Groq 提供 OpenAI 相容的 endpoint，所以同一個 `OpenAI()` SDK 換 `base_url` 就能用 Groq——**不必裝兩套 SDK**。

**單片失敗不要整體 fail**（`podcast.py:553-560`）：

```python
for i, chunk in enumerate(chunks, 1):
    try:
        text, model = _whisper_single(chunk)
        parts.append(text or "")
    except Exception as e:
        # 留個 marker，繼續處理下一片
        parts.append(f"[第 {i} 段轉文字失敗：{type(e).__name__}]")
```

50 分鐘影片切 3 片，第 2 片爆 → 仍能拿到 1 + 3 共兩片的轉文字 + marker，比整個 episode 死掉好。

---

### 5️⃣ Gemini 2.5 Flash（結構化萃取）

**為什麼 Gemini 不用 Claude**：
- 用戶生態系本來就 Gemini-heavy
- Gemini 2.5 Flash 1M token context、JSON mode 穩定、便宜
- 想保持 Claude Code（寫 code）跟生產 LLM（萃取）解耦

**JSON mode 是關鍵**（`podcast.py:644-651`）：

```python
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={"response_mime_type": "application/json"},
)
```

`response_mime_type="application/json"` 強制模型輸出合法 JSON，不要 markdown wrap。

**但 Gemini 偶爾仍會包 markdown fence**——所以收到後仍要 sanitize（`podcast.py:657-660`）：

```python
text = response.text.strip()
if text.startswith("```"):
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
```

防禦性程式設計：API 文件說會回 JSON，但你不能完全相信。

**Prompt 設計重點**（`podcast.py:605-631`）：

```python
GEMINI_EXTRACT_PROMPT = """你是台灣財經 podcast 重點萃取助手。下方是一段 podcast / YouTube 影片的 transcript。
請萃取結構化資訊，**只輸出 JSON**（不要 markdown code fence、不要解釋）。

JSON schema:
{
  "summary": "整集 100 字內中文摘要",
  "main_topics": ["3-5 個主題關鍵字"],
  "insights": [
    {
      "type": "stock | sector | macro | event | strategy",
      "content": "該 insight 的核心觀點（30-80 字）",
      "tickers": ["相關股票代號 list，台股 4-6 位數字 / 美股 2-5 位英文"],
      "sectors": ["相關產業，例：AI 伺服器、CPO、半導體"],
      "key_points": ["2-5 個支持該 insight 的具體論點，每個 10-30 字"]
    }
  ]
}

規則：
- 只列 transcript 中**明確提到**的 ticker / 產業，不要瞎掰
- insights 5-15 個，依重要性排序
- 中文輸出
- 如果 transcript 內容是英文，照樣產出中文 insights 但保留專有名詞英文
"""
```

**Prompt 設計幾個值得學的點**：

1. **明確列舉枚舉值**：`"type": "stock | sector | macro | event | strategy"` — 模型不會自創新類型
2. **欄位帶單位 / 範例**：`"tickers": ["...台股 4-6 位數字 / 美股 2-5 位英文，例 2330 / NVDA"]`
3. **明確禁止 hallucination**：「只列 transcript 中**明確提到**的，不要瞎掰」
4. **數量上限**：「insights 5-15 個」，避免模型有時吐 50 條雜訊

**80k 字截斷**（`podcast.py:641-642`）：

```python
if len(transcript) > 80_000:
    transcript = transcript[:80_000] + "\n[...transcript 已截斷...]"
```

Gemini 2.5 Flash 1M token context 理論上吃得下整個 transcript，但太長會：
- 注意力被稀釋（important info 漏掉）
- token 成本可惜

80k 字 ≈ 15-20 萬 token，相當於 2 小時 podcast 全文，足夠。

**Fallback：rule-based**（`podcast.py:139-164`）：

當沒 `GOOGLE_API_KEY` 或 Gemini API 掛時，回退到 regex 抓 ticker + 切上下文：

```python
def _auto_detect_tickers(transcript):
    tw = re.findall(r"\b\d{4,6}\b", transcript)        # 台股
    us = re.findall(r"\b[A-Z]{2,5}\b", transcript)      # 美股
    blacklist = {"AI", "GPU", "CPU", "USD", "TWD", "EPS", "ROE", "ETF"}
    us = [t for t in us if t not in blacklist]
    ...
```

不夠精準（會漏一些 context-dependent insight），但**能跑**。
教學上的價值：show that 「永遠要有 graceful degradation」。

---

### 6️⃣ JSON Schema（產出格式）

完整 record schema（`podcast.py:705-716`）：

```json
{
  "podcast_name": "Gooaye 股癌",
  "episode": "EP641 ...",
  "date": "2026-03-04",
  "note": "（一句話節目重點）",
  "summary": "（Gemini 100 字摘要）",
  "main_topics": ["AI 伺服器", "美股科技股", "台股月線", ...],
  "insights": [
    {
      "type": "stock",
      "content": "...",
      "tickers": ["2330"],
      "sectors": ["半導體"],
      "key_points": ["論點1", "論點2", ...]
    }
  ],
  "_video_id": "abc123XYZ",
  "_video_url": "https://youtube.com/watch?v=abc123XYZ",
  "_transcript_language": "zh-TW",
  "_transcript_chars": 12345,
  "_ingested_at": "2026-05-09T15:30:00",
  "_extraction_mode": "gemini"
}
```

**Schema 設計重點**：

- **`_*` 前綴是 metadata**：不參與 wiki 渲染、純 debug 用
- **`insights[]` 跟 llm-wiki-graph schema 一致**：podcast.py 跟 llm-wiki-graph 是上下游關係，一份 JSON 兩邊都吃
- **`tickers` 是 list 不是 string**：一個 insight 可能涵蓋 2330 + 2454 + 2308（產業鏈）
- **`type` 枚舉**：stock / sector / macro / event / strategy 五種，前端 UI 可依此上色

---

### 7️⃣ 跨集 Synthesis（Bonus，但很值得）

`POST /api/podcast/synthesis`（`podcast.py:846-968`）：

把所有 episode 的 summary + insights 餵給 Gemini，請它做**跨集綜合分析**：

```json
{
  "market_overview": "整體市場觀點 100-150 字摘要",
  "top_tickers": [{"ticker": "2330", "mentions": 5, "view": "..."}],
  "top_sectors": [{"sector": "AI 伺服器", "mentions": 8}],
  "consensus": ["多集共識 1", ...],
  "disagreements": ["集間矛盾 1", ...],
  "timeline": [{"date": "...", "podcast": "...", "key": "..."}],
  "recommended_watchlist": ["2330", "NVDA", ...]
}
```

**設計亮點 — MD5 hash cache**（`podcast.py:889-906`）：

```python
content_str = json.dumps(episodes, sort_keys=True, ensure_ascii=False)
content_hash = hashlib.md5(content_str.encode("utf-8")).hexdigest()[:16]

if not force and cache_path.exists():
    cached = json.loads(cache_path.read_text(encoding="utf-8"))
    if cached.get("hash") == content_hash:
        return {**cached["result"], "cached": True}
```

**為什麼用 hash 不用時間 TTL**：
- 內容沒變就絕對不用重跑（省 token）
- 加一集才 invalidate
- TTL 沒法表達「累積到第 30 集才該重跑」這種語義

**`force=true` query 參數**強制 bypass cache，方便 prompt 微調後重跑驗證。

---

## 環境檢查 endpoint

`GET /api/podcast/youtube_health`（`podcast.py:971-1010`）：

```json
{
  "youtube_transcript_api": true,
  "yt_dlp": true,
  "openai_sdk": true,
  "ffmpeg": true,
  "groq_api_key_set": true,
  "openai_api_key_set": false,
  "gemini_available": true,
  "gemini_api_key_set": true,
  "transcript_methods": [
    "youtube-transcript-api (字幕)",
    "yt-dlp + Whisper (groq) + 自動切片"
  ],
  "extraction_mode": "gemini",
  "ready": true,
  "warning": null
}
```

**為什麼要這個**：使用者第一次裝 dependency 會少裝某幾個（最常見：忘了 `brew install ffmpeg`）。打 `/youtube_health` 立刻知道 pipeline 哪段會崩，不用等真的跑才發現。

---

## 接到 wiki：JSON → markdown 頁面

產出 JSON 後，下一步是把它整理成 wiki/sources/<slug>.md。

`llm-wiki-graph/wiki/batch_ingest.py` 是現成腳本（用戶 repo 已實作）：

```bash
# 從 raw/ 讀新 JSON、寫進 wiki/sources/
cd ~/google-agent-ecosystem/llm-wiki-graph
uv run python wiki/batch_ingest.py
```

它會：
1. 對每份 `raw/*.json` 檢查 wiki/sources/ 有沒有對應頁
2. 沒有就用 LLM 生成一頁摘要、寫進 frontmatter
3. 同步 wiki/index.md / wiki/log.md

> 詳細的「JSON 進 wiki」流程屬於 wiki-side 教學，不在本文範圍。但兩個流程**透過 JSON schema 解耦**，所以你可以：
> - 把 podcast.py 接到任何能吃這個 schema 的 wiki agent
> - 從別處（手動轉錄、別的 source）產生同 schema JSON 直接餵 wiki

---

## 環境變數總覽

| 變數 | 必要？ | 用途 | 申請 |
|---|---|---|---|
| `GROQ_API_KEY` | 推薦 | Whisper 字幕 fallback | https://console.groq.com/keys |
| `OPENAI_API_KEY` | 替代 Groq | Whisper 字幕 fallback | https://platform.openai.com/api-keys |
| `GOOGLE_API_KEY` | 推薦 | Gemini 結構化萃取 | https://aistudio.google.com/apikey |
| `PODCAST_DATA_DIR` | 選用 | 自訂輸出目錄（預設 `data/podcasts/`） | — |

只裝 `youtube-transcript-api` 也能跑（純字幕模式），但會：
- 沒字幕的影片整個失敗
- 萃取走 rule-based regex（粗糙）

完整版四個 key 都設能讓 ready=true。

---

## 系統依賴

```bash
# Python 套件（透過 uv）
uv add yt-dlp youtube-transcript-api openai google-genai

# 系統工具（macOS）
brew install ffmpeg

# 系統工具（Linux）
apt install ffmpeg
```

`ffmpeg` 不裝也能跑，但**音訊 > 24 MB 會失敗**（無法切片）。對應「30 分鐘以上 podcast」會中招。

---

## 常見錯誤排查

| 症狀 | 原因 | 解法 |
|---|---|---|
| `yt-dlp 下載失敗：Sign in to confirm` | YouTube 反爬 / 年齡驗證 | 升級 yt-dlp `uv add yt-dlp@latest`；或換另一支影片 |
| `Requested format is not available` | yt-dlp 版本舊 | 同上 |
| `ffmpeg 切片失敗` | ffmpeg 沒裝或路徑問題 | `brew install ffmpeg` 後 `which ffmpeg ffprobe` 確認 |
| `Whisper API 失敗：rate_limit_exceeded` | Groq 免費額度用完 | 等一小時再跑、或設 `OPENAI_API_KEY` 切 OpenAI |
| `Gemini 回應非合法 JSON` | Gemini 偶爾包 markdown / 模型抽風 | 已有 sanitize；持續發生重啟 service |
| transcript 字幕拿不到、yt-dlp 也下不了 | 影片下架 / 私人 | 沒解，跳過該影片 |

---

## 對照表：哪份 code 在哪

| 功能 | 檔案 | 行號 |
|---|---|---|
| 主入口 | `podcast.py` | `ingest_youtube`, line 688-794 |
| URL → video_id | `podcast.py` | `_extract_video_id`, line 253-266 |
| 字幕路徑 | `podcast.py` | `_fetch_via_subtitles`, line 288-318 |
| yt-dlp 下載 | `podcast.py` | `_download_audio`, line 321-384 |
| ffmpeg 切片 | `podcast.py` | `_split_audio_for_whisper`, line 416-484 |
| Whisper 呼叫 | `podcast.py` | `_whisper_single` / `_whisper_transcribe`, line 487-564 |
| Gemini 萃取 | `podcast.py` | `_gemini_extract`, line 634-664 |
| Rule-based fallback | `podcast.py` | `_build_insights`, line 139-164 |
| 跨集 synthesis | `podcast.py` | `synthesize_podcasts`, line 846-968 |
| Health check | `podcast.py` | `youtube_health`, line 971-1010 |

---

## 延伸：為什麼 pipeline 設計成「字幕優先 + 音訊備援」？

**字幕路徑成本**（每集）：
- 時間：~5 秒
- 金錢：0
- token：0

**音訊路徑成本**（每集 50 分鐘）：
- 時間：~60 秒（yt-dlp 30s + Whisper 20s + Gemini 10s）
- 金錢：~$0.30（Whisper $0.30，Groq 免費；Gemini 萃取 ~$0.005）
- token：~30k（Whisper 不算 token；Gemini 萃取算）

差 **12x 時間**、**∞ 倍金錢**。所以哪怕字幕路徑失敗率 30%，仍要先試。

**這個設計可以推廣到任何 LLM agentic pipeline**：

> **永遠先試「免費快慢精度低」的路徑，失敗時 graceful fallback 到「貴慢精度高」的路徑。**

例如：
- RAG 檢索：先 BM25 → 失敗 fallback embedding
- code search：先 grep → 失敗 fallback subagent search
- agent action：先 dry-run → 失敗 fallback ask-user

這是「pipeline cost-tier」設計哲學，podcast.py 是個示範案例。

---

## 一鍵試用

如果你要在你的某個專案 import 這套 pipeline：

```bash
# 1. 開後端
cd ~/google-agent-ecosystem/stockclaw-backend
./run.sh
# 等 http://localhost:8088 起來

# 2. 健康檢查
curl http://localhost:8088/api/podcast/youtube_health | jq

# 3. ingest 一支影片
curl -X POST http://localhost:8088/api/podcast/ingest_youtube \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/abc123XYZ"}' | jq '.summary, .insights_count'

# 4. 看 JSON 寫到哪
ls -t ~/google-agent-ecosystem/stockclaw-backend/data/podcasts/*.json | head -3
```

JSON 出來後：

```bash
# 倒進 wiki repo 處理
cp data/podcasts/*.json ~/google-agent-ecosystem/llm-wiki-graph/raw/
cd ~/google-agent-ecosystem/llm-wiki-graph
uv run python wiki/batch_ingest.py
```

---

## 想擴充什麼？

| 方向 | 怎麼做 |
|---|---|
| 加 Spotify / Apple Podcast 來源 | 開新 endpoint `_fetch_spotify`、改主入口 dispatch by URL host |
| 換成本地 Whisper（whisper.cpp） | `_whisper_transcribe` 內加分支：env var `WHISPER_LOCAL=1` 時走 local binary |
| 自動排程每天 ingest 訂閱頻道 | 加 cron / FastAPI BackgroundTasks 跑「YouTube channel 新影片清單 → ingest」 |
| 多語言支援（日文 / 韓文 podcast） | `languages` 參數加 `["ja", "ko"]`、Gemini prompt 加多語言處理規則 |
| 加 Anthropic Claude 萃取 | `_claude_extract`，跟 `_gemini_extract` 同 schema，env var 切換 |

---

## 相關 skill

- `youtube-to-podcast-json` skill 已裝在 `llm-wiki-graph/.claude/skills/` 跟 `Kmoney-news-stock-graph/.claude/skills/`，Claude Code 在這兩個 repo 看到「ingest YouTube」「下載 podcast」這類關鍵字就會自動 invoke
- 在這兩個 repo 內跟 Claude Code 對話：「幫我把 https://youtu.be/xxx 這支影片 ingest 成 wiki」就能跑全鏈

詳細 skill 內容跟 invoke 行為見對應 `.claude/skills/youtube-to-podcast-json/SKILL.md`。
