# Kanban 看板 —— 功能規格（agent team 照這份蓋）

> 這是「丟給 agent team 的大案子」。team 裡的 4 個 owner 照這份 SPEC，
> 從 `app/` 的骨架長出一個完整、能跑、測試全綠的 Kanban 看板。
>
> **契約以 backend-owner 在 team 裡最終定的為準** —— SPEC 給方向，細節由隊友對齊。

## 一句話

一個三欄（todo / doing / done）的看板：可以新增卡片、用按鈕在欄位間移動卡片、刪除卡片。

## 資料模型

```
card {
  id:         int           # 後端產生，遞增
  title:      str           # 非空
  status:     "todo" | "doing" | "done"
  created_at: str           # ISO 8601
}
```

儲存：後端記憶體內的 list（教學沙盒，**不接資料庫**；重啟即清空）。

## API 契約（backend-owner 負責）

base：`http://localhost:8000`

| method | path | 行為 | 成功 | 錯誤 |
|---|---|---|---|---|
| GET | `/api/cards` | 列全部卡片 | `200 [card, ...]` | — |
| POST | `/api/cards` | 建卡（body: `{title}`，status 預設 `todo`） | `201 card` | 空 title → `400` |
| PATCH | `/api/cards/{id}` | 改 `status` 或 `title`（body 帶要改的欄位） | `200 card` | 不存在 → `404`；status 非法 → `400` |
| DELETE | `/api/cards/{id}` | 刪卡 | `204`（無 body） | 不存在 → `404` |

規則：
- 驗證輸入，永遠不信任 client。
- 錯誤回乾淨的 JSON（`{"error": "..."}`），不要噴 stack trace。
- 所有回應帶 `Access-Control-Allow-Origin: *`（前端是 file:// 開的）。

## 前端需求（frontend-owner 負責）

- 三欄版面：todo / doing / done，每欄列出該 status 的卡片。
- 頂部一個輸入框 + 「新增」鈕：建立卡片（預設進 todo 欄）。
- 每張卡片上：
  - `←` / `→` 鈕：在 todo ↔ doing ↔ done 之間移動（呼叫 PATCH 改 status）。
    最左欄沒有 `←`、最右欄沒有 `→`。
  - 刪除鈕：呼叫 DELETE。
- 任何操作成功後重新 render（簡單做：重新 GET 全部再畫）。
- **用按鈕移動，不做拖拉**（避免前端複雜度爆掉）。
- 用 `textContent` 塞使用者文字，不要用 `innerHTML`（避免 XSS）。
- API base URL 跟 response shape 集中在一個地方，契約好改。

## 測試需求（test-owner 負責）

用 `pytest` + 執行緒起短命 server（沿用 `test_health.py` 的 fixture 模式），
不打外部網路、deterministic：

- happy path：GET（空清單）、POST 建卡、PATCH 改 status、PATCH 改 title、DELETE。
- edge case：空 title → 400、不存在 id 的 PATCH/DELETE → 404、status 非法 → 400。
- 跑法：`uv run --with pytest pytest app/tests/ -v`，要全綠。

## 文件需求（docs-owner 負責）

在 `app/docs/` 寫：
- `api.md` —— 每個 endpoint 的最終契約（以 backend-owner 定的為準）。
- `usage.md` —— 怎麼啟動後端、怎麼開前端、怎麼操作看板。

## 任務依賴

```
backend（定契約 + 實作）   ← 先跑，無依賴
        │
        ├──→ frontend（串 UI）
        ├──→ test（釘契約）
        └──→ docs（API 文件）   ← 三個都只依賴 backend，可並行
```

## 完成定義（驗收）

```bash
uv run --with pytest pytest app/tests/ -v   # 全綠，涵蓋 CRUD + edge cases
uv run python app/backend/server.py          # 瀏覽器開 app/frontend/index.html，
                                             # 能新增卡片、用 ←/→ 移動、刪除
```

## 非目標（不要做）

- 不接資料庫、不做使用者登入、不做拖拉、不做卡片排序/截止日/標籤。
- 不要把多層塞進同一個檔（破壞檔案所有權邊界）。
