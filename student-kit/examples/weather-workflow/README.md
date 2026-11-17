# Command → Agent → Skill：一張真實天氣卡

對應講義 **Part 04 自訂 Slash Commands、Part 10 Skills、Part 11 Sub-agents**。先完成基本 CLI 與權限練習，再做這個約 20 分鐘的整合實驗。

這是 `claude-code-best-practice` 天氣範例的可攜性修正版；保留 Dubai 座標與 SVG 模板，讓你專注比較三個層次的分工。

## 執行

需要已安裝且可登入的 Claude Code，以及連到 `api.open-meteo.com` 的網路。這個端點不需在範例中填入 API key；Claude 的使用額度依你的帳號計算。

從精華包根目錄執行：

```bash
cd examples/weather-workflow
claude
```

在 Claude 對話中輸入：

```text
/weather-orchestrator celsius
```

也可以用 `fahrenheit`，或不帶引數，觀察主對話先詢問單位。首次 WebFetch 或寫檔可能需要依環境的權限規則核准。

如果目前 CLI 未探索到子目錄的 commands/agents/skills，把**整個** `weather-workflow` 資料夾複製到精華包外，從該資料夾啟動一個新 session。不要只複製 README；`.claude/` 是隱藏資料夾，也必須一起複製。

## 觀察四個檔案的合作

```text
/weather-orchestrator
  → weather-agent（獨立脈絡）
    → weather-fetcher（skills: 預載 API 操作指示）
  → weather-svg-creator（主對話呼叫，寫出 SVG 與摘要）
```

| 位置 | 責任 | 應該看到的行為 |
|---|---|---|
| [.claude/commands/weather-orchestrator.md](.claude/commands/weather-orchestrator.md) | 單位、委派、檢查結果 | 有代理結果才進入產圖 |
| [.claude/agents/weather-agent.md](.claude/agents/weather-agent.md) | 使用 Read/WebFetch 取得讀數 | 不寫檔、不產圖 |
| [.claude/skills/weather-fetcher/SKILL.md](.claude/skills/weather-fetcher/SKILL.md) | API URL 與欄位知識 | 在代理開始時預載 |
| [.claude/skills/weather-svg-creator/SKILL.md](.claude/skills/weather-svg-creator/SKILL.md) | 使用 reference.md 模板產圖 | 不再抓一次 API |

## 驗收

完成後應新增：

- `orchestration-workflow/weather.svg`：300 × 160 的獨立 SVG，可用瀏覽器開啟。
- `orchestration-workflow/output.md`：數值、單位與地點一致，圖片連結可開啟。
- 最終對話回報本次來源 API URL 與 API 資料時間；不要把執行時間當成資料時間。

切換到 Fahrenheit 再跑一次，確認 URL 參數、SVG 與摘要三處一起改變。接著模擬網路無法使用：應回報失敗並停止，不得把 `examples.md` 裡的 `26.2°C` 當成本次真實天氣。

## 常見卡點

| 現象 | 處理 |
|---|---|
| `/weather-orchestrator` 不見了 | 確認啟動目錄、隱藏 `.claude/` 是否存在，並開新 session |
| 找不到 `weather-agent` | 確認 `.claude/agents/weather-agent.md`；用 `/agents` 檢查可見代理 |
| WebFetch 被拒絕或 API 無回應 | 先處理權限、網路或 API 回應；不要改成假資料 |
| 產圖前 Read 報檔案不存在 | 新版指示會直接建立新檔；只有覆寫既有檔才先 Read |
| 沒有 Agent/Skill 工具 | 此範例需要 Claude Code；一般聊天視窗不等同執行環境 |

## 與上游的差異

原始來源固定於 commit `17b25b2948ecea4aa5e7e60c4e015876fc7063c7`，來源與 MIT 授權由精華包根目錄統一記錄。

1. `weather-agent` 改用 `tools: Read, WebFetch`，直接遵循預載 `skills:`。上游範例同時強迫代理再呼叫 Skill 工具，容易混淆「預載」與「主對話呼叫」兩種機制。
2. 移除依賴上游音效腳本的 hooks、跨 session memory 與固定模型選擇，避免缺檔與額外環境設定。
3. Command 支援明確的單位引數，並要求回報 API 資料時間；失敗時停止。
4. SVG skill 僅在目標已存在時先 Read；reference.md、examples.md 與 weather-fetcher 原樣保留。

**驗證範圍：**已核對來源、檔案依賴、相對連結與 frontmatter 結構。此包製作時未登入 Claude 執行真實 Agent/WebFetch 流程，完整端到端行為須按上面步驟於課堂驗收。

## 加分練習

讓呼叫者選 Taipei 或 Dubai，再把城市選擇傳給代理。先寫清楚座標、輸出地點與失敗條件；不要只改 SVG 上的城市文字。
