---
name: slide-content
description: 撰寫投影片內容（純文字中間態，不含 Marp 語法）。當要把章節大綱展開成逐頁講解內容時使用。主題無關。
---

# slide-content（空白 skeleton）

> 🟦 skeleton。Claude 依描述生成正式版（WALKTHROUGH 階段 7），或補滿 TODO。
> **鐵則**：主題無關，風格從 `_Context/` 載入。本 skill 只產「內容」，格式化交給 marp-render。

## 觸發時機

把某章節展開成逐頁投影片內容（純文字）。

## 開工前必讀

- `_Context/teaching-philosophy.md`
- `_Context/slide-design-rules.md`
- 目標課程 `01-syllabus.md`

## 工作流程

<!-- TODO 階段 7：
1. 讀 syllabus 抓該章節目標
2. 依 slide-design-rules 把內容拆成「一頁一概念」
3. 每頁附 speaker notes
4. 輸出純文字中間態 markdown（不寫 Marp directive）-->

## 輸出

中間態 markdown（交給 marp-render 轉格式）
