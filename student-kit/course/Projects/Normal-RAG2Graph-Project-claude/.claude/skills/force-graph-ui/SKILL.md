---
name: force-graph-ui
description: Next.js + react-force-graph-2d 雙面板 UI。Use when implementing the frontend graph panel, node highlighting flow, or whenever the user says「前端圖譜」「highlight node」「graph visualization」「force graph」.
---

## 架構
- 左右雙面板：左 450px Chat/Index tab，右滿版 ForceGraph2D
- ForceGraph2D 必須 dynamic import + ssr:false
- 深色 glassmorphism 風格：bg-slate-950, border-slate-800

## 高亮流程
Chat 回覆 → response.highlighted_node_ids →
1. 過濾有座標的節點
2. 算重心 (cx, cy)
3. `fgRef.current.centerAt(cx, cy, 1000)`
4. `fgRef.current.zoomToFit(800, 80, filterFn)`
5. 節點 glow: radial gradient rgba(129,140,248,0.55)
6. Link 兩端都在 highlight set → 也高亮

## 節點 grounding
點節點 → `GET /graph/node/{id}/chunks` → 側欄顯示：
- 節點名 + group badge + val
- aliases 標籤列
- Supporting Chunks 卡片：filename, salience bar, text snippet
- 「Chat about this Concept」按鈕

## 節點繪製
nodeCanvasObject 自定義：
- radius = val * 2
- highlighted: radius+2, glow ring, bold label, white text
- normal: nodeAutoColorBy="group", gray label

## Data Index tab
- Upload 按鈕（gradient indigo）
- Processing jobs 列表（spinner + stage label）
- Indexed Documents（trash icon, confirm before delete）
- 頂部 Reset Graph 按鈕（二次確認）
