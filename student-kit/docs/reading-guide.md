# 五分鐘選讀：讀完要做出什麼

`claude-code-zh-tw` 是 `shanraisshan/claude-code-best-practice` 的繁體中文翻譯；使用者提供的英文庫是 `kevin801221` fork。兩者共用內容脈絡，不當成兩套互不相關的方法。以下只保留七個閱讀入口，連結固定於本次本機 commit，方便課後追溯。

中文與英文快照日期不同，欄位、模型、權限預設、context 容量與 CLI 旗標以自己安裝版本的 `/help`、`claude --help` 與官方文件為準。以下整理的是可實作的設計方法。

## 1. Part 00 核心概念

來源：[「reports/why-harness-is-important.md」](https://github.com/kevin801221/claude-code-zh-tw/blob/9c6e34d69eee8cf634bbf269df5f812b6e13e987/reports/why-harness-is-important.md)（`claude-code-zh-tw`）。

把輸入資料、可用工具、執行回饋分開看，設計一個有實際驗收的任務。不要把 token 數字或模型比較當成固定規格。

**讀後練習：**拿同一個修改需求，先只給 prompt，再提供檔案、測試指令與驗收；記錄差異。

## 2. Part 04／10／11

來源：[「reports/claude-agent-command-skill.md」](https://github.com/kevin801221/claude-code-zh-tw/blob/9c6e34d69eee8cf634bbf269df5f812b6e13e987/reports/claude-agent-command-skill.md)（`claude-code-zh-tw`）。

Command 是進入點、agent 隔離子任務、skill 封裝可重用知識；本包天氣範例把三者串起來。

**讀後練習：**畫出天氣工作流，指出哪個技能預載、哪個技能由主對話呼叫。

## 3. Part 08 CLAUDE.md／Memory

來源：[「best-practice/claude-memory.md」](https://github.com/kevin801221/claude-code-zh-tw/blob/9c6e34d69eee8cf634bbf269df5f812b6e13e987/best-practice/claude-memory.md)（`claude-code-zh-tw`）。

共用約定寫在根層，特定元件規則靠近該元件；把可直接執行的驗收命令寫進規則。

**讀後練習：**把一份很長的 CLAUDE.md 拆成根層慣例與子目錄說明，再觀察實際載入內容。

## 4. Part 09 Context Engineering／Part 10

來源：[「reports/claude-skills-for-larger-mono-repos.md」](https://github.com/kevin801221/claude-code-zh-tw/blob/9c6e34d69eee8cf634bbf269df5f812b6e13e987/reports/claude-skills-for-larger-mono-repos.md)（`claude-code-zh-tw`）。

區分 skill 的可發現性、description 與完整內容載入；代理 skills: 預載是另一種情境。

**讀後練習：**讓一個 skill 只放簡短流程，把詳細模板放 references，觀察何時讀檔。

## 5. Part 10 Skills

來源：[「tips/claude-thariq-tips-17-mar-26.md」](https://github.com/kevin801221/claude-code-zh-tw/blob/9c6e34d69eee8cf634bbf269df5f812b6e13e987/tips/claude-thariq-tips-17-mar-26.md)（`claude-code-zh-tw`）。

Skill 可以是一個含腳本、範本與參考的資料夾；最有價值的內容通常是專案特有陷阱。

**讀後練習：**替自己的 skill 加入兩個真實 Gotchas，並提供一個成功與一個失敗輸入。

## 6. Part 07 日常操作／Part 09

來源：[「tips/claude-thariq-tips-16-apr-26.md」](https://github.com/kevin801221/claude-code-zh-tw/blob/9c6e34d69eee8cf634bbf269df5f812b6e13e987/tips/claude-thariq-tips-16-apr-26.md)（`claude-code-zh-tw`）。

開始新任務、壓縮現有任務與把子任務委派出去，保留的脈絡不同；選擇前先寫下要保留什麼。

**讀後練習：**寫一份含目標、限制、已驗證事實、下一步的交接摘要。不要把文章中的 1M 或百分比套用到所有帳號。

## 7. Part 04／10／11 整合

來源：[「orchestration-workflow/orchestration-workflow.md」](https://github.com/kevin801221/claude-code-best-practice/blob/17b25b2948ecea4aa5e7e60c4e015876fc7063c7/orchestration-workflow/orchestration-workflow.md)（`claude-code-best-practice`）。

回頭對照上游架構，學會讀實際檔案依賴，而不是把所有 .claude 設定照搬。

**讀後練習：**對照本包可攜版，說明移除音效 hooks 與調整預載 skill 行為的原因。

## 課堂上保留的三個問題

1. 這個資訊應常駐 CLAUDE.md、按需讀取，還是交給獨立代理？
2. 什麼能由程式檢查，什麼仍然需要人工判斷？
3. 出錯時要留下哪些證據，下一個 session 才能接手？

做完後，回到 [天氣工作流](../examples/weather-workflow/README.md) 用實際工具呼叫與輸出檔驗證你的答案。
