from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "templates" / "trust-seed"
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
STATIC_FILES = ("README.md", "ECONOMY.md", "AI_STEWARD.md")


def fail(message: str) -> None:
    raise SystemExit(message)


def derive_trust_name(destination: Path) -> str:
    parts = [part for part in re.split(r"[\s_-]+", destination.name.strip()) if part]
    if not parts:
        return "Local Trust Seed"
    return " ".join(part.capitalize() for part in parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Instantiate a local trust seed from the canonical template.",
    )
    parser.add_argument(
        "destination",
        nargs="?",
        default="local-trust-seed",
        help="Directory where the trust seed will be created.",
    )
    parser.add_argument(
        "--name",
        help="Trust name. Defaults to a title-cased version of the destination directory.",
    )
    parser.add_argument(
        "--trust-type",
        action="append",
        dest="trust_types",
        help="Trust type to record. May be passed more than once.",
    )
    parser.add_argument(
        "--purpose",
        help="Short statement of what the trust stewards.",
    )
    parser.add_argument(
        "--primary-steward",
        default="Primary local steward",
        help="Primary steward label for GOVERNANCE.md.",
    )
    parser.add_argument(
        "--location-precision",
        default="private only",
        help="Location privacy level for MAP.md and LOCAL_MANIFEST.json.",
    )
    parser.add_argument(
        "--federation-visibility",
        default="Private local seed",
        help="Federation visibility level recorded in TRUST.md.",
    )
    return parser.parse_args()


def ensure_template_ready(template_dir: Path | None = None) -> None:
    template_dir = TEMPLATE_DIR if template_dir is None else template_dir
    if not template_dir.is_dir():
        fail(f"Trust seed template is missing: {template_dir}")
    missing = [name for name in REQUIRED_TEMPLATE_FILES if not (template_dir / name).is_file()]
    if missing:
        fail(f"Trust seed template is incomplete: {', '.join(missing)}")


def ensure_destination_ready(destination: Path) -> None:
    if destination.exists():
        if not destination.is_dir():
            fail(f"Destination exists and is not a directory: {destination}")
        if any(destination.iterdir()):
            fail(f"Destination already exists and is not empty: {destination}")
        return
    destination.mkdir(parents=True, exist_ok=False)


def write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def load_manifest(path: Path) -> dict[str, object]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Template LOCAL_MANIFEST.json is not valid JSON: {exc}")
    if not isinstance(manifest, dict):
        fail("Template LOCAL_MANIFEST.json must contain a JSON object")
    return manifest


def validate_relative_file_path(seed_dir: Path, raw_path: object, label: str) -> None:
    if not isinstance(raw_path, str) or not raw_path:
        fail(f"{label} must be a non-empty string path")
    if "\\" in raw_path or ":" in raw_path:
        fail(f"{label} must use a relative POSIX path: {raw_path}")

    path = PurePosixPath(raw_path)
    if path.is_absolute() or ".." in path.parts or "." in path.parts or not path.parts:
        fail(f"{label} escapes the generated trust seed: {raw_path}")

    current = seed_dir.resolve()
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            fail(f"{label} uses a symlinked path: {raw_path}")
        if not current.exists():
            fail(f"{label} is missing: {raw_path}")

    resolved = current.resolve()
    if not resolved.is_relative_to(seed_dir.resolve()):
        fail(f"{label} escapes the generated trust seed: {raw_path}")
    if not resolved.is_file():
        fail(f"{label} must be a file: {raw_path}")


def render_trust_document(
    name: str,
    trust_types: list[str],
    purpose: str,
    federation_visibility: str,
) -> str:
    trust_types_lines = "\n".join(f"- {trust_type}" for trust_type in trust_types)
    return f"""# Trust

## Trust Name

`{name}`

## Trust Type

Selected type(s):

{trust_types_lines}

## Purpose

`{purpose}`

## Values

- human agency;
- privacy by default;
- evidence-bounded claims;
- local-first operation;
- voluntary federation.

## Sovereignty Boundaries

Private by default:

- trust records, working documents, and identity details remain local unless explicitly shared.

Shared with selected people or groups:

- no shared data declared yet.

Public to the Federation or world:

- no public disclosures declared yet.

## Stewardship Commitments

This trust commits to:

- protect human agency;
- preserve privacy by default;
- distinguish evidence from doctrine;
- prefer local-first operation;
- avoid overstating legal, financial, medical, empirical, or production claims;
- contribute to the Federation only by consent.

## Federation Link

Federation visibility level:

- Private local seed
- Shared with trusted circle
- Public profile only
- Public project node
- Public marketplace node
- Public research or repository node

Selected level: `{federation_visibility}`

## Notes

`Bootstrap generated from the canonical trust-seed template. Review and customize locally before sharing anything publicly.`
"""


def render_tree_of_life_document(name: str, purpose: str) -> str:
    return f"""# Tree of Life

The Tree of Life is the growth model for this trust.

## Seed

Origin, consent, identity, keys, and values.

- Trust origin: `Local bootstrap from the canonical trust-seed template`
- Consent foundation: `Explicit human steward control`
- Identity root: `{name}`
- Core values: `human agency; privacy by default; local-first stewardship`

## Roots

Foundations that nourish the trust.

- Family and trusted circle: `Defined locally by the steward`
- Land or local place: `Kept private unless explicitly shared`
- Skills and knowledge: `Steward knowledge, documents, and practical experience`
- Records and history: `Local records maintained under steward control`
- Community relationships: `Declared locally and shared only by consent`

## Trunk

The enduring mission and stewardship path.

- Mission: `{purpose}`
- Responsibilities: `Maintain truthful records, permissions, and local stewardship boundaries`
- Commitments: `Preserve privacy by default and require human approval for sensitive actions`
- Governance rhythm: `Review and update this seed during normal stewardship cycles`

## Branches

Active projects, businesses, repositories, ministries, research, and collaborations.

- Branch 1: `Trust documentation and local records`
- Branch 2: `Current projects and mission work chosen by the steward`
- Branch 3: `Optional federation participation by explicit consent`

## Leaves

Daily work and active contributions.

- Tasks: `Review and customize this seed for local use`
- Documents: `Maintain the trust documents and manifest`
- Issues or pull requests: `Track repository work only when a repository is part of this trust`
- Local actions: `Carry out steward-approved work`
- Meetings or events: `Record only what the steward chooses to keep`

## Fruit

Completed value that can nourish others.

- Releases: `Local outputs are recorded here when they exist`
- Revenue or services delivered: `Tracked only if this trust chooses to operate in that way`
- Public goods: `Documented when the trust intentionally shares them`
- Mentorship: `Record mentoring or support work if applicable`
- Repairs completed: `Track completed repairs and improvements`
- Lessons learned: `Capture what improves truthful stewardship`

## New Seeds

Future trusts, projects, communities, or opportunities that grow from the fruit.

- New seed 1: `A project-specific trust seed if future work needs one`
- New seed 2: `A community collaboration seed by explicit consent`
- New seed 3: `A repository or research seed when a distinct boundary is needed`

## Growth Principle

The goal is not extraction or leaderboard status. The goal is cultivation: every contribution should help the tree become more resilient, truthful, useful, and life-giving.
"""


def render_governance_document(primary_steward: str) -> str:
    return f"""# Governance

## Governance Purpose

Governance defines how this trust makes decisions, grants consent, resolves conflicts, accepts contributions, and changes its own rules.

## Steward Roles

- Primary steward: `{primary_steward}`
- Co-stewards: `None declared yet`
- Advisors: `None declared yet`
- Contributors: `None declared yet`
- Beneficiaries or served community: `To be declared by the steward if applicable`

## Decision Types

### Routine Decisions

Examples: task updates, document edits, and ordinary operational choices.

Decision rule: `Primary steward may decide and record routine local changes`

### Material Decisions

Examples: publishing private information, spending shared resources, changing governance, entering partnerships, or making formal commitments.

Decision rule: `Require explicit human approval from the primary steward and any affected co-stewards`

### Emergency Decisions

Examples: account compromise, safety issue, urgent deadline, or critical infrastructure failure.

Decision rule: `Take the smallest protective action first, then document and review it with the steward`

## Consent Boundaries

The following require explicit human approval:

- sharing private or sensitive information;
- changing legal, financial, medical, identity, custody, or safety-sensitive claims;
- creating public commitments;
- granting an AI agent new write access;
- changing this governance document.

## Conflict and Repair

When conflict occurs, the trust should prefer:

1. clarification;
2. evidence review;
3. mutual accountability;
4. restorative repair;
5. documented decision;
6. qualified professional help when required.

## Amendment Process

This document may be amended by: `explicit steward approval recorded in an auditable history`

Amendment history should be tracked through Git or another auditable record system.
"""


def render_map_document(location_precision: str) -> str:
    return f"""# Living Atlas

## Green Zone

The Green Zone is the trust's local present layer.

It is where identity, location, current tasks, relationships, permissions, and observation meet.

## Location Privacy

Location precision should be chosen by the trust.

Options:

- private only;
- approximate region;
- city-level;
- neighborhood-level;
- public project location;
- public business location;
- event-specific temporary location.

Selected setting: `{location_precision}`

## Map Layers

Possible layers:

- self and trust identity;
- family or trusted circle;
- local community;
- businesses and services;
- projects and missions;
- repositories;
- assets and resources;
- events;
- public contributions;
- Federation nodes.

## Zoom Principle

The interface should allow the trust to zoom from:

- planet;
- region;
- city;
- neighborhood;
- trust location;
- project;
- repository;
- document;
- task;
- contribution record.

Every scale should preserve the same pattern: identity, relationship, contribution, stewardship, and optional federation.

## Local Missions

Local missions may include:

- volunteer opportunities;
- repairs;
- deliveries;
- garden work;
- local commerce;
- mutual aid;
- education;
- events;
- repository work connected to local needs.

## Atlas Rule

The map centers the user in their own frame of reference while preserving the dignity and sovereignty of every other node.
"""


def build_local_manifest(
    template_manifest: dict[str, object],
    *,
    name: str,
    trust_types: list[str],
    purpose: str,
    location_precision: str,
) -> dict[str, object]:
    manifest = json.loads(json.dumps(template_manifest))
    trust = manifest.get("trust")
    privacy = manifest.get("privacy")
    tree_of_life = manifest.get("treeOfLife")

    if not isinstance(trust, dict) or not isinstance(privacy, dict) or not isinstance(tree_of_life, dict):
        fail("Template LOCAL_MANIFEST.json is missing trust seed sections")

    manifest["status"] = "local-draft"
    trust["name"] = name
    trust["type"] = trust_types
    trust["purpose"] = purpose
    trust["visibility"] = "private-by-default"

    privacy["defaultDataState"] = "local-private"
    privacy["locationPrecision"] = location_precision
    privacy["publicProfile"] = False
    privacy["sharedWithFederation"] = []

    tree_of_life["seed"] = [
        "local bootstrap from canonical trust-seed template",
        "explicit human steward control",
        name,
    ]
    tree_of_life["roots"] = [
        "local records",
        "trusted relationships",
        "skills and knowledge",
    ]
    tree_of_life["trunk"] = [
        purpose,
        "privacy-preserving stewardship",
        "local-first governance",
    ]
    tree_of_life["branches"] = [
        "trust documentation",
        "current local projects",
        "optional federation participation by consent",
    ]
    tree_of_life["leaves"] = [
        "seed review",
        "document customization",
        "steward-approved tasks",
    ]
    tree_of_life["fruit"] = []
    tree_of_life["newSeeds"] = []

    return manifest


def validate_seed_directory(seed_dir: Path) -> None:
    manifest_path = seed_dir / "LOCAL_MANIFEST.json"
    if not manifest_path.is_file():
        fail(f"Generated trust seed is missing LOCAL_MANIFEST.json: {seed_dir}")

    manifest = load_manifest(manifest_path)
    trust = manifest.get("trust")
    privacy = manifest.get("privacy")
    documents = manifest.get("documents")
    federation_link = manifest.get("federationLink")
    agent_policy = manifest.get("agentPolicy")

    if manifest.get("kind") != "trust-seed":
        fail("Generated trust seed manifest kind must be trust-seed")
    if manifest.get("status") != "local-draft":
        fail('Generated trust seed manifest status must be "local-draft"')
    if not isinstance(trust, dict):
        fail("Generated trust seed manifest trust section must be an object")
    if trust.get("visibility") != "private-by-default":
        fail('Generated trust seed trust.visibility must be "private-by-default"')
    if not isinstance(trust.get("name"), str) or not str(trust["name"]).strip():
        fail("Generated trust seed trust.name must be non-empty")
    if not isinstance(trust.get("type"), list) or not trust["type"]:
        fail("Generated trust seed trust.type must contain at least one entry")
    if not isinstance(trust.get("purpose"), str) or not str(trust["purpose"]).strip():
        fail("Generated trust seed trust.purpose must be non-empty")

    if not isinstance(privacy, dict):
        fail("Generated trust seed manifest privacy section must be an object")
    if privacy.get("defaultDataState") != "local-private":
        fail('Generated trust seed privacy.defaultDataState must be "local-private"')
    if privacy.get("publicProfile") is not False:
        fail("Generated trust seed privacy.publicProfile must be false")
    if privacy.get("sharedWithFederation") != []:
        fail("Generated trust seed privacy.sharedWithFederation must default to an empty list")

    if not isinstance(federation_link, dict):
        fail("Generated trust seed manifest federationLink section must be an object")
    if federation_link.get("enabled") is not False or federation_link.get("publicNode") is not False:
        fail("Generated trust seed federationLink must remain disabled by default")
    if federation_link.get("syncPolicy") != "explicit-consent-only":
        fail('Generated trust seed federationLink.syncPolicy must be "explicit-consent-only"')

    if not isinstance(agent_policy, dict):
        fail("Generated trust seed manifest agentPolicy section must be an object")
    if agent_policy.get("humanApprovalRequired") is not True:
        fail("Generated trust seed agentPolicy.humanApprovalRequired must be true")

    if not isinstance(documents, dict) or not documents:
        fail("Generated trust seed manifest documents section must be a non-empty object")

    for relative_path in documents.values():
        validate_relative_file_path(
            seed_dir,
            relative_path,
            "Generated trust seed document path",
        )

    for file_name in REQUIRED_TEMPLATE_FILES:
        generated_path = seed_dir / file_name
        if not generated_path.is_file():
            fail(f"Generated trust seed is missing file: {file_name}")
        if "TODO" in generated_path.read_text(encoding="utf-8"):
            fail(f"Generated trust seed still contains TODO placeholders: {file_name}")


def create_trust_seed(
    destination: Path,
    *,
    name: str | None = None,
    trust_types: list[str] | None = None,
    purpose: str | None = None,
    primary_steward: str = "Primary local steward",
    location_precision: str = "private only",
    federation_visibility: str = "Private local seed",
) -> Path:
    ensure_template_ready()

    resolved_destination = destination.expanduser().resolve()
    trust_name = name.strip() if isinstance(name, str) and name.strip() else derive_trust_name(resolved_destination)
    selected_trust_types = [item.strip() for item in (trust_types or ["Individual trust"]) if item and item.strip()]
    if not selected_trust_types:
        fail("At least one non-empty trust type is required")
    trust_purpose = (
        purpose.strip()
        if isinstance(purpose, str) and purpose.strip()
        else f"Steward the local trust seed for {trust_name}."
    )

    destination_created = not resolved_destination.exists()
    ensure_destination_ready(resolved_destination)

    try:
        for file_name in STATIC_FILES:
            shutil.copy2(TEMPLATE_DIR / file_name, resolved_destination / file_name)

        write_text(
            resolved_destination / "TRUST.md",
            render_trust_document(
                trust_name,
                selected_trust_types,
                trust_purpose,
                federation_visibility,
            ),
        )
        write_text(
            resolved_destination / "TREE_OF_LIFE.md",
            render_tree_of_life_document(trust_name, trust_purpose),
        )
        write_text(
            resolved_destination / "GOVERNANCE.md",
            render_governance_document(primary_steward),
        )
        write_text(
            resolved_destination / "MAP.md",
            render_map_document(location_precision),
        )

        template_manifest = load_manifest(TEMPLATE_DIR / "LOCAL_MANIFEST.json")
        manifest = build_local_manifest(
            template_manifest,
            name=trust_name,
            trust_types=selected_trust_types,
            purpose=trust_purpose,
            location_precision=location_precision,
        )
        (resolved_destination / "LOCAL_MANIFEST.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )

        validate_seed_directory(resolved_destination)
        return resolved_destination
    except BaseException:
        if destination_created:
            shutil.rmtree(resolved_destination, ignore_errors=True)
        raise


def main() -> None:
    args = parse_args()
    destination = create_trust_seed(
        Path(args.destination),
        name=args.name,
        trust_types=args.trust_types,
        purpose=args.purpose,
        primary_steward=args.primary_steward,
        location_precision=args.location_precision,
        federation_visibility=args.federation_visibility,
    )
    print(f"Created trust seed at {destination}")


if __name__ == "__main__":
    main()
