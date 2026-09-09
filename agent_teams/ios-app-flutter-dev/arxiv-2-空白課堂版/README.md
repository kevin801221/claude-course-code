# arxiv-2 空白課堂版 —— 明天上課現場帶學生開 Agent team

> **這份是給上課現場用的。** 跟完成版同一套方法、同一份規格,差別只是:這裡是**乾淨起手**,
> 現場帶學生從零開一個 Agent team 把「arXiv 每日論文閱讀器 + 呼吸提醒」App 蓋出來。

帶課逐步腳本看 [`WALKTHROUGH.md`](WALKTHROUGH.md)(120 分鐘);要直接貼的提示看 [`../agent-team-playbook.md`](../agent-team-playbook.md)。

## 上課前檢查(老師先做)
- [ ] 已彩排過 [`../arxiv-1-完成版/`](../arxiv-1-完成版/README.md)(自己跑成功過一次)
- [ ] 旗標開好:`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- [ ] `claude --version` ≥ 2.1.32、`flutter --version`、`uv --version` 正常
- [ ] `GEMINI_API_KEY` 已設好(後端摘要要用),確認沒被 commit 進 repo
- [ ] 學生機器若要實際編譯,先裝好 Flutter SDK + uv(只到規劃階段可以先不裝)

## 這裡有什麼

```
arxiv-2-空白課堂版/
├── README.md          # 你正在看的
├── WALKTHROUGH.md     # 120 分鐘帶課敘事(Phase 0-3 + 整合)
└── _Context/
    ├── app-spec.md        # 要蓋成什麼(目標規格)
    ├── team-roles.md      # 誰擁有哪些檔案 + mailbox 規則
    └── research-intake.md # researcher 隊友要查什麼
```

現場跑完,這裡會多出 `backend/`(後端)與 Flutter app 專案(學生看著 Agent team 蓋出來的)。

⚠️ 閱讀疲勞 / 呼吸提醒內容僅供 App 功能設計參考,不構成醫療建議。
