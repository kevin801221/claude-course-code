# clip-translate

macOS 的剪貼簿背景翻譯：選取英文按 ⌘C，幾秒後剪貼簿裡的內容就換成繁體中文譯文，直接 ⌘V 貼上。

翻譯由 Claude Code 的非互動模式 `claude -p` 負責。腳本做的事，等於把下面這行放進迴圈，讓它自己盯著剪貼簿：

```bash
pbpaste | claude -p "翻譯成繁中" | pbcopy
```

## 需要

- macOS：腳本用到 `zsh`、`pbpaste`、`pbcopy`、`osascript`。
- 已安裝並登入 Claude Code：在終端機執行 `claude -p "hi"` 會回話就可以。

## 使用

```bash
git clone https://github.com/kevin801221/clip-translate.git
cd clip-translate
nohup ./clip-translate.sh >/dev/null 2>&1 &   # 開始，在背景執行
pkill -f clip-translate.sh                    # 停止
```

執行後：選取英文 → ⌘C → 右上角出現「翻譯中…」→ 出現「翻好了，直接 ⌘V」→ 貼上就是中文。實測一句話大約 9 秒。

沒看到通知的話，到「系統設定 → 通知」允許「工序指令編寫程式」（Script Editor）傳送通知。沒有通知也不影響翻譯。

## 運作方式

1. 每秒用 `pbpaste` 讀一次剪貼簿，內容沒變就跳過。
2. 內容至少要有兩個用空格隔開的英文單字才翻。沒有空格的單一字串，例如密碼或 token，不會送出去。
3. 用 `claude -p --model haiku` 翻成繁體中文，再用 `pbcopy` 寫回剪貼簿。
4. 記住剛寫回去的譯文，下一秒就不會把譯文再翻一次。

## 注意

- 執行期間，你複製的英文句子都會送給 Claude。複製機密內容前，先停掉腳本。
- 每翻一次都算一次 Claude Code 用量。
- 每翻一次，Claude Code 都會多一筆對話紀錄，記在啟動腳本的那個資料夾名下，在那裡執行 `claude --resume` 看得到。
- 預設用 Haiku，速度最快。想要譯文品質更好，把腳本裡的 `--model haiku` 拿掉，改用你的預設模型，但每次會比較慢。
- 重開機後不會自動啟動，要再執行一次。
