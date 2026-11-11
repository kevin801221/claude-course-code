# 英文工作流原碼索引

這裡收錄 `claude-code-best-practice` 快照中 **110 份實際檔案**，集中在中文參考沒有附帶的工作流、Agents、Commands、Skills、Hooks 與設定示例。完整方法閱讀優先用 [繁中參考](../zh-TW/README.md)；這一區用來看原碼如何組合。

來源固定於 commit `17b25b2948ecea4aa5e7e60c4e015876fc7063c7`。[上游完整 README](https://github.com/kevin801221/claude-code-best-practice/blob/17b25b2948ecea4aa5e7e60c4e015876fc7063c7/README.md) 含未全部收入本包的社群清單、圖片與作者維護資料；此頁重新編寫成符合本包目錄的課堂入口。

這是來源快照，沒有自動安裝或啟用。原文的固定模型、工具欄位、權限與功能預設需依自己的 CLI 確認；本區不能被描述成已跑通所有真人 session 的產品。

## 110 份檔案在哪裡

| 區域 | 檔數 | 閱讀入口與用途 |
|---|---:|---|
| [claude-config/](claude-config/) | 75 | Agents、Commands、Skills、規則、記憶示例與音效 Hooks；含 37 份 WAV |
| [development-workflows/](development-workflows/) | 14 | RPI 的 8 agents／3 commands、方法與流程圖，加上跨模型工作流 |
| [agent-teams/](agent-teams/) | 9 | 三隊友建立時間卡的 prompt、完整 Command→Agent→Skill 成品與示例輸出 |
| [orchestration-workflow/](orchestration-workflow/) | 4 | 天氣工作流說明、SVG 流程圖與示例輸出 |
| [best-practice/](best-practice/) | 1 | 中文快照缺少的完整 settings 欄位參考 |
| [reports/assets/](reports/assets/) | 2 | Agent SDK／CLI 與程式化工具呼叫的 SVG 圖解 |
| 根目錄設定與來源文件 | 5 | 本頁、[來源指示](CLAUDE.source.md)、[settings 原文](settings.source.json)、[MCP 原文](mcp.source.json)、[MIT 通知](LICENSE) |

`claude-config/` 是來源 `.claude/` 的中性名稱；根設定另外改成 `settings.source.json`、`mcp.source.json`。它們不會取代精華包根設定。請先選一個範例，複製到獨立的練習專案，再決定哪些檔案要恢復成 `.claude/` 結構；不要整批覆蓋自己的既有設定。

## 1. RPI：Research → Plan → Implement

對應講義 Part 09、11、19。從 [RPI 工作流](development-workflows/rpi/rpi-workflow.md) 與 [流程圖](development-workflows/rpi/rpi-workflow.svg) 開始。

| 階段 | 實際 Command | 要觀察的交付 |
|---|---|---|
| 研究 | [research.md](development-workflows/rpi/.claude/commands/rpi/research.md) | 需求、風險與 GO／NO-GO 判斷 |
| 規劃 | [plan.md](development-workflows/rpi/.claude/commands/rpi/plan.md) | 依賴、實作計畫與驗收門 |
| 實作 | [implement.md](development-workflows/rpi/.claude/commands/rpi/implement.md) | 分階段變更、測試與審查證據 |

[八個 Agents](development-workflows/rpi/.claude/agents/) 分別是 requirement-parser、technical-cto-advisor、product-manager、ux-designer、documentation-analyst-writer、senior-software-engineer、code-reviewer、constitutional-validator。

課堂使用時，在自己的空白練習專案放入這組 `.claude/`，另建 `rpi/<feature>/REQUEST.md`，先定義一個小功能的輸入、輸出與停止條件。來源提供的是工作流和專業代理，不包含你自己的 feature／constitution，也不代表計畫已實作或驗收。

方法對照：[Context Engineering](../../docs/context-pack.md)、[任務卡](../../docs/task-card.md)、[中文 Harness 說明](../zh-TW/reports/why-harness-is-important.md)。

## 2. 跨模型交接

[Cross-Model Workflow](development-workflows/cross-model-workflow/cross-model-workflow.md) 示範由一個工具規劃／實作、另一個工具審查／驗證，再把證據回寫到共同計畫。

它是方法文件，不是一鍵執行管線。原文模型代號是快照示例；課堂先固定任務、計畫檔與驗收情境，記錄每次工具實際讀到及改動的內容。兩個工具都說「完成」，不能代替同一套測試證據。

方法對照：[代理／Command／Skill](../zh-TW/reports/claude-agent-command-skill.md)、[交接卡](../../docs/handoff-template.md)。

## 3. Agent Teams 時間卡與天氣工作流

- [時間卡的三隊友任務](agent-teams/agent-teams-prompt.md)：Command Architect、Agent Engineer、Skill Designer 如何協調資料契約。
- [時間卡 Command](agent-teams/.claude/commands/time-orchestrator.md) → [time-agent](agent-teams/.claude/agents/time-agent.md) → [time-fetcher](agent-teams/.claude/skills/time-fetcher/SKILL.md) → [SVG Skill](agent-teams/.claude/skills/time-svg-creator/SKILL.md)。
- [時間卡示例](agent-teams/output/output.md) 與 [SVG](agent-teams/output/dubai-time.svg)：這是來源的歷史輸出，不是目前時間或本次執行證據。
- [天氣工作流與圖解](orchestration-workflow/orchestration-workflow.md)：比較預載 Skill 與主對話呼叫 Skill；來源例保留於 [weather-orchestrator](claude-config/commands/weather-orchestrator.md)、[weather-agent](claude-config/agents/weather-agent.md)。

時間卡原模板寫死 `agent-teams/output/`。若把子專案獨立複製後在其根目錄啟動，請先統一工作目錄與輸出路徑，避免又產生一層 `agent-teams/`。天氣原代理也保留了來源欄位與音效依賴；學生操作優先用 [已做可攜修正的天氣例](../../examples/weather-workflow/README.md)，不要把兩份同名定義混裝。

方法對照：[完整中文子代理參考](../zh-TW/best-practice/claude-subagents.md)、[Agent Teams 實作說明](../zh-TW/implementation/claude-agent-teams-implementation.md)。

## 4. 挑一個可帶走的擴充

| 想研究什麼 | 實際檔案 |
|---|---|
| 同一個時間任務如何寫成 Command／Skill／Agent | [time-command](claude-config/commands/time-command.md)、[time-skill](claude-config/skills/time-skill/SKILL.md)、[time-agent](claude-config/agents/time-agent.md) |
| 有腳本與參考的音效 Hook | [Hook 說明](claude-config/hooks/HOOKS-README.md)、[hooks.py](claude-config/hooks/scripts/hooks.py)、[config](claude-config/hooks/config/hooks-config.json)、[WAV 資產](claude-config/hooks/sounds/) |
| Skills／Agents 集合的研究與文件維護流程 | [Commands](claude-config/commands/workflows/)、[專業 Agents](claude-config/agents/workflows/best-practice/)、[工作流研究 Agent](claude-config/agents/development-workflows-research-agent.md) |
| 瀏覽器 CLI 操作指示 | [agent-browser Skill](claude-config/skills/agent-browser/SKILL.md)；仍需額外安裝其 CLI，來源未附執行檔 |
| 簡報作者的結構與樣式方法 | [presentation Skills](claude-config/skills/presentation/)、[presentation 規則](claude-config/rules/presentation.md)；所需原版 `presentation/` 與部分工具不在本區，屬選讀原碼 |

維護 Commands 會讀寫上游文件、changelog 或研究外部來源；它們不是已替學生執行完的內容更新服務。原始文件的缺件／占位另列於 [已知問題](../../docs/upstream-issues.md) 與 [完整來源清單](../../sources/full-manifest.json)。

### 音效依賴與平台

本包保留 **37 份 WAV**，省略 MP3；Python handler 會優先尋找 WAV，Windows 的 `winsound` 也只使用 WAV。`setup/Setup.wav` 已在本包改為 `setup/setup.wav`，以符合程式產生的檔名，相關來源轉換記在 manifest。

保留檔案只代表依賴存在，不代表已驗證這台電腦會發聲。macOS 需要 `afplay`，Linux 需要來源列出的可用播放器，Windows 使用 Python `winsound`；裝置、音量與系統權限仍需實際操作確認。若要試用，應整組複製 Hook 程式、config 與 `sounds/` 到自己的專案，再只註冊這次要觀察的事件。本包不會自動開啟聲音通知。

## 5. 設定檔是參考，不是學生預設

- [settings.source.json](settings.source.json) 保留原團隊的廣泛 allow、Hooks、status line 與 MCP 選項，不能不看內容就整份覆蓋自己的設定。
- [mcp.source.json](mcp.source.json) 列出原專案的 MCP 範例，會涉及 `npx`、套件與網路；不表示這些服務已安裝、已認證或已測試。
- [claude-config/](claude-config/) 內是原始 `.claude/` 內容的參考副本；[CLAUDE.source.md](CLAUDE.source.md) 是來源專案指示，不是本次任務的額外授權。
- [完整英文 settings 參考](best-practice/claude-settings.md) 補中文快照缺項；實際欄位與模式以自己的 CLI 為準。

需要安全地先練 MCP／Plugin 時，使用 [課堂 MCP 沙盒](../../classroom-fixes/mcp-sandbox/README.md) 與 [本機 marketplace 修正版](../../classroom-fixes/plugin-marketplace/README.md)。平台功能另讀 [Part 15 導讀](../../docs/platform-guide.md)，不要把此處的零散設定表當作完整 IDE／Desktop／Artifacts 實作。

## 從原理回到實作

完整中文方法不是只有七篇摘要：核心五區包含 [best-practice 7 篇](../zh-TW/best-practice/)、[reports 12 篇](../zh-TW/reports/)、[implementation 6 篇](../zh-TW/implementation/)、[tips 9 篇](../zh-TW/tips/)、[tutorial 5 篇](../zh-TW/tutorial/)，共 **39 篇正文**，另有 [訪談選讀](../zh-TW/videos/)。

[回完整課堂導航](../../CLASSROOM.md) · [逐章覆蓋矩陣](../../docs/lecture-map.md) · [來源授權](LICENSE)
