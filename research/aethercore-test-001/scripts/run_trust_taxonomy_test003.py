"""AetherCore Test 003: Centralized vs Decentralized Trust Taxonomy.

This pass tests whether COVID shock outcomes are better explained by distinct
trust channels rather than one undifferentiated trust composite.

Core hypothesis:
    Mortality and behavioral resistance may rise where centralized institutional
    trust is low, expert/information trust is low, and decentralized social trust
    becomes the primary coordination pathway.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT = SCRIPT_DIR.parents[0]
DATA_PROCESSED = PROJECT / "data_processed"
OUTPUTS = PROJECT / "outputs"
FIGURES = PROJECT / "figures"
REPORT = PROJECT / "report"

sys.path.insert(0, str(SCRIPT_DIR))
from run_analysis import find_wvs_file, read_wvs, recode_confidence  # noqa: E402


TAXONOMY = {
    "centralized_institutional_trust": {
        "Q69": "police",
        "Q70": "courts",
        "Q71": "government",
        "Q72": "political_parties",
        "Q73": "parliament",
        "Q74": "civil_service",
        "Q76": "elections",
    },
    "expert_epistemic_trust": {
        "Q75": "universities",
        "Q158": "science_item_1",
        "Q159": "science_item_2",
    },
    "information_trust": {
        "Q66": "press",
        "Q67": "television",
    },
    "bonding_social_trust": {
        "Q58": "family",
        "Q59": "neighborhood",
        "Q60": "people_known_personally",
    },
    "bridging_social_trust": {
        "Q61": "people_met_first_time",
        "Q62": "people_another_religion",
        "Q63": "people_another_nationality",
    },
}


def ensure_dirs() -> None:
    for directory in [DATA_PROCESSED, OUTPUTS, FIGURES, REPORT]:
        directory.mkdir(parents=True, exist_ok=True)


def first_present(columns: list[str], candidates: list[str]) -> str | None:
    for candidate in candidates:
        if candidate in columns:
            return candidate
    lower = {str(c).lower(): c for c in columns}
    for candidate in candidates:
        if candidate.lower() in lower:
            return lower[candidate.lower()]
    return None


def build_taxonomy() -> tuple[pd.DataFrame, dict]:
    wvs_path = find_wvs_file()
    if wvs_path is None:
        raise SystemExit("WVS Wave 7 file not found. Run Test 001 first.")
    wvs = read_wvs(wvs_path)
    iso_col = first_present(list(wvs.columns), ["B_COUNTRY_ALPHA", "COUNTRY_ALPHA", "ISO3", "S003B"])
    country_col = first_present(list(wvs.columns), ["B_COUNTRY", "COUNTRY", "Country", "S003"])
    if iso_col is None:
        raise SystemExit("Could not locate WVS ISO3 country column.")

    work = pd.DataFrame()
    work["iso_code"] = wvs[iso_col].astype(str).str.upper().str.strip()
    work["location_wvs"] = wvs[country_col].astype(str) if country_col else np.nan
    audit = {"wvs_file": str(wvs_path), "iso_column": iso_col, "country_column": country_col, "constructs": {}}

    for construct, mapping in TAXONOMY.items():
        present = [col for col in mapping if col in wvs.columns]
        audit["constructs"][construct] = {col: mapping[col] for col in present}
        if present:
            recoded = pd.DataFrame({col: recode_confidence(wvs[col]) for col in present})
            work[construct] = recoded.mean(axis=1)
        else:
            work[construct] = np.nan

    work["decentralized_social_trust"] = work[["bonding_social_trust", "bridging_social_trust"]].mean(axis=1)
    agg = (
        work.groupby("iso_code", as_index=False)
        .agg(
            location_wvs=("location_wvs", lambda s: s.dropna().astype(str).mode().iloc[0] if len(s.dropna()) else np.nan),
            centralized_institutional_trust=("centralized_institutional_trust", "mean"),
            expert_epistemic_trust=("expert_epistemic_trust", "mean"),
            information_trust=("information_trust", "mean"),
            bonding_social_trust=("bonding_social_trust", "mean"),
            bridging_social_trust=("bridging_social_trust", "mean"),
            decentralized_social_trust=("decentralized_social_trust", "mean"),
            wvs_taxonomy_n=("centralized_institutional_trust", "count"),
        )
    )
    agg["centralization_gap"] = agg["decentralized_social_trust"] - agg["centralized_institutional_trust"]
    agg["epistemic_gap"] = agg["decentralized_social_trust"] - agg["expert_epistemic_trust"]
    agg.to_csv(DATA_PROCESSED / "wvs_trust_taxonomy_country.csv", index=False)
    (OUTPUTS / "test003_trust_taxonomy_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    return agg, audit


def standardize(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col not in out:
            continue
        sd = out[col].std(skipna=True)
        if pd.notna(sd) and sd > 0:
            out[f"z_{col}"] = (out[col] - out[col].mean(skipna=True)) / sd
    return out


def data_columns_from_terms(terms: list[str]) -> list[str]:
    cols: list[str] = []
    for term in terms:
        cols.extend(part.strip() for part in term.split(":"))
    return sorted(set(cols))


def run_ols(df: pd.DataFrame, outcome: str, predictors: list[str], model: str, min_n: int = 18) -> list[dict]:
    cols = [outcome] + data_columns_from_terms(predictors)
    if any(col not in df.columns for col in cols):
        return []
    data = df[cols + ["iso_code", "location"]].dropna()
    if len(data) < max(min_n, len(predictors) + 7):
        return []
    fit = smf.ols(f"{outcome} ~ " + " + ".join(predictors), data=data).fit(cov_type="HC3")
    conf = fit.conf_int()
    rows = []
    for term in fit.params.index:
        rows.append(
            {
                "outcome": outcome,
                "model": model,
                "term": term,
                "coef": fit.params[term],
                "std_err_hc3": fit.bse[term],
                "p_value": fit.pvalues[term],
                "ci_low": conf.loc[term, 0],
                "ci_high": conf.loc[term, 1],
                "n": int(fit.nobs),
                "adj_r2": fit.rsquared_adj,
                "aic": fit.aic,
                "bic": fit.bic,
            }
        )
    return rows


def run_models(df: pd.DataFrame) -> pd.DataFrame:
    controls_full = [
        "z_log_gdp_per_capita",
        "z_human_development_index",
        "z_median_age",
        "z_log_population_density",
        "z_healthcare_capacity",
        "z_stringency_index",
    ]
    controls_compact = ["z_log_gdp_per_capita", "z_human_development_index", "z_median_age"]
    trust_terms = {
        "central_only": ["z_centralized_institutional_trust"],
        "decentralized_only": ["z_decentralized_social_trust"],
        "expert_only": ["z_expert_epistemic_trust"],
        "information_only": ["z_information_trust"],
        "gap_only": ["z_centralization_gap"],
        "taxonomy_channels": [
            "z_centralized_institutional_trust",
            "z_decentralized_social_trust",
            "z_expert_epistemic_trust",
            "z_information_trust",
        ],
        "central_x_decentralized": [
            "z_centralized_institutional_trust",
            "z_decentralized_social_trust",
            "z_centralized_institutional_trust:z_decentralized_social_trust",
        ],
        "central_x_expert": [
            "z_centralized_institutional_trust",
            "z_expert_epistemic_trust",
            "z_centralized_institutional_trust:z_expert_epistemic_trust",
        ],
    }
    mortality_outcomes = [
        "deaths_per_million",
        "acute_deaths_per_million",
        "recovery_deaths_per_million",
        "excess_mortality",
        "vaccination_rate",
        "non_vaccinated_share",
    ]
    behavior_outcomes = [
        "mask_refusal_outside_acute_2020",
        "mask_compliance_outside_acute_2020",
        "vaccine_refusal_vaccine_rollout_2021",
        "vaccine_intent_vaccine_rollout_2021",
        "government_control_belief_vaccine_rollout_2021",
        "health_authority_vaccine_trust_vaccine_rollout_2021",
    ]

    rows = []
    for outcome in mortality_outcomes:
        for name, terms in trust_terms.items():
            rows.extend(run_ols(df, outcome, controls_full + terms, f"full_{name}", min_n=35))
    for outcome in behavior_outcomes:
        for name, terms in trust_terms.items():
            # Small-n behavioral models: compact controls for mask outcomes, bivariate for n=9 vaccine/conspiracy screens.
            if "vaccine_rollout_2021" in outcome:
                rows.extend(run_ols(df, outcome, terms, f"bivariate_{name}", min_n=8))
            else:
                rows.extend(run_ols(df, outcome, controls_compact + terms, f"compact_{name}", min_n=16))
    return pd.DataFrame(rows)


def make_figures(df: pd.DataFrame, results: pd.DataFrame) -> None:
    pairs = [
        ("centralized_institutional_trust", "deaths_per_million", "test003_central_trust_vs_deaths.png"),
        ("decentralized_social_trust", "deaths_per_million", "test003_decentralized_trust_vs_deaths.png"),
        ("centralization_gap", "deaths_per_million", "test003_gap_vs_deaths.png"),
        ("centralization_gap", "government_control_belief_vaccine_rollout_2021", "test003_gap_vs_government_control_belief.png"),
        ("expert_epistemic_trust", "health_authority_vaccine_trust_vaccine_rollout_2021", "test003_expert_vs_health_authority_trust.png"),
    ]
    for x, y, filename in pairs:
        if x not in df or y not in df:
            continue
        plot = df[[x, y, "location"]].dropna()
        if len(plot) < 8:
            continue
        plt.figure(figsize=(8, 5.5))
        sns.regplot(data=plot, x=x, y=y, scatter_kws={"s": 46, "alpha": 0.8}, line_kws={"color": "#9b1c31"})
        plt.title(f"{x} vs {y} (n={len(plot)})")
        plt.tight_layout()
        plt.savefig(FIGURES / filename, dpi=180)
        plt.close()

    terms = [
        "z_centralized_institutional_trust",
        "z_decentralized_social_trust",
        "z_expert_epistemic_trust",
        "z_information_trust",
        "z_centralization_gap",
        "z_centralized_institutional_trust:z_decentralized_social_trust",
        "z_centralized_institutional_trust:z_expert_epistemic_trust",
    ]
    coef = results[results["term"].isin(terms)].copy()
    if coef.empty:
        return
    coef = coef.sort_values(["outcome", "model", "term"])
    coef["label"] = coef["outcome"] + " | " + coef["model"]
    plt.figure(figsize=(12, max(6, 0.20 * len(coef))))
    y = np.arange(len(coef))
    plt.errorbar(
        coef["coef"],
        y,
        xerr=[coef["coef"] - coef["ci_low"], coef["ci_high"] - coef["coef"]],
        fmt="o",
        color="#1f4e79",
        ecolor="#8aa9c4",
        capsize=2,
    )
    plt.axvline(0, color="black", linewidth=1)
    plt.yticks(y, coef["label"], fontsize=5)
    plt.xlabel("OLS coefficient with HC3 95% CI")
    plt.title("Test 003 Trust Taxonomy Coefficients")
    plt.tight_layout()
    plt.savefig(FIGURES / "test003_taxonomy_coefficient_plot.png", dpi=180)
    plt.close()


def p_label(p: float) -> str:
    if pd.isna(p):
        return "not estimable"
    if p < 0.01:
        return "p<0.01"
    if p < 0.05:
        return "p<0.05"
    if p < 0.10:
        return "p<0.10"
    return "n.s."


def write_report(merged: pd.DataFrame, results: pd.DataFrame, audit: dict) -> None:
    report = REPORT / "aethercore_test_003_trust_taxonomy.md"
    focus_terms = [
        "z_centralized_institutional_trust",
        "z_decentralized_social_trust",
        "z_expert_epistemic_trust",
        "z_information_trust",
        "z_centralization_gap",
        "z_centralized_institutional_trust:z_decentralized_social_trust",
        "z_centralized_institutional_trust:z_expert_epistemic_trust",
    ]
    focus = results[results["term"].isin(focus_terms)].copy()
    lines = [
        "# AetherCore Test 003: Centralized Trust vs Decentralized Trust Migration",
        "",
        "## Purpose",
        "",
        "This pass tests whether COVID shock response is better explained by a taxonomy of trust rather than a single trust-density composite.",
        "",
        "The core hypothesis is that risk may rise where centralized institutional trust is low, expert/information trust is weak, and decentralized social trust becomes the dominant coordination pathway.",
        "",
        "## Data",
        "",
        f"- WVS taxonomy countries merged with OWID/Test 001 data: {merged['centralized_institutional_trust'].notna().sum()}",
        f"- Rows in final Test 003 dataset: {len(merged)}",
        "- Behavioral resistance variables are included when Test 002 YouGov aggregates are available.",
        "",
        "## Trust Taxonomy",
        "",
        "- `centralized_institutional_trust`: police, courts, government, political parties, parliament, civil service, elections.",
        "- `expert_epistemic_trust`: universities and available science-oriented WVS items.",
        "- `information_trust`: press and television confidence.",
        "- `bonding_social_trust`: family, neighborhood, people known personally.",
        "- `bridging_social_trust`: people met for the first time, people of another religion, people of another nationality.",
        "- `decentralized_social_trust`: average of bonding and bridging social trust.",
        "- `centralization_gap`: decentralized social trust minus centralized institutional trust.",
        "",
        "## Variable Audit",
        "",
        "```json",
        json.dumps(audit, indent=2),
        "```",
        "",
        "## Main Coefficients",
        "",
    ]
    if focus.empty:
        lines.append("No Test 003 models could be estimated.")
    else:
        lines.append("| Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |")
        lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
        for _, row in focus.sort_values(["outcome", "model", "term"]).iterrows():
            lines.append(
                f"| {row['outcome']} | {row['model']} | {row['term']} | "
                f"{row['coef']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | "
                f"{row['p_value']:.3f} ({p_label(row['p_value'])}) | {int(row['n'])} | {row['adj_r2']:.3f} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This test should not be read as proof that centralized distrust caused mortality. It asks whether mortality and behavioral resistance align more strongly with particular trust channels.",
            "",
            "The migration hypothesis gains support if low centralized trust, high centralization gap, or negative central x decentralized interactions predict worse outcomes. It is weakened if decentralized trust is protective, if central trust is not associated with outcomes, or if effects vanish after controls.",
            "",
            "## Limitations",
            "",
            "- WVS Wave 7 timing overlaps the pandemic in some countries, so trust may be partly post-shock rather than purely pre-shock.",
            "- Country-level regressions cannot prove individual-level behavioral mechanisms.",
            "- The YouGov behavioral overlap remains small for vaccine/conspiracy outcomes.",
            "- Central institutions may be trusted because they are competent; trust may be a signal of state capacity as well as public psychology.",
        ]
    )
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    taxonomy, audit = build_taxonomy()
    base_path = DATA_PROCESSED / "aethercore_test001_merged.csv"
    if not base_path.exists():
        raise SystemExit("Run Test 001 first.")
    base = pd.read_csv(base_path)
    merged = base.merge(taxonomy.drop(columns=["location_wvs"], errors="ignore"), on="iso_code", how="inner")

    behavior_path = DATA_PROCESSED / "aethercore_test002_behavioral_merged.csv"
    if behavior_path.exists():
        behavior = pd.read_csv(behavior_path)
        behavior_cols = [c for c in behavior.columns if c not in merged.columns or c == "iso_code"]
        merged = merged.merge(behavior[behavior_cols], on="iso_code", how="left")

    z_cols = [
        "centralized_institutional_trust",
        "expert_epistemic_trust",
        "information_trust",
        "bonding_social_trust",
        "bridging_social_trust",
        "decentralized_social_trust",
        "centralization_gap",
        "epistemic_gap",
        "log_gdp_per_capita",
        "human_development_index",
        "median_age",
        "log_population_density",
        "healthcare_capacity",
        "stringency_index",
    ]
    merged = standardize(merged, z_cols)
    merged.to_csv(DATA_PROCESSED / "aethercore_test003_trust_taxonomy_merged.csv", index=False)

    results = run_models(merged)
    results.to_csv(OUTPUTS / "test003_trust_taxonomy_regression_results.csv", index=False)
    make_figures(merged, results)
    write_report(merged, results, audit)

    summary = {
        "merged_countries": int(len(merged)),
        "models_estimated": int(results[["outcome", "model"]].drop_duplicates().shape[0]) if not results.empty else 0,
        "result_rows": int(len(results)),
    }
    (OUTPUTS / "test003_trust_taxonomy_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Report: {REPORT / 'aethercore_test_003_trust_taxonomy.md'}")


if __name__ == "__main__":
    main()
