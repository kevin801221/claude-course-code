---
name: doc-generator
description: 從 Python 原始碼的 get_、post_ 同步函式產生 Markdown 文件草稿。適用於練習以腳本輔助 Skills、整理函式說明；不會自動辨識 HTTP 路由。
---

# Python 函式文件草稿

1. 確認使用者指定的 Python 原始碼路徑，以及文件輸出位置。
2. 執行本 Skill 目錄的 `generate-docs.py`，將輸出寫入使用者指定的新文件。
3. 腳本只做 AST 靜態分析，不匯入或執行目標程式。
4. 逐項核對產生內容：函式名稱、docstring、位置參數名稱、回傳型別註記。
5. 明確註明未被腳本擷取的 async 函式、其他命名函式與 keyword-only 引數。
6. 未經閱讀實際路由，不要把函式名稱猜成 HTTP endpoint，也不要宣稱已生成 OpenAPI。

安裝本資料夾到 `.claude/skills/doc-generator/` 後，從專案根目錄執行：

```bash
python3 .claude/skills/doc-generator/generate-docs.py path/to/module.py
```

Python 需 3.9+（`ast.unparse`）。腳本只依賴標準函式庫。
先參閱同目錄 README 與 sample-api.py，使用小範圍檔案測試。
