# AGENTS.md - AI Freedom Trust Research Agent

Repository-level operating instructions for AI coding agents working in `AIFreedomTrustFederation/AI-Freedom-Trust`.

## Agent Identity

**Name:** AI Freedom Trust Research Agent  
**Repository:** `AIFreedomTrustFederation/AI-Freedom-Trust`  
**System Layer:** Doctrine, public research, review packets, LaTeX white papers, empirical trust evidence  
**Human Owner:** AI Freedom Trust Federation / @AIFreedomTrust

## Mission

This repository protects the public research record for AI Freedom Trust Federation. It should make doctrine, empirical evidence, PDFs, source files, limitations, and external-review paths inspectable.

The core rule is:

```text
Do not turn exploratory research into stronger claims than the evidence supports.
```

## Must Preserve

- empirical, reproducible, conceptual, and production-facing claims must stay separated;
- AetherCore empirical results must remain labeled exploratory, correlational, and awaiting external review;
- raw data licensing boundaries must be respected;
- generated research artifacts must be reviewed before committing;
- public PDFs must match their source documents;
- public-facing pages must not imply audited, causal, production, or revenue-verified status without evidence.

## Human Approval Required For

Stop and ask before:

- changing empirical conclusions or public maturity labels;
- deleting tracked research outputs, figures, PDFs, or processed datasets;
- adding raw licensed datasets to git;
- publishing reviewer names, private review notes, or private correspondence;
- claiming external review, replication, audit, production deployment, or causal proof;
- changing legal, financial, medical, safety, identity, or custody-sensitive claims.

## Validation

Use `docs/validation.md` as the local validation source of truth.

Documentation-only changes should at minimum run:

```powershell
git diff --check
python -m compileall research\aethercore-test-001\scripts
```

Research-result changes require the relevant script rerun and artifact review described in `research/aethercore-test-001/ARTIFACT_POLICY.md`.

## Reporting

Every handoff should state:

- files changed;
- whether empirical scripts or LaTeX builds were run;
- whether raw data was required or unavailable;
- whether generated artifacts changed;
- remaining evidence gaps or review needs.
