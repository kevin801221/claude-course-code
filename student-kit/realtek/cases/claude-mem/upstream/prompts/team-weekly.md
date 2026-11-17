# 主管：團隊週報彙整 Prompt

> 主管端使用。由排程腳本把 `{{WEEK_START}}`、`{{WEEK_END}}`、`{{WEEK_LABEL}}`、`{{TEAM_REPORTS_DIR}}`、`{{REPO_DIR}}` 換成實際值後執行。

請彙整 {{WEEK_LABEL}}（{{WEEK_START}} 到 {{WEEK_END}}）全團隊的週報。

## 步驟

1. 讀取 `{{TEAM_REPORTS_DIR}}` 底下每位成員的 `weekly/{{WEEK_LABEL}}.md`。
2. 有成員缺週報時，改讀他這週的日報。
3. 存成 `{{REPO_DIR}}/reports/team/weekly-{{WEEK_LABEL}}.md`。

## 格式

```markdown
# 團隊週報 {{WEEK_LABEL}}

## 本週總結
<三到五句>

## 各專案進度
| 專案 | 負責成員 | 本週進展 | 狀態 | 風險 |
| --- | --- | --- | --- | --- |

## 跨人趨勢
- 連續延遲的專案：
- 負擔可能過重的成員：
- 多人重複遇到的問題：

## 本週重要決策
- <決策> 〔來源：<成員>/weekly/{{WEEK_LABEL}}.md〕

## 下週重點
- <事項>
```

## 規則

- 每一項引用來源週報。
- 「跨人趨勢」是這份報告的重點，要根據實際內容判斷，沒有就寫「無明顯趨勢」。
- 用繁體中文。
