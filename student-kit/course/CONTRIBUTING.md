<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-code-tutorial-logo-dark.svg">
  <img alt="Claude Code 完整教學" src="resources/logos/claude-code-tutorial-logo.svg">
</picture>

# 為 Claude Code 完整教學 做出貢獻

感謝你有興趣為這個專案做出貢獻！本指南將協助你了解如何有效地參與貢獻。

## 關於本專案

Claude Code 完整教學 是一份以視覺化、範例導向的方式介紹 Claude Code 的指南。我們提供：
- **Mermaid 圖表**說明功能如何運作
- 可立即使用的**生產就緒範本**
- 附帶背景脈絡與最佳實踐的**實際範例**
- 從初階到進階的**漸進式學習路徑**

## 貢獻類型

### 1. 新範例或範本
為現有功能新增範例（斜線指令（Slash Commands）、技能（Skills）、Hooks 等）：
- 可直接複製貼上使用的程式碼
- 清楚說明運作方式
- 使用情境與優點
- 疑難排解技巧

### 2. 文件改善
- 釐清令人困惑的章節
- 修正錯字與文法
- 補上缺漏的資訊
- 改善程式碼範例

### 3. 功能指南
為 Claude Code 的新功能撰寫指南：
- 逐步教學
- 架構圖
- 常見模式與反模式
- 實際工作流程

### 4. 錯誤回報
回報你遇到的問題：
- 描述你預期的結果
- 描述實際發生的情況
- 附上重現步驟
- 附上相關的 Claude Code 版本與作業系統

### 5. 意見回饋與建議
協助改善這份指南：
- 建議更好的說明方式
- 指出涵蓋範圍的缺口
- 建議新增章節或重新編排

## 快速開始

### 1. Fork 並複製（clone）
```bash
git clone https://github.com/kevin801221/claude-code-tutorial.git
cd claude-code-tutorial
```

### 2. 建立分支
使用具描述性的分支名稱：
```bash
git checkout -b add/feature-name
git checkout -b fix/issue-description
git checkout -b docs/improvement-area
```

### 3. 設定你的環境

Pre-commit hooks 會在每次 commit 前，於本機執行與 CI 相同的檢查。所有 5 項檢查都必須通過，PR 才會被接受。

**必要的相依套件：**

```bash
# Python 工具（uv 是本專案使用的套件管理工具）
pip install uv
uv venv
source .venv/bin/activate
uv pip install -r scripts/requirements-dev.txt

# Markdown 檢查工具（Node.js）
npm install -g markdownlint-cli

# Mermaid 圖表驗證工具（Node.js）
npm install -g @mermaid-js/mermaid-cli

# 安裝 pre-commit 並啟用 hooks
uv pip install pre-commit
pre-commit install
```

**驗證你的環境設定：**

```bash
pre-commit run --all-files
```

每次 commit 都會執行以下 hooks：

| Hook | 檢查內容 |
|------|---------------|
| `markdown-lint` | Markdown 格式與結構 |
| `cross-references` | 相對連結、錨點、程式碼區塊 |
| `mermaid-syntax` | 所有 ` ```mermaid ` 區塊都能正確解析 |
| `link-check` | 外部 URL 可以連線 |
| `build-epub` | EPUB 產生時沒有錯誤（`.md` 有變更時） |

## 目錄結構

```
├── 01-slash-commands/      # 使用者手動觸發的捷徑
├── 02-memory/              # 持久化上下文範例
├── 03-skills/              # 可重複使用的能力
├── 04-subagents/           # 專門化的 AI 助理
├── 05-mcp/                 # Model Context Protocol 範例
├── 06-hooks/               # 事件驅動自動化
├── 07-plugins/             # 打包的功能組合
├── 08-checkpoints/         # 工作階段快照
├── 09-advanced-features/   # 規劃、思考、背景任務
├── 10-cli/                 # CLI 參考
├── scripts/                # 建置與工具腳本
└── README.md               # 主要指南
```

## 如何貢獻範例

### 新增斜線指令
1. 在 `01-slash-commands/` 中建立一個 `.md` 檔案
2. 內容須包含：
   - 清楚描述它的功能
   - 使用情境
   - 安裝說明
   - 使用範例
   - 客製化技巧
3. 更新 `01-slash-commands/README.md`

### 新增技能
1. 在 `03-skills/` 中建立一個目錄
2. 內容須包含：
   - `SKILL.md` — 主要文件
   - `scripts/` — 若有需要的輔助腳本
   - `templates/` — 提示詞範本
   - README 中的使用範例
3. 更新 `03-skills/README.md`

### 新增子代理
1. 在 `04-subagents/` 中建立一個 `.md` 檔案
2. 內容須包含：
   - 代理的用途與能力
   - 系統提示詞結構
   - 使用情境範例
   - 整合範例
3. 更新 `04-subagents/README.md`

### 新增 MCP 設定
1. 在 `05-mcp/` 中建立一個 `.json` 檔案
2. 內容須包含：
   - 設定說明
   - 必要的環境變數
   - 設定步驟
   - 使用範例
3. 更新 `05-mcp/README.md`

### 新增 Hook
1. 在 `06-hooks/` 中建立一個 `.sh` 檔案
2. 內容須包含：
   - Shebang 與說明
   - 清楚說明邏輯的註解
   - 錯誤處理
   - 安全性考量
3. 更新 `06-hooks/README.md`

## 撰寫準則

### Markdown 風格
- 使用清楚的標題（章節用 H2，子章節用 H3）
- 段落簡短聚焦
- 清單使用項目符號
- 程式碼區塊需標明語言
- 章節之間加上空行

### 程式碼範例
- 讓範例可直接複製貼上使用
- 為不易理解的邏輯加上註解
- 同時提供簡易版與進階版
- 展示實際使用情境
- 標示潛在問題

### 文件
- 說明「為什麼」而不只是「是什麼」
- 附上先備知識
- 加上疑難排解章節
- 連結至相關主題
- 保持對初學者友善

### JSON/YAML
- 使用一致的縮排（統一用 2 或 4 個空格）
- 加上說明設定的註解
- 附上驗證範例

### 圖表
- 盡可能使用 Mermaid
- 保持圖表簡單易讀
- 在圖表下方附上說明
- 連結至相關章節

## 提交準則

遵循慣例式 commit 格式：
```
type(scope): description

[optional body]
```

類型：
- `feat`：新功能或新範例
- `fix`：錯誤修正
- `docs`：文件變更
- `refactor`：程式碼重構
- `style`：格式變更
- `test`：新增或變更測試
- `chore`：建置、相依套件等雜項

範例：
```
feat(slash-commands): Add API documentation generator
docs(memory): Improve personal preferences example
fix(README): Correct table of contents link
docs(skills): Add comprehensive code review skill
```

## 提交前

### 檢查清單
- [ ] 程式碼符合專案風格與慣例
- [ ] 新範例包含清楚的文件
- [ ] README 檔案已更新（本地與根目錄皆然）
- [ ] 沒有敏感資訊（API 金鑰、憑證）
- [ ] 範例已測試且可正常運作
- [ ] 連結已驗證且正確
- [ ] 檔案權限正確（腳本可執行）
- [ ] 提交訊息清楚且具描述性

### 本機測試
```bash
# 執行所有 pre-commit 檢查（與 CI 相同的檢查）
pre-commit run --all-files

# 檢視你的變更
git diff
```

## Pull Request 流程

1. **建立內容清楚的 PR**：
   - 這個 PR 新增或修正了什麼？
   - 為什麼需要這個變更？
   - 相關 Issue（若有）

2. **提供相關細節**：
   - 新功能？請附上使用情境
   - 文件變更？請說明改善之處
   - 範例？請展示前後對照

3. **連結至 Issue**：
   - 使用 `Closes #123` 自動關閉相關 Issue

4. **耐心等候審查**：
   - 維護者可能會提出改善建議
   - 依回饋進行迭代
   - 最終決定權在維護者手上

## 程式碼審查流程

審查者會檢查：
- **正確性**：是否如描述般正常運作？
- **品質**：是否達到生產就緒的水準？
- **一致性**：是否遵循專案模式？
- **文件**：是否清楚完整？
- **安全性**：是否存在任何漏洞？

## 回報問題

### 錯誤回報
內容須包含：
- Claude Code 版本
- 作業系統
- 重現步驟
- 預期行為
- 實際行為
- 若適用，附上截圖

### 功能請求
內容須包含：
- 使用情境或要解決的問題
- 建議的解決方案
- 你考慮過的替代方案
- 其他背景資訊

### 文件問題
內容須包含：
- 哪裡令人困惑或缺漏
- 建議的改善方式
- 範例或參考資料

## 專案政策

### 敏感資訊
- 絕不提交 API 金鑰、token 或憑證
- 範例中使用佔位值
- 為設定檔提供 `.env.example`
- 記錄必要的環境變數

### 程式碼品質
- 讓範例聚焦且易讀
- 避免過度工程化的解法
- 為不易理解的邏輯加上註解
- 提交前徹底測試

### 智慧財產權
- 原創內容歸作者所有
- 專案採用教育用途授權
- 尊重現有的著作權
- 於需要時提供出處標註

## 尋求協助

- **問題**：在 GitHub Issues 中開啟討論
- **一般協助**：查看現有文件
- **開發協助**：參考類似範例
- **程式碼審查**：在 PR 中標註維護者

## 致謝

貢獻者會在以下地方獲得肯定：
- README.md 的貢獻者章節
- GitHub 貢獻者頁面
- 提交歷史紀錄

## 安全性

貢獻範例與文件時，請遵循安全的程式撰寫方式：

- **絕不寫死機密資訊或 API 金鑰** — 使用環境變數
- **警示安全性影響** — 標示潛在風險
- **使用安全的預設值** — 預設啟用安全性功能
- **驗證輸入資料** — 展示適當的輸入驗證與清理方式
- **加上安全性備註** — 記錄安全性考量

若有安全性問題，請參閱 [SECURITY.md](SECURITY.md) 了解我們的漏洞回報流程。

## 行為準則

我們致力於打造一個歡迎且包容的社群。完整的社群標準請參閱 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

簡而言之：
- 保持尊重與包容
- 大方接受回饋
- 幫助他人學習與成長
- 避免騷擾或歧視
- 向維護者回報問題

我們期望所有貢獻者都能遵守本準則，並以善意與尊重對待彼此。

## 授權條款

貢獻本專案即表示你同意，你的貢獻將依 MIT 授權條款釋出。詳情請參閱 [LICENSE](LICENSE) 檔案。

## 有疑問嗎？

- 查看 [README](README.md)
- 參考 [LEARNING-ROADMAP.md](LEARNING-ROADMAP.md)
- 查看現有範例
- 開一個 Issue 進行討論

感謝你的貢獻！🙏

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/overview
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
