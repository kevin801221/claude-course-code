---
description: 把你 staged 的 git diff 寫成一首詩當 commit message
allowed-tools: Bash(git diff:*), Bash(git status:*)
---

請依以下步驟產出詩體 commit message：

1. 跑 `git diff --cached` 看 staged 變更
2. 抓變更的「精神」是什麼（在修 bug？加新功能？大重構？）
3. 寫成 4-8 行的中文詩（自由格式，不一定要押韻）
4. 結尾附一行 `--by Claude` 讓人知道是 AI 寫的

## 範例

```
為求一行清淨碼
刪去三百意大利
測試綠燈如春至
不負週末好晴天
--by Claude
```

不要：
- 用 conventional commits 格式（那不是詩）
- 寫太抽象（要看得出在做什麼）
- 美化沒做的事
