"""來源登錄（arXiv parser、去重、skipped）、合成資料可重生、schema 範例。"""
import subprocess
import sys
import unittest

from helpers import REPO, read_json, sha, tmpdir
from workshop import b_sources
from workshop.util import WorkshopError, check_schema


class SourcesTest(unittest.TestCase):
    def test_parse_arxiv_sample_and_dedupe_by_doi(self):
        xml = (REPO / "fixtures/b/arxiv_sample.xml").read_text(encoding="utf-8")
        recs = b_sources.parse_arxiv_atom(xml, "2026-11-16T00:00:00Z")
        self.assertEqual(len(recs), 3)
        self.assertEqual(recs[0]["title"], "Synthetic Paper on Median Filtering")
        self.assertEqual(recs[0]["access_level"], "abstract_only")
        kept, dups = b_sources.dedupe(recs)
        self.assertEqual(len(kept), 2)                       # DOI 大小寫不同仍視為同一篇
        self.assertTrue(dups[0]["key"].startswith("doi:"))

    def test_rejects_dtd(self):
        with self.assertRaises(WorkshopError):
            b_sources.parse_arxiv_atom('<!DOCTYPE x [<!ENTITY a "b">]><feed/>', "now")

    def test_offline_collect_records_skipped_and_dedupes_arxiv_versions(self):
        out = b_sources.collect(REPO / "fixtures/b", False, [], None, lambda m: None)
        ids = [s["source_id"] for s in out["sources"]]
        self.assertNotIn("SYN-ARXIV-001-DUP", ids)
        self.assertEqual(out["duplicates_removed"][0]["duplicate_of"], "SYN-ARXIV-001")
        self.assertEqual(out["skipped"][0]["source_id"], "SYN-IEEE-002")
        self.assertTrue(all(s["access_level"] == "synthetic" for s in out["sources"]))

    def test_report_source_summary_follows_actual_sources(self):
        from workshop.b_run import _source_summary
        offline = {"mode": "offline", "sources": [{"source_id": "S1", "access_level": "synthetic"}], "skipped": []}
        self.assertIn("全為教案合成", _source_summary(offline))
        self.assertIn("未執行", _source_summary(offline))
        online = {"mode": "online", "skipped": [{"source_id": "arxiv-query:q", "reason": "timeout"}],
                  "sources": [{"source_id": "S1", "access_level": "synthetic"},
                              {"source_id": "U1", "access_level": "user_supplied"}]}
        txt = _source_summary(online)
        self.assertNotIn("全為教案合成", txt)
        self.assertIn("取得 0 筆摘要、1 個查詢失敗", txt)


class FixturesTest(unittest.TestCase):
    def test_generated_data_reproducible(self):
        d = tmpdir()
        subprocess.run([sys.executable, str(REPO / "fixtures/b/generate_data.py"), "--out", str(d)], check=True)
        for f in sorted((REPO / "fixtures/b").glob("*/*.*")):
            if f.parent.name in ("dev", "eval"):
                self.assertEqual(sha(f), sha(d / f.parent.name / f.name), f.name)

    def test_schema_examples_and_seeds_validate(self):
        for ex in sorted((REPO / "schemas/examples").glob("*.example.json")):
            self.assertEqual(check_schema(read_json(ex), ex.name.split(".")[0]), [], ex.name)
        for name, f in (("requirements", "requirements.seed.json"), ("acceptance", "acceptance.seed.json"),
                        ("c-evidence", "evidence.json")):
            self.assertEqual(check_schema(read_json(REPO / "fixtures/c" / f), name), [], f)


if __name__ == "__main__":
    unittest.main()
