---
name: mermaid-png
description: Use when Mermaid diagrams need PNG images for documents, chat, websites, or fixed-size previews, including PNG-only delivery. For SVG-only use mermaid-svg; for editable PowerPoint or PNG+SVG+PPTX use mermaid-ppt; for Mermaid source design without a requested export format use mermaid-design.
---

# Mermaid PNG

將 Mermaid 流程圖製作為清楚可讀的 PNG。保留 `.mmd` 原始碼供修改；未要求其他格式時，公開成品只交付 PNG 與原始碼。

先讀 [共用設計與驗收](references/export-skills.md)，沿用產品設計風、繁體中文、語意完整與「渲染後開圖」規範。處理換行、節點比例、構圖或宿主差異時讀 [排版參考](references/layout.md)，可從 [產品風格範例](assets/product-flow.mmd) 開始。

## 匯出

需要既有 Node.js、Mermaid CLI `mmdc` 與 Puppeteer／Chrome。不要自動下載、升級套件或瀏覽器；缺少依賴時回報具體項目與安裝指令。

```sh
node <skill-dir>/scripts/export.mjs diagram.mmd --out output/diagram --formats png
```

單圖產出 `output/diagram.png`。同任務多圖可在同一命令傳入多個 `.mmd`，檔名為 `diagram-01-輸入檔名.png` 等。底層可暫存 SVG 作渲染用途，不把暫存 SVG 當成公開交付檔。

開啟所有 PNG，以實際呈現寬度檢查文字、箭頭、完整分支及留白，再修正並重繪。提高像素密度無法補救同一顯示尺寸下過小的文字；優先改構圖或拆圖。交付前說明實際驗證寬度與渲染器；未看圖時明確標示尚未完成視覺驗證。

若要求可編輯 PowerPoint，改用 `mermaid-ppt` 的三格式同步交付；不要將 PNG 改副檔名充作投影片。
