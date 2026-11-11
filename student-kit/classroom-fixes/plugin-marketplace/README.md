# 三個完整 Plugin：可攜工作坊修正版

對應講義 Part 14。來源是 `Projects/plugins-from-zero-to-marketplace/`，保留三個名稱與元件關係：`personal-productivity`、`dev-essentials`、`fun-pack`。這裡是課堂修正版，原始快照仍由完整課程區保留。

## 先讀哪個

| Plugin | 內容 | 額外依賴 / 副作用 |
|---|---|---|
| [fun-pack](plugins/fun-pack/README.md) | commit 詩稿、食譜 agent | 可先練無 Hook 的本機載入；食譜搜尋需要網路 |
| [personal-productivity](plugins/personal-productivity/README.md) | 週俳句、YouTube notes、PostToolUse 番茄鐘 | git；YouTube 另需 yt-dlp/字幕；工具次數紀錄與可選桌面通知 |
| [dev-essentials](plugins/dev-essentials/README.md) | review agent、PreToolUse guard、PostToolUse formatter | jq；已安裝 formatter 會修改檔案；專案本地編輯紀錄 |

此目錄放在 `classroom-fixes/`，不會隨精華包自動啟用。先複製待練習專案到獨立位置；本機載入只對此次 session 生效。請勿同時載入原始及修正版的同名 plugin。

## 建議主線：本機載入，不做安裝

從精華包根目錄：

```bash
claude plugin validate classroom-fixes/plugin-marketplace
claude plugin validate classroom-fixes/plugin-marketplace/plugins/fun-pack
claude --permission-mode manual --plugin-dir ./classroom-fixes/plugin-marketplace/plugins/fun-pack
```

在互動對話使用 `/fun-pack:commit-poet`。如要換另兩套，關閉 session，將 `--plugin-dir` 換成對應 Plugin 目錄再開啟。需要 agents 時用代理清單確認；`recipe-genie` 和 `code-reviewer` 不是 slash command。

`--plugin-dir` 載入是本機練習，不會把套件安裝到全域 cache，也不會覆寫 `~/.claude/settings.json`。載入後的 Hook 仍會依表列方式操作目前專案；使用者/組織既有設定也仍可能生效。

## 選修：本機 Marketplace 流程

先閱讀 `.claude-plugin/marketplace.json`：`owner` 是 object，條目的 `source` 以 marketplace 根目錄為基準；對應三個 `plugins/<name>/`，不使用原例的 `path` 欄位。這是本機目錄，不是已發布的 GitHub marketplace。

要實際體驗註冊及安裝時，再從精華包根目錄開啟 Claude，於互動對話輸入：

```text
/plugin marketplace add ./classroom-fixes/plugin-marketplace --scope project
/plugin install fun-pack@course-workshop --scope project
```

上述是**選做的實際安裝**，會寫入專案的啟用設定，並可能產生使用者 Plugin/marketplace 快取；本包製作時未執行。先用本機載入即可完成主線，不必為上課先改全域設定。移除時使用自己版本 `/plugin` 的管理介面，或核對 `claude plugin uninstall --help` 與 `claude plugin marketplace remove --help`；先分清專案啟用狀態與共享 marketplace 快取。

## 與原例的差異

1. Marketplace 放到正確的 `.claude-plugin/marketplace.json`；名稱改為 `course-workshop`，`owner` object、`source` 相對路徑取代過時欄位。
2. 各 `plugin.json` 使用 author object，移除未支援的 `components`，以標準元件目錄探索。
3. 兩個含 Hook 的 Plugin 各加上 `hooks/hooks.json`；腳本路徑使用加引號的 `${CLAUDE_PLUGIN_ROOT}`。
4. Counter/log 改寫目前專案 `.outputs/plugin-demo/`，避免原例直接寫 HOME；日期命令改為 macOS/Linux 都可用的格式。
5. guard 缺 jq/格式錯誤時明確拒絕，formatter 缺 jq 時標示 skipped。這仍是教學 guard，未升格為安全沙箱。
6. 代理使用 `inherit`；週俳句不依賴巢狀 shell 作者查詢，輸出只作草稿；YouTube Skill 改為手動並明列缺資料要停止。

保留來源 [MIT](LICENSE)。來源與逐檔改寫會列入整體 manifest。靜態 validator 不證明模型、MCP、桌面通知、yt-dlp 或 formatter 端到端整合可用。

## 本次離線驗證結果

Claude Code 靜態 validator 已實跑 marketplace 與三個 Plugin，四項皆通過，manifest errors/warnings 皆為 0。Plugin directory 的 `ICON_MISSING` 是上架目錄的非阻擋建議；本工作坊沒有圖示，也沒有宣稱已通過官方上架審查。

另在臨時專案用通知/formatter 替身驗證三支 Hook：計數 1 與 50、通知命令分支、guard 拒絕/放行、formatter 呼叫與專案日誌位置皆符合預期。沒有發出真通知、修改真實來源檔、寫使用者設定、呼叫模型或安裝 Plugin。
