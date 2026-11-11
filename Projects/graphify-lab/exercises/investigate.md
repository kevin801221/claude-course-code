# 學生任務：先交影響分析，再動程式

在 Claude Code（已安裝本專案的 Skill、完成建圖、放入 docs/ticket-flow.md）貼：

> 請用 Graphify 找出 submit_ticket() 到 send_notification() 的路徑，讀 docs/ticket-flow.md 及路徑上的 Python 檔。PM 現在要 email 可選。先不要改程式；用表格列出「規格 → 函式 → 目前行為 → 要改的行為 → 檔案與行號」。幫我標出哪些關係是圖明示、哪些是推論、哪些已從原始碼核對。指出一個圖不能回答、必須跑測試的問題。

自行打開一個引用位置驗證。你應找到：service.py 的 create_ticket 目前先驗證、再儲存、最後**無條件**通知；validation.py 沒處理 None；repository.py 只是將傳值放進 dict，不能從節點相連就推論它需要改。驗證、儲存、通知是 create_ticket 的三個被呼叫者，並不是三者彼此逐一呼叫。

確認計畫後再貼：

> 按剛才核對的來源與 PM 規格，實作 email 可選。維持顯式 import 和五個公開函式；不得更動驗收腳本。執行父目錄 checks/check_tickets.py 的 acceptance 模式，貼出實際結果，再更新圖重新解釋改動。同時說明為什麼無 email 時圖上仍可能看見到通知的路徑。

## 兩個 session 的課堂比較

在同一份未修改的 starter、同模型、同題目、同時間預算開兩個新 session。A 只搜尋與讀檔，B 先查圖再讀檔；都交第一段的表格，不執行修改。用真正執行的結果填：

| 方法 | 正確來源／抽查數 | 漏掉的規則或依賴 | 查題時間 | 建圖時間 | 實際模型用量（看不到填 N/A） |
|---|---|---|---|---|---|
| A 搜尋＋讀檔 | | | | 不適用 | |
| B 查圖＋讀檔 | | | | | |

不用虛構 token、百分比或優勝者。可從同一個學員的兩份輸出比較。
