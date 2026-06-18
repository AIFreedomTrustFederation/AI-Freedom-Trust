# AetherCore Test 008: Post-Shock Trust Topology and Sphere of Fear Proxy

## Purpose

This pass asks whether post-shock trust observations show a measurable pattern consistent with the AetherCore Sphere of Fear model: contraction away from centralized institutions, migration toward decentralized trust channels, weakened expert/information trust, and worse crisis-coordination outcomes.

This is not a true longitudinal pre/post design. WVS Wave 7 does not provide the same countries measured both before and after COVID. The comparison is between countries whose WVS fieldwork ended before 2020 and countries whose WVS fieldwork occurred in 2020 or later.

## Operational Definition

`fear_trust_topology_index` is a trust-only proxy combining standardized institutional distrust, centralization gap, expert distrust, and information distrust.

`fear_misalignment_index` combines standardized centralization gap, expert misalignment, and information misalignment.

In layman's terms, the Sphere of Fear proxy is high when trust has moved away from central institutions and reliable knowledge channels into a more disconnected social configuration.

## Sample Counts

| Group | Countries |
|---|---:|
| Strict pre-shock WVS | 38 |
| Pandemic-overlap WVS | 27 |

## Pre-Shock vs Pandemic-Overlap Differences

Main result: the pandemic-overlap WVS group does not show a higher average Sphere-of-Fear trust-topology score than the strict pre-shock group. In fact, the group mean is lower, and the difference is not statistically significant. Therefore, this pass does not support a simple claim that post-shock countries universally collapsed into higher fear topology.

However, within the pandemic-overlap group, the Sphere-of-Fear and misalignment proxies are associated with worse outcomes, especially deaths per million, acute deaths, lower vaccination, and higher non-vaccinated share. The stronger finding is therefore conditional: the fear topology is harmful where it appears, not universally higher after the shock.

| Variable | Pre mean | Post mean | Post - Pre | Cohen d | Welch p |
|---|---:|---:|---:|---:|---:|
| centralization_gap | 0.111 | 0.091 | -0.020 | -0.151 | 0.562 |
| centralized_institutional_trust | 0.430 | 0.472 | 0.042 | 0.311 | 0.228 |
| deaths_per_million | 1786.163 | 1137.380 | -648.783 | -0.480 | 0.061 |
| decentralized_social_trust | 0.541 | 0.563 | 0.022 | 0.315 | 0.220 |
| expert_distrust | 0.409 | 0.386 | -0.024 | -0.253 | 0.308 |
| expert_epistemic_trust | 0.591 | 0.614 | 0.024 | 0.253 | 0.308 |
| fear_misalignment_index | 0.071 | -0.100 | -0.170 | -0.174 | 0.503 |
| fear_trust_topology_index | 0.086 | -0.122 | -0.208 | -0.237 | 0.361 |
| information_distrust | 0.564 | 0.552 | -0.013 | -0.117 | 0.656 |
| information_trust | 0.436 | 0.448 | 0.013 | 0.117 | 0.656 |
| institutional_distrust | 0.570 | 0.528 | -0.042 | -0.311 | 0.228 |
| misaligned_expert_index | -0.480 | -0.523 | -0.043 | -0.214 | 0.404 |
| misaligned_information_index | -0.325 | -0.357 | -0.033 | -0.143 | 0.582 |
| non_vaccinated_share | 27.242 | 35.894 | 8.652 | 0.449 | 0.089 |
| vaccination_rate | 72.758 | 64.106 | -8.652 | -0.449 | 0.089 |

## Regression Signals

| Sample | Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| all_pre_vs_post | acute_deaths_per_million | central_bivariate | z8_centralized_institutional_trust | -565.501 | [-883.554, -247.448] | 0.000 | 62 | 0.228 |
| all_pre_vs_post | acute_deaths_per_million | gap_bivariate | z8_centralization_gap | 460.697 | [236.649, 684.746] | 0.000 | 62 | 0.147 |
| all_pre_vs_post | acute_deaths_per_million | misalignment_bivariate | z8_fear_misalignment_index | 474.748 | [232.729, 716.767] | 0.000 | 62 | 0.157 |
| all_pre_vs_post | acute_deaths_per_million | misalignment_compact_controls | z8_fear_misalignment_index | 454.751 | [224.719, 684.784] | 0.000 | 60 | 0.218 |
| all_pre_vs_post | acute_deaths_per_million | post_indicator_compact | post_shock_wvs | -404.584 | [-1012.556, 203.388] | 0.192 | 60 | 0.097 |
| all_pre_vs_post | acute_deaths_per_million | post_x_sphere | post_shock_wvs | -342.013 | [-873.409, 189.383] | 0.207 | 60 | 0.269 |
| all_pre_vs_post | acute_deaths_per_million | post_x_sphere | post_shock_wvs:z8_fear_trust_topology_index | -328.971 | [-839.051, 181.108] | 0.206 | 60 | 0.269 |
| all_pre_vs_post | acute_deaths_per_million | post_x_sphere | z8_fear_trust_topology_index | 646.951 | [164.806, 1129.095] | 0.009 | 60 | 0.269 |
| all_pre_vs_post | acute_deaths_per_million | sphere_bivariate | z8_fear_trust_topology_index | 508.997 | [228.256, 789.737] | 0.000 | 62 | 0.182 |
| all_pre_vs_post | acute_deaths_per_million | sphere_compact_controls | z8_fear_trust_topology_index | 498.772 | [235.939, 761.605] | 0.000 | 60 | 0.255 |
| all_pre_vs_post | deaths_per_million | central_bivariate | z8_centralized_institutional_trust | -631.176 | [-979.044, -283.309] | 0.000 | 62 | 0.203 |
| all_pre_vs_post | deaths_per_million | gap_bivariate | z8_centralization_gap | 575.663 | [308.289, 843.037] | 0.000 | 62 | 0.168 |
| all_pre_vs_post | deaths_per_million | misalignment_bivariate | z8_fear_misalignment_index | 588.487 | [297.693, 879.281] | 0.000 | 62 | 0.176 |
| all_pre_vs_post | deaths_per_million | misalignment_compact_controls | z8_fear_misalignment_index | 528.858 | [271.551, 786.165] | 0.000 | 60 | 0.333 |
| all_pre_vs_post | deaths_per_million | post_indicator_compact | post_shock_wvs | -521.649 | [-1197.659, 154.361] | 0.130 | 60 | 0.221 |
| all_pre_vs_post | deaths_per_million | post_x_sphere | post_shock_wvs | -450.411 | [-1033.863, 133.042] | 0.130 | 60 | 0.388 |
| all_pre_vs_post | deaths_per_million | post_x_sphere | post_shock_wvs:z8_fear_trust_topology_index | -395.889 | [-963.099, 171.321] | 0.171 | 60 | 0.388 |
| all_pre_vs_post | deaths_per_million | post_x_sphere | z8_fear_trust_topology_index | 747.692 | [215.270, 1280.114] | 0.006 | 60 | 0.388 |
| all_pre_vs_post | deaths_per_million | sphere_bivariate | z8_fear_trust_topology_index | 605.972 | [278.329, 933.615] | 0.000 | 62 | 0.187 |
| all_pre_vs_post | deaths_per_million | sphere_compact_controls | z8_fear_trust_topology_index | 570.582 | [283.943, 857.221] | 0.000 | 60 | 0.363 |
| all_pre_vs_post | non_vaccinated_share | central_bivariate | z8_centralized_institutional_trust | -5.134 | [-9.865, -0.402] | 0.033 | 64 | 0.053 |
| all_pre_vs_post | non_vaccinated_share | gap_bivariate | z8_centralization_gap | 4.861 | [-0.045, 9.766] | 0.052 | 64 | 0.045 |
| all_pre_vs_post | non_vaccinated_share | misalignment_bivariate | z8_fear_misalignment_index | 5.205 | [0.588, 9.821] | 0.027 | 64 | 0.056 |
| all_pre_vs_post | non_vaccinated_share | misalignment_compact_controls | z8_fear_misalignment_index | 7.601 | [3.365, 11.838] | 0.000 | 61 | 0.319 |
| all_pre_vs_post | non_vaccinated_share | post_indicator_compact | post_shock_wvs | 4.031 | [-5.572, 13.635] | 0.411 | 61 | 0.175 |
| all_pre_vs_post | non_vaccinated_share | post_x_sphere | post_shock_wvs | 4.912 | [-3.793, 13.616] | 0.269 | 61 | 0.298 |
| all_pre_vs_post | non_vaccinated_share | post_x_sphere | post_shock_wvs:z8_fear_trust_topology_index | -0.564 | [-9.635, 8.507] | 0.903 | 61 | 0.298 |
| all_pre_vs_post | non_vaccinated_share | post_x_sphere | z8_fear_trust_topology_index | 7.605 | [1.748, 13.463] | 0.011 | 61 | 0.298 |
| all_pre_vs_post | non_vaccinated_share | sphere_bivariate | z8_fear_trust_topology_index | 5.587 | [1.225, 9.949] | 0.012 | 64 | 0.067 |
| all_pre_vs_post | non_vaccinated_share | sphere_compact_controls | z8_fear_trust_topology_index | 7.193 | [2.900, 11.486] | 0.001 | 61 | 0.307 |
| all_pre_vs_post | recovery_deaths_per_million | central_bivariate | z8_centralized_institutional_trust | -65.675 | [-129.967, -1.383] | 0.045 | 62 | 0.016 |
| all_pre_vs_post | recovery_deaths_per_million | gap_bivariate | z8_centralization_gap | 114.965 | [49.572, 180.359] | 0.001 | 62 | 0.085 |
| all_pre_vs_post | recovery_deaths_per_million | misalignment_bivariate | z8_fear_misalignment_index | 113.739 | [45.575, 181.904] | 0.001 | 62 | 0.083 |
| all_pre_vs_post | recovery_deaths_per_million | misalignment_compact_controls | z8_fear_misalignment_index | 74.107 | [21.752, 126.462] | 0.006 | 60 | 0.500 |
| all_pre_vs_post | recovery_deaths_per_million | post_indicator_compact | post_shock_wvs | -117.065 | [-268.475, 34.346] | 0.130 | 60 | 0.484 |
| all_pre_vs_post | recovery_deaths_per_million | post_x_sphere | post_shock_wvs | -108.398 | [-253.776, 36.980] | 0.144 | 60 | 0.511 |
| all_pre_vs_post | recovery_deaths_per_million | post_x_sphere | post_shock_wvs:z8_fear_trust_topology_index | -66.917 | [-168.499, 34.664] | 0.197 | 60 | 0.511 |
| all_pre_vs_post | recovery_deaths_per_million | post_x_sphere | z8_fear_trust_topology_index | 100.741 | [16.521, 184.962] | 0.019 | 60 | 0.511 |
| all_pre_vs_post | recovery_deaths_per_million | sphere_bivariate | z8_fear_trust_topology_index | 96.976 | [28.902, 165.049] | 0.005 | 62 | 0.056 |
| all_pre_vs_post | recovery_deaths_per_million | sphere_compact_controls | z8_fear_trust_topology_index | 71.810 | [20.654, 122.967] | 0.006 | 60 | 0.499 |
| all_pre_vs_post | vaccination_rate | central_bivariate | z8_centralized_institutional_trust | 5.134 | [0.402, 9.865] | 0.033 | 64 | 0.053 |
| all_pre_vs_post | vaccination_rate | gap_bivariate | z8_centralization_gap | -4.861 | [-9.766, 0.045] | 0.052 | 64 | 0.045 |
| all_pre_vs_post | vaccination_rate | misalignment_bivariate | z8_fear_misalignment_index | -5.205 | [-9.821, -0.588] | 0.027 | 64 | 0.056 |
| all_pre_vs_post | vaccination_rate | misalignment_compact_controls | z8_fear_misalignment_index | -7.601 | [-11.838, -3.365] | 0.000 | 61 | 0.319 |
| all_pre_vs_post | vaccination_rate | post_indicator_compact | post_shock_wvs | -4.031 | [-13.635, 5.572] | 0.411 | 61 | 0.175 |
| all_pre_vs_post | vaccination_rate | post_x_sphere | post_shock_wvs | -4.912 | [-13.616, 3.793] | 0.269 | 61 | 0.298 |
| all_pre_vs_post | vaccination_rate | post_x_sphere | post_shock_wvs:z8_fear_trust_topology_index | 0.564 | [-8.507, 9.635] | 0.903 | 61 | 0.298 |
| all_pre_vs_post | vaccination_rate | post_x_sphere | z8_fear_trust_topology_index | -7.605 | [-13.463, -1.748] | 0.011 | 61 | 0.298 |
| all_pre_vs_post | vaccination_rate | sphere_bivariate | z8_fear_trust_topology_index | -5.587 | [-9.949, -1.225] | 0.012 | 64 | 0.067 |
| all_pre_vs_post | vaccination_rate | sphere_compact_controls | z8_fear_trust_topology_index | -7.193 | [-11.486, -2.900] | 0.001 | 61 | 0.307 |
| behavior_overlap_tiny | government_control_belief_vaccine_rollout_2021 | behavior_gap_bivariate | z8_centralization_gap | 0.124 | [0.063, 0.185] | 0.000 | 9 | 0.567 |
| behavior_overlap_tiny | government_control_belief_vaccine_rollout_2021 | behavior_misalignment_bivariate | z8_fear_misalignment_index | 0.137 | [0.062, 0.212] | 0.000 | 9 | 0.556 |
| behavior_overlap_tiny | government_control_belief_vaccine_rollout_2021 | behavior_sphere_bivariate | z8_fear_trust_topology_index | 0.160 | [0.052, 0.268] | 0.004 | 9 | 0.428 |
| behavior_overlap_tiny | health_authority_vaccine_trust_vaccine_rollout_2021 | behavior_gap_bivariate | z8_centralization_gap | 0.000 | [-0.071, 0.071] | 0.999 | 9 | -0.143 |
| behavior_overlap_tiny | health_authority_vaccine_trust_vaccine_rollout_2021 | behavior_misalignment_bivariate | z8_fear_misalignment_index | -0.002 | [-0.084, 0.080] | 0.965 | 9 | -0.142 |
| behavior_overlap_tiny | health_authority_vaccine_trust_vaccine_rollout_2021 | behavior_sphere_bivariate | z8_fear_trust_topology_index | -0.012 | [-0.120, 0.095] | 0.820 | 9 | -0.119 |
| behavior_overlap_tiny | mask_refusal_outside_acute_2020 | behavior_gap_bivariate | z8_centralization_gap | 0.111 | [0.040, 0.181] | 0.002 | 20 | 0.403 |
| behavior_overlap_tiny | mask_refusal_outside_acute_2020 | behavior_misalignment_bivariate | z8_fear_misalignment_index | 0.109 | [0.039, 0.180] | 0.002 | 20 | 0.371 |
| behavior_overlap_tiny | mask_refusal_outside_acute_2020 | behavior_sphere_bivariate | z8_fear_trust_topology_index | 0.095 | [0.018, 0.172] | 0.015 | 20 | 0.219 |
| behavior_overlap_tiny | vaccine_refusal_vaccine_rollout_2021 | behavior_gap_bivariate | z8_centralization_gap | 0.016 | [-0.107, 0.140] | 0.797 | 9 | -0.130 |
| behavior_overlap_tiny | vaccine_refusal_vaccine_rollout_2021 | behavior_misalignment_bivariate | z8_fear_misalignment_index | 0.023 | [-0.126, 0.171] | 0.766 | 9 | -0.123 |
| behavior_overlap_tiny | vaccine_refusal_vaccine_rollout_2021 | behavior_sphere_bivariate | z8_fear_trust_topology_index | 0.038 | [-0.175, 0.252] | 0.726 | 9 | -0.109 |
| post_shock_wvs_only | acute_deaths_per_million | central_bivariate | z8_centralized_institutional_trust | -290.879 | [-613.946, 32.188] | 0.078 | 27 | 0.042 |
| post_shock_wvs_only | acute_deaths_per_million | gap_bivariate | z8_centralization_gap | 423.607 | [171.607, 675.606] | 0.001 | 27 | 0.134 |
| post_shock_wvs_only | acute_deaths_per_million | misalignment_bivariate | z8_fear_misalignment_index | 412.672 | [155.789, 669.555] | 0.002 | 27 | 0.125 |
| post_shock_wvs_only | acute_deaths_per_million | misalignment_compact_controls | z8_fear_misalignment_index | 313.978 | [2.084, 625.873] | 0.048 | 27 | 0.453 |
| post_shock_wvs_only | acute_deaths_per_million | sphere_bivariate | z8_fear_trust_topology_index | 359.640 | [71.355, 647.925] | 0.014 | 27 | 0.086 |
| post_shock_wvs_only | acute_deaths_per_million | sphere_compact_controls | z8_fear_trust_topology_index | 306.215 | [1.608, 610.822] | 0.049 | 27 | 0.453 |
| post_shock_wvs_only | deaths_per_million | central_bivariate | z8_centralized_institutional_trust | -315.086 | [-702.879, 72.707] | 0.111 | 27 | 0.026 |
| post_shock_wvs_only | deaths_per_million | gap_bivariate | z8_centralization_gap | 530.824 | [216.961, 844.688] | 0.001 | 27 | 0.147 |
| post_shock_wvs_only | deaths_per_million | misalignment_bivariate | z8_fear_misalignment_index | 513.451 | [199.640, 827.261] | 0.001 | 27 | 0.135 |
| post_shock_wvs_only | deaths_per_million | misalignment_compact_controls | z8_fear_misalignment_index | 363.660 | [1.587, 725.733] | 0.049 | 27 | 0.513 |
| post_shock_wvs_only | deaths_per_million | sphere_bivariate | z8_fear_trust_topology_index | 430.409 | [83.020, 777.798] | 0.015 | 27 | 0.083 |
| post_shock_wvs_only | deaths_per_million | sphere_compact_controls | z8_fear_trust_topology_index | 345.641 | [-0.527, 691.809] | 0.050 | 27 | 0.509 |
| post_shock_wvs_only | non_vaccinated_share | central_bivariate | z8_centralized_institutional_trust | -6.454 | [-14.597, 1.689] | 0.120 | 27 | 0.059 |
| post_shock_wvs_only | non_vaccinated_share | gap_bivariate | z8_centralization_gap | 4.484 | [-3.599, 12.566] | 0.277 | 27 | 0.008 |
| post_shock_wvs_only | non_vaccinated_share | misalignment_bivariate | z8_fear_misalignment_index | 4.554 | [-3.158, 12.266] | 0.247 | 27 | 0.009 |
| post_shock_wvs_only | non_vaccinated_share | misalignment_compact_controls | z8_fear_misalignment_index | 9.142 | [2.729, 15.555] | 0.005 | 27 | 0.392 |
| post_shock_wvs_only | non_vaccinated_share | sphere_bivariate | z8_fear_trust_topology_index | 5.124 | [-2.334, 12.581] | 0.178 | 27 | 0.022 |
| post_shock_wvs_only | non_vaccinated_share | sphere_compact_controls | z8_fear_trust_topology_index | 8.284 | [1.022, 15.546] | 0.025 | 27 | 0.364 |
| post_shock_wvs_only | recovery_deaths_per_million | central_bivariate | z8_centralized_institutional_trust | -24.207 | [-108.323, 59.910] | 0.573 | 27 | -0.033 |
| post_shock_wvs_only | recovery_deaths_per_million | gap_bivariate | z8_centralization_gap | 107.218 | [29.178, 185.257] | 0.007 | 27 | 0.100 |
| post_shock_wvs_only | recovery_deaths_per_million | misalignment_bivariate | z8_fear_misalignment_index | 100.779 | [26.300, 175.258] | 0.008 | 27 | 0.084 |
| post_shock_wvs_only | recovery_deaths_per_million | misalignment_compact_controls | z8_fear_misalignment_index | 49.682 | [-21.850, 121.214] | 0.173 | 27 | 0.519 |
| post_shock_wvs_only | recovery_deaths_per_million | sphere_bivariate | z8_fear_trust_topology_index | 70.769 | [-2.883, 144.420] | 0.060 | 27 | 0.021 |
| post_shock_wvs_only | recovery_deaths_per_million | sphere_compact_controls | z8_fear_trust_topology_index | 39.426 | [-24.449, 103.301] | 0.226 | 27 | 0.508 |
| post_shock_wvs_only | vaccination_rate | central_bivariate | z8_centralized_institutional_trust | 6.454 | [-1.689, 14.597] | 0.120 | 27 | 0.059 |
| post_shock_wvs_only | vaccination_rate | gap_bivariate | z8_centralization_gap | -4.484 | [-12.566, 3.599] | 0.277 | 27 | 0.008 |
| post_shock_wvs_only | vaccination_rate | misalignment_bivariate | z8_fear_misalignment_index | -4.554 | [-12.266, 3.158] | 0.247 | 27 | 0.009 |
| post_shock_wvs_only | vaccination_rate | misalignment_compact_controls | z8_fear_misalignment_index | -9.142 | [-15.555, -2.729] | 0.005 | 27 | 0.392 |
| post_shock_wvs_only | vaccination_rate | sphere_bivariate | z8_fear_trust_topology_index | -5.124 | [-12.581, 2.334] | 0.178 | 27 | 0.022 |
| post_shock_wvs_only | vaccination_rate | sphere_compact_controls | z8_fear_trust_topology_index | -8.284 | [-15.546, -1.022] | 0.025 | 27 | 0.364 |

## Interpretation

The central scientific question is whether post-shock trust topology looks more contracted and whether that contraction proxy aligns with worse recovery outcomes. The first condition is not supported as a universal group-level claim: pandemic-overlap countries do not have higher mean fear-topology scores than strict pre-shock countries. The second condition receives stronger support: among pandemic-overlap countries, higher fear-topology and misalignment scores predict worse mortality and vaccination outcomes.

This refines the Sphere of Fear hypothesis. The evidence does not say that all societies collapsed into fear after COVID. It says that where trust becomes configured as institutional distrust, centralization gap, and expert/information misalignment, outcomes look worse. The collapse pattern is a topology within the post-shock field, not a universal post-shock average.

Behavioral evidence remains extremely limited in the pandemic-overlap WVS group because YouGov overlap is very small. Those rows should be treated as illustrative, not confirmatory.

## What Would Falsify or Weaken This Layer?

- Pandemic-overlap WVS countries do not show higher institutional distrust, centralization gap, or fear-topology scores.
- Fear-topology and misalignment indices do not predict mortality, vaccination gaps, or behavioral contraction proxies.
- Direct longitudinal data show that post-shock trust does not migrate away from institutions after severe shocks.
- Information/media variables fully explain the fear-topology pattern.

## Next Step

The stronger future design is true panel or repeated-cross-section analysis: measure trust before the shock, during the shock, and after the shock in the same country or individual samples. That would allow direct estimation of trust migration into or out of the Sphere of Fear.