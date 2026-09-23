from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = REPO_ROOT / "scripts" / "create_trust_seed.py"
MODULE_SPEC = importlib.util.spec_from_file_location("create_trust_seed", MODULE_PATH)
assert MODULE_SPEC and MODULE_SPEC.loader
create_trust_seed = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(create_trust_seed)


class CreateTrustSeedTests(unittest.TestCase):
    def test_creates_private_by_default_seed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "oak-garden-trust"
            created = create_trust_seed.create_trust_seed(destination)

            self.assertEqual(created, destination.resolve())

            manifest = json.loads((created / "LOCAL_MANIFEST.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "local-draft")
            self.assertEqual(manifest["trust"]["name"], "Oak Garden Trust")
            self.assertEqual(manifest["trust"]["type"], ["Individual trust"])
            self.assertEqual(
                manifest["trust"]["purpose"],
                "Steward the local trust seed for Oak Garden Trust.",
            )
            self.assertEqual(manifest["privacy"]["defaultDataState"], "local-private")
            self.assertFalse(manifest["privacy"]["publicProfile"])
            self.assertEqual(manifest["privacy"]["locationPrecision"], "private only")
            self.assertEqual(manifest["privacy"]["sharedWithFederation"], [])
            self.assertFalse(manifest["federationLink"]["enabled"])
            self.assertFalse(manifest["federationLink"]["publicNode"])
            self.assertEqual(manifest["federationLink"]["syncPolicy"], "explicit-consent-only")
            self.assertTrue(manifest["agentPolicy"]["humanApprovalRequired"])

            for file_name in create_trust_seed.REQUIRED_TEMPLATE_FILES:
                content = (created / file_name).read_text(encoding="utf-8")
                self.assertNotIn("TODO", content, file_name)

    def test_supports_custom_values_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination_one = Path(tmpdir) / "seed-one"
            destination_two = Path(tmpdir) / "seed-two"

            create_trust_seed.create_trust_seed(
                destination_one,
                name="Harbor Commons",
                trust_types=["Community trust", "Project trust"],
                purpose="Steward the Harbor Commons local mission.",
                primary_steward="Harbor steward circle",
                location_precision="city-level",
            )
            create_trust_seed.create_trust_seed(
                destination_two,
                name="Harbor Commons",
                trust_types=["Community trust", "Project trust"],
                purpose="Steward the Harbor Commons local mission.",
                primary_steward="Harbor steward circle",
                location_precision="city-level",
            )

            for file_name in create_trust_seed.REQUIRED_TEMPLATE_FILES:
                self.assertEqual(
                    (destination_one / file_name).read_text(encoding="utf-8"),
                    (destination_two / file_name).read_text(encoding="utf-8"),
                    file_name,
                )

    def test_rejects_non_empty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "occupied"
            destination.mkdir()
            (destination / "placeholder.txt").write_text("occupied\n", encoding="utf-8")

            with self.assertRaises(SystemExit) as exc:
                create_trust_seed.create_trust_seed(destination)

            self.assertIn("Destination already exists and is not empty", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
