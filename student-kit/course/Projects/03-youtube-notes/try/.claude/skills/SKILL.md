---
name: youtube-notes
description: |
  Turn a YouTube link into structured study notes with timestamps.
  Triggers when user pastes a youtube.com or youtu.be link and
  asks for notes / summary / 重點 / 整理 / 抓重點.
---

# YouTube Notes

## Workflow

1. 確認連結（v=ID 或 youtu.be/ID）
2. 跑 `yt-dlp --write-auto-sub --skip-download --sub-lang en,zh <url>`
3. 讀生成的 .vtt 檔，把 timestamps 與台詞對齊
4. 整理成以下格式輸出

## Output 格式

```
## 🎬 (影片標題) — 全長 X 分 / 讀完 5 分

### 💡 三大重點 (附 [時間戳])
- 重點 A [4:32 看講者實演]
- 重點 B [9:18]
- 重點 C [21:00]

### 📚 提到的工具 / 概念
- ...

### 🤔 我的一句話觀察
...
```

## Critical rules

- 不要「逐字翻譯」字幕，要「重新組織」
- 時間戳一定要對 — 寫錯時間比沒寫還糟
- 影片講的不要當定見，加自己的觀察一句
- 影片如果太長（>1 小時），先問使用者「要全部還是某段重點」
