# AetherCore Test 006: Trust Migration Mechanism Interactions

## Purpose

This pass tests whether the centralization-gap risk is conditioned by expert or information trust.

Main mechanism models:

- outcome ~ controls + centralization_gap + expert_trust + gap x expert_trust
- outcome ~ controls + centralization_gap + information_trust + gap x information_trust
- outcome ~ controls + misaligned_migration_index
- outcome ~ controls + misaligned_information_index

## Coefficients

| Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |
|---|---|---:|---:|---:|---:|---:|---:|
| acute_deaths_per_million | full_gap_x_expert | z_centralization_gap | 400.535 | [52.640, 748.429] | 0.024 | 57 | 0.167 |
| acute_deaths_per_million | full_gap_x_expert | z_centralization_gap:z_expert_epistemic_trust | 114.396 | [-220.683, 449.475] | 0.503 | 57 | 0.167 |
| acute_deaths_per_million | full_gap_x_expert | z_expert_epistemic_trust | 16.738 | [-388.680, 422.156] | 0.936 | 57 | 0.167 |
| acute_deaths_per_million | full_gap_x_information | z_centralization_gap | 66.443 | [-326.699, 459.586] | 0.740 | 57 | 0.209 |
| acute_deaths_per_million | full_gap_x_information | z_centralization_gap:z_information_trust | 70.868 | [-231.860, 373.595] | 0.646 | 57 | 0.209 |
| acute_deaths_per_million | full_gap_x_information | z_information_trust | -437.660 | [-946.386, 71.066] | 0.092 | 57 | 0.209 |
| acute_deaths_per_million | full_misaligned_expert_index | z_misaligned_migration_index | 365.364 | [124.100, 606.628] | 0.003 | 57 | 0.171 |
| acute_deaths_per_million | full_misaligned_information_index | z_misaligned_information_index | 478.992 | [219.145, 738.840] | 0.000 | 57 | 0.226 |
| deaths_per_million | full_gap_x_expert | z_centralization_gap | 465.660 | [50.714, 880.606] | 0.028 | 57 | 0.308 |
| deaths_per_million | full_gap_x_expert | z_centralization_gap:z_expert_epistemic_trust | 123.550 | [-257.995, 505.094] | 0.526 | 57 | 0.308 |
| deaths_per_million | full_gap_x_expert | z_expert_epistemic_trust | 20.324 | [-435.260, 475.909] | 0.930 | 57 | 0.308 |
| deaths_per_million | full_gap_x_information | z_centralization_gap | 58.405 | [-377.985, 494.795] | 0.793 | 57 | 0.354 |
| deaths_per_million | full_gap_x_information | z_centralization_gap:z_information_trust | 105.712 | [-223.868, 435.292] | 0.530 | 57 | 0.354 |
| deaths_per_million | full_gap_x_information | z_information_trust | -519.171 | [-1063.034, 24.692] | 0.061 | 57 | 0.354 |
| deaths_per_million | full_misaligned_expert_index | z_misaligned_migration_index | 423.898 | [154.837, 692.958] | 0.002 | 57 | 0.309 |
| deaths_per_million | full_misaligned_information_index | z_misaligned_information_index | 557.146 | [271.453, 842.839] | 0.000 | 57 | 0.362 |
| excess_mortality | full_gap_x_expert | z_centralization_gap | 572.631 | [-91.533, 1236.795] | 0.091 | 43 | 0.028 |
| excess_mortality | full_gap_x_expert | z_centralization_gap:z_expert_epistemic_trust | 61.900 | [-411.275, 535.076] | 0.798 | 43 | 0.028 |
| excess_mortality | full_gap_x_expert | z_expert_epistemic_trust | 255.416 | [-626.913, 1137.745] | 0.570 | 43 | 0.028 |
| excess_mortality | full_gap_x_information | z_centralization_gap | -103.397 | [-1110.251, 903.457] | 0.840 | 43 | 0.079 |
| excess_mortality | full_gap_x_information | z_centralization_gap:z_information_trust | -222.200 | [-818.288, 373.889] | 0.465 | 43 | 0.079 |
| excess_mortality | full_gap_x_information | z_information_trust | -766.506 | [-1901.357, 368.345] | 0.186 | 43 | 0.079 |
| excess_mortality | full_misaligned_expert_index | z_misaligned_migration_index | 330.592 | [-133.065, 794.248] | 0.162 | 43 | 0.062 |
| excess_mortality | full_misaligned_information_index | z_misaligned_information_index | 502.865 | [34.466, 971.264] | 0.035 | 43 | 0.097 |
| government_control_belief_vaccine_rollout_2021 | bivariate_misaligned_expert_index | z_misaligned_migration_index | 0.150 | [0.039, 0.261] | 0.008 | 9 | 0.402 |
| government_control_belief_vaccine_rollout_2021 | bivariate_misaligned_information_index | z_misaligned_information_index | 0.125 | [0.062, 0.189] | 0.000 | 9 | 0.562 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_misaligned_expert_index | z_misaligned_migration_index | -0.018 | [-0.108, 0.072] | 0.695 | 9 | -0.090 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_misaligned_information_index | z_misaligned_information_index | 0.005 | [-0.066, 0.076] | 0.885 | 9 | -0.135 |
| mask_compliance_outside_acute_2020 | compact_gap_x_expert | z_centralization_gap | -0.194 | [-0.274, -0.113] | 0.000 | 19 | 0.722 |
| mask_compliance_outside_acute_2020 | compact_gap_x_expert | z_centralization_gap:z_expert_epistemic_trust | 0.129 | [0.067, 0.191] | 0.000 | 19 | 0.722 |
| mask_compliance_outside_acute_2020 | compact_gap_x_expert | z_expert_epistemic_trust | -0.146 | [-0.282, -0.010] | 0.036 | 19 | 0.722 |
| mask_compliance_outside_acute_2020 | compact_gap_x_information | z_centralization_gap | -0.092 | [-0.348, 0.163] | 0.479 | 19 | 0.461 |
| mask_compliance_outside_acute_2020 | compact_gap_x_information | z_centralization_gap:z_information_trust | 0.094 | [0.002, 0.186] | 0.046 | 19 | 0.461 |
| mask_compliance_outside_acute_2020 | compact_gap_x_information | z_information_trust | 0.055 | [-0.161, 0.272] | 0.616 | 19 | 0.461 |
| mask_compliance_outside_acute_2020 | compact_misaligned_expert_index | z_misaligned_migration_index | -0.052 | [-0.173, 0.069] | 0.397 | 19 | 0.280 |
| mask_compliance_outside_acute_2020 | compact_misaligned_information_index | z_misaligned_information_index | -0.084 | [-0.187, 0.019] | 0.109 | 19 | 0.392 |
| mask_refusal_outside_acute_2020 | compact_gap_x_expert | z_centralization_gap | 0.181 | [0.104, 0.257] | 0.000 | 19 | 0.711 |
| mask_refusal_outside_acute_2020 | compact_gap_x_expert | z_centralization_gap:z_expert_epistemic_trust | -0.109 | [-0.167, -0.051] | 0.000 | 19 | 0.711 |
| mask_refusal_outside_acute_2020 | compact_gap_x_expert | z_expert_epistemic_trust | 0.140 | [0.007, 0.274] | 0.040 | 19 | 0.711 |
| mask_refusal_outside_acute_2020 | compact_gap_x_information | z_centralization_gap | 0.096 | [-0.140, 0.332] | 0.427 | 19 | 0.480 |
| mask_refusal_outside_acute_2020 | compact_gap_x_information | z_centralization_gap:z_information_trust | -0.086 | [-0.170, -0.002] | 0.046 | 19 | 0.480 |
| mask_refusal_outside_acute_2020 | compact_gap_x_information | z_information_trust | -0.046 | [-0.244, 0.153] | 0.653 | 19 | 0.480 |
| mask_refusal_outside_acute_2020 | compact_misaligned_expert_index | z_misaligned_migration_index | 0.056 | [-0.053, 0.165] | 0.315 | 19 | 0.308 |
| mask_refusal_outside_acute_2020 | compact_misaligned_information_index | z_misaligned_information_index | 0.084 | [-0.010, 0.177] | 0.080 | 19 | 0.422 |
| non_vaccinated_share | full_gap_x_expert | z_centralization_gap | 3.102 | [-4.030, 10.234] | 0.394 | 57 | 0.405 |
| non_vaccinated_share | full_gap_x_expert | z_centralization_gap:z_expert_epistemic_trust | -0.156 | [-5.526, 5.214] | 0.955 | 57 | 0.405 |
| non_vaccinated_share | full_gap_x_expert | z_expert_epistemic_trust | -6.233 | [-12.991, 0.525] | 0.071 | 57 | 0.405 |
| non_vaccinated_share | full_gap_x_information | z_centralization_gap | 7.088 | [-0.215, 14.391] | 0.057 | 57 | 0.354 |
| non_vaccinated_share | full_gap_x_information | z_centralization_gap:z_information_trust | 0.861 | [-3.513, 5.235] | 0.700 | 57 | 0.354 |
| non_vaccinated_share | full_gap_x_information | z_information_trust | 0.167 | [-8.469, 8.803] | 0.970 | 57 | 0.354 |
| non_vaccinated_share | full_misaligned_expert_index | z_misaligned_migration_index | 8.194 | [4.830, 11.557] | 0.000 | 57 | 0.420 |
| non_vaccinated_share | full_misaligned_information_index | z_misaligned_information_index | 7.346 | [3.519, 11.173] | 0.000 | 57 | 0.365 |
| recovery_deaths_per_million | full_gap_x_expert | z_centralization_gap | 65.125 | [-52.018, 182.268] | 0.276 | 57 | 0.518 |
| recovery_deaths_per_million | full_gap_x_expert | z_centralization_gap:z_expert_epistemic_trust | 9.154 | [-54.614, 72.921] | 0.778 | 57 | 0.518 |
| recovery_deaths_per_million | full_gap_x_expert | z_expert_epistemic_trust | 3.586 | [-103.244, 110.416] | 0.948 | 57 | 0.518 |
| recovery_deaths_per_million | full_gap_x_information | z_centralization_gap | -8.038 | [-179.688, 163.612] | 0.927 | 57 | 0.544 |
| recovery_deaths_per_million | full_gap_x_information | z_centralization_gap:z_information_trust | 34.844 | [-23.542, 93.231] | 0.242 | 57 | 0.544 |
| recovery_deaths_per_million | full_gap_x_information | z_information_trust | -81.511 | [-296.463, 133.441] | 0.457 | 57 | 0.544 |
| recovery_deaths_per_million | full_misaligned_expert_index | z_misaligned_migration_index | 58.534 | [3.643, 113.424] | 0.037 | 57 | 0.533 |
| recovery_deaths_per_million | full_misaligned_information_index | z_misaligned_information_index | 78.154 | [10.370, 145.937] | 0.024 | 57 | 0.548 |
| vaccination_rate | full_gap_x_expert | z_centralization_gap | -3.102 | [-10.234, 4.030] | 0.394 | 57 | 0.405 |
| vaccination_rate | full_gap_x_expert | z_centralization_gap:z_expert_epistemic_trust | 0.156 | [-5.214, 5.526] | 0.955 | 57 | 0.405 |
| vaccination_rate | full_gap_x_expert | z_expert_epistemic_trust | 6.233 | [-0.525, 12.991] | 0.071 | 57 | 0.405 |
| vaccination_rate | full_gap_x_information | z_centralization_gap | -7.088 | [-14.391, 0.215] | 0.057 | 57 | 0.354 |
| vaccination_rate | full_gap_x_information | z_centralization_gap:z_information_trust | -0.861 | [-5.235, 3.513] | 0.700 | 57 | 0.354 |
| vaccination_rate | full_gap_x_information | z_information_trust | -0.167 | [-8.803, 8.469] | 0.970 | 57 | 0.354 |
| vaccination_rate | full_misaligned_expert_index | z_misaligned_migration_index | -8.194 | [-11.557, -4.830] | 0.000 | 57 | 0.420 |
| vaccination_rate | full_misaligned_information_index | z_misaligned_information_index | -7.346 | [-11.173, -3.519] | 0.000 | 57 | 0.365 |

## Interpretation

The mechanism hypothesis is strengthened if centralization-gap effects are larger where expert or information trust is weak, or if misaligned migration indices predict worse outcomes consistently.