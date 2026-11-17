---
name: review
description: 對照任務卡審查指定檔案，交出可重現的問題
disable-model-invocation: true
---

審查目標：$ARGUMENTS

1. 先讀根目錄 CLAUDE.md、任務卡、指定檔案和對應測試。
2. 檢查資料遺失、錯誤處理、輸入驗證、相容性。
3. 每個 finding 附檔案位置、觸發情境、影響與驗證方式。
4. 沒有實跑就標示靜態分析；沒有可證實問題就明說未發現。
5. 本次只讀，不修改、不提交、不發布留言。
