"""B 執行：建置 → 單元測試 → dev → 鎖協議 → eval → 效能 → 報告 → 證據包。"""
from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from . import b_metrics as M
from .b_sources import collect
from .util import (WorkshopError, check_schema, prepare_out_dir, new_run_id, read_json,
                   sha256_file, utc_now, write_json, write_text)

SPLITS = ["dev", "eval"]
SCENARIOS = ["stable", "noise", "spike", "sustained_rise", "missing"]
CANDIDATES = ["sma", "ema", "median"]
LIMITATIONS = ("合成資料（dataset_kind=synthetic；數值為本次實際輸出，不是編造）；單一固定種子、每情境 180 筆；"
               "教案預設參數，不是量產門檻；不代表目標硬體或真實設備表現。")


class Log:
    def __init__(self, path: Path):
        self.path = path

    def __call__(self, msg: str) -> None:
        line = f"[{utc_now()}] {msg}"
        print(line)
        with open(self.path, "a", encoding="utf-8", newline="\n") as f:
            f.write(line + "\n")


def _sh(cmd: list[str], log: Log, label: str) -> str:
    log(f"$ {' '.join(cmd)}")
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    for stream in (p.stdout, p.stderr):
        if stream.strip():
            with open(log.path, "a", encoding="utf-8", newline="\n") as f:
                f.write(stream.rstrip() + "\n")
    if p.returncode != 0:
        raise WorkshopError(f"{label}失敗（exit {p.returncode}）：{p.stderr.strip()[-300:]}（詳見 run.log）")
    return p.stdout


def build(src: Path, build_dir: Path, log: Log) -> Path:
    missing = [t for t in ("cmake", "ctest") if not shutil.which(t)]
    if missing:
        raise WorkshopError(f"找不到 {', '.join(missing)}。請先安裝 CMake ≥ 3.20 與 C++17 編譯器；本工具不自動安裝軟體。", code=2)
    _sh(["cmake", "-S", str(src), "-B", str(build_dir), "-DCMAKE_BUILD_TYPE=Release"], log, "CMake 設定")
    _sh(["cmake", "--build", str(build_dir), "--config", "Release"], log, "C++ 建置")
    _sh(["ctest", "--test-dir", str(build_dir), "-C", "Release", "--output-on-failure"], log, "C++ 單元測試")
    # 建置成功後才找 binary；建置失敗已在上面中止，不會誤用舊檔
    for exe in ("wb_filter", "wb_filter.exe"):
        for d in (build_dir, build_dir / "Release"):
            if (d / exe).is_file():
                return d / exe
    raise WorkshopError(f"建置完成但在 {build_dir} 找不到 wb_filter")


def make_protocol(fx: Path) -> dict:
    datasets = {}
    for split in SPLITS:
        datasets[split] = {}
        for s in SCENARIOS:
            files = {}
            for kind, suffix in (("raw", "raw.csv"), ("truth", "truth.csv"), ("events", "events.json")):
                p = fx / split / f"{s}.{suffix}"
                if not p.is_file():
                    raise WorkshopError(f"缺少資料檔：{p}")
                files[kind] = {"path": f"{split}/{s}.{suffix}", "sha256": sha256_file(p)}
            datasets[split][s] = files
    return {
        "schema_version": "1.0",
        "case": "設備溫度濾波與持續升溫告警（瑞昱工作坊教案合成案例）",
        "note": "教案預設，數值不是量產門檻；本協議在跑評估組前寫入並計算雜湊。",
        "dataset_kind": "synthetic",
        "input": {"columns": ["timestamp_s", "temp_c"], "rate_hz": 1,
                  "timestamps": "嚴格遞增、每秒一筆", "missing": "空值為缺測，不當 0"},
        "candidates": {"sma": {"window": 5}, "ema": {"alpha": 0.30, "init": "first_valid_sample"},
                       "median": {"window": 5, "even_count": "mean_of_middle_two"}},
        "filter_rules": [
            "SMA／Median 啟動期用實有、含當筆的樣本",
            "缺測：輸出空值、重置濾波器與連續告警計數；下一筆有效值重新初始化",
        ],
        "alarm": {"shared_by_all_candidates": True, "threshold_c": 45.0, "comparison": ">=", "consecutive": 3,
                  "trigger": "第 3 筆連續有效且 ≥ 門檻的濾波輸出觸發",
                  "reset": "低於門檻或缺值即重置計數",
                  "state": "alarm=1 當且僅當連續計數 ≥ 3",
                  "onset": "alarm 由 0 轉 1 的那一筆；不逐筆重複計數",
                  "isolated_spike": "教案定義為干擾，不應觸發"},
        "metrics": {
            "mae_c": "有效濾波輸出且有真值的列之 |濾波−真值| 平均（°C）",
            "coverage": "有效濾波輸出筆數 ÷ 有真值筆數",
            "onset_count": "alarm 0→1 次數",
            "false_alarms": "僅無事件情境：onset 次數",
            "missed": "僅事件情境：事件起點後沒有任何 onset 記 1",
            "detection_latency_s": "僅事件情境：事件起點後第一次 onset 時間 − 真值首達 45°C 時間（帶號）；missed 時為 null，不記 0",
            "early_alert": "僅事件情境：detection_latency_s < 0 記 1；缺測後的重新觸發只計入 onset_count，不算誤報",
        },
        "selection": {"order": ["先篩 eval 全情境 false_alarms=0 且 missed=0",
                                "通過者比較平均 detection_latency_s（只計 ≥ 0 的偵測；提早告警另列），再比平均 mae_c",
                                "執行時間只供同環境參考"],
                      "latency_tie_s": 1.0, "mae_tie_c": 0.05,
                      "no_pass": "寫「無候選通過」", "tie": "差異不足時列取捨，不硬挑冠軍"},
        "splits": {"dev": "開發組：冒煙檢查；若要調參只能用這組", "eval": "評估組：協議雜湊記錄後才執行"},
        "tuning": "未調參：參數皆為教案固定值。",
        "datasets": datasets,
        "build": {"cmake_build_type": "Release", "cxx_standard": 17, "same_binary_and_scorer_for_all_candidates": True},
        "perf": {"samples": 100000, "warmup": 3, "trials": 15, "input": "eval/sustained_rise.raw.csv 循環填滿",
                 "timer": "std::chrono::steady_clock", "scope": "只計濾波 step，不含檔案 I/O 與告警",
                 "statistic": "每樣本耗時中位數（ns）",
                 "note": "只供同一環境內參考；不作回歸 hard gate；不代表 MCU／晶片性能"},
    }


def _cpu() -> str:
    try:
        if sys.platform == "darwin":
            return subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
        if Path("/proc/cpuinfo").is_file():
            for line in Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="replace").splitlines():
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def _run_split(binary: Path, protocol: dict, fx: Path, out: Path, split: str, log: Log) -> list[list[str]]:
    a = protocol["alarm"]
    rows_out = []
    for s in SCENARIOS:
        ds = protocol["datasets"][split][s]
        truth = M.read_truth(fx / ds["truth"]["path"])
        ev = M.read_events(fx / ds["events"]["path"])
        for key in ("has_event", "event_start_s", "t_true_45_s"):
            if key not in ev:
                raise WorkshopError(f"事件標註缺少 {key}：{ds['events']['path']}")
        for c in CANDIDATES:
            p = protocol["candidates"][c]
            dst = out / "rows" / split / s / f"{c}.csv"
            dst.parent.mkdir(parents=True, exist_ok=True)
            _sh([str(binary), "run", "--method", c, "--in", str(fx / ds["raw"]["path"]), "--out", str(dst),
                 "--window", str(p.get("window", 5)), "--alpha", str(p.get("alpha", 0.3)),
                 "--threshold", str(a["threshold_c"]), "--consecutive", str(a["consecutive"])],
                log, f"{split}/{s}/{c} 執行")
            rows = M.read_rows(dst)
            if [r["t"] for r in rows] != sorted(truth):
                raise WorkshopError(f"{split}/{s}：真值與原始資料時間戳不一致")
            rows_out += M.to_rows(split, c, s, M.score(rows, truth, ev))
        log(f"{split}/{s} 完成（3 候選同輸入、同告警器、同計分程式）")
    return rows_out


def _fmt(v, nd=2):
    if v in (None, ""):
        return "—"
    s = str(v)
    return f"{float(s):.{nd}f}" if "." in s else s


def _report(run_id: str, out_label: str, brief: dict, sources: dict, protocol: dict, psha: str,
            metric_rows: list[dict], sel: dict, perf: dict) -> str:
    def get(split, c, s, m):
        for r in metric_rows:
            if (r["split"], r["candidate"], r["scenario"], r["metric"]) == (split, c, s, m):
                return r["value"]
        return ""

    L = [f"# B 研究報告：設備溫度濾波與持續升溫告警（合成資料）", "",
         f"- run_id：`{run_id}`　狀態：**成功**　產出：`{out_label}`",
         f"- protocol_sha256：`{psha}`　dataset_kind：`synthetic`",
         "- 這是瑞昱工作坊教案，不是瑞昱的產品、設備或已核准需求；數值不是量產門檻。", "",
         "## 1. 研究問題", "", brief["question"], "", "目標："]
    L += [f"- {g}" for g in brief["goals"]] + ["", "限制："] + [f"- {c}" for c in brief["constraints"]]
    L += ["", "## 2. 證據", "", f"{_source_summary(sources)}來源類別不同不代表證據強度相同。", "",
          "| 來源 | 類型 | 存取層級 | 主張 | 限制 |", "|---|---|---|---|---|"]
    L += [f"| {s['source_id']} | {s['kind']} | {s['access_level']} | {s['claim']} | {s['limitations']} |" for s in sources["sources"]]
    if sources["skipped"]:
        L += ["", "跳過（skipped）："] + [f"- {s['source_id']}：{s['reason']}" for s in sources["skipped"]]
    if sources.get("duplicates_removed"):
        L += ["", "去重："] + [f"- {d['source_id']} 與 {d['duplicate_of']} 重複（{d['key']}）" for d in sources["duplicates_removed"]]
    basis = {"source_claim": "有來源主張（合成來源）", "teaching_choice": "教案為了示範而選"}
    L += ["", "候選選用理由：", "", "| 候選 | 依據 | 來源 | 說明 |", "|---|---|---|---|"]
    L += [f"| {c['name']} | {basis.get(c['basis'], c['basis'])} | {', '.join(c['supporting_sources'])} | {c['rationale']} |"
          for c in brief["candidates"]]
    L += ["", "## 3. 測試方法", "",
          "- 三個候選用同一份輸入 CSV、同一個 Release binary、同一個告警器與同一個 Python 計分程式。",
          "- 告警：濾波輸出 ≥ 45°C 且連續 3 筆有效讀值，第 3 筆觸發；低於門檻或缺值即重置。",
          "- 缺測輸出空值並重置濾波器與計數，不當 0；SMA／Median 啟動期用實有樣本。",
          "- 開發組（dev, seed 101）與評估組（eval, seed 202）分開；協議在跑 eval 前寫入並雜湊；未調參。",
          "- 指標：MAE（另列 coverage）、無事件情境誤報次數（0→1 次數）、漏報、相對真值首達 45°C 的首次告警延遲（帶號；漏報為 null）、early_alert。",
          f"- 詳細定義見 `protocol.json`（sha256 `{psha[:16]}…`）。", "",
          "## 4. 實測結果（eval）", "",
          "| 情境 | 候選 | MAE °C | coverage | 誤報 | 漏報 | 延遲 s | 提早 |", "|---|---|---|---|---|---|---|---|"]
    for s in SCENARIOS:
        for c in CANDIDATES:
            g = lambda m: get("eval", c, s, m)
            L.append(f"| {s} | {c} | {_fmt(g('mae_c'), 3)} | {_fmt(g('coverage'), 3)} | {_fmt(g('false_alarms'))} | "
                     f"{_fmt(g('missed'))} | {_fmt(g('detection_latency_s'))} | {_fmt(g('early_alert'))} |")
    L += ["", "（— 表示該指標不適用於此情境，或漏報時延遲為 null。）", "",
          "## 5. 篩選與取捨", "",
          "| 候選 | 誤報合計 | 漏報合計 | 提早告警 | 平均延遲 s（不含提早） | 平均 MAE °C | 通過篩選 |", "|---|---|---|---|---|---|---|"]
    for c in CANDIDATES:
        x = sel["summary"][c]
        lat = "—" if x["mean_latency_s"] is None else f"{x['mean_latency_s']:.2f}"
        mae = "—" if x["mean_mae_c"] is None else f"{x['mean_mae_c']:.3f}"
        L.append(f"| {c} | {x['false_alarms']} | {x['missed']} | {x['early_alerts']} | {lat} | {mae} | "
                 f"{'是' if x['passed'] else '否'} |")
    L += ["", f"**結論：{sel['verdict']}**", "", "取捨（由實測資料逐項列出）："]
    for c in CANDIDATES:
        fa = [s for s in SCENARIOS if get("eval", c, s, "false_alarms") not in ("", "0")]
        lat = [f"{s} {get('eval', c, s, 'detection_latency_s') or 'null'} s" for s in ("sustained_rise", "missing")]
        L.append(f"- {c}：誤報情境 {', '.join(fa) if fa else '無'}；延遲 {', '.join(lat)}；"
                 f"noise MAE {_fmt(get('eval', c, 'noise', 'mae_c'), 3)} °C、spike MAE {_fmt(get('eval', c, 'spike', 'mae_c'), 3)} °C。")
    env = perf["env"]
    L += ["", "## 6. 效能（僅供本環境內參考）", "",
          f"環境：{env['cpu']}／{env['os']}／{env['compiler_id']} {env['compiler_version']}（{env['build_type']}，`{env['cxx_flags'].strip()}`）。",
          f"口徑：{protocol['perf']['scope']}；N={protocol['perf']['samples']}、暖機 {protocol['perf']['warmup']}、試次 {protocol['perf']['trials']}、{protocol['perf']['timer']}。",
          "不作回歸 hard gate，不代表 MCU／晶片性能。", "", "| 候選 | 每樣本 ns（中位數） | min | max |", "|---|---|---|---|"]
    L += [f"| {r['method']} | {r['ns_per_sample_median']:.2f} | {r['ns_per_sample_min']:.2f} | {r['ns_per_sample_max']:.2f} |" for r in perf["results"]]
    L += ["", "## 7. 開發組（dev）概況", "", "| 候選 | 誤報合計 | 漏報合計 |", "|---|---|---|"]
    dev = M.select(metric_rows, CANDIDATES, split="dev")
    L += [f"| {c} | {dev['summary'][c]['false_alarms']} | {dev['summary'][c]['missed']} |" for c in CANDIDATES]
    L += ["", "## 8. 未驗證事項", "",
          "- 只用合成資料；真實感測器噪聲、漂移、取樣抖動未驗證。",
          "- 未在目標硬體／MCU 上量測；耗時只代表本機教室環境。",
          "- 每情境只有一組種子；統計信心有限。",
          f"- 來源：{_source_summary(sources)}",
          "", "## 9. 下一步", "",
          "- 以實機記錄的 CSV（含真值或人工事件標註）重跑同一協議。",
          "- 增加多種子／多參數的敏感度分析（只用 dev 調參）。",
          "- 由 C 流程把延遲目標列為「待驗證」，待獨立決策證據後再定產品門檻。",
          "", "## 附錄：產物", "",
          "`sources.json`、`protocol.json`、`metrics.csv`、`perf.json`、`rows/<split>/<scenario>/<candidate>.csv`、`run.log`、`evidence.json`、`handoff-a.md`。"]
    return "\n".join(L) + "\n"


def _source_summary(sources: dict) -> str:
    """由實際寫出的 sources.json 推導，不由執行模式假設。"""
    levels = {}
    for s in sources["sources"]:
        levels[s["access_level"]] = levels.get(s["access_level"], 0) + 1
    if set(levels) == {"synthetic"}:
        txt = f"本次 {levels['synthetic']} 筆來源全為教案合成（synthetic），只示範登錄格式，不構成真實文獻支持；"
    else:
        txt = "本次來源存取層級：" + "、".join(f"{k} {v} 筆" for k, v in sorted(levels.items())) + "；合成來源只示範格式，摘要不等於全文；"
    if sources["mode"] == "online":
        got = sum(1 for s in sources["sources"] if s["source_id"].startswith("arxiv:"))
        bad = sum(1 for s in sources["skipped"] if s["source_id"].startswith("arxiv-query:"))
        txt += f"線上 arXiv 查詢取得 {got} 筆摘要、{bad} 個查詢失敗記為 skipped。"
    else:
        txt += "線上 arXiv 查詢未執行。"
    return txt


def _handoff(run_id: str, ok: bool, summary: str, report: str | None) -> str:
    return "\n".join([
        "# B → A 交接摘要（供日報／週報人工貼用）", "",
        f"- 日期：{utc_now()[:10]}",
        f"- run_id：{run_id}",
        f"- 執行狀態：{'成功' if ok else '失敗'}",
        f"- 摘要：{summary}",
        f"- 報告路徑：{report or '（失敗，未產生報告；見 run.log）'}", "",
        "> 本摘要不代替人工回報，未自動發布、未修改 A 的 Repo。", ""])


def _artifacts(out: Path) -> list[dict]:
    files = sorted(p for p in out.rglob("*") if p.is_file() and not p.is_symlink() and p.name != "evidence.json")
    return [{"path": p.relative_to(out).as_posix(), "sha256": sha256_file(p)} for p in files]


def run(args) -> int:
    if args.arxiv_query and not args.online:
        raise WorkshopError("--arxiv-query 需要搭配 --online（預設離線，不會連網）", code=2)
    run_id = new_run_id("b")
    out = prepare_out_dir(Path(args.out) if args.out else Path("outputs") / "b" / run_id)
    out_label = out.as_posix()
    log = Log(out / "run.log")
    psha = None
    try:
        fx = Path(args.fixtures)
        log(f"run_id={run_id} mode={'online' if args.online else 'offline'} out={out_label}")
        brief = read_json(fx / "brief.json")
        sources = collect(fx, args.online, args.arxiv_query or brief.get("queries", []), args.import_sources, log)
        write_json(out / "sources.json", sources)
        log(f"來源登錄：{len(sources['sources'])} 筆，skipped {len(sources['skipped'])} 筆")

        binary = build(Path(args.src), Path(args.build_dir), log)
        protocol = make_protocol(fx)
        write_json(out / "protocol.json", protocol)
        psha = sha256_file(out / "protocol.json")
        log(f"protocol_sha256={psha}")

        metric_rows = _run_split(binary, protocol, fx, out, "dev", log)
        log(f"dev 完成；協議雜湊 {psha[:16]}… 已鎖定，開始 eval")
        metric_rows += _run_split(binary, protocol, fx, out, "eval", log)
        M.write_csv(out / "metrics.csv", metric_rows)
        mrows = M.read_csv(out / "metrics.csv")
        sel = M.select(mrows, CANDIDATES, latency_tie_s=protocol["selection"]["latency_tie_s"],
                       mae_tie_c=protocol["selection"]["mae_tie_c"])

        pp = protocol["perf"]
        results = [json.loads(_sh([str(binary), "bench", "--method", c, "--in", str(fx / "eval" / "sustained_rise.raw.csv"),
                                   "--samples", str(pp["samples"]), "--warmup", str(pp["warmup"]), "--trials", str(pp["trials"]),
                                   "--window", str(protocol["candidates"][c].get("window", 5)),
                                   "--alpha", str(protocol["candidates"][c].get("alpha", 0.3))], log, f"{c} 效能量測"))
                   for c in CANDIDATES]
        info = json.loads(_sh([str(binary), "info"], log, "編譯資訊"))
        perf = {"run_id": run_id, "env": {**info, "cpu": _cpu(), "os": platform.platform(), "machine": platform.machine()},
                "method": pp, "results": results}
        write_json(out / "perf.json", perf)

        write_text(out / "research-report.md", _report(run_id, out_label, brief, sources, protocol, psha, mrows, sel, perf))
        write_text(out / "handoff-a.md", _handoff(run_id, True, f"SMA／EMA／Median 於 5 個合成情境實測；{sel['verdict']}",
                                                  f"{out_label}/research-report.md"))
        claims = []
        for r in mrows:
            if r["split"] != "eval" or r["value"] == "":
                continue
            claims.append({
                "evidence_id": f"B-E{len(claims) + 1:03d}",
                "statement": f"[合成資料] {r['candidate']} 於 eval/{r['scenario']}：{r['metric']} = {r['value']} {r['unit']}",
                "metric": r["metric"], "value": float(r["value"]), "unit": r["unit"], "scenario": r["scenario"],
                "candidate": r["candidate"], "split": r["split"], "artifact_path": "metrics.csv",
                "row_locator": f"split={r['split']};candidate={r['candidate']};scenario={r['scenario']};metric={r['metric']}",
                "limitations": LIMITATIONS,
            })
        log(f"完成：{sel['verdict']}")
        evidence = {"schema_version": "1.0", "run_id": run_id, "status": "succeeded", "dataset_kind": "synthetic",
                    "protocol_sha256": psha, "error": None, "artifacts": _artifacts(out), "claims": claims}
        errs = check_schema(evidence, "b-evidence")
        if errs:
            raise WorkshopError("證據包格式錯誤：" + "；".join(errs[:5]))
        write_json(out / "evidence.json", evidence)
        print(f"B 完成：{out_label}/research-report.md；證據包 {out_label}/evidence.json")
        return 0
    except Exception as e:  # 任何錯誤都不得產出看似成功的證據包
        code = e.code if isinstance(e, WorkshopError) else 1
        log(f"失敗：{e}")
        (out / "research-report.md").unlink(missing_ok=True)
        write_text(out / "handoff-a.md", _handoff(run_id, False, f"執行失敗：{e}", None))
        write_json(out / "evidence.json", {
            "schema_version": "1.0", "run_id": run_id, "status": "failed", "dataset_kind": "synthetic",
            "protocol_sha256": psha, "error": str(e), "artifacts": _artifacts(out), "claims": []})
        print(f"錯誤：B 執行失敗：{e}（log：{out_label}/run.log）", file=sys.stderr)
        return code or 1
