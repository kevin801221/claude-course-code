# 完整課堂原碼導航

先用根目錄12個Lab熟悉工具，再依講義選下列實戰。course/、references/是來源快照，不會覆蓋根層設定；複製單個專案到Repo外才開始自己的Claude練習。

## 十個功能模組

- [01-slash-commands](course/01-slash-commands/README.md)
- [02-memory](course/02-memory/README.md)
- [03-skills](course/03-skills/README.md)
- [04-subagents](course/04-subagents/README.md)
- [05-mcp](course/05-mcp/README.md)
- [06-hooks](course/06-hooks/README.md)
- [07-plugins](course/07-plugins/README.md)
- [08-checkpoints](course/08-checkpoints/README.md)
- [09-advanced-features](course/09-advanced-features/README.md)
- [10-cli](course/10-cli/README.md)

## 九個核心專題與進階實作

| 專題 | 真正包含的內容 | 依賴/限制 |
|---|---|---|
| [Projects/01-weekly-haiku](course/Projects/01-weekly-haiku/README.md) | git log → 本週俳句的完整 legacy command 範例 | Claude Code；Git repository with commits |
| [Projects/02-recipe-genie](course/Projects/02-recipe-genie/README.md) | 具工具/輸出契約的食譜子代理 | Claude Code subagents |
| [Projects/03-youtube-notes](course/Projects/03-youtube-notes/README.md) | YouTube → 字幕整理 → 繁中學習筆記 Skill | Claude Code；字幕取得工具/網路或自己提供字幕 |
| [Projects/04-pomodoro](course/Projects/04-pomodoro/README.md) | PostToolUse 工具次數提醒 Hook | Bash；支援 terminal-notifier / osascript / notify-send 之一才有通知 |
| [Projects/05-organize-downloads](course/Projects/05-organize-downloads/README.md) | 檔案系統 MCP 整理 Downloads 設定示例 | Claude Code；Node/npx；filesystem MCP package；自己授權的資料夾 |
| [Projects/06-discord-dm-bot](course/Projects/06-discord-dm-bot/README.md) | Discord 文字冒險 bot：實際為 Gemini SDK，不是 Claude Agent SDK | Python；discord.py>=2.3；google-genai>=1.0；DISCORD_TOKEN；GEMINI_API_KEY；Discord Message Content intent |
| [Projects/07-weekly-reports-skill](course/Projects/07-weekly-reports-skill/README.md) | 完整週報 Skill：scripts + references + examples 的黃金結構 | Claude Code；Git；Python；Bash；選用 gh CLI 讀 PR/issues |
| [Projects/08-agent-team-review](course/Projects/08-agent-team-review/README.md) | 四 owner 的 Kanban Agent Teams 練習骨架 | Claude Code Agent Teams 可用；Python/uv；pytest；瀏覽器 |
| [Projects/09-timetrace](course/Projects/09-timetrace/README.md) | TimeTrace SaaS 六模組建構藍圖 | Claude Code；Node.js；uv；視建構階段而定的 MCP/設計/外部服務 |
| [Projects/build-gitnexus-skill-commandline](course/Projects/build-gitnexus-skill-commandline/README.md) | GitNexus command + helper Skill + 安裝/AB實驗協定 | Node/npx GitNexus；可供索引的 Git Repo；Claude Code |
| [Projects/plugins-from-zero-to-marketplace](course/Projects/plugins-from-zero-to-marketplace/README.md) | 三套 Plugin 元件與 marketplace 開發/發佈工作坊 | Claude Code Plugins；Bash；各 Plugin 選用工具 |
| [Projects/Normal-RAG2Graph-Project-claude](course/Projects/Normal-RAG2Graph-Project-claude/README.md) | 額外 RAG/GraphRAG + LLM Wiki 實作，包含兩本不同目的 notebooks | backend Python>=3.13；uv；FastAPI；ChromaDB；google-generativeai；Gemini API key；Node/Next.js15/React19 |
| [Projects/llm-wiki-graph](course/Projects/llm-wiki-graph/README.md) | 可離線跑的原始 JSON → Markdown wiki → 互動圖譜工具與測試 | Python>=3.11；uv；pyproject 無第三方依賴 |
| [agent_group_projects/computer-vision-wafer-detection](course/agent_group_projects/computer-vision-wafer-detection) | 四代理晶圓 pipeline 完整腳本基線 | Python>=3.11；uv；roboflow；Ultralytics/PyTorch；ROBOFLOW_API_KEY；Mac MPS 或自行調整CPU/CUDA |
| [agent_group_projects/computer-vision-wafer-agents-detection-demo](course/agent_group_projects/computer-vision-wafer-agents-detection-demo) | 用 /agents 從零建構的示範版，附資料拆分與推論腳本 | Python>=3.11；uv；Roboflow；YOLO；訓練/推論資源 |
| [agent_group_projects/computer-vision-wafer-template](course/agent_group_projects/computer-vision-wafer-template/README.md) | 學生空白起點，保留與demo對照的領域/流程資料 | Claude Code；實作訓練時再安裝ML環境 |
| [agent_teams/ios-app-flutter-dev](course/agent_teams/ios-app-flutter-dev/README.md) | 原生 Agent Teams 的 arXiv 閱讀器：完成版與課堂起點 | Claude Code Agent Teams；Flutter/Dart ^3.9.2；後端 Python>=3.12/uv；FastAPI；google-genai；GEMINI_API_KEY（真摘要）；iOS/Android平台工具 |
| [context-engineering-intro](course/context-engineering-intro/README.md) | 完整INITIAL → generate-prp → execute-prp → validation工作流 | Claude Code；每use-case各自環境 |
| [context-engineering-intro/use-cases/agent-factory-with-subagents](course/context-engineering-intro/use-cases/agent-factory-with-subagents/README.md) | Pydantic AI agent-factory的專業agents、範例、RAG agent、測試與PRP | Pydantic AI；Python；Postgres/embedding或依agents/rag_agent各自requirements |
| [context-engineering-intro/use-cases/ai-coding-wisc-framework](course/context-engineering-intro/use-cases/ai-coding-wisc-framework/README.md) | WISC Context Engineering 知識框架 | Claude Code；文檔為主 |
| [context-engineering-intro/use-cases/ai-coding-workflows-foundation](course/context-engineering-intro/use-cases/ai-coding-workflows-foundation/README.md) | 標準實作/規劃/驗證工作流範本 | Claude Code；各模板工具 |
| [context-engineering-intro/use-cases/build-with-agent-team](course/context-engineering-intro/use-cases/build-with-agent-team/README.md) | 原生Agent Team流程Skill | Claude Code Agent Teams |
| [context-engineering-intro/use-cases/mcp-server](course/context-engineering-intro/use-cases/mcp-server/README.md) | TypeScript MCP建構樣板 | Node.js；npm package.json/lock；TypeScript |
| [context-engineering-intro/use-cases/pydantic-ai](course/context-engineering-intro/use-cases/pydantic-ai/README.md) | Pydantic AI 範本產生與tool/structured-output/測試示例 | Python；Pydantic AI；按例子設模型憑證 |
| [context-engineering-intro/use-cases/template-generator](course/context-engineering-intro/use-cases/template-generator/README.md) | Context模板產生工作流 | Claude Code |

## 優先使用的課堂修正版

- [週報Skill](classroom-fixes/weekly-reports/README.md)：完整資料流與JSON escaping回歸驗證。
- [匿名檔案MCP](classroom-fixes/mcp-sandbox/README.md)：新設定格式、只操作練習資料夾。
- [本機Plugin marketplace](classroom-fixes/plugin-marketplace/README.md)：正確manifest、三個完整Plugin、可選副作用。

## 五庫精華與實際工作流

- [完整繁中參考](references/zh-TW/README.md)：39篇核心文件加訪談選讀；English欄位與指令保留。
- [英文工作流](references/english-workflows/README.md)：RPI/Agents/Commands、Agent Teams時間卡、音效Hook、缺漏設定參考。根設定已改為source檔，手動選用。
- [Howto功能版本對照](references/howto/README.md)：十模組完整原始版本，對照course較新版，而非只留一個doc-generator。
- [Matt完整原文](references/matt-flow-mods/README.md)：核心TSX、測試、術語、tracker/domain契約、設計歷史；[學生導讀](advanced/matt-flow-mods/STUDENT-GUIDE.md)。
- [平台操作](docs/platform-guide.md)：CLI/IDE/Desktop/Remote/Cowork/Artifacts等對應Part15。

## 狀態必須分清楚

- Discord來源真的使用Gemini SDK，不是Claude Agent SDK。
- TimeTrace是完整「課堂藍圖」，沒有現成SaaS成品。
- arXiv有完成版及已有骨架的課堂版，保留Flutter平台檔、圖示與lockfile。
- ML保留訓練/推論程式、設定與Agent契約，不附資料集、權重或大量歷史預測圖。
- llm-wiki的raw/wiki也是測試fixture，已完整保留；只移除可再生成graph.html/畫布截圖。
- 各專案需自己的環境與帳號；本包不會一次安裝所有依賴或對外呼叫。

[逐章覆蓋](docs/lecture-map.md) · [來源原有問題](docs/upstream-issues.md) · [v1漏收了什麼](docs/v1-coverage-gaps.md) · [驗證範圍](docs/v2-verification.md)
