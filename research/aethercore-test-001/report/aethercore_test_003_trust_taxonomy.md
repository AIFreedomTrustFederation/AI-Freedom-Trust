# AetherCore Test 003: Centralized Trust vs Decentralized Trust Migration

## Purpose

This pass tests whether COVID shock response is better explained by a taxonomy of trust rather than a single trust-density composite.

The core hypothesis is that risk may rise where centralized institutional trust is low, expert/information trust is weak, and decentralized social trust becomes the dominant coordination pathway.

## Data

- WVS taxonomy countries merged with OWID/Test 001 data: 65
- Rows in final Test 003 dataset: 65
- Behavioral resistance variables are included when Test 002 YouGov aggregates are available.

## Trust Taxonomy

- `centralized_institutional_trust`: police, courts, government, political parties, parliament, civil service, elections.
- `expert_epistemic_trust`: universities and available science-oriented WVS items.
- `information_trust`: press and television confidence.
- `bonding_social_trust`: family, neighborhood, people known personally.
- `bridging_social_trust`: people met for the first time, people of another religion, people of another nationality.
- `decentralized_social_trust`: average of bonding and bridging social trust.
- `centralization_gap`: decentralized social trust minus centralized institutional trust.

## Variable Audit

```json
{
  "wvs_file": "C:\\Users\\aifre\\OneDrive\\Documents\\CCP\\AI-Freedom-Trust\\research\\aethercore-test-001\\data_raw\\WVS_Cross-National_Wave_7_csv_v6_0.csv",
  "iso_column": "B_COUNTRY_ALPHA",
  "country_column": "B_COUNTRY",
  "constructs": {
    "centralized_institutional_trust": {
      "Q69": "police",
      "Q70": "courts",
      "Q71": "government",
      "Q72": "political_parties",
      "Q73": "parliament",
      "Q74": "civil_service",
      "Q76": "elections"
    },
    "expert_epistemic_trust": {
      "Q75": "universities",
      "Q158": "science_item_1",
      "Q159": "science_item_2"
    },
    "information_trust": {
      "Q66": "press",
      "Q67": "television"
    },
    "bonding_social_trust": {
      "Q58": "family",
      "Q59": "neighborhood",
      "Q60": "people_known_personally"
    },
    "bridging_social_trust": {
      "Q61": "people_met_first_time",
      "Q62": "people_another_religion",
      "Q63": "people_another_nationality"
    }
  }
}
```

## Main Coefficients

| Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |
|---|---|---:|---:|---:|---:|---:|---:|
| acute_deaths_per_million | full_central_only | z_centralized_institutional_trust | -610.875 | [-946.229, -275.522] | 0.000 (p<0.01) | 57 | 0.360 |
| acute_deaths_per_million | full_central_x_decentralized | z_centralized_institutional_trust | -465.194 | [-698.703, -231.685] | 0.000 (p<0.01) | 57 | 0.412 |
| acute_deaths_per_million | full_central_x_decentralized | z_centralized_institutional_trust:z_decentralized_social_trust | 137.078 | [-476.273, 750.429] | 0.661 (n.s.) | 57 | 0.412 |
| acute_deaths_per_million | full_central_x_decentralized | z_decentralized_social_trust | -265.744 | [-558.240, 26.751] | 0.075 (p<0.10) | 57 | 0.412 |
| acute_deaths_per_million | full_central_x_expert | z_centralized_institutional_trust | -854.180 | [-1389.299, -319.061] | 0.002 (p<0.01) | 57 | 0.381 |
| acute_deaths_per_million | full_central_x_expert | z_centralized_institutional_trust:z_expert_epistemic_trust | 31.186 | [-418.428, 480.800] | 0.892 (n.s.) | 57 | 0.381 |
| acute_deaths_per_million | full_central_x_expert | z_expert_epistemic_trust | 370.415 | [-50.484, 791.314] | 0.085 (p<0.10) | 57 | 0.381 |
| acute_deaths_per_million | full_decentralized_only | z_decentralized_social_trust | -501.601 | [-977.797, -25.405] | 0.039 (p<0.05) | 57 | 0.248 |
| acute_deaths_per_million | full_expert_only | z_expert_epistemic_trust | -267.448 | [-544.566, 9.669] | 0.059 (p<0.10) | 57 | 0.118 |
| acute_deaths_per_million | full_gap_only | z_centralization_gap | 401.650 | [180.502, 622.797] | 0.000 (p<0.01) | 57 | 0.190 |
| acute_deaths_per_million | full_information_only | z_information_trust | -521.988 | [-833.515, -210.460] | 0.001 (p<0.01) | 57 | 0.234 |
| acute_deaths_per_million | full_taxonomy_channels | z_centralized_institutional_trust | -655.942 | [-1143.436, -168.447] | 0.008 (p<0.01) | 57 | 0.410 |
| acute_deaths_per_million | full_taxonomy_channels | z_decentralized_social_trust | -271.405 | [-656.789, 113.979] | 0.167 (n.s.) | 57 | 0.410 |
| acute_deaths_per_million | full_taxonomy_channels | z_expert_epistemic_trust | 251.512 | [-76.026, 579.050] | 0.132 (n.s.) | 57 | 0.410 |
| acute_deaths_per_million | full_taxonomy_channels | z_information_trust | -44.771 | [-476.824, 387.282] | 0.839 (n.s.) | 57 | 0.410 |
| deaths_per_million | full_central_only | z_centralized_institutional_trust | -679.612 | [-1025.524, -333.700] | 0.000 (p<0.01) | 57 | 0.469 |
| deaths_per_million | full_central_x_decentralized | z_centralized_institutional_trust | -549.934 | [-804.386, -295.482] | 0.000 (p<0.01) | 57 | 0.497 |
| deaths_per_million | full_central_x_decentralized | z_centralized_institutional_trust:z_decentralized_social_trust | 90.787 | [-557.876, 739.449] | 0.784 (n.s.) | 57 | 0.497 |
| deaths_per_million | full_central_x_decentralized | z_decentralized_social_trust | -279.824 | [-594.131, 34.482] | 0.081 (p<0.10) | 57 | 0.497 |
| deaths_per_million | full_central_x_expert | z_centralized_institutional_trust | -921.017 | [-1480.015, -362.018] | 0.001 (p<0.01) | 57 | 0.483 |
| deaths_per_million | full_central_x_expert | z_centralized_institutional_trust:z_expert_epistemic_trust | -1.293 | [-472.998, 470.411] | 0.996 (n.s.) | 57 | 0.483 |
| deaths_per_million | full_central_x_expert | z_expert_epistemic_trust | 370.978 | [-90.526, 832.482] | 0.115 (n.s.) | 57 | 0.483 |
| deaths_per_million | full_decentralized_only | z_decentralized_social_trust | -521.065 | [-1017.586, -24.545] | 0.040 (p<0.05) | 57 | 0.348 |
| deaths_per_million | full_expert_only | z_expert_epistemic_trust | -311.325 | [-616.687, -5.964] | 0.046 (p<0.05) | 57 | 0.258 |
| deaths_per_million | full_gap_only | z_centralization_gap | 465.330 | [211.679, 718.980] | 0.000 (p<0.01) | 57 | 0.327 |
| deaths_per_million | full_information_only | z_information_trust | -609.880 | [-937.035, -282.726] | 0.000 (p<0.01) | 57 | 0.372 |
| deaths_per_million | full_taxonomy_channels | z_centralized_institutional_trust | -684.713 | [-1222.016, -147.409] | 0.013 (p<0.05) | 57 | 0.502 |
| deaths_per_million | full_taxonomy_channels | z_decentralized_social_trust | -271.587 | [-681.527, 138.353] | 0.194 (n.s.) | 57 | 0.502 |
| deaths_per_million | full_taxonomy_channels | z_expert_epistemic_trust | 272.657 | [-96.995, 642.309] | 0.148 (n.s.) | 57 | 0.502 |
| deaths_per_million | full_taxonomy_channels | z_information_trust | -120.125 | [-551.977, 311.726] | 0.586 (n.s.) | 57 | 0.502 |
| excess_mortality | full_central_only | z_centralized_institutional_trust | -649.104 | [-1168.392, -129.817] | 0.014 (p<0.05) | 43 | 0.148 |
| excess_mortality | full_central_x_decentralized | z_centralized_institutional_trust | -608.022 | [-1197.818, -18.227] | 0.043 (p<0.05) | 43 | 0.130 |
| excess_mortality | full_central_x_decentralized | z_centralized_institutional_trust:z_decentralized_social_trust | -126.370 | [-816.627, 563.887] | 0.720 (n.s.) | 43 | 0.130 |
| excess_mortality | full_central_x_decentralized | z_decentralized_social_trust | -408.474 | [-1047.525, 230.578] | 0.210 (n.s.) | 43 | 0.130 |
| excess_mortality | full_central_x_expert | z_centralized_institutional_trust | -919.461 | [-1613.964, -224.958] | 0.009 (p<0.01) | 43 | 0.125 |
| excess_mortality | full_central_x_expert | z_centralized_institutional_trust:z_expert_epistemic_trust | 15.010 | [-490.308, 520.328] | 0.954 (n.s.) | 43 | 0.125 |
| excess_mortality | full_central_x_expert | z_expert_epistemic_trust | 446.670 | [-356.967, 1250.308] | 0.276 (n.s.) | 43 | 0.125 |
| excess_mortality | full_decentralized_only | z_decentralized_social_trust | -479.530 | [-1084.676, 125.615] | 0.120 (n.s.) | 43 | 0.097 |
| excess_mortality | full_expert_only | z_expert_epistemic_trust | -206.006 | [-784.771, 372.758] | 0.485 (n.s.) | 43 | 0.040 |
| excess_mortality | full_gap_only | z_centralization_gap | 390.860 | [-42.003, 823.724] | 0.077 (p<0.10) | 43 | 0.075 |
| excess_mortality | full_information_only | z_information_trust | -609.613 | [-1125.586, -93.640] | 0.021 (p<0.05) | 43 | 0.116 |
| excess_mortality | full_taxonomy_channels | z_centralized_institutional_trust | -578.800 | [-1818.276, 660.676] | 0.360 (n.s.) | 43 | 0.112 |
| excess_mortality | full_taxonomy_channels | z_decentralized_social_trust | -260.184 | [-849.372, 329.003] | 0.387 (n.s.) | 43 | 0.112 |
| excess_mortality | full_taxonomy_channels | z_expert_epistemic_trust | 275.378 | [-587.727, 1138.482] | 0.532 (n.s.) | 43 | 0.112 |
| excess_mortality | full_taxonomy_channels | z_information_trust | -216.024 | [-1524.173, 1092.125] | 0.746 (n.s.) | 43 | 0.112 |
| government_control_belief_vaccine_rollout_2021 | bivariate_central_only | z_centralized_institutional_trust | -0.158 | [-0.293, -0.024] | 0.021 (p<0.05) | 9 | 0.208 |
| government_control_belief_vaccine_rollout_2021 | bivariate_decentralized_only | z_decentralized_social_trust | 0.098 | [0.059, 0.137] | 0.000 (p<0.01) | 9 | 0.497 |
| government_control_belief_vaccine_rollout_2021 | bivariate_expert_only | z_expert_epistemic_trust | 0.010 | [-0.286, 0.305] | 0.948 (n.s.) | 9 | -0.141 |
| government_control_belief_vaccine_rollout_2021 | bivariate_gap_only | z_centralization_gap | 0.124 | [0.063, 0.185] | 0.000 (p<0.01) | 9 | 0.567 |
| government_control_belief_vaccine_rollout_2021 | bivariate_information_only | z_information_trust | -0.117 | [-0.212, -0.022] | 0.016 (p<0.05) | 9 | 0.416 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_central_only | z_centralized_institutional_trust | 0.037 | [-0.062, 0.136] | 0.466 (n.s.) | 9 | -0.014 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_decentralized_only | z_decentralized_social_trust | 0.015 | [-0.027, 0.057] | 0.481 (n.s.) | 9 | -0.040 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_expert_only | z_expert_epistemic_trust | 0.053 | [0.011, 0.095] | 0.013 (p<0.05) | 9 | 0.199 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_gap_only | z_centralization_gap | 0.000 | [-0.071, 0.071] | 0.999 (n.s.) | 9 | -0.143 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_information_only | z_information_trust | -0.012 | [-0.076, 0.052] | 0.719 (n.s.) | 9 | -0.104 |
| mask_compliance_outside_acute_2020 | compact_central_only | z_centralized_institutional_trust | -0.002 | [-0.095, 0.090] | 0.958 (n.s.) | 19 | 0.242 |
| mask_compliance_outside_acute_2020 | compact_central_x_decentralized | z_centralized_institutional_trust | 0.070 | [-0.007, 0.146] | 0.075 (p<0.10) | 19 | 0.660 |
| mask_compliance_outside_acute_2020 | compact_central_x_decentralized | z_centralized_institutional_trust:z_decentralized_social_trust | 0.032 | [-0.115, 0.179] | 0.665 (n.s.) | 19 | 0.660 |
| mask_compliance_outside_acute_2020 | compact_central_x_decentralized | z_decentralized_social_trust | -0.136 | [-0.224, -0.049] | 0.002 (p<0.01) | 19 | 0.660 |
| mask_compliance_outside_acute_2020 | compact_central_x_expert | z_centralized_institutional_trust | 0.125 | [-0.190, 0.441] | 0.435 (n.s.) | 19 | 0.363 |
| mask_compliance_outside_acute_2020 | compact_central_x_expert | z_centralized_institutional_trust:z_expert_epistemic_trust | -0.085 | [-0.356, 0.186] | 0.540 (n.s.) | 19 | 0.363 |
| mask_compliance_outside_acute_2020 | compact_central_x_expert | z_expert_epistemic_trust | -0.190 | [-0.475, 0.095] | 0.191 (n.s.) | 19 | 0.363 |
| mask_compliance_outside_acute_2020 | compact_decentralized_only | z_decentralized_social_trust | -0.115 | [-0.186, -0.044] | 0.002 (p<0.01) | 19 | 0.633 |
| mask_compliance_outside_acute_2020 | compact_expert_only | z_expert_epistemic_trust | -0.111 | [-0.271, 0.048] | 0.171 (n.s.) | 19 | 0.339 |
| mask_compliance_outside_acute_2020 | compact_gap_only | z_centralization_gap | -0.078 | [-0.180, 0.024] | 0.135 (n.s.) | 19 | 0.377 |
| mask_compliance_outside_acute_2020 | compact_information_only | z_information_trust | 0.084 | [-0.016, 0.184] | 0.100 (p<0.10) | 19 | 0.378 |
| mask_compliance_outside_acute_2020 | compact_taxonomy_channels | z_centralized_institutional_trust | -0.066 | [-0.330, 0.197] | 0.622 (n.s.) | 19 | 0.747 |
| mask_compliance_outside_acute_2020 | compact_taxonomy_channels | z_decentralized_social_trust | -0.101 | [-0.208, 0.006] | 0.065 (p<0.10) | 19 | 0.747 |
| mask_compliance_outside_acute_2020 | compact_taxonomy_channels | z_expert_epistemic_trust | 0.021 | [-0.216, 0.259] | 0.861 (n.s.) | 19 | 0.747 |
| mask_compliance_outside_acute_2020 | compact_taxonomy_channels | z_information_trust | 0.141 | [-0.057, 0.340] | 0.163 (n.s.) | 19 | 0.747 |
| mask_refusal_outside_acute_2020 | compact_central_only | z_centralized_institutional_trust | -0.002 | [-0.085, 0.081] | 0.956 (n.s.) | 19 | 0.261 |
| mask_refusal_outside_acute_2020 | compact_central_x_decentralized | z_centralized_institutional_trust | -0.071 | [-0.138, -0.003] | 0.039 (p<0.05) | 19 | 0.681 |
| mask_refusal_outside_acute_2020 | compact_central_x_decentralized | z_centralized_institutional_trust:z_decentralized_social_trust | -0.029 | [-0.159, 0.101] | 0.661 (n.s.) | 19 | 0.681 |
| mask_refusal_outside_acute_2020 | compact_central_x_decentralized | z_decentralized_social_trust | 0.131 | [0.055, 0.206] | 0.001 (p<0.01) | 19 | 0.681 |
| mask_refusal_outside_acute_2020 | compact_central_x_expert | z_centralized_institutional_trust | -0.116 | [-0.405, 0.174] | 0.433 (n.s.) | 19 | 0.367 |
| mask_refusal_outside_acute_2020 | compact_central_x_expert | z_centralized_institutional_trust:z_expert_epistemic_trust | 0.067 | [-0.182, 0.317] | 0.597 (n.s.) | 19 | 0.367 |
| mask_refusal_outside_acute_2020 | compact_central_x_expert | z_expert_epistemic_trust | 0.182 | [-0.085, 0.450] | 0.181 (n.s.) | 19 | 0.367 |
| mask_refusal_outside_acute_2020 | compact_decentralized_only | z_decentralized_social_trust | 0.108 | [0.042, 0.174] | 0.001 (p<0.01) | 19 | 0.641 |
| mask_refusal_outside_acute_2020 | compact_expert_only | z_expert_epistemic_trust | 0.101 | [-0.044, 0.246] | 0.172 (n.s.) | 19 | 0.348 |
| mask_refusal_outside_acute_2020 | compact_gap_only | z_centralization_gap | 0.079 | [-0.014, 0.171] | 0.095 (p<0.10) | 19 | 0.412 |
| mask_refusal_outside_acute_2020 | compact_information_only | z_information_trust | -0.082 | [-0.170, 0.007] | 0.071 (p<0.10) | 19 | 0.400 |
| mask_refusal_outside_acute_2020 | compact_taxonomy_channels | z_centralized_institutional_trust | 0.047 | [-0.192, 0.286] | 0.701 (n.s.) | 19 | 0.751 |
| mask_refusal_outside_acute_2020 | compact_taxonomy_channels | z_decentralized_social_trust | 0.099 | [0.004, 0.194] | 0.041 (p<0.05) | 19 | 0.751 |
| mask_refusal_outside_acute_2020 | compact_taxonomy_channels | z_expert_epistemic_trust | -0.014 | [-0.244, 0.217] | 0.909 (n.s.) | 19 | 0.751 |
| mask_refusal_outside_acute_2020 | compact_taxonomy_channels | z_information_trust | -0.123 | [-0.308, 0.061] | 0.191 (n.s.) | 19 | 0.751 |
| non_vaccinated_share | full_central_only | z_centralized_institutional_trust | -4.471 | [-8.789, -0.153] | 0.042 (p<0.05) | 57 | 0.284 |
| non_vaccinated_share | full_central_x_decentralized | z_centralized_institutional_trust | -8.142 | [-13.051, -3.233] | 0.001 (p<0.01) | 57 | 0.429 |
| non_vaccinated_share | full_central_x_decentralized | z_centralized_institutional_trust:z_decentralized_social_trust | -4.061 | [-8.625, 0.503] | 0.081 (p<0.10) | 57 | 0.429 |
| non_vaccinated_share | full_central_x_decentralized | z_decentralized_social_trust | 5.854 | [2.225, 9.483] | 0.002 (p<0.01) | 57 | 0.429 |
| non_vaccinated_share | full_central_x_expert | z_centralized_institutional_trust | 3.073 | [-2.690, 8.835] | 0.296 (n.s.) | 57 | 0.415 |
| non_vaccinated_share | full_central_x_expert | z_centralized_institutional_trust:z_expert_epistemic_trust | -2.802 | [-7.217, 1.613] | 0.213 (n.s.) | 57 | 0.415 |
| non_vaccinated_share | full_central_x_expert | z_expert_epistemic_trust | -11.288 | [-17.024, -5.552] | 0.000 (p<0.01) | 57 | 0.415 |
| non_vaccinated_share | full_decentralized_only | z_decentralized_social_trust | 5.133 | [0.732, 9.534] | 0.022 (p<0.05) | 57 | 0.296 |
| non_vaccinated_share | full_expert_only | z_expert_epistemic_trust | -8.572 | [-11.972, -5.173] | 0.000 (p<0.01) | 57 | 0.416 |
| non_vaccinated_share | full_gap_only | z_centralization_gap | 7.341 | [3.466, 11.217] | 0.000 (p<0.01) | 57 | 0.378 |
| non_vaccinated_share | full_information_only | z_information_trust | -6.270 | [-10.560, -1.980] | 0.004 (p<0.01) | 57 | 0.315 |
| non_vaccinated_share | full_taxonomy_channels | z_centralized_institutional_trust | 0.739 | [-10.150, 11.628] | 0.894 (n.s.) | 57 | 0.468 |
| non_vaccinated_share | full_taxonomy_channels | z_decentralized_social_trust | 5.413 | [-0.143, 10.970] | 0.056 (p<0.10) | 57 | 0.468 |
| non_vaccinated_share | full_taxonomy_channels | z_expert_epistemic_trust | -7.674 | [-14.070, -1.279] | 0.019 (p<0.05) | 57 | 0.468 |
| non_vaccinated_share | full_taxonomy_channels | z_information_trust | -2.731 | [-12.260, 6.799] | 0.574 (n.s.) | 57 | 0.468 |
| recovery_deaths_per_million | full_central_only | z_centralized_institutional_trust | -68.737 | [-124.746, -12.727] | 0.016 (p<0.05) | 57 | 0.544 |
| recovery_deaths_per_million | full_central_x_decentralized | z_centralized_institutional_trust | -84.740 | [-162.087, -7.393] | 0.032 (p<0.05) | 57 | 0.536 |
| recovery_deaths_per_million | full_central_x_decentralized | z_centralized_institutional_trust:z_decentralized_social_trust | -46.291 | [-148.768, 56.185] | 0.376 (n.s.) | 57 | 0.536 |
| recovery_deaths_per_million | full_central_x_decentralized | z_decentralized_social_trust | -14.080 | [-139.918, 111.758] | 0.826 (n.s.) | 57 | 0.536 |
| recovery_deaths_per_million | full_central_x_expert | z_centralized_institutional_trust | -66.837 | [-155.891, 22.217] | 0.141 (n.s.) | 57 | 0.531 |
| recovery_deaths_per_million | full_central_x_expert | z_centralized_institutional_trust:z_expert_epistemic_trust | -32.479 | [-96.980, 32.022] | 0.324 (n.s.) | 57 | 0.531 |
| recovery_deaths_per_million | full_central_x_expert | z_expert_epistemic_trust | 0.562 | [-90.058, 91.183] | 0.990 (n.s.) | 57 | 0.531 |
| recovery_deaths_per_million | full_decentralized_only | z_decentralized_social_trust | -19.464 | [-109.797, 70.869] | 0.673 (n.s.) | 57 | 0.510 |
| recovery_deaths_per_million | full_expert_only | z_expert_epistemic_trust | -43.877 | [-100.040, 12.286] | 0.126 (n.s.) | 57 | 0.520 |
| recovery_deaths_per_million | full_gap_only | z_centralization_gap | 63.680 | [1.392, 125.968] | 0.045 (p<0.05) | 57 | 0.537 |
| recovery_deaths_per_million | full_information_only | z_information_trust | -87.893 | [-179.608, 3.822] | 0.060 (p<0.10) | 57 | 0.553 |
| recovery_deaths_per_million | full_taxonomy_channels | z_centralized_institutional_trust | -28.771 | [-221.737, 164.195] | 0.770 (n.s.) | 57 | 0.527 |
| recovery_deaths_per_million | full_taxonomy_channels | z_decentralized_social_trust | -0.182 | [-120.990, 120.626] | 0.998 (n.s.) | 57 | 0.527 |
| recovery_deaths_per_million | full_taxonomy_channels | z_expert_epistemic_trust | 21.145 | [-83.970, 126.259] | 0.693 (n.s.) | 57 | 0.527 |
| recovery_deaths_per_million | full_taxonomy_channels | z_information_trust | -75.354 | [-308.353, 157.644] | 0.526 (n.s.) | 57 | 0.527 |
| vaccination_rate | full_central_only | z_centralized_institutional_trust | 4.471 | [0.153, 8.789] | 0.042 (p<0.05) | 57 | 0.284 |
| vaccination_rate | full_central_x_decentralized | z_centralized_institutional_trust | 8.142 | [3.233, 13.051] | 0.001 (p<0.01) | 57 | 0.429 |
| vaccination_rate | full_central_x_decentralized | z_centralized_institutional_trust:z_decentralized_social_trust | 4.061 | [-0.503, 8.625] | 0.081 (p<0.10) | 57 | 0.429 |
| vaccination_rate | full_central_x_decentralized | z_decentralized_social_trust | -5.854 | [-9.483, -2.225] | 0.002 (p<0.01) | 57 | 0.429 |
| vaccination_rate | full_central_x_expert | z_centralized_institutional_trust | -3.073 | [-8.835, 2.690] | 0.296 (n.s.) | 57 | 0.415 |
| vaccination_rate | full_central_x_expert | z_centralized_institutional_trust:z_expert_epistemic_trust | 2.802 | [-1.613, 7.217] | 0.213 (n.s.) | 57 | 0.415 |
| vaccination_rate | full_central_x_expert | z_expert_epistemic_trust | 11.288 | [5.552, 17.024] | 0.000 (p<0.01) | 57 | 0.415 |
| vaccination_rate | full_decentralized_only | z_decentralized_social_trust | -5.133 | [-9.534, -0.732] | 0.022 (p<0.05) | 57 | 0.296 |
| vaccination_rate | full_expert_only | z_expert_epistemic_trust | 8.572 | [5.173, 11.972] | 0.000 (p<0.01) | 57 | 0.416 |
| vaccination_rate | full_gap_only | z_centralization_gap | -7.341 | [-11.217, -3.466] | 0.000 (p<0.01) | 57 | 0.378 |
| vaccination_rate | full_information_only | z_information_trust | 6.270 | [1.980, 10.560] | 0.004 (p<0.01) | 57 | 0.315 |
| vaccination_rate | full_taxonomy_channels | z_centralized_institutional_trust | -0.739 | [-11.628, 10.150] | 0.894 (n.s.) | 57 | 0.468 |
| vaccination_rate | full_taxonomy_channels | z_decentralized_social_trust | -5.413 | [-10.970, 0.143] | 0.056 (p<0.10) | 57 | 0.468 |
| vaccination_rate | full_taxonomy_channels | z_expert_epistemic_trust | 7.674 | [1.279, 14.070] | 0.019 (p<0.05) | 57 | 0.468 |
| vaccination_rate | full_taxonomy_channels | z_information_trust | 2.731 | [-6.799, 12.260] | 0.574 (n.s.) | 57 | 0.468 |
| vaccine_intent_vaccine_rollout_2021 | bivariate_central_only | z_centralized_institutional_trust | 0.002 | [-0.218, 0.222] | 0.986 (n.s.) | 9 | -0.143 |
| vaccine_intent_vaccine_rollout_2021 | bivariate_decentralized_only | z_decentralized_social_trust | 0.021 | [-0.069, 0.110] | 0.648 (n.s.) | 9 | -0.108 |
| vaccine_intent_vaccine_rollout_2021 | bivariate_expert_only | z_expert_epistemic_trust | 0.056 | [-0.165, 0.277] | 0.618 (n.s.) | 9 | -0.076 |
| vaccine_intent_vaccine_rollout_2021 | bivariate_gap_only | z_centralization_gap | 0.015 | [-0.104, 0.134] | 0.802 (n.s.) | 9 | -0.130 |
| vaccine_intent_vaccine_rollout_2021 | bivariate_information_only | z_information_trust | -0.011 | [-0.163, 0.142] | 0.891 (n.s.) | 9 | -0.137 |
| vaccine_refusal_vaccine_rollout_2021 | bivariate_central_only | z_centralized_institutional_trust | -0.039 | [-0.269, 0.191] | 0.737 (n.s.) | 9 | -0.120 |
| vaccine_refusal_vaccine_rollout_2021 | bivariate_decentralized_only | z_decentralized_social_trust | 0.005 | [-0.086, 0.096] | 0.910 (n.s.) | 9 | -0.141 |
| vaccine_refusal_vaccine_rollout_2021 | bivariate_expert_only | z_expert_epistemic_trust | -0.046 | [-0.318, 0.227] | 0.741 (n.s.) | 9 | -0.104 |
| vaccine_refusal_vaccine_rollout_2021 | bivariate_gap_only | z_centralization_gap | 0.016 | [-0.107, 0.140] | 0.797 (n.s.) | 9 | -0.130 |
| vaccine_refusal_vaccine_rollout_2021 | bivariate_information_only | z_information_trust | -0.022 | [-0.180, 0.136] | 0.789 (n.s.) | 9 | -0.123 |

## Interpretation

This test should not be read as proof that centralized distrust caused mortality. It asks whether mortality and behavioral resistance align more strongly with particular trust channels.

The migration hypothesis gains support if low centralized trust, high centralization gap, or negative central x decentralized interactions predict worse outcomes. It is weakened if decentralized trust is protective, if central trust is not associated with outcomes, or if effects vanish after controls.

## Limitations

- WVS Wave 7 timing overlaps the pandemic in some countries, so trust may be partly post-shock rather than purely pre-shock.
- Country-level regressions cannot prove individual-level behavioral mechanisms.
- The YouGov behavioral overlap remains small for vaccine/conspiracy outcomes.
- Central institutions may be trusted because they are competent; trust may be a signal of state capacity as well as public psychology.