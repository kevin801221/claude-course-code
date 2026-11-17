---
name: PR 審查外掛
description: 為 Pull Request 提供完整的程式碼審查工作流程
tags: plugins, code-review, pull-request
---

# PR 審查外掛

完整的 PR 審查工作流程，包含安全、測試和文件檢查。

## 功能

✅ 安全分析
✅ 測試覆蓋率檢查
✅ 文件校驗
✅ 程式碼品質評估
✅ 效能影響分析

## 安裝

```bash
claude --plugin-dir ./07-plugins/pr-review
```

## 包含內容

### Slash 命令
- `/review-pr` - 全面 PR 審查
- `/check-security` - 面向安全的審查
- `/check-tests` - 測試覆蓋率分析

### 子 agents
- `security-reviewer` - 安全漏洞檢測
- `test-checker` - 測試覆蓋率分析
- `performance-analyzer` - 效能影響評估

### MCP 伺服器
- 用於 PR 資料的 GitHub 整合

### Hooks
- `pre-review.js` - 審查前驗證

## 使用

### 基礎 PR 審查

```
/review-pr
```

### 僅安全檢查

```
/check-security
```

### 僅測試覆蓋率檢查

```
/check-tests
```

## 要求

- Claude Code 2.1+
- GitHub 訪問許可權
- Git 儲存庫

## 設定

設定 GitHub token：

```bash
export GITHUB_TOKEN="your_github_token"
```

## 範例工作流程

```
使用者：/review-pr

Claude:
1. 執行 pre-review hook（驗證 git 儲存庫）
2. 透過 GitHub MCP 獲取 PR 資料
3. 將安全審查委派給 security-reviewer subagent
4. 將測試分析委派給 test-checker subagent
5. 將效能分析委派給 performance-analyzer subagent
6. 彙總所有發現
7. 提供完整審查報告

結果：
✅ 安全：未發現關鍵問題
⚠️  測試：覆蓋率為 65%，建議達到 80%+
✅ 效能：沒有明顯影響
📝 建議：為邊界情況新增測試
```

---

**最後更新**: 2026 年 10 月 18 日
**Claude Code 版本**: 2.1.302
**來源**:
- https://code.claude.com/docs/en/plugins/cli-reference
- https://code.claude.com/docs/en/plugins/install
