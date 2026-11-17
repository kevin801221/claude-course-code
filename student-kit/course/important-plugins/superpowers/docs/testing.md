# 測試 Superpowers 技能 (Testing Superpowers Skills)

本文件描述了如何測試 Superpowers 技能，特別是針對複雜技能（如 `subagent-driven-development`）的整合測試（Integration Tests）。

## 概述

測試涉及子代理（Subagents）、工作流（Workflows）和複雜交互的技能，需要以無頭模式（Headless Mode）運行實際的 Claude Code Session，並透過分析對話紀錄（Session Transcripts）來驗證其行為。

## 測試目錄結構

```
tests/
├── claude-code/
│   ├── test-helpers.sh                    # 共享測試公用工具
│   ├── test-subagent-driven-development-integration.sh
│   ├── analyze-token-usage.py             # Token 用量分析工具
│   └── run-skill-tests.sh                 # 測試執行器（若存在）
```

## 執行測試

### 整合測試

整合測試會配合實際的技能，執行真實的 Claude Code Session：

```bash
# 執行 subagent-driven-development 整合測試
cd tests/claude-code
./test-subagent-driven-development-integration.sh
```

> [!NOTE]
> 整合測試可能需要 10 到 30 分鐘，因為它們需要配合多個子代理（Subagents）來執行真實的實作計畫。

### 環境要求

- 必須在 **superpowers 插件目錄**中執行（不能在臨時目錄中執行）。
- 必須安裝 Claude Code，且 `claude` 指令在環境變數中可用。
- 必須在 `~/.claude/settings.json` 的 `enabledPlugins` 中啟用本地開發插件市場：`"superpowers@superpowers-dev": true`。

## 整合測試：subagent-driven-development

### 測試範疇

整合測試會驗證 `subagent-driven-development` 技能是否能正確執行以下行為：

1. **載入計畫 (Plan Loading)**：在開始時讀取一次計畫。
2. **完整任務描述 (Full Task Text)**：為子代理提供完整的任務描述（不需要子代理自己去讀取檔案）。
3. **自我審查 (Self-Review)**：確保子代理在回報結果之前，先進行自我程式碼審查。
4. **評審順序 (Review Order)**：在執行程式碼品質（Code Quality）審查之前，先運行規格合規性（Spec Compliance）審查。
5. **評審循環 (Review Loops)**：在發現問題時，啟動評審循環進行修正。
6. **獨立驗證 (Independent Verification)**：規格評審員會獨立讀取並驗證代碼，而不僅僅信任實作者報告的內容。

### 運作原理

1. **環境設定 (Setup)**：建立一個包含極簡實作計畫的臨時 Node.js 專案。
2. **執行開發 (Execution)**：在無頭模式下執行 Claude Code 並載入此技能。
3. **行為驗證 (Verification)**：解析對話紀錄（`.jsonl` 檔案）以驗證：
   - 是否調用了 `Skill` 工具。
   - 是否指派了子代理（調用了 `Task` 工具）。
   - 是否使用了 `TodoWrite` 來進行任務追蹤。
   - 實作的檔案是否被正確建立。
   - 測試是否全部通過。
   - Git commit 歷史是否展現了正確的工作流。
4. **Token 分析 (Token Analysis)**：展示每個子代理所消耗的 Token 詳細細目。

### 測試輸出範例

```
========================================
 Integration Test: subagent-driven-development
========================================

Test project: /tmp/tmp.xyz123

=== Verification Tests ===

Test 1: Skill tool invoked...
  [PASS] subagent-driven-development skill was invoked

Test 2: Subagents dispatched...
  [PASS] 7 subagents dispatched

Test 3: Task tracking...
  [PASS] TodoWrite used 5 time(s)

Test 6: Implementation verification...
  [PASS] src/math.js created
  [PASS] add function exists
  [PASS] multiply function exists
  [PASS] test/math.test.js created
  [PASS] Tests pass

Test 7: Git commit history...
  [PASS] Multiple commits created (3 total)

Test 8: No extra features added...
  [PASS] No extra features added

=========================================
 Token Usage Analysis
=========================================

Usage Breakdown:
----------------------------------------------------------------------------------------------------
Agent           Description                          Msgs      Input     Output      Cache     Cost
----------------------------------------------------------------------------------------------------
main            Main session (coordinator)             34         27      3,996  1,213,703 $   4.09
3380c209        implementing Task 1: Create Add Function     1          2        787     24,989 $   0.09
34b00fde        implementing Task 2: Create Multiply Function     1          4        644     25,114 $   0.09
3801a732        reviewing whether an implementation matches...   1          5        703     25,742 $   0.09
4c142934        doing a final code review...                    1          6        854     25,319 $   0.09
5f017a42        a code reviewer. Review Task 2...               1          6        504     22,949 $   0.08
a6b7fbe4        a code reviewer. Review Task 1...               1          6        515     22,534 $   0.08
f15837c0        reviewing whether an implementation matches...   1          6        416     22,485 $   0.07
----------------------------------------------------------------------------------------------------

TOTALS:
  Total messages:         41
  Input tokens:           62
  Output tokens:          8,419
  Cache creation tokens:  132,742
  Cache read tokens:      1,382,835

  Total input (incl cache): 1,515,639
  Total tokens:             1,524,058

  Estimated cost: $4.67
  (at $3/$15 per M tokens for input/output)

========================================
 Test Summary
========================================

STATUS: PASSED
```

## Token 用量分析工具

### 使用方法

你可以使用此工具分析任何 Claude Code Session 的 Token 消耗情況：

```bash
python3 tests/claude-code/analyze-token-usage.py ~/.claude/projects/<project-dir>/<session-id>.jsonl
```

### 尋找對話紀錄檔案

對話紀錄儲存在 `~/.claude/projects/` 底下，其目錄名稱是工作路徑經過編碼後的字串：

```bash
# 例如以 /Users/yourname/Documents/GitHub/superpowers/superpowers 為工作目錄：
SESSION_DIR="$HOME/.claude/projects/-Users-yourname-Documents-GitHub-superpowers-superpowers"

# 尋找最近的對話紀錄
ls -lt "$SESSION_DIR"/*.jsonl | head -5
```

### 分析報告內容

- **主對話用量 (Main session usage)**：協調者（你或主要的 Claude 實例）所消耗的 Token。
- **子代理細目 (Per-subagent breakdown)**：每次調用 Task 的詳細數據，包含：
  - 代理 ID (Agent ID)
  - 任務描述（從提示詞中提取）
  - 訊息數量
  - 輸入與輸出 Token 數
  - 快取（Cache）使用量
  - 預估花費成本
- **總計 (Totals)**：整體的 Token 使用總量與成本預估。

### 解讀分析數據

- **高快取讀取量 (High cache reads)**：好現象 —— 這代表 Prompt Caching（提示詞快取）運作良好，能大幅降低成本。
- **主對話有極高的輸入 Token**：符合預期 —— 協調者需要掌握全局的上下文。
- **每個子代理的花費成本相近**：符合預期 —— 每個子代理分派到的任務複雜度類似。
- **單個任務成本**：視複雜度而定，每個子代理的典型成本在 $0.05 到 $0.15 美元之間。

## 故障排除

### 技能無法載入

**問題**：在運行無頭測試時找不到技能。

**解決方案**：
1. 確保你是在 superpowers 目錄中執行測試：`cd /path/to/superpowers && tests/...`
2. 檢查 `~/.claude/settings.json` 的 `enabledPlugins` 內是否正確加入了 `"superpowers@superpowers-dev": true`。
3. 驗證技能是否確實存在於 `skills/` 目錄下。

### 權限錯誤

**問題**：Claude 被阻止寫入檔案或存取目錄。

**解決方案**：
1. 使用 `--permission-mode bypassPermissions` 參數。
2. 使用 `--add-dir /path/to/temp/dir` 參數來手動授予對測試目錄的存取權限。
3. 檢查測試目錄的檔案系統權限。

### 測試逾時 (Timeouts)

**問題**：測試執行時間過長而導致逾時。

**解決方案**：
1. 增加逾時限制：`timeout 1800 claude ...`（30分鐘）。
2. 檢查技能邏輯中是否存在無窮迴圈（Infinite loops）。
3. 重新檢視並簡化子代理的任務複雜度。

### 找不到對話紀錄檔案

**問題**：測試運行結束後找不到 `.jsonl` 對話紀錄。

**解決方案**：
1. 檢查 `~/.claude/projects/` 底下的專案路徑是否正確。
2. 使用 `find ~/.claude/projects -name "*.jsonl" -mmin -60` 來尋找最近一小時內建立的對話紀錄。
3. 驗證測試是否確實成功啟動並運行（檢查測試輸出的錯誤訊息）。

## 編寫新的整合測試

### 測試模板

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

# 建立臨時測試專案
TEST_PROJECT=$(create_test_project)
trap "cleanup_test_project $TEST_PROJECT" EXIT

# 設定測試檔案...
cd "$TEST_PROJECT"

# 配合技能運行 Claude Code
PROMPT="在此填寫你的測試提示詞"
cd "$SCRIPT_DIR/../.." && timeout 1800 claude -p "$PROMPT" \
  --allowed-tools=all \
  --add-dir "$TEST_PROJECT" \
  --permission-mode bypassPermissions \
  2>&1 | tee output.txt

# 尋找並分析 Session 檔案
WORKING_DIR_ESCAPED=$(echo "$SCRIPT_DIR/../.." | sed 's/\\//-/g' | sed 's/^-//')
SESSION_DIR="$HOME/.claude/projects/$WORKING_DIR_ESCAPED"
SESSION_FILE=$(find "$SESSION_DIR" -name "*.jsonl" -type f -mmin -60 | sort -r | head -1)

# 透過解析 Session 對話紀錄來驗證行為
if grep -q '"name":"Skill".*"skill":"your-skill-name"' "$SESSION_FILE"; then
    echo "[PASS] 技能已成功調用"
fi

# 顯示 Token 分析
python3 "$SCRIPT_DIR/analyze-token-usage.py" "$SESSION_FILE"
```

### 最佳實踐

1. **務必清理環境**：使用 `trap` 指令確保在測試結束（不論成功或失敗）時，自動清理臨時目錄。
2. **解析對話紀錄**：不要去 grep 使用者端的可讀輸出，而是解析 `.jsonl` 格式的底層對話紀錄，這更準確且不易出錯。
3. **授權權限**：使用 `--permission-mode bypassPermissions` 和 `--add-dir` 來避免交互式權限詢問。
4. **在插件目錄執行**：技能只有在從 superpowers 目錄啟動 Claude 時才會被正確載入。
5. **分析 Token**：務必在測試結尾輸出 Token 分析，這能提供極佳的成本透明度。
6. **測試真實行為**：驗證檔案是否真的被建立、測試是否通過，以及 Git commits 是否按規範生成。

## 對話紀錄格式

對話紀錄是 JSONL（JSON Lines）格式，每一行都是一個 JSON 物件，代表一條訊息或一個工具執行結果。

### 核心欄位範例

```json
{
  "type": "assistant",
  "message": {
    "content": [...],
    "usage": {
      "input_tokens": 27,
      "output_tokens": 3996,
      "cache_read_input_tokens": 1213703
    }
  }
}
```

### 工具執行結果範例

```json
{
  "type": "user",
  "toolUseResult": {
    "agentId": "3380c209",
    "usage": {
      "input_tokens": 2,
      "output_tokens": 787,
      "cache_read_input_tokens": 24989
    },
    "prompt": "You are implementing Task 1...",
    "content": [{"type": "text", "text": "..."}]
  }
}
```

其中 `agentId` 欄位會關聯到子代理（Subagent）的 Session，而 `usage` 欄位則包含該次子代理調用所消耗的 Token 數量。
