# pomocat — TUI 番茄鐘 設計文件

- **日期**：2026-05-14
- **作者**：Kevin Luo
- **狀態**：Design approved，待 implementation plan

## 1. 目標與範圍

打造一個 TUI 番茄鐘 `pomocat`，能：

- 倒數計時（work / short break / long break 三相位）
- 番茄結束時發聲提示
- 統計完成輪數，支援任務標籤（task label）
- 圖表顯示週/月成果
- 可透過 `uv tool install pomocat` 安裝為使用者全域工具

**非目標（明確排除）**：
- 跨平台聲音（只支援 macOS afplay + 終端 bell fallback）
- 雲端同步、多裝置統計
- 中途修改任務標籤
- 通知中心整合（macOS notification、Linux notify-send）

## 2. 技術棧

| 層 | 選擇 | 理由 |
|---|---|---|
| 語言 | Python 3.11+ | `tomllib` 內建、`StrEnum` 可用 |
| 套件管理 | uv | 與 `uv tool install` 一致 |
| TUI | Textual >= 0.80 | 主流 Python TUI，pilot 測試支援好 |
| 圖表 | textual-plotext >= 0.2.1 | 真實 line chart，非 ASCII block |
| CLI | typer >= 0.12 | subcommand 結構乾淨 |
| TOML 寫入 | tomli-w >= 1.0 | 讀用內建 tomllib，寫需外掛 |
| Build | hatchling | uv 預設、`force-include` 支援 bundle 資產 |
| Test | pytest + pytest-asyncio | textual pilot 需要 async |

## 3. 架構

三層拆分，core 不依賴 Textual，UI 不直接碰 storage：

```
src/pomocat/
├── __init__.py
├── cli.py                    # typer entry，路由到 ui/
├── core/                     # 純邏輯，零 Textual 依賴
│   ├── __init__.py
│   ├── timer.py              # TimerState、tick、next_phase
│   ├── stats.py              # Round、daily/weekly/monthly summary
│   └── config.py             # Config dataclass + toml I/O
├── ui/                       # Textual screens
│   ├── __init__.py
│   ├── app.py                # PomocatApp(App)
│   ├── timer_screen.py
│   ├── stats_screen.py
│   ├── config_screen.py
│   └── pomocat.tcss          # Midnight Executive 配色
├── sound.py                  # afplay + bell fallback
├── storage.py                # ~/.pomocat/ I/O
└── assets/
    └── alarm.wav             # bundled，importlib.resources 載入
```

**依賴方向**（單向）：
```
cli.py → ui/ → core/ + storage.py + sound.py
core/ 不 import 任何外部 I/O（不知道 storage、sound、Textual 存在）
storage.py 跟 sound.py 只被 cli.py / ui/ 呼叫
```

## 4. Domain model（core/）

### 4.1 `core/timer.py`

```python
class Phase(StrEnum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"

@dataclass(frozen=True)
class TimerState:
    phase: Phase
    remaining_seconds: int
    round_index: int           # 第幾個 work round（1-based）
    is_running: bool
    task_label: str | None

def tick(state: TimerState, elapsed_seconds: int = 1) -> TimerState:
    """Pure function：吃 state 出 state。is_running=False 時 no-op。"""

def next_phase(state: TimerState, cfg: Config) -> TimerState:
    """切下一相位。WORK→SHORT_BREAK/LONG_BREAK，BREAK→WORK。
    每 cfg.rounds_until_long_break 輪 work 結束後是 LONG_BREAK。
    LONG_BREAK 結束後 round_index reset 回 1。"""
```

**關鍵不變式**：
- `tick` 跟 `next_phase` 都不碰 I/O、不碰系統時間
- 「現實時間」由 UI 層注入（每秒 `set_interval` 呼叫 `tick(state, 1)`）
- `TimerState` frozen → 強制 immutable update

### 4.2 `core/stats.py`

```python
@dataclass(frozen=True)
class Round:
    started_at: datetime
    ended_at: datetime
    phase: Phase
    task_label: str | None
    completed: bool            # False = 中途 quit / reset / skip

@dataclass(frozen=True)
class DailySummary:
    date: date
    completed_work_count: int
    completed_work_minutes: int
    interrupted_count: int
    task_breakdown: dict[str, int]   # label → 顆數

def daily_summary(rounds: list[Round], target: date) -> DailySummary: ...
def weekly_summary(rounds: list[Round], week_start: date) -> list[DailySummary]: ...
def monthly_summary(rounds: list[Round], year: int, month: int) -> list[DailySummary]: ...
```

**統計規則**：
- 每個 round（含 break）一筆，append 進 storage
- `completed_work_count` 只算 `phase == WORK and completed == True`
- 中途 quit、reset、skip 都標 `completed=False`
- 任務未指定（None）顯示為 `"(no label)"`

### 4.3 `core/config.py`

```python
@dataclass
class Config:
    work_minutes: int = 25
    short_break_minutes: int = 5
    long_break_minutes: int = 15
    rounds_until_long_break: int = 4
    sound_enabled: bool = True

def load_config(path: Path) -> Config: ...    # 不存在回 default
def save_config(cfg: Config, path: Path) -> None:  # 用 tomli-w 寫
```

## 5. UI（ui/）

### 5.1 `PomocatApp`

```python
class PomocatApp(App):
    CSS_PATH = "pomocat.tcss"
    BINDINGS = [("q", "quit")]

    def __init__(self, initial_screen: str = "timer",
                 initial_task: str | None = None,
                 stats_range: str = "week"):
        ...

    def on_mount(self) -> None:
        # 依 initial_screen push timer/stats/config screen
```

### 5.2 `TimerScreen`

**Layout**：
```
┌─ pomocat ──────────────────────── round 3 / 4 ──┐
│                                                  │
│              ╔══════════════════╗                │
│              ║     24 : 13      ║                │
│              ╚══════════════════╝                │
│                  WORK · 寫教材                    │
│                                                  │
│         ████████████████░░░░░░░░  62%            │
│                                                  │
│   今日完成 5 顆 🍅  ·  本週 23 顆                │
│                                                  │
├──────────────────────────────────────────────────┤
│ [space] pause   [s] skip   [r] reset   [q] quit │
└──────────────────────────────────────────────────┘
```

**Widgets**：
- `Digits` 顯示 `MM:SS`
- 標題列：`Static` 顯示 round 計數
- phase badge：`Static`，CSS class 切換顏色
- `ProgressBar`：百分比
- footer：Textual `Footer` 顯示 bindings

**Bindings**：
- `space` → `action_toggle_pause`
- `s` → `action_skip_phase`（當前 round 標 `completed=False` append 進 storage，切下一 phase，`round_index` 照常前進）
- `r` → `action_reset`（當前 round 標 `completed=False` append 進 storage，**重置當前 phase 倒數時間為滿值**，`round_index` 不變）
- `q` → `action_quit`（當前 round 標 `completed=False` append 進 storage，退出 app）

**Driver**：
```python
def on_mount(self):
    self.set_interval(1.0, self.tick)

def tick(self):
    self.state = core.timer.tick(self.state)
    if self.state.remaining_seconds == 0:
        self._on_phase_complete()

def _on_phase_complete(self):
    storage.append_round(self._build_round(completed=True))
    sound.play_alarm()
    self.state = core.timer.next_phase(self.state, self.cfg)
    self._refresh_counters()    # 只在 phase 完成時重讀統計
```

**「今日 X 顆 / 本週 Y 顆」更新時機**：on_mount 載一次、`_on_phase_complete` 後重算一次。**不**在每秒 tick 讀檔——避免 I/O 影響倒數順暢度。

### 5.3 `StatsScreen`

**Layout**：
```
┌─ stats ──────────────────────────── 2026-05-14 ─┐
│                                                  │
│  今日：5 顆 (125 min) · 中斷 1 · 寫教材(3) debug(2) │
│                                                  │
│  ┌─ 本週 ────────────────────────────────────┐  │
│  │   plotext line chart                        │  │
│  └─────────────────────────────────────────────┘  │
│                                                  │
├──────────────────────────────────────────────────┤
│ [←/→] 切週   [d/w/m] 切粒度   [q] back          │
└──────────────────────────────────────────────────┘
```

**Widgets**：
- 頂部 summary：`Static`
- 圖表：`textual_plotext.PlotextPlot`，畫該週每日完成顆數
- footer：Textual `Footer`

**Bindings**：
- `left/right`：切上週/下週
- `d/w/m`：切日/週/月粒度
- `q`：回到 timer screen（若從 cli `pomocat stats` 進來則退出 app）

### 5.4 `ConfigScreen`

`Input` widget × 5（對應 Config 五個欄位）+ `Button` 儲存。儲存後 `save_config()` 並彈 toast「設定已儲存」。

Timer 進行中時 `pomocat config` 仍可開（不同 process），但本 process 內不能從 TimerScreen 切過去（避免中途改設定造成 round inconsistency）。

### 5.5 `pomocat.tcss` 配色

對齊教學 PPT 的 Midnight Executive：

```css
$primary: #1E2761;       /* navy */
$accent: #D97757;        /* coral */
$work: #D97757;          /* WORK phase */
$short-break: #7FB069;   /* mint */
$long-break: #9B7EBD;    /* lavender */
```

## 6. CLI（cli.py）

```python
import typer
app = typer.Typer(no_args_is_help=False)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        start(task=None)

@app.command()
def start(task: str = typer.Argument(None)):
    PomocatApp(initial_task=task).run()

@app.command()
def stats(range: str = typer.Option("week", "--range", "-r")):
    PomocatApp(initial_screen="stats", stats_range=range).run()

@app.command()
def config():
    PomocatApp(initial_screen="config").run()
```

**指令矩陣**：

| 指令 | 行為 |
|---|---|
| `pomocat` | 等同 `pomocat start`（無 label） |
| `pomocat start` | 啟 TUI timer，無 label |
| `pomocat start "寫教材"` | 啟 TUI timer，label = 寫教材 |
| `pomocat stats` | 進 stats screen，預設週視圖 |
| `pomocat stats -r day` | 進 stats screen，當日視圖 |
| `pomocat stats -r month` | 進 stats screen，月視圖 |
| `pomocat stats -r {day,week,month}` 以外 | typer 報錯退出（透過 Enum 強制） |
| `pomocat config` | 進 config screen |

## 7. Sound（sound.py）

```python
import sys, subprocess
from importlib.resources import files, as_file

def play_alarm() -> None:
    if sys.platform != "darwin":
        print("\a", end="", flush=True)
        return
    wav = files("pomocat.assets") / "alarm.wav"
    with as_file(wav) as path:
        subprocess.Popen(
            ["afplay", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
```

**設計重點**：
- `Popen` 不 wait → 不卡 UI
- `importlib.resources` 取 wheel 內資產 → 不依賴 `__file__` 路徑
- 非 macOS 用 `\a` 終端 bell fallback

## 8. Storage（storage.py）

```python
DATA_DIR = Path.home() / ".pomocat"
ROUNDS_FILE = DATA_DIR / "rounds.jsonl"
CONFIG_FILE = DATA_DIR / "config.toml"

def append_round(r: Round) -> None: ...   # JSONL append
def load_rounds() -> list[Round]: ...      # 不存在回 []
```

**為什麼 JSONL**：
- Append-only，crash-safe（write 一行不會壞掉前面）
- 不需 read-modify-write，避免 race
- 可用 `tail -f ~/.pomocat/rounds.jsonl` 外部觀察

**Serialize 規則**：
- `datetime` → ISO 8601 字串（`.isoformat()`）
- `Phase` (StrEnum) → 直接 str
- `Round` → dict via `dataclasses.asdict()` + 上述兩個 hook
- Load 時逐行 `json.loads` 再用 `Round(**parsed_with_decoded_fields)` 還原
- 損壞行（parse error）跳過並 stderr 警告，不 crash

## 9. Packaging

### 9.1 `pyproject.toml`（關鍵段落）

```toml
[project]
name = "pomocat"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "textual>=0.80",
    "textual-plotext>=0.2.1",
    "typer>=0.12",
    "tomli-w>=1.0",
]

[project.scripts]
pomocat = "pomocat.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/pomocat"]

[tool.hatch.build.targets.wheel.force-include]
"src/pomocat/assets/alarm.wav" = "pomocat/assets/alarm.wav"

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
]
```

### 9.2 安裝/開發流程

```bash
# 開發
uv sync
uv run pomocat
uv run pytest

# 本地試裝
uv build
uv tool install dist/pomocat-0.1.0-py3-none-any.whl

# PyPI 發布後
uv tool install pomocat
uv tool upgrade pomocat
```

## 10. Testing

```
tests/
├── unit/
│   ├── test_timer.py         # tick / next_phase 各種 transition
│   ├── test_stats.py         # daily / weekly / monthly summary
│   ├── test_config.py        # default、load 不存在、roundtrip
│   └── test_storage.py       # append、load、tmp_path 隔離
├── integration/
│   ├── test_cli.py           # typer CliRunner，mock App.run
│   └── test_app_smoke.py     # textual pilot，confirm 開得起來+能 quit
└── conftest.py               # round_fixture、config_fixture
```

**測試紀律**：
- Core 層所有測試 < 10ms / case，不 sleep、不碰 I/O
- Storage 測試強制 `monkeypatch DATA_DIR` 到 `tmp_path`
- Sound 測試只 mock `sys.platform`、不真的播音
- UI 測試只做 smoke（app 開得起來、能 quit），**不**斷言文字座標或截圖

**目標覆蓋率**：core/ >= 90%，整體 >= 70%。

## 11. 開放問題 / 未來

- Linux 聲音支援（用 `paplay` / `aplay`）
- Notification 整合（macOS `osascript`）
- 自訂音檔（讓 user 替換 `~/.pomocat/alarm.wav`）
- Export stats 成 CSV
- `pomocat history --json` 給外部腳本接

以上四項都明確排除在 v0.1.0 範圍外。
