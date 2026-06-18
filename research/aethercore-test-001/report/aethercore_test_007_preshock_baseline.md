# AetherCore Test 007: Strict Pre-Shock Trust Baseline

## Purpose

This pass reruns the main trust-topology models after excluding all countries whose WVS Wave 7 fieldwork occurred in 2020 or later. The goal is to test whether the central trust and centralization-gap findings survive when trust is measured before the COVID shock.

## Sample Counts

| Sample | Countries |
|---|---:|
| All WVS Wave 7 countries in merged data | 65 |
| Strict pre-shock WVS countries, fieldwork max <= 2019 | 38 |
| Pandemic-overlap WVS countries, fieldwork max >= 2020 | 27 |

## Main Interpretation

- Across comparable key-term models, the pre-shock coefficient kept the same direction as the all-Wave-7 coefficient in 100.0% of cases.
- Pre-shock key-term coefficients with p < 0.05 in the selected focus set: 16.
- Smaller sample size makes the pre-shock test harder to pass; p-values should be interpreted with more caution than coefficient direction and robustness across related outcomes.

## Key Coefficients

| Outcome | Sample | Model | Term | Coef | 95% CI | p | n | Adj. R2 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| acute_deaths_per_million | all_wave7 | central_full | z7_centralized_institutional_trust | -610.875 | [-946.229, -275.522] | 0.000 | 57 | 0.360 |
| acute_deaths_per_million | all_wave7 | central_gap_full | z7_centralization_gap | -611.237 | [-1333.860, 111.386] | 0.097 | 57 | 0.414 |
| acute_deaths_per_million | all_wave7 | central_gap_full | z7_centralized_institutional_trust | -1135.248 | [-1985.881, -284.614] | 0.009 | 57 | 0.414 |
| acute_deaths_per_million | all_wave7 | central_state | z7_centralized_institutional_trust | -592.864 | [-922.869, -262.860] | 0.000 | 57 | 0.353 |
| acute_deaths_per_million | all_wave7 | gap_full | z7_centralization_gap | 401.650 | [180.502, 622.797] | 0.000 | 57 | 0.190 |
| acute_deaths_per_million | all_wave7 | gap_state | z7_centralization_gap | 401.637 | [170.815, 632.458] | 0.001 | 57 | 0.208 |
| acute_deaths_per_million | all_wave7 | misaligned_expert_state | z7_misaligned_expert_index | 347.509 | [104.348, 590.671] | 0.005 | 57 | 0.178 |
| acute_deaths_per_million | all_wave7 | misaligned_information_state | z7_misaligned_information_index | 465.950 | [209.543, 722.356] | 0.000 | 57 | 0.235 |
| acute_deaths_per_million | all_wave7 | trust_alignment_state | z7_trust_alignment_index | -403.675 | [-673.047, -134.303] | 0.003 | 57 | 0.180 |
| acute_deaths_per_million | pre_shock_only | central_full | z7_centralized_institutional_trust | -818.213 | [-1363.302, -273.125] | 0.003 | 32 | 0.479 |
| acute_deaths_per_million | pre_shock_only | central_gap_full | z7_centralization_gap | -723.969 | [-1671.579, 223.640] | 0.134 | 32 | 0.556 |
| acute_deaths_per_million | pre_shock_only | central_gap_full | z7_centralized_institutional_trust | -1444.396 | [-2548.838, -339.954] | 0.010 | 32 | 0.556 |
| acute_deaths_per_million | pre_shock_only | central_state | z7_centralized_institutional_trust | -798.642 | [-1360.073, -237.211] | 0.005 | 32 | 0.463 |
| acute_deaths_per_million | pre_shock_only | gap_full | z7_centralization_gap | 502.975 | [50.271, 955.678] | 0.029 | 32 | 0.198 |
| acute_deaths_per_million | pre_shock_only | gap_state | z7_centralization_gap | 484.300 | [17.226, 951.375] | 0.042 | 32 | 0.195 |
| acute_deaths_per_million | pre_shock_only | misaligned_expert_state | z7_misaligned_expert_index | 472.949 | [-27.561, 973.459] | 0.064 | 32 | 0.179 |
| acute_deaths_per_million | pre_shock_only | misaligned_information_state | z7_misaligned_information_index | 577.463 | [65.677, 1089.249] | 0.027 | 32 | 0.242 |
| acute_deaths_per_million | pre_shock_only | trust_alignment_state | z7_trust_alignment_index | -421.684 | [-975.814, 132.446] | 0.136 | 32 | 0.117 |
| deaths_per_million | all_wave7 | central_full | z7_centralized_institutional_trust | -679.612 | [-1025.524, -333.700] | 0.000 | 57 | 0.469 |
| deaths_per_million | all_wave7 | central_gap_full | z7_centralization_gap | -601.211 | [-1368.521, 166.099] | 0.125 | 57 | 0.504 |
| deaths_per_million | all_wave7 | central_gap_full | z7_centralized_institutional_trust | -1195.383 | [-2080.343, -310.422] | 0.008 | 57 | 0.504 |
| deaths_per_million | all_wave7 | central_state | z7_centralized_institutional_trust | -670.512 | [-1014.681, -326.343] | 0.000 | 57 | 0.459 |
| deaths_per_million | all_wave7 | gap_full | z7_centralization_gap | 465.330 | [211.679, 718.980] | 0.000 | 57 | 0.327 |
| deaths_per_million | all_wave7 | gap_state | z7_centralization_gap | 465.318 | [202.706, 727.930] | 0.001 | 57 | 0.332 |
| deaths_per_million | all_wave7 | misaligned_expert_state | z7_misaligned_expert_index | 409.363 | [137.776, 680.949] | 0.003 | 57 | 0.306 |
| deaths_per_million | all_wave7 | misaligned_information_state | z7_misaligned_information_index | 546.378 | [262.418, 830.338] | 0.000 | 57 | 0.361 |
| deaths_per_million | all_wave7 | trust_alignment_state | z7_trust_alignment_index | -474.550 | [-772.651, -176.449] | 0.002 | 57 | 0.307 |
| deaths_per_million | pre_shock_only | central_full | z7_centralized_institutional_trust | -910.507 | [-1456.910, -364.104] | 0.001 | 32 | 0.575 |
| deaths_per_million | pre_shock_only | central_gap_full | z7_centralization_gap | -647.266 | [-1634.517, 339.984] | 0.199 | 32 | 0.618 |
| deaths_per_million | pre_shock_only | central_gap_full | z7_centralized_institutional_trust | -1470.347 | [-2619.263, -321.431] | 0.012 | 32 | 0.618 |
| deaths_per_million | pre_shock_only | central_state | z7_centralized_institutional_trust | -898.984 | [-1477.270, -320.697] | 0.002 | 32 | 0.558 |
| deaths_per_million | pre_shock_only | gap_full | z7_centralization_gap | 601.722 | [104.926, 1098.518] | 0.018 | 32 | 0.334 |
| deaths_per_million | pre_shock_only | gap_state | z7_centralization_gap | 585.726 | [73.291, 1098.161] | 0.025 | 32 | 0.323 |
| deaths_per_million | pre_shock_only | misaligned_expert_state | z7_misaligned_expert_index | 580.359 | [49.983, 1110.735] | 0.032 | 32 | 0.310 |
| deaths_per_million | pre_shock_only | misaligned_information_state | z7_misaligned_information_index | 689.792 | [134.806, 1244.777] | 0.015 | 32 | 0.370 |
| deaths_per_million | pre_shock_only | trust_alignment_state | z7_trust_alignment_index | -504.956 | [-1133.736, 123.823] | 0.115 | 32 | 0.234 |
| non_vaccinated_share | all_wave7 | central_full | z7_centralized_institutional_trust | -4.471 | [-8.789, -0.153] | 0.042 | 57 | 0.284 |
| non_vaccinated_share | all_wave7 | central_gap_full | z7_centralization_gap | 14.290 | [5.551, 23.028] | 0.001 | 57 | 0.408 |
| non_vaccinated_share | all_wave7 | central_gap_full | z7_centralized_institutional_trust | 7.788 | [-0.972, 16.547] | 0.081 | 57 | 0.408 |
| non_vaccinated_share | all_wave7 | central_state | z7_centralized_institutional_trust | -4.301 | [-8.561, -0.041] | 0.048 | 57 | 0.271 |
| non_vaccinated_share | all_wave7 | gap_full | z7_centralization_gap | 7.341 | [3.466, 11.217] | 0.000 | 57 | 0.378 |
| non_vaccinated_share | all_wave7 | gap_state | z7_centralization_gap | 7.341 | [3.520, 11.162] | 0.000 | 57 | 0.374 |
| non_vaccinated_share | all_wave7 | misaligned_expert_state | z7_misaligned_expert_index | 8.102 | [4.781, 11.423] | 0.000 | 57 | 0.410 |
| non_vaccinated_share | all_wave7 | misaligned_information_state | z7_misaligned_information_index | 7.255 | [3.546, 10.965] | 0.000 | 57 | 0.356 |
| non_vaccinated_share | all_wave7 | trust_alignment_state | z7_trust_alignment_index | -2.471 | [-7.582, 2.640] | 0.343 | 57 | 0.231 |
| non_vaccinated_share | pre_shock_only | central_full | z7_centralized_institutional_trust | -3.656 | [-11.496, 4.185] | 0.361 | 32 | 0.152 |
| non_vaccinated_share | pre_shock_only | central_gap_full | z7_centralization_gap | 8.486 | [-6.110, 23.082] | 0.254 | 32 | 0.190 |
| non_vaccinated_share | pre_shock_only | central_gap_full | z7_centralized_institutional_trust | 3.684 | [-10.662, 18.031] | 0.615 | 32 | 0.190 |
| non_vaccinated_share | pre_shock_only | central_state | z7_centralized_institutional_trust | -2.722 | [-10.283, 4.840] | 0.480 | 32 | 0.199 |
| non_vaccinated_share | pre_shock_only | gap_full | z7_centralization_gap | 5.356 | [-2.246, 12.959] | 0.167 | 32 | 0.210 |
| non_vaccinated_share | pre_shock_only | gap_state | z7_centralization_gap | 4.930 | [-2.175, 12.035] | 0.174 | 32 | 0.266 |
| non_vaccinated_share | pre_shock_only | misaligned_expert_state | z7_misaligned_expert_index | 7.496 | [1.256, 13.737] | 0.019 | 32 | 0.378 |
| non_vaccinated_share | pre_shock_only | misaligned_information_state | z7_misaligned_information_index | 5.336 | [-1.739, 12.412] | 0.139 | 32 | 0.271 |
| non_vaccinated_share | pre_shock_only | trust_alignment_state | z7_trust_alignment_index | -1.058 | [-8.772, 6.656] | 0.788 | 32 | 0.175 |
| recovery_deaths_per_million | all_wave7 | central_full | z7_centralized_institutional_trust | -68.737 | [-124.746, -12.727] | 0.016 | 57 | 0.544 |
| recovery_deaths_per_million | all_wave7 | central_gap_full | z7_centralization_gap | 10.026 | [-179.309, 199.362] | 0.917 | 57 | 0.534 |
| recovery_deaths_per_million | all_wave7 | central_gap_full | z7_centralized_institutional_trust | -60.135 | [-240.491, 120.221] | 0.513 | 57 | 0.534 |
| recovery_deaths_per_million | all_wave7 | central_state | z7_centralized_institutional_trust | -77.648 | [-132.229, -23.066] | 0.005 | 57 | 0.548 |
| recovery_deaths_per_million | all_wave7 | gap_full | z7_centralization_gap | 63.680 | [1.392, 125.968] | 0.045 | 57 | 0.537 |
| recovery_deaths_per_million | all_wave7 | gap_state | z7_centralization_gap | 63.682 | [0.463, 126.900] | 0.048 | 57 | 0.533 |
| recovery_deaths_per_million | all_wave7 | misaligned_expert_state | z7_misaligned_expert_index | 61.853 | [5.126, 118.580] | 0.033 | 57 | 0.532 |
| recovery_deaths_per_million | all_wave7 | misaligned_information_state | z7_misaligned_information_index | 80.429 | [12.678, 148.179] | 0.020 | 57 | 0.547 |
| recovery_deaths_per_million | all_wave7 | trust_alignment_state | z7_trust_alignment_index | -70.875 | [-174.513, 32.763] | 0.180 | 57 | 0.531 |
| recovery_deaths_per_million | pre_shock_only | central_full | z7_centralized_institutional_trust | -92.294 | [-202.498, 17.910] | 0.101 | 32 | 0.555 |
| recovery_deaths_per_million | pre_shock_only | central_gap_full | z7_centralization_gap | 76.703 | [-111.891, 265.297] | 0.425 | 32 | 0.547 |
| recovery_deaths_per_million | pre_shock_only | central_gap_full | z7_centralized_institutional_trust | -25.951 | [-210.155, 158.253] | 0.782 | 32 | 0.547 |
| recovery_deaths_per_million | pre_shock_only | central_state | z7_centralized_institutional_trust | -100.342 | [-217.343, 16.660] | 0.093 | 32 | 0.547 |
| recovery_deaths_per_million | pre_shock_only | gap_full | z7_centralization_gap | 98.747 | [-12.435, 209.930] | 0.082 | 32 | 0.565 |
| recovery_deaths_per_million | pre_shock_only | gap_state | z7_centralization_gap | 101.425 | [-12.475, 215.326] | 0.081 | 32 | 0.552 |
| recovery_deaths_per_million | pre_shock_only | misaligned_expert_state | z7_misaligned_expert_index | 107.410 | [3.381, 211.438] | 0.043 | 32 | 0.556 |
| recovery_deaths_per_million | pre_shock_only | misaligned_information_state | z7_misaligned_information_index | 112.329 | [-20.661, 245.319] | 0.098 | 32 | 0.559 |
| recovery_deaths_per_million | pre_shock_only | trust_alignment_state | z7_trust_alignment_index | -83.273 | [-288.165, 121.620] | 0.426 | 32 | 0.515 |
| vaccination_rate | all_wave7 | central_full | z7_centralized_institutional_trust | 4.471 | [0.153, 8.789] | 0.042 | 57 | 0.284 |
| vaccination_rate | all_wave7 | central_gap_full | z7_centralization_gap | -14.290 | [-23.028, -5.551] | 0.001 | 57 | 0.408 |
| vaccination_rate | all_wave7 | central_gap_full | z7_centralized_institutional_trust | -7.788 | [-16.547, 0.972] | 0.081 | 57 | 0.408 |
| vaccination_rate | all_wave7 | central_state | z7_centralized_institutional_trust | 4.301 | [0.041, 8.561] | 0.048 | 57 | 0.271 |
| vaccination_rate | all_wave7 | gap_full | z7_centralization_gap | -7.341 | [-11.217, -3.466] | 0.000 | 57 | 0.378 |
| vaccination_rate | all_wave7 | gap_state | z7_centralization_gap | -7.341 | [-11.162, -3.520] | 0.000 | 57 | 0.374 |
| vaccination_rate | all_wave7 | misaligned_expert_state | z7_misaligned_expert_index | -8.102 | [-11.423, -4.781] | 0.000 | 57 | 0.410 |
| vaccination_rate | all_wave7 | misaligned_information_state | z7_misaligned_information_index | -7.255 | [-10.965, -3.546] | 0.000 | 57 | 0.356 |
| vaccination_rate | all_wave7 | trust_alignment_state | z7_trust_alignment_index | 2.471 | [-2.640, 7.582] | 0.343 | 57 | 0.231 |
| vaccination_rate | pre_shock_only | central_full | z7_centralized_institutional_trust | 3.656 | [-4.185, 11.496] | 0.361 | 32 | 0.152 |
| vaccination_rate | pre_shock_only | central_gap_full | z7_centralization_gap | -8.486 | [-23.082, 6.110] | 0.254 | 32 | 0.190 |
| vaccination_rate | pre_shock_only | central_gap_full | z7_centralized_institutional_trust | -3.684 | [-18.031, 10.662] | 0.615 | 32 | 0.190 |
| vaccination_rate | pre_shock_only | central_state | z7_centralized_institutional_trust | 2.722 | [-4.840, 10.283] | 0.480 | 32 | 0.199 |
| vaccination_rate | pre_shock_only | gap_full | z7_centralization_gap | -5.356 | [-12.959, 2.246] | 0.167 | 32 | 0.210 |
| vaccination_rate | pre_shock_only | gap_state | z7_centralization_gap | -4.930 | [-12.035, 2.175] | 0.174 | 32 | 0.266 |
| vaccination_rate | pre_shock_only | misaligned_expert_state | z7_misaligned_expert_index | -7.496 | [-13.737, -1.256] | 0.019 | 32 | 0.378 |
| vaccination_rate | pre_shock_only | misaligned_information_state | z7_misaligned_information_index | -5.336 | [-12.412, 1.739] | 0.139 | 32 | 0.271 |
| vaccination_rate | pre_shock_only | trust_alignment_state | z7_trust_alignment_index | 1.058 | [-6.656, 8.772] | 0.788 | 32 | 0.175 |

## Comparison Table

| Outcome | Model | Term | Coef all | Coef pre | Same direction | p all | p pre | n all | n pre |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| acute_deaths_per_million | central_full | z7_centralized_institutional_trust | -610.875 | -818.213 | True | 0.000 | 0.003 | 57 | 32 |
| acute_deaths_per_million | central_gap_full | z7_centralization_gap | -611.237 | -723.969 | True | 0.097 | 0.134 | 57 | 32 |
| acute_deaths_per_million | central_gap_full | z7_centralized_institutional_trust | -1135.248 | -1444.396 | True | 0.009 | 0.010 | 57 | 32 |
| acute_deaths_per_million | central_state | z7_centralized_institutional_trust | -592.864 | -798.642 | True | 0.000 | 0.005 | 57 | 32 |
| acute_deaths_per_million | gap_full | z7_centralization_gap | 401.650 | 502.975 | True | 0.000 | 0.029 | 57 | 32 |
| acute_deaths_per_million | gap_state | z7_centralization_gap | 401.637 | 484.300 | True | 0.001 | 0.042 | 57 | 32 |
| acute_deaths_per_million | misaligned_expert_state | z7_misaligned_expert_index | 347.509 | 472.949 | True | 0.005 | 0.064 | 57 | 32 |
| acute_deaths_per_million | misaligned_information_state | z7_misaligned_information_index | 465.950 | 577.463 | True | 0.000 | 0.027 | 57 | 32 |
| acute_deaths_per_million | trust_alignment_state | z7_trust_alignment_index | -403.675 | -421.684 | True | 0.003 | 0.136 | 57 | 32 |
| deaths_per_million | central_full | z7_centralized_institutional_trust | -679.612 | -910.507 | True | 0.000 | 0.001 | 57 | 32 |
| deaths_per_million | central_gap_full | z7_centralization_gap | -601.211 | -647.266 | True | 0.125 | 0.199 | 57 | 32 |
| deaths_per_million | central_gap_full | z7_centralized_institutional_trust | -1195.383 | -1470.347 | True | 0.008 | 0.012 | 57 | 32 |
| deaths_per_million | central_state | z7_centralized_institutional_trust | -670.512 | -898.984 | True | 0.000 | 0.002 | 57 | 32 |
| deaths_per_million | gap_full | z7_centralization_gap | 465.330 | 601.722 | True | 0.000 | 0.018 | 57 | 32 |
| deaths_per_million | gap_state | z7_centralization_gap | 465.318 | 585.726 | True | 0.001 | 0.025 | 57 | 32 |
| deaths_per_million | misaligned_expert_state | z7_misaligned_expert_index | 409.363 | 580.359 | True | 0.003 | 0.032 | 57 | 32 |
| deaths_per_million | misaligned_information_state | z7_misaligned_information_index | 546.378 | 689.792 | True | 0.000 | 0.015 | 57 | 32 |
| deaths_per_million | trust_alignment_state | z7_trust_alignment_index | -474.550 | -504.956 | True | 0.002 | 0.115 | 57 | 32 |
| excess_mortality | central_full | z7_centralized_institutional_trust | -649.104 | -397.907 | True | 0.014 | 0.427 | 43 | 27 |
| excess_mortality | central_gap_full | z7_centralization_gap | -619.572 | -526.973 | True | 0.216 | 0.544 | 43 | 27 |
| excess_mortality | central_gap_full | z7_centralized_institutional_trust | -1193.282 | -823.618 | True | 0.029 | 0.374 | 43 | 27 |
| excess_mortality | central_state | z7_centralized_institutional_trust | -792.290 | -386.239 | True | 0.003 | 0.478 | 43 | 27 |
| excess_mortality | gap_full | z7_centralization_gap | 390.860 | 137.882 | True | 0.077 | 0.732 | 43 | 27 |
| excess_mortality | gap_state | z7_centralization_gap | 641.906 | 254.221 | True | 0.011 | 0.540 | 43 | 27 |
| excess_mortality | misaligned_expert_state | z7_misaligned_expert_index | 525.893 | 185.038 | True | 0.051 | 0.666 | 43 | 27 |
| excess_mortality | misaligned_information_state | z7_misaligned_information_index | 697.869 | 230.677 | True | 0.014 | 0.621 | 43 | 27 |
| excess_mortality | trust_alignment_state | z7_trust_alignment_index | -678.298 | -332.859 | True | 0.013 | 0.461 | 43 | 27 |
| non_vaccinated_share | central_full | z7_centralized_institutional_trust | -4.471 | -3.656 | True | 0.042 | 0.361 | 57 | 32 |
| non_vaccinated_share | central_gap_full | z7_centralization_gap | 14.290 | 8.486 | True | 0.001 | 0.254 | 57 | 32 |
| non_vaccinated_share | central_gap_full | z7_centralized_institutional_trust | 7.788 | 3.684 | True | 0.081 | 0.615 | 57 | 32 |
| non_vaccinated_share | central_state | z7_centralized_institutional_trust | -4.301 | -2.722 | True | 0.048 | 0.480 | 57 | 32 |
| non_vaccinated_share | gap_full | z7_centralization_gap | 7.341 | 5.356 | True | 0.000 | 0.167 | 57 | 32 |
| non_vaccinated_share | gap_state | z7_centralization_gap | 7.341 | 4.930 | True | 0.000 | 0.174 | 57 | 32 |
| non_vaccinated_share | misaligned_expert_state | z7_misaligned_expert_index | 8.102 | 7.496 | True | 0.000 | 0.019 | 57 | 32 |
| non_vaccinated_share | misaligned_information_state | z7_misaligned_information_index | 7.255 | 5.336 | True | 0.000 | 0.139 | 57 | 32 |
| non_vaccinated_share | trust_alignment_state | z7_trust_alignment_index | -2.471 | -1.058 | True | 0.343 | 0.788 | 57 | 32 |
| recovery_deaths_per_million | central_full | z7_centralized_institutional_trust | -68.737 | -92.294 | True | 0.016 | 0.101 | 57 | 32 |
| recovery_deaths_per_million | central_gap_full | z7_centralization_gap | 10.026 | 76.703 | True | 0.917 | 0.425 | 57 | 32 |
| recovery_deaths_per_million | central_gap_full | z7_centralized_institutional_trust | -60.135 | -25.951 | True | 0.513 | 0.782 | 57 | 32 |
| recovery_deaths_per_million | central_state | z7_centralized_institutional_trust | -77.648 | -100.342 | True | 0.005 | 0.093 | 57 | 32 |
| recovery_deaths_per_million | gap_full | z7_centralization_gap | 63.680 | 98.747 | True | 0.045 | 0.082 | 57 | 32 |
| recovery_deaths_per_million | gap_state | z7_centralization_gap | 63.682 | 101.425 | True | 0.048 | 0.081 | 57 | 32 |
| recovery_deaths_per_million | misaligned_expert_state | z7_misaligned_expert_index | 61.853 | 107.410 | True | 0.033 | 0.043 | 57 | 32 |
| recovery_deaths_per_million | misaligned_information_state | z7_misaligned_information_index | 80.429 | 112.329 | True | 0.020 | 0.098 | 57 | 32 |
| recovery_deaths_per_million | trust_alignment_state | z7_trust_alignment_index | -70.875 | -83.273 | True | 0.180 | 0.426 | 57 | 32 |
| vaccination_rate | central_full | z7_centralized_institutional_trust | 4.471 | 3.656 | True | 0.042 | 0.361 | 57 | 32 |
| vaccination_rate | central_gap_full | z7_centralization_gap | -14.290 | -8.486 | True | 0.001 | 0.254 | 57 | 32 |
| vaccination_rate | central_gap_full | z7_centralized_institutional_trust | -7.788 | -3.684 | True | 0.081 | 0.615 | 57 | 32 |
| vaccination_rate | central_state | z7_centralized_institutional_trust | 4.301 | 2.722 | True | 0.048 | 0.480 | 57 | 32 |
| vaccination_rate | gap_full | z7_centralization_gap | -7.341 | -5.356 | True | 0.000 | 0.167 | 57 | 32 |
| vaccination_rate | gap_state | z7_centralization_gap | -7.341 | -4.930 | True | 0.000 | 0.174 | 57 | 32 |
| vaccination_rate | misaligned_expert_state | z7_misaligned_expert_index | -8.102 | -7.496 | True | 0.000 | 0.019 | 57 | 32 |
| vaccination_rate | misaligned_information_state | z7_misaligned_information_index | -7.255 | -5.336 | True | 0.000 | 0.139 | 57 | 32 |
| vaccination_rate | trust_alignment_state | z7_trust_alignment_index | 2.471 | 1.058 | True | 0.343 | 0.788 | 57 | 32 |
| vaccination_rate_2021 | central_full | z7_centralized_institutional_trust | 3.226 | 2.508 | True | 0.151 | 0.544 | 57 | 32 |
| vaccination_rate_2021 | central_gap_full | z7_centralization_gap | -13.840 | -10.106 | True | 0.001 | 0.150 | 57 | 32 |
| vaccination_rate_2021 | central_gap_full | z7_centralized_institutional_trust | -8.647 | -6.233 | True | 0.044 | 0.354 | 57 | 32 |
| vaccination_rate_2021 | central_state | z7_centralized_institutional_trust | 3.192 | 1.793 | True | 0.156 | 0.674 | 57 | 32 |
| vaccination_rate_2021 | gap_full | z7_centralization_gap | -6.125 | -4.811 | True | 0.002 | 0.221 | 57 | 32 |
| vaccination_rate_2021 | gap_state | z7_centralization_gap | -6.125 | -4.495 | True | 0.002 | 0.246 | 57 | 32 |
| vaccination_rate_2021 | misaligned_expert_state | z7_misaligned_expert_index | -6.438 | -6.096 | True | 0.000 | 0.055 | 57 | 32 |
| vaccination_rate_2021 | misaligned_information_state | z7_misaligned_information_index | -5.742 | -4.450 | True | 0.005 | 0.260 | 57 | 32 |
| vaccination_rate_2021 | trust_alignment_state | z7_trust_alignment_index | 2.696 | 1.457 | True | 0.290 | 0.742 | 57 | 32 |

## What Would Weaken the AetherCore Trust-Alignment Claim?

The refined claim is weakened if the pre-shock-only subset reverses the central trust and centralization-gap directions, if vaccination/mortality associations disappear entirely, or if trust-alignment and misalignment indices add no information beyond material controls. It is strengthened if pre-shock-only coefficients preserve direction and remain meaningful despite the smaller sample.

## Caveats

- This pass still uses WVS Wave 7 only; it removes pandemic-overlap countries but does not add earlier WVS waves.
- Strict pre-shock filtering reduces sample size from 65 to 38 countries.
- Smaller samples reduce power and make confidence intervals wider.
- The analysis remains observational and country-level.