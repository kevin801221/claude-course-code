# 課程節奏(90 分鐘)

> 給講師排時間用。逐字帶課版在專案根的 `WALKTHROUGH.md`。

| 段落 | 時長 | 做什麼 | 學生帶走 |
|---|---|---|---|
| 開場 | 5 分 | 為什麼用「平行鏡頭」而不是一個全能 agent | 心智模型:矛盾才是價值 |
| Phase 0 環境 | 10 分 | `uv sync`、(可選)填 Finnhub key、`claude` 進場 | 跑得起來的環境 |
| Phase 1 第一個 agent ⭐ | 30 分 | 細看 `fundamentals-analyst`,跑出 `fundamentals.md` | 看懂 agent frontmatter + 鏡頭隔離 |
| Phase 2 另外兩個鏡頭 | 20 分 | 同節奏跑 technicals / news,加速 | 三份獨立分析 |
| Phase 3 收斂 ⭐ | 20 分 | `research-synthesizer` 彙整,重點看「矛盾訊號」 | 一頁 research-note + 交叉檢核的威力 |
| 收尾 | 5 分 | 進階:4 agent 改寫成 4 skill 的橋接 | 往 Skills 章節的接點 |

## 故意踩的坑(現場演示比口頭講有效)
1. 用一個拼錯的 ticker(例 `NVDDA`)→ 讓學生看「資料缺漏」如何被誠實標出而不是捏造。
2. 不裝 Finnhub key 跑 news → 看 fallback 到 yfinance 的降級行為。
3. 故意問 Claude「那我該買嗎?」→ 看 synthesizer 如何把問題轉成「重視 X 偏多、擔心 Y 偏空」而不下指令。
