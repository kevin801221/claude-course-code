---
description: 用繁體中文逐段解釋指定檔案在做什麼，並把解釋落檔保存
argument-hint: <file-path>
allowed-tools: Read, Write, Bash(mkdir:*), Bash(wc:*), Glob
---

# Explain This（檔案逐段解析）

目標：把一份程式碼／設定檔／markdown 變成「給隊友看的繁體中文導讀」。

## 參數

- 目標檔案路徑：`$1`
- 若 `$1` 為空，請用 Glob 列出 repo 根目錄前 10 個常見檔案，問使用者要看哪個。
- 若路徑不存在，立刻停下來告知，不要亂猜。

## 規則

1. 先 `wc -l <file>` 看檔案行數，超過 800 行只解析前 300 行 + 後 100 行，並在輸出開頭註明「已截斷」。
2. 解析時請按「邏輯區塊」分段（不是「每 10 行」這種機械切法），常見區塊：
   - imports / dependencies
   - 設定常數 / 型別定義
   - 主要 class / function
   - 入口（main、CLI handler、router）
   - 測試 / 範例
3. 每個區塊輸出格式：

   ```markdown
   ### L<起>–L<迄>：<這段在幹嘛的一句話>

   <2–4 句白話解釋>

   **為什麼這樣寫**：<設計動機，不可省>
   **可以怎麼改**：<一個具體改進方向，例如效能、可讀性、測試>
   ```

4. 最後加一個「## 三個你應該追問的問題」區塊，列出讀者看完後應該主動釐清的事（例如「這個 retry 機制有 backoff 嗎？」）。

## 落檔

寫到 `Projects/explanations/<filename-with-dashes>.md`：
- 路徑 `src/foo/bar.ts` → `Projects/explanations/src-foo-bar.ts.md`
- 開頭加 frontmatter：

  ```yaml
  ---
  source: <原始路徑>
  generated_at: <YYYY-MM-DD HH:MM>
  ---
  ```

完成後在對話中告知：解析輸出檔案路徑 + 全檔最重要的「一句話總結」。
