from __future__ import annotations

import argparse
import json
import shutil
import stat
import tempfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "templates" / "trust-seed"
REQUIRED_DOCUMENTS = {
    "trust": "TRUST.md",
    "treeOfLife": "TREE_OF_LIFE.md",
    "governance": "GOVERNANCE.md",
    "economy": "ECONOMY.md",
    "aiSteward": "AI_STEWARD.md",
    "map": "MAP.md",
}
REQUIRED_TEMPLATE_FILES = (
    "README.md",
    "TRUST.md",
    "TREE_OF_LIFE.md",
    "GOVERNANCE.md",
    "ECONOMY.md",
    "AI_STEWARD.md",
    "MAP.md",
    "LOCAL_MANIFEST.json",
)
EXECUTABLE_BITS = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH


def fail(message: str) -> None:
    raise SystemExit(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Instantiate a local trust seed from the canonical template.",
    )
    parser.add_argument(
        "destination",
        nargs="?",
        default="local-trust-seed",
        help="Relative directory to create under the current working directory.",
    )
    return parser.parse_args()


def read_text_utf8(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{label} is not valid UTF-8: {path} ({exc})")


def load_json_object(path: Path, label: str) -> dict[str, object]:
    source = read_text_utf8(path, label)
    try:
        value = json.loads(source)
    except json.JSONDecodeError as exc:
        fail(f"{label} is not valid JSON: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must contain a JSON object")
    return value


def validate_relative_posix_path(raw_path: object, label: str) -> PurePosixPath:
    if not isinstance(raw_path, str) or not raw_path:
        fail(f"{label} must be a non-empty string path")
    if "\\" in raw_path or ":" in raw_path:
        fail(f"{label} must use a relative POSIX path: {raw_path}")

    path = PurePosixPath(raw_path)
    if path.is_absolute() or ".." in path.parts or "." in path.parts or not path.parts:
        fail(f"{label} escapes the intended working location: {raw_path}")
    return path


def is_executable_file(path: Path) -> bool:
    return bool(path.stat().st_mode & EXECUTABLE_BITS)


def validate_flat_text_tree(directory: Path, label: str) -> None:
    if not directory.is_dir():
        fail(f"{label} is missing: {directory}")

    discovered_names: set[str] = set()
    for child in sorted(directory.iterdir()):
        if child.is_symlink():
            fail(f"{label} contains a symlinked entry: {child.name}")
        if child.name.startswith("."):
            fail(f"{label} contains a hidden entry: {child.name}")
        if child.is_dir():
            fail(f"{label} contains a nested directory: {child.name}")
        if not child.is_file():
            fail(f"{label} contains a non-file entry: {child.name}")
        if child.name not in REQUIRED_TEMPLATE_FILES:
            fail(f"{label} contains an unexpected file: {child.name}")
        if is_executable_file(child):
            fail(f"{label} contains an executable file: {child.name}")
        read_text_utf8(child, f"{label} file")
        discovered_names.add(child.name)

    expected_names = set(REQUIRED_TEMPLATE_FILES)
    if discovered_names != expected_names:
        missing = sorted(expected_names - discovered_names)
        extra = sorted(discovered_names - expected_names)
        details: list[str] = []
        if missing:
            details.append(f"missing {', '.join(missing)}")
        if extra:
            details.append(f"unexpected {', '.join(extra)}")
        fail(f"{label} has an invalid file set: {'; '.join(details)}")


def validate_document_paths(seed_dir: Path, documents: dict[str, object]) -> None:
    if set(documents) != set(REQUIRED_DOCUMENTS):
        fail("Generated trust seed manifest documents must match the canonical template")

    for manifest_label, expected_path in REQUIRED_DOCUMENTS.items():
        raw_path = documents[manifest_label]
        relative_path = validate_relative_posix_path(raw_path, f"documents.{manifest_label}")
        if raw_path != expected_path:
            fail(
                f"documents.{manifest_label} must point to the canonical file: {expected_path}"
            )
        current = seed_dir.resolve()
        for part in relative_path.parts:
            current = current / part
            if current.is_symlink():
                fail(f"documents.{manifest_label} uses a symlinked path: {raw_path}")
            if not current.exists():
                fail(f"documents.{manifest_label} is missing: {raw_path}")

        resolved = current.resolve()
        if not resolved.is_relative_to(seed_dir.resolve()):
            fail(f"documents.{manifest_label} escapes the generated trust seed: {raw_path}")
        if not resolved.is_file():
            fail(f"documents.{manifest_label} must be a file: {raw_path}")


def validate_manifest_structure(
    manifest: dict[str, object],
    *,
    expected_status: str,
) -> None:
    if manifest.get("kind") != "trust-seed":
        fail("Generated trust seed manifest kind must be trust-seed")
    if manifest.get("status") != expected_status:
        fail(f'Generated trust seed manifest status must be "{expected_status}"')
    if not isinstance(manifest.get("version"), str) or not manifest["version"]:
        fail("Generated trust seed manifest version must be a non-empty string")

    trust = manifest.get("trust")
    if not isinstance(trust, dict):
        fail("Generated trust seed manifest trust section must be an object")
    if trust.get("visibility") != "private-by-default":
        fail('Generated trust seed trust.visibility must be "private-by-default"')
    if not isinstance(trust.get("name"), str) or not trust["name"].strip():
        fail("Generated trust seed trust.name must be non-empty")
    trust_types = trust.get("type")
    if not isinstance(trust_types, list) or not trust_types:
        fail("Generated trust seed trust.type must contain at least one entry")
    if not all(isinstance(item, str) and item.strip() for item in trust_types):
        fail("Generated trust seed trust.type entries must be non-empty strings")
    if not isinstance(trust.get("purpose"), str) or not trust["purpose"].strip():
        fail("Generated trust seed trust.purpose must be non-empty")

    holographic_pattern = manifest.get("holographicPattern")
    if not isinstance(holographic_pattern, dict):
        fail("Generated trust seed manifest holographicPattern section must be an object")
    if holographic_pattern.get("containsFederationPattern") is not True:
        fail("Generated trust seed holographicPattern.containsFederationPattern must be true")
    if holographic_pattern.get("localFirst") is not True:
        fail("Generated trust seed holographicPattern.localFirst must be true")
    if holographic_pattern.get("offlineFirstGoal") is not True:
        fail("Generated trust seed holographicPattern.offlineFirstGoal must be true")
    if holographic_pattern.get("federationOptional") is not True:
        fail("Generated trust seed holographicPattern.federationOptional must be true")

    documents = manifest.get("documents")
    if not isinstance(documents, dict):
        fail("Generated trust seed manifest documents section must be an object")

    privacy = manifest.get("privacy")
    if not isinstance(privacy, dict):
        fail("Generated trust seed manifest privacy section must be an object")
    if privacy.get("defaultDataState") != "local-private":
        fail('Generated trust seed privacy.defaultDataState must be "local-private"')
    if not isinstance(privacy.get("locationPrecision"), str) or not privacy["locationPrecision"].strip():
        fail("Generated trust seed privacy.locationPrecision must be a non-empty string")
    if privacy.get("publicProfile") is not False:
        fail("Generated trust seed privacy.publicProfile must be false")
    shared_with_federation = privacy.get("sharedWithFederation")
    if not isinstance(shared_with_federation, list):
        fail("Generated trust seed privacy.sharedWithFederation must be a list")
    if not all(isinstance(item, str) for item in shared_with_federation):
        fail("Generated trust seed privacy.sharedWithFederation entries must be strings")

    federation_link = manifest.get("federationLink")
    if not isinstance(federation_link, dict):
        fail("Generated trust seed manifest federationLink section must be an object")
    if federation_link.get("enabled") is not False:
        fail("Generated trust seed federationLink.enabled must be false")
    if federation_link.get("publicNode") is not False:
        fail("Generated trust seed federationLink.publicNode must be false")
    if federation_link.get("syncPolicy") != "explicit-consent-only":
        fail('Generated trust seed federationLink.syncPolicy must be "explicit-consent-only"')

    tree_of_life = manifest.get("treeOfLife")
    if not isinstance(tree_of_life, dict):
        fail("Generated trust seed manifest treeOfLife section must be an object")
    for key in ("seed", "roots", "trunk", "branches", "leaves", "fruit", "newSeeds"):
        value = tree_of_life.get(key)
        if not isinstance(value, list):
            fail(f"Generated trust seed treeOfLife.{key} must be a list")

    agent_policy = manifest.get("agentPolicy")
    if not isinstance(agent_policy, dict):
        fail("Generated trust seed manifest agentPolicy section must be an object")
    if agent_policy.get("aiStewardEnabled") is not False:
        fail("Generated trust seed agentPolicy.aiStewardEnabled must be false")
    if not isinstance(agent_policy.get("readScopes"), list):
        fail("Generated trust seed agentPolicy.readScopes must be a list")
    if agent_policy.get("readScopes") != []:
        fail("Generated trust seed agentPolicy.readScopes must default to an empty list")
    if not isinstance(agent_policy.get("writeScopes"), list):
        fail("Generated trust seed agentPolicy.writeScopes must be a list")
    if agent_policy.get("writeScopes") != []:
        fail("Generated trust seed agentPolicy.writeScopes must default to an empty list")
    if agent_policy.get("humanApprovalRequired") is not True:
        fail("Generated trust seed agentPolicy.humanApprovalRequired must be true")


def validate_template_tree(template_dir: Path | None = None) -> None:
    template_dir = TEMPLATE_DIR if template_dir is None else template_dir
    validate_flat_text_tree(template_dir, "Trust seed template")
    manifest = load_json_object(template_dir / "LOCAL_MANIFEST.json", "Template LOCAL_MANIFEST.json")
    validate_manifest_structure(manifest, expected_status="template")
    validate_document_paths(template_dir, manifest["documents"])


def validate_seed_directory(seed_dir: Path) -> None:
    validate_flat_text_tree(seed_dir, "Generated trust seed")
    manifest = load_json_object(seed_dir / "LOCAL_MANIFEST.json", "Generated trust seed LOCAL_MANIFEST.json")
    validate_manifest_structure(manifest, expected_status="local-draft")
    validate_document_paths(seed_dir, manifest["documents"])


def resolve_destination(destination: Path, working_root: Path | None = None) -> Path:
    root = (Path.cwd() if working_root is None else working_root).resolve()
    relative_path = validate_relative_posix_path(str(destination), "Destination path")

    current = root
    for part in relative_path.parts[:-1]:
        current = current / part
        if current.is_symlink():
            fail(f"Destination path uses a symlinked parent: {current}")
        if current.exists() and not current.is_dir():
            fail(f"Destination parent is not a directory: {current}")

    resolved_destination = root.joinpath(*relative_path.parts)
    if resolved_destination.exists() or resolved_destination.is_symlink():
        fail(f"Destination already exists: {resolved_destination}")
    return resolved_destination


def create_trust_seed(
    destination: Path,
    *,
    working_root: Path | None = None,
) -> Path:
    validate_template_tree()

    final_destination = resolve_destination(destination, working_root=working_root)
    final_destination.parent.mkdir(parents=True, exist_ok=True)
    staging_directory = Path(
        tempfile.mkdtemp(
            prefix=f".{final_destination.name}.tmp-",
            dir=final_destination.parent,
        )
    )

    try:
        for file_name in REQUIRED_TEMPLATE_FILES:
            shutil.copy2(TEMPLATE_DIR / file_name, staging_directory / file_name)

        manifest_path = staging_directory / "LOCAL_MANIFEST.json"
        manifest = load_json_object(manifest_path, "Template LOCAL_MANIFEST.json")
        manifest["status"] = "local-draft"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        validate_seed_directory(staging_directory)
        staging_directory.rename(final_destination)
    except BaseException:
        shutil.rmtree(staging_directory, ignore_errors=True)
        raise

    return final_destination.resolve()


def main() -> None:
    args = parse_args()
    destination = create_trust_seed(Path(args.destination))
    print(f"Created trust seed at {destination}")


if __name__ == "__main__":
    main()
