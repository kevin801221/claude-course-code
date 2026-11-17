# recipe-genie：只給搜尋工具的生活子代理

講義 **Part 11，投影片 256–257**（原始 agent 定義在 257，PDF 實體頁 256）。
來源：[固定 commit 原檔](https://github.com/kevin801221/claude-course-code/blob/475fe057ed234f836ff3eb06f4c5eecad9e36332/Projects/02-recipe-genie/.claude/agents/recipe-genie.md)。
`source/agents/recipe-genie.md` 原樣保留，沒有複製 GitHub setup 文件或其他不必要內容。

## 操作

1. 複製原檔到自己練習專案的 `.claude/agents/recipe-genie.md`。
2. 開啟新 Claude 對話，明確說：「請委派 recipe-genie，我有蛋、培根、青菜、白飯，給三道 30 分鐘內的晚餐選項，附來源連結。」
3. 若 WebSearch / WebFetch 提示權限，依課堂示範檢查要存取的網站後再允許。
4. 指定一道選項，要求補完整步驟，核對缺少的食材有列出。

## 驗收與相容性

- 三個選項各有料理名稱/風格、時間/難度、缺少食材、三步摘要。
- 來源是實際搜尋結果，不把推測說成查證；搜尋失敗要明說。
- 原 agent 的工具只有 `WebSearch, WebFetch`，不含 Bash、寫檔或購物工具；它只提供資訊。
- `model: sonnet` 保留模型別名，不綁固定代號；是否能用該模型、搜尋工具依實際帳號與環境。
- CLI 2.1.319 課堂以 `manual` 權限模式示範；此原檔沒有 `permissionMode`，不另改全域設定。
- 已檢查原始 frontmatter；未呼叫外部搜尋、未啟動 Claude 或驗證食譜。課堂操作需連網及可用 Claude 帳號。
