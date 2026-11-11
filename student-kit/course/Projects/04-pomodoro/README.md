# 小專案 4：pomodoro hook — 番茄鐘提醒喝水

> Claude 跑大任務時，你開始發呆滑手機 → 1 小時過去沒喝一口水。
> 這個 hook 每 50 個 tool call 自動彈桌面通知。

## 為什麼做

- ❌ 寫 code 進入心流忘了喝水 / 起來活動
- ❌ 番茄鐘 app 你也忘了開
- ✅ Claude 在跑時順便當你的健康提醒

## 用到的 Claude Code feature

- PostToolUse hook（每次 tool 跑完觸發）
- 計數器存在 `~/.claude/.pomodoro-count`
- macOS `osascript` / Linux `notify-send`

## 安裝

### 方式 A：個人層（推薦，所有 repo 都生效）

```bash
# 1. 複製 hook script
mkdir -p ~/.claude/hooks
cp .claude/hooks/pomodoro.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/pomodoro.sh

# 2. 加進 ~/.claude/settings.json 的 hooks 區塊
# （如果你已經有 settings.json，手動 merge 進去；沒有就 cp）
cp .claude/settings.json ~/.claude/settings.json
```

如果你 `~/.claude/settings.json` 已有內容，**不要 cp 覆蓋**，手動加：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/pomodoro.sh" }
        ]
      }
    ]
  }
}
```

### 方式 B：專案層

```bash
cd ~/your-repo
cp -r .claude/hooks ~/.claude/  # 或 .claude/hooks/ 進這個 repo
cp .claude/settings.json .claude/   # merge 進現有 settings
```

## 使用

啥都不用做。背景自動數，Claude 用一陣子自然彈通知。

想看當前計數：
```bash
cat ~/.claude/.pomodoro-count
```

想重設：
```bash
rm ~/.claude/.pomodoro-count
```

## 進階變化

### 變化 1：依工具 weight 計分（寫 code 算 3 分、read 算 1 分）

```bash
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
case "$TOOL" in
  Edit|Write) WEIGHT=3 ;;
  Bash)       WEIGHT=2 ;;
  *)          WEIGHT=1 ;;
esac
N=$((N + WEIGHT))
```

### 變化 2：整點提醒做伸展

```bash
HOUR=$(date +%H)
MINUTE=$(date +%M)
if [ "$MINUTE" -lt "5" ] && [ "$HOUR" -ge 9 ] && [ "$HOUR" -le 18 ]; then
  osascript -e 'display notification "現在是整點，做 5 分鐘伸展"'
fi
```

### 變化 3：搭配 Spotify 自動播 lo-fi

```bash
if [ $((N % 50)) -eq 0 ]; then
  # 用 spotify CLI 播 5 分鐘 lo-fi
  spotify play "lofi hip hop"
  (sleep 300 && spotify pause) &
fi
```

### 變化 4：週報統計

```bash
# 在 SessionEnd hook 跑
TODAY=$(date +%Y-%m-%d)
echo "$TODAY $(cat ~/.claude/.pomodoro-count)" >> ~/.claude/logs/pomodoro.log
```

## 故障排除

| 症狀 | 解法 |
|---|---|
| 沒彈通知 | macOS：系統設定 → 通知 → 終端機 → 允許通知 |
| Linux 沒 notify-send | `sudo apt install libnotify-bin` |
| Permission denied | `chmod +x ~/.claude/hooks/pomodoro.sh` |
| jq not found | `brew install jq` 或 `apt install jq` |
