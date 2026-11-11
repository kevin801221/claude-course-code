# ✦ matt-flow：Matt 導航

Claude Code 的 mod（一種外掛）。讓 Claude 沿著 [Matt Pocock](https://github.com/mattpocock/skills) 的開發流程走：它知道目前在哪一步，想跳步時會被擋下，每一步結束時把下一步的指令交給你，按 Tab 收下就繼續。分新手、進階、高手三個等級，旁邊有看進度用的面板，`/matt-flow all` 還能一次看所有專案。

**為什麼要用**：直接用 Claude Code，需求還沒問清楚它就開始改程式，做完也不一定檢查、複盤，流程全靠你自己記。Matt Pocock 把一套開發流程寫成了 skill：先追問到需求清楚，再寫測試和程式，接著檢查，最後複盤、改進下一次的環境。matt-flow 不加新的 skill，只讓你和 Claude 照這套流程的順序走。

**適合誰**：自己用 Claude Code 做功能的人。它是給自己的護欄，不是權限控管：總覽只看得到你這台電腦上的專案，你也隨時可以跳過步驟或關掉它。想看流程會產出什麼，[.scratch/rail/](.scratch/rail) 是做 0.3 版時留下的規格書和任務卡。

![還沒到動手做時叫 Claude 直接改程式碼，它停手，把 /implement 留給你；接著打開面板、按「我卡住了」、看所有專案](https://raw.githubusercontent.com/kevin801221/matt-flow-mods/70b50bc1b822eb18d770f8f75588b3b01f77cc27/docs/images/demo.gif)

_示範：叫 Claude 直接改程式碼，它停手，把下一步要打的 `/implement` 留給你；接著打開面板、按「我卡住了」、看所有專案。示範在一個暫時建立的專案裡錄製，總覽裡的其他專案是示範資料。_

第一次用：先照下面的「前置條件」和「安裝 matt-flow」裝好，再照 [從零開一個新專案](docs/new-project.md) 一步一步做。

## ⚠️ 前置條件

**Claude Code 要夠新**：matt-flow 用到 Claude Code 新的 mod 功能，作者用的是 2.1.312 以後的版本。用 `claude --version` 看版本，太舊就先執行 `claude update`。目前只在 macOS 上用過；Windows 請在 WSL 裡用，原生 Windows 的路徑寫法不同，程式碼關卡可能擋不住。

**先安裝 mattpocock-skills**：matt-flow 只是導航，本身不包含任何 skill。面板叫你執行的 `/grill-with-docs`、`/to-spec`、`/implement` 等指令，全部來自 `mattpocock-skills` 這個 plugin。沒有先裝的話，面板還是打得開，但它叫你跑的指令都無法執行。

在**個人層級**或**專案層級**擇一安裝：

```bash
# 個人層級：這台電腦上所有專案都能用（建議）
claude plugin install mattpocock-skills@claude-plugins-official

# 專案層級：只有這個專案能用，在專案根目錄執行
claude plugin install mattpocock-skills@claude-plugins-official --scope project
```

也可以在 Claude Code 的提示列輸入 `/plugin install mattpocock-skills@claude-plugins-official`，再選範圍。

`mattpocock-skills` 收錄在 Anthropic 官方的 marketplace（`anthropics/claude-plugins-official`）。安裝時如果出現找不到 marketplace 的錯誤，先加入這個 marketplace，再重新安裝：

```bash
claude plugin marketplace add anthropics/claude-plugins-official
```

安裝時會自動把檔案下載到 `~/.claude/plugins/cache/claude-plugins-official/mattpocock-skills/<版本>/`，啟用設定則寫進 settings：個人層級寫在 `~/.claude/settings.json`，專案層級寫在專案的 `.claude/settings.json`。**不要自己把檔案複製進 `cache` 資料夾**，沒有經過安裝登記的 plugin 不會被啟用。

確認是否裝好：

```bash
claude plugin list
```

看到下面這樣就代表可以用了：

```
❯ mattpocock-skills@claude-plugins-official
  Version: 1.3.1
  Scope: user
  Status: ✔ enabled
```

## 安裝 matt-flow

下面兩種方法擇一就好。兩種都裝的話，只有其中一份會跑，兩份的進度也分開記。

### 方法一：用 plugin 指令安裝（建議）

在 Claude Code 的提示列輸入：

```
/plugin install matt-flow --marketplace kevin801221/matt-flow-mods
```

出現 `Add marketplace?` 時按 `y`，接著選安裝範圍（預設是個人層級，直接按 Enter）。

從 shell 安裝：

```bash
claude plugin install matt-flow --marketplace kevin801221/matt-flow-mods
```

桌面版 App 不能用 `/plugin`：點提示框旁邊的 + → Plugins → Add marketplace，輸入 `kevin801221/matt-flow-mods`，再按 Add plugin。

### 方法二：下載到 skills 資料夾

放在 skills 資料夾裡的 mod，Claude Code 會自動載入，而且一存檔就套用到所有開著的 session。所以這個資料夾只拿來安裝，不要在裡面改程式碼（要改的話見最後的「開發」）：

```bash
# 個人層級
git clone https://github.com/kevin801221/matt-flow-mods ~/.claude/skills/matt-flow

# 專案層級（在專案根目錄執行）
git clone https://github.com/kevin801221/matt-flow-mods .claude/skills/matt-flow
```

下載好之後，開一個新的 Claude Code session 就會生效。專案層級的話，把 `.claude/skills/matt-flow/` 加進專案的 `.gitignore`，不然 git 會把它當成另一個 repo 一起加進去。

### 更新、停用、移除

| | 方法一（plugin 指令） | 方法二（skills 資料夾） |
| --- | --- | --- |
| 更新 | `claude plugin update matt-flow@matt-flow`，再重開 Claude Code | `git -C ~/.claude/skills/matt-flow pull` |
| 暫時停用 | `claude plugin disable matt-flow@matt-flow`，用 `enable` 打開 | 把資料夾移出 `~/.claude/skills/` |
| 移除 | `claude plugin uninstall matt-flow@matt-flow` | 刪掉 `~/.claude/skills/matt-flow` |

只想在某個專案關掉，用 `/matt-flow off`（見「跳過、結束、關掉」）。matt-flow 自己出錯、每個專案都改不了程式碼時，照上表停用它。

## 使用方式

matt-flow 是一條軌道：它記得每個專案走到流程的哪一步，把這件事附在你的輸入旁邊告訴 Claude，擋下跳步的指令和還沒到時候的動作，並在每一步做完時把下一步的指令交給你。指令一律由你輸入，matt-flow 自己不會執行任何步驟。

### 已知問題

- Claude 改用 Bash（或其他能跑指令的工具）寫檔，不會被程式擋下，只靠擋下訊息和軌道禁止。

### 等級

| 等級 | 流程 |
| --- | --- |
| 🌱 新手 | `/setup-matt-pocock-skills` → `/grill-with-docs` → `/implement` → `/mattpocock-skills:code-review` → `/retro` |
| 🚀 進階 | `/setup-matt-pocock-skills` → `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement` → `/retro` |
| 👑 高手 | `/setup-matt-pocock-skills` → `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement-spec` → `/pr` → `/retro` |

「檢查」要打全名 `/mattpocock-skills:code-review`：Claude Code 自己也有一個 `/code-review`，打短的會跑到內建那個，而且它在背景跑，matt-flow 看不到它跑過，commit 關卡也不會解開。matt-flow 給你的檢查指令都是全名。

等級在面板上隨時可以換。第一步一定是 `/setup-matt-pocock-skills`，每個專案只要做一次：它會建立 `docs/agents/issue-tracker.md`，偵測到這個檔案就算通過。**沒做過 setup 的專案，軌道完全安靜**：不擋、不提示，也不附流程說明。

在專案的子資料夾開 session，算同一個專案：從那裡往上找，最近一個有 `docs/agents/issue-tracker.md` 的資料夾就是專案。每個 linked worktree 有自己的 checkout，各算一個專案，所以想同時做兩個功能，就開一個 worktree。

### 步驟怎麼往前走

每一步有四種狀態：○ 還沒開始、▶ 進行中、✔ 通過、↷ 跳過。

- **你**輸入一個步驟的指令，那一步就**進行中**；還沒有進行中的功能時，同時開始一個**功能**（setup 除外）。Claude 透過 Skill 工具跑的 skill 不會開始功能，例如 `/triage` 背後跑的 grilling。
- 進行中的那一步，要等你輸入**下一步**的指令才通過：你打下一步，就代表你說這一步定案了。
- 有兩種步驟，還要先看到東西才能往下：
  - 用本地 markdown tracker 時，「寫成規格書」要先看到 `.scratch/<功能>/spec.md`，「切成任務卡」要先看到同一個資料夾 `issues/` 裡的卡。規格寫出來後，功能就用它的資料夾名稱稱呼。用 GitHub 或 GitLab tracker 時看不到檔案，你打下一步就算。
  - 新手和進階的「動手做」，要先跑過這次的 code-review。新手的下一步就是「檢查」，所以 `/implement` 最後自己跑的那次 review，就讓動手做通過、檢查開始。
- 「動手做」只能由**你**輸入 `/implement`（高手是 `/implement-spec`）開始；Claude 自己跑會被擋下，要它停下來交棒。
- Claude 在主線透過 Skill 工具跑 skill，只有一種會讓流程往前：動手做之後的 code-review，例如 `/implement` 最後自己跑的那次。其他步驟都由你輸入才開始，前一步什麼時候定案由你決定；Claude 自己跑會被擋下，要它停下來交棒。分身（subagent）跑的不算。
- 沒有規格書的功能，用動手做時 Claude 第一個 commit 的標題稱呼。
- 「複盤」開始後，程式碼保持解鎖，讓你落實複盤建議的環境修改。改完輸入 `/matt-flow end`，功能才算完成，已完成的功能數加一；直接輸入 `/grill-with-docs` 開始下一個功能也一樣。還沒做到複盤就結束的功能是**中止**，不算完成。

### 跳步會被擋下

流程只會往下一步走。你輸入的指令越過了下一步，matt-flow 會在送出前擋下它，告訴你下一步是什麼；真的要跳過，先輸入 `/matt-flow skip`，一次跳一步。Claude 透過 Skill 工具跳步也會被擋下，並被要求停下來交棒。例如設定完直接打 `/implement`，畫面會顯示：

```
matt-flow：還沒到「動手做」。下一步是「把想法問清楚」：輸入 /grill-with-docs 加上你的想法；真的要跳過，先輸入 /matt-flow skip。
```

這幾種指令照常執行，但流程不動：進行中這一步的指令再打一次、前面步驟的指令、不在這個等級裡的步驟（動手做的指令除外：別的等級的 `/implement`、`/implement-spec` 算這個等級的動手做），以及動手做開始之前輸入的 `/mattpocock-skills:code-review`、`/pr`、`/retro`。

### 交棒

每一步開始時會跳出提示，寫明怎樣算做完和之後的指令。看得出這一步做完時，Claude 這次回覆完，下一步的指令會以灰字預填在輸入框，按 Tab 收下、再按 Enter 啟動。Claude Code 自己的建議也是灰字，晚到時會蓋掉它，所以以狀態列為準：

- setup 做完，預填 `/grill-with-docs`。
- 規格書或任務卡寫出來，預填下一步。
- 新手動手做之後 code-review 跑過，預填 `/retro`。

「把想法問清楚」和「複盤」什麼時候定案由你決定，永遠不預填；Claude 還在問你問題時（例如 `/implement` 一開始會問要測哪些地方），也不會預填。進階等級動手做時，提示會同時列出兩條路：還有卡就 `/clear` 後 `/implement` 下一張，都做好了再 `/retro`。

流程說明附在你的輸入旁邊給 Claude，寫著目前的功能、等級、進行中的步驟、下一步、哪些動作會被擋、怎麼解鎖、還能做什麼，以及交棒的規矩：你啟動的 skill 整個做完才停下來，把下一步的指令告訴你；流程的 skill 只能照順序跑；除了下一步的指令和 `/matt-flow`，不主動建議流程指令；沒有進行中的功能、或你問該怎麼辦時，可以點名 Matt 的入口（`/triage`、`/diagnosing-bugs`、`/wayfinder`、`/improve-codebase-architecture`、`/to-questionnaire`），一樣由你輸入；你輸入 `/ask-matt` 時照常回答；絕不繞過阻擋。說明只在內容變了，或它已經不在對話裡（壓縮、`/clear`、倒帶之後）才重送，不會每次輸入都附一份。

### 程式碼關卡

在動手做開始之前，Claude 對**程式碼**的 Edit、Write、NotebookEdit 都會被擋下。擋下訊息寫明下一步和解鎖用的指令（沒有進行中的功能時是 `/grill-with-docs`，否則是下一步的指令），要 Claude 停下來交棒。沒有步驟進行中時，同一個指令也會預填進輸入框；有步驟進行中時不預填，那一步什麼時候定案由你決定。

![叫 Claude 直接改也一樣：它讀到軌道就停手，提出改法，把 /implement 留給你輸入](docs/images/gate.png)

markdown 檔、`docs/`、`.scratch/` 和專案外的檔案不算程式碼，所以思考類的步驟照樣能寫詞彙表、ADR、規格和任務卡。

關卡自己出錯時（例如更新後壞了），照樣擋程式碼和 `git commit`，其他動作不受影響。擋下訊息會說怎麼退回上一版（方法二）；用方法一安裝的，照「更新、停用、移除」先停用它。這只限 matt-flow 載入之後才出錯；更新後整個載入失敗時，matt-flow 完全不作用，不擋也不提示，一樣照上面的方法退回或停用。

### commit 關卡

新手和進階：每次你輸入 `/implement` 之後，要先跑過一次 code-review（你輸入 `/mattpocock-skills:code-review`，或 Claude 透過 Skill 工具執行，例如 `/implement` 自己跑的那次），Claude 的 `git commit` 才會放行；review 之後的修正不用再 review 一次。被擋下時，`/mattpocock-skills:code-review` 會預填在輸入框。動手做以外的 commit 一律放行，那時候 Claude 改得到的只有文件。關卡只擋這個專案的 commit：每個 commit 用自己的 `git -C`、或前面的 `cd` 指到專案外面的絕對路徑時，不會被擋；用相對路徑、`~` 或變數寫的路徑，仍然算這個專案。高手不擋，`/implement-spec` 最後一步自己會 review。在新手或進階等級輸入 `/implement-spec` 時，它的分身（subagent）可以 commit 自己的任務卡，主線照樣要先 review。

### 跳過、結束、關掉

| 指令 | 作用 |
| --- | --- |
| `/matt-flow` | 打開或關閉面板 |
| `/matt-flow all` | 總覽：所有專案停在哪一步、幾天沒動，以及最近 7 天結束和中止的功能 |
| `/matt-flow skip` | 跳過擋在前面的那一步：通常是下一步；進行中的那一步還沒做完、不能往下時（例如規格書沒寫出來），跳過的是它。跳過複盤會結束功能 |
| `/matt-flow end` | 結束目前的功能：複盤進行中就算完成，還沒做到複盤就是中止 |
| `/matt-flow off` | 在這個專案關掉軌道：不擋指令、程式碼和 commit，不交棒，也不附流程說明 |
| `/matt-flow on` | 在這個專案重新打開軌道 |

每個參數都會回一行訊息，說明改了什麼、下一步是什麼。`/matt-flow` 自己的指令永遠不會被擋。

動手做途中換等級時，新等級裡到它的動手做為止還沒通過的步驟都記為跳過，流程從動手做之後接著走。

### 總覽

`/matt-flow all` 每個專案列一行：等級、功能、下一步、幾天沒動；沒有進行中的功能時，再加上已完成幾個功能。「沒動」指流程沒有往前：沒有步驟通過或跳過、沒有功能開始或結束，也沒有再輸入 `/implement` 或跑 code-review；換等級、開關軌道都不算。功能進行中、超過 3 天沒動的那一行前面加 ⚠，最久沒動的排最前面。最後一行列出最近 7 天結束的功能，以及各花了幾天、跳過了哪些步驟；有中止的功能時，再多一行把它們分開列出來。

![/matt-flow all：四個示範專案，4 天沒動的那個標 ⚠ 排在最前面，最後一行是最近 7 天結束的功能](docs/images/overview.png)

沒有進行中的功能、也沒完成過功能的專案不會列出來。總覽只看得到這台電腦上、你這個使用者的專案。

### 面板

面板用來看進度：等級按鈕、目前的功能、每個步驟的狀態（✔ 通過、▶ 進行中、↷ 跳過、○ 還沒開始）、流程所在那一步的卡片、對話用掉多少 context，以及已完成的功能數。卡片是進行中的那一步，寫著怎樣算做完和之後的指令；沒有進行中的步驟時，卡片是下一步。卡片上有兩個按鈕：`↷ 跳過「步驟」`（跟 `/matt-flow skip` 一樣，按鈕上寫著會跳過哪一步）和 `? 我卡住了`（把 `/ask-matt` 放在輸入框最前面，附上你卡在哪一步、跳過了哪些步驟、現在什麼會被擋、幾天沒動；你打到一半的字會接在後面）。在終端機裡要先按 `ctrl+x tab` 進入面板，再按 `1`（跳過）或 `2`（我卡住了）。

![面板：等級、每個步驟的狀態、進行中那一步的卡片（跳過鍵寫著會跳過哪一步）和 context 用量](docs/images/pane.png)

![按「我卡住了」：/ask-matt 連同卡在哪一步、跳過了什麼、什麼會被擋、幾天沒動，一起預填進輸入框](docs/images/stuck.png)

狀態列會一直顯示進行中的步驟和下一步的指令，不用打開面板也看得到。

升級前存的進度會延續下來：通過的步驟還是通過。0.2 版記下的步驟算通過，記下的次數算已完成的功能。0.5 版以前存的進度沒記下流程上次往前的時間，下次往前之前，總覽先用功能開始的時間代替；功能紀錄從 0.5 版開始留。

## 開發

你的電腦上會有兩份 matt-flow：

- **安裝的那份**：`~/.claude/skills/matt-flow`。每個專案都會自動載入，平常做事用的就是它。不要在裡面改程式碼，它一存檔就會套用到所有開著的 session。
- **開發的那份**：另外 clone 的 `~/matt-flow`。程式碼都在這裡改。

開 Claude Code 的方式決定這次用哪一份：

```mermaid
flowchart TD
    where["在任何一個專案<br/>的資料夾<br/>開 Claude Code"] --> how{"怎麼開？"}
    how -->|"claude"| inst["安裝的那份<br/>~/.claude/skills/<br/>matt-flow"]
    how -->|"claude --plugin-dir<br/>~/matt-flow"| devc["開發的那份<br/>~/matt-flow"]
    inst --> daily["平常做事<br/>進度照常記"]
    devc --> trial["試你改的版本<br/>只影響<br/>這個 session<br/>進度另外記"]
```

開發的那份只要 clone 一次，所有專案共用：在哪個專案的資料夾打 `claude --plugin-dir ~/matt-flow`，試的就是哪個專案，安裝的那份這次不會跑。兩份的進度分開記，開發的那份看不到你平常的進度，所以只拿來試，正式做事用安裝的那份。

整個開發流程：

```mermaid
flowchart TD
    first["只做一次<br/>clone 到<br/>~/matt-flow<br/>打開自動檢查"] --> change["改程式碼"]
    change --> trial2["用 --plugin-dir<br/>開 Claude Code 試"]
    trial2 --> good{"可以了嗎？"}
    good -->|"還不行"| change
    good -->|"可以了"| cmt["git commit<br/>會自動跑檢查"]
    cmt -->|"沒通過"| change
    cmt -->|"通過"| role{"你是？"}
    role -->|"repo 主人"| pushgh["git push<br/>到 GitHub"]
    pushgh --> deploy["部署<br/>在安裝的那份<br/>git pull<br/>所有 session<br/>立刻換成新版"]
    role -->|"別的開發者"| fork["push 到<br/>自己的 fork<br/>發 PR 回來"]
```

第一次的設定：

```bash
git clone https://github.com/kevin801221/matt-flow-mods ~/matt-flow
cd ~/matt-flow
git config core.hooksPath .githooks
claude plugin validate .
claude plugin test .
scripts/typecheck
```

`git config core.hooksPath .githooks` 每個 clone 執行一次：之後每次 commit 前都會自動跑 validate、測試和型別檢查，沒通過就不能 commit，你和 Claude 都一樣。型別檢查要先裝 Node.js（用 `npx` 跑 TypeScript），還要用到 Claude Code 的型別檔：它只在某個 session 載入過 plugin-authoring skill 之後才會出現，找不到時 `scripts/typecheck` 會說明並略過。

改了狀態怎麼載入、關卡或軌道的程式，commit 前再跑一次 `scripts/live-check`。它會在暫時的專案裡用 Haiku 實際開一次 Claude Code，檢查三件事：跳步被擋下、`/matt-flow skip` 有記下、`/clear` 之後叫 Claude 改程式碼還是被擋。結束後印出結果和截圖的資料夾，暫時的專案和它留下的進度會自動清掉。每一步都等畫面出現證據才往下，最後從對話紀錄確認真的是關卡擋下的；Claude 那次沒去改檔案的話，會說沒檢查到，請再跑一次。要先裝 VHS 和 jq（`brew install vhs jq`），沒裝就會說明並略過；每跑一次會花一次 Haiku 呼叫，所以沒有放進 pre-commit。

這個 repo 自己也用 matt-flow 管開發，所以在 clone 裡第一次叫 Claude 改程式碼會被擋下。這是正常的，照擋下訊息從流程的第一步開始就好。別的開發者沒有這個 repo 的 push 權限：先 fork，clone 自己的 fork 來改，最後發 PR 回來。

部署：先 push，再讓 skills 資料夾從 GitHub 拉新版，所有開著的 session 會立刻換成新版。先 push 是為了讓 GitHub 上一直有一份備份，不會只剩你電腦上那一份。部署前也可以先備份進度，也就是 `~/.claude/plugins/store/` 底下 `matt-flow_` 開頭的 JSON 檔。

```bash
git -C ~/matt-flow push origin main
git -C ~/.claude/skills/matt-flow pull --ff-only
```

部署之後，確認新版真的載入了、hook 沒有被其他外掛跳過。排在 matt-flow 前面的外掛，測試看不到，只有真的跑一次才知道（會花一次很小的 Haiku 呼叫）：

```bash
rm -f /tmp/matt-flow.log
cd /tmp && claude -p --debug --debug-file /tmp/matt-flow.log --model claude-haiku-5-5 "Reply with just: ok"
grep -E 'matt-flow@[^ ]* loaded|\] matt-flow: |Not loaded.*matt-flow' /tmp/matt-flow.log
```

應該只看到一行 `loaded`；其他每一行都是引擎回報的問題，例如 `bypassed by` 就是那個 hook 被排在前面的外掛跳過、沒在跑，`Not loaded` 就是這份因為名字重複沒有載入（另一種方法裝的那份在跑）。第一行先刪掉舊的紀錄，免得看到上次留下的行。想知道引擎其他的實際行為（例如外掛讀得到哪些對話內容），也可以照這個做法，用一個臨時外掛跑 `claude -p --plugin-dir <資料夾>`。

部署壞了就退回上一版：

```bash
git -C ~/.claude/skills/matt-flow reset --hard 'HEAD@{1}'
```

## 授權

MIT，見 [LICENSE](LICENSE)。這是個人做的非官方專案，跟 Matt Pocock 本人沒有關係；流程和所有 skill 都來自 [mattpocock/skills](https://github.com/mattpocock/skills)。
