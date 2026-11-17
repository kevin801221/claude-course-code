#!/usr/bin/env bash
# SessionEnd hook：詢問這次處理了哪些模組，然後把工作階段記錄附加
# 到 ~/.claude-code-tutorial-progress.json，用來持續追蹤學習進度。
#
# 只在 Claude Code 工作階段結束時觸發一次 — 不是每次回應後都觸發。
# 用 /dev/tty 做互動輸入，因為 stdin 已經被 hook 的 JSON payload 佔用。
#
# 安裝方式：在 .claude/settings.json 的「SessionEnd」事件底下加入（見下方）。

PROGRESS_FILE="$HOME/.claude-code-tutorial-progress.json"

# 防護：只在此 repo 內執行
if [[ "$CLAUDE_PROJECT_DIR" != *"claude-code-tutorial"* ]] && [[ "$PWD" != *"claude-code-tutorial"* ]]; then
  exit 0
fi

# 若進度檔不存在就建立它
if [ ! -f "$PROGRESS_FILE" ]; then
  echo '{"sessions":[]}' > "$PROGRESS_FILE"
fi

DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M")

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Claude Code — 學習工作階段結束"
echo " $DATE $TIME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo " 你這次處理了哪些模組？（例如 06,07，直接按 Enter 可跳過）"
echo " 01=斜線指令  02=記憶  03=技能  04=子代理  05=MCP"
echo " 06=Hooks  07=外掛 08=檢查點 09=進階功能 10=CLI"
echo ""
printf " > "
read -r INPUT </dev/tty

if [ -z "$INPUT" ] || [ "$INPUT" = "skip" ]; then
  echo " 已跳過 — 未記錄任何工作階段。"
  echo ""
  exit 0
fi

# 把數字代碼對應到模組名稱（用 for 迴圈避免 pipeline+while，因為 bash 3.2 無法解析）
IFS=',' read -ra PARTS <<< "$INPUT"
MODULES_JSON=""
for m in "${PARTS[@]}"; do
  m="${m// /}"  # 去除空白
  case "$m" in
    01) label='"01-slash-commands"' ;;
    02) label='"02-memory"' ;;
    03) label='"03-skills"' ;;
    04) label='"04-subagents"' ;;
    05) label='"05-mcp"' ;;
    06) label='"06-hooks"' ;;
    07) label='"07-plugins"' ;;
    08) label='"08-checkpoints"' ;;
    09) label='"09-advanced-features"' ;;
    10) label='"10-cli"' ;;
    *)  label="\"$m\"" ;;
  esac
  MODULES_JSON="${MODULES_JSON:+$MODULES_JSON,}$label"
done

printf " 備註？（選填，按 Enter 可跳過）："
read -r NOTES </dev/tty

# 把 NOTES 當成獨立參數傳入，讓 Python 處理 JSON 跳脫 —
# 避免 notes 內含引號或反斜線時破壞 JSON 格式。
python3 - "$PROGRESS_FILE" "$DATE" "$TIME" "$MODULES_JSON" "$NOTES" <<'PYEOF'
import sys, json

path, date, time_str, modules_raw, notes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

new_session = {
    "date": date,
    "time": time_str,
    "modules": json.loads(f"[{modules_raw}]") if modules_raw else [],
    "notes": notes,
}

with open(path, 'r') as f:
    data = json.load(f)

data.setdefault('sessions', []).append(new_session)

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
PYEOF

echo ""
echo " 已儲存到 $PROGRESS_FILE"
[ -n "$NOTES" ] && echo " 備註：$NOTES"
echo ""

exit 0
