"""AetherCore Test 008: Post-shock trust topology and Sphere of Fear proxy.

This pass treats WVS Wave 7 countries with 2020+ fieldwork as pandemic-overlap
trust observations. It does not claim true within-country pre/post change,
because Wave 7 does not provide pre- and post-shock observations for the same
countries. Instead it asks whether the post-shock trust topology is consistent
with a measurable Sphere of Fear pattern:

    institutional distrust + decentralized trust migration
    + weak expert/information trust
    + contraction outcomes such as non-vaccination, control belief, and deaths.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from scipy import stats


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT = SCRIPT_DIR.parents[0]
DATA_PROCESSED = PROJECT / "data_processed"
OUTPUTS = PROJECT / "outputs"
FIGURES = PROJECT / "figures"
REPORT = PROJECT / "report"


def ensure_dirs() -> None:
    for directory in [DATA_PROCESSED, OUTPUTS, FIGURES, REPORT]:
        directory.mkdir(parents=True, exist_ok=True)


def zscore(series: pd.Series) -> pd.Series:
    sd = series.std(skipna=True)
    if pd.isna(sd) or sd == 0:
        return pd.Series(np.nan, index=series.index)
    return (series - series.mean(skipna=True)) / sd


def add_sphere_variables(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["institutional_distrust"] = 1 - out["centralized_institutional_trust"]
    out["expert_distrust"] = 1 - out["expert_epistemic_trust"]
    out["information_distrust"] = 1 - out["information_trust"]
    out["decentralized_over_central_gap"] = out["centralization_gap"]
    out["fear_trust_topology_index"] = (
        zscore(out["institutional_distrust"])
        + zscore(out["decentralized_over_central_gap"])
        + zscore(out["expert_distrust"])
        + zscore(out["information_distrust"])
    ) / 4
    out["fear_misalignment_index"] = (
        zscore(out["centralization_gap"])
        + zscore(out["misaligned_expert_index"])
        + zscore(out["misaligned_information_index"])
    ) / 3
    behavior_cols = [
        "government_control_belief_vaccine_rollout_2021",
        "vaccine_refusal_vaccine_rollout_2021",
        "mask_refusal_outside_acute_2020",
    ]
    present = [c for c in behavior_cols if c in out.columns]
    if present:
        out["fear_behavior_index"] = pd.concat([zscore(out[c]) for c in present], axis=1).mean(axis=1)
    else:
        out["fear_behavior_index"] = np.nan
    return out


def load_data() -> pd.DataFrame:
    path = DATA_PROCESSED / "aethercore_test007_samples_long.csv"
    if not path.exists():
        raise SystemExit("Run Test 007 first: scripts/run_preshock_test007.py")
    df = pd.read_csv(path)
    df = df[df["test007_sample"].isin(["pre_shock_only", "pandemic_overlap_only"])].copy()
    # The long file contains separate sample copies; these two are mutually exclusive.
    df["post_shock_wvs"] = df["test007_sample"].eq("pandemic_overlap_only").astype(int)
    return add_sphere_variables(df)


def group_tests(df: pd.DataFrame) -> pd.DataFrame:
    variables = [
        "centralized_institutional_trust",
        "decentralized_social_trust",
        "centralization_gap",
        "expert_epistemic_trust",
        "information_trust",
        "institutional_distrust",
        "expert_distrust",
        "information_distrust",
        "misaligned_expert_index",
        "misaligned_information_index",
        "fear_trust_topology_index",
        "fear_misalignment_index",
        "deaths_per_million",
        "vaccination_rate",
        "non_vaccinated_share",
    ]
    rows = []
    for var in variables:
        if var not in df.columns:
            continue
        pre = df[df["post_shock_wvs"].eq(0)][var].dropna()
        post = df[df["post_shock_wvs"].eq(1)][var].dropna()
        if len(pre) < 5 or len(post) < 5:
            continue
        t = stats.ttest_ind(post, pre, equal_var=False, nan_policy="omit")
        try:
            u = stats.mannwhitneyu(post, pre, alternative="two-sided")
            u_p = float(u.pvalue)
        except ValueError:
            u_p = np.nan
        pooled_sd = np.sqrt(((len(pre) - 1) * pre.var(ddof=1) + (len(post) - 1) * post.var(ddof=1)) / (len(pre) + len(post) - 2))
        d = (post.mean() - pre.mean()) / pooled_sd if pooled_sd and pd.notna(pooled_sd) else np.nan
        rows.append(
            {
                "variable": var,
                "pre_n": int(len(pre)),
                "post_n": int(len(post)),
                "pre_mean": float(pre.mean()),
                "post_mean": float(post.mean()),
                "post_minus_pre": float(post.mean() - pre.mean()),
                "cohens_d_post_minus_pre": float(d) if pd.notna(d) else np.nan,
                "welch_t_p": float(t.pvalue) if pd.notna(t.pvalue) else np.nan,
                "mann_whitney_p": u_p,
            }
        )
    return pd.DataFrame(rows)


def columns_from_terms(terms: list[str]) -> list[str]:
    cols: list[str] = []
    for term in terms:
        cols.extend(part.strip() for part in term.split(":"))
    return sorted(set(cols))


def run_model(df: pd.DataFrame, sample: str, outcome: str, predictors: list[str], model: str, min_n: int) -> list[dict]:
    needed = [outcome] + columns_from_terms(predictors)
    if any(col not in df.columns for col in needed):
        return []
    data = df[needed + ["iso_code", "location"]].dropna()
    if len(data) < max(min_n, len(predictors) + 5):
        return []
    formula = f"{outcome} ~ " + " + ".join(predictors)
    fit = smf.ols(formula, data=data).fit(cov_type="HC3")
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
        }
        for term in fit.params.index
    ]


def add_standardized_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in [
        "log_gdp_per_capita",
        "human_development_index",
        "median_age",
        "centralization_gap",
        "centralized_institutional_trust",
        "expert_epistemic_trust",
        "information_trust",
        "fear_trust_topology_index",
        "fear_misalignment_index",
        "misaligned_expert_index",
        "misaligned_information_index",
    ]:
        if col in out.columns:
            out[f"z8_{col}"] = zscore(out[col])
    return out


def run_models(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    samples = {
        "all_pre_vs_post": df,
        "post_shock_wvs_only": df[df["post_shock_wvs"].eq(1)].copy(),
    }
    outcomes = [
        "deaths_per_million",
        "acute_deaths_per_million",
        "recovery_deaths_per_million",
        "vaccination_rate",
        "non_vaccinated_share",
    ]
    compact_controls = ["z8_log_gdp_per_capita", "z8_human_development_index", "z8_median_age"]
    specs = {
        "sphere_bivariate": ["z8_fear_trust_topology_index"],
        "misalignment_bivariate": ["z8_fear_misalignment_index"],
        "gap_bivariate": ["z8_centralization_gap"],
        "central_bivariate": ["z8_centralized_institutional_trust"],
        "sphere_compact_controls": compact_controls + ["z8_fear_trust_topology_index"],
        "misalignment_compact_controls": compact_controls + ["z8_fear_misalignment_index"],
        "post_indicator_compact": compact_controls + ["post_shock_wvs"],
        "post_x_sphere": compact_controls + ["post_shock_wvs", "z8_fear_trust_topology_index", "post_shock_wvs:z8_fear_trust_topology_index"],
    }
    for sample_name, sample_df in samples.items():
        min_n = 16 if sample_name == "post_shock_wvs_only" else 25
        working = add_standardized_columns(sample_df)
        for outcome in outcomes:
            for model, predictors in specs.items():
                if sample_name == "post_shock_wvs_only" and ("post_shock_wvs" in " ".join(predictors)):
                    continue
                rows.extend(run_model(working, sample_name, outcome, predictors, model, min_n=min_n))

    # Tiny behavioral layer, reported separately by n.
    behavior_outcomes = [
        "government_control_belief_vaccine_rollout_2021",
        "health_authority_vaccine_trust_vaccine_rollout_2021",
        "vaccine_refusal_vaccine_rollout_2021",
        "mask_refusal_outside_acute_2020",
    ]
    working = add_standardized_columns(df)
    for outcome in behavior_outcomes:
        for model, predictors in {
            "behavior_sphere_bivariate": ["z8_fear_trust_topology_index"],
            "behavior_gap_bivariate": ["z8_centralization_gap"],
            "behavior_misalignment_bivariate": ["z8_fear_misalignment_index"],
        }.items():
            rows.extend(run_model(working, "behavior_overlap_tiny", outcome, predictors, model, min_n=4))
    return pd.DataFrame(rows)


def make_figures(df: pd.DataFrame) -> None:
    plot_df = df.copy()
    plot_df["timing"] = np.where(plot_df["post_shock_wvs"].eq(1), "Pandemic-overlap WVS", "Strict pre-shock WVS")
    for var, filename, title in [
        ("centralization_gap", "test008_centralization_gap_by_timing.png", "Centralization Gap by WVS Timing"),
        ("fear_trust_topology_index", "test008_sphere_proxy_by_timing.png", "Sphere of Fear Trust-Topology Proxy by WVS Timing"),
    ]:
        data = plot_df[[var, "timing"]].dropna()
        if len(data) < 10:
            continue
        plt.figure(figsize=(8, 5.5))
        sns.boxplot(data=data, x="timing", y=var, color="#d8e3ef")
        sns.stripplot(data=data, x="timing", y=var, color="#1f4e79", alpha=0.75)
        plt.title(title)
        plt.xticks(rotation=10)
        plt.tight_layout()
        plt.savefig(FIGURES / filename, dpi=180)
        plt.close()

    for x, y, filename in [
        ("fear_trust_topology_index", "deaths_per_million", "test008_sphere_vs_deaths.png"),
        ("fear_misalignment_index", "deaths_per_million", "test008_misalignment_vs_deaths.png"),
        ("fear_misalignment_index", "non_vaccinated_share", "test008_misalignment_vs_nonvaccinated.png"),
    ]:
        data = plot_df[[x, y, "timing", "location"]].dropna()
        if len(data) < 12:
            continue
        plt.figure(figsize=(8, 5.5))
        sns.scatterplot(data=data, x=x, y=y, hue="timing", s=55)
        sns.regplot(data=data, x=x, y=y, scatter=False, color="#9b1c31")
        plt.title(f"{x} vs {y}")
        plt.tight_layout()
        plt.savefig(FIGURES / filename, dpi=180)
        plt.close()


def write_report(df: pd.DataFrame, group: pd.DataFrame, results: pd.DataFrame) -> None:
    focus_terms = [
        "z8_fear_trust_topology_index",
        "z8_fear_misalignment_index",
        "z8_centralization_gap",
        "z8_centralized_institutional_trust",
        "post_shock_wvs",
        "post_shock_wvs:z8_fear_trust_topology_index",
    ]
    focus = results[results["term"].isin(focus_terms)].copy()
    lines = [
        "# AetherCore Test 008: Post-Shock Trust Topology and Sphere of Fear Proxy",
        "",
        "## Purpose",
        "",
        "This pass asks whether post-shock trust observations show a measurable pattern consistent with the AetherCore Sphere of Fear model: contraction away from centralized institutions, migration toward decentralized trust channels, weakened expert/information trust, and worse crisis-coordination outcomes.",
        "",
        "This is not a true longitudinal pre/post design. WVS Wave 7 does not provide the same countries measured both before and after COVID. The comparison is between countries whose WVS fieldwork ended before 2020 and countries whose WVS fieldwork occurred in 2020 or later.",
        "",
        "## Operational Definition",
        "",
        "`fear_trust_topology_index` is a trust-only proxy combining standardized institutional distrust, centralization gap, expert distrust, and information distrust.",
        "",
        "`fear_misalignment_index` combines standardized centralization gap, expert misalignment, and information misalignment.",
        "",
        "In layman's terms, the Sphere of Fear proxy is high when trust has moved away from central institutions and reliable knowledge channels into a more disconnected social configuration.",
        "",
        "## Sample Counts",
        "",
        "| Group | Countries |",
        "|---|---:|",
        f"| Strict pre-shock WVS | {int((df['post_shock_wvs'] == 0).sum())} |",
        f"| Pandemic-overlap WVS | {int((df['post_shock_wvs'] == 1).sum())} |",
        "",
        "## Pre-Shock vs Pandemic-Overlap Differences",
        "",
        "Main result: the pandemic-overlap WVS group does not show a higher average Sphere-of-Fear trust-topology score than the strict pre-shock group. In fact, the group mean is lower, and the difference is not statistically significant. Therefore, this pass does not support a simple claim that post-shock countries universally collapsed into higher fear topology.",
        "",
        "However, within the pandemic-overlap group, the Sphere-of-Fear and misalignment proxies are associated with worse outcomes, especially deaths per million, acute deaths, lower vaccination, and higher non-vaccinated share. The stronger finding is therefore conditional: the fear topology is harmful where it appears, not universally higher after the shock.",
        "",
        "| Variable | Pre mean | Post mean | Post - Pre | Cohen d | Welch p |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for _, row in group.sort_values("variable").iterrows():
        lines.append(
            f"| {row['variable']} | {row['pre_mean']:.3f} | {row['post_mean']:.3f} | "
            f"{row['post_minus_pre']:.3f} | {row['cohens_d_post_minus_pre']:.3f} | {row['welch_t_p']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Regression Signals",
            "",
            "| Sample | Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for _, row in focus.sort_values(["sample", "outcome", "model", "term"]).iterrows():
        lines.append(
            f"| {row['sample']} | {row['outcome']} | {row['model']} | {row['term']} | "
            f"{row['coef']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | "
            f"{row['p_value']:.3f} | {int(row['n'])} | {row['adj_r2']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The central scientific question is whether post-shock trust topology looks more contracted and whether that contraction proxy aligns with worse recovery outcomes. The first condition is not supported as a universal group-level claim: pandemic-overlap countries do not have higher mean fear-topology scores than strict pre-shock countries. The second condition receives stronger support: among pandemic-overlap countries, higher fear-topology and misalignment scores predict worse mortality and vaccination outcomes.",
            "",
            "This refines the Sphere of Fear hypothesis. The evidence does not say that all societies collapsed into fear after COVID. It says that where trust becomes configured as institutional distrust, centralization gap, and expert/information misalignment, outcomes look worse. The collapse pattern is a topology within the post-shock field, not a universal post-shock average.",
            "",
            "Behavioral evidence remains extremely limited in the pandemic-overlap WVS group because YouGov overlap is very small. Those rows should be treated as illustrative, not confirmatory.",
            "",
            "## What Would Falsify or Weaken This Layer?",
            "",
            "- Pandemic-overlap WVS countries do not show higher institutional distrust, centralization gap, or fear-topology scores.",
            "- Fear-topology and misalignment indices do not predict mortality, vaccination gaps, or behavioral contraction proxies.",
            "- Direct longitudinal data show that post-shock trust does not migrate away from institutions after severe shocks.",
            "- Information/media variables fully explain the fear-topology pattern.",
            "",
            "## Next Step",
            "",
            "The stronger future design is true panel or repeated-cross-section analysis: measure trust before the shock, during the shock, and after the shock in the same country or individual samples. That would allow direct estimation of trust migration into or out of the Sphere of Fear.",
        ]
    )
    (REPORT / "aethercore_test_008_postshock_sphere.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    df = load_data()
    group = group_tests(df)
    results = run_models(df)
    make_figures(df)
    df.to_csv(DATA_PROCESSED / "aethercore_test008_postshock_sphere.csv", index=False)
    group.to_csv(OUTPUTS / "test008_group_differences.csv", index=False)
    results.to_csv(OUTPUTS / "test008_postshock_sphere_regression_results.csv", index=False)
    write_report(df, group, results)
    summary = {
        "pre_shock_countries": int((df["post_shock_wvs"] == 0).sum()),
        "pandemic_overlap_countries": int((df["post_shock_wvs"] == 1).sum()),
        "group_difference_rows": int(len(group)),
        "regression_rows": int(len(results)),
    }
    (OUTPUTS / "test008_postshock_sphere_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Report: {REPORT / 'aethercore_test_008_postshock_sphere.md'}")


if __name__ == "__main__":
    main()
