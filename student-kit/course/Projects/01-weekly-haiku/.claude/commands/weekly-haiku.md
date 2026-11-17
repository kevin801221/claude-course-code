---
description: 用本週 git log 寫一首俳句總結這週工作
allowed-tools: Bash(git log:*)
---

請依以下步驟產出本週工作俳句：

1. 跑 `git log --since="7 days ago" --pretty=format:"%s" --author="$(git config user.email)"`
2. 讀完所有 commit message，抓到本週的「主旋律」
   （是在打仗 bug？做新功能？大重構？文件補完？）
3. 寫一首中文俳句（5-7-5 字數）總結本週
4. 附一句英文 one-liner 解釋俳句的隱喻

## 範例輸出

```
鍵盤聲不停
修了三日舊夢魘
終於綠燈亮
(Three days hunting one bug, finally green CI.)
```

注意事項：
- 字數嚴格 5-7-5（不要硬湊到 5-7-7）
- 不要 commit log 沒提到的事
- 失敗也照寫（人生本來就不一定贏）
