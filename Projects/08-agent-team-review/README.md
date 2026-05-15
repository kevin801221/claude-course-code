# 小專案 8：agent team 跨層功能開發

> 一個只做一半的「便利貼板」app（前端缺輸入框、後端 POST 沒做、測試沒補）。
> 開一個 3 人 agent team：frontend / backend / test 各擁一層，並行把它做完。

## 為什麼做

- ❌ 一個人 session 做跨層功能：寫前端要等後端契約、寫測試要等前後端都好，序列化很慢
- ❌ Sub-agent 只能回報結論給主對話，三個 agent 之間**無法直接喊話對齊契約**
- ✅ Agent team：三個隊友共享任務列表、直接互相傳訊息、各自獨立 context 並行做

> ⚠️ **誠實說**：官方文件指出跨層開發**不是 agent team 最強用例**（最強是研究/審查/競爭假設 debug，因為它們天然無檔案衝突）。
> 但跨層開發**最能讓你直觀看到並行價值**，也最能逼出「避免檔案衝突」這個關鍵踩雷 —— 所以拿來當教學沙盒。

## 用到的 Claude Code feature

- **Agent teams**（實驗性，需 v2.1.32+）—— 見 `.claude/settings.json` 的 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
- **Sub-agent 定義當 teammate**（`.claude/agents/*.md`）—— 同一份定義既可當 subagent 也可當隊友
- **共享任務列表 + 隊友間 mailbox**
- **檔案所有權邊界**（每個隊友硬規則只能碰自己那層）

## 沙盒長什麼樣

```
app/
├── backend/server.py     GET /api/notes ✅  | POST /api/notes ❌(backend-owner 的活)
├── frontend/index.html   顯示便利貼 ✅      | 新增輸入框 ❌(frontend-owner 的活)
├── frontend/app.js       loadNotes ✅       | POST + 重 render ❌
└── tests/test_notes.py   GET smoke ✅       | POST 測試 ❌(test-owner 的活)
```

三個缺口刻意設計成有依賴關係：**backend 定契約 → frontend 照契約串 → test 釘契約**。
這正是 agent team 任務依賴（dependency）的天然教材。

## 起手式

```bash
cd Projects/08-agent-team-review

# 0. 確認版本（agent teams 需要 v2.1.32+）
claude --version

# 1. 確認沙盒能跑（應該 1 passed）
uv run --with pytest pytest app/tests/ -v

# 2. 起後端，瀏覽器開 app/frontend/index.html 看現況（只有 1 張歡迎便利貼）
uv run python app/backend/server.py
```

## 安裝 sub-agent 定義

三個隊友定義已在 `.claude/agents/`。專案層直接生效，不用複製。
要個人層共用：

```bash
mkdir -p ~/.claude/agents
cp .claude/agents/{frontend,backend,test}-owner.md ~/.claude/agents/
```

## 跑 agent team（核心演練）

啟用實驗性 flag（本資料夾的 `.claude/settings.json` 已設好；或全域設）：

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

在這個資料夾開 `claude`，貼這段（**可直接照跨**）：

```text
這個 app/ 是一個只做一半的便利貼板。開一個 agent team，三個隊友：
- frontend-owner（用 frontend-owner agent 定義）擁 app/frontend/
- backend-owner（用 backend-owner agent 定義）擁 app/backend/
- test-owner（用 test-owner agent 定義）擁 app/tests/

要做的功能：新增便利貼（文字 + 顏色）。
任務依賴：backend 先定 POST /api/notes 契約並實作 → frontend 照契約串輸入框
→ test 釘住契約寫測試。隊友只能改自己那層，跨層需求用訊息對齊，不要自己越界改。
完成後 test-owner 跑 uv run pytest 給我 pass/fail 摘要，然後清理團隊。
```

主管會：建 team → 生 3 個隊友 → 拆出有依賴的任務 → 隊友認領並互相喊話 → 綜合結果 → 清理。

## 驗收（怎麼知道成功了）

```bash
uv run --with pytest pytest app/tests/ -v   # 多了 POST 的測試且全綠
uv run python app/backend/server.py          # 瀏覽器能新增便利貼並看到它出現
```

## 觀察重點（這才是這堂課的價值）

- 用 **Shift+Down** 在隊友間循環，直接跟某個隊友喊話
- 看**共享任務列表**：backend 任務沒完成前，test 任務應該是 blocked
- 看隊友**互相傳訊息**對齊契約（frontend 問、backend 回精確 shape）
- 對照 sub-agent：sub-agent 三個各做各的、只回報主對話，**不會互相對齊契約**

## 故障排除

| 症狀 | 解法 |
|---|---|
| 沒生出隊友 | 確認 `claude --version` ≥ 2.1.32；確認 flag 有開；in-process 模式按 Shift+Down 找隊友 |
| 主管自己動手沒委派 | 回：「等你的隊友完成任務再繼續，不要自己做」 |
| 兩個隊友改到同一檔互相覆蓋 | 這就是本課重點 —— 收斂任務邊界，每個隊友只擁一層；重申硬規則 |
| test 任務一直 blocked | 任務狀態可能滯後（實驗性已知限制）—— 叫主管推 backend-owner 把任務標完成 |
| 權限提示太多 | 生隊友前先在 settings 預批准常用操作（隊友權限會冒泡到主管）|
| 主管提前說做完了 | 回：「先驗收 pytest 全綠再說，沒綠就繼續」 |
| 結束後殘留 tmux session | `tmux ls` 然後 `tmux kill-session -t <name>` |

## 看 agent team 真正的強大（強烈建議先看這份）

跨層開發是 agent team **最弱**的展示。要親眼看到它不可替代，去跑**盲評一致性**：

- 📄 教案：[`../../docs/walkthroughs/agent_team_walkthrough.md`](../../docs/walkthroughs/agent_team_walkthrough.md)
- 📝 主演練 sample：[`blind-review-sample/`](blind-review-sample/README.md) —— 三份品質接近的文案，**換閱讀順序，單一 agent 名次就翻盤**（已驗證真實數據）；agent team 隔離評分就穩。這個弱點換更強的模型也逃不掉，只能靠架構隔離解決。
- 🐛 反例 sample：[`debug-sample/chat_server.py`](debug-sample/chat_server.py) —— 多嫌疑 bug，但強 LLM 靜態消去就收斂，示範「什麼場景**不**需要 agent team」（教案私房筆記有完整脈絡）

## 進階變化

- **改成研究/審查場景**（agent team 最強用例）：同一份 sub-agent 定義，叫 3 個 reviewer 各看 security / performance / test-coverage 同一個 PR
- **加計畫批准閘門**：prompt 加「backend-owner 改動前要先提計畫給主管批准」
- **加品質閘門 hook**：用 `TaskCompleted` hook 在任務標完成時跑 lint，不過就擋下並回饋
- **指定模型**：prompt 加「每個隊友用 Sonnet」省 token

## 把這個專案推上 GitHub

第一次玩 GitHub？看隔壁 [`../02-recipe-genie/docs/GITHUB_SETUP.md`](../02-recipe-genie/docs/GITHUB_SETUP.md) —— 完整三方案教學（gh CLI + SSH / GitHub MCP / PAT），含常見錯誤排查。
