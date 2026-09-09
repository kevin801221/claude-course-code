# Wafer Defect Detection — `/agents` 互動式建構教學 Walkthrough

> **對象**：用過 Claude Code、不會寫 sub-agent 的工程師
> **形式**：講師現場帶、學生跟著做
> **時長**：90 分鐘
> **產出**：4 個 sub-agent + 1 套可重現的 wafer YOLO pipeline
> **核心方法**：全程用 `/agents` slash command 互動建立（不手寫 .md）

---

## 為什麼這份 walkthrough 跟一般教學不一樣？

大部分 sub-agent 教學會直接叫你「在 `.claude/agents/` 寫一個 .md 檔」——這是進階玩法。
**新手的痛點是「我不知道 frontmatter 該寫什麼」**。

`/agents` slash command 是 Claude Code 內建的**互動引導**：
- 你只描述需求 → Claude 自動生 frontmatter + system prompt
- 你不用記 YAML 語法
- 你不用想 description 怎麼寫才能被路由到

這份 walkthrough 全程用 `/agents`，學生最後會擁有 4 個自己親手「**對話建出來**」的 agent。

---

## 📁 課程資料夾結構（講師必懂）

開課前你會準備 3 個資料夾：

```
agent_group_projects/
├── computer-vision-wafer-detection/                  # 講師「真實實驗」
│   └── (Kevin 親自跑通的版本，含實驗結果)
│
├── computer-vision-wafer-agents-detection-demo/      # 講師「示範教材」
│   ├── .claude/agents/   ✅ 4 個 agent 已建好（紅黃藍綠）
│   ├── CLAUDE.md
│   └── WALKTHROUGH.md   ← 你正在看的這份
│
└── computer-vision-wafer-template/                   # 學生「空白模板」⭐
    ├── .claude/agents/   ❌ 空的（學生自己用 /agents 建）
    ├── _Context/
    │   ├── lesson-flow.md       # 課程指引（4 個 agent 完整需求描述）
    │   ├── troubleshooting.md   # 卡點對照表
    │   └── wafer-basics.md      # 領域知識
    ├── CLAUDE.md         ✅ 路由規則已寫
    ├── .env.example      ✅ 學生填 Roboflow key
    ├── .gitignore        ✅ 保護 .env
    └── README.md         ✅ 給學生看的入口
```

### 為什麼要分 demo 跟 template？

| | demo 資料夾 | template 資料夾 |
|---|---|---|
| 用途 | 你示範 + 你自己跑 | 學生上課用 |
| `.claude/agents/` | ✅ 已有 4 個 agent | ❌ 空的 |
| `/agents` 看到 | 「已存在 4 個 agent」 | 「Create new agent」⭐ |
| 教學完整度 | 看不到「從零建」流程 | **看得到完整 9 個畫面流程** |

**如果學生直接用 demo 資料夾，會看不到 `/agents` 完整建構流程**——這就是課程設計的關鍵。

### 怎麼讓學生拿到 template？

| 方式 | 適用 | 做法 |
|---|---|---|
| **A. GitHub clone** | 學生有 GitHub 帳號 | `git clone <your-template-repo>` |
| **B. ZIP 下載** | 簡單 workshop | 講師發 ZIP 連結 |
| **C. 現場 mkdir** | 第一堂深度教學 | 課堂上跟著 `mkdir`、`touch`，10 分鐘建完 |

**第一次教時推薦 C（最有感）**，之後可以改用 A 加速。

---

## 開場（5 分鐘）

### 講師說

> 「今天我們不教 YOLO，也不教 wafer 領域知識。
> 我們教**怎麼用 `/agents` 指令建一個 sub-agent 團隊，讓 AI 幫你跑完整個 ML pipeline**。
> 90 分鐘後你會有：4 個顏色標籤不同的 agent、一份可進 git 的 `.claude/agents/`、一份 demo 級的成果。」

### 教學分層（畫黑板）

| Phase | 內容 | 今天教 |
|---|---|---|
| 1 | 用 `/agents` 建 4-agent baseline | ✅ 90 分鐘 |
| 2 | 加 evaluator（自動分析訓練結果） | Demo 20 分鐘 |
| 3 | 加 hyper-tuner（自動 HPO） | Demo 20 分鐘 |
| 4 | 加 orchestrator（自我改進迴圈） | 概念 20 分鐘 |

---

## Phase 0：環境準備（5 分鐘，課前必做）

### 檢查清單

```bash
node --version          # 18+
claude --version        # 任何近期版本
uv --version            # https://docs.astral.sh/uv/
python3 --version       # 3.11+
```

### 另外要做

1. 去 https://app.roboflow.com 註冊（免費，Google 登入最快）
2. Settings → API → 複製 Private API Key
3. 建工作資料夾：

```bash
mkdir -p ~/your-tutorial-folder/computer-vision-wafer-detection-demo/{.claude/agents,_Context,Projects}
cd ~/your-tutorial-folder/computer-vision-wafer-detection-demo
```

4. 建最小 `CLAUDE.md`（讓 Claude Code 一進來知道專案在做什麼）：

```markdown
# Wafer Defect Detection — /agents Demo

教學用工作區。用 /agents 建構 4 個 sub-agent，跑完 wafer YOLO pipeline。

## 規則
- 預設委派 sub-agent
- Python 套件用 uv 管理
- Mac 環境（MPS）
- 路徑用 pathlib.Path
- ROBOFLOW_API_KEY 從 .env 載入
```

5. 建 `.env`（學生自己填 Roboflow key）：

```bash
echo "ROBOFLOW_API_KEY=你的key" > .env
echo ".env" > .gitignore
echo ".venv/" >> .gitignore
echo "Projects/" >> .gitignore
echo "*.pt" >> .gitignore
```

> 💡 講師提示：課前 1 天請學生先做，現場不要花時間在註冊跟裝 node。

---

## Phase 1：用 `/agents` 建 4 個 Sub-Agent

### 進入 Claude Code

在工作資料夾啟動：

```bash
cd ~/your-tutorial-folder/computer-vision-wafer-detection-demo
claude
```

進去後在對話框打：

```
/agents
```

按 Enter。

---

### 第一個 agent: `data-hunter`（紅色）⭐ 全課最重要 20 分鐘

> 「第一個 agent 我們一步一步走，每個畫面都停下來解釋。
> 後面 3 個 agent 用同樣流程，我會講得快。」

#### 畫面 1：`/agents` 頂層

```
Agents · Running · Library
No subagents are currently running.
←/→ to switch · ↑/↓ to navigate · Enter to select · Esc to close
```

**講師說**：
- 3 個 tab：`Agents`（你的 agent 清單）、`Running`（此刻在跑的）、`Library`（內建範本庫）
- 「我們要建新的，先切到 Agents tab」

**操作**：按 `←` 切到 **Agents** tab。

---

#### 畫面 2：Agents tab 主畫面

```
Create new agent
Describe what this agent should do and when it should be used (be comprehensive for best results)

e.g., Help me write unit tests for my code...

Enter to submit · ctrl+g to open in editor · Esc to go back
```

**講師說**：
- 空專案時，最上面就是「Create new agent」+ 一個輸入框
- 之前建過的 agent 會列在這頁
- `ctrl+g` 可以開外部編輯器寫描述（適合長文）

**操作**：先**不要輸入**，這頁先跳過。實際上 `/agents` 的順序是：

```
Agents tab
  → Enter（選 Create new agent）
  → 選儲存位置（Project / Personal）
  → 選建立方式（Generate with Claude / Manual）
  → 然後才到輸入需求描述
```

> ⚠️ **這裡是 walkthrough 待補：** Anthropic 偶爾調整流程。教學時以實際畫面為準，請學生看到什麼選什麼。

---

#### 畫面 3：選儲存位置

```
Project (.claude/agents/)        ← 進這個專案
Personal (~/.claude/agents/)     ← 進你的個人 home
```

**講師說**：

| 選項 | 存哪 | 何時用 |
|---|---|---|
| **Project** | `<repo>/.claude/agents/` | 團隊共用、進 git ✅ 本課堂選這個 |
| Personal | `~/.claude/agents/` | 個人偏好型 agent，跨專案 |

**操作**：選 **Project (.claude/agents/)** → Enter。

---

#### 畫面 4：選建立方式

```
Generate with Claude (recommended)
Manual configuration
```

**講師說**：

| 選項 | 你做什麼 | 何時用 |
|---|---|---|
| **Generate with Claude** | 描述需求，Claude 自動寫所有欄位 | 新手友善 ✅ 本課堂選這個 |
| Manual | 自己填 name / description / system prompt 每一欄 | 進階、有強烈格式偏好 |

**操作**：選 **Generate with Claude** → Enter。

---

#### 畫面 5：輸入需求描述 ⭐ 教學金句

```
Create new agent
Describe what this agent should do and when it should be used (be comprehensive for best results)

[ 輸入框 ]

Enter to submit · ctrl+g to open in editor · Esc to go back
```

**講師說**：
> 「這一段你寫得多用心，agent 就多好用。
> **Claude 拿你的描述去自動生：name、description、system prompt 三件事**。
> 寫法有黃金結構（5 段）：」

**黃金結構**：
1. **「你是 X agent，負責 Y」** ← 角色定位
2. **「當使用者要 A、B、C 時使用」** ← 觸發句（路由的關鍵）
3. **預設參數** ← 別讓 agent 每次問你
4. **執行步驟 1, 2, 3...** ← 可重現
5. **錯誤處理 + 環境約定** ← 韌性

**範例（data-hunter 用）**：

```
你是 data-hunter agent，負責從 Roboflow Universe 下載 WM-811K 晶圓瑕疵資料集。
當使用者要抓資料、下載資料集、取得 wafer 訓練資料時使用。

預設參數：
- Workspace: wm811k-paasr
- Project: wm811k
- Version: 3
- Format: yolov8
- 下載目的地: Projects/2026-001-mvp/01-raw-data/

執行步驟：
1. 讀取專案根目錄的 .env，用 python-dotenv 載入 ROBOFLOW_API_KEY
2. 用 uv 管理套件（uv add roboflow python-dotenv）
3. 寫 Python script 用 Roboflow SDK 下載
4. 所有路徑用 pathlib.Path
5. 完成後印出資料夾結構與圖片數量

注意：
- 若 v3 不存在，列出可用版本並用最新版
- 若 API key 失效，明確報錯
- 用 Mac MPS 環境

完成標準：01-raw-data/ 下有 train（或含 valid/test）+ data.yaml，並回報圖片數量。
```

**操作**：貼上 → Enter。

---

#### 畫面 6：Select tools ⭐ 安全邊界

```
[ Continue ]

☒ All tools
☒ Read-only tools
☒ Edit tools
☒ Execution tools
☒ MCP tools
☒ Other tools

[ Show advanced options ]

All tools selected
```

**講師說**：
> 「工具是 agent 的**安全邊界**。
> 為什麼不全選？三個理由：
> 1. **權限最小化** — data-hunter 只要下載，不需要砍檔案
> 2. **減少 Claude 抓錯工具** — 給太多選項反而混淆
> 3. **訓練學生思考** — 『這個 agent 真的需要什麼？』」

**工具分類對照**：
| 類別 | 包含 |
|---|---|
| Read-only | Read, Glob, Grep, WebFetch, WebSearch |
| Edit | Edit, Write, NotebookEdit |
| Execution | Bash, BashOutput |
| MCP | 你裝的 MCP server 工具 |
| Other | Agent, TodoWrite 等 |

**操作（data-hunter）**：
1. 按 ↓ 移到 `All tools`，按空白鍵 → 變 ☐
2. 按 ↓ 移到 `MCP tools`，按空白鍵 → 變 ☐
3. 按 ↓ 移到 `Other tools`，按空白鍵 → 變 ☐
4. 保留 ☒ Read-only / Edit / Execution
5. ↑ 回到 `[ Continue ]` → Enter

```
☐ All tools
☒ Read-only tools
☒ Edit tools
☒ Execution tools
☐ MCP tools
☐ Other tools
```

---

#### 畫面 7：Choose background color 🎨

```
> Automatic color
  Red
  Blue
  Green
  Yellow
  Purple
  Orange
  Pink
  Cyan

Preview: @data-hunter
```

**講師說**：
> 「顏色不是裝飾，是視覺辨識。當 4 個 agent 接力跑時，不同色標籤幫你一眼分辨誰在說話。」

**教學配色慣例（你可以發給學生）**：
- 🔴 **Red** = data-hunter（資料源頭，紅色醒目）
- 🟡 **Yellow** = bbox-labeler（標註，警示色）
- 🔵 **Blue** = training-runner（訓練，沉穩專注）
- 🟢 **Green** = inference-runner（成果輸出，綠燈）

**操作**：選 **Red** → Enter。

---

#### 畫面 8：Confirm and save ⭐ 最關鍵的一步

```
Create new agent
Confirm and save

Name: data-hunter
Location: .claude/agents/data-hunter.md
Tools: Bash, Edit, NotebookEdit, Write, ListMcpResourcesTool, Read,
       ReadMcpResourceTool, TaskStop, WebFetch, WebSearch
Model: Opus
Memory: Project (.claude/agent-memory/)

Description (tells Claude when to use this agent):
  Use this agent when the user wants to download, fetch, or obtain
  wafer defect datasets (specifically WM-811K) from Roboflow Universe.
  Triggered by phrases like '抓資料', '下載資料集', ...

System prompt:
  You are **data-hunter**, an expert data acquisition agent specialized
  in fetching computer vision datasets from Roboflow Universe...

Warnings:
  ● System prompt is very long (over 10,000 characters)

Press s or Enter to save, e to save and edit
s/Enter to save · e to edit in your editor · Esc to cancel
```

**講師說**（這頁要逐項拆給學生看）：

| 欄位 | 意義 | 教學重點 |
|---|---|---|
| **Name** | 從你描述提取，**就是檔名** | 自動取名規則 |
| **Location** | `.claude/agents/data-hunter.md` | Project 級會進 git ✅ |
| **Tools** | 比你勾的多 ⚠️ | 「分類大致範圍 + 自動補一些常用」 |
| **Model** | Opus | 預設用最強模型跑 agent |
| **Memory** | Project | 跨對話記憶（新功能） |
| **Description** | 含**範例對話** | 路由依據 |
| **System prompt** | 自動擴寫到 10,000+ 字元 | ⚠️ 太長警告 |

**自動生成 vs. 手寫對照（必講金句）**：

| | Claude 自動生 | 手寫 |
|---|---|---|
| 字元數 | ~10,000+ | ~1,500 |
| 結構完整度 | 高（含 example 對話） | 看人 |
| 載入成本 | 貴 | 便宜 |
| 學習曲線 | 0（新手友善） | 高 |

> **教學金句**：「自動生成的版本『像新人手冊』——什麼都寫但太厚。手寫像『便利貼』——只寫關鍵字。**課堂選自動生成是因為新手不會漏欄位，熟了再學減肥。**」

---

### ⚠️ 黃金規則：永遠按 `s`，不要按 `e`

```
Press s or Enter to save  ← 用這個
e to save and edit         ← 別用！
```

**講師說**（這條超重要，寫進筆記）：
> 「`e` 的真實行為是：
> 1. 先把檔案存到 disk ✅
> 2. 用你的 `$EDITOR` 開檔案 ✅
> 3. **等編輯器關閉**才會繼續 ❌ ← 這裡會卡
>
> 在 VS Code 裡按 `e`，VS Code 跳到 .md 那個 tab，但你沒**關閉 VS Code**，所以 Claude Code 一直等。看起來像卡住，**其實是它在等你**。
>
> **規則**：永遠按 `s`。想編輯？save 完用 VS Code 開 `.claude/agents/<name>.md`，就是普通 .md 檔。」

**操作**：按 `s`。

---

#### 畫面 9：回到 `/agents` 主選單

存完會回 Agents tab，現在多了一筆：

```
data-hunter   .claude/agents/data-hunter.md   Red   Project
[Create new agent]
```

**講師說**：
> 「第一個 agent 生出來了。我們現在去檔案系統看它長什麼樣。」

**操作**：按 Esc 退出 `/agents`，在終端打：

```bash
cat .claude/agents/data-hunter.md | head -50
```

學生會看到完整的 YAML frontmatter + 中文 system prompt。

---

### 🎉 恭喜，第一個 agent 完成

**你做了什麼**：
- 0 行手寫程式碼
- 0 個 YAML 語法錯誤
- 1 段中文需求描述 → 1 個 264 行、20KB 的完整 sub-agent

**這就是 `/agents` 的威力。**

---

### 第二、三、四個 agent（用同樣流程，更快）

> 「剩下 3 個，**步驟完全一樣**。我們只換『需求描述 + 顏色』。
> 你打 `/agents` → Agents tab → Create new agent → Project → Generate with Claude → 貼需求 → 選工具 → 選顏色 → **按 `s`** → 完成。」

---

#### Agent 2: `bbox-labeler`（🟡 Yellow）

**需求描述（貼進畫面 5）**：

```
你是 bbox-labeler agent，負責驗證 YOLO 格式標註的合法性，並把資料切分成 train/val/test 結構。
當使用者要驗證標註、組織資料集、切分 train/val/test、產生 data.yaml 時使用。

任務：
- 輸入：Projects/2026-001-mvp/01-raw-data/（data-hunter 下載的 Roboflow 資料）
- 輸出：Projects/2026-001-mvp/02-dataset/（標準 YOLO 結構 + data.yaml）

執行步驟：
1. 掃描 01-raw-data/ 下所有 label .txt 檔
2. 驗證每行格式 class_id cx cy w h，座標必須在 [0, 1]，class_id 為非負整數
3. 統計圖片數、bbox 數、類別分佈、空 label 數
4. 若 Roboflow 只給 train split（沒 val/test），用 seed=42 隨機切 70/20/10
5. 用 shutil.copy2 複製 images/labels 到 02-dataset/{images,labels}/{train,val,test}/
6. 產生 data.yaml（path 用絕對路徑，class names 從原 data.yaml 沿用）
7. 印出統計摘要

重要：
- 不要重新生成 bbox，Roboflow 已有就直接信任
- 套件用 uv add 安裝
- 路徑用 pathlib.Path
- 完成標準：02-dataset/ 下三個 split 各自 images 數 == labels 數
```

**工具**：Read-only / Edit / Execution（取消 All / MCP / Other）
**顏色**：🟡 Yellow
**最後按 `s`**

---

#### Agent 3: `training-runner`（🔵 Blue）

**需求描述**：

```
你是 training-runner agent，負責在 Mac MPS 上訓練 YOLOv8 wafer 瑕疵偵測模型。
當使用者要訓練、fine-tune、跑 training 時使用。

⚠️ 最重要規則：訓練前必須顯示預估時間並等使用者明確說 GO/開始/繼續 才能執行訓練。
絕對不可以自己默默開始訓練。這是不可協商的硬性規則。

任務：
- 輸入：Projects/2026-001-mvp/02-dataset/data.yaml
- 輸出：Projects/2026-001-mvp/04-experiments/exp001/weights/best.pt

預設超參數：
- model: yolov8n.pt
- epochs: 50, batch: 8, imgsz: 416
- device: mps
- project: Projects/2026-001-mvp/04-experiments, name: exp001

執行流程：
Step 1（環境檢查）：uv add ultralytics、確認 torch.backends.mps.is_available()
Step 2（預估時間，必做）：算 train 圖片數 × epochs ÷ batch = iterations，每 iter 約 0.2s，顯示「📊 訓練預估」並停下來等 GO
Step 3（訓練）：用 ultralytics YOLO API，device='mps', exist_ok=True
Step 4（回報）：best.pt 路徑、最終 mAP@0.5、實際耗時

錯誤處理：
- MPS 不支援某 op → export PYTORCH_ENABLE_MPS_FALLBACK=1
- OOM → batch 改 4
- 訓練中斷 → resume=True

環境：Mac MPS、uv 套件管理、pathlib.Path、繁體中文回應
```

**工具**：Read-only / Edit / Execution
**顏色**：🔵 Blue
**最後按 `s`**

> 💡 **教學重點**：訓練 agent 必須有「**人類在 loop**」規則。這條規則就是你寫進需求描述的「⚠️ 最重要規則」那段。你會看到 Claude 自動生成的 system prompt 會把這段擴寫成 3-4 段強調。

---

#### Agent 4: `inference-runner`（🟢 Green）

**需求描述**：

```
你是 inference-runner agent，負責用訓練好的 YOLO 模型對 test set 跑推論並產生視覺化。
當使用者要 inference、預測、視覺化 bbox、評估模型時使用。

任務：
- 輸入：Projects/2026-001-mvp/04-experiments/exp001/weights/best.pt
- 輸出：Projects/2026-001-mvp/05-inference/ 下 10 張 PNG + summary.md

執行步驟：
Step 1（載入 + 抽樣）：
- 載入 best.pt
- 從 02-dataset/images/test 隨機抽 10 張（seed=42）

Step 2（推論 + 視覺化）：
- 對每張跑 model.predict()
- 用 matplotlib 畫原圖 + bbox + class name + confidence
- 存成 05-inference/pred_<原檔名>.png

Step 3（評估）：
- 跑 model.val(split="test")
- 印出 mAP@0.5 與 mAP@0.5:0.95

Step 4（寫 summary.md）：
- 模型路徑、test mAP、10 張視覺化清單、觀察筆記（誤判類別、低 confidence 樣本）

環境：Mac MPS、uv 套件管理（matplotlib 已裝）、pathlib.Path、繁體中文
完成標準：10 張 PNG + 1 個 summary.md + 終端印出 mAP 數字
```

**工具**：Read-only / Edit / Execution
**顏色**：🟢 Green
**最後按 `s`**

---

### Phase 1 收尾：驗收 4 個 agent

回到終端：

```bash
ls -la .claude/agents/
```

預期看到：

```
data-hunter.md       ~20KB  🔴
bbox-labeler.md      ~20KB  🟡
training-runner.md   ~20KB  🔵
inference-runner.md  ~20KB  🟢
```

#### 講師收尾金句

> 「你剛剛做了什麼？
> - 0 行 YAML 手寫
> - 0 次查文件
> - 4 段中文需求描述 → 4 個 sub-agent
>
> **這就是 `/agents` 的核心價值：把「描述需求」變成「建構工具」的唯一動作。**」

---

## Phase 1 補充：實際跑一次 pipeline（25 分鐘）

建好 agent 不等於 work，要讓它們**真的跑一次**。

### Step 1: 觸發 data-hunter

在 Claude Code 對話框打：

```
幫我從 Roboflow 抓 WM-811K 資料集
```

學生會看到：
- Claude 自動識別 → 呼叫 `@data-hunter`（紅色標籤跳出）
- agent 跑 `uv add roboflow python-dotenv`
- 寫 `scripts/download_dataset.py`
- 執行下載

**現實會卡的點（要教學生面對）**：
- Roboflow v3 可能**只有 train、沒有 val/test split**
- 可能**只有 1 個類別**（例如 Donut），不是預期的 6 類
- 學生會問：「那怎麼辦？」→ **這就是 agent 教育的精髓**：agent 把問題回報給你，你決策

---

### Step 2: 觸發 bbox-labeler

```
用 bbox-labeler 把 01-raw-data 的圖切成 70/20/10 train/val/test
```

預期輸出：
| Split | 圖片 | bbox |
|---|---|---|
| train | 286 | 290 |
| val | 81 | 81 |
| test | 42 | 42 |

---

### Step 3: 觸發 training-runner（看「人類在 loop」生效）

```
開始訓練
```

**預期看到 agent 停下來**：

```
📊 訓練預估
- dataset: 286 張 train
- epochs: 50, batch: 8 → iterations ≈ 1800
- 預估時間: 約 6–10 分鐘
- 輸出: Projects/2026-001-mvp/04-experiments/exp001/

要開始嗎？(請回 GO)
```

> 💡 **教學金句**：「**這就是『規則 → 行為』的範例。** 你在需求描述寫『訓練前必須等使用者 GO』，Claude 把這條翻譯成 system prompt 的硬規則，agent 真的就會停。」

學生回 `GO` → 訓練開始。

---

### Step 4: 觸發 inference-runner

```
用訓練好的模型跑 test set 推論並產出視覺化
```

預期看到：
- 10 張 PNG（每張畫 bbox + class + confidence）
- 終端印出 test mAP
- `summary.md` 寫了觀察筆記

---

## Phase 1 學生常問的 3 個問題

### Q1：agent 之間怎麼傳資料？

**A**：透過**檔案系統**。data-hunter 寫到 `01-raw-data/`，bbox-labeler 讀進去再寫到 `02-dataset/`。沒有 in-memory pipeline，這樣才能**跨 session 接續**——你今天跑到 training 中斷，明天回來繼續，agent 不需要重跑前面。

### Q2：agent 可以平行跑嗎？

**A**：可以，用 `dispatching-parallel-agents` 技能。但今天的 4 個是**有依賴關係**（要先有資料才能訓練），不能平行。

例如：你想同時建 5 個模型比較，那 5 個 training-runner 可以平行跑。

### Q3：怎麼 debug agent？

**A**：記住 agent **不是黑箱**——它做的每件事都會：
- 寫檔案（看 `01-raw-data/`, `02-dataset/` 等）
- 跑指令（看 Claude Code 顯示的 Bash 輸出）
- 在對話裡回報

debug 流程：
1. 看 agent 在對話裡說了什麼
2. 看它寫了哪些檔案（`ls` / `git status`）
3. 看 `.claude/agents/<name>.md` 的 system prompt（是不是規則寫不清楚）

---

## Phase 2：加入 evaluator agent（20 分鐘 demo）

### 講師說

> 「Phase 1 結束你有一個能跑的 pipeline，但**還不能自我改進**。
> 第一步：加一個 evaluator，**自動分析訓練結果寫人話 report**。」

### evaluator 的職責

讀 `04-experiments/exp001/`，產出 `evaluation.md`：
1. **訓練曲線健康度**（讀 `results.csv`）
   - 是否 overfit（train loss ↓ 但 val mAP 停滯）
   - 是否還能 train 更多 epoch
2. **失敗案例**（讀 confusion matrix）
   - 哪一類預測差？
   - 哪些 confidence 低？
3. **下一輪建議**（人話）
   - 「val mAP 在 epoch 30 就飽和，建議 epochs=30」
   - 「small bbox 預測差，建議 imgsz=640」

### 用 `/agents` 建 evaluator

**需求描述（貼進 `/agents` 流程的畫面 5）**：

```
你是 evaluator agent，負責讀訓練結果產出「下一輪該怎麼改」的人話 report。
當使用者要分析訓練、看訓練曲線、診斷模型問題、決定下一步調整時使用。

任務：
- 輸入：Projects/2026-001-mvp/04-experiments/exp001/（含 results.csv, confusion_matrix.png, weights/）
- 輸出：同資料夾下的 evaluation.md

分析項目：
1. 訓練曲線健康度（讀 results.csv，用 pandas）
   - train/val loss 趨勢
   - mAP 是否還在上升或飽和
   - 是否 overfit（train↓ val 平/反升）
2. 失敗類別分析
   - 從 confusion matrix 找最差類
   - 從 val predictions 找低 confidence 樣本
3. 下一輪建議（3 條具體可執行）
   - 例：「epochs 調 30 就夠」「imgsz 改 640」「需要更多 X 類資料」

輸出格式：evaluation.md（含表格 + 圖片 link + 建議清單）
重要：不訓練、不推論，只讀 + 寫
```

**工具**：Read-only / Edit（**不需要 Execution**，evaluator 不跑訓練）
**顏色**：🟣 Purple（分析 = 沉思紫）
**最後按 `s`**

### 教學重點

- evaluator **不訓練、不推論**，只**讀 + 寫**
- 它的輸出是給**人類**或**下一個 agent**（orchestrator）讀的
- 這是「**從工具型 agent → 分析型 agent**」的跳躍

---

## Phase 3：加入 hyper-tuner（20 分鐘 demo）

### 講師說

> 「現在我們讓 agent 自己跑多組實驗找最佳參數。
> 不再是『跑 1 次』而是『跑 N 次比一比』。」

### hyper-tuner 的職責

1. 讀 evaluator 的建議
2. 定義 search space（例如 lr ∈ [1e-4, 1e-2], imgsz ∈ {416, 640}）
3. 用 **Ultralytics 內建** `model.tune()` 或 **Optuna** 跑 N 個 trial
4. 每個 trial 跑短訓（10 epochs）
5. 挑最好的參數，回報

### 兩種實作法（講師選一個 demo）

**法 1：Ultralytics 內建 tune（最快上手）**
```python
model = YOLO("yolov8n.pt")
model.tune(data="data.yaml", epochs=10, iterations=10, optimizer="AdamW")
```

**法 2：Optuna（更彈性）**
```python
import optuna
def objective(trial):
    lr = trial.suggest_float("lr", 1e-4, 1e-2, log=True)
    imgsz = trial.suggest_categorical("imgsz", [416, 640])
    model = YOLO("yolov8n.pt")
    results = model.train(data=..., lr0=lr, imgsz=imgsz, epochs=10)
    return results.box.map50

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=10)
```

### 用 `/agents` 建 hyper-tuner

**需求描述**：

```
你是 hyper-tuner agent，負責跑超參數搜尋（HPO）找最佳參數組合。
當使用者要做 HPO、tune、找最佳 lr/batch/imgsz 時使用。

⚠️ 跑 HPO 前必須讓使用者確認（這會跑很久），等使用者明確說 GO。

任務：
1. 讀 04-experiments/exp001/evaluation.md（evaluator 的建議）
2. 從建議生成 search space
3. 跑 N 個 trial（每個 10 epochs 短訓）
4. 挑 mAP@0.5 最高的，輸出 best_params.json
5. 把所有 trial 結果寫進 experiments.md

工具選擇：Ultralytics 內建 model.tune() 或 Optuna（看使用者偏好）
環境：MPS, uv add optuna
```

**工具**：Read-only / Edit / Execution
**顏色**：🟠 Orange（多次嘗試 = 警告橙）
**最後按 `s`**

### 教學重點

- HPO 是「Phase 2 → Phase 3 的質變」：從 1 次訓練變多次
- **token 成本和時間成本都會跳一級**，所以要使用者確認
- 學生會問：「那要跑幾個 trial？」→ Pareto 原則：先 5–10 個看趨勢，覺得有戲再加

---

## Phase 4：Orchestrator + 自我改進迴圈（20 分鐘概念）

### 講師說

> 「最後一個 phase **不一定要實作**，但**一定要懂**。
> 這是『agent 團隊』vs.『agent 自我演化』的分水嶺。」

### Orchestrator 的職責

```
┌──────────────────────────────────────────────┐
│  orchestrator (大腦)                           │
│  - 讀 experiments.md (記憶所有過去 run)         │
│  - 決定下一步: 收資料? 換模型? 再 tune? 收手?   │
└──────────────────────────────────────────────┘
                  │
       ┌──────────┼─────────┬──────────┐
       ▼          ▼         ▼          ▼
   data-hunter  trainer  evaluator  hyper-tuner
       │          │         │          │
       └──────────┴────┬────┴──────────┘
                       ▼
              ┌─────────────────┐
              │ experiments.md  │  ← 唯一真相來源
              └─────────────────┘
```

### `experiments.md`（記憶 schema）

```markdown
# Experiment Log

## exp001 — 2026-05-12
- params: yolov8n, lr=0.01, imgsz=416, epochs=50
- mAP@0.5: 0.85
- 觀察: val 在 epoch 30 飽和
- 下一步: 減 epochs, 試 imgsz=640

## exp002 — 2026-05-12 (orchestrator 決策)
- params: yolov8n, lr=0.01, imgsz=640, epochs=30
- mAP@0.5: 0.88 ⬆️
- 觀察: small bbox 召回變好
- 下一步: 試 yolov8s 看是否更好
```

### 自我改進迴圈的本質

```python
while not converged:
    plan = orchestrator.read(experiments_md).decide_next()
    if plan.action == "train": result = trainer(plan.params)
    if plan.action == "tune":  result = hyper_tuner(plan.search_space)
    if plan.action == "audit": result = evaluator(latest_exp)
    if plan.action == "stop":  break
    write_to(experiments_md, result)
```

### 教學重點

- **記憶（experiments.md）是核心**，沒有記憶就沒有自我改進
- Orchestrator **本身就是一個 agent**，只是它的 tools 是「呼叫別的 agent」
- 真實世界 Claude Code 還沒原生支援 agent-call-agent 的迴圈，需要用**外部 driver script** 或 **workflow 工具**（LangGraph / Vercel Workflow）來驅動

### 進階提問（給工程師同行）

- **Q：這跟 AutoML（Google Vertex AI AutoML）差在哪？**
  A：AutoML 是黑箱、固定 search space。Agent 團隊是**可解釋、可干預、可擴展**。你可以隨時插一個「-看一下這次的圖」agent。

- **Q：成本怎麼控制？**
  A：Phase 4 很燒 token。實務上 orchestrator 應該有 budget cap，跑超過就停。

---

## 課程後續（給學生帶走）

### 作業（選一個做）

1. **改資料源**：找 Roboflow 上另一個多類別 wafer 資料集，重跑 4-agent
2. **加 evaluator**：用 `/agents` 自己生 evaluator，產 evaluation.md
3. **加 deploy-agent**：把 best.pt 包成 FastAPI 服務
4. **改領域**：把 4-agent 改成「PCB 瑕疵」或「醫療影像分類」

### 進階閱讀

- [Anthropic Sub-agent 官方文件](https://docs.claude.com/en/docs/agents/sub-agents)
- Ultralytics YOLOv8 `model.tune()` 文件
- Optuna 文件
- 真實世界 ML pipeline 工具：MLflow / Weights & Biases / ClearML

---

## 講師備忘錄

### 常見卡點對照表

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| 按 `e` 後 Claude Code 不動 | VS Code 開了 .md tab 但沒關，Claude Code 在等 | 關掉 VS Code 那個 tab；以後一律按 `s` |
| `/agents` 找不到「Create new agent」 | 沒切到 Agents tab | `←` 切回左邊 |
| 工具勾選後 Confirm 畫面多了奇怪工具 | `/agents` 會自動補一些常用（NotebookEdit, WebFetch...） | 事後手改 `.claude/agents/<name>.md` 的 `tools:` 那行 |
| `ROBOFLOW_API_KEY unauthorized` | key 沒設或 `.env` 位置錯 | 確認 `.env` 在專案根、`load_dotenv()` 載到 |
| `roboflow project not found` | workspace/project 拼錯 | 用 SDK 列 workspace 下所有 project |
| MPS 不支援某 op | PyTorch + Apple Silicon 限制 | `export PYTORCH_ENABLE_MPS_FALLBACK=1` |
| 訓練爆 RAM | batch 太大 | batch 8 → 4 |
| Roboflow 下載卡在 0% | overwrite=False + 資料夾已存在 | `Version.download(..., overwrite=True)` |
| `uv run` 找不到套件 | uv 隔離環境 vs. .venv 衝突 | 統一用 `uv add`（更新 pyproject.toml） |
| Claude 沒呼叫 sub-agent | description 寫太短或太籠統 | 改成「當使用者要 X、Y、Z 時使用」 |
| Sub-agent 跑到一半停 | tools 不夠或卡在權限確認 | 檢查 frontmatter `tools:` |

### 教學節奏建議

| 時間 | 內容 | 重點 |
|---|---|---|
| 0–5 | 開場 + 分層說明 | 讓學生知道今天會走到哪 |
| 5–10 | Phase 0 環境檢查 | 別花太久，課前準備好 |
| 10–30 | Agent 1: data-hunter ⭐ | **全課最重要 20 分鐘**，逐畫面解釋 |
| 30–40 | Agent 2: bbox-labeler | 加速，提醒按 `s` |
| 40–50 | Agent 3: training-runner | 強調「人類在 loop」規則寫法 |
| 50–60 | Agent 4: inference-runner | 收尾 4-agent |
| 60–85 | 跑完整 pipeline | data → label → train → infer |
| 85–90 | Phase 1 收尾 + 3 個 Q&A | |
| 90–110 | Phase 2 evaluator demo | |
| 110–130 | Phase 3 hyper-tuner demo | |
| 130–150 | Phase 4 orchestrator 概念 | |

---

## 講師私房筆記（Kevin 親自驗證的真實狀況）

### 1. Roboflow 版本不一定符合預期
原本以為 wm811k v3 有 6 類 + 切好 split，**實際**只有 1 類（Donut）、只有 train split。
**這是好教材**：教學生面對「資料不完美」的真實工程現場。
**處理**：讓 bbox-labeler 自切 70/20/10、單類別繼續跑 pipeline。

### 2. 「按 `e` 卡住」是必踩坑
講師上課時可以**故意按一次 `e`** 給學生看「為什麼會卡」+「怎麼救」。
這比口頭講「不要按 `e`」更有印象。

### 3. Claude 自動生成的 system prompt 會很長（10K 字元）
這不是 bug，是 feature。
適合教學一開始照用，**熟了之後**回頭手動精修到 2K 字元（省 token）。

### 4. 用過 `/agents` 之後 `.claude/agents/<name>.md` 就是普通檔案
直接用 VS Code 編輯、進 git、跨專案複製貼上都可以。
這個觀念要在學生離開教室前**強調一次**。

---

## 一句話總結

> **`/agents` 把「寫 agent」從『寫 YAML + 想 prompt』降級成『描述需求』。
> 你不是在寫程式，你是在跟 Claude 約定『以後遇到 X 時，你就做 Y』。**

---

_Last updated: 2026-05-12_
_Maintainer: Kevin (kevin@legalsign.ai)_
_Verified by: Kevin 親自跑過 data-hunter、bbox-labeler 兩個 agent 的完整 `/agents` 流程_
