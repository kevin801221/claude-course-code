# Claude Code 同學實作精華包

Kevin Luo 課程配套 · 2026-11-11 · v1.0.0

**從一個能離線執行的小專案開始，把 CLAUDE.md、Commands、Skills、Agents、Hooks、MCP 串成能驗收的工作流。**本包依課堂完整講義編排，從五個指定 Repo 去重、挑選原碼並修正可攜性；不用先讀完數百頁文件。

## 同學請從這裡下載

**[下載學生專用 ZIP](https://raw.githubusercontent.com/kevin801221/claude-course-code/student-kit-v1.0.0/student-kit/dist/claude-code-student-kit-v1.0.0-2026-11-11.zip)**，解壓到獨立資料夾，例如桌面。解壓後應有 `claude-code-student-kit/`，裡面可看到 `package.json`、`CLAUDE.md`、`labs/` 與隱藏的 `.claude/`。

這個 GitHub 頁面位於較大的 `claude-course-code` Repo 的 `student-kit/` 子目錄；GitHub 的 Code → Download ZIP 會下載整個分支，外層目錄名稱和本包不同。首次上課請使用上面的學生專用 ZIP。

如果你已 clone 整個 Repo，可在 `student-kit/dist/` 找到同一份 ZIP，將它解壓到該 Repo 外再啟動 Claude。從父 Repo 內直接進入 `student-kit/`，Claude 仍可能向上載入父層的 CLAUDE.md 與設定，影響這份精華包的操作。

## 15 分鐘開始

先完成上面的獨立解壓，再準備 Node.js 22+、Python 3.10+。本包根專案只用標準函式庫，**不需要 `npm install`、API key 或 Claude 登入就能跑測試**。從解壓資料夾的外層執行：

```bash
cd claude-code-student-kit
node --version
python3 --version
npm test
npm run check
npm run tasks -- add "完成第一個 Claude Code 練習"
npm run tasks -- list
```

`add` 會回傳任務 ID；複製後執行 `npm run tasks -- done <id>`，將 `<id>` 換成真的 ID，不含角括號。資料存在目前目錄的 `tasks.json`，已排除版控。測試使用臨時目錄，不會清空你的任務。

使用 Claude Code 時，先依 [官方安裝文件](https://code.claude.com/docs/en/setup) 安裝並登入，再從本 Repo 根目錄啟動：

```bash
claude --version
claude --permission-mode manual
```

對話中先試：`請先讀 CLAUDE.md，解釋這個專案的輸入、輸出與驗收方式，先不要修改。`

接著輸入 `/course-plan 新增 list --pending，只顯示未完成任務`。這個功能是課堂作業，出廠版本尚未實作。完成後用 `/course-check` 交出測試證據。

## 跟著課程做

以下時間是建議練習時間，不包含安裝與講解。路線：首次使用做 00～03；半日實作做 00～07；進階課再做 08～11。

| Lab | 你會做出什麼 | 建議時間 | 講義 Part |
|---|---|---|---|
| [00 CLI 與權限](labs/00-cli/README.md) | 能讀懂 CLI、工具與檔案影響範圍 | 15 分 | 00～03、05～07 |
| [01 Memory / Context](labs/01-memory/README.md) | 專案規則、任務卡、context pack | 20 分 | 08～09 |
| [02 Commands](labs/02-commands/README.md) | 帶參數的 `/course-plan` | 15 分 | 04 |
| [03 Skills](labs/03-skills/README.md) | 可執行的文件產生器與驗收 SOP | 25 分 | 10 |
| [04 Agents](labs/04-agents/README.md) | 有輸入、輸出與證據的只讀 reviewer | 20 分 | 11 |
| [05 Hooks](labs/05-hooks/README.md) | 可獨立測試的 PreToolUse guard | 25 分 | 12 |
| [06 MCP](labs/06-mcp/README.md) | 不需網路的課程搜尋工具 | 25 分 | 13 |
| [07 Plugins](labs/07-plugins/README.md) | 本機載入 `/course-review:review` | 20 分 | 14 |
| [08 整合工作流](labs/08-workflows/README.md) | Command → Agent → Skill 天氣卡 | 25 分 | 04、10～11 |
| [09 自動化](labs/09-automation/README.md) | 有明確工具範圍的 JSON 摘要腳本 | 15 分 | 16 |
| [10 專案與交接](labs/10-projects/README.md) | ML / Teams / RAG 配方與可驗收交接 | 40 分 | 18～20、附錄 B |
| [11 Mods 選修](labs/11-mods/README.md) | 看懂 Matt 導航的狀態機與關卡 | 40 分 | 14 |

## 寶藏在哪裡

- [講義原生小專案](examples/lecture-mini-projects/README.md)：俳句 Command／Skill、食譜 Agent、番茄鐘 Hook，附原碼與可攜設定。

- [可攜天氣工作流](examples/weather-workflow/README.md)：保留真實原碼，拿掉未附的音效依賴。
- [可帶走的範本](resources/templates/README.md)：文件產生器、三種代理、兩個 commands、PRP 與審查模板。
- [進階專案配方](advanced/project-recipes/README.md)：晶圓四代理、原生 Agent Teams 契約、離線 RAG 流程。
- [Matt Mods 原碼與導讀](advanced/matt-flow-mods/STUDENT-GUIDE.md)：完整核心、型別與測試原碼，列出版本依賴。
- [七篇精選導讀](docs/reading-guide.md)、[講義頁碼對照](docs/lecture-map.md)、[講師帶課建議](docs/teaching-notes.md)。

## 打開資料夾前先知道

本包根層提供規則、command、skill 與只讀代理，專案權限設定為 `manual`；你既有的使用者/組織設定仍可能影響 session。Hooks、MCP、Plugin 都由各 Lab 明確載入；Mods 與專案原始代理是選讀，不會自動執行。不要把整個 advanced/ 搬進 `.claude/`。

真人 Claude 對話、天氣查詢、Headless、Teams 與 ML 訓練需要各自環境或帳號；離線測試不代表這些端到端流程已通過。請看 [驗證紀錄與限制](docs/verification.md) 和 [版本說明](docs/compatibility.md)。

分享前的獨立複檢與修正，見 [分享檢查紀錄](docs/share-review.md)。

## 來源與授權

五個來源：`claude-code-best-practice`、`claude-code-zh-tw`、`claude-course-code`、`claude-howto-zh-TW`、`matt-flow-mods`。中文 best-practice 是英文上游的翻譯，course-code 與 howto 有衍生與重複內容，本包依用途去重。

每份精選原碼可在 [來源清單](SOURCES.md) 與 [逐檔 manifest](sources/manifest.json) 查到原路徑、固定 commit、原樣／改寫分類與雜湊。新撰程式與說明採 [MIT](LICENSE)，來源授權完整保留於 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 與 `licenses/`。本包未附講師版完整 PDF、模型權重、資料集、個人憑證或 Git 歷史。

想建立自己的作業 Repo，可在解壓後執行 `git init -b main`，設定自己的 Git 作者，再 `git add .` 與 `git commit`。上課不需要先推送 GitHub。
