"""AetherCore Test 007: Strict pre-shock WVS trust baseline.

This pass reruns the main trust-topology models after excluding countries whose
WVS Wave 7 fieldwork overlaps 2020 or later. It directly tests whether the
central trust / centralization-gap signal survives when trust is measured before
the COVID shock.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT = SCRIPT_DIR.parents[0]
DATA_PROCESSED = PROJECT / "data_processed"
OUTPUTS = PROJECT / "outputs"
FIGURES = PROJECT / "figures"
REPORT = PROJECT / "report"


def ensure_dirs() -> None:
    for directory in [DATA_PROCESSED, OUTPUTS, FIGURES, REPORT]:
        directory.mkdir(parents=True, exist_ok=True)


def standardize_within_sample(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col not in out.columns:
            continue
        sd = out[col].std(skipna=True)
        if pd.notna(sd) and sd > 0:
            out[f"z7_{col}"] = (out[col] - out[col].mean(skipna=True)) / sd
    return out


def columns_from_terms(terms: list[str]) -> list[str]:
    cols: list[str] = []
    for term in terms:
        cols.extend(part.strip() for part in term.split(":"))
    return sorted(set(cols))


def run_model(df: pd.DataFrame, sample: str, outcome: str, predictors: list[str], model: str) -> list[dict]:
    needed = [outcome] + columns_from_terms(predictors)
    if any(col not in df.columns for col in needed):
        return []
    data = df[needed + ["iso_code", "location"]].dropna()
    if len(data) < max(18, len(predictors) + 8):
        return []
    fit = smf.ols(f"{outcome} ~ " + " + ".join(predictors), data=data).fit(cov_type="HC3")
    conf = fit.conf_int()
    return [
        {
            "sample": sample,
            "outcome": outcome,
            "model": model,
            "term": term,
            "coef": float(fit.params[term]),
            "std_err_hc3": float(fit.bse[term]),
            "p_value": float(fit.pvalues[term]),
            "ci_low": float(conf.loc[term, 0]),
            "ci_high": float(conf.loc[term, 1]),
            "n": int(fit.nobs),
            "adj_r2": float(fit.rsquared_adj),
            "aic": float(fit.aic),
            "bic": float(fit.bic),
        }
        for term in fit.params.index
    ]


def build_samples() -> dict[str, pd.DataFrame]:
    path = DATA_PROCESSED / "aethercore_test005_timing_statecapacity_merged.csv"
    if not path.exists():
        raise SystemExit("Run Test 005 first: scripts/run_timing_statecapacity_test005.py")
    base = pd.read_csv(path)
    base = base.loc[:, :].copy()
    base["misaligned_expert_index"] = base["centralization_gap"] - base["expert_epistemic_trust"]
    base["misaligned_information_index"] = base["centralization_gap"] - base["information_trust"]
    base["trust_alignment_dispersion"] = base[
        [
            "centralized_institutional_trust",
            "expert_epistemic_trust",
            "information_trust",
            "decentralized_social_trust",
        ]
    ].std(axis=1)
    base["trust_alignment_index"] = -base["trust_alignment_dispersion"]

    z_cols = [
        "log_gdp_per_capita",
        "human_development_index",
        "median_age",
        "log_population_density",
        "healthcare_capacity",
        "stringency_index",
        "state_capacity_index_2019",
        "centralized_institutional_trust",
        "decentralized_social_trust",
        "expert_epistemic_trust",
        "information_trust",
        "centralization_gap",
        "misaligned_expert_index",
        "misaligned_information_index",
        "trust_alignment_index",
    ]

    samples = {
        "all_wave7": base.copy(),
        "pre_shock_only": base[base["wvs_timing_group"].eq("pre_covid")].copy(),
        "pandemic_overlap_only": base[base["wvs_timing_group"].eq("pandemic_overlap")].copy(),
    }
    return {name: standardize_within_sample(df, z_cols) for name, df in samples.items()}


def run_tests(samples: dict[str, pd.DataFrame]) -> pd.DataFrame:
    controls_full = [
        "z7_log_gdp_per_capita",
        "z7_human_development_index",
        "z7_median_age",
        "z7_log_population_density",
        "z7_healthcare_capacity",
        "z7_stringency_index",
    ]
    controls_state = controls_full + ["z7_state_capacity_index_2019"]
    outcomes = [
        "deaths_per_million",
        "acute_deaths_per_million",
        "recovery_deaths_per_million",
        "excess_mortality",
        "vaccination_rate",
        "vaccination_rate_2021",
        "non_vaccinated_share",
    ]
    specs = {
        "central_full": controls_full + ["z7_centralized_institutional_trust"],
        "gap_full": controls_full + ["z7_centralization_gap"],
        "central_gap_full": controls_full + ["z7_centralized_institutional_trust", "z7_centralization_gap"],
        "central_state": controls_state + ["z7_centralized_institutional_trust"],
        "gap_state": controls_state + ["z7_centralization_gap"],
        "trust_alignment_state": controls_state + ["z7_trust_alignment_index"],
        "misaligned_expert_state": controls_state + ["z7_misaligned_expert_index"],
        "misaligned_information_state": controls_state + ["z7_misaligned_information_index"],
    }

    rows = []
    for sample_name, df in samples.items():
        for outcome in outcomes:
            for model, predictors in specs.items():
                rows.extend(run_model(df, sample_name, outcome, predictors, model))
    return pd.DataFrame(rows)


def compare_key_terms(results: pd.DataFrame) -> pd.DataFrame:
    key_terms = [
        "z7_centralized_institutional_trust",
        "z7_centralization_gap",
        "z7_trust_alignment_index",
        "z7_misaligned_expert_index",
        "z7_misaligned_information_index",
    ]
    key_models = [
        "central_full",
        "gap_full",
        "central_gap_full",
        "central_state",
        "gap_state",
        "trust_alignment_state",
        "misaligned_expert_state",
        "misaligned_information_state",
    ]
    focus = results[results["term"].isin(key_terms) & results["model"].isin(key_models)].copy()
    all_ref = focus[focus["sample"].eq("all_wave7")][["outcome", "model", "term", "coef", "p_value", "n"]]
    pre_ref = focus[focus["sample"].eq("pre_shock_only")][["outcome", "model", "term", "coef", "p_value", "n"]]
    comp = all_ref.merge(pre_ref, on=["outcome", "model", "term"], suffixes=("_all", "_pre"), how="inner")
    comp["same_direction"] = np.sign(comp["coef_all"]) == np.sign(comp["coef_pre"])
    comp["abs_coef_ratio_pre_to_all"] = comp["coef_pre"].abs() / comp["coef_all"].abs().replace(0, np.nan)
    return comp


def make_figure(results: pd.DataFrame) -> None:
    plot_terms = {
        "z7_centralized_institutional_trust": "central trust",
        "z7_centralization_gap": "centralization gap",
        "z7_misaligned_expert_index": "misaligned expert",
        "z7_misaligned_information_index": "misaligned info",
        "z7_trust_alignment_index": "trust alignment",
    }
    plot = results[
        results["sample"].isin(["all_wave7", "pre_shock_only"])
        & results["term"].isin(plot_terms.keys())
        & results["outcome"].isin(["deaths_per_million", "acute_deaths_per_million", "vaccination_rate", "non_vaccinated_share"])
        & results["model"].isin(["central_full", "gap_full", "misaligned_expert_state", "misaligned_information_state", "trust_alignment_state"])
    ].copy()
    if plot.empty:
        return
    plot["term_label"] = plot["term"].map(plot_terms)
    plot["label"] = plot["outcome"] + " | " + plot["model"] + " | " + plot["term_label"] + " | " + plot["sample"]
    plot = plot.sort_values(["outcome", "model", "term", "sample"])
    y = np.arange(len(plot))
    colors = np.where(plot["sample"].eq("pre_shock_only"), "#9b1c31", "#1f4e79")
    plt.figure(figsize=(12, max(7, len(plot) * 0.24)))
    for idx, row in enumerate(plot.itertuples(index=False)):
        plt.errorbar(
            row.coef,
            idx,
            xerr=[[row.coef - row.ci_low], [row.ci_high - row.coef]],
            fmt="o",
            color=colors[idx],
            ecolor=colors[idx],
            alpha=0.85,
            capsize=2,
        )
    plt.axvline(0, color="black", linewidth=1)
    plt.yticks(y, plot["label"], fontsize=6)
    plt.xlabel("Standardized-predictor OLS coefficient with HC3 95% CI")
    plt.title("Test 007: All Wave 7 vs Strict Pre-Shock Trust Baseline")
    plt.tight_layout()
    plt.savefig(FIGURES / "test007_preshock_coefficients.png", dpi=180)
    plt.close()


def write_report(samples: dict[str, pd.DataFrame], results: pd.DataFrame, comparison: pd.DataFrame) -> None:
    key_terms = [
        "z7_centralized_institutional_trust",
        "z7_centralization_gap",
        "z7_trust_alignment_index",
        "z7_misaligned_expert_index",
        "z7_misaligned_information_index",
    ]
    focus = results[
        results["sample"].isin(["all_wave7", "pre_shock_only"])
        & results["term"].isin(key_terms)
        & results["outcome"].isin(["deaths_per_million", "acute_deaths_per_million", "recovery_deaths_per_million", "vaccination_rate", "non_vaccinated_share"])
    ].copy()
    focus = focus.sort_values(["outcome", "sample", "model", "term"])

    counts = {name: int(len(df)) for name, df in samples.items()}
    same_direction_rate = float(comparison["same_direction"].mean()) if not comparison.empty else np.nan
    preshock_sig = focus[(focus["sample"].eq("pre_shock_only")) & (focus["p_value"].lt(0.05))]

    lines = [
        "# AetherCore Test 007: Strict Pre-Shock Trust Baseline",
        "",
        "## Purpose",
        "",
        "This pass reruns the main trust-topology models after excluding all countries whose WVS Wave 7 fieldwork occurred in 2020 or later. The goal is to test whether the central trust and centralization-gap findings survive when trust is measured before the COVID shock.",
        "",
        "## Sample Counts",
        "",
        "| Sample | Countries |",
        "|---|---:|",
        f"| All WVS Wave 7 countries in merged data | {counts.get('all_wave7', 0)} |",
        f"| Strict pre-shock WVS countries, fieldwork max <= 2019 | {counts.get('pre_shock_only', 0)} |",
        f"| Pandemic-overlap WVS countries, fieldwork max >= 2020 | {counts.get('pandemic_overlap_only', 0)} |",
        "",
        "## Main Interpretation",
        "",
    ]

    if comparison.empty:
        lines.append("No comparable all-vs-pre-shock model pairs were estimable.")
    else:
        lines.extend(
            [
                f"- Across comparable key-term models, the pre-shock coefficient kept the same direction as the all-Wave-7 coefficient in {same_direction_rate:.1%} of cases.",
                f"- Pre-shock key-term coefficients with p < 0.05 in the selected focus set: {len(preshock_sig)}.",
                "- Smaller sample size makes the pre-shock test harder to pass; p-values should be interpreted with more caution than coefficient direction and robustness across related outcomes.",
            ]
        )

    lines.extend(
        [
            "",
            "## Key Coefficients",
            "",
            "| Outcome | Sample | Model | Term | Coef | 95% CI | p | n | Adj. R2 |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for _, row in focus.iterrows():
        lines.append(
            f"| {row['outcome']} | {row['sample']} | {row['model']} | {row['term']} | "
            f"{row['coef']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | "
            f"{row['p_value']:.3f} | {int(row['n'])} | {row['adj_r2']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Comparison Table",
            "",
            "| Outcome | Model | Term | Coef all | Coef pre | Same direction | p all | p pre | n all | n pre |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for _, row in comparison.sort_values(["outcome", "model", "term"]).iterrows():
        lines.append(
            f"| {row['outcome']} | {row['model']} | {row['term']} | "
            f"{row['coef_all']:.3f} | {row['coef_pre']:.3f} | {bool(row['same_direction'])} | "
            f"{row['p_value_all']:.3f} | {row['p_value_pre']:.3f} | {int(row['n_all'])} | {int(row['n_pre'])} |"
        )

    lines.extend(
        [
            "",
            "## What Would Weaken the AetherCore Trust-Alignment Claim?",
            "",
            "The refined claim is weakened if the pre-shock-only subset reverses the central trust and centralization-gap directions, if vaccination/mortality associations disappear entirely, or if trust-alignment and misalignment indices add no information beyond material controls. It is strengthened if pre-shock-only coefficients preserve direction and remain meaningful despite the smaller sample.",
            "",
            "## Caveats",
            "",
            "- This pass still uses WVS Wave 7 only; it removes pandemic-overlap countries but does not add earlier WVS waves.",
            "- Strict pre-shock filtering reduces sample size from 65 to 38 countries.",
            "- Smaller samples reduce power and make confidence intervals wider.",
            "- The analysis remains observational and country-level.",
        ]
    )
    path = REPORT / "aethercore_test_007_preshock_baseline.md"
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    samples = build_samples()
    results = run_tests(samples)
    comparison = compare_key_terms(results)
    all_with_flags = pd.concat(
        [
            df.assign(test007_sample=name)
            for name, df in samples.items()
        ],
        ignore_index=True,
    )
    samples["pre_shock_only"].to_csv(DATA_PROCESSED / "aethercore_test007_preshock_only.csv", index=False)
    all_with_flags.to_csv(DATA_PROCESSED / "aethercore_test007_samples_long.csv", index=False)
    results.to_csv(OUTPUTS / "test007_preshock_regression_results.csv", index=False)
    comparison.to_csv(OUTPUTS / "test007_all_vs_preshock_comparison.csv", index=False)
    make_figure(results)
    write_report(samples, results, comparison)
    summary = {
        "all_wave7_countries": int(len(samples["all_wave7"])),
        "pre_shock_countries": int(len(samples["pre_shock_only"])),
        "pandemic_overlap_countries": int(len(samples["pandemic_overlap_only"])),
        "result_rows": int(len(results)),
        "comparison_rows": int(len(comparison)),
        "same_direction_share": float(comparison["same_direction"].mean()) if not comparison.empty else None,
    }
    (OUTPUTS / "test007_preshock_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Report: {REPORT / 'aethercore_test_007_preshock_baseline.md'}")


if __name__ == "__main__":
    main()
