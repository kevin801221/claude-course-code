import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import batch_ingest  # noqa: E402


class BatchIngestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root_dir = Path(__file__).parent.parent

    def test_discover_pending_raw_files_skips_processed_and_cross_summary(self) -> None:
        processed = {
            "2023-10-27_財經_Podcast_財經_Podcast_EPXXX.json",
            "2026-02-12_游庭皓的財經皓角__市場觀察_2026_台灣人如何迎接_少子化海嘯_.json",
            "2026-02-13_游庭皓的財經皓角__市場觀察_2026台灣人如何_迎接AI時代_.json",
        }
        files = batch_ingest.discover_pending_raw_files(self.root_dir, processed=processed)
        names = [path.name for path in files]

        self.assertEqual(len(names), 23)
        self.assertNotIn("2023-10-27_財經_Podcast_財經_Podcast_EPXXX.json", names)
        self.assertNotIn("2026-02-12_游庭皓的財經皓角__市場觀察_2026_台灣人如何迎接_少子化海嘯_.json", names)
        self.assertNotIn("2026-02-13_游庭皓的財經皓角__市場觀察_2026台灣人如何_迎接AI時代_.json", names)
        self.assertNotIn("_cross_summary.json", names)
        self.assertIn("2026-04-04_Gooaye_股癌_EP650____.json", names)

    def test_extract_entities_and_concepts_maps_keywords_to_canonical_pages(self) -> None:
        title = "【理財達人秀】川普變驚嚇 先蹲跳更高 壓不住 鎖低軌、封測、CPO"
        insight = {
            "type": "strategy",
            "tickers": ["2330.TW", "NVDA.US"],
            "content": "川普關稅與伊朗風險讓市場波動加劇，但 CPO、CoWoS、HBM、PCB 仍是觀察重點，建議用 ETF 與正二做資產配置。",
            "key_points": ["聚焦低軌衛星", "台積電與輝達仍是核心"],
        }

        entities, concepts = batch_ingest.extract_entities_and_concepts(title, insight)

        self.assertIn("川普", entities)
        self.assertIn("台積電", entities)
        self.assertIn("NVIDIA", entities)
        self.assertIn("CPO", entities)
        self.assertIn("CoWoS", entities)
        self.assertIn("HBM", entities)
        self.assertIn("川普關稅", entities)

        self.assertIn("地緣政治與市場波動", concepts)
        self.assertIn("CPO 與矽光子", concepts)
        self.assertIn("先進封裝與封測供應鏈", concepts)
        self.assertIn("記憶體與 HBM 週期", concepts)
        self.assertIn("PCB 與 CCL 供應鏈", concepts)
        self.assertIn("ETF 資產配置與槓桿策略", concepts)

    def test_build_source_page_metadata_uses_episode_as_title(self) -> None:
        payload = {
            "episode": "EP650 | 🦄",
            "podcast_name": "Gooaye 股癌",
            "date": "2026-04-04",
            "insights": [
                {
                    "type": "macro",
                    "tickers": [],
                    "content": "近期市場波動大，美股比台股更難操作。",
                    "key_points": ["市場波動大"],
                }
            ],
        }

        source = batch_ingest.build_source_record(
            file_name="2026-04-04_Gooaye_股癌_EP650____.json",
            payload=payload,
        )

        self.assertEqual(source["title"], "EP650 | 🦄")
        self.assertIn("近期市場波動大", source["summary"])
        self.assertIn("2026-04-04_Gooaye_股癌_EP650____.json", source["sources"])


if __name__ == "__main__":
    unittest.main()
