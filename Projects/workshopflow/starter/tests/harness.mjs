import { mkdtemp, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { createInterface } from "node:readline";
import assert from "node:assert/strict";
// Only public HTTP endpoints are inspected. Each case receives a new temporary DB.
export async function fixture(t, phase = "v1") {
  const dir = await mkdtemp(path.join(os.tmpdir(), "workshop-grade-"));
  const env = {
    ...process.env,
    PORT: "0",
    WORKSHOP_DB: path.join(dir, "case.sqlite"),
  };
  let proc, closed, base;
  const stop = async () => {
    if (proc && proc.exitCode === null && proc.signalCode === null) proc.kill();
    if (closed) await closed;
  };
  const restart = async (next = phase) => {
    await stop();
    proc = spawn(process.execPath, ["server/start.mjs"], {
      env: { ...env, WORKSHOP_PHASE: next },
      stdio: ["ignore", "pipe", "inherit"],
    });
    closed = once(proc, "exit");
    const reader = createInterface({ input: proc.stdout });
    let timer;
    try {
      base = await Promise.race([
        new Promise((resolve) =>
          reader.on("line", (s) => {
            if (s.startsWith("READY ")) resolve(s.slice(6));
          }),
        ),
        closed.then(() => {
          throw Error("server exited before READY");
        }),
        new Promise((_, reject) => {
          timer = setTimeout(
            () => reject(Error("server start timeout")),
            10000,
          );
        }),
      ]);
    } finally {
      clearTimeout(timer);
      reader.close();
    }
  };
  t.after(async () => {
    await stop();
    await rm(dir, { recursive: true, force: true });
  });
  await restart(phase);
  const req = async (user, method, url, body) => {
    const r = await fetch(base + "/api" + url, {
      method,
      headers: { "Content-Type": "application/json", "X-Participant": user },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    return { code: r.status, data: await r.json() };
  };
  const ok = async (...args) => {
    const x = await req(...args);
    assert.ok(
      x.code >= 200 && x.code < 300,
      "Expected 2xx: " + JSON.stringify(x),
    );
    return x.data;
  };
  return {
    get base() {
      return base;
    },
    restart,
    req,
    ok,
    join: (u, s = "s2") => ok(u, "POST", "/sessions/" + s + "/enroll"),
    cancel: (u, s = "s2") => ok(u, "POST", "/sessions/" + s + "/cancel/" + u),
    patch: (b, s = "s2") => ok("hr", "PATCH", "/sessions/" + s, b),
    list: () => ok("hr", "GET", "/registrations"),
    session: (s = "s2") => ok("hr", "GET", "/sessions/" + s),
    review: (u, decision = "approve", s = "s2") =>
      ok("hr", "POST", "/sessions/" + s + "/review/" + u, { decision }),
  };
}
