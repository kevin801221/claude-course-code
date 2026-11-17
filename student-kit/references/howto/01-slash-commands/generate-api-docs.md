---
description: 根據原始碼生成完整的 API 文件
---

# API 文件生成器

按以下步驟生成 API 文件：

1. 掃描 `/src/api/` 下的所有檔案
2. 提取函式簽名和 JSDoc 註解
3. 按端點/模組進行組織
4. 生成帶範例的 Markdown
5. 包含請求/響應 Schema
6. 新增錯誤文件

輸出格式：
- 輸出為 `/docs/api.md` 中的 Markdown 檔案
- 為所有端點加入 curl 範例
- 新增 TypeScript 型別
