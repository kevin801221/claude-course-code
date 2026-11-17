# PR Review Toolkit — 講師 Walkthrough

> **對象**:學過 sub-agent(看過 Part 7)、想看「一個 plugin 裝一整隊專業 agent」的人
> **形式**:講師現場帶 / 自學
> **時長**:45 分鐘
> **產出**:用 6 個官方 review agent 對自己的 diff 做一次多角度審查,並看懂「一個 plugin 怎麼打包一整支 sub-agent 團隊」
> **核心方法**:用官方 plugin 把 Part 7「sub-agent 各擁一個鏡頭」的概念,放到真實 code review 場景
>
> 來源:Anthropic 官方 `anthropics/claude-code/plugins/pr-review-toolkit`(作者 Daisy)。本資料夾是教學用 clone,非我方作品。

---

## 開場(5 分鐘):code review 為什麼適合拆成一隊 agent?

一個人 review PR,常常顧此失彼:盯邏輯就漏了測試、看型別就忘了錯誤處理。
這個 plugin 把 review 拆成 **6 個各盯一個面向的專家 agent**,你問什麼、它自動派對的人上。

| 一個全能 reviewer | 6 個專科 review agent |
|---|---|
| 一個 context 塞所有面向,容易漏 | 每個 agent 只盯一面,挖得深 |
| 結論糊成一團 | 每面各自給嚴重度評分、可行動建議 |
| — | 可單獨叫、可平行全跑 |

> **教學金句**:「這跟我們 stock / wafer 範例的精神一模一樣 —— 鏡頭隔離。差別是:這次是官方把鏡頭打包成 plugin,裝上就有一整隊。」

---

## 📁 plugin 解剖(裝 agent 的 plugin 長這樣)

```
pr-review-toolkit/
├── .claude-plugin/plugin.json   # plugin 身分證
├── agents/                       # ⭐ 6 個 sub-agent,各盯一面
│   ├── comment-analyzer.md           # 註解/文件正確性
│   ├── pr-test-analyzer.md           # 測試覆蓋(行覆蓋 vs 行為覆蓋)
│   ├── silent-failure-hunter.md      # 吞錯/靜默失敗
│   ├── type-design-analyzer.md       # 型別設計(4 維各 1-10 分)
│   ├── code-reviewer.md              # 一般品質 + CLAUDE.md 合規
│   └── code-simplifier.md            # 簡化/重構
└── commands/review-pr.md         # /review-pr:一鍵調度多個 agent
```

> **教學金句**:「Part 7 你學會寫一個 sub-agent;這個 plugin 教你『把一整隊 sub-agent 連同調度指令打包成可安裝的 plugin』—— 這就是從『寫 agent』到『發佈 agent 團隊』的跳躍。」

帶學生打開任一 agent(例 `silent-failure-hunter.md`)看 frontmatter 的 `description` 怎麼用 `<example>` 寫觸發情境 —— 這是讓 Claude **自動路由**到對的 agent 的關鍵。

---

## Phase 0:環境(5 分鐘)
```bash
claude --version
# 教學上直接看本資料夾 pr-review-toolkit/agents/ 原始碼即可;
# 要真的裝:/plugins 從官方 marketplace 安裝 pr-review-toolkit
```

## Phase 1:看懂「description 決定路由」⭐(15 分鐘)
打開 2-3 個 agent,對照它們的 `description`:
- 講「測試覆蓋」→ `pr-test-analyzer`
- 講「錯誤處理 / catch block」→ `silent-failure-hunter`
- 講「型別設計」→ `type-design-analyzer`

重點:**description 寫得越精準(含 example),自動路由越準**。這是 Part 7 沒講透、但實戰最重要的一點。

## Phase 2:對自己的 diff 跑一次(20 分鐘)
在一個有改動的 repo 裡:
```text
我準備開 PR,請幫我:1) 檢查測試覆蓋 2) 找靜默失敗 3) 確認註解正確 4) 一般品質審查
```
看 Claude 依需求**派出對應 agent**、各自回帶嚴重度評分的結構化報告。或直接用 `/review-pr` 一鍵調度。

---

## 常見問題 / FAQ
1. **6 個 agent 會一起跑嗎?** 可單獨叫、可平行全跑(`/review-pr all`),也可只點名某幾個。
2. **它怎麼知道要派哪個 agent?** 靠每個 agent 的 `description`(含 `<example>` 觸發情境)自動路由 —— 講清楚你的關注點命中率最高。
3. **跟我自己在 .claude/agents/ 寫的 agent 衝突嗎?** 不會,plugin 的 agent 與專案 agent 並存;這也是「為什麼要打包成 plugin」的好例子 —— 一次帶一整隊走。
4. **跟 stock/wafer 的 agent 團隊差在哪?** 概念同(鏡頭隔離),但這是「官方打包好、可安裝」的形態,示範 plugin 怎麼承載 agent 團隊。

---

## 卡點對照表 ⭐
| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 該跑的 agent 沒被觸發 | 請求太籠統 | 講明面向(「測試覆蓋」/「錯誤處理」)或直接點名 agent |
| agent review 到不相干的檔 | 沒限定範圍 | 指定檔案 / branch / 「最近的改動」/ PR 編號 |
| 報告太多看不完 | 一次全跑 6 個 | 聚焦改動檔,先處理高嚴重度(agent 已排序) |
| 想理解路由原理 | — | 打開 agent frontmatter 的 `description`,看 example 怎麼寫 |

---

## 講師私房筆記
- **接在 Part 7 sub-agent 之後教最順**:學生剛會寫單一 agent,這裡讓他們看「一整隊 + 自動路由 + 打包成 plugin」的完整形態。
- **對照自家範例**:跟 `agent_group_projects/stock-groups-skills`、`wafer-detection` 一起講 —— 「鏡頭隔離」是同一招,官方 plugin 只是把它產品化。
- **重點敲 description**:現場故意把請求講得很模糊,看 agent 不觸發;再講清楚,看它精準上 —— 學生立刻懂「description 是路由的命脈」。
- **誠實邊界**:這 6 個是 review/分析型 agent,給的是建議與評分,**不會自動改你的 code**;要不要採納還是人決定。

---

## 一句話總結
> **PR Review Toolkit = 把 6 個「各盯一面」的 review sub-agent 連同調度指令打包成官方 plugin —— 它示範了從『寫一個 agent』到『發佈一整隊 agent』的跳躍,而路由的命脈是 description。**

---

## 進階閱讀
- 🔗 Part 7 sub-agent 實戰:[`../Projects/02-recipe-genie/`](../Projects/02-recipe-genie/README.md)
- 🔗 自家多 agent 團隊範例:[`../agent_group_projects/stock-groups-skills/`](../agent_group_projects/stock-groups-skills/README.md) ・ [`../agent_group_projects/computer-vision-wafer-detection/`](../agent_group_projects/computer-vision-wafer-detection/WALKTHROUGH.md)
- 🔗 官方原始 plugin:https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit

---

_Last updated: 2026-05-22_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材(同目錄):README(各 plugin)、superpowers_walkthrough.md、ralph_wiggum_walkthrough.md_
