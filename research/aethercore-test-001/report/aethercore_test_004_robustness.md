# AetherCore Test 004: Robustness and Influence Checks

## Purpose

This pass checks whether the Test 003 central-institutional-trust and centralization-gap signals survive alternative outcome transformations, robust regression, and leave-one-country-out influence checks.

## Robustness Coefficients

| Outcome | Transform | Model | Term | Coef | 95% CI | p | n |
|---|---|---|---:|---:|---:|---:|---:|
| acute_deaths_per_million | raw | gap_full_controls | z_centralization_gap | 401.650 | [180.502, 622.797] | 0.000 | 57 |
| acute_deaths_per_million | robust_rlm_huber | gap_full_controls | z_centralization_gap | 348.805 | [98.618, 598.993] | 0.006 | 57 |
| acute_deaths_per_million | raw | central_full_controls | z_centralized_institutional_trust | -610.875 | [-946.229, -275.522] | 0.000 | 57 |
| acute_deaths_per_million | raw | taxonomy_full_controls | z_centralized_institutional_trust | -655.942 | [-1143.436, -168.447] | 0.008 | 57 |
| acute_deaths_per_million | robust_rlm_huber | central_full_controls | z_centralized_institutional_trust | -527.315 | [-766.035, -288.596] | 0.000 | 57 |
| acute_deaths_per_million | robust_rlm_huber | taxonomy_full_controls | z_centralized_institutional_trust | -590.208 | [-1053.842, -126.574] | 0.013 | 57 |
| deaths_per_million | raw | gap_full_controls | z_centralization_gap | 465.330 | [211.679, 718.980] | 0.000 | 57 |
| deaths_per_million | robust_rlm_huber | gap_full_controls | z_centralization_gap | 432.389 | [134.626, 730.151] | 0.004 | 57 |
| deaths_per_million | raw | central_full_controls | z_centralized_institutional_trust | -679.612 | [-1025.524, -333.700] | 0.000 | 57 |
| deaths_per_million | raw | taxonomy_full_controls | z_centralized_institutional_trust | -684.713 | [-1222.016, -147.409] | 0.013 | 57 |
| deaths_per_million | robust_rlm_huber | central_full_controls | z_centralized_institutional_trust | -614.050 | [-879.888, -348.212] | 0.000 | 57 |
| deaths_per_million | robust_rlm_huber | taxonomy_full_controls | z_centralized_institutional_trust | -621.830 | [-1141.117, -102.542] | 0.019 | 57 |
| excess_mortality | raw | gap_full_controls | z_centralization_gap | 390.860 | [-42.003, 823.724] | 0.077 | 43 |
| excess_mortality | robust_rlm_huber | gap_full_controls | z_centralization_gap | 357.557 | [-176.659, 891.774] | 0.190 | 43 |
| excess_mortality | raw | central_full_controls | z_centralized_institutional_trust | -649.104 | [-1168.392, -129.817] | 0.014 | 43 |
| excess_mortality | raw | taxonomy_full_controls | z_centralized_institutional_trust | -578.800 | [-1818.276, 660.676] | 0.360 | 43 |
| excess_mortality | robust_rlm_huber | central_full_controls | z_centralized_institutional_trust | -665.995 | [-1118.953, -213.036] | 0.004 | 43 |
| excess_mortality | robust_rlm_huber | taxonomy_full_controls | z_centralized_institutional_trust | -796.097 | [-1841.457, 249.263] | 0.136 | 43 |
| log1p_acute_deaths_per_million | log1p | gap_full_controls | z_centralization_gap | 0.659 | [0.184, 1.133] | 0.007 | 57 |
| log1p_acute_deaths_per_million | log1p | central_full_controls | z_centralized_institutional_trust | -0.825 | [-1.273, -0.377] | 0.000 | 57 |
| log1p_acute_deaths_per_million | log1p | taxonomy_full_controls | z_centralized_institutional_trust | -0.848 | [-1.768, 0.072] | 0.071 | 57 |
| log1p_deaths_per_million | log1p | gap_full_controls | z_centralization_gap | 0.511 | [0.176, 0.846] | 0.003 | 57 |
| log1p_deaths_per_million | log1p | central_full_controls | z_centralized_institutional_trust | -0.615 | [-0.913, -0.318] | 0.000 | 57 |
| log1p_deaths_per_million | log1p | taxonomy_full_controls | z_centralized_institutional_trust | -0.579 | [-1.200, 0.042] | 0.068 | 57 |
| log1p_excess_mortality | log1p | gap_full_controls | z_centralization_gap | 0.116 | [-0.032, 0.265] | 0.125 | 42 |
| log1p_excess_mortality | log1p | central_full_controls | z_centralized_institutional_trust | -0.212 | [-0.365, -0.058] | 0.007 | 42 |
| log1p_excess_mortality | log1p | taxonomy_full_controls | z_centralized_institutional_trust | -0.241 | [-0.684, 0.202] | 0.286 | 42 |
| log1p_recovery_deaths_per_million | log1p | gap_full_controls | z_centralization_gap | 0.431 | [0.057, 0.804] | 0.024 | 57 |
| log1p_recovery_deaths_per_million | log1p | central_full_controls | z_centralized_institutional_trust | -0.497 | [-0.815, -0.180] | 0.002 | 57 |
| log1p_recovery_deaths_per_million | log1p | taxonomy_full_controls | z_centralized_institutional_trust | -0.210 | [-0.867, 0.447] | 0.531 | 57 |
| rank_acute_deaths_per_million | rank_percentile | gap_full_controls | z_centralization_gap | 0.111 | [0.047, 0.175] | 0.001 | 57 |
| rank_acute_deaths_per_million | rank_percentile | central_full_controls | z_centralized_institutional_trust | -0.148 | [-0.215, -0.081] | 0.000 | 57 |
| rank_acute_deaths_per_million | rank_percentile | taxonomy_full_controls | z_centralized_institutional_trust | -0.147 | [-0.285, -0.009] | 0.037 | 57 |
| rank_deaths_per_million | rank_percentile | gap_full_controls | z_centralization_gap | 0.103 | [0.044, 0.161] | 0.001 | 57 |
| rank_deaths_per_million | rank_percentile | central_full_controls | z_centralized_institutional_trust | -0.132 | [-0.187, -0.078] | 0.000 | 57 |
| rank_deaths_per_million | rank_percentile | taxonomy_full_controls | z_centralized_institutional_trust | -0.125 | [-0.243, -0.007] | 0.038 | 57 |
| rank_excess_mortality | rank_percentile | gap_full_controls | z_centralization_gap | 0.071 | [0.003, 0.139] | 0.039 | 43 |
| rank_excess_mortality | rank_percentile | central_full_controls | z_centralized_institutional_trust | -0.123 | [-0.201, -0.045] | 0.002 | 43 |
| rank_excess_mortality | rank_percentile | taxonomy_full_controls | z_centralized_institutional_trust | -0.160 | [-0.374, 0.054] | 0.143 | 43 |
| rank_recovery_deaths_per_million | rank_percentile | gap_full_controls | z_centralization_gap | 0.067 | [0.013, 0.120] | 0.015 | 57 |
| rank_recovery_deaths_per_million | rank_percentile | central_full_controls | z_centralized_institutional_trust | -0.073 | [-0.116, -0.030] | 0.001 | 57 |
| rank_recovery_deaths_per_million | rank_percentile | taxonomy_full_controls | z_centralized_institutional_trust | -0.049 | [-0.161, 0.063] | 0.394 | 57 |
| recovery_deaths_per_million | raw | gap_full_controls | z_centralization_gap | 63.680 | [1.392, 125.968] | 0.045 | 57 |
| recovery_deaths_per_million | robust_rlm_huber | gap_full_controls | z_centralization_gap | 69.887 | [20.368, 119.406] | 0.006 | 57 |
| recovery_deaths_per_million | raw | central_full_controls | z_centralized_institutional_trust | -68.737 | [-124.746, -12.727] | 0.016 | 57 |
| recovery_deaths_per_million | raw | taxonomy_full_controls | z_centralized_institutional_trust | -28.771 | [-221.737, 164.195] | 0.770 | 57 |
| recovery_deaths_per_million | robust_rlm_huber | central_full_controls | z_centralized_institutional_trust | -56.823 | [-108.252, -5.394] | 0.030 | 57 |
| recovery_deaths_per_million | robust_rlm_huber | taxonomy_full_controls | z_centralized_institutional_trust | -56.301 | [-156.587, 43.985] | 0.271 | 57 |
| winsor_acute_deaths_per_million | winsor_5_95 | gap_full_controls | z_centralization_gap | 369.190 | [169.396, 568.984] | 0.000 | 57 |
| winsor_acute_deaths_per_million | winsor_5_95 | central_full_controls | z_centralized_institutional_trust | -508.441 | [-724.998, -291.885] | 0.000 | 57 |
| winsor_acute_deaths_per_million | winsor_5_95 | taxonomy_full_controls | z_centralized_institutional_trust | -569.401 | [-1000.762, -138.040] | 0.010 | 57 |
| winsor_deaths_per_million | winsor_5_95 | gap_full_controls | z_centralization_gap | 433.548 | [200.281, 666.815] | 0.000 | 57 |
| winsor_deaths_per_million | winsor_5_95 | central_full_controls | z_centralized_institutional_trust | -583.704 | [-818.687, -348.720] | 0.000 | 57 |
| winsor_deaths_per_million | winsor_5_95 | taxonomy_full_controls | z_centralized_institutional_trust | -601.011 | [-1096.674, -105.349] | 0.017 | 57 |
| winsor_excess_mortality | winsor_5_95 | gap_full_controls | z_centralization_gap | 393.616 | [20.494, 766.738] | 0.039 | 43 |
| winsor_excess_mortality | winsor_5_95 | central_full_controls | z_centralized_institutional_trust | -652.550 | [-1096.612, -208.488] | 0.004 | 43 |
| winsor_excess_mortality | winsor_5_95 | taxonomy_full_controls | z_centralized_institutional_trust | -681.617 | [-1767.005, 403.770] | 0.218 | 43 |
| winsor_recovery_deaths_per_million | winsor_5_95 | gap_full_controls | z_centralization_gap | 60.562 | [6.413, 114.711] | 0.028 | 57 |
| winsor_recovery_deaths_per_million | winsor_5_95 | central_full_controls | z_centralized_institutional_trust | -54.089 | [-97.898, -10.280] | 0.016 | 57 |
| winsor_recovery_deaths_per_million | winsor_5_95 | taxonomy_full_controls | z_centralized_institutional_trust | -50.293 | [-180.554, 79.968] | 0.449 | 57 |

## Leave-One-Out Summary

| Outcome | Model | Term | Min Coef | Median Coef | Max Coef | Sign Flips |
|---|---|---:|---:|---:|---:|---:|
| acute_deaths_per_million | central_full_controls | z_centralized_institutional_trust | -658.969 | -612.703 | -483.282 | 0 |
| acute_deaths_per_million | gap_full_controls | z_centralization_gap | 356.049 | 401.395 | 465.512 | 0 |
| deaths_per_million | central_full_controls | z_centralized_institutional_trust | -734.677 | -681.166 | -550.962 | 0 |
| deaths_per_million | gap_full_controls | z_centralization_gap | 418.483 | 464.712 | 536.912 | 0 |
| recovery_deaths_per_million | central_full_controls | z_centralized_institutional_trust | -76.399 | -68.703 | -54.634 | 0 |
| recovery_deaths_per_million | gap_full_controls | z_centralization_gap | 53.481 | 63.475 | 82.898 | 0 |

## Interpretation

The signal is more credible if coefficient signs remain stable across transformations and leave-one-out runs. Sign flips or large swings indicate sensitivity to influential countries.