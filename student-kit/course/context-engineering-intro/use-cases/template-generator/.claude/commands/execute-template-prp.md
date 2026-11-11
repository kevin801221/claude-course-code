# 執行範本生成 PRP (Execute Template Generation PRP)

執行一個全面的範本生成 PRP，為特定的技術/框架建立完整的上下文工程範本包。

## PRP 檔案：$ARGUMENTS

## 執行流程 (Execution Process)

1. **載入範本生成 PRP**
   - 完整閱讀指定的範本生成 PRP 檔案。
   - 理解目標技術和所有需求。
   - 審查 PRP 中記錄的所有網頁研究發現。
   - 遵循建立範本包的所有說明。

2. **深度思考 (ULTRATHINK) —— 範本包設計**
   - 建立全面的實作計畫。
   - 根據 PRP 研究規劃完整的範本包結構。
   - 設計領域特定的上下文工程調整方案。
   - 將技術模式對應到上下文工程原則。
   - 規劃所有需要的檔案及其相互關係。

3. **生成完整的範本包**
   - 為該技術用例建立完整的目錄結構。
   - 生成帶有全局規則的領域特定 `CLAUDE.md`。
   - 為該技術建立專門的範本 PRP 生成和執行命令。
   - 結合研究發現開發領域特定的基礎 PRP 範本。
   - 包含來自網頁研究的全面範例和說明文件。

4. **驗證範本包**
   - 執行 PRP 中指定的所有驗證命令。
   - 驗證所有需要的檔案均已建立且格式正確。
   - 測試範本結構的完整性與準確性。
   - 檢查與基礎上下文工程框架的整合情況。

5. **品質保證 (QA)**
   - 確保範本遵循所有上下文工程原則。
   - 驗證領域特定模式是否被準確呈現。
   - 檢查驗證迴圈是否適合該技術且可執行。
   - 確認範本對於目標技術是否可立即使用。

6. **完成實作**
   - 對照所有 PRP 需求審查範本包。
   - 確保滿足 PRP 中的所有成功準則。
   - 驗證範本已達到生產就緒水準。

## 範本包需求

建立一個具備以下確切結構的完整用例範本：

### 要求的目錄結構
```
use-cases/{技術名稱}/
├── CLAUDE.md                                    # 領域全局規則
├── .claude/commands/
│   ├── generate-{技術名稱}-prp.md               # 領域 PRP 生成
│   └── execute-{技術名稱}-prp.md                # 領域 PRP 執行
├── PRPs/
│   ├── templates/
│   │   └── prp_{技術名稱}_base.md               # 領域基礎 PRP 範本
│   ├── ai_docs/                                # 領域文件 (選填)
│   └── INITIAL.md                              # 功能請求範例
├── examples/                                   # 領域程式碼範例
├── copy_template.py                            # 範本部署腳本
└── README.md                                   # 全面的使用指南
```

### 基於 PRP 研究的內容需求

**CLAUDE.md** 必須包含 (領域全局規則)：
- 技術特定的工具和套件管理命令。
- 領域架構模式與慣例。
- 框架特定的開發工作流程序。
- 針對該技術的安全性與最佳實踐。
- 常見陷阱與整合點。

**領域 PRP 命令** 必須包含：
- 技術特定的研究流程與網頁搜尋策略。
- 基於 PRP 發現的領域文件收集方法。
- 適合框架的驗證迴圈與測試模式。
- 針對該技術的專門實作藍圖。

**基礎 PRP 範本** 必須包含：
- 預填入來自 PRP 中進行的網頁研究的領域上下文。
- 技術特定的成功準則與驗證關卡。
- 適合框架的實作模式與範例。
- 領域專門的文件參考與注意事項。

**複製腳本 (copy_template.py)** 必須包含：
- 接受目標目錄作為命令列參數。
- 將整個範本目錄結構複製到目標位置。
- 包含「所有」檔案：`CLAUDE.md`, `.claude/`, `PRPs/`, `examples/`, `README.md`。
- 優雅地處理目錄建立和錯誤。
- 提供清晰的成功回饋及後續步驟。

**README.md** 必須包含：
- 範本目的與能力的清晰描述。
- 複製腳本使用說明 (顯眼地放在頂部附近)。
- 完整的 PRP 框架工作流說明 (3 步驟流程)。
- 範本結構概覽及檔案說明。
- 技術特定的範例與能力。
- 常見陷阱與疑難排解指引。

## 驗證需求

### 結構驗證
```bash
# 驗證完整結構是否存在
find use-cases/{技術名稱} -type f -name "*.md" | sort
ls -la use-cases/{技術名稱}/.claude/commands/
ls -la use-cases/{技術名稱}/PRPs/templates/

# 檢查必要檔案是否存在
test -f use-cases/{技術名稱}/CLAUDE.md
test -f use-cases/{技術名稱}/README.md
test -f use-cases/{技術名稱}/PRPs/INITIAL.md
test -f use-cases/{技術名稱}/copy_template.py

# 測試複製腳本功能
python use-cases/{技術名稱}/copy_template.py 2>&1 | grep -q "Usage:" || echo "複製腳本需要正確的使用訊息"
```

### 內容驗證
```bash
# 檢查不完整的內容
grep -r "TODO\|PLACEHOLDER\|WEBSEARCH_NEEDED" use-cases/{技術名稱}/
grep -r "{technology}" use-cases/{技術名稱}/ | wc -l  # 應為 0

# 驗證領域特定內容是否存在
grep -r "framework\|library\|technology" use-cases/{技術名稱}/CLAUDE.md
grep -r "WebSearch\|web search" use-cases/{技術名稱}/.claude/commands/

# 驗證 README 具備必要章節
grep -q "Quick Start.*Copy Template" use-cases/{技術名稱}/README.md
grep -q "PRP Framework Workflow" use-cases/{技術名稱}/README.md
grep -q "python copy_template.py" use-cases/{技術名稱}/README.md
```

### 功能測試
```bash
# 測試範本功能
cd use-cases/{技術名稱}

# 驗證命令是否已正確命名
ls .claude/commands/ | grep "{技術名稱}"

# 測試 INITIAL.md 範例是否存在且內容詳盡
wc -l PRPs/INITIAL.md  # 應有實質內容，而不僅僅是幾行
```

## 成功準則

- [ ] 已完全按照規格建立範本包結構。
- [ ] 所有必要檔案均存在且格式正確。
- [ ] 領域特定內容根據 PRP 研究準確代表了該技術。
- [ ] 上下文工程原則已為該技術進行適當調整。
- [ ] 驗證迴圈適合該框架且可執行。
- [ ] 範本包可立即用於在該領域構建專案。
- [ ] 與基礎上下文工程框架的整合保持完好。
- [ ] 來自 PRP 的所有網頁研究發現均已正確整合至範本中。
- [ ] 範例與說明文件全面且具備技術專門性。
- [ ] 複製腳本 (copy_template.py) 功能正常且具備完整文件。
- [ ] README 在頂部顯眼位置包含複製腳本說明。
- [ ] README 透過具體範例說明了完整的 PRP 框架工作流。

注意：如果任何驗證失敗，請分析錯誤、修復範本包組件，並重新驗證直到所有準則均通過。範本必須達到生產就緒水準，且可供使用目標技術的開發人員立即使用。
