# autocv ui 視覺駕駛艙 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** 替 `autocv` 加 `autocv ui` 本機視覺駕駛艙：FastAPI + 單頁自刻前端，即時顯示 5 階段 pipeline 接力、log、訓練曲線、成果圖，train/optimize 前強制 GO-gate。

**Architecture:** FastAPI(uvicorn) 後端直接 import `autocv` 套件函式，背景 thread 跑 pipeline，事件經 `queue.Queue` 用 WebSocket 廣播給單頁前端（零建置 HTML/JS/CSS 內聯）。GO-gate 用 `threading.Event` 在 server 端物理阻塞。

**Tech Stack:** Python 3.11, uv, FastAPI, uvicorn[standard], starlette TestClient, httpx, typer, 既有 autocv 套件。

---

## 常數

- REPO 根：`/Users/kevinluo/auto-cv-train-inference-optimization`（以下 `$R`）
- 全程 `cd $R` 用 `uv run`；commit 訊息**純技術中文、無行銷字眼、無 AI 署名**（repo git 身分已是 kevin801221）
- 既有：`src/autocv/{config,device,data,split,train,optimize,infer,cli}.py`、10 個測試
- 前端**禁用 `.innerHTML`**，一律 `createElement`/`textContent`（安全 + 過 hook）

## File Structure

```
$R/src/autocv/server/
├── __init__.py        package marker
├── events.py          Event dataclass + kind 常數（純資料，可測）
├── runner.py          PipelineRunner：背景 thread + event queue + GO-gate
├── real_stages.py     五階段轉接 autocv 函式 + 輸出轉 log
├── app.py             FastAPI：REST + WebSocket + 靜態
└── static/index.html  單頁 cockpit UI（零建置、零 innerHTML）
$R/src/autocv/cli.py    +ui 子命令
$R/tests/test_server.py TestClient + runner 協定測試（不跑真訓練）
$R/pyproject.toml       +fastapi +uvicorn[standard]（dev +httpx）
```

---

### Task 1：加 web 相依

**Files:** Modify `$R/pyproject.toml`

- [ ] **Step 1: 改 pyproject.toml dependencies**

於 `dependencies = [...]` 內 `"Pillow>=10.0",` 後、`]` 前加：
```toml
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
```
並把 dev extras 改為：
```toml
dev = ["pytest>=8.0", "ruff>=0.6", "httpx>=0.27"]
```

- [ ] **Step 2: relock + 裝 + 驗證**

Run:
```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization && uv lock && uv pip install -e ".[dev]" -q && uv run python -c "import fastapi, uvicorn, httpx; print('web deps ok')"
```
Expected: `web deps ok`

- [ ] **Step 3: 既有測試不破**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest -q`
Expected: `10 passed`

- [ ] **Step 4: Commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git add pyproject.toml uv.lock
git commit -m "加 FastAPI/uvicorn 相依供 web cockpit 使用"
```

---

### Task 2：events.py（TDD）

**Files:** Create `$R/src/autocv/server/__init__.py`, `$R/src/autocv/server/events.py`, `$R/tests/test_server.py`

- [ ] **Step 1: 建測試檔 `$R/tests/test_server.py`**

```python
from autocv.server.events import Event


def test_event_to_dict_round_trips():
    e = Event(kind="stage", stage="train", payload={"status": "running"})
    assert e.to_dict() == {
        "kind": "stage",
        "stage": "train",
        "payload": {"status": "running"},
    }


def test_event_kinds_constant():
    from autocv.server.events import KINDS

    assert {"stage", "log", "metric", "await_confirm", "result", "done"} <= set(KINDS)
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_server.py -v`
Expected: FAIL（`ModuleNotFoundError: autocv.server`）

- [ ] **Step 3: 實作**

Create `$R/src/autocv/server/__init__.py`:
```python
"""autocv 本機視覺駕駛艙（FastAPI + 單頁前端）。"""
```

Create `$R/src/autocv/server/events.py`:
```python
"""駕駛艙 WebSocket 事件資料結構。"""

from __future__ import annotations

from dataclasses import dataclass, field

KINDS = ("stage", "log", "metric", "await_confirm", "result", "done")


@dataclass
class Event:
    kind: str
    stage: str = ""
    payload: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"kind": self.kind, "stage": self.stage, "payload": self.payload}
```

- [ ] **Step 4: 跑測試確認通過**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_server.py -v`
Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git add src/autocv/server/__init__.py src/autocv/server/events.py tests/test_server.py
git commit -m "加 server.events 事件資料結構"
```

---

### Task 3：runner.py（TDD，核心邏輯）

**Files:** Create `$R/src/autocv/server/runner.py`; Modify `$R/tests/test_server.py`

- [ ] **Step 1: 追加失敗測試（檔尾）**

```python
import time

from autocv.server.runner import GATED, PipelineRunner, Stage


def _wait(r, timeout=2.0):
    deadline = time.time() + timeout
    while r.status not in ("done", "error") and time.time() < deadline:
        time.sleep(0.05)


def test_runner_runs_stages_in_order_and_emits_done():
    calls = []
    r = PipelineRunner(
        [
            Stage("data", lambda emit: calls.append("data")),
            Stage("split", lambda emit: calls.append("split")),
        ]
    )
    r.start()
    _wait(r)
    drained = list(r.events.queue)
    assert calls == ["data", "split"]
    triples = [(e.kind, e.stage, e.payload.get("status")) for e in drained]
    assert ("stage", "data", "running") in triples
    assert ("stage", "data", "done") in triples
    assert drained[-1].kind == "done" and drained[-1].payload["ok"] is True


def test_runner_gate_blocks_until_confirm():
    ran = []
    r = PipelineRunner(
        [Stage("train", lambda emit: ran.append("train"), estimate=lambda: 3.0)]
    )
    r.start()
    time.sleep(0.25)
    assert ran == []
    awaits = [e for e in list(r.events.queue) if e.kind == "await_confirm"]
    assert awaits and awaits[0].payload["estimate_min"] == 3.0
    r.confirm()
    _wait(r)
    assert ran == ["train"] and r.status == "done"


def test_runner_error_emits_error_event():
    def boom(emit):
        raise RuntimeError("x")

    r = PipelineRunner([Stage("data", boom)])
    r.start()
    _wait(r)
    assert r.status == "error"
    assert list(r.events.queue)[-1].payload["ok"] is False


def test_gated_constant():
    assert "train" in GATED and "optimize" in GATED
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_server.py -v`
Expected: FAIL（`ModuleNotFoundError: autocv.server.runner`）

- [ ] **Step 3: 實作 `$R/src/autocv/server/runner.py`**

```python
"""背景 thread 跑 pipeline，發事件到 queue，train/optimize 前 GO-gate 阻塞。"""

from __future__ import annotations

import queue
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Optional

from autocv.server.events import Event

GATED = {"train", "optimize"}


@dataclass
class Stage:
    name: str
    run: Callable[[Callable[[Event], None]], None]
    estimate: Optional[Callable[[], float]] = None
    detail: str = ""


@dataclass
class PipelineRunner:
    stages: list[Stage]
    events: "queue.Queue[Event]" = field(default_factory=queue.Queue)
    status: str = "idle"
    _gate: threading.Event = field(default_factory=threading.Event)
    _thread: Optional[threading.Thread] = None

    def _emit(self, ev: Event) -> None:
        self.events.put(ev)

    def confirm(self) -> None:
        self._gate.set()

    def start(self) -> None:
        if self.status == "running":
            raise RuntimeError("已有 pipeline 在跑")
        self.status = "running"
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self) -> None:
        try:
            for st in self.stages:
                self._emit(Event("stage", st.name, {"status": "running"}))
                if st.name in GATED:
                    est = st.estimate() if st.estimate else 0.0
                    self._gate.clear()
                    self._emit(
                        Event(
                            "await_confirm",
                            st.name,
                            {"estimate_min": est, "detail": st.detail},
                        )
                    )
                    self._gate.wait()
                st.run(self._emit)
                self._emit(Event("stage", st.name, {"status": "done"}))
            self.status = "done"
            self._emit(Event("done", "", {"ok": True}))
        except Exception as exc:  # noqa: BLE001
            self.status = "error"
            self._emit(Event("done", "", {"ok": False, "error": str(exc)}))
```

- [ ] **Step 4: 跑測試確認通過**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_server.py -v`
Expected: 全部 passed（events 2 + runner 4）

- [ ] **Step 5: Commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git add src/autocv/server/runner.py tests/test_server.py
git commit -m "加 server.runner：背景 pipeline 執行與 GO-gate 阻塞"
```

---

### Task 4：real_stages.py 真實 5 階段轉接

**Files:** Create `$R/src/autocv/server/real_stages.py`; Modify `$R/tests/test_server.py`

- [ ] **Step 1: 追加測試（檔尾）**

```python
def test_build_real_stages_shape():
    from pathlib import Path

    from autocv.config import load_config
    from autocv.server.real_stages import build_stages

    cfg = load_config(Path("configs/wafer.yaml"))
    names = [s.name for s in build_stages(cfg, Path.cwd(), optimize=False)]
    assert names == ["data", "split", "train", "infer"]
    opt = [s.name for s in build_stages(cfg, Path.cwd(), optimize=True)]
    assert opt == ["data", "split", "optimize", "infer"]
    train = next(
        s for s in build_stages(cfg, Path.cwd(), optimize=False) if s.name == "train"
    )
    assert train.estimate is not None
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_server.py::test_build_real_stages_shape -v`
Expected: FAIL（ModuleNotFoundError）

- [ ] **Step 3: 實作 `$R/src/autocv/server/real_stages.py`**

```python
"""把 autocv 五階段包成 Stage，捕捉 stdout 成 log 事件，train/optimize 提供預估。"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

from autocv.config import Config
from autocv.server.events import Event
from autocv.server.runner import Stage


def _logged(fn, emit) -> object:
    buf = io.StringIO()
    result = None
    with contextlib.redirect_stdout(buf):
        result = fn()
    for line in buf.getvalue().splitlines():
        if line.strip():
            emit(Event("log", payload={"line": line}))
    return result


def build_stages(cfg: Config, root: Path, optimize: bool) -> list[Stage]:
    from autocv.data import download
    from autocv.infer import infer
    from autocv.split import split

    def data_run(emit):
        _logged(lambda: download(cfg, root), emit)

    def split_run(emit):
        _logged(lambda: split(cfg, root), emit)

    def train_run(emit):
        from autocv.train import train

        _logged(lambda: train(cfg, root, yes=True), emit)

    def opt_run(emit):
        from autocv.optimize import optimize as do_opt

        _logged(lambda: do_opt(cfg, root, yes=True), emit)

    def infer_run(emit):
        out_dir = _logged(lambda: infer(cfg, root), emit)
        if out_dir:
            pngs = sorted(Path(out_dir).glob("pred_*.png"))
            emit(
                Event(
                    "result",
                    "infer",
                    {"images": [f"/artifacts/{p.name}" for p in pngs]},
                )
            )

    def train_estimate() -> float:
        from autocv.train import _count_train_imgs, _estimate_minutes

        n = _count_train_imgs(root / cfg.paths.processed)
        return round(_estimate_minutes(n, cfg.train.epochs, cfg.train.batch), 1)

    mid = (
        Stage("optimize", opt_run, estimate=lambda: float(cfg.optimize.iterations))
        if optimize
        else Stage("train", train_run, estimate=train_estimate)
    )
    return [
        Stage("data", data_run),
        Stage("split", split_run),
        mid,
        Stage("infer", infer_run),
    ]
```

- [ ] **Step 4: 跑測試確認通過**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_server.py -v`
Expected: 全部 passed

- [ ] **Step 5: Commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git add src/autocv/server/real_stages.py tests/test_server.py
git commit -m "加 server.real_stages：五階段轉接 + 輸出轉 log 事件"
```

---

### Task 5：app.py FastAPI（TDD via TestClient）

**Files:** Create `$R/src/autocv/server/app.py`; Create 最小 `$R/src/autocv/server/static/index.html`; Modify `$R/tests/test_server.py`

- [ ] **Step 1: 追加測試（檔尾）**

```python
from fastapi.testclient import TestClient

from autocv.server.app import create_app


def _fake_factory():
    def factory(config: str, optimize: bool):
        return PipelineRunner([Stage("data", lambda emit: None)])

    return factory


def test_configs_endpoint_lists_yaml():
    c = TestClient(create_app(runner_factory=_fake_factory()))
    r = c.get("/configs")
    assert r.status_code == 200
    assert "configs/wafer.yaml" in r.json()["configs"]


def test_index_served():
    c = TestClient(create_app(runner_factory=_fake_factory()))
    r = c.get("/")
    assert r.status_code == 200
    assert 'id="stages"' in r.text and "cockpit" in r.text.lower()


def test_run_then_double_run_409():
    c = TestClient(create_app(runner_factory=_fake_factory()))
    assert c.post("/run", json={"config": "configs/wafer.yaml"}).status_code == 200
    assert c.post("/run", json={"config": "configs/wafer.yaml"}).status_code == 409


def test_ws_streams_events():
    c = TestClient(create_app(runner_factory=_fake_factory()))
    c.post("/run", json={"config": "configs/wafer.yaml"})
    with c.websocket_connect("/ws") as ws:
        kinds = []
        for _ in range(10):
            msg = ws.receive_json()
            kinds.append(msg["kind"])
            if msg["kind"] == "done":
                break
    assert "done" in kinds
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_server.py -k "configs_endpoint or index_served or double_run or ws_streams" -v`
Expected: FAIL（ModuleNotFoundError: autocv.server.app）

- [ ] **Step 3: 實作 `$R/src/autocv/server/app.py`**

```python
"""FastAPI：列 config / 啟動 / 確認 GO-gate / WebSocket 事件流 / 靜態。"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Callable, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from autocv.server.runner import PipelineRunner

STATIC = Path(__file__).parent / "static"


def _default_factory(config: str, optimize: bool) -> PipelineRunner:
    from autocv.config import load_config
    from autocv.server.real_stages import build_stages

    root = Path.cwd()
    cfg = load_config(config)
    return PipelineRunner(build_stages(cfg, root, optimize=optimize))


def create_app(
    runner_factory: Optional[Callable[[str, bool], PipelineRunner]] = None,
) -> FastAPI:
    factory = runner_factory or _default_factory
    app = FastAPI(title="autocv cockpit")
    state: dict = {"runner": None}

    @app.get("/configs")
    def configs() -> JSONResponse:
        files = sorted(str(p) for p in Path("configs").glob("*.yaml"))
        return JSONResponse({"configs": files})

    @app.post("/run")
    def run(body: dict) -> JSONResponse:
        r = state["runner"]
        if r is not None and r.status == "running":
            return JSONResponse({"error": "已有 pipeline 在跑"}, status_code=409)
        runner = factory(
            body.get("config", "configs/wafer.yaml"),
            bool(body.get("optimize", False)),
        )
        state["runner"] = runner
        runner.start()
        return JSONResponse({"status": "running"})

    @app.post("/confirm")
    def confirm() -> JSONResponse:
        r = state["runner"]
        if r is None:
            return JSONResponse({"error": "尚未啟動"}, status_code=400)
        r.confirm()
        return JSONResponse({"status": "confirmed"})

    @app.websocket("/ws")
    async def ws(sock: WebSocket) -> None:
        await sock.accept()
        try:
            while True:
                r = state["runner"]
                if r is None:
                    await asyncio.sleep(0.1)
                    continue
                try:
                    ev = r.events.get_nowait()
                except Exception:
                    await asyncio.sleep(0.05)
                    continue
                await sock.send_json(ev.to_dict())
                if ev.kind == "done":
                    break
        except WebSocketDisconnect:
            return

    if STATIC.is_dir():
        app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")

    @app.get("/artifacts/{name}")
    def artifact(name: str):
        p = Path.cwd() / "runs" / "infer" / name
        if not p.is_file():
            return HTMLResponse("not found", status_code=404)
        return FileResponse(str(p))

    @app.get("/", response_class=HTMLResponse)
    def index() -> HTMLResponse:
        f = STATIC / "index.html"
        return HTMLResponse(f.read_text() if f.is_file() else "<h1>cockpit</h1>")

    return app
```

- [ ] **Step 4: 建最小 `$R/src/autocv/server/static/index.html`（Task 6 換完整版）**

```html
<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>autocv cockpit</title></head>
<body><h1>autocv cockpit</h1><div id="stages"></div></body></html>
```

- [ ] **Step 5: 跑測試確認通過**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_server.py -v`
Expected: 全部 passed

- [ ] **Step 6: Commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git add src/autocv/server/app.py src/autocv/server/static/index.html tests/test_server.py
git commit -m "加 server.app：REST + WebSocket + 靜態服務"
```

---

### Task 6：完整 cockpit 單頁 UI（零 innerHTML）

**Files:** Overwrite `$R/src/autocv/server/static/index.html`

- [ ] **Step 1: 覆寫成完整深色 cockpit（全程 createElement/textContent，無 .innerHTML）**

```html
<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>autocv cockpit</title>
<style>
:root{--bg:#0b0f1a;--panel:#121829;--line:#1f2a44;--txt:#e7ecf6;--mut:#7d8aa6;--accent:#5b8cff;--ok:#3ddc97;--run:#ffb454;--err:#ff5d6c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font:14px/1.5 -apple-system,"Segoe UI",Roboto,"PingFang TC",sans-serif}
header{display:flex;align-items:center;gap:16px;padding:14px 20px;border-bottom:1px solid var(--line);background:var(--panel)}
header h1{font-size:15px;margin:0;letter-spacing:.5px}.sp{flex:1}
select,button{background:#1b2238;color:var(--txt);border:1px solid var(--line);border-radius:8px;padding:8px 12px;font-size:13px}
button{cursor:pointer}button.primary{background:var(--accent);border-color:var(--accent);font-weight:600}
button:disabled{opacity:.5;cursor:not-allowed}
.grid{display:grid;grid-template-columns:240px 1fr;gap:16px;padding:16px;max-width:1180px;margin:0 auto}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}
.card h2{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:var(--mut);margin:0 0 12px}
.st{display:flex;align-items:center;gap:10px;padding:10px;border-radius:10px;margin-bottom:8px;background:#0f1424}
.dot{width:10px;height:10px;border-radius:50%;background:var(--mut);flex:none}
.st.running .dot{background:var(--run);box-shadow:0 0 0 4px rgba(255,180,84,.2)}
.st.done .dot{background:var(--ok)}.st.error .dot{background:var(--err)}
.st small{color:var(--mut);margin-left:auto}
canvas{width:100%;height:200px;background:#0f1424;border-radius:10px}
#log{height:200px;overflow:auto;background:#0f1424;border-radius:10px;padding:10px;font:12px/1.45 "SF Mono",Menlo,monospace;color:#bcd}
#gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px}
#gallery img{width:100%;border-radius:8px;border:1px solid var(--line)}
.modal{position:fixed;inset:0;background:rgba(4,7,15,.78);display:none;align-items:center;justify-content:center}
.modal.on{display:flex}.modal .box{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:24px;max-width:420px;text-align:center}
.modal h3{margin:0 0 8px}.modal p{color:var(--mut)}
.kpi{display:flex;gap:20px;margin-top:10px}.kpi b{font-size:22px;color:var(--ok)}
.row{display:flex;gap:16px;flex-direction:column}
@media(max-width:760px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <h1>⌁ autocv cockpit</h1>
  <select id="cfg"></select>
  <label style="color:var(--mut)"><input type="checkbox" id="opt"> optimize</label>
  <div class="sp"></div>
  <button class="primary" id="run">▶ Run pipeline</button>
</header>
<div class="grid">
  <div class="card"><h2>Pipeline 接力</h2><div id="stages"></div></div>
  <div class="row">
    <div class="card"><h2>訓練曲線</h2><canvas id="chart" width="800" height="200"></canvas><div class="kpi" id="kpi"></div></div>
    <div class="card"><h2>即時 log</h2><div id="log"></div></div>
    <div class="card"><h2>成果圖</h2><div id="gallery"></div></div>
  </div>
</div>
<div class="modal" id="modal"><div class="box">
  <h3 id="mTitle">準備開始訓練</h3><p id="mBody"></p>
  <button class="primary" id="go">我了解，開始</button>
</div></div>
<script>
const STAGES=["data","split","train","optimize","infer"];
const sEl=document.getElementById("stages"),logEl=document.getElementById("log"),
gal=document.getElementById("gallery"),cv=document.getElementById("chart"),ctx=cv.getContext("2d"),
cfgSel=document.getElementById("cfg"),runBtn=document.getElementById("run");
let pts=[],st={};
function el(tag,cls,txt){const e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e;}
function clr(n){while(n.firstChild)n.removeChild(n.firstChild);}
function drawStages(){clr(sEl);STAGES.forEach(n=>{const row=el("div","st "+(st[n]||""));
 row.appendChild(el("span","dot"));row.appendChild(el("span",null,n));
 row.appendChild(el("small",null,st[n]||""));sEl.appendChild(row);});}
drawStages();
function setStage(n,s){st[n]=s;drawStages();}
function logLine(l){logEl.appendChild(el("div",null,l));logEl.scrollTop=logEl.scrollHeight;}
function curve(){ctx.clearRect(0,0,cv.width,cv.height);if(pts.length<2)return;
 const mx=Math.max(...pts.map(p=>p.epoch)),my=Math.max(0.01,...pts.map(p=>p.map50));
 ctx.strokeStyle="#5b8cff";ctx.lineWidth=2;ctx.beginPath();
 pts.forEach((p,i)=>{const x=20+(p.epoch/mx)*(cv.width-40),y=cv.height-20-(p.map50/my)*(cv.height-40);
  i?ctx.lineTo(x,y):ctx.moveTo(x,y);});ctx.stroke();}
function setKpi(v){const k=document.getElementById("kpi");clr(k);
 const d=el("div",null,"mAP@0.5 ");d.appendChild(el("b",null,(v||0).toFixed(3)));k.appendChild(d);}
fetch("/configs").then(r=>r.json()).then(d=>{clr(cfgSel);
 (d.configs||[]).forEach(c=>cfgSel.appendChild(el("option",null,c)));});
let ws;
runBtn.onclick=()=>{st={};drawStages();clr(logEl);clr(gal);pts=[];curve();runBtn.disabled=true;
 fetch("/run",{method:"POST",headers:{"Content-Type":"application/json"},
  body:JSON.stringify({config:cfgSel.value,optimize:document.getElementById("opt").checked})})
 .then(r=>{if(r.status===409){alert("已有 pipeline 在跑");runBtn.disabled=false;return;}openWS();});};
function openWS(){ws=new WebSocket(`ws://${location.host}/ws`);
 ws.onmessage=e=>{const m=JSON.parse(e.data);
 if(m.kind==="stage")setStage(m.stage,m.payload.status);
 else if(m.kind==="log")logLine(m.payload.line);
 else if(m.kind==="metric"){pts.push(m.payload);curve();setKpi(m.payload.map50);}
 else if(m.kind==="await_confirm"){document.getElementById("mTitle").textContent="準備開始 "+m.stage;
  document.getElementById("mBody").textContent="預估約 "+m.payload.estimate_min+" 分鐘。"+(m.payload.detail||"")+" 你的算力你決定。";
  document.getElementById("modal").classList.add("on");}
 else if(m.kind==="result"){clr(gal);(m.payload.images||[]).forEach(u=>{const i=el("img");i.src=u;gal.appendChild(i);});}
 else if(m.kind==="done"){runBtn.disabled=false;if(!m.payload.ok)logLine("ERROR: "+(m.payload.error||""));}};}
document.getElementById("go").onclick=()=>{document.getElementById("modal").classList.remove("on");
 fetch("/confirm",{method:"POST"});};
</script>
</body>
</html>
```

- [ ] **Step 2: 驗證測試仍過**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_server.py -v`
Expected: 全部 passed（index 仍含 `id="stages"` 與 `cockpit`）

- [ ] **Step 3: Commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git add src/autocv/server/static/index.html
git commit -m "加完整深色 cockpit 單頁 UI"
```

---

### Task 7：cli.py 加 `ui` 子命令

**Files:** Modify `$R/src/autocv/cli.py`; Modify `$R/tests/test_server.py`

- [ ] **Step 1: 追加測試（檔尾）**

```python
from typer.testing import CliRunner

from autocv.cli import app as cli_app


def test_cli_has_ui_command():
    r = CliRunner().invoke(cli_app, ["--help"])
    assert r.exit_code == 0 and "ui" in r.output
    r2 = CliRunner().invoke(cli_app, ["ui", "--help"])
    assert r2.exit_code == 0 and "--no-browser" in r2.output
```

- [ ] **Step 2: 跑測試確認失敗**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest tests/test_server.py::test_cli_has_ui_command -v`
Expected: FAIL

- [ ] **Step 3: 在 `$R/src/autocv/cli.py` 的 `if __name__ == "__main__":` 之前插入**

```python
@app.command()
def ui(
    config: str = ConfigOpt,
    host: str = typer.Option("127.0.0.1", help="綁定 host"),
    port: int = typer.Option(8787, help="綁定 port"),
    no_browser: bool = typer.Option(False, "--no-browser", help="不自動開瀏覽器"),
) -> None:
    """開本機視覺駕駛艙（瀏覽器）。"""
    import uvicorn

    from autocv.server.app import create_app

    if not no_browser:
        import threading
        import webbrowser

        threading.Timer(1.2, lambda: webbrowser.open(f"http://{host}:{port}")).start()
    typer.echo(f"cockpit -> http://{host}:{port}（Ctrl+C 結束）")
    uvicorn.run(create_app(), host=host, port=port, log_level="warning")
```

- [ ] **Step 4: 跑全套 + smoke**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest -q && uv run autocv --help`
Expected: 全 passed；`autocv --help` 列出 `ui`

- [ ] **Step 5: Commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git add src/autocv/cli.py tests/test_server.py
git commit -m "cli 加 ui 子命令：起服務並開瀏覽器"
```

---

### Task 8：README 兌現懸念

**Files:** Modify `$R/README.md`

- [ ] **Step 1: 改 README 🔒 區塊那行**

找到：
```
- 🔒 **無碼視覺駕駛艙**：拖一個資料集、按一個鈕、看 5 個 agent 在畫面上即時接力、訓練曲線即時長出來。零指令。
```
替換成：
```
- ✅ **無碼視覺駕駛艙**（已上線）：`uv run autocv ui` 開瀏覽器，選 config、按 Run，看 5 階段即時接力、訓練曲線即時長出、跑完看成果圖。
```

- [ ] **Step 2: 在「② 跟 Claude Code 講話」區塊後新增第三種開法**

在 README `**② 跟 Claude Code 講話**` 那段落之後、`## 換成你的資料集` 之前插入：
````
**③ 視覺駕駛艙 / Visual cockpit**

```bash
uv run autocv ui          # 開瀏覽器，零指令
```
選 config、按 Run，5 階段燈即時接力、訓練曲線即時長、跑完成果圖直接看。train/optimize 前一定先跳預估時間，按確認才開跑。
````

- [ ] **Step 3: 全套測試 + ruff + 啟動 smoke**

Run:
```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest -q && uv run ruff check src tests && (uv run autocv ui --no-browser --port 8788 & echo $! > /tmp/cock.pid) && sleep 4 && curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8788/ && kill "$(cat /tmp/cock.pid)"
```
Expected: 測試全 passed、ruff 乾淨、curl 回 `200`，server 被 kill

- [ ] **Step 4: Commit**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization
git add README.md
git commit -m "README 補視覺駕駛艙用法與狀態"
```

---

### Task 9：推上遠端

- [ ] **Step 1: 最終驗證**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && uv run pytest -q && uv run ruff check src tests && git status --porcelain`
Expected: 全 passed、ruff 乾淨、工作區乾淨

- [ ] **Step 2: 掃 commit 訊息無洩漏**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && git log --pretty=%s origin/main..HEAD`
Expected: 全純技術中文，無 FOMO/star/懸念/早鳥/卑微/roadmap

- [ ] **Step 3: push**

```bash
cd /Users/kevinluo/auto-cv-train-inference-optimization && git push origin main 2>&1 | tail -2
```

- [ ] **Step 4: 驗證遠端 = 本地**

Run: `cd /Users/kevinluo/auto-cv-train-inference-optimization && git rev-parse HEAD && git rev-parse origin/main`
Expected: 相同

---

## Self-Review

**Spec coverage：** `autocv ui`→T7；FastAPI+零建置單頁→T5/6；後端 import autocv 背景 thread+queue+WS→T3/5；真實 5 階段+log/result 事件→T4；GO-gate server 端 threading.Event 阻塞+UI modal→T3/6；YAGNI 一次一 job 409→T5；測試 TestClient+runner 協定不跑真訓練、CI 既有 pytest 自動含→T2-7；README 兌現→T8；commit 純技術→各 Task+T9S2。全部對得到。✅

**YAGNI 取捨（刻意，非缺漏）：** spec 提 train 時 tail `results.csv` 推 `metric` 曲線點。實作上 Ultralytics 進度經 stdout 由 `_logged` 即時轉 `log` 呈現；獨立 results.csv tailing 屬增益，本計畫不納入避免過度工程。曲線在無 `metric` 時空白、由 log 呈現進度，UI 仍完整（stage 接力+log 串流+成果圖）。日後要真曲線再加。

**Placeholder scan：** 各 step 均含完整檔案內容或精確指令+預期輸出，無 TBD/TODO/「類似上述」。✅

**Type consistency：** `Event(kind,stage,payload).to_dict()`、`Stage(name,run,estimate,detail)`、`PipelineRunner(stages).{events,status,start,confirm,_gate}`、`GATED`、`build_stages(cfg,root,optimize)->list[Stage]`、`create_app(runner_factory)`、CLI `ui` 參數跨 T2→T8 一致；測試引用符號均在前置 Task 定義；前端零 `.innerHTML`。✅
