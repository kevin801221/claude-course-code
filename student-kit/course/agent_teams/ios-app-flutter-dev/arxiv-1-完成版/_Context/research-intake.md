# 研究搜集任務單(給 researcher 隊友)

> 研究先行的目的:讓 App 的功能設計**有依據**,而不是拍腦袋。
> team lead 會 spawn 一個 researcher 隊友照這份做,結論寫進 `_Context/research-findings.md`。
>
> ⚠️ 這是為了 App 功能設計做的整理,**不是醫療或心理治療建議**。引用一律標來源。

## 怎麼搜集
- 整理公開可信資訊(官方文件、API 說明、綜述、可信報導)。
- 每個結論後標「依據」:來源名稱 + 連結(查得到的話)+ 日期。
- 拿不準的標「證據有限 / 仍有爭議」,不要寫死。

## 要產出(填進 `_Context/research-findings.md`)

1. **arXiv 抓取設定** → 給後端(backend-owner)依據
   - 該收哪些領域分類(cs.AI / cs.LG / cs.CL 之外還有沒有更該收的科技類)
   - 用哪個 API 端點、回傳格式(Atom XML?)、欄位有哪些
   - 「最新 5 篇」怎麼排序:`submittedDate` vs `lastUpdatedDate` 差在哪
   - 取用速率限制 / 禮貌間隔(arXiv API 使用規範)
2. **閱讀疲勞與休息間隔** → 給呼吸提醒(breathing-owner)依據
   - 連續閱讀累積幾分鐘提醒休息一次合理(預設 10 分鐘是否有依據)
   - 深呼吸的吸 / 吐節奏多少秒一輪、一次做幾輪
3. **「資訊餵食」App 不該用的成長駭客做法** → 給全員設計紅線
   - 無限滑、紅點焦慮、罪惡感推播這類暗黑模式為什麼該避免

## 收斂(team lead 做)
findings 寫完後,team lead 把可落地的結論抄進 `_Context/app-spec.md` 的「研究結論」欄位,
標清楚「這個設定 / 預設值來自研究」,然後**凍結規格**,才進入平行開發。
