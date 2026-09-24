from __future__ import annotations

import base64
import binascii
import json
import os
import shutil
import tempfile
from pathlib import Path, PurePosixPath

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


REQUIRED_DOCUMENTS = {
    "trust": "TRUST.md",
    "treeOfLife": "TREE_OF_LIFE.md",
    "governance": "GOVERNANCE.md",
    "economy": "ECONOMY.md",
    "aiSteward": "AI_STEWARD.md",
    "map": "MAP.md",
}
LOCAL_STATE_DIR = ".trust-seed-local"
IDENTITY_DIR = "identity"
PROVENANCE_DIR = "provenance"
PRIVATE_KEY_FILE = "private_key.pem"
PUBLIC_IDENTITY_FILE = "public_identity.json"
PROVENANCE_FILE = "trust-seed-provenance.json"
SIGNED_STATE_SCHEMA = (
    "https://aifreedomtrustfederation.org/schemas/trust-seed-signed-state.v0.json"
)
PUBLIC_IDENTITY_SCHEMA = (
    "https://aifreedomtrustfederation.org/schemas/trust-seed-public-identity.v0.json"
)
PROVENANCE_SCHEMA = (
    "https://aifreedomtrustfederation.org/schemas/trust-seed-provenance.v0.json"
)
CANONICALIZATION_ALGORITHM = "json-sort-keys-utf8-v1"
SIGNING_ALGORITHM = "ed25519"
CONTENT_DIGEST_ALGORITHM = "sha256"
PRIVATE_FILE_MODE = 0o600
PRIVATE_DIR_MODE = 0o700


def fail(message: str) -> None:
    raise SystemExit(message)


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize().hex()


def read_text_utf8(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{label} is not valid UTF-8: {path} ({exc})")


def load_json_object(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(read_text_utf8(path, label))
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
        fail(f"{label} escapes the trust seed: {raw_path}")
    return path


def resolve_cli_seed_path(seed_path: Path | str, working_root: Path | None = None) -> Path:
    raw_path = str(seed_path)
    if not raw_path:
        fail("Trust seed path must be provided")
    if "\\" in raw_path:
        fail(f"Trust seed path must not use backslashes: {raw_path}")

    root = (Path.cwd() if working_root is None else working_root).resolve()
    candidate = Path(raw_path)
    current = Path(candidate.anchor) if candidate.is_absolute() else root

    for part in candidate.parts:
        if part in ("", candidate.anchor, "."):
            continue
        if part == "..":
            fail(f"Trust seed path escapes the working location: {raw_path}")
        current = current / part
        if current.is_symlink():
            fail(f"Trust seed path uses a symlinked component: {raw_path}")

    resolved = current.resolve(strict=False)
    if not resolved.exists():
        fail(f"Trust seed directory is missing: {resolved}")
    if resolved.is_symlink():
        fail(f"Trust seed directory must not be a symlink: {resolved}")
    if not resolved.is_dir():
        fail(f"Trust seed path must be a directory: {resolved}")
    return resolved


def validate_child_path(seed_dir: Path, raw_path: object, label: str) -> Path:
    relative_path = validate_relative_posix_path(raw_path, label)
    current = seed_dir.resolve()
    for part in relative_path.parts:
        current = current / part
        if current.is_symlink():
            fail(f"{label} uses a symlinked path: {raw_path}")
        if not current.exists():
            fail(f"{label} is missing: {raw_path}")

    resolved = current.resolve()
    if not resolved.is_relative_to(seed_dir.resolve()):
        fail(f"{label} escapes the trust seed: {raw_path}")
    if not resolved.is_file():
        fail(f"{label} must be a file: {raw_path}")
    return resolved


def validate_seed_manifest(manifest: dict[str, object]) -> None:
    if manifest.get("kind") != "trust-seed":
        fail("Trust seed manifest kind must be trust-seed")
    if manifest.get("status") != "local-draft":
        fail('Trust seed manifest status must be "local-draft"')
    if not isinstance(manifest.get("version"), str) or not manifest["version"]:
        fail("Trust seed manifest version must be a non-empty string")

    trust = manifest.get("trust")
    if not isinstance(trust, dict):
        fail("Trust seed manifest trust section must be an object")
    if trust.get("visibility") != "private-by-default":
        fail('Trust seed trust.visibility must be "private-by-default"')

    holographic_pattern = manifest.get("holographicPattern")
    if not isinstance(holographic_pattern, dict):
        fail("Trust seed manifest holographicPattern section must be an object")
    for key in (
        "containsFederationPattern",
        "localFirst",
        "offlineFirstGoal",
        "federationOptional",
    ):
        if holographic_pattern.get(key) is not True:
            fail(f"Trust seed holographicPattern.{key} must be true")

    privacy = manifest.get("privacy")
    if not isinstance(privacy, dict):
        fail("Trust seed manifest privacy section must be an object")
    if privacy.get("defaultDataState") != "local-private":
        fail('Trust seed privacy.defaultDataState must be "local-private"')
    if privacy.get("publicProfile") is not False:
        fail("Trust seed privacy.publicProfile must be false")
    if not isinstance(privacy.get("sharedWithFederation"), list):
        fail("Trust seed privacy.sharedWithFederation must be a list")

    federation_link = manifest.get("federationLink")
    if not isinstance(federation_link, dict):
        fail("Trust seed manifest federationLink section must be an object")
    if federation_link.get("enabled") is not False:
        fail("Trust seed federationLink.enabled must be false")
    if federation_link.get("publicNode") is not False:
        fail("Trust seed federationLink.publicNode must be false")
    if federation_link.get("syncPolicy") != "explicit-consent-only":
        fail('Trust seed federationLink.syncPolicy must be "explicit-consent-only"')

    documents = manifest.get("documents")
    if not isinstance(documents, dict):
        fail("Trust seed manifest documents section must be an object")
    if set(documents) != set(REQUIRED_DOCUMENTS):
        fail("Trust seed manifest documents must match the canonical template")

    for label, expected_path in REQUIRED_DOCUMENTS.items():
        raw_path = documents.get(label)
        validate_relative_posix_path(raw_path, f"documents.{label}")
        if raw_path != expected_path:
            fail(f"Trust seed documents.{label} must point to {expected_path}")


def validate_existing_seed(seed_dir: Path) -> dict[str, object]:
    manifest_path = validate_child_path(seed_dir, "LOCAL_MANIFEST.json", "LOCAL_MANIFEST.json")
    manifest = load_json_object(manifest_path, "Trust seed LOCAL_MANIFEST.json")
    validate_seed_manifest(manifest)

    documents = manifest["documents"]
    assert isinstance(documents, dict)
    for label, raw_path in documents.items():
        document_path = validate_child_path(seed_dir, raw_path, f"documents.{label}")
        read_text_utf8(document_path, f"documents.{label}")

    return manifest


def local_state_root(seed_dir: Path) -> Path:
    root = seed_dir / LOCAL_STATE_DIR
    if root.is_symlink():
        fail(f"Local state directory must not be a symlink: {root}")
    return root


def private_key_path(seed_dir: Path) -> Path:
    path = local_state_root(seed_dir) / IDENTITY_DIR / PRIVATE_KEY_FILE
    if path.is_symlink():
        fail(f"Private key path must not be a symlink: {path}")
    return path


def public_identity_path(seed_dir: Path) -> Path:
    path = local_state_root(seed_dir) / IDENTITY_DIR / PUBLIC_IDENTITY_FILE
    if path.is_symlink():
        fail(f"Public identity path must not be a symlink: {path}")
    return path


def provenance_path(seed_dir: Path) -> Path:
    path = local_state_root(seed_dir) / PROVENANCE_DIR / PROVENANCE_FILE
    if path.is_symlink():
        fail(f"Provenance path must not be a symlink: {path}")
    return path


def enforce_private_permissions(path: Path) -> None:
    if os.name == "nt":
        return
    path.chmod(PRIVATE_FILE_MODE)


def enforce_private_directory_permissions(path: Path) -> None:
    if os.name == "nt":
        return
    path.chmod(PRIVATE_DIR_MODE)


def public_identity_record(public_key: Ed25519PublicKey) -> dict[str, object]:
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return {
        "schema": PUBLIC_IDENTITY_SCHEMA,
        "kind": "trust-seed-public-identity",
        "version": "0.1.0",
        "algorithm": SIGNING_ALGORITHM,
        "publicKey": {
            "format": "base64-raw",
            "value": base64.b64encode(public_bytes).decode("ascii"),
        },
        "keyId": f"{CONTENT_DIGEST_ALGORITHM}:{sha256_hex(public_bytes)}",
    }


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.tmp-",
        delete=False,
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        temp_path.replace(path)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise


def load_private_key(seed_dir: Path) -> Ed25519PrivateKey:
    path = private_key_path(seed_dir)
    if not path.is_file():
        fail(f"Private key is missing: {path}")
    try:
        key = serialization.load_pem_private_key(
            path.read_bytes(),
            None,
        )
    except ValueError as exc:
        fail(f"Private key is invalid: {exc}")
    if not isinstance(key, Ed25519PrivateKey):
        fail("Private key must be Ed25519")
    return key

def load_public_key_from_record(record: dict[str, object]) -> Ed25519PublicKey:
    if record.get("algorithm") != SIGNING_ALGORITHM:
        fail(f"Unsupported verification algorithm: {record.get('algorithm')}")

    public_key = record.get("publicKey")
    if not isinstance(public_key, dict):
        fail("Public identity publicKey must be an object")
    if public_key.get("format") != "base64-raw":
        fail("Public identity publicKey.format must be base64-raw")
    value = public_key.get("value")
    if not isinstance(value, str) or not value:
        fail("Public identity publicKey.value must be a non-empty string")
    try:
        public_bytes = base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error):  # type: ignore[name-defined]
        fail("Public identity publicKey.value must be valid base64")
    if len(public_bytes) != 32:
        fail("Public identity public key must be 32 bytes")
    expected_key_id = f"{CONTENT_DIGEST_ALGORITHM}:{sha256_hex(public_bytes)}"
    if record.get("keyId") != expected_key_id:
        fail("Public identity keyId does not match the public key")
    try:
        return Ed25519PublicKey.from_public_bytes(public_bytes)
    except ValueError as exc:
        fail(f"Public identity public key is invalid: {exc}")


def manifest_canonical_digest(seed_dir: Path) -> tuple[dict[str, object], str]:
    manifest_path = validate_child_path(seed_dir, "LOCAL_MANIFEST.json", "LOCAL_MANIFEST.json")
    manifest = load_json_object(manifest_path, "Trust seed LOCAL_MANIFEST.json")
    validate_seed_manifest(manifest)
    digest = sha256_hex(canonical_json_bytes(manifest))
    return manifest, digest


def build_signed_state(seed_dir: Path) -> dict[str, object]:
    manifest, manifest_digest = manifest_canonical_digest(seed_dir)
    documents = manifest["documents"]
    assert isinstance(documents, dict)

    signed_documents: dict[str, object] = {}
    for label in sorted(REQUIRED_DOCUMENTS):
        raw_path = documents[label]
        document_path = validate_child_path(seed_dir, raw_path, f"documents.{label}")
        content = read_text_utf8(document_path, f"documents.{label}").encode("utf-8")
        signed_documents[label] = {
            "path": str(raw_path),
            "sha256": sha256_hex(content),
        }

    return {
        "schema": SIGNED_STATE_SCHEMA,
        "kind": "trust-seed-signed-state",
        "version": "0.1.0",
        "canonicalization": CANONICALIZATION_ALGORITHM,
        "manifest": {
            "path": "LOCAL_MANIFEST.json",
            "canonicalJsonSha256": manifest_digest,
        },
        "documents": signed_documents,
    }


def init_identity(seed_dir: Path) -> dict[str, object]:
    validate_existing_seed(seed_dir)
    state_root = local_state_root(seed_dir)
    if state_root.exists():
        fail(f"Local identity already exists: {state_root}")

    staging_root = Path(tempfile.mkdtemp(prefix=".trust-seed-local.tmp-", dir=seed_dir))
    try:
        identity_dir = staging_root / IDENTITY_DIR
        provenance_dir = staging_root / PROVENANCE_DIR
        identity_dir.mkdir()
        provenance_dir.mkdir()
        enforce_private_directory_permissions(staging_root)
        enforce_private_directory_permissions(identity_dir)
        enforce_private_directory_permissions(provenance_dir)

        private_key = Ed25519PrivateKey.generate()
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        private_path = identity_dir / PRIVATE_KEY_FILE
        private_path.write_bytes(private_key_bytes)
        enforce_private_permissions(private_path)

        public_record = public_identity_record(private_key.public_key())
        (identity_dir / PUBLIC_IDENTITY_FILE).write_text(
            json.dumps(public_record, indent=2) + "\n",
            encoding="utf-8",
        )

        staging_root.rename(state_root)
    except BaseException:
        shutil.rmtree(staging_root, ignore_errors=True)
        raise

    return public_record


def sign_seed(seed_dir: Path) -> dict[str, object]:
    validate_existing_seed(seed_dir)
    private_key = load_private_key(seed_dir)
    public_record = public_identity_record(private_key.public_key())
    signed_state = build_signed_state(seed_dir)
    canonical_bytes = canonical_json_bytes(signed_state)
    signature = private_key.sign(canonical_bytes)

    record = {
        "schema": PROVENANCE_SCHEMA,
        "kind": "trust-seed-provenance",
        "version": "0.1.0",
        "signedState": signed_state,
        "contentDigest": {
            "algorithm": CONTENT_DIGEST_ALGORITHM,
            "value": sha256_hex(canonical_bytes),
        },
        "verification": public_record,
        "signature": {
            "format": "base64",
            "value": base64.b64encode(signature).decode("ascii"),
        },
    }

    output_path = provenance_path(seed_dir)
    atomic_write_text(output_path, json.dumps(record, indent=2) + "\n")
    return record


def load_provenance(seed_dir: Path) -> dict[str, object]:
    path = provenance_path(seed_dir)
    if not path.is_file():
        fail(f"Trust seed provenance is missing: {path}")
    record = load_json_object(path, "Trust seed provenance")
    if record.get("schema") != PROVENANCE_SCHEMA:
        fail("Trust seed provenance schema is invalid")
    if record.get("kind") != "trust-seed-provenance":
        fail("Trust seed provenance kind is invalid")
    if record.get("version") != "0.1.0":
        fail("Trust seed provenance version is invalid")

    signed_state = record.get("signedState")
    if not isinstance(signed_state, dict):
        fail("Trust seed provenance signedState must be an object")
    if signed_state.get("schema") != SIGNED_STATE_SCHEMA:
        fail("Trust seed provenance signedState schema is invalid")
    if signed_state.get("kind") != "trust-seed-signed-state":
        fail("Trust seed provenance signedState kind is invalid")
    if signed_state.get("version") != "0.1.0":
        fail("Trust seed provenance signedState version is invalid")
    if signed_state.get("canonicalization") != CANONICALIZATION_ALGORITHM:
        fail("Trust seed provenance canonicalization is invalid")

    manifest = signed_state.get("manifest")
    if not isinstance(manifest, dict):
        fail("Trust seed provenance manifest summary must be an object")
    if manifest.get("path") != "LOCAL_MANIFEST.json":
        fail("Trust seed provenance manifest path is invalid")
    if not isinstance(manifest.get("canonicalJsonSha256"), str) or not manifest["canonicalJsonSha256"]:
        fail("Trust seed provenance manifest digest is invalid")

    documents = signed_state.get("documents")
    if not isinstance(documents, dict) or set(documents) != set(REQUIRED_DOCUMENTS):
        fail("Trust seed provenance documents are invalid")
    for label, expected_path in REQUIRED_DOCUMENTS.items():
        entry = documents.get(label)
        if not isinstance(entry, dict):
            fail(f"Trust seed provenance documents.{label} must be an object")
        if entry.get("path") != expected_path:
            fail(f"Trust seed provenance documents.{label}.path is invalid")
        if not isinstance(entry.get("sha256"), str) or not entry["sha256"]:
            fail(f"Trust seed provenance documents.{label}.sha256 is invalid")

    content_digest = record.get("contentDigest")
    if not isinstance(content_digest, dict):
        fail("Trust seed provenance contentDigest must be an object")
    if content_digest.get("algorithm") != CONTENT_DIGEST_ALGORITHM:
        fail("Trust seed provenance contentDigest.algorithm is invalid")
    if not isinstance(content_digest.get("value"), str) or not content_digest["value"]:
        fail("Trust seed provenance contentDigest.value is invalid")

    verification = record.get("verification")
    if not isinstance(verification, dict):
        fail("Trust seed provenance verification must be an object")
    if verification.get("schema") != PUBLIC_IDENTITY_SCHEMA:
        fail("Trust seed provenance verification schema is invalid")
    if verification.get("kind") != "trust-seed-public-identity":
        fail("Trust seed provenance verification kind is invalid")
    if verification.get("version") != "0.1.0":
        fail("Trust seed provenance verification version is invalid")

    signature = record.get("signature")
    if not isinstance(signature, dict):
        fail("Trust seed provenance signature must be an object")
    if signature.get("format") != "base64":
        fail("Trust seed provenance signature.format is invalid")
    if not isinstance(signature.get("value"), str) or not signature["value"]:
        fail("Trust seed provenance signature.value is invalid")

    return record


def verify_seed(seed_dir: Path) -> dict[str, object]:
    validate_existing_seed(seed_dir)
    provenance = load_provenance(seed_dir)
    current_state = build_signed_state(seed_dir)
    recorded_state = provenance["signedState"]
    assert isinstance(recorded_state, dict)

    if current_state != recorded_state:
        fail("Trust seed state does not match the recorded provenance")

    canonical_bytes = canonical_json_bytes(current_state)
    expected_digest = sha256_hex(canonical_bytes)
    content_digest = provenance["contentDigest"]
    assert isinstance(content_digest, dict)
    if content_digest["value"] != expected_digest:
        fail("Trust seed provenance digest does not match the current signed state")

    verification = provenance["verification"]
    assert isinstance(verification, dict)
    public_key = load_public_key_from_record(verification)

    signature = provenance["signature"]
    assert isinstance(signature, dict)
    try:
        signature_bytes = base64.b64decode(signature["value"], validate=True)
    except ValueError:
        fail("Trust seed provenance signature must be valid base64")

    try:
        public_key.verify(signature_bytes, canonical_bytes)
    except InvalidSignature:
        fail("Trust seed provenance signature verification failed")

    return provenance


def print_init_result(seed_dir: Path, record: dict[str, object]) -> None:
    print(f"Initialized local trust identity at {seed_dir / LOCAL_STATE_DIR}")
    print(f"Public verification identity: {record['keyId']}")


def print_sign_result(seed_dir: Path, record: dict[str, object]) -> None:
    digest = record["contentDigest"]["value"]  # type: ignore[index]
    print(f"Signed trust seed state at {provenance_path(seed_dir)}")
    print(f"Signed content digest: {digest}")


def print_verify_result(seed_dir: Path, record: dict[str, object]) -> None:
    key_id = record["verification"]["keyId"]  # type: ignore[index]
    print(f"Verified trust seed state at {seed_dir}")
    print(f"Verification identity: {key_id}")
