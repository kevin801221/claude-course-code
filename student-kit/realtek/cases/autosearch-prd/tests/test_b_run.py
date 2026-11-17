"""B 端到端：A2 重跑一致、A3 同輸入同告警器且指標可由逐筆結果重算、缺測不冒充 0。"""
import csv
import unittest

from helpers import REPO, b_run, cli, needs_cmake, read_json, sha, tmpdir

SCEN = ["stable", "noise", "spike", "sustained_rise", "missing"]
CANDS = ["sma", "ema", "median"]


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


@needs_cmake
class BRunTest(unittest.TestCase):
    def test_outputs_and_evidence(self):
        d = b_run()
        for f in ("sources.json", "protocol.json", "metrics.csv", "perf.json", "run.log", "evidence.json",
                  "research-report.md", "handoff-a.md"):
            self.assertTrue((d / f).is_file(), f)
        ev = read_json(d / "evidence.json")
        self.assertEqual((ev["status"], ev["dataset_kind"]), ("succeeded", "synthetic"))
        self.assertEqual(ev["protocol_sha256"], sha(d / "protocol.json"))
        for a in ev["artifacts"]:
            self.assertEqual(sha(d / a["path"]), a["sha256"], a["path"])
        self.assertIn("執行狀態：成功", (d / "handoff-a.md").read_text(encoding="utf-8"))

    def test_rerun_reproducible(self):  # A2
        d1 = b_run()
        d2 = tmpdir() / "b2"
        p = cli("b", "run", "--offline", "--out", d2)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(sha(d1 / "metrics.csv"), sha(d2 / "metrics.csv"))
        self.assertEqual(sha(d1 / "protocol.json"), sha(d2 / "protocol.json"))
        for split in ("dev", "eval"):
            for s in SCEN:
                for c in CANDS:
                    rel = f"rows/{split}/{s}/{c}.csv"
                    self.assertEqual(sha(d1 / rel), sha(d2 / rel), rel)
        e1, e2 = read_json(d1 / "evidence.json"), read_json(d2 / "evidence.json")
        self.assertNotEqual(e1["run_id"], e2["run_id"])
        self.assertEqual([c["value"] for c in e1["claims"]], [c["value"] for c in e2["claims"]])

    def test_rows_recompute(self):  # A3
        d = b_run()
        metrics = {(r["split"], r["candidate"], r["scenario"], r["metric"]): r["value"] for r in read(d / "metrics.csv")}
        for split in ("dev", "eval"):
            for s in SCEN:
                raw = read(REPO / f"fixtures/b/{split}/{s}.raw.csv")
                truth = {r["timestamp_s"]: float(r["true_temp_c"]) for r in read(REPO / f"fixtures/b/{split}/{s}.truth.csv")}
                for c in CANDS:
                    rows = read(d / f"rows/{split}/{s}/{c}.csv")
                    # 同一份輸入
                    self.assertEqual([(r["timestamp_s"], r["temp_c"]) for r in rows],
                                     [(r["timestamp_s"], r["temp_c"]) for r in raw])
                    count, prev, onsets, errs = 0, 0, 0, []
                    for r in rows:
                        if r["temp_c"] == "":  # 缺測：輸出空值、不當 0、告警重置
                            self.assertEqual((r["filtered_c"], r["alarm"]), ("", "0"))
                        # 獨立重算共用告警器：≥45 連續 3 筆
                        count = count + 1 if r["filtered_c"] != "" and float(r["filtered_c"]) >= 45.0 else 0
                        alarm = 1 if count >= 3 else 0
                        self.assertEqual(alarm, int(r["alarm"]), f"{split}/{s}/{c} t={r['timestamp_s']}")
                        onsets += alarm and not prev
                        prev = alarm
                        if r["filtered_c"] != "":
                            errs.append(abs(float(r["filtered_c"]) - truth[r["timestamp_s"]]))
                    self.assertEqual(str(onsets), metrics[(split, c, s, "onset_count")])
                    self.assertAlmostEqual(sum(errs) / len(errs), float(metrics[(split, c, s, "mae_c")]), places=6)


if __name__ == "__main__":
    unittest.main()
