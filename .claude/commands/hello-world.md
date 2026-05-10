---
description: 用指定語言生成一個 Hello World 範例專案（含 README 與執行指令）
argument-hint: <lang: python|go|rust|ts|bash>（預設 python）
allowed-tools: Read, Write, Edit, Bash(mkdir:*), Bash(ls:*), Bash(uv:*)
---

# Hello World Scaffold

請依下列步驟，為使用者建立一個結構完整的 Hello World 範例專案：

## 參數

- 目標語言：`$1`（若為空，預設使用 `python`）
- 合法值：`python`、`go`、`rust`、`ts`、`bash`
- 若使用者輸入不在合法值內，請列出可用語言並停下來等使用者確認。

## 規則

1. 全部產出必須放在 `Projects/hello-world-<lang>/` 下，**不要污染 repo 根目錄**。
2. 一定要附一份 `README.md`，內容包含：
   - 一句話說明這個範例展示什麼
   - 「如何執行」區塊（含完整 shell 指令）
   - 「下一步可以怎麼玩」3 條建議（例如改成 `Hello, <name>!`、加 CLI 參數、加測試）
3. 程式內容不能只是 `print("Hello, World!")` 一行，至少要：
   - 有 `main()` 函式（或對應的入口函式）
   - 接收一個可選的 `name` 參數，預設為 `World`
   - 印出 `Hello, <name>!`
4. **Python 專案規則（這條重要）**：
   - 必須用 `uv` 管理套件，建立 `pyproject.toml`（用 `uv init`）
   - 不要用 `pip`、不要用 `requirements.txt`
   - README 的執行指令要寫 `uv run python main.py` 或 `uv run python main.py --name Kevin`
5. **Rust / Go / TS 專案**：用該語言慣用的 scaffold 工具（`cargo init`、`go mod init`、`pnpm init` 之類）。若工具未安裝，改成手寫最小可執行檔並在 README 註記。
6. **Bash 專案**：寫一個有 shebang、`set -euo pipefail`、可帶 `--name` 參數的 `hello.sh`，並 `chmod +x`。

## 完成後

1. 用 `ls -la Projects/hello-world-<lang>/` 列出產出的檔案。
2. 跑一次範例驗證能正常輸出 `Hello, World!`。
3. 用一句話告訴使用者：「已建立在 `Projects/hello-world-<lang>/`，跑 `<execute-command>` 試試」。
