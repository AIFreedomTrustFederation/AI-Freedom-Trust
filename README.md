# AI Freedom Trust Federation

Public repository for the AI Freedom Trust Federation website, LaTeX white papers, and the AetherCore empirical research package.

The current research release centers on **AetherCore Test 001: Trust Density and COVID Shock Recovery**, an empirical test suite asking whether measurable trust variables help predict COVID-19 shock response outcomes after controlling for conventional material and institutional factors.

## Primary Links

- Public site: https://aifreedomtrustfederation.github.io/AI-Freedom-Trust/
- GitHub repository: https://github.com/AIFreedomTrustFederation/AI-Freedom-Trust
- AetherCore empirical test folder: [research/aethercore-test-001](research/aethercore-test-001)
- Empirical white paper PDF: [docs/pdf/aethercore-empirical-trust-density-covid.pdf](docs/pdf/aethercore-empirical-trust-density-covid.pdf)
- AetherCore Volume I PDF: [docs/pdf/aethercore-white-paper-volume-i.pdf](docs/pdf/aethercore-white-paper-volume-i.pdf)
- Aetherion economy PDF: [docs/pdf/aetherion-restorative-civilization-economy.pdf](docs/pdf/aetherion-restorative-civilization-economy.pdf)
- LaTeX source: [latex/documents](latex/documents)

## Repository Map

- `index.html` and `styles.css`: static GitHub Pages website.
- `assets/`: website media assets.
- `docs/`: doctrine drafts, source summaries, internal inventory notes, and generated public PDFs.
- `docs/pdf/`: compiled PDF deliverables intended for reading and sharing.
- `latex/`: LaTeX document sources, shared style package, and build outputs.
- `scripts/build-latex.ps1`: PowerShell builder for LaTeX documents.
- `research/aethercore-test-001/`: reproducible empirical research project with scripts, processed data, outputs, figures, and reports.

## AetherCore Empirical Research

The empirical package currently includes six linked tests:

1. **Test 001: Trust Density and COVID Shock Recovery**  
   Country-level WVS Wave 7 trust variables merged with OWID COVID outcomes and controls.
2. **Test 002: Behavioral Resistance**  
   YouGov/Imperial behavioral indicators for vaccine refusal, mask refusal, and authority-trust behavior.
3. **Test 003: Trust Taxonomy**  
   Centralized institutional trust, decentralized social trust, expert trust proxies, and trust-gap measures.
4. **Test 004: Robustness**  
   Robustness checks, leave-one-out diagnostics, and sensitivity analysis.
5. **Test 005: Timing and State Capacity**  
   Fieldwork timing checks and World Governance Indicators state-capacity controls.
6. **Test 006: Mechanism Interactions**  
   Interaction tests for trust, expert/information alignment, state capacity, and behavioral mechanisms.

The main empirical conclusion is deliberately cautious: the results do **not** prove AetherCore. They suggest that trust is not a simple universally positive variable. Trust topology matters. Centralized institutional and expert trust tend to behave differently from decentralized interpersonal or community trust, and trust gaps can mark vulnerability during institutional shocks.

## Data Policy

Large and/or license-sensitive raw datasets are intentionally excluded from git. The repo tracks processed country-level outputs, reproducible scripts, figures, regression tables, and reports.

Raw source datasets should be placed locally under:

```text
research/aethercore-test-001/data_raw/
```

That directory is ignored by git.

Primary data sources:

- World Values Survey Wave 7: https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp
- Our World in Data COVID-19 dataset: https://covid.ourworldindata.org/data/owid-covid-data.csv
- Our World in Data COVID GitHub: https://github.com/owid/covid-19-data
- World Governance Indicators: https://www.worldbank.org/en/publication/worldwide-governance-indicators
- YouGov/Imperial COVID-19 Behaviour Tracker: data availability varies by archive; see [research/aethercore-test-001/README.md](research/aethercore-test-001/README.md)

Tracked processed datasets include:

- [research/aethercore-test-001/data_processed/aethercore_test001_merged.csv](research/aethercore-test-001/data_processed/aethercore_test001_merged.csv)
- [research/aethercore-test-001/data_processed/aethercore_test002_behavioral_merged.csv](research/aethercore-test-001/data_processed/aethercore_test002_behavioral_merged.csv)
- [research/aethercore-test-001/data_processed/aethercore_test003_trust_taxonomy_merged.csv](research/aethercore-test-001/data_processed/aethercore_test003_trust_taxonomy_merged.csv)
- [research/aethercore-test-001/data_processed/aethercore_test005_timing_statecapacity_merged.csv](research/aethercore-test-001/data_processed/aethercore_test005_timing_statecapacity_merged.csv)
- [research/aethercore-test-001/data_processed/aethercore_test006_mechanism_merged.csv](research/aethercore-test-001/data_processed/aethercore_test006_mechanism_merged.csv)

## Reproduce the Empirical Tests

From the repository root:

```powershell
cd research\aethercore-test-001
python -m pip install -r requirements.txt
python scripts\run_analysis.py
python scripts\run_behavioral_test002.py
python scripts\run_trust_taxonomy_test003.py
python scripts\run_robustness_test004.py
python scripts\run_timing_statecapacity_test005.py
python scripts\run_mechanism_test006.py
```

Outputs are written to:

- `research/aethercore-test-001/data_processed/`
- `research/aethercore-test-001/outputs/`
- `research/aethercore-test-001/figures/`
- `research/aethercore-test-001/report/`

## Build the PDFs

Build all LaTeX documents:

```powershell
.\scripts\build-latex.ps1
```

Build one document:

```powershell
.\scripts\build-latex.ps1 -Document aethercore-empirical-trust-density-covid
```

Final PDFs are written to `docs/pdf/`.

## Publication Status

This is an active research repository. The empirical work should be read as exploratory, correlational, and falsifiable. The results identify patterns worth testing more deeply; they do not establish causal proof.

