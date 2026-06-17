# Incubating and Legacy Repository Review

Date: June 17, 2026

Scope:

- `biozone-harmony-boost`
- `chktex`
- private `c-848263`
- private `repo-brainstorm-backend-forge`

## Executive Recommendation

| Repository | Current Classification | Recommendation | Reason |
| --- | --- | --- | --- |
| `biozone-harmony-boost` | Public / Incubating | Keep public but mark as incubating; do not promote yet | Buildable Aether/Biozone front-end prototype, but README is still generic Lovable copy, dependency audit has one critical issue, and public claims need tightening |
| `chktex` | Public / Fork | Leave as forked reference or archive later | External LaTeX utility fork with no AIFT-specific product role; useful only as tooling history |
| `c-848263` | Private / Incubating | Rename and keep private as `mysterion-mind-map-cortex` or similar | Real Mind Map/Cortex interface code exists; build passes; concept fits Stewardship/Research, but public language and repo name need cleanup before promotion |
| `repo-brainstorm-backend-forge` | Private / Incubating | Keep private for now; likely merge concepts into `AIFT-Forge` or archive | Buildable GitHub repository viewer/prototype, but it is not yet a backend forge and mostly looks like a focused Lovable prototype |

## Verification Performed

### `biozone-harmony-boost`

- `npm ci`: passed
- `npm run build`: passed
- Audit result: 24 vulnerabilities: 2 low, 8 moderate, 13 high, 1 critical
- Build warnings:
  - Browserslist data is stale
  - `/src/assets/earth-pattern.png` does not resolve at build time and remains a runtime reference

Observed value:

- Vite/React/Tailwind/shadcn app.
- Aether Coin/Biozone-facing content.
- Wallet, tokenomics, API, GitHub, presale, privacy, and terms pages/components.
- Contains API client patterns and wallet hooks that may overlap with `Aether_Coin_biozonecurrency`.

Risks:

- README is generic Lovable boilerplate.
- Public token/presale/ecological currency claims need review.
- Dependency set is stale.
- Critical audit finding blocks promotion.

Decision:

Keep as `Incubating`. Do not archive yet. Do not present as an active public product until dependency and public-claims cleanup is complete.

Recommended next actions:

1. Open repo issue: clean dependency audit and upgrade Vite/React Router/Axios-related dependencies.
2. Replace Lovable README with federation status, purpose, setup, verification, and public-claims warning.
3. Decide whether useful wallet/token UI should be merged into `Aether_Coin_biozonecurrency`.
4. Remove or soften any unsupported presale, token, API, wallet, or ecological funding claims.

## `chktex`

Verification:

- Inspected branch, files, README, and NEWS.
- Default branch is `master`.
- Last code history is upstream-style C utility work from 2016.

Observed value:

- External C-based LaTeX checker fork.
- Could be useful for document/tooling workflows.

Risks:

- No clear AI Freedom Trust Federation product role.
- Public repo list may confuse visitors if it appears beside active federation work.

Decision:

Keep marked as `Fork` / external tooling. Consider archiving if it is not actively used.

Recommended next actions:

1. Leave description/topics as fork/tooling.
2. Add a short README note if kept public: "External fork retained for tooling reference."
3. Archive only after confirming no local document/tooling workflow depends on it.

## `c-848263`

Verification:

- `npm ci`: passed
- `npm run build`: passed
- Audit result: 21 vulnerabilities: 2 low, 7 moderate, 12 high
- Build warnings:
  - Browserslist data is stale
  - One chunk larger than 500 kB after minification

Observed value:

- Private Vite/React/Tailwind/shadcn app.
- Contains substantial Mind Map / Cortex interface code.
- Includes dashboard, import, search, profile, manage views, mind map utilities, cortex data, project roadmap, and chat UI.
- Has an `AGENTS.md` identifying the system layer as "Mind mapping, interface mapping, and doctrine synthesis."

Risks:

- Repository name `c-848263` is opaque.
- README has malformed/generic setup text and some public language that needs grounding.
- Public promotion would require claims cleanup and clearer product boundaries.
- Dependency audit needs cleanup before any deployment.

Decision:

Keep private and rename. Strong candidate name: `mysterion-mind-map-cortex`.

Recommended next actions:

1. Rename repo from `c-848263` to `mysterion-mind-map-cortex`.
2. Standardize README with federation status.
3. Keep private until public claims and dependency audit are cleaned.
4. Decide relationship to `TheMindofAll`: UI layer, research interface, or companion app.

## `repo-brainstorm-backend-forge`

Verification:

- `npm ci`: passed
- `npm run build`: passed
- Audit result: 21 vulnerabilities: 2 low, 7 moderate, 12 high
- Build warnings:
  - Browserslist data is stale

Observed value:

- Private Vite/React/Tailwind/shadcn app.
- GitHub repository viewer/prototype with route `/repository/:owner/:repo`.
- Fetches repository metadata, README, files, commits, contributors, and related details.
- Could become a repo intelligence panel for federation operations.

Risks:

- Not currently a backend forge despite the name.
- README is generic Lovable boilerplate.
- Some copy refers broadly to blockchain/sustainability and may not match actual scope.
- Dependency audit needs cleanup.

Decision:

Keep private as incubating. Do not promote. Review for merger into `AIFT-Forge` as a repo intelligence panel or archive after extracting useful code.

Recommended next actions:

1. Rename only if it remains standalone.
2. If useful, merge repo-viewer concepts into `AIFT-Forge`.
3. Replace README and clarify purpose.
4. Clean dependencies before deployment.

## Consolidated Next Actions

1. Keep `biozone-harmony-boost` public but visibly incubating.
2. Keep `chktex` as fork/external tooling; consider archive later.
3. Rename private `c-848263` to `mysterion-mind-map-cortex`.
4. Keep `repo-brainstorm-backend-forge` private and decide merge vs archive.
5. Create follow-up issues for dependency cleanup and README standardization.

