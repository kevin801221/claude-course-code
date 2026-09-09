# Claude Code Skill 層級完全指南

> Skill 到底存在哪？為什麼有些看得到、有些找不到？這份文件用你機器上的真實路徑解釋四個層級，並附排查指令。

## TL;DR

Claude Code 的 skill 來自**四個獨立來源**，會被合併成同一份清單給模型用：

| 層級 | 路徑 | namespace | 跟 git 走？ |
|---|---|---|---|
| **1. Project** | `<repo>/.claude/skills/<name>/SKILL.md` | 無 | ✅ commit 進 repo |
| **2. User** | `~/.claude/skills/<name>/SKILL.md` | 無 | ❌ 個人機器 |
| **3. Plugin** | `~/.claude/plugins/cache/<market>/<plugin>/<ver>/skills/<name>/SKILL.md` | `plugin-name:skill-name` | ❌ marketplace 訂閱 |
| **4. Built-in slash** | Claude Code 二進位內建 | 無 | n/a |

看 skill 名字就能判斷來源：**名字含 `:` = plugin、不含 `:` = project / user**。

---

## 1️⃣ Project-scope skills（最常用，跟 repo 走）

### 路徑

```
<your-project>/.claude/skills/<skill-name>/SKILL.md
```

可選的同層檔案：
- `references/*.md` — 模型可選擇載入的補充資料（例如模板、SOP）
- `scripts/*.py` — 模型可執行的腳本

### 何時用

- **整個團隊都該遵守的規則**：例如本專案的 `rag-pipeline`（每 chunk 必含 chunk_id、metadata schema 鎖死）
- **跟 repo 強耦合的工作流**：例如 `cli-extension-sync`（`/sync` 跑這個 repo 內的 `.collab-sync.md`）

### 命名

無 namespace，直接 `rag-pipeline`、`fastapi-uv-setup`。Claude Code 會用 `Skill(rag-pipeline)` invoke。

### 真實案例

本專案的 `.claude/skills/`：

```
.claude/
├── skills/
│   ├── fastapi-uv-setup/SKILL.md
│   ├── rag-pipeline/SKILL.md
│   ├── graph-extraction/SKILL.md
│   ├── force-graph-ui/SKILL.md
│   └── cli-extension-sync/
│       ├── SKILL.md
│       └── references/
│           └── sync_template.md
└── commands/
    └── sync.md
```

---

## 2️⃣ User-scope skills（個人跨專案習慣）

### 路徑

```
~/.claude/skills/<skill-name>/SKILL.md
```

### 何時用

- **跨所有專案都想要的個人習慣**：例如自己寫的 `code-style-zh`（一律繁中註解）、`uv-only`（禁 pip）
- **不適合塞進某個 repo 的協作協議**：例如「commit 後寄 Slack 通知給自己」這種

### 命名

跟 Project-scope 一樣無 namespace。

### 衝突處理

當 project 跟 user 有同名 skill 時，**Claude Code 載入 project 版（覆蓋 user 版）**。這個機制讓 repo 可以「override」個人習慣。

### 真實案例

你機器上 `~/.claude/skills/` 大部分是 **firecrawl symlink**（不是你手動裝的，是 firecrawl 安裝時放的）：

```bash
$ ls ~/.claude/skills/
firecrawl -> ../../.agents/skills/firecrawl
firecrawl-agent -> ../../.agents/skills/firecrawl-agent
firecrawl-build-interact -> ../../.agents/skills/firecrawl-build-interact
...（還有十幾個）
```

那些 `../../.agents/skills/...` 是 firecrawl 的 user-level 安裝目錄（`~/.agents/`），跟 `.claude/` 是兩套東西，不要搞混。

> **注意**：你個人有想跨專案用的 skill 直接放 `~/.claude/skills/<name>/SKILL.md` 即可。不要動 firecrawl 那些 symlink，它們是 firecrawl 自己管的。

---

## 3️⃣ Plugin-scope skills（你最常混亂的）

### 路徑

```
~/.claude/plugins/
├── marketplaces/                          ← 訂閱了哪些 marketplace
│   ├── cc-marketplace/
│   └── vercel/
├── data/                                  ← 安裝 metadata
│   └── superpowers-claude-plugins-official/
└── cache/                                 ← ⭐ skill 真檔案在這
    └── <marketplace>/
        └── <plugin>/
            └── <version>/
                └── skills/
                    └── <skill-name>/
                        └── SKILL.md
```

### 何時用

- **訂閱別人寫好的 skill**：例如 superpowers（Jesse 的 brainstorming / TDD / debugging 套件）、vercel（Anthropic 官方部署 skill）
- **不想自己維護**：marketplace 升級時，cache 內容跟著換版

### 命名

**有 namespace**，格式 `plugin-name:skill-name`。例如：

| skill 名 | 來自 marketplace | 來自 plugin |
|---|---|---|
| `superpowers:brainstorming` | superpowers-marketplace | superpowers |
| `vercel:nextjs` | claude-plugins-official | vercel |
| `document-skills:pptx` | anthropic-agent-skills | document-skills |
| `firecrawl:firecrawl` | claude-plugins-official | firecrawl |
| `figma:figma-use` | claude-plugins-official | figma |

### 你機器上實況

你機器有 **185 個 plugin SKILL.md**，分布在：

```
~/.claude/plugins/cache/
├── superpowers-marketplace/superpowers/4.0.3/skills/      (~16 個)
├── claude-plugins-official/                                (~80 個 — vercel/playwright/context7/figma...)
├── anthropic-agent-skills/document-skills/                 (~14 個 — pptx/xlsx/pdf/docx...)
├── finlab-plugins/finlab-plugin/1.0.0/                     (1 個)
├── ui-ux-pro-max-skill/                                    (1 個)
├── sinotrade-plugins/                                      (1 個)
└── claude-code-marketplace/                                (其他)
```

**版本號是路徑一部分**——`superpowers/4.0.3/` 升級成 `4.0.4` 時，整個資料夾搬家。所以**永遠不要在 code 裡 hardcode plugin cache 路徑**，會跟著 plugin 升級壞掉。

### invoke 方式

Plugin skill 一定要帶 namespace：

```
✅ Skill(superpowers:brainstorming)
❌ Skill(brainstorming)              ← 錯，會找不到
```

### 排查：訂了哪些 marketplace、裝了哪些 plugin

```bash
# 列訂閱的 marketplace
ls ~/.claude/plugins/marketplaces/

# 列每個 marketplace 下的 plugin
ls ~/.claude/plugins/cache/

# 列某 plugin 下的 skills
ls ~/.claude/plugins/cache/superpowers-marketplace/superpowers/*/skills/
```

---

## 4️⃣ Built-in slash commands（不是 skill，但常被混為一談）

Claude Code 二進位內建幾個 slash command：

| 指令 | 用途 |
|---|---|
| `/init` | 為新專案產生 `CLAUDE.md` |
| `/review` | review 一個 PR |
| `/security-review` | 對當前 branch 做 security review |
| `/loop`, `/schedule` | 來自 plugin（loop / schedule） |

這些**不是 skill**——它們是 commands，由 Claude Code 啟動時內建讀進來。

### Skill vs Command vs Subagent 三者差異

| | 觸發方式 | 內容 | 路徑 |
|---|---|---|---|
| **Skill** | 模型自己判斷 description 後 invoke | YAML frontmatter + markdown 規則 | `.claude/skills/<name>/SKILL.md` |
| **Slash command** | 使用者打 `/<name>` 觸發 | YAML frontmatter + prompt 模板（含 `$ARGUMENTS`） | `.claude/commands/<name>.md` |
| **Subagent** | 主 Claude Code 用 Agent 工具 dispatch | 獨立 conversation，有自己 system prompt | `.claude/agents/<name>.md` |

舉例：
- `Skill(rag-pipeline)` ← 模型自己 invoke 載入規則
- `/sync` ← 使用者打的 slash command（路徑：`.claude/commands/sync.md`）
- `Agent(subagent_type="code-reviewer")` ← 主 agent 開新一輪 conversation 給 subagent 跑

---

## 三個你常踩的坑

### 坑 1：找不到 skill 檔案、但 Claude 卻在用

**原因**：那個 skill 在 plugin cache 裡（`~/.claude/plugins/cache/...`），不在 project / user 兩個你會 grep 的地方。

**解**：

```bash
# 在所有可能的位置找某個 skill
find ~/.claude/plugins/cache ~/.claude/skills <your-project>/.claude/skills \
  -name "SKILL.md" -path "*<skill-name>*" 2>/dev/null
```

### 坑 2：Plugin 升版後我的 reference 失效

**原因**：`~/.claude/plugins/cache/.../v4.0.3/...` 升級成 `v4.0.4` 整個資料夾搬家。

**解**：永遠**不要 hardcode 版本號**到任何 script、絕對不要把 plugin cache 路徑寫進專案的 `CLAUDE.md`。如果非要 reference plugin 內容，用 marketplace 的 stable URL（GitHub repo 的 main branch）。

### 坑 3：兩個 skill 同名，不知道載到哪個

**原因**：`Project skill` > `User skill`（同名時 project 覆蓋 user）；plugin 因為有 namespace 不會撞名。

**解**：刻意撞名是合法的——當你在某個 repo 想 override 個人 user-level skill 時很有用。沒有衝突警告，所以**自己留意**。

---

## 一鍵排查指令

存成 `~/.local/bin/claude-skills-where`（或加 alias）：

```bash
#!/usr/bin/env bash
# 列出當前所有可用 skill 跟它們的真實路徑
set -euo pipefail

PROJECT=${1:-.}

echo "=== Project skills ($PROJECT/.claude/skills/) ==="
find "$PROJECT/.claude/skills" -name "SKILL.md" 2>/dev/null \
  | sed "s|^$PROJECT/.claude/skills/||; s|/SKILL.md\$||"
echo

echo "=== User skills (~/.claude/skills/) ==="
find ~/.claude/skills -maxdepth 3 -name "SKILL.md" 2>/dev/null \
  | sed "s|^$HOME/.claude/skills/||; s|/SKILL.md\$||"
echo

echo "=== Plugin skills (~/.claude/plugins/cache/) ==="
find ~/.claude/plugins/cache -name "SKILL.md" 2>/dev/null \
  | awk -F'/' '{
      # cache/<market>/<plugin>/<ver>/skills/<name>/SKILL.md
      market=$(NF-5); plugin=$(NF-4); skill=$(NF-1);
      print plugin ":" skill "  ← " market
    }' \
  | sort -u
```

跑：

```bash
chmod +x ~/.local/bin/claude-skills-where
claude-skills-where /path/to/project
```

---

## 關鍵心法

1. **看 namespace 判斷來源**：有 `:` = plugin、無 `:` = project / user
2. **Project skills 跟 git 走、user 跟你走、plugin 跟 marketplace 走**
3. **不要 hardcode plugin cache 路徑**——版本號會變
4. **Skill 是模型自動 invoke、Slash command 是使用者手動打、Subagent 是另起 conversation**——三者完全不同

---

## 延伸閱讀

- 本專案 `.claude/skills/cli-extension-sync/SKILL.md`：看一份「IDE Extension ↔ CLI 雙 Agent 協作」skill 怎麼設計
- 本專案 `.claude/commands/sync.md`：看一份 project-scope slash command 怎麼寫
- `walkthrough.md` 的 Phase 0-4：在 Stage 1 教學情境下解釋 Skill auto-load 機制

如果你之後想學「自己寫一份 plugin 上架」，可以參考 `superpowers:writing-skills` 跟 anthropic 官方 `skill-creator` skill。
