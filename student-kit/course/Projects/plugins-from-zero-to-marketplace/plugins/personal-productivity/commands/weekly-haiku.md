---
description: 用本週 git log 寫一首俳句
allowed-tools: Bash(git log:*)
---

請依以下步驟產出本週工作俳句：

1. 跑 `git log --since="7 days ago" --pretty=format:"%s" --author="$(git config user.email)"`
2. 抓本週主旋律（打 bug / 做新功能 / 重構 / 文件...）
3. 寫一首中文俳句（5-7-5 字）總結本週
4. 附一句英文 one-liner 解釋俳句的隱喻

範例：
> 鍵盤聲不停
> 修了三日舊夢魘
> 終於綠燈亮
> (Three days hunting one bug, finally green CI.)
