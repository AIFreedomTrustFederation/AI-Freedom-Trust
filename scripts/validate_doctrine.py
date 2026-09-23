from __future__ import annotations

import compileall
import json
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "manifests" / "federation.manifest.json"
RESEARCH_SCRIPTS_PATH = ROOT / "research" / "aethercore-test-001" / "scripts"


def validate_manifest() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    assert manifest["kind"] == "federation-manifest"
    assert manifest["trustSeedPattern"]["localFirst"] is True
    assert manifest["trustSeedPattern"]["federationOptional"] is True
    assert manifest["trustSeedPattern"]["privacyDefault"] == "local-private"

    declared = {
        **manifest["canonicalDocuments"],
        "trustSeedPattern": manifest["trustSeedPattern"]["templatePath"],
    }
    for label, raw_path in declared.items():
        path = PurePosixPath(raw_path)
        assert not path.is_absolute() and ".." not in path.parts, (
            f"{label} escapes the repository: {raw_path}"
        )
        target = ROOT.joinpath(*path.parts)
        assert target.exists(), f"{label} is missing: {raw_path}"

    return len(declared)


def validate_research_scripts() -> None:
    compiled = compileall.compile_dir(
        str(RESEARCH_SCRIPTS_PATH),
        quiet=1,
    )
    if not compiled:
        raise SystemExit("Research script compilation failed.")


def main() -> None:
    validated_paths = validate_manifest()
    print(f"Validated {validated_paths} declared doctrine paths")
    validate_research_scripts()
    print(f"Compiled research scripts in {RESEARCH_SCRIPTS_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
