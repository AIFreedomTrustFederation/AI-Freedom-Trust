"""AetherCore Test 004: Robustness and Influence Checks."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


PROJECT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = PROJECT / "data_processed"
OUTPUTS = PROJECT / "outputs"
FIGURES = PROJECT / "figures"
REPORT = PROJECT / "report"


def winsorize(s: pd.Series, lo: float = 0.05, hi: float = 0.95) -> pd.Series:
    return s.clip(lower=s.quantile(lo), upper=s.quantile(hi))


def standardize(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        sd = out[col].std(skipna=True)
        if pd.notna(sd) and sd > 0:
            out[f"z_{col}"] = (out[col] - out[col].mean(skipna=True)) / sd
    return out


def safe_log1p(series: pd.Series) -> pd.Series:
    out = pd.Series(np.nan, index=series.index, dtype=float)
    valid = series.gt(-1) & series.notna()
    out.loc[valid] = np.log1p(series.loc[valid])
    return out


def fit_ols(df: pd.DataFrame, outcome: str, predictors: list[str], model: str, transform: str) -> list[dict]:
    cols = [outcome] + predictors
    data = df[cols + ["iso_code", "location"]].dropna()
    if len(data) < len(predictors) + 10:
        return []
    fit = smf.ols(f"{outcome} ~ " + " + ".join(predictors), data=data).fit(cov_type="HC3")
    conf = fit.conf_int()
    return [
        {
            "outcome": outcome,
            "model": model,
            "transform": transform,
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
        for term in fit.params.index
    ]


def fit_rlm(df: pd.DataFrame, outcome: str, predictors: list[str], model: str) -> list[dict]:
    cols = [outcome] + predictors
    data = df[cols + ["iso_code", "location"]].dropna()
    if len(data) < len(predictors) + 10:
        return []
    y = data[outcome]
    x = sm.add_constant(data[predictors])
    fit = sm.RLM(y, x, M=sm.robust.norms.HuberT()).fit()
    return [
        {
            "outcome": outcome,
            "model": model,
            "transform": "robust_rlm_huber",
            "term": term,
            "coef": fit.params[term],
            "std_err_hc3": fit.bse[term],
            "p_value": fit.pvalues[term],
            "ci_low": fit.conf_int().loc[term, 0],
            "ci_high": fit.conf_int().loc[term, 1],
            "n": int(fit.nobs),
            "adj_r2": np.nan,
            "aic": np.nan,
            "bic": np.nan,
        }
        for term in fit.params.index
    ]


def leave_one_out(df: pd.DataFrame, outcome: str, predictors: list[str], term: str, model: str) -> pd.DataFrame:
    cols = [outcome] + predictors
    data = df[cols + ["iso_code", "location"]].dropna().copy()
    rows = []
    for iso in data["iso_code"]:
        sub = data[data["iso_code"] != iso]
        if len(sub) < len(predictors) + 10:
            continue
        fit = smf.ols(f"{outcome} ~ " + " + ".join(predictors), data=sub).fit(cov_type="HC3")
        rows.append(
            {
                "outcome": outcome,
                "model": model,
                "term": term,
                "left_out_iso": iso,
                "left_out_location": data.loc[data["iso_code"].eq(iso), "location"].iloc[0],
                "coef": fit.params.get(term, np.nan),
                "p_value": fit.pvalues.get(term, np.nan),
                "n": int(fit.nobs),
                "adj_r2": fit.rsquared_adj,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    path = DATA_PROCESSED / "aethercore_test003_trust_taxonomy_merged.csv"
    if not path.exists():
        raise SystemExit("Run Test 003 first.")
    df = pd.read_csv(path)
    controls = [
        "z_log_gdp_per_capita",
        "z_human_development_index",
        "z_median_age",
        "z_log_population_density",
        "z_healthcare_capacity",
        "z_stringency_index",
    ]
    focal = {
        "central": ["z_centralized_institutional_trust"],
        "gap": ["z_centralization_gap"],
        "taxonomy": [
            "z_centralized_institutional_trust",
            "z_decentralized_social_trust",
            "z_expert_epistemic_trust",
            "z_information_trust",
        ],
    }
    outcomes = ["deaths_per_million", "acute_deaths_per_million", "recovery_deaths_per_million", "excess_mortality"]
    work = df.copy()
    for outcome in outcomes:
        work[f"log1p_{outcome}"] = safe_log1p(work[outcome])
        work[f"winsor_{outcome}"] = winsorize(work[outcome])
        work[f"rank_{outcome}"] = work[outcome].rank(pct=True)

    rows = []
    for outcome in outcomes:
        for transform, out_col in [
            ("raw", outcome),
            ("log1p", f"log1p_{outcome}"),
            ("winsor_5_95", f"winsor_{outcome}"),
            ("rank_percentile", f"rank_{outcome}"),
        ]:
            for name, terms in focal.items():
                rows.extend(fit_ols(work, out_col, controls + terms, f"{name}_full_controls", transform))
        for name, terms in focal.items():
            rows.extend(fit_rlm(work, outcome, controls + terms, f"{name}_full_controls"))

    results = pd.DataFrame(rows)
    results.to_csv(OUTPUTS / "test004_robustness_results.csv", index=False)

    loo_frames = []
    for outcome in ["deaths_per_million", "acute_deaths_per_million", "recovery_deaths_per_million"]:
        loo_frames.append(leave_one_out(work, outcome, controls + focal["central"], "z_centralized_institutional_trust", "central_full_controls"))
        loo_frames.append(leave_one_out(work, outcome, controls + focal["gap"], "z_centralization_gap", "gap_full_controls"))
    loo = pd.concat(loo_frames, ignore_index=True)
    loo.to_csv(OUTPUTS / "test004_leave_one_out.csv", index=False)

    focus_terms = ["z_centralized_institutional_trust", "z_centralization_gap"]
    focus = results[results["term"].isin(focus_terms)].copy()
    plt.figure(figsize=(11, max(5, 0.18 * len(focus))))
    focus = focus.sort_values(["outcome", "term", "transform"])
    focus["label"] = focus["outcome"] + " | " + focus["transform"] + " | " + focus["term"]
    y = np.arange(len(focus))
    plt.errorbar(
        focus["coef"],
        y,
        xerr=[focus["coef"] - focus["ci_low"], focus["ci_high"] - focus["coef"]],
        fmt="o",
        capsize=2,
    )
    plt.axvline(0, color="black", linewidth=1)
    plt.yticks(y, focus["label"], fontsize=5)
    plt.title("Test 004 Robustness: Central Trust and Centralization Gap")
    plt.tight_layout()
    plt.savefig(FIGURES / "test004_robustness_coefficients.png", dpi=180)
    plt.close()

    loo_summary = (
        loo.groupby(["outcome", "model", "term"], as_index=False)
        .agg(min_coef=("coef", "min"), median_coef=("coef", "median"), max_coef=("coef", "max"), sign_flips=("coef", lambda s: int(((s > 0) != (s.median() > 0)).sum())), min_p=("p_value", "min"), max_p=("p_value", "max"))
    )
    loo_summary.to_csv(OUTPUTS / "test004_leave_one_out_summary.csv", index=False)

    report = REPORT / "aethercore_test_004_robustness.md"
    lines = [
        "# AetherCore Test 004: Robustness and Influence Checks",
        "",
        "## Purpose",
        "",
        "This pass checks whether the Test 003 central-institutional-trust and centralization-gap signals survive alternative outcome transformations, robust regression, and leave-one-country-out influence checks.",
        "",
        "## Robustness Coefficients",
        "",
        "| Outcome | Transform | Model | Term | Coef | 95% CI | p | n |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for _, row in focus.iterrows():
        lines.append(
            f"| {row['outcome']} | {row['transform']} | {row['model']} | {row['term']} | "
            f"{row['coef']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | {row['p_value']:.3f} | {int(row['n'])} |"
        )
    lines.extend(["", "## Leave-One-Out Summary", "", "| Outcome | Model | Term | Min Coef | Median Coef | Max Coef | Sign Flips |", "|---|---|---:|---:|---:|---:|---:|"])
    for _, row in loo_summary.iterrows():
        lines.append(
            f"| {row['outcome']} | {row['model']} | {row['term']} | {row['min_coef']:.3f} | "
            f"{row['median_coef']:.3f} | {row['max_coef']:.3f} | {int(row['sign_flips'])} |"
        )
    lines.extend(["", "## Interpretation", "", "The signal is more credible if coefficient signs remain stable across transformations and leave-one-out runs. Sign flips or large swings indicate sensitivity to influential countries."])
    report.write_text("\n".join(lines), encoding="utf-8")

    summary = {"result_rows": int(len(results)), "leave_one_out_rows": int(len(loo))}
    (OUTPUTS / "test004_robustness_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
