# 一份精簡 Context Pack

對應講義 Part 00、08、09，並參考 [PRP 精選範本](../resources/templates/README.md)。

```text
目標：為任務 CLI 新增 list --pending。
先讀：CLAUDE.md、bin/tasks.mjs、src/task-board.mjs、tests/task-board.test.mjs。
已知：資料為 {id:string,title:string,done:boolean}[]；只支援單程序。
限制：不加 npm 套件、不改原始資料、不破壞不帶旗標的 list。
驗收：正常、空集合、全部完成、壞 JSON；npm test 與 npm run check。
先交計畫：列出需要修改的檔案、未確認假設與測試案例。
```

常駐規則放 CLAUDE.md；本次需求放 task card；大量來源按需查；可獨立判斷的工作再交 agent。別把整份教學文件塞進每輪對話。

實驗：用「幫我加個過濾」和上面這份 context 各做一次，只比較是否問對問題、是否保留原行為、是否交出證據，不以回覆長度評分。
