# 《Claude Code 完全攻略》— 書籍大綱（提案稿 v1）

> 作者：KevinLuo
> 規格目標：約 780 頁（落在 600–800 頁區間上緣）・全彩圖文・繁體中文
> 建議定價：NT$1,200（工具書／完全攻略定位）
> 骨幹來源：338 頁完整教學 PPT（Part 1–19）擴寫 + 書專屬新增章節
> 最終產出格式：PDF 排版稿

---

## 一、定位與賣點

**一句話定位**：市面上第一本「從 CLI 第一行指令，到多 agent 平行協作、再到逐一解剖全世界最紅的 MCP / Skill / Plugin」的中文 Claude Code 工具書。

三大差異化賣點：

1. **六大延伸能力（Sub-agents / Skills / Hooks / MCP / Plugins / Agent SDK）每個都有 WHY → WHAT → HOW → WHEN → PITFALLS → TEST 的完整教學閉環**，且每章配一個可獨立跑完的自製範例。
2. **獨家「熱門 Repo 巡禮」整篇**：把 GitHub 上星數最高、安裝量最大的 MCP server、Skill、Plugin 一個一個拆開講，附有趣比喻 + 可貼上就跑的 code demo。
3. **多 Agent 協作實戰**：用真實案例（晶圓瑕疵 4-agent ML pipeline、個股研究平行團隊、Flutter App 多 Claude worktree）教讀者怎麼指揮一群 agent。

---

## 二、頁數與篇章總覽

| 篇 | 篇名 | 章 | 頁數 | 對應 PPT | 性質 |
|---|---|---|---|---|---|
| 前 | 前置（序・如何閱讀・環境準備） | — | 18 | — | 新增 |
| 1 | 入門與基礎 | 1–3 | 72 | Part 1–3 | 擴寫 |
| 2 | 客製化你的 Claude Code | 4–6 | 78 | Part 4–6 | 擴寫 |
| 3 | 六大延伸能力（核心） | 7–12 | 210 | Part 7–12 | 擴寫 |
| 4 | 熱門 Repo 巡禮（獨家） | 13–16 | 124 | 部分 Part 11/17 | 新增為主 |
| 5 | 多 Agent 協作實戰 | 17–20 | 88 | Part 7·設計 / 18·6 | 擴寫+新增 |
| 6 | 工程化與上線 | 21–24 | 82 | Part 13–16 | 擴寫 |
| 7 | Context Engineering 與心法 | 25–27 | 68 | Part 17–18 | 擴寫 |
| 8 | 結語與附錄 | 28 + A–E | 50 | Part 19 | 擴寫+新增 |
| | **合計** | | **790** | | |

> 正文 + 附錄約 790 頁；含全彩圖文、留白與排版後，印刷成書落在 600–800 頁設定的上緣，支撐 NT$1,200 的工具書定位。

---

## 三、詳細章節大綱

### 前置（18 頁）

- 推薦序 ×2（4）
- 作者序：為什麼寫這本書（2）
- 如何閱讀本書 + 三條學習路徑圖（新手 / 開發者 / 團隊導入）（4）
- 環境準備與安裝：macOS / Windows / Linux、Node、權限、第一次啟動（8）

---

### 第 1 篇　入門與基礎（72 頁｜PPT Part 1–3）

**第 1 章　認識 Claude Code（22）**
什麼是 Claude Code、為什麼用它、它和 ChatGPT/Copilot 的差異、安裝與第一次對話、心智模型（agentic CLI）。
- 圖文：Claude Code 在 AI 工具光譜上的定位圖。

**第 2 章　CLI 基礎（26）**
互動模式、Print mode、常用 flags、快捷鍵、session 管理、貼圖片/檔案、@ 引用、! bash。
- Demo：第一個真實任務從頭到尾。

**第 3 章　內建 Slash Commands（24）**
20+ 內建指令速查與用法（/init、/clear、/compact、/review、/agents、/mcp、/hooks…）。
- 速查表 + 每個指令的使用時機。

---

### 第 2 篇　客製化你的 Claude Code（78 頁｜PPT Part 4–6）

**第 4 章　自訂 Slash Commands（26）**　▶ 自製範例：`Projects/01-weekly-haiku/`
把常用 prompt 封裝成 `/your-command`、參數、frontmatter、放哪一層。
- 實戰：用本週 git log 自動寫俳句的 `/weekly-haiku`。

**第 5 章　Settings 設定（24）**
三層級配置（個人/專案/本地）、權限管理、settings.json 全欄位導覽。

**第 6 章　CLAUDE.md / Memory（28）**
讓 Claude 記住專案脈絡、CLAUDE.md 寫法心法、import、auto-memory、團隊共用。
- 本書 repo 的 CLAUDE.md 當完整範例拆解。

---

### 第 3 篇　六大延伸能力（210 頁｜PPT Part 7–12）★核心

**第 7 章　Sub-agents（34）**　▶ 自製範例：`Projects/02-recipe-genie/`
委派子任務、省 context 的心智模型、`/agents` UI 自動生成、5 個高價值 agent prompt 範例、description 路由。
- 實戰：冰箱食譜助手 sub-agent。

**第 8 章　Skills（38）**　▶ 自製範例：`03-youtube-notes/`、`07-weekly-reports-skill/`、`build-gitnexus-skill-commandline/`
SKILL.md 結構、漸進式揭露、資料夾型 skill、可重用 SOP、production-grade skill 設計。
- 實戰：YouTube 連結變筆記、GitHub commit 變週報、`/gitnexus` 知識圖譜工具包。

**第 9 章　Hooks（34）**　▶ 自製範例：`Projects/04-pomodoro/`
9 種生命週期事件 × 30+ 真實應用、PreToolUse 守門、Stop 通知、exit code 語意。
- 實戰：番茄鐘提醒喝水 hook；本書 repo 的 guard-secrets / notify-done。

**第 10 章　MCP（Model Context Protocol）（34）**　▶ 自製範例：`Projects/05-organize-downloads/`
MCP 是什麼、stdio vs SSE、`claude mcp add`、自己寫一個 MCP server、權限與風險。
- 實戰：整理 Downloads 資料夾的 MCP server。

**第 11 章　Plugins / Marketplaces（36）**　▶ 自製範例：`Projects/plugins-from-zero-to-marketplace/`
把 skills+agents+commands+hooks 打包、plugin.json、建 marketplace、發佈與安裝。
- 實戰：從零到 marketplace 的 3 個 plugin 範例。

**第 12 章　Claude Agent SDK（34）**　▶ 自製範例：`Projects/06-discord-dm-bot/`
用程式碼建構 agentic 系統、SDK 架構、tool use、串接外部服務。
- 實戰：Discord 文字冒險 bot。

---

### 第 4 篇　熱門 Repo 巡禮（124 頁）★獨家新增

> 把全世界最紅的 MCP / Skill / Plugin 一個一個拆開講，每個都附「有趣比喻 + 可貼上就跑的 code demo」。星數/排名引用自 2026 年 5 月公開資料。

**第 13 章　怎麼評估與安裝一個 repo（14）**
看星數/維護活躍度/開 issue、安全紅旗、`claude mcp add` 與 `/plugins` 安裝流程、沙箱與權限。

**第 14 章　MCP 名人堂（42）**
逐一拆解（含 demo）：
1. **Filesystem**（Anthropic 官方參考）— 沙箱檔案讀寫
2. **GitHub MCP** — repo / PR / issue 全自動
3. **Context7**（Upstash，安裝量榜首）— 即時注入最新版文件，治「AI 用過時 API」
4. **Playwright MCP**（Microsoft，30k★）— 瀏覽器自動化
5. **Sequential Thinking**（Anthropic 官方參考）— 結構化逐步推理
6. **Brave Search / Fetch** — 讓 Claude 上網
7. **Notion MCP** — 知識庫變可操作工具
8. **Slack MCP** — 團隊訊息自動化
9. **MindsDB**（39k★）— 資料庫 + AI 預測
- 收尾：怎麼組合多個 MCP（GitHub + Context7 黃金組合）。

**第 15 章　Skills 名人堂（34）**
1. **Anthropic 官方 document skills**（pdf / docx / xlsx / pptx）— 本書 PDF 就是它做的
2. **obra/superpowers**（Jesse Vincent）— 一整座 skill 工廠（TDD / brainstorming / worktree）
3. **VoltAgent/awesome-agent-skills**（1000+，含 Stripe / Cloudflare / Vercel / Figma / Trail of Bits 官方隊伍）
4. **Trail of Bits 安全稽核 skills**
5. awesome 清單導覽：ComposioHQ / travisvn / Chat2AnyLLM（9,959 skills）

**第 16 章　Plugins & Marketplace 名人堂（34）**
深度解剖三支對應三大 pillar（取自本書 repo `important-plugins/`）：
1. **superpowers**（Skills pillar）— 一座 skill 工廠 + marketplace
2. **ralph-wiggum**（Hooks pillar，Anthropic 官方）— Stop hook 讓 Claude 不准下班，自動迭代到測試全綠
3. **pr-review-toolkit**（Sub-agents pillar，Anthropic 官方）— 6 個 review agent 一鍵調度
- Marketplace 導覽：`anthropics/claude-plugins-official`、`superpowers-marketplace`、Chat2AnyLLM / ComposioHQ awesome 清單、claudemarketplaces.com。
- 配套實作：用 superpowers 做出 pomocat 終端番茄鐘（`important-plugins/project1-superpowers/`）。

---

### 第 5 篇　多 Agent 協作實戰（88 頁）

**第 17 章　Sub-agent 團隊：晶圓瑕疵 4-agent ML Pipeline（26）**　▶ `agent_group_projects/computer-vision-wafer-detection/`
抓資料 → 標註 → 訓練 → 推論，4 個 agent 分階段協作的 production 範例；含完成版/模板/demo 三件套怎麼用。

**第 18 章　平行鏡頭：個股研究團隊（22）**　▶ `agent_group_projects/stock-groups-skills/`
基本面 / 技術面 / 新聞情緒 3 分析師 + 1 彙整，平行研究同一檔股票後收斂（全程「非投資建議」免責）。

**第 19 章　多 Claude 平行 worktree：Flutter App（22）**　▶ `agent_teams/ios-app-flutter-dev/`
研究先行 → 凍結規格與 API 契約 → 三隊友平行 backend/reader/breathing → git merge 整合驗收。

**第 20 章　課程工廠生產線（18）**　▶ `agent_group_projects/new-course-material2presentation-blank/`
丟一個主題，sub-agent + skill 組成生產線，自動產出大綱/投影片/範例/評量/講師備忘。

---

### 第 6 篇　工程化與上線（82 頁｜PPT Part 13–16）

**第 21 章　IDE 整合（16）** — VS Code / JetBrains 內用 Claude Code。
**第 22 章　Headless / 自動化（22）** — 跑進 CI/CD、背景任務、`-p` print mode、JSON 輸出。
**第 23 章　Permissions / 安全（22）** — 把 agentic 工具關進籠子、allow/deny、網路控制、企業治理。
**第 24 章　進階主題（22）** — Output styles、Statusline、Cost 控制、Background tasks、Debug。

---

### 第 7 篇　Context Engineering 與心法（68 頁｜PPT Part 17–18）

**第 25 章　GitHub 精選資源（14）** — 官方 repo + Awesome 清單必看。
**第 26 章　Context Engineering 實戰（PRP 流程）（30）** — CLAUDE.md + INITIAL.md → `/generate-prp` → PRP.md → `/execute-prp` → 功能；含 IO 對照圖與踩雷。
**第 27 章　心法集（24）** — AI Skill 實戰架構藍圖等心法，配實例（drafting-weekly-reports）。

---

### 第 8 篇　結語與附錄（50 頁｜PPT Part 19）

**第 28 章　學習路徑與結語（12）** — 從零到熟手路線、下一步。
- 附錄 A　指令速查表（10）
- 附錄 B　Settings / Permissions 速查（8）
- 附錄 C　中英名詞對照表（6）
- 附錄 D　疑難排解 FAQ（8）
- 附錄 E　資源連結總整理（6）

---

## 四、自製範例插入對照表

| 自製範例 | 路徑 | 插入章節 |
|---|---|---|
| weekly-haiku | `Projects/01-weekly-haiku/` | 第 4 章 |
| recipe-genie | `Projects/02-recipe-genie/` | 第 7 章 |
| youtube-notes | `Projects/03-youtube-notes/` | 第 8 章 |
| weekly-reports-skill | `Projects/07-weekly-reports-skill/` | 第 8 章 |
| gitnexus 工具包 | `Projects/build-gitnexus-skill-commandline/` | 第 8 章 |
| pomodoro | `Projects/04-pomodoro/` | 第 9 章 |
| organize-downloads | `Projects/05-organize-downloads/` | 第 10 章 |
| plugins-from-zero | `Projects/plugins-from-zero-to-marketplace/` | 第 11 章 |
| discord-dm-bot | `Projects/06-discord-dm-bot/` | 第 12 章 |
| superpowers / ralph / pr-review / pomocat | `important-plugins/` | 第 16 章 |
| wafer 4-agent | `agent_group_projects/computer-vision-wafer-detection/` | 第 17 章 |
| stock 研究團隊 | `agent_group_projects/stock-groups-skills/` | 第 18 章 |
| Flutter worktree | `agent_teams/ios-app-flutter-dev/` | 第 19 章 |
| 課程工廠 | `agent_group_projects/new-course-material2presentation-blank/` | 第 20 章 |

---

## 五、定價與市場定位

- **頁數**：約 790 頁（正文+附錄），落在 600–800 頁設定上緣。
- **定價**：NT$1,200。
- **同級比較**：台灣技術書多為 NT$520–680 / 約 400–500 頁；本書以「完全攻略 + 獨家熱門 Repo 巡禮 + 多 agent 實戰 + 全彩圖文」的工具書定位，頁數約為一般書的 1.6–1.8 倍，NT$1,200 屬合理偏premium 定位。
- **建議**：可同步出電子版（PDF/EPUB），定價約紙本 7 折（NT$840）以擴大觸及。

---

## 六、給下一輪的提醒（分章生產用）

1. 每章固定六段式骨架：WHY / WHAT / HOW / WHEN / PITFALLS / TEST。
2. 視覺沿用 PPT 的 Midnight Executive 配色（navy `1E2761` + 珊瑚 `D97757`），code block 用 Menlo。
3. 自製範例直接引用 repo 內既有 README/CLAUDE.md，不重寫。
4. 熱門 Repo 的星數/排名標註資料日期（2026-05），避免過時。
5. 全書去除任何公司元素（公開課定位）。
