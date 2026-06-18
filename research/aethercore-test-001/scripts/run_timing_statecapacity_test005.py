"""AetherCore Test 005: WVS Timing and State-Capacity Controls."""

from __future__ import annotations

import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import statsmodels.formula.api as smf


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT = SCRIPT_DIR.parents[0]
DATA_RAW = PROJECT / "data_raw"
DATA_PROCESSED = PROJECT / "data_processed"
OUTPUTS = PROJECT / "outputs"
REPORT = PROJECT / "report"

sys.path.insert(0, str(SCRIPT_DIR))
from run_analysis import find_wvs_file, read_wvs  # noqa: E402

WGI_URL = "https://databank.worldbank.org/data/download/WGI_CSV.zip"
WGI_MAP = {
    "GOV_WGI_GE.EST": "wgi_government_effectiveness_2019",
    "GOV_WGI_RL.EST": "wgi_rule_of_law_2019",
    "GOV_WGI_CC.EST": "wgi_control_corruption_2019",
    "GOV_WGI_VA.EST": "wgi_voice_accountability_2019",
}


def standardize(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        if col in out:
            sd = out[col].std(skipna=True)
            if pd.notna(sd) and sd > 0:
                out[f"z_{col}"] = (out[col] - out[col].mean(skipna=True)) / sd
    return out


def parse_wvs_timing() -> pd.DataFrame:
    path = find_wvs_file()
    if path is None:
        raise SystemExit("WVS Wave 7 file not found.")
    wvs = read_wvs(path)
    iso_col = "B_COUNTRY_ALPHA" if "B_COUNTRY_ALPHA" in wvs.columns else "COUNTRY_ALPHA"
    work = pd.DataFrame({"iso_code": wvs[iso_col].astype(str).str.upper().str.strip()})
    for col in ["A_YEAR", "FW_START", "FW_END", "J_INTDATE"]:
        if col in wvs.columns:
            work[col] = wvs[col]
    work["A_YEAR_num"] = pd.to_numeric(work.get("A_YEAR"), errors="coerce")
    for col in ["FW_START", "FW_END", "J_INTDATE"]:
        if col in work:
            work[f"{col}_dt"] = pd.to_datetime(work[col], errors="coerce", dayfirst=True)

    agg = work.groupby("iso_code", as_index=False).agg(
        wvs_year_median=("A_YEAR_num", "median"),
        wvs_year_min=("A_YEAR_num", "min"),
        wvs_year_max=("A_YEAR_num", "max"),
        fw_start_min=("FW_START_dt", "min") if "FW_START_dt" in work else ("A_YEAR_num", "min"),
        fw_end_max=("FW_END_dt", "max") if "FW_END_dt" in work else ("A_YEAR_num", "max"),
    )
    agg["wvs_timing_group"] = np.where(agg["wvs_year_max"].le(2019), "pre_covid", "pandemic_overlap")
    agg["wvs_post2019"] = (agg["wvs_timing_group"] == "pandemic_overlap").astype(int)
    agg.to_csv(DATA_PROCESSED / "wvs_fieldwork_timing_country.csv", index=False)
    return agg


def download_wgi() -> pd.DataFrame:
    dest = DATA_RAW / "WGI_CSV.zip"
    if not dest.exists() or dest.stat().st_size < 1000:
        r = requests.get(WGI_URL, timeout=180)
        r.raise_for_status()
        dest.write_bytes(r.content)
    with zipfile.ZipFile(dest) as zf:
        raw = pd.read_csv(zf.open("WGICSV.csv"))
    year_col = "2019" if "2019" in raw.columns else "2019 [YR2019]"
    code_col = "Indicator Code" if "Indicator Code" in raw.columns else "Series Code"
    keep = raw[raw[code_col].isin(WGI_MAP.keys())][["Country Code", code_col, year_col]].copy()
    keep[year_col] = pd.to_numeric(keep[year_col], errors="coerce")
    wide = keep.pivot_table(index="Country Code", columns=code_col, values=year_col, aggfunc="first").reset_index()
    wide = wide.rename(columns={"Country Code": "iso_code", **WGI_MAP})
    wide["state_capacity_index_2019"] = wide[list(WGI_MAP.values())].mean(axis=1)
    wide.to_csv(DATA_PROCESSED / "wgi_state_capacity_2019.csv", index=False)
    return wide


def add_continent() -> pd.DataFrame:
    raw = pd.read_csv(DATA_RAW / "owid-covid-data.csv", usecols=["iso_code", "continent"])
    raw = raw[raw["iso_code"].astype(str).str.len().eq(3)]
    cont = raw.dropna().drop_duplicates("iso_code")
    return cont


def run_model(df: pd.DataFrame, outcome: str, predictors: list[str], model: str) -> list[dict]:
    data_predictors = sorted(set(part.strip() for predictor in predictors for part in predictor.split(":")))
    cols = [outcome] + data_predictors
    if any(col not in df.columns for col in cols):
        return []
    data = df[cols + ["iso_code", "location"]].dropna()
    if len(data) < len(predictors) + 10:
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
    timing = parse_wvs_timing()
    wgi = download_wgi()
    cont = add_continent()
    base = pd.read_csv(DATA_PROCESSED / "aethercore_test003_trust_taxonomy_merged.csv")
    df = base.merge(timing, on="iso_code", how="left").merge(wgi, on="iso_code", how="left").merge(cont, on="iso_code", how="left")
    df = pd.get_dummies(df, columns=["continent"], prefix="continent", dummy_na=False)
    df.columns = [str(c).replace(" ", "_").replace("-", "_") for c in df.columns]
    cont_terms = [c for c in df.columns if c.startswith("continent_")][:-1]
    df = standardize(
        df,
        [
            "state_capacity_index_2019",
            "wgi_government_effectiveness_2019",
            "wgi_rule_of_law_2019",
            "wgi_control_corruption_2019",
            "wgi_voice_accountability_2019",
            "centralized_institutional_trust",
            "centralization_gap",
        ],
    )
    df.to_csv(DATA_PROCESSED / "aethercore_test005_timing_statecapacity_merged.csv", index=False)

    controls = [
        "z_log_gdp_per_capita",
        "z_human_development_index",
        "z_median_age",
        "z_log_population_density",
        "z_healthcare_capacity",
        "z_stringency_index",
    ]
    state = ["z_state_capacity_index_2019"]
    outcomes = ["deaths_per_million", "acute_deaths_per_million", "recovery_deaths_per_million", "excess_mortality", "vaccination_rate", "non_vaccinated_share"]
    specs = {
        "central_plus_state_capacity": controls + state + ["z_centralized_institutional_trust"],
        "gap_plus_state_capacity": controls + state + ["z_centralization_gap"],
        "central_gap_state_capacity": controls + state + ["z_centralized_institutional_trust", "z_centralization_gap"],
        "gap_x_wvs_timing": controls + ["z_centralization_gap", "wvs_post2019", "z_centralization_gap:wvs_post2019"],
        "central_x_wvs_timing": controls + ["z_centralized_institutional_trust", "wvs_post2019", "z_centralized_institutional_trust:wvs_post2019"],
    }
    if len(cont_terms) >= 2:
        specs["gap_plus_region"] = controls + cont_terms + ["z_centralization_gap"]
        specs["central_plus_region"] = controls + cont_terms + ["z_centralized_institutional_trust"]

    rows = []
    for outcome in outcomes:
        for name, predictors in specs.items():
            rows.extend(run_model(df, outcome, predictors, name))
    results = pd.DataFrame(rows)
    results.to_csv(OUTPUTS / "test005_timing_statecapacity_results.csv", index=False)

    report = REPORT / "aethercore_test_005_timing_statecapacity.md"
    focus_terms = [
        "z_centralized_institutional_trust",
        "z_centralization_gap",
        "z_state_capacity_index_2019",
        "z_centralization_gap:wvs_post2019",
        "z_centralized_institutional_trust:wvs_post2019",
    ]
    focus = results[results["term"].isin(focus_terms)].copy()
    timing_counts = timing["wvs_timing_group"].value_counts(dropna=False)
    timing_lines = ["| Timing group | Countries |", "|---|---:|"]
    for key, value in timing_counts.items():
        timing_lines.append(f"| {key} | {int(value)} |")
    lines = [
        "# AetherCore Test 005: WVS Timing and State-Capacity Controls",
        "",
        "## Purpose",
        "",
        "This pass tests whether the trust-taxonomy results survive pre-pandemic state-capacity controls and whether WVS fieldwork timing changes the signal.",
        "",
        "State capacity uses 2019 Worldwide Governance Indicators from the World Bank WGI bulk CSV.",
        "",
        "## Fieldwork Timing Counts",
        "",
        *timing_lines,
        "",
        "## Main Coefficients",
        "",
        "| Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for _, row in focus.sort_values(["outcome", "model", "term"]).iterrows():
        lines.append(
            f"| {row['outcome']} | {row['model']} | {row['term']} | {row['coef']:.3f} | "
            f"[{row['ci_low']:.3f}, {row['ci_high']:.3f}] | {row['p_value']:.3f} | {int(row['n'])} | {row['adj_r2']:.3f} |"
        )
    lines.extend(["", "## Interpretation", "", "If central trust and centralization gap remain meaningful after WGI controls, the result is less likely to be only state capacity. If timing interactions are large, WVS timing may be contaminating predictor direction."])
    report.write_text("\n".join(lines), encoding="utf-8")

    summary = {"rows": int(len(df)), "result_rows": int(len(results)), "wgi_rows": int(len(wgi))}
    (OUTPUTS / "test005_timing_statecapacity_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
