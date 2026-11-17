---
name: 文件生成外掛
description: 為文件編寫、同步和校驗提供完整工作流程
tags: plugins, documentation, automation
---

# 文件生成外掛

這個外掛把文件相關的命令、subagents、模板和 MCP 伺服器打包在一起，幫助你生成、同步和校驗文件。

## 特性

✅ 生成 API 文件
✅ 建立和更新 README
✅ 同步文件
✅ 改進程式碼註解
✅ 生成範例

## 包含內容

### 命令
- [commands/generate-api-docs.md](commands/generate-api-docs.md) - 生成 API 文件
- [commands/generate-readme.md](commands/generate-readme.md) - 生成 README
- [commands/sync-docs.md](commands/sync-docs.md) - 同步文件
- [commands/validate-docs.md](commands/validate-docs.md) - 校驗文件

### Subagents
- [agents/api-documenter.md](agents/api-documenter.md) - API 文件 subagent
- [agents/code-commentator.md](agents/code-commentator.md) - 程式碼註解 subagent
- [agents/example-generator.md](agents/example-generator.md) - 範例生成 subagent

### 模板
- [templates/adr-template.md](templates/adr-template.md) - ADR 模板
- [templates/api-endpoint.md](templates/api-endpoint.md) - API 端點模板
- [templates/function-docs.md](templates/function-docs.md) - 函式文件模板

### MCP 伺服器
- GitHub 整合 - 用於文件同步

## 安裝

```bash
claude --plugin-dir ./07-plugins/documentation
```

## 使用方式

### 生成 API 文件
```bash
/generate-api-docs
```

### 建立 README
```bash
/generate-readme
```

### 同步文件
```bash
/sync-docs
```

### 校驗文件
```bash
/validate-docs
```

## 適用場景

- 想標準化專案文件產出
- 想自動生成 README、API 文件和範例
- 想同步多個文件之間的一致性
- 想維護程式碼註解和範例品質

## 需求

- Claude Code 2.1+
- GitHub 訪問許可權（可選）

## 範例工作流程

```text
使用者：/generate-api-docs

Claude：
1. 掃描 /src/api/ 下的所有 API 端點
2. 委派給 api-documenter subagent
3. 提取函式簽名和 JSDoc
4. 按模組 / 端點組織內容
5. 使用 api-endpoint.md 模板
6. 生成完整的 Markdown 文件
7. 包含 curl、JavaScript 和 Python 範例

結果：
✅ API 文件已生成
📄 已建立檔案：
   - docs/api/users.md
   - docs/api/auth.md
   - docs/api/products.md
📊 覆蓋率：23/23 個端點已文件化
```

## 模板用途

### API 端點模板
用於編寫帶完整範例的 REST API 文件。

### 函式文件模板
用於編寫單個函式或方法的說明文件。

### ADR 模板
用於記錄架構決策。

## 設定

為文件同步設定 GitHub token：
```bash
export GITHUB_TOKEN="your_github_token"
```

## 最佳實踐

- 文件儘量貼近程式碼
- 隨著程式碼變化同步更新文件
- 提供可直接執行的範例
- 定期校驗文件有效性
- 使用模板保持一致性

---

**最後更新**: 2026 年 10 月 18 日
**Claude Code 版本**: 2.1.302
**來源**:
- https://code.claude.com/docs/en/plugins/cli-reference
- https://code.claude.com/docs/en/plugins/install
