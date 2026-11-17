"""C：A4 無 B／壞包、A5 REQ 追回 metrics 原始列、A6 變更流程。"""
import csv
import os
import shutil
import unittest

from helpers import (REPO, b_run, cli, copy_b_run, needs_cmake, read_json, reseal, sha, tmpdir,
                     write_json)

FEEDBACK = REPO / "fixtures/c/feedback.json"


def draft(research=None):
    out = tmpdir() / "proj"
    args = ["c", "draft", "--offline", "--out", out] + (["--research", research] if research else [])
    p = cli(*args)
    assert p.returncode == 0, p.stdout + p.stderr
    return out, p


def req(project, rid, version="v1"):
    return next(r for r in read_json(project / f"versions/{version}/requirements.json")["requirements"] if r["id"] == rid)


def version_hashes(project, v="v1"):
    d = project / "versions" / v
    return {f.name: sha(f) for f in sorted(d.iterdir())}


class StandaloneTest(unittest.TestCase):
    def test_standalone_draft_marks_pending_and_passes_review(self):  # A4（無 B）
        proj, _ = draft()
        r4 = req(proj, "REQ-004")
        self.assertFalse(r4.get("reference_values"))
        self.assertIsNone(r4["target"]["value"])
        prd = (proj / "versions/v1/prd.md").read_text(encoding="utf-8")
        self.assertIn("研究參考值：待驗證", prd)
        for f in ("prd.md", "sow.md", "traceability.md", "open-questions.md"):
            self.assertTrue((proj / "versions/v1" / f).is_file())
        p = cli("c", "review", "--project", proj)
        self.assertEqual(p.returncode, 0, p.stdout)
        rv = read_json(proj / "review.json")
        self.assertEqual(rv["semantic_review"]["status"], "not_run")
        self.assertIn("語意審查未執行", (proj / "review.md").read_text(encoding="utf-8"))


@needs_cmake
class BrokenPackTest(unittest.TestCase):
    def _assert_withdrawn(self, research):
        proj, p = draft(research)
        self.assertIn("警示", p.stderr)
        self.assertEqual(read_json(proj / "project.json")["b_package"]["status"], "invalid")
        evs = read_json(proj / "versions/v1/evidence.json")["evidence"]
        self.assertFalse([e for e in evs if e["evidence_kind"] == "b_measurement"])
        self.assertFalse(req(proj, "REQ-004").get("reference_values"))
        self.assertIn("待驗證", (proj / "versions/v1/prd.md").read_text(encoding="utf-8"))
        self.assertEqual(cli("c", "review", "--project", proj).returncode, 0)
        return proj

    def test_missing_pack(self):
        self._assert_withdrawn(tmpdir() / "nope" / "evidence.json")

    def test_failed_status(self):
        d = copy_b_run()
        ev = read_json(d / "evidence.json")
        ev["status"] = "failed"
        write_json(d / "evidence.json", ev)
        self._assert_withdrawn(d / "evidence.json")

    def test_tampered_metrics(self):
        d = copy_b_run()
        text = (d / "metrics.csv").read_text(encoding="utf-8")
        (d / "metrics.csv").write_text(text.replace("detection_latency_s,5,s", "detection_latency_s,1,s", 1), encoding="utf-8")
        self._assert_withdrawn(d / "evidence.json")

    def test_path_escape(self):
        d = copy_b_run()
        ev = read_json(d / "evidence.json")
        ev["artifacts"][0]["path"] = "../outside.txt"
        write_json(d / "evidence.json", ev)
        self._assert_withdrawn(d / "evidence.json")

    def test_symlinked_artifact(self):
        d = copy_b_run()
        outside = tmpdir() / "metrics.csv"
        shutil.copy(d / "metrics.csv", outside)
        (d / "metrics.csv").unlink()
        os.symlink(outside, d / "metrics.csv")
        self._assert_withdrawn(d / "evidence.json")

    def test_review_rechecks_pack_after_draft(self):
        d = copy_b_run()
        proj, _ = draft(d / "evidence.json")
        self.assertEqual(cli("c", "review", "--project", proj).returncode, 0)
        with open(d / "metrics.csv", "a", encoding="utf-8") as f:
            f.write("tampered\n")
        p = cli("c", "review", "--project", proj)
        self.assertEqual(p.returncode, 1)
        self.assertIn("B 證據包目前無效", p.stdout)

    def test_number_claimed_without_valid_pack_fails_review(self):
        proj, _ = draft(tmpdir() / "nope" / "evidence.json")
        rq = read_json(proj / "versions/v1/requirements.json")
        for r in rq["requirements"]:
            if r["id"] == "REQ-004":
                r["reference_values"] = [{"evidence_id": "B-E041", "value": 5, "unit": "s", "run_id": "x",
                                          "scenario": "sustained_rise", "metric": "detection_latency_s", "basis": "手填"}]
        write_json(proj / "versions/v1/requirements.json", rq)
        reseal(proj)
        p = cli("c", "review", "--project", proj)
        self.assertEqual(p.returncode, 1)
        self.assertIn("仍宣稱 B-E041", p.stdout)


@needs_cmake
class TraceTest(unittest.TestCase):
    def test_trace_req_to_metrics_row(self):  # A5
        bdir = b_run()
        proj, _ = draft(bdir / "evidence.json")
        bev = read_json(bdir / "evidence.json")
        r4 = req(proj, "REQ-004")
        self.assertIsNone(r4["target"]["value"])                  # 研究值不變成產品門檻
        ref = r4["reference_values"][0]
        self.assertIn(ref["evidence_id"], r4["evidence_ids"])
        ev = {e["evidence_id"]: e for e in read_json(proj / "versions/v1/evidence.json")["evidence"]}[ref["evidence_id"]]
        tr = ev["b_trace"]
        self.assertEqual(tr["run_id"], bev["run_id"])
        self.assertEqual(tr["artifact_sha256"], sha(bdir / tr["artifact_path"]))
        with open(bdir / tr["artifact_path"], encoding="utf-8", newline="") as f:
            lines = list(csv.reader(f))
        row = dict(zip(lines[0], lines[tr["metrics_line"] - 1]))
        want = dict(kv.split("=") for kv in tr["row_locator"].split(";"))
        self.assertEqual({k: row[k] for k in want}, want)
        self.assertEqual(float(row["value"]), ref["value"])
        self.assertIn("合成", tr["limitations"])
        self.assertIn(bev["run_id"], (proj / "versions/v1/traceability.md").read_text(encoding="utf-8"))


class ChangeFlowTest(unittest.TestCase):
    def test_change_flow(self):  # A6
        proj, _ = draft()
        v1 = version_hashes(proj)
        self.assertEqual(cli("c", "change", "--project", proj, "--feedback", FEEDBACK).returncode, 0)
        cr1 = read_json(proj / "changes/CR-001.json")
        self.assertEqual((cr1["status"], cr1["base_version"]), ("proposed", "v1"))
        self.assertIn("REQ-001", cr1["affected_requirements"])
        self.assertEqual(cr1["new_acceptance"], ["AT-007", "AT-008"])
        self.assertEqual(version_hashes(proj), v1)                                   # 產生提案不改版本
        self.assertEqual(cli("c", "review", "--project", proj).returncode, 0)       # 待決 CR 不影響檢核

        self.assertEqual(cli("c", "apply", "--project", proj, "--cr", "CR-001", "--decision", "reject").returncode, 0)
        self.assertEqual(read_json(proj / "changes/CR-001.json")["status"], "rejected")
        self.assertFalse((proj / "versions/v2").exists())

        cli("c", "change", "--project", proj, "--feedback", FEEDBACK)               # CR-002
        self.assertEqual(cli("c", "apply", "--project", proj, "--cr", "CR-002", "--decision", "defer").returncode, 0)
        self.assertFalse((proj / "versions/v2").exists())
        cli("c", "change", "--project", proj, "--feedback", FEEDBACK)               # CR-003

        p = cli("c", "apply", "--project", proj, "--cr", "CR-003", "--decision", "accept")
        self.assertEqual(p.returncode, 0, p.stderr)
        pj = read_json(proj / "project.json")
        self.assertEqual(pj["current_version"], "v2")
        self.assertEqual(version_hashes(proj), v1)                                   # 前版保留不變
        self.assertEqual(req(proj, "REQ-005", "v2")["approved_via"], "CR-003")
        self.assertEqual(cli("c", "review", "--project", proj).returncode, 0)

        p = cli("c", "apply", "--project", proj, "--cr", "CR-002", "--decision", "accept")
        self.assertEqual(p.returncode, 1)                                           # 過期基準拒絕
        self.assertIn("過期提案", p.stderr)
        self.assertFalse((proj / "versions/v3").exists())
        decisions = (proj / "decisions.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(decisions), 4)


if __name__ == "__main__":
    unittest.main()
