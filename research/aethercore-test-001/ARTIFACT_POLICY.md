# AetherCore Artifact Policy

This folder mixes hand-written research code and documentation with generated research artifacts. The goal of this policy is to keep future changes reviewable and reproducible.

## Runtime Baseline

- Python baseline used for the current published outputs: `3.13.7`
- Dependency baseline: pinned in `requirements.txt`
- If a rerun uses a different Python minor version or different package versions, treat numeric diffs as environment-sensitive until confirmed.

## Canonical Tracked Inputs

These are hand-maintained and should be reviewed line by line:

- `README.md`
- `ARTIFACT_POLICY.md`
- `requirements.txt`
- `scripts/*.py`
- `report/*.md`

These are tracked generated inputs to downstream analysis and should remain committed because the raw source files are excluded:

- `data_processed/*.csv`

## Canonical Tracked Outputs

These are the generated files that define the published research state and are expected to stay in git:

- `outputs/*.csv`
- `outputs/*.json`
- `figures/*.png`
- `report/*.md`
- `../../docs/pdf/*.pdf`

## Non-Canonical / Local-Only Artifacts

These should stay out of git:

- `data_raw/`
- local virtual environments such as `.venv/` or `venv/`
- notebook checkpoints, cache folders, and Python bytecode
- ad hoc exploratory exports not referenced by the README or reports

## Change Rules

When changing analysis code:

1. Update the relevant script under `scripts/`.
2. Regenerate only the affected outputs.
3. Confirm the matching `report/*.md` and summary JSON/CSV files still agree.
4. If the public claim changed, update `README.md` and the affected report.

When changing documentation only:

1. Do not rewrite generated CSV/JSON/PNG artifacts unless the analysis actually changed.
2. Keep PDF rebuilds scoped to documents whose source changed.

## Commit Hygiene

Prefer small commits by intent:

- one commit for code or methodology changes
- one commit for regenerated outputs from that exact code change
- one commit for documentation-only clarifications when possible

If a run changes many generated artifacts, mention the exact script(s) and environment in the commit message or PR description.

## Review Checklist

Before publishing a new research state:

- `requirements.txt` is still pinned
- the changed script list is known
- summary JSON files match the narrative claims
- reports reference the same sample counts and directional findings as the outputs
- PDFs were rebuilt only when their source changed
