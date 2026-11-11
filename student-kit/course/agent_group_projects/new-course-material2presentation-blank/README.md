# Course Factory — 教學課程開發 AI 團隊（空白模板）

> **學什麼**：用 sub-agent + skill + `_Context/` 教學 DNA，組一條「丟主題 → 自動產出整套課程（大綱／投影片／範例程式／評量／講師備忘）」的生產線
> **時長**：首次建構 4–6 小時（含親手寫 `_Context/`），之後每堂新課 ≤ 1.5 小時
> **產出**：4 個 sub-agent + 5 個 skill + 你自己的教學 DNA，一座「無限產出課程的工廠」

## 為什麼這個範例存在？

這是 `agent_group_projects/` 裡**抽象層級最高**的一份。Wafer 那組教你用 agent 團隊「**做某件事**」（晶圓偵測，寫死流程）；這組教你用 agent 團隊「**用某種哲學做事**」（主題無關，靈魂在 `_Context/`）。從「Claude Code 使用者」跨到「**系統設計者**」的分水嶺。

完整建構步驟、設計哲學、自我增生玩法 → 看同目錄 **[`WALKTHROUGH.md`](WALKTHROUGH.md)**（這份 README 只是入口，七階段流程都在那）。

## 這是「空白模板」——裡面的檔案都是 skeleton

| 路徑 | 狀態 | 誰來填、何時填 |
|---|---|---|
| `_Context/*.md` (5) | 🟦 空白 skeleton | **你親自寫**（WALKTHROUGH 階段 2）— 這是教學品味數位化，不交給 AI |
| `CLAUDE.md` | 🟦 範本骨架 | 讀完 `_Context/` 後由你/Claude 補齊（階段 3） |
| `.claude/skills/*/SKILL.md` (5) | 🟦 空白 skeleton | Claude 依你描述生成（階段 4、7） |
| `.claude/agents/*.md` (4) | 🟦 空白 skeleton | 用 `/agents` 互動式建（階段 5、7） |
| `Courses/` | 空 | agent 跑起來自動產出 |

> ⚠️ skeleton 故意留白：填法在 `WALKTHROUGH.md` 對應階段。**不要看到空白就亂補**，先讀 WALKTHROUGH。

## 你會用到的 Claude Code 功能

- [x] sub-agents（4 個，用 `/agents` 建）
- [x] skills（5 個共用工具）
- [x] CLAUDE.md（主小隊長路由）
- [x] `_Context/` 動態載入（教學 DNA）
- [ ] hooks / slash commands（本範例不需要）

## 起手式

```bash
cd agent_group_projects/new-course-material2presentation-blank
claude
# 接著照 WALKTHROUGH.md 七階段走（先做階段 2：親手寫 _Context/）
```

## 流程（七階段，細節在 WALKTHROUGH）

1. 搭骨架（已由本模板完成）
2. **親手寫 `_Context/` 教學 DNA** ⭐ 最重要
3. 補 `CLAUDE.md`（主小隊長大腦）
4. 建第一個 skill（`outline-design`）
5. 用 `/agents` 建第一個 sub-agent（`curriculum-architect` 🟣）
6. 第一次完整跑通（測試）
7. 擴充其餘 3 agent + 4 skill，每建一個立刻測

## 進階閱讀

- 配套教材：[`WALKTHROUGH.md`](WALKTHROUGH.md)（七階段完整建構指引 + 自我增生）
- 對照組：[`../computer-vision-wafer-detection/WALKTHROUGH.md`](../computer-vision-wafer-detection/WALKTHROUGH.md)（領域特定 agent 團隊，對比抽象層級差異）
- 課程教案：[`../../docs/walkthroughs/course_12hr_walkthrough.md`](../../docs/walkthroughs/course_12hr_walkthrough.md)
