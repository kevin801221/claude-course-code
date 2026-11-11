# Ralph Wiggum Plugin — 講師 Walkthrough

> **對象**:學過 Hooks 基本概念(看過 Part 9)、想看「hook 能做到多狂」的人
> **形式**:講師現場帶 / 自學
> **時長**:40 分鐘
> **產出**:親手跑一次「Claude 自己跳不出來、一直改到測試全綠」的自動迭代迴圈,並看懂背後就是一個 Stop hook
> **核心方法**:用一個官方爆紅 plugin,把「hook 是管 Claude 的 harness」這句話演到底
>
> 來源:Anthropic 官方 `anthropics/claude-code/plugins/ralph-wiggum`(作者 Daisy Hollman)。本資料夾是教學用 clone,非我方作品。

---

## 開場(5 分鐘):這就是 hook 最戲劇化的一課

Part 9 講過「hook 是 harness,不會問 Claude 同不同意就跑」。Ralph 把這句話演到極致:
**用一個 Stop hook 攔截 Claude 的「我做完了要退出」,把同一個 prompt 再餵回去 —— 於是 Claude 被卡在迴圈裡,一直改到任務真的完成。**

| 一般 session | Ralph(Stop hook 迴圈) |
|---|---|
| Claude 覺得做完就停 | Stop hook 攔下退出,再餵同一個 prompt |
| 你要一直手動說「繼續」 | 自己跑,看著測試紅→綠 |
| 靠人判斷何時收工 | 靠 `--completion-promise` 字串 + `--max-iterations` 收工 |

> **教學金句**:「Ralph 證明了一件事 —— hook 不是裝飾,它能直接改寫 Claude 的『生命週期』。一個 Stop hook 就能讓 Claude 不准下班。」

---

## 📁 plugin 解剖(這就是一個極簡 plugin 的範本)

```
ralph-wiggum/
├── .claude-plugin/plugin.json   # plugin 身分證(name/version/description/author)
├── commands/
│   ├── ralph-loop.md            # /ralph-loop:開始迴圈
│   ├── cancel-ralph.md          # /cancel-ralph:中止
│   └── help.md                  # /help
├── hooks/
│   ├── hooks.json               # 把 stop-hook.sh 掛到 Stop 事件
│   └── stop-hook.sh             # ⭐ 核心:攔退出、餵回 prompt、數 iteration
└── scripts/setup-ralph-loop.sh  # 起手設定
```

> **教學金句**:「一個 plugin 最小可以多小?slash command + 一個 hook + 一張 plugin.json,就齊了。Ralph 是學『plugin 結構』的絕佳解剖標的。」

帶學生打開 `hooks/hooks.json` 看它怎麼掛 Stop 事件,再打開 `hooks/stop-hook.sh` 看那段「攔退出→餵回 prompt→比對完成字串→數 max-iterations」的邏輯。這比任何投影片都直接。

---

## Phase 0:環境(5 分鐘)
```bash
claude --version          # 要支援 plugin
# 教學上直接看本資料夾的 ralph-wiggum/ 原始碼即可;
# 要真的裝來玩:用 /plugins 從官方 marketplace 安裝 ralph-wiggum
```

## Phase 1:讀懂 Stop hook ⭐(15 分鐘)
逐行帶 `hooks/stop-hook.sh`,把這四件事指出來:
1. Stop 事件觸發時,hook 用 exit code 阻止正常退出
2. 把原始 prompt 再餵回去(prompt 永遠不變)
3. Claude 看得到自己上一輪改過的檔案 + git 歷史 → 自我修正
4. 比對 `--completion-promise` 字串 / 到 `--max-iterations` 才放行

## Phase 2:跑一次真迴圈(15 分鐘)
找一個有「自動驗證」的小任務現場跑(關鍵:任務要能被測試自動判對錯):
```bash
/ralph-loop "用 TDD 做一個 todo REST API:先寫失敗測試→實作→跑測試→紅就修→全綠輸出 <promise>COMPLETE</promise>" --completion-promise "COMPLETE" --max-iterations 20
```
讓學生看著它紅→改→綠,完成後吐出 promise 字串、迴圈才停。

---

## 常見問題 / FAQ
1. **會不會無限跑爆錢?** 所以**一定要設 `--max-iterations`** 當保險絲,這是課堂鐵則。
2. **completion-promise 能設多個條件嗎?** 不行,精確字串比對;多條件就靠 max-iterations 收。
3. **什麼任務適合 Ralph?** 有明確完成標準 + 能自動驗證(測試/linter)的;**不適合**要人判斷設計、一次性操作、標準模糊的活。
4. **跟 Part 9 的 pomodoro hook 差在哪?** pomodoro 是 Notification/提醒類;Ralph 是 **Stop hook 改寫生命週期**,層級更狠。

---

## 卡點對照表 ⭐
| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 迴圈停不下來 | 沒設 max-iterations / 完成字串沒被輸出 | 一律設 `--max-iterations`;prompt 明確要求輸出 promise 字串 |
| Claude 一直繞同樣的錯 | 任務沒有自動驗證,它看不到「自己錯了」 | 換成有測試/linter 能自動判對錯的任務 |
| 想中途喊停 | — | `/cancel-ralph` |
| 學生想拿來 debug 線上問題 | 用錯場景 | Ralph 是 greenfield/可自動驗證任務用的,不是 production debug |

---

## 講師私房筆記
- **這堂最好接在 Part 9 hooks 之後**:學生剛學完 hook 事件,Ralph 是「同一個機制能多狂」的震撼彈,記憶點極強。
- **故意不設 max-iterations 演一次**(用很小的任務),讓學生體感「保險絲為什麼是鐵則」。
- **強調 operator skill**:Ralph 的 README 自己說「成功靠的是會寫 prompt,不是模型多強」—— 這正好呼應你整套課「prompt/context 工程」的主軸。
- **真實戰績當鉤子**:README 提到「一晚生 6 個 repo」「$297 API 成本完成 $50k 合約」,當開場 hook 學生會坐直。

---

## 一句話總結
> **Ralph Wiggum = 一個 Stop hook 讓 Claude 不准下班,一直改到測試全綠 —— 它是「hook 能改寫 Claude 生命週期」這句話最戲劇化的證明,也是最小可解剖的 plugin 範本。**

---

## 進階閱讀
- 🔗 Hooks 心智模型教案:[`../docs/walkthroughs/hook_walkthrough.md`](../docs/walkthroughs/hook_walkthrough.md)
- 🔗 Part 9 實戰 hook 範例:[`../Projects/04-pomodoro/`](../Projects/04-pomodoro/README.md)
- 🔗 原始技術出處(Geoffrey Huntley):https://ghuntley.com/ralph/
- 🔗 官方原始 plugin:https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum

---

_Last updated: 2026-05-22_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材(同目錄):README(各 plugin)、superpowers_walkthrough.md、pr_review_toolkit_walkthrough.md_
