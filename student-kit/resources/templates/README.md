# 可帶回自己專案的精選模板

這裡只放手動選用的模板，不會在本 Repo 啟動時自動載入。
`claude-course-code` 與 `claude-howto-zh-TW` 有許多相同功能與衍生內容，本包依用途各留一份，避免重複安裝。

| 精選 | 來源 | 用在哪 | 講義 |
|---|---|---|---|
| [Python doc-generator](skills/doc-generator/README.md) | howto 的 AST 原碼；Skill 說明改寫 | `.claude/skills/` | Part 10 |
| [三個子代理](agents/README.md) | course-code reviewer/test、howto docs | `.claude/agents/` | Part 11 |
| [兩個 slash commands](commands/README.md) | course-code 測試、howto 文件 | `.claude/commands/` | Part 04 |
| [精簡 PRP](context/README.md) | course-code Context Engineering | `task.md` | Part 09/19 |
| [審查清單](review/README.md) | howto code-review-specialist | 人工/代理檢查輸出 | Part 19 |

## 選用原則

先在全新的練習專案試一份，再挑需要的裝進既有專案。複製前檢查是否同名，不整批覆蓋現有 `.claude`。
原始碼與改寫清單見 Repo 的來源清單；授權沿用各來源 MIT，完整授權由根目錄第三方授權檔保留。

## 已修正的教材陷阱

- 原 doc-generator 說明的 OpenAPI/HTTP 範圍大於腳本能力，學生版改成 Python 函式草稿。
- 原代理文件中的模型版本清單不作為相容性承諾，改用 `model: inherit`。
- 不再要求每個測試都 setup/teardown、或未量測就回報涵蓋率。
- 文件 command 的來源/輸出改成專案內的明確路徑。
