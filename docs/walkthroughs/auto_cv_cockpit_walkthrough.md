# autocv Cockpit Walkthrough — 用 Superpowers 從零做到一個可 po LinkedIn 的小產品

> **對象**：用過 Claude Code、會寫 Python、想學「怎麼把腦袋裡一個爆款點子真的端到端做成可上線的 repo」的工程師
> **形式**：講師現場帶，學員邊聽邊看
> **時長**：120 分鐘（含真實踩坑示範與修補）
> **產出**：一個可跑通的 CV 自動訓練 + 視覺駕駛艙 repo（kevin801221/auto-cv-train-optimization-claude_code）+ 一篇 LinkedIn 文案
> **核心方法**：**全程不手寫程式**，全程跟 Claude Code 對話；用 superpowers 的 brainstorming → writing-plans → 直接做完工作流；每個動作都 commit、commit 訊息有紀律

---

## 開場（5 分鐘）：為什麼這份跟別的「AI 幫你寫 code」教學不一樣？

| 路線 | 怎麼做 | 問題 |
|---|---|---|
| 一般「AI 寫 code」教學 | 開 Cursor / VSCode chat，丟需求，貼回程式碼 | 沒設計階段、commit 訊息亂、上 GitHub 才發現一堆紀律問題 |
| **這份** | brainstorming → spec → plan → 一個 commit 一個 task → push 前掃 → 上線 → 修補 | 從第一行起就把 repo 當「會公開」在做 |

> **教學金句**：「不是『AI 幫你寫 code』，是『AI 幫你跑 spec → plan → code → commit → push 整套工作流』——少任何一步，repo 上 GitHub 都會看起來像實習生作業。」

---

## 📁 全景圖：兩個 repo + 兩條工作流

```
教學 repo（claude-code-complete-tutorial）
└── docs/superpowers/
    ├── specs/2026-05-19-auto-cv-...-design.md      ← brainstorming 產物
    ├── plans/2026-05-19-auto-cv-...-plan.md         ← writing-plans 產物
    ├── specs/2026-05-19-autocv-ui-cockpit-design.md ← 第二輪（cockpit）
    └── plans/2026-05-19-autocv-ui-cockpit.md

公開 repo（kevin801221/auto-cv-train-optimization-claude_code）
├── src/autocv/{config,device,data,split,train,optimize,infer,cli}.py
├── src/autocv/server/{events,runner,real_stages,app,static/index.html}
├── .claude/agents/  5 個 config 驅動 agent
├── configs/{wafer,template,wafer-quick}.yaml
├── docs/screenshots/{cockpit-training,cockpit-done}.jpg  ← LinkedIn 用素材
├── README.md（中英雙語 + 真截圖）
└── ROADMAP.md
```

兩條工作流：
1. **第一輪**（autocv 套件本體）：把 wafer 4-agent demo 重構成通用 CV 模板
2. **第二輪**（cockpit）：兌現 README 賣的「無碼視覺駕駛艙」懸念

兩輪都跑同一條：`brainstorming → spec → writing-plans → plan → 動手 → commit → push`。

> **教學金句**：「同一條工作流跑兩輪，差別只在 spec 內容——這就是『可重複』的價值，不是『AI 幫我寫了一個 script』。」

---

## Phase 0：環境準備（10 分鐘）

| 必備 | 為什麼 |
|---|---|
| Claude Code CLI（最新版） | brainstorming / writing-plans skill 要 |
| superpowers 外掛已掛 | 提供 `brainstorming` / `writing-plans` / `subagent-driven-development` |
| `uv` 已裝 | Python 套件唯一管法，禁止 pip |
| Mac MPS（Apple Silicon） | 訓練不靠雲端 |
| `gh` CLI + 個人 GitHub 帳號 | push 上線。⚠️ 看 Phase 4 真實踩坑 |
| `~/.ssh/config` 有 `github-personal` alias | 分離個人/工作 GitHub 身分 |

開課前實機檢查清單：

```bash
claude --version              # Claude Code 在
uv --version                  # uv 在
gh auth status                # gh 看的到哪個帳號（注意！）
ssh -T git@github-personal    # SSH alias 通
```

> **教學金句**：「環境準備不是『裝 Python』——是『把 commit、push、身分這些紀律一次擺對』，後面才不會臨時補。」

---

## Phase 1：用 brainstorming skill 設計 autocv（20 分鐘）⭐ 最詳細

### Step 1.1：開頭就丟「爆款」級需求

```
你：可不可以把這個專案包裝成能夠爆款的自動訓練 computer vision 模板上傳到我的個人 github？
```

Claude 因為 superpowers 強制規則，**不會直接動手**——會先觸發 `brainstorming` skill。

### Step 1.2：Claude 問的 4 個關鍵問題（一個都不要跳）

| 問題 | 為什麼問 | 影響 |
|---|---|---|
| 定位（通用模板 vs wafer 專用 vs Claude Code 多 agent 玩法） | 決定 README / 命名 / code 怎麼改寫 | 全篇都不一樣 |
| README 語言（中英雙語 / 雙語同頁 / 純繁中） | 國際 vs 在地觸及 | star 量級差十倍 |
| 附權重 vs 附成果圖 vs 都不附 | repo 體積 + 說服力 trade-off | 體驗差很多 |
| 通用化深度（config 驅動 / 完整 CLI / 只改 README） | 重構程度 | 工時差 5 倍 |

> **教學金句**：「brainstorming 不是『AI 問你問題』——是『AI 幫你把腦袋裡『直覺』翻成『可執行決策』』。沒這步直接動手，做到一半才發現方向錯。」

### Step 1.3：confirmed 後 Claude 寫 design.md → commit

關鍵：**spec 要 commit**，不要存在你腦袋。教學 repo 的 `docs/superpowers/specs/` 是它的家。

```bash
# Claude 會幫你做
git add docs/superpowers/specs/2026-05-19-auto-cv-...-design.md
git commit -m "新增設計：wafer demo 重構成通用 CV 自動訓練模板"
```

**現場練習**：學員打開那份 spec 看，找出「YAGNI 取捨」那段——這段是 brainstorming 的精華（明寫『不做什麼』比『做什麼』更難）。

---

## Phase 2：writing-plans 把 spec 拆成 task（15 分鐘）

### Step 2.1：spec 過關後自動接 writing-plans

Claude 會把 design.md 拆成 9 個 task，**每個都含**：
- 確切檔案路徑
- 完整 code（不是「在這裡實作」這種空話）
- 對應測試
- commit 訊息
- 預期 pytest 輸出

```
Task 1: 建立 repo 骨架與 git
Task 2: pyproject.toml 與套件 metadata
Task 3: config.py（TDD）
...
Task 9: 建 GitHub repo 並 push
```

### Step 2.2：plan 也 commit

同樣放教學 repo `docs/superpowers/plans/`。

### Step 2.3：執行方式選擇

Claude 會問「subagent-driven 還是 inline execution」。

| 選項 | 適合 | 注意 |
|---|---|---|
| Subagent-driven | task 互相獨立、預算多 | 每個 task 派一個 fresh subagent，會多很多權限 prompt（**學員會抓狂**） |
| Inline | task 連動、要快 | controller 自己跑，省 prompt |

⚠️ **Kevin 親自踩過**：subagent-driven 在「mechanical 任務」上會狂跳權限框，學員 / 你自己會崩潰。**這個專案我直接切 inline**，commit 紀律照樣維持。

> **教學金句**：「subagent-driven 是好東西——但用錯時機會讓你的鍵盤想砸地。先用 inline，等真的有並行需求再切。」

---

## Phase 3：實作 + commit 紀律（30 分鐘）

### Step 3.1：照 plan 跑、一個 task 一個 commit

```bash
# 每個 task 結束都是這組節奏
uv run pytest -q                # 跑測試
uv run ruff check src tests     # 跑 lint
git add <剛動過的檔>            # 只加該動的
git commit -m "<純技術中文，無行銷字眼，無 AI 署名>"
```

### Step 3.2：commit 訊息紀律 ⭐⭐⭐

| ❌ 不能寫 | ✅ 該寫 |
|---|---|
| `加強 FOMO（早鳥票/鎖定 roadmap）` | `README 補視覺駕駛艙用法與狀態` |
| `成果先行 + 駕駛艙懸念 不卑微求 star` | `重寫 README 文案結構` |
| `Co-Authored-By: Claude` | （什麼都不要加） |
| `feat:` `fix:` `chore:` 等 conventional 前綴 | 純中文白話 |

> **教學金句**：「commit message 是給 6 個月後完全不認識你的工程師看的——在那寫『加強 FOMO』等於把你的行銷劇本貼在牆上。」

### Step 3.3：故意踩坑——讓學員看「ruff E402」如何修

寫測試時把 import 接在檔案中段（writing-plans 的 plan 沒注意這個），跑 `ruff check` 會炸 6 個 `E402 Module level import not at top of file`。

正解：所有 module-level import 收到檔案頂端，function 內 import 不動。

> **教學金句**：「ruff 是 commit 前的最後守門員——它擋下的不是 bug，是『一年後你回來看會皺眉』的小髒。」

---

## Phase 4：上 GitHub + 真實踩坑（20 分鐘）⭐ 故意踩給學員看

### Step 4.1：踩坑 1 — `gh` 用錯帳號

```bash
gh auth status
# ✓ Logged in to github.com account KevinLegalAI (GITHUB_TOKEN)
```

⚠️ `GITHUB_TOKEN` 環境變數綁的是工作帳號。**直接 `gh repo create kevin801221/...` 會用工作 token 失敗 / 建到錯帳號**。

**正解**：不靠 `gh` 建，叫使用者去 https://github.com/new 用個人帳號親手建空 repo（30 秒），然後本地 push 走 SSH alias：

```bash
git remote add origin git@github-personal:kevin801221/<repo>.git
git push -u origin main
```

`git@github-personal:` 走 `~/.ssh/id_ed25519`（個人金鑰），完全繞過 `gh` 與 `GITHUB_TOKEN`。

### Step 4.2：踩坑 2 — commit 訊息洩漏行銷策略

第一次寫 README 時 commit 了：
```
0e4db9c 重寫 README：成果先行 + 駕駛艙 roadmap 懸念，不卑微求 star
dd8bc0e 作者掛羅子嘉，README 加強 FOMO（早鳥票/鎖定 roadmap）
```

push 完才發現：**這兩行公開可見**——讀 commit log 的人馬上知道整套行銷套路，效果直接破功。

**第一次處理**：force push 改寫歷史

```bash
git reset --soft <洩漏前的 commit>
git commit -m "更新 README 與作者資訊"   # 中性訊息
git push --force origin main
```

**第二次處理**（學員主動問「會不會殘留」）：直接刪 GitHub repo 重建、push 全乾淨歷史。本地 22 個 commit 訊息已經乾淨，所以重建後不會再有殘留。

> **教學金句**：「公開 repo 沒有『撤回』——只有『重建』。在打 commit message 前先想：『這行被當眾念出來，我會臉紅嗎？』」

### Step 4.3：踩坑 3 — README 網頁編輯後分歧

使用者在 GitHub 網頁直接刪了 README 幾行（FOMO 段太肉麻），本地不知道，繼續 commit cockpit 功能往上疊。push 被擋（non-fast-forward）。

**正解**：不要 force push（會洗掉使用者那筆 web edit）。改用 rebase：

```bash
git fetch origin
git rebase origin/main          # 把本地 commit 疊到 web edit 上
# 如有 conflict 手動解，**保留使用者的刪除 + 自己新增的內容**
git push origin main            # 現在 fast-forward
```

> **教學金句**：「使用者在網頁編的 commit 是聖物——你的 force push 不能蓋過去。」

---

## Phase 5：第二輪——加 cockpit 前端（25 分鐘）

跑同一條工作流：`brainstorming → spec → plan → 動手`，這次題目是「兌現 README 賣的『無碼視覺駕駛艙』」。

### Step 5.1：brainstorming 鎖三件事

| 決策 | 結論 |
|---|---|
| 真的做 vs 假動畫 | 真的——repo 主打誠實，假動畫被識破會反噬 |
| 前端路線 | FastAPI + 自刻單頁（零建置、深色 cockpit、不靠 React） |
| 範圍 | 本機單人、一次一條 pipeline；不做登入/雲端/DB |

### Step 5.2：核心設計——GO-gate 用 server 端 `threading.Event` 阻塞

```python
GATED = {"train", "optimize"}

def _loop(self):
    for st in self.stages:
        self._emit(Event("stage", st.name, {"status": "running"}))
        if st.name in GATED:
            self._gate.clear()
            self._emit(Event("await_confirm", st.name, {"estimate_min": ...}))
            self._gate.wait()      # ⭐ 物理阻塞，不靠前端自律
        st.run(self._emit)
```

> **教學金句**：「不偷燒 GPU 不是『前端按鈕』——是 server 端的 `threading.Event`，前端再壞，runner 也不會跑。」

### Step 5.3：踩坑 4 — modal 沒彈出

cockpit 跑到 train 階段卡住，看起來「停了」其實是在等 GO-gate confirm，但 modal 沒成功彈。**curl 救**：

```bash
curl -X POST http://127.0.0.1:8787/confirm
```

學員體會：UI 失靈時，**設計成 server 端有獨立 API 是救命的**——不靠 UI 也能繼續推進。

### Step 5.4：踩坑 5 — 訓練曲線 watcher 第一版會吐上輪歷史

第一版 `_start_csv_tail` 開跑前不清 `results.csv`，如果上次 50 epoch 的 csv 還在，watcher 一啟動就 emit 50 個歷史 metric，畫面瞬間滿——然後 YOLO 覆寫檔案 watcher 又因為 `seen=50` 追不到新列。

**正解**：開跑前 `csv_path.unlink(missing_ok=True)`。

> **教學金句**：「tail 一個會被覆寫的檔，第一件事是『先把舊的清掉』——這不是強迫症，是不清就 bug。」

---

## Phase 6：截圖兌現 + LinkedIn 故事（10 分鐘）

### Step 6.1：兩張截圖配對

| 截圖 | 角色 |
|---|---|
| `cockpit-training.jpg` | 訓練中——曲線即時長、KPI 0.951、stage 燈接力 |
| `cockpit-done.jpg` | 跑完——10 張 bbox 成果圖、mAP@0.5 = 0.9950、log 完整 |

塞進 README 「③ 視覺駕駛艙」段下方——**懸念到這裡兌現閉環**。

### Step 6.2：LinkedIn 文案結構

四件事必備：
1. **首三句鉤子**：LinkedIn 動態流前 ~200 字必須砸完數字 + 反直覺對比（Mac 不是雲）
2. **不卑微**：不寫「excited to share」、不求按讚
3. **差異化記憶點**：「asks before it burns your GPU」這種一句話釘住的賣點
4. **單一 CTA**：repo 連結，乾淨

中英文各發一篇，分時段發。中文針對在地、英文針對國際——同篇 po 兩個 ID，演算法也吃。

> **教學金句**：「LinkedIn 不是『分享我做了什麼』——是『讓陌生人在 3 秒內知道為什麼這值得他停下來』。三秒內沒打到就划走，不會看完。」

---

## 整合 demo：一條龍跑完（5 分鐘）

打開 cockpit 跑一次給學員看：
```bash
cd auto-cv-train-inference-optimization
cp configs/wafer.yaml configs/wafer-quick.yaml
sed -i '' 's/epochs: 50/epochs: 5/' configs/wafer-quick.yaml
uv run autocv ui
```
瀏覽器選 `wafer-quick.yaml` → Run → 看 5 階段燈、log、曲線、bbox gallery 全部跑出來 → 截圖。

---

## 常見問題 / FAQ

| Q | A |
|---|---|
| 為什麼 brainstorming 要寫 spec 才 plan？不能直接 plan 嗎？ | spec 是「**為什麼做、做什麼、不做什麼**」，plan 是「**怎麼做**」。混在一起 = AI 邊跑邊改方向、commit 雜亂。 |
| ruff 太煩，可不可以關掉？ | 不要。ruff 擋下的 6 個 E402 你今天看是煩，半年後 PR review 才看是丟臉。 |
| 為什麼 cockpit 不用 React / Next.js？ | 一個檔案、無 npm build、複製貼上就能跑——對「viral repo」截圖足夠了。多人要協作再上 React。 |
| 為什麼 commit 不用 `feat:` `fix:` 前綴？ | conventional commits 是給 CI 自動 changelog 用的，這個 repo 沒這需求，純白話更好讀。 |
| GO-gate 為什麼要在 server 端阻塞？前端 confirm 不就好？ | 前端 JS 可以被改、可以被繞過。server 端 `threading.Event` 物理上不確認就不跑——這是設計，不是禮儀。 |

---

## 卡點對照表 ⭐

| 卡點 | 真實原因 | 處理 |
|---|---|---|
| `gh repo create` 建到工作帳號 | `GITHUB_TOKEN` 環境變數鎖死 gh | 不靠 gh，瀏覽器手建 + SSH alias `git@github-personal:` push |
| commit 訊息洩漏行銷策略 | 寫了「加強 FOMO」「不卑微」 | 第一次：force push 改寫；最終解：刪 repo 重建 + 從此純技術訊息 |
| push 被擋 non-fast-forward | 使用者在網頁編 README 留下 commit | `git fetch + git rebase origin/main`，**不要** force push 蓋掉使用者編輯 |
| GO-gate modal 沒彈出 | 前端 bug | `curl -X POST :8787/confirm` 解卡（記得設計 server 端獨立 API） |
| ruff 6 個 E402 | plan 把 import 接在檔中段 | 全部收到檔頂端，function 內 import 不動 |
| 訓練曲線吐上輪 50 個歷史點 | watcher 啟動時舊 `results.csv` 還在 | `csv_path.unlink(missing_ok=True)` 在跑 train 前 |
| README 渲染成 H2 標題 | rebase 自動合留下 `text\n---` 沒空行 | 中間補一個空行 |
| autocv ui 跑了但 modal 看不到 | 可能瀏覽器重整把那次 await_confirm 消耗掉 | server 加 `GET /status` 暴露 pending_confirm（roadmap 已列） |

---

## 講師私房筆記

### 時間配置（120 分鐘）
- Phase 0：10 分鐘 — 環境必裝、SSH alias 設定（不要省，會卡爆）
- Phase 1：20 分鐘 — brainstorming 4 問題現場演練（**最值錢的一段**，學員會「啊原來該這樣想」）
- Phase 2：15 分鐘 — plan 拆解，重點看「YAGNI 取捨」段
- Phase 3：30 分鐘 — 實作 + commit + ruff 踩坑
- Phase 4：20 分鐘 — 上 GitHub 三個真實踩坑（**全班學員手上會學到一輩子**）
- Phase 5：25 分鐘 — cockpit 第二輪，重點看 GO-gate server 阻塞
- Phase 6：10 分鐘 — LinkedIn 文案

### 故意踩坑（比口頭講有效十倍）
1. **commit 寫「加強 FOMO」然後 push** → 等學員自己問「會被看到嗎？」 → 才示範 force push + delete repo 重建
2. **跑 cockpit 時不要先教 curl /confirm** → 讓他們撞到 modal 不彈、卡住、想砸電腦 → 才丟救命指令
3. **第一輪 cockpit 跑完不刪 results.csv** → 第二輪訓練曲線吐 50 個點然後沒新動靜 → 學員自己 debug 出 unlink

### 給不同學員角色推薦
| 角色 | 重點學 |
|---|---|
| 純 ML 工程師 | Phase 1 brainstorming、Phase 5 server 端 GO-gate |
| 純前端工程師 | Phase 5 零建置單頁 + WebSocket、Phase 6 LinkedIn 文案 |
| 想做 side project 的全端 | 全篇從頭到尾，重點放 Phase 4 上 GitHub 紀律 |
| 想學「跟 AI 對話開發」工作流 | Phase 1-3 brainstorming → spec → plan 三段接力 |

### Kevin 親自驗證的真實狀況
- 我親自踩過 **commit 洩漏 FOMO** 那段——當下心臟漏一拍。學員看到我修 + 重建的過程比看完美教學記憶深 10 倍
- subagent-driven 在這個專案**真的會狂跳權限框**，我半路切回 inline 才順——這是真實 trade-off，不是書上規則
- mAP 第一次跑 50 epochs 拿到 **0.9950**（比 4-agent demo 那次的 0.9913 高），純粹是 split 不同—— wafer-quick 5 epochs 拿到 ~0.95，截圖夠看
- LinkedIn 文案實機改了 4 次（從通用「我做了 YOLO wrapper」→ 改成「你有用 Claude Code 嗎？」針對性切角），**切角才是文案的命**，文法是其次

---

## 一句話總結

> **這份 walkthrough 不是教「怎麼寫 YOLO 訓練腳本」——是教『怎麼把腦袋裡的爆款想法，用 spec → plan → 紀律 commit → 截圖兌現 → LinkedIn 文案 一條工作流，變成公開可分享的成品』。少任何一段，做出來的東西都還沒準備好被陌生人看到。**

---

## 進階閱讀
- 🔗 [auto-cv repo（成品）](https://github.com/kevin801221/auto-cv-train-optimization-claude_code)
- 🔗 [autocv 第一輪 spec](../superpowers/specs/2026-05-19-auto-cv-train-inference-optimization-design.md)
- 🔗 [autocv 第一輪 plan](../superpowers/plans/2026-05-19-auto-cv-train-inference-optimization.md)
- 🔗 [cockpit 第二輪 spec](../superpowers/specs/2026-05-19-autocv-ui-cockpit-design.md)
- 🔗 [cockpit 第二輪 plan](../superpowers/plans/2026-05-19-autocv-ui-cockpit.md)
- 🔗 [superpowers brainstorming skill 原始檔](https://github.com/.../superpowers/skills/brainstorming)

---

_Last updated: 2026-05-21_
_Maintainer: Kevin (kevin@legalsign.ai)_
_配套教材（同目錄）：course_12hr_walkthrough.md（總帶課譜）、four_skills_walkthrough.md（四技能組合）、agent_team_walkthrough.md（多 agent 真實案例）_
_專案實戰案例：https://github.com/kevin801221/auto-cv-train-optimization-claude_code_
