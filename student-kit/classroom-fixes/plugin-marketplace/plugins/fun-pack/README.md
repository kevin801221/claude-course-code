# fun-pack：先試沒有自動 Hook 的 Plugin

從精華包根目錄啟動：

```bash
claude --permission-mode manual --plugin-dir ./classroom-fixes/plugin-marketplace/plugins/fun-pack
```

在對話輸入 `/fun-pack:commit-poet`，先在有 staged diff 的練習 Repo 產生草稿；沒有變更時應明說，不建立 commit。食譜 agent 用 WebSearch/WebFetch，需可用網路與模型額度；此處不是醫療或飲食安全專題。

保留來源 agent/command，模型改為 `inherit`，避免強迫固定模型；manifest 改 author object 並移除非現版欄位。沒有自動 Hook、MCP 或安裝腳本。完整本機與 marketplace 流程見 [工作坊首頁](../../README.md)。

**驗證範圍：**靜態 Plugin validation；未呼叫模型、搜尋網站或代使用者提交。

This local workshop plugin drafts text from real staged changes and offers a web-enabled recipe agent. It does not commit, push, install dependencies, or register hooks. Review any generated draft before using it.
