from __future__ import annotations

import json
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "manifests" / "federation.manifest.json"
RESEARCH_SCRIPTS_PATH = ROOT / "research" / "aethercore-test-001" / "scripts"


def fail(message: str) -> None:
    raise SystemExit(message)


def require_object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def validate_declared_path(
    root: Path,
    raw_path: object,
    label: str,
    *,
    expect_directory: bool,
) -> None:
    if not isinstance(raw_path, str) or not raw_path:
        fail(f"{label} must be a non-empty string path")
    if "\\" in raw_path or ":" in raw_path:
        fail(f"{label} must use a relative POSIX path: {raw_path}")

    path = PurePosixPath(raw_path)
    if path.is_absolute() or ".." in path.parts or "." in path.parts or not path.parts:
        fail(f"{label} escapes the repository: {raw_path}")

    current = root.resolve()
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            fail(f"{label} uses a symlinked path: {raw_path}")
        if not current.exists():
            fail(f"{label} is missing: {raw_path}")

    resolved = current.resolve()
    if not resolved.is_relative_to(root.resolve()):
        fail(f"{label} escapes the repository: {raw_path}")
    if expect_directory and not resolved.is_dir():
        fail(f"{label} must be a directory: {raw_path}")
    if not expect_directory and not resolved.is_file():
        fail(f"{label} must be a file: {raw_path}")


def validate_manifest(
    root: Path = ROOT,
    manifest_path: Path = MANIFEST_PATH,
) -> int:
    if not manifest_path.is_file():
        fail(f"Manifest is missing: {manifest_path.relative_to(root)}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Manifest is not valid JSON: {exc}")

    manifest_object = require_object(manifest, "manifest")
    trust_seed_pattern = require_object(
        manifest_object.get("trustSeedPattern"),
        "trustSeedPattern",
    )
    canonical_documents = require_object(
        manifest_object.get("canonicalDocuments"),
        "canonicalDocuments",
    )

    if manifest_object.get("kind") != "federation-manifest":
        fail("Manifest kind must be federation-manifest")
    if trust_seed_pattern.get("localFirst") is not True:
        fail("trustSeedPattern.localFirst must be true")
    if trust_seed_pattern.get("federationOptional") is not True:
        fail("trustSeedPattern.federationOptional must be true")
    if trust_seed_pattern.get("privacyDefault") != "local-private":
        fail('trustSeedPattern.privacyDefault must be "local-private"')

    for label, raw_path in canonical_documents.items():
        validate_declared_path(root, raw_path, label, expect_directory=False)
    validate_declared_path(
        root,
        trust_seed_pattern.get("templatePath"),
        "trustSeedPattern.templatePath",
        expect_directory=True,
    )

    return len(canonical_documents) + 1


def iter_research_script_files(scripts_path: Path) -> list[Path]:
    discovered: list[Path] = []
    pending = [scripts_path]

    while pending:
        current = pending.pop()
        for child in sorted(current.iterdir()):
            if child.is_symlink():
                fail(f"Research scripts path contains a symlink: {child}")
            if child.is_dir():
                pending.append(child)
                continue
            if child.is_file() and child.suffix == ".py":
                discovered.append(child)

    return discovered


def validate_research_scripts(
    root: Path = ROOT,
    scripts_path: Path = RESEARCH_SCRIPTS_PATH,
) -> int:
    if not scripts_path.is_dir():
        fail(f"Research scripts directory is missing: {scripts_path.relative_to(root)}")

    python_files = iter_research_script_files(scripts_path)
    if not python_files:
        fail(f"No research scripts found in {scripts_path.relative_to(root)}")

    for script_path in python_files:
        relative_path = script_path.relative_to(root)
        try:
            source = script_path.read_text(encoding="utf-8")
            compile(source, str(relative_path), "exec")
        except SyntaxError as exc:
            fail(
                f"Research script compilation failed for {relative_path}: "
                f"{exc.msg} (line {exc.lineno})"
            )

    return len(python_files)


def main() -> None:
    validated_paths = validate_manifest()
    print(f"Validated {validated_paths} declared doctrine paths")
    compiled_scripts = validate_research_scripts()
    print(
        "Compiled "
        f"{compiled_scripts} research scripts in {RESEARCH_SCRIPTS_PATH.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
