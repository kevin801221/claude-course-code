# 設計：08-agent-team-review 改造為「Agent Team 蓋一個 Kanban 看板」

> 日期：2026-05-22
> 範圍：把 `Projects/08-agent-team-review` 從「agent team 批判性對比沙盒」改造成
> 「好好教 agent team 怎麼用 + 它的好處 + 一個一小時內可測完的相對大案子」。

## 1. 目標與定位轉向

現有 08 專案的重心是**批判性對比**：大篇幅論證「agent team 不是最強用例」、保留兩個
「驗證失敗 / 反例」素材（`debug-sample/`、`blind-review-sample/`），教學主軸是
「什麼時候才該開 team」。

使用者的新需求：**不要再強調差別，好好講怎麼用 agent team、它的好處，並用一個相對大、
但一小時內能測完的真案子讓設好的 team 去跑。**

| 維度 | 現在 | 改成 |
|---|---|---|
| 主軸 | 「不是最強用例」批判對比 | 怎麼用 + 好處 |
| 沙盒 | 便利貼板（3 個小缺口） | 從骨架蓋完整 Kanban 看板 |
| 反例素材 | `debug-sample/`、`blind-review-sample/` | 刪除 |
| 教案 | 四問判準 + 失敗反例 | 操作教學 + 好處導向 |
| Owner 數 | 3（frontend/backend/test） | 4（+ docs-owner） |

## 2. 關鍵設計決策

### 2.1 沙盒起點：骨架 + SPEC.md

評估三種：
- 全空（team 從零自己想）→ 一小時內變數太大，team 花時間猜需求。否決。
- 半成品（像便利貼留缺口）→ 太小，撐不起「大案子」。否決。
- **骨架 + SPEC.md（採用）** → 給空殼檔 + 一份明確功能規格，team 照 SPEC 從骨架長出
  完整 app。份量夠大，又因需求明確所以一小時可控。

起點結構：
```
app/
├── SPEC.md              # 完整功能規格（team 照這蓋；這是「丟給 team 的大案子」）
├── backend/server.py    # 空殼：只有 GET /api/health + TODO 指向 SPEC
├── frontend/index.html  # 空白頁 + TODO
├── frontend/app.js      # 空 + TODO
└── tests/test_health.py # 一個 placeholder smoke test（驗證骨架能跑）
```

**重要界線**：本專案交付的是「骨架 + SPEC + agent 定義 + 操作教學」。真正把 Kanban
蓋完的是使用者之後開的 agent team，**不是我們在改造階段幫它蓋完**。改造階段的驗收 =
骨架空殼能啟動、placeholder test 能跑、SPEC 完整、agent 定義正確、README 步驟可照做。

### 2.2 Agent Team 組成：4 個 owner

| owner | 擁有層 | 工作 |
|---|---|---|
| backend-owner | `app/backend/` | 定 cards CRUD 契約 + 實作 4 個 endpoint |
| frontend-owner | `app/frontend/` | 三欄看板 UI + 串 API |
| test-owner | `app/tests/` | 釘契約 + edge cases |
| docs-owner（新增） | `app/docs/` | API 契約文件 + 使用說明 |

加第 4 個 owner 的理由：讓「並行有感」更強——backend 完成後，frontend / test / docs
三個**同時解鎖並行**，牆鐘時間明顯短於一人序列。這正是要展示的好處。

## 3. Kanban 功能規格（app/SPEC.md 的內容）

資料模型：`card { id: int, title: str, status: "todo"|"doing"|"done", created_at: iso8601 }`
儲存：記憶體內 list（教學沙盒不接 DB；重啟即清空，SPEC 明寫此限制）。

| endpoint | 行為 | 成功回應 | 錯誤 |
|---|---|---|---|
| `GET /api/cards` | 列全部卡片 | `200 [{card}, ...]` | — |
| `POST /api/cards` | 建卡（title，預設 status=todo） | `201 {card}` | 空 title → `400` |
| `PATCH /api/cards/{id}` | 改 status 或 title | `200 {card}` | 不存在 → `404`；status 非法 → `400` |
| `DELETE /api/cards/{id}` | 刪卡 | `204` | 不存在 → `404` |

前端：三欄 todo / doing / done；頂部新增輸入框（加到 todo）；每張卡有 `←` / `→`
移動鈕 + 刪除鈕（**用按鈕，不做拖拉**，避免前端卡關）；任何操作後重新 render。

測試（pytest）：GET smoke、POST 建卡、PATCH 改 status、DELETE，加 edge case
（空 title 400、不存在 id 404、status 非法 400）。

## 4. 任務依賴鏈（agent team 教學亮點）

```
backend（定契約 + 實作）   ← 無依賴，先跑
        │
        ├──→ frontend（串 UI）    ┐
        ├──→ test（釘契約）       ├─ 三個都只依賴 backend → 並行解鎖
        └──→ docs（API 文件）     ┘
```

學生會親眼看到：backend 任務未完成前下游三個 `blocked`；backend 一完成，三個同時動。

## 5. 驗收（改造後 + 一小時實跑各一套）

改造後（我方）：
```bash
uv run --with pytest pytest app/tests/ -v   # placeholder smoke 綠（骨架能跑）
uv run python app/backend/server.py          # GET /api/health 回 200
```

一小時實跑（使用者開 agent team 後）：
```bash
uv run --with pytest pytest app/tests/ -v   # 全綠，涵蓋 CRUD + edge cases
uv run python app/backend/server.py          # 瀏覽器能建卡、移動卡、刪卡
```

## 6. 教學重點（README 與 walkthrough 要凸顯的「好處」）

1. 並行：4 owner 同時動，牆鐘時間遠短於一人序列。
2. 隊友直接對齊契約：frontend 直接問 backend 精確 shape，不繞主對話。
3. 共享任務列表 + 依賴自動解鎖：看得到 blocked → 解鎖的過程。
4. 各自獨立 context：主對話保持乾淨，不互相污染。
5. 檔案所有權邊界：每個 owner 只碰自己那層 = 零衝突（「把 team set 好」的關鍵）。

## 7. 檔案異動清單

- 改寫：`README.md`、`CLAUDE.md`、`docs/walkthroughs/agent_team_walkthrough.md`
  （動 walkthrough 觸發 walkthrough-style skill）
- 新增：`.claude/agents/docs-owner.md`、`app/SPEC.md`、`app/docs/`（含 placeholder）
- 改造：`app/`（便利貼骨架 → Kanban 骨架），更新 3 個現有 agent 定義的層描述
- 刪除：`debug-sample/`、`blind-review-sample/`
- 不動：PPT（Part 7/8 footer 仍指向本資料夾，路徑沒變）

## 8. 非目標（YAGNI）

- 不接資料庫（記憶體 list 即可）。
- 不做拖拉、不做登入、不做卡片排序/截止日。
- 改造階段不幫 team 把 Kanban 蓋完（那是使用者實跑時的事）。
- 不改 PPT slide 內文（路徑沒變；之後要再說）。
