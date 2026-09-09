# Claude Code 12 小時完整課程 — 講師教案

> **對象**：有寫過 code 的開發者 / 工程師（中階以上、會用 Git、會看 YAML / JSON、會跑終端機）
> **形式**：講師現場帶（兩天 × 6 小時 / 三天 × 4 小時 / 一週 × 4 次 × 3 小時 都可拆）
> **時長**：12 × 60 分鐘 session（不含休息），純內容約 11 小時，含休息 12 小時
> **產出**：學完每人帶走 ⓐ 8 個跑得起來的 Projects ⓑ 一份自己建的 sub-agent + skill + hook + plugin ⓒ Context Engineering 完整流程體感
> **核心方法**：PPT 講觀念（為什麼）→ 切 IDE 跑真實檔案（怎麼做）→ 學員當場跟著敲（記得住）
> **跟現有 WALKTHROUGH.md 的關係**：根目錄 [WALKTHROUGH.md](../../WALKTHROUGH.md) 已寫過 4h / 7h / 2h 時間配置；**這份是 12h 完整版**，每小時細到金句、卡點、Q&A、節奏。

---

## 開場（5 分鐘）：為什麼要 12 小時？

PPT 一共 338 頁、19 個 Part、8 個 Projects、3 個 agent 案例。短時間版本（2h / 4h / 7h）一定要砍東西。**12 小時是「全部不砍」的最小配額**——每個 Part 都能切 IDE、每個案例都能跑完、每個學員都有時間自己動手。

> **教學金句**：「短版本是讓你『知道有這東西』，12 小時版本是讓你『回去能自己用』。」

| 對比 | 短版本 (2-4h) | 12 小時版本 |
|---|---|---|
| 看 PPT | 80% | 50% |
| 切 IDE | 20% | 30% |
| 學員自己敲 | 0% | 20% |
| 帶走的 artifact | 觀念筆記 | 自己建的 sub-agent + skill + hook |
| 最大風險 | 「聽完了但不會用」 | 「節奏掌握失準、超時」 |

---

## 📁 12 小時切割總圖

```
Day 1（6 小時）= 入門到中階
├── Hour 1  · 開場 + Part 1 認識 Claude Code        (純 PPT + 終端 demo)
├── Hour 2  · Part 2-3 CLI + 內建 Slash Commands     (純 PPT + 終端 demo)
├── Hour 3  · Part 4 自訂 Slash Commands ⭐          (切 IDE: 01-weekly-haiku)
├── Hour 4  · Part 5-6 Settings + CLAUDE.md/Memory   (純 PPT + 現場 demo)
├── Hour 5  · Part 7 Sub-agents 入門 ⭐              (切 IDE: 02-recipe-genie)
└── Hour 6  · Part 7 進階：Wafer 4-agent 真實案例    (切 IDE: agent_group_projects/)

Day 2（6 小時）= 中階到進階
├── Hour 7  · Part 8 Skills × 3 範例 ⭐⭐            (切 IDE: 03/07/build-gitnexus)
├── Hour 8  · Part 9 Hooks                           (切 IDE: 04-pomodoro)
├── Hour 9  · Part 10 MCP + Part 12 Agent SDK        (切 IDE: 05-organize / 06-discord-bot)
├── Hour 10 · Part 11 Plugins 入門 + superpowers 14 招 (切 IDE: plugins-from-zero / superpowers)
├── Hour 11 · Part 11 進階：Pomocat 真實案例 + Part 13-17 (切 IDE: project1-superpowers)
└── Hour 12 · Part 18 Context Engineering 實戰 + Part 19 收尾 (切 IDE: wafer-detection)
```

每小時固定結構：
1. **時段表**（PPT 頁數 / 是否切 IDE / 開哪個資料夾）
2. **時間分配**（每 5–15 分鐘做什麼）
3. **教學金句**（1–2 句，必說）
4. **內容重點**（要講清楚的 5–10 點）
5. **動手環節**（如果有切 IDE）
6. **預期 Q&A**（學員一定會問的 2–3 題）
7. **本小時卡點**（學員會在哪卡住）

---

## Phase 0：開課前置檢查（5 分鐘・前一晚就要做）

```bash
# 講師自己的環境
claude --version                    # 確認最新版
which claude && which node          # 確認路徑沒撞
open Claude_Code_完整教學.pptx       # 338 頁能開
code ~/claude-code-complete-tutorial # IDE 開好

# 提前裝（現場裝會卡）
/plugin install superpowers@claude-plugins-official
/plugin install document-skills@anthropic-agent-skills

# 學員端
- 預先發 zip 檔（含 8 個 Projects），不要現場 clone
- Roboflow API Key 預先申請（教 Wafer 案例會用到）
- VS Code / Cursor 任選一個，但講師示範用哪個就要求學員裝那個
```

> **教學金句**：「現場裝環境是教學車禍第一名——前一晚都裝好。」

---

# 🟢 Day 1 · 入門到中階

---

## 🕐 Hour 1 · 開場 + Part 1 認識 Claude Code

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 1–13 |
| 切 IDE | ❌ 純 PPT + 終端機 demo |
| 開哪個資料夾 | — |
| 對應 Project | — |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–5 min | 自我介紹、目錄、規則（休息時間、Q&A 時機） |
| 5–10 min | 一張圖講「為什麼是現在學 Claude Code」（agentic coding 時代） |
| 10–25 min | Claude Code vs Cursor vs Copilot vs Cline 四象限 |
| 25–40 min | 系統需求、安裝、認證（現場 demo `claude --version` + `claude` 進 REPL） |
| 40–55 min | REPL 長相、$ vs `claude` 怎麼切、第一個對話 |
| 55–60 min | Hour 1 收尾 + Q&A |

### 教學金句

> 「Cursor 是『AI 在你的 IDE 裡』，Claude Code 是『AI 在你的終端機裡，IDE 是它的工具』——主從關係相反。」
> 「Claude Code 不是補全工具，是 agent。你給它任務，它自己決定要讀哪幾個檔、跑哪幾個指令。」

### 內容重點

1. **agentic vs autocomplete 的差別**——一句話：Copilot 是「補你下一行」、Claude Code 是「幫你做完一個 PR」
2. **terminal-first 的好處**：不被 IDE 鎖住、能 SSH、能 CI/CD、能 headless
3. **三種計費方式**：API key / Pro / Max（Max 適合每天用）
4. **macOS / Linux / Windows WSL** 都支援，**原生 Windows 不行**
5. **第一次 auth**：`claude` 跳瀏覽器、貼 token、確認帳號

### 預期 Q&A

**Q：跟 Cursor 能不能並用？**
A：能。Claude Code 跑終端、Cursor 跑 IDE。很多人兩個都開。

**Q：API 費用怎麼算？**
A：Claude Code 預設用 Anthropic API 計 token。一天輕用 $1–3 美金，重用 $10+。考慮 Max 訂閱比較划算。

**Q：能離線用嗎？**
A：不能。Claude 是雲端模型，必須連線。

### Hour 1 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 學員 `claude` 跑不起來 | npm 路徑沒進 PATH | `echo $PATH` 看有沒有 npm global bin |
| 認證卡在瀏覽器 | 公司網路擋 Anthropic | 改用 API key 直接設 `ANTHROPIC_API_KEY` |
| 「我裝了但 `claude --version` 找不到」 | brew vs npm 衝突 | 先 `which -a claude` 看裝幾份 |

---

## 🕑 Hour 2 · Part 2-3 CLI 基礎 + 內建 Slash Commands

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 14–35 |
| 切 IDE | ❌ 純 PPT + 終端 demo |
| 開哪個資料夾 | — |
| 對應 Project | — |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–15 min | REPL 互動模式、Print mode (`-p`)、常用 flag |
| 15–25 min | 檔案引用 `@`、記憶觸發 `#`、shell 模式 `!` |
| 25–35 min | 快捷鍵總覽（`Ctrl+R` history、`Ctrl+L` clear、`Esc` interrupt） |
| 35–55 min | 內建 slash commands 速查（`/help` `/clear` `/compact` `/init` `/model` `/agents` `/mcp` `/cost` `/plugin` `/login` 等 20+） |
| 55–60 min | 現場 demo：`/init` 在一個空資料夾，看 Claude 自動產 CLAUDE.md |

### 教學金句

> 「`@` 是『把這個檔讀進來』、`#` 是『把這條規則記下來』、`!` 是『執行 shell』——三個記號搞懂 80% 的 REPL 操作。」
> 「`/init` 是新進專案的『讓 Claude 認識你的 repo』儀式。」

### 內容重點

1. **互動模式 vs Print mode**：互動是聊天、Print 是一次性（適合 pipe / CI）
2. **常用 flag**：`-p` print、`-c` continue、`-r` resume、`--model` 強制模型
3. **三個記號的使用情境**：`@README.md`、`# 這個 repo 只用 uv`、`!ls`
4. **`/compact` 的時機**：context 達到 80% 就該下手，不要等爆
5. **`/cost` 看花多少**、`/status` 看現在 session 狀態

### 動手環節（學員一起跑）

```bash
cd ~/claude-code-complete-tutorial
claude
> @README.md 這個 repo 在幹嘛？
> /cost
> /clear
> 我剛剛問你什麼？  # 預期：忘了，因為 /clear 清掉了
```

### 預期 Q&A

**Q：`/compact` 跟 `/clear` 差在哪？**
A：`/compact` 壓縮但保留上下文摘要、`/clear` 整個清掉。長對話用 `/compact`，換主題用 `/clear`。

**Q：怎麼回到之前的 session？**
A：`claude -r` 列出歷史 session 選一個 resume，或 `claude -c` 接續最後一個。

**Q：可以同時開兩個 session 嗎？**
A：可以，每個終端視窗各一個。記憶（CLAUDE.md、memory）是 repo 共用。

### Hour 2 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `@` 補全沒跳出來 | 沒按到 `@` 後等一下 | 多打幾個字觸發 fuzzy search |
| `/compact` 後 Claude 「忘了」 | 摘要太粗 | 重要規則寫進 CLAUDE.md 而不是靠記憶 |
| Print mode `-p` 沒輸出 | pipe stdin 沒餵 | `echo "問題" \| claude -p` 或 `claude -p "問題"` |

---

## 🕒 Hour 3 · Part 4 自訂 Slash Commands ⭐ 第一次切 IDE

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 36–44 |
| 切 IDE | ✅ **本課第一次切** |
| 開哪個資料夾 | `Projects/01-weekly-haiku/` |
| 對應 Project | weekly-haiku（俳句生成 slash command） |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–15 min | PPT 講 .claude/commands/ 結構、frontmatter、`$ARGUMENTS` |
| 15–20 min | **切 IDE → 開 Projects/01-weekly-haiku/** |
| 20–35 min | 一起讀 `.claude/commands/weekly-haiku.md`（對照 PPT 講的 frontmatter） |
| 35–45 min | 現場跑 `/weekly-haiku`，看輸出 |
| 45–55 min | **學員自己改一個**：把 `/weekly-haiku` 改成 `/daily-mood`，產出今天心情打油詩 |
| 55–60 min | 收尾 + 回 PPT 看 Part 4 剩下幾頁 |

### 教學金句

> 「自訂 slash command = 把你常用的 prompt 封裝起來。寫一次、所有 session 共用、團隊 commit 進 repo 大家都能用。」
> 「Frontmatter 三件套：`name` `description` `allowed-tools`——第三件決定這個指令能不能讀檔、能不能跑 bash。」

### 內容重點

1. **三種放置位置**：`.claude/commands/`（專案）、`~/.claude/commands/`（個人）、`plugins/`（分享）
2. **frontmatter 必填**：`name`、`description`、（可選）`allowed-tools`、`model`
3. **`$ARGUMENTS`** 怎麼接學員輸入：`/weekly-haiku 公司近況`
4. **檔名 = 指令名**：`weekly-haiku.md` → `/weekly-haiku`
5. **能呼叫 shell**：在 command 內部用 `!` 跑 git log，當輸入

### 動手環節

```bash
# 切 IDE
code ~/claude-code-complete-tutorial/Projects/01-weekly-haiku
```

讓學員：
1. 打開 `.claude/commands/weekly-haiku.md` 看內容
2. 在終端跑 `cd Projects/01-weekly-haiku && claude`
3. 打 `/weekly-haiku` 試一次
4. 複製檔案改名 `daily-mood.md`、改內容、再跑 `/daily-mood`

### 預期 Q&A

**Q：commands 寫在 `.claude/commands/` 跟 `~/.claude/commands/` 有差？**
A：專案目錄會 commit 進 git 給團隊共用、家目錄只有自己。優先順序：專案 > 個人。

**Q：可以放 sub-folder 嗎？**
A：可以，路徑會變成 `/folder:command`。例：`.claude/commands/test/run.md` → `/test:run`。

**Q：能呼叫其他 command 嗎？**
A：可以，在 prompt 內提到 `/another-command` Claude 會自己接力。

### Hour 3 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 自訂 command 沒出現 | session 沒重啟 | 退出 claude 再進，或 `/reload` |
| `$ARGUMENTS` 沒值 | 學員打 `/cmd` 沒加參數 | 強調 `/cmd 參數內容` 寫法 |
| frontmatter YAML 報錯 | 縮排或冒號錯 | 直接複製範例改 |

---

## 🕓 Hour 4 · Part 5-6 Settings + CLAUDE.md / Memory

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 45–65 |
| 切 IDE | 部分（現場開 settings.json + CLAUDE.md 對照） |
| 開哪個資料夾 | 本 repo 根目錄 |
| 對應 Project | — |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–25 min | **Part 5 Settings**：三層級配置（user / project / local）、permissions 三大區塊、env vars |
| 25–30 min | 現場開本 repo 的 `.claude/settings.json` 給大家看真實長相 |
| 30–55 min | **Part 6 CLAUDE.md / Memory**：CLAUDE.md 用法、`/memory` 編輯、`#` 即時記、`@` 引用 |
| 55–60 min | 講「auto-memory」（cowork 自動學習）跟全域 `~/.claude/CLAUDE.md` 的差別 |

### 教學金句

> 「Settings 管『Claude 能做什麼』、CLAUDE.md 管『Claude 知道什麼』——前者是權限、後者是知識。」
> 「CLAUDE.md 不是文件給人看的，是『給 Claude 看的 onboarding』——寫法要直白、規則化、不要講廢話。」

### 內容重點

1. **三層級優先順序**：local > project > user（local 不進 git，個人 override）
2. **permissions 三區塊**：`allow` 白名單、`deny` 黑名單、`ask` 詢問
3. **常見 deny 範例**：`Bash(rm -rf:*)`、`Read(.env)`、`Write(/Users/**/.ssh/**)`
4. **CLAUDE.md 三層級**：repo 根 / 子資料夾 / 全域 `~/.claude/CLAUDE.md`
5. **記憶優先順序**：全域 < repo < session 內 `#` 加的
6. **auto-memory（cowork）**：自動把 user feedback 寫進 `~/.claude/projects/*/memory/`

### 動手環節

```bash
# 在 IDE 打開兩個檔案對照
~/.claude/CLAUDE.md                          # 全域偏好（Kevin 的個人慣例）
~/claude-code-complete-tutorial/CLAUDE.md   # 專案規則（教學包專用）
```

讓學員看「全域寫的是 Kevin 個人偏好（用 uv、繁中、commit 用個人帳號）、專案寫的是 repo 規則（怎麼改 PPT、PPT 設計慣例）」。

### 預期 Q&A

**Q：CLAUDE.md 該寫多長？**
A：原則是「上下文預算 < 5%」。500 行內為佳，超過要拆子資料夾 CLAUDE.md。

**Q：`#` 跟 `/memory` 差在哪？**
A：`#` 是「直接記」、`/memory` 是「打開編輯器改記憶檔」。`#` 比較快，`/memory` 比較完整。

**Q：sub-agent 看得到 CLAUDE.md 嗎？**
A：看得到，但只看「啟動時」的 CLAUDE.md。session 中用 `#` 加的不會傳給 sub-agent。

### Hour 4 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `settings.local.json` 不小心 commit | gitignore 沒設 | `.gitignore` 加 `.claude/settings.local.json` |
| CLAUDE.md 寫太多 Claude 「忘了」 | 超過 context 預算 | 拆成幾個子資料夾的 CLAUDE.md |
| permissions 設了還在問 | 拼字錯（`Bash` vs `bash`） | 大小寫嚴格，看 PPT 的精確語法 |

---

## 🕔 Hour 5 · Part 7 Sub-agents 入門 ⭐ recipe-genie

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 66–77 |
| 切 IDE | ✅ |
| 開哪個資料夾 | `Projects/02-recipe-genie/` |
| 對應 Project | recipe-genie（食譜推薦 sub-agent） |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–15 min | PPT 講 sub-agent 是什麼、為什麼用、跟 main session 隔離的好處 |
| 15–25 min | `.claude/agents/*.md` 結構：frontmatter（name / description / tools / model / color） |
| 25–30 min | 切 IDE → 開 `Projects/02-recipe-genie/` |
| 30–45 min | 一起讀 `.claude/agents/recipe-genie.md`，現場跑「我想吃辣的、半小時內、有雞肉」 |
| 45–55 min | **介紹 `/agents` 互動建構流程**（9 個畫面）——下一小時會用到 |
| 55–60 min | 收尾 |

### 教學金句

> 「Sub-agent 不是另一個模型——是『另一個帶不同 system prompt 的 session』，跟主 session 隔離記憶但共享檔案系統。」
> 「Description 寫得好不好決定 agent 會不會被叫——觸發詞要明確，例如『下載資料』『驗證標註』，不要寫『處理事情』。」

### 內容重點

1. **三大用途**：① 隔離 context（避免主 session 爆）② 專業化（同任務反覆用）③ 限制權限（agent 只給 4 個 tool）
2. **frontmatter 五件套**：`name`、`description`（觸發句）、`tools`、`model`、`color`
3. **tools 限制**：給最少必要的，例如 data-hunter 只需 Bash/Read/Write
4. **model 選擇**：複雜推理 `opus`、批次處理 `sonnet`、瑣碎用 `haiku`
5. **觸發方式**：Claude 自動路由（看 description）、或 `@agent-name` 明示

### 動手環節

```bash
code Projects/02-recipe-genie
cat .claude/agents/recipe-genie.md   # 看 frontmatter
claude
> 我想吃辣的、半小時內做完、冰箱有雞肉跟蛋
# 預期：Claude 自動呼叫 @recipe-genie
```

### 預期 Q&A

**Q：sub-agent 能呼叫另一個 sub-agent 嗎？**
A：能。父 agent 在 prompt 內提到 `@another-agent` 會接力。但要小心無限循環。

**Q：sub-agent 跟 skill 差在哪？**
A：agent 是「人格 + 工具」、skill 是「SOP 知識」。agent 能跑 tool、skill 只是給 prompt 指引。下小時細講。

**Q：tools 寫 `*` 跟不寫差在哪？**
A：不寫 = 全給、寫 `*` = 全給（顯式）、寫 `Bash, Read` = 只給這兩個。建議**明列**。

### Hour 5 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| Claude 沒呼叫 agent | description 觸發詞太弱 | 重寫 description，加更多關鍵字 |
| `/agents` 找不到 | tab 沒切到 Agents | 按 `←` 切左邊那個 tab |
| agent 跑了但用錯工具 | 沒設 tools 限制 | 明列 `tools: Bash, Edit, Read, Write` |

---

## 🕕 Hour 6 · Part 7 進階：Wafer 4-agent 真實案例

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 78–84 |
| 切 IDE | ✅ |
| 開哪個資料夾 | `agent_group_projects/computer-vision-wafer-agents-detection-demo/` |
| 對應 Project | Wafer YOLO 4-agent ML pipeline |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–10 min | 為什麼要 4 個 agent 不是 1 個？任務分工的甜蜜點 |
| 10–25 min | **講師 live demo `/agents` 9 個畫面建第一個 agent**（data-hunter） |
| 25–35 min | 帶大家看 4 個 agent 的 frontmatter（color 怎麼選、tools 怎麼限） |
| 35–55 min | 現場接力跑：「幫我抓 WM-811K」→ 🔴 data-hunter → 「驗證並切分」→ 🟡 bbox-labeler |
| 55–60 min | 收尾——training-runner / inference-runner 留學員回家自己跑 |

### 教學金句

> 「⚠️ 在 `/agents` 的 Confirm 畫面，**永遠按 `s`，不要按 `e`**——VS Code 開了 .md tab 沒關，Claude Code 會卡死。」
> 「Wafer 案例的關鍵不是 ML、是『把一個任務拆成 4 個負責人』——這個拆法套到任何 pipeline 都通。」

### 內容重點

1. **任務拆解原則**：階段化（data → label → train → inference）、每個 agent 只做一件事
2. **顏色編碼**：🔴 紅 = 資料源頭、🟡 黃 = 中游處理、🔵 藍 = 訓練、🟢 綠 = 產出
3. **`/agents` 9 個畫面流程**：Agents tab → Create new → Project → Generate with Claude → 描述 → 工具 → 顏色 → Confirm（按 `s`！）
4. **不可協商規則**：training-runner 要「停下來等使用者說 GO」才訓練（避免暴衝）
5. **agent 不是黑箱**：每個 agent 做的事都是檔案 + 指令，全部能追蹤

### 動手環節（講師主導，學員看）

```bash
cd agent_group_projects/computer-vision-wafer-agents-detection-demo
claude
> /agents       # 講師現場建 data-hunter
# ... 9 個畫面走完
> 幫我從 Roboflow 抓 WM-811K 資料集
# 預期：🔴 @data-hunter 跳出來執行
```

學員端：開講義 `WALKTHROUGH.md` 跟著看，**不一起敲**（避免拖節奏）。

### 預期 Q&A

**Q：為什麼 training-runner 要停下來等 GO？**
A：訓練很貴（時間 + token + 電）。要讓人類確認 hyperparameter、check 預估時間，才下手。

**Q：4 個 agent 共用 token 嗎？**
A：每個 sub-agent 有自己的 context window。父 session 只看到 agent 的最終回報。

**Q：如果我想換領域，這個架構通嗎？**
A：通。「下載 → 驗證 → 處理 → 產出」是 universal pattern。下個課程用 Course Factory 就是這個架構抽象化。

### Hour 6 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 按 `e` 之後 Claude Code 停住 | VS Code 開了 .md tab 你沒關 | 關掉 VS Code 那個 tab，下次直接按 `s` |
| Roboflow 下載卡 0% | 資料夾已存在 + overwrite=False | script 加 `overwrite=True` |
| `uv run` vs `.venv/bin/python` 衝突 | 環境隔離不一致 | 統一用 `uv add` + `.venv/bin/python` 跑 |
| MPS 不支援某 op | PyTorch + Apple Silicon 限制 | `export PYTORCH_ENABLE_MPS_FALLBACK=1` |

---

# 🟦 Day 2 · 中階到進階

---

## 🕖 Hour 7 · Part 8 Skills × 3 個範例 ⭐⭐

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 85–97 |
| 切 IDE | ✅ **三次** |
| 開哪個資料夾 | `Projects/03-youtube-notes/` → `Projects/07-weekly-reports-skill/` → `Projects/build-gitnexus-skill-commandline/` |
| 對應 Project | 最小 skill / production skill / command + skill 工具包 |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–15 min | PPT 講 skill = SKILL.md（YAML frontmatter + 內容）、跟 sub-agent 差在哪 |
| 15–25 min | **切 IDE 1：03-youtube-notes（最小 skill）** |
| 25–35 min | **切 IDE 2：07-weekly-reports-skill（production 級）**——對比差在哪 |
| 35–50 min | **切 IDE 3：build-gitnexus-skill-commandline（command + skill 工具包）** |
| 50–60 min | Skill description 怎麼寫才會被觸發（最重要的 5 分鐘） |

### 教學金句

> 「Sub-agent 是『新員工』、Skill 是『員工手冊』——同一個 Claude 翻手冊照做，不開新 session。」
> 「Skill description 寫得好 = 自動觸發；寫得爛 = 要明示 `/skill-name`——前者才是 skill 的精髓。」

### 內容重點

1. **SKILL.md 結構**：YAML frontmatter (`name`、`description`)，下面寫指引內容
2. **三個位置**：`.claude/skills/`（專案）、`~/.claude/skills/`（個人）、plugin 內
3. **description 的觸發力**：寫「Use when X」明確情境，不要寫「is useful for」
4. **rigid vs flexible**：rigid skill（TDD / debugging）嚴格照做、flexible（pattern）可調整
5. **skill 配 command**：例如 `/gitnexus` 命令觸發某個複雜 skill workflow

### 動手環節

每個 Project 開 1 個檔（README.md 或 SKILL.md），對照 PPT 講解差異：

| Project | 看哪個檔 | 重點 |
|---|---|---|
| 03-youtube-notes | `.claude/skills/youtube-notes/SKILL.md` | 最簡 skill 長相 |
| 07-weekly-reports-skill | `.claude/skills/weekly-reports/SKILL.md` | production 級結構（references/、scripts/） |
| build-gitnexus-skill-commandline | `INSTALL.md` + `SKILL.md` | 怎麼包成可分享工具包 |

### 預期 Q&A

**Q：skill 跟 sub-agent 何時用哪個？**
A：要新 context 隔離 → agent；只是給 SOP 不開新 session → skill。Skill 比較輕。

**Q：skill 能呼叫 sub-agent 嗎？**
A：能，skill 內部說「用 Agent tool」就會呼叫。

**Q：skill description 上限多少字？**
A：建議 200 字以內。重點是「具體情境關鍵字」，不是長度。

### Hour 7 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| skill 沒被自動觸發 | description 沒有匹配關鍵字 | 加「Use when 使用者說 X」明確觸發句 |
| `/skills` 看不到自訂 skill | 沒重啟 session | 退出 claude 再進 |
| skill 內部呼叫 agent 失敗 | sub-agent 沒裝在當下 repo | skill 文件提醒 prerequisite |

---

## 🕗 Hour 8 · Part 9 Hooks ⭐ pomodoro

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 98–122 |
| 切 IDE | ✅ |
| 開哪個資料夾 | `Projects/04-pomodoro/` |
| 對應 Project | pomodoro 番茄鐘 hook |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–15 min | PPT 講 8 種 hook event、什麼時候各自觸發 |
| 15–20 min | **澄清頁：「hook event 不是 slash command」**（學員最常搞混） |
| 20–25 min | **澄清頁：`/hooks` TUI 是 read-only 檢視器**（不是註冊地） |
| 25–35 min | 切 IDE → `Projects/04-pomodoro/`，看 `.claude/hooks/` 跟 `settings.json` |
| 35–50 min | 現場 demo：跑一次任務，看 PreToolUse / PostToolUse hook 觸發 |
| 50–60 min | 9 種 event × 30+ 真實應用速覽（PPT Part 9·X）+ Q&A |

### 教學金句

> 「Hook 不會問 Claude 同意才跑——它是『管 Claude 的 harness』。Claude 不知道 hook 存在。」
> 「`/hooks` TUI 是給你『看現在裝了哪些』、不是給你『加新的』——要加 hook 改 settings.json。」

### 內容重點

1. **8 種 event**：SessionStart、UserPromptSubmit、PreToolUse、PostToolUse、Stop、Notification、SubagentStop、PreCompact
2. **hook 跑在哪**：每個 event 觸發時，harness 跑 shell script
3. **PreToolUse 可以擋 tool**：return non-zero exit code → tool 被擋下
4. **註冊方式**：`.claude/settings.json` 的 `hooks` 物件，**不是** `.claude/hooks/` 自動掃描
5. **真實應用**：擋 `rm -rf`、commit 前跑 lint、自動播音、發 Slack、寫 audit log

### 動手環節

```bash
code Projects/04-pomodoro
cat .claude/settings.json   # 看 hooks 物件怎麼綁
cat .claude/hooks/pomodoro.sh  # 看實際 script
```

讓學員試「複製這個 hook 改成『PostToolUse 時印 timestamp』」。

### 預期 Q&A

**Q：hook 失敗會怎樣？**
A：看 event。PreToolUse 失敗 → 擋住 tool；其他 event 失敗 → 只是 log，不影響流程。

**Q：hook 能存取對話內容嗎？**
A：能，event payload 有 prompt / tool input / tool output。stdin 拿到 JSON。

**Q：hook 跑太慢會卡 Claude 嗎？**
A：會。Hook 是同步的。重操作要在 hook 內 `&` 背景跑。

### Hour 8 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 「我寫了 hook 但沒跑」 | 只放 .claude/hooks/ 沒在 settings.json 註冊 | 看 PPT 澄清頁 |
| `/hooks` 想加新的 | 以為 TUI 能編輯 | 改 settings.json，TUI 只是檢視 |
| PreToolUse 沒擋住 | exit code 不是 non-zero | `exit 1` 或 `exit 2` |

---

## 🕘 Hour 9 · Part 10 MCP + Part 12 Agent SDK

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 123–140（MCP）+ 192–203（SDK） |
| 切 IDE | ✅ 兩次 |
| 開哪個資料夾 | `Projects/05-organize-downloads/` + `Projects/06-discord-dm-bot/` |
| 對應 Project | MCP server / Agent SDK Discord bot |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–20 min | **Part 10 MCP**：MCP 是什麼、三種 transport（stdio / SSE / HTTP）、為什麼需要 |
| 20–30 min | 切 IDE → `05-organize-downloads/`，看自寫 MCP server 結構 |
| 30–40 min | `claude mcp add` 三種寫法、settings.json 手寫、安全注意（不要灌爛 server） |
| 40–55 min | **Part 12 Agent SDK**：何時用 SDK 不用 CLI；切 IDE → `06-discord-dm-bot/` |
| 55–60 min | 收尾 |

### 教學金句

> 「MCP 是『把外部資料源 / 工具接到 Claude』的標準協議——Anthropic 版的 LSP。」
> 「Agent SDK 是把 Claude Code 變成 library——當你需要 program 程式碼控制 agent，CLI 不夠就用 SDK。」

### 內容重點

1. **MCP vs hook vs skill**：MCP 接外部、hook 管內部、skill 給 SOP
2. **三種 transport**：stdio（本機 process）、SSE（推送）、HTTP（standard）
3. **常用 MCP server**：filesystem、github、postgres、firecrawl、playwright
4. **Agent SDK 兩種語言**：Python、TypeScript
5. **典型用途**：把 Claude 包進 Discord bot / Slack bot / 排程任務

### 動手環節

```bash
# MCP demo
code Projects/05-organize-downloads
cat .claude/settings.json  # mcpServers 設定
claude
> 幫我整理 ~/Downloads 把超過 30 天的 zip 搬到 archive

# SDK demo
code Projects/06-discord-dm-bot
cat src/index.ts  # 看 Claude.query() 怎麼用
```

### 預期 Q&A

**Q：MCP 跟 sub-agent 哪個應該用？**
A：要接外部資料 → MCP；要分工 → agent。Wafer 案例用 agent + Roboflow SDK（直接 import）就不用 MCP。

**Q：SDK 收費怎麼算？**
A：跟 CLI 一樣，按 token 收。要把 API key 放在 server 環境變數。

**Q：SDK 能不能跑 sub-agent？**
A：能，SDK 有 Agent tool 可呼叫，等於把 CLI 的 agent 系統嵌進你的程式。

### Hour 9 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `claude mcp add` 失敗 | server 路徑寫錯 | 用絕對路徑、確認 server 自己能跑 |
| MCP server 連不上 | stdin/stdout 被汙染 | server 千萬別印 log 到 stdout |
| SDK 跑 Discord bot 沒回應 | bot token 失效或權限不夠 | `.env` 對一下、Discord 端開 message intent |

---

## 🕙 Hour 10 · Part 11 Plugins 入門 + superpowers 14 招

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 141–183 |
| 切 IDE | ✅ 兩次 |
| 開哪個資料夾 | `Projects/plugins-from-zero-to-marketplace/` + `important-plugins/superpowers/` |
| 對應 Project | 自建 plugin / superpowers 14 招 |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–15 min | PPT 講 plugin = skills + agents + commands + hooks 打包，marketplace 是 plugin 集散地 |
| 15–25 min | 釐清誤會：`~/.claude/plugins/` **存在**（Claude Code 自動管的安裝區） |
| 25–35 min | 切 IDE → `plugins-from-zero-to-marketplace/`，看 3 個範例 plugin 從 0 到上架 |
| 35–55 min | 切 IDE → `important-plugins/superpowers/`，看 14 招的 SKILL.md（brainstorming / TDD / debugging / writing-plans 等） |
| 55–60 min | 講 HARD-GATE + Anti-Pattern 三招設計手法 |

### 教學金句

> 「Plugin = .claude/ 的所有東西打包成 zip 給別人 install——marketplace 就是 zip 集散地。」
> 「Superpowers 厲害的不是 14 個 skill，是『SKILL.md 怎麼寫才能讓 Claude 不敢偷懶』——HARD-GATE + Anti-Pattern。」

### 內容重點

1. **plugin 結構**：`plugin.json` + `.claude/` 子目錄（skills / agents / commands / hooks 都可）
2. **marketplace.json**：把多個 plugin 集中讓 `/plugin install` 找得到
3. **`~/.claude/plugins/` 是 Claude Code 管的**：marketplaces/ / data/ / cache/ / installed_plugins.json
4. **5 個必裝**（Kevin 推薦）：superpowers、document-skills、firecrawl、context7、figma
5. **superpowers 三招**：HARD-GATE（紅旗清單）、Anti-Pattern（負面範例）、checklist 強制

### 動手環節

```bash
# 自建 plugin
code Projects/plugins-from-zero-to-marketplace
cat plugin1-hello-skill/plugin.json

# superpowers 內部結構
code important-plugins/superpowers
cat skills/brainstorming/SKILL.md  # 看 HARD-GATE 怎麼寫
```

### 預期 Q&A

**Q：marketplace 一定要 GitHub 嗎？**
A：不一定。可以是 git URL、tarball URL、本機路徑。GitHub 最方便共享。

**Q：plugin 跟單獨 skill 差在哪？**
A：plugin 可以**綁多個**（skill + agent + command 一起）。單獨 skill 只是一份 SKILL.md。

**Q：怎麼讓 plugin 自動更新？**
A：marketplace 端版本號改了，學員 `/plugin update <name>` 拉新版。

### Hour 10 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `/plugin install` 失敗 | marketplace 沒加 | 先 `/plugin marketplace add <url>` |
| plugin 裝了沒效果 | session 沒重啟 | 退出 claude 再進 |
| 自寫 plugin 報錯 | plugin.json 拼字錯 | 對照 official 範例改 |

---

## 🕚 Hour 11 · Part 11 進階 Pomocat 真實案例 + Part 13-17 (純 PPT)

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 184–244（Pomocat 案例 + IDE 整合 + Headless + Permissions + 進階 + GitHub 資源） |
| 切 IDE | ✅ |
| 開哪個資料夾 | `important-plugins/project1-superpowers/` |
| 對應 Project | Pomocat（用 superpowers 開發的真實 app） |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–25 min | 切 IDE → `project1-superpowers/`，看 Pomocat 完整時間軸：brainstorming → spec → plan → implementation |
| 25–40 min | 讀 `docs/superpowers/specs/` 跟 `plans/`——這是 brainstorming + writing-plans 的真實產出 |
| 40–50 min | **Part 13–14**：IDE 整合（VS Code / JetBrains demo）+ Headless（CI/CD） |
| 50–58 min | **Part 15–17**：Permissions 安全 / 進階主題（Output style / statusline / cost）/ GitHub 精選資源 |
| 58–60 min | 收尾預告下一小時 |

### 教學金句

> 「Pomocat 是 superpowers 自己證明自己——『brainstorming → spec → plan → implement』四階段是真的可用，不是教科書理論。」
> 「Headless 模式（`claude -p`）= 把 Claude Code 變 CI/CD 工具——commit 自動寫 changelog、PR 自動 review、issue 自動分類。」

### 內容重點

1. **Pomocat 四階段產出**：spec.md（要做什麼）→ plan.md（怎麼做）→ tasks.md（拆 todo）→ 真實 code
2. **superpowers 不是只有 skill**：它教你「**用 skill 的順序**」——brainstorm 一定在 implement 之前
3. **Part 13 IDE 整合**：VS Code extension 跟 Claude Code CLI 是兩件事，extension 是 GUI、CLI 是引擎
4. **Part 14 Headless**：`claude -p` + pipe，commit hook 跑、CI 跑、cron 跑都行
5. **Part 15 Permissions**：sandbox、deny 重要路徑、`--dangerously-skip-permissions` 慎用
6. **Part 16 進階**：output style（Markdown / JSON 切換）、statusline、background 任務
7. **Part 17 GitHub 資源**：awesome-claude-code、official docs、社群好物

### 動手環節

```bash
code important-plugins/project1-superpowers
ls docs/superpowers/specs/ docs/superpowers/plans/
cat docs/superpowers/specs/*.md | head -100  # 看 spec 長相
```

### 預期 Q&A

**Q：Pomocat 是真的有人在用嗎？**
A：是。Kevin 自己用、寫成 walkthrough 給人學。`project1-superpowers/` 就是它的源碼。

**Q：Headless 跑出來怎麼確認對的？**
A：output 用 JSON 模式 (`--output-format json`)，下游 script parse。或在 Print mode 內加「驗證指令」。

**Q：能不能完全跳過 permissions 自動跑？**
A：能（`--dangerously-skip-permissions`），但**絕對不要在生產環境用**。CI 用 server-side、本機 demo 才用。

### Hour 11 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| spec / plan 文件難讀 | 一次給太多 | 分階段讀，先看 spec，consensus 後再 plan |
| Headless 跑爆 token | 沒設 `/compact` 或時限 | 設 `--max-turns` 或 timeout |
| permissions deny 太多 Claude 不敢動 | 規則太緊 | 從 ask 開始、確認沒問題再升 deny |

---

## 🕛 Hour 12 · Part 18 Context Engineering 實戰 + Part 19 收尾

| 項目 | 內容 |
|---|---|
| PPT 頁碼 | 245–318 |
| 切 IDE | ✅ |
| 開哪個資料夾 | `agent_group_projects/computer-vision-wafer-detection/`（或 `context-engineering-intro/`） |
| 對應 Project | Wafer 4-agent 完整跑 + Context Engineering 流程 |

### 時間分配

| 時段 | 內容 |
|---|---|
| 0–10 min | Part 18 開場：Context Engineering 是什麼、為什麼比 prompt engineering 高一階 |
| 10–25 min | **四步驟流程**：CLAUDE.md → INITIAL.md → `/generate-prp` → `/execute-prp` |
| 25–40 min | 切 IDE → `wafer-detection/` 或 `context-engineering-intro/`，PPT 一頁一步驟對照走 |
| 40–50 min | 心法集（PPT Part 18·5）：AI Skill 實戰架構藍圖 5 條心法快帶 |
| 50–55 min | **Part 19 學習路徑**：新手 30 天計畫、中階 90 天、進階一年 |
| 55–60 min | 一句話收尾 + 課後 resources + 學員自由 Q&A |

### 教學金句

> 「Prompt Engineering 是『把問題講清楚』，Context Engineering 是『把工作環境準備好』——後者一勞永逸。」
> 「`/generate-prp` 是讓 Claude『先寫實作藍圖再動手』——比直接叫它寫 code 成功率高一個數量級。」
> 「課程結束不是結束——回去複用 8 個 Projects、改成你自己的領域，才是真正的開始。」

### 內容重點

1. **Context Engineering vs Prompt Engineering**：前者管整個 repo 設定、後者管單句 prompt
2. **PRP（Project Requirements Prompt）** 四步驟流程
3. **`/generate-prp`**：讀 CLAUDE.md + INITIAL.md → 產出完整實作藍圖
4. **`/execute-prp`**：照 PRP 把功能做出來、自動驗收
5. **心法集 5 條**：架構藍圖、Skill 拆分原則、避免「萬能 Skill」、Skill 跟 agent 何時切換、Production-grade Skill 的長相
6. **學員回家作業**：選一個自己領域的問題，套 Context Engineering 流程做完一輪

### 動手環節

```bash
code agent_group_projects/computer-vision-wafer-detection
cat CLAUDE.md INITIAL.md  # 對照 Part 18·1 + 18·2
# 講師可現場跑 /generate-prp 給大家看
```

### 預期 Q&A

**Q：Context Engineering 跟 superpowers brainstorming 差在哪？**
A：brainstorming 是「對話式釐清需求」、Context Engineering 是「把釐清結果寫成文件給 Claude 看」。兩個串起來最強。

**Q：12 小時學完我要從哪個 Project 開始模仿？**
A：選跟你領域最近的：寫 web → 04-pomodoro（hook）+ 06-discord-bot（SDK）；做資料 → wafer-detection；寫文件 → 07-weekly-reports。

**Q：之後 Claude Code 升級會不會洗掉我學的？**
A：CLI flag 跟 plugin 規格穩定。核心觀念（agent/skill/hook/MCP）是 Anthropic 的長期方向，不會大變。

### Hour 12 卡點

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `/generate-prp` 沒這指令 | context-engineering-intro repo 沒 clone | 先 clone coleam00/context-engineering-intro |
| INITIAL.md 寫太空泛 | 跳過 brainstorming | 強迫先跑 brainstorming skill |
| 學員聽完不知從何下手 | 內容量大、無作業 | 出明確回家作業（下一節） |

---

## 🎓 課後作業（強烈建議派）

1. **第一週**：選 1 個 Project 改成自己領域版本（例：把 02-recipe-genie 改成「程式碼 review 員」）
2. **第二週**：建一個自己的 plugin（包 1 個 skill + 1 個 command）push 到 GitHub
3. **第三週**：用 Context Engineering 流程做一個小專案（INITIAL.md → /generate-prp → /execute-prp）
4. **第四週**：把整套流程寫成 blog / 公司內部 sharing，**教別人就是最好的學習**

---

## ⚠️ 總卡點對照表（12 小時可能踩的所有坑）

| 卡點 | 出現在哪小時 | 真實原因 | 處理 |
|---|---|---|---|
| `claude --version` 找不到 | Hour 1 | npm bin 沒進 PATH | `which -a claude` 排查 |
| 認證卡瀏覽器 | Hour 1 | 公司網路擋 | 直接設 `ANTHROPIC_API_KEY` |
| `@` 補全沒跳 | Hour 2 | 觸發太快 | 多打幾字觸發 fuzzy |
| 自訂 command 沒出現 | Hour 3 | session 沒重啟 | 退出 claude 再進 |
| `settings.local.json` commit 進 git | Hour 4 | .gitignore 沒設 | 加進 .gitignore |
| Claude 沒呼叫 agent | Hour 5 | description 觸發詞弱 | 加關鍵字、明示 `@agent` |
| 按 `e` 之後 `/agents` 停住 | Hour 6 | VS Code 開了 tab 沒關 | 永遠按 `s` |
| MPS 不支援某 op | Hour 6 | PyTorch + Apple Silicon | `PYTORCH_ENABLE_MPS_FALLBACK=1` |
| skill 沒自動觸發 | Hour 7 | description 沒匹配關鍵字 | 加「Use when X」明確情境 |
| `/hooks` 想加 hook | Hour 8 | 以為 TUI 能編輯 | 改 settings.json |
| MCP server 連不上 | Hour 9 | server 印 log 到 stdout | server 改 log 到 stderr |
| `/plugin install` 失敗 | Hour 10 | marketplace 沒加 | 先 `/plugin marketplace add` |
| Headless 跑爆 token | Hour 11 | 沒設 max-turns | 加 `--max-turns` |
| `/generate-prp` 不存在 | Hour 12 | repo 沒 clone | clone context-engineering-intro |

---

## 📝 講師私房筆記

### 節奏控制

- **Day 1 上午（Hour 1–3）**：偏觀念，學員還在熱身。**不要追進度**，寧可砍 Q&A 也要把 Part 4 IDE 第一次切換做完整——這是學員「啊原來這就是 Claude Code」的轉折點。
- **Day 1 下午（Hour 4–6）**：開始切 IDE 高密度切換。**每切一次 IDE 前先在 PPT 暫停 30 秒**讓學員心理切換、別直接切換。
- **Day 2 上午（Hour 7–9）**：學員開始累。Hour 7 Skills 三個範例會超時，**寧可砍 Project 3（build-gitnexus）也要把 production skill (Project 7) 講完整**。
- **Day 2 下午（Hour 10–12）**：高潮段。Pomocat + Context Engineering 是收尾關鍵——這兩段不能砍。Hour 11 的 Part 13–17 五個 part 是 buffer，**時間緊就純 PPT 飛快帶過**。

### 故意踩坑（比口頭講有效）

- **Hour 3**：講師故意在自訂 command 不重啟 session，讓 `/your-cmd` 找不到，然後現場退出再進。學員看到「啊原來要重啟」比聽你說 10 次有用。
- **Hour 5**：講師故意把 sub-agent description 寫得很爛（「處理事情」），然後試「幫我找食譜」Claude 沒呼叫——再改成「當使用者要食譜、料理推薦時」，瞬間就被觸發。對比效果超強。
- **Hour 6**：講師**故意按一次 `e`**，看 Claude Code 卡住，現場示範「按 Ctrl+C 救回來」——學員回去自己踩這個坑機率超高，先讓他們看一次。
- **Hour 8**：故意只把 hook 放 `.claude/hooks/` 不註冊 settings.json，跑一次看沒效果，再加上 settings.json 設定才work。

### 不同學員角色推薦

| 學員角色 | 對哪段最有共鳴 | 給他/她的個人化建議 |
|---|---|---|
| 全端工程師 | Hour 3 / 8 / 9 / 12 | 回去把 commit hook、CI auto-review 接上 |
| ML / 資料工程師 | Hour 6 / 12 | wafer-detection + Context Engineering 直接套到自己 pipeline |
| 技術 PM | Hour 7 / 10 / 11 | Skills + plugins 包 SOP 給團隊用 |
| DevOps / SRE | Hour 8 / 9 / 14 | Hooks + Headless + MCP 接內部 infra |
| 教學者 / 講師 | Hour 11 / 12 | Pomocat + Context Engineering 流程當示範 |

### Kevin 親自驗證的真實狀況

- ✅ 「按 `s` 不要按 `e`」這條我自己踩過——VS Code 真的會卡，不是傳說。
- ✅ Wafer 案例 Roboflow `wm811k-paasr/wm811k v3` 只有 Donut 一個類別、只有 train split——這是教學版本不是 bug。
- ✅ MPS `PYTORCH_ENABLE_MPS_FALLBACK=1` 必設，不然某些 op 直接報錯。
- ✅ superpowers 14 招我**自己整套跑完才寫進 PPT**，不是 paper review。
- ✅ Context Engineering coleam00/context-engineering-intro 我**整個 repo clone 過**，PRP 流程是真的可重現的。
- ⚠️ 12 小時的時間表是「**全部按表操課**」估計，**90% 機率會超時 30–60 分鐘**——預備一個 Hour 13 buffer 給 Q&A，或敢砍 Part 13–17。
- ⚠️ Hour 6 跟 Hour 12 兩段最危險——agent 跑起來常會出意外（網路、API、權限），**前一晚務必把全 pipeline 跑過一次**。

### 課後 Resources（給學員帶走）

```
本 repo 必看：
├── WALKTHROUGH.md                                  ← 各時長配置（4h/7h/2h）
├── docs/walkthroughs/course_12hr_walkthrough.md    ← 你正在讀的這份
├── Claude_Code_建構指南.md                          ← 1559 行完整 reference
└── Projects/README.md                              ← 8 個 Project 總覽

官方：
├── code.claude.com/docs                            ← 官方文件
├── github.com/anthropics/claude-code               ← 官方 issue
└── claude.ai/code                                  ← Web 版

社群：
├── github.com/hesreallyhim/awesome-claude-code     ← Awesome 清單
├── github.com/coleam00/context-engineering-intro   ← Context Engineering 經典
└── github.com/obra/superpowers                     ← superpowers 源頭
```

---

## 一句話總結

> **12 小時 = 8 個 Projects + 3 個 agent 案例 + 4 個心法循環（觀念 → 切 IDE → 動手 → 故意踩坑）—— 學員回去能自己建 sub-agent / skill / hook / plugin / MCP，並用 Context Engineering 跑完自己領域的第一個專案。**

---

## 進階閱讀

- 🔗 [WALKTHROUGH.md](../../WALKTHROUGH.md) — 12h 作戰指揮譜・鳥瞰版（Part×Hour 全景表 + 各刀卡點 + 砍場順序），帶課時主看
- 🔗 [Claude_Code_建構指南.md](../../Claude_Code_建構指南.md) — 1559 行完整 reference
- 🔗 [Projects/README.md](../../Projects/README.md) — 8 個 Projects 總覽
- 🔗 [agent_group_projects/computer-vision-wafer-detection/WALKTHROUGH.md](../../agent_group_projects/computer-vision-wafer-detection/WALKTHROUGH.md) — Hour 6 + Hour 12 用到的 wafer 案例 20K 字講師版
- 🔗 [important-plugins/superpowers_walkthrough.md](../../important-plugins/superpowers_walkthrough.md) — Hour 10 superpowers 14 招導覽
- 🔗 [important-plugins/superpowers_production_walkthrough.md](../../important-plugins/superpowers_production_walkthrough.md) — Hour 11 Pomocat 真實案例 120 分鐘版
- 🔗 [gitnexus_walkthrough.md](gitnexus_walkthrough.md) — Hour 9 加碼：GitNexus knowledge graph 工具深入（接 Part 10 / 16）
- 🔗 [karpathy_skills_walkthrough.md](karpathy_skills_walkthrough.md) — Hour 4 尾 或 Hour 10：Karpathy 4 原則 + 最小 plugin 解剖（接 Part 6 / 11）
- 🔗 [agent_group_projects/new-course-material2presentation-blank/WALKTHROUGH.md](../../agent_group_projects/new-course-material2presentation-blank/WALKTHROUGH.md) — 進階加菜：Course Factory（主題無關的課程開發 agent 團隊，接 Part 7 之後）

---

_Last updated: 2026-05-14_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材（同目錄）：anthropics_marketplace_skills_walkthrough.md、four_skills_walkthrough.md、hook_walkthrough.md、gitnexus_walkthrough.md、karpathy_skills_walkthrough.md_
_主指揮譜：[../../WALKTHROUGH.md](../../WALKTHROUGH.md)（12h 作戰指揮譜・鳥瞰版）_
_對應 PPT：`Claude_Code_完整教學.pptx`（338 頁）_
