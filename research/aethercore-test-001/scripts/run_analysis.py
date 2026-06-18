"""AetherCore Test 001: Trust Density and COVID Shock Recovery.

This script builds a country-level dataset from World Values Survey Wave 7
and Our World in Data COVID data, then tests whether trust variables improve
prediction of COVID shock response after conventional controls.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import re
import textwrap
import zipfile
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

try:
    import pyreadstat
except ImportError:  # pragma: no cover
    pyreadstat = None


PROJECT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT / "data_raw"
DATA_PROCESSED = PROJECT / "data_processed"
OUTPUTS = PROJECT / "outputs"
FIGURES = PROJECT / "figures"
REPORT = PROJECT / "report"

OWID_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
OWID_GITHUB_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
WVS_DOC_URL = "https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp"
WVS_OSF_URL = "https://osf.io/36dgb/download"

MISSING_CODES = {-5, -4, -3, -2, -1, 999, 9999}


def ensure_dirs() -> None:
    for directory in [DATA_RAW, DATA_PROCESSED, OUTPUTS, FIGURES, REPORT]:
        directory.mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path, timeout: int = 180) -> bool:
    if dest.exists() and dest.stat().st_size > 1000:
        return True
    try:
        with requests.get(url, stream=True, timeout=timeout) as response:
            response.raise_for_status()
            with dest.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)
        return dest.exists() and dest.stat().st_size > 1000
    except Exception as exc:
        print(f"Download failed for {url}: {exc}")
        return False


def try_download_wvs() -> Path | None:
    """Best-effort WVS discovery.

    WVS commonly requires a browser license/registration step. If the public
    documentation page exposes direct data links, this function downloads one.
    Otherwise the script proceeds with a manual-placement instruction.
    """
    local = find_wvs_file()
    if local is not None:
        return local

    osf_dest = DATA_RAW / "WVS_Cross-National_Wave_7_csv_v6_0.csv"
    if download_file(WVS_OSF_URL, osf_dest, timeout=300):
        return osf_dest

    try:
        html = requests.get(WVS_DOC_URL, timeout=30).text
    except Exception:
        return None

    hrefs = sorted(set(re.findall(r'href=["\']([^"\']+)["\']', html, flags=re.I)))
    candidates = []
    for href in hrefs:
        lower = href.lower()
        if "wv7" in lower or "wave_7" in lower or "wave7" in lower:
            if any(ext in lower for ext in [".zip", ".csv", ".sav", ".dta", ".xlsx"]):
                candidates.append(href)

    for href in candidates:
        url = href
        if href.startswith("/"):
            url = "https://www.worldvaluessurvey.org" + href
        elif not href.startswith("http"):
            url = "https://www.worldvaluessurvey.org/" + href
        dest = DATA_RAW / Path(url.split("?")[0]).name
        if download_file(url, dest, timeout=180):
            return dest
    return None


def find_wvs_file() -> Path | None:
    patterns = [
        "*WVS*7*.zip",
        "*Wave*7*.zip",
        "*WVS*7*.csv",
        "*Wave*7*.csv",
        "*WVS*7*.dta",
        "*Wave*7*.dta",
        "*WVS*7*.sav",
        "*Wave*7*.sav",
        "*WVS*7*.xlsx",
        "*Wave*7*.xlsx",
        "*.sav",
        "*.dta",
    ]
    for pattern in patterns:
        matches = sorted(DATA_RAW.glob(pattern))
        if matches:
            return matches[0]
    return None


def extract_from_zip(path: Path) -> Path:
    with zipfile.ZipFile(path) as zf:
        members = [
            m for m in zf.namelist()
            if m.lower().endswith((".csv", ".dta", ".sav", ".xlsx", ".xls"))
            and "__macosx" not in m.lower()
        ]
        if not members:
            raise FileNotFoundError(f"No readable data file found inside {path.name}")
        preferred = sorted(
            members,
            key=lambda m: (
                0 if "csv" in m.lower() else 1,
                0 if ("wave" in m.lower() or "wvs" in m.lower()) else 1,
                len(m),
            ),
        )[0]
        out = DATA_RAW / Path(preferred).name
        if not out.exists():
            out.write_bytes(zf.read(preferred))
        return out


def read_wvs(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".zip":
        path = extract_from_zip(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        for enc in ["utf-8-sig", "utf-8", "latin1"]:
            try:
                return pd.read_csv(path, low_memory=False, encoding=enc)
            except UnicodeDecodeError:
                continue
        return pd.read_csv(path, low_memory=False)
    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    if suffix == ".dta":
        if pyreadstat is not None:
            df, _ = pyreadstat.read_dta(path)
            return df
        return pd.read_stata(path)
    if suffix == ".sav":
        if pyreadstat is None:
            raise ImportError("pyreadstat is required to read SPSS .sav WVS files.")
        df, _ = pyreadstat.read_sav(path)
        return df
    raise ValueError(f"Unsupported WVS file type: {path}")


def first_present(columns: Iterable[str], candidates: Iterable[str]) -> str | None:
    cols = set(columns)
    for candidate in candidates:
        if candidate in cols:
            return candidate
    lower_map = {str(c).lower(): c for c in columns}
    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]
    return None


def numeric_clean(series: pd.Series) -> pd.Series:
    out = pd.to_numeric(series, errors="coerce")
    return out.mask(out.isin(MISSING_CODES))


def recode_binary_trust(series: pd.Series) -> pd.Series:
    values = numeric_clean(series)
    return np.where(values.eq(1), 1.0, np.where(values.eq(2), 0.0, np.nan))


def recode_confidence(series: pd.Series) -> pd.Series:
    values = numeric_clean(series)
    # WVS confidence items are usually 1=A great deal, 4=None at all.
    return np.where(values.between(1, 4), (4.0 - values) / 3.0, np.nan)


def build_wvs_country_trust(wvs: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    iso_col = first_present(
        wvs.columns,
        [
            "B_COUNTRY_ALPHA",
            "COUNTRY_ALPHA",
            "ISO3",
            "iso3",
            "country_alpha",
            "S003B",
        ],
    )
    country_col = first_present(
        wvs.columns,
        ["B_COUNTRY", "COUNTRY", "country", "Country", "S003", "S003A"],
    )
    if iso_col is None:
        raise ValueError(
            "Could not find an ISO3 country column in the WVS file. "
            "Expected one of B_COUNTRY_ALPHA, COUNTRY_ALPHA, ISO3, or S003B."
        )

    gen_col = first_present(wvs.columns, ["Q57", "A165"])
    if gen_col is None:
        raise ValueError("Could not find generalized trust variable Q57/A165 in WVS.")

    institution_candidates = [
        "Q69",  # police
        "Q70",  # courts
        "Q71",  # government
        "Q73",  # parliament
        "Q74",  # civil service
        "Q76",  # elections
    ]
    institution_cols = [c for c in institution_candidates if c in set(wvs.columns)]

    expert_candidates = [
        "Q75",  # universities in WVS Wave 7; expert-adjacent proxy
        "Q158",
        "Q159",
    ]
    expert_cols = [c for c in expert_candidates if c in set(wvs.columns)]

    info_candidates = ["Q66", "Q67"]  # press and television confidence, exploratory proxy
    info_cols = [c for c in info_candidates if c in set(wvs.columns)]

    work = pd.DataFrame()
    work["iso_code"] = wvs[iso_col].astype(str).str.upper().str.strip()
    work["location_wvs"] = wvs[country_col].astype(str) if country_col else np.nan
    work["trust_generalized"] = recode_binary_trust(wvs[gen_col])

    for col in institution_cols:
        work[f"inst_{col}"] = recode_confidence(wvs[col])
    if institution_cols:
        work["trust_institutions"] = work[[f"inst_{c}" for c in institution_cols]].mean(axis=1)
    else:
        work["trust_institutions"] = np.nan

    for col in expert_cols:
        work[f"expert_{col}"] = recode_confidence(wvs[col])
    if expert_cols:
        work["trust_experts"] = work[[f"expert_{c}" for c in expert_cols]].mean(axis=1)
    else:
        work["trust_experts"] = np.nan

    for col in info_cols:
        work[f"info_{col}"] = recode_confidence(wvs[col])
    if info_cols:
        work["information_integrity_proxy"] = work[[f"info_{c}" for c in info_cols]].mean(axis=1)
    else:
        work["information_integrity_proxy"] = np.nan

    agg = (
        work.groupby("iso_code", as_index=False)
        .agg(
            location_wvs=("location_wvs", lambda s: s.dropna().astype(str).mode().iloc[0] if len(s.dropna()) else np.nan),
            trust_generalized=("trust_generalized", "mean"),
            trust_institutions=("trust_institutions", "mean"),
            trust_experts=("trust_experts", "mean"),
            information_integrity_proxy=("information_integrity_proxy", "mean"),
            wvs_n=("trust_generalized", "count"),
        )
    )
    trust_parts = ["trust_generalized", "trust_institutions"]
    if agg["trust_experts"].notna().sum() >= 10:
        trust_parts.append("trust_experts")
    z = agg[trust_parts].apply(lambda s: (s - s.mean()) / s.std(ddof=0), axis=0)
    agg["trust_density_composite"] = z.mean(axis=1)

    audit = {
        "iso_column": iso_col,
        "country_column": country_col,
        "generalized_trust_column": gen_col,
        "institution_columns": institution_cols,
        "expert_columns": expert_cols,
        "information_integrity_proxy_columns": info_cols,
        "trust_composite_parts": trust_parts,
        "notes": [
            "Generalized trust recoded as 1='most people can be trusted', 0='need to be careful'.",
            "Institution/expert/media confidence items recoded from 1..4 to 1.0..0.0 where lower WVS values mean higher confidence.",
            "Q75 is treated as an expert-adjacent universities confidence proxy if present; this is weaker than direct trust in doctors/scientists.",
        ],
    }
    return agg, audit


def latest_nonnull(group: pd.DataFrame, column: str) -> float:
    if column not in group:
        return np.nan
    s = group.sort_values("date")[column].dropna()
    return s.iloc[-1] if len(s) else np.nan


def max_nonnull(group: pd.DataFrame, column: str) -> float:
    if column not in group:
        return np.nan
    return group[column].max(skipna=True)


def build_owid_country_data() -> pd.DataFrame:
    raw_path = DATA_RAW / "owid-covid-data.csv"
    if not download_file(OWID_URL, raw_path) and not download_file(OWID_GITHUB_URL, raw_path):
        raise RuntimeError("Could not download OWID COVID dataset.")
    owid = pd.read_csv(raw_path, low_memory=False, parse_dates=["date"])
    owid = owid[owid["iso_code"].str.len().eq(3) & ~owid["iso_code"].str.startswith("OWID")]
    owid["year"] = owid["date"].dt.year
    pandemic_policy = owid[owid["year"].between(2020, 2021)]
    acute = owid[owid["date"].le(pd.Timestamp("2021-12-31"))]
    recovery = owid[owid["date"].ge(pd.Timestamp("2022-01-01"))]

    rows = []
    for iso, g in owid.groupby("iso_code"):
        p = pandemic_policy[pandemic_policy["iso_code"].eq(iso)]
        a = acute[acute["iso_code"].eq(iso)]
        r = recovery[recovery["iso_code"].eq(iso)]
        deaths_acute = max_nonnull(a, "total_deaths_per_million")
        deaths_final = max_nonnull(g, "total_deaths_per_million")
        vacc_2021 = max_nonnull(a, "people_vaccinated_per_hundred")
        vacc_final = max_nonnull(g, "people_vaccinated_per_hundred")
        rows.append(
            {
                "iso_code": iso,
                "location": latest_nonnull(g, "location"),
                "vaccination_rate": vacc_final,
                "vaccination_rate_2021": vacc_2021,
                "non_vaccinated_share": 100.0 - vacc_final if pd.notna(vacc_final) else np.nan,
                "non_vaccinated_share_2021": 100.0 - vacc_2021 if pd.notna(vacc_2021) else np.nan,
                "fully_vaccinated_rate": max_nonnull(g, "people_fully_vaccinated_per_hundred"),
                "excess_mortality": latest_nonnull(g, "excess_mortality_cumulative_per_million"),
                "deaths_per_million": deaths_final,
                "acute_deaths_per_million": deaths_acute,
                "recovery_deaths_per_million": deaths_final - deaths_acute if pd.notna(deaths_final) and pd.notna(deaths_acute) else np.nan,
                "gdp_per_capita": latest_nonnull(g, "gdp_per_capita"),
                "human_development_index": latest_nonnull(g, "human_development_index"),
                "median_age": latest_nonnull(g, "median_age"),
                "aged_65_older": latest_nonnull(g, "aged_65_older"),
                "population_density": latest_nonnull(g, "population_density"),
                "healthcare_capacity": latest_nonnull(g, "hospital_beds_per_thousand"),
                "stringency_index": p["stringency_index"].mean(skipna=True) if "stringency_index" in p else np.nan,
            }
        )
    out = pd.DataFrame(rows)
    out["log_gdp_per_capita"] = np.log(out["gdp_per_capita"])
    out["log_population_density"] = np.log(out["population_density"])
    return out


def standardize_predictors(df: pd.DataFrame, columns: list[str]) -> tuple[pd.DataFrame, dict]:
    out = df.copy()
    params = {}
    for col in columns:
        if col in out:
            mean = out[col].mean(skipna=True)
            sd = out[col].std(skipna=True)
            if sd and not math.isnan(sd):
                out[f"z_{col}"] = (out[col] - mean) / sd
                params[col] = {"mean": float(mean), "sd": float(sd)}
    return out, params


def run_ols(df: pd.DataFrame, outcome: str, predictors: list[str], model_name: str) -> dict | None:
    data_predictors: list[str] = []
    for predictor in predictors:
        data_predictors.extend(part.strip() for part in predictor.split(":"))
    cols = [outcome] + sorted(set(data_predictors))
    missing = [col for col in cols if col not in df.columns]
    if missing:
        return None
    model_df = df[cols + ["iso_code", "location"]].dropna()
    if len(model_df) < max(18, len(predictors) + 8):
        return None
    formula = f"{outcome} ~ " + " + ".join(predictors)
    fit = smf.ols(formula, data=model_df).fit(cov_type="HC3")
    rows = []
    conf = fit.conf_int()
    for term in fit.params.index:
        rows.append(
            {
                "model": model_name,
                "outcome": outcome,
                "term": term,
                "coef": fit.params[term],
                "std_err_hc3": fit.bse[term],
                "p_value": fit.pvalues[term],
                "ci_low": conf.loc[term, 0],
                "ci_high": conf.loc[term, 1],
                "n": int(fit.nobs),
                "r2": fit.rsquared,
                "adj_r2": fit.rsquared_adj,
                "aic": fit.aic,
                "bic": fit.bic,
            }
        )
    return {"fit": fit, "rows": rows, "n": int(fit.nobs), "formula": formula}


def run_models(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    base_controls = [
        "z_log_gdp_per_capita",
        "z_human_development_index",
        "z_median_age",
        "z_log_population_density",
        "z_healthcare_capacity",
        "z_stringency_index",
    ]
    outcomes = [
        "vaccination_rate",
        "vaccination_rate_2021",
        "non_vaccinated_share",
        "non_vaccinated_share_2021",
        "excess_mortality",
        "deaths_per_million",
        "acute_deaths_per_million",
        "recovery_deaths_per_million",
    ]
    trust_models = {
        "A_controls_only": [],
        "B_generalized_trust": ["z_trust_generalized"],
        "C_institutional_trust": ["z_trust_institutions"],
        "D_trust_density": ["z_trust_density_composite"],
        "E_expert_proxy_trust": ["z_trust_experts"],
        "F_information_proxy_trust": ["z_information_integrity_proxy"],
    }
    interaction_models = {
        "I_trust_x_material_capacity": ["z_trust_density_composite", "z_log_gdp_per_capita", "z_trust_density_composite:z_log_gdp_per_capita"],
        "I_trust_x_policy_stringency": ["z_trust_density_composite", "z_stringency_index", "z_trust_density_composite:z_stringency_index"],
        "I_trust_x_information_integrity": ["z_trust_density_composite", "z_information_integrity_proxy", "z_trust_density_composite:z_information_integrity_proxy"],
    }

    rows = []
    comparisons = []
    fits = {}
    for outcome in outcomes:
        for name, trust_terms in trust_models.items():
            predictors = base_controls + trust_terms
            result = run_ols(df, outcome, predictors, name)
            if result is None:
                continue
            rows.extend(result["rows"])
            fits[(outcome, name)] = result["fit"]
            comparisons.append(
                {
                    "outcome": outcome,
                    "model": name,
                    "n": result["n"],
                    "formula": result["formula"],
                    "adj_r2": result["fit"].rsquared_adj,
                    "aic": result["fit"].aic,
                    "bic": result["fit"].bic,
                }
            )
        for name, terms in interaction_models.items():
            predictors = [c for c in base_controls if c not in terms] + terms
            result = run_ols(df, outcome, predictors, name)
            if result is None:
                continue
            rows.extend(result["rows"])
            fits[(outcome, name)] = result["fit"]
            comparisons.append(
                {
                    "outcome": outcome,
                    "model": name,
                    "n": result["n"],
                    "formula": result["formula"],
                    "adj_r2": result["fit"].rsquared_adj,
                    "aic": result["fit"].aic,
                    "bic": result["fit"].bic,
                }
            )
    return pd.DataFrame(rows), pd.DataFrame(comparisons), fits


def scatter_with_reg(df: pd.DataFrame, x: str, y: str, filename: str, title: str) -> None:
    plot_df = df[[x, y, "location"]].dropna()
    if len(plot_df) < 8:
        return
    plt.figure(figsize=(8, 5.5))
    sns.regplot(data=plot_df, x=x, y=y, scatter_kws={"s": 42, "alpha": 0.75}, line_kws={"color": "#9b1c31"})
    r, p = stats.pearsonr(plot_df[x], plot_df[y])
    plt.title(f"{title}\nr={r:.2f}, p={p:.3f}, n={len(plot_df)}")
    plt.tight_layout()
    plt.savefig(FIGURES / filename, dpi=180)
    plt.close()


def make_figures(df: pd.DataFrame, results: pd.DataFrame) -> None:
    scatter_with_reg(df, "trust_density_composite", "vaccination_rate", "trust_vs_vaccination.png", "Trust Density vs Vaccination Uptake")
    scatter_with_reg(df, "trust_density_composite", "non_vaccinated_share", "trust_vs_non_vaccinated_share.png", "Trust Density vs Non-Vaccinated Share")
    scatter_with_reg(df, "trust_density_composite", "vaccination_rate_2021", "trust_vs_vaccination_2021.png", "Trust Density vs Vaccination Uptake by End of 2021")
    scatter_with_reg(df, "trust_density_composite", "excess_mortality", "trust_vs_excess_mortality.png", "Trust Density vs Excess Mortality")
    scatter_with_reg(df, "trust_density_composite", "deaths_per_million", "trust_vs_deaths.png", "Trust Density vs COVID Deaths per Million")
    scatter_with_reg(df, "trust_density_composite", "acute_deaths_per_million", "trust_vs_acute_deaths.png", "Trust Density vs Acute-Phase Deaths per Million")
    scatter_with_reg(df, "trust_density_composite", "recovery_deaths_per_million", "trust_vs_recovery_deaths.png", "Trust Density vs Recovery-Phase Deaths per Million")

    heat_cols = [
        "trust_generalized",
        "trust_institutions",
        "trust_experts",
        "trust_density_composite",
        "vaccination_rate",
        "vaccination_rate_2021",
        "non_vaccinated_share",
        "non_vaccinated_share_2021",
        "excess_mortality",
        "deaths_per_million",
        "acute_deaths_per_million",
        "recovery_deaths_per_million",
        "gdp_per_capita",
        "human_development_index",
        "median_age",
        "population_density",
        "healthcare_capacity",
        "stringency_index",
    ]
    heat_df = df[[c for c in heat_cols if c in df]].dropna(axis=1, how="all")
    plt.figure(figsize=(11, 8))
    sns.heatmap(heat_df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="vlag", center=0, square=False)
    plt.title("Country-Level Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(FIGURES / "correlation_heatmap.png", dpi=180)
    plt.close()

    coef_terms = [
        "z_trust_generalized",
        "z_trust_institutions",
        "z_trust_density_composite",
        "z_trust_experts",
        "z_information_integrity_proxy",
        "z_trust_density_composite:z_log_gdp_per_capita",
        "z_trust_density_composite:z_stringency_index",
        "z_trust_density_composite:z_information_integrity_proxy",
    ]
    coef_df = results[results["term"].isin(coef_terms)].copy()
    if not coef_df.empty:
        coef_df["label"] = coef_df["outcome"] + " | " + coef_df["model"]
        coef_df = coef_df.sort_values(["term", "outcome", "model"])
        plt.figure(figsize=(11, max(5, 0.34 * len(coef_df))))
        y = np.arange(len(coef_df))
        plt.errorbar(
            coef_df["coef"],
            y,
            xerr=[coef_df["coef"] - coef_df["ci_low"], coef_df["ci_high"] - coef_df["coef"]],
            fmt="o",
            color="#1f4e79",
            ecolor="#8aa9c4",
            capsize=3,
        )
        plt.axvline(0, color="black", linewidth=1)
        plt.yticks(y, coef_df["label"], fontsize=8)
        plt.xlabel("OLS coefficient with HC3 95% CI")
        plt.title("Trust Coefficients Across Models")
        plt.tight_layout()
        plt.savefig(FIGURES / "coefficient_plot.png", dpi=180)
        plt.close()

    # Partial regression: residualize vaccination and trust over controls.
    controls = [
        "z_log_gdp_per_capita",
        "z_human_development_index",
        "z_median_age",
        "z_log_population_density",
        "z_healthcare_capacity",
        "z_stringency_index",
    ]
    part_cols = ["vaccination_rate", "z_trust_density_composite"] + controls
    part = df[part_cols].dropna()
    if len(part) >= len(controls) + 10:
        y_res = sm.OLS(part["vaccination_rate"], sm.add_constant(part[controls])).fit().resid
        x_res = sm.OLS(part["z_trust_density_composite"], sm.add_constant(part[controls])).fit().resid
        plt.figure(figsize=(8, 5.5))
        sns.regplot(x=x_res, y=y_res, scatter_kws={"s": 42, "alpha": 0.75}, line_kws={"color": "#9b1c31"})
        plt.xlabel("Trust density residual after controls")
        plt.ylabel("Vaccination residual after controls")
        plt.title("Partial Association: Trust Density and Vaccination Uptake")
        plt.tight_layout()
        plt.savefig(FIGURES / "partial_trust_vaccination.png", dpi=180)
        plt.close()


def interpret_p(p: float) -> str:
    if pd.isna(p):
        return "not estimable"
    if p < 0.01:
        return "statistically significant at p<0.01"
    if p < 0.05:
        return "statistically significant at p<0.05"
    if p < 0.10:
        return "marginal at p<0.10"
    return "not statistically significant"


def write_report(merged: pd.DataFrame, results: pd.DataFrame, comparisons: pd.DataFrame, audit: dict) -> None:
    report_path = REPORT / "aethercore_test_001_report.md"
    trust_rows = results[results["term"].isin(["z_trust_generalized", "z_trust_institutions", "z_trust_density_composite"])]
    interaction_rows = results[results["term"].str.contains(":", regex=False, na=False)]

    lines = [
        "# AetherCore Test 001: Trust Density and COVID Shock Recovery",
        "",
        "## Executive Summary",
        "",
        "This analysis tests whether country-level trust variables from World Values Survey Wave 7 improve prediction of COVID-19 shock-response outcomes after controlling for conventional country-level factors from Our World in Data.",
        "",
        "This is an observational cross-country analysis. It can identify associations and incremental predictive value, but it cannot prove that trust caused better or worse COVID outcomes.",
        "",
        "## Data Used",
        "",
        f"- World Values Survey countries merged: {merged['trust_density_composite'].notna().sum()}",
        f"- Final merged country rows: {len(merged)}",
        "- OWID COVID source: `https://covid.ourworldindata.org/data/owid-covid-data.csv`",
        "- OWID GitHub fallback: `https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv`",
        "- WVS Wave 7 source page: `https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp`",
        "- WVS Wave 7 OSF mirror used when available: `https://osf.io/36dgb/download`",
        "",
        "## Constructed Variables",
        "",
        "- `trust_generalized`: country mean of generalized interpersonal trust, coded 1 for generalized trust and 0 for caution.",
        "- `trust_institutions`: country mean of available WVS confidence variables for police, courts, government, parliament, civil service, and elections, scaled 0 to 1.",
        "- `trust_experts`: country mean of available expert-adjacent WVS confidence variables. In this run, direct expert trust availability depends on the WVS columns present.",
        "- `trust_density_composite`: average z-score of generalized trust, institutional trust, and expert trust if expert trust is sufficiently available.",
        "- `vaccination_rate`: maximum OWID people vaccinated per hundred.",
        "- `vaccination_rate_2021`: maximum OWID people vaccinated per hundred through 2021-12-31.",
        "- `non_vaccinated_share`: 100 minus final vaccination rate. This is an uptake-gap proxy, not a direct measure of anti-vaccine identity.",
        "- `non_vaccinated_share_2021`: 100 minus vaccination rate through 2021-12-31. This is also an uptake-gap proxy.",
        "- `excess_mortality`: latest OWID cumulative excess mortality per million where available.",
        "- `deaths_per_million`: maximum OWID total COVID deaths per million.",
        "- `acute_deaths_per_million`: maximum OWID total COVID deaths per million through 2021-12-31.",
        "- `recovery_deaths_per_million`: final deaths per million minus acute deaths per million, approximating post-2021 recovery-phase mortality burden.",
        "- Controls: log GDP per capita, HDI, median age, log population density, hospital beds per thousand, and mean 2020-2021 stringency index.",
        "",
        "## WVS Variable Audit",
        "",
        "```json",
        json.dumps(audit, indent=2),
        "```",
        "",
        "## Model Design",
        "",
        "- Model A: outcome ~ controls only",
        "- Model B: outcome ~ controls + generalized trust",
        "- Model C: outcome ~ controls + institutional trust",
        "- Model D: outcome ~ controls + trust density composite",
        "- Interaction models: trust density interacted with material capacity, policy stringency, and an exploratory information-integrity proxy when available.",
        "- OLS estimates use HC3 robust standard errors. Predictors are standardized; outcomes remain in original units.",
        "",
        "## Main Trust Coefficients",
        "",
    ]

    if trust_rows.empty:
        lines.append("No trust models could be estimated with the available complete cases.")
    else:
        lines.append("| Outcome | Model | Term | Coef | 95% CI | p | Interpretation |")
        lines.append("|---|---|---:|---:|---:|---:|---|")
        for _, row in trust_rows.sort_values(["outcome", "model", "term"]).iterrows():
            lines.append(
                f"| {row['outcome']} | {row['model']} | {row['term']} | "
                f"{row['coef']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | "
                f"{row['p_value']:.3f} | {interpret_p(row['p_value'])} |"
            )

    lines.extend(["", "## Model Comparison", ""])
    if comparisons.empty:
        lines.append("No models could be estimated.")
    else:
        lines.append("| Outcome | Model | n | Adj. R² | AIC | BIC |")
        lines.append("|---|---|---:|---:|---:|---:|")
        for _, row in comparisons.sort_values(["outcome", "model"]).iterrows():
            lines.append(
                f"| {row['outcome']} | {row['model']} | {int(row['n'])} | "
                f"{row['adj_r2']:.3f} | {row['aic']:.1f} | {row['bic']:.1f} |"
            )

    lines.extend(["", "## Interaction Tests", ""])
    if interaction_rows.empty:
        lines.append("No interaction models could be estimated with the available complete cases.")
    else:
        lines.append("| Outcome | Model | Interaction | Coef | 95% CI | p | Interpretation |")
        lines.append("|---|---|---:|---:|---:|---:|---|")
        for _, row in interaction_rows.sort_values(["outcome", "model", "term"]).iterrows():
            lines.append(
                f"| {row['outcome']} | {row['model']} | {row['term']} | "
                f"{row['coef']:.3f} | [{row['ci_low']:.3f}, {row['ci_high']:.3f}] | "
                f"{row['p_value']:.3f} | {interpret_p(row['p_value'])} |"
            )

    lines.extend(
        [
            "",
            "## Intellectual Honesty and Falsification Criteria",
            "",
            "The AetherCore Trust Density claim is weakened if trust coefficients are small, directionally inconsistent, statistically insignificant after controls, or fail to improve adjusted R²/AIC/BIC across outcomes. It is also weakened if effects disappear when alternative outcomes or control sets are used.",
            "",
            "The claim receives tentative support only where trust variables add incremental predictive value after controls, show directionally coherent effects across outcomes, and where interaction terms suggest that trust strengthens the performance of material capacity, policy response, or information integrity. Even then, these results remain correlational.",
            "",
            "## Data Quality Limitations",
            "",
            "- Cross-country sample size is limited by WVS Wave 7 country coverage and missing COVID excess-mortality data.",
            "- WVS confidence-in-experts measures are not guaranteed to include direct trust in scientists or doctors; the script uses available expert-adjacent variables and reports the exact columns.",
            "- COVID outcomes were shaped by reporting practices, pandemic timing, variants, policy regimes, geography, and measurement quality.",
            "- Anti-vaxxer and no-masker behavior are not directly measured in this pass. `non_vaccinated_share` is an uptake-gap proxy only; no masking refusal variable is present in WVS/OWID.",
            "- Some controls are highly collinear, especially GDP per capita, HDI, and healthcare capacity.",
            "- Results should be treated as a first-pass empirical screen, not as proof of the theory.",
            "",
            "## Generated Artifacts",
            "",
            "- Clean merged dataset: `data_processed/aethercore_test001_merged.csv`",
            "- Country-level WVS trust dataset: `data_processed/wvs_wave7_country_trust.csv`",
            "- Country-level OWID dataset: `data_processed/owid_covid_country.csv`",
            "- Regression table: `outputs/regression_results.csv`",
            "- Model comparison table: `outputs/model_comparison.csv`",
            "- Figures: `figures/`",
            "",
            "## Future Tests Needed",
            "",
            "- Replicate with alternative trust datasets and survey waves.",
            "- Add independent information-integrity proxies such as press freedom, misinformation exposure, or institutional transparency indices.",
            "- Use panel or longitudinal designs where possible.",
            "- Test pre-registered model specifications and alternative outcome windows.",
            "- Compare COVID with other shocks such as natural disasters, financial crises, and public-health campaigns.",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wvs-path", type=Path, default=None, help="Optional path to WVS Wave 7 file.")
    args = parser.parse_args()

    ensure_dirs()
    wvs_path = args.wvs_path or try_download_wvs()
    if wvs_path is None:
        note = REPORT / "manual_wvs_required.md"
        note.write_text(
            textwrap.dedent(
                f"""\
                # Manual WVS Wave 7 File Required

                The OWID COVID dataset can be downloaded automatically, but World Values Survey Wave 7
                was not available through a direct public file link during this run. This commonly happens
                because WVS requires free registration and license acceptance before dataset download.

                Download the Wave 7 country-pooled dataset from:

                {WVS_DOC_URL}

                Place the downloaded `.csv`, `.dta`, `.sav`, `.xlsx`, or `.zip` file in:

                {DATA_RAW}

                Then rerun:

                python scripts\\run_analysis.py
                """
            ),
            encoding="utf-8",
        )
        raise SystemExit(f"WVS Wave 7 file not found. See {note}")

    print(f"Using WVS file: {wvs_path}")
    wvs = read_wvs(wvs_path)
    trust, audit = build_wvs_country_trust(wvs)
    trust.to_csv(DATA_PROCESSED / "wvs_wave7_country_trust.csv", index=False)
    (OUTPUTS / "wvs_variable_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

    owid = build_owid_country_data()
    owid.to_csv(DATA_PROCESSED / "owid_covid_country.csv", index=False)

    merged = owid.merge(trust, on="iso_code", how="inner")
    predictor_cols = [
        "log_gdp_per_capita",
        "human_development_index",
        "median_age",
        "log_population_density",
        "healthcare_capacity",
        "stringency_index",
        "trust_generalized",
        "trust_institutions",
        "trust_experts",
        "trust_density_composite",
        "information_integrity_proxy",
    ]
    merged, z_params = standardize_predictors(merged, predictor_cols)
    merged.to_csv(DATA_PROCESSED / "aethercore_test001_merged.csv", index=False)
    (OUTPUTS / "standardization_params.json").write_text(json.dumps(z_params, indent=2), encoding="utf-8")

    results, comparisons, _ = run_models(merged)
    results.to_csv(OUTPUTS / "regression_results.csv", index=False)
    comparisons.to_csv(OUTPUTS / "model_comparison.csv", index=False)
    make_figures(merged, results)
    write_report(merged, results, comparisons, audit)
    print(f"Analysis complete. Report: {REPORT / 'aethercore_test_001_report.md'}")


if __name__ == "__main__":
    main()
