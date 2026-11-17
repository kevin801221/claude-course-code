# 自訂 slash commands

對應講義 Part 04；練習將固定流程寫成可重複的捷徑。
將 `unit-test-expand.md`、`generate-api-docs.md` 複製到自己的專案 `.claude/commands/`，重開 Claude，輸入 `/unit-test-expand <檔案>` 或 `/generate-api-docs <來源> <輸出>`。

這兩份分別改寫自 course-code 與 howto；兩庫有大量共用內容，因此各功能只保留一份。
學生版拿掉固定模型清單與過期版號，文件指令也不再使用容易誤指向檔案系統根目錄的 `/src/api/`、`/docs/api.md`。

驗收：指令出現在 slash 選單；`$ARGUMENTS` 被使用者輸入取代；輸出範圍與執行證據符合指定任務。
新版 Claude Code 也可用同名 Skill 實作捷徑；不要同時安裝重名 command 與 Skill，以免不清楚實際載入哪份。
