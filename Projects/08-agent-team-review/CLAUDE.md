# 08. agent-team-review — Claude 規則

教學用沙盒。一個刻意只做一半的便利貼板，用來演練 agent team 跨層協作。

## 目標

開一個 3 人 agent team（frontend/backend/test 各擁一層），並行補完「新增便利貼」功能。

## 規則

- Python 套件用 uv 管理（絕不用 pip）
- Mac 環境
- 路徑用 pathlib.Path
- 回覆繁體中文
- **檔案所有權邊界是硬規則**：每個隊友只能改自己那層的資料夾
  - frontend-owner → `app/frontend/`
  - backend-owner → `app/backend/`
  - test-owner → `app/tests/`
- 跨層需求一律用隊友間訊息對齊契約，不要自己越界改別人的層
- 任務有依賴順序：backend 定契約 → frontend 串 → test 釘

## 不要做的事

- 不要拿掉 `app/` 裡刻意留的「半成品」缺口去先做（那是給隊友演練的）
- 不要把三層塞進同一個檔（會破壞檔案所有權邊界的教學意義）
- 主管不要自己動手實作，要委派給隊友
- 不要 hardcode 任何 key（這個沙盒本來就不需要）
