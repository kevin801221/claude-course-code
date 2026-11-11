---
name: youtube-notes
description: |
  Turn a YouTube link into structured study notes with timestamps.
  Triggers when user pastes a youtube.com or youtu.be link and asks for
  notes / summary / 重點 / 整理 / 抓重點.
---

# YouTube Notes

## Workflow
1. 確認連結
2. 跑 `yt-dlp --write-auto-sub --skip-download --sub-lang en,zh <url>`
3. 讀 .vtt 檔，把 timestamps 與台詞對齊
4. 整理成下方格式

## Output 格式
```
## 🎬 (影片標題) — 全長 X 分 / 讀完 5 分
### 💡 三大重點 (附 [時間戳])
### 📚 提到的工具 / 概念
### 🤔 我的一句話觀察
```

## Critical rules
- 不要逐字翻譯，要重新組織
- 時間戳要對
- 影片講的不要當定見，加自己觀察一句
