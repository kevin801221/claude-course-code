# dev-essentials plugin

> 開發必備 3 件套：code review agent、production 防護、自動格式化

## 內含

| 元件 | 類型 | 用途 |
|---|---|---|
| `code-reviewer` | Sub-agent | commit 前自動 review，給 🔴🟡🟢 報告 |
| `prod-guard.sh` | Hook (PreToolUse) | 擋 production DB 寫入 + secrets 讀取 |
| `post-edit-format.sh` | Hook (PostToolUse) | 編輯後自動跑 black/prettier/gofmt/rustfmt |

## settings.json hook 註冊（裝完手動加）

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash|Read",
        "hooks": [{ "type": "command",
                   "command": "${CLAUDE_PLUGIN_ROOT}/dev-essentials/hooks/prod-guard.sh" }] }
    ],
    "PostToolUse": [
      { "matcher": "Edit|Write",
        "hooks": [{ "type": "command",
                   "command": "${CLAUDE_PLUGIN_ROOT}/dev-essentials/hooks/post-edit-format.sh" }] }
    ]
  }
}
```

## 為什麼包成 plugin

開發者通用、不限定專案——做成 plugin 比每個 repo 重抄一份方便。

## 為什麼用 sub-agent 而不是 slash command

Code review 需要獨立 context（不要污染主對話）+ 多步驟思考（讀檔、分析、判斷）→ sub-agent 適合。
