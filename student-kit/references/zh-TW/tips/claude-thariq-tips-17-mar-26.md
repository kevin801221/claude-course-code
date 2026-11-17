# 打造 Claude Code 的心得：我們怎麼用 Skills —— Thariq

Thariq（[@trq212](https://x.com/trq212)）於 2026 年 3 月 17 日分享的完整指南，說明 Anthropic 內部如何使用 skills。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`tips/claude-thariq-tips-17-mar-26.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/tips/claude-thariq-tips-17-mar-26.md)

---

## 背景

Skills 已成為 Claude Code 最常用的擴充點之一。它們彈性大、好做、易散佈。但這份彈性也讓人難以判斷什麼做法最好。Thariq 分享了 Anthropic 大量使用 skills（數百個在活躍使用中）所學到的心得。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/1.png" alt="Thariq 開場推文" width="50%" /></a>

---

## 什麼是 Skills？

一個常見的誤解是 skills「只是 markdown 檔」，但最有意思的部分是它們是**資料夾**，可以包含腳本、素材、資料等 —— 代理能探索、瀏覽並操作的東西。Skills 也有各式各樣的設定選項，包括註冊動態 hook。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/2.png" alt="什麼是 Skills？" width="50%" /></a>

---

## Skills 的類型

把所有 skills 編目之後，團隊發現它們聚成 9 個反覆出現的類別。最好的 skills 乾淨地落在其中一類；比較混亂的則橫跨好幾類。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/3.png" alt="Skills 類型總覽" width="50%" /></a>

---

### 1/ 函式庫與 API 參考

說明如何正確使用某個函式庫、CLI 或 SDK 的 skills。可以是內部函式庫，也可以是 Claude Code 有時會卡住的常見函式庫。它們通常包含一個參考程式碼片段資料夾，以及寫腳本時要避開的陷阱清單。

**範例：** billing-lib、internal-platform-cli、frontend-design

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/4.png" alt="函式庫與 API 參考" width="50%" /></a>

---

### 2/ 產品驗證

描述如何測試或驗證你的程式碼能動的 skills。它們常搭配 Playwright、tmux 等外部工具。驗證型 skills 對確保 Claude 輸出正確極為有用。讓一位工程師花整整一週把驗證 skills 做到卓越，是值得的。

**範例：** signup-flow-driver、checkout-verifier、tmux-cli-driver

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/5.png" alt="產品驗證" width="50%" /></a>

---

### 3/ 資料擷取與分析

連接你的資料與監控堆疊的 skills。可能包含帶憑證抓資料的函式庫、特定儀表板 ID 等，以及常見工作流或取數方式的說明。

**範例：** funnel-query、cohort-compare、grafana

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/6.png" alt="資料擷取與分析" width="50%" /></a>

---

### 4/ 業務流程與團隊自動化

把重複工作流自動化成一個命令的 skills。它們通常指令相當簡單，但可能對其他 skills 或 MCP 有較複雜的相依。把先前結果存進日誌檔，能幫助模型保持一致並回顧該工作流的過往執行。

**範例：** standup-post、create-\<ticket-system\>-ticket、weekly-recap

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/7.png" alt="業務流程與團隊自動化" width="50%" /></a>

---

### 5/ 程式碼鷹架與範本

為 codebase 中特定功能產生框架樣板的 skills。你可能會把這類 skills 與可組合的腳本結合。當你的鷹架有無法純靠程式碼涵蓋的自然語言需求時，它們特別有用。

**範例：** new-\<framework\>-workflow、new-migration、create-app

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/8.png" alt="程式碼鷹架與範本" width="50%" /></a>

---

### 6/ 程式碼品質與審查

在你的組織內執行程式碼品質規範並協助審查的 skills。它們可以包含確定性的腳本或工具以求最大穩健性。你可能會想把這些 skills 當成 hooks 的一部分或在 GitHub Action 中自動執行。

**範例：** adversarial-review、code-style、testing-practices

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/9.png" alt="程式碼品質與審查" width="50%" /></a>

---

### 7/ CI/CD 與部署

協助你在 codebase 中擷取、推送與部署程式碼的 skills。這些 skills 可能會參照其他 skills 來蒐集資料。

**範例：** babysit-pr、deploy-\<service\>、cherry-pick-prod

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/10.png" alt="CI/CD 與部署" width="50%" /></a>

---

### 8/ Runbooks

接收一個症狀（例如一串 Slack 討論、警報或錯誤簽章），走過多工具的調查流程，並產出結構化報告的 skills。

**範例：** \<service\>-debugging、oncall-runner、log-correlator

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/11.png" alt="Runbooks" width="50%" /></a>

---

### 9/ 基礎設施維運

執行例行維護與維運程序的 skills —— 其中有些涉及破壞性動作，很適合加上護欄。它們讓工程師更容易在關鍵操作中遵循最佳實踐。

**範例：** \<resource\>-orphans、dependency-management、cost-investigation

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/12.png" alt="基礎設施維運" width="50%" /></a>

---

## 製作 Skills 的技巧

撰寫有效 skills 的 9 個最佳實踐，加上散佈與衡量的指引。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/13.png" alt="製作 Skills 的技巧總覽" width="50%" /></a>

---

### 技巧 1：不要講顯而易見的事

Claude Code 對你的 codebase 知道很多，Claude 對寫程式也知道很多，包括許多預設意見。如果你要發佈的 skill 主要是知識型的，試著聚焦在能把 Claude 推離它慣常思路的資訊。前端設計 skill 就是個好例子 —— 它是透過與客戶反覆迭代、改善 Claude 的設計品味而建立的，避開了 Inter 字體與紫色漸層這類老套模式。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/14.png" alt="不要講顯而易見的事" width="50%" /></a>

---

### 技巧 2：建立一個 Gotchas（陷阱）段落

任何 skill 中訊號最強的內容就是 Gotchas 段落。這些段落應該從 Claude 使用你的 skill 時常碰到的失敗點累積起來。理想上，你會隨時間更新 skill 來收錄這些陷阱。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/15.png" alt="建立 Gotchas 段落" width="50%" /></a>

---

### 技巧 3：善用檔案系統與漸進式揭露

一個 skill 是資料夾，不只是一個 markdown 檔。你該把整個檔案系統視為一種脈絡工程與漸進式揭露的形式。告訴 Claude 你的 skill 裡有哪些檔案，它就會在適當時機讀取。最簡單的形式是指向其他 markdown 檔 —— 例如把詳細的函式簽章與使用範例拆到 `references/api.md`。你可以有整個資料夾的參考、腳本、範例等。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/16.png" alt="漸進式揭露" width="50%" /></a>

---

### 技巧 4：不要把 Claude 綁死在軌道上

Claude 通常會盡力遵守你的指令，而正因為 skills 重複使用性高，你要小心不要寫得太過具體。給 Claude 它需要的資訊，但也給它因應情況調整的彈性。與其給規定式的逐步指令，不如給出目標與限制。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/17.png" alt="不要把 Claude 綁死" width="50%" /></a>

---

### 技巧 5：想清楚設定流程

有些 skills 可能需要使用者提供脈絡來完成設定。一個好模式是把這些設定資訊存在 skill 目錄下的 `config.json`。若 config 尚未設定，代理就能向使用者詢問資訊。你可以指示 Claude 用 AskUserQuestion 工具做結構化的多選題。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/18.png" alt="想清楚設定流程" width="50%" /></a>

---

### 技巧 6：description 欄位是寫給模型看的

Claude Code 啟動 session 時，會建立一份列出每個可用 skill 與其 description 的清單。Claude 就是掃這份清單來決定「這個請求有對應的 skill 嗎？」。這表示 description 欄位不是摘要 —— 它是**何時該觸發**這個 skill 的描述。要為模型而寫。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/19.png" alt="Description = 觸發條件" width="50%" /></a>

---

### 技巧 7：記憶與資料儲存

有些 skills 可以藉由在自身內部儲存資料而具備某種記憶。你可以用簡單如只追加的文字日誌檔或 JSON 檔，也可以複雜到用 SQLite 資料庫。存在 skill 目錄下的資料在你升級 skill 時可能被刪除，所以請用 `${CLAUDE_PLUGIN_DATA}` 作為每個外掛的穩定資料夾來存資料。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/20.png" alt="記憶與資料儲存" width="50%" /></a>

---

### 技巧 8：儲存腳本並產生程式碼

你能給 Claude 最強大的工具之一就是程式碼。給 Claude 腳本與函式庫，讓它把回合花在「組合」上 —— 決定接下來做什麼，而不是重建樣板。Claude 接著就能即時產生腳本來組合這些功能，做更進階的分析。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/21.png" alt="儲存腳本並產生程式碼" width="50%" /></a>

---

### 技巧 9：按需 Hooks

Skills 可以包含只在該 skill 被呼叫時才啟用、並持續到 session 結束的 hooks。把這用在那些你不想一直執行、但有時極其有用的、意見較強的 hooks 上。

**範例：**
- `/careful` —— 透過 Bash 的 PreToolUse matcher 封鎖 rm -rf、DROP TABLE、force-push、kubectl delete
- `/freeze` —— 封鎖任何不在特定目錄內的 Edit/Write

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/22.png" alt="按需 Hooks" width="50%" /></a>

---

## 散佈 Skills

與團隊分享 skills 的兩種方式：
- **Commit 進你的 repo**（放在 `.claude/skills` 底下）—— 最適合橫跨少數 repo 的小團隊
- **做成外掛**，並建立 Claude Code 外掛市集讓使用者上傳與安裝

每個 commit 進去的 skill 都會為模型的脈絡增加一點負擔。隨著規模擴大，內部外掛市集讓你能散佈 skills，並讓團隊自行決定要裝哪些。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/23.png" alt="散佈 Skills" width="50%" /></a>

---

## 管理市集

沒有一個中央團隊決定哪些 skills 可以進市集。相反地，試著有機地找出最有用的 skills。先上傳到 GitHub 的沙箱資料夾，在 Slack 或其他論壇指引大家去看。一旦某個 skill 獲得關注（由 skill 擁有者判定），他們就能提 PR 把它搬進市集。釋出前的策展很重要，能避免重複的 skills。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/24.png" alt="管理市集" width="50%" /></a>

---

## 組合 Skills

你可能會想讓 skills 互相依賴。例如一個上傳檔案的 skill，以及一個產生 CSV 後上傳它的 CSV 生成 skill。這種相依管理目前還沒原生內建進市集或 skills，但你可以直接用名稱參照其他 skills，只要它們已安裝，模型就會呼叫它們。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/25.png" alt="組合 Skills" width="50%" /></a>

---

## 衡量 Skills

要了解一個 skill 表現如何，可用 PreToolUse hook 在公司內記錄 skill 使用狀況。這樣你就能找出受歡迎的 skills，或是觸發率低於預期的 skills。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/26.png" alt="衡量 Skills" width="50%" /></a>

---

## 結論

Skills 是給代理用的、極其強大且彈性的工具，但現在還很早期，大家都還在摸索怎麼用得最好。把這篇當成「我們看過有效的實用技巧雜燴」，而非權威指南。理解 skills 最好的方式是開始動手、實驗，看什麼適合你。我們大多數的 skills 一開始只有幾行字和一個陷阱，之後因為大家在 Claude 碰到新的邊界情況時持續往裡面加東西而變好。

<a href="https://x.com/trq212/status/2033949937936085378"><img src="../tips/assets/thariq-26-3-17/27.png" alt="結論" width="50%" /></a>

---

## 資料來源

- [Thariq (@trq212) on X — 2026 年 3 月 17 日](https://x.com/trq212/status/2033949937936085378)
- [Skilljar — Agent Skills course](https://code.claude.com/docs/en/skills)
- [Skill Creator](https://code.claude.com/docs/en/skills)
