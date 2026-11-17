# 理解大型 Monorepo 中的 Claude Skills 探索機制

在 monorepo 中使用 Claude Code 時，理解 skills 如何被探索並載入脈絡，是有效組織專案專屬能力的關鍵。

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`reports/claude-skills-for-larger-mono-repos.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/reports/claude-skills-for-larger-mono-repos.md)

## 與 CLAUDE.md 的重要差異

**Skills 的載入行為與 CLAUDE.md 檔案不同。** CLAUDE.md 會往目錄樹**上**走（祖先載入），而 skills 使用的是另一套探索機制，聚焦在專案內的巢狀目錄。

## Skills 如何被探索

### 1. 標準 skill 位置

Skills 依範圍從這些固定位置載入：

| 位置 | 路徑 | 適用對象 |
|----------|------|------------|
| 企業（Enterprise） | 受管設定 | 組織中所有使用者 |
| 個人（Personal） | `~/.claude/skills/<skill-name>/SKILL.md` | 你的所有專案 |
| 專案（Project） | `.claude/skills/<skill-name>/SKILL.md` | 僅此專案 |
| 外掛（Plugin） | `<plugin>/skills/<skill-name>/SKILL.md` | 啟用該外掛的地方 |

### 2. 從巢狀目錄自動探索

當你處理子目錄中的檔案時，Claude Code 會自動從巢狀的 `.claude/skills/` 目錄探索 skills。例如，如果你正在編輯 `packages/frontend/` 裡的檔案，Claude Code 也會到 `packages/frontend/.claude/skills/` 找 skills。

這支援各套件擁有自己 skills 的 monorepo 架構。

## Monorepo 結構範例

想像一個典型的 monorepo，有多個獨立套件：

```
/mymonorepo/
├── .claude/
│   └── skills/
│       └── shared-conventions/SKILL.md    # 專案層級 skill
├── packages/
│   ├── frontend/
│   │   ├── .claude/
│   │   │   └── skills/
│   │   │       └── react-patterns/SKILL.md  # 前端專屬 skill
│   │   └── src/
│   │       └── App.tsx
│   ├── backend/
│   │   ├── .claude/
│   │   │   └── skills/
│   │   │       └── api-design/SKILL.md      # 後端專屬 skill
│   │   └── src/
│   └── shared/
│       ├── .claude/
│       │   └── skills/
│       │       └── utils-patterns/SKILL.md  # 共用工具 skill
│       └── src/
```

## 情境 1：剛在根目錄啟動 Claude（還沒編輯任何檔案）

當你在 `/mymonorepo/` 執行 Claude Code 且尚未編輯任何檔案時：

```bash
cd /mymonorepo
claude
# 剛啟動 —— 還沒編輯任何檔案
```

| Skill | 在脈絡中？ | 原因 |
|-------|-------------|--------|
| `shared-conventions` | **是** | 根目錄 `.claude/skills/` 中的專案層級 skill |
| `react-patterns` | **否** | 未被探索 —— 還沒處理 `packages/frontend/` 的檔案 |
| `api-design` | **否** | 未被探索 —— 還沒處理 `packages/backend/` 的檔案 |
| `utils-patterns` | **否** | 未被探索 —— 還沒處理 `packages/shared/` 的檔案 |

## 情境 2：編輯過某套件的檔案之後

在你請 Claude 編輯 `packages/frontend/src/App.tsx` 之後：

| Skill | 在脈絡中？ | 原因 |
|-------|-------------|--------|
| `shared-conventions` | **是** | 根目錄 `.claude/skills/` 中的專案層級 skill |
| `react-patterns` | **是** | 編輯 `packages/frontend/` 的檔案時被探索到 |
| `api-design` | **否** | 仍未被探索 —— 還沒處理 `packages/backend/` 的檔案 |
| `utils-patterns` | **否** | 仍未被探索 —— 還沒處理 `packages/shared/` 的檔案 |

**關鍵洞察**：巢狀 skills 是在你處理那些目錄的檔案時**按需**探索的，不會在 session 啟動時預載。

## 關鍵行為：description vs 完整內容

skill 的 description 會載入脈絡讓 Claude 知道有哪些可用，但**完整的 skill 內容只在被呼叫時才載入**。這是個重要的最佳化：

- **description**：一律在脈絡中（在字元預算範圍內）
- **完整內容**：skill 被呼叫時按需載入

> 注意：預載 skills 的子代理運作方式不同 —— 完整 skill 內容會在啟動時注入。

## 優先順序（當 skills 同名時）

當不同層級有同名的 skills 時，優先層級較高的勝出：

| 優先序 | 位置 | 範圍 |
|----------|----------|-------|
| 1（最高） | 企業 | 全組織 |
| 2 | 個人（`~/.claude/skills/`） | 你的所有專案 |
| 3（最低） | 專案（`.claude/skills/`） | 僅此專案 |

外掛 skills 使用 `plugin-name:skill-name` 命名空間，所以不會與其他層級衝突。

## 這個設計為什麼適合 Monorepo

- **套件專屬 skills 保持隔離** —— 在 `packages/frontend/` 工作的前端開發者會拿到前端專屬 skills，不會被後端 skills 塞滿脈絡。

- **自動探索減少設定成本** —— 不需明確註冊套件層級 skills；你在那些目錄工作時它們就會被探索到。

- **脈絡經過最佳化** —— 一開始只載入 skill description，巢狀 skills 則按需探索。

- **各團隊可維護自己的 skills** —— 每個套件團隊都能定義自己領域的 skills，不必與其他團隊協調。

## 字元預算的考量

skill description 載入脈絡時有字元預算上限（預設 15,000 字元）。在套件與 skills 很多的大型 monorepo 中，你可能會碰到這個上限。

- 執行 `/context` 檢查是否有 skill 被排除的警告
- 設定 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 環境變數以提高上限

## 最佳實踐

1. **共用工作流放根目錄 `.claude/skills/`** —— 整個 repo 適用的慣例、commit 工作流與共通模式。

2. **套件專屬 skills 放套件的 `.claude/skills/`** —— 框架專屬模式、元件慣例、該套件獨有的測試工具。

3. **危險的 skill 設 `disable-model-invocation: true`** —— 部署或破壞性的 skill 應該要求使用者明確呼叫。

4. **保持 skill description 精簡** —— description 一律在脈絡中（在字元預算內），冗長的描述會浪費脈絡空間。

5. **在 skill 名稱中使用命名空間** —— 考慮用套件名稱當前綴（例如 `frontend-review`、`backend-deploy`）以避免混淆。

## 比較：Skills vs CLAUDE.md 的載入方式

| 行為 | CLAUDE.md | Skills |
|----------|-----------|--------|
| 祖先載入（往目錄樹上） | 是 | 否 |
| 巢狀／後代探索（往目錄樹下） | 是（延遲） | 是（自動探索） |
| 全域位置 | `~/.claude/CLAUDE.md` | `~/.claude/skills/` |
| 專案位置 | `.claude/` 或 repo 根目錄 | `.claude/skills/` |
| 內容載入 | 完整內容 | 僅 description（呼叫時才完整載入） |

---

## 資料來源

- [Claude Code Documentation - Extend Claude with Skills](https://code.claude.com/docs/en/skills)
- [Claude Code Documentation - Automatic Discovery from Nested Directories](https://code.claude.com/docs/en/skills#automatic-discovery-from-nested-directories)
