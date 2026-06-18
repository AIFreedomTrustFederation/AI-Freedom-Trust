# AetherCore Test 002: Trust Density and COVID Behavioral Resistance

## Purpose

This second pass tests whether WVS trust variables predict direct behavioral COVID resistance proxies from the Imperial College London / YouGov COVID-19 Behaviour Tracker.

This is still an observational, small-N cross-country screen. It is designed to generate stronger hypotheses, not final proof.

## Data

- Behavioral source: `https://github.com/YouGov-Data/covid-19-tracker`
- Countries in YouGov behavioral aggregate: 20
- Countries after merge with WVS/OWID controls: 20

## Behavioral Variables

- `vaccine_refusal`: disagreement with vaccine-intent items. This is the best anti-vax proxy in this pass.
- `vaccine_intent`: agreement with vaccine-intent items.
- `mask_refusal_outside`: reporting rarely or never wearing a mask outside the home.
- `mask_compliance_outside`: frequency-scaled mask wearing outside the home.
- `health_authority_vaccine_trust`: belief that government health authorities will provide an effective vaccine.
- `government_control_belief`: agreement that COVID-19 is being exploited by government to control people.

## Phase Windows

- `acute_2020`: survey responses through 2020-12-31.
- `vaccine_rollout_2021`: responses from 2021-01-01 through 2021-12-31.
- `early_recovery_2022`: responses after 2022-01-01.

## Compact-Control Trust Coefficients

| Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |
|---|---|---:|---:|---:|---:|---:|---:|
| mask_compliance_outside_acute_2020 | compact_controls_expert_proxy_trust | z_trust_experts | -0.081 | [-0.197, 0.035] | 0.171 (n.s.) | 19 | 0.339 |
| mask_compliance_outside_acute_2020 | compact_controls_generalized_trust | z_trust_generalized | -0.143 | [-0.314, 0.029] | 0.103 (n.s.) | 19 | 0.617 |
| mask_compliance_outside_acute_2020 | compact_controls_information_proxy | z_information_integrity_proxy | 0.083 | [-0.016, 0.182] | 0.100 (p<0.10) | 19 | 0.378 |
| mask_compliance_outside_acute_2020 | compact_controls_institutional_trust | z_trust_institutions | -0.005 | [-0.086, 0.076] | 0.902 (n.s.) | 19 | 0.242 |
| mask_compliance_outside_acute_2020 | compact_controls_trust_density | z_trust_density_composite | -0.072 | [-0.142, -0.001] | 0.047 (p<0.05) | 19 | 0.401 |
| mask_refusal_outside_acute_2020 | compact_controls_expert_proxy_trust | z_trust_experts | 0.073 | [-0.032, 0.178] | 0.172 (n.s.) | 19 | 0.348 |
| mask_refusal_outside_acute_2020 | compact_controls_generalized_trust | z_trust_generalized | 0.127 | [-0.044, 0.299] | 0.146 (n.s.) | 19 | 0.585 |
| mask_refusal_outside_acute_2020 | compact_controls_information_proxy | z_information_integrity_proxy | -0.081 | [-0.168, 0.007] | 0.071 (p<0.10) | 19 | 0.400 |
| mask_refusal_outside_acute_2020 | compact_controls_institutional_trust | z_trust_institutions | 0.001 | [-0.073, 0.075] | 0.975 (n.s.) | 19 | 0.261 |
| mask_refusal_outside_acute_2020 | compact_controls_trust_density | z_trust_density_composite | 0.063 | [-0.005, 0.130] | 0.072 (p<0.10) | 19 | 0.393 |

## Exploratory Bivariate Vaccine and Conspiracy Screens

These models use only 9 countries after WVS/YouGov overlap, so they are hypothesis-generating only.

| Outcome | Model | Term | Coef | 95% CI | p | n | Adj. R2 |
|---|---|---:|---:|---:|---:|---:|---:|
| government_control_belief_vaccine_rollout_2021 | bivariate_expert_proxy_trust | z_trust_experts | 0.007 | [-0.207, 0.221] | 0.948 (n.s.) | 9 | -0.141 |
| government_control_belief_vaccine_rollout_2021 | bivariate_generalized_trust | z_trust_generalized | 0.145 | [0.011, 0.279] | 0.034 (p<0.05) | 9 | 0.253 |
| government_control_belief_vaccine_rollout_2021 | bivariate_information_proxy | z_information_integrity_proxy | -0.115 | [-0.209, -0.021] | 0.016 (p<0.05) | 9 | 0.416 |
| government_control_belief_vaccine_rollout_2021 | bivariate_institutional_trust | z_trust_institutions | -0.133 | [-0.238, -0.029] | 0.012 (p<0.05) | 9 | 0.174 |
| government_control_belief_vaccine_rollout_2021 | bivariate_trust_density | z_trust_density_composite | 0.028 | [-0.213, 0.269] | 0.819 (n.s.) | 9 | -0.123 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_expert_proxy_trust | z_trust_experts | 0.039 | [0.008, 0.069] | 0.013 (p<0.05) | 9 | 0.199 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_generalized_trust | z_trust_generalized | 0.003 | [-0.067, 0.074] | 0.927 (n.s.) | 9 | -0.141 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_information_proxy | z_information_integrity_proxy | -0.012 | [-0.075, 0.052] | 0.719 (n.s.) | 9 | -0.104 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_institutional_trust | z_trust_institutions | 0.034 | [-0.046, 0.114] | 0.402 (n.s.) | 9 | -0.001 |
| health_authority_vaccine_trust_vaccine_rollout_2021 | bivariate_trust_density | z_trust_density_composite | 0.034 | [-0.008, 0.076] | 0.111 (n.s.) | 9 | 0.054 |
| vaccine_intent_vaccine_rollout_2021 | bivariate_expert_proxy_trust | z_trust_experts | 0.041 | [-0.120, 0.201] | 0.618 (n.s.) | 9 | -0.076 |
| vaccine_intent_vaccine_rollout_2021 | bivariate_generalized_trust | z_trust_generalized | 0.008 | [-0.071, 0.087] | 0.842 (n.s.) | 9 | -0.141 |
| vaccine_intent_vaccine_rollout_2021 | bivariate_information_proxy | z_information_integrity_proxy | -0.011 | [-0.161, 0.140] | 0.891 (n.s.) | 9 | -0.137 |
| vaccine_intent_vaccine_rollout_2021 | bivariate_institutional_trust | z_trust_institutions | 0.001 | [-0.194, 0.197] | 0.989 (n.s.) | 9 | -0.143 |
| vaccine_intent_vaccine_rollout_2021 | bivariate_trust_density | z_trust_density_composite | 0.026 | [-0.153, 0.206] | 0.772 (n.s.) | 9 | -0.122 |
| vaccine_refusal_vaccine_rollout_2021 | bivariate_expert_proxy_trust | z_trust_experts | -0.033 | [-0.231, 0.164] | 0.741 (n.s.) | 9 | -0.104 |
| vaccine_refusal_vaccine_rollout_2021 | bivariate_generalized_trust | z_trust_generalized | 0.036 | [-0.047, 0.119] | 0.396 (n.s.) | 9 | -0.117 |
| vaccine_refusal_vaccine_rollout_2021 | bivariate_information_proxy | z_information_integrity_proxy | -0.021 | [-0.177, 0.135] | 0.789 (n.s.) | 9 | -0.123 |
| vaccine_refusal_vaccine_rollout_2021 | bivariate_institutional_trust | z_trust_institutions | -0.031 | [-0.240, 0.177] | 0.768 (n.s.) | 9 | -0.125 |
| vaccine_refusal_vaccine_rollout_2021 | bivariate_trust_density | z_trust_density_composite | -0.011 | [-0.235, 0.212] | 0.921 (n.s.) | 9 | -0.140 |

## Interpretation Rules

A useful signal is directional consistency across related outcomes, not a declaration of proof. For example, trust should predict lower vaccine refusal and higher vaccine intent, or lower government-control belief and higher confidence in health authorities.

The claim is weakened when coefficients are directionally inconsistent, insignificant across related outcomes, or only appear in bivariate models and disappear under compact controls.

## Limitations

- The YouGov country sample is much smaller than OWID's country coverage.
- Country overlap with WVS reduces the usable model sample further.
- Compact controls are used to avoid extreme overfitting; full-control models are not appropriate at this sample size.
- Mask refusal and vaccine refusal are behavioral/attitudinal proxies, not identity labels.
- Survey timing varies by country and question availability.