# 08. agent-team-review — Claude 規則

教學用沙盒。一個 Kanban 看板的骨架 + 完整規格（`app/SPEC.md`），
用來教 agent team 怎麼用、以及它的好處。

## 目標

開一個 4 人 agent team（backend / frontend / test / docs 各擁一層），
照 `app/SPEC.md` 從骨架蓋出一個完整、能跑、測試全綠的 Kanban 看板。

## 規則

- Python 套件用 uv 管理（絕不用 pip）
- Mac 環境
- 路徑用 pathlib.Path
- 回覆繁體中文
- **檔案所有權邊界是硬規則**：每個隊友只能改自己那層
  - backend-owner  → `app/backend/`
  - frontend-owner → `app/frontend/`
  - test-owner     → `app/tests/`
  - docs-owner     → `app/docs/`
- 跨層需求一律用隊友間訊息對齊契約，不要越界改別人的層
- 任務依賴：backend 定契約 → frontend / test / docs 並行（都依賴 backend）

## 不要做的事

- 維護「這個教學專案」時，**不要自己先把 Kanban 蓋完** ——
  蓋 app 是使用者開 agent team 實跑時的事；這裡只維護骨架 + SPEC + 教材
- 不要動 `app/` 骨架裡指向 SPEC 的 TODO（那是給隊友的起點）
- 不要把多層塞進同一個檔（破壞檔案所有權邊界的教學意義）
- 主管不要自己動手實作，要委派給隊友
- 不要 hardcode 任何 key（這個沙盒不需要）
