# Lab 00：先知道工具會碰哪些檔案

講義 Part 00～03、05～07。目標是跑通本機專案、區分終端機命令與 Claude 對話指令。

## 操作

1. 在根目錄跑 `npm test`、`npm run tasks -- list`，讀 `bin/tasks.mjs` 與 `src/task-board.mjs`。
2. 有 Claude Code 後，先跑 `claude --version`、`claude --help`，再用 `claude --permission-mode manual` 開啟互動對話。
3. 對 Claude 說：「只讀取 CLAUDE.md、src/、bin/ 與 tests/，解釋現有行為，不修改。」
4. 在互動對話用 `/help`、`/model`、`/permissions` 檢查自己版本實際提供的功能。
5. 用 `/plan` 討論 `list --pending`；確認進入規劃模式後，提出驗收案例。

`npm test`、`claude --help` 在終端機跑；`/help`、`/plan` 在 Claude 互動對話中輸入。模型與功能是否可用以自己的帳號和版本為準。

## 驗收

- 說得出測試用了哪些工具、資料存在哪裡、是否連外。
- 能指出 `CLAUDE.md` 是指示，`settings.json` 是產品設定；指示文字不等同技術權限隔離。
- 能區分需要確認的工具動作與只讀規劃，並在操作後檢查實際檔案。

不要在這個練習開啟跳過權限。根層 `manual` 不保證覆蓋組織管理規則；若畫面不同，先查 `/permissions` 與 [排錯表](../../docs/troubleshooting.md)。
