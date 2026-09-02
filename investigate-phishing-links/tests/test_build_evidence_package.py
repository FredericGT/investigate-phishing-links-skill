#!/usr/bin/env python3
"""Safe regression tests for evidence packaging using synthetic case files."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
PACKAGER = SKILL_ROOT / "scripts" / "build_evidence_package.py"


class EvidencePackageTests(unittest.TestCase):
    def run_packager(self, case_dir: Path, output_zip: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(PACKAGER), str(case_dir), str(output_zip)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_package_is_deterministic_and_contains_manifest(self) -> None:
        with tempfile.TemporaryDirectory(prefix="phishing-package-test-") as temp:
            root = Path(temp)
            case = root / "case"
            case.mkdir()
            (case / "case-summary.md").write_text("Synthetic test evidence\n", encoding="utf-8")
            nested = case / "evidence"
            nested.mkdir()
            (nested / "headers.txt").write_text("HTTP/1.1 200 OK\n", encoding="utf-8")

            first = root / "first.zip"
            second = root / "second.zip"
            result = self.run_packager(case, first)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = self.run_packager(case, second)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(first.read_bytes(), second.read_bytes())

            digest = hashlib.sha256(first.read_bytes()).hexdigest()
            self.assertIn(digest, result.stdout)
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(
                    archive.namelist(),
                    ["case-summary.md", "evidence/headers.txt", "PACKAGE_SHA256SUMS.txt"],
                )
                manifest = archive.read("PACKAGE_SHA256SUMS.txt").decode("utf-8")
                self.assertIn("case-summary.md", manifest)
                self.assertIn("evidence/headers.txt", manifest)

    def test_symlink_is_rejected_without_creating_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="phishing-package-test-") as temp:
            root = Path(temp)
            case = root / "case"
            case.mkdir()
            (case / "safe.txt").write_text("safe\n", encoding="utf-8")
            (case / "linked.txt").symlink_to(case / "safe.txt")
            output = root / "output.zip"

            result = self.run_packager(case, output)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing symlink", result.stderr)
            self.assertFalse(output.exists())

    def test_output_inside_case_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="phishing-package-test-") as temp:
            case = Path(temp) / "case"
            case.mkdir()
            (case / "evidence.txt").write_text("safe\n", encoding="utf-8")
            output = case / "output.zip"

            result = self.run_packager(case, output)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("outside the case directory", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
