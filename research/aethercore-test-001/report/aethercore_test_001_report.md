# AetherCore Test 001: Trust Density and COVID Shock Recovery

## Executive Summary

This analysis tests whether country-level trust variables from World Values Survey Wave 7 improve prediction of COVID-19 shock-response outcomes after controlling for conventional country-level factors from Our World in Data.

This is an observational cross-country analysis. It can identify associations and incremental predictive value, but it cannot prove that trust caused better or worse COVID outcomes.

## Data Used

- World Values Survey countries merged: 65
- Final merged country rows: 65
- OWID COVID source: `https://covid.ourworldindata.org/data/owid-covid-data.csv`
- OWID GitHub fallback: `https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv`
- WVS Wave 7 source page: `https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp`
- WVS Wave 7 OSF mirror used when available: `https://osf.io/36dgb/download`

## Constructed Variables

- `trust_generalized`: country mean of generalized interpersonal trust, coded 1 for generalized trust and 0 for caution.
- `trust_institutions`: country mean of available WVS confidence variables for police, courts, government, parliament, civil service, and elections, scaled 0 to 1.
- `trust_experts`: country mean of available expert-adjacent WVS confidence variables. In this run, direct expert trust availability depends on the WVS columns present.
- `trust_density_composite`: average z-score of generalized trust, institutional trust, and expert trust if expert trust is sufficiently available.
- `vaccination_rate`: maximum OWID people vaccinated per hundred.
- `vaccination_rate_2021`: maximum OWID people vaccinated per hundred through 2021-12-31.
- `non_vaccinated_share`: 100 minus final vaccination rate. This is an uptake-gap proxy, not a direct measure of anti-vaccine identity.
- `non_vaccinated_share_2021`: 100 minus vaccination rate through 2021-12-31. This is also an uptake-gap proxy.
- `excess_mortality`: latest OWID cumulative excess mortality per million where available.
- `deaths_per_million`: maximum OWID total COVID deaths per million.
- `acute_deaths_per_million`: maximum OWID total COVID deaths per million through 2021-12-31.
- `recovery_deaths_per_million`: final deaths per million minus acute deaths per million, approximating post-2021 recovery-phase mortality burden.
- Controls: log GDP per capita, HDI, median age, log population density, hospital beds per thousand, and mean 2020-2021 stringency index.

## WVS Variable Audit

```json
{
  "iso_column": "B_COUNTRY_ALPHA",
  "country_column": "B_COUNTRY",
  "generalized_trust_column": "Q57",
  "institution_columns": [
    "Q69",
    "Q70",
    "Q71",
    "Q73",
    "Q74",
    "Q76"
  ],
  "expert_columns": [
    "Q75",
    "Q158",
    "Q159"
  ],
  "information_integrity_proxy_columns": [
    "Q66",
    "Q67"
  ],
  "trust_composite_parts": [
    "trust_generalized",
    "trust_institutions",
    "trust_experts"
  ],
  "notes": [
    "Generalized trust recoded as 1='most people can be trusted', 0='need to be careful'.",
    "Institution/expert/media confidence items recoded from 1..4 to 1.0..0.0 where lower WVS values mean higher confidence.",
    "Q75 is treated as an expert-adjacent universities confidence proxy if present; this is weaker than direct trust in doctors/scientists."
  ]
}
```

## Model Design

- Model A: outcome ~ controls only
- Model B: outcome ~ controls + generalized trust
- Model C: outcome ~ controls + institutional trust
- Model D: outcome ~ controls + trust density composite
- Interaction models: trust density interacted with material capacity, policy stringency, and an exploratory information-integrity proxy when available.
- OLS estimates use HC3 robust standard errors. Predictors are standardized; outcomes remain in original units.

## Main Trust Coefficients

| Outcome | Model | Term | Coef | 95% CI | p | Interpretation |
|---|---|---:|---:|---:|---:|---|
| acute_deaths_per_million | B_generalized_trust | z_trust_generalized | -611.864 | [-983.128, -240.600] | 0.001 | statistically significant at p<0.01 |
| acute_deaths_per_million | C_institutional_trust | z_trust_institutions | -609.008 | [-949.606, -268.409] | 0.000 | statistically significant at p<0.01 |
| acute_deaths_per_million | D_trust_density | z_trust_density_composite | -584.967 | [-915.667, -254.268] | 0.001 | statistically significant at p<0.01 |
| acute_deaths_per_million | I_trust_x_information_integrity | z_trust_density_composite | -528.984 | [-985.679, -72.290] | 0.023 | statistically significant at p<0.05 |
| acute_deaths_per_million | I_trust_x_material_capacity | z_trust_density_composite | -647.636 | [-982.142, -313.130] | 0.000 | statistically significant at p<0.01 |
| acute_deaths_per_million | I_trust_x_policy_stringency | z_trust_density_composite | -566.094 | [-889.442, -242.746] | 0.001 | statistically significant at p<0.01 |
| deaths_per_million | B_generalized_trust | z_trust_generalized | -708.589 | [-1057.585, -359.594] | 0.000 | statistically significant at p<0.01 |
| deaths_per_million | C_institutional_trust | z_trust_institutions | -671.730 | [-1023.640, -319.820] | 0.000 | statistically significant at p<0.01 |
| deaths_per_million | D_trust_density | z_trust_density_composite | -662.551 | [-1005.377, -319.726] | 0.000 | statistically significant at p<0.01 |
| deaths_per_million | I_trust_x_information_integrity | z_trust_density_composite | -573.722 | [-1056.357, -91.087] | 0.020 | statistically significant at p<0.05 |
| deaths_per_million | I_trust_x_material_capacity | z_trust_density_composite | -744.199 | [-1079.151, -409.247] | 0.000 | statistically significant at p<0.01 |
| deaths_per_million | I_trust_x_policy_stringency | z_trust_density_composite | -637.939 | [-966.998, -308.880] | 0.000 | statistically significant at p<0.01 |
| excess_mortality | B_generalized_trust | z_trust_generalized | -806.778 | [-1685.179, 71.624] | 0.072 | marginal at p<0.10 |
| excess_mortality | C_institutional_trust | z_trust_institutions | -669.080 | [-1181.894, -156.267] | 0.011 | statistically significant at p<0.05 |
| excess_mortality | D_trust_density | z_trust_density_composite | -740.772 | [-1345.835, -135.709] | 0.016 | statistically significant at p<0.05 |
| excess_mortality | I_trust_x_information_integrity | z_trust_density_composite | -574.751 | [-1410.246, 260.744] | 0.178 | not statistically significant |
| excess_mortality | I_trust_x_material_capacity | z_trust_density_composite | -846.984 | [-1491.909, -202.058] | 0.010 | statistically significant at p<0.05 |
| excess_mortality | I_trust_x_policy_stringency | z_trust_density_composite | -754.491 | [-1379.935, -129.047] | 0.018 | statistically significant at p<0.05 |
| non_vaccinated_share | B_generalized_trust | z_trust_generalized | -1.788 | [-7.433, 3.856] | 0.535 | not statistically significant |
| non_vaccinated_share | C_institutional_trust | z_trust_institutions | -4.098 | [-8.521, 0.326] | 0.069 | marginal at p<0.10 |
| non_vaccinated_share | D_trust_density | z_trust_density_composite | -5.921 | [-10.146, -1.696] | 0.006 | statistically significant at p<0.01 |
| non_vaccinated_share | I_trust_x_information_integrity | z_trust_density_composite | -4.063 | [-11.043, 2.916] | 0.254 | not statistically significant |
| non_vaccinated_share | I_trust_x_material_capacity | z_trust_density_composite | -5.229 | [-9.832, -0.626] | 0.026 | statistically significant at p<0.05 |
| non_vaccinated_share | I_trust_x_policy_stringency | z_trust_density_composite | -5.228 | [-10.275, -0.181] | 0.042 | statistically significant at p<0.05 |
| non_vaccinated_share_2021 | B_generalized_trust | z_trust_generalized | -1.516 | [-8.332, 5.300] | 0.663 | not statistically significant |
| non_vaccinated_share_2021 | C_institutional_trust | z_trust_institutions | -2.835 | [-7.221, 1.550] | 0.205 | not statistically significant |
| non_vaccinated_share_2021 | D_trust_density | z_trust_density_composite | -4.306 | [-8.871, 0.259] | 0.064 | marginal at p<0.10 |
| non_vaccinated_share_2021 | I_trust_x_information_integrity | z_trust_density_composite | -3.233 | [-10.297, 3.831] | 0.370 | not statistically significant |
| non_vaccinated_share_2021 | I_trust_x_material_capacity | z_trust_density_composite | -3.945 | [-9.029, 1.139] | 0.128 | not statistically significant |
| non_vaccinated_share_2021 | I_trust_x_policy_stringency | z_trust_density_composite | -3.688 | [-8.623, 1.246] | 0.143 | not statistically significant |
| recovery_deaths_per_million | B_generalized_trust | z_trust_generalized | -96.725 | [-217.046, 23.595] | 0.115 | not statistically significant |
| recovery_deaths_per_million | C_institutional_trust | z_trust_institutions | -62.723 | [-117.166, -8.279] | 0.024 | statistically significant at p<0.05 |
| recovery_deaths_per_million | D_trust_density | z_trust_density_composite | -77.584 | [-147.424, -7.744] | 0.029 | statistically significant at p<0.05 |
| recovery_deaths_per_million | I_trust_x_information_integrity | z_trust_density_composite | -44.738 | [-171.881, 82.406] | 0.490 | not statistically significant |
| recovery_deaths_per_million | I_trust_x_material_capacity | z_trust_density_composite | -96.563 | [-173.545, -19.580] | 0.014 | statistically significant at p<0.05 |
| recovery_deaths_per_million | I_trust_x_policy_stringency | z_trust_density_composite | -71.845 | [-137.146, -6.545] | 0.031 | statistically significant at p<0.05 |
| vaccination_rate | B_generalized_trust | z_trust_generalized | 1.788 | [-3.856, 7.433] | 0.535 | not statistically significant |
| vaccination_rate | C_institutional_trust | z_trust_institutions | 4.098 | [-0.326, 8.521] | 0.069 | marginal at p<0.10 |
| vaccination_rate | D_trust_density | z_trust_density_composite | 5.921 | [1.696, 10.146] | 0.006 | statistically significant at p<0.01 |
| vaccination_rate | I_trust_x_information_integrity | z_trust_density_composite | 4.063 | [-2.916, 11.043] | 0.254 | not statistically significant |
| vaccination_rate | I_trust_x_material_capacity | z_trust_density_composite | 5.229 | [0.626, 9.832] | 0.026 | statistically significant at p<0.05 |
| vaccination_rate | I_trust_x_policy_stringency | z_trust_density_composite | 5.228 | [0.181, 10.275] | 0.042 | statistically significant at p<0.05 |
| vaccination_rate_2021 | B_generalized_trust | z_trust_generalized | 1.516 | [-5.300, 8.332] | 0.663 | not statistically significant |
| vaccination_rate_2021 | C_institutional_trust | z_trust_institutions | 2.835 | [-1.550, 7.221] | 0.205 | not statistically significant |
| vaccination_rate_2021 | D_trust_density | z_trust_density_composite | 4.306 | [-0.259, 8.871] | 0.064 | marginal at p<0.10 |
| vaccination_rate_2021 | I_trust_x_information_integrity | z_trust_density_composite | 3.233 | [-3.831, 10.297] | 0.370 | not statistically significant |
| vaccination_rate_2021 | I_trust_x_material_capacity | z_trust_density_composite | 3.945 | [-1.139, 9.029] | 0.128 | not statistically significant |
| vaccination_rate_2021 | I_trust_x_policy_stringency | z_trust_density_composite | 3.688 | [-1.246, 8.623] | 0.143 | not statistically significant |

## Model Comparison

| Outcome | Model | n | Adj. R² | AIC | BIC |
|---|---|---:|---:|---:|---:|
| acute_deaths_per_million | A_controls_only | 57 | 0.088 | 970.1 | 984.4 |
| acute_deaths_per_million | B_generalized_trust | 57 | 0.275 | 957.9 | 974.3 |
| acute_deaths_per_million | C_institutional_trust | 57 | 0.361 | 950.7 | 967.0 |
| acute_deaths_per_million | D_trust_density | 57 | 0.322 | 954.1 | 970.4 |
| acute_deaths_per_million | E_expert_proxy_trust | 57 | 0.118 | 969.1 | 985.4 |
| acute_deaths_per_million | F_information_proxy_trust | 57 | 0.234 | 961.0 | 977.3 |
| acute_deaths_per_million | I_trust_x_information_integrity | 57 | 0.295 | 957.9 | 978.4 |
| acute_deaths_per_million | I_trust_x_material_capacity | 57 | 0.352 | 952.3 | 970.7 |
| acute_deaths_per_million | I_trust_x_policy_stringency | 57 | 0.317 | 955.3 | 973.7 |
| deaths_per_million | A_controls_only | 57 | 0.226 | 979.7 | 994.0 |
| deaths_per_million | B_generalized_trust | 57 | 0.408 | 965.3 | 981.6 |
| deaths_per_million | C_institutional_trust | 57 | 0.465 | 959.5 | 975.8 |
| deaths_per_million | D_trust_density | 57 | 0.443 | 961.8 | 978.2 |
| deaths_per_million | E_expert_proxy_trust | 57 | 0.258 | 978.2 | 994.5 |
| deaths_per_million | F_information_proxy_trust | 57 | 0.372 | 968.7 | 985.0 |
| deaths_per_million | I_trust_x_information_integrity | 57 | 0.424 | 965.3 | 985.8 |
| deaths_per_million | I_trust_x_material_capacity | 57 | 0.485 | 958.2 | 976.6 |
| deaths_per_million | I_trust_x_policy_stringency | 57 | 0.443 | 962.6 | 981.0 |
| excess_mortality | A_controls_only | 43 | 0.057 | 772.5 | 784.9 |
| excess_mortality | B_generalized_trust | 43 | 0.140 | 769.4 | 783.5 |
| excess_mortality | C_institutional_trust | 43 | 0.157 | 768.5 | 782.6 |
| excess_mortality | D_trust_density | 43 | 0.150 | 768.9 | 783.0 |
| excess_mortality | E_expert_proxy_trust | 43 | 0.040 | 774.1 | 788.2 |
| excess_mortality | F_information_proxy_trust | 43 | 0.116 | 770.6 | 784.7 |
| excess_mortality | I_trust_x_information_integrity | 43 | 0.124 | 771.7 | 789.3 |
| excess_mortality | I_trust_x_material_capacity | 43 | 0.164 | 768.9 | 784.8 |
| excess_mortality | I_trust_x_policy_stringency | 43 | 0.126 | 770.8 | 786.7 |
| non_vaccinated_share | A_controls_only | 57 | 0.240 | 489.9 | 504.2 |
| non_vaccinated_share | B_generalized_trust | 57 | 0.231 | 491.4 | 507.7 |
| non_vaccinated_share | C_institutional_trust | 57 | 0.275 | 488.0 | 504.4 |
| non_vaccinated_share | D_trust_density | 57 | 0.323 | 484.1 | 500.5 |
| non_vaccinated_share | E_expert_proxy_trust | 57 | 0.416 | 475.7 | 492.1 |
| non_vaccinated_share | F_information_proxy_trust | 57 | 0.315 | 484.8 | 501.1 |
| non_vaccinated_share | I_trust_x_information_integrity | 57 | 0.344 | 484.0 | 504.4 |
| non_vaccinated_share | I_trust_x_material_capacity | 57 | 0.329 | 484.4 | 502.8 |
| non_vaccinated_share | I_trust_x_policy_stringency | 57 | 0.359 | 481.9 | 500.3 |
| non_vaccinated_share_2021 | A_controls_only | 57 | 0.466 | 483.2 | 497.5 |
| non_vaccinated_share_2021 | B_generalized_trust | 57 | 0.459 | 484.8 | 501.2 |
| non_vaccinated_share_2021 | C_institutional_trust | 57 | 0.474 | 483.2 | 499.5 |
| non_vaccinated_share_2021 | D_trust_density | 57 | 0.496 | 480.7 | 497.1 |
| non_vaccinated_share_2021 | E_expert_proxy_trust | 57 | 0.535 | 476.2 | 492.5 |
| non_vaccinated_share_2021 | F_information_proxy_trust | 57 | 0.490 | 481.4 | 497.7 |
| non_vaccinated_share_2021 | I_trust_x_information_integrity | 57 | 0.502 | 481.6 | 502.1 |
| non_vaccinated_share_2021 | I_trust_x_material_capacity | 57 | 0.490 | 482.2 | 500.6 |
| non_vaccinated_share_2021 | I_trust_x_policy_stringency | 57 | 0.517 | 479.2 | 497.6 |
| recovery_deaths_per_million | A_controls_only | 57 | 0.517 | 803.0 | 817.3 |
| recovery_deaths_per_million | B_generalized_trust | 57 | 0.558 | 798.8 | 815.1 |
| recovery_deaths_per_million | C_institutional_trust | 57 | 0.538 | 801.3 | 817.7 |
| recovery_deaths_per_million | D_trust_density | 57 | 0.551 | 799.6 | 816.0 |
| recovery_deaths_per_million | E_expert_proxy_trust | 57 | 0.520 | 803.5 | 819.8 |
| recovery_deaths_per_million | F_information_proxy_trust | 57 | 0.553 | 799.3 | 815.7 |
| recovery_deaths_per_million | I_trust_x_information_integrity | 57 | 0.564 | 799.6 | 820.0 |
| recovery_deaths_per_million | I_trust_x_material_capacity | 57 | 0.582 | 796.4 | 814.8 |
| recovery_deaths_per_million | I_trust_x_policy_stringency | 57 | 0.551 | 800.5 | 818.9 |
| vaccination_rate | A_controls_only | 57 | 0.240 | 489.9 | 504.2 |
| vaccination_rate | B_generalized_trust | 57 | 0.231 | 491.4 | 507.7 |
| vaccination_rate | C_institutional_trust | 57 | 0.275 | 488.0 | 504.4 |
| vaccination_rate | D_trust_density | 57 | 0.323 | 484.1 | 500.5 |
| vaccination_rate | E_expert_proxy_trust | 57 | 0.416 | 475.7 | 492.1 |
| vaccination_rate | F_information_proxy_trust | 57 | 0.315 | 484.8 | 501.1 |
| vaccination_rate | I_trust_x_information_integrity | 57 | 0.344 | 484.0 | 504.4 |
| vaccination_rate | I_trust_x_material_capacity | 57 | 0.329 | 484.4 | 502.8 |
| vaccination_rate | I_trust_x_policy_stringency | 57 | 0.359 | 481.9 | 500.3 |
| vaccination_rate_2021 | A_controls_only | 57 | 0.466 | 483.2 | 497.5 |
| vaccination_rate_2021 | B_generalized_trust | 57 | 0.459 | 484.8 | 501.2 |
| vaccination_rate_2021 | C_institutional_trust | 57 | 0.474 | 483.2 | 499.5 |
| vaccination_rate_2021 | D_trust_density | 57 | 0.496 | 480.7 | 497.1 |
| vaccination_rate_2021 | E_expert_proxy_trust | 57 | 0.535 | 476.2 | 492.5 |
| vaccination_rate_2021 | F_information_proxy_trust | 57 | 0.490 | 481.4 | 497.7 |
| vaccination_rate_2021 | I_trust_x_information_integrity | 57 | 0.502 | 481.6 | 502.1 |
| vaccination_rate_2021 | I_trust_x_material_capacity | 57 | 0.490 | 482.2 | 500.6 |
| vaccination_rate_2021 | I_trust_x_policy_stringency | 57 | 0.517 | 479.2 | 497.6 |

## Interaction Tests

| Outcome | Model | Interaction | Coef | 95% CI | p | Interpretation |
|---|---|---:|---:|---:|---:|---|
| acute_deaths_per_million | I_trust_x_information_integrity | z_trust_density_composite:z_information_integrity_proxy | 3.294 | [-384.656, 391.244] | 0.987 | not statistically significant |
| acute_deaths_per_million | I_trust_x_material_capacity | z_trust_density_composite:z_log_gdp_per_capita | -346.295 | [-658.447, -34.142] | 0.030 | statistically significant at p<0.05 |
| acute_deaths_per_million | I_trust_x_policy_stringency | z_trust_density_composite:z_stringency_index | -119.272 | [-401.398, 162.853] | 0.407 | not statistically significant |
| deaths_per_million | I_trust_x_information_integrity | z_trust_density_composite:z_information_integrity_proxy | -55.377 | [-462.407, 351.653] | 0.790 | not statistically significant |
| deaths_per_million | I_trust_x_material_capacity | z_trust_density_composite:z_log_gdp_per_capita | -451.168 | [-798.761, -103.574] | 0.011 | statistically significant at p<0.05 |
| deaths_per_million | I_trust_x_policy_stringency | z_trust_density_composite:z_stringency_index | -155.538 | [-457.094, 146.017] | 0.312 | not statistically significant |
| excess_mortality | I_trust_x_information_integrity | z_trust_density_composite:z_information_integrity_proxy | 382.674 | [-580.202, 1345.550] | 0.436 | not statistically significant |
| excess_mortality | I_trust_x_material_capacity | z_trust_density_composite:z_log_gdp_per_capita | -490.590 | [-1103.103, 121.923] | 0.116 | not statistically significant |
| excess_mortality | I_trust_x_policy_stringency | z_trust_density_composite:z_stringency_index | -54.645 | [-1231.220, 1121.930] | 0.927 | not statistically significant |
| non_vaccinated_share | I_trust_x_information_integrity | z_trust_density_composite:z_information_integrity_proxy | -3.848 | [-9.269, 1.573] | 0.164 | not statistically significant |
| non_vaccinated_share | I_trust_x_material_capacity | z_trust_density_composite:z_log_gdp_per_capita | 3.826 | [-3.305, 10.957] | 0.293 | not statistically significant |
| non_vaccinated_share | I_trust_x_policy_stringency | z_trust_density_composite:z_stringency_index | -4.382 | [-14.096, 5.331] | 0.377 | not statistically significant |
| non_vaccinated_share_2021 | I_trust_x_information_integrity | z_trust_density_composite:z_information_integrity_proxy | -3.423 | [-9.509, 2.664] | 0.270 | not statistically significant |
| non_vaccinated_share_2021 | I_trust_x_material_capacity | z_trust_density_composite:z_log_gdp_per_capita | 1.996 | [-4.728, 8.720] | 0.561 | not statistically significant |
| non_vaccinated_share_2021 | I_trust_x_policy_stringency | z_trust_density_composite:z_stringency_index | -3.905 | [-12.822, 5.012] | 0.391 | not statistically significant |
| recovery_deaths_per_million | I_trust_x_information_integrity | z_trust_density_composite:z_information_integrity_proxy | -58.671 | [-109.797, -7.545] | 0.024 | statistically significant at p<0.05 |
| recovery_deaths_per_million | I_trust_x_material_capacity | z_trust_density_composite:z_log_gdp_per_capita | -104.873 | [-211.461, 1.715] | 0.054 | marginal at p<0.10 |
| recovery_deaths_per_million | I_trust_x_policy_stringency | z_trust_density_composite:z_stringency_index | -36.266 | [-91.402, 18.870] | 0.197 | not statistically significant |
| vaccination_rate | I_trust_x_information_integrity | z_trust_density_composite:z_information_integrity_proxy | 3.848 | [-1.573, 9.269] | 0.164 | not statistically significant |
| vaccination_rate | I_trust_x_material_capacity | z_trust_density_composite:z_log_gdp_per_capita | -3.826 | [-10.957, 3.305] | 0.293 | not statistically significant |
| vaccination_rate | I_trust_x_policy_stringency | z_trust_density_composite:z_stringency_index | 4.382 | [-5.331, 14.096] | 0.377 | not statistically significant |
| vaccination_rate_2021 | I_trust_x_information_integrity | z_trust_density_composite:z_information_integrity_proxy | 3.423 | [-2.664, 9.509] | 0.270 | not statistically significant |
| vaccination_rate_2021 | I_trust_x_material_capacity | z_trust_density_composite:z_log_gdp_per_capita | -1.996 | [-8.720, 4.728] | 0.561 | not statistically significant |
| vaccination_rate_2021 | I_trust_x_policy_stringency | z_trust_density_composite:z_stringency_index | 3.905 | [-5.012, 12.822] | 0.391 | not statistically significant |

## Intellectual Honesty and Falsification Criteria

The AetherCore Trust Density claim is weakened if trust coefficients are small, directionally inconsistent, statistically insignificant after controls, or fail to improve adjusted R²/AIC/BIC across outcomes. It is also weakened if effects disappear when alternative outcomes or control sets are used.

The claim receives tentative support only where trust variables add incremental predictive value after controls, show directionally coherent effects across outcomes, and where interaction terms suggest that trust strengthens the performance of material capacity, policy response, or information integrity. Even then, these results remain correlational.

## Data Quality Limitations

- Cross-country sample size is limited by WVS Wave 7 country coverage and missing COVID excess-mortality data.
- WVS confidence-in-experts measures are not guaranteed to include direct trust in scientists or doctors; the script uses available expert-adjacent variables and reports the exact columns.
- COVID outcomes were shaped by reporting practices, pandemic timing, variants, policy regimes, geography, and measurement quality.
- Anti-vaxxer and no-masker behavior are not directly measured in this pass. `non_vaccinated_share` is an uptake-gap proxy only; no masking refusal variable is present in WVS/OWID.
- Some controls are highly collinear, especially GDP per capita, HDI, and healthcare capacity.
- Results should be treated as a first-pass empirical screen, not as proof of the theory.

## Generated Artifacts

- Clean merged dataset: `data_processed/aethercore_test001_merged.csv`
- Country-level WVS trust dataset: `data_processed/wvs_wave7_country_trust.csv`
- Country-level OWID dataset: `data_processed/owid_covid_country.csv`
- Regression table: `outputs/regression_results.csv`
- Model comparison table: `outputs/model_comparison.csv`
- Figures: `figures/`

## Future Tests Needed

- Replicate with alternative trust datasets and survey waves.
- Add independent information-integrity proxies such as press freedom, misinformation exposure, or institutional transparency indices.
- Use panel or longitudinal designs where possible.
- Test pre-registered model specifications and alternative outcome windows.
- Compare COVID with other shocks such as natural disasters, financial crises, and public-health campaigns.