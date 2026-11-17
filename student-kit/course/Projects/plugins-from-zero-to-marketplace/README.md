# 3 個 Plugin 從設計到註冊（完整教學）

> 這份教學帶你從 **想做一個 plugin** 走到 **別人能 `/plugin install` 用**。
> 內附 3 個範例 plugin（personal-productivity / dev-essentials / fun-pack）。

---

## 📋 目錄

1. [`.claude/plugins/` 是什麼？（破除誤會）](#1-claudeplugins-是什麼破除誤會)
2. [Plugin 是什麼 vs 直接放 `.claude/`](#2-plugin-是什麼-vs-直接放-claude)
3. [一個 plugin 的完整解剖](#3-一個-plugin-的完整解剖)
4. [3 個範例 plugin 的設計思路](#4-3-個範例-plugin-的設計思路)
5. [從 0 到別人能 install — 6 步驟](#5-從-0-到別人能-install--6-步驟)
6. [註冊到 Marketplace](#6-註冊到-marketplace)
7. [版本管理 + 升級流程](#7-版本管理--升級流程)
8. [常見坑 + Best Practices](#8-常見坑--best-practices)

---

## 1. `.claude/plugins/` 是什麼？（破除誤會）

**結論：`.claude/plugins/` 不是 Claude Code 自動讀取的標準路徑。**

Claude Code 自動載入的只有：

```
.claude/
├── commands/        ← 自訂 slash commands
├── agents/          ← sub-agents
├── skills/          ← skills (每個 skill 一個資料夾)
├── hooks/           ← hook scripts (在 settings.json 註冊)
├── output-styles/   ← 自訂 output style
└── settings.json    ← 含 mcpServers / hooks / permissions
```

**Plugin 是另一個機制**：
- 別人寫好的「skill + agent + command + hook 套裝」
- 透過 `/plugin marketplace add` 加 marketplace（GitHub repo）
- 透過 `/plugin install` 安裝個別 plugin
- Claude Code 自己管 cache 路徑（在 `~/.claude/plugin-cache/` 之類的地方，使用者不直接放）

所以：
- ❌ **不要** 把 plugin 源碼放在 `.claude/plugins/`（不會被讀）
- ✅ **要** 把 plugin 源碼放在獨立 GitHub repo 的 `plugins/<name>/` 結構下
- ✅ 安裝時透過 `/plugin marketplace add <你的 repo>`

這就是這份教學專案 `Projects/plugins-from-zero-to-marketplace/` 的結構由來。

---

## 2. Plugin 是什麼 vs 直接放 `.claude/`

| | **直接放 `.claude/`** | **包成 Plugin** |
|---|---|---|
| 適合 | 個人用、單一 repo | 跨團隊分享、跨專案共用、公開分享 |
| 安裝 | `cp` 到 `~/.claude/` 或 `<repo>/.claude/` | `/plugin install <name>` |
| 升級 | 手動 `cp` 一次 | `/plugin update <name>` |
| 版本 | 沒有 | semver + git tag |
| 成本 | 5 秒 | 30 分鐘建構（一次） |

**規則**：自己用 → 直接放；想給別人用 → 包 plugin。

---

## 3. 一個 Plugin 的完整解剖

```
plugins/personal-productivity/
├── .claude-plugin/
│   └── plugin.json              ← 必要！manifest
├── commands/                    ← 0 或多個自訂 slash commands
│   └── weekly-haiku.md
├── agents/                      ← 0 或多個 sub-agents
│   └── code-reviewer.md
├── skills/                      ← 0 或多個 skills
│   └── youtube-notes/
│       └── SKILL.md
├── hooks/                       ← 0 或多個 hook scripts
│   └── pomodoro.sh             (chmod +x)
└── README.md                    ← 強烈建議寫
```

### plugin.json 必要欄位

```json
{
  "name": "personal-productivity",          // kebab-case，全 marketplace 唯一
  "version": "1.0.0",                        // semver
  "description": "個人生產力套件...",         // 必填，marketplace 會顯示
  "author": "kevinluo",                      // 選填
  "license": "MIT",                          // 強烈建議
  "homepage": "https://github.com/...",      // 選填
  "components": {                            // 列出包含什麼（給 Claude 看）
    "commands": ["weekly-haiku"],
    "hooks": ["pomodoro"],
    "skills": ["youtube-notes"],
    "agents": []
  }
}
```

---

## 4. 3 個範例 Plugin 的設計思路

### Plugin 1：[`personal-productivity`](plugins/personal-productivity/README.md)
- **目標族群**：所有開發者（最廣）
- **內含**：weekly-haiku（slash）+ pomodoro（hook）+ youtube-notes（skill）
- **為什麼這樣 bundle**：3 個都是「個人偏好、跨專案、健康/生活」性質，邏輯上是同一類使用者要的

### Plugin 2：[`dev-essentials`](plugins/dev-essentials/README.md)
- **目標族群**：認真寫 code 的工程師
- **內含**：code-reviewer（agent）+ prod-guard（hook）+ post-edit-format（hook）
- **為什麼這樣 bundle**：「寫 code 安全網」三件套——review 品質 + 防爆 production + 自動格式化

### Plugin 3：[`fun-pack`](plugins/fun-pack/README.md)
- **目標族群**：想玩 / 想 demo 的人
- **內含**：recipe-genie（agent）+ commit-poet（slash）
- **為什麼這樣 bundle**：純好玩，適合公開課 demo 觀眾會「哈哈」的東西。版本標 `0.1.0` 提示這是 experimental

### Bundle 設計原則

1. **同類使用者** — 一個 plugin 服務同一群人。不要把「給律師的工具」跟「給工程師的工具」混在一起
2. **5±2 個元件** — 太少不值得包、太多 maintenance 痛苦
3. **單一情境** — 取個情境名（productivity / dev / fun）比技術名（hooks-bundle）好懂
4. **依賴清楚** — plugin 用到的外部工具寫在 README（如 yt-dlp、jq、gofmt）

---

## 5. 從 0 到別人能 Install — 6 步驟

### Step 1：建 GitHub repo

```bash
gh repo create my-claude-plugins --public
cd my-claude-plugins
```

或 fork 這個教學 repo 直接改。

### Step 2：建 `marketplace.json`（root）

```json
{
  "name": "My Claude Plugins",
  "description": "...",
  "owner": "yourname",
  "license": "MIT",
  "plugins": [
    {
      "name": "personal-productivity",
      "version": "1.0.0",
      "path": "plugins/personal-productivity",
      "description": "..."
    }
  ]
}
```

### Step 3：建 plugin folder 結構

```bash
mkdir -p plugins/personal-productivity/.claude-plugin
mkdir -p plugins/personal-productivity/{commands,hooks,skills,agents}
```

### Step 4：寫 `plugin.json` manifest

見上面 [3. 一個 Plugin 的完整解剖](#3-一個-plugin-的完整解剖)

### Step 5：放元件 + 寫 README

每個 plugin folder 都該有自己的 README，講：
- 內含什麼
- 為什麼包成 plugin
- 怎麼用（含範例輸出）
- 依賴的外部工具

### Step 6：commit + tag + push

```bash
git add .
git commit -m "Initial release: personal-productivity v1.0.0"
git tag v1.0.0
git push origin main --tags
```

完成！別人裝法見下方。

---

## 6. 註冊到 Marketplace

### 你（plugin 作者）發佈

push 到 GitHub 後別人就能裝，不用「註冊」到任何中央 registry。

### 別人（使用者）安裝你的 plugin

```bash
# 1. 加你的 marketplace（一次性）
> /plugin marketplace add yourname/my-claude-plugins

# 2. 看你 marketplace 有什麼
> /plugin marketplace list yourname/my-claude-plugins

# 3. 裝特定 plugin
> /plugin install personal-productivity

# 4. 看裝了哪些
> /plugin list

# 5. 升級
> /plugin update personal-productivity

# 6. 移除
> /plugin uninstall personal-productivity
```

### 想被收錄到 awesome-claude-code？

社群 awesome 清單（如 `hesreallyhim/awesome-claude-code`、
`rohitg00/awesome-claude-code-toolkit`）開 PR 加你的 plugin entry 即可。

---

## 7. 版本管理 + 升級流程

### Semver 規則

| 改了什麼 | 升哪個位 | 範例 |
|---|---|---|
| 加新指令 / 不影響舊功能 | minor | 1.0.0 → 1.1.0 |
| 改 bug、改 prompt 文字 | patch | 1.1.0 → 1.1.1 |
| 改 plugin name、刪指令、breaking change | major | 1.x.x → 2.0.0 |

### 發佈新版本流程

```bash
# 1. 更新 plugins/<name>/.claude-plugin/plugin.json 的 version
# 2. 更新 marketplace.json 的對應 version
# 3. 寫 CHANGELOG.md
# 4. commit + tag + push

git add .
git commit -m "Release personal-productivity v1.1.0: 加 /commit-roast 指令"
git tag personal-productivity-v1.1.0
git push origin main --tags
```

### 多 plugin 在同 repo 的 tag 規則

- **單 plugin repo** → 用 `v1.0.0`
- **多 plugin repo（這份教學就是）** → 用 `<plugin-name>-v1.0.0` 區分

---

## 8. 常見坑 + Best Practices

### ❌ 常見坑

| 坑 | 解法 |
|---|---|
| 把 plugin 源碼放 `.claude/plugins/` | 不對！放獨立 repo 的 `plugins/<name>/` |
| Hook script 沒 `chmod +x` | 一定要 `chmod +x hooks/*.sh` 後才 commit |
| `plugin.json` 缺 `description` | marketplace UI 會空白，沒人想裝 |
| 版本號跳過 v0.x.x 直接 v1.0.0 | OK 但建議先 0.x.x 跑幾週驗證 |
| 沒 README | 看 marketplace list 不知這 plugin 幹嘛的 |
| 把 secrets commit 進去 | 用 `settings.local.json` + `.gitignore` |
| Plugin 名跟別人撞 | 加 prefix，例：`<your-org>-productivity` |
| 用相對路徑寫死 | 用 `${CLAUDE_PLUGIN_ROOT}` 環境變數 |

### ✅ Best Practices

1. **每個 plugin 寫自己的 README** — 不只 marketplace，個別 plugin 也要
2. **有 examples/ 資料夾** — 照抄就能用
3. **寫 CHANGELOG.md** — 升級透明
4. **License 寫清楚** — 沒 license 公司不敢用
5. **dependencies 條列在 README** — 例：「需要先裝 yt-dlp / jq」
6. **小步發佈** — 1 個元件先發，validation 過再加第 2 個
7. **回應 Issues** — 開源 plugin 有人用就會有 issue，回得快會被信任

---

## 📁 這份教學包的結構

```
plugins-from-zero-to-marketplace/
├── README.md                              ← 你正在看的
├── marketplace.json                        ← marketplace 註冊檔
└── plugins/
    ├── personal-productivity/             ← Plugin 1
    │   ├── .claude-plugin/plugin.json
    │   ├── commands/weekly-haiku.md
    │   ├── hooks/pomodoro.sh
    │   ├── skills/youtube-notes/SKILL.md
    │   └── README.md
    ├── dev-essentials/                    ← Plugin 2
    │   ├── .claude-plugin/plugin.json
    │   ├── agents/code-reviewer.md
    │   ├── hooks/prod-guard.sh
    │   ├── hooks/post-edit-format.sh
    │   └── README.md
    └── fun-pack/                          ← Plugin 3
        ├── .claude-plugin/plugin.json
        ├── agents/recipe-genie.md
        ├── commands/commit-poet.md
        └── README.md
```

## 🚀 你下一步

1. **想看實際 plugin 怎麼長**：分別開 `plugins/<name>/README.md`
2. **想自己發 plugin**：fork 這個 repo、改 marketplace.json + plugin.json
3. **想看 production-grade plugin**：去看 `../build-gitnexus-skill-commandline/` 跟 [GitNexus repo](https://github.com/abhigyanpatwari/GitNexus)

## 📚 對照其他教學文件

- 概念講解 → `../../Claude_Code_完整教學.pptx` Part 11 + Part 11.X
- 詳細建構 → `../../Claude_Code_建構指南.md` Part 5.6
