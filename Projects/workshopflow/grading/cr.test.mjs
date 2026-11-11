import test from "node:test";
import assert from "node:assert/strict";
import { fixture } from "./harness.mjs";
test("13/14 待審不占位與併發核准，重送不重排", async (t) => {
  const a = await fixture(t, "cr");
  for (const u of ["e1", "e2"]) {
    const e = await a.join(u);
    assert.equal(e.status, "pending_approval");
    assert.equal(e.queue, null);
  }
  assert.equal((await a.session()).remaining, 1);
  const rows = await Promise.all([a.review("e1"), a.review("e2")]);
  assert.deepEqual(rows.map((x) => x.status).sort(), [
    "confirmed",
    "waitlisted",
  ]);
  const w = rows.find((x) => x.status === "waitlisted");
  assert.equal((await a.review(w.participantId)).queue, w.queue);
  assert.equal((await a.list()).length, 2);
});
test("14 核准當下排在既有候補之後", async (t) => {
  const a = await fixture(t, "cr");
  await a.join("e1");
  await a.join("i1");
  const i = await a.join("i2");
  const e = await a.review("e1");
  assert.ok(e.queue > i.queue);
  await a.cancel("i1");
  assert.equal((await a.ok("i2", "GET", "/mine"))[0].status, "confirmed");
});
test("15 拒絕／取消待審、禁止學生審核、可重新申請", async (t) => {
  const a = await fixture(t, "cr");
  await a.join("i1");
  await a.join("i2");
  await a.join("e1");
  assert.equal(
    (
      await a.req("e1", "POST", "/sessions/s2/review/e1", {
        decision: "approve",
      })
    ).code,
    403,
  );
  assert.equal((await a.review("e1", "reject")).status, "rejected");
  assert.equal(
    (
      await a.req("hr", "POST", "/sessions/s2/review/e1", {
        decision: "approve",
      })
    ).code,
    409,
  );
  await a.join("e1");
  await a.cancel("e1");
  assert.equal(
    (
      await a.req("hr", "POST", "/sessions/s2/review/e1", {
        decision: "approve",
      })
    ).code,
    409,
  );
  assert.equal((await a.ok("i2", "GET", "/mine"))[0].status, "waitlisted");
});
test("16 同一 DB 從 v1 更新，不重審舊資料；截止仍可核准", async (t) => {
  const a = await fixture(t);
  await a.join("e1");
  await a.join("e2");
  await a.restart("cr");
  assert.deepEqual((await a.list()).map((x) => x.status).sort(), [
    "confirmed",
    "waitlisted",
  ]);
  await a.cancel("e2");
  assert.equal((await a.join("e2")).status, "pending_approval");
  await a.patch({ open: false });
  assert.equal((await a.req("i1", "POST", "/sessions/s2/enroll")).code, 409);
  assert.equal((await a.review("e2")).status, "waitlisted");
});
