"""真實臨時 Git repo 的 JSON 回歸測試；不使用帳號、模型或網路。"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT / ".claude/skills/drafting-weekly-reports/scripts"
FETCH = SCRIPTS / "fetch_commits.sh"
AUTHOR = "kevin801221@users.noreply.github.com"


class FetchCommitsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="weekly-report-test-")
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.git("config", "user.name", "kevin801221")
        self.git("config", "user.email", AUTHOR)
        self.subject = 'fix: "quoted" \\ path 與繁中'
        self.body = 'line 1: "JSON" \\\nline 2: preserve\\slashes\n\nlast line\n'
        self.git("commit", "--allow-empty", "-q", "-m", self.subject + "\n\n" + self.body)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True).strip()

    def fetch(self, *args, env=None):
        return subprocess.run(
            ["bash", str(FETCH), "--since", "2020-01-01", *args],
            cwd=self.repo, env=env, capture_output=True, text=True,
        )

    def assert_payload(self, text):
        data = json.loads(text)
        self.assertEqual(data["period"], "2020-01-01")
        self.assertEqual(data["author"], AUTHOR)
        self.assertEqual(len(data["commits"]), 1)
        commit = data["commits"][0]
        self.assertEqual(commit["sha"], self.git("rev-parse", "HEAD"))
        self.assertEqual(commit["subject"], self.subject)
        self.assertEqual(commit["body"], self.body)
        return data

    def test_stdout_preserves_quotes_backslashes_and_newlines(self):
        result = self.fetch("--author", AUTHOR)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_payload(result.stdout)

    def test_output_file_preserves_same_payload(self):
        output = self.repo / "commits with spaces.json"
        result = self.fetch("--author", AUTHOR, "--output", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assert_payload(output.read_text(encoding="utf-8"))

    def test_explicit_dev_stdout_does_not_reopen_a_pipe(self):
        result = self.fetch("--author", AUTHOR, "--output", "/dev/stdout")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_payload(result.stdout)

    def test_default_author_uses_only_local_git_config(self):
        result = self.fetch()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_payload(result.stdout)

    def test_multiple_commits_keep_separate_bodies(self):
        self.git("commit", "--allow-empty", "-q", "-m", 'docs: first line\nsecond "line"', "-m", 'second body\\path\nnext line')
        result = self.fetch("--author", AUTHOR)
        self.assertEqual(result.returncode, 0, result.stderr)
        commits = json.loads(result.stdout)["commits"]
        self.assertEqual(len(commits), 2)
        self.assertEqual(commits[0]["subject"], 'docs: first line second "line"')
        self.assertEqual(commits[0]["body"], 'second body\\path\nnext line\n')
        self.assertEqual(commits[1]["subject"], self.subject)
        self.assertEqual(commits[1]["body"], self.body)

    def test_no_matching_author_returns_empty_commits(self):
        result = self.fetch("--author", "nobody@example.invalid")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["commits"], [])

    def test_missing_argument_leaves_previous_output_untouched(self):
        output = self.repo / "existing.json"
        output.write_text('{"keep":true}\n', encoding="utf-8")
        result = self.fetch("--output", str(output), "--author")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_text(), '{"keep":true}\n')

    def test_gh_json_is_embedded_without_a_network_call(self):
        stub_dir = self.repo / "stub-bin"
        stub_dir.mkdir()
        python = shutil.which("python3")
        self.assertIsNotNone(python)
        stub = stub_dir / "gh"
        stub.write_text(
            "#!" + python + "\nimport json,sys\n"
            "print(json.dumps([{'number':1,'title':sys.argv[1]+' \\\"quote\\\"\\\\path'}]))\n",
            encoding="utf-8",
        )
        stub.chmod(0o700)
        env = dict(os.environ, PATH=str(stub_dir) + os.pathsep + os.environ.get("PATH", ""))
        result = self.fetch("--author", AUTHOR, "--include-prs", "--include-issues", env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = self.assert_payload(result.stdout)
        self.assertEqual(data["prs"][0]["title"], 'pr "quote"\\path')
        self.assertEqual(data["issues"][0]["title"], 'issue "quote"\\path')

    def test_original_classify_and_format_pipeline_accepts_output(self):
        fetched = self.fetch("--author", AUTHOR)
        self.assertEqual(fetched.returncode, 0, fetched.stderr)
        classified = subprocess.run(
            ["python3", str(SCRIPTS / "classify_commits.py")], input=fetched.stdout,
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(classified.stdout)["totals"], {"fix": 1})
        formatted = subprocess.run(
            ["python3", str(SCRIPTS / "format_report.py")], input=classified.stdout,
            capture_output=True, text=True, check=True,
        )
        self.assertIn(self.subject, formatted.stdout)


if __name__ == "__main__":
    unittest.main()
