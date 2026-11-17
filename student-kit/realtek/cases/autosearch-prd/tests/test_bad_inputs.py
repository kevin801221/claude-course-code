"""A7 刻意壞資料：重複 ID、遺失來源、缺驗收、竄改已確認版本、壞 CSV、建置失敗。"""
import os
import shutil
import subprocess
import time
import unittest

from helpers import REPO, cli, needs_cmake, read_json, reseal, tmpdir, write_json


def project():
    out = tmpdir() / "proj"
    assert cli("c", "draft", "--offline", "--out", out).returncode == 0
    return out


def mutate(proj, fname, fn, seal=True):
    path = proj / "versions/v1" / fname
    data = read_json(path)
    fn(data)
    write_json(path, data)
    if seal:
        reseal(proj)


class BadCDataTest(unittest.TestCase):
    def assert_review_fails(self, proj, msg):
        p = cli("c", "review", "--project", proj)
        self.assertEqual(p.returncode, 1, p.stdout)
        self.assertIn(msg, p.stdout)
        self.assertFalse(read_json(proj / "review.json")["structural_ok"])

    def test_duplicate_req_id(self):
        proj = project()
        mutate(proj, "requirements.json", lambda d: d["requirements"].append(dict(d["requirements"][0])))
        self.assert_review_fails(proj, "需求 ID重複：REQ-001")

    def test_missing_evidence_source(self):
        proj = project()
        mutate(proj, "requirements.json", lambda d: d["requirements"][1]["evidence_ids"].append("EV-999"))
        self.assert_review_fails(proj, "引用的證據不存在：EV-999")

    def test_requirement_without_evidence(self):
        proj = project()
        mutate(proj, "requirements.json", lambda d: d["requirements"][3].update(evidence_ids=[]))
        self.assert_review_fails(proj, "有效需求沒有任何可追溯的證據來源")

    def test_corrupted_project_json_gives_clear_error(self):
        proj = project()
        (proj / "versions/v1/requirements.json").write_text("{ not json", encoding="utf-8")
        p = cli("c", "review", "--project", proj)
        self.assertEqual(p.returncode, 1)
        self.assertIn("錯誤：", p.stderr)
        self.assertNotIn("Traceback", p.stderr)

    def test_arxiv_query_requires_online(self):
        out = tmpdir() / "b"
        p = cli("b", "run", "--offline", "--arxiv-query", "x", "--out", out)
        self.assertEqual(p.returncode, 2)
        self.assertFalse(out.exists())

    def test_missing_acceptance(self):
        proj = project()
        mutate(proj, "requirements.json", lambda d: d["requirements"][2].update(acceptance_ids=[]))
        self.assert_review_fails(proj, "有效需求沒有任何驗收")

    def test_approved_only_on_unresolved_evidence(self):
        proj = project()
        mutate(proj, "requirements.json", lambda d: d["requirements"][1].update(evidence_ids=["EV-003"]))
        self.assert_review_fails(proj, "只依賴 unresolved")

    def test_research_number_as_product_target(self):
        proj = project()
        mutate(proj, "requirements.json", lambda d: d["requirements"][3]["target"].update(value=5))
        self.assert_review_fails(proj, "研究測量不能直接寫成產品門檻")

    def test_unknown_unit(self):
        proj = project()
        mutate(proj, "requirements.json", lambda d: d["requirements"][3]["target"].update(unit="ms"))
        self.assert_review_fails(proj, "單位「ms」不在詞彙表")

    def test_baseline_tampered_without_reseal(self):
        proj = project()
        mutate(proj, "acceptance.json", lambda d: d["acceptance"].pop(), seal=False)
        self.assert_review_fails(proj, "已確認的版本被改動")

    def test_acceptance_cannot_claim_passed(self):
        proj = project()
        mutate(proj, "acceptance.json", lambda d: d["acceptance"][0].update(status="passed"))
        self.assert_review_fails(proj, "不在 ['not_run']")

    def test_missing_section(self):
        proj = project()
        prd = proj / "versions/v1/prd.md"
        prd.write_text(prd.read_text(encoding="utf-8").replace("## 4. 假設", "## 4. 其他"), encoding="utf-8")
        self.assert_review_fails(proj, "缺少必填章節：假設")

    def test_existing_out_dir_refused(self):
        proj = project()
        p = cli("c", "draft", "--offline", "--out", proj)
        self.assertEqual(p.returncode, 2)
        self.assertIn("輸出目錄已存在", p.stderr)


@needs_cmake
class BadBDataTest(unittest.TestCase):
    def assert_failed_run(self, out, p, msg):
        self.assertNotEqual(p.returncode, 0)
        self.assertFalse((out / "research-report.md").exists())
        ev = read_json(out / "evidence.json")
        self.assertEqual((ev["status"], ev["claims"]), ("failed", []))
        self.assertIn("執行狀態：失敗", (out / "handoff-a.md").read_text(encoding="utf-8"))
        self.assertIn(msg, (out / "run.log").read_text(encoding="utf-8"))

    def test_build_failure_does_not_use_stale_binary(self):
        src, build = tmpdir() / "src", tmpdir() / "build"
        shutil.copytree(REPO / "b_research", src)
        for cmd in (["cmake", "-S", src, "-B", build, "-DCMAKE_BUILD_TYPE=Release"], ["cmake", "--build", build]):
            subprocess.run(list(map(str, cmd)), check=True, capture_output=True)
        self.assertTrue((build / "wb_filter").is_file())          # 先留下一個可用的舊 binary
        with open(src / "src/main.cpp", "a", encoding="utf-8") as f:
            f.write("\nthis is not C++;\n")
        # make 在 macOS 只有秒級 mtime：同一秒內的修改會被當成「已是最新」。把修改時間往後推，模擬事後才改原始碼。
        later = time.time() + 5
        os.utime(src / "src/main.cpp", (later, later))
        out = tmpdir() / "b"
        p = cli("b", "run", "--offline", "--out", out, "--src", src, "--build-dir", build)
        self.assert_failed_run(out, p, "C++ 建置失敗")
        self.assertFalse((out / "rows").exists())                 # 沒有用舊 binary 跑任何資料

    def test_bad_csv(self):
        fx = tmpdir() / "fx"
        shutil.copytree(REPO / "fixtures/b", fx)
        f = fx / "eval/stable.raw.csv"
        f.write_text(f.read_text(encoding="utf-8").replace("\n5,", "\n4,", 1), encoding="utf-8")
        out = tmpdir() / "b"
        p = cli("b", "run", "--offline", "--out", out, "--fixtures", fx)
        self.assert_failed_run(out, p, "嚴格遞增")

    def test_missing_temp_column(self):
        fx = tmpdir() / "fx"
        shutil.copytree(REPO / "fixtures/b", fx)
        f = fx / "dev/noise.raw.csv"
        f.write_text(f.read_text(encoding="utf-8").replace("timestamp_s,temp_c", "timestamp_s,temperature", 1), encoding="utf-8")
        out = tmpdir() / "b"
        p = cli("b", "run", "--offline", "--out", out, "--fixtures", fx)
        self.assert_failed_run(out, p, "缺少欄位：temp_c")


if __name__ == "__main__":
    unittest.main()
