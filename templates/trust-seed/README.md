# Trust Seed Template

This folder is the canonical starter pattern for a new AI Freedom Trust Federation trust.

A trust seed is not merely an account. It is a local, sovereign, inspectable copy of the Federation pattern, scaled to one person, family, business, ministry, cooperative, community, repository, or project.

## What This Seed Contains

- `TRUST.md`: the trust identity, purpose, boundaries, and stewardship commitments.
- `TREE_OF_LIFE.md`: roots, trunk, branches, leaves, fruit, and future seeds.
- `GOVERNANCE.md`: local decision rules, consent process, stewardship roles, and dispute paths.
- `ECONOMY.md`: contribution, value flow, bounties, grants, services, assets, and compliance boundaries.
- `AI_STEWARD.md`: local AI assistant rules, permissions, and safety boundaries.
- `MAP.md`: Living Atlas and local Green Zone specification.
- `LOCAL_MANIFEST.json`: machine-readable trust seed metadata.

## Local-First Rule

This seed should be usable as a local folder, a Git repository, a Mobox workspace, a Forge repository, or a federated node.

Private data stays local by default. Federation is voluntary and permissioned.

## Local Bootstrap

Instantiate a private-by-default local seed from this canonical template with:

```bash
python scripts/create_trust_seed.py
```

The bootstrap creates a local draft without resolving identity, governance, publication, or other human decisions for the steward.

## Local Cryptographic Identity And Provenance

This milestone adds local-only cryptographic identity and provenance for an already valid trust seed.

Initialize identity:

```bash
python scripts/init_trust_identity.py ./my-trust
```

Sign the canonical local trust-seed state:

```bash
python scripts/sign_trust_seed.py ./my-trust
```

Verify locally and offline:

```bash
python scripts/verify_trust_seed.py ./my-trust
```

### What Gets Signed

The signed state is a deterministic canonical JSON object containing:

- the canonical JSON digest of `LOCAL_MANIFEST.json`;
- the SHA-256 digest of each canonical document declared in `documents`;
- the canonicalization and schema/version metadata needed to reproduce the same bytes.

Filesystem timestamps, mtimes, ownership, permissions, Git metadata, networking state, and other host metadata are not signed.

### Local Storage Separation

- Private key: `.trust-seed-local/identity/private_key.pem`
- Public verification material: `.trust-seed-local/identity/public_identity.json`
- Provenance record: `.trust-seed-local/provenance/trust-seed-provenance.json`

Private key material is generated locally, kept local, never embedded in public manifests, never required for verification, and never silently regenerated if identity already exists.

### Primitive And Dependency Choice

This implementation uses Ed25519 from the Python `cryptography` library.

- Ed25519 is a modern, widely reviewed signing primitive with deterministic signatures.
- `cryptography` is a mature, broadly maintained library with licensing compatible with this repository and offline local use.
- No custom cryptographic primitive is introduced here.

### Minimal Threat Model

This milestone helps detect:

- accidental local modification of the manifest or signed documents;
- malicious local modification by someone who does not control the private key;
- corrupted provenance, signature, or public verification material.

This milestone does **not** solve:

- private-key theft;
- a compromised local machine;
- rollback to an older but still valid signed state;
- identity recovery;
- multi-device identity coordination;
- federation trust, publication, discovery, or synchronization.

## First Setup Questions

1. What is the trust name?
2. Who or what does this trust steward?
3. What are its values?
4. What is private, shared, or public?
5. What is its local Green Zone?
6. What are its roots, trunk, branches, leaves, fruit, and future seeds?
7. What may the AI steward read, write, summarize, or suggest?
8. What may this trust optionally publish to the Federation?

## Constitutional Pattern

The whole Federation pattern is present here in miniature: identity, values, governance, economy, map, AI, records, and federation link.

The trust is sovereign locally and cooperative voluntarily.
