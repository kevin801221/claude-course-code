"""從空白目錄驗收 Q2、Q4，每個動作啟動獨立 Python 程序。"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def main():
    with tempfile.TemporaryDirectory() as tmp:
        def run(*args):
            return subprocess.check_output([sys.executable, str(ROOT / "classroom.py"), *args],
                                           cwd=tmp, text=True, encoding="utf-8")

        assert "4 筆" in run("save")
        assert "4 筆" in run("save")
        assert run("search", "重複報名").splitlines() == [
            "#101 | 2026-11-16 | 重複報名 | 初報", "#102 | 2026-11-17 | 重複報名 | 完成"]
        timeline = run("timeline", "102")
        assert "#101" in timeline and "#102" in timeline and "#104" not in timeline
        record = json.loads(run("get", "102"))
        assert record["evidence"] == "TEST-12" and record["kind"] == "完成"
        assert "查無" in run("search", "課堂不存在的記錄")
        run("reports")
        reports = Path(tmp) / "practice" / "reports"
        assert len(list(reports.rglob("*.md"))) == 8
        assert (reports / "team/weekly/2026-W47.md").read_text(encoding="utf-8") == (
            ROOT / "expected/team-weekly.md").read_text(encoding="utf-8")
        eng = (reports / "members/eng/weekly/2026-W47.md").read_text(encoding="utf-8")
        pm = (reports / "members/pm/weekly/2026-W47.md").read_text(encoding="utf-8")
        assert eng.index("## 完成") < eng.index("## 初報") and "TKT-9" not in eng
        assert pm.index("## 待查") < pm.index("## 決議") and "TEST-12" not in pm
    print("PASS：4 筆合成記憶可跨程序查回，8 份個人與主管報告符合預期。")


if __name__ == "__main__":
    main()
