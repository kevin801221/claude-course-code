---
name: claude-md
description: 按最佳實踐建立或更新 CLAUDE.md 檔案，以便為 AI agent 提供最優的專案入門上下文
---

## 使用者輸入

```text
$ARGUMENTS
```

在繼續之前，你**必須**先考慮使用者輸入（如果不為空）。使用者可能會指定：
- `create` - 從零建立新的 CLAUDE.md
- `update` - 改進已有的 CLAUDE.md
- `audit` - 分析並報告當前 CLAUDE.md 的品質
- 一個具體路徑，用於建立或更新（例如 `src/api/CLAUDE.md` 代表目錄級說明）

## 核心原則

**LLM 是無狀態的**：CLAUDE.md 是每次對話都會載入的主要專案檔案（與自動記憶和未限定作用域的 rules 一起載入）。它是讓 AI agent 瞭解程式碼庫的主要入門文件。

### 黃金法則

1. **少即是多**：前沿 LLM 大約能遵循 150-200 條指令。Claude Code 的系統提示詞本身已經佔了大約 50 條，因此 CLAUDE.md 必須聚焦且簡潔。

2. **只放通用資訊**：只包含每次會話都適用的內容。任務特定的說明應該放在單獨檔案裡。

3. **不要把 Claude 當成 lint 工具**：風格指南會膨脹上下文並降低指令遵循效果。應改用確定性工具（如 prettier、eslint 等）。

4. **絕不自動生成**：CLAUDE.md 是 AI harness 中槓桿最高的位置。應該經過認真思考後手工編寫。

## 執行流程

### 1. 專案分析

首先分析當前專案狀態：

1. 檢查是否存在已有的 CLAUDE.md 檔案：
   - 根目錄：`./CLAUDE.md` 或 `.claude/CLAUDE.md`
   - 目錄級：`**/CLAUDE.md`
   - 全域性使用者設定：`~/.claude/CLAUDE.md`

2. 識別專案結構：
   - 技術棧（語言、框架）
   - 專案型別（monorepo、單體應用、庫）
   - 開發工具（包管理器、建置系統、測試執行器）

3. 檢視已有文件：
   - README.md
   - CONTRIBUTING.md
   - package.json、pyproject.toml、Cargo.toml 等

### 2. 內容策略（WHAT, WHY, HOW）

圍繞三個維度組織 CLAUDE.md：

#### WHAT - 技術與結構
- 技術棧概覽
- 專案組織方式（對 monorepo 尤其重要）
- 關鍵目錄及其用途

#### WHY - 目的與背景
- 專案是做什麼的
- 為什麼做出這些架構決策
- 每個主要元件負責什麼

#### HOW - 工作流程與約定
- 開發流程（bun vs node、pip vs uv 等）
- 測試流程和命令
- 驗證與建置方法
- 關鍵“坑點”或非顯而易見的要求

### 3. 漸進式披露策略

對於較大的專案，建議建立 `agent_docs/` 資料夾：

```text
agent_docs/
  |- building_the_project.md
  |- running_tests.md
  |- code_conventions.md
  |- architecture_decisions.md
```

在 CLAUDE.md 中引用這些檔案，並寫明：
```markdown
關於詳細的建置說明，請參考 `agent_docs/building_the_project.md`
```

**重要**：使用 `file:line` 引用，而不是程式碼片段，以避免上下文過時。

### 4. 品質約束

建立或更新 CLAUDE.md 時：

1. **目標長度**：少於 200 行
2. **不要寫風格規則**：移除任何 lint/format 相關說明
3. **不要寫任務特定說明**：移到單獨檔案中
4. **不要寫程式碼片段**：改用檔案引用
5. **不要重複資訊**：不要重複 package.json 或 README 中已有內容

### 5. 必備章節

一個結構良好的 CLAUDE.md 應包含：

```markdown
# 專案名稱

一句簡短的專案描述。

## 技術棧
- 主語言和版本
- 關鍵框架/庫
- 資料庫/儲存（如有）

## 專案結構
[僅適用於 monorepo 或複雜結構]
- `apps/` - 應用入口
- `packages/` - 共享庫

## 開發命令
- 安裝：`command`
- 測試：`command`
- 建置：`command`

## 關鍵約定
[只保留非顯而易見、高影響的約定]
- 約定 1，簡要說明
- 約定 2，簡要說明

## 已知問題 / 坑點
[經常讓開發者踩坑的內容]
- 問題 1
- 問題 2
```

### 6. 需要避免的反模式

**不要包含：**
- 程式碼風格指南（交給 lint 工具）
- 如何使用 Claude 的說明
- 對顯而易見模式的冗長解釋
- 複製貼上的程式碼範例
- 泛泛而談的最佳實踐（例如“寫乾淨的程式碼”）
- 特定任務的說明
- 自動生成內容
- 大量 TODO 列表

### 7. 驗證清單

在最終確定前，檢查：

- [ ] 少於 200 行
- [ ] 每一行都適用於所有會話
- [ ] 沒有風格/格式規則
- [ ] 沒有程式碼片段（使用檔案引用）
- [ ] 命令已經驗證可用
- [ ] 對複雜專案使用了漸進式披露
- [ ] 已記錄關鍵坑點
- [ ] 沒有與 README.md 重複

## 輸出格式

### 對於 `create` 或預設模式：

1. 分析專案
2. 按上述結構起草 CLAUDE.md
3. 向使用者展示草稿以供審閱
4. 在獲得批准後寫入相應位置

### 對於 `update`：

1. 讀取現有 CLAUDE.md
2. 按最佳實踐進行審計
3. 識別：
   - 需要刪除的內容（風格規則、程式碼片段、任務特定內容）
   - 需要壓縮的內容
   - 缺失的重要資訊
4. 向使用者展示修改建議
5. 在獲得批准後應用修改

### 對於 `audit`：

1. 讀取現有 CLAUDE.md
2. 生成報告，包括：
   - 當前行數與目標的對比
   - 可通用於所有會話內容的百分比
   - 發現的反模式列表
   - 改進建議
3. 不要修改檔案，只做報告

## AGENTS.md 處理

如果使用者請求建立或更新 AGENTS.md：

**從 v2.1.277 起，Claude Code 會直接把 `AGENTS.md` 作為專案指令讀取。** 但前提是工作目錄以及它上面的每一級目錄都沒有 `CLAUDE.md`、`.claude/CLAUDE.md` 或 `CLAUDE.local.md`。`~/.claude/CLAUDE.md`、受管理的 CLAUDE.md 和 `.claude/rules/` 不計入這項檢查，它們仍會一併載入。該行為由 `/config` 中的 **Project instructions** 控制：`claude-md-or-agents-md`（預設）、`claude-md-and-agents-md`、`claude-md`、`managed-only`。在無法直接讀取的環境中 — v2.1.277 之前的版本（在 Bedrock/Vertex/Foundry、LLM 閘道器或關閉遙測的情況下為 v2.1.281 之前），或升級後的第一個會話 — 退回到在 CLAUDE.md 中用 `@AGENTS.md` 匯入，或者把 `CLAUDE.md` 軟連結到它。

AGENTS.md 是一個跨工具的專案上下文件案 — 和 CLAUDE.md 屬於同一*類*文件，而不是 agent 定義格式。它的存在是為了讓多個編碼 agent 共用同一套專案約定：
- 建置、測試和 lint 命令
- 程式碼風格與架構約定
- 儲存庫結構以及各部分所在位置

Subagents 是單獨定義的，放在 `.claude/agents/*.md` 裡 — 不在 AGENTS.md 中。

同樣適用以下原則：
- 保持聚焦和簡潔
- 使用漸進式披露
- 用外部文件引用代替內聯內容

## 備註

- 在寫入前始終驗證命令是否可用
- 不確定時就不要寫，少即是多
- 系統提醒會告訴 Claude，CLAUDE.md “可能相關，也可能不相關” - 噪音越多，越容易被忽略
- monorepo 最需要清晰的 WHAT/WHY/HOW 結構
- 目錄級 CLAUDE.md 應該更聚焦

---

**最後更新**: 2026 年 10 月 18 日
**Claude Code 版本**: 2.1.302
**來源**:
- https://code.claude.com/docs/en/memory
