import unittest
import json
import re
from pathlib import Path


SKILL = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "spec-driven-development"
    / "SKILL.md"
)
PROJECT_TEMPLATE = (
    Path(__file__).resolve().parents[1]
    / "templates"
    / "projects"
    / "PROJECT.md.template"
)
REPO_ROOT = Path(__file__).resolve().parents[1]


class SpecDrivenDevelopmentSkillTests(unittest.TestCase):
    def test_project_registry_template_keeps_specification_optional(self):
        self.assertTrue(PROJECT_TEMPLATE.is_file())
        content = PROJECT_TEMPLATE.read_text(encoding="utf-8")

        for required_field in (
            "project_id:",
            "status:",
            "repository:",
            "## objective",
            "## specification and delivery",
        ):
            with self.subTest(field=required_field):
                self.assertIn(required_field, content.lower())
        self.assertNotIn("portfolio: true", content)

    def test_second_brain_template_link_resolves_inside_repository(self):
        skill_path = REPO_ROOT / ".agents/skills/second-brain-ops/SKILL.md"
        content = skill_path.read_text(encoding="utf-8")
        match = re.search(r"\]\(([^)]+/templates/projects/PROJECT\.md\.template)\)", content)

        self.assertIsNotNone(match)
        template_path = skill_path.parent / match.group(1)
        self.assertTrue(template_path.resolve().is_file())

    def test_project_and_portfolio_routes_are_discoverable(self):
        documents = {
            "coordinator": (
                REPO_ROOT / ".agents/skills/llm-wiki/SKILL.md",
                ("existing codebase", "spec-driven-development", "portfolio-export.py"),
            ),
            "second brain": (
                REPO_ROOT / ".agents/skills/second-brain-ops/SKILL.md",
                (
                    "projects/<project-id>/project.md",
                    "templates/projects/project.md.template",
                    "docs/specs/<initiative-id>/",
                ),
            ),
            "readme": (
                REPO_ROOT / "README.md",
                ("spec-driven development", "portfolio-export.py"),
            ),
            "prompt index": (REPO_ROOT / "prompts/README.md", ("project-sdd.md",)),
        }

        for document_name, (path, expected_terms) in documents.items():
            content = path.read_text(encoding="utf-8").lower()
            for expected_term in expected_terms:
                with self.subTest(document=document_name, term=expected_term):
                    self.assertTrue(
                        expected_term in content,
                        f"Missing {expected_term!r} from {document_name}",
                    )

    def test_root_instructions_route_projects_and_describe_local_skill_inventory(self):
        root_instructions = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
        skill_catalog = (REPO_ROOT / ".agents/README.md").read_text(encoding="utf-8").lower()
        lockfile = json.loads((REPO_ROOT / "skills-lock.json").read_text(encoding="utf-8"))

        for required_term in ("existing repository", "spec-driven-development", "portfolio"):
            with self.subTest(document="AGENTS.md", term=required_term):
                self.assertIn(required_term, root_instructions)

        installed_skills = {
            path.name for path in (REPO_ROOT / ".agents/skills").iterdir() if path.is_dir()
        }
        for skill_name in installed_skills:
            with self.subTest(document="skill catalog", skill=skill_name):
                self.assertIn(skill_name, skill_catalog)

        lock_only_skills = set(lockfile["skills"]) - installed_skills
        self.assertIn("skills-lock.json", skill_catalog)
        if lock_only_skills:
            self.assertIn("not installed", skill_catalog)

    def test_workflow_does_not_require_missing_companion_skills(self):
        content = SKILL.read_text(encoding="utf-8")

        for missing_dependency in (
            "api-and-interface-design",
            "planning-and-task-breakdown",
            "incremental-implementation",
            "context-engineering",
            "/build",
        ):
            with self.subTest(dependency=missing_dependency):
                self.assertTrue(
                    missing_dependency not in content,
                    f"Unexpected dependency reference: {missing_dependency}",
                )

    def test_workflow_preserves_existing_repo_conventions_and_human_gates(self):
        content = SKILL.read_text(encoding="utf-8")

        for required_phrase in (
            "existing codebase",
            "does not scaffold applications",
            "docs/specs/<initiative-id>/",
            "existing specification system",
            "human approval",
        ):
            with self.subTest(phrase=required_phrase):
                self.assertTrue(
                    required_phrase in content,
                    f"Missing workflow contract: {required_phrase}",
                )


if __name__ == "__main__":
    unittest.main()