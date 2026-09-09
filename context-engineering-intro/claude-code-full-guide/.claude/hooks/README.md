# Claude Code 掛鉤 (Hooks) 範例

此目錄包含 Claude Code 的掛鉤範例，展示了如何為您的 AI 編碼工作流增加確定性行為。

## 什麼是掛鉤 (Hooks)？

掛鉤是使用者定義的 Shell 指令，會在 Claude Code 生命週期的特定時間點執行。它們提供了對 Claude 行為的控制，確保某些動作「始終」發生，而不是依賴 AI 選擇去執行它們。

## 此目錄中的檔案

1. **format-after-edit.sh** —— 一個 `PostToolUse` 掛鉤，在編輯檔案後自動對程式碼進行格式化。
2. **example-hook-config.json** —— 示範如何設定各種掛鉤的配置範例。

## 如何使用這些掛鉤

### 選項 1：複製到您的設定檔

將 `example-hook-config.json` 中的掛鉤配置複製到您的 Claude Code 設定中：

**專案特定** (`.claude/settings.json`)：
```bash
# 如果設定檔不存在，請建立它
touch .claude/settings.json

# 從 example-hook-config.json 新增掛鉤配置
```

**使用者全域** (`~/.claude/settings.json`)：
```bash
# 將掛鉤應用於所有 Claude Code 對話
cp example-hook-config.json ~/.claude/settings.json
```

### 選項 2：使用單個掛鉤

1. 將掛鉤腳本複製到您的專案：
```bash
cp format-after-edit.sh /您的/專案/.claude/hooks/
chmod +x /您的/專案/.claude/hooks/format-after-edit.sh
```

2. 新增至您的 `settings.json`：
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/format-after-edit.sh"
          }
        ]
      }
    ]
  }
}
```

## 可用的掛鉤事件 (Hook Events)

- **PreToolUse**：在工具執行前 (可以阻擋工具執行)。
- **PostToolUse**：在工具成功完成後。
- **UserPromptSubmit**：當使用者提交提示詞時。
- **SubagentStop**：當子代理人完成任務時。
- **Stop**：當主代理人完成回應時。
- **Notification**：在系統通知期間。
- **PreCompact**：在上下文壓縮 (Compaction) 之前。
- **SessionStart**：在對話初始化時。

## 建立您自己的掛鉤

1. 撰寫一個具備以下功能的 Shell 腳本：
   - 從 `stdin` 讀取 JSON 輸入。
   - 處理輸入內容。
   - 回傳 JSON 輸出 (成功時回傳空的 `{}`)。
   - 可以回傳 `{"action": "block", "message": "原因"}` 來阻擋操作。

2. 使其可執行：
```bash
chmod +x 您的-掛鉤.sh
```

3. 新增至 `settings.json`，並配合適當的 `matcher` 和事件。

## 安全性考量

- 掛鉤會執行任意的 Shell 指令。
- 務必驗證並清理 (Sanitize) 輸入內容。
- 使用完整路徑以避免 `PATH` 操控。
- 處理檔案操作時請務必小心。
- 在部署前徹底測試掛鉤。

## 除錯掛鉤

執行具備 `--debug` 旗標的 Claude Code 以檢視掛鉤執行情況：
```bash
claude --debug
```

這將會顯示：
- 哪些掛鉤被觸發。
- 每個掛鉤的輸入/輸出。
- 任何錯誤或問題。

## 與子代理人整合

範例配置包含一個與 `validation-gates` 子代理人整合的掛鉤，展示了掛鉤與子代理人如何協同工作，以實現更穩健的開發工作流。
