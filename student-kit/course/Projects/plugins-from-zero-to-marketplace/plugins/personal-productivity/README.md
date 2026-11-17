# personal-productivity plugin

> 個人生產力 3 件套：週俳句、番茄鐘、YouTube 學習筆記

## 內含

| 元件 | 類型 | 用途 |
|---|---|---|
| `/weekly-haiku` | Slash command | 用本週 git log 寫一首俳句 |
| `pomodoro.sh` | Hook (PostToolUse) | Claude 用太久彈通知喝水 |
| `youtube-notes` | Skill | YouTube 連結變學習筆記 |

## 為什麼包成 plugin

3 個都是「跨專案、個人偏好」性質——做成 plugin 一行裝齊，比逐個 cp 快。

## 使用情境

```bash
# 週五下班
> /weekly-haiku  → 一首詩貼 IG

# 寫 code 寫太久
（背景自動彈通知）→ 去喝水

# 朋友傳 YouTube 必看連結
> 整理 https://youtu.be/xxx 的筆記
```
