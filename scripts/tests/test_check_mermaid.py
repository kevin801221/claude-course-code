"""Regression tests for diagrams shown inside Markdown teaching examples."""

from check_mermaid import mermaid_blocks


def test_rendered_fences_and_quoted_diagram():
    text = "> ~~~mermaid\n> graph TD\n>   A --> B\n> ~~~\n"
    assert list(mermaid_blocks(text)) == ["graph TD\n  A --> B\n"]


def test_markdown_sample_does_not_become_an_independent_diagram():
    text = (
        "````markdown\n```mermaid\nsample text\n```\n````\n"
        "```mermaid\ngraph LR\n  A --> B\n```\n"
    )
    assert list(mermaid_blocks(text)) == ["graph LR\n  A --> B\n"]
