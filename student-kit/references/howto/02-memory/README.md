<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Memory 指南

## 概覽

Memory 讓 Claude Code 在不同會話之間保留上下文。你可以把團隊規範、專案規則、個人偏好和目錄級約束寫進 `CLAUDE.md`，讓 Claude 在合適的時候自動載入。

## Memory 命令速查

| 命令 | 作用 |
|------|------|
| `/init` | 初始化專案級 `CLAUDE.md` |
| `/memory` | 開啟並編輯記憶檔案 |
| `#` | 快速把當前規則寫入 memory |

## 快速上手：初始化 Memory

### 使用 `/init`

在專案目錄中執行：

```bash
/init
```

Claude 會根據當前專案生成一個 `CLAUDE.md`，通常包含類似如下結構：

```md
# 專案設定
## 專案概覽
## 開發規範
```

### 使用 `#` 快速更新記憶

當你想把一句規則寫入 memory 時，可以直接在輸入前加 `#`：

```text
# 這個專案始終使用 TypeScript 嚴格模式
# 優先使用 async/await，而不是 promise 鏈
# 每次提交前都執行 npm test
# 檔名統一使用 kebab-case
```

這會把規則加入當前會話能感知到的記憶中。

### 使用 `/memory`

`/memory` 會開啟記憶編輯器，讓你在不同範圍之間切換：

1. 受管策略記憶
2. 專案記憶（`./CLAUDE.md`）
3. 使用者記憶（`~/.claude/CLAUDE.md`）
4. 本地專案記憶

適合你把長期規則、專案規範和個人偏好分層管理。

## Memory 架構

Claude Code 的記憶系統通常有以下層級：

| 層級 | 作用範圍 | 典型內容 |
|------|----------|----------|
| 受管策略 | 組織級 | 合規、安全、統一流程 |
| 專案記憶 | 單個專案 | 架構、編碼標準、工作流程 |
| 目錄記憶 | 子目錄 | 模組約束、區域性規範 |
| 使用者記憶 | 單個使用者 | 個人偏好、預設設定 |

## 記憶層級

Claude 會按更接近當前上下文的規則優先使用更具體的 memory。一般來說：

- 組織級規則優先於普通偏好
- 專案規則優先於個人偏好
- 目錄級規則優先於專案級通用規則

## 排除規則

如果某些 `CLAUDE.md` 不應該被自動載入，可以透過 `claudeMdExcludes` 之類的設定排除。

## 設定檔案層級

專案設定、使用者設定和企業託管設定會共同影響 memory 的載入方式。你可以把它理解為：

1. 組織策略
2. 專案設定
3. 本地設定
4. 臨時會話輸入

## 模組化規則系統

Memory 不一定要寫成一個巨大檔案。你可以把規則拆成多個目錄檔案，再按路徑組織。

### 透過 YAML frontmatter 設定路徑規則

```md
---
description: API development rules
---

# API Development Rules
```

### 子目錄與符號連結

你可以用子目錄和 symlink 把區域性規則複用到多個專案區域。

## Memory 位置表

常見位置包括：

- 專案根目錄的 `CLAUDE.md`
- 使用者目錄的 `~/.claude/CLAUDE.md`
- 子目錄的 `CLAUDE.md`

## Memory 更新生命週期

一般流程是：

1. 建立或編輯 `CLAUDE.md`
2. Claude 重新載入
3. 新規則在後續會話中生效

## Auto Memory

Auto memory 讓 Claude 根據當前目錄自動尋找並載入合適的記憶檔案。

### 工作方式

Claude 會根據當前工作目錄、父目錄和已設定路徑，逐層查詢相關 memory。

### 目錄結構

```text
project/
├── CLAUDE.md
├── src/
│   ├── CLAUDE.md
│   └── api/
│       └── CLAUDE.md
```

### 版本要求

某些 auto memory 行為依賴較新的 Claude Code 版本。

### 自訂 auto memory 目錄

如果預設目錄不適合你的專案，可以在設定中指定新的 memory 路徑。

### worktree 和儲存庫共享

在 worktree、monorepo 或多人協作場景中，auto memory 可以幫助保持規則一致。

### Subagent 記憶

Subagents 也可以擁有自己的記憶範圍，用於在各自職責內保持一致性。

### 控制 auto memory

```bash
# 當前會話禁用 auto memory

# 顯式開啟 auto memory
```

## 透過 `--add-dir` 新增額外目錄

你可以用 `--add-dir` 把額外目錄也加入 Claude 的可見範圍，適合多目錄協作。

## 實戰範例

### 範例 1：專案記憶結構

```md
# 專案設定
## 專案概覽
## 架構
## 開發規範
### 程式碼風格
### 命名約定
### Git 工作流程
### 測試要求
### API 規範
### 資料庫
### 部署
## 常用命令
## 團隊聯絡人
## 已知問題與解決辦法
## 相關專案
```

### 範例 2：目錄級記憶

```md
# API 模組規範
## API 專屬規範
### 請求校驗
### 身份驗證
### 響應格式
### 分頁
### 限流
### 快取
```

### 範例 3：個人記憶

```md
# 我的開發偏好
## 關於我
## 程式碼偏好
### 錯誤處理
### 註解
### 測試
### 架構
## 除錯偏好
## 溝通方式
## 專案組織
## 工具鏈
```

### 範例 4：會話中更新記憶

兩種常見方式：

1. 直接提要求，讓 Claude 把規則寫進 memory
2. 使用 `# new rule into memory` 這種模式追加規則

## 最佳實踐

### 應該做的

- 用專案記憶儲存團隊標準
- 用目錄記憶儲存區域性差異
- 先寫簡潔規則，再逐步補充
- 把可重複內容寫進 `CLAUDE.md`

### 不應該做的

- 不要把 README 整份複製進 `CLAUDE.md`
- 不要把明顯屬於程式碼的實現細節硬塞進 memory
- 不要讓 memory 變成垃圾桶

### 記憶管理建議

- 優先引用已有文件，而不是重複貼上
- 只保留真正影響 Claude 行為的資訊
- 定期整理過期或衝突的規則

## 安裝說明

### 設定專案記憶

#### 方法 1：使用 `/init`（推薦）

```bash
/init
```

#### 方法 2：手動建立

```bash
cp project-CLAUDE.md CLAUDE.md
```

#### 方法 3：快速更新

```text
# Use semantic versioning for all releases
# Always run tests before committing
# Prefer composition over inheritance
```

### 設定個人記憶

```bash
cp personal-CLAUDE.md ~/.claude/CLAUDE.md
```

### 設定目錄記憶

```bash
cp directory-api-CLAUDE.md src/api/CLAUDE.md
```

### 驗證安裝

- 重新開啟 Claude Code 會話
- 檢查 `CLAUDE.md` 是否被自動載入
- 用一條明顯會受 memory 影響的提示詞測試

## 官方文件

如果你想看更詳細的行為定義、相容性和最新限制，建議參考 Claude Code 官方 memory 文件。

## 相關概念

- [Slash Commands 中文參考](../01-slash-commands/README.md)
- [Skills 中文指南](../03-skills/README.md)
- [Subagents 中文參考](../04-subagents/README.md)
- [Advanced Features 中文指南](../09-advanced-features/README.md)
