# Lab 11：讀懂一個 Mods 流程引擎

對應講義 Part 14「Plugins / Mods＋Lab」。建議先完成傳統 Hooks、Plugins 與 Sub-agents 的練習，再用約 40 分鐘做這個進階選修。

素材在 [advanced/matt-flow-mods](../../advanced/matt-flow-mods/README.md)，完整說明見[學生導讀](../../advanced/matt-flow-mods/STUDENT-GUIDE.md)。保留的 TypeScript/TSX 與原測試來自同一份 `0.7.0` 快照。

## 目標

能解釋 Mods 如何同時管理狀態、攔截工具呼叫、注入上下文與顯示面板，並提出一組可驗收的測試案例。Mods 依 CLI 版本與執行環境而定；此 Lab 預設用原碼推演完成，不會替你安裝或啟用外掛。

此快照已在 macOS、Claude Code `2.1.319` 跑過原測試：**76 pass / 0 fail**，約 1.96 秒。測試使用隔離設定，沒有真人 UI 操作、模型呼叫，亦沒有變更使用者 history／trust；完整型別編譯與外部 Matt Skills 互動仍未驗證。

## 練習步驟

1. 讀 `types/index.d.ts`，把 `Progress` 欄位分成「本次功能」與「跨功能保存」。指出未開始的步驟在資料中如何表示。
2. 在 `hooks/register.tsx` 找 `LEVELS`、`judge`、`moveOnto`、`noteRan`，推演新手從 grilling 到 build 的過程。記下人輸入指令和 AI 呼叫 Skill 的差別。
3. 對照 `codeGate`、`commitGate`，列出「開始實作前寫 src」、「寫 docs」、「實作中尚未 review 就 commit」三個操作的預期結果。
4. 找 `revive`、`reread`、`railPrompt`，說明為什麼 `/clear` 不該解除程式碼關卡，以及如何把丟掉的流程說明補回去。
5. 從原測試挑一個 skip 或 end 案例，畫出修改前後的 `steps`、`feature`、`isReviewed`、`features`。這個版本沒有 `/matt-flow reset`；請分辨清對話、結束功能與關閉軌道。

## 可交作業的驗收表

| 情境 | 預期證據 |
| --- | --- |
| 未做 setup 的專案 | 軌道安靜，不攔截工具。 |
| 新手做完 setup，直接輸入 `/implement` | 跳過 grilling，指令被拒絕，狀態未進入 build。 |
| `/matt-flow skip` 後查看狀態 | grilling 是 `skipped`，不是 `passed`，也未直接進入 build。 |
| 新手開始 build，尚未 code-review | 程式碼可寫，Claude 的專案 commit 仍被擋。 |
| `/clear` 後在開始 build 前嘗試 Edit | 從持久 store 恢復後仍被擋。 |
| retro 已開始再 `/matt-flow end` | 本次功能清空、完成數加一；若 retro 未開始，記為中止。 |

每列填入「找到的函式／測試名稱」及「你觀察或推演的狀態」。自行重跑原測試可標為「引擎測試工具驗證」；只讀原碼則標為「靜態推演」。真人操作 UI 的結果另外記錄。

## 重跑原測試

在精華包根目錄執行：

```sh
CLAUDE_CONFIG_DIR=/private/tmp/claude-course-kit-validation claude plugin test advanced/matt-flow-mods
```

預期摘要為 76 個測試通過、0 失敗。這使用 `claude-code/testing` 與測試檔的模擬引擎事件，不需要呼叫模型；`CLAUDE_CONFIG_DIR` 將測試設定隔離於暫存目錄。請記下自己的 CLI 版本與實際輸出，版本不支援時改做靜態推演。

加分：針對多 session 同時更新 store 的競爭，或 Bash 寫檔不經 `codeGate` 的限制，寫出一個失敗案例。這套導航是流程護欄，不提供完整的工具安全隔離。

## 環境足夠時的延伸

由老師先確認該 CLI 支援 Mods 與相關子命令，再按[學生導讀的環境表](../../advanced/matt-flow-mods/STUDENT-GUIDE.md)做額外的 validate、型別編譯或真人互動驗收。上述 test 通過不代表這些額外項目也已驗證。`scripts/typecheck` 與 `scripts/live-check` 印出 `skipped` 不算驗證成功；live-check 會真正開 Claude session 並呼叫模型，需在隔離的示範專案進行。
