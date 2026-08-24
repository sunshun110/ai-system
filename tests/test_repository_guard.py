import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "tools" / "repository_guard.py"


class RepositoryGuardTests(unittest.TestCase):
    def run_guard(self, root, *args, cwd=None):
        return subprocess.run(
            [sys.executable, str(GUARD), "--root", str(root), *args],
            cwd=str(cwd or root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_success_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repository"
            root.mkdir()
            (root / "README.md").write_text(
                "Security guidance may discuss tokens without assigning one.\n"
                "API_TOKEN=<redacted>\n",
                encoding="utf-8",
            )
            result = self.run_guard(root, cwd=Path(tmp))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Repository guard: OK", result.stdout)
            self.assertIn("Files scanned: 1", result.stdout)
            self.assertIn("Errors: 0", result.stdout)

    def test_forbidden_term_in_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            term = "internal-codename"
            (root / "notes.md").write_text(f"Reference: {term}\n", encoding="utf-8")
            result = self.run_guard(root, "--forbidden-term", term)
            self.assertEqual(result.returncode, 1)
            self.assertIn("[forbidden-term]", result.stdout)
            self.assertNotIn(term, result.stdout)

    def test_forbidden_term_in_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            term = "private-product"
            path = root / f"{term}-notes.md"
            path.write_text("generic text\n", encoding="utf-8")
            result = self.run_guard(root, "--forbidden-term", term)
            self.assertEqual(result.returncode, 1)
            self.assertIn("<redacted>-notes.md", result.stdout)
            self.assertNotIn(term, result.stdout)

    def test_local_absolute_user_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            local_path = "/" + "Users" + "/developer/private/file.txt"
            (root / "notes.md").write_text(f"Found at {local_path}\n", encoding="utf-8")
            result = self.run_guard(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("[local-path]", result.stdout)
            self.assertNotIn(local_path, result.stdout)

    def test_likely_credential_is_rejected_without_printing_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secret = "gh" + "p_" + "A1b2C3d4E5f6G7h8I9j0K1l2"
            assignment = "API_" + "TOKEN=" + secret
            (root / "config.txt").write_text(assignment + "\n", encoding="utf-8")
            result = self.run_guard(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("[credential]", result.stdout)
            self.assertNotIn(secret, result.stdout)
            self.assertNotIn(secret, result.stderr)

    def test_binary_archives_and_excluded_directories_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secret = "gh" + "p_" + "Z9y8X7w6V5u4T3s2R1q0P9o8"
            payload = ("API_" + "TOKEN=" + secret).encode("ascii")
            (root / "binary.dat").write_bytes(b"\x00" + payload)
            (root / "export.zip").write_bytes(payload)
            for directory in (".git", ".venv", ".local", "__pycache__"):
                excluded = root / directory
                excluded.mkdir()
                (excluded / "config.txt").write_bytes(payload)
            result = self.run_guard(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Files excluded: 2", result.stdout)
            self.assertIn("Directories excluded: 4", result.stdout)

    def test_explicit_and_automatic_denylists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            local = root / ".local"
            local.mkdir()
            auto_term = "internal-alpha"
            explicit_term = "internal-beta"
            (local / "forbidden-terms.txt").write_text(auto_term + "\n", encoding="utf-8")
            denylist = root / "extra-denylist.txt"
            denylist.write_text(explicit_term + "\n", encoding="utf-8")
            (root / "notes.md").write_text(
                f"{auto_term}\n{explicit_term}\n",
                encoding="utf-8",
            )
            result = self.run_guard(
                root,
                "--denylist",
                str(denylist),
                "--forbidden-term",
                "third-term",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("[forbidden-term]", result.stdout)
            self.assertNotIn(auto_term, result.stdout)
            self.assertNotIn(explicit_term, result.stdout)


if __name__ == "__main__":
    unittest.main()
