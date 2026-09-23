from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = REPO_ROOT / "scripts" / "validate_doctrine.py"
MODULE_SPEC = importlib.util.spec_from_file_location("validate_doctrine", MODULE_PATH)
assert MODULE_SPEC and MODULE_SPEC.loader
validate_doctrine = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(validate_doctrine)


class ValidateDoctrineTests(unittest.TestCase):
    def make_fixture_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        tmpdir = tempfile.TemporaryDirectory()
        root = Path(tmpdir.name)

        for relative_path in (
            "README.md",
            "AGENTS.md",
            "docs/holographic-trust-architecture.md",
            "docs/constitutional-chapter-holographic-trusts.md",
            "templates/trust-seed/README.md",
            "research/aethercore-test-001/scripts/good_script.py",
        ):
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("print('ok')\n", encoding="utf-8")

        manifest = {
            "kind": "federation-manifest",
            "canonicalDocuments": {
                "readme": "README.md",
                "agents": "AGENTS.md",
                "holographicTrustArchitecture": "docs/holographic-trust-architecture.md",
                "constitutionalHolographicTrustsChapter": (
                    "docs/constitutional-chapter-holographic-trusts.md"
                ),
                "trustSeedTemplate": "templates/trust-seed/README.md",
            },
            "trustSeedPattern": {
                "templatePath": "templates/trust-seed",
                "localFirst": True,
                "federationOptional": True,
                "privacyDefault": "local-private",
            },
        }

        manifest_path = root / "manifests" / "federation.manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        return tmpdir, root

    def write_manifest(self, root: Path, manifest: dict[str, object]) -> Path:
        manifest_path = root / "manifests" / "federation.manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return manifest_path

    def exit_message(self, exc: SystemExit) -> str:
        return str(exc.exception)

    def test_rejects_missing_canonical_document(self) -> None:
        tmpdir, root = self.make_fixture_repo()
        self.addCleanup(tmpdir.cleanup)

        manifest_path = root / "manifests" / "federation.manifest.json"
        (root / "README.md").unlink()

        with self.assertRaises(SystemExit) as exc:
            validate_doctrine.validate_manifest(root, manifest_path)

        self.assertIn("readme is missing", self.exit_message(exc))

    def test_rejects_absolute_manifest_path(self) -> None:
        tmpdir, root = self.make_fixture_repo()
        self.addCleanup(tmpdir.cleanup)

        manifest = json.loads(
            (root / "manifests" / "federation.manifest.json").read_text(encoding="utf-8")
        )
        manifest["canonicalDocuments"]["readme"] = "/tmp/escape.md"
        manifest_path = self.write_manifest(root, manifest)

        with self.assertRaises(SystemExit) as exc:
            validate_doctrine.validate_manifest(root, manifest_path)

        self.assertIn("readme escapes the repository", self.exit_message(exc))

    def test_rejects_traversal_manifest_path(self) -> None:
        tmpdir, root = self.make_fixture_repo()
        self.addCleanup(tmpdir.cleanup)

        manifest = json.loads(
            (root / "manifests" / "federation.manifest.json").read_text(encoding="utf-8")
        )
        manifest["canonicalDocuments"]["readme"] = "../escape.md"
        manifest_path = self.write_manifest(root, manifest)

        with self.assertRaises(SystemExit) as exc:
            validate_doctrine.validate_manifest(root, manifest_path)

        self.assertIn("readme escapes the repository", self.exit_message(exc))

    def test_rejects_invalid_manifest_invariant(self) -> None:
        tmpdir, root = self.make_fixture_repo()
        self.addCleanup(tmpdir.cleanup)

        manifest = json.loads(
            (root / "manifests" / "federation.manifest.json").read_text(encoding="utf-8")
        )
        manifest["trustSeedPattern"]["privacyDefault"] = "public"
        manifest_path = self.write_manifest(root, manifest)

        with self.assertRaises(SystemExit) as exc:
            validate_doctrine.validate_manifest(root, manifest_path)

        self.assertIn(
            'trustSeedPattern.privacyDefault must be "local-private"',
            self.exit_message(exc),
        )

    def test_rejects_non_string_manifest_path(self) -> None:
        tmpdir, root = self.make_fixture_repo()
        self.addCleanup(tmpdir.cleanup)

        manifest = json.loads(
            (root / "manifests" / "federation.manifest.json").read_text(encoding="utf-8")
        )
        manifest["canonicalDocuments"]["readme"] = {"path": "README.md"}
        manifest_path = self.write_manifest(root, manifest)

        with self.assertRaises(SystemExit) as exc:
            validate_doctrine.validate_manifest(root, manifest_path)

        self.assertIn(
            "readme must be a non-empty string path",
            self.exit_message(exc),
        )

    def test_rejects_invalid_python_source(self) -> None:
        tmpdir, root = self.make_fixture_repo()
        self.addCleanup(tmpdir.cleanup)

        scripts_path = root / "research" / "aethercore-test-001" / "scripts"
        (scripts_path / "bad_script.py").write_text("def broken(:\n", encoding="utf-8")

        with self.assertRaises(SystemExit) as exc:
            validate_doctrine.validate_research_scripts(root, scripts_path)

        self.assertIn("Research script compilation failed", self.exit_message(exc))

    def test_rejects_missing_research_scripts_directory(self) -> None:
        tmpdir, root = self.make_fixture_repo()
        self.addCleanup(tmpdir.cleanup)

        scripts_path = root / "research" / "aethercore-test-001" / "scripts"
        for script_path in scripts_path.glob("*.py"):
            script_path.unlink()
        scripts_path.rmdir()

        with self.assertRaises(SystemExit) as exc:
            validate_doctrine.validate_research_scripts(root, scripts_path)

        self.assertIn(
            "Research scripts directory is missing",
            self.exit_message(exc),
        )

    def test_rejects_symlink_escape(self) -> None:
        tmpdir, root = self.make_fixture_repo()
        self.addCleanup(tmpdir.cleanup)

        outside = root.parent / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        (root / "docs" / "linked.md").symlink_to(outside)

        manifest = json.loads(
            (root / "manifests" / "federation.manifest.json").read_text(encoding="utf-8")
        )
        manifest["canonicalDocuments"]["holographicTrustArchitecture"] = "docs/linked.md"
        manifest_path = self.write_manifest(root, manifest)

        with self.assertRaises(SystemExit) as exc:
            validate_doctrine.validate_manifest(root, manifest_path)

        self.assertIn("uses a symlinked path", self.exit_message(exc))

    def test_validation_leaves_no_pycache_artifacts(self) -> None:
        tmpdir, root = self.make_fixture_repo()
        self.addCleanup(tmpdir.cleanup)

        manifest_path = root / "manifests" / "federation.manifest.json"
        scripts_path = root / "research" / "aethercore-test-001" / "scripts"

        validate_doctrine.validate_manifest(root, manifest_path)
        validate_doctrine.validate_research_scripts(root, scripts_path)

        pycache_paths = list(root.rglob("__pycache__"))
        self.assertEqual(pycache_paths, [])


if __name__ == "__main__":
    unittest.main()
