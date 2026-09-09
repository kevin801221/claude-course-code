# important-plugins — 真實熱門 plugin 教學參考集

> 這裡收**真實世界最受歡迎的 Claude Code plugin**,clone 進來當教學解剖標的。
> 每個 plugin 都對應課程的一個 feature pillar,讓學生看到「概念」在真實 plugin 裡長什麼樣。
>
> ⚠️ **出處與授權**:以下 plugin 都是第三方/官方作品,非 Kevin 本人所寫,僅作教學參考 clone。
> 各自版權歸原作者,使用請依原 repo 授權。下表附原始出處連結。

## Plugin 清單(對應課程 pillar)

| Plugin | 教什麼 pillar | 一句話 | 作者 / 出處 |
|---|---|---|---|
| [`superpowers/`](superpowers/README.md) | **Skills**(Part 8) | 一整套工作流 skill(TDD、brainstorming、寫計畫、用 worktree…),含 marketplace | Jesse Vincent ・ [obra/superpowers](https://github.com/obra/superpowers) |
| [`ralph-wiggum/`](ralph-wiggum/README.md) | **Hooks**(Part 9) | 用一個 Stop hook 讓 Claude 不准下班,自動迭代到測試全綠 | Anthropic 官方 ・ [anthropics/claude-code](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) |
| [`pr-review-toolkit/`](pr-review-toolkit/README.md) | **Sub-agents**(Part 7) | 6 個各盯一面的 review agent + 一鍵調度,示範「plugin 打包一整隊 agent」 | Anthropic 官方 ・ [anthropics/claude-code](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit) |

## 配套:用 plugin 做出來的實作專案

| 資料夾 | 是什麼 |
|---|---|
| [`project1-superpowers/`](project1-superpowers/README.md) | 用 superpowers 工作流做出來的真實小工具 **pomocat**(終端番茄鐘),示範「裝了 plugin 之後怎麼產出東西」 |

## 配套教案(walkthrough,本目錄)

| 教案 | 對應 |
|---|---|
| [`plugins_install_and_cases_walkthrough.md`](plugins_install_and_cases_walkthrough.md) | **三支一起**:marketplace 安裝 + plugin 安裝 + 各自實戰案例 + 逐步 prompt |
| [`superpowers_walkthrough.md`](superpowers_walkthrough.md) | superpowers 入門 |
| [`superpowers_production_walkthrough.md`](superpowers_production_walkthrough.md) | 用 superpowers 做到 production(pomocat) |
| [`ralph_wiggum_walkthrough.md`](ralph_wiggum_walkthrough.md) | Ralph 的 Stop hook 自動迴圈 |
| [`pr_review_toolkit_walkthrough.md`](pr_review_toolkit_walkthrough.md) | 一個 plugin 裝一整隊 review agent |

## 三個 plugin 怎麼搭起整套課

```
Skills    → superpowers      :把「做法」打包成可重用能力(一整座 skill 工廠)
Hooks     → ralph-wiggum     :hook 能改寫 Claude 生命週期(Stop hook 自動迴圈)
Sub-agents→ pr-review-toolkit:把一整隊專科 agent 打包成可安裝 plugin(靠 description 自動路由)
```

> **教學金句**:「同樣是 plugin,superpowers 給你一座 skill 工廠、ralph 給你一個會卡住 Claude 的 hook、pr-review-toolkit 給你一整隊 agent —— 三個合起來,就把 plugin 能裝什麼(skill / hook / agent)演完了。」

## 怎麼看 / 怎麼裝

- **教學上**:直接讀各資料夾原始碼(plugin.json / commands / hooks / agents / skills),這是最好的解剖。
- **要真的裝來玩**:在 Claude Code 用 `/plugins` 從對應 marketplace 安裝(官方兩個在 Anthropic 官方 marketplace;superpowers 見其 repo 說明)。

## 怎麼自己加新 plugin 進這個資料夾

1. clone 真實 plugin repo(或從官方 `anthropics/claude-code/plugins/<name>` 取出單一 plugin)
2. 放成 `important-plugins/<name>/`,**去掉巢狀 `.git`**,保留原 README/LICENSE
3. 在本目錄寫一份 `<name>_walkthrough.md`(走 `walkthrough-style`)
4. 更新本 README 的清單表 + 標清楚作者/出處/授權
