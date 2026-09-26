# AI Freedom Trust Validation

This document is the local validation source of truth for `AI-Freedom-Trust`.

## Validation levels

| Level | Scope | Commands |
| --- | --- | --- |
| Documentation check | Markdown, HTML, policy, status, review packet changes | `git diff --check` |
| Doctrine validation | Manifest path checks plus research script syntax without raw data | `python scripts/validate_doctrine.py` |
| Unit tests | Trust-seed generation and doctrine-validator behavior | `python -m unittest discover -s tests -v` |
| Empirical rerun | Recompute processed data, outputs, figures, and reports | Run the relevant scripts in `research/aethercore-test-001\scripts` after installing `requirements.txt` |
| PDF rebuild | Rebuild LaTeX PDFs | `.\scripts\build-latex.ps1` or `.\scripts\build-latex.ps1 -Document <name>` |

## Documentation-only gate

For docs/status/policy changes, run from the repository root:

```powershell
git diff --check
python scripts/validate_doctrine.py
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m unittest discover -s tests -v
```

This does not prove the empirical outputs were regenerated. It checks manifest consistency, doctrine-path safety, research script syntax, deterministic trust-seed behavior, offline operation, and unsafe-path rejection so the documented local gate matches CI. Disabling bytecode generation keeps validation from creating untracked files in the checkout.

## Empirical reproduction

From `research\aethercore-test-001`:

```powershell
python --version
python -m pip install -r requirements.txt
python scripts\run_analysis.py
python scripts\run_behavioral_test002.py
python scripts\run_trust_taxonomy_test003.py
python scripts\run_robustness_test004.py
python scripts\run_timing_statecapacity_test005.py
python scripts\run_mechanism_test006.py
python scripts\run_preshock_test007.py
python scripts\run_postshock_sphere_test008.py
```

Only run the full suite when the required local raw data is present and licensing terms permit use.

## Artifact review

When empirical scripts change:

1. Run only the affected script(s) first.
2. Inspect changed `data_processed/`, `outputs/`, `figures/`, and `report/` files.
3. Confirm sample counts, coefficient directions, and limitations still match the narrative.
4. Update README, reports, and PDFs only when the public claim changes.

## PDF rebuilds

The PDF builder requires `xelatex`.

```powershell
.\scripts\build-latex.ps1
```

If `xelatex` is unavailable, report that the PDF build was not run and do not claim PDFs were refreshed.

## Failure reporting

When validation fails, record:

- exact command;
- first meaningful error;
- whether raw data or external tooling was missing;
- whether generated artifacts changed;
- safest next repair step.

Never summarize a skipped empirical rerun or skipped PDF build as passing.
