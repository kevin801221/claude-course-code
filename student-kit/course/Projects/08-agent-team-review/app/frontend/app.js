// Kanban 看板前端 —— agent team 的起點骨架。
//
// 這是空殼。frontend-owner 隊友照 app/SPEC.md 蓋：
//   - 三欄看板 todo / doing / done，各欄列出該狀態的卡片
//   - 頂部輸入框新增卡片（POST /api/cards，預設 todo）
//   - 每張卡有 ←/→ 移動鈕（PATCH status）+ 刪除鈕（DELETE）
//   - 任何操作後重新 render
// 串 API 前，先跟 backend-owner 確認 /api/cards 的契約（見 app/SPEC.md）。

const API_BASE = "http://localhost:8000";

// 骨架自我檢查：確認後端活著（蓋好後可刪這段）。
fetch(`${API_BASE}/api/health`)
  .then((r) => r.json())
  .then((d) => console.log("backend health:", d))
  .catch(() => console.warn("後端還沒起？先跑 uv run python app/backend/server.py"));

// TODO(frontend-owner): 從這裡開始蓋。
