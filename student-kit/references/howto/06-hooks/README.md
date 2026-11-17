<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Hooks 參考

Hooks 是在 Claude Code 事件發生時自動執行的 shell 命令，用來做格式化、校驗、通知、審計等自動化工作。

## 概覽

Hooks 是事件驅動的自動化機制。它們會在 Claude Code 發生某些動作時自動執行，不需要你手動觸發。

常見用途：

- 寫檔案前自動格式化
- 提交前執行測試
- 掃描安全問題
- 記錄 bash 命令
- 校驗使用者提示詞
- 傳送團隊通知

## Hook 型別

Claude Code 支援 33 個 hook 事件，按用途分為以下 4 組。事件的 handler 型別共 5 種：`command`、`http`、`mcp_tool`、`prompt`、`agent`。

- **Tool Hooks**：`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PostToolBatch`、`PermissionRequest`、`PermissionDenied`
- **Session Hooks**：`SessionStart`、`Setup`、`SessionEnd`、`Stop`、`StopFailure`、`SubagentStart`、`SubagentStop`
- **Task Hooks**：`UserPromptSubmit`、`UserPromptExpansion`、`MessageDisplay`、`TaskCompleted`、`TaskCreated`、`TeammateIdle`（`TaskCompleted` 和 `TaskCreated` 僅在啟用 todo 工具時觸發 —— 預設僅在 Claude 3.x 模型、Opus 4 至 4.7、Sonnet 4 至 4.6 及 Haiku 4.5 上可用；`CLAUDE_CODE_ENABLE_TODO_TOOLS=1` 可恢復）
- **Lifecycle Hooks**：`ConfigChange`、`CwdChanged`、`DirectoryAdded`、`FileChanged`、`PreCompact`、`PostCompact`、`PreModelSwitch`、`PostModelSwitch`、`WorktreeCreate`、`WorktreeRemove`、`Notification`、`InstructionsLoaded`、`Elicitation`、`ElicitationResult`

## 安裝

```bash
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

然後在 `~/.claude/settings.json` 裡設定：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/format-code.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/security-scan.sh"
          }
        ]
      }
    ]
  }
}
```

## 使用方法

Hooks 會在匹配到事件時自動執行。你可以把它理解成 Claude Code 的事件回撥。

## 常見範例

- `format-code.sh` - 寫入前自動格式化
- `pre-commit.sh` - 提交前跑測試
- `security-scan.sh` - 做安全掃描
- `log-bash.sh` - 記錄 bash 命令
- `validate-prompt.sh` - 校驗輸入
- `notify-team.sh` - 發通知

## 最佳實踐

- 把 hooks 保持短小明確
- 只做單一職責
- 先在本地測試
- 不要在 hook 裡放複雜業務邏輯
- 對副作用保持謹慎

## 故障排查

- 檢查檔案路徑和許可權
- 確認指令碼可執行
- 檢查 settings.json 語法
- 檢視 Claude Code 版本相容性

## 相關概念

- [Checkpoints and Rewind](../08-checkpoints/README.md)
- [Slash Commands](../01-slash-commands/README.md)
- [Skills](../03-skills/README.md)
- [Subagents](../04-subagents/README.md)
- [Plugins](../07-plugins/README.md)
- [Advanced Features](../09-advanced-features/README.md)

## 更多資源

- [Memory Guide](../02-memory/README.md)
- [Official Hooks Documentation](https://code.claude.com/docs/en/hooks)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)

---

**最後更新**: 2026 年 9 月 19 日
**Claude Code 版本**: 2.1.278
**來源**:
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/tools-reference#task-tool-availability
