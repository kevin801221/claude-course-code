<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-code-tutorial-logo-dark.svg">
  <img alt="Claude Code 完整教學" src="../resources/logos/claude-code-tutorial-logo.svg">
</picture>

# 進階功能

完整說明 Claude Code 的進階功能，涵蓋規劃模式（Planning Mode）、延伸思考（Extended Thinking）、自動模式、背景任務、權限模式、Print 模式（非互動式）、工作階段（session）管理、互動功能、頻道、語音輸入、遠端控制、網頁工作階段、桌面應用程式、任務清單、提示詞建議、Git worktree、沙箱、受管設定與設定選項。

## 目錄

1. [總覽](#總覽)
2. [規劃模式](#規劃模式)
3. [延伸思考](#延伸思考)
4. [自動模式](#自動模式)
5. [背景任務](#背景任務)
6. [Monitor 工具（事件驅動串流）](#monitor-工具事件驅動串流)
7. [動態工作流程](#動態工作流程)
8. [排程任務](#排程任務)
9. [權限模式](#權限模式)
10. [無介面模式（headless）](#無介面模式headless)
11. [工作階段管理](#工作階段管理)
12. [跨工作階段訊息](#跨工作階段訊息)
13. [互動功能](#互動功能)
14. [輸出樣式](#輸出樣式)
15. [狀態列](#狀態列)
16. [TUI 模式（全螢幕）](#tui-模式全螢幕)
17. [語音輸入](#語音輸入)
18. [頻道](#頻道)
19. [Chrome 整合](#chrome-整合)
20. [遠端控制](#遠端控制)
21. [網頁工作階段](#網頁工作階段)
22. [桌面應用程式](#桌面應用程式)
23. [任務清單](#任務清單)
24. [提示詞建議](#提示詞建議)
25. [Git Worktree](#git-worktree)
26. [沙箱](#沙箱)
27. [受管設定（企業版）](#受管設定企業版)
28. [設定與組態](#設定與組態)
29. [信任與權限範圍](#信任與權限範圍)
30. [代理團隊](#代理團隊)
31. [最佳實踐](#最佳實踐)
32. [延伸資源](#延伸資源)

---

## 總覽

Claude Code 的進階功能，以規劃、推理、自動化與控制機制擴充了核心能力。這些功能能為複雜的開發任務、程式碼審查、自動化與多工作階段管理，帶來精細的工作流程。

**主要進階功能包括：**
- **規劃模式**：在撰寫程式碼前建立詳細的實作計畫
- **延伸思考**：針對複雜問題進行深度推理
- **自動模式**：背景安全分類器會在執行前審查每個動作
- **背景任務**：在不阻塞對話的情況下執行長時間作業
- **權限模式**：控制 Claude 能做什麼（`manual` — 前身為 `default`、`acceptEdits`、`plan`、`auto`、`dontAsk`、`bypassPermissions`）
- **Print 模式**：以非互動方式執行 Claude Code，用於自動化與 CI/CD（`claude -p`）
- **工作階段管理**：管理多個工作階段
- **互動功能**：鍵盤快捷鍵、多行輸入與指令歷史
- **語音輸入**：支援按住說話的語音輸入，涵蓋 20 種語言的語音辨識（STT）
- **頻道**：MCP 伺服器可將訊息推播到執行中的工作階段（研究預覽）
- **遠端控制**：從 Claude.ai 或 Claude 應用程式控制 Claude Code
- **網頁工作階段**：在瀏覽器的 claude.ai/code 執行 Claude Code
- **桌面應用程式**：獨立應用程式，可視覺化檢視差異並管理多個工作階段
- **任務清單**：跨上下文壓縮（compact）仍能持續追蹤的任務清單
- **提示詞建議**：根據上下文提供智慧指令建議
- **Git Worktree**：以隔離的 worktree 分支進行平行作業
- **沙箱**：作業系統層級的檔案系統與網路隔離
- **受管設定**：透過 plist、登錄檔（Registry）或受管檔案進行企業部署
- **設定**：透過 JSON 設定檔自訂行為

---

## 規劃模式

規劃模式讓 Claude 在實作複雜任務前先充分思考，建立一份你可以審閱並核准的詳細計畫。

### 什麼是規劃模式？

規劃模式是一套兩階段的做法：
1. **規劃階段**：Claude 分析任務並建立詳細的實作計畫
2. **實作階段**：核准後，Claude 執行該計畫

### 何時該使用規劃模式

✅ 適合使用規劃模式的情境：
- 複雜的多檔案重構
- 新功能的實作
- 架構變更
- 資料庫遷移
- 大型 API 重新設計

❌ 不適合使用規劃模式的情境：
- 簡單的錯誤修正
- 格式調整
- 單一檔案的編輯
- 快速查詢

### 啟用規劃模式

**斜線指令（Slash Commands）**：
```bash
/plan 實作使用者驗證系統
```

**CLI 旗標**：
```bash
claude --permission-mode plan
```

**設為預設值**：
```json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

**鍵盤快捷鍵**：
- `Shift + Tab` - 切換權限模式（包含規劃模式）
- `Alt + M` - 切換權限模式（Windows/Linux）

### 規劃模式的好處

- **結構化的實作方式**：詳細拆解實作步驟
- **審閱與核准**：在執行前核准或調整計畫
- **風險識別**：在實作前找出潛在問題
- **清楚的階段劃分**：有條理的實作階段與里程碑

### 範例：功能實作

```
User: /plan 新增即時通知系統

Claude: 我會建立一個實作即時通知功能的計畫。

## 實作計畫

### 第一階段：基礎架構設定
1. 安裝 WebSocket 函式庫（socket.io）
2. 設定 WebSocket 伺服器
3. 設定連線管理

### 第二階段：後端實作
4. 建立通知服務
5. 實作通知佇列
6. 新增通知的資料庫結構
7. 建立 API 端點

### 第三階段：前端整合
8. 設定 WebSocket 客戶端
9. 建立通知 UI 元件
10. 實作通知狀態管理
11. 新增通知權限

### 第四階段：測試與部署
12. 撰寫單元測試
13. 撰寫整合測試
14. 更新文件
15. 部署到預備環境

預估時間：3-4 小時
需修改的檔案數：12
需新增的檔案數：8

要繼續嗎？（yes/no/modify plan）

User: yes

Claude: [依計畫開始實作]
```

### 計畫修改

```
User: 修改一下計畫，先跳過佇列，我們之後再加

Claude: 更新後的計畫：
[顯示已移除佇列的修改後計畫]

User: 很好，繼續

Claude: [實作修改後的計畫]
```

### 規劃模式設定

規劃模式可透過 CLI 旗標或斜線指令啟用：

```bash
# 透過 CLI 啟用規劃模式
claude --permission-mode plan

# 或在 REPL 中使用 /plan 斜線指令
/plan 實作使用者驗證系統
```

**規劃用的模型別名**：使用模型別名 `opusplan`，規劃階段用 Opus、執行階段用 Sonnet：

```bash
claude --model opusplan "設計並實作新的 API"
```

**在外部編輯計畫**：按下 `Ctrl+G` 即可在外部編輯器中開啟目前的計畫，進行詳細修改。

> **v2.1.112 更新**：計畫檔案現在會以產生它的提示詞命名（而非隨機單字），更方便瀏覽與重複使用。

> **v2.1.136 更新 — 規劃模式的寫入封鎖為無條件**：規劃模式現在會封鎖所有檔案寫入，即使 `permissions.allow` 中有相符的 `Edit(...)` 規則也一樣。過去寬鬆的 `Edit(...)` 規則可能讓寫入在規劃模式下通過；這個漏洞已經修補。如果你的工作流程仰賴舊行為，請先離開規劃模式（`Shift+Tab`）再進行編輯。

---

## 延伸思考

延伸思考讓 Claude 在提供解法之前，能花更多時間思考複雜的問題。

### 什麼是延伸思考？

延伸思考是一套刻意、逐步進行的推理流程，Claude 會：
- 拆解複雜的問題
- 考量多種做法
- 評估各種取捨
- 針對邊界情況進行推理

### 啟用延伸思考

**鍵盤快捷鍵**：
- `Option + T`（macOS）/ `Alt + T`（Windows/Linux）- 切換延伸思考

**自動啟用**：
- 所有模型（Opus 5、Opus 4.8、Opus 4.7、Sonnet 4.6、Haiku 4.5）預設皆啟用
- Opus 5 / Opus 4.8：自適應推理，effort 等級分為 `low`（○）、`medium`（◐）、`high`（●）、`xhigh`、`max`。Opus 5（v2.1.219）、Opus 4.8（v2.1.154）、Opus 4.6 與 Sonnet 4.6 的預設值為 `high`，Opus 4.7 的預設值為 `xhigh`。`xhigh` 可用於 Opus 5、Opus 4.8 與 Opus 4.7（在 Opus 4.6 / Sonnet 4.6 上會退回 `high`）。`max` 可用於 Opus 5、Opus 4.8/4.7/4.6 與 Sonnet 4.6（僅限當次工作階段）。Haiku 4.5 沒有 effort 等級。Opus 5、Opus 4.8 與 Opus 4.7 具備原生 1M token 的上下文視窗（1M 上下文的修正在 v2.1.117 推出 — 在此之前，`/context` 會以 200K 視窗誤算 Opus 4.7 的用量，導致過早觸發自動壓縮）。自 v2.1.129 起，`/context` 只會在畫面上顯示視覺化結果；ASCII 視覺化不再流入對話上下文（每次呼叫可省下約 1,600 個 token），因此可以放心隨時呼叫 `/context`。
- Opus 4.6 / Sonnet 4.6 上的 Pro/Max 訂閱者：預設 effort 在 v2.1.117 從 `medium` 提高為 `high`。
- 其他模型：固定預算，最高 31,999 個 token

**設定方式**：
- 切換：`Alt+T` / `Option+T`，或透過 `/config`
- 檢視推理過程：`Ctrl+O`（詳細模式）
- 設定 effort：使用 `/effort` 指令或 `--effort` 旗標

**自訂預算**：
```bash
export MAX_THINKING_TOKENS=1024
```

**Effort 等級**（支援 Opus 5、Opus 4.8、Opus 4.7、Opus 4.6 與 Sonnet 4.6 — Haiku 4.5 不支援）：
```bash
export CLAUDE_CODE_EFFORT_LEVEL=high   # low（○）、medium（◐）、high（●）、xhigh（Opus 5/4.8/4.7）或 max — Opus 5 與 Opus 4.8 的預設值為 high
```

**CLI 旗標**：
```bash
claude --effort high "複雜的架構審查"
```

**斜線指令**：
```
/effort high
```

> **備註：** 在提示詞中使用關鍵字「ultrathink」可啟用深度推理模式。effort 等級 `low`、`medium`、`high` 與 `max` 支援 Opus 5、Opus 4.8、Opus 4.7、Opus 4.6 與 Sonnet 4.6（Haiku 4.5 沒有）。`xhigh` 則可用於 Opus 5、Opus 4.8 與 Opus 4.7。Opus 5、Opus 4.8（以及 Opus 4.6 / Sonnet 4.6）的預設 effort 為 `high`，Opus 4.7 的預設值為 `xhigh`。Opus 4.8 與 Opus 4.7 會在第一次執行時固定其預設 effort，Opus 5 則沒有這個限制 — 你先前設定的等級會延續下去。`/effort` 選單還提供 `ultracode` 選項，這**不是**模型的 effort 等級 — 它會送出 `xhigh`，並讓 Claude 協調動態工作流程（僅限當次工作階段）。

### Opus 5 的安全分類器備援

與處理過載和無法使用情況的 [`fallbackModel` 設定](#備援模型fallbackmodel) 不同，Claude Code 在安全分類器標記某個請求時，會套用**依類別分類的備援機制**。此功能需要 Claude Code v2.1.219 以上版本。

- **Opus 5**：被標記為網路安全相關的請求，會在 Opus 4.8 上重新執行。被標記為生物相關的請求則會直接以拒絕回應收場，因為 Opus 5 使用自己的生物分類器，沒有備援模型。從第一次被標記的請求開始，你就會收到這類拒絕回應。
- 攻擊性資安或生物相關的工作 — 滲透測試、CTF（Capture the Flag）演練，以及與生物學相關的程式碼庫 — 經常會觸發備援機制，通常在第一次請求時就會發生。

這點之所以重要：如果你在 Opus 5 上執行 [security-review 子代理（Subagents）](../04-subagents/README.md) 或進行 CTF／滲透測試工作，網路安全相關的提示詞會在你不知情的情況下重新在 Opus 4.8 上執行（effort 上限與上下文視窗都不同），而生物相關的提示詞則會直接被拒絕。如果這樣的行為造成困擾，可以明確指定使用其他模型。

**控制切換行為** — `switchModelsOnFlag` 設定（v2.1.170 以上，預設為 `true`）決定備援是否會在不知情的情況下自動發生。將它設為 `false`，Claude Code 就會改為暫停，讓你選擇要切換模型還是修改提示詞。此選項在 `/config` 中顯示為 **Switch models when a message is flagged**。

```json
{
  "switchModelsOnFlag": false
}
```

### 延伸思考的好處

- **深度推理**：花更多時間思考複雜的問題
- **更好的架構決策**：透過全面評估做出有根據的選擇
- **考量邊界情況**：全面思考潛在的問題與情境
- **徹底的分析**：以結構化的方式解決複雜問題

### 範例：架構決策

```
User: ultrathink 我們的電商平台應該用微服務還是單體架構？

Claude: 讓我仔細思考這個架構決策……

<extended_thinking>
## 上下文分析
- 團隊規模：5 名開發者
- 預期流量：初期每天 1 萬使用者
- 需要擴展到 10 萬以上使用者
- DevOps 資源有限
- MVP 時程為 6 個月

## 方案一：微服務
優點：
+ 可獨立擴展
+ 技術選型彈性
+ 團隊獨立作業
+ 故障隔離

缺點：
- 維運複雜度高
- 網路額外開銷
- 需要分散式追蹤
- 需要 DevOps 專業能力
- 初期開發較慢

## 方案二：單體架構
優點：
+ 部署較簡單
+ 初期開發較快
+ 除錯較容易
+ 維運開銷較低
+ 單一程式碼庫

缺點：
- 之後擴展較困難
- 部署是全有或全無
- 技術選型被鎖定
- 可能出現緊密耦合

## 決策因素
1. 團隊規模（5 人）→ 偏向單體架構
2. DevOps 資源（有限）→ 偏向單體架構
3. 時程（6 個月）→ 偏向單體架構
4. 未來規模（10 萬使用者）→ 單體架構加快取即可達成
5. 複雜度預算 → 有限

## 建議
先從**模組化單體架構**開始：
- 單一部署單元
- 清楚的模組邊界
- 模組之間介面乾淨
- 為日後視需要拆分成微服務預做準備

這樣做能帶來：
✓ 快速的初期開發
✓ 較低的維運複雜度
✓ 之後仍可拆分服務
✓ 清楚的架構

遷移路徑：當你的使用者達到 5 萬以上，或特定模組需要獨立擴展時，再把那些模組拆分成微服務。
</extended_thinking>

**建議**：採用模組化單體架構，模組邊界要乾淨明確。

這個做法在你目前的限制（團隊規模、時程、DevOps 資源）與未來的可擴展性需求之間取得平衡。之後若有明確的業務需求，你可以再把特定模組遷移到微服務。
```

### 延伸思考設定

延伸思考可透過環境變數、鍵盤快捷鍵與 CLI 旗標控制：

```bash
# 設定思考 token 預算
export MAX_THINKING_TOKENS=16000

# 設定 effort 等級（Opus 5、Opus 4.8、Opus 4.7、Opus 4.6、Sonnet 4.6）：low（○）、medium（◐）、high（●）、xhigh（Opus 5/4.8/4.7）或 max — Opus 5 與 Opus 4.8 的預設值為 high
export CLAUDE_CODE_EFFORT_LEVEL=high
```

在工作階段中可用 `Alt+T` / `Option+T` 切換，用 `/effort` 設定 effort 等級，或透過 `/config` 進行設定。

> **精簡系統提示詞（v2.1.154）：** 除了 Haiku、Sonnet，以及 Opus 4.7 以前（含）的版本外，精簡系統提示詞現在是所有模型的**預設值**，可降低 Opus 5 與 Opus 4.8 的基礎 token 開銷。

---

## 自動模式

自動模式是一種權限模式，會用背景安全分類器在每個動作執行前先進行審查。它讓 Claude 能自主運作，同時封鎖危險的操作。所有方案皆可使用，但需要符合資格的模型（在 Anthropic API 與 AWS 上的 Claude Platform 為 Claude Opus 5、Opus 4.6 以上、Sonnet 4.6 以上，或 Fable 5；在 Bedrock、Vertex、Foundry，以及已登入的 Claude 應用程式閘道工作階段為 Opus 5、Sonnet 5、Opus 4.7、Opus 4.8，或 Fable 5）。在 Team 與 Enterprise 方案上預設為開啟 — 管理員可在受管設定中為整個組織關閉此功能。

### 需求

自動模式僅在你的帳號符合以下所有條件時才可使用：

- **方案**：所有方案皆適用。
- **組織**：在 Team 與 Enterprise 方案上，自動模式預設為可用。管理員可在受管設定中將 `permissions.disableAutoMode` 設為 `"disable"`，藉此為整個組織關閉此功能。
- **模型**：在 Anthropic API 與 AWS 上的 Claude Platform — Claude Opus 4.6 以上版本（含 Opus 5）、Sonnet 4.6 以上版本，或 Fable 5。在 Amazon Bedrock、Google Cloud 的 Agent Platform（Vertex AI）、Microsoft Foundry，以及已登入的 Claude 應用程式閘道工作階段 — 僅支援 Claude Sonnet 5、Opus 4.7 以上版本（含 Opus 5），以及 Fable 5。較舊的模型 — Sonnet 4.5、Opus 4.5、Haiku 與 claude-3 系列模型 — 在任何供應商上都不支援。
- **供應商**：在 Anthropic API、AWS 上的 Claude Platform、Amazon Bedrock、Google Cloud 的 Agent Platform（Vertex AI）、Microsoft Foundry，以及已登入的 Claude 應用程式閘道工作階段上，預設皆可使用。在 v2.1.158 到 v2.1.206 之間，除了 Anthropic API 與 AWS 上的 Claude Platform 外，其餘皆須設定 `CLAUDE_CODE_ENABLE_AUTO_MODE=1` 才會開啟自動模式；v2.1.207 移除了這項限制。該環境變數仍可設定以維持相容性，但自 v2.1.207 起已無作用。
- **分類器**：以 Claude Sonnet 4.6 執行（會產生額外的 token 費用）

### 啟用自動模式

```bash
# 用 CLI 旗標解鎖自動模式（Max 訂閱者在 Opus 4.7 上已不再需要 — 可直接使用）
claude --enable-auto-mode

# 接著在 REPL 中用 Shift+Tab 切換過去
```

> **v2.1.112 更新**：自動模式不再需要 `--enable-auto-mode` 旗標。Max 訂閱者在 Opus 4.7 上可直接使用。

> **v2.1.158 更新**：自動模式在 Bedrock、Vertex 與 Foundry 上開放給 Opus 4.7/4.8 使用，但須設定 `CLAUDE_CODE_ENABLE_AUTO_MODE=1` 才能開啟。
>
> **v2.1.207 更新**：移除了上述的選擇加入（opt-in）限制。自動模式現在對 Claude Sonnet 5、Opus 4.7、Opus 4.8 與 Fable 5（自 v2.1.219 起也包含 Opus 5）在 Bedrock、Vertex AI、Microsoft Foundry，以及已登入的 Claude 應用程式閘道工作階段上預設可用 — 不需要旗標或環境變數。管理員可在受管設定中用 `disableAutoMode` 停用此功能。`CLAUDE_CODE_ENABLE_AUTO_MODE` 仍可設定以維持相容性，但自 v2.1.207 起已無作用。

或將它設為預設權限模式：

```bash
claude --permission-mode auto
```

透過設定檔設定：
```json
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

### 分類器如何運作

背景分類器會依以下判斷順序評估每個動作：

1. **允許／拒絕規則** — 先檢查明確的權限規則
2. **唯讀／編輯自動核准** — 檔案讀取與編輯會自動放行
3. **分類器** — 背景分類器審查該動作
4. **回退機制** — 連續 3 次或累計 20 次被封鎖後，改回詢問使用者

### 預設封鎖的動作

自動模式預設會封鎖以下動作：

| 封鎖的動作 | 範例 |
|----------------|---------|
| 透過管線安裝（pipe-to-shell） | `curl \| bash` |
| 將敏感資料外傳 | 透過網路傳送 API 金鑰、憑證 |
| 生產環境部署 | 以生產環境為目標的部署指令 |
| 大量刪除 | 對大型目錄執行 `rm -rf` |
| IAM 變更 | 修改權限與角色 |
| 強制推送到 main | `git push --force origin main` |

> **更多決策交給分類器處理（v2.1.218）**：分類器現在也會判斷以檔案系統根目錄或家目錄為目標的刪除動作，例如 `rm -rf /` 與 `rm -rf ~`，包含這類刪除出現在指令替換或行程替換內部的情況。在 v2.1.218 之前，一般寫法會跳出核准提示，而替換寫法則是在 v2.1.208 到 v2.1.217 之間才會跳出提示。背景執行的 `&` 與可疑的 Windows 路徑檢查，同樣不再跳出權限對話框 — 一律交由分類器判斷。

### 預設允許的動作

| 允許的動作 | 範例 |
|----------------|---------|
| 本機檔案操作 | 讀取、寫入、編輯專案檔案 |
| 安裝清單中宣告的相依套件 | 依 manifest 執行 `npm install`、`pip install` |
| 唯讀 HTTP 請求 | 用 `curl` 擷取文件 |
| 推送到目前分支 | `git push origin feature-branch` |

### 設定自動模式

**以 JSON 格式印出預設規則**：
```bash
claude auto-mode defaults
```

**還原自動模式的預設設定**（v2.1.212），會出現確認提示（可用 `--yes` 略過）：
```bash
claude auto-mode reset
claude auto-mode reset --yes
```

**設定信任的基礎架構**，可透過企業部署用的 `autoMode.environment` 受管設定進行。這讓管理員能定義信任的 CI/CD 環境、部署目標與基礎架構模式。

#### 用 `"$defaults"` 擴充預設值（v2.1.118）

自 v2.1.118 起，`autoMode.allow`、`autoMode.soft_deny` 與 `autoMode.environment` 都接受 `"$defaults"` 這個特殊值，讓你的規則**附加**到內建清單後面，而不是取代它。在 v2.1.118 之前，任何使用者自訂的陣列都會在不知不覺間覆蓋掉內建規則。

#### 用 `autoMode.hard_deny` 進行無條件封鎖（v2.1.136）

`autoMode.hard_deny`（v2.1.136 以上）是一組分類器規則，**無論推斷出的使用者意圖為何**都會封鎖某一類動作。適合用在絕對不能在自動模式下執行的動作 — 例如對根目錄執行 `rm -rf`，或對受保護分支執行 `git push --force`。與 `soft_deny` 不同，hard-deny 規則沒有讓分類器協商的餘地。

```json
{
  "autoMode": {
    "hard_deny": ["Bash(rm -rf /:*)", "Bash(git push --force*)"]
  }
}
```

**之前（會取代內建規則 — v2.1.118 之前的行為）：**

```json
{
  "autoMode": {
    "allow": ["Bash(gh pr list:*)"]
  }
}
```

**之後（擴充內建規則 — v2.1.118 以上）：**

```json
{
  "autoMode": {
    "allow": ["$defaults", "Bash(gh pr list:*)"],
    "soft_deny": ["$defaults", "Bash(kubectl delete:*)"],
    "environment": ["$defaults", "trusted-ci.internal"]
  }
}
```

使用 `"$defaults"` 就能保留內建的基準規則，同時再疊加組織或專案專屬的新增規則。

#### 用 `autoMode.classifyAllShell` 分類每一個 shell 指令（v2.1.193）

`autoMode.classifyAllShell`（布林值，v2.1.193 以上）會讓**所有** Bash/PowerShell 指令都經過自動模式分類器。當你希望分類器檢查工作階段中的每一個 shell 指令時，可以啟用它。

```json
{
  "autoMode": {
    "classifyAllShell": true
  }
}
```

同一版本也會在自動模式封鎖某個動作時顯示**拒絕原因** — 可在對話紀錄、拒絕提示（toast）以及 `/permissions` 底下的「最近拒絕」清單中看到（v2.1.193 以上）。

#### 內建的意圖判斷保護機制（v2.1.183）

除了使用者自行設定的 `hard_deny` 之外，只要你在本次工作階段沒有明確要求，自動模式預設也會封鎖以下具破壞性的指令：

- `git reset --hard`、`git checkout -- .`、`git clean -fd`、`git stash drop`
- `git commit --amend`（當該次提交不是本次工作階段由代理所做時）
- `terraform destroy`、`pulumi destroy`、`cdk destroy`（除非你有指定要處理該堆疊）

這是由推斷意圖驅動的內建預設保護機制 — 你不需要自己把這些指令加進 `hard_deny`。

### 回退行為

當分類器無法確定時，自動模式會回退為詢問使用者：
- 連續 **3 次**被分類器封鎖之後
- 在單一工作階段中累計 **20 次**被分類器封鎖之後

這確保了當分類器無法有把握地核准某個動作時，使用者永遠保有最終控制權。

### 建立等同於自動模式的權限（不需要 Team 方案）

如果你沒有 Team 方案，或想用不依賴背景分類器的簡單做法，可以先在 `~/.claude/settings.json` 中建立一組保守的安全權限規則基準。這個腳本一開始只有唯讀與本機檢查類規則，之後你可以自行選擇是否加入編輯、測試、本機 git 寫入、套件安裝與 GitHub 寫入等動作。

**檔案：** `09-advanced-features/setup-auto-mode-permissions.py`

```bash
# 預覽會新增哪些內容（不會實際寫入變更）
python3 09-advanced-features/setup-auto-mode-permissions.py --dry-run

# 套用保守的基準規則
python3 09-advanced-features/setup-auto-mode-permissions.py

# 只在需要時再加入更多能力
python3 09-advanced-features/setup-auto-mode-permissions.py --include-edits --include-tests
python3 09-advanced-features/setup-auto-mode-permissions.py --include-git-write --include-packages
```

這個腳本會在以下類別中新增規則：

| 類別 | 範例 |
|----------|---------|
| 核心唯讀工具 | `Read(*)`、`Glob(*)`、`Grep(*)`、`Agent(*)`、`WebSearch(*)`、`WebFetch(*)` |
| 本機檢查 | `Bash(git status:*)`、`Bash(git log:*)`、`Bash(git diff:*)`、`Bash(cat:*)` |
| 可選的編輯 | `Edit(*)`、`Write(*)`、`NotebookEdit(*)` |
| 可選的測試／建置 | `Bash(pytest:*)`、`Bash(python3 -m pytest:*)`、`Bash(cargo test:*)` |
| 可選的 git 寫入 | `Bash(git add:*)`、`Bash(git commit:*)`、`Bash(git stash:*)` |
| Git（本機寫入） | `Bash(git add:*)`、`Bash(git commit:*)`、`Bash(git checkout:*)` |
| 套件管理工具 | `Bash(npm install:*)`、`Bash(pip install:*)`、`Bash(cargo build:*)` |
| 建置與測試 | `Bash(make:*)`、`Bash(pytest:*)`、`Bash(go test:*)` |
| 常見 shell 指令 | `Bash(ls:*)`、`Bash(cat:*)`、`Bash(find:*)`、`Bash(cp:*)`、`Bash(mv:*)` |
| GitHub CLI | `Bash(gh pr view:*)`、`Bash(gh pr create:*)`、`Bash(gh issue list:*)` |

危險操作（`rm -rf`、`sudo`、強制推送、`DROP TABLE`、`terraform destroy` 等）刻意被排除在外。這個腳本具備冪等性 — 執行兩次不會重複新增規則。

---

## 背景任務

背景任務讓長時間執行的作業，可以在不阻塞對話的情況下執行。

### 什麼是背景任務？

背景任務會以非同步方式執行，你可以繼續進行手邊的工作：
- 長時間執行的測試套件
- 建置流程
- 資料庫遷移
- 部署腳本
- 分析工具

**基本用法：**
```bash
User: 在背景執行測試

Claude: 已啟動任務 bg-1234

/task list           # 顯示所有任務
/task status bg-1234 # 查看進度
/task show bg-1234   # 檢視輸出
/task cancel bg-1234 # 取消任務
```

### 啟動背景任務

```
User: 在背景執行完整的測試套件

Claude: 已在背景啟動測試（task-id：bg-1234）
你可以在測試執行的同時繼續工作。

[你可以繼續對話]

User: 同時，我們來重構 auth 模組吧

Claude: [在測試於背景執行的同時處理 auth 模組]

[稍後，測試完成時]

Claude: 📢 背景任務 bg-1234 已完成：
✅ 245 個測試通過
❌ 3 個測試失敗
查看結果：/task show bg-1234
```

### 管理背景任務

**列出進行中的任務**：
```
User: /task list

進行中的背景任務：
1. [bg-1234] 執行測試中（完成 50%，剩餘 2 分鐘）
2. [bg-1235] 建置 Docker 映像檔（完成 25%，剩餘 8 分鐘）
3. [bg-1236] 部署到預備環境（完成 90%，剩餘 30 秒）
```

**查看任務狀態**：
```
User: /task status bg-1234

任務 bg-1234：執行測試中
狀態：進行中
進度：120/245 個測試（49%）
開始時間：2025-11-08 10:30:15
預估完成時間：2025-11-08 10:34:22
```

**檢視任務輸出**：
```
User: /task show bg-1234

[顯示測試執行的即時輸出]
```

**取消任務**：
```
User: /task cancel bg-1234

已取消背景任務 bg-1234
```

### 範例：平行開發

```
User: 在背景執行建置

Claude: 開始建置……（task-id：bg-5001）

User: 也在背景執行 linter

Claude: 開始執行 linter……（task-id：bg-5002）

User: 這些執行的同時，我們來實作新的 API 端點吧

Claude: [在建置與 linter 執行的同時實作 API 端點]

[10 分鐘後]

Claude: 📢 建置成功完成（bg-5001）
📢 Linter 發現 12 個問題（bg-5002）

User: 讓我看看 linter 的問題

Claude: [顯示 bg-5002 的 linter 輸出]
```

### 設定

背景任務沒有對應的 `settings.json` 區塊，這項功能是透過環境變數控制的：

```bash
# 完全關閉背景任務
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=true
```

並行數量同樣不是背景任務的設定項目 — 同時執行的代理數量是由 `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`（預設為 `20`）控制的。

---

## Monitor 工具（事件驅動串流）

> **v2.1.98 新功能**：Monitor 工具讓 Claude 能監看背景指令的 stdout，並在出現符合條件的事件時立即反應——取代了輪詢迴圈與用 `sleep` 等待長時間執行處理程序的做法。

Monitor 可附加到任何會寫入 stdout 的 shell 指令。該指令輸出的每一行 stdout 都會變成喚醒工作階段的通知。指令由 Claude 指定；harness 負責串流輸出，並在事件觸發時傳遞。啟動底層處理程序的做法請參閱相關的[背景任務](#背景任務)一節。

### 為何重要

用 `/loop` 或 `sleep` 做輪詢，每一輪都會耗用一次完整的 API 往返，無論有沒有變化發生。Monitor 在指令安靜時毫無動靜，**零 token** 消耗。一旦事件真的發生，Claude 會立即反應——不必等到下一次輪詢才發現。對於執行時間超過幾分鐘的任務，這種做法比輪詢迴圈更省錢也更快。

### 兩種常見模式

**串流過濾（Stream filters）** 監看來自長時間執行來源的持續輸出。指令會一直執行；每一行符合條件的輸出都是一個事件。

```bash
tail -f /var/log/app.log | grep --line-buffered "ERROR"
```

**輪詢後送出過濾（Poll-and-emit filters）** 定期檢查來源，只有在有變化時才送出事件。適用於 API、資料庫，或任何沒有原生串流的來源。

```bash
last=$(date -u +%Y-%m-%dT%H:%M:%SZ)
while true; do
  gh api "repos/owner/repo/issues/123/comments?since=$last" || true
  last=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  sleep 30
done
```

### 具體範例

「啟動我的開發伺服器並監看是否有錯誤。」Claude 會把伺服器當成背景任務啟動，附加一個 Monitor 過濾器（`tail -F server.log | grep --line-buffered -E "ERROR|FATAL"`），然後工作階段就安靜下來。一旦記錄檔中出現錯誤行，Claude 就會醒來、讀取錯誤，並可以做出反應——重啟伺服器、修好問題，或是回報給你——完全不需要你去確認進度。

> **警告**：透過管線接到 `grep` 時，**務必**使用 `grep --line-buffered`。少了它，grep 會以 4KB 為單位緩衝 stdout，在低流量的串流上可能讓事件延遲好幾分鐘。這是 Monitor 在實務上失靈的頭號原因——如果你的過濾器明明該有反應卻很安靜，先檢查有沒有加上 `--line-buffered` 旗標。

---

## 動態工作流程

> **v2.1.154 新功能**

動態工作流程讓 Claude 能夠**確定性地**協調數十到數百個背景[子代理](../04-subagents/README.md)——扇出、管線、平行階段都寫在腳本裡，而不是交給模型臨場發揮。單一代理只有一個上下文視窗，工作流程則會把任務拆到多個代理上，再把結果重新組合起來。

從 v2.1.219 起，動態工作流程預設採用**中等規模準則（目標少於 15 個代理）**。可以在 `/config` 的**動態工作流程規模**選項中選擇別的規模——或不設限——也可以在設定檔中設定 `workflowSizeGuideline` 這個 key。執行中工作流程的狀態列會顯示目前的規模，並提示可到 `/config` 修改。

### 何時該使用

- **全面涵蓋** — 平行對許多檔案／面向做稽核或審查。
- **提高信心** — 產生多個獨立觀點，在採用結論前先做對抗性驗證。
- **超越單一上下文的規模** — 大型遷移、廣泛掃描，或是任何單一上下文放不下的研究工作。

對於你已經理解透徹的一次性任務，單一代理（或是直接編輯）仍然是正確的工具——工作流程要在工作能扇出時才划算。

### 啟動與檢視

- **啟動**：請 Claude 為任務建立一個工作流程（例如「跑一個工作流程去審查 `src/` 裡的每個檔案」）。Claude 會編寫協調腳本並在背景執行。
- **檢視**：`/workflows` 指令會顯示執行中與已完成的工作流程執行紀錄，並即時顯示進度。
- **`ultracode`**：在 `/effort` 選單中選擇 `ultracode` 會為本次工作階段開啟這個功能——它會把 `xhigh` 傳給模型，*並且* 讓 Claude 預設協調動態工作流程。這只在單一工作階段內生效，無法寫進設定檔。（從 v2.1.160 起觸發關鍵字是 `ultracode`；單純的「workflow」一詞已不會再觸發執行。）

工作流程建立在子代理模型之上——個別代理如何定義與限定範圍，請參閱[子代理](../04-subagents/README.md)。

---

## 排程任務

排程任務讓你能依重複排程自動執行 Prompt，或設定一次性提醒。任務是綁定工作階段的——只在 Claude Code 執行中運作，工作階段結束就會清除。自 v2.1.72 起可用。

> **在 claude.com 上行銷為「Routines」（2026-05-14）**：Anthropic 的產品部落格把這個功能介紹為 **Routines**。CLI 指令仍然是 `/schedule`；本指南沿用原本的「排程任務（Scheduled Tasks）」命名以保持一致。如果你在 claude.com 文件或桌面應用程式中看到「Routines」，指的就是同一個功能。

### `/loop` 指令

```bash
# 明確指定間隔
/loop 5m 檢查部署是否完成

# 自然語言
/loop 每 30 分鐘檢查一次建置狀態
```

也支援標準的 5 欄位 cron 表達式，可做更精確的排程。

### 一次性提醒

設定只會在特定時間觸發一次的提醒：

```
下午 3 點提醒我推送發布分支
45 分鐘後執行整合測試
```

### 管理排程任務

| 工具 | 說明 |
|------|-------------|
| `CronCreate` | 建立新的排程任務 |
| `CronList` | 列出所有進行中的排程任務。自 v2.1.136 起，輸出內容也包含條件限定詞與排程的 Prompt 內容本身，讓你不用開啟就能稽核每個 cron 會執行什麼。 |
| `CronDelete` | 移除排程任務 |

**限制與行為**：
- 每個工作階段最多 **50 個排程任務**
- 綁定工作階段——工作階段結束就會清除
- 重複性任務會在 **3 天** 後自動過期
- 任務只會在 Claude Code 執行中時觸發——錯過的觸發時間不會補跑

### 行為細節

| 項目 | 細節 |
|--------|--------|
| **重複性抖動** | 最多為間隔的 10%（上限 15 分鐘） |
| **一次性抖動** | 在 :00／:30 邊界上最多 90 秒 |
| **錯過的觸發** | 不補跑——若 Claude Code 未執行則直接略過 |
| **持久性** | 不會跨重啟保留 |

### 雲端排程任務

使用 `/schedule` 建立在 Anthropic 基礎架構上執行的雲端排程任務：

```
/schedule 每天早上 9 點執行測試套件並回報失敗
```

雲端排程任務會跨重啟持續存在，且不需要 Claude Code 在本機執行。

### 停用排程任務

```bash
export CLAUDE_CODE_DISABLE_CRON=1
```

> **API 金鑰方案會自動停用 `/schedule`（v2.1.139）**：只要設定了 `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 或 `apiKeyHelper` 其中之一，雲端 `/schedule` 就會被靜默停用——即使你同時也用 claude.ai 登入。同樣的條件也會停用[遠端控制](#停用遠端控制disableremotecontrolv21128)、claude.ai 的 MCP 連接器，以及通知偏好設定。取消設定 API 金鑰（或改用 Pro／Max 的 OAuth 方案）即可使用 `/schedule`。本機的 `CronCreate` 不受影響。

### 範例：監控部署

```
/loop 5m 檢查預備環境的部署狀態。
        若部署成功，通知我並停止迴圈。
        若失敗，顯示錯誤記錄。
```

> **提示**：排程任務是綁定工作階段的。若需要跨重啟持續存在的自動化，請改用 CI/CD 管線、GitHub Actions，或桌面應用程式的排程任務。

---

## 權限模式

權限模式控制 Claude 在未經明確核准下可以執行哪些動作。

### 可用的權限模式

| 模式 | 行為 |
|---|---|
| `manual` | 只能讀取檔案；其他動作皆須詢問。v2.1.200 起由 `default` 改名而來——`default` 仍可作為別名使用 |
| `acceptEdits` | 可讀取與編輯檔案；指令仍須詢問 |
| `plan` | 只能讀取檔案（研究模式，不可編輯） |
| `auto` | 所有動作皆經背景安全分類器檢查。需要合格的模型（Opus 5、Sonnet 5、Opus 4.7／4.8，或多數供應商上的 Fable 5）與供應商——所有方案皆可使用，參見[自動模式](#自動模式) |
| `bypassPermissions` | 所有動作皆不做權限檢查（危險） |
| `dontAsk` | 只執行預先核准的工具；其餘一律拒絕 |

> **備註**：互動預設模式已在 v2.1.200 從 `default` 改名為 **Manual**（涵蓋 CLI、`--help`、VS Code 與 JetBrains），啟用時頁尾會出現灰色 ⏸ 徽章（v2.1.203）。`--permission-mode manual` 與 `--permission-mode default` 兩者皆可用，設定檔中的 `"defaultMode": "manual"` 與 `"defaultMode": "default"` 也一樣。注意設定 key 是 `permissions.defaultMode`——並沒有 `permissions.mode` 這個 key，以下範例一律採用正式寫法。

在 CLI 中按 `Shift+Tab` 可在各模式間循環切換。可用 `--permission-mode` 旗標或 `permissions.defaultMode` 設定指定預設模式。

> **規劃模式下的 shell 指令交由分類器判斷（v2.1.218）**：當[自動模式](#自動模式)可用、且 `useAutoModeDuringPlan` 設定為開啟（預設即為開啟）時，分類器會在規劃期間審查 shell 指令，而不是詢問你。核准的指令會執行，被拒絕的則會被擋下。規劃模式仍然無條件封鎖檔案寫入。

從 v2.1.160 起，即使是 `acceptEdits` 模式，在寫入 shell 啟動檔（`.zshenv`、`.zlogin`、`.bash_login`、`~/.config/git/`）與會執行程式碼的建置設定檔（`.npmrc`、`.yarnrc*`、`bunfig.toml`、`.bazelrc`、`.pre-commit-config.yaml`、`.devcontainer/` 等）之前也會先詢問，因為這些檔案可能導致非預期的指令執行。

> **`--dangerously-skip-permissions` 擴大路徑涵蓋範圍（v2.1.121、v2.1.126）**：`--dangerously-skip-permissions` CLI 旗標（以及等效的 `bypassPermissions` 模式）現在對更廣泛的允許清單——`.claude/skills/`、`.claude/agents/`、`.claude/commands/`、`.claude/`、`.git/`、`.vscode/`，以及 shell 設定檔——的寫入都會略過詢問。災難性的刪除指令（`rm -rf /` 等）在此模式下仍會詢問（在自動模式下則改由分類器判斷，參見[自動模式](#自動模式)）。請把這個旗標當成比以往更鋒利的工具，只在可拋棄的沙箱環境中使用。

> **Windows shell 偵測（v2.1.120、v2.1.126）**：不再需要 Git for Windows／Git Bash。當 Git Bash 不存在時，Claude Code 會改用 PowerShell 作為 shell 工具。自 v2.1.126 起，只要啟用了 PowerShell 工具，PowerShell 就是*主要*的 shell，偵測範圍也涵蓋透過 Microsoft Store 安裝的 PowerShell 7、未加入 PATH 的 MSI 安裝，或作為 `.NET global tool` 安裝的版本。

> **在 Windows 上，Bedrock／Vertex／Foundry 預設啟用 PowerShell 工具（v2.1.143）**：自 v2.1.143 起，PowerShell 工具在 Windows 上對 Bedrock、Vertex 與 Foundry 使用者**預設為啟用**。Claude Code 會以 `-ExecutionPolicy Bypass` 呼叫 PowerShell，因此即使系統原則是 `Restricted` 腳本仍可執行。若要讓 Claude Code 遵守系統執行原則，請設定 `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1`。若要完全停用 PowerShell 工具，請設定 `CLAUDE_CODE_USE_POWERSHELL_TOOL=0`。

### 啟用方式

**鍵盤快捷鍵**：
```bash
Shift + Tab  # 在全部 6 種模式間循環切換
```

**斜線指令**：
```bash
/plan                  # 進入規劃模式
```

**CLI 旗標**：
```bash
claude --permission-mode plan
claude --permission-mode auto
```

**設定**：
```json
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

### 權限模式範例

#### 預設模式
Claude 會在重大動作前要求確認：

```
User: 修好 auth.ts 裡的 bug

Claude: 我需要修改 src/auth.ts 來修好這個 bug。
這個變更會更新密碼驗證邏輯。

是否核准這個變更？（yes/no/show）
```

#### 規劃模式
先審閱實作計畫再執行：

```
User: /plan 實作使用者驗證系統

Claude: 我會建立一份實作驗證功能的計畫。

## 實作計畫
[詳細計畫，包含各階段與步驟]

是否要繼續？（yes/no/modify）
```

#### 自動接受編輯模式
自動接受檔案修改：

```
User: acceptEdits
User: 修好 auth.ts 裡的 bug

Claude: [直接進行變更，不再詢問]
```

### 使用情境

**程式碼審查**：
```
User: claude --permission-mode plan
User: 審查這個 PR 並提出改善建議

Claude: [讀取程式碼、給出意見，但無法修改]
```

**結對程式設計**：
```
User: claude --permission-mode default
User: 我們一起來實作這個功能

Claude: [每次變更前都會請求核准]
```

**自動化任務**：
```
User: claude --permission-mode acceptEdits
User: 修好整個程式碼庫裡所有的 linting 問題

Claude: [自動接受檔案編輯，不再詢問]
```

---

## 無介面模式（headless）

Print 模式（`claude -p`）讓 Claude Code 可以在沒有互動輸入的情況下執行，非常適合自動化與 CI/CD。這是非互動模式，取代了舊有的 `--headless` 旗標。

### 什麼是 Print 模式？

Print 模式可以做到：
- 自動化腳本執行
- CI/CD 整合
- 批次處理
- 排程任務

### 在 Print 模式下執行（非互動）

```bash
# 執行特定任務
claude -p "執行所有測試"

# 處理管線輸入的內容
cat error.log | claude -p "分析這些錯誤"

# CI/CD 整合（GitHub Actions）
- name: AI Code Review
  run: claude -p "審查 PR"
```

### 更多 Print 模式使用範例

```bash
# 執行特定任務並擷取輸出
claude -p "執行所有測試並產生涵蓋率報告"

# 使用結構化輸出
claude -p --output-format json "分析程式碼品質"

# 從 stdin 輸入
echo "分析程式碼品質" | claude -p "解釋這個"
```

### 範例：CI/CD 整合

**GitHub Actions**：
```yaml
# .github/workflows/code-review.yml
name: AI Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Claude Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p --output-format json \
            --max-turns 3 \
            "審查這個 PR，檢查以下項目：
            - 程式碼品質問題
            - 安全性漏洞
            - 效能疑慮
            - 測試涵蓋率
            將結果輸出為 JSON" > review.json

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = JSON.parse(fs.readFileSync('review.json', 'utf8'));
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: JSON.stringify(review, null, 2)
            });
```

### Print 模式設定

Print 模式（`claude -p`）支援多個自動化用的旗標：

```bash
# 限制自主回合數
claude -p --max-turns 5 "重構這個模組"

# 結構化 JSON 輸出
claude -p --output-format json "分析這個程式碼庫"

# 搭配結構描述驗證
claude -p --json-schema '{"type":"object","properties":{"issues":{"type":"array"}}}' \
  "找出這段程式碼裡的 bug"

# 停用工作階段持久化
claude -p --no-session-persistence "一次性分析"
```

### 安全模式（疑難排解用）

`--safe-mode`（以及 `CLAUDE_CODE_SAFE_MODE` 環境變數，例如 `CLAUDE_CODE_SAFE_MODE=1`）會以**停用所有自訂功能**的方式啟動 Claude Code——CLAUDE.md、外掛（Plugins）、技能（Skills）、Hooks 與 MCP 伺服器全部關閉。

```bash
# 啟動時停用所有自訂功能
claude --safe-mode

# 透過環境變數達到相同效果
CLAUDE_CODE_SAFE_MODE=1 claude
```

這是一個疑難排解工具：當自訂設定造成問題時，用安全模式啟動可以判斷問題是出在你的設定，還是 Claude Code 本身。

---

## 工作階段管理

有效管理多個 Claude Code 工作階段。

### 工作階段管理指令

| 指令 | 說明 |
|---------|-------------|
| `/resume` | 依 ID 或名稱回復對話 |
| `/rename` | 為目前的工作階段命名 |
| `/fork [prompt]` | 把對話複製到一個新的獨立背景工作階段，自己則繼續留在這裡工作（v2.1.212+） |
| `/subtask <task>` | 衍生出一個繼承完整對話的子代理，完成後把結果回報到這裡（v2.1.212+） |
| `/branch [name]` | 切換到這個時間點的對話副本，同時保留原本的對話 |
| `claude -c` | 繼續最近一次的對話 |
| `claude -r "session"` | 依名稱或 ID 回復工作階段 |

### 回復工作階段

**繼續最近一次的對話**：
```bash
claude -c
```

**回復具名的工作階段**：
```bash
claude -r "auth-refactor" "finish this PR"
```

**為目前的工作階段命名**（在 REPL 內）：
```
/rename auth-refactor
```

> **v2.1.212 更新**：在代理檢視畫面中直接輸入 `/resume`（不帶任何參數）現在會開啟一個過去工作階段的選擇器——包含已從可見清單中移除的工作階段——並將選中的工作階段以背景工作階段的形式回復。

### 複製與分支工作階段

有三個指令可以複製對話，差別在於*副本會在哪裡執行*：

`/subtask <task>` 會衍生出一個繼承完整對話的子代理，讓它去處理任務，而你可以繼續手上的工作——它在 `claude agents` 裡會有自己的一列，完成後結果會回傳到你的對話中：

```
/subtask Investigate why the auth tests are flaky
```

`/fork [prompt]` 則是把對話複製到一個新的**背景工作階段**。副本會從目前為止的所有內容開始，獨立執行——不會有任何東西回傳到這個對話：

```
/fork Try the OAuth approach end to end
```

如果你想親自切換到副本，而不是委派出去，可以用 `/branch [name]`，它會保留原本的對話，讓你之後能用 `/resume` 回去：

```
/branch try-oauth-instead
```

> **備註**：`/fork` 與 `/subtask` 的角色在 **v2.1.212** 互換了。在 v2.1.161 之前，`/fork` 是 `/branch` 的別名；從 v2.1.161 到 v2.1.211 期間，它會啟動一個衍生子代理——這個行為現在由 `/subtask` 承接。當代理檢視功能關閉時，`/subtask` 無法使用，`/fork` 則會保留衍生子代理的行為。

也可以從 CLI 進行複製：
```bash
claude --resume auth-refactor --fork-session "try OAuth instead"
```

### 工作階段持久化

工作階段會自動儲存，並可以隨時回復：

```bash
# 繼續最近一次的對話
claude -c

# 依名稱或 ID 回復特定工作階段
claude -r "auth-refactor"

# 回復並複製出去做實驗
claude --resume auth-refactor --fork-session "alternative approach"
```

### 用量上限自動續傳（v2.1.234）

自 **v2.1.234** 起，若工作階段因 claude.ai 用量上限而卡住，一旦限制重置就會自動繼續——不需要手動重新輸入提示詞。可以在 `/config` 中的「Continue automatically at usage limit」項目切換這個功能。

### 工作階段回顧（v2.1.108）

當你離開一段時間後回到工作階段，Claude 可以顯示一份簡短的回顧，說明先前完成了哪些工作。這項功能對停用遙測的使用者（Bedrock、Vertex、Foundry 使用者）預設為啟用。

> **OTEL 遙測 — 重新啟用意見回饋問卷（v2.1.136+）**：有蒐集 OpenTelemetry 資料的組織，可以透過設定 `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL=1` 重新啟用 Anthropic 的工作階段品質問卷。在 OTEL 部署環境中，這份問卷預設是關閉的，因為它先前會被排除在遙測管線之外。

> **OTEL 遙測 — `assistant_response` 記錄事件（v2.1.193+）**：Claude Code 會發出帶有模型回應文字的 `claude_code.assistant_response` OpenTelemetry 記錄事件，讓 OTEL 管線除了既有的工具／事件遙測之外，也能擷取 Claude 說了什麼。

**控制回顧行為：**

```bash
/recap                                 # 手動觸發一次回顧
/config                                # 切換自動回顧的開關
```

也可以透過環境變數：
```bash
CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0 claude   # 停用回顧
CLAUDE_CODE_ENABLE_AWAY_SUMMARY=1 claude   # 強制啟用回顧
```

---

## 跨工作階段訊息

> **v2.1.224 新增**，功能延伸至 v2.1.239。可在 **macOS、Linux，以及（自 v2.1.239 起）Windows** 上使用。

工作階段以前彼此孤立。跨工作階段訊息讓一個 Claude Code 工作階段可以與另一個
對話——包括你其他機器上的工作階段，以及你的雲端工作階段——這樣你就能把問題
交給已經載入正確上下文的工作階段，而不必重新解釋一遍。

### 探索工作階段

`ListAgents` 會列出所有你可以對話的對象：你派生的子代理、這台機器上的其他本機
工作階段、你的雲端工作階段，以及（在連上遠端控制時）你其他機器上的工作階段。
每一列都會標示種類，自 v2.1.229 起，各列也會加上 `offline` 與 `cloud` 標籤，
讓你分辨哪個工作階段是可連線的、哪個是休眠中的。

每一列裡的**名稱就是位址**——你就是傳送給這個名稱。

### 傳送訊息

`SendMessage` 需要目標與訊息內容：

```text
SendMessage({ to: "<session name>", message: "你對重試邏輯得出了什麼結論？" })
```

自 v2.1.232 起，只要輸入名稱本身即可——除非真的有兩列共用同一個名稱，否則不必
再加上用來消歧義的 ref。

### 等待工作階段進入閒置（`notify_when_idle`，v2.1.236）

當你傳訊息的對象正在執行任務時，你通常會想知道它何時完成，而不是自己去輪詢。
`SendMessage` 正好提供了 `notify_when_idle` 這個輸入參數：

```text
SendMessage({
  to: "auth-refactor",
  message: "遷移完成時通知我一聲",
  notify_when_idle: true
})
```

這個功能是**選擇加入且僅觸發一次**——目標工作階段下次進入閒置時會送出一次
通知，之後訂閱就結束了。不會有輪詢迴圈，若工作階段之後又變忙碌再閒置，也不會
重複通知。

與此相關的兩項 v2.1.239 變更：`ListAgents` 現在除了列出目前活躍的隊友之外，也
會回報**工作階段自己的名稱**（這樣工作階段就能告訴別人該怎麼稱呼自己），而且
跨工作階段訊息也開始支援 **Windows**。

### `@` 提及捷徑（v2.1.232）

除了明確呼叫工具之外，你也可以直接在提示詞中用 `@` 提及某個工作階段來傳訊給它：

```text
@auth-refactor did the migration tests pass?
```

### 控制收到的內容：`crossSessionInbound`

收到的訊息由 `crossSessionInbound` 這個設定項目控制（v2.1.224+）：

| 值 | 行為 |
|---|---|
| `"accept"` | 收到的訊息會傳送給這個工作階段裡的 Claude |
| `"hold"` | 你會看到有訊息送達的通知，但不會實際傳遞 |
| `"refuse"` | 收到的訊息會被丟棄 |

這些值形成一個階梯——`accept < hold < refuse`——而且**只有在比使用者層級設定
更嚴格時，專案與本機設定才會生效**。專案只能收緊訊息的傳遞，不能放寬。自
v2.1.232 起，這個設定在 `/config` 中也有對應的項目「Messages from your other
sessions」。

### 可觸及範圍與限制

- 同一台機器上的本機工作階段，以及你的雲端工作階段。
- 你其他機器上的遠端控制工作階段，可依名稱定址（v2.1.225）。
- 雲端工作階段**收得到**你的訊息，但目前還無法回傳訊息給本機工作階段——要看
  它的回覆，得到它自己的逐字稿裡查看。
- macOS 與 Linux 自 v2.1.224 起支援；Windows 自 v2.1.239 起支援。

---

## 互動功能

### 鍵盤快捷鍵

Claude Code 支援鍵盤快捷鍵，讓操作更有效率。以下是官方文件的完整參考：

| 快捷鍵 | 說明 |
|----------|-------------|
| `Ctrl+C` | 取消目前的輸入／生成 |
| `Ctrl+D` | 結束 Claude Code |
| `Ctrl+G` | 在外部編輯器中編輯計畫 |
| `Ctrl+L` | 重新繪製畫面（僅重繪——連按兩下觸發 `/clear` 的捷徑已在 v2.1.238 移除） |
| `Ctrl+O` | 切換詳細輸出（檢視推理過程） |
| `Ctrl+R` | 反向搜尋歷史紀錄。預設會搜尋**所有專案的所有提示詞**（v2.1.129+）；在選擇器內按 `Ctrl+S` 可縮小到目前的專案。舊版預設只搜尋目前專案。 |
| `Ctrl+T` | 切換任務清單檢視 |
| `Ctrl+B` | 把執行中的任務放到背景 |
| `Esc+Esc` | 回溯程式碼／對話 |
| `Shift+Tab` / `Alt+M` | 切換權限模式 |
| `Option+P` / `Alt+P` | 切換模型 |
| `Option+T` / `Alt+T` | 切換延伸思考 |
| `Option+O` / `Alt+O` | 切換快速模式（`/fast`） |
| `Ctrl+X` `Ctrl+K` | 停止所有背景子代理 |
| `Ctrl+S` | 暫存目前的提示詞；再按一次可還原 |
| `Ctrl+_` | 復原最後一次對提示詞輸入的編輯 |
| `:` | 在單字開頭輸入 `:` 可開啟 emoji 短碼自動完成，例如 `:heart:`（v2.1.217+） |

**行編輯（標準 readline 快捷鍵）：**

| 快捷鍵 | 動作 |
|----------|--------|
| `Ctrl + A` | 移動到行首 |
| `Ctrl + E` | 移動到行尾 |
| `Ctrl + K` | 剪下到行尾 |
| `Ctrl + U` | 剪下到行首 |
| `Ctrl + W` | 向後刪除一個單字 |
| `Ctrl + Y` | 貼上（yank） |
| `Tab` | 自動完成 |
| `↑ / ↓` | 指令歷史 |

### 無障礙功能

螢幕報讀模式（v2.1.208+）會把 CLI 切換成專為螢幕報讀軟體設計的純文字算繪模式。可以透過 CLI 旗標、環境變數或設定 key 來啟用：

```bash
claude --ax-screen-reader
```

```bash
export CLAUDE_AX_SCREEN_READER=1
```

```json
{
  "axScreenReader": true
}
```

### 自訂鍵盤綁定

執行 `/keybindings` 即可建立自訂鍵盤快捷鍵，這會開啟 `~/.claude/keybindings.json` 供你編輯（v2.1.18+）。

**設定格式**：

```json
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null,
        "ctrl+k ctrl+s": "chat:stash"
      }
    },
    {
      "context": "Confirmation",
      "bindings": {
        "ctrl+a": "confirmation:yes"
      }
    }
  ]
}
```

把某個綁定設為 `null` 即可解除預設快捷鍵的綁定。

### 可用情境

鍵盤綁定的作用範圍是特定的 UI 情境：

| 情境 | 主要動作 |
|---------|-------------|
| **Chat** | `submit`, `cancel`, `cycleMode`, `modelPicker`, `thinkingToggle`, `undo`, `externalEditor`, `stash`, `imagePaste` |
| **Confirmation** | `yes`, `no`, `previous`, `next`, `nextField`, `cycleMode`, `toggleExplanation` |
| **Global** | `interrupt`, `exit`, `toggleTodos`, `toggleTranscript` |
| **Autocomplete** | `accept`, `dismiss`, `next`, `previous` |
| **HistorySearch** | `search`, `previous`, `next` |
| **Settings** | 依情境而定的設定導覽 |
| **Tabs** | 分頁切換與管理 |
| **Help** | 說明面板導覽 |

總共有 18 種情境，包括 `Transcript`、`Task`、`ThemePicker`、`Attachments`、`Footer`、`MessageSelector`、`DiffDialog`、`ModelPicker` 與 `Select`。

### 組合鍵支援

鍵盤綁定支援組合鍵序列（多按鍵組合）：

```
"ctrl+k ctrl+s"   → 兩鍵序列：先按 ctrl+k，再按 ctrl+s
"ctrl+shift+p"    → 同時按下的修飾鍵
```

**按鍵語法**：
- **修飾鍵**：`ctrl`、`alt`（或 `opt`）、`shift`、`meta`（或 `cmd`）
- **大寫代表按住 Shift**：`K` 等同於 `shift+k`
- **特殊按鍵**：`escape`、`enter`、`return`、`tab`、`space`、`backspace`、`delete`、方向鍵

### 保留與衝突按鍵

| 按鍵 | 狀態 | 備註 |
|-----|--------|-------|
| `Ctrl+C` | 保留 | 無法重新綁定（中斷） |
| `Ctrl+D` | 保留 | 無法重新綁定（結束） |
| `Ctrl+B` | 與終端機衝突 | tmux 的前綴鍵 |
| `Ctrl+A` | 與終端機衝突 | GNU Screen 的前綴鍵 |
| `Ctrl+Z` | 與終端機衝突 | 暫停處理程序 |

> **提示**：如果快捷鍵沒有作用，請檢查是否與你的終端機模擬器或多工器（multiplexer）有衝突。

### Tab 自動完成

Claude Code 提供智慧型 Tab 自動完成：

```
User: /rew<TAB>
→ /rewind

User: /plu<TAB>
→ /plugin

User: /plugin <TAB>
→ /plugin install
→ /plugin enable
→ /plugin disable
```

### 指令歷史

存取先前執行過的指令：

```
User: <↑>  # 上一筆指令
User: <↓>  # 下一筆指令
User: Ctrl+R  # 搜尋歷史紀錄

(reverse-i-search)`test': run all tests
```

### 多行輸入

若要輸入複雜的查詢，可以使用多行模式：

```bash
User: \
> 又長又複雜的提示詞
> 橫跨多行
> \end
```

**範例：**

```
User: \
> 實作一個使用者驗證系統
> 需求如下：
> - JWT token
> - Email 驗證
> - 密碼重設
> - 支援 2FA
> \end

Claude: [處理這個多行請求]
```

### 行內編輯

傳送前先編輯指令：

```
User: Deploy to prodcution<Backspace><Backspace>uction

[傳送前先就地編輯]
```

### Vim 模式

啟用 Vi／Vim 鍵盤綁定進行文字編輯：

**啟用方式**：
- 透過 `/config`（切換「Editor / Vim mode」）啟用，或在 `~/.claude/settings.json` 中設定 `editorMode: "vim"`。獨立的 `/vim` 斜線指令已被移除（參見 [issue #43370](https://github.com/anthropics/claude-code/issues/43370)）；Vim 模式現在改由設定驅動。
- 用 `Esc` 切到 NORMAL 模式、`i/a/o` 切到 INSERT 模式、`v` 切到 VISUAL 模式、`V` 切到 VISUAL-LINE 模式（v2.1.118+）

**導覽按鍵**：
- `h` / `l` - 向左／向右移動
- `j` / `k` - 向下／向上移動
- `w` / `b` / `e` - 以單字為單位移動
- `0` / `$` - 移動到行首／行尾
- `gg` / `G` - 跳到文字開頭／結尾

**文字物件**：
- `iw` / `aw` - 單字內部／含邊界
- `i"` / `a"` - 引號字串內部／含邊界
- `i(` / `a(` - 括號內部／含邊界

**Visual 模式（v2.1.118+）**：

| 按鍵 | 模式 | 行為 |
|-----|------|----------|
| `v` | Visual | 以字元為單位選取並提供視覺回饋；可用移動按鍵擴大選取範圍 |
| `V` | Visual-line | 以行為單位選取；一律選取整行 |
| `y` | Yank | 複製目前的 Visual 選取範圍 |
| `d` / `x` | Delete | 刪除目前的 Visual 選取範圍 |
| `c` | Change | 刪除選取範圍並進入 INSERT 模式 |
| `Esc` | Exit | 回到 NORMAL 模式 |

Visual 選取範圍會在輸入欄位中反白顯示，讓你在真正執行操作前，就能清楚看到哪些內容會被複製、刪除或變更。

### Bash 模式

用 `!` 前綴可以直接執行 shell 指令：

```bash
! npm test
! git status
! cat src/index.js
```

適合用來快速執行指令，不必切換情境。

**自 v2.1.193 起：** Bash 模式（`!`）具備即時檔案路徑自動完成功能，讓你在輸入 shell 指令時，不必離開提示詞就能自動補完路徑。

**自 v2.1.186 起：** `!` 指令的輸出現在會自動送給 Claude，並由它做出回應。若想維持先前的行為——輸出只會加進上下文而不觸發回應——請在 `settings.json` 中設定 `"respondToBashCommands": false`。

---

## 輸出樣式

輸出樣式改變的是 Claude **如何**回應，而不是它知道什麼。它會修改系統提示詞，設定角色、語氣與預設的回應格式。當你每一輪都要重複交代同一種語氣，或是想讓 Claude 扮演軟體工程師以外的角色時，就適合用輸出樣式。

若是關於你專案或程式碼庫的指示，請改用 [CLAUDE.md](../02-memory/)——那是另一種機制，有不同的取捨。

### 內建樣式

| 樣式 | 行為 |
|-------|----------|
| **Default** | 標準系統提示詞，針對高效完成軟體工程任務調校 |
| **Proactive** | Claude 會立刻執行並做出合理假設，而不是為了例行決策暫停等待。比自動模式提供更強的自主執行指引，但**不會**改變你的權限模式——你仍然會看到權限提示 |
| **Explanatory** | 在步驟之間加入教學性質的「Insights」，說明實作選擇與程式碼庫的模式 |
| **Learning** | 協作式的邊做邊學。Claude 會分享洞見，*同時*留下 `TODO(human)` 標記，讓你自己動手實作一些策略性的小片段 |
| **Concise**（v2.1.237） | Claude 會直接給出結果，省略前言與敘述。內容的完整程度不變——只是拿掉了包裝答案的鋪陳。可在 `/config` → Output style 中選擇，或設定 `"outputStyle": "Concise"` |

### 選擇樣式

執行 `/config` 並選擇 **Output style**。選擇的結果會存到 `.claude/settings.local.json`。若不想透過選單設定，也可以直接編輯這個設定：

```json
{
  "outputStyle": "Explanatory"
}
```

> **備註**：獨立的 `/output-style` 指令已在 v2.1.73 棄用，並在 **v2.1.91 移除**。請改用 `/config` 或 `outputStyle` 設定。

輸出樣式是系統提示詞的一部分，Claude Code 只會在工作階段開始時讀取一次——變更要等到 `/clear` 之後，或是在新的工作階段中才會生效。

### 自訂輸出樣式

自訂樣式是一個帶有 frontmatter 的 Markdown 檔案，可以存放在三個層級之一：

- 使用者：`~/.claude/output-styles/`
- 專案：`.claude/output-styles/`
- 受管政策：受管設定目錄裡的 `.claude/output-styles/`

專案樣式會從工作目錄到儲存庫根目錄之間，每一個 `.claude/output-styles/` 都載入。自 v2.1.178 起，若巢狀目錄定義了相同的樣式名稱，離工作目錄最近的那個會勝出。

```markdown
---
name: Diagrams first
description: 每次說明都先給一張圖表
keep-coding-instructions: true
---

在說明程式碼、架構或資料流時，先用 Mermaid 圖表呈現結構，
再用文字說明。
```

| Frontmatter | 用途 | 預設值 |
|-------------|---------|---------|
| `name` | 樣式名稱（若與檔名不同） | 沿用檔名 |
| `description` | 顯示在 `/config` 選擇器中 | 無 |
| `keep-coding-instructions` | 保留 Claude Code 內建的軟體工程指示 | `false` |
| `force-for-plugin` | 僅適用於外掛樣式：只要外掛啟用就自動套用，覆蓋使用者的 `outputStyle` | `false` |

**當你只是想改變 Claude 的溝通方式，但仍希望它用同樣的方式寫程式時**，請設定 `keep-coding-instructions: true`。如果 Claude 完全不做軟體工程——例如寫作助理或資料分析師——就不用加這個設定。

### 範圍與成本

輸出樣式只套用在**主對話**上。子代理有自己的系統提示詞，所以樣式不會改變子代理的回應方式；`fork` 是例外，因為它會繼承父層完整的系統提示詞。

加入這些指示會增加輸入 token，不過 Prompt 快取會在第一次請求之後吸收掉大部分的成本。Explanatory 與 Learning 依設計就會產生較長的回應，因此會增加輸出 token。

### 比較一覽

| 功能 | 運作方式 | 適用時機 |
|---------|--------------|-------------|
| 輸出樣式 | 修改系統提示詞 | 你想在每一輪都用不同的角色、語氣或格式 |
| [CLAUDE.md](../02-memory/) | 在系統提示詞之後加入一則使用者訊息 | Claude 應該隨時都知道你的專案慣例 |
| `--append-system-prompt` | 附加到系統提示詞後面，不移除任何內容 | 單次呼叫的一次性附加內容 |
| [子代理](../04-subagents/) | 以自己的系統提示詞、模型與工具執行 | 你想要一個獨立範圍的輔助角色 |
| [技能](../03-skills/) | 呼叫時載入特定任務的指示 | 你有一個可重複使用的工作流程 |

---

## 狀態列

狀態列是一個自訂指令，其輸出會顯示在工作階段的底部。可以用 `/statusline` 設定，或直接設定：

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

`padding` 預設為 `0`。Claude Code 會透過 stdin 把一個 JSON 物件傳給這個指令，顯示什麼內容則由腳本自行決定。

### 可用的輸入欄位

| 分類 | 欄位 |
|-------|--------|
| 工作階段 | `session_id`, `session_name`, `prompt_id`, `transcript_path`, `cwd`, `version` |
| 模型 | `model.id`, `output_style.name`, `effort.level`, `fast_mode`, `thinking.enabled` |
| 代理 | `agent.name`, `vim.mode` |
| 成本 | `cost.total_cost_usd`, `cost.total_duration_ms`, `cost.total_api_duration_ms`, `cost.total_lines_added` |
| 上下文 | `context_window.context_window_size`, `.current_usage`, `.remaining_percentage`, `.total_input_tokens`, `.used_percentage` |
| 限制 | `rate_limits.five_hour.used_percentage`, `.resets_at` |
| 儲存庫 | `pr.number`, `pr.review_state`, `workspace.project_dir`, `workspace.added_dirs`, `workspace.git_worktree`, `workspace.repo.host` |
| Worktree | `worktree.name`, `.branch`, `.path`, `.original_branch`, `.original_cwd` |

### 範例

```bash
#!/bin/bash
# ~/.claude/statusline.sh — 模型、上下文用量與成本
input=$(cat)
model=$(echo "$input" | jq -r '.model.id')
used=$(echo "$input" | jq -r '.context_window.used_percentage')
cost=$(echo "$input" | jq -r '.cost.total_cost_usd')
printf '%s | ctx %.0f%% | $%.2f' "$model" "$used" "$cost"
```

> **備註**：`statusLine` 需要工作區信任（workspace trust）。自 v2.1.153 起，狀態列腳本的執行環境中也會收到 `COLUMNS` 與 `LINES`，讓它們能依終端機大小調整輸出。

---

## TUI 模式（全螢幕）

> **v2.1.110 新功能**

TUI（Text User Interface，文字使用者介面）模式會以全螢幕、不閃爍的方式算繪 Claude Code——很適合 tmux 或 iTerm2 分割視窗這類終端機多工器。

### 啟用 TUI 模式

用 `/tui` 指令切換 TUI 模式，或用 `--tui` 旗標啟動：

```bash
/tui          # 在工作階段內切換
claude --tui  # 直接以 TUI 模式啟動
```

### 設定

| 設定 | 說明 | 預設值 |
|---------|-------------|---------|
| `autoScrollEnabled` | 自動捲動到最新訊息 | `true` |

可透過 `/config` 或 `settings.json` 停用自動捲動：

```json
{
  "autoScrollEnabled": false
}
```

### 焦點檢視

`/focus` 指令會切換焦點檢視——一種只顯示最相關輸出、不受干擾的顯示模式。現在 `Ctrl+O` 只會在一般與詳細逐字稿之間切換（焦點檢視則用 `/focus`）。

---

## 語音輸入

語音輸入為 Claude Code 提供按鍵通話式（push-to-talk）的語音輸入功能，讓你可以用說的方式輸入提示詞，而不必打字。

### 啟用語音輸入

```
/voice
```

### 功能

| 功能 | 說明 |
|---------|-------------|
| **按鍵通話** | 按住按鍵錄音，放開即傳送 |
| **支援 20 種語言** | 語音轉文字支援 20 種語言 |
| **自訂鍵盤綁定** | 可透過 `/keybindings` 設定按鍵通話用的按鍵 |
| **帳號需求** | STT（語音轉文字）處理需要 Claude.ai 帳號 |

### 設定

可在鍵盤綁定檔案（`/keybindings`）中自訂按鍵通話的按鍵。語音輸入會使用你的 Claude.ai 帳號進行語音轉文字處理。

---

## 頻道

頻道是一項研究預覽（Research Preview）功能，會透過 MCP 伺服器把外部服務的事件推送到執行中的 Claude Code 工作階段。來源包括 Telegram、Discord、iMessage，以及任意的 webhook，讓 Claude 可以對即時通知做出反應，不必輪詢。

> **驗證方式（v2.1.128+）**：`--channels` 現在同時支援 Pro/Max OAuth **與** API 金鑰（console）驗證。先前的版本只支援 OAuth。

### 訂閱頻道

```bash
# 啟動時訂閱頻道外掛
claude --channels discord,telegram

# 訂閱多個來源
claude --channels discord,telegram,imessage,webhooks
```

### 支援的整合

| 整合項目 | 說明 |
|-------------|-------------|
| **Discord** | 在工作階段中接收並回覆 Discord 訊息 |
| **Telegram** | 在工作階段中接收並回覆 Telegram 訊息 |
| **iMessage** | 在工作階段中接收 iMessage 通知 |
| **Webhooks** | 接收任意 webhook 來源的事件 |

### 設定

可用 `--channels` 旗標在啟動時設定頻道。企業部署可用受管設定來控制允許哪些頻道外掛：

```json
{
  "allowedChannelPlugins": ["discord", "telegram"]
}
```

`allowedChannelPlugins` 這個受管設定，可以控制整個組織允許使用哪些頻道外掛。

### 運作原理

1. MCP 伺服器扮演頻道外掛的角色，負責連接外部服務
2. 傳入的訊息與事件會被推送到目前使用中的 Claude Code 工作階段
3. Claude 可以在工作階段的上下文中讀取並回覆訊息
4. 頻道外掛必須透過 `allowedChannelPlugins` 受管設定核准
5. 不需要輪詢——事件會即時推送

---

## Chrome 整合

Chrome 整合能把 Claude Code 連接到你的 Chrome 或 Microsoft Edge 瀏覽器，用於即時網頁自動化與除錯。這是一項自 v2.0.73+ 起提供的 beta 功能（Edge 支援則是在 v1.0.36+ 加入）。

### 啟用 Chrome 整合

**啟動時**：

```bash
claude --chrome      # 啟用 Chrome 連線
claude --no-chrome   # 停用 Chrome 連線
```

**在工作階段內**：

```
/chrome
```

選擇「Enabled by default」即可讓 Chrome 整合在往後所有工作階段中都自動啟用。Claude Code 會共用你瀏覽器的登入狀態，因此可以與需要登入的網頁應用程式互動。

### 功能

| 功能 | 說明 |
|------------|-------------|
| **即時除錯** | 讀取主控台記錄、檢查 DOM 元素、即時偵錯 JavaScript |
| **設計驗證** | 比對算繪出的頁面與設計稿 |
| **表單驗證** | 測試表單提交、輸入驗證與錯誤處理 |
| **網頁應用程式測試** | 與需要登入的應用程式互動（Gmail、Google Docs、Notion 等） |
| **資料擷取** | 從網頁擷取並處理內容 |
| **工作階段錄製** | 把瀏覽器操作錄製成 GIF 檔案 |

### 網站層級權限

Chrome 擴充功能會管理各網站的存取權限。你可以隨時透過擴充功能的彈出視窗，針對特定網站授予或撤銷存取權。Claude Code 只會與你明確允許的網站互動。

### 運作方式

Claude Code 會在一個看得見的視窗中操作瀏覽器——你可以即時看到動作發生的過程。當瀏覽器遇到登入頁面或 CAPTCHA 時，Claude 會暫停下來，等你手動處理完再繼續。

### 已知限制

- **瀏覽器支援**：僅支援 Chrome 與 Edge——不支援 Brave、Arc 與其他 Chromium 系瀏覽器
- **WSL**：在 Windows Subsystem for Linux 中無法使用
- **第三方供應商**：不支援 Bedrock、Vertex 或 Foundry API 供應商
- **Service worker 閒置**：在長時間的工作階段中，Chrome 擴充功能的 service worker 可能會進入閒置狀態

> **提示**：Chrome 整合目前是 beta 功能，未來版本可能會擴大支援的瀏覽器範圍。

---

## 遠端控制

遠端控制讓你可以從手機、平板，或任何瀏覽器繼續操作在本機執行中的 Claude Code 工作階段。你的本機工作階段仍然在你的機器上執行——不會有任何東西移到雲端。Pro、Max、Team 與 Enterprise 方案皆可使用（v2.1.51+）。

遠端控制**已不再是研究預覽**——這個標籤在 2026 年第 34 週被拿掉了。現在任何執行 `claude remote-control` 的機器，都會在 Claude app 的 Code 分頁中顯示為一張**裝置卡片**，讓你可以直接從手機在那台機器上啟動工作階段，不必先在機器上啟動再去連線。

### 啟動遠端控制

**從 CLI**：

```bash
# 以預設的工作階段名稱啟動
claude remote-control

# 以自訂名稱啟動
claude remote-control --name "Auth Refactor"
```

**在工作階段內**：

```
/remote-control
/remote-control "Auth Refactor"
```

**可用旗標**：

| 旗標 | 說明 |
|------|-------------|
| `--name "title"` | 自訂工作階段標題，方便識別 |
| `--verbose` | 顯示詳細的連線記錄 |
| `--sandbox` | 啟用檔案系統與網路隔離 |
| `--no-sandbox` | 停用沙箱（預設） |

### 連線到工作階段

有三種方式可以從其他裝置連線：

1. **工作階段 URL** — 工作階段啟動時會印在終端機上；用任何瀏覽器開啟即可
2. **QR code** — 啟動後按 `spacebar` 即可顯示可掃描的 QR code
3. **依名稱尋找** — 在 claude.ai/code 或 Claude 行動應用程式（iOS/Android）中瀏覽你的工作階段

### 安全性

- 你的機器上**不會開啟任何傳入連接埠**
- **僅有透過 TLS 的傳出 HTTPS** 流量
- **範圍受限的憑證** — 多組短效期、範圍狹窄的 token
- **工作階段隔離** — 每個遠端工作階段彼此獨立

### 遠端控制 vs. 網頁版 Claude Code

| 面向 | 遠端控制 | 網頁版 Claude Code |
|--------|---------------|-------------------|
| **執行位置** | 在你的機器上執行 | 在 Anthropic 雲端執行 |
| **本機工具** | 完整存取本機 MCP 伺服器、檔案與 CLI | 不依賴任何本機環境 |
| **使用情境** | 從其他裝置繼續本機的工作 | 從任何瀏覽器重新開始 |

### 限制

- 每個 Claude Code 執行個體只能有一個遠端工作階段
- 主控端機器上的終端機必須保持開啟
- 若網路無法連線，工作階段大約 10 分鐘後就會逾時

### 使用情境

- 不在座位上時，用行動裝置或平板控制 Claude Code
- 使用功能更豐富的 claude.ai 介面，同時仍在本機執行工具
- 在移動中也能用完整的本機開發環境快速做程式碼審查

### 推播通知（v2.1.110）

當遠端控制啟用中，且在 `/config` 中開啟「Push when Claude decides」時，Claude 就能把推播通知送到你的手機——例如當一個長時間任務完成，或需要你輸入時。

啟用方式：
1. 啟動遠端控制：`/remote-control` 或 `claude --rc`
2. 開啟 `/config` 並啟用 **Push when Claude decides**

推播通知需要 Claude 訂閱方案與 Claude 行動應用程式。

### 停用遠端控制（`disableRemoteControl`，v2.1.128+）

Team 或 Enterprise 方案的管理員可以用 `disableRemoteControl` 設定完全封鎖遠端控制。設為 `true` 時，`claude remote-control` 與 `/remote-control` 都會拒絕啟動。

```json
{
  "disableRemoteControl": true
}
```

這個設定會在**受管／政策**層級生效（例如 macOS 上的 `/Library/Application Support/ClaudeCode/managed-settings.json`），因此個別使用者無法覆蓋它。適合用在必須在整個組織強制僅限本機執行的情況。

> **API 金鑰方案會自動停用遠端控制（v2.1.139）**：只要設定了以下任何一項，遠端控制就會被**靜默停用**，即使你同時也用 claude.ai 登入：
>
> - `ANTHROPIC_API_KEY`
> - `ANTHROPIC_AUTH_TOKEN`
> - `apiKeyHelper`（settings.json）
>
> 同樣的條件也會停用 [`/schedule`](#排程任務)、claude.ai 的 MCP 連接器，以及通知偏好設定——這四個與 claude.ai 串接的介面，都要求作用中的憑證必須是 OAuth 登入。取消設定 API 金鑰（或改用 Pro/Max 的 OAuth 方案）即可使用這些功能。

---

## 網頁工作階段

網頁工作階段讓你可以直接在瀏覽器的 claude.ai/code 上執行 Claude Code，也可以從 CLI 建立網頁工作階段。

### 建立網頁工作階段

```bash
# 從 CLI 建立新的網頁工作階段
claude --remote "implement the new API endpoints"
```

這會在 claude.ai 上啟動一個 Claude Code 工作階段，你可以從任何瀏覽器存取。

### 在本機回復網頁工作階段

如果你在網頁上啟動了一個工作階段，想要在本機繼續：

```bash
# 在本機終端機中回復網頁工作階段——會開啟你的網頁工作階段選擇器
claude --teleport
```

或是在互動式 REPL 內：

```text
/teleport
```

`/tp` 是 `/teleport` 的別名。兩者都需要 claude.ai 訂閱方案。雲端工作階段會顯示
`/teleport` 的提示，說明如何在本機繼續（v2.1.223）。

> **來源：更新日誌**：v2.1.223 的更新日誌顯示有一種帶參數的形式
> `claude --teleport <session id>`，可以直接跳到已知的工作階段。CLI 參考文件只
> 記載了不帶參數的選擇器形式，所以除非你手上已經有工作階段 ID，否則建議使用
> `claude --teleport`。

### 使用情境

- 在一台機器上開始工作，在另一台機器上繼續
- 把工作階段 URL 分享給團隊成員
- 用網頁介面做視覺化的差異審查，再切換到終端機執行

---

## 桌面應用程式

Claude Code 桌面應用程式是一個獨立的應用程式，具備視覺化差異審查、平行工作階段，以及整合式連接器。支援 macOS 與 Windows（Pro、Max、Team 與 Enterprise 方案）。

### 安裝

從 [claude.ai](https://claude.ai) 下載適合你平台的版本：
- **macOS**：Universal 版本（支援 Apple Silicon 與 Intel）
- **Windows**：提供 x64 與 ARM64 安裝程式

設定說明請參閱[桌面版快速上手指南](https://code.claude.com/docs/en/desktop-quickstart)。

### 從 CLI 交接

把目前的 CLI 工作階段轉移到桌面應用程式：

```
/desktop
```

### 核心功能

| 功能 | 說明 |
|---------|-------------|
| **差異檢視** | 逐檔視覺化審查並可加上行內註解；Claude 會讀取註解並進行修訂 |
| **應用程式預覽** | 自動啟動開發伺服器，並用內嵌瀏覽器進行即時驗證 |
| **PR 監控** | 整合 GitHub CLI，可自動修正 CI 失敗，並在檢查通過時自動合併 |
| **平行工作階段** | 側邊欄可同時容納多個工作階段，並自動以 Git worktree 隔離 |
| **排程任務** | 應用程式開啟期間會執行的重複性任務（每小時、每天、平日、每週） |
| **豐富算繪** | 支援語法高亮的程式碼、Markdown 與圖表算繪；GitHub Flavored Markdown 的任務清單核取方塊（`- [ ]` / `- [x]`）會算繪成真正的核取方塊（v2.1.149+） |

### 應用程式預覽設定

在 `.claude/launch.json` 中設定開發伺服器的行為：

```json
{
  "command": "npm run dev",
  "port": 3000,
  "readyPattern": "ready on",
  "persistCookies": true
}
```

### 連接器

連接外部服務以取得更豐富的上下文：

| 連接器 | 功能 |
|-----------|------------|
| **GitHub** | PR 監控、Issue 追蹤、程式碼審查 |
| **Slack** | 通知、頻道上下文 |
| **Linear** | Issue 追蹤、Sprint 管理 |
| **Notion** | 文件、知識庫存取 |
| **Asana** | 任務管理、專案追蹤 |
| **Calendar** | 掌握行程、會議上下文 |

> **備註**：遠端（雲端）工作階段無法使用連接器。

### 遠端與 SSH 工作階段

- **遠端工作階段**：在 Anthropic 雲端基礎架構上執行；即使關閉應用程式也會繼續。可從 claude.ai/code 或 Claude 行動應用程式存取
- **SSH 工作階段**：透過 SSH 連線到遠端機器，完整存取遠端的檔案系統與工具。遠端機器上必須已安裝 Claude Code

### 桌面版的權限模式

桌面應用程式支援與 CLI 相同的權限模式：

| 模式 | 行為 |
|------|----------|
| **Ask permissions**（預設） | 審查並核准每一次編輯與指令 |
| **Auto accept edits** | 檔案編輯自動核准；指令仍需手動核准 |
| **Plan mode** | 在做出任何變更之前先審閱做法 |
| **Bypass permissions** | 自動執行（僅限沙箱，由管理員控制） |

### 企業功能

- **管理主控台**：控制整個組織的 Code 分頁存取權與權限設定
- **MDM 部署**：在 macOS 上透過 MDM 部署，Windows 上透過 MSIX 部署
- **SSO 整合**：要求組織成員使用單一登入
- **受管設定**：集中管理團隊設定與可用模型

---

## 任務清單

任務清單功能提供持久性的任務追蹤，即使經過上下文壓縮（對話紀錄被裁剪以符合上下文視窗）也不會消失。

### 切換任務清單

在工作階段中按 `Ctrl+T` 即可切換任務清單檢視的開關。

### 持久性任務

任務會跨上下文壓縮持續存在，確保對話上下文被裁剪時，長時間執行的工作項目不會遺失。這對複雜、多步驟的實作工作特別有用。

### 具名任務目錄

使用 `CLAUDE_CODE_TASK_LIST_ID` 環境變數，可以建立跨工作階段共用的具名任務目錄：

```bash
export CLAUDE_CODE_TASK_LIST_ID=my-project-sprint-3
```

這樣多個工作階段就能共用同一份任務清單，很適合團隊工作流程或多工作階段的專案。

---

## 提示詞建議

提示詞建議會依據你的 git 歷史紀錄與目前的對話上下文，顯示灰色的範例指令。

### 運作原理

- 建議會以灰色文字顯示在輸入提示詞的下方
- 按 `Tab` 可接受建議
- 按 `Enter` 可接受並立即送出
- 建議會依上下文而定，取材自 git 歷史紀錄與對話狀態

### 停用提示詞建議

```bash
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

---

## Git Worktree

Git Worktree 讓你可以在一個獨立的 worktree 中啟動 Claude Code，不必 stash 或切換分支，就能在不同分支上平行工作。

### 在 Worktree 中啟動

```bash
# 在獨立的 worktree 中啟動 Claude Code
claude --worktree
# 或者
claude -w
```

### Worktree 位置

Worktree 會建立在：
```
<repo>/.claude/worktrees/<name>
```

### Monorepo 的 Sparse Checkout

使用 `worktree.sparsePaths` 設定，可以在 monorepo 中執行 sparse checkout，減少磁碟用量與複製（clone）時間：

```json
{
  "worktree": {
    "sparsePaths": ["packages/my-package", "shared/"]
  }
}
```

### 基準分支參照（`worktree.baseRef`）

**`worktree.baseRef`**（v2.1.133 新增）— 控制 `claude --worktree` 要從 `origin/<default>` 還是本機 `HEAD` 建立分支。

- `"fresh"`（預設）— 從 `origin/<default-branch>` 建立分支，忽略本機尚未推送的提交。**這推翻了 v2.1.128 引入的行為**，因此若你在 v2.1.128 之後依賴本機 HEAD 建立分支，必須重新選擇加入。
- `"head"` — 從本機 `HEAD` 建立分支，保留尚未推送的提交。

在 `~/.claude/settings.json` 中設定：

```json
{ "worktree": { "baseRef": "head" } }
```

### 背景工作階段隔離（`worktree.bgIsolation`）

**`worktree.bgIsolation`**（v2.1.143 新增）— 控制背景工作階段（例如來自 `/bg`、`claude --bg`，或代理檢視畫面）要有自己的 worktree，還是直接編輯前景的工作副本。

- *（預設）* — 背景工作階段會在 `<repo>/.claude/worktrees/` 下建立獨立的 worktree，做法與 `--worktree` 相同。
- `"none"` — 背景工作階段會直接編輯目前的工作副本。適合在 worktree 不切實際時使用（例如原生建置產物很龐大），或是背景代理必須與前景工作階段協調編輯內容時。

```json
{ "worktree": { "bgIsolation": "none" } }
```

取捨：`"none"` 會移除 worktree 隔離這道安全網——背景與前景工作階段的並行編輯，可能會在正式使用中的工作副本裡產生合併衝突。

### Worktree 工具與 Hooks

| 項目 | 說明 |
|------|-------------|
| `EnterWorktree` | 用來進入 worktree 的工具；自 v2.1.157 起，可以在工作階段中途切換 Claude 管理的不同 worktree |
| `ExitWorktree` | 用來離開並清理目前 worktree 的工具 |
| `WorktreeCreate` | worktree 建立時觸發的 Hook 事件 |
| `WorktreeRemove` | worktree 移除時觸發的 Hook 事件 |

自 v2.1.157 起，代理完成工作後，由 Claude 管理的 worktree 會保持解鎖狀態，讓 `git worktree remove`／`prune` 可以清理它們。

### 自動清理

如果在 worktree 中沒有做任何變更，工作階段結束時會自動清理它。

### 使用情境

- 在功能分支上工作，同時不動到 main 分支
- 獨立執行測試，不影響工作目錄
- 在可拋棄的環境中嘗試實驗性的變更
- 對 monorepo 中特定的套件做 sparse checkout，加快啟動速度

---

## 沙箱

沙箱為 Claude Code 執行的 Bash 指令提供作業系統層級的檔案系統與網路隔離。這是權限規則之外的補充機制，提供多一層的安全性。

### 啟用沙箱

**斜線指令**：
```
/sandbox
```

**CLI 旗標**：
```bash
claude --sandbox       # 啟用沙箱
claude --no-sandbox    # 停用沙箱
```

### 設定選項

| 設定 | 說明 |
|---------|-------------|
| `sandbox.enabled` | 啟用或停用沙箱 |
| `sandbox.failIfUnavailable` | 若無法啟用沙箱則直接失敗 |
| `sandbox.filesystem.allowWrite` | 允許寫入的路徑 |
| `sandbox.filesystem.allowRead` | 允許讀取的路徑 |
| `sandbox.filesystem.denyRead` | 禁止讀取的路徑 |
| `sandbox.network.allowedDomains` | Bash 啟動的處理程序可以連到的網域（支援 `*.` 萬用字元） |
| `sandbox.network.deniedDomains` | 即使 `allowedDomains` 的萬用字元原本會允許，仍要封鎖的網域（v2.1.113+） |
| `sandbox.network.strictAllowlist` | （v2.1.219）不經詢問，直接拒絕沙箱指令連往不在允許清單中的主機 |
| `sandbox.enableWeakerNetworkIsolation` | 在 macOS 上啟用較弱的網路隔離 |
| `sandbox.bwrapPath` | （v2.1.133+，Linux/WSL）`bubblewrap` 執行檔的路徑。預設：從 `$PATH` 中尋找。 |
| `sandbox.socatPath` | （v2.1.133+，Linux/WSL）`socat` 執行檔的路徑。預設：從 `$PATH` 中尋找。 |
| `sandbox.credentials` | （v2.1.187+）封鎖沙箱指令讀取憑證檔案與機密環境變數。 |
| `sandbox.allowAppleEvents` | （v2.1.181+，macOS）選擇讓沙箱指令可以送出 Apple Events。 |
| `sandbox.filesystem.disabled` | （v2.1.216+）完全略過檔案系統隔離，但仍強制執行網路隔離——適合在檔案沙箱會弄壞工具鏈、但仍需維持網路連出控管時使用。只有使用者設定、受管設定或 `--settings` 才會生效；專案設定無法設定這個選項。 |

**Linux/WSL 執行檔路徑**（v2.1.133+）— 讓 Claude Code 指向非標準的安裝位置：

```json
{
  "sandbox": {
    "bwrapPath": "/opt/bubblewrap/bin/bwrap",
    "socatPath": "/opt/socat/bin/socat"
  }
}
```

`deniedDomains` 覆蓋廣泛萬用字元的範例（v2.1.113+）：

```json
{
  "sandbox": {
    "network": {
      "allowedDomains": ["*.example.com"],
      "deniedDomains": ["evil.example.com"]
    }
  }
}
```

這個萬用字元會放行 `example.com` 底下的所有東西，但 `deniedDomains` 仍會封鎖特別指名的那個主機。

> **備註**（v2.1.243）：沙箱化 Bash 工具的權限提示**不再列出允許的網路主機**。Claude 只會直接嘗試發出請求，每出現一個新主機你就核准一次——所以不要預期提示會事先秀出允許清單。同一版也修正了「被封鎖的指令剛好以 `0` 結束時，網路違規細節會被吞掉」的問題，所以現在即使看起來像是靜默成功，也仍會回報被封鎖的內容。

### 憑證遮罩（v2.1.221、v2.1.224）

> **來源：更新日誌**：這些 `sandbox.credentials` 選項來自 v2.1.221 與
> v2.1.224 的更新日誌條目；設定參考文件目前尚未詳細記載。

在 v2.1.221 之前，`sandbox.credentials` 只能 `deny`（拒絕）一個憑證檔案——需要用到
該憑證的沙箱指令就會直接失敗。`mode: "mask"` 能讓指令繼續運作，同時不外洩機密：
沙箱處理程序讀到的是檔案的**哨兵**（sentinel）副本，而沙箱代理伺服器（proxy）
會在資料送往網路的路上，把真正的值替換回去。

```json
{
  "sandbox": {
    "network": { "tlsTerminate": true },
    "credentials": {
      "files": [
        { "path": "~/.aws/credentials", "mode": "mask" }
      ]
    }
  }
}
```

| 功能 | 起始版本 | 作用 |
|---|---|---|
| 憑證**檔案**的 `mode: "mask"` | v2.1.221 | 沙箱指令讀到的是哨兵值；proxy 會在資料送出時換回真正的值。**僅限 Linux 與 WSL**——在 macOS 上，檔案遮罩會退回為 `deny`。 |
| `extract` / `onExtractNoMatch` | v2.1.224 | 只遮罩結構化環境變數值裡的其中一個欄位，而不是整個變數，並決定樣式不符時該怎麼處理。 |
| `decode: "jwt"` 搭配 `maskClaims` | v2.1.224 | 解碼 JWT，只遮罩指名的 claim，其餘保持可讀。 |
| `awsPairs` / `sigv4` | v2.1.224 | 在 proxy 換回真正的 access key 之後，重新簽署 AWS SigV4 請求。 |

**兩個容易被忽略的限制：**

- 所有遮罩都需要 `network.tlsTerminate`——proxy 必須能看到請求內部才能替換數值。
- 這些選項**只有**在使用者設定、受管設定或 `--settings` 中才會生效。專案設定無法
  開啟遮罩，也無法變更要遮罩的內容。

### 設定範例

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "filesystem": {
      "allowWrite": ["/Users/me/project"],
      "allowRead": ["/Users/me/project", "/usr/local/lib"],
      "denyRead": ["/Users/me/.ssh", "/Users/me/.aws"]
    },
    "enableWeakerNetworkIsolation": true
  }
}
```

### 運作原理

- Bash 指令會在受限的檔案系統存取環境中執行
- 網路存取可以被隔離，防止非預期的對外連線
- 與權限規則搭配運作，提供縱深防禦
- 在 macOS 上，網路限制請使用 `sandbox.enableWeakerNetworkIsolation`（macOS 上無法做到完整的網路隔離）

### 使用情境

- 安全地執行不受信任或自動產生的程式碼
- 避免意外修改到專案以外的檔案
- 限制自動化任務期間的網路存取

---

## 受管設定（企業版）

受管設定讓企業管理員可以用平台原生的管理工具，在整個組織中部署 Claude Code 的設定。

### 部署方式

| 平台 | 方法 | 起始版本 |
|----------|--------|-------|
| macOS | 受管 plist 檔案（MDM） | v2.1.51+ |
| Windows | Windows 登錄檔（Registry） | v2.1.51+ |
| 跨平台 | 受管設定檔案 | v2.1.51+ |
| 跨平台 | 受管 drop-in 檔案（`managed-settings.d/` 目錄） | v2.1.83+ |

### 受管 Drop-in 檔案

自 v2.1.83 起，管理員可以把多個受管設定檔案部署到 `managed-settings.d/` 目錄中。這些檔案會依字母順序合併，讓不同團隊可以做模組化的設定：

```
~/.claude/managed-settings.d/
  00-org-defaults.json
  10-team-policies.json
  20-project-overrides.json
```

### 可用的受管設定

| 設定 | 說明 |
|---------|-------------|
| `disableBypassPermissionsMode` | 防止使用者啟用略過權限模式 |
| `availableModels` | 限制使用者可以選擇的模型 |
| `enforceAvailableModels` | （v2.1.175）設為 `true` 時，`availableModels` 允許清單*也*會限制**預設**模型——如果設定的預設模型不在清單中，Claude Code 會退回使用清單中第一個允許的模型。使用者與專案設定不能再放寬受管的 `availableModels` 清單。 |
| `allowedChannelPlugins` | 控制允許使用哪些頻道外掛 |
| `autoMode.environment` | 為自動模式設定受信任的基礎架構 |
| `workflowSizeGuideline` | （v2.1.219）設定建議性質的[動態工作流程規模準則](#動態工作流程)。任何設定檔都能讀取，不限受管設定；只要有設定它，`/config` 中的 **Dynamic workflow size** 項目就會被隱藏 |
| `wslInheritsWindowsSettings` | 僅限 Windows/WSL（v2.1.118+）：設為 `true` 時，在 WSL 中執行的 Claude Code 會繼承 Windows 主機的受管設定，讓透過登錄檔／MDM 部署的企業政策，在 Windows 與 WSL 的 shell 中一致套用 |
| `parentSettingsBehavior` | （v2.1.133+，管理員層級）控制 SDK 的 `managedSettings` 如何與父處理程序的設定合併。`"first-wins"` 維持既有的優先順序（衝突時較早的設定勝出）；`"merge"` 則會做深度合併。 |
| 自訂政策 | 組織專屬的權限與工具政策 |

### 範例：macOS Plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>disableBypassPermissionsMode</key>
  <true/>
  <key>availableModels</key>
  <array>
    <string>claude-sonnet-4-6</string>
    <string>claude-haiku-4-5</string>
  </array>
</dict>
</plist>
```

---

## 設定與組態

### 設定檔案位置

1. **全域設定**：`~/.claude/config.json`
2. **專案設定**：`./.claude/config.json`
3. **使用者設定**：`~/.config/claude-code/settings.json`

### 完整設定範例

**核心進階功能設定：**

```json
{
  "permissions": {
    "defaultMode": "manual"
  },
  "hooks": {
    "PreToolUse:Edit": "eslint --fix ${file_path}",
    "PostToolUse:Write": "~/.claude/hooks/security-scan.sh"
  },
  "mcp": {
    "enabled": true,
    "servers": {
      "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"]
      }
    }
  }
}
```

**擴充設定範例：**

```json
{
  "permissions": {
    "defaultMode": "manual",
    "allowedTools": ["Bash(git log:*)", "Read"],
    "disallowedTools": ["Bash(rm -rf:*)"]
  },

  "hooks": {
    "PreToolUse": [{ "matcher": "Edit", "hooks": ["eslint --fix ${file_path}"] }],
    "PostToolUse": [{ "matcher": "Write", "hooks": ["~/.claude/hooks/security-scan.sh"] }],
    "Stop": [{ "hooks": ["~/.claude/hooks/notify.sh"] }]
  },

  "mcp": {
    "enabled": true,
    "servers": {
      "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {
          "GITHUB_TOKEN": "${GITHUB_TOKEN}"
        }
      }
    }
  }
}
```

### 其他個人設定

這些 key 放在 `~/.claude/settings.json`（或專案的 `.claude/settings.json`）中，用來控制個別使用者的互動行為：

| 設定 | 說明 |
|---------|-------------|
| `askUserQuestionTimeout` | 讓未回答的 `AskUserQuestion` 對話框，在閒置一段時間後自動繼續。自 **v2.1.200** 起，對話框預設不再自動繼續——設定這個項目即可重新選擇加入計時自動繼續。 |
| `enableArtifact` | 依個別使用者啟用／停用 Artifact 工具（v2.1.196）。 |
| `crossSessionInbound` |（v2.1.224）決定收到的[跨工作階段訊息](#跨工作階段訊息)如何處理——`"accept"`、`"hold"` 或 `"refuse"`。專案與本機的值只有在 `accept < hold < refuse` 這個階梯上*更嚴格*時才會生效。自 v2.1.232 起在 `/config` 中顯示為「Messages from your other sessions」。 |
| `dialogExpiry` |（v2.1.224）未回答的對話框要保持開啟多久。預設為 `"5m"`；可接受 `"60s"`、`"5m"`、`"10m"` 或 `"never"`。會被 `CLAUDE_CODE_USER_DIALOG_TIMEOUT_MS` 覆蓋。自 v2.1.232 起在 `/config` 中顯示為「Dialog expiry」。 |
| `modelPicker` |（v2.1.243）選擇 `/model` 選擇器要列出哪些模型，並自訂順序與標籤。這是少數在各層設定之間會**取代而非合併**的設定之一——最接近的層級的值會直接勝出。 |
| `promptCacheTtl` |（v2.1.243）選擇主對話的 Prompt 快取存活時間。 |
| `subagentPromptCacheTtl` |（v2.1.243）針對子代理與主對話以外其他請求的相同設定。 |
| `modelPricing` |（v2.1.243）**受管設定。** 提供你組織議定的費率，讓 `/cost`、狀態列與遙測回報的是這個費率，而不是牌價。 |
| `keybindingFlavor` | **自 v2.1.261 起已棄用，不再有作用。** 提示詞的單字編輯按鍵一律遵循 readline 慣例，與 Bash 相同：`Ctrl+W` 會刪到空白為止，`Alt+F` 與 `Alt+D` 在單字結尾處停下，標點符號會分隔單字。Claude Code 仍會接受這個 key，所以設定檔中有它仍然有效。（在 v2.1.238–v2.1.260 期間，它可在 `"classic"` 與 `"readline"` 之間選擇。） |
| `spellcheck` |（v2.1.235）用 `PATH` 上找得到的 `aspell`、`hunspell` 或 `ispell`（依序嘗試）為提示詞輸入中拼錯的單字加上底線。值為物件——`{"enabled": true, "language": "en_GB"}`——預設關閉。**只會從使用者設定、`--settings` 旗標與受管設定讀取**：專案 `.claude/settings.json` 或 `.claude/settings.local.json` 中的 `spellcheck` 區塊會被忽略。 |
| `bashOutputMaxChars` |（v2.1.261）**成功**的 Bash 或 PowerShell 指令輸出，Claude 可以內嵌收到多少字元，上限 128K。超過上限時，Claude Code 會把輸出存成檔案，Claude 只會拿到簡短預覽加上路徑。設定這個項目後，Claude Code 會忽略 `BASH_MAX_OUTPUT_LENGTH`。 |
| `taskOutputMaxChars` |（v2.1.261）用 `TaskOutput` 工具讀取**背景任務**輸出時，Claude 可以內嵌收到多少字元，上限 128K。對於更長的已完成任務，Claude 會收到最近的那部分字元。設定這個項目後，Claude Code 會忽略 `TASK_MAX_OUTPUT_LENGTH`。 |

### 備援模型（`fallbackModel`）

`fallbackModel` 設定讓你可以設定**最多三個**備援模型，在主要模型過載或無法使用時依序嘗試。

```json
{
  "fallbackModel": ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5"]
}
```

自 **v2.1.166** 起，`--fallback-model` 旗標也適用於互動式工作階段（不只是無介面模式）。發生備援時，Claude Code 會對非預期、原本不可重試的錯誤重試一次；驗證、速率限制、請求大小與傳輸層的錯誤仍會立即失敗。

### 環境變數

用環境變數覆寫設定：

```bash
# 模型選擇
export ANTHROPIC_MODEL=claude-opus-4-8
export ANTHROPIC_DEFAULT_MODEL=claude-opus-4-8   # (v2.1.236) 新工作階段一開始使用的模型。與 ANTHROPIC_MODEL 不同，用 /model 選擇仍然可以覆蓋它——而且這個選擇會跨重啟保留
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-8
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6
export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5

# API 設定
export ANTHROPIC_API_KEY=sk-ant-...

# 延伸思考設定
export MAX_THINKING_TOKENS=16000
export CLAUDE_CODE_EFFORT_LEVEL=high   # low、medium、high、xhigh（Opus 5/4.8/4.7）或 max——在 Opus 5 與 Opus 4.8 上預設為 high（Opus 5、Opus 4.8、Opus 4.7、Opus 4.6、Sonnet 4.6 皆支援）

# 功能開關
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=true
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=true
export CLAUDE_CODE_DISABLE_CRON=1
export CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=true
export CLAUDE_CODE_DISABLE_TERMINAL_TITLE=true
export CLAUDE_CODE_DISABLE_1M_CONTEXT=true
export CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK=true
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
export CLAUDE_CODE_ENABLE_TASKS=true
export CLAUDE_CODE_SIMPLE=true              # 由 --bare 旗標設定

# MCP 設定
export MAX_MCP_OUTPUT_TOKENS=50000
export ENABLE_TOOL_SEARCH=true

# Prompt 快取
export ENABLE_PROMPT_CACHING_1H=1      # 使用 1 小時的 Prompt 快取 TTL（預設為 5 分鐘）

# 任務管理
export CLAUDE_CODE_TASK_LIST_ID=my-project-tasks

# 代理團隊（實驗性）
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 子代理與外掛設定
export CLAUDE_CODE_SUBAGENT_MODEL=sonnet
export CLAUDE_CODE_PLUGIN_SEED_DIR=./my-plugins
export CLAUDE_CODE_NEW_INIT=1

# 子處理程序與串流
export CLAUDE_CODE_SUBPROCESS_ENV_SCRUB="SECRET_KEY,DB_PASSWORD"
export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=80
export CLAUDE_STREAM_IDLE_TIMEOUT_MS=30000
export ANTHROPIC_CUSTOM_MODEL_OPTION=my-custom-model
export SLASH_COMMAND_TOOL_CHAR_BUDGET=50000

# 輸出與套件管理員（v2.1.129+）
export CLAUDE_CODE_FORCE_SYNC_OUTPUT=1                      # 對自動偵測失效的終端機（Emacs eat 等）強制使用同步輸出
export CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1            # 為 Homebrew／WinGet 安裝啟用背景升級
export CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1         # 在設定 ANTHROPIC_BASE_URL 時，選擇加入 /v1/models 閘道探索

# Windows PowerShell 工具（v2.1.143+）— 在 Windows 上對 Bedrock/Vertex/Foundry 預設開啟
export CLAUDE_CODE_USE_POWERSHELL_TOOL=0                    # 完全停用 PowerShell 工具
export CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1    # 遵循系統的 ExecutionPolicy，而非使用 `-ExecutionPolicy Bypass`

# 工作負載身分聯合（v2.1.141+）
export ANTHROPIC_WORKSPACE_ID=ws_abc123                     # 當規則涵蓋多個工作區時，把聯合 token 的範圍限定在特定工作區

# Stop hook 安全上限（v2.1.143+）
export CLAUDE_CODE_STOP_HOOK_BLOCK_CAP=8                    # 工作階段因連續 Stop hook 封鎖而結束並顯示警告前的最大次數。設為 0 可停用此上限。

# 工作階段層級的派生上限（v2.1.212）
export CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION=200         # 每個工作階段 WebSearch 工具呼叫次數的上限，避免搜尋迴圈失控。預設為 200。

# 無障礙功能（v2.1.208）
export CLAUDE_AX_SCREEN_READER=1                            # 啟用純文字螢幕報讀算繪模式。效果與 --ax-screen-reader 或設定中的 "axScreenReader": true 相同。

# 較新的變數（v2.1.221–v2.1.234）— 來源為更新日誌；CLI 參考文件尚無環境變數專節
export CLAUDE_CODE_ENABLE_TODO_TOOLS=1                      # （v2.1.233）恢復待辦／任務追蹤工具（TaskCreate/Get/Update/List、TodoWrite），這些工具在 Opus 4.8、Sonnet 5、Fable 5、Mythos 5 及更新的模型上預設關閉
export CLAUDE_CODE_WEBFETCH_CACHE_TTL_MS=900000             # （v2.1.233）WebFetch URL 快取的 TTL。預設 15 分鐘。
export CLAUDE_CODE_TOOL_MEMORY_LIMIT=2G                     # （v2.1.233，Linux）套用在 Bash 指令上的選擇性加入記憶體 cgroup
export ANTHROPIC_BEDROCK_REGION_PREFIX=us                   # （v2.1.224）偏好特定的 Bedrock 跨區域推論設定檔
export CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1  # （v2.1.223）在無法辨識的模型 ID 上恢復 v2.1.223 之前的自動壓縮行為
export CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS=0             # （v2.1.229）停用動態工作流程扇出時的前綴錯開
export CLAUDE_CODE_USER_DIALOG_TIMEOUT_MS=300000            # （v2.1.224）覆蓋 dialogExpiry 設定
export CLAUDE_CODE_PROJECT_DIR_NAME=my-app                  # （v2.1.234）每個專案逐字稿目錄的簡短名稱，適用於為每個工作階段提供各自設定目錄的主機
export CLAUDE_CODE_GOAL_CHECKIN_MINUTES=30                  # （v2.1.234）在 /goal 進行中時，背景任務可以停滯多少分鐘後 Claude 才會來確認進度。設為 0 可停用確認進度。
```

> **v2.1.223 — `CLAUDE_CODE_DISABLE_1M_CONTEXT` 涵蓋範圍擴大**：這個變數現在適用於**所有**
> 原生具備 1M token 視窗、透過自動壓縮縮到 200K 的 Claude 模型，而不再只是固定的一份模型 ID 清單。

> **v2.1.108**：`ENABLE_PROMPT_CACHING_1H=1` — 使用 1 小時的 Prompt 快取 TTL，取代預設的 5 分鐘 TTL。可以減少長時間、穩定的工作階段中的快取未命中。（v2.1.129 修正了一個問題：1 小時 TTL 曾被靜默降級為 5 分鐘。）

> **v2.1.129**：`CLAUDE_CODE_FORCE_SYNC_OUTPUT=1` 會對能力自動偵測失敗的終端機（例如 Emacs `eat`）強制使用同步輸出。`CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1` 會為 Homebrew/WinGet 安裝啟用背景升級，否則這些安裝方式永遠不會自動更新。

### 設定管理指令

```
User: /config
[開啟互動式設定選單]
```

`/config` 指令提供一個互動式選單，可以切換以下這類設定：
- 延伸思考開／關
- 詳細輸出
- 權限模式
- 模型選擇
- 動態工作流程規模（v2.1.219）— 當設定檔中設定了 `workflowSizeGuideline` 時會被隱藏，參見[動態工作流程](#動態工作流程)

在互動式選單中，按 Enter 或 Space 可以變更選取的設定，按 Esc 可以儲存並關閉（v2.1.183+）。

你也可以直接從提示詞設定，不必開啟選單：

```bash
/config thinking=false      # 直接內嵌設定單一項目（v2.1.181+）
/config --help              # 列出可用的簡寫 key（v2.1.183+）
```

`key=value` 這種簡寫在互動式工作階段、搭配 `-p`，以及在遠端控制中都能使用。

### 依專案設定

在你的專案中建立 `.claude/config.json`：

```json
{
  "hooks": {
    "PreToolUse": [{ "matcher": "Bash", "hooks": ["npm test && npm run lint"] }]
  },
  "permissions": {
    "defaultMode": "manual"
  },
  "mcp": {
    "servers": {
      "project-db": {
        "command": "mcp-postgres",
        "env": {
          "DATABASE_URL": "${PROJECT_DB_URL}"
        }
      }
    }
  }
}
```

---

## 信任與權限範圍

> **來源：更新日誌（v2.1.222、v2.1.232）**：這些收緊措施來自更新日誌；
> 設定參考文件目前尚未詳細說明。

近期版本反覆出現一個主題：與安全性相關的設定，不能再被你複製下來的儲存庫放寬。
以下是三個你該知道的變更。

**巢狀儲存庫需要各自確認信任（v2.1.232）。** 位在受信任父目錄底下的 git 儲存庫，
不再自動繼承那份信任。如果你信任 `~/work/monorepo`，而它裡面有一個 vendored 的
子模組，Claude Code 第一次在該子模組中工作時，還是會另外請你確認信任。

**`sandbox.ripgrep` 僅限使用者層級（v2.1.232）。** 這個指定沙箱要用哪個 ripgrep
執行檔的設定，只會從使用者設定、受管設定或 `--settings` 中生效。專案設定不能再
讓沙箱指向另一個執行檔。

**遠端控制自動啟動僅限使用者層級（v2.1.222）。** 儲存庫本機的設定無法啟用遠端
控制自動啟動；這項功能只能透過 `/config` 在使用者層級開啟。

值得內化的原則是：如果某個設定會讓一個已提交（checked-in）的檔案，擴大 Claude
Code 在你機器上被允許做的事，就該假設它現在僅限使用者層級。

---

## 代理團隊

代理團隊（Agent Teams）是一項實驗性功能，能讓多個 Claude Code 執行個體協作完成一項任務。預設為停用。

### 啟用代理團隊

可透過環境變數或設定啟用：

```bash
# 環境變數
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

或加到你的設定 JSON 中：

```json
{
  "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
}
```

### 代理團隊如何運作

- **團隊負責人（team lead）** 統籌整個任務，並把子任務指派給隊友
- **隊友（teammates）** 各自獨立工作，各有自己的上下文視窗
- **共用任務清單** 讓團隊成員之間可以自行協調
- 用子代理定義（`.claude/agents/` 或 `--agents` 旗標）來定義隊友的角色與專長

### 顯示模式

代理團隊支援兩種顯示模式，可用 `--teammate-mode` 旗標設定：

| 模式 | 說明 |
|------|-------------|
| `in-process`（預設） | 隊友在同一個終端機處理程序內執行 |
| `tmux` | 每個隊友都有專屬的分割視窗（需要 tmux 或 iTerm2） |
| `auto` | 自動選擇最合適的顯示模式 |

```bash
# 用 tmux 分割視窗顯示隊友
claude --teammate-mode tmux

# 明確指定使用 in-process 模式
claude --teammate-mode in-process
```

### 使用情境

- 大型重構任務，讓不同隊友負責不同模組
- 平行進行程式碼審查與實作
- 跨程式碼庫、需要協調的多檔案變更

> **備註**：代理團隊是實驗性功能，未來版本可能會有所變動。完整參考請見 [code.claude.com/docs/en/agent-teams](https://code.claude.com/docs/en/agent-teams)。

---

## 最佳實踐

### 規劃模式
- ✅ 用於複雜的多步驟任務
- ✅ 核准前先審閱計畫
- ✅ 需要時修改計畫
- ❌ 不要用在簡單的任務上

### 延伸思考
- ✅ 用於架構決策
- ✅ 用於複雜的問題解決
- ✅ 檢視思考過程
- ❌ 不要用在簡單的查詢上

### 背景任務
- ✅ 用於長時間執行的操作
- ✅ 監控任務進度
- ✅ 妥善處理任務失敗
- ❌ 不要同時啟動太多並行任務

### 權限
- ✅ 程式碼審查（唯讀）用 `plan`
- ✅ 互動式開發用 `default`
- ✅ 自動化工作流程用 `acceptEdits`
- ✅ 需要安全防護的自主工作用 `auto`
- ❌ 除非絕對必要，否則不要使用 `bypassPermissions`

### 工作階段
- ✅ 不同任務用不同的工作階段
- ✅ 儲存重要的工作階段狀態
- ✅ 清理舊的工作階段
- ❌ 不要在同一個工作階段裡混雜不相關的工作

---

## 延伸資源

想了解更多關於 Claude Code 與相關功能的資訊：

- [官方互動模式文件](https://code.claude.com/docs/en/interactive-mode)
- [官方無介面模式文件](https://code.claude.com/docs/en/headless)
- [CLI 參考](https://code.claude.com/docs/en/cli-reference)
- [檢查點（Checkpoints）指南](../08-checkpoints/) - 工作階段管理與回溯
- [斜線指令](../01-slash-commands/) - 指令參考
- [記憶（Memory）指南](../02-memory/) - 持久上下文
- [技能指南](../03-skills/) - 自主能力
- [子代理指南](../04-subagents/) - 委派任務執行
- [MCP 指南](../05-mcp/) - 外部資料存取
- [Hooks 指南](../06-hooks/) - 事件驅動自動化
- [外掛指南](../07-plugins/) - 套件化擴充功能
- [官方排程任務文件](https://code.claude.com/docs/en/scheduled-tasks)
- [官方 Chrome 整合文件](https://code.claude.com/docs/en/chrome)
- [官方遠端控制文件](https://code.claude.com/docs/en/remote-control)
- [官方鍵盤綁定文件](https://code.claude.com/docs/en/keybindings)
- [官方桌面應用程式文件](https://code.claude.com/docs/en/desktop)
- [官方代理團隊文件](https://code.claude.com/docs/en/agent-teams)

---

**最後更新**：2026 年 9 月 6 日
**Claude Code 版本**：2.1.263
**資料來源**：
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/sandboxing
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/cli-reference
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/permission-modes
- https://code.claude.com/docs/en/settings.md
- https://code.claude.com/docs/en/settings-reference
- https://code.claude.com/docs/en/whats-new/2026-w34
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
