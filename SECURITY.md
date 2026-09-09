# 安全性政策

## 總覽

Claude Code 完整教學 專案的安全性對我們來說很重要。本文件說明我們的安全性作法，以及如何負責任地回報安全性漏洞。

## 支援版本

我們為以下版本提供安全性更新：

| 版本 | 狀態 | 支援期限 |
|---------|--------|---------------|
| 最新版（main） | ✅ 維護中 | 目前 + 6 個月 |

**備註**：由於這是一個教學指南專案，我們著重於維持目前的最佳實踐與文件安全性，而非傳統的版本支援模式。更新會直接套用到 main 分支。

## 安全性作法

### 程式碼安全性

1. **相依套件管理**
   - 所有 Python 相依套件都在 `requirements.txt` 中鎖定版本
   - 透過 dependabot 定期更新並人工審查
   - 每次 commit 都用 Bandit 進行安全性掃描
   - 用 pre-commit hooks 進行安全性檢查

2. **程式碼品質**
   - 用 Ruff 進行 lint 以抓出常見問題
   - 用 mypy 做型別檢查，避免與型別相關的漏洞
   - pre-commit hooks 強制執行標準
   - 所有變更在合併前都會經過審查

3. **存取控制**
   - `main` 分支有分支保護
   - 合併前需要審查
   - 合併前狀態檢查必須全數通過
   - 儲存庫的寫入權限受到限制

### 文件安全性

1. **範例中不含機密資訊**
   - 範例中的所有 API 金鑰都是佔位字串
   - 憑證絕不寫死在程式碼中
   - `.env.example` 檔案展示所需的變數
   - 針對機密管理提供清楚的警告

2. **安全性最佳實踐**
   - 範例示範安全的做法
   - 文件中會特別標示安全性警告
   - 提供官方安全性指南的連結
   - 在相關章節討論憑證處理方式

3. **內容審查**
   - 所有文件都會審查安全性問題
   - 貢獻指南中包含安全性考量
   - 驗證外部連結與參考資料

### 相依套件安全性

1. **掃描**
   - Bandit 會掃描所有 Python 程式碼以找出漏洞
   - 透過 GitHub 安全性警示檢查相依套件漏洞
   - 定期進行人工安全性稽核

2. **更新**
   - 安全性修補會即時套用
   - 主要版本會謹慎評估
   - 更新日誌會包含安全性相關更新

3. **透明度**
   - 安全性更新會記錄在 commit 中
   - 負責任地處理漏洞揭露
   - 適當時發布公開的安全性公告

## 回報漏洞

### 我們關心的安全性問題

我們歡迎針對以下項目的回報：
- 腳本或範例中的**程式碼漏洞**
- Python 套件中的**相依套件漏洞**
- 任何程式碼範例中的**加密問題**
- 文件中的**驗證／授權缺陷**
- 設定範例中的**資料外洩風險**
- **注入漏洞**（SQL、指令注入等）
- **SSRF／XXE／路徑遍歷**問題

### 不在範圍內的安全性問題

以下項目不在本專案的範圍內：
- Claude Code 本身的漏洞（請回報給 Anthropic）
- 外部服務或函式庫的問題（請回報給上游專案）
- 社交工程或使用者教育（不適用於本指南）
- 沒有概念驗證（PoC）的理論性漏洞
- 已透過官方管道回報的相依套件漏洞

## 如何回報

### 私下回報（建議方式）

**針對敏感的安全性問題，請使用 GitHub 的私密漏洞回報功能：**

1. 造訪：https://github.com/kevin801221/claude-code-tutorial/security/advisories
2. 點選「Report a vulnerability」
3. 填寫漏洞詳細資訊
4. 內容須包含：
   - 漏洞的清楚描述
   - 受影響的元件（檔案、章節、範例）
   - 潛在影響
   - 重現步驟（若適用）
   - 建議的修正方式（若有）

**接下來會發生什麼事：**
- 我們會在 48 小時內確認已收到回報
- 我們會展開調查並評估嚴重程度
- 我們會與你合作開發修正方案
- 我們會協調揭露時程
- 我們會在安全性公告中列出你的名字（除非你希望匿名）

### 公開回報

針對非敏感或已公開的問題：

1. **開一個 GitHub Issue**，標籤設為 `security`
2. 內容須包含：
   - 標題：`[SECURITY]` 加上簡短說明
   - 詳細描述
   - 受影響的檔案或章節
   - 潛在影響
   - 建議的修正方式

## 漏洞回應流程

### 評估（24 小時內）

1. 我們會確認已收到回報
2. 我們會用 [CVSS v3.1](https://www.first.org/cvss/v3.1/specification-document) 評估嚴重程度
3. 我們會判斷是否在處理範圍內
4. 我們會與你聯絡，提供初步評估結果

### 開發（1–7 天）

1. 我們會開發修正方案
2. 我們會審查並測試修正方案
3. 我們會建立安全性公告
4. 我們會準備發行說明

### 揭露（依嚴重程度而異）

**危急（CVSS 9.0–10.0）**
- 立即發布修正
- 發布公開公告
- 提前 24 小時通知回報者

**高（CVSS 7.0–8.9）**
- 在 48–72 小時內發布修正
- 提前 5 天通知回報者
- 發布時同步公開公告

**中（CVSS 4.0–6.9）**
- 在下一次例行更新中發布修正
- 發布時同步公開公告

**低（CVSS 0.1–3.9）**
- 包含在下一次例行更新中
- 發布時同步公告

### 發布

我們發布的安全性公告會包含：
- 漏洞描述
- 受影響的元件
- 嚴重程度評估（CVSS 分數）
- 修正版本
- 因應方式（若適用）
- 回報者致謝（經同意後）

## 給回報者的最佳實踐

### 回報前

- **確認問題**：你能穩定重現這個問題嗎？
- **搜尋既有 Issue**：這個問題是否已被回報過？
- **檢查文件**：是否已有安全使用方式的說明？
- **測試修正方式**：你建議的修正方式有效嗎？

### 回報時

- **具體明確**：提供確切的檔案路徑與行號
- **提供背景資訊**：為什麼這是安全性問題？
- **說明影響**：攻擊者可能做出什麼行為？
- **提供步驟**：我們該如何重現這個問題？
- **建議修正方式**：你會怎麼修正？

### 回報後

- **請耐心等候**：我們的資源有限
- **保持回應**：儘快回答後續問題
- **保密**：在修正完成前不要公開揭露
- **配合協調**：遵循我們的揭露時程

## 安全性標頭與設定

### 儲存庫安全性

- **分支保護**：main 分支的變更需要 2 位審查者核准
- **狀態檢查**：所有 CI/CD 檢查都必須通過
- **CODEOWNERS**：為關鍵檔案指定審查者
- **簽署 commit**：建議貢獻者使用

### 開發安全性

```bash
# 安裝 pre-commit hooks
pre-commit install

# 在本機執行安全性掃描
bandit -c pyproject.toml -r scripts/
mypy scripts/ --ignore-missing-imports
ruff check scripts/
```

### 相依套件安全性

```bash
# 檢查已知漏洞
pip install safety
safety check

# 或使用 pip-audit
pip install pip-audit
pip-audit
```

## 給貢獻者的安全性準則

### 撰寫範例時

1. **絕不寫死機密資訊**
   ```python
   # ❌ 不好的做法
   api_key = "sk-1234567890"

   # ✅ 好的做法
   api_key = os.getenv("API_KEY")
   ```

2. **警示安全性影響**
   ```markdown
   ⚠️ **安全性提醒**：切勿將 `.env` 檔案提交到 git。
   請立即將它加入 `.gitignore`。
   ```

3. **使用安全的預設值**
   - 預設啟用驗證
   - 適用時使用 HTTPS
   - 驗證並清理輸入資料
   - 使用參數化查詢

4. **記錄安全性考量**
   - 說明為何安全性很重要
   - 展示安全與不安全做法的對比
   - 連結至權威資料來源
   - 在明顯處加上警告

### 審查貢獻時

1. **檢查是否有外洩的機密資訊**
   - 掃描常見模式（`api_key=`、`password=`）
   - 審查設定檔
   - 檢查環境變數

2. **確認安全的程式撰寫方式**
   - 沒有寫死的憑證
   - 適當的輸入驗證
   - 安全的驗證／授權機制
   - 安全的檔案處理方式

3. **測試安全性影響**
   - 這是否可能被濫用？
   - 最壞情況是什麼？
   - 是否有邊界情況？

## 安全性資源

### 官方標準
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [CVSS Calculator](https://www.first.org/cvss/calculator/3.1)

### Python 安全性
- [Python Security Advisories](https://www.python.org/dev/security/)
- [PyPI Security](https://pypi.org/help/#security)
- [Bandit Documentation](https://bandit.readthedocs.io/)

### 相依套件管理
- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/)
- [GitHub Security Alerts](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts)

### 一般安全性
- [Anthropic Security](https://www.anthropic.com/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

## 安全性公告存檔

過去的安全性公告可在 [GitHub Security Advisories](https://github.com/kevin801221/claude-code-tutorial/security/advisories) 分頁中查看。

## 聯絡方式

若有安全性相關問題，或想討論安全性作法：

1. **私密安全性回報**：使用 GitHub 的私密漏洞回報功能
2. **一般安全性問題**：開啟討論並加上 `[SECURITY]` 標籤
3. **安全性政策意見回饋**：建立 Issue 並加上 `security` 標籤

## 致謝

我們感謝協助維護本專案安全性的安全研究人員與社群成員。以負責任的方式回報漏洞的貢獻者，將會在我們的安全性公告中獲得致謝（除非他們希望匿名）。

## 政策更新

本安全性政策會在以下情況下進行審查與更新：
- 發現新漏洞時
- 安全性最佳實踐演進時
- 專案範圍改變時
- 至少每年一次

**最後更新**：2026 年 8 月 25 日
**Claude Code 版本**：2.1.245
**資料來源**：
- https://code.claude.com/docs/en/overview
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
**下次審查**：2027 年 4 月

---

感謝你協助讓 Claude Code 完整教學 保持安全！🔒
