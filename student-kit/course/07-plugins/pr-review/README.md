<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../resources/logos/claude-code-tutorial-logo-dark.svg">
  <img alt="Claude Code 完整教學" src="../../resources/logos/claude-code-tutorial-logo.svg">
</picture>

# PR Review 外掛

完整的 PR 審查工作流程，涵蓋安全性、測試與文件檢查。

## 功能

✅ 安全性分析
✅ 測試涵蓋率檢查
✅ 文件驗證
✅ 程式碼品質評估
✅ 效能影響分析

## 安裝

```bash
/plugin install pr-review
```

## 包含內容

### 斜線指令
- `/review-pr` - 完整的 PR 審查
- `/check-security` - 以安全性為核心的審查
- `/check-tests` - 測試涵蓋率分析

### 子代理
- `security-reviewer` - 安全性漏洞偵測
- `test-checker` - 測試涵蓋率分析
- `performance-analyzer` - 效能影響評估

### MCP 伺服器
- 用於取得 PR 資料的 GitHub 整合

### Hooks
- `pre-review.js` - 審查前驗證

## 用法

### 基本 PR 審查
```
/review-pr
```

### 僅執行安全性檢查
```
/check-security
```

### 測試涵蓋率檢查
```
/check-tests
```

## 需求

- Claude Code 2.1+
- GitHub 存取權限
- Git 儲存庫

## 設定

設定你的 GitHub token：
```bash
export GITHUB_TOKEN="your_github_token"
```

## 範例工作流程

```
User: /review-pr

Claude:
1. 執行審查前 Hook（驗證 Git 儲存庫）
2. 透過 GitHub MCP 取得 PR 資料
3. 將安全性審查委派給 security-reviewer 子代理
4. 將測試委派給 test-checker 子代理
5. 將效能評估委派給 performance-analyzer 子代理
6. 彙整所有發現
7. 提供完整的審查報告

結果：
✅ 安全性：未發現重大問題
⚠️  測試：涵蓋率為 65%，建議提升至 80% 以上
✅ 效能：無明顯影響
📝 建議：為邊界案例補充測試
```

---

**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/plugins
- https://github.com/anthropics/claude-code/releases/tag/v2.1.131
- https://github.com/anthropics/claude-code/releases/tag/v2.1.138
- https://code.claude.com/docs/en/model-config
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
