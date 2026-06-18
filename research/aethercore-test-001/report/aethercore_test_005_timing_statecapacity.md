# AetherCore Test 005: WVS Timing and State-Capacity Controls

## Purpose

This pass tests whether the trust-taxonomy results survive pre-pandemic state-capacity controls and whether WVS fieldwork timing changes the signal.

State capacity uses 2019 Worldwide Governance Indicators from the World Bank WGI bulk CSV.

## Fieldwork Timing Counts

| Timing group | Countries |
|---|---:|
| pre_covid | 38 |
| pandemic_overlap | 28 |

## Main Coefficients

| Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |
|---|---|---:|---:|---:|---:|---:|---:|
| acute_deaths_per_million | central_gap_state_capacity | z_centralization_gap | -637.652 | [-1479.463, 204.159] | 0.138 | 57 | 0.402 |
| acute_deaths_per_million | central_gap_state_capacity | z_centralized_institutional_trust | -1164.856 | [-2142.182, -187.530] | 0.019 | 57 | 0.402 |
| acute_deaths_per_million | central_gap_state_capacity | z_state_capacity_index_2019 | 61.526 | [-579.321, 702.374] | 0.851 | 57 | 0.402 |
| acute_deaths_per_million | central_plus_region | z_centralized_institutional_trust | -402.917 | [-821.198, 15.364] | 0.059 | 57 | 0.469 |
| acute_deaths_per_million | central_plus_state_capacity | z_centralized_institutional_trust | -592.864 | [-922.869, -262.860] | 0.000 | 57 | 0.353 |
| acute_deaths_per_million | central_plus_state_capacity | z_state_capacity_index_2019 | -159.509 | [-693.259, 374.242] | 0.558 | 57 | 0.353 |
| acute_deaths_per_million | central_x_wvs_timing | z_centralized_institutional_trust | -867.661 | [-1356.008, -379.313] | 0.000 | 57 | 0.417 |
| acute_deaths_per_million | central_x_wvs_timing | z_centralized_institutional_trust:wvs_post2019 | 615.957 | [90.840, 1141.073] | 0.022 | 57 | 0.417 |
| acute_deaths_per_million | gap_plus_region | z_centralization_gap | 202.421 | [-86.056, 490.898] | 0.169 | 57 | 0.422 |
| acute_deaths_per_million | gap_plus_state_capacity | z_centralization_gap | 401.637 | [170.815, 632.458] | 0.001 | 57 | 0.208 |
| acute_deaths_per_million | gap_plus_state_capacity | z_state_capacity_index_2019 | -388.638 | [-936.705, 159.429] | 0.165 | 57 | 0.208 |
| acute_deaths_per_million | gap_x_wvs_timing | z_centralization_gap | 551.191 | [133.905, 968.476] | 0.010 | 57 | 0.215 |
| acute_deaths_per_million | gap_x_wvs_timing | z_centralization_gap:wvs_post2019 | -319.509 | [-777.759, 138.740] | 0.172 | 57 | 0.215 |
| deaths_per_million | central_gap_state_capacity | z_centralization_gap | -665.679 | [-1541.032, 209.675] | 0.136 | 57 | 0.497 |
| deaths_per_million | central_gap_state_capacity | z_centralized_institutional_trust | -1267.644 | [-2266.480, -268.808] | 0.013 | 57 | 0.497 |
| deaths_per_million | central_gap_state_capacity | z_state_capacity_index_2019 | 150.160 | [-552.300, 852.621] | 0.675 | 57 | 0.497 |
| deaths_per_million | central_plus_region | z_centralized_institutional_trust | -442.343 | [-899.654, 14.967] | 0.058 | 57 | 0.540 |
| deaths_per_million | central_plus_state_capacity | z_centralized_institutional_trust | -670.512 | [-1014.681, -326.343] | 0.000 | 57 | 0.459 |
| deaths_per_million | central_plus_state_capacity | z_state_capacity_index_2019 | -80.590 | [-683.094, 521.914] | 0.793 | 57 | 0.459 |
| deaths_per_million | central_x_wvs_timing | z_centralized_institutional_trust | -942.683 | [-1438.851, -446.516] | 0.000 | 57 | 0.520 |
| deaths_per_million | central_x_wvs_timing | z_centralized_institutional_trust:wvs_post2019 | 654.391 | [96.898, 1211.884] | 0.021 | 57 | 0.520 |
| deaths_per_million | gap_plus_region | z_centralization_gap | 212.561 | [-124.904, 550.026] | 0.217 | 57 | 0.498 |
| deaths_per_million | gap_plus_state_capacity | z_centralization_gap | 465.318 | [202.706, 727.930] | 0.001 | 57 | 0.332 |
| deaths_per_million | gap_plus_state_capacity | z_state_capacity_index_2019 | -339.728 | [-954.585, 275.129] | 0.279 | 57 | 0.332 |
| deaths_per_million | gap_x_wvs_timing | z_centralization_gap | 648.645 | [184.472, 1112.818] | 0.006 | 57 | 0.366 |
| deaths_per_million | gap_x_wvs_timing | z_centralization_gap:wvs_post2019 | -392.480 | [-911.522, 126.563] | 0.138 | 57 | 0.366 |
| excess_mortality | central_gap_state_capacity | z_centralization_gap | -158.282 | [-1138.017, 821.454] | 0.752 | 43 | 0.447 |
| excess_mortality | central_gap_state_capacity | z_centralized_institutional_trust | -928.904 | [-1992.595, 134.786] | 0.087 | 43 | 0.447 |
| excess_mortality | central_gap_state_capacity | z_state_capacity_index_2019 | -2579.392 | [-4367.519, -791.265] | 0.005 | 43 | 0.447 |
| excess_mortality | central_plus_region | z_centralized_institutional_trust | -155.655 | [-1296.455, 985.144] | 0.789 | 43 | 0.343 |
| excess_mortality | central_plus_state_capacity | z_centralized_institutional_trust | -792.290 | [-1316.387, -268.193] | 0.003 | 43 | 0.461 |
| excess_mortality | central_plus_state_capacity | z_state_capacity_index_2019 | -2623.474 | [-4299.032, -947.916] | 0.002 | 43 | 0.461 |
| excess_mortality | central_x_wvs_timing | z_centralized_institutional_trust | -684.809 | [-1491.707, 122.090] | 0.096 | 43 | 0.157 |
| excess_mortality | central_x_wvs_timing | z_centralized_institutional_trust:wvs_post2019 | 376.747 | [-485.871, 1239.366] | 0.392 | 43 | 0.157 |
| excess_mortality | gap_plus_region | z_centralization_gap | -30.392 | [-875.381, 814.597] | 0.944 | 43 | 0.340 |
| excess_mortality | gap_plus_state_capacity | z_centralization_gap | 641.906 | [150.077, 1133.734] | 0.011 | 43 | 0.400 |
| excess_mortality | gap_plus_state_capacity | z_state_capacity_index_2019 | -2727.373 | [-4468.386, -986.361] | 0.002 | 43 | 0.400 |
| excess_mortality | gap_x_wvs_timing | z_centralization_gap | 355.816 | [-512.442, 1224.073] | 0.422 | 43 | 0.108 |
| excess_mortality | gap_x_wvs_timing | z_centralization_gap:wvs_post2019 | -22.809 | [-968.127, 922.508] | 0.962 | 43 | 0.108 |
| non_vaccinated_share | central_gap_state_capacity | z_centralization_gap | 17.547 | [7.727, 27.368] | 0.000 | 57 | 0.438 |
| non_vaccinated_share | central_gap_state_capacity | z_centralized_institutional_trust | 11.439 | [1.845, 21.033] | 0.019 | 57 | 0.438 |
| non_vaccinated_share | central_gap_state_capacity | z_state_capacity_index_2019 | -7.588 | [-15.732, 0.557] | 0.068 | 57 | 0.438 |
| non_vaccinated_share | central_plus_region | z_centralized_institutional_trust | -6.507 | [-12.462, -0.552] | 0.032 | 57 | 0.639 |
| non_vaccinated_share | central_plus_state_capacity | z_centralized_institutional_trust | -4.301 | [-8.561, -0.041] | 0.048 | 57 | 0.271 |
| non_vaccinated_share | central_plus_state_capacity | z_state_capacity_index_2019 | -1.505 | [-10.181, 7.170] | 0.734 | 57 | 0.271 |
| non_vaccinated_share | central_x_wvs_timing | z_centralized_institutional_trust | -5.097 | [-12.133, 1.939] | 0.156 | 57 | 0.301 |
| non_vaccinated_share | central_x_wvs_timing | z_centralized_institutional_trust:wvs_post2019 | -0.667 | [-14.516, 13.181] | 0.925 | 57 | 0.301 |
| non_vaccinated_share | gap_plus_region | z_centralization_gap | 6.522 | [0.818, 12.226] | 0.025 | 57 | 0.644 |
| non_vaccinated_share | gap_plus_state_capacity | z_centralization_gap | 7.341 | [3.520, 11.162] | 0.000 | 57 | 0.374 |
| non_vaccinated_share | gap_plus_state_capacity | z_state_capacity_index_2019 | -3.167 | [-11.555, 5.220] | 0.459 | 57 | 0.374 |
| non_vaccinated_share | gap_x_wvs_timing | z_centralization_gap | 7.081 | [0.012, 14.150] | 0.050 | 57 | 0.381 |
| non_vaccinated_share | gap_x_wvs_timing | z_centralization_gap:wvs_post2019 | 0.773 | [-9.348, 10.893] | 0.881 | 57 | 0.381 |
| recovery_deaths_per_million | central_gap_state_capacity | z_centralization_gap | -28.027 | [-217.943, 161.890] | 0.772 | 57 | 0.539 |
| recovery_deaths_per_million | central_gap_state_capacity | z_centralized_institutional_trust | -102.788 | [-282.058, 76.482] | 0.261 | 57 | 0.539 |
| recovery_deaths_per_million | central_gap_state_capacity | z_state_capacity_index_2019 | 88.634 | [-51.158, 228.426] | 0.214 | 57 | 0.539 |
| recovery_deaths_per_million | central_plus_region | z_centralized_institutional_trust | -39.426 | [-142.892, 64.040] | 0.455 | 57 | 0.535 |
| recovery_deaths_per_million | central_plus_state_capacity | z_centralized_institutional_trust | -77.648 | [-132.229, -23.066] | 0.005 | 57 | 0.548 |
| recovery_deaths_per_million | central_plus_state_capacity | z_state_capacity_index_2019 | 78.919 | [-62.580, 220.417] | 0.274 | 57 | 0.548 |
| recovery_deaths_per_million | central_x_wvs_timing | z_centralized_institutional_trust | -75.023 | [-156.788, 6.742] | 0.072 | 57 | 0.545 |
| recovery_deaths_per_million | central_x_wvs_timing | z_centralized_institutional_trust:wvs_post2019 | 38.434 | [-74.748, 151.616] | 0.506 | 57 | 0.545 |
| recovery_deaths_per_million | gap_plus_region | z_centralization_gap | 10.140 | [-71.379, 91.658] | 0.807 | 57 | 0.530 |
| recovery_deaths_per_million | gap_plus_state_capacity | z_centralization_gap | 63.682 | [0.463, 126.900] | 0.048 | 57 | 0.533 |
| recovery_deaths_per_million | gap_plus_state_capacity | z_state_capacity_index_2019 | 48.911 | [-94.059, 191.880] | 0.503 | 57 | 0.533 |
| recovery_deaths_per_million | gap_x_wvs_timing | z_centralization_gap | 97.454 | [8.383, 186.525] | 0.032 | 57 | 0.557 |
| recovery_deaths_per_million | gap_x_wvs_timing | z_centralization_gap:wvs_post2019 | -72.971 | [-200.613, 54.672] | 0.263 | 57 | 0.557 |
| vaccination_rate | central_gap_state_capacity | z_centralization_gap | -17.547 | [-27.368, -7.727] | 0.000 | 57 | 0.438 |
| vaccination_rate | central_gap_state_capacity | z_centralized_institutional_trust | -11.439 | [-21.033, -1.845] | 0.019 | 57 | 0.438 |
| vaccination_rate | central_gap_state_capacity | z_state_capacity_index_2019 | 7.588 | [-0.557, 15.732] | 0.068 | 57 | 0.438 |
| vaccination_rate | central_plus_region | z_centralized_institutional_trust | 6.507 | [0.552, 12.462] | 0.032 | 57 | 0.639 |
| vaccination_rate | central_plus_state_capacity | z_centralized_institutional_trust | 4.301 | [0.041, 8.561] | 0.048 | 57 | 0.271 |
| vaccination_rate | central_plus_state_capacity | z_state_capacity_index_2019 | 1.505 | [-7.170, 10.181] | 0.734 | 57 | 0.271 |
| vaccination_rate | central_x_wvs_timing | z_centralized_institutional_trust | 5.097 | [-1.939, 12.133] | 0.156 | 57 | 0.301 |
| vaccination_rate | central_x_wvs_timing | z_centralized_institutional_trust:wvs_post2019 | 0.667 | [-13.181, 14.516] | 0.925 | 57 | 0.301 |
| vaccination_rate | gap_plus_region | z_centralization_gap | -6.522 | [-12.226, -0.818] | 0.025 | 57 | 0.644 |
| vaccination_rate | gap_plus_state_capacity | z_centralization_gap | -7.341 | [-11.162, -3.520] | 0.000 | 57 | 0.374 |
| vaccination_rate | gap_plus_state_capacity | z_state_capacity_index_2019 | 3.167 | [-5.220, 11.555] | 0.459 | 57 | 0.374 |
| vaccination_rate | gap_x_wvs_timing | z_centralization_gap | -7.081 | [-14.150, -0.012] | 0.050 | 57 | 0.381 |
| vaccination_rate | gap_x_wvs_timing | z_centralization_gap:wvs_post2019 | -0.773 | [-10.893, 9.348] | 0.881 | 57 | 0.381 |

## Interpretation

If central trust and centralization gap remain meaningful after WGI controls, the result is less likely to be only state capacity. If timing interactions are large, WVS timing may be contaminating predictor direction.