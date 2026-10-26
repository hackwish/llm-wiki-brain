import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "portfolio-export.py"


class PortfolioExportTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.projects = self.root / "projects"
        self.projects.mkdir()
        self.output = self.root / "public"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_project(self, name, metadata, body=""):
        (self.projects / name).write_text(f"---\n{metadata}\n---\n\n{body}", encoding="utf-8")

    def export_portfolio(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_exports_only_explicitly_published_projects_and_escapes_html(self):
        self.write_project(
            "public-case.md",
            'title: "Public case"\ndescription: "A <strong>measured</strong> result"\n'
            "portfolio: true\nvisibility: public\nstatus: published\nskills: [Python, Research]",
            "## Outcome\n\nSafe content. <script>alert(1)</script>",
        )
        self.write_project(
            "private-case.md",
            'title: "Private case"\ndescription: "Do not expose"\n'
            "portfolio: true\nvisibility: private\nstatus: published",
            "Private body.",
        )

        result = self.export_portfolio()

        self.assertEqual(result.returncode, 0, result.stderr)
        page = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertIn("Public case", page)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertNotIn("Private case", page)
        self.assertNotIn("Do not expose", page)

    def test_reexport_removes_projects_that_are_no_longer_public(self):
        self.write_project(
            "case.md",
            'title: "Previously public"\ndescription: "Description"\n'
            "portfolio: true\nvisibility: public\nstatus: published",
        )
        self.assertEqual(self.export_portfolio().returncode, 0)
        self.write_project(
            "case.md",
            'title: "Previously public"\ndescription: "Description"\n'
            "portfolio: false\nvisibility: private\nstatus: draft",
        )

        result = self.export_portfolio()

        self.assertEqual(result.returncode, 0, result.stderr)
        page = (self.output / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("Previously public", page)
        self.assertIn("No projects are currently approved", page)


if __name__ == "__main__":
    unittest.main()