import express from "express";
import { randomUUID } from "node:crypto";
import { db } from "./database.mjs";
export const api = express.Router();
const phase = process.env.WORKSHOP_PHASE || "v1";
if (!["v1", "cr"].includes(phase))
  throw Error("WORKSHOP_PHASE must be v1 or cr");
db.exec(`CREATE TABLE IF NOT EXISTS registrations(
 sessionId TEXT REFERENCES sessions(id), participantId TEXT REFERENCES participants(id),
 status TEXT NOT NULL CHECK(status IN ('confirmed','waitlisted','cancelled','pending_approval','rejected')),
 queue INTEGER UNIQUE, PRIMARY KEY(sessionId,participantId));
 CREATE TABLE IF NOT EXISTS seq(id INTEGER PRIMARY KEY CHECK(id=1),v INTEGER NOT NULL);
 INSERT OR IGNORE INTO seq VALUES(1,0);`);
const one = (q, ...v) => db.prepare(q).get(...v),
  all = (q, ...v) => db.prepare(q).all(...v),
  set = (q, ...v) => db.prepare(q).run(...v);
const fail = (status, message) => {
  throw Object.assign(Error(message), { status });
};
const getSession = (id) =>
  one("SELECT * FROM sessions WHERE id=?", id) || fail(404, "找不到場次");
const entry = (sid, uid) =>
  one(
    "SELECT * FROM registrations WHERE sessionId=? AND participantId=?",
    sid,
    uid,
  );
const remaining = (s) =>
  s.capacity -
  one(
    "SELECT COUNT(*) AS n FROM registrations WHERE sessionId=? AND status='confirmed'",
    s.id,
  ).n;
function allocate(s, uid) {
  const seat = remaining(s) > 0,
    queue = seat ? null : one("UPDATE seq SET v=v+1 WHERE id=1 RETURNING v").v;
  set(
    "UPDATE registrations SET status=?,queue=? WHERE sessionId=? AND participantId=?",
    seat ? "confirmed" : "waitlisted",
    queue,
    s.id,
    uid,
  );
}
function promote(s) {
  while (remaining(s) > 0) {
    const head = one(
      "SELECT participantId FROM registrations WHERE sessionId=? AND status='waitlisted' ORDER BY queue LIMIT 1",
      s.id,
    );
    if (!head) break;
    allocate(s, head.participantId);
  }
}
function tx(fn) {
  db.exec("BEGIN IMMEDIATE");
  try {
    const result = fn();
    db.exec("COMMIT");
    return result;
  } catch (e) {
    db.exec("ROLLBACK");
    throw e;
  }
}
const hr = (q) => {
  if (q.actor.kind !== "hr") fail(403, "需要 HR 身分");
};
const learner = (q) => {
  if (q.actor.kind === "hr") fail(403, "請使用學員身分");
};
api.use((q, _r, n) => {
  q.actor =
    one(
      "SELECT * FROM participants WHERE id=?",
      q.get("X-Participant") || "",
    ) || fail(401, "請先選擇教學身分");
  n();
});
api.get("/participants", (_q, r) =>
  r.json(all("SELECT * FROM participants ORDER BY id")),
);
api.get("/sessions", (_q, r) =>
  r.json(
    all("SELECT * FROM sessions ORDER BY id").map((s) => ({
      ...s,
      remaining: remaining(s),
    })),
  ),
);
api.get("/sessions/:id", (q, r) => {
  const s = getSession(q.params.id);
  r.json({
    ...s,
    remaining: remaining(s),
    mine: entry(s.id, q.actor.id) || null,
  });
});
api.get("/mine", (q, r) =>
  r.json(
    all(
      "SELECT * FROM registrations WHERE participantId=? ORDER BY sessionId",
      q.actor.id,
    ),
  ),
);
api.get("/registrations", (q, r) => {
  hr(q);
  r.json(
    all("SELECT * FROM registrations ORDER BY sessionId,queue,participantId"),
  );
});
function capacity(n) {
  if (!Number.isSafeInteger(n) || n <= 0) fail(400, "容量必須是正整數");
  return n;
}
api.post("/sessions", (q, r) => {
  hr(q);
  const { title, description, starts, capacity: n } = q.body || {};
  if (
    typeof title !== "string" ||
    !title.trim() ||
    typeof description !== "string" ||
    typeof starts !== "string" ||
    !Number.isFinite(Date.parse(starts))
  )
    fail(400, "請提供名稱、說明及開始時間");
  capacity(n);
  const id = randomUUID();
  set(
    "INSERT INTO sessions(id,title,description,starts,capacity) VALUES(?,?,?,?,?)",
    id,
    title.trim(),
    description,
    starts,
    n,
  );
  r.status(201).json(getSession(id));
});
api.patch("/sessions/:id", (q, r) => {
  hr(q);
  r.json(
    tx(() => {
      const s = getSession(q.params.id),
        b = q.body || {},
        n = b.capacity === undefined ? s.capacity : capacity(b.capacity),
        open = b.open === undefined ? !!s.open : b.open;
      if (typeof open !== "boolean") fail(400, "open 必須是布林值");
      if (n < s.capacity - remaining(s)) fail(409, "容量不得低於正取人數");
      set(
        "UPDATE sessions SET open=?,capacity=? WHERE id=?",
        Number(open),
        n,
        s.id,
      );
      const updated = getSession(s.id);
      promote(updated);
      return updated;
    }),
  );
});
api.post("/sessions/:id/enroll", (q, r) => {
  learner(q);
  r.json(
    tx(() => {
      const s = getSession(q.params.id),
        u = q.actor.id,
        old = entry(s.id, u);
      if (old && !["cancelled", "rejected"].includes(old.status)) return old;
      if (!s.open) fail(409, "場次已停止報名");
      set(
        "INSERT INTO registrations VALUES(?,?,'pending_approval',NULL) ON CONFLICT(sessionId,participantId) DO UPDATE SET status='pending_approval',queue=NULL",
        s.id,
        u,
      );
      if (!(phase === "cr" && q.actor.kind === "external")) allocate(s, u);
      return entry(s.id, u);
    }),
  );
});
api.post("/sessions/:id/cancel/:uid", (q, r) => {
  learner(q);
  if (q.actor.id !== q.params.uid) fail(403, "只能取消自己的報名");
  r.json(
    tx(() => {
      const s = getSession(q.params.id),
        old = entry(s.id, q.actor.id) || fail(404, "沒有報名");
      if (old.status === "rejected") fail(409, "已拒絕的報名不能取消");
      if (old.status !== "cancelled") {
        set(
          "UPDATE registrations SET status='cancelled',queue=NULL WHERE sessionId=? AND participantId=?",
          s.id,
          q.actor.id,
        );
        if (old.status === "confirmed") promote(s);
      }
      return entry(s.id, q.actor.id);
    }),
  );
});
api.post("/sessions/:id/review/:uid", (q, r) => {
  hr(q);
  if (phase !== "cr") fail(404, "v1 尚無審核");
  const decision = q.body?.decision;
  if (!["approve", "reject"].includes(decision))
    fail(400, "決定需為 approve 或 reject");
  r.json(
    tx(() => {
      const s = getSession(q.params.id),
        old = entry(s.id, q.params.uid) || fail(404, "沒有申請");
      if (old.status !== "pending_approval") {
        if (
          (decision === "approve" &&
            ["confirmed", "waitlisted"].includes(old.status)) ||
          (decision === "reject" && old.status === "rejected")
        )
          return old;
        fail(409, "申請已失效或已作出不同決定");
      }
      if (decision === "approve") allocate(s, q.params.uid);
      else
        set(
          "UPDATE registrations SET status='rejected' WHERE sessionId=? AND participantId=?",
          s.id,
          q.params.uid,
        );
      return entry(s.id, q.params.uid);
    }),
  );
});
api.use((_q, r) => r.status(404).json({ error: "沒有此 API" }));
