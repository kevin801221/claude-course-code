# `anthropics/skills` Marketplace — 從安裝到 10 個必玩 Skill 的 Walkthrough

> **對象**：用過 Claude Code、想加裝官方 Skill 卻不知道從哪開始的工程師
> **形式**：講師現場帶、學生跟著做
> **時長**：90 分鐘
> **產出**：marketplace 安裝完成 + 10 個 skill 各跑過一次應用流程 + 一份可帶走的「以後想用哪個就翻哪頁」對照表
> **核心方法**：先懂 marketplace 概念，再 10 個 skill 各一個 demo prompt

---

## 開場（5 分鐘）：為什麼要學這個？

到目前為止我們學過：
- **Sub-agent**（`/agents`）：「教 Claude 幫你做事的專家分身」
- **Hook**（`settings.json`）：「教 Claude Code harness 在事件流上加規則」

**Skill 是第三條路**：「教 Claude **怎麼做一類特定任務**的可重用 SOP」。

最大差別：
- Sub-agent 是**獨立 AI 實例**，你會把整個任務交出去
- Hook 是**shell 自動化**，跟 AI 無關
- **Skill 是 Claude 自己在主對話裡按需引用的「工作手冊」**——讀進來、照著做、做完繼續對話

> **教學金句**：「Sub-agent 是請外包，hook 是裝門禁，**skill 是給 Claude 自己看的 SOP 手冊**。」

`anthropics/skills` 是**官方維護**的 skill 集合，**有 133k star**，是目前最值得裝的 marketplace。

🔗 **GitHub**：https://github.com/anthropics/skills

---

## 📁 Skill vs. 其他機制 一張圖

| 機制 | 由誰執行 | 何時觸發 | 適合 |
|---|---|---|---|
| Sub-agent | Claude（獨立實例） | description 路由命中 | 把整個子任務外包 |
| Skill | Claude（主對話） | description 命中 → Claude 自己讀進來 | 給工作流程、領域知識、工具 SOP |
| Hook | 你的 shell | 特定事件（PreToolUse 等） | 自動化、安全邊界 |
| Slash command | Claude（主對話） | 你打 `/xxx` | 把長 prompt 模板化 |

---

## Phase 0：環境準備（5 分鐘）

### 檢查清單

```bash
claude --version       # 確認 Claude Code 有裝
node --version         # 18+
```

### 進到你要的專案資料夾（或新開都行）

```bash
cd ~/your-workspace
claude
```

> 💡 marketplace 是**全域**安裝，不會綁專案。在哪開都可以。

---

## Phase 1：安裝 anthropics/skills marketplace（10 分鐘）

### Step 1：第一次加 marketplace

在 Claude Code 裡打：

```
/plugin marketplace add anthropics/skills
```

按 Enter。

**這條指令做了什麼？**
- Claude Code 去 clone `https://github.com/anthropics/skills`
- 讀 `.claude-plugin/marketplace.json`（marketplace 的目錄索引）
- 把它註冊成你的可用 marketplace 之一
- **沒裝任何 skill**——只是「把書店加到地圖上」

> ⚠️ **必踩坑**：很多人以為這條就裝完了。沒有！你還要選要裝哪個 plugin。

---

### Step 2：看 marketplace 有什麼

```
/plugin
```

進到 plugin UI，會看到剛剛加的 marketplace（名字大概是 `anthropic-agent-skills` 或類似）。

裡面有兩個 plugin pack：

| Plugin pack | 內容 | 大小 |
|---|---|---|
| `document-skills@anthropic-agent-skills` | 全部 17 個官方 skill（含文件處理、設計、開發） | 大包 |
| `example-skills@anthropic-agent-skills` | 範例 skill（document-skills 的子集合，給人參考寫法） | 小包 |

> 💡 **教學金句**：「document-skills 是『拿來用』，example-skills 是『拿來學寫』。**第一次裝 document-skills 就對了**。」

---

### Step 3：裝 document-skills

```
/plugin install document-skills@anthropic-agent-skills
```

或在 `/plugin` UI 裡選 install。

裝完重啟 Claude Code（**這步絕對不能省**）：

```bash
/exit
claude
```

---

### Step 4：驗證裝好了

```
/skills
```

或在對話框打：

```
你現在裝了哪些 skill？列前 10 個
```

預期會看到 `document-skills:` 開頭的一堆 skill：
```
- document-skills:pdf
- document-skills:docx
- document-skills:xlsx
- document-skills:pptx
- document-skills:skill-creator
- document-skills:mcp-builder
- document-skills:frontend-design
- document-skills:web-artifacts-builder
- document-skills:webapp-testing
- document-skills:canvas-design
...
```

🎉 你完成了 marketplace 安裝。

---

### 補充：移除 / 更新 / 列出

```
/plugin marketplace list                                # 列已加的 marketplace
/plugin marketplace remove anthropics/skills            # 移除整個 marketplace
/plugin uninstall document-skills@anthropic-agent-skills # 移除 plugin
/plugin marketplace update anthropics/skills            # 更新到最新（如官方推新 skill）
```

---

## Phase 2：認識 anthropic/skills 的目錄結構（10 分鐘）

去 GitHub 看一次，建立**對應檔案系統**的直覺。

🔗 https://github.com/anthropics/skills/tree/main/skills

```
skills/
├── algorithmic-art/        # p5.js 算法藝術
├── brand-guidelines/       # Anthropic 品牌色 / 字型
├── canvas-design/          # 海報 / 視覺設計（PNG/PDF）
├── claude-api/             # 用 Anthropic SDK 蓋 app
├── doc-coauthoring/        # 文件協作工作流
├── docx/                   # Word 文件 (生成/編輯/註解)
├── frontend-design/        # 高質感前端 UI（React/Tailwind）
├── internal-comms/         # 公司內部溝通文體
├── mcp-builder/            # 蓋 MCP server
├── pdf/                    # PDF 抽取/生成/合併/拆分/填表
├── pptx/                   # PowerPoint
├── skill-creator/          # 蓋 Skill 的 Skill（元工具）
├── slack-gif-creator/      # Slack 用動畫 GIF
├── theme-factory/          # 預設 10 種主題給 artifact
├── web-artifacts-builder/  # 複雜 React/shadcn artifact
├── webapp-testing/         # Playwright 本機測試
└── xlsx/                   # Excel（公式/分析/視覺化）
```

每個 skill 資料夾通常有：

```
<skill-name>/
├── SKILL.md          # 主要指令（必看！）
├── scripts/          # 可呼叫的 helper script
├── references/       # 進階參考（按需讀）
└── assets/           # 範例檔案、模板
```

> 💡 **教學金句**：「SKILL.md 就像書的封面+第一章，scripts 是附錄，references 是延伸閱讀。**Claude 預設只讀 SKILL.md，需要時才打開 references**。」

---

## Phase 3：10 個必玩 Skill 的應用流程 ⭐ 主菜

> 每個 skill 都按同一個模板講：
> - **是什麼** / **GitHub link** / **能做什麼** / **應用流程** / **示範 prompt**

---

### Skill 1: 🛠 `skill-creator`（元技能，最該先學）

**是什麼**：蓋自己 skill 的 skill。Claude 會引導你拆出 name / description / 主流程 / scripts。

🔗 https://github.com/anthropics/skills/tree/main/skills/skill-creator

**能做什麼**：
- 把你常用的 SOP（例如「我們公司寫 API spec 的 3 段格式」）變成 skill
- 自動生 SKILL.md frontmatter（你不用記 YAML）
- 教你怎麼設計 description 才能被 Claude 路由到

**應用流程**：
1. 想清楚一個你**每天會做 3 次以上**的小任務（例如「把 commit log 翻成中文 changelog」）
2. 對 Claude 打：「用 skill-creator 幫我蓋一個 skill 叫 commit-to-changelog，做 X」
3. Claude 會問你 5–8 個問題：scope、trigger 句、輸入輸出、example 對話、edge case
4. 全部答完，Claude 寫到 `~/.claude/skills/commit-to-changelog/SKILL.md`
5. 重啟 Claude Code，新 skill 可用

**示範 prompt**：
```
用 skill-creator 幫我蓋一個 skill 叫 `weekly-summary`，
任務：讀過去 7 天的 git commit + slack export + GitHub PR，
產出一份中文週報 markdown，分為「完成」「進行中」「下週」三段。
```

> 💡 **教學重點**：學會 skill-creator 之後，你會發現「以後不用記 frontmatter，全部用 skill 幫我蓋」。

---

### Skill 2: 🔌 `mcp-builder`

**是什麼**：教 Claude 怎麼**從零蓋一個 MCP server**——FastMCP (Python) 或 MCP SDK (Node)。

🔗 https://github.com/anthropics/skills/tree/main/skills/mcp-builder

**能做什麼**：
- 從某個 REST API 包出 MCP server，讓 Claude / 別的 LLM 能直接呼叫
- 內含工具設計原則：tool name 怎麼取、description 怎麼寫、schema 怎麼定
- 包含 error handling、auth、testing 模板

**應用流程**：
1. 挑一個你常用的內部 API（公司 ticket 系統、自家資料庫、CRM）
2. 對 Claude 打：「用 mcp-builder 幫我蓋一個 MCP server 連到 X」
3. Claude 會請你提供：API 文件 / OpenAPI schema / 認證方式
4. Skill 帶 Claude 跑：規劃 tools → 寫 server.py → 加 .env → 寫 README
5. 跑 `uv run mcp-server` 本機測，再加到 `~/.claude.json` 的 `mcpServers`
6. Claude Code 重啟，新 MCP tools 出現

**示範 prompt**：
```
我有一個內部 REST API 在 https://api.internal.example.com/v1，
swagger 在 /docs。用 mcp-builder skill 幫我蓋 MCP server，
用 FastMCP + uv，包出 list_tickets / get_ticket / update_status 三個 tool。
```

---

### Skill 3: 📄 `pdf`

**是什麼**：完整 PDF 工具包——讀文字、抽表格、生成新檔、合併、拆分、填表單。

🔗 https://github.com/anthropics/skills/tree/main/skills/pdf

**能做什麼**：
- **讀**：抽出文字 / 表格 / 圖
- **寫**：用 reportlab/PyPDF 產 PDF（含表單 fields）
- **整理**：合併 N 份、拆 1 份、加 watermark、加密
- **OCR**：跟 unstructured 結合做掃描檔抽取

**應用流程**：
1. 把 PDF 拖進對話（或給絕對路徑）
2. Claude 自動引用 `pdf` skill
3. 依任務分流：
   - 「幫我抽第 3–5 頁的表格成 CSV」→ Claude 用 skill 裡的 helper script
   - 「合併這三份 PDF」→ Claude 寫 `merge_pdfs.py` 用 PyPDF
   - 「填這個表格 PDF」→ Claude 讀 form fields 後填入
4. 產出檔案丟回專案

**示範 prompt**：
```
這份 PDF 是去年的財報（attach 進來），幫我：
1. 抽出第 12 頁的損益表變成 markdown 表格
2. 把第 1–10 頁切成單獨檔案 quarterly_report.pdf
3. 在每頁加上 "CONFIDENTIAL" 浮水印
```

---

### Skill 4: 📝 `docx`

**是什麼**：Word 文件 (.docx) 的生成、編輯、註解、tracked changes、格式保留。

🔗 https://github.com/anthropics/skills/tree/main/skills/docx

**能做什麼**：
- 從 markdown / 純文字產出 Word（保留樣式）
- 修改既有 .docx **不破壞既有格式**（這點很值錢）
- 加 tracked changes、加 comments
- 抽文字、抽表格、抽圖片

**應用流程**：
1. 給 Claude 一份 .docx 模板（公司格式）+ 你要的內容大綱
2. Claude 用 `python-docx` 寫填入腳本
3. 產出新 .docx 保留原模板樣式（封面、樣式、頁碼）
4. 需要協作就加 tracked changes，老闆能用 Word 的「審閱」功能審

**示範 prompt**：
```
這是公司提案模板 proposal_template.docx（attach）。
幫我用 docx skill 填入以下內容：
- 標題：「Wafer Defect Detection MVP」
- 摘要：[貼一段]
- 預算表：[3 行]
保留模板所有樣式，產出 proposal_v1.docx。
```

---

### Skill 5: 📊 `xlsx`

**是什麼**：Excel 完整工具包——公式、格式、樞紐、視覺化、保留既有公式編輯。

🔗 https://github.com/anthropics/skills/tree/main/skills/xlsx

**能做什麼**：
- 讀 .xlsx / .xlsm / .csv / .tsv
- **寫公式不只是寫值**（會用 openpyxl 寫 `=SUMIFS(...)` 進儲存格）
- 修改既有試算表**不破壞既有公式**
- 加 chart、加 conditional formatting

**應用流程**：
1. 給 Claude raw CSV 或既有 .xlsx
2. 描述你要的分析：「按月份 group、算各品類銷售、加長條圖」
3. Claude 用 openpyxl 寫腳本，產出含公式 + 圖表的 .xlsx
4. 你打開 Excel，公式還是活的（不是死值）

**示範 prompt**：
```
這是 sales_2025.csv（attach），幫我用 xlsx skill 產一份 dashboard.xlsx：
- Sheet1: 原始資料
- Sheet2: 按月 pivot（用 SUMIFS 公式不是死值）
- Sheet3: 長條圖 + 折線圖
- 樣式：表頭 bold、金額格千分位
```

---

### Skill 6: 🎤 `pptx`

**是什麼**：PowerPoint 生成、編輯、加 speaker notes、layout 操作。

🔗 https://github.com/anthropics/skills/tree/main/skills/pptx

**能做什麼**：
- 從大綱直接產投影片
- 改現有 .pptx 內容**不破壞 master slide**
- 加 speaker notes（presenter view 看得到）
- 套用既有 template（公司模板）

**應用流程**：
1. 給 Claude 一份大綱（markdown 條列）+ 可選的公司 template .pptx
2. Claude 用 python-pptx 寫腳本
3. 每張 slide 對應大綱一段，自動配版面（title slide / content / two-column）
4. 產出 .pptx

**示範 prompt**：
```
幫我把這份 README.md 用 pptx skill 變成 12 張投影片：
- 第 1 張：title slide「Wafer Defect Detection」
- 第 2 張：agenda（自動從章節抽）
- 之後每張對應一個 h2
- 每張加 speaker note：對應段落內文摘要
- 用 anthropic 風格（咖啡橘色）
```

---

### Skill 7: 🎨 `frontend-design`

**是什麼**：產**有設計感、不像 AI 出的**前端 UI。

🔗 https://github.com/anthropics/skills/tree/main/skills/frontend-design

**能做什麼**：
- React / HTML / Tailwind 元件
- **避免 generic AI 樣式**（內含「設計反模式對照表」）
- 含字型配對、色票建議、layout 直覺

**應用流程**：
1. 描述產品定位（B2B SaaS / 個人作品集 / 內部 dashboard）
2. Claude 引用 `frontend-design` skill 出 3 個風格選項
3. 你選風格 → Claude 出完整 React component / Next.js page
4. 可以接著用 `theme-factory` 套主題

**示範 prompt**：
```
用 frontend-design skill 幫我設計一個 wafer defect detection 的內部 dashboard 首頁：
- React + Tailwind + shadcn/ui
- 風格走 industrial（深色 + 單一強調色）
- 含：今日推論 count、最近 10 張預測縮圖、mAP 趨勢圖
- 不要 generic AI 那種藍紫漸層
```

---

### Skill 8: 🧱 `web-artifacts-builder`

**是什麼**：蓋**複雜、多元件、含路由/state**的 Claude.ai HTML artifact。

🔗 https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder

**能做什麼**：
- React + Tailwind + shadcn/ui 三件套
- 多 page 路由、state 管理（zustand 等）
- 適合「給客戶 demo 用的單頁互動 app」

**應用流程**：
1. 描述要做的互動 demo（不只是 hello world、要有狀態）
2. Claude 引用 skill，列出元件樹 + state shape + 路由表
3. 確認後出完整 artifact
4. 在 Claude.ai 直接預覽 / 分享

**示範 prompt**：
```
用 web-artifacts-builder 蓋一個 demo artifact：
「YOLO 預測互動展示」
- 首頁：上傳圖片區 + 預設範例縮圖 6 張
- 點縮圖跳預測頁，顯示 bbox + confidence
- 設定頁：confidence threshold slider，跨頁同步
- 用 shadcn/ui，深色模式
```

---

### Skill 9: 🧪 `webapp-testing`

**是什麼**：用 Playwright 跟本地 web app 互動、測 UI、抓 console log。

🔗 https://github.com/anthropics/skills/tree/main/skills/webapp-testing

**能做什麼**：
- 跑本機 Playwright，點按鈕、填表、截圖
- 抓 browser console error
- 驗 frontend 真的 work（不只是 type check 過）

**應用流程**：
1. 你正在改一個前端功能（例如登入流程）
2. 改完後對 Claude 打：「用 webapp-testing 驗一次登入 happy path」
3. Claude 寫 playwright script 跑：
   - 開 localhost:3000
   - 填 email + password
   - 按 submit
   - assert 跳到 dashboard
   - 截圖存證
4. 失敗 → 顯示哪一步死、印 console error

**示範 prompt**：
```
我的 Next.js app 在 localhost:3000，剛改完 /login 頁面。
用 webapp-testing skill 跑一次：
1. 開 /login
2. 填 test@example.com / Password123
3. 按 sign in
4. 確認 1 秒內跳到 /dashboard
5. 抓所有 browser console error，有就 fail
```

---

### Skill 10: 🖼 `canvas-design`

**是什麼**：產**靜態視覺設計**（海報、卡片、PDF 美編）——用設計原則畫，不抄藝術家。

🔗 https://github.com/anthropics/skills/tree/main/skills/canvas-design

**能做什麼**：
- 用 SVG / Pillow / matplotlib 產 .png / .pdf
- 內含設計原則：對比、留白、層級、字型
- 適合「給社群發的活動圖」「給內部用的封面」

**應用流程**：
1. 描述用途 + 尺寸 + 主視覺元素
2. Claude 用 skill 內的設計原則拆：色票 / 字型 / layout / focal point
3. 出 SVG → 轉 PNG/PDF
4. 不滿意可以指定「再強對比」「字大一點」迭代

**示範 prompt**：
```
用 canvas-design skill 幫我設計一張活動海報：
- 尺寸：1080×1350（IG 直式）
- 主題：「Claude Code Workshop — 用 /agents 蓋 ML pipeline」
- 風格：技術感 + 留白 + 不要漸層
- 必要資訊：日期 2026/06/15 19:00、地點 LINE 線上、報名 QR code（用佔位圖）
```

---

### 🎁 Bonus 4 個值得知道的

| Skill | 一句話 | 場景 |
|---|---|---|
| `claude-api` | 用 Anthropic SDK 蓋 app，內建 prompt caching 建議 | 開發要呼 API 的服務 |
| `doc-coauthoring` | 結構化文件協作工作流（spec / 提案 / decision doc） | 寫長文件、要迭代多次 |
| `internal-comms` | 公司內溝通文體（status report、leadership update、incident report） | 寫週報、寫公告 |
| `slack-gif-creator` | Slack 用動畫 GIF（含尺寸 / 大小 / 動畫限制） | 寫團隊文化、做 react |
| `theme-factory` | 10 種預設主題 / 自製主題套到 artifact | 統一視覺 |
| `brand-guidelines` | Anthropic 官方色 / 字型 | 套 Anthropic 品牌風 |
| `algorithmic-art` | p5.js 算法藝術（flow field、particle） | 玩生成藝術 |

---

## Phase 4：整合 demo — 4 個 skill 接力（15 分鐘）

故事：「我做完 wafer detection MVP，要交付一份完整 deliverable」。

### Step 1：用 `pptx` 產交付簡報

```
用 pptx skill 把這份 README.md 轉成 10 張 demo 簡報
```

### Step 2：用 `xlsx` 產實驗結果表

```
用 xlsx skill 把 Projects/2026-001-mvp/05-results/summary.md 的
mAP/precision/recall 數字做成 dashboard.xlsx，含長條圖
```

### Step 3：用 `pdf` 合併交付包

```
用 pdf skill 把 deck.pdf（投影片）+ dashboard.pdf（試算表）+
predictions.pdf（10 張視覺化）合併成 final_deliverable.pdf，加封面
```

### Step 4：用 `frontend-design` 蓋客戶 demo 頁

```
用 frontend-design skill 蓋一個 single-page React demo，
互動展示這些 prediction 結果（含 confidence slider）
```

**4 個 skill 接力、0 行手刻、1 份完整交付包**。

---

## 常見問題（學生會問）

### Q1：Skill 跟 sub-agent 怎麼選？

- 任務**有清楚的開始/結束 + 你會交給專家全權處理** → sub-agent（例：訓練 YOLO）
- 任務是**主對話中你想要 Claude 照特定流程做** → skill（例：寫公司格式週報）
- **兩者可以混用**：sub-agent 內部也可以引用 skill

### Q2：marketplace 安裝會吃 token 嗎？

不會。**只有實際使用某個 skill 時才會載入它的 SKILL.md**。裝再多 skill 也只是檔案在磁碟上，未觸發不耗 token。

### Q3：Claude 怎麼知道何時用哪個 skill？

靠 SKILL.md 開頭 frontmatter 的 `description`。**寫得好的 description = Claude 自動路由準**。這也是 `skill-creator` skill 存在的原因——它教你怎麼寫 description。

### Q4：可以只裝 marketplace 裡的一個 skill 不要全部嗎？

文件級可以——`/plugin install` 是 pack 級，但你可以裝完後手動移除 `~/.claude/plugins/.../document-skills/skills/<不要的 skill>/`。**不過建議全裝**，未用不耗 token。

### Q5：自己寫的 skill 跟官方 marketplace 衝突嗎？

不會。你的 skill 放 `~/.claude/skills/`，marketplace 裝到 `~/.claude/plugins/`。**重名時 user 級優先**。

---

## 卡點對照表 ⭐ 10 個必踩坑

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `/plugin marketplace add anthropics/skills` 跑完，`/skills` 看不到 | 加完只是註冊書店，沒裝 plugin | 跑 `/plugin install document-skills@anthropic-agent-skills` |
| 裝完 plugin 還是沒生效 | 沒重啟 Claude Code | `/exit` 重開 |
| Claude 沒主動用 skill | 你的描述跟 skill description 不夠像 | 明說「用 `pdf` skill 做 X」 |
| Skill 找不到 helper script | skill 內部 script 路徑不對 | 確認 plugin 解壓正常：`ls ~/.claude/plugins/` |
| 更新 marketplace 後 skill 變了 | 官方 push 新版 | `/plugin marketplace update anthropics/skills` 後重啟 |
| 想看 skill 原始碼 | skill 在 plugin 目錄 | `cd ~/.claude/plugins/ && find . -name SKILL.md` |
| Python skill 跑不起來 | skill 的 helper script 缺套件 | 用 `uv add ...` 加（不要污染 system Python） |
| docx/xlsx 編輯後格式亂掉 | 不是 skill 問題，是 python-docx 限制 | 改用「不要動樣式只填內容」的策略 |
| webapp-testing 連不到 localhost | 你的 dev server 沒開 / port 不對 | 先 `curl localhost:3000` 自測 |
| skill 跟自家 CLAUDE.md 衝突 | CLAUDE.md 規則 > skill | 改 CLAUDE.md 或在 prompt 明說「skill 優先」 |

---

## 講師私房筆記

### 1. 介紹順序的心法

**順序建議**：
1. 先講 marketplace 概念（書店）vs. plugin（書）vs. skill（章節）
2. 安裝 → 看清單 → 隨意挑一個 demo
3. 從 `pdf` 開始（成就感最快、所有人都有 PDF）
4. 進到 `xlsx` / `docx` / `pptx`（文件三件套）
5. 最後示範 `skill-creator`（學員回家最有動力的）

### 2. 故意踩一次：「裝完就走」的坑

很多學生 `/plugin marketplace add` 後就走人。**故意這樣做**讓他們發現「為什麼沒生效」——比口頭講有效。

### 3. 哪些 skill 適合在工作場景馬上用

| 工作角色 | 第一個該裝 |
|---|---|
| 軟體工程師 | `mcp-builder` / `claude-api` |
| 資料科學家 | `xlsx` / `pdf` |
| PM | `docx` / `pptx` / `internal-comms` |
| 設計師 | `canvas-design` / `frontend-design` / `theme-factory` |
| 主管 | `internal-comms` / `doc-coauthoring` |

### 4. Skill 改不到？

很多 skill 是 Apache 2.0，可以 fork。**進階玩法**：
1. fork `anthropics/skills`
2. 改裡面的 SKILL.md（加公司術語、改規則）
3. 自家 repo 用 `/plugin marketplace add your-org/skills`
4. 全公司用同一套客製化 marketplace

### 5. 真的常用前 3 名（Kevin 親自驗）

1. **`pdf`**——日常處理客戶 PDF 抽資料
2. **`skill-creator`**——把自己的 SOP 變 skill
3. **`mcp-builder`**——蓋自家 API 的 MCP 接口

---

## 進階閱讀

- 🔗 [anthropics/skills GitHub](https://github.com/anthropics/skills)
- 🔗 [Agent Skills spec](https://github.com/anthropics/skills/tree/main/spec)
- 🔗 [Skills API Quickstart](https://docs.claude.com/en/api/skills-guide)
- 🔗 [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- 🔗 [Skill template](https://github.com/anthropics/skills/tree/main/template) — 自製 skill 起手式

---

## 一句話總結

> **`/plugin marketplace add anthropics/skills` 是把「整本 Claude 工具書」搬進你的工作環境。
> 你不用每次重新教 Claude 「Word 文件該怎麼編、PDF 怎麼抽、UI 怎麼避免 AI 味」——
> skill 就是 Claude 的『以後不用問』。**

---

_Last updated: 2026-05-12_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材（同目錄）：`hook_walkthrough.md`（hooks）+ `four_skills_walkthrough.md`（4 skill 工作流）_
_專案實戰案例：`../../agent_group_projects/computer-vision-wafer-agents-detection-demo/WALKTHROUGH.md`（sub-agents）_
