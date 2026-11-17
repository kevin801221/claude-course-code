<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../resources/logos/claude-code-tutorial-logo-dark.svg">
  <img alt="Claude Code 完整教學" src="../../resources/logos/claude-code-tutorial-logo.svg">
</picture>

# Documentation 外掛

為你的專案提供全面的文件產生與維護。

## 功能

✅ API 文件產生
✅ README 建立與更新
✅ 文件同步
✅ 程式碼註解改善
✅ 範例產生

## 安裝

```bash
/plugin install documentation
```

## 包含內容

### 斜線指令
- `/generate-api-docs` - 產生 API 文件
- `/generate-readme` - 建立或更新 README
- `/sync-docs` - 讓文件與程式碼變更同步
- `/validate-docs` - 驗證文件

### 子代理
- `api-documenter` - API 文件專家
- `code-commentator` - 程式碼註解改善
- `example-generator` - 建立程式碼範例

### 範本
- `api-endpoint.md` - API 端點文件範本
- `function-docs.md` - 函式文件範本
- `adr-template.md` - 架構決策紀錄（ADR）範本

### MCP 伺服器
- 用於文件同步的 GitHub 整合

## 用法

### 產生 API 文件
```
/generate-api-docs
```

### 建立 README
```
/generate-readme
```

### 同步文件
```
/sync-docs
```

### 驗證文件
```
/validate-docs
```

## 需求

- Claude Code 2.1+
- GitHub 存取權限（選用）

## 範例工作流程

```
User: /generate-api-docs

Claude:
1. 掃描 /src/api/ 中的所有 API 端點
2. 委派給 api-documenter 子代理
3. 擷取函式簽章與 JSDoc
4. 依模組／端點分類
5. 使用 api-endpoint.md 範本
6. 產生完整的 Markdown 文件
7. 納入 curl、JavaScript 與 Python 範例

結果：
✅ API 文件已產生
📄 已建立的檔案：
   - docs/api/users.md
   - docs/api/auth.md
   - docs/api/products.md
📊 涵蓋率：23/23 個端點已建立文件
```

## 範本用法

### API 端點範本
用於以完整範例記錄 REST API 端點。

### 函式文件範本
用於記錄個別函式／方法。

### ADR 範本
用於記錄架構決策。

## 設定

設定用於文件同步的 GitHub token：
```bash
export GITHUB_TOKEN="your_github_token"
```

## 最佳實踐

- 讓文件貼近程式碼
- 隨程式碼變更更新文件
- 納入實用範例
- 定期驗證
- 使用範本以維持一致性

---

**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/plugins
- https://github.com/anthropics/claude-code/releases/tag/v2.1.131
- https://github.com/anthropics/claude-code/releases/tag/v2.1.138
- https://code.claude.com/docs/en/model-config
**相容模型**：Claude Fable 5、Claude Opus 5、Claude Sonnet 5、Claude Sonnet 4.6、Claude Opus 4.8、Claude Haiku 4.5
