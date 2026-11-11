# 小專案 2：recipe-genie 冰箱食譜助手

> 開冰箱看一眼：「蛋、培根、青菜、半罐番茄醬」→ 跟 recipe-genie 說 → 30 秒給你 3 個食譜選項。

## 為什麼做

- ❌ 下班開冰箱不知道吃啥，常常變成叫外送
- ❌ Google「蛋 培根 青菜 食譜」結果像論文
- ✅ 直接告訴 AI 你有啥，給你 3 個選項 + cook time + 缺什麼

## 用到的 Claude Code feature

- Sub-agent (`.claude/agents/recipe-genie.md`)
- `WebSearch` + `WebFetch` 權限 — 讓 agent 搜尋網路食譜
- 模型：`sonnet`（日常任務不用 opus）

## 安裝

### 方式 A：個人層

```bash
mkdir -p ~/.claude/agents
cp .claude/agents/recipe-genie.md ~/.claude/agents/
```

### 方式 B：專案層

```bash
cd ~/your-repo
mkdir -p .claude/agents
cp /path/to/this-folder/.claude/agents/recipe-genie.md .claude/agents/
```

## 使用

```bash
claude
> recipe-genie，我有蛋、培根、青菜、白飯
```

或讓 Claude 自動派（看 description 判斷）：
```bash
> 我冰箱有蛋、培根、青菜、白飯，今晚晚餐吃啥
```

## 範例輸出

```
🍳 培根蛋炒飯 (中式)
⏱ 15 分 / easy
🛒 你都有了！缺：蔥（沒有也行）
📝
- 培根切丁先煎香逼油
- 蛋打散下鍋炒成顆粒狀盛起
- 飯下鍋拌炒，回培根+蛋+青菜，鹽糖醬油調味

🍳 Carbonara (意式)
⏱ 20 分 / medium
🛒 缺：義大利麵、起司、黑胡椒
📝
...

Want full recipe for which one?
```

## 進階變化

- **加飲食限制**：「我吃素 / 過敏花生 / 低碳」
- **配酒建議**：再串一個 wine-pairing agent
- **週菜單版**：「給我這週 5 天晚餐 + 一張買菜清單」
- **學技巧版**：選定一個食譜後問「教我這道菜的 3 個關鍵技巧」

## 故障排除

| 症狀 | 解法 |
|---|---|
| Claude 沒派 recipe-genie | 在 prompt 明確說「請 recipe-genie 處理」|
| 食譜太複雜 | 在 prompt 加「30 分鐘內可完成」|
| 老是推薦中式 | 在 prompt 加「給我 1 中 1 西 1 日」|

## 把這個專案推上 GitHub

第一次玩 GitHub？看 [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md) — 完整三方案教學：

- **方案 A**：gh CLI + SSH key（日常 push/pull 必學，含雙帳號設定）
- **方案 B**：GitHub MCP（讓 Claude Code 直接讀 PR、開 issue）
- **方案 C**：Personal Access Token（MCP / CI / script 用）

含常見錯誤排查（Permission denied、push 錯帳號、token 過期…）。
