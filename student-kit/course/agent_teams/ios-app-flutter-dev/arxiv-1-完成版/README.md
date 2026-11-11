# arxiv-1 完成版 —— 上課前,你自己用 Agent team 跑一次

> **這份是給你(講師)上課前彩排用的。** 目的:照 [`../agent-team-playbook.md`](../agent-team-playbook.md) 自己開一個 Agent team,
> 把這個「arXiv 每日論文閱讀器 + 呼吸提醒」App 從零蓋到**跑得起來**,先做出「一個成功的成品」當底氣 —— 這樣明天上課你心裡有數。

⚠️ 重點不是「有人幫你把 App 做好放這」,而是「**你親自用 Agent team 把它做出來**」。所以這個資料夾一開始是空的(只有 `_Context` 規格與分工),成品由你開 team 蓋進來。

## 怎麼做(摘要,完整貼上腳本看 playbook)

1. 開旗標 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`,確認 `claude --version` ≥ 2.1.32
2. `cd` 進這個資料夾,開一個乾淨的 `claude`(它就是 team lead)
3. 照 [`../agent-team-playbook.md`](../agent-team-playbook.md) 一步步貼:
   - Step 1 研究先行(spawn researcher 查 arXiv 抓取設定 / 閱讀提醒間隔 / 呼吸節奏)
   - Step 2 凍結規格 + team lead 定 API 契約與 `lib/shared/`
   - Step 3 spawn 三個隊友平行做 backend / reader / breathing
   - Step 4 整合 + 後端 `uv run` 驗收 + 前端 `flutter analyze` / `flutter test`
   - Step 5 關隊友 + 清理 team

## 這裡有什麼

```
arxiv-1-完成版/
├── README.md                     # 你正在看的
└── _Context/
    ├── app-spec.md               # 要蓋成什麼(已是凍結目標)
    ├── team-roles.md             # 誰擁有哪些檔案 + mailbox 規則
    └── research-findings.md      # ← 跑完 Step 1 後,researcher 會把研究結論寫在這
```

跑完 playbook 後,這裡會多出 `backend/`(後端)與 Flutter app 專案(你親手用 team 蓋出來的)。

## 驗收(代表你彩排成功)

```bash
# 後端
cd backend && uv run <啟動指令>     # FastAPI 起得來
curl .../reports/today              # 回得到當天報告(papers 5 篇 + markdownBody)

# 前端
flutter analyze     # No issues found!
flutter test        # 全綠
flutter run         # 能讀報告、閱讀計時到門檻跳呼吸動畫、做完回到閱讀
```

⚠️ 閱讀疲勞 / 呼吸提醒內容僅供 App 功能設計參考,不構成醫療建議。
