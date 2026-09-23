from __future__ import annotations

import importlib.util
import json
import shutil
import socket
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = REPO_ROOT / "scripts" / "create_trust_seed.py"
MODULE_SPEC = importlib.util.spec_from_file_location("create_trust_seed", MODULE_PATH)
assert MODULE_SPEC and MODULE_SPEC.loader
create_trust_seed = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(create_trust_seed)


class CreateTrustSeedTests(unittest.TestCase):
    def copy_template(self, root: Path) -> Path:
        destination = root / f"template-copy-{len(list(root.iterdir()))}"
        shutil.copytree(create_trust_seed.TEMPLATE_DIR, destination)
        return destination

    def use_template(self, template_dir: Path) -> None:
        original = create_trust_seed.TEMPLATE_DIR
        create_trust_seed.TEMPLATE_DIR = template_dir
        self.addCleanup(setattr, create_trust_seed, "TEMPLATE_DIR", original)

    def snapshot_tree(self, root: Path) -> dict[str, bytes]:
        snapshot: dict[str, bytes] = {}
        for path in sorted(root.rglob("*")):
            if path.is_file():
                snapshot[str(path.relative_to(root).as_posix())] = path.read_bytes()
        return snapshot

    def set_executable(self, path: Path) -> None:
        path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def test_creates_local_draft_without_resolving_human_choices(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = create_trust_seed.create_trust_seed(
                Path("oak-seed"),
                working_root=Path(tmpdir),
            )

            self.assertEqual(destination, (Path(tmpdir) / "oak-seed").resolve())
            manifest = json.loads((destination / "LOCAL_MANIFEST.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "local-draft")
            self.assertEqual(manifest["trust"]["name"], "TODO")
            self.assertEqual(manifest["trust"]["type"], ["TODO"])
            self.assertEqual(manifest["trust"]["purpose"], "TODO")
            self.assertEqual(manifest["privacy"]["defaultDataState"], "local-private")
            self.assertEqual(manifest["privacy"]["locationPrecision"], "TODO")
            self.assertFalse(manifest["privacy"]["publicProfile"])
            self.assertEqual(manifest["privacy"]["sharedWithFederation"], [])
            self.assertFalse(manifest["federationLink"]["enabled"])
            self.assertFalse(manifest["federationLink"]["publicNode"])
            self.assertFalse(manifest["agentPolicy"]["aiStewardEnabled"])
            self.assertEqual(manifest["agentPolicy"]["readScopes"], [])
            self.assertEqual(manifest["agentPolicy"]["writeScopes"], [])
            self.assertTrue(manifest["agentPolicy"]["humanApprovalRequired"])
            self.assertIn("`TODO: Name of the trust`", (destination / "TRUST.md").read_text(encoding="utf-8"))

    def test_determinism_compares_complete_relative_tree_and_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            seed_one = create_trust_seed.create_trust_seed(Path("alpha"), working_root=root)
            seed_two = create_trust_seed.create_trust_seed(Path("beta"), working_root=root)

            self.assertEqual(self.snapshot_tree(seed_one), self.snapshot_tree(seed_two))

    def test_round_trip_validation_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = create_trust_seed.create_trust_seed(Path("seed"), working_root=Path(tmpdir))
            before = self.snapshot_tree(seed)

            create_trust_seed.validate_seed_directory(seed)
            middle = self.snapshot_tree(seed)
            create_trust_seed.validate_seed_directory(seed)
            after = self.snapshot_tree(seed)

            self.assertEqual(before, middle)
            self.assertEqual(middle, after)

    def test_template_integrity_is_preserved_before_and_after_generation(self) -> None:
        template_before = self.snapshot_tree(create_trust_seed.TEMPLATE_DIR)
        with tempfile.TemporaryDirectory() as tmpdir:
            create_trust_seed.create_trust_seed(Path("seed"), working_root=Path(tmpdir))
        template_after = self.snapshot_tree(create_trust_seed.TEMPLATE_DIR)
        self.assertEqual(template_before, template_after)

    def test_creation_and_validation_do_not_attempt_network_access(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            deny = AssertionError("network access attempted")
            with mock.patch.object(socket, "create_connection", side_effect=deny), mock.patch.object(
                socket,
                "getaddrinfo",
                side_effect=deny,
            ), mock.patch.object(socket.socket, "connect", side_effect=deny):
                seed = create_trust_seed.create_trust_seed(Path("seed"), working_root=Path(tmpdir))
                create_trust_seed.validate_seed_directory(seed)

    def test_rejects_existing_empty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "seed"
            destination.mkdir()
            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("seed"), working_root=Path(tmpdir))
            self.assertIn("Destination already exists", str(exc.exception))

    def test_rejects_absolute_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path(tmpdir) / "seed", working_root=Path(tmpdir))
            self.assertIn("Destination path escapes the intended working location", str(exc.exception))

    def test_rejects_traversal_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("../seed"), working_root=Path(tmpdir))
            self.assertIn("Destination path escapes the intended working location", str(exc.exception))

    def test_rejects_windows_style_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path(r"folder\seed"), working_root=Path(tmpdir))
            self.assertIn("Destination path must use a relative POSIX path", str(exc.exception))

    def test_rejects_symlinked_destination_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            outside = root / "outside"
            outside.mkdir()
            linked_parent = root / "linked"
            linked_parent.symlink_to(outside, target_is_directory=True)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("linked/seed"), working_root=root)
            self.assertIn("Destination path uses a symlinked parent", str(exc.exception))

    def test_rejects_symlinked_template_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = self.copy_template(root)
            (template / "README.md").unlink()
            (template / "README.md").symlink_to(root / "outside.md")
            (root / "outside.md").write_text("outside\n", encoding="utf-8")
            self.use_template(template)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("seed"), working_root=root)
            self.assertIn("contains a symlinked entry", str(exc.exception))

    def test_rejects_hidden_executable_in_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = self.copy_template(root)
            hidden = template / ".evil.sh"
            hidden.write_text("#!/bin/sh\n", encoding="utf-8")
            self.set_executable(hidden)
            self.use_template(template)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("seed"), working_root=root)
            self.assertIn("contains a hidden entry", str(exc.exception))

    def test_rejects_nested_executable_in_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = self.copy_template(root)
            nested = template / "bin"
            nested.mkdir()
            script = nested / "evil.sh"
            script.write_text("#!/bin/sh\n", encoding="utf-8")
            self.set_executable(script)
            self.use_template(template)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("seed"), working_root=root)
            self.assertIn("contains a nested directory", str(exc.exception))

    def test_rejects_unexpected_executable_template_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = self.copy_template(root)
            extra = template / "extra.sh"
            extra.write_text("#!/bin/sh\n", encoding="utf-8")
            self.set_executable(extra)
            self.use_template(template)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("seed"), working_root=root)
            self.assertIn("contains an unexpected file", str(exc.exception))

    def test_rejects_malformed_template_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = self.copy_template(root)
            (template / "LOCAL_MANIFEST.json").write_text("{broken\n", encoding="utf-8")
            self.use_template(template)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("seed"), working_root=root)
            self.assertIn("Template LOCAL_MANIFEST.json is not valid JSON", str(exc.exception))
            self.assertFalse((root / "seed").exists())

    def test_rejects_missing_manifest_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = self.copy_template(root)
            manifest = json.loads((template / "LOCAL_MANIFEST.json").read_text(encoding="utf-8"))
            del manifest["privacy"]
            (template / "LOCAL_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
            self.use_template(template)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("seed"), working_root=root)
            self.assertIn("privacy section must be an object", str(exc.exception))

    def test_rejects_wrong_manifest_types(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = self.copy_template(root)
            manifest = json.loads((template / "LOCAL_MANIFEST.json").read_text(encoding="utf-8"))
            manifest["documents"] = ["TRUST.md"]
            (template / "LOCAL_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
            self.use_template(template)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("seed"), working_root=root)
            self.assertIn("documents section must be an object", str(exc.exception))

    def test_rejects_manifest_document_path_escape_variants(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            variants = {
                "../TRUST.md": "escapes the intended working location",
                "/tmp/TRUST.md": "escapes the intended working location",
                r"folder\TRUST.md": "must use a relative POSIX path",
            }

            for raw_path, message in variants.items():
                with self.subTest(raw_path=raw_path):
                    template = self.copy_template(root)
                    manifest = json.loads((template / "LOCAL_MANIFEST.json").read_text(encoding="utf-8"))
                    manifest["documents"]["trust"] = raw_path
                    (template / "LOCAL_MANIFEST.json").write_text(
                        json.dumps(manifest),
                        encoding="utf-8",
                    )
                    original = create_trust_seed.TEMPLATE_DIR
                    create_trust_seed.TEMPLATE_DIR = template
                    try:
                        with self.assertRaises(SystemExit) as exc:
                            create_trust_seed.create_trust_seed(Path("seed"), working_root=root)
                        self.assertIn(message, str(exc.exception))
                    finally:
                        create_trust_seed.TEMPLATE_DIR = original
                    shutil.rmtree(template)

    def test_rejects_invalid_utf8_template_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = self.copy_template(root)
            (template / "README.md").write_bytes(b"\xff\xfe")
            self.use_template(template)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("seed"), working_root=root)
            self.assertIn("is not valid UTF-8", str(exc.exception))

    def test_rejects_unsafe_agent_policy_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            template = self.copy_template(root)
            manifest = json.loads((template / "LOCAL_MANIFEST.json").read_text(encoding="utf-8"))
            manifest["agentPolicy"]["aiStewardEnabled"] = True
            manifest["agentPolicy"]["readScopes"] = ["all"]
            manifest["agentPolicy"]["writeScopes"] = ["all"]
            (template / "LOCAL_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
            self.use_template(template)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(Path("seed"), working_root=root)
            self.assertIn("agentPolicy.aiStewardEnabled must be false", str(exc.exception))

    def test_cleans_up_after_permission_failure_without_leaving_seed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            original_copy2 = shutil.copy2

            def guarded_copy(source: object, destination: object, *, follow_symlinks: bool = True) -> object:
                source_path = Path(source)
                if source_path.name == "TREE_OF_LIFE.md":
                    raise PermissionError("simulated permission failure")
                return original_copy2(source, destination, follow_symlinks=follow_symlinks)

            with mock.patch.object(create_trust_seed.shutil, "copy2", side_effect=guarded_copy):
                with self.assertRaises(PermissionError):
                    create_trust_seed.create_trust_seed(Path("seed"), working_root=root)

            self.assertFalse((root / "seed").exists())
            self.assertEqual(sorted(root.iterdir()), [])

    def test_validate_rejects_extra_generated_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = create_trust_seed.create_trust_seed(Path("seed"), working_root=Path(tmpdir))
            extra = seed / "extra.sh"
            extra.write_text("#!/bin/sh\n", encoding="utf-8")
            self.set_executable(extra)

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.validate_seed_directory(seed)
            self.assertIn("contains an unexpected file", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
