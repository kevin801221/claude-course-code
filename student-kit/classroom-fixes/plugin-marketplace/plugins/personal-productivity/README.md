# personal-productivity：Command、Skill、Hook 組合

從精華包根目錄啟動：

```bash
claude --permission-mode manual --plugin-dir ./classroom-fixes/plugin-marketplace/plugins/personal-productivity
```

對話輸入 `/personal-productivity:weekly-haiku`。在有 commit 的獨立練習 Repo 用實際 git log 產生草稿；無 log 時不編造。`/personal-productivity:youtube-notes` 是手動 Skill，需自己準備 yt-dlp、可取得的字幕、網路與模型額度；不會替你安裝工具，未取得字幕不能產生假時間戳。

已加入 `hooks/hooks.json` 讓原來僅列在 components 的番茄鐘真正連到 PostToolUse。載入後每次工具完成都會增加 `${CLAUDE_PROJECT_DIR}/.outputs/plugin-demo/pomodoro-count`，每 50 次嘗試 macOS/Linux 桌面通知；這是工具次數，並非 25 分鐘計時。跨 session 共用而且沒有鎖，不是精準用量統計。

計數由原本 HOME 改到目前專案，不改全域設定；關閉這次 session、以不含 `--plugin-dir` 的命令重開即可停止本機載入。不要把原始與修正版同名 Plugin 同時載入。完整流程見 [工作坊首頁](../../README.md)。

**驗證範圍：**靜態 Plugin validation，以及臨時專案計數 1/50 和通知替身分支；未呼叫模型、YouTube 或真實桌面通知。
