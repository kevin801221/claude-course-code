# 小專案 5：整理塞滿 1.2k 個檔案的 Downloads

> Downloads 半年沒整理 → 一行指令裝 filesystem MCP → 跟 Claude 說「整理一下」→ 5 分鐘乾淨。

## 為什麼做

- ❌ Downloads 1.2k 個檔案、半年沒整理
- ❌ 手動分類想到就頭痛
- ✅ 接 filesystem MCP，Claude 自己看、自己分類、自己搬

## 用到的 Claude Code feature

- 官方 `@modelcontextprotocol/server-filesystem` MCP server
- 不需自己寫 code

## 安裝

### 一行指令裝（推薦）

```bash
claude mcp add fs -- npx -y @modelcontextprotocol/server-filesystem ~/Downloads
```

### 或手動編輯 settings.json

把這個 repo 的 `.claude/settings.json` 內容 merge 進你的：
- 個人層：`~/.claude/settings.json`
- 專案層：`.claude/settings.json`

⚠️ **記得改 `YOUR_USERNAME`** 成你的 Mac 帳號名稱。

### 確認連線

```bash
claude
> /mcp
# 應該看到：fs ✓ connected
```

## 使用

### Step 1：先看一眼

```bash
> 用 fs MCP 看 ~/Downloads 統計：總共幾個檔、依副檔名分類
```

Claude 會回類似：
```
Downloads 共 1,247 個檔案
- .pdf:   312 (合約、發票、論文...)
- .png:   289 (截圖)
- .zip:   198 (下載過的安裝檔)
- .dmg:    47 (macOS 安裝檔)
- .mp4:    23
- .docx:   18
- 其他:   360
```

### Step 2：建子資料夾分類

```bash
> 在 ~/Downloads 建子資料夾：images / pdfs / installers / archives / videos
> 把對應檔案搬進去，跑之前先給我清單讓我確認
```

### Step 3：清掉太久沒動的

```bash
> 找 6 個月以上沒動的檔案，列清單問我要不要刪
```

## 進階變化

### 變化 1：依日期分

```bash
> 把 Downloads 依下載日期分到 2024-Q1 / 2024-Q2 / 2024-Q3 / 2024-Q4 / 2025
```

### 變化 2：找重複檔案

```bash
> 找 ~/Downloads 內 md5 相同的檔案，列清單問我哪份要保留
```

### 變化 3：搶救 Desktop

```bash
# 改授權範圍到 Desktop
claude mcp add fs npx -y @modelcontextprotocol/server-filesystem ~/Desktop
```

### 變化 4：週末自動跑（搭配 cron + claude -p）

```bash
# crontab -e
0 10 * * 6  cd ~ && claude -p "用 fs MCP 整理 Downloads 一次" \
  --allowed-tools "mcp__fs__*" --max-turns 20
```

## 安全提醒

- ⚠️ filesystem MCP 給 Claude 完整讀寫權限到該資料夾
- ⚠️ 不要把整個 `/` 或 `~` 開放給 Claude
- ⚠️ 重要檔案先備份一份再讓 Claude 動

## 故障排除

| 症狀 | 解法 |
|---|---|
| `/mcp` 看不到 fs | 重啟 claude，再 `claude mcp list` 確認 |
| Claude 說沒權限 | 確認 args 裡的路徑是絕對路徑 |
| 搬檔搬到一半中斷 | 沒事，filesystem MCP 是冪等的，再跑一次會接續 |
| 想撤銷剛剛的整理 | 跟 Claude 說「把剛剛的搬移操作 undo」（它會 mv 回去）|
