from pathlib import Path

from check_links import external_urls
from check_markdown_prose import frozen_student_snapshot, markdown_prose


def test_real_markdown_targets_are_distinct_from_examples():
    text = """[目錄](https://example.org/流程圖) [repo](https://github.com/example/tool_)
[`source.md`](https://example.org/walkthrough.md) https://example.net/notes.
`https://in-code.test`
````markdown
```sh
https://also-code.test
```
````
~~~sh
curl https://in-shell.test
~~~
"""
    assert external_urls(text) == {
        "https://example.org/%E6%B5%81%E7%A8%8B%E5%9C%96",
        "https://github.com/example/tool_",
        "https://example.org/walkthrough.md",
        "https://example.net/notes",
    }


def test_inner_fence_cannot_close_longer_outer_fence():
    prose, open_fence = markdown_prose("````markdown\n```sh\n\n```\n")
    assert not prose
    assert open_fence


def test_new_file_under_student_sources_is_checked(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    manifest = Path("student-kit/sources")
    manifest.mkdir(parents=True)
    (manifest / "manifest.json").write_text('{"files":[]}')
    (manifest / "full-manifest.json").write_text(
        '{"files":[{"destination":"course/pinned.md"}]}'
    )
    assert frozen_student_snapshot(Path("student-kit/course/pinned.md"))
    assert not frozen_student_snapshot(Path("student-kit/course/new.md"))
