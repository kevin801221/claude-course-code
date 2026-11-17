---
name: weekly-haiku
description: 根據最近七天的 Git commit 訊息，寫中文 5-7-5 字的工作俳句。
disable-model-invocation: true
allowed-tools: Bash(git log *)
---

1. 執行 `git log --since="7 days ago" --pretty=format:"%s"`，只取目前專案近七天的 commit 訊息。
2. 如果沒有 commit，直接說明沒有素材，不杜撰工作內容。
3. 抓出工作主旋律，寫三行中文，字數依序為 5、7、5 字，再附一句英文解釋。
4. 逐行數字確認，保留 Git 內容有證據支持的主題。

只讀取 history，不建立 commit、不推送、不修改專案。
本 Skill 是原 command 的學生版轉寫，改成目前 repo 的所有作者，避免本機 email 與歷史作者不同導致空結果。
