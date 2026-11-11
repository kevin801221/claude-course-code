---
name: marp-render
description: 把投影片中間態 markdown 轉成 Marp 格式（含 frontmatter、分頁、theme）。當內容已備好要產出可放映投影片時使用。主題無關。
---

# marp-render（空白 skeleton）

> 🟦 skeleton。Claude 依描述生成正式版（WALKTHROUGH 階段 7），或補滿 TODO。
> **鐵則**：只做格式轉換，不改內容語意。

## 觸發時機

slide-content 的中間態 → 可放映的 Marp 投影片。

## 開工前必讀

- `_Context/slide-design-rules.md`（theme / 版型偏好）

## 工作流程

<!-- TODO 階段 7：
1. 接收中間態 markdown
2. 加 Marp frontmatter（marp: true、theme、paginate 等）
3. 用 `---` 正確分頁，speaker notes 放 HTML comment
4. 輸出 → Courses/{課程名}/02-slides/ch{NN}-{name}.md
（Marp 是純本機 CLI，不需 API key）-->

## 輸出

`Courses/{課程名}/02-slides/ch{NN}-{name}.md`
