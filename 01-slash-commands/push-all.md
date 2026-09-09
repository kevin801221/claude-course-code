---
description: 暫存所有變更、建立 commit 並推送到遠端（請謹慎使用）
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(git diff:*), Bash(git log:*), Bash(git pull:*)
---

# 提交並推送所有變更

⚠️ **注意**：這會暫存「所有」變更、建立 commit 並推送到遠端。只有在確信所有變更都屬於同一批時才使用。

## 工作流程

### 1. 分析變更

平行執行：
- `git status` — 顯示已修改／新增／刪除／未追蹤的檔案
- `git diff --stat` — 顯示變更統計
- `git log -1 --oneline` — 顯示最近一次 commit，作為訊息風格參考

### 2. 安全檢查

**❌ 偵測到以下情況時，停止並提出警告：**
- 機密資訊：`.env*`、`*.key`、`*.pem`、`credentials.json`、`secrets.yaml`、`id_rsa`、`*.p12`、`*.pfx`、`*.cer`
- API 金鑰：任何帶有實際數值（而非 `your-api-key`、`xxx`、`placeholder` 這類佔位字串）的 `*_API_KEY`、`*_SECRET`、`*_TOKEN` 變數
- 大型檔案：超過 `10MB` 且未使用 Git LFS
- 建置產物：`node_modules/`、`dist/`、`build/`、`__pycache__/`、`*.pyc`、`.venv/`
- 暫存檔案：`.DS_Store`、`thumbs.db`、`*.swp`、`*.tmp`

**API 金鑰驗證：**
檢查已修改的檔案是否含有以下模式：
```bash
OPENAI_API_KEY=sk-proj-xxxxx  # ❌ 偵測到真實金鑰！
AWS_SECRET_KEY=AKIA...         # ❌ 偵測到真實金鑰！
STRIPE_API_KEY=sk_live_...    # ❌ 偵測到真實金鑰！

# ✅ 可接受的佔位字串：
API_KEY=your-api-key-here
SECRET_KEY=placeholder
TOKEN=xxx
API_KEY=<your-key>
SECRET=${YOUR_SECRET}
```

**✅ 確認事項：**
- `.gitignore` 設定正確
- 沒有合併衝突
- 分支正確（若為 main／master 要提出警告）
- API 金鑰只是佔位字串

### 3. 要求使用者確認

呈現摘要：
```
📊 變更摘要：
- X 個檔案修改、Y 個新增、Z 個刪除
- 總計：+AAA 行新增、-BBB 行刪除

🔒 安全性：✅ 無機密資訊 | ✅ 無大型檔案 | ⚠️ [警告內容]
🌿 分支：[名稱] → origin/[名稱]

我將執行：git add . → commit → push

輸入「yes」以繼續，或輸入「no」以取消。
```

**在得到明確的「yes」之前，先等待確認。**

### 4. 執行（確認後）

依序執行：
```bash
git add .
git status  # 確認暫存結果
```

### 5. 產生提交訊息

分析變更並建立符合 conventional commits 的訊息：

**格式：**
```
[type]: 簡短摘要（最多 72 個字元）

- 關鍵變更 1
- 關鍵變更 2
- 關鍵變更 3
```

**類型：** `feat`、`fix`、`docs`、`style`、`refactor`、`test`、`chore`、`perf`、`build`、`ci`

**範例：**
```
docs: 更新概念說明 README 檔案，補齊完整文件

- 加入架構圖與表格
- 加入實際範例
- 擴充最佳實踐段落
```

### 6. 提交並推送

```bash
git commit -m "$(cat <<'EOF'
[產生的提交訊息]
EOF
)"
git push  # 若失敗：git pull --rebase && git push
git log -1 --oneline --decorate  # 確認結果
```

### 7. 確認成功

```
✅ 已成功推送到遠端！

Commit：[hash] [message]
分支：[branch] → origin/[branch]
變更檔案數：X（+新增行數，-刪除行數）
```

## 錯誤處理

- **git add 失敗**：檢查權限、是否有檔案被鎖定、確認儲存庫已初始化
- **git commit 失敗**：修正 pre-commit hooks、檢查 git 設定（user.name／email）
- **git push 失敗**：
  - 非快進式（Non-fast-forward）：`git pull --rebase && git push`
  - 遠端沒有對應分支：`git push -u origin [branch]`
  - 受保護分支：改用 PR 工作流程

## 何時使用

✅ **適合使用：**
- 多檔案的文件更新
- 含測試與文件的功能開發
- 跨檔案的錯誤修正
- 專案整體的格式化／重構
- 設定變更

❌ **避免使用：**
- 不確定要提交什麼內容
- 內含機密／敏感資料
- 受保護分支且未經審查
- 存在合併衝突
- 想要更細緻的 commit 歷史
- pre-commit hooks 執行失敗

## 替代方案

若使用者想要更多控制權，建議：
1. **選擇性暫存**：檢視／暫存特定檔案
2. **互動式暫存**：使用 `git add -p` 進行區塊選取
3. **PR 工作流程**：建立分支 → 推送 → 建立 PR（使用 `/pr` 指令）

**⚠️ 提醒**：推送前務必先檢視變更內容。若有疑慮，改用個別的 git 指令以取得更多控制權。

---
**最後更新**：2026 年 8 月 4 日
**Claude Code 版本**：2.1.220
**資料來源**：
- https://code.claude.com/docs/en/commands
**相容模型**：Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
