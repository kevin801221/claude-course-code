---
description: 透過子代理取得 Dubai 溫度，再產生 SVG 天氣卡
argument-hint: "[celsius|fahrenheit]"
allowed-tools: AskUserQuestion, Agent, Skill, Read, Write
---

# Weather Orchestrator（學生可攜版）

使用者提供的單位：$ARGUMENTS

1. 若引數為 `celsius` 或 `fahrenheit`，採用該單位；若省略或不明確，先詢問偏好。
2. 透過 Agent 工具委派給 `weather-agent`，在 prompt 傳入單位；要求回傳溫度數值、單位、API URL 與 API 資料時間。
3. 等待代理結果。若沒有數值與可確認的單位，停止並說明失敗，不得沿用範例或捏造即時讀數。
4. 呼叫 `weather-svg-creator` skill，傳入剛取得的數值與單位；主對話負責產出檔案。
5. 回報 `orchestration-workflow/weather.svg` 與 `orchestration-workflow/output.md`，並列出 API URL 與資料時間。

分工契約：主對話負責編排，不自行抓天氣；子代理負責取得資料，不寫 SVG；SVG skill 使用已驗證的資料，不重抓一次。
若 Agent 或 Skill 工具不可用，說明執行環境限制並停止。
