# /weekly-haiku：把 Git 記錄變成工作俳句

講義 **Part 04，投影片 85–86**（PDF 實體頁 84–85）。
來源：[固定 commit 原檔](https://github.com/kevin801221/claude-course-code/blob/475fe057ed234f836ff3eb06f4c5eecad9e36332/Projects/01-weekly-haiku/.claude/commands/weekly-haiku.md)。

## 兩種版本擇一

- `source/commands/weekly-haiku.md`：原始 legacy command，逐字保留。
- `modern-skill/SKILL.md`：學生版 Skill，使用 `Bash(git log *)`，由使用者手動呼叫；改看專案所有作者的近七天紀錄。

不要同時安裝同名 command 與 Skill。這裡都不放在生效的 `.claude/`，不會改你的 Claude 設定。

## 操作

需要 Git、有 commit 的練習 Repo，以及已登入的 Claude Code。以新版 Skill 為例：

1. 在自己的練習專案建立 `.claude/skills/weekly-haiku/`。
2. 將 `modern-skill/SKILL.md` 複製進去。
3. 開啟新的 `claude` 對話，輸入 `/weekly-haiku`。
4. 先手動跑 `git log --since="7 days ago" --pretty=format:"%s"`，核對詩裡提到的工作確實有來源。

要學講義舊 command 的結構，就把原檔放到 `.claude/commands/weekly-haiku.md`。

## 驗收與相容性

- 產生三行中文，每行各 5、7、5 字，附一句英文解釋；沒有紀錄時必須明說。
- 原檔 `--author="$(git config user.email)"` 會只看本機 email 符合的作者；換帳號後可能找不到歷史紀錄，不能因此改寫歷史作者。
- 原檔的 `Bash(git log:*)` 是舊式權限語法，保留作對照；新版示例用空格萬用字元。
- CLI 2.1.319 以 `manual` 作為本課程的權限設定示範；不要把舊文的 `default` 當成目前可用值。此例不設定 permission mode。
- 已檢查來源與 Skill 結構；詩的品質、實際 Claude 載入與對話執行待課堂實測。
