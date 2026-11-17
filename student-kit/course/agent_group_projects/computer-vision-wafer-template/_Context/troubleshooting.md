# 常見卡點對照表

| 症狀 | 原因 | 解決 |
|---|---|---|
| 按 `e` 之後 Claude Code 停住不動 | VS Code 開了 .md tab 但你沒關，Claude Code 在等你 | 關掉 VS Code 那個 tab，下次直接按 `s` |
| `/agents` 找不到「Create new agent」 | 沒切到 Agents tab | 按 `←` 切到最左邊 |
| `ROBOFLOW_API_KEY unauthorized` | `.env` 沒設或 key 過期 | 確認 `.env` 在專案根目錄、`python-dotenv` 有 `load_dotenv()` |
| `roboflow project not found` | workspace 或 project 名拼錯 | 用 SDK 列 workspace 下所有 project 確認名稱 |
| Roboflow 下載卡在 0% | 資料夾已存在 + overwrite=False | script 加 `overwrite=True` |
| 套件找不到 | `uv run` vs `.venv/bin/python` 環境不一致 | 統一用 `uv add`（會更新 pyproject.toml）+ `.venv/bin/python` 執行 |
| MPS 不可用 | macOS 太舊或 PyTorch 沒裝對 | 升級到 macOS 12.3+、確認 `torch.backends.mps.is_built()` |
| MPS 訓練中某 op 不支援 | PyTorch + Apple Silicon 限制 | `export PYTORCH_ENABLE_MPS_FALLBACK=1` |
| 訓練爆 RAM | batch 太大 | batch 8 改 4 |
| Claude 沒呼叫 sub-agent | description 觸發句不夠強 | 重新觸發時加入 agent 提到的關鍵字（例如「下載」「切分」「訓練」） |
| Roboflow 只給 train 沒 val/test | 該版本沒切分 | 讓 bbox-labeler 用 seed=42 自切 70/20/10 |
| Roboflow 只有 1 個類別 | 該版本只標一類 | 接受現況、單類別繼續跑（教學重點是 pipeline 跑通） |
| matplotlib 在訓練後產不出圖 | 沒設 Agg backend | `matplotlib.use('Agg')` 寫在 `import pyplot` **之前** |
| `summary.md` 圖片不顯示 | 路徑寫錯 | 用相對路徑 `![](pred_xxx.png)`，summary.md 跟 PNG 同層 |

## 如果還是不行

1. 看 agent 在對話裡實際說了什麼（不是黑箱）
2. 看它寫了哪些檔案：`ls Projects/2026-001-mvp/`
3. 看 agent 定義：`cat .claude/agents/<name>.md`，確認 system prompt 規則沒寫錯

agent 不是黑箱，它做的每件事都是檔案 + 指令，全部都能追蹤。
