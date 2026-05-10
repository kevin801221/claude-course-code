import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import graph_builder  # noqa: E402


class GraphBuilderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.wiki_dir = Path(__file__).parent

    def test_collect_graph_builds_known_nodes_and_links(self) -> None:
        graph = graph_builder.collect_graph(self.wiki_dir)

        node_titles = {node["title"] for node in graph["nodes"]}
        self.assertIn("財經 Podcast EP.XXX", node_titles)
        self.assertIn("Agentic AI 與 CPU 投資主線", node_titles)
        self.assertIn("市場觀察 2026 台灣人如何迎接AI時代", node_titles)
        self.assertNotIn("某份文件摘要", node_titles)

        links = {
            (link["source"], link["target"])
            for link in graph["links"]
        }
        self.assertIn(("財經 Podcast EP.XXX", "Agentic AI 與 CPU 投資主線"), links)
        self.assertIn(("市場觀察 2026 台灣人如何迎接AI時代", "台積電"), links)

    def test_collect_graph_includes_raw_nodes_and_source_links(self) -> None:
        graph = graph_builder.collect_graph(self.wiki_dir)

        nodes = {node["title"]: node for node in graph["nodes"]}
        self.assertIn("raw/2023-10-27_財經_Podcast_財經_Podcast_EPXXX.json", nodes)
        self.assertEqual(nodes["raw/2023-10-27_財經_Podcast_財經_Podcast_EPXXX.json"]["type"], "raw")

        links = {
            (link["source"], link["target"])
            for link in graph["links"]
        }
        self.assertIn(
            ("raw/2023-10-27_財經_Podcast_財經_Podcast_EPXXX.json", "財經 Podcast EP.XXX"),
            links,
        )

    def test_collect_graph_keeps_abstract_knowledge_nodes(self) -> None:
        graph = graph_builder.collect_graph(self.wiki_dir)

        nodes = {node["title"]: node for node in graph["nodes"]}
        self.assertEqual(nodes["事件後應對投資法"]["type"], "concept")
        self.assertEqual(nodes["整體知識摘要"]["type"], "overview")
        self.assertIn("與其把精力放在預測事件何時發生", nodes["事件後應對投資法"]["summary"])

    def test_collect_graph_adds_summary_for_raw_and_wiki_nodes(self) -> None:
        graph = graph_builder.collect_graph(self.wiki_dir)

        nodes = {node["title"]: node for node in graph["nodes"]}
        source_summary = nodes["財經 Podcast EP.XXX"]["summary"]
        raw_summary = nodes["raw/2023-10-27_財經_Podcast_財經_Podcast_EPXXX.json"]["summary"]

        self.assertIn("這份來源整理了數個主題", source_summary)
        self.assertIn("財經 Podcast EP.XXX", raw_summary)
        self.assertIn("Kingyo捕蚊燈", raw_summary)

    def test_render_html_embeds_graph_data(self) -> None:
        graph = graph_builder.collect_graph(self.wiki_dir)
        html = graph_builder.render_html(graph)

        self.assertIn("LLM Wiki Graph", html)
        self.assertIn('"title": "台積電"', html)
        self.assertIn('"source": "財經 Podcast EP.XXX"', html)
        self.assertIn('"type": "raw"', html)
        self.assertIn("summary", html)
        self.assertIn("顯示 raw 節點", html)
        self.assertIn("間距", html)
        self.assertIn("spacing-value", html)
        self.assertIn("重新排版", html)
        self.assertIn("收斂後會自動停止", html)


if __name__ == "__main__":
    unittest.main()
