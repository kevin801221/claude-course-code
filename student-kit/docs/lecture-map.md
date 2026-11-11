# 講義 → 實作對照

依 `Claude_Code_完整教學_v13_2_講師版_2026-10-2.pdf` 的目錄與各 Part 起始頁整理。原檔有 **609 個 PDF 實體頁**，頁腳標示總計 **610 張投影片**；從第二個 PDF 頁起，頁腳號碼比 PDF 閱讀器頁碼大 1。下表同列兩種編號，避免課堂找錯頁。封面與隱藏講師導覽不另複製到學生包。

| Part | 內容 | 講義印刷頁碼 | PDF 實體頁碼 | 本包實作 |
|---|---|---|---|---|
| 00 | 核心概念 | 10–33 | 9–32 | [對應內容](../labs/00-cli/README.md) |
| 01 | 認識 Claude Code | 34–42 | 33–41 | [對應內容](../labs/00-cli/README.md) |
| 02 | CLI 基礎與模型 | 43–64 | 42–63 | [對應內容](../labs/00-cli/README.md) |
| 03 | 內建 Slash Commands | 65–79 | 64–78 | [對應內容](../labs/00-cli/README.md) |
| 04 | 自訂 Slash Commands | 80–90 | 79–89 | [對應內容](../labs/02-commands/README.md) |
| 05 | Settings | 91–104 | 90–103 | [對應內容](../labs/00-cli/README.md) |
| 06 | Permissions / Sandbox | 105–121 | 104–120 | [對應內容](../labs/00-cli/README.md) |
| 07 | 日常操作與效率 | 122–144 | 121–143 | [對應內容](../labs/00-cli/README.md) |
| 08 | CLAUDE.md / Memory | 145–170 | 144–169 | [對應內容](../labs/01-memory/README.md) |
| 09 | Context Engineering | 171–192 | 170–191 | [對應內容](../labs/01-memory/README.md) |
| 10 | Skills | 193–236 | 192–235 | [對應內容](../labs/03-skills/README.md) |
| 11 | Sub-agents 與平行化 | 237–293 | 236–292 | [對應內容](../labs/04-agents/README.md) |
| 12 | Hooks | 294–337 | 293–336 | [對應內容](../labs/05-hooks/README.md) |
| 13 | MCP | 338–362 | 337–361 | [對應內容](../labs/06-mcp/README.md) |
| 14 | Plugins / Mods + Lab | 363–478 | 362–477 | [對應內容](../labs/07-plugins/README.md) |
| 15 | IDE、平台與 Artifacts | 479–506 | 478–505 | [對應內容](../docs/reading-guide.md) |
| 16 | Headless / 自動化 | 507–516 | 506–515 | [對應內容](../labs/09-automation/README.md) |
| 17 | GitHub 精選資源 | 517–546 | 516–545 | [對應內容](../SOURCES.md) |
| 18 | 4-Agent ML Pipeline | 547–554 | 546–553 | [對應內容](../labs/10-projects/README.md) |
| 19 | 可驗收的成果 | 555–566 | 554–565 | [對應內容](../docs/task-card.md) |
| 20 | 實戰疑難雜症 | 567–574 | 566–573 | [對應內容](../docs/troubleshooting.md) |
| 21 | 學習路徑與結語 | 575–585 | 574–584 | [對應內容](../README.md) |
| A | 版本變更對照 | 586–602 | 585–601 | [對應內容](../docs/compatibility.md) |
| B | AgenticRAG | 603–609 | 602–608 | [對應內容](../advanced/project-recipes/agentic-rag/README.md) |

## 選材原則

- Part 00～13 濃縮成一個共用任務專案，讓每種擴充可單獨觀察與測試。
- Part 14 拆成本機 Plugin 與 [Mods 選修](../labs/11-mods/README.md)，避免混淆事件 API。
- Part 15 是平台功能導讀，未虛構 IDE/Artifacts 程式範例；依官方文件與實際帳號示範。
- Part 17 用固定 commit 來源索引取代大清單；Part 18 與附錄 B 用小配方理解流程。
- Part 19 的任務卡、證據與交接觀念貫穿每堂，Part 20 的常見錯誤整理為排錯表。

完整 PDF 未隨包發行；來源檔名與 SHA-256 記在 manifest，供講師確認依據版本。
