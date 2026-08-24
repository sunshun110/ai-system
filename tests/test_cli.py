import json
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "bin" / "ai-system"


class CliTests(unittest.TestCase):
    def run_cli(self, *args, cwd=None):
        result = subprocess.run(
            [str(CLI), *args],
            cwd=str(cwd or ROOT.parent),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            self.fail(f"command failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        return result.stdout

    def test_source_commands(self):
        self.assertIn("AI System", self.run_cli("info"))
        self.assertIn("triage-issue", self.run_cli("list", "workflows"))
        self.assertIn("test-acceptance", self.run_cli("list", "workflows"))
        self.assertIn("qa-tester", self.run_cli("list", "agents"))
        self.assertIn("策划", self.run_cli("list", "company-roles"))
        self.assertIn("运维架构师", self.run_cli("list", "company-roles"))
        self.assertIn("h5-game", self.run_cli("list", "departments"))
        self.assertIn("Workflow: Triage Issue", self.run_cli("show", "workflows", "triage-issue"))
        self.assertIn("Workflow: Test Acceptance", self.run_cli("show", "workflows", "test-acceptance"))
        self.assertIn("Agent: QA Tester", self.run_cli("show", "agents", "qa-tester"))
        self.assertIn("# 策划岗位", self.run_cli("show", "company-roles", "策划"))
        self.assertIn("# 运维架构师岗位", self.run_cli("show", "company-roles", "运维架构师"))
        self.assertIn("doctor: ok", self.run_cli("doctor"))

    def test_project_lifecycle(self):
        with tempfile.TemporaryDirectory(prefix="ai-system-test.") as tmp:
            target = Path(tmp) / "demo"

            self.run_cli(
                "new-project",
                str(target),
                "--name",
                "demo-project",
                "--adapter",
                "claude",
                "--adapter",
                "codex",
            )

            state_path = target / ".ai-system" / "state.json"
            self.assertTrue(state_path.exists())
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["project"]["name"], "demo-project")
            self.assertEqual(state["adapters"], ["claude", "codex"])
            self.assertEqual(state["domains"], [])
            self.assertTrue((target / ".claude" / "commands" / "triage-issue.md").exists())
            self.assertTrue((target / ".claude" / "agents" / "qa-tester.md").exists())
            self.assertTrue((target / ".ai-system" / "agents" / "qa-tester.md").exists())
            self.assertTrue((target / ".ai-system" / "workflows" / "test-acceptance.md").exists())
            self.assertIn("validate: ok", self.run_cli("validate", "--target", str(target)))

            self.run_cli("install", "--target", str(target), "--adapter", "cursor", "--force")
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["adapters"], ["claude", "codex", "cursor"])
            self.assertTrue((target / ".cursor" / "rules" / "ai-system.md").exists())

            self.run_cli("remove", "--target", str(target), "--adapter", "codex")
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["adapters"], ["claude", "cursor"])
            self.assertFalse((target / ".ai-system" / "adapters" / "codex.md").exists())

            self.assertIn("Active domain packs: none", (target / "AGENTS.md").read_text(encoding="utf-8"))

            self.assertIn("initialized:", self.run_cli("update", "--target", str(target)))
            self.assertIn("validate: ok", self.run_cli("validate", "--target", str(target)))

            self.run_cli("remove", "--target", str(target), "--all")
            self.assertTrue((target / "README.md").exists())
            self.assertFalse((target / ".ai-system").exists())
            self.assertFalse((target / ".claude").exists())
            self.assertFalse((target / ".cursor").exists())
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertFalse((target / "CLAUDE.md").exists())

    def test_export(self):
        created_files = []
        created_directories = []
        excluded_directory_names = (".kiro", ".local", ".git", "__pycache__")

        try:
            for directory_name in excluded_directory_names:
                directory = ROOT / directory_name
                existed = directory.exists()
                if not existed:
                    directory.mkdir()
                    created_directories.append(directory)
                self.assertTrue(directory.is_dir(), f"expected directory fixture: {directory}")

                # Never write into a pre-existing excluded directory.
                if existed:
                    continue

                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    prefix="ai-system-export-test-",
                    suffix=".txt",
                    dir=directory,
                    delete=False,
                ) as fixture:
                    fixture.write("local-only export fixture\n")
                    created_files.append(Path(fixture.name))

            with tempfile.NamedTemporaryFile(
                mode="wb",
                prefix="ai-system-export-test-",
                suffix=".tar.gz",
                dir=ROOT,
                delete=False,
            ) as fixture:
                fixture.write(b"generated archive fixture")
                generated_archive = Path(fixture.name)
                created_files.append(generated_archive)

            with tempfile.TemporaryDirectory(prefix="ai-system-export.") as tmp:
                output = Path(tmp) / "ai-system.tar.gz"
                self.run_cli("export", "--output", str(output))
                self.assertTrue(output.exists())
                self.assertGreater(output.stat().st_size, 0)
                with tarfile.open(output, "r:gz") as archive:
                    names = set(archive.getnames())

            self.assertIn("ai-system/bin/ai-system", names)
            self.assertIn("ai-system/core/constitution.md", names)
            self.assertIn("ai-system/company/AGENTS.md", names)
            self.assertIn("ai-system/company/roles/策划.md", names)
            self.assertIn("ai-system/company/roles/运维架构师.md", names)
            self.assertIn("ai-system/company/departments/h5-game/AGENTS.md", names)

            for directory_name in excluded_directory_names:
                archive_path = f"ai-system/{directory_name}"
                self.assertNotIn(archive_path, names)
                self.assertFalse(
                    any(name.startswith(f"{archive_path}/") for name in names),
                    f"export included excluded directory: {archive_path}",
                )
            self.assertNotIn(f"ai-system/{generated_archive.name}", names)
        finally:
            for path in reversed(created_files):
                path.unlink(missing_ok=True)
            for directory in reversed(created_directories):
                try:
                    directory.rmdir()
                except OSError:
                    # Preserve unexpected content rather than deleting anything
                    # that was not created by this test.
                    pass

    def test_demo(self):
        with tempfile.TemporaryDirectory(prefix="ai-system-demo-target.") as tmp:
            target = Path(tmp) / "demo"
            output = self.run_cli("demo", "--target", str(target), "--name", "demo-test")
            self.assertIn("Demo project is ready.", output)
            self.assertTrue((target / ".ai-system" / "state.json").exists())
            self.assertTrue((target / ".claude" / "commands" / "triage-issue.md").exists())
            state = json.loads((target / ".ai-system" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["domains"], [])


if __name__ == "__main__":
    unittest.main()
