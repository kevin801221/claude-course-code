---
description: 從原始碼產生完整的 API 文件
---

# API 文件產生器

透過以下步驟產生 API 文件：

1. 掃描 `/src/api/` 下的所有檔案
2. 擷取函式簽章與 JSDoc 註解
3. 依端點／模組分類整理
4. 建立含範例的 markdown 文件
5. 納入請求／回應結構
6. 加入錯誤說明文件

輸出格式：
- markdown 檔案輸出至 `/docs/api.md`
- 為所有端點加上 curl 範例
- 加入 TypeScript 型別

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/commands
**相容模型**：Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
