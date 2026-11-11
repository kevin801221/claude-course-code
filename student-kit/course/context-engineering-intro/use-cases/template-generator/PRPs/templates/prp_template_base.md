---
name: "範本生成器 PRP 基礎 (Template Generator PRP Base)"
description: "用於為特定技術領域和用例生成上下文工程範本包的元範本 (Meta-template)"
---

## 目的 (Purpose)

針對 AI 代理人優化的範本，用於為特定的技術領域 (AI 框架、前端技術棧、後端技術等) 生成完整的上下文工程範本包，並具備全面的領域專業化與驗證功能。

## 核心原則 (Core Principles)

1. **元上下文工程 (Meta-Context Engineering)**：應用上下文工程原則來生成領域特定的範本。
2. **技術專業化 (Technology Specialization)**：與目標框架的模式和慣例深度整合。
3. **完整包生成 (Complete Package Generation)**：建立整個範本生態系統，而不僅僅是單個檔案。
4. **驗證驅動 (Validation-Driven)**：包含全面且適合領域的測試與驗證迴圈。
5. **易用性優先 (Usability First)**：生成的範本應能讓開發人員立即使用。

---

## 目標 (Goal)

為 **[目標技術]** 生成一個完整的上下文工程範本包，包含：

- 領域特定的 CLAUDE.md 實作指引。
- 專門的 PRP 生成與執行命令。
- 適合該技術的基礎 PRP 範本。
- 全面的範例與說明文件。
- 領域特定的驗證迴圈與成功準則。

## 為什麼 (Why)

- **開發加速**：實現將上下文工程快速應用於任何技術。
- **模式一致性**：在所有領域中維持上下文工程原則。
- **品質保證**：確保每種技術都具備全面的驗證與測試。
- **知識捕捉**：記錄特定技術的最佳實踐與模式。
- **可擴展框架**：建立能隨技術變遷而演進的可重用範本。

## 內容 (What)

### 範本包組件 (Template Package Components)

**完整的目錄結構：**
```
use-cases/{技術名稱}/
├── CLAUDE.md                      # 領域實作指引
├── .claude/commands/
│   ├── generate-{技術名稱}-prp.md  # 領域 PRP 生成
│   └── execute-{技術名稱}-prp.md   # 領域 PRP 執行  
├── PRPs/
│   ├── templates/
│   │   └── prp_{技術名稱}_base.md  # 領域基礎 PRP 範本
│   ├── ai_docs/                      # 領域文件 (選填)
│   └── INITIAL.md                    # 功能請求範例
├── examples/                         # 領域程式碼範例
├── copy_template.py                  # 範本部署腳本
└── README.md                         # 全面的使用指南
```

**技術整合：**
- 框架特定的工具與命令。
- 架構模式與慣例。
- 開發工作流整合。
- 測試與驗證方法。
- 安全性與效能考量。

**上下文工程調整：**
- 領域特定的研究流程。
- 適合技術的驗證迴圈。
- 框架專門的實作藍圖。
- 與基礎上下文工程原則的整合。

### 成功準則 (Success Criteria)

- [ ] 已生成完整的範本包結構。
- [ ] 所有必要檔案均存在且格式正確。
- [ ] 領域特定內容準確呈現了技術模式。
- [ ] 上下文工程原則已適當調整至該技術。
- [ ] 驗證迴圈適合框架且可執行。
- [ ] 範本可立即用於在該領域建立專案。
- [ ] 與基礎上下文工程框架的整合保持完好。
- [ ] 包含全面的說明文件與範例。

## 所有需要的上下文 (All Needed Context)

### 說明文件與參考資料 (必讀)

```yaml
# 上下文工程基礎 —— 了解基礎框架
- file: ../../../README.md
  why: 要調整的核心上下文工程原則與工作流

- file: ../../../.claude/commands/generate-prp.md
  why: 要為領域專門化的基礎 PRP 生成模式

- file: ../../../.claude/commands/execute-prp.md  
  why: 要為技術調整的基礎 PRP 執行模式

- file: ../../../PRPs/templates/prp_base.md
  why: 要為領域專門化的基礎 PRP 範本結構

# MCP 伺服器範例 —— 領域專業化的參考實作
- file: ../mcp-server/CLAUDE.md
  why: 領域特定實作指引模式的範例

- file: ../mcp-server/.claude/commands/prp-mcp-create.md
  why: 專門的 PRP 生成命令範例

- file: ../mcp-server/PRPs/templates/prp_mcp_base.md
  why: 領域專業化基礎 PRP 範本的範例

# 目標技術研究 —— 新增領域特定文件
- url: [官方框架文件]
  why: 核心框架概念、API 與架構模式

- url: [最佳實踐指南]
  why: 該技術建立的模式與慣例

- url: [安全性考量]
  why: 安全性最佳實踐與常見漏洞

- url: [測試框架]
  why: 該技術的測試方法與驗證模式

- url: [部署模式]
  why: 生產部署與監控考量
```

### 目前上下文工程結構

```bash
# 要擴展的基礎框架結構
context-engineering-intro/
├── README.md                    # 要調整的核心原則
├── .claude/commands/            # 要專門化的基礎命令
├── PRPs/templates/prp_base.md   # 要擴展的基礎範本
├── CLAUDE.md                    # 要繼承的基礎規則
└── use-cases/
    ├── mcp-server/              # 參考專業化範例
    └── template-generator/      # 此元範本系統
```

### 目標技術分析需求

```typescript
// 技術專業化的研究領域
interface TechnologyAnalysis {
  // 核心框架模式
  architecture: {
    project_structure: string[];
    configuration_files: string[];
    dependency_management: string;
    module_organization: string[];
  };
  
  // 開發工作流
  development: {
    package_manager: string;
    dev_server_commands: string[];
    build_process: string[];
    testing_frameworks: string[];
  };
  
  // 最佳實踐
  patterns: {
    code_organization: string[];
    state_management: string[];
    error_handling: string[];
    performance_optimization: string[];
  };
  
  // 整合點
  ecosystem: {
    common_libraries: string[];
    deployment_platforms: string[];
    monitoring_tools: string[];
    CI_CD_patterns: string[];
  };
}
```

### 已知的範本生成模式

```typescript
// 重要：範本生成必須遵循以下模式

// 1. 務必繼承自基礎上下文工程原則
const basePatterns = {
  prp_workflow: "INITIAL.md → generate-prp → execute-prp",
  validation_loops: "語法 → 單元 → 整合 → 部署",
  context_richness: "說明文件 + 範例 + 模式 + 注意事項"
};

// 2. 務必針對目標技術進行專業化
const specialization = {
  tooling: "將通用命令替換為框架特定的命令",
  patterns: "包含框架的架構慣例",
  validation: "使用適合技術的測試與 Lint 檢查",
  examples: "為該領域提供真實、可運行的程式碼範例"
};

// 3. 務必維持易用性與完整性
const quality_gates = {
  immediate_usability: "範本可即插即用",
  comprehensive_docs: "記錄所有模式與注意事項",
  working_examples: "範例可成功編譯與執行",
  validation_loops: "所有驗證命令均可執行"
};

// 4. 應避免的常見陷阱
const anti_patterns = {
  generic_content: "不要使用佔位符文字 —— 請研究實際模式",
  incomplete_research: "不要跳過技術特定的文件",
  broken_examples: "不要包含無法運行的程式碼範例",
  missing_validation: "不要跳過適合領域的測試模式"
};
```

## 實作藍圖 (Implementation Blueprint)

### 技術研究階段

**重要：在任何範本生成之前進行廣泛的網頁研究。這是成功的關鍵。**

透過網頁研究對目標技術進行全面分析：

```yaml
研究任務 1 —— 核心框架分析 (需網頁搜尋)：
  徹底網頁搜尋並學習官方文件：
    - 框架架構與設計模式  
    - 專案結構慣例與最佳實踐
    - 配置檔案模式與管理方法
    - 該技術的包/依賴項管理
    - 入門指南與設定程序

研究任務 2 —— 開發工作流分析 (需網頁搜尋)：
  網頁搜尋並分析開發模式：
    - 本地開發設定與工具
    - 建置流程與編譯步驟
    - 該技術常用的測試框架
    - 除錯工具與開發環境
    - CLI 命令與包管理工作流

研究任務 3 —— 最佳實踐調查 (需網頁搜尋)：
  網頁搜尋並研究已建立的模式：
    - 程式碼組織與檔案結構慣例
    - 該技術特定的安全性最佳實踐
    - 常見陷阱、缺陷與邊緣情況
    - 錯誤處理模式與策略
    - 效能考量與優化技術

研究任務 4 —— 範本包結構規劃：
  規劃如何為此技術建立上下文工程範本：
    - 如何為此特定技術調整 PRP 框架
    - 需要哪些領域特定的 CLAUDE.md 規則
    - 哪些驗證迴圈適合此框架
    - 應包含哪些範例與說明文件
```

### 範本包生成

根據網頁研究結果建立完整的上下文工程範本包：

```yaml
生成任務 1 —— 建立範本目錄結構：
  建立完整的用例目錄結構：
    - use-cases/{技術名稱}/
    - .claude/commands/ 子目錄  
    - PRPs/templates/ 子目錄
    - examples/ 子目錄
    - 根據範本包要求建立所有其他必需的子目錄

生成任務 2 —— 生成領域特定 CLAUDE.md：
  建立技術特定的全局規則檔案：
    - 技術特定的工具與包管理命令
    - 來自網頁研究的框架架構模式與慣例
    - 該技術特定的開發工作流程序
    - 透過研究發現的安全性與最佳實踐
    - 文件中發現的常見陷阱與整合點

生成任務 3 —— 建立專門的範本 PRP 命令：
  生成領域特定的斜線命令：
    - generate-{技術名稱}-prp.md 帶有技術研究模式
    - execute-{技術名稱}-prp.md 帶有框架驗證迴圈
    - 命令應參考研究中的技術特定模式
    - 包含針對該技術領域的網頁搜尋策略

生成任務 4 —— 開發領域特定基礎 PRP 範本：
  建立專門的 prp_{技術名稱}_base.md 範本：
    - 預填入來自網頁研究的技術上下文
    - 技術特定的成功準則與驗證關卡
    - 透過研究發現的框架文件參考
    - 領域適用的實作模式與驗證迴圈

生成任務 5 —— 建立範例與 INITIAL.md 範本：
  生成全面的範本包內容：
    - INITIAL.md 範例，展示如何為此技術請求功能
    - 與該技術相關的可執行程式碼範例 (來自研究)
    - 配置檔案範本與模式

生成任務 6 —— 建立範本複製腳本：
  建立用於範本部署的 Python 腳本：
    - copy_template.py 腳本，接受目標目錄參數
    - 將整個範本目錄結構複製到指定位置
    - 包含所有檔案：CLAUDE.md, commands, PRPs, examples 等
    - 處理目錄建立與檔案複製，並具備錯誤處理
    - 簡單的命令列介面，便於使用

生成任務 7 —— 生成全面的 README：
  建立全面且簡潔的 README.md：
    - 清晰描述此範本的用途與目的
    - PRP 框架工作流說明 (3 步驟流程)
    - 範本複製腳本使用說明 (顯眼地放在頂部附近)
    - 帶有具體範例的快速開始指南
    - 顯示所有生成檔案的範本結構概覽
    - 該技術領域特定的使用範例
```

### 複製腳本與 README 的實作細節

**複製腳本 (copy_template.py) 需求：**
```python
# 核心複製腳本功能：
# 1. 接受目標目錄作為命令列參數
# 2. 將整個範本目錄結構複製到目標位置
# 3. 包含「所有」檔案：CLAUDE.md, .claude/, PRPs/, examples/, README.md
# 4. 處理目錄建立與錯誤處理
# 5. 提供清晰的成功回饋及後續步驟
# 6. 簡單用法：python copy_template.py /path/to/target
```

**README 結構需求：**
```markdown
# 必須按此順序包含以下章節：
# 1. 標題與範本用途簡述
# 2. 🚀 快速開始 —— 先複製範本 (顯眼地放在頂部)
# 3. 📋 PRP 框架工作流 (3 步驟流程說明)
# 4. 📁 範本結構 (帶有說明的目錄樹)
# 5. 🎯 您可以構建的內容 (技術特定範例)
# 6. 📚 關鍵特點 (框架能力)
# 7. 🔍 包含的範例 (提供的可執行範例)
# 8. 📖 說明文件參考 (研究來源)
# 9. 🚫 常見陷阱 (技術特定缺陷)

# 複製腳本的使用方式必須顯眼地放在頂部附近
# PRP 工作流必須清晰顯示帶有實際命令的 3 個步驟
# 所有內容都應具備技術專門性，而非通用性
```

### 領域專業化細節 (Domain Specialization Details)

```typescript
// 針對特定領域的範本專業化模式

// 對於 AI/ML 框架 (Pydantic AI, CrewAI 等)
const ai_specialization = {
  patterns: ["代理人架構", "工具整合", "模型配置"],
  validation: ["模型回應測試", "代理人行為驗證"],
  examples: ["基礎代理人", "多代理人系統", "工具整合"],
  gotchas: ["Token 限制", "模型相容性", "非同步模式"]
};

// 對於前端框架 (React, Vue, Svelte 等)
const frontend_specialization = {
  patterns: ["組件架構", "狀態管理", "路由"],
  validation: ["組件測試", "E2E 測試", "無障礙性"],
  examples: ["基礎應用", "狀態整合", "API 串接"],
  gotchas: ["包體大小", "SSR 考量", "效能"]
};

// 對於後端框架 (FastAPI, Express, Django 等)
const backend_specialization = {
  patterns: ["API 設計", "資料庫整合", "身分驗證"],
  validation: ["API 測試", "資料庫測試", "安全性測試"],
  examples: ["REST API", "驗證系統", "資料庫模型"],
  gotchas: ["安全性漏洞", "效能瓶頸", "可擴展性"]
};

// 對於資料庫/資料框架 (SQLModel, Prisma 等)
const data_specialization = {
  patterns: ["Schema 設計", "遷移管理", "查詢優化"],
  validation: ["Schema 測試", "遷移測試", "查詢效能"],
  examples: ["基礎模型", "關聯關係", "複雜查詢"],
  gotchas: ["遷移衝突", "N+1 查詢", "索引優化"]
};
```

### 整合點 (Integration Points)

```yaml
上下文工程框架：
  - 基礎工作流：繼承自基礎框架的核心 PRP 生成與執行模式
  - 驗證原則：使用該技術的領域特定檢查來擴展基礎驗證
  - 文件標準：與基礎上下文工程文件模式保持一致

技術整合：
  - 包管理：包含框架特定的包管理員與工具
  - 開發工具：包含技術特定的開發與測試工具
  - 框架模式：使用適合技術的架構與程式碼模式
  - 驗證方法：包含框架特定的測試與驗證方法

範本結構：
  - 目錄結構：遵循基礎框架建立的用例範本模式
  - 檔案命名：維持一致的命名慣例 (generate-{tech}-prp.md 等)
  - 內容格式：使用建立的 Markdown 與文件格式
  - 命令模式：為特定技術擴展基礎斜線命令功能
```

## 驗證迴圈 (Validation Loop)

### 第一層：範本結構驗證

```bash
# 重要：驗證完整的範本包結構
find use-cases/{技術名稱} -type f | sort
ls -la use-cases/{技術名稱}/.claude/commands/
ls -la use-cases/{技術名稱}/PRPs/templates/

# 驗證複製腳本存在且功能正常
test -f use-cases/{技術名稱}/copy_template.py
python use-cases/{技術名稱}/copy_template.py --help 2>/dev/null || echo "複製腳本需要 Help 選項"

# 預期：所有必要檔案均存在，包含 copy_template.py
# 如果缺失：遵循建立的模式生成缺失的組件
```

### 第二層：內容品質驗證

```bash
# 驗證領域特定內容的準確性
grep -r "TODO\|PLACEHOLDER\|{domain}" use-cases/{技術名稱}/
grep -r "{技術名稱}" use-cases/{技術名稱}/ | wc -l

# 檢查技術特定模式
grep -r "框架特定模式" use-cases/{技術名稱}/
grep -r "validation" use-cases/{技術名稱}/.claude/commands/

# 預期：無佔位符內容，技術模式已呈現
# 若有問題：研究並新增正確的領域特定內容
```

### 第三層：功能驗證

```bash
# 測試範本功能
cd use-cases/{技術名稱}

# 測試 PRP 生成命令
/generate-prp INITIAL.md
ls PRPs/*.md | grep -v templates

# 測試範本完整性
grep -r "Context is King" . | wc -l  # 應繼承原則
grep -r "{技術特定內容}" . | wc -l  # 應有專業化內容

# 預期：PRP 生成正常，內容具備專業性
# 如果失敗：除錯命令模式與範本結構
```

### 第四層：整合測試

```bash
# 驗證與基礎上下文工程框架的整合
diff -r ../../.claude/commands/ .claude/commands/ | head -20
diff ../../CLAUDE.md CLAUDE.md | head -20

# 測試範本產生正確結果
cd examples/
# 執行該技術特定的任何範例驗證命令

# 預期：在不破壞基礎模式的情況下進行正確的專業化
# 若有問題：調整專業化內容以維持相容性
```

## 最終驗證檢查表 (Final Validation Checklist)

### 範本包完整性

- [ ] 完整的目錄結構： `tree use-cases/{技術名稱}`
- [ ] 所有必要檔案均存在：CLAUDE.md, 命令, 基礎 PRP, 範例
- [ ] 複製腳本存在： `copy_template.py` 功能正確
- [ ] README 內容全面：包含複製腳本說明與 PRP 工作流
- [ ] 領域特定內容：技術模式準確呈現
- [ ] 可執行範例：所有範例均可成功編譯/執行
- [ ] 說明文件完整：README 與使用說明清晰

### 品質與易用性

- [ ] 無佔位符內容： `grep -r "TODO\|PLACEHOLDER"`
- [ ] 技術專業化：框架模式已正確記錄
- [ ] 驗證迴圈正常：所有命令均可執行且功能正常
- [ ] 維持整合性：可與基礎上下文工程框架協作
- [ ] 使用就緒：開發人員可立即開始使用範本

### 框架整合

- [ ] 繼承基礎原則：保留上下文工程工作流
- [ ] 正確專業化：包含技術特定模式
- [ ] 命令相容性：斜線命令按預期運作
- [ ] 文件一致性：遵循建立的文件模式
- [ ] 可維護結構：隨技術演進易於更新

---

## 應避免的反模式 (Anti-Patterns to Avoid)

### 範本生成

- ❌ 不要建立通用的範本 —— 務必深入研究並專業化。
- ❌ 不要跳過全面的技術研究 —— 徹底理解框架。
- ❌ 不要使用佔位符內容 —— 務必包含真實的、經過研究的資訊。
- ❌ 不要忽略驗證迴圈 —— 包含該技術的全方位測試。

### 內容品質

- ❌ 不要假設讀者已具備知識 —— 為該領域明確記錄所有內容。
- ❌ 不要跳過邊緣情況 —— 包含常見陷阱與錯誤處理。
- ❌ 不要忽略安全性 —— 務必包含該技術的安全性考量。
- ❌ 不要忘記維護性 —— 確保範本能隨技術變更而演進。

### 框架整合

- ❌ 不要破壞基礎模式 —— 維持與上下文工程原則的相容性。
- ❌ 不要重複勞動 —— 重用並擴展基礎框架組件。
- ❌ 不要忽略一致性 —— 遵循建立的命名與結構慣例。
- ❌ 不要跳過驗證 —— 在完成前確保範本確實可用。
