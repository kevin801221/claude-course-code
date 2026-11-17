# pomodoro：每 50 次工具完成後提醒休息

講義 **Part 12，投影片 324–326**（PDF 實體頁 323–325）。它按 tool call 計數，並非真正計時 25 分鐘的番茄鐘。
來源：[原 hook](https://github.com/kevin801221/claude-course-code/blob/475fe057ed234f836ff3eb06f4c5eecad9e36332/Projects/04-pomodoro/.claude/hooks/pomodoro.sh)、[原設定](https://github.com/kevin801221/claude-course-code/blob/475fe057ed234f836ff3eb06f4c5eecad9e36332/Projects/04-pomodoro/try/.claude/settings.json)。

## 包含什麼

- `source/hooks/pomodoro.sh`：原始 hook，逐字保留。
- `source/settings.json`：來源 `try/.claude/settings.json` 的原設定；原專案根目錄並沒有 README 所說的 `.claude/settings.json`，此處從實際存在的檔案補齊。
- `settings.project.example.json`：手動選用的專案設定，把相對執行路徑改成引號包住 `$CLAUDE_PROJECT_DIR`，由 bash 執行。
- `smoke-test.py`：用臨時目錄的計數檔與通知替身測試原腳本，完全不寫入你的 `~/.claude`，也不發真通知。

## 先跑離線驗證

Bash + Python 3，從精華 Repo 根目錄：

```bash
python3 examples/lecture-mini-projects/pomodoro/smoke-test.py
```

預期 `PASS: count=1, count=50, notification branch`。這只證明計數與通知命令分支，不證明桌面會顯示通知。

## 在自己的練習專案啟用

1. 將 `source/hooks/pomodoro.sh` 複製到自己專案 `.claude/hooks/pomodoro.sh`。
2. 確認本機 `~/.claude/` 已存在；原腳本不會建立這個資料夾。
3. 把 `settings.project.example.json` 的 `hooks.PostToolUse` 區段合併到自己的 `.claude/settings.local.json`，不要整份覆蓋現有設定。
4. 重開 Claude，執行數次工具操作，再查看 `~/.claude/.pomodoro-count` 是否增加。
5. 到 50 的倍數時，通知依序嘗試 `terminal-notifier`、macOS `osascript`、Linux `notify-send`。
6. 練完刪除自己合併的 hook 區段，即可停止後續觸發。

## 範圍、依賴與限制

- 原腳本即使從專案層啟用，計數仍存在全域 `~/.claude/.pomodoro-count`，跨專案/多個 session 共用。沒有檔案鎖，平行執行可能丟失次數；不要當精準用量統計。
- 原腳本沒有讀取 stdin JSON，不需 `jq`；來源 README 的 jq 建議是其他變化版的依賴。
- 沒有上述通知工具時只會計數；通知權限未開也可能看不到畫面。
- Windows 原生 PowerShell 不適用此 Bash 腳本；WSL 內通知需自行整合。
- 原設定使用相對路徑，執行目錄改變可能失效；學生設定用 `$CLAUDE_PROJECT_DIR` 改善這點。
- CLI 2.1.319 課堂以 `manual` 權限模式示範；這份 hook 設定不改 permission mode，也不代替危險指令防護。
- 已驗證 Bash 語法、JSON 與隔離 smoke；未啟用真實 Claude hook、未發桌面通知。
