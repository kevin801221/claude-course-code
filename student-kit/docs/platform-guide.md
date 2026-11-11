# Part 15：IDE、執行平台、Cowork 與 Artifacts 課堂導讀

這份導讀補足 v1 只有章節對照、沒有實際平台練習的缺漏。依據 `Claude_Code_完整教學_v13_2_講師版_2026-10-2.pdf` **印刷投影片 479–506／PDF 實體頁 478–505**，把每個平台的入口、條件、操作與驗收串起來。

**本頁是依講義撰寫的原創操作教材，沒有假稱五個來源 Repo 附有完整的平台程式。**來源 Repo 主要提供 CLI／設定參考表及瀏覽器工具比較；IDE、Desktop、Remote Control、Cowork、Artifacts 等段落原本就是產品操作示範。本次只整理與靜態核對，沒有替學生登入、啟用功能、控制 App、發布頁面或呼叫模型。

講義為 2026-10 快照，其中方案、最低版本、介面名稱與預覽功能可能改變。下文寫「講義列為」的條件是該版本的紀錄；上課時以自己的 `claude --help`、`/help`、實際帳號與官方文件為準。功能不在清單時記為「此環境不可用」，不把它當作程式測試失敗，也不為了完成練習移除組織限制。

## 先選對入口

| 你要完成的工作 | 先用哪個入口 | 本堂要看見的成果 |
|---|---|---|
| 讀程式、修 bug、跑測試或自動化 | CLI | 可回查的命令、檔案變更與測試結果 |
| 邊看編輯器邊討論程式與 diff | VS Code／JetBrains | 選取範圍、檔案引用與 diff 對得上 |
| 用圖形介面管理本機 session、預覽與 review | Desktop 的 Code 入口 | 知道 session 的工作目錄與實際輸出 |
| 用手機接手本機正在跑的工作 | Remote Control | 同一個本機 session 可接續與中止 |
| 讓任務在託管的 checkout 中跑 | Web／Mobile 的雲端 Code session | 遠端 checkout 的 commit 與環境可辨認 |
| 研究、整理文件或交付報表 | Claude／Cowork | 在授權的資料範圍交出可檢查成品 |
| 用頁面呈現一次工作的結果 | Artifacts | 有正確內容、可更新且可見範圍清楚的頁面 |
| 做可編輯設計稿或簡報 | `/design`／`/slides`，若帳號提供 | 可編輯成品與匯出檔，不只是一張截圖 |

同樣叫 session，不代表跑在同一台機器；看得到一份文件，也不代表能讀到你電腦上的任意資料夾。每個練習先確認「在哪裡跑、能碰哪些資料、成果放哪裡」。

## 共同準備與記錄

1. 先將學生專用 ZIP 解壓到獨立資料夾，避免在其他 Repo 底下啟動而載入父層設定。細節見 [首頁](../README.md)。
2. 在根目錄執行 `node --version`、`python3 --version`、`npm test`，先確認不依賴模型的基線。
3. 使用 Claude Code 時執行 `claude --version`、`claude --help`；進入互動對話後用 `/help` 確認指令。只有尚未登入時，才依產品提示或 `/login` 完成自己的認證。
4. 在使用 IDE、Desktop 或手機前，確認選到這個練習資料夾／Repo／分支。需要 Git worktree 的功能另需有效的 Git Repo 與起始 commit；不要把既有未提交工作當成乾淨練習場。
5. 每次只驗一個平台；保留版本、操作、觀察與成果位置。**不要記錄 token、登入 QR code 或私密配對連結。**

共同驗收任務可以使用這句話：

```text
先讀 CLAUDE.md、bin/tasks.mjs 與 src/task-board.mjs。
只解釋目前 add、list、done 的輸入、輸出及資料檔位置，先不要修改。
把實際讀到的內容與尚未測試的推論分開。
```

本機 CLI、IDE 與 Desktop 可用同一份專案比較；雲端 session 必須另外確認 checkout，不能假設本機尚未提交的檔案會自動出現。

### 講義記錄的門檻，供上課時比對

下表轉錄的是**講義當時的條件**，不是本次已連線確認的最新支援矩陣。版本達標也不代表帳號、組織開關或權限已具備。

| 功能 | 講義列出的條件 | 印刷頁碼 |
|---|---|---|
| Desktop 面板／編輯器 | Desktop v1.2581.0+；PR 監控另需已登入的 `gh` | 485 |
| Computer use | macOS、Pro／Max、互動式 session；系統輔助使用與螢幕錄製權限；不適用 `-p` | 489 |
| Self-hosted runner | Team／Enterprise、CLI v2.1.224+、Git 2.24+、Linux／macOS；由組織部署 | 490 |
| Cowork 合一介面 | Pro／Max 逐步推出、Team beta、Enterprise 管理員開關；本機操作另需 Desktop | 493–498 |
| Artifact 發布 | Pro／Max／Team／Enterprise、claude.ai 登入、CLI v2.1.183+ 或 Desktop v1.13576.0+；組織需允許 | 500、505 |
| Artifact 留言／自動回覆 | Team／Enterprise 的組織內分享；留言 v2.1.221+、自動回覆 v2.1.228+ | 503 |
| Artifact connector | v2.1.209+、可用 connector、檢視者授權與組織獨立開關；不能把它當公開資料頁分享 | 504 |
| `/design`／`/slides` | v2.1.265+、beta 範本；Enterprise 由 Owner 開啟，仍須符合 artifact 條件 | 506 |

講義也把 CMEK、HIPAA、ZDR、第三方雲端憑證，以及 SDK／CI 等列為需要另外核對或封鎖 artifact 的情境。課堂不要為了讓示範成功而調整這些組織條件；改記「此環境不可用」即可。

## 1. CLI：所有比較的基線

來源定位：投影片 480–481（PDF 479–480），CLI 操作細節另見 Part 02。

**適合：**需要完整終端機工具、腳本化輸出、可明確指定工作目錄的工程工作。CLI 本身、互動對話與 `-p` 模式是不同使用方式；手機遙控不等於把 CLI 安裝到手機。

**需要：**已安裝的 CLI、自己的有效認證，以及對練習資料夾的檔案權限。執行程式或呼叫模型時，分別受本機環境及帳號額度影響。

1. 從精華包根目錄執行 `claude --permission-mode manual`；若自己的版本未列出 `manual`，先對照 [版本說明](compatibility.md)。
2. 貼上共同驗收任務，觀察實際讀檔，不只看回答是否流暢。
3. 需要討論變更時先用 `/plan`，完成條件寫成能重現的輸入與輸出。
4. 在終端機自行執行 `npm test`，區分模型敘述與真實程序結果。

**驗收：**回答能指出目前資料存放方式與限制；沒有執行測試時不宣稱測試通過。後面各平台都用相同任務比較，不用模型回答長度評分。

## 2. VS Code：檔案、選取範圍與 diff

來源定位：投影片 480、482、484（PDF 479、481、483）。

**適合：**要在編輯器裡核對程式位置、使用選取範圍作 context、逐段檢查修改。需要官方 Claude Code 擴充套件、支援版本的 VS Code，以及可用帳號。請由官方平台入口確認安裝方式與發行者。

1. 在 VS Code 開啟獨立精華包資料夾，打開 `src/task-board.mjs`。
2. 從擴充套件的入口開啟 Claude Code。講義使用右上圖示與 `Cmd+Esc`／`Ctrl+Esc` 切換焦點；實際快捷鍵以自己的 keybindings 為準。
3. 選取 `completeTask`，用插入檔案／選取範圍的功能加入對話。講義記錄 macOS `Option+K`、其他平台 `Alt+K`。
4. 問：「只解釋這段在找不到 ID 時會做什麼。」檢查引用檔案、行範圍與原文一致。
5. 在練習分支請它替錯誤訊息加一個不改行為的說明，查看 IDE diff，再自行跑 `npm test`。若不想修改，可只觀察教師準備的 diff。
6. 若從外部終端機啟動 CLI，在自己的 `/help` 有提供時使用 `/ide`，確認連到這個 VS Code 視窗。講義另提 `--ide`、`autoConnectIde`；需先由自己版本確認支援。

**驗收：**選取內容確實成為脈絡；diff 顯示的是這個工作目錄的檔案；測試結果與回報一致。只是在 VS Code 內建 terminal 跑 `claude`，不等於已驗證所有擴充套件整合。

## 3. JetBrains：把同一個情境換到另一個 IDE

來源定位：投影片 480、483–484（PDF 479、482–483）。

**適合：**使用 IntelliJ、PyCharm、WebStorm 等 JetBrains IDE 的同學。講義要求安裝 Claude Code plugin，並另備 CLI；支援的產品／版本要以當前 Marketplace 與官方平台頁為準。

1. 在 IDE 開啟同一個獨立練習專案，確認 plugin 已啟用。
2. 從 IDE 的 terminal 或整合入口開啟 Claude Code，選取 `completeTask`。
3. 使用 plugin 提供的檔案／選取範圍引用，再問與 VS Code 相同的問題。講義記錄 macOS `Cmd+Option+K`；請以自己的 keymap 核對。
4. 若外部終端機沒有連上 IDE，先用 `/ide` 檢查偵測結果，避免連到另一個已開啟的專案。
5. 觀察 diff viewer、診斷資訊與實際檔案是否一致，再跑原本的專案測試。

**驗收：**能指出 plugin 做了哪些 IDE 整合，哪些仍是 CLI／測試工具的工作。沒有 JetBrains 環境的同學可做觀察與流程比較，記錄為「未操作」。

## 4. Desktop：session、工作目錄與本機預覽

來源定位：投影片 485–486（PDF 484–485）。官方入口：[Desktop](https://code.claude.com/docs/en/desktop)、[Desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart)。

**適合：**偏好圖形介面的本機 session、diff、任務與預覽管理。講義記錄 Desktop 的 Code 入口與 Git worktree 隔離；面板、作業系統支援與最低版本屬快照條件，請先在自己的 App 確認。PR 監控另需可用的 GitHub CLI 認證，不是這個基本練習的必要條件。

1. 在 Desktop 的 Code 入口選取練習專案，開一個本機 session。
2. 確認 session 顯示的工作目錄、Repo／分支；若它使用 worktree，後續檔案必須在這個 worktree 建立。
3. 執行共同驗收任務，再用 diff／檔案面板核對結果。若沒有修改，不應出現憑空的變更數字。
4. 若要測試瀏覽器面板，在**此 session 的實際工作目錄**建立一個最小預覽：

```bash
mkdir -p .outputs/platform-preview
cat > .outputs/platform-preview/index.html <<'HTML'
<!doctype html>
<html lang="zh-Hant">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>課堂預覽</title>
<main>
  <h1>Claude Code 課堂預覽</h1>
  <button onclick="this.textContent='已完成練習'">完成練習</button>
</main>
</html>
HTML
python3 -m http.server 8765 --bind 127.0.0.1 --directory .outputs/platform-preview
```

5. 開啟 `http://127.0.0.1:8765`，確認頁首及按鈕可見，點按鈕後文字改為「已完成練習」。若要讓 Desktop 啟動預覽，講義的 `.claude/launch.json` 格式可改成下列例子；僅在目前 App 確認支援後使用：

```json
{
  "version": "0.0.1",
  "configurations": [{
    "name": "classroom-preview",
    "runtimeExecutable": "python3",
    "runtimeArgs": ["-m", "http.server", "8765", "--bind", "127.0.0.1", "--directory", ".outputs/platform-preview"],
    "port": 8765
  }]
}
```

6. 在瀏覽器面板請 Claude 檢查同一個頁首與按鈕，對照實際工具紀錄／畫面。完成後在啟動 server 的 terminal 按 `Ctrl+C`。

**驗收：**知道頁面由哪個程序與 worktree 提供；能完成一次真實點擊，關閉程序後預覽不再可用。這是本頁供同學手動建立的最小示範，不是來源 Repo 已附的完整 Web App。內建 browser 的登入狀態不應假設與自己的 Chrome 共用。

## 5. Remote Control：接手本機 session

來源定位：投影片 487（PDF 486）。官方入口：[Remote Control](https://code.claude.com/docs/en/remote-control)。

**適合：**工作依賴本機檔案、工具或本機 MCP，但想從另一個畫面接續。需要支援此功能的 CLI、相同帳號、可用網路與持續運作的本機程序；組織可能限制此功能。

1. 先跑 `claude remote-control --help`，確認自己的版本提供此子命令。
2. 在練習目錄啟動 `claude remote-control`，依畫面取得自己的連線方式。若要從已存在的互動 session 開啟，先確認 `/help` 提供 `/remote-control` 或 `/rc`。
3. 在自己的瀏覽器或手機登入同一帳號，選取該 session，請它讀取公開的練習 README。
4. 回到本機終端機核對：兩個畫面是否對應同一個任務、目錄與工具結果。
5. 在本機停止 Remote Control 程序，再確認遠端不會繼續把它當作可操作的本機 session。

**驗收：**能說出程式仍在哪台機器跑、何時會中斷；不能把雲端 checkout 與本機目錄混稱同一份工作。配對 QR code／連線網址不放進公開作業。講義的 capacity、spawn、continue 等進階旗標請另外按自己的 help 測試，不是完成這個基本驗收的必要條件。

## 6. Web 與 Mobile：先辨認三種任務去向

來源定位：投影片 488、491（PDF 487、490）。官方入口：[Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)。

| 講義中的方式 | 任務在哪裡跑 | 課堂先確認什麼 |
|---|---|---|
| Web／Mobile 的雲端 Code session | 遠端 checkout／雲端環境 | Repo、branch、commit、可用工具與依賴 |
| Remote Control | 自己電腦的 CLI session | 本機程序是否還在、目錄是否正確 |
| Dispatch | 自己電腦的 Desktop 路線 | 帳號是否仍有入口；講義將它列為不再開放新用戶的既有功能 |

1. 在自己的 Web／Mobile Code 入口找一個可用路線，不以介面名稱推斷它的執行位置。
2. 若使用雲端 session，明確選練習 Repo／分支；從 README 找一段已提交文字，要求它指出讀到的內容。
3. 另在本機新建一個尚未提交的示範檔，確認雲端不會憑空看見它；不要放私人資料作測試。
4. 若使用 Remote Control，接續上一節，核對它看見的是本機工作。
5. 檢查可選權限模式、通知及可用指令，記錄與講義不同之處。講義的 `/mobile`、`/ios`、`/android` 只在自己 `/help` 仍提供時使用。

**驗收：**能畫出「手機／Web 畫面 → 實際執行環境 → 資料來源」；知道關閉筆電對哪條路線有影響。無此入口或認證不足時，記為「帳號條件未具備」，不用假裝成功執行。

## 7. Computer use：原生介面操作選修

來源定位：投影片 489（PDF 488）。官方入口：[Computer use](https://code.claude.com/docs/en/computer-use)。

講義將它列為特定 macOS／方案的互動功能，需要輔助使用與螢幕錄製權限；本包沒有操作任何 App，也不替你開啟這些權限。

1. 先核對自己的作業系統、帳號與 `/mcp` 清單是否提供這個功能。
2. 若同學選擇操作，依 App／系統提示授予必要權限，先用不含私人資料的課堂預覽或測試視窗。
3. 要求它只檢查一個已指定按鈕及結果，對照實際畫面與工具紀錄。
4. 測試產品提供的停止方式；講義記錄 `Esc`，請在目前介面確認。

**驗收：**有真實的輸入動作與畫面狀態變化；截圖存在不等於按鈕真的操作過。沒有可用環境時，保留這節作演示觀察，不把它列為每人必過的離線測試。

## 8. Self-hosted runner：組織環境選修

來源定位：投影片 490–491（PDF 489–490）。從[官方平台入口](https://code.claude.com/docs/en/platforms) 查目前的環境選項。

講義把自架環境列為 Team／Enterprise 的公開測試功能，需組織管理員、runner 主機／容器、Git 與對外連線。這是組織基礎設施練習，本包沒有提供已部署的 runner。

1. 先由管理員確認目前產品與組織政策是否支援；沒有條件的同學只讀流程。
2. 在組織提供的隔離環境，依官方步驟建立 cloud environment、保存 environment key，再啟動 runner。講義的 `claude self-hosted-runner setup` 只有在本機 help 仍提供時使用。
3. 到管理畫面確認 runner 的健康狀態，再從 Code 的雲端入口選取該環境。
4. 用不含機密的示範 Repo，核對實際工具鏈、checkout、建置產物的位置。

**驗收：**管理畫面、session 環境與測試輸出相互一致；environment key 不進程式庫。講義也提醒自架執行環境不等於推論完全離線，需另外核對推論供應商與資料流。

## 9. Claude／Cowork：知識工作與工程工作的交接

來源定位：投影片 492–498（PDF 491–497）。官方入口：[Claude Help Center](https://support.claude.com)。

**適合：**研究、分析、整理檔案、產生文件與報表。講義記錄 Chat 與 Cowork 合一的逐步推出狀態；你的帳號可能呈現不同入口，不把某個分頁名稱當作一定存在。

**條件：**自己的可用方案；若要碰本機資料夾、瀏覽器或電腦，還需支援的 Desktop、已連接的資料範圍與實際授權。雲端／手機入口看見任務，不等於它隨時能碰到所有本機檔案。

1. 準備只有假資料的課程表，例如「CLI：已完成；Hooks：待練習；MCP：待練習」。
2. 在可用的 Claude／Cowork 入口要求整理成一份課堂進度表，說清楚預期檔案或 artifact；只引用這三筆資料。
3. 如果用本機檔案，僅連接練習資料夾，記下任務實際從哪裡讀到資料。
4. 核對完成狀態與來源三筆資料一致，打開交付物確認它不是只有聊天描述。
5. 將「替程式修 bug、跑測試」交給 Claude Code，將「整理驗收結果、編排報告」交給知識工作入口，觀察兩者需要的輸入與證據差異。

**Skills／Plugins 對照練習：**講義指出 Cowork 的 account／Customize 路線與本機 `~/.claude/` 不同；本機檔案存在不能作為它已載入的證據。挑一個不含 shell 的純文字 Skill，分別查看實際可見性與呼叫方式；需要 Bash 的 Skill 不應直接當作跨介面可攜成品。記錄目前介面的實際限制，未驗證的同步行為不要自行補成事實。

**驗收：**交付物可開啟、內容可回到來源，並說得出它在哪裡執行、能讀哪些資料。這不是本包已替學生做好的雲端工作環境。

## 10. Artifacts：產生、更新、分享與資料來源

來源定位：投影片 499–505（PDF 498–504）。官方入口：[Artifacts](https://code.claude.com/docs/en/artifacts)。

### A. 先確認可用條件

講義列出以下條件：使用 claude.ai 認證、支援的方案／版本、組織允許發布，並可能有獨立的 connector 開關；API key、第三方雲端憑證、SDK／CI 情境不應直接視為已具備同樣能力。上課先在自己的帳號／設定確認，不能只看 CLI 版本號。

### B. 產生一個只含示範資料的頁面

在可用的 Claude Code 對話中要求：

```text
請用以下示範資料製作一個課堂進度 artifact：
CLI 已完成、Hooks 待練習、MCP 待練習。
顯示三項狀態與來源是本次假資料，不串接任何外部服務。
發布前列出將使用的檔案和可見範圍；本次維持私人。
```

1. 核對實際發布提示中的檔案、標題與範圍，再依自己的選擇完成發布。
2. 開啟**這次回傳的真實網址**，確認三項狀態、頁面標題與畫面可讀性。
3. 不把講義裡截斷的 `5fbea6f3-...` 範例當成可用的成品網址。

### C. 更新同一份，而不是再建一份

1. 在同一個 session 將 Hooks 改為已完成，指定更新既有 artifact。
2. 重整原網址，確認它顯示新狀態，而非只有聊天回覆說改好了。
3. 新開 session 時，明確提供那個網址；若自己的版本提供 `/artifacts`，也可從清單附上既有頁面。

**驗收：**網址及頁面身份仍對得上，更新結果可觀察，沒有把新的不同網址誤認成原頁更新。

### D. 分享與留言是另一個驗收

先看 Share 控制項的實際範圍。講義記錄私密、組織與公開連結的差別，且組織政策可能停用某些選項。若要練習分享，只使用上面的假資料，明確選取對象／範圍，再由另一個有相應身分的視窗確認能否開啟。

講義的組織內留言／回覆另有版本與帳號條件。只有實際出現留言功能時，才留一則「請將 Hooks 標為已完成」的示範留言，觀察 session 是否收到，以及回應／修改是否真的發生；不要把沒有測試的自動回覆當作已完成。公開頁面的可用功能也要分開確認。

### E. Connector 頁面與本機 MCP 不同

以可用的唯讀 connector 做選修示範前，先確認頁面允許呼叫的範圍、檢視者要授權的帳號，以及資料來源。講義指出發布後的頁面不能直接呼叫你本機 `.mcp.json`，使用 connector 的頁面亦有分享範圍限制。

**驗收：**畫面資料可對照到這次 connector 的結果與時間；換檢視者時知道用的是誰的授權。沒有 connector 的同學仍可完成上面的靜態假資料練習，不能捏造查詢結果。

### F. 說得出產品邊界

講義的 artifact 是工作結果的呈現，不應被當成已具備後端、持久化表單與多路由的完整產品。頁面上的按鈕能變色，不代表資料已寫入資料庫；需要這些功能時，回到實際應用專案設計資料與後端契約。

## 11. `/design` 與 `/slides`：可編輯成品驗收

來源定位：投影片 506（PDF 505），相關可用條件見 505。從 [Artifacts 官方入口](https://code.claude.com/docs/en/artifacts) 與自己的 `/help` 確認目前支援；講義把這些範本列為 beta，不能視為所有帳號必然可用。

1. 在獨立練習專案中，準備設計需求與一小段 design system：

```markdown
## Design system
- Colors: primary #1a4d8f, accent #f59e0b, surface #f8fafc
- Typography: Inter for body, JetBrains Mono for code
- Spacing: 8px scale, 6px border radius
```

2. 若 `/design` 可用，要求設計「課程進度設定畫面」，包含三個課程狀態與一個保存按鈕；不要用真實金融或個人資料作範例。
3. 打開產出的編輯介面，修改一個標題／元件，重新載入確認編輯是否保留；實際匯出一個目前介面支援的 PNG／PDF 並打開檢查。
4. 若 `/slides` 可用，要求用同一份假資料做三頁簡報：課程目標、目前進度、下一步。逐頁核對文字、順序、可編輯性與匯出結果。
5. 若只有一般 HTML／Markdown／圖片輸出，就按實際格式記錄，不將它描述成已驗證的可編輯 Design／Slides 成品。

**驗收：**設計規則真的影響成品；內容符合三筆資料；至少一次編輯與匯出被實際打開確認。模型說「已產生」或貼出預覽截圖，不能代替上述操作。

## 交付一張平台驗收表

每位同學只填自己真的操作過的項目；其他填「不可用」「只看示範」或「未驗證」。

| 平台／版本 | 執行在哪裡 | 使用的資料範圍 | 實際操作 | 成果位置／可見範圍 | 已觀察結果 | 尚未驗證 |
|---|---|---|---|---|---|---|
| CLI | 本機練習目錄 | 公開教材 | 讀檔、測試 | terminal／檔案 | 自行填寫 | 自行填寫 |
| 自選 IDE／Desktop | 自行填寫 | 自行填寫 | 選取／diff／點擊 | 自行填寫 | 自行填寫 | 自行填寫 |
| 自選 Remote／Web／Mobile | 自行填寫 | 自行填寫 | 接續／讀取 checkout | 自行填寫 | 自行填寫 | 自行填寫 |
| 自選 Cowork／Artifacts／Design／Slides | 自行填寫 | 假資料或已授權來源 | 產生／更新／開啟 | 自行填寫 | 自行填寫 | 自行填寫 |

本頁補的是 Part 15 的完整操作路線。核心程式是否正確、平台能否使用、外部帳號是否允許、真人流程是否驗證，是四個不同的問題；作業回報要分開寫。

## 來源定位與文件範圍

- 原講義：印刷 479–506／PDF 478–505；其中 IDE 480–484、Desktop 485–486、Remote／Mobile 487–488、computer use 489、self-hosted 490、路線比較 491、Cowork 492–498、Artifacts 499–505、Design／Slides 506。
- 講義明列官方入口：[Platforms](https://code.claude.com/docs/en/platforms)、[Artifacts](https://code.claude.com/docs/en/artifacts)、[Claude Help Center](https://support.claude.com)。其餘本頁官方 URL 可在指定來源 Repo 的 Markdown 中找到；未在本次工作連外確認內容更新。
- `claude-code-zh-tw/best-practice/claude-cli-startup-flags.md` 僅補充部分平台旗標；`reports/claude-in-chrome-v-chrome-devtools-mcp.md` 是瀏覽器工具比較；英文 `claude-code-best-practice/best-practice/claude-settings.md` 有相關設定欄位。三者都不是以上全部平台的現成應用程式。
- 沒有在這次整理中替學生安裝、登入、開權限、操作原生 App、建立遠端連線、啟動 runner 或發布 artifact；步驟是供教師與同學實際操作後留下證據。
