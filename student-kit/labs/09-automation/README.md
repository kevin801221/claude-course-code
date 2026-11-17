# Lab 09：Headless 產出可讀的 JSON

講義 Part 16。先讀 [summarize.sh](../../scripts/summarize.sh)，確認它給模型的工具只有 Read、Glob、Grep，且沒有使用權限略過選項。

此練習會呼叫你登入的 Claude 帳號，使用該帳號的額度或計費。不是 `npm test` 的一部分。

## 操作

```bash
bash scripts/summarize.sh
```

回應儲存在 `.outputs/summary.json`。CLI 的 JSON 是外層回應封裝；不要假設 `result` 一定是結構化業務資料。檢查 `is_error`、result 與實際提供的成本/用量欄位。

腳本用 `--max-budget-usd 0.25` 設定此次呼叫的預算選項；計費欄位與生效範圍以自己的 CLI、供應商與帳號為準，不把它當成整個帳號的硬上限。失敗時暫存檔會移除，避免把半份結果當成功交付。

## 驗收

摘要說得出現有三個指令與單程序限制，不聲稱跑過測試、不改來源。再想想要放 CI 時應如何處理認證、失敗退出碼、過期資料與重試，先不用真的排程。

此腳本也限制只讀專案設定與空 MCP 清單；它仍不等於作業系統沙箱。若自己的版本不支援某個旗標，先對照 `claude --help`，不要直接刪掉限制來湊到能跑。
