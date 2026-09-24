from __future__ import annotations

import importlib.util
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


create_trust_seed = load_module("create_trust_seed", SCRIPTS_DIR / "create_trust_seed.py")
trust_seed_identity = load_module("trust_seed_identity", SCRIPTS_DIR / "trust_seed_identity.py")


class TrustSeedIdentityTests(unittest.TestCase):
    def create_seed(self, root: Path, name: str = "seed") -> Path:
        return create_trust_seed.create_trust_seed(Path(name), working_root=root)

    def run_cli(self, script_name: str, seed_dir: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / script_name), str(seed_dir)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def load_json(self, path: Path) -> dict[str, object]:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_identity_initialization_creates_private_and_public_material(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))

            public_record = trust_seed_identity.init_identity(seed)

            state_root = seed / trust_seed_identity.LOCAL_STATE_DIR
            private_key = trust_seed_identity.private_key_path(seed)
            public_identity = trust_seed_identity.public_identity_path(seed)

            self.assertTrue(state_root.is_dir())
            self.assertTrue(private_key.is_file())
            self.assertTrue(public_identity.is_file())
            self.assertEqual(public_record["algorithm"], trust_seed_identity.SIGNING_ALGORITHM)
            self.assertIn("BEGIN PRIVATE KEY", private_key.read_text(encoding="utf-8"))
            self.assertNotIn("PRIVATE KEY", public_identity.read_text(encoding="utf-8"))

            if os.name != "nt":
                self.assertEqual(private_key.stat().st_mode & 0o077, 0)

    def test_refuses_to_overwrite_existing_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))
            trust_seed_identity.init_identity(seed)

            with self.assertRaises(SystemExit) as exc:
                trust_seed_identity.init_identity(seed)

            self.assertIn("Local identity already exists", str(exc.exception))

    def test_sign_and_verify_succeed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))
            trust_seed_identity.init_identity(seed)

            record = trust_seed_identity.sign_seed(seed)
            verified = trust_seed_identity.verify_seed(seed)

            self.assertEqual(record["contentDigest"], verified["contentDigest"])
            self.assertTrue(trust_seed_identity.provenance_path(seed).is_file())

    def test_verification_succeeds_without_private_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))
            trust_seed_identity.init_identity(seed)
            trust_seed_identity.sign_seed(seed)

            trust_seed_identity.private_key_path(seed).unlink()

            verified = trust_seed_identity.verify_seed(seed)
            self.assertEqual(
                verified["verification"]["algorithm"],  # type: ignore[index]
                trust_seed_identity.SIGNING_ALGORITHM,
            )

    def test_modified_manifest_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))
            trust_seed_identity.init_identity(seed)
            trust_seed_identity.sign_seed(seed)

            manifest_path = seed / "LOCAL_MANIFEST.json"
            manifest = self.load_json(manifest_path)
            manifest["trust"]["name"] = "Oak Trust"  # type: ignore[index]
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(SystemExit) as exc:
                trust_seed_identity.verify_seed(seed)

            self.assertIn("does not match the recorded provenance", str(exc.exception))

    def test_modified_signed_document_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))
            trust_seed_identity.init_identity(seed)
            trust_seed_identity.sign_seed(seed)

            trust_path = seed / "TRUST.md"
            trust_path.write_text(
                trust_path.read_text(encoding="utf-8") + "\nTampered.\n",
                encoding="utf-8",
            )

            with self.assertRaises(SystemExit) as exc:
                trust_seed_identity.verify_seed(seed)

            self.assertIn("does not match the recorded provenance", str(exc.exception))

    def test_corrupted_signature_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))
            trust_seed_identity.init_identity(seed)
            trust_seed_identity.sign_seed(seed)

            provenance_path = trust_seed_identity.provenance_path(seed)
            provenance = self.load_json(provenance_path)
            signature = provenance["signature"]["value"]  # type: ignore[index]
            mutated = bytearray(signature.encode("ascii"))
            mutated[-2] = ord("A") if mutated[-2] != ord("A") else ord("B")
            provenance["signature"]["value"] = mutated.decode("ascii")  # type: ignore[index]
            provenance_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(SystemExit) as exc:
                trust_seed_identity.verify_seed(seed)

            self.assertIn("signature verification failed", str(exc.exception))

    def test_corrupted_public_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))
            trust_seed_identity.init_identity(seed)
            trust_seed_identity.sign_seed(seed)

            provenance_path = trust_seed_identity.provenance_path(seed)
            provenance = self.load_json(provenance_path)
            provenance["verification"]["publicKey"]["value"] = "A" * 43 + "="  # type: ignore[index]
            provenance["verification"]["keyId"] = "sha256:" + ("0" * 64)  # type: ignore[index]
            provenance_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(SystemExit) as exc:
                trust_seed_identity.verify_seed(seed)

            self.assertIn("keyId does not match", str(exc.exception))

    def test_malformed_provenance_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))
            trust_seed_identity.init_identity(seed)
            trust_seed_identity.sign_seed(seed)

            provenance_path = trust_seed_identity.provenance_path(seed)
            provenance_path.write_text('{"kind":"broken"}\n', encoding="utf-8")

            with self.assertRaises(SystemExit) as exc:
                trust_seed_identity.verify_seed(seed)

            self.assertIn("schema is invalid", str(exc.exception))

    def test_path_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            seed = self.create_seed(root)
            manifest_path = seed / "LOCAL_MANIFEST.json"
            manifest = self.load_json(manifest_path)
            manifest["documents"]["trust"] = "../outside.md"  # type: ignore[index]
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            with self.assertRaises(SystemExit) as exc:
                trust_seed_identity.init_identity(seed)

            self.assertIn("escapes the trust seed", str(exc.exception))

    def test_symlinked_document_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            seed = self.create_seed(root)
            trust_seed_identity.init_identity(seed)
            outside = root / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            trust_path = seed / "TRUST.md"
            trust_path.unlink()
            trust_path.symlink_to(outside)

            with self.assertRaises(SystemExit) as exc:
                trust_seed_identity.sign_seed(seed)

            self.assertIn("uses a symlinked path", str(exc.exception))

    def test_canonicalization_is_deterministic_for_manifest_formatting_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))
            before = trust_seed_identity.build_signed_state(seed)

            manifest_path = seed / "LOCAL_MANIFEST.json"
            manifest = self.load_json(manifest_path)
            reordered = {key: manifest[key] for key in reversed(list(manifest))}
            manifest_path.write_text(json.dumps(reordered, indent=4) + "\n", encoding="utf-8")

            after = trust_seed_identity.build_signed_state(seed)
            self.assertEqual(before, after)

    def test_operations_do_not_attempt_network_access(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))
            deny = AssertionError("network access attempted")
            with mock.patch.object(socket, "create_connection", side_effect=deny), mock.patch.object(
                socket,
                "getaddrinfo",
                side_effect=deny,
            ), mock.patch.object(socket.socket, "connect", side_effect=deny):
                trust_seed_identity.init_identity(seed)
                trust_seed_identity.sign_seed(seed)
                trust_seed_identity.verify_seed(seed)

    def test_private_key_never_appears_in_cli_output_or_public_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))

            init_result = self.run_cli("init_trust_identity.py", seed)
            self.assertEqual(init_result.returncode, 0, init_result.stderr)

            private_pem = trust_seed_identity.private_key_path(seed).read_text(encoding="utf-8")
            self.assertNotIn("PRIVATE KEY", init_result.stdout)
            self.assertNotIn("PRIVATE KEY", init_result.stderr)
            self.assertNotIn(private_pem, init_result.stdout)
            self.assertNotIn(private_pem, init_result.stderr)

            sign_result = self.run_cli("sign_trust_seed.py", seed)
            verify_result = self.run_cli("verify_trust_seed.py", seed)
            self.assertEqual(sign_result.returncode, 0, sign_result.stderr)
            self.assertEqual(verify_result.returncode, 0, verify_result.stderr)

            provenance_text = trust_seed_identity.provenance_path(seed).read_text(encoding="utf-8")
            public_identity_text = trust_seed_identity.public_identity_path(seed).read_text(encoding="utf-8")
            self.assertNotIn("PRIVATE KEY", sign_result.stdout + sign_result.stderr)
            self.assertNotIn("PRIVATE KEY", verify_result.stdout + verify_result.stderr)
            self.assertNotIn("BEGIN PRIVATE KEY", provenance_text)
            self.assertNotIn("BEGIN PRIVATE KEY", public_identity_text)

    def test_init_failure_cleans_up_partial_identity_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            seed = self.create_seed(Path(tmpdir))

            with mock.patch.object(
                trust_seed_identity,
                "public_identity_record",
                side_effect=RuntimeError("boom"),
            ):
                with self.assertRaises(RuntimeError):
                    trust_seed_identity.init_identity(seed)

            self.assertFalse((seed / trust_seed_identity.LOCAL_STATE_DIR).exists())
            leftovers = list(seed.glob(".trust-seed-local.tmp-*"))
            self.assertEqual(leftovers, [])

    def test_verify_path_argument_rejects_parent_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            nested = root / "nested"
            nested.mkdir()

            with self.assertRaises(SystemExit) as exc:
                trust_seed_identity.resolve_cli_seed_path("../seed", working_root=nested)

            self.assertIn("escapes the working location", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
