"""計分與選型的純 Python 測試（不需 cmake）。"""
import unittest

from helpers import REPO  # noqa: F401  (確保 repo 在 sys.path)
from workshop import b_metrics as M

EVENT = {"has_event": True, "event_start_s": 2, "t_true_45_s": 4}
NO_EVENT = {"has_event": False, "event_start_s": None, "t_true_45_s": None}


def rows(alarms, ys=None):
    ys = ys or [40.0] * len(alarms)
    return [{"t": t, "temp": 40.0, "y": y, "count": 0, "alarm": a} for t, (a, y) in enumerate(zip(alarms, ys))]


class ScoreTest(unittest.TestCase):
    def test_false_alarms_count_transitions_not_rows(self):
        m = M.score(rows([0, 1, 1, 1, 0, 1, 1]), {t: 40.0 for t in range(7)}, NO_EVENT)
        self.assertEqual(m["false_alarms"], 2)
        self.assertIsNone(m["missed"])

    def test_missed_event_latency_is_null_not_zero(self):
        m = M.score(rows([0] * 8), {t: 40.0 for t in range(8)}, EVENT)
        self.assertEqual(m["missed"], 1)
        self.assertIsNone(m["detection_latency_s"])
        self.assertIsNone(m["false_alarms"])

    def test_latency_and_early_alert(self):
        late = M.score(rows([0, 0, 0, 0, 0, 0, 1, 1]), {t: 40.0 for t in range(8)}, EVENT)
        self.assertEqual((late["detection_latency_s"], late["early_alert"]), (2, 0))
        early = M.score(rows([0, 0, 0, 1, 1, 1, 1, 1]), {t: 40.0 for t in range(8)}, EVENT)
        self.assertEqual((early["detection_latency_s"], early["early_alert"]), (-1, 1))

    def test_onset_before_event_start_is_ignored_for_detection(self):
        m = M.score(rows([1, 0, 0, 0, 0, 0, 0, 0]), {t: 40.0 for t in range(8)}, EVENT)
        self.assertEqual(m["missed"], 1)

    def test_mae_excludes_missing_and_reports_coverage(self):
        m = M.score(rows([0, 0, 0, 0], ys=[41.0, None, 39.0, None]), {t: 40.0 for t in range(4)}, NO_EVENT)
        self.assertAlmostEqual(m["mae_c"], 1.0)
        self.assertAlmostEqual(m["coverage"], 0.5)


def metric_rows(spec):
    """spec: {cand: (false_alarms, missed, latency, mae)}；latency < 0 視為提早告警"""
    out = []
    for c, (fa, ms, lat, mae) in spec.items():
        out.append({"split": "eval", "candidate": c, "scenario": "rise", "metric": "early_alert",
                    "value": "" if lat is None else str(int(lat < 0))})
        out += [{"split": "eval", "candidate": c, "scenario": "spike", "metric": "false_alarms", "value": str(fa)},
                {"split": "eval", "candidate": c, "scenario": "rise", "metric": "missed", "value": str(ms)},
                {"split": "eval", "candidate": c, "scenario": "rise", "metric": "detection_latency_s",
                 "value": "" if lat is None else str(lat)},
                {"split": "eval", "candidate": c, "scenario": "rise", "metric": "mae_c", "value": str(mae)}]
    return out


class SelectTest(unittest.TestCase):
    def test_no_candidate_passes(self):
        s = M.select(metric_rows({"a": (1, 0, 3, 0.2), "b": (0, 1, None, 0.2)}), ["a", "b"])
        self.assertEqual(s["passed"], [])
        self.assertIn("無候選通過", s["verdict"])

    def test_single_pass(self):
        s = M.select(metric_rows({"a": (1, 0, 3, 0.2), "b": (0, 0, 4, 0.2)}), ["a", "b"])
        self.assertEqual(s["passed"], ["b"])

    def test_tie_lists_tradeoffs_without_champion(self):
        s = M.select(metric_rows({"a": (0, 0, 4, 0.20), "b": (0, 0, 5, 0.22)}), ["a", "b"])
        self.assertIn("差異不足", s["verdict"])

    def test_clear_difference_is_observation_only(self):
        s = M.select(metric_rows({"a": (0, 0, 3, 0.2), "b": (0, 0, 8, 0.2)}), ["a", "b"])
        self.assertIn("僅列為觀察", s["verdict"])

    def test_early_alert_is_not_counted_as_fastest(self):
        s = M.select(metric_rows({"a": (0, 0, -5, 0.2), "b": (0, 0, 3, 0.2)}), ["a", "b"])
        self.assertIn("b 平均延遲最短", s["verdict"])
        self.assertIn("a 有 1 次提早告警", s["verdict"])
        self.assertIsNone(s["summary"]["a"]["mean_latency_s"])


if __name__ == "__main__":
    unittest.main()
