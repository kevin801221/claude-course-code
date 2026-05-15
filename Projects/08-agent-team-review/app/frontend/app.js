// 便利貼板前端（教學沙盒，刻意留半成品）。
//
// 已實作：載入時 GET /api/notes 並 render。
// ❌ 還沒做 —— frontend-owner 隊友的任務：
//    加一個輸入框 + 按鈕，POST 新便利貼到後端，成功後重新 render。
//    送出前務必跟 backend-owner 確認 POST /api/notes 的契約。

const API_BASE = "http://localhost:8000";

async function loadNotes() {
  const res = await fetch(`${API_BASE}/api/notes`);
  const notes = await res.json();
  render(notes);
}

function render(notes) {
  const board = document.getElementById("board");
  board.replaceChildren(); // 清空（不用 innerHTML，避免 XSS 教壞學生）
  for (const n of notes) {
    const el = document.createElement("div");
    el.className = `note ${n.color || "yellow"}`;
    el.textContent = n.text; // textContent：純文字，安全
    board.appendChild(el);
  }
}

loadNotes();
