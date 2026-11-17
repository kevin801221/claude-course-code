# 有腳本的 Skill：Python 文件擷取器

對應講義 Part 10 Skills：提示詞負責工作流程，腳本負責可重現的靜態處理。
`generate-docs.py` 是 `claude-howto-zh-TW/03-skills/doc-generator/` 的原始碼；`SKILL.md` 為學生版改寫，縮小原文件宣稱範圍。

## 不裝 Claude 也能先練

Python 3.9+，只有標準函式庫，不需要 pip install。從本 Repo 根目錄：

```bash
python3 resources/templates/skills/doc-generator/generate-docs.py resources/templates/skills/doc-generator/sample-api.py
```

預期會看到 `get_lesson`、`post_enrollment`，各自有中文 docstring、參數與 `dict` 回傳型別；不會看到 `get_async_lesson`。可與 [expected-api.md](expected-api.md) 比對。

## 在自己的練習專案啟用

將整個 `doc-generator/` 資料夾複製到練習專案 `.claude/skills/`，重開 Claude，輸入 `/doc-generator`，指定 Python 檔案及輸出位置。請先用沒有同名 Skill 的練習專案，避免覆蓋自己的設定。

## 學生要理解的界線

- 腳本遍歷同步 `def`，名稱需 `get_` 或 `post_` 開頭；不辨識 Flask/FastAPI decorator。
- 只取位置參數的名稱，不取參數型別、預設值或 keyword-only 引數；無回傳型別時顯示 `Any`。
- 沒有 docstring 時輸出 `None`；這是待人工補充的草稿。
- 原碼沒有 argparse，缺檔案參數會拋錯；課堂先照上述完整指令執行。
- Python 原始碼必須可被解析。輸出不是 OpenAPI，也不是已部署的 API 規格。

## 驗收與延伸

1. 修改 sample docstring，再跑一次，確認文件跟著改。
2. 加入一個 `delete_lesson`：觀察它未被擷取，解釋命名規則帶來的限制。
3. 延伸題：先為 async 函式寫出預期輸出，再實作 `visit_AsyncFunctionDef`；保留既有同步函式行為。
