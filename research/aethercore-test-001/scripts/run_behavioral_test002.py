"""AetherCore Test 002: Trust Density and COVID Behavioral Resistance.

This pass uses Imperial College London / YouGov COVID-19 Behaviour Tracker
respondent-level files to build direct behavioral proxies for:

- vaccine refusal / willingness
- mask non-compliance
- confidence in government health authorities
- government-control conspiracy belief

It then tests whether pre-existing WVS Wave 7 trust variables predict these
behavioral outcomes. This is a small-N cross-country screen, not proof.
"""

from __future__ import annotations

import io
import json
import math
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import statsmodels.formula.api as smf


PROJECT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT / "data_raw"
DATA_PROCESSED = PROJECT / "data_processed"
OUTPUTS = PROJECT / "outputs"
FIGURES = PROJECT / "figures"
REPORT = PROJECT / "report"
YOUGOV_RAW = DATA_RAW / "yougov_behavior_tracker"

GITHUB_API = "https://api.github.com/repos/YouGov-Data/covid-19-tracker/contents/data"
GITHUB_RAW = "https://github.com/YouGov-Data/covid-19-tracker/raw/master/data"
REPO_URL = "https://github.com/YouGov-Data/covid-19-tracker"

COUNTRY_ISO = {
    "australia": "AUS",
    "brazil": "BRA",
    "canada": "CAN",
    "china": "CHN",
    "denmark": "DNK",
    "finland": "FIN",
    "france": "FRA",
    "germany": "DEU",
    "hong-kong": "HKG",
    "india": "IND",
    "indonesia": "IDN",
    "israel": "ISR",
    "italy": "ITA",
    "japan": "JPN",
    "malaysia": "MYS",
    "mexico": "MEX",
    "netherlands": "NLD",
    "norway": "NOR",
    "philippines": "PHL",
    "saudi-arabia": "SAU",
    "singapore": "SGP",
    "south-korea": "KOR",
    "spain": "ESP",
    "sweden": "SWE",
    "taiwan": "TWN",
    "thailand": "THA",
    "united-arab-emirates": "ARE",
    "united-kingdom": "GBR",
    "united-states": "USA",
    "vietnam": "VNM",
}

SELECTED_COLUMNS = [
    "endtime",
    "qweek",
    "weight",
    "i12_health_1",
    "m2",
    "m3",
    "vac_1",
    "vac_2",
    "vac2_2",
    "vac2_3",
    "vac9",
    "vac12_12",
    "WCRex1",
    "Vent_3",
]


def ensure_dirs() -> None:
    for directory in [YOUGOV_RAW, DATA_PROCESSED, OUTPUTS, FIGURES, REPORT]:
        directory.mkdir(parents=True, exist_ok=True)


def download_country_files() -> list[Path]:
    ensure_dirs()
    response = requests.get(GITHUB_API, timeout=60)
    response.raise_for_status()
    items = response.json()
    files = []
    for item in items:
        name = item["name"]
        if not name.endswith((".csv", ".zip")):
            continue
        dest = YOUGOV_RAW / name
        if not dest.exists() or dest.stat().st_size < 1000:
            url = f"{GITHUB_RAW}/{name}"
            with requests.get(url, stream=True, timeout=240) as r:
                r.raise_for_status()
                with dest.open("wb") as handle:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            handle.write(chunk)
        files.append(dest)
    return sorted(files)


def read_country_file(path: Path) -> pd.DataFrame:
    usecols = lambda c: c in SELECTED_COLUMNS
    def read_csv_handle(handle):
        for enc in ["utf-8", "latin1", "cp1252"]:
            try:
                return pd.read_csv(handle, usecols=usecols, low_memory=False, encoding=enc)
            except UnicodeDecodeError:
                if hasattr(handle, "seek"):
                    handle.seek(0)
                continue
        if hasattr(handle, "seek"):
            handle.seek(0)
        return pd.read_csv(handle, usecols=usecols, low_memory=False, encoding="latin1")

    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as zf:
            csvs = [m for m in zf.namelist() if m.endswith(".csv")]
            if not csvs:
                raise FileNotFoundError(path)
            data = io.BytesIO(zf.read(csvs[0]))
            return read_csv_handle(data)
    with path.open("rb") as handle:
        return read_csv_handle(handle)


def slug_from_path(path: Path) -> str:
    return path.stem


def weighted_mean(value: pd.Series, weight: pd.Series) -> float:
    valid = value.notna() & weight.notna() & (weight > 0)
    if valid.sum() == 0:
        return np.nan
    return float(np.average(value[valid], weights=weight[valid]))


def normalize_text(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().replace({"nan": np.nan, "": np.nan})


def frequency_scale(series: pd.Series) -> pd.Series:
    mapping = {
        "always": 1.0,
        "frequently": 0.75,
        "sometimes": 0.50,
        "rarely": 0.25,
        "not at all": 0.0,
    }
    return normalize_text(series).map(mapping)


def refusal_from_frequency(series: pd.Series) -> pd.Series:
    txt = normalize_text(series)
    values = np.where(txt.isin(["rarely", "not at all"]), 1.0, np.where(txt.notna(), 0.0, np.nan))
    return pd.Series(values, index=series.index)


def agree_scale(series: pd.Series) -> pd.Series:
    txt = normalize_text(series)
    mapping = {
        "1 - strongly agree": 1.0,
        "1 – strongly agree": 1.0,
        "strongly agree": 1.0,
        "2": 0.75,
        "3": 0.50,
        "4": 0.25,
        "5 - strongly disagree": 0.0,
        "5 – strongly disagree": 0.0,
        "strongly disagree": 0.0,
    }
    numeric = pd.to_numeric(series, errors="coerce")
    scaled = np.where(numeric.between(1, 5), (5.0 - numeric) / 4.0, np.nan)
    return pd.Series(scaled, index=series.index).where(pd.notna(scaled), txt.map(mapping))


def disagree_indicator(series: pd.Series) -> pd.Series:
    txt = normalize_text(series)
    numeric = pd.to_numeric(series, errors="coerce")
    disagree = numeric.isin([4, 5]) | txt.isin(["4", "5 - strongly disagree", "5 – strongly disagree", "strongly disagree"])
    answered = numeric.between(1, 5) | txt.notna()
    values = np.where(disagree, 1.0, np.where(answered, 0.0, np.nan))
    return pd.Series(values, index=series.index)


def yes_indicator(series: pd.Series) -> pd.Series:
    txt = normalize_text(series)
    numeric = pd.to_numeric(series, errors="coerce")
    yes = numeric.eq(1) | txt.eq("yes")
    no = numeric.eq(0) | txt.eq("no")
    values = np.where(yes, 1.0, np.where(no, 0.0, np.nan))
    return pd.Series(values, index=series.index)


def government_handling_good(series: pd.Series) -> pd.Series:
    txt = normalize_text(series)
    good = txt.isin(["very well", "somewhat well"])
    bad = txt.isin(["somewhat badly", "very badly"])
    values = np.where(good, 1.0, np.where(bad, 0.0, np.nan))
    return pd.Series(values, index=series.index)


def numeric_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    num = pd.to_numeric(numerator, errors="coerce")
    den = pd.to_numeric(denominator, errors="coerce")
    return (num / den).where((den > 0) & (num >= 0) & (num <= den))


def phase(date: pd.Timestamp) -> str | float:
    if pd.isna(date):
        return np.nan
    if date <= pd.Timestamp("2020-12-31"):
        return "acute_2020"
    if date <= pd.Timestamp("2021-12-31"):
        return "vaccine_rollout_2021"
    return "early_recovery_2022"


def add_behavior_variables(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["date"] = pd.to_datetime(out["endtime"], errors="coerce", dayfirst=True)
    out["phase"] = out["date"].map(phase)
    out["weight"] = pd.to_numeric(out.get("weight", 1.0), errors="coerce").fillna(1.0)

    out["mask_compliance_outside"] = frequency_scale(out.get("i12_health_1", pd.Series(index=out.index, dtype=object)))
    out["mask_refusal_outside"] = refusal_from_frequency(out.get("i12_health_1", pd.Series(index=out.index, dtype=object)))
    if "m2" in out and "m3" in out:
        out["mask_days_ratio"] = numeric_ratio(out["m3"], out["m2"])
    else:
        out["mask_days_ratio"] = np.nan

    vac_intent_now = agree_scale(out.get("vac_1", pd.Series(index=out.index, dtype=object)))
    vac_intent_2021 = agree_scale(out.get("vac_2", pd.Series(index=out.index, dtype=object)))
    out["vaccine_intent"] = vac_intent_now.combine_first(vac_intent_2021)
    out["vaccine_refusal"] = disagree_indicator(out.get("vac_1", pd.Series(index=out.index, dtype=object))).combine_first(
        disagree_indicator(out.get("vac_2", pd.Series(index=out.index, dtype=object)))
    )
    out["vaccine_side_effect_worry"] = agree_scale(out.get("vac2_2", pd.Series(index=out.index, dtype=object)))
    out["health_authority_vaccine_trust"] = agree_scale(out.get("vac2_3", pd.Series(index=out.index, dtype=object)))
    out["government_control_belief"] = yes_indicator(out.get("vac12_12", pd.Series(index=out.index, dtype=object)))
    out["government_handling_good"] = government_handling_good(out.get("WCRex1", pd.Series(index=out.index, dtype=object)))
    out["avoid_others_compliance"] = frequency_scale(out.get("Vent_3", pd.Series(index=out.index, dtype=object)))
    return out


def aggregate_country_behavior() -> tuple[pd.DataFrame, pd.DataFrame]:
    files = download_country_files()
    country_phase_rows = []
    country_overall_rows = []

    variables = [
        "mask_compliance_outside",
        "mask_refusal_outside",
        "mask_days_ratio",
        "vaccine_intent",
        "vaccine_refusal",
        "vaccine_side_effect_worry",
        "health_authority_vaccine_trust",
        "government_control_belief",
        "government_handling_good",
        "avoid_others_compliance",
    ]

    for path in files:
        slug = slug_from_path(path)
        iso = COUNTRY_ISO.get(slug)
        if iso is None:
            continue
        print(f"Aggregating YouGov behavior: {slug}")
        df = add_behavior_variables(read_country_file(path))
        df["iso_code"] = iso
        df["country_slug"] = slug

        overall = {"iso_code": iso, "country_slug": slug, "n_behavior": len(df)}
        for variable in variables:
            overall[f"{variable}_overall"] = weighted_mean(df[variable], df["weight"])
            overall[f"{variable}_n_overall"] = int(df[variable].notna().sum())
        country_overall_rows.append(overall)

        for ph, g in df.dropna(subset=["phase"]).groupby("phase"):
            row = {"iso_code": iso, "country_slug": slug, "phase": ph, "n_behavior_phase": len(g)}
            for variable in variables:
                row[variable] = weighted_mean(g[variable], g["weight"])
                row[f"{variable}_n"] = int(g[variable].notna().sum())
            country_phase_rows.append(row)

    phase_df = pd.DataFrame(country_phase_rows)
    overall_df = pd.DataFrame(country_overall_rows)
    if not phase_df.empty:
        wide = phase_df.pivot(index=["iso_code", "country_slug"], columns="phase")
        wide.columns = [f"{var}_{ph}" for var, ph in wide.columns]
        wide = wide.reset_index()
        overall_df = overall_df.merge(wide, on=["iso_code", "country_slug"], how="left")
    overall_df.to_csv(DATA_PROCESSED / "yougov_behavior_country.csv", index=False)
    phase_df.to_csv(DATA_PROCESSED / "yougov_behavior_country_phase_long.csv", index=False)
    return overall_df, phase_df


def standardize(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col in out:
            sd = out[col].std(skipna=True)
            if pd.notna(sd) and sd > 0:
                out[f"z_{col}"] = (out[col] - out[col].mean(skipna=True)) / sd
    return out


def run_ols(df: pd.DataFrame, outcome: str, predictors: list[str], model: str) -> list[dict]:
    cols = [outcome] + predictors
    if any(c not in df.columns for c in cols):
        return []
    data = df[cols + ["iso_code", "location"]].dropna()
    min_n = 8 if model.startswith("bivariate") else 12
    if len(data) < max(min_n, len(predictors) + 6):
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


def run_behavior_models(df: pd.DataFrame) -> pd.DataFrame:
    outcomes = [
        "vaccine_refusal_vaccine_rollout_2021",
        "vaccine_intent_vaccine_rollout_2021",
        "health_authority_vaccine_trust_vaccine_rollout_2021",
        "government_control_belief_vaccine_rollout_2021",
        "mask_refusal_outside_acute_2020",
        "mask_compliance_outside_acute_2020",
        "mask_refusal_outside_early_recovery_2022",
        "avoid_others_compliance_early_recovery_2022",
    ]
    trust_terms = {
        "trust_density": ["z_trust_density_composite"],
        "generalized_trust": ["z_trust_generalized"],
        "institutional_trust": ["z_trust_institutions"],
        "expert_proxy_trust": ["z_trust_experts"],
        "information_proxy": ["z_information_integrity_proxy"],
    }
    compact_controls = ["z_log_gdp_per_capita", "z_human_development_index", "z_median_age"]
    rows = []
    for outcome in outcomes:
        for name, term in trust_terms.items():
            rows.extend(run_ols(df, outcome, term, f"bivariate_{name}"))
            rows.extend(run_ols(df, outcome, compact_controls + term, f"compact_controls_{name}"))
    return pd.DataFrame(rows)


def make_behavior_figures(df: pd.DataFrame, results: pd.DataFrame) -> None:
    pairs = [
        ("trust_density_composite", "vaccine_refusal_vaccine_rollout_2021", "test002_trust_vs_vaccine_refusal.png"),
        ("trust_density_composite", "mask_refusal_outside_acute_2020", "test002_trust_vs_mask_refusal_acute.png"),
        ("trust_institutions", "government_control_belief_vaccine_rollout_2021", "test002_institutional_trust_vs_control_belief.png"),
        ("trust_experts", "health_authority_vaccine_trust_vaccine_rollout_2021", "test002_expert_proxy_vs_health_authority_trust.png"),
    ]
    for x, y, filename in pairs:
        if x not in df or y not in df:
            continue
        plot = df[[x, y, "location"]].dropna()
        if len(plot) < 8:
            continue
        plt.figure(figsize=(8, 5.5))
        sns.regplot(data=plot, x=x, y=y, scatter_kws={"s": 48, "alpha": 0.8}, line_kws={"color": "#9b1c31"})
        plt.title(f"{x} vs {y} (n={len(plot)})")
        plt.tight_layout()
        plt.savefig(FIGURES / filename, dpi=180)
        plt.close()

    coef = results[
        results["term"].isin(
            [
                "z_trust_density_composite",
                "z_trust_generalized",
                "z_trust_institutions",
                "z_trust_experts",
                "z_information_integrity_proxy",
            ]
        )
    ].copy()
    if coef.empty:
        return
    coef = coef.sort_values(["outcome", "model", "term"])
    coef["label"] = coef["outcome"] + " | " + coef["model"].str.replace("compact_controls_", "ctrl_", regex=False)
    plt.figure(figsize=(12, max(6, 0.24 * len(coef))))
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
    plt.yticks(y, coef["label"], fontsize=6)
    plt.xlabel("OLS coefficient with HC3 95% CI")
    plt.title("Test 002 Trust Coefficients Across Behavioral Outcomes")
    plt.tight_layout()
    plt.savefig(FIGURES / "test002_behavior_coefficient_plot.png", dpi=180)
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


def write_report(merged: pd.DataFrame, results: pd.DataFrame) -> None:
    report = REPORT / "aethercore_test_002_behavioral_resistance.md"
    trust_rows = results[
        results["model"].str.startswith("compact_controls")
        & results["term"].isin(
            [
                "z_trust_density_composite",
                "z_trust_generalized",
                "z_trust_institutions",
                "z_trust_experts",
                "z_information_integrity_proxy",
            ]
        )
    ].copy()
    if trust_rows.empty:
        trust_rows = results[
            results["term"].isin(
                [
                    "z_trust_density_composite",
                    "z_trust_generalized",
                    "z_trust_institutions",
                    "z_trust_experts",
                    "z_information_integrity_proxy",
                ]
            )
        ].copy()
    bivar_rows = results[
        results["model"].str.startswith("bivariate")
        & results["outcome"].isin(
            [
                "vaccine_refusal_vaccine_rollout_2021",
                "vaccine_intent_vaccine_rollout_2021",
                "health_authority_vaccine_trust_vaccine_rollout_2021",
                "government_control_belief_vaccine_rollout_2021",
            ]
        )
        & results["term"].isin(
            [
                "z_trust_density_composite",
                "z_trust_generalized",
                "z_trust_institutions",
                "z_trust_experts",
                "z_information_integrity_proxy",
            ]
        )
    ].copy()

    lines = [
        "# AetherCore Test 002: Trust Density and COVID Behavioral Resistance",
        "",
        "## Purpose",
        "",
        "This second pass tests whether WVS trust variables predict direct behavioral COVID resistance proxies from the Imperial College London / YouGov COVID-19 Behaviour Tracker.",
        "",
        "This is still an observational, small-N cross-country screen. It is designed to generate stronger hypotheses, not final proof.",
        "",
        "## Data",
        "",
        f"- Behavioral source: `{REPO_URL}`",
        f"- Countries in YouGov behavioral aggregate: {merged['country_slug'].notna().sum()}",
        f"- Countries after merge with WVS/OWID controls: {len(merged)}",
        "",
        "## Behavioral Variables",
        "",
        "- `vaccine_refusal`: disagreement with vaccine-intent items. This is the best anti-vax proxy in this pass.",
        "- `vaccine_intent`: agreement with vaccine-intent items.",
        "- `mask_refusal_outside`: reporting rarely or never wearing a mask outside the home.",
        "- `mask_compliance_outside`: frequency-scaled mask wearing outside the home.",
        "- `health_authority_vaccine_trust`: belief that government health authorities will provide an effective vaccine.",
        "- `government_control_belief`: agreement that COVID-19 is being exploited by government to control people.",
        "",
        "## Phase Windows",
        "",
        "- `acute_2020`: survey responses through 2020-12-31.",
        "- `vaccine_rollout_2021`: responses from 2021-01-01 through 2021-12-31.",
        "- `early_recovery_2022`: responses after 2022-01-01.",
        "",
        "## Compact-Control Trust Coefficients",
        "",
    ]
    if trust_rows.empty:
        lines.append("No behavioral models could be estimated.")
    else:
        lines.append("| Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |")
        lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
        for _, row in trust_rows.sort_values(["outcome", "model", "term"]).iterrows():
            lines.append(
                f"| {row['outcome']} | {row['model']} | {row['term']} | "
                f"{row['coef']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | "
                f"{row['p_value']:.3f} ({p_label(row['p_value'])}) | {int(row['n'])} | {row['adj_r2']:.3f} |"
            )

    lines.extend(["", "## Exploratory Bivariate Vaccine and Conspiracy Screens", ""])
    if bivar_rows.empty:
        lines.append("No vaccine/conspiracy bivariate models could be estimated.")
    else:
        lines.append("These models use only 9 countries after WVS/YouGov overlap, so they are hypothesis-generating only.")
        lines.append("")
        lines.append("| Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |")
        lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
        for _, row in bivar_rows.sort_values(["outcome", "model", "term"]).iterrows():
            lines.append(
                f"| {row['outcome']} | {row['model']} | {row['term']} | "
                f"{row['coef']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | "
                f"{row['p_value']:.3f} ({p_label(row['p_value'])}) | {int(row['n'])} | {row['adj_r2']:.3f} |"
            )

    lines.extend(
        [
            "",
            "## Interpretation Rules",
            "",
            "A useful signal is directional consistency across related outcomes, not a declaration of proof. For example, trust should predict lower vaccine refusal and higher vaccine intent, or lower government-control belief and higher confidence in health authorities.",
            "",
            "The claim is weakened when coefficients are directionally inconsistent, insignificant across related outcomes, or only appear in bivariate models and disappear under compact controls.",
            "",
            "## Limitations",
            "",
            "- The YouGov country sample is much smaller than OWID's country coverage.",
            "- Country overlap with WVS reduces the usable model sample further.",
            "- Compact controls are used to avoid extreme overfitting; full-control models are not appropriate at this sample size.",
            "- Mask refusal and vaccine refusal are behavioral/attitudinal proxies, not identity labels.",
            "- Survey timing varies by country and question availability.",
        ]
    )
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    behavior, phase_long = aggregate_country_behavior()

    base_path = DATA_PROCESSED / "aethercore_test001_merged.csv"
    if not base_path.exists():
        raise SystemExit("Run scripts/run_analysis.py first to create the WVS/OWID merged dataset.")
    base = pd.read_csv(base_path)
    merged = base.merge(behavior, on="iso_code", how="inner")

    z_cols = [
        "trust_density_composite",
        "trust_generalized",
        "trust_institutions",
        "trust_experts",
        "information_integrity_proxy",
        "log_gdp_per_capita",
        "human_development_index",
        "median_age",
    ]
    merged = standardize(merged, z_cols)
    merged.to_csv(DATA_PROCESSED / "aethercore_test002_behavioral_merged.csv", index=False)

    results = run_behavior_models(merged)
    results.to_csv(OUTPUTS / "test002_behavioral_regression_results.csv", index=False)
    make_behavior_figures(merged, results)
    write_report(merged, results)

    summary = {
        "behavior_countries": int(len(behavior)),
        "merged_countries": int(len(merged)),
        "phase_rows": int(len(phase_long)),
        "models_estimated": int(results[["outcome", "model"]].drop_duplicates().shape[0]) if not results.empty else 0,
    }
    (OUTPUTS / "test002_behavior_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Report: {REPORT / 'aethercore_test_002_behavioral_resistance.md'}")


if __name__ == "__main__":
    main()
