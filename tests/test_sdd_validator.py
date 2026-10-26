import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sdd-lint.py"
VALID_SPEC = """# Initiative

## Requirements

### REQ-001: Show project status
- Statement: The project page shows the current status.
- Acceptance: A reader can identify the current status without opening another page.
"""
VALID_TASKS = """# Tasks

### TASK-001: Add the status field
- Requirements: REQ-001
- Acceptance: The rendered project page displays the status.
- Evidence: The project page test passes.
"""


class SddValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.spec = self.root / "spec.md"
        self.tasks = self.root / "tasks.md"

    def tearDown(self):
        self.temp_dir.cleanup()

    def validate(self, spec=VALID_SPEC, tasks=VALID_TASKS):
        self.spec.write_text(spec, encoding="utf-8")
        self.tasks.write_text(tasks, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--spec", str(self.spec), "--tasks", str(self.tasks)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_accepts_valid_requirement_and_task_traceability(self):
        result = self.validate()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("validation passed", result.stdout.lower())

    def test_rejects_duplicate_requirement_definitions(self):
        duplicate_spec = VALID_SPEC + "\n### REQ-001: Duplicate\n- Acceptance: Duplicate definition.\n"

        result = self.validate(spec=duplicate_spec)

        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate requirement id req-001", result.stdout.lower())

    def test_rejects_requirements_or_tasks_with_empty_acceptance(self):
        invalid_spec = VALID_SPEC.replace("A reader can identify the current status without opening another page.", "[Acceptance criteria]")
        invalid_tasks = VALID_TASKS.replace("The rendered project page displays the status.", "")

        for spec, tasks in ((invalid_spec, VALID_TASKS), (VALID_SPEC, invalid_tasks)):
            with self.subTest(spec=spec != VALID_SPEC):
                result = self.validate(spec=spec, tasks=tasks)
                self.assertEqual(result.returncode, 1)
                self.assertIn("acceptance", result.stdout.lower())

    def test_rejects_tasks_without_requirement_links(self):
        unlinked_tasks = VALID_TASKS.replace("- Requirements: REQ-001", "- Requirements:")

        result = self.validate(tasks=unlinked_tasks)

        self.assertEqual(result.returncode, 1)
        self.assertIn("task task-001 has no requirement", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()