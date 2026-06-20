# AI Freedom Trust Security And Privacy

This document records security, privacy, data, and public-claim boundaries for `AI-Freedom-Trust`.

## Security status

| Area | Status |
| --- | --- |
| Formal security audit | Not audited |
| Raw data handling | Raw datasets are local-only and ignored by git |
| Public research data | Processed country-level outputs are tracked for review |
| Public site | Static GitHub Pages site |
| Secret requirement | No committed secrets required |
| External review | Awaiting independent review |

## No secrets or private data in public source

Do not commit:

- private reviewer correspondence;
- private reviewer contact lists unless already approved for publication;
- raw licensed survey files;
- account credentials or API keys;
- private owner notes;
- local `.env` files;
- local virtual environments or caches.

## Raw data policy

Raw data belongs under:

```text
research/aethercore-test-001/data_raw/
```

That path is ignored by git. Some source datasets may require registration, licensing, or archive-specific access. Public source should document how to acquire them without redistributing restricted raw files.

## Public claim boundaries

The repo may claim:

- exploratory empirical findings;
- reproducible scripts and tracked processed outputs;
- public PDFs generated from source documents;
- review packet readiness.

The repo must not claim without evidence:

- causal proof;
- peer review;
- independent replication;
- audited security;
- production deployment;
- verified revenue, order volume, or customer outcomes for applied projects.

## Research integrity boundaries

When analysis outputs change, preserve:

- sample counts;
- control sets;
- model limitations;
- raw data caveats;
- distinction between correlation and causation;
- distinction between AetherCore as a tested hypothesis and AetherCore as a broader doctrine.

## Incident response

If private data, raw licensed files, or unsupported claims are published:

1. Stop publication or release promotion.
2. Record the affected files and public surface.
3. Remove or correct the exposed material.
4. Rotate any exposed credential outside the repository if applicable.
5. Add a regression check or review checklist item where practical.
6. Report what remains unknown.
