# GitHub 連接完整教學（三方案）

> 給「第一次把 Claude Code 專案推上 GitHub」的學員。
> 涵蓋 gh CLI / SSH key / GitHub MCP / Personal Access Token 全部方案，
> 並解釋什麼情境用什麼工具，以及為什麼。

---

## 一、為什麼要分三個方案？

很多初學者卡在這裡：
- 看到網路教學叫你「git push」，結果跳 `Permission denied (publickey)`
- 用了 token 卻不知道要存哪、過期了又得重來
- 看到 Claude 講「用 GitHub MCP」，但其實 `git push` 不會走 MCP

**根本問題**：GitHub 連接其實是**三件不同的事**，混在一起學就會亂。

| 我想做的事 | 該用的方案 |
|---|---|
| 把 code push 上去 / clone 別人的 repo | **方案 A：gh CLI + SSH key** |
| 讓 Claude Code 幫我讀 PR、開 issue、做 code review | **方案 B：GitHub MCP** |
| 寫 CI/CD、自動化 script、跑 GitHub Actions 呼叫 API | **方案 C：PAT (Personal Access Token)** |

三者**不互斥**，多數開發者三個都會用。但學習順序強烈建議：A → B → C。

---

## 二、方案 A：gh CLI + SSH key（基礎必學）

### A.1 為什麼用 SSH 不用 HTTPS？

| | HTTPS | SSH |
|---|---|---|
| 每次 push 要打密碼？ | 要（或設 credential helper） | 不用 |
| 雙帳號切換 | 麻煩，要改 remote URL + 密碼 | 一個 alias 就解決 |
| 防火牆友善度 | 高（80/443） | 中（22 port 有時被擋） |
| 推薦給誰 | 公司網路擋 SSH、純自動化 | **個人開發者、長期使用** |

**結論**：本機開發走 SSH，CI 走 HTTPS+PAT。

### A.2 第一次設定 SSH key（如果沒有）

```bash
# 1. 生 key（ed25519 比較新、比較安全，不要用 rsa）
ssh-keygen -t ed25519 -C "kevin801221@users.noreply.github.com" -f ~/.ssh/id_ed25519

# 2. 啟動 ssh-agent + 加 key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 3. 複製 public key（注意是 .pub 不是私鑰）
pbcopy < ~/.ssh/id_ed25519.pub
# Linux: cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard

# 4. 貼到 GitHub
# 開 https://github.com/settings/keys → New SSH key → 貼上 → Save
```

驗證：
```bash
ssh -T git@github.com
# 應該看到：Hi <你的帳號>! You've successfully authenticated...
```

### A.3 雙帳號設定（個人 + 工作）

這是最多人踩雷的地方。場景：你想把**公司 repo** push 到工作帳號、**個人 side project** push 到個人帳號，但同一台電腦。

#### Step 1：生兩把 key

```bash
# 個人
ssh-keygen -t ed25519 -C "kevin801221@users.noreply.github.com" -f ~/.ssh/id_ed25519

# 工作（不同檔名！）
ssh-keygen -t ed25519 -C "kevin@company.com" -f ~/.ssh/id_ed25519_company
```

兩把 public key 分別貼到對應 GitHub 帳號的 SSH keys 設定。

#### Step 2：寫 `~/.ssh/config`

```ssh-config
# GitHub - 工作帳號（預設）
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_company
    IdentitiesOnly yes

# GitHub - 個人帳號（透過 alias）
Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

關鍵在 `Host github-personal` 這個**虛擬主機名**——SSH 看到這個名字會用個人 key，但實際連的還是真正的 `github.com`。

#### Step 3：clone / push 時用對應 URL

```bash
# 工作 repo（用預設 git@github.com）
git clone git@github.com:CompanyOrg/work-repo.git

# 個人 repo（用 alias git@github-personal）
git clone git@github-personal:kevin801221/recipe-genie.git
```

#### Step 4：每個 repo 設對的 user.name / user.email

`git config --global` 會讓**所有 repo** 共用同一個身份，雙帳號絕對不要這樣做。改用 per-repo：

```bash
cd ~/path/to/personal-repo
git config user.name "kevin801221"
git config user.email "kevin801221@users.noreply.github.com"

cd ~/path/to/work-repo
git config user.name "KevinLegalAI"
git config user.email "kevin@company.com"
```

驗證：在 repo 內跑 `git config user.email`，看出來的 email 對不對。

#### Step 5：驗證雙帳號都通

```bash
ssh -T git@github.com           # 應該說 Hi <工作帳號>!
ssh -T git@github-personal      # 應該說 Hi <個人帳號>!
```

### A.4 gh CLI（GitHub 官方 CLI）

`gh` 不取代 `git`，是補充。`git` 管本機 commit/push，`gh` 管 GitHub 雲端那邊的東西（建 repo、開 PR、看 issue）。

#### 安裝

```bash
# macOS
brew install gh

# 驗證
gh --version
```

#### 登入

```bash
gh auth login
# 互動式問答：
# ? What account do you want to log into? GitHub.com
# ? What is your preferred protocol for Git operations? SSH
# ? Upload your SSH public key to your GitHub account? <選現有的 key>
# ? How would you like to authenticate GitHub CLI? Login with a web browser
```

雙帳號切換：
```bash
gh auth login              # 加第二個帳號
gh auth switch             # 切換 active 帳號
gh auth status             # 看目前是哪個帳號
```

> **常見坑**：如果 shell 有設 `GITHUB_TOKEN` 環境變數，`gh` 會優先吃 token，看起來像登入哪個帳號都沒用。先 `unset GITHUB_TOKEN` 或在 `~/.zshrc` 移掉。

#### 常用指令

```bash
gh repo create recipe-genie --public --source=. --remote=origin --push
# 一行：建 repo + 設 remote + push

gh pr create --title "feat: add bacon recipes" --body "..."
gh pr list
gh pr view 42 --web        # 開瀏覽器看 PR
gh issue create
gh repo clone kevin801221/recipe-genie
```

### A.5 Recipe Genie 實戰：把這個專案推到個人 GitHub

```bash
cd ~/claude-code-complete-tutorial/Projects/02-recipe-genie

# 1. 初始化 git（如果還沒）
git init -b main

# 2. 設定身份（個人）
git config user.name "kevin801221"
git config user.email "kevin801221@users.noreply.github.com"

# 3. 寫 .gitignore（重要！）
cat > .gitignore << 'EOF'
.DS_Store
*.log
.env
.env.local
node_modules/
__pycache__/
EOF

# 4. 第一次 commit
git add .
git commit -m "init: recipe-genie sub-agent 範例"

# 5. 在 GitHub 建 repo（gh CLI 一行搞定）
gh repo create kevin801221/recipe-genie \
  --public \
  --description "冰箱食譜助手 - Claude Code sub-agent 範例" \
  --source=. \
  --remote=origin \
  --push

# 6. 改 remote 走 SSH alias（gh 預設可能設成 git@github.com，要改）
git remote set-url origin git@github-personal:kevin801221/recipe-genie.git

# 7. 驗證
git remote -v
# origin  git@github-personal:kevin801221/recipe-genie.git (fetch)
# origin  git@github-personal:kevin801221/recipe-genie.git (push)

# 8. 之後 push 直接：
git push
```

---

## 三、方案 B：GitHub MCP（讓 Claude Code 直接操作 GitHub）

### B.1 是什麼？不是什麼？

**是**：給 Claude 一組 tool，可以用自然語言叫它「幫我看 PR #42 的 review、列出最近 5 個 issue、回覆 reviewer」。

**不是**：取代 `git push`。push code 還是走 SSH/HTTPS（方案 A）。

**什麼時候裝**：你要讓 Claude 做以下事情時：
- 自動讀 PR diff 並提建議
- 列 issue / 開 issue / 關 issue
- 看 Actions 跑得怎樣
- 做 PR review

如果你只是要 push code，**不需要裝 MCP**。

### B.2 安裝

GitHub 官方 MCP server：https://github.com/github/github-mcp-server

```bash
# Claude Code 內裝（推薦）
claude mcp add github \
  --env GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx \
  -- npx -y @modelcontextprotocol/server-github
```

**注意**：MCP server 走的是 PAT，不是 SSH key。所以你要先有方案 C 的 token（見下節）。

### B.3 在 Claude Code 內驗證

```bash
claude
> /mcp
# 應該看到 github server，狀態 connected
```

實際用：
```
> 列出我 recipe-genie repo 最近 3 個 issue
> 開個 issue 叫 "新增素食食譜支援"
> 看 PR #5 的 review comments
```

### B.4 安全提醒

- MCP server 用的 token **權限不要開太大**：只給用得到的 scope（通常 `repo` + `read:org` 就夠）
- token 寫在 `claude mcp add --env` 的話會存在 Claude Code config，不會 commit 進 repo，但別貼到聊天訊息

---

## 四、方案 C：PAT (Personal Access Token)

### C.1 什麼時候才需要 PAT？

| 情境 | 需要 PAT？ |
|---|---|
| 一般 git push（已用 SSH） | 不需要 |
| GitHub MCP server | 需要 |
| CI/CD（GitHub Actions 例外，用內建 `GITHUB_TOKEN`） | 需要 |
| Script 呼叫 GitHub API（curl / Octokit） | 需要 |
| HTTPS clone private repo | 需要（取代密碼） |

### C.2 Fine-grained vs Classic

GitHub 現在有兩種 token：

| | Classic | Fine-grained（推薦） |
|---|---|---|
| 權限粒度 | 粗（整個帳號） | 細（指定 repo / 指定操作） |
| 過期日 | 可設可不設 | **強制設過期日** |
| 適用場景 | 老 script、相容性 | 新專案、公司用 |

**建議**：能用 fine-grained 就用 fine-grained。

### C.3 怎麼建

1. 去 https://github.com/settings/tokens?type=beta （fine-grained）
2. **Token name**：寫清楚用途（例：`recipe-genie-mcp`、`weekly-report-ci`），未來你會看到一堆，沒名字會混亂
3. **Expiration**：建議 90 天，到期前 GitHub 會 email 提醒
4. **Repository access**：選 `Only select repositories` → 勾要用的 repo
5. **Permissions** → Repository permissions：
   - `Contents: Read and write`（要 push）
   - `Issues: Read and write`（MCP 要管 issue）
   - `Pull requests: Read and write`（MCP 要管 PR）
   - `Metadata: Read`（必選）
6. **Generate token** → 立刻複製，**這頁關掉就再也看不到**

### C.4 安全存放

**絕對不要**：
- commit 進 repo（即使是 private）
- 貼到聊天紀錄 / Slack / Discord
- 寫死在 source code

**正確做法**：

```bash
# 方法 1：環境變數（適合 script 用）
echo 'export GITHUB_TOKEN=ghp_xxx' >> ~/.zshrc
source ~/.zshrc

# 方法 2：.env 檔（適合專案內用，記得加進 .gitignore）
echo "GITHUB_TOKEN=ghp_xxx" >> .env
echo ".env" >> .gitignore

# 方法 3：macOS keychain（最安全）
security add-generic-password -a "$USER" -s "github-token-recipe-genie" -w "ghp_xxx"
# 讀取：
security find-generic-password -a "$USER" -s "github-token-recipe-genie" -w
```

### C.5 過期前怎麼辦

GitHub 會在到期前 7 天 email 你：
1. 去 settings/tokens 找到那個 token
2. 點 `Regenerate token` → 設新過期日
3. 把新 token 更新到所有用到的地方（`.env` / keychain / Claude MCP config）

---

## 五、整合視角：三方案怎麼搭

一個典型的個人開發者設定：

```
本機開發環境
├── SSH key（個人）         ─→ 用於 git push/pull   ─→ 方案 A
├── SSH key（工作）         ─→ 用於 git push/pull   ─→ 方案 A
├── gh CLI（個人 + 工作）   ─→ 用於建 repo / 開 PR  ─→ 方案 A
├── GitHub MCP（裝 1 個）   ─→ 用於 Claude 操作     ─→ 方案 B + C 的 token
└── PAT × N                ─→ MCP / CI / script    ─→ 方案 C
```

---

## 六、常見錯誤排查

### Q1：`Permission denied (publickey)`

**原因**：SSH key 沒被 GitHub 認得，或用錯 key。

**檢查**：
```bash
ssh -vT git@github.com 2>&1 | grep -i "offering\|identity"
# 看它試了哪些 key
```

**修法**：
1. 確認 `~/.ssh/id_ed25519.pub` 內容有貼到 GitHub
2. 確認 `~/.ssh/config` 的 `IdentityFile` 路徑正確
3. `ssh-add -l` 看 key 有沒有在 agent 裡

### Q2：push 推到錯帳號了

**症狀**：commit 顯示是工作帳號的頭像，但這是個人專案。

**原因**：`user.email` 設錯，或 SSH 走了工作 key。

**修法**：
```bash
# 1. 改 commit author（只改最後一個）
git commit --amend --author="kevin801221 <kevin801221@users.noreply.github.com>" --no-edit

# 2. 改 remote 走個人 alias
git remote set-url origin git@github-personal:kevin801221/<repo>.git

# 3. 改 per-repo 的 user
git config user.email "kevin801221@users.noreply.github.com"
git config user.name "kevin801221"

# 4. force push（注意：只在自己 branch 用）
git push --force-with-lease
```

### Q3：`gh` 永遠用錯帳號

**原因**：`GITHUB_TOKEN` 環境變數蓋過 `gh auth` 設定。

**修法**：
```bash
echo $GITHUB_TOKEN          # 看是不是有值
unset GITHUB_TOKEN          # 暫時 unset
gh auth switch              # 切到對的帳號
# 永久：把 ~/.zshrc 裡的 export GITHUB_TOKEN=... 移掉或註解
```

### Q4：MCP server 連不上

**檢查順序**：
```bash
claude mcp list             # 看 server 有沒有註冊
claude mcp logs github      # 看錯誤訊息
echo $GITHUB_PERSONAL_ACCESS_TOKEN  # token 還在嗎
# 試 token 是不是有效
curl -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/user
```

### Q5：HTTPS clone 一直要密碼

**原因**：GitHub 從 2021 年起 HTTPS 不收密碼，只收 PAT。

**修法**：把 PAT 當密碼貼上（macOS 會存進 keychain，之後不用再打），或乾脆切 SSH：
```bash
git remote set-url origin git@github-personal:user/repo.git
```

---

## 七、推薦學習路徑

1. **第一週**：方案 A 全部練熟（SSH key、雙帳號 config、gh CLI）
2. **第二週**：把任一個 Projects/ 範例推上 GitHub，開 PR 跟自己玩
3. **第三週**：裝 GitHub MCP（方案 B），讓 Claude 幫你 review PR
4. **要寫 CI 時**：方案 C，學 fine-grained PAT

**不要一次學三個**。新手最容易死在 SSH key 設定，把那關過了再說。

---

## 八、參考資料

- GitHub SSH 官方文件：https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- `gh` CLI manual：https://cli.github.com/manual/
- GitHub MCP server：https://github.com/github/github-mcp-server
- Fine-grained PAT：https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

---

*這份教學是 `Projects/02-recipe-genie` 的配套文件，未來其他 Projects 涉及 GitHub 連接時請 link 回這份，不要重複寫。*
