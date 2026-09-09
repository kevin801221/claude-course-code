---
name: unit-test-expand
description: 針對未測試的分支與邊界情況擴增測試涵蓋率
---

# 擴增單元測試

依專案的測試框架擴增現有的單元測試：

1. **分析涵蓋率**：執行涵蓋率報告，找出未測試的分支、邊界情況與涵蓋率偏低的區域
2. **找出缺口**：檢視程式碼中的邏輯分支、錯誤路徑、邊界條件、null／空值輸入
3. **撰寫測試**，使用專案的框架：
   - Jest／Vitest／Mocha（JavaScript／TypeScript）
   - pytest／unittest（Python）
   - Go testing／testify（Go）
   - Rust 測試框架（Rust）
4. **鎖定特定情境**：
   - 錯誤處理與例外
   - 邊界值（最小值／最大值、空值、null）
   - 邊界情況與極端情況
   - 狀態轉換與副作用
5. **驗證改善成效**：再次執行涵蓋率報告，確認有可衡量的提升

只呈現新增的測試程式碼區塊，並遵循現有測試的模式與命名慣例。

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/commands
**相容模型**：Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
