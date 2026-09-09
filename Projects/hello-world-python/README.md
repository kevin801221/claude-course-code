# hello-world-python

一個用 `uv` 管理的最小 Python 範例，示範 `main()` 入口、預設參數與 CLI 參數解析（`--name`）。

## 如何執行

```bash
cd Projects/hello-world-python

# 預設輸出 Hello, World!
uv run python main.py

# 帶名字
uv run python main.py --name Kevin
```

## 下一步可以怎麼玩

1. 改成讀環境變數 `USER`，沒帶 `--name` 時自動問候目前登入者。
2. 加一個 `--upper` flag，讓輸出變大寫（`HELLO, KEVIN!`）。
3. 用 `pytest` 為 `greet()` 寫測試（`uv add --dev pytest` 後 `uv run pytest`）。
