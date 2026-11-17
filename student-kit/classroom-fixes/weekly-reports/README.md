# 完整週報 Skill：課堂修正版

對應講義 Part 10 Skills，保留 `claude-course-code/Projects/07-weekly-reports-skill` 的完整三層結構：Skill、三類 references、正反 examples、收集/分類/套版 scripts。來源快照為 `475fe057ed234f836ff3eb06f4c5eecad9e36332`；原版由完整課堂資料區保留，本目錄是可獨立帶走的修正版。

## 修正了什麼

原始 `fetch_commits.sh` 把 `git log` 的 subject/body 直接拼成 JSON。遇到雙引號、反斜線或多行 body，程式可能 exit 0 卻產出無法解析的 JSON；預設反覆開啟 `/dev/stdout` 在部分管線環境還會失敗。

此版保留原參數名稱與輸出欄位，讓 Bash 入口呼叫同目錄 `fetch_commits.py`：

- 使用 Git 的 NUL 分隔欄位，不以換行切 commit，保留 body 原有換行。
- 使用 Python `json.dumps`，正確處理引號、反斜線與繁體中文。
- 預設 stdout，以及 `--output -`、`--output /dev/stdout`，都直接寫標準輸出，不重新開啟管線裝置。
- 所有 Git/gh 資料成功取得並解析後才寫 `--output FILE`，上游失敗不覆寫舊檔。
- Skill 操作改成先儲存 commits.json，再分類與套版，避免原指引讀取未建立的 `/tmp/commits.json`。

Git `%s` 依 Git 定義把首段多行 subject 合成一行；`body` 使用 `%b` 並保留換行。這與原版欄位契約一致。

## 所有相依

- Bash、Git、Python 3.10+；Python 腳本只用標準函式庫，不需 pip install。
- 要收集歷史，需要目前目錄是已有 commits 的 Git Repo，以及 `--author` 或該 Repo 的 `git config user.email`。
- 只有 `--include-prs` / `--include-issues` 需要 gh CLI、相應帳號與網路。沒有 gh 時會在 stderr 提示並略過該欄，commits 仍正常輸出；gh 指令失敗時整體回傳非零。
- 要讓 AI 撰寫週報，另需可登入的 Claude Code 與帳號額度；離線腳本不呼叫模型。
- `fetch_commits.sh` 需要同目錄的 `fetch_commits.py`，請複製整個 Skill，不要只拿一個 .sh。

## 先跑離線回歸驗證

從本精華包根目錄執行：

```bash
python3 -m unittest discover -s classroom-fixes/weekly-reports/tests -p 'test_*.py' -v
```

9 個測試全部使用新建的臨時 Git Repo，驗證引號、反斜線、繁中、subject/body 換行、stdout、檔案、明確 `/dev/stdout`、無符合作者、缺參數，以及原分類/套版管線。PR/issues 用臨時 gh 替身回傳 JSON，不連外、不使用真實憑證。測試不修改你的 Git Repo 或全域設定。

## 複製到獨立專案

1. 在你自己的練習 Git Repo 中確認已有 commits；先檢查是否已有同名 `drafting-weekly-reports` Skill。
2. 建立目標 `.claude/skills/`，將本目錄的整個 `.claude/skills/drafting-weekly-reports/` 複製進去，確認包含新增的 `fetch_commits.py`。
3. 新開 Claude session 時，從該獨立 Repo 啟動；避免在完整教材的父 Repo 裡直接做實作。
4. `.outputs/weekly/` 是本次工作資料，建議在你自己的 `.gitignore` 排除；不要覆蓋既有忽略設定。

## 不使用模型也能看完整管線

以下命令從已安裝 Skill 的目標 Git Repo 根目錄執行：

```bash
mkdir -p .outputs/weekly
bash .claude/skills/drafting-weekly-reports/scripts/fetch_commits.sh \
  --since "7 days ago" --output .outputs/weekly/commits.json
python3 .claude/skills/drafting-weekly-reports/scripts/classify_commits.py \
  --input .outputs/weekly/commits.json > .outputs/weekly/classified.json
python3 .claude/skills/drafting-weekly-reports/scripts/format_report.py \
  < .outputs/weekly/classified.json > .outputs/weekly/draft.md
```

若只是要接 pipe，可省略 `--output`；stdout 只會是 JSON。`--output` 的父資料夾需先存在。

保留原版的查詢範圍：`--since` 只套用 commits；PR/issues 各取至多 20 筆所有狀態資料，不會自動依週期篩選。這不是一份包含所有遠端分支、會議或工作事件的完整工作紀錄。

## 已測與未測

已先以回歸測試重現原錯誤，再最小修正；9 項測試通過，包含預設 stdout、`--output FILE` 的 `json.loads` 與欄位逐項一致，以及原分類/套版管線。

未執行真人 Claude 的週報生成、真實 gh PR/issues 查詢或外部服務。`draft.md` 只是機械式草稿；references/examples 的示例成果與數字不能當成本次實測。

原版素材沿用來源 MIT 授權，見精華包根目錄第三方授權與逐檔來源清單；本目錄只修正可重現的資料收集問題，未把完整模型整合描述為已驗證。
