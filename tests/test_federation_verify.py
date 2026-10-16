"""Regression checks for the federation's declared verification command."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class FederationVerifyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        manifest = json.loads((ROOT / "aift.repo.json").read_text(encoding="utf-8"))
        cls.command = manifest["commands"]["verify"]

    def run_fixture(self, *, validator_exit: int = 0, unit_tests_pass: bool = True) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "tests").mkdir()
            (root / "scripts" / "validate_doctrine.py").write_text(
                "import sys\nprint('VALIDATOR_EXECUTED')\nsys.exit(" + str(validator_exit) + ")\n",
                encoding="utf-8",
            )
            (root / "tests" / "test_probe.py").write_text(
                "import unittest\n"
                "class Probe(unittest.TestCase):\n"
                "    def test_probe(self):\n"
                "        print('UNIT_TESTS_EXECUTED')\n"
                f"        self.assertEqual({1 if unit_tests_pass else 0}, 1)\n",
                encoding="utf-8",
            )
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            return subprocess.run(
                self.command, shell=True, cwd=root, env=env,
                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                check=False, timeout=15,
            )

    def test_verification_runs_both_existing_gates(self) -> None:
        self.assertIn("scripts/validate_doctrine.py", self.command)
        self.assertIn("unittest discover -s tests", self.command)
        self.assertNotIn("--if-present", self.command)

    def test_success_executes_both_gates(self) -> None:
        result = self.run_fixture()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("VALIDATOR_EXECUTED", result.stdout)
        self.assertIn("UNIT_TESTS_EXECUTED", result.stdout)

    def test_doctrine_failure_stops_before_tests(self) -> None:
        result = self.run_fixture(validator_exit=7)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("VALIDATOR_EXECUTED", result.stdout)
        self.assertNotIn("UNIT_TESTS_EXECUTED", result.stdout)

    def test_unit_test_failure_is_not_reported_as_success(self) -> None:
        result = self.run_fixture(unit_tests_pass=False)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("VALIDATOR_EXECUTED", result.stdout)
        self.assertIn("UNIT_TESTS_EXECUTED", result.stdout)


if __name__ == "__main__":
    unittest.main()
