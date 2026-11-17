# 學生導讀：讓流程有狀態、有驗收、有交棒

對應講義 Part 14「Plugins / Mods＋Lab」，也能回看 Part 11 的人與代理分工、Part 12 的傳統 Hooks、Part 19 的可驗收成果。

## 先知道這份原碼的適用條件

來源 README 表示作者使用 Claude Code `2.1.312` 以後的版本，並只在 macOS 使用過。這是來源快照的環境紀錄，不代表已在每一版 CLI 或所有作業系統驗證。講義與本機 CLI 的功能可能不同；老師示範前必須檢查實際 CLI 是否提供 Mods，以及 `claude plugin test` 等子命令。

`hooks/register.tsx` 從 `claude-code` 匯入 `atom`、`read`、`update` 與引擎型別，測試從 `claude-code/testing` 匯入測試工具。這些由支援 Mods 的引擎供應；本資料夾沒有一般 npm 專案的 `package.json`。請勿為了讓 import 通過，隨意安裝同名 npm 套件。

matt-flow 只負責導航與把關，沒有收錄 `/grill-with-docs`、`/implement` 等 Skills。本機要跑完整流程，還需另外具有對應的 `mattpocock-skills` 外掛。沒有這個依賴時，可以閱讀原碼與測試設計，不能把面板出現視為完整流程已可運作。

## 把 1,030 行原碼拆成五段讀

| 先讀什麼 | 原碼位置 | 要回答的問題 |
| --- | --- | --- |
| 資料模型 | [types/index.d.ts](types/index.d.ts)、`STEPS`、`LEVELS`、`FRESH` | 哪些資料屬於功能，哪些屬於專案？ |
| 狀態推進 | `stateOf`、`nextStep`、`underWay`、`judge`、`moveOnto`、`noteRan` | 誰有權開始下一步？開始與通過差在哪？ |
| 驗收證據 | `artifacts`、`holdOf`、`checkArtifacts` | 規格與任務卡何時真的算寫出來？ |
| 動作關卡 | `codeGate`、`commitGate`、`isElsewhere` | 哪些工具動作會被攔下，哪些會通過？ |
| 引擎整合 | `register`、`railPrompt`、`revive`、`reread` | 訊息、狀態保存、面板如何接在一起？ |

在編輯器搜尋以上函式名稱即可定位；完整原碼在 [hooks/register.tsx](hooks/register.tsx)。對照 [hooks/register.test.tsx](hooks/register.test.tsx) 的英文測試名稱，可以直接找到每條規則的範例。

## 三種學習路徑

| 等級 | 內部 step keys | 你會看到的操作 |
| --- | --- | --- |
| 新手 | `setup → grill → build → review → retro` | 問清楚、做一個小功能、檢查、複盤 |
| 進階 | `setup → grill → spec → tickets → build → retro` | 先有規格與任務卡，再逐張實作 |
| 高手 | `setup → grill → spec → tickets → parallel → pr → retro` | 讓代理平行實作，最後整理 PR 與複盤 |

`setup` 每個專案只做一次，以 `docs/agents/issue-tracker.md` 是否存在判斷。還沒 setup 的專案保持安靜，不攔截也不注入流程。專案根目錄從工作目錄往上找最近的 setup 檔；linked worktree 各自具有 checkout，因此各自記進度。

每一步的畫面狀態有四種：未開始、`underWay`、`passed`、`skipped`。資料中「未開始」是沒有 key，不是第四個字串值。人輸入某一步的指令，該步才進入 `underWay`；人輸入下一步時，前一步才通過。這讓「AI 說寫完」和「人決定定案」分開。

在本地 Markdown tracker 模式，`spec` 要看到這次功能開始之後修改的 `.scratch/<功能>/spec.md`，`tickets` 要看到同一功能資料夾內的 `issues/*.md`。來源引擎只提供修改時間，原碼因此用 `mtimeMs`，不能把它誤認成檔案建立時間。GitHub/GitLab tracker 沒有同樣的本地檔案證據，改由人輸入下一步定案。

## 兩道關卡與一個人為交棒

1. `codeGate`：還沒進入 `build` 或 `parallel` 時，攔截專案程式碼的 `Edit`、`Write`、`NotebookEdit`。Markdown、`docs/`、`.scratch/` 與專案外檔案可寫，讓需求與規格工作先進行。
2. `commitGate`：新手與進階在每次人輸入實作指令後，要先跑一次主線 code-review 才能由 Claude commit。高手不使用這道 commit 關卡；有特定平行實作狀態的 subagent 可以提交任務卡。
3. `judge`：實作必須由人輸入指令啟動。AI 透過 Skill 工具自行跳到實作或其他下一步時，會收到拒絕與交棒訊息。主線實作後執行 code-review 是例外；subagent 的 review 不會解鎖主線 commit。

這些是使用者自訂的流程護欄。來源明列 Bash 寫檔可繞過程式碼關卡，Git alias 與複雜 shell 語法也不是完整語法分析；不要拿它替代作業系統沙箱或 CLI 權限規則。程式保留了這些限制的註解，方便上課討論。

## skip、end、off 與 reset 的差別

| 操作 | 實際語義 |
| --- | --- |
| `/matt-flow skip` | 跳過下一個擋住流程的步驟；若目前步驟缺成果而不能離開，就跳過目前步驟。 |
| `/matt-flow end` | 結束目前功能；複盤已開始算完成，否則記為中止。 |
| `/matt-flow off` / `on` | 關閉或恢復此專案軌道，保留既有進度。 |
| `/clear` | 清對話與 session state；`revive` 重新讀取持久進度，關卡不應因此解除。 |
| 結束功能後的重置 | `finish` 清空本次 steps、feature、review 狀態，保留 setup、歷史紀錄及完成數。 |

此版本沒有 `/matt-flow reset` 指令。跳過尚未開始的複盤會中止功能；複盤已進行中再跳過，才按完成結束。不要把 `skip` 理解成「做完這步」。

`save` 將狀態存到引擎 store 的 `progress:<project root>`。`restore` 也負責舊版資料的遷移；`reread` 在動作前重新讀，減少多 session 的陳舊狀態。不過來源註解指出 store 沒有 compare-and-set，多 session 同時存檔仍可能遺失更新。

`railPrompt` 把目前位置、下一步及解鎖條件附在 prompt context；`sent` 與 `seen` 避免每回合重送相同內容，又在 compact、rewind 或 clear 之後補送。這是 Context Engineering 如何落在實際程式裡的例子。

## 這份快照實際驗證到哪裡

本包已檢查 JSON 可解析、shell 腳本語法有效、逐檔內容與來源快照一致；另外在 macOS 上，以 Claude Code `2.1.319` 實際執行原測試，結果 **76 pass / 0 fail**，約 1.96 秒。

在精華包根目錄可使用 macOS/Linux/WSL 適用的暫存目錄重跑：

```sh
CLAUDE_CONFIG_DIR="$(mktemp -d)" claude plugin test advanced/matt-flow-mods
```

此測試使用隔離的 Claude 設定目錄，沒有開互動 session、呼叫模型或變更使用者的 history／trust。測試透過 `claude-code/testing` 與原測試內的模擬引擎事件檢查狀態轉移、關卡和 UI 事件輸出；**未驗證真人操作的實際 UI、完整 TypeScript 型別編譯，或與外部 `mattpocock-skills` 的完整互動**。它也沒有執行 `scripts/live-check`。其他 CLI 版本仍需自行確認是否提供這個測試子命令。

要自行重做最基本的 shell 檢查，在本資料夾執行：

```sh
sh -n scripts/typecheck
sh -n scripts/live-check
sh -n .githooks/pre-commit
```

原測試有 76 個 `test(...)` 宣告（部分會迭代多個介面）。先挑這幾組讀，畫出事件前後的 `Progress`：

- `a step the person types is under way, not passed...`：輸入指令與通過步驟。
- `on the local tracker, spec and tickets wait for their files...`：成果檔案驗收。
- `a beginner building cannot commit until code-review runs...`：commit 關卡。
- `after /clear, the next tool call or prompt finds the project again...`：對話重置後的恢復。
- `a subagent running code-review does not unlock the commit`：主線與分身界線。

## 課堂重跑與真實互動驗收

本包的 76 個原測試已在上述版本通過。學生重跑前，先從本機 `claude --help`、`claude plugin --help` 與該版本的官方 Mods 文件確認指令存在，再於精華包根目錄執行上面的隔離設定命令。來源另有 `claude plugin validate .`，需從本 Mods 資料夾執行；不要把 test 通過當成 validate 或完整型別編譯也已執行。看到不支援子命令或找不到 `claude-code/testing` 時，記錄版本與錯誤，改做原碼推演。

| 原腳本 | 真正需要什麼 | 判讀限制 |
| --- | --- | --- |
| [scripts/typecheck](scripts/typecheck) | Node.js/npx、TypeScript `5.6.3`；`/tmp/claude-*/bundled-skills/*/*/plugin-authoring/types/claude-code.d.ts` | 型別來自某個 session 載入的 plugin-authoring skill。找不到就印 `skipped` 並退出 0；退出 0 不等於型別檢查通過。腳本會用 npx 取套件。 |
| [scripts/live-check](scripts/live-check) | 相容 Claude CLI、已登入帳號、VHS、jq，以及可用的指定 Haiku 模型 | 真的啟動 session、使用 `acceptEdits` 並產生模型費用；會寫入使用者的信任與 history 設定，不屬於離線檢查。模型 ID 依來源固定，可能不可用。缺工具亦會印 `skipped`、退出 0。 |
| [.githooks/pre-commit](.githooks/pre-commit) | 已支援 validate/test 的 CLI，加上上列型別環境 | 原始腳本附作閱讀，不會替你設定 `core.hooksPath`。它檢查 working tree，而非僅 staged 內容。 |

`live-check` 驗證跳步被拒絕、skip 有保存、`/clear` 後仍擋寫檔。它會清理臨時專案、該路徑的 transcripts 與新增 store 檔，但來源註解明說信任答案和全域 history 可能留下紀錄。測試輸出 `FAIL: not checked` 表示 Claude 沒嘗試觸發關卡，不能算關卡已經驗證。

課堂驗收應記下「CLI 版本、實際命令、輸出、觀察到的狀態變化」。只完成原碼推演時，請在作業寫「靜態驗證」；重跑 `plugin test` 時寫「引擎測試工具驗證」；真人操作 UI 或 live-check 另記實際證據，讓驗證範圍清楚。
