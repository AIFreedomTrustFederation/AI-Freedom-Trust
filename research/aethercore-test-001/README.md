# AetherCore Test 001: Trust Density and COVID Shock Recovery

This folder contains the reproducible empirical research package for the first AetherCore trust-density test suite.

The research question is:

> Do measurable trust variables improve prediction of COVID-19 shock-response and recovery outcomes after controlling for conventional explanatory variables?

The goal is **not final proof**. The goal is a falsifiable, reproducible first pass that can be improved, challenged, replicated, and expanded.

## Short Findings

The results are mixed but informative:

- Trust variables can add predictive information beyond material controls in some COVID response models.
- Trust is not one thing. Centralized institutional trust, expert trust, generalized interpersonal trust, and decentralized community trust behave differently.
- Centralized institutional and expert trust are generally more protective in vaccination and mortality models.
- A large gap between decentralized social trust and centralized institutional trust can mark vulnerability during institutional shocks.
- The results are correlational and country-level. They do not prove causality.

## Folder Structure

- `data_raw/`: local-only raw datasets. Ignored by git.
- `data_processed/`: cleaned country-level datasets tracked in git.
- `scripts/`: executable Python analysis scripts.
- `outputs/`: regression tables, model comparisons, audits, and summary JSON/CSV files.
- `figures/`: generated plots.
- `report/`: plain-English markdown reports for each test.

## Data Sources

### World Values Survey Wave 7

Source: https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp

Use: country-level trust variables.

Raw WVS data may require free registration and license acceptance. Place the downloaded Wave 7 country-pooled file in:

```text
data_raw/
```

Accepted file types include `.csv`, `.dta`, `.sav`, `.xlsx`, and `.zip`, depending on what was downloaded.

Generated processed files:

- `data_processed/wvs_wave7_country_trust.csv`
- `data_processed/wvs_trust_taxonomy_country.csv`
- `data_processed/wvs_fieldwork_timing_country.csv`

Variable audit:

- `outputs/wvs_variable_audit.json`
- `outputs/test003_trust_taxonomy_audit.json`

### Our World in Data COVID-19

Source CSV: https://covid.ourworldindata.org/data/owid-covid-data.csv  
Source repository: https://github.com/owid/covid-19-data

Use: COVID outcomes and controls including vaccination, mortality, GDP per capita, HDI, median age, population density, hospital beds, and policy stringency where available.

Generated processed file:

- `data_processed/owid_covid_country.csv`

### World Governance Indicators

Source: https://www.worldbank.org/en/publication/worldwide-governance-indicators

Use: state-capacity controls and institutional quality proxies.

Generated processed file:

- `data_processed/wgi_state_capacity_2019.csv`

### YouGov / Imperial COVID-19 Behaviour Tracker

Use: behavioral resistance and trust-in-health-authority proxies where available.

Because public archive availability can vary, local raw files should be placed under:

```text
data_raw/yougov_behavior_tracker/
```

Generated processed files:

- `data_processed/yougov_behavior_country.csv`
- `data_processed/yougov_behavior_country_phase_long.csv`
- `data_processed/aethercore_test002_behavioral_merged.csv`

## Constructed Variables

Core trust variables:

- `trust_generalized`: generalized interpersonal trust from WVS.
- `trust_institutions`: average trust across selected centralized institutions.
- `trust_experts`: expert trust proxy where available, generally based on trust in universities, science/technology confidence, doctors, or adjacent WVS items depending on data availability.
- `trust_density_composite`: standardized composite of available trust variables.
- `centralized_trust`: institutional/government/legal/health authority trust grouping.
- `decentralized_trust`: interpersonal/community/social trust grouping.
- `centralization_gap`: decentralized trust minus centralized trust.

COVID outcome variables:

- `vaccination_rate`
- `vaccination_rate_2021`
- `non_vaccinated_share`
- `excess_mortality`
- `deaths_per_million`
- `acute_deaths_per_million`
- `recovery_deaths_per_million`

Controls:

- `gdp_per_capita`
- `human_development_index`
- `median_age`
- `population_density`
- `hospital_beds_per_thousand`
- `stringency_index`
- WGI state-capacity proxies where available.

Behavioral variables:

- vaccine refusal or non-uptake proxies.
- mask refusal or non-mask-use proxies.
- health authority trust.
- belief that government control measures are excessive.
- pre-shock, acute-shock, and recovery-phase aggregates where available.

## Test Suite

### Test 001: Core Trust Density Models

Script:

```powershell
python scripts\run_analysis.py
```

Main outputs:

- `data_processed/aethercore_test001_merged.csv`
- `outputs/regression_results.csv`
- `outputs/model_comparison.csv`
- `figures/coefficient_plot.png`
- `figures/correlation_heatmap.png`
- `report/aethercore_test_001_report.md`

### Test 002: Behavioral Resistance

Script:

```powershell
python scripts\run_behavioral_test002.py
```

Main outputs:

- `data_processed/aethercore_test002_behavioral_merged.csv`
- `outputs/test002_behavioral_regression_results.csv`
- `figures/test002_behavior_coefficient_plot.png`
- `report/aethercore_test_002_behavioral_resistance.md`

### Test 003: Trust Taxonomy

Script:

```powershell
python scripts\run_trust_taxonomy_test003.py
```

Main outputs:

- `data_processed/aethercore_test003_trust_taxonomy_merged.csv`
- `outputs/test003_trust_taxonomy_regression_results.csv`
- `figures/test003_taxonomy_coefficient_plot.png`
- `report/aethercore_test_003_trust_taxonomy.md`

### Test 004: Robustness

Script:

```powershell
python scripts\run_robustness_test004.py
```

Main outputs:

- `outputs/test004_robustness_results.csv`
- `outputs/test004_leave_one_out.csv`
- `outputs/test004_leave_one_out_summary.csv`
- `figures/test004_robustness_coefficients.png`
- `report/aethercore_test_004_robustness.md`

### Test 005: Timing and State Capacity

Script:

```powershell
python scripts\run_timing_statecapacity_test005.py
```

Main outputs:

- `data_processed/aethercore_test005_timing_statecapacity_merged.csv`
- `outputs/test005_timing_statecapacity_results.csv`
- `report/aethercore_test_005_timing_statecapacity.md`

### Test 006: Mechanism Interactions

Script:

```powershell
python scripts\run_mechanism_test006.py
```

Main outputs:

- `data_processed/aethercore_test006_mechanism_merged.csv`
- `outputs/test006_mechanism_interactions_results.csv`
- `figures/test006_mechanism_coefficients.png`
- `report/aethercore_test_006_mechanism_interactions.md`

## Reproduction

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run all tests from this directory:

```powershell
python scripts\run_analysis.py
python scripts\run_behavioral_test002.py
python scripts\run_trust_taxonomy_test003.py
python scripts\run_robustness_test004.py
python scripts\run_timing_statecapacity_test005.py
python scripts\run_mechanism_test006.py
```

## Raw Data Policy

The following are intentionally **not** committed:

- WVS raw country-pooled files.
- OWID raw COVID download.
- WGI archive files.
- YouGov/Imperial raw behavioral files.

Reasons:

- Raw files are large.
- Some sources have license or registration requirements.
- GitHub is not the correct archival location for large raw public datasets.

The tracked `data_processed/` files are country-level derived datasets suitable for review and replication checks.

## Main Scientific Cautions

- This is observational, country-level analysis.
- Correlation is not causation.
- WVS fieldwork timing varies by country, so trust measures are not a perfect pre-shock baseline everywhere.
- Country-level aggregation can hide within-country variation.
- Trust variables are sensitive to coding decisions and survey-item availability.
- Behavioral tracker data availability differs across countries and waves.
- Results should be treated as evidence for further testing, not final confirmation.

## Publication Artifacts

- Empirical white paper PDF: `../../docs/pdf/aethercore-empirical-trust-density-covid.pdf`
- LaTeX source: `../../latex/documents/aethercore-empirical-trust-density-covid.tex`
- Main report: `report/aethercore_test_001_report.md`
- Follow-up test reports: `report/aethercore_test_002_behavioral_resistance.md` through `report/aethercore_test_006_mechanism_interactions.md`

