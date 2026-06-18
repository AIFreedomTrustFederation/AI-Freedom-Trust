"""AetherCore Test 006: Trust Migration Mechanism Interactions."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


PROJECT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = PROJECT / "data_processed"
OUTPUTS = PROJECT / "outputs"
FIGURES = PROJECT / "figures"
REPORT = PROJECT / "report"


def standardize(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        if col in out:
            sd = out[col].std(skipna=True)
            if pd.notna(sd) and sd > 0:
                out[f"z_{col}"] = (out[col] - out[col].mean(skipna=True)) / sd
    return out


def run_model(df: pd.DataFrame, outcome: str, predictors: list[str], model: str, min_n: int) -> list[dict]:
    cols = [outcome] + sorted(set(part for p in predictors for part in p.split(":")))
    data = df[cols + ["iso_code", "location"]].dropna()
    if len(data) < max(min_n, len(predictors) + 8):
        return []
    fit = smf.ols(f"{outcome} ~ " + " + ".join(predictors), data=data).fit(cov_type="HC3")
    conf = fit.conf_int()
    return [
        {
            "outcome": outcome,
            "model": model,
            "term": term,
            "coef": fit.params[term],
            "p_value": fit.pvalues[term],
            "ci_low": conf.loc[term, 0],
            "ci_high": conf.loc[term, 1],
            "n": int(fit.nobs),
            "adj_r2": fit.rsquared_adj,
            "aic": fit.aic,
            "bic": fit.bic,
        }
        for term in fit.params.index
    ]


def main() -> None:
    path = DATA_PROCESSED / "aethercore_test003_trust_taxonomy_merged.csv"
    if not path.exists():
        raise SystemExit("Run Test 003 first.")
    df = pd.read_csv(path)
    df["misaligned_migration_index"] = df["centralization_gap"] - df["expert_epistemic_trust"]
    df["misaligned_information_index"] = df["centralization_gap"] - df["information_trust"]
    df = standardize(df, ["misaligned_migration_index", "misaligned_information_index"])
    df.to_csv(DATA_PROCESSED / "aethercore_test006_mechanism_merged.csv", index=False)

    controls = [
        "z_log_gdp_per_capita",
        "z_human_development_index",
        "z_median_age",
        "z_log_population_density",
        "z_healthcare_capacity",
        "z_stringency_index",
    ]
    outcomes = ["deaths_per_million", "acute_deaths_per_million", "recovery_deaths_per_million", "excess_mortality", "vaccination_rate", "non_vaccinated_share"]
    behavior_outcomes = [
        "mask_refusal_outside_acute_2020",
        "mask_compliance_outside_acute_2020",
        "government_control_belief_vaccine_rollout_2021",
        "health_authority_vaccine_trust_vaccine_rollout_2021",
    ]
    specs = {
        "gap_x_expert": ["z_centralization_gap", "z_expert_epistemic_trust", "z_centralization_gap:z_expert_epistemic_trust"],
        "gap_x_information": ["z_centralization_gap", "z_information_trust", "z_centralization_gap:z_information_trust"],
        "misaligned_expert_index": ["z_misaligned_migration_index"],
        "misaligned_information_index": ["z_misaligned_information_index"],
    }

    rows = []
    for outcome in outcomes:
        for name, terms in specs.items():
            rows.extend(run_model(df, outcome, controls + terms, f"full_{name}", min_n=35))

    compact = ["z_log_gdp_per_capita", "z_human_development_index", "z_median_age"]
    for outcome in behavior_outcomes:
        for name, terms in specs.items():
            min_n = 8 if "vaccine_rollout_2021" in outcome else 16
            controls_use = [] if "vaccine_rollout_2021" in outcome else compact
            rows.extend(run_model(df, outcome, controls_use + terms, f"{'bivariate' if not controls_use else 'compact'}_{name}", min_n=min_n))

    results = pd.DataFrame(rows)
    results.to_csv(OUTPUTS / "test006_mechanism_interactions_results.csv", index=False)

    focus_terms = [
        "z_centralization_gap",
        "z_expert_epistemic_trust",
        "z_information_trust",
        "z_centralization_gap:z_expert_epistemic_trust",
        "z_centralization_gap:z_information_trust",
        "z_misaligned_migration_index",
        "z_misaligned_information_index",
    ]
    focus = results[results["term"].isin(focus_terms)].copy()
    plt.figure(figsize=(11, max(5, 0.18 * len(focus))))
    focus = focus.sort_values(["outcome", "model", "term"])
    focus["label"] = focus["outcome"] + " | " + focus["model"] + " | " + focus["term"]
    y = np.arange(len(focus))
    plt.errorbar(focus["coef"], y, xerr=[focus["coef"] - focus["ci_low"], focus["ci_high"] - focus["coef"]], fmt="o", capsize=2)
    plt.axvline(0, color="black", linewidth=1)
    plt.yticks(y, focus["label"], fontsize=5)
    plt.title("Test 006 Mechanism Interactions")
    plt.tight_layout()
    plt.savefig(FIGURES / "test006_mechanism_coefficients.png", dpi=180)
    plt.close()

    report = REPORT / "aethercore_test_006_mechanism_interactions.md"
    lines = [
        "# AetherCore Test 006: Trust Migration Mechanism Interactions",
        "",
        "## Purpose",
        "",
        "This pass tests whether the centralization-gap risk is conditioned by expert or information trust.",
        "",
        "Main mechanism models:",
        "",
        "- outcome ~ controls + centralization_gap + expert_trust + gap x expert_trust",
        "- outcome ~ controls + centralization_gap + information_trust + gap x information_trust",
        "- outcome ~ controls + misaligned_migration_index",
        "- outcome ~ controls + misaligned_information_index",
        "",
        "## Coefficients",
        "",
        "| Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for _, row in focus.iterrows():
        lines.append(
            f"| {row['outcome']} | {row['model']} | {row['term']} | {row['coef']:.3f} | "
            f"[{row['ci_low']:.3f}, {row['ci_high']:.3f}] | {row['p_value']:.3f} | {int(row['n'])} | {row['adj_r2']:.3f} |"
        )
    lines.extend(["", "## Interpretation", "", "The mechanism hypothesis is strengthened if centralization-gap effects are larger where expert or information trust is weak, or if misaligned migration indices predict worse outcomes consistently."])
    report.write_text("\n".join(lines), encoding="utf-8")

    summary = {"result_rows": int(len(results)), "models_estimated": int(results[["outcome", "model"]].drop_duplicates().shape[0]) if not results.empty else 0}
    (OUTPUTS / "test006_mechanism_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
