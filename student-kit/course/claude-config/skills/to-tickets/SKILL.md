---
name: to-tickets
description: Break a plan or spec into tracer-bullet vertical slice tickets, each declaring its blocking edges (Ticket Graph).
disable-model-invocation: true
---

# To Tickets (Matt Pocock Skills Suite)

將規格書拆分為帶有明確阻擋相依性（Blocking edges）的垂直工單：

## 核心規則

1. **Tracer Bullet 垂直切片**：每個任務貫穿資料庫、邏輯、UI 與測試，避免水平拆分。
2. **聲明 Blocking Edges**：明確標記 `Blocked by: Task X`。無阻擋者標為 `None`。
3. **單一窗口大小**：每個 Ticket 需能容納在單一乾淨的 Context Window 中完成。
