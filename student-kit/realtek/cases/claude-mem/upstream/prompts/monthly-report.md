# 每月報告 Prompt

> 由排程腳本把 `{{MONTH}}`（YYYY-MM）、`{{REPO_DIR}}`、`{{AUTHOR}}` 換成實際值後執行。

請幫我寫 {{MONTH}} 的個人月報。

## 步驟

1. 讀取 `{{REPO_DIR}}/reports/weekly/` 底下涵蓋 {{MONTH}} 的所有週報。
2. 週報不足時，讀取 `{{REPO_DIR}}/reports/daily/` 底下 {{MONTH}} 的日報補足。
3. 存成 `{{REPO_DIR}}/reports/monthly/{{MONTH}}.md`。

## 月報格式

```markdown
# 月報 {{MONTH}}（{{AUTHOR}}）

## 本月關鍵成果（3 到 5 項）
- <成果> 〔來源：weekly/<週次>.md〕

## 各專案狀態
| 專案 | 本月進展 | 目前狀態 | 下月目標 |
| --- | --- | --- | --- |

## 本月重要決策
- <決策> 〔來源：weekly/<週次>.md 或 meetings/<檔名>〕

## 反覆出現的問題
- <問題與建議的改善方向>

## 下月計畫
- <事項>
```

## 規則

- 每一項附來源，引用週報或日報檔名。
- 重點放在成果與趨勢，不要重複週報細節。
- 用繁體中文。

## 送出

送出目的地：`{{REPORT_DESTINATION}}`（空白代表只存檔，略過這一段）

- `notion`：用 Notion 連接器，在資料庫 {{NOTION_REPORT_DB}} 新增一頁，標題 `月報 {{MONTH}} {{AUTHOR}}`，屬性：成員 = {{AUTHOR}}、類型 = 月報、日期 = {{DATE}}。資料庫沒有的欄位就略過；已有同標題頁面時更新它。
- `jira`：用 Atlassian 連接器，在 issue {{JIRA_ISSUE}} 新增一則留言，內容為完整月報。
- 送出失敗時不要改用其他方式，在回覆裡說明原因；月報檔案仍然要存好。

最後只回覆一行：月報存放的路徑，以及是否已送出。
