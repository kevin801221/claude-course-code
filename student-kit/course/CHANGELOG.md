# Changelog

> 用「給人讀」而不是「給機器讀」的方式記錄這個 repo 的演進。

## 2026-10-24

### 🚀 旗艦重構與規範對齊
- 重新撰寫根目錄總指揮譜 `WALKTHROUGH.md`，深度整合雙軌時鐘（12 小時全景作戰版 ＋ 6 小時一日精華版）、全 9 大 Projects、原生 Agent Teams 實戰與避坑指南
- 補齊 `Projects/09-timetrace` SaaS 一鏡到底大專案導航與 `Projects/README.md` 架構
- 修復 `agent_teams/README.md` 描述與檔案路徑，正式對齊「arXiv 每日論文閱讀器」App
- 解決 cross-references 壞鏈與錨點問題，補齊 `superpowers_production_walkthrough.md` 引用
- 強制規範 Python 依賴管理全面走 `uv`，更新指令與設定檔
- 統一作者與 GitHub 帳號規範至 `@kevin801221`

## 2026-09-09

### 📚 教學架構全面升級
- 升級旗艦版 `README.md`，系統化串接 10 大理論模組、多 Agent 協作產線與工業級專案 (9115b9c)
- 導入 10 個核心理論與實戰章節（01-slash-commands 至 10-cli）(13b4ed6)
- 新增 `LEARNING-ROADMAP.md`、`claude_concepts_guide.md` 與自我評量技能 (`/self-assessment`, `/lesson-quiz`) (30e94eb, f8dd62a)
- 整理並優化繁體中文教學體系與社群規範 (8ca6d02, c76fbe8)

## 2026-05-22

### 🛠 實戰專案與插件體系擴充
- 新增第 9 號小專案 `09-timetrace`（五大組件一鏡到底蓋 SaaS 藍圖）
- 擴充 `important-plugins/`：引進 `superpowers` 14 招心法、`ralph-wiggum` 自治循環與 `pr-review-toolkit`
- 建立 Auto-CV 視覺化晶圓瑕疵訓練駕駛艙與多階段 ML 流水線
- 新增 `agent_teams/ios-app-flutter-dev`：原生 Agent teams 跨技術棧開發 arXiv 論文閱讀器

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
