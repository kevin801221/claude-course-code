# Wafer Defect Detection — 課程模板

> 學生課堂用空白模板。
> 你會用 `/agents` 親手建出 4 個 sub-agent，最後跑完一個 wafer YOLO pipeline。

## 你會做什麼

1. 建 4 個 sub-agent（data-hunter / bbox-labeler / training-runner / inference-runner）
2. 讓 Claude Code 自動路由到正確的 agent
3. 跑完整 pipeline：抓資料 → 切分 → 訓練 → 推論
4. 產出 10 張帶 bbox 的視覺化 + mAP 數字

## 開始前你需要

- [ ] 已安裝 Claude Code、Node 18+、uv、Python 3.11+
- [ ] 已申請 Roboflow 免費帳號（https://app.roboflow.com）
- [ ] 已複製 Roboflow Private API Key

## 第一步：設定環境變數

複製 `.env.example` 成 `.env`，把你的 Roboflow API key 填進去：

```bash
cp .env.example .env
# 編輯 .env，把 YOUR_KEY_HERE 換成你的 key
```

⚠️ **絕不要把 `.env` commit 進 git**（`.gitignore` 已經保護）。

## 第二步：啟動 Claude Code

```bash
claude
```

進入後請看 [_Context/lesson-flow.md](_Context/lesson-flow.md)，跟著步驟一個一個建 agent。

## 資料夾結構

```
.
├── .claude/agents/    # 你的 sub-agent 會放這裡（目前空）
├── _Context/          # 領域知識 + 課程指引
├── Projects/          # 你的訓練結果會放這裡（目前空）
├── .env.example       # API key 範本
├── .gitignore         # 保護 .env
├── CLAUDE.md          # Claude Code 自動讀取的專案規則
└── README.md          # 你正在看的這份
```

## 卡住了？

看 [_Context/troubleshooting.md](_Context/troubleshooting.md)。
