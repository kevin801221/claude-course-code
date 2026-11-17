# 延伸 A．在 Mac 複製一段英文，直接貼出繁中

試著把公開的更新公告放進中文筆記。啟動後腳本每秒檢查剪貼簿內容是否變動，並尋找以空格相連的英文字串；符合條件時把內容送給 Claude Code，將回傳的台灣繁中譯文寫回剪貼簿。

## 1．在前景啟動

實際翻譯需要 macOS 的 `zsh`、`pbpaste`、`pbcopy`、`osascript`，以及已登入且可連網的 Claude Code。從學生 ZIP 根目錄執行：

```sh
cd realtek/cases/clip-translate
zsh ./clip-translate.sh
```

保持這個終端機開著，先複製 `Retry`，再複製下面這一句到剪貼簿：

```text
Please restart the application after the update.
```

單獨的 `Retry` 會被略過。複製整句後等到「翻好了，直接 ⌘V」，再貼進空白筆記。課堂實測的一次譯文為「更新後請重新啟動應用程式。」用詞可有不同，驗收時確認它傳達「更新後再重新啟動」即可。原始腳本會記住剛寫回的文字，下一次輪詢時跳過同一份內容。

回到原終端機按 **Ctrl+C** 停止。監聽期間，符合條件的剪貼簿內容都可能送到 Claude 並計入用量。請用公開文字，等譯文貼完再複製下一筆。需要常駐時，可參考[講師原始說明](README.md)的背景啟動與停止方式。

## 2．離線測試監聽規則

在上述實驗資料夾，使用 Python 3 與 zsh 執行：

```sh
python3 check_clip.py
```

測試用臨時檔和固定譯文代替系統剪貼簿、通知和模型，執行[同一支腳本](clip-translate.sh)。預期看到 `PASS: Retry skipped, one request, clipboard updated, no self-translation.`。這項檢查驗證觸發條件、寫回和避免重複翻譯，完全在本機完成。

**教材來源**　原始腳本和 README 取自講師 [kevin801221/clip-translate](https://github.com/kevin801221/clip-translate/tree/bb05f1bdda1c0eb49dfc4a1c3001c83023d3a7bf)，由講師授權收錄於本次學生包。該來源提交未附獨立 LICENSE。學生包另提供這份指南與隔離測試。
