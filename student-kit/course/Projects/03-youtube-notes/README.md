# 小專案 3：youtube-notes — YouTube 連結變學習筆記

> 朋友傳「必看！」30 分鐘的 YouTube → 你 5 分鐘看完結構化重點。

## 為什麼做

- ❌ 朋友傳 30 分鐘 YouTube「必看！」，你沒時間
- ❌ 一邊看一邊 take note 累死
- ✅ 丟連結給 Claude → 1 分鐘給你 markdown 筆記 + 關鍵時間戳

## 用到的 Claude Code feature

- Skill (`.claude/skills/youtube-notes/SKILL.md`)
- Bash 跑 `yt-dlp` 抓字幕

## 前置：裝 yt-dlp

```bash
# macOS
brew install yt-dlp

# Linux
pip install --user yt-dlp

# 驗證
yt-dlp --version
```

## 安裝 skill

### 方式 A：個人層

```bash
mkdir -p ~/.claude/skills
cp -r .claude/skills/youtube-notes ~/.claude/skills/
```

### 方式 B：專案層

```bash
cd ~/your-repo
mkdir -p .claude/skills
cp -r /path/to/this-folder/.claude/skills/youtube-notes .claude/skills/
```

## 使用

```bash
claude
> 幫我整理 https://youtu.be/xxxxx 的筆記
```

或更明確：
```bash
> 用 youtube-notes skill 整理這個影片
```

## 範例輸出

```markdown
## 🎬 「Claude Code 從入門到進階」— 全長 32 分 / 讀完 5 分

### 💡 三大重點 (附 [時間戳])
- Hooks 是最被低估的功能 [8:30 講者 demo notify]
- 自訂 slash command 是最低門檻入手 [15:20]
- MCP 讓 Claude 能接任何資料源 [22:10]

### 📚 提到的工具 / 概念
- yt-dlp / ffmpeg / pbpaste / pbcopy
- Sub-agent description 寫法
- Hook exit code 規則

### 🤔 我的一句話觀察
講者的「unix pipeline」哲學是核心 — 別把 Claude 當聊天 bot，
要當 unix command 串接。
```

## 進階變化

- **podcast 也能用** — 有 transcript 的 podcast 一樣 work
- **自動翻譯** — 英文影片自動翻中文筆記
- **存 Notion** — 串 Notion MCP 一鍵入庫
- **讀書會** — 給多支影片，自動生討論題目
- **時段筆記** — 「只整理 5:00-15:00 那段重點」

## 故障排除

| 症狀 | 解法 |
|---|---|
| `yt-dlp: command not found` | `brew install yt-dlp` |
| 沒有字幕 | 影片本來就沒字幕，叫 Claude 用 `--write-sub` 試 manual sub |
| 中文字幕亂碼 | 加 `--sub-lang zh-Hant,zh-Hans,zh,en` |
| 影片是 private | 沒救，要 owner 開放 |
