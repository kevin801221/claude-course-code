# Agent Teams：契約先定好，檔案再分給不同隊友

對應講義 Part 11。來源的原生 Teams 實作在 `ios-app-flutter-dev/agent-team-playbook.md`；同 Repo 較早的總覽仍有 worktree 描述，請不要把兩者混成同一套機制。

`source-context/` 保留 [api-contract.md](source-context/api-contract.md) 與 [team-roles.md](source-context/team-roles.md) 的原始內容，展示如何靠契約隔開 Python 後端與 Flutter 前端。它們不是可直接啟動的 App。

## 先做不需 Flutter 的最小演練

1. 在新的練習專案，先確認 Claude 的原生 Agent Teams 功能是否可用；不能使用時改做順序分工，不宣稱已驗證 mailbox。
2. team lead 把範圍縮成三份文件：`backend/plan.md`、`reader/plan.md`、`breathing/plan.md`。
3. 先將 API 契約另存為 `contracts/report.md`，刪掉和本次範圍無關的 Flutter 實作資訊；所有欄位維持同一份定義。
4. 若有原生 Teams，可貼以下提示；沒有則由主對話分次委派同樣任務。

```text
請建立一個 team，先只規劃，不寫 App、不安裝依賴。
team lead 先閱讀 contracts/report.md，定好 Report 欄位與錯誤情境。
backend-owner 只寫 backend/plan.md；reader-owner 只寫 reader/plan.md；
breathing-owner 只寫 breathing/plan.md。
每份文件寫出自己接收的資料、輸出介面與驗收步驟。
需要改 API 欄位時，先向 team lead 討論，由 lead 統一修改契約。
最後由 lead 檢查三份文件的欄位是否一致，列出實際差異。
```

## 驗收

- 三個隊友各自擁有不同檔案，不同時改共用契約。
- 後端與 reader 都使用 `markdownBody`、相同日期格式與錯誤回應，不各自發明欄位。
- 原生 Teams 的共享 task list / mailbox 確實出現才算驗證；一般 sub-agent 交回摘要不算原生 Teams。
- 原文件的閱讀提醒門檻有 playbook 與完成契約的差異，學生版以自己凍結的契約為準，不能兩邊各讀一份。

## 延伸完整 App

[固定版本 playbook](https://github.com/kevin801221/claude-course-code/tree/475fe057ed234f836ff3eb06f4c5eecad9e36332/agent_teams/ios-app-flutter-dev/agent-team-playbook.md) 與 [空白課堂版](https://github.com/kevin801221/claude-course-code/tree/475fe057ed234f836ff3eb06f4c5eecad9e36332/agent_teams/ios-app-flutter-dev/arxiv-2-空白課堂版)。
完整 App 才需要 Python/uv、Flutter、模擬器及對應 API 環境；先走 fixture/sample 資料，再接外部模型。原環境變數與 Teams 啟用方式需在上課當天對照官方文件，不把原版號或 UI 按鍵當成永久保證。
此精華包未啟動原生 Teams、Flutter 或外部模型服務。
