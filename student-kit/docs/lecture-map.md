# 講義內容覆蓋矩陣（v2）

每個Part分開記錄「原碼」「模板/骨架」「導讀」「缺件」，不再以一個入門Lab連結代表整章已收齊。講義印刷總頁數610，實際PDF609頁；兩種定位均保留。

| Part | 內容 | 印刷/PDF頁碼 | 本包實際狀態 | 入口 |
|---|---|---|---|---|
| 00 | 核心概念 | 10–33 / 9–32 | 完整參考 | [why-harness-is-important.md](../references/zh-TW/reports/why-harness-is-important.md)、[claude_concepts_guide.md](../course/claude_concepts_guide.md) |
| 01 | 認識 Claude Code | 34–42 / 33–41 | 完整導讀 | [README.md](../course/README.md)、[LEARNING-ROADMAP.md](../course/LEARNING-ROADMAP.md) |
| 02 | CLI 基礎與模型 | 43–64 / 42–63 | 完整來源模組 | [README.md](../course/10-cli/README.md)、[claude-cli-startup-flags.md](../references/zh-TW/best-practice/claude-cli-startup-flags.md) |
| 03 | 內建 Slash Commands | 65–79 / 64–78 | 完整參考與範例 | [README.md](../course/01-slash-commands/README.md)、[claude-commands.md](../references/zh-TW/best-practice/claude-commands.md) |
| 04 | 自訂 Slash Commands | 80–90 / 79–89 | 完整原碼 | [01-slash-commands](../course/01-slash-commands)、[01-weekly-haiku](../course/Projects/01-weekly-haiku) |
| 05 | Settings | 91–104 / 90–103 | 設定參考（需按版本調整） | [claude-settings.md](../references/english-workflows/best-practice/claude-settings.md)、[09-advanced-features](../course/09-advanced-features) |
| 06 | Permissions / Sandbox | 105–121 / 104–120 | 完整參考（不自動套用） | [09-advanced-features](../course/09-advanced-features)、[compatibility.md](../docs/compatibility.md) |
| 07 | 日常操作與效率 | 122–144 / 121–143 | 完整參考 | [08-checkpoints](../course/08-checkpoints)、[tips](../references/zh-TW/tips) |
| 08 | CLAUDE.md / Memory | 145–170 / 144–169 | 完整原碼與範本 | [02-memory](../course/02-memory)、[claude-memory.md](../references/zh-TW/best-practice/claude-memory.md) |
| 09 | Context Engineering | 171–192 / 170–191 | 完整來源專題 | [context-engineering-intro](../course/context-engineering-intro)、[context-pack.md](../docs/context-pack.md) |
| 10 | Skills | 193–236 / 192–235 | 完整來源與修正版 | [03-skills](../course/03-skills)、[03-youtube-notes](../course/Projects/03-youtube-notes)、[07-weekly-reports-skill](../course/Projects/07-weekly-reports-skill)、[weekly-reports](../classroom-fixes/weekly-reports)、[build-gitnexus-skill-commandline](../course/Projects/build-gitnexus-skill-commandline) |
| 11 | Sub-agents 與平行化 | 237–293 / 236–292 | 完整原碼／骨架並列 | [04-subagents](../course/04-subagents)、[agent_teams](../course/agent_teams)、[agent_group_projects](../course/agent_group_projects)、[development-workflows](../references/english-workflows/development-workflows) |
| 12 | Hooks | 294–337 / 293–336 | 完整原碼與修正版 | [06-hooks](../course/06-hooks)、[04-pomodoro](../course/Projects/04-pomodoro)、[pomodoro](../examples/lecture-mini-projects/pomodoro) |
| 13 | MCP | 338–362 / 337–361 | 完整設定範例／課堂修正版 | [05-mcp](../course/05-mcp)、[05-organize-downloads](../course/Projects/05-organize-downloads)、[mcp-sandbox](../classroom-fixes/mcp-sandbox) |
| 14 | Plugins / Mods + Lab | 363–478 / 362–477 | 完整原碼／現版打包示例 | [07-plugins](../course/07-plugins)、[plugins-from-zero-to-marketplace](../course/Projects/plugins-from-zero-to-marketplace)、[important-plugins](../course/important-plugins)、[plugin-marketplace](../classroom-fixes/plugin-marketplace)、[matt-flow-mods](../references/matt-flow-mods) |
| 15 | IDE、平台與 Artifacts | 479–506 / 478–505 | 平台操作導讀；無對應本機程式 | [platform-guide.md](../docs/platform-guide.md) |
| 16 | Headless / 自動化 | 507–516 / 506–515 | 完整CLI參考／SDK來源差異標示 | [10-cli](../course/10-cli)、[summarize.sh](../scripts/summarize.sh)、[06-discord-dm-bot](../course/Projects/06-discord-dm-bot) |
| 17 | GitHub 精選資源 | 517–546 / 516–545 | 完整來源索引 | [SOURCES.md](../SOURCES.md)、[full-manifest.json](../sources/full-manifest.json)、[README.md](../references/zh-TW/README.md) |
| 18 | 4-Agent ML Pipeline | 547–554 / 546–553 | 完整ML原碼；不含資料/權重/實驗輸出 | [computer-vision-wafer-detection](../course/agent_group_projects/computer-vision-wafer-detection)、[computer-vision-wafer-template](../course/agent_group_projects/computer-vision-wafer-template)、[computer-vision-wafer-agents-detection-demo](../course/agent_group_projects/computer-vision-wafer-agents-detection-demo) |
| 19 | 可驗收的成果 | 555–566 / 554–565 | 任務方法／PM範本與來源延伸 | [task-card.md](../docs/task-card.md)、[handoff-template.md](../docs/handoff-template.md)、[claude-config](../course/claude-config)、[09-timetrace](../course/Projects/09-timetrace) |
| 20 | 實戰疑難雜症 | 567–574 / 566–573 | 排錯與來源已知問題 | [troubleshooting.md](../docs/troubleshooting.md)、[upstream-issues.md](../docs/upstream-issues.md) |
| 21 | 學習路徑與結語 | 575–585 / 574–584 | 完整路徑與課堂導航 | [CLASSROOM.md](../CLASSROOM.md)、[WALKTHROUGH.md](../course/WALKTHROUGH.md) |
| A | 版本變更對照 | 586–602 / 585–601 | 版本差異參考 | [compatibility.md](../docs/compatibility.md) |
| B | AgenticRAG | 603–609 / 602–608 | 講義指定Notebook缺件；另收真實RAG專案 | [agentic-rag](../advanced/project-recipes/agentic-rag)、[Normal-RAG2Graph-Project-claude](../course/Projects/Normal-RAG2Graph-Project-claude)、[llm-wiki-graph](../course/Projects/llm-wiki-graph) |

附錄B原版 AgenticRAG / CRAG / AdaptiveRAG notebooks 不在指定五庫；Normal-RAG2Graph 的兩本 notebooks 是不同專案，已清除執行輸出，沒有冒稱補到原版。
