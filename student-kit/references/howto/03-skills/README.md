<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Agent Skills 指南

## 概覽

Skills 是可以複用、可自動觸發的能力包。一個 skill 通常包含 `SKILL.md`、參考檔案、指令碼和模板。Claude 在合適的場景下會自動載入它。

### 主要好處

- 可複用
- 可漸進載入
- 可以把指令碼、模板、說明放在一起
- 適合標準化流程

## Skills 的工作方式：漸進式披露

Skills 不會一次性把所有內容都塞進上下文，而是按需載入。

### 三層載入

1. **只看描述**：先判斷這個 skill 是否相關
2. **載入 `SKILL.md`**：讀取核心說明
3. **按需載入支援檔案**：指令碼、模板、參考資料

## Skill 載入流程

1. Claude 掃描技能目錄
2. 根據描述判斷是否匹配當前任務
3. 讀取 `SKILL.md`
4. 如有需要，再載入指令碼和輔助檔案

## Skill 型別與位置

Skills 可以放在：

- 專案目錄下的 `.claude/skills/`
- 使用者目錄下的 `~/.claude/skills/`

### 自動發現

只要目錄結構正確，Claude 就會自動發現這些 Skills。

## 建立自訂 Skills

### 基本目錄結構

```text
my-skill/
└── SKILL.md
```

### `SKILL.md` 格式

```yaml
---
name: my-skill
description: 這個 skill 的用途，以及什麼時候觸發
---

# Your Skill Name

## Instructions

## Examples
```

### 推薦欄位

- `description`（推薦）：說明這個 skill 做什麼、什麼時候用；Claude 就是靠它判斷是否啟用
- `name`（可選）：省略時預設取 skill 的目錄名

### 可選 frontmatter 欄位

- `argument-hint`
- `allowed-tools`
- `model`
- `disable-model-invocation`
- `user-invocable`
- `context`
- `agent`
- `hooks`

## Skill 內容型別

### 參考內容

適合放規則、標準、文件片段和範例。

### 任務內容

適合放具體步驟、執行流程和結果格式要求。

## 控制 Skill 的呼叫

你可以透過 `disable-model-invocation`、`user-invocable` 和工具白名單來控制 Claude 是否能自動呼叫這個 skill。

## 字串替換

Skills 支援 `$ARGUMENTS`、`$0`、`$1` 等引數替換。

### 動態上下文注入

你可以在 prompt 裡插入 shell 命令結果：

> **注意（v2.1.299）**：`UserPromptSubmit` hooks 會在命令展開之前執行，因此阻止該 prompt 的 hook 也會阻止這些 `!` 命令執行。

```md
- 當前 git 狀態：!`git status`
- 當前 diff：!`git diff HEAD`
- 當前分支：!`git branch --show-current`
```

## 在 subagent 中執行 Skills

某些 skill 適合在隔離上下文中執行，這樣可以降低對主會話的影響。

## 實戰範例

### 範例 1：程式碼審查 Skill

一個典型的審查 skill 會包含：

- 審查模板
- 風險等級
- 輸出格式
- 需要關注的維度

### 範例 2：程式碼庫視覺化 Skill

可以把程式碼庫結構、依賴關係和模組邊界總結給 Claude，便於快速理解。

### 範例 3：部署 Skill（只允許使用者觸發）

適合帶副作用的操作，比如正式環境部署。通常會配合 `disable-model-invocation: true`。

### 範例 4：品牌語氣 Skill

用於檢查輸出是否符合品牌語氣、語調和表達風格。

### 範例 5：`CLAUDE.md` 生成 Skill

可以從專案文件中生成或補充 `CLAUDE.md`。

### 範例 6：帶指令碼的重構 Skill

常見組合是：

- `SKILL.md`
- `scripts/`
- `templates/`
- `references/`

## 管理 Skills

### 檢視可用 Skills

```bash
/skills
```

### 測試一個 Skill

把它放到測試目錄或者臨時專案裡，然後透過相應命令觸發。

### 更新 Skill

修改 `SKILL.md` 或支援檔案後，重新開啟會話或重新載入即可。

### 限制 Claude 對 Skill 的訪問

你可以透過許可權設定，只允許 Claude 訪問某些 skill。

## 最佳實踐

### 1. 描述要具體

讓 `description` 明確說明這個 skill 在什麼時候觸發。

### 2. 保持聚焦

一個 skill 解決一個問題，不要什麼都塞進去。

### 3. 包含觸發詞

在描述裡加入相關關鍵詞，幫助 Claude 更準確地選擇它。

### 4. `SKILL.md` 不要太長

儘量控制在 500 行以內，超過就拆分支援檔案。

### 5. 引用支援檔案

把重複內容移到指令碼或參考檔案中，主檔案只保留核心說明。

## 故障排查

### 快速參考

- 檢查目錄結構是否正確
- 檢查 `SKILL.md` frontmatter 是否有效
- 檢查 skill 名稱是否和呼叫名一致

### Skill 沒有觸發

- 檢查描述是否足夠具體
- 檢查目錄是否在 Claude 可見範圍內
- 檢查是否被更高優先順序的 skill 覆蓋

### Skill 觸發太頻繁

- 收緊描述
- 增加約束條件
- 用更具體的觸發詞

### Claude 看不到全部 Skills

- 檢查路徑
- 檢查許可權
- 重新載入會話

## 安全注意事項

- 不要在 skill 中硬編碼金鑰
- 對副作用操作保持使用者觸發
- 給自動觸發的 skill 設定清晰邊界

## Skills vs 其他功能

| 功能 | 觸發方式 | 適合場景 |
|------|----------|----------|
| Skills | 自動/半自動 | 複用能力、流程標準化 |
| Slash Commands | 手動 | 快捷命令 |
| Subagents | 自動委派 | 隔離任務 |
| Hooks | 事件觸發 | 自動化和驗證 |

## 內建 Skills

Claude Code 自帶一些 Skills，例如批處理、除錯、簡化和 Claude API 相關內容。

## 共享 Skills

### 專案 Skills（團隊共享）

把 skill 放在專案目錄裡，團隊成員都能用。

### 個人 Skills

```bash
# 複製到個人目錄
mkdir -p ~/.claude/skills

# 讓指令碼可執行
chmod +x ~/.claude/skills/*/scripts/*
```

### Plugin 分發

你也可以把 Skills 作為外掛的一部分發布出去。

## 繼續深入

如果你要管理一整套 Skills，可以再做一個 skill collection 或 skill manager，用來統一發現、更新和分發。

## 更多資源

- [根目錄中文指南](../README.md)
- [Slash Commands 中文參考](../01-slash-commands/README.md)
- [Memory 中文指南](../02-memory/README.md)
- [Subagents 中文參考](../04-subagents/README.md)

---

**最後更新**: 2026 年 10 月 15 日
**Claude Code 版本**: 2.1.300
**來源**:
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/hooks#hook-lifecycle
- https://code.claude.com/docs/en/changelog#2-1-299
