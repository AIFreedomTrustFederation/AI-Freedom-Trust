# AetherCore External Review Packet

Status: awaiting external review

This packet is the public checklist for moving the AetherCore empirical work from internal publication to outside review.

## Core Materials

- Empirical PDF: [`docs/pdf/aethercore-empirical-trust-density-covid.pdf`](pdf/aethercore-empirical-trust-density-covid.pdf)
- LaTeX source: [`latex/documents/aethercore-empirical-trust-density-covid.tex`](../latex/documents/aethercore-empirical-trust-density-covid.tex)
- Research package: [`research/aethercore-test-001`](../research/aethercore-test-001)
- Artifact policy: [`research/aethercore-test-001/ARTIFACT_POLICY.md`](../research/aethercore-test-001/ARTIFACT_POLICY.md)
- Main repository README: [`README.md`](../README.md)

## Reproducibility Checklist

1. Confirm Python version and dependencies from `research/aethercore-test-001/requirements.txt`.
2. Confirm raw data acquisition instructions and data-license limits.
3. Re-run all test scripts from `research/aethercore-test-001/scripts`.
4. Compare regenerated processed data, figures, outputs, and reports with tracked artifacts.
5. Record any differences caused by upstream data revisions or package-version drift.

## Review Questions

External reviewers should focus on:

1. Whether the trust variables are operationalized clearly enough to test the stated claims.
2. Whether the controls, samples, and robustness checks are appropriate for exploratory cross-national analysis.
3. Whether the conclusions are calibrated to correlational evidence rather than causal proof.
4. Whether any alternative explanation is stronger than the trust-topology interpretation.
5. Whether the paper states what would weaken or falsify the proposed framework.

## Limitations To Preserve

- The results are exploratory and correlational.
- The work does not prove AetherCore as a full framework.
- Cross-national COVID data has reporting, policy, timing, and measurement limitations.
- Trust measures differ by survey timing, culture, institutional context, and post-shock exposure.
- Stronger future claims require preregistration, independent replication, and additional datasets.

## Reviewer Invitation List

Target reviewers should include at least one person from each category:

1. Quantitative social science or political economy.
2. Public health crisis-response research.
3. Survey methodology or cross-national measurement.
4. Governance/institutional trust research.
5. Independent statistical replication.

## Next Actions

1. Freeze a review release tag.
2. Export a clean PDF and source archive for reviewers.
3. Add a short reviewer cover note.
4. Invite two independent reviewers before expanding public claims.
5. Publish reviewer feedback or a response memo when available.
