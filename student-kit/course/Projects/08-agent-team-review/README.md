# 小專案 8：用 Agent Team 蓋一個 Kanban 看板

> 丟一個相對大的案子給設好的 agent team：開一個 4 人團隊（backend / frontend / test / docs
> 各擁一層），照 `app/SPEC.md` 從骨架蓋出一個完整、能跑、測試全綠的 Kanban 看板。
> **一小時內在你的機器上就能跑完整套。**

## 這堂課教什麼

不是教你「要不要用 agent team」，而是**怎麼用、以及它好在哪**：

1. 怎麼把一個團隊 set 好（4 個 owner、各擁一層、任務有依賴）
2. 怎麼丟一個夠大的案子讓團隊自己跑完
3. 親眼看到 agent team 的好處

## Agent team 跟 sub-agent 差在哪（一句話）

- **Sub-agent**：各做各的，只把結論回報給主對話，**隊友之間不能直接對話**。
- **Agent team**：隊友**共享一個任務列表**、**可以直接互相傳訊息對齊契約**、各自獨立 context 並行做。

跨層蓋功能正好需要「frontend 直接問 backend 契約」——這就是 agent team 發揮的場景。

## Agent team 的好處（這趟要你看到的）

1. **並行**：backend 一完成，frontend / test / docs 三個同時動，牆鐘時間遠短於一人序列。
2. **隊友直接對齊契約**：frontend 直接問 backend「POST 的 body 跟 response 長怎樣」，不繞主對話。
3. **共享任務列表 + 依賴自動解鎖**：backend 沒好之前，下游三個是 `blocked`；一完成就解鎖並行。
4. **各自獨立 context**：每個 owner 自己一份 context，不互相污染，主對話保持乾淨。
5. **檔案所有權邊界**：每個 owner 只碰自己那層 = 零檔案衝突。這就是「把 team set 好」的關鍵。

## 沙盒長什麼樣（起點是骨架，不是空白）

```
app/
├── SPEC.md              ← 完整功能規格（team 照這蓋；這就是「丟給 team 的大案子」）
├── backend/server.py    ← 空殼：只有 GET /api/health
├── frontend/index.html  ← 空白頁 + TODO
├── frontend/app.js      ← 空殼 + TODO（會 ping health 證明骨架活著）
├── tests/test_health.py ← 一個 smoke test（證明骨架能跑）
└── docs/README.md       ← 留給 docs-owner 寫 api.md / usage.md
```

給「骨架 + 明確 SPEC」而不是全空，是為了讓團隊不用猜需求，**一小時內可控**。

## 四個 owner（已放好在 `.claude/agents/`）

| owner | 擁有層 | 工作 |
|---|---|---|
| backend-owner | `app/backend/` | 定 cards CRUD 契約 + 實作 4 個 endpoint |
| frontend-owner | `app/frontend/` | 三欄看板 UI + 串 API |
| test-owner | `app/tests/` | 釘契約 + edge cases |
| docs-owner | `app/docs/` | API 文件 + 使用說明 |

專案層直接生效，不用複製。要個人層共用：

```bash
mkdir -p ~/.claude/agents
cp .claude/agents/{backend,frontend,test,docs}-owner.md ~/.claude/agents/
```

## 起手式

```bash
cd Projects/08-agent-team-review

# 0. 確認版本（agent teams 需要 v2.1.32+）
claude --version

# 1. 確認骨架能跑（應該 1 passed）
uv run --with pytest pytest app/tests/ -v

# 2. 起後端，確認 health 活著
uv run python app/backend/server.py        # 另開一個終端機：curl localhost:8000/api/health
```

實驗性 flag 已在本資料夾的 `.claude/settings.json` 設好：

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

## 跑 agent team（核心演練）

在這個資料夾開 `claude`，貼這段（**可直接照跨**）：

```text
這個 app/ 是一個 Kanban 看板的骨架，完整需求寫在 app/SPEC.md。
開一個 agent team，四個隊友各擁一層：
- backend-owner（用 backend-owner agent 定義）擁 app/backend/
- frontend-owner（用 frontend-owner agent 定義）擁 app/frontend/
- test-owner（用 test-owner agent 定義）擁 app/tests/
- docs-owner（用 docs-owner agent 定義）擁 app/docs/

照 app/SPEC.md 把 Kanban 看板蓋完。任務依賴：backend 先定 cards CRUD 契約並實作
→ frontend / test / docs 三個都依賴 backend，backend 完成後並行進行。
隊友只能改自己那層，跨層需求用訊息對齊契約，不要越界改別人的層。
全部完成後 test-owner 跑 uv run --with pytest pytest app/tests/ -v 給我 pass/fail 摘要，然後清理團隊。
```

主管會：建 team → 生 4 個隊友 → 拆出有依賴的任務 → 隊友認領並互相喊話 → 綜合結果 → 清理。

## 一小時時間表（讓你抓節奏）

| 時間 | 階段 | 你在看什麼 |
|---|---|---|
| 0–5 min | 確認版本/flag、跑骨架 smoke | 1 passed、health 200 |
| 5–10 min | 貼 prompt，team 建立、拆任務 | 共享任務列表出現，下游三個 `blocked` |
| 10–25 min | backend 定契約 + 實作 | frontend 來問契約、backend 回精確 shape |
| 25–50 min | frontend / test / docs **並行** | 三個隊友同時動 —— 這就是並行價值 |
| 50–60 min | 驗收 + 清理 | pytest 全綠、瀏覽器能操作看板、清掉 team |

## 驗收（怎麼知道成功了）

```bash
uv run --with pytest pytest app/tests/ -v   # 全綠，涵蓋 CRUD + edge cases
uv run python app/backend/server.py          # 瀏覽器開 app/frontend/index.html，
                                             # 能新增卡片、用 ←/→ 移動、刪除
```

## 觀察重點（這才是這堂課的價值）

- 用 **Shift+Down** 在隊友間循環，直接跟某個隊友喊話。
- 看**共享任務列表**：backend 任務沒完成前，下游三個應該是 `blocked`。
- 看隊友**互相傳訊息**對齊契約（frontend 問、backend 回精確 shape）。
- 對照 sub-agent：sub-agent 各做各的、只回報主對話，**不會互相對齊契約**。

## 故障排除

| 症狀 | 解法 |
|---|---|
| 沒生出隊友 | 確認 `claude --version` ≥ 2.1.32；確認 flag 有開；in-process 模式按 Shift+Down 找隊友 |
| 主管自己動手沒委派 | 回：「等你的隊友完成任務再繼續，不要自己做」 |
| 兩個隊友改到同一檔互相覆蓋 | 收斂任務邊界，每個隊友只擁一層；重申硬規則 |
| 下游任務一直 blocked | 任務狀態可能滯後（實驗性已知限制）—— 叫主管推 backend-owner 把任務標完成 |
| 權限提示太多 | 生隊友前先在 settings 預批准常用操作（隊友權限會冒泡到主管）|
| 主管提前說做完了 | 回：「先驗收 pytest 全綠、瀏覽器能操作再說，沒綠就繼續」 |
| 結束後殘留 tmux session | `tmux ls` 然後 `tmux kill-session -t <name>` |

## 進階變化

- **改成研究/審查場景**：同一批 owner 定義，叫多個 reviewer 各看 security / performance /
  test-coverage 同一個 PR（agent team 另一個強用例）。
- **加計畫批准閘門**：prompt 加「backend-owner 改動前要先提計畫給主管批准」。
- **加品質閘門 hook**：用 `TaskCompleted` hook 在任務標完成時跑 lint，不過就擋下並回饋。
- **指定模型**：prompt 加「每個隊友用 Sonnet」省 token。
- **把看板做大**：加截止日、標籤、拖拉、卡片排序——每加一個 feature 就是一條新的依賴鏈。

## 配套教材

- 講師教案：[`../../docs/walkthroughs/agent_team_walkthrough.md`](../../docs/walkthroughs/agent_team_walkthrough.md)
- 功能規格：[`app/SPEC.md`](app/SPEC.md)

## 把這個專案推上 GitHub

第一次玩 GitHub？看隔壁 [`../02-recipe-genie/docs/GITHUB_SETUP.md`](../02-recipe-genie/docs/GITHUB_SETUP.md) —— 完整三方案教學（gh CLI + SSH / GitHub MCP / PAT），含常見錯誤排查。
