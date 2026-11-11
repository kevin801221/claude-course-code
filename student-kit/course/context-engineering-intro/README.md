# 上下文工程範本 (Context Engineering Template)

這是一個全方位的範本，旨在幫助您開始使用「上下文工程 (Context Engineering)」。這是一門為 AI 程式碼編寫助手建構上下文的學問，確保 AI 擁有完成任務所需的所有資訊。

> **上下文工程 (Context Engineering) 比提示工程 (Prompt Engineering) 好 10 倍，比憑感覺編碼 (Vibe Coding) 好 100 倍。**

## 🚀 快速開始

```bash
# 1. 複製此範本
git clone https://github.com/coleam00/Context-Engineering-Intro.git
cd Context-Engineering-Intro

# 2. 設定您的專案規則 (選填 - 已提供範本)
# 編輯 CLAUDE.md 以新增您的專案特定指引

# 3. 新增範例 (強烈建議)
# 將相關程式碼範例放入 examples/ 資料夾中

# 4. 建立初始功能請求
# 編輯 INITIAL.md 以包含您的功能需求

# 5. 生成完整的 PRP (產品需求提示，Product Requirements Prompt)
# 在 Claude Code 中執行：
/generate-prp INITIAL.md

# 6. 執行 PRP 以實作您的功能
# 在 Claude Code 中執行：
/execute-prp PRPs/your-feature-name.md
```

## 📚 目錄

- [什麼是上下文工程？](#什麼是上下文工程？)
- [範本結構](#範本結構)
- [逐步指南](#逐步指南)
- [撰寫有效的 INITIAL.md 檔案](#撰寫有效的-initialmd-檔案)
- [PRP 工作流程](#the-prp-workflow)
- [有效率地使用範例](#有效率地使用範例)
- [最佳實踐](#最佳實踐)

## 什麼是上下文工程？

上下文工程代表了從傳統提示工程的範式轉移：

### 提示工程 vs 上下文工程

**提示工程 (Prompt Engineering)：**
- 專注於巧妙的措辭和特定的表達方式
- 侷限於您如何描述一個任務
- 就像給某人一張便利貼

**上下文工程 (Context Engineering)：**
- 一個提供全面上下文的完整系統
- 包含文件、範例、規則、模式和驗證
- 就像撰寫一份包含所有細節的完整電影劇本

### 為什麼上下文工程很重要

1. **減少 AI 失敗**：大多數代理人 (Agent) 的失敗並非模型失敗，而是上下文失敗。
2. **確保一致性**：AI 會遵循您的專案模式和慣例。
3. **實現複雜功能**：AI 可以透過適當的上下文處理多步驟的實作。
4. **自我修正**：驗證迴圈允許 AI 修復自己的錯誤。

## 範本結構

```
context-engineering-intro/
├── .claude/
│   ├── commands/
│   │   ├── generate-prp.md    # 生成完整的 PRP
│   │   └── execute-prp.md     # 執行 PRP 以實作功能
│   └── settings.local.json    # Claude Code 權限設定
├── PRPs/
│   ├── templates/
│   │   └── prp_base.md       # PRP 的基礎範本
│   └── EXAMPLE_multi_agent_prp.md  # 完整的 PRP 範例
├── examples/                  # 您的程式碼範例 (至關重要！)
├── CLAUDE.md                 # AI 助手的全局規則
├── INITIAL.md               # 功能請求範本
├── INITIAL_EXAMPLE.md       # 功能請求範例
└── README.md                # 本檔案
```

這個範本目前沒有側重於 RAG 和上下文工程工具，因為我很快就會推出更多相關內容。 ;)

## 逐步指南

### 1. 設定全局規則 (CLAUDE.md)

`CLAUDE.md` 檔案包含 AI 助手在每次對話中都會遵循的專案範圍規則。範本包括：

- **專案感知**：讀取規劃文件、檢查任務
- **程式碼結構**：檔案大小限制、模組組織
- **測試需求**：單元測試模式、覆蓋率預期
- **風格慣例**：語言偏好、格式化規則
- **文件標準**：Docstring 格式、註解實踐

**您可以直接使用提供的範本，或根據您的專案進行自訂。**

### 2. 建立初始功能請求

編輯 `INITIAL.md` 來描述您想要構建的功能：

```markdown
## FEATURE (功能)：
[描述您想要構建的功能 - 請具體說明功能和需求]

## EXAMPLES (範例)：
[列出 examples/ 資料夾中的任何範例檔案，並說明應如何使用它們]

## DOCUMENTATION (文件)：
[包含相關文件、API 或 MCP 伺服器資源的連結]

## OTHER CONSIDERATIONS (其他考量)：
[提到任何注意事項、特定需求或 AI 助手通常會忽略的事情]
```

**請參閱 `INITIAL_EXAMPLE.md` 以獲取完整範例。**

### 3. 生成 PRP

PRP (產品需求提示，Product Requirements Prompts) 是全面的實作藍圖，包括：

- 完整的上下文和文件
- 帶有驗證的實作步驟
- 錯誤處理模式
- 測試需求

它們類似於 PRD (產品需求文件，Product Requirements Documents)，但更專門用於指導 AI 編碼助手。

在 Claude Code 中執行：
```bash
/generate-prp INITIAL.md
```

**注意**：斜線命令是定義在 `.claude/commands/` 中的自訂命令。您可以查看它們的實作：
- `.claude/commands/generate-prp.md` - 了解它如何研究並建立 PRP
- `.claude/commands/execute-prp.md` - 了解它如何根據 PRP 實作功能

這些命令中的 `$ARGUMENTS` 變數會接收您在命令名稱後傳遞的內容 (例如 `INITIAL.md` 或 `PRPs/your-feature.md`)。

此命令將：
1. 讀取您的功能請求
2. 研究程式碼庫中的模式
3. 搜尋相關文件
4. 在 `PRPs/your-feature-name.md` 中建立完整的 PRP

### 4. 執行 PRP

生成後，執行 PRP 以實作您的功能：

```bash
/execute-prp PRPs/your-feature-name.md
```

AI 編碼助手將：
1. 從 PRP 中讀取所有上下文
2. 建立詳細的實作計畫
3. 執行每個步驟並進行驗證
4. 執行測試並修復任何問題
5. 確保滿足所有成功標準

## 撰寫有效的 INITIAL.md 檔案

### 關鍵章節說明

**FEATURE (功能)**：具體且全面
- ❌ 「建立一個網頁爬蟲」
- ✅ 「使用 BeautifulSoup 建立一個非同步網頁爬蟲，從電子商務網站提取產品數據，處理速率限制，並將結果儲存在 PostgreSQL 中」

**EXAMPLES (範例)**：善用 examples/ 資料夾
- 將相關的程式碼模式放在 `examples/` 中
- 參考特定的檔案和要遵循的模式
- 說明應模仿哪些方面

**DOCUMENTATION (文件)**：包含所有相關資源
- API 文件連結
- 函式庫指南
- MCP 伺服器文件
- 資料庫綱要 (Schemas)

**OTHER CONSIDERATIONS (其他考量)**：捕捉重要細節
- 身分驗證需求
- 速率限制或配額
- 常見陷阱
- 效能需求

## PRP 工作流程

### /generate-prp 如何運作

該命令遵循以下過程：

1. **研究階段**
   - 分析您的程式碼庫中的模式
   - 搜尋類似的實作
   - 識別要遵循的慣例

2. **文件收集**
   - 獲取相關的 API 文件
   - 包含函式庫文件
   - 加入注意事項和特殊情況

3. **藍圖建立**
   - 建立逐步實作計畫
   - 包含驗證關卡
   - 加入測試需求

4. **品質檢查**
   - 評分置信度 (1-10)
   - 確保包含所有上下文

### /execute-prp 如何運作

1. **載入上下文**：讀取整個 PRP
2. **計畫**：使用 TodoWrite 建立詳細的任務列表
3. **執行**：實作每個組件
4. **驗證**：執行測試和 Lint 檢查
5. **迭代**：修復發現的任何問題
6. **完成**：確保滿足所有需求

請參閱 `PRPs/EXAMPLE_multi_agent_prp.md` 以了解生成內容的完整範例。

## 有效率地使用範例

`examples/` 資料夾對成功**至關重要**。當 AI 編碼助手可以看到要遵循的模式時，其表現會好得多。

### 範例中應包含的內容

1. **程式碼結構模式**
   - 您如何組織模組
   - 匯入 (Import) 慣例
   - 類別/函式模式

2. **測試模式**
   - 測試檔案結構
   - 模擬 (Mocking) 方法
   - 斷言 (Assertion) 風格

3. **整合模式**
   - API 客戶端實作
   - 資料庫連線
   - 身分驗證流程

4. **CLI 模式**
   - 參數解析
   - 輸出格式化
   - 錯誤處理

### 範例結構

```
examples/
├── README.md           # 說明每個範例演示的內容
├── cli.py             # CLI 實作模式
├── agent/             # 代理人架構模式
│   ├── agent.py      # 代理人建立模式
│   ├── tools.py      # 工具實作模式
│   └── providers.py  # 多提供者模式
└── tests/            # 測試模式
    ├── test_agent.py # 單元測試模式
    └── conftest.py   # Pytest 設定
```

## 最佳實踐

### 1. 在 INITIAL.md 中明確表達
- 不要假設 AI 知道您的偏好
- 包含具體的需求和約束
- 大量參考範例

### 2. 提供全面的範例
- 範例越多 = 實作越好
- 展示「該做什麼」以及「不該做什麼」
- 包含錯誤處理模式

### 3. 使用驗證關卡
- PRP 包含必須通過的測試命令
- AI 將持續迭代直到所有驗證成功
- 這確保了第一次嘗試就能獲得可運行的程式碼

### 4. 利用文件
- 包含官方 API 文件
- 新增 MCP 伺服器資源
- 參考特定的文件章節

### 5. 自訂 CLAUDE.md
- 加入您的慣例
- 包含專案特定規則
- 定義編碼標準

## 資源

- [Claude Code 文件](https://docs.anthropic.com/en/docs/claude-code)
- [上下文工程最佳實踐](https://www.philschmid.de/context-engineering)
