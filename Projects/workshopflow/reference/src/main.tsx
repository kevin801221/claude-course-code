import { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";
type Session = {
  id: string;
  title: string;
  description: string;
  starts: string;
  capacity: number;
  remaining: number;
  open: number;
};
type Reg = {
  sessionId: string;
  participantId: string;
  status: string;
  queue: number | null;
};
type Person = { id: string; kind: string };
const tags: Record<string, string> = {
  confirmed: "正取",
  waitlisted: "候補",
  cancelled: "已取消",
  pending_approval: "待審核",
  rejected: "已拒絕",
};
function App() {
  const [user, U] = useState(localStorage.getItem("actor") || "i1"),
    [loc, L] = useState(location.hash || "#list"),
    [people, P] = useState<Person[]>([]),
    [sessions, S] = useState<Session[]>([]),
    [regs, R] = useState<Reg[]>([]),
    [err, E] = useState(""),
    [version, V] = useState(0);
  const admin = user === "hr";
  async function api(path: string, method = "GET", body?: object) {
    const r = await fetch("/api" + path, {
      method,
      headers: { "X-Participant": user, "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    const j = await r.json();
    if (!r.ok) throw Error(j.error || "連線失敗");
    return j;
  }
  useEffect(() => {
    const f = () => L(location.hash || "#list");
    window.addEventListener("hashchange", f);
    return () => window.removeEventListener("hashchange", f);
  }, []);
  useEffect(() => {
    let active = true;
    Promise.all([
      api("/participants"),
      api("/sessions"),
      api(admin ? "/registrations" : "/mine"),
    ])
      .then(([p, s, r]) => {
        if (active) {
          P(p);
          S(s);
          R(r);
        }
      })
      .catch((e) => {
        if (active) E(String(e.message));
      });
    return () => {
      active = false;
    };
  }, [user, version]);
  async function act(path: string, body?: object, method = "POST") {
    try {
      await api(path, method, body);
      E("");
      V((n) => n + 1);
    } catch (e) {
      E(e instanceof Error ? e.message : String(e));
    }
  }
  function row(x: Reg) {
    return (
      <li key={x.sessionId + ":" + x.participantId}>
        {sessions.find((s) => s.id === x.sessionId)?.title} · {x.participantId}{" "}
        · <strong>{tags[x.status]}</strong>{" "}
        {x.queue !== null && "序號 " + x.queue}{" "}
        {!admin && !["cancelled", "rejected"].includes(x.status) && (
          <button
            onClick={() => act("/sessions/" + x.sessionId + "/cancel/" + user)}
          >
            取消報名
          </button>
        )}
        {admin && x.status === "pending_approval" && (
          <>
            <button
              onClick={() =>
                act("/sessions/" + x.sessionId + "/review/" + x.participantId, {
                  decision: "approve",
                })
              }
            >
              核准
            </button>
            <button
              onClick={() =>
                act("/sessions/" + x.sessionId + "/review/" + x.participantId, {
                  decision: "reject",
                })
              }
            >
              拒絕
            </button>
          </>
        )}
      </li>
    );
  }
  const sid = loc.split("/")[1],
    s = sessions.find((x) => x.id === sid),
    mine = regs.find((x) => x.sessionId === sid && x.participantId === user);
  return (
    <main>
      <h1>WorkshopFlow</h1>
      <p>企業內訓｜本機模擬身分</p>
      <label>
        目前身分{" "}
        <select
          value={user}
          onChange={(e) => {
            localStorage.setItem("actor", e.target.value);
            U(e.target.value);
            S([]);
            R([]);
            E("");
            location.hash = "list";
          }}
        >
          {people.map((x) => (
            <option key={x.id} value={x.id}>
              {x.id} · {x.kind}
            </option>
          ))}
        </select>
      </label>
      <nav>
        <a href="#list">場次列表</a>
        <a href="#mine">我的報名</a>
        {admin && <a href="#hr">HR 管理</a>}
      </nav>
      {err && <p role="alert">{err}</p>}
      {loc === "#list" && (
        <>
          <h2>場次列表</h2>
          {sessions.map((x) => (
            <article key={x.id}>
              <a href={"#details/" + x.id}>{x.title}</a>
              <p>
                {x.open ? "開放" : "已截止"} · 剩餘 {x.remaining} / {x.capacity}
              </p>
            </article>
          ))}
        </>
      )}
      {loc.startsWith("#details/") && s && (
        <>
          <h2>{s.title}</h2>
          <p>
            {s.description} · {s.starts}
          </p>
          <p>
            {s.open ? "開放" : "已截止"} · 剩餘 {s.remaining} / {s.capacity}
          </p>
          <p>我的狀態：{mine ? tags[mine.status] : "尚未報名"}</p>
          {!admin && (
            <button
              disabled={
                !s.open ||
                !!(mine && !["cancelled", "rejected"].includes(mine.status))
              }
              onClick={() => act("/sessions/" + sid + "/enroll")}
            >
              報名
            </button>
          )}
        </>
      )}
      {loc === "#mine" && (
        <>
          <h2>我的報名</h2>
          <ul>{regs.filter((x) => x.participantId === user).map(row)}</ul>
        </>
      )}
      {loc === "#hr" && admin && (
        <>
          <h2>HR 管理</h2>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const d = new FormData(e.currentTarget);
              act("/sessions", {
                title: d.get("title"),
                description: d.get("desc"),
                starts: new Date(String(d.get("start"))).toISOString(),
                capacity: Number(d.get("capacity")),
              });
            }}
          >
            <h3>建立場次</h3>
            <label>
              名稱 <input name="title" required />
            </label>
            <label>
              說明 <input name="desc" required />
            </label>
            <label>
              開始時間 <input name="start" required type="datetime-local" />
            </label>
            <label>
              容量{" "}
              <input
                name="capacity"
                defaultValue={1}
                required
                type="number"
                min="1"
              />
            </label>
            <button>建立</button>
          </form>
          {sessions.map((x) => (
            <article key={x.id}>
              <h3>{x.title}</h3>
              <p>
                {x.open ? "開放" : "已截止"} · 剩餘 {x.remaining} / {x.capacity}
              </p>
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  act(
                    "/sessions/" + x.id,
                    {
                      capacity: Number(
                        new FormData(e.currentTarget).get("capacity"),
                      ),
                    },
                    "PATCH",
                  );
                }}
              >
                <label>
                  容量{" "}
                  <input
                    type="number"
                    required
                    min="1"
                    name="capacity"
                    defaultValue={x.capacity}
                  />
                </label>
                <button>更新容量</button>
              </form>
              <button
                onClick={() =>
                  act("/sessions/" + x.id, { open: !x.open }, "PATCH")
                }
              >
                {x.open ? "截止報名" : "開放報名"}
              </button>
            </article>
          ))}
          <h3>全部報名與待審清單</h3>
          <ul>{regs.map(row)}</ul>
        </>
      )}
    </main>
  );
}
createRoot(document.querySelector("#root")!).render(<App />);
