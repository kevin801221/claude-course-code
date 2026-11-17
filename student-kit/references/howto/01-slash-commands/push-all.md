---
description: 暫存所有變更，建立提交併推送到遠端（請謹慎使用）
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(git diff:*), Bash(git log:*), Bash(git pull:*)
---

# 提交併推送全部內容

⚠️ **注意**：將所有變更都暫存、提交併推送到遠端。只有在你確認所有改動都應該放在一起時才使用。

## 工作流程

### 1. 分析變更
並行執行：
- `git status` - 顯示已修改/已新增/已刪除/未跟蹤檔案
- `git diff --stat` - 顯示變更統計
- `git log -1 --oneline` - 檢視最近一次提交，便於統一提交資訊風格

### 2. 安全檢查

**❌ 如果發現以下內容，立即停止並警告：**
- Secrets：`.env*`、`*.key`、`*.pem`、`credentials.json`、`secrets.yaml`、`id_rsa`、`*.p12`、`*.pfx`、`*.cer`
- API Keys：任何 `*_API_KEY`、`*_SECRET`、`*_TOKEN` 變數包含真實值，而不是佔位符，如 `your-api-key`、`xxx`、`placeholder`
- 大檔案：`>10MB` 且未使用 Git LFS
- 建置產物：`node_modules/`、`dist/`、`build/`、`__pycache__/`、`*.pyc`、`.venv/`
- 臨時檔案：`.DS_Store`、`thumbs.db`、`*.swp`、`*.tmp`

**API Key 校驗：**
檢查修改檔案中是否存在以下模式：
```bash
OPENAI_API_KEY=sk-proj-xxxxx  # ❌ 檢測到真實金鑰！
AWS_SECRET_KEY=AKIA...         # ❌ 檢測到真實金鑰！
STRIPE_API_KEY=sk_live_...    # ❌ 檢測到真實金鑰！

# ✅ 可接受的佔位符：
API_KEY=your-api-key-here
SECRET_KEY=placeholder
TOKEN=xxx
API_KEY=<your-key>
SECRET=${YOUR_SECRET}
```

**✅ 確認：**
- `.gitignore` 設定正確
- 沒有合併衝突
- 分支正確（如果是 `main`/`master` 要提醒）
- API key 只是佔位符

### 3. 請求確認

展示摘要：
```
📊 變更摘要：
- X 個檔案已修改，Y 個檔案已新增，Z 個檔案已刪除
- 總計：+AAA 行新增，-BBB 行刪除

🔒 安全性：✅ 無 secrets | ✅ 無大檔案 | ⚠️ [警告]
🌿 分支： [name] → origin/[name]

我將執行：git add . → commit → push

請輸入 'yes' 繼續，或輸入 'no' 取消。
```

**在收到明確的 "yes" 之前不要繼續。**

### 4. 執行（確認後）

按順序執行：
```bash
git add .
git status  # 驗證暫存狀態
```

### 5. 生成提交資訊

分析變更並建立 conventional commit：

**格式：**
```
[type]: 簡要摘要（最多 72 個字元）

- 關鍵改動 1
- 關鍵改動 2
- 關鍵改動 3
```

**型別：** `feat`、`fix`、`docs`、`style`、`refactor`、`test`、`chore`、`perf`、`build`、`ci`

**範例：**
```
docs: 更新概念文件，補充完整說明

- 新增架構圖和表格
- 補充實用範例
- 擴充套件最佳實踐部分
```

### 6. 提交併推送

```bash
git commit -m "$(cat <<'EOF'
[生成的提交資訊]
EOF
)"
git push  # 如果失敗：git pull --rebase && git push
git log -1 --oneline --decorate  # 驗證
```

### 7. 確認成功

```
✅ 已成功推送到遠端！

Commit: [hash] [message]
Branch: [branch] → origin/[branch]
Files changed: X (+insertions, -deletions)
```

## 錯誤處理

- `git add` 失敗：檢查許可權、鎖定檔案，確認儲存庫已初始化
- `git commit` 失敗：修復 pre-commit hooks，檢查 git 設定（user.name/email）
- `git push` 失敗：
  - 非快進：`git pull --rebase && git push`
  - 沒有遠端分支：`git push -u origin [branch]`
  - 受保護分支：改用 PR 工作流程

## 適用場景

✅ **適合：**
- 多檔案文件更新
- 同時包含測試和文件的功能
- 跨多個檔案的 bug 修復
- 專案級格式化/重構
- 設定變更

❌ **避免：**
- 不確定要提交哪些內容
- 包含 secrets/敏感資料
- 受保護分支且未經過稽核
- 存在合併衝突
- 想保留更細粒度的提交歷史
- pre-commit hooks 失敗

## 替代方案

如果使用者想保留控制權，可以建議：
1. **選擇性暫存**：檢視並暫存特定檔案
2. **互動式暫存**：使用 `git add -p` 逐塊選擇
3. **PR 工作流程**：建立分支 → 推送 → 發起 PR（使用 `/pr` 命令）

**⚠️ 記住**：在推送前始終先檢查變更。拿不準時，使用單獨的 git 命令會更可控。
