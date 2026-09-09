# Changelog

> 用「給人讀」而不是「給機器讀」的方式記錄這個 repo 的演進。

## 2026-05-16

### ✨ 新增功能
- 為「每週俳句」教學專案（01-weekly-haiku）加上 Google Doc 日報／週報設計，可把產出直接寫進 Google 文件 (e8009ae)
- 新增第 8 號小專案「agent team」：示範多個 Claude 實例跨層協作開發功能 (5563917)
- 在 Projects/ 建立一整批可實際執行的教學範例專案 (3844c1c)
- 新增 6 個專案層級的自訂指令（slash command），放在 .claude/commands (4cb9c75)

### 🎨 範例 / Demo
- 新增「盲評一致性」示範素材，用來演練 agent team 為何無法被單一 agent 取代 (6a966a3)
- 把 debug 示範改為「正解版」，並降級為反面教材使用 (1465ecc)
- 新增「競爭假設 debug」演練素材 (3908bc1)

### 📚 文件 / 教學
- 重寫 agent team 教學講義：主軸從 debug 換成盲評一致性 (976576f)
- 新增 agent team 教學講義，帶學員體會「隊友互相證偽」的威力 (a4100cc)
- 更新第 8 號專案 README：盲評升為主推範例、debug 降為反例 (d371b15)
- 第 8 號專案 README 串接上 agent team 教學講義 (0aac29a)
- 在 Projects 總覽表掛上第 7、8 號小專案 (8f3e0f4)

### 🔧 重構 / 維護
- 初始化 repo，建立 README 骨架與 .gitignore (e61df4f)
