# MCP Servers 最佳實踐

![Last Updated](https://img.shields.io/badge/Last_Updated-Mar%2002%2C%202026%2012%3A30%20PM%20PKT-white?style=flat&labelColor=555)<br>
[![Implemented](https://img.shields.io/badge/Implemented-2ea44f?style=flat)](https://github.com/kevin801221/claude-code-best-practice/blob/main/.mcp.json)

MCP（Model Context Protocol）server 讓 Claude Code 能連接外部工具、資料庫與 API。本指南涵蓋日常推薦使用的 server 與設定最佳實踐。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`best-practice/claude-mcp.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/best-practice/claude-mcp.md)

---

## 日常使用的 MCP Servers

> *「裝了 15 個 MCP server，以為越多越好。結果每天真正用到的只有 4 個。」* —— [r/mcp](https://reddit.com/r/mcp/comments/1mj0fxs/)（682 讚）

| MCP Server | 功能 | 資源 |
|------------|-------------|-----------|
| [**Context7**](https://github.com/upstash/context7) | 把最新的函式庫文件抓進脈絡。避免因訓練資料過時而幻想出不存在的 API | [Reddit：「寫程式用過最好的 MCP」](https://reddit.com/r/mcp/comments/1qarjqm/) · [npm](https://www.npmjs.com/package/@upstash/context7-mcp) |
| [**Playwright**](https://github.com/microsoft/playwright-mcp) | 瀏覽器自動化 —— 自主實作、測試與驗證 UI 功能。截圖、導覽、表單測試 | [Reddit：前端必備](https://reddit.com/r/mcp/comments/1m59pk0/) · [文件](https://playwright.dev/) |
| [**Claude in Chrome**](https://github.com/nicobailon/claude-code-in-chrome-mcp) | 把 Claude 接到你真正的 Chrome 瀏覽器 —— 檢查 console、網路、DOM。除錯使用者真正看到的東西 | [Reddit：除錯的「遊戲規則改變者」](https://reddit.com/r/mcp/comments/1qarjqm/5_mcps_that_have_genuinely_made_me_10x_faster/nza0i7t/) · [比較報告](../reports/claude-in-chrome-v-chrome-devtools-mcp.md) |
| [**DeepWiki**](https://github.com/devanshusemwal/deepwiki-mcp) | 為任何 GitHub repo 抓取結構化的 wiki 式文件 —— 架構、API 介面、關聯關係 | [Reddit：「跟 Context7 一起放在 gateway 後面」](https://reddit.com/r/mcp/comments/1qarjqm/) |
| [**Excalidraw**](https://github.com/antonpk1/excalidraw-mcp-app) | 從 prompt 產生架構圖、流程圖與系統設計，輸出成手繪風格的 Excalidraw 草圖 | [GitHub](https://github.com/antonpk1/excalidraw-mcp-app) |

研究（Context7／DeepWiki）→ 除錯（Playwright／Chrome）→ 文件化（Excalidraw）

---

## 設定

MCP server 設定在專案根目錄的 `.mcp.json`（專案範圍）或 `~/.claude.json`（使用者範圍）。

### Server 類型

| 類型 | 傳輸方式 | 範例 |
|------|-----------|---------|
| **stdio** | 生成一個本機行程 | `npx`、`python`、執行檔 |
| **http** | 連到遠端 URL | HTTP/SSE 端點 |

### `.mcp.json` 範例

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    },
    "deepwiki": {
      "command": "npx",
      "args": ["-y", "deepwiki-mcp"]
    },
    "remote-api": {
      "type": "http",
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```

機密資訊請用環境變數展開，不要把 API key commit 進 `.mcp.json`：

```json
{
  "mcpServers": {
    "remote-api": {
      "type": "http",
      "url": "https://mcp.example.com/mcp?token=${MCP_API_TOKEN}"
    }
  }
}
```

### MCP Server 相關設定

`.claude/settings.json` 中這些設定控制 MCP server 的核准：

| 鍵 | 型別 | 說明 |
|-----|------|-------------|
| `enableAllProjectMcpServers` | boolean | 自動核准所有 `.mcp.json` 中的 server，不再提示 |
| `enabledMcpjsonServers` | array | 要自動核准的特定 server 名稱白名單 |
| `disabledMcpjsonServers` | array | 要拒絕的特定 server 名稱黑名單 |

### MCP 工具的權限規則

MCP 工具在權限規則中遵循 `mcp__<server>__<tool>` 命名慣例：

```json
{
  "permissions": {
    "allow": [
      "mcp__*",
      "mcp__context7__*",
      "mcp__playwright__browser_snapshot"
    ],
    "deny": [
      "mcp__dangerous-server__*"
    ]
  }
}
```

---

## MCP 範圍（Scopes）

MCP server 可以定義在三個層級：

| 範圍 | 位置 | 用途 |
|-------|----------|---------|
| **專案（Project）** | `.mcp.json`（repo 根目錄） | 團隊共用的 server，commit 進 git |
| **使用者（User）** | `~/.claude.json`（`mcpServers` 鍵） | 跨所有專案的個人 server |
| **子代理（Subagent）** | 代理 frontmatter（`mcpServers` 欄位） | 僅限特定子代理使用的 server |

優先順序：子代理 > 專案 > 使用者

---

## 資料來源

- [MCP Servers — Claude Code Docs](https://code.claude.com/docs/en/mcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [5 MCPs that have genuinely made me 10x faster — r/mcp](https://reddit.com/r/mcp/comments/1qarjqm/)
- [MCP Server Overload Discussion — r/mcp](https://reddit.com/r/mcp/comments/1mj0fxs/)
