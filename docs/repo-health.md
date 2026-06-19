# Federation Repository Health

Last reviewed: 2026-06-19

This dashboard separates current status from historical failure notifications. Old failed runs remain in GitHub history; the status below reflects the latest checked operational signal.

| Repository | Role | Latest CI / Build Status | Deployment Status | Current Action |
| --- | --- | --- | --- | --- |
| `AI-Freedom-Trust` | Canonical papers, PDFs, empirical package, GitHub Pages site | Passing GitHub Pages build | Live on GitHub Pages | Keep paper library and review packet current |
| `www.aifreedomtrust.com` | Public portal | Passing GitHub Pages build | Live on GitHub Pages | Keep portal synchronized with canonical research status |
| `tastycutz` | Production-facing provisions app | Passing `CCP CI` after test glob and E2E stabilization | Latest Vercel production deployments are `Ready` | Monitor scheduled recovery processor and Vercel deployments |
| `capital-city-provisions` | Applied systems / provisions operations | Passing current CI | Public deployment status not verified in this pass | Preserve as production-facing, revenue-unverified until operating metrics are published |
| `Aether_Coin_biozonecurrency` | Aetherion wallet/value protocol | Passing latest auto-sync and deploy workflows | Latest checked Aetherion deployment workflows are green | Keep deployment secrets documented; avoid failing when optional deploy targets are not configured |
| `VPS` | Infrastructure layer | Not checked in this pass | Not checked in this pass | Add CI/deployment signal to dashboard |
| `AIFT-Forge` | Federation coordination/templates | Not checked in this pass | Not checked in this pass | Add CI/deployment signal to dashboard |

## Cleared Issues

- `tastycutz` CI previously failed because Linux CI passed `tests/**/*.test.ts` literally to `tsx`; fixed by using `tests/*.test.ts`.
- `tastycutz` recovery processor previously failed when `RECOVERY_PROCESS_URL` and `RECOVERY_PROCESS_SECRET` were absent; fixed by skipping cleanly when not configured.
- `tastycutz` homepage E2E previously targeted stale `Build My Box` text; fixed with a stable `#boxes a[href="/freezer-boxes"]` selector.
- `Aether_Coin_biozonecurrency` previously failed deployment when SSH secrets were missing. Current workflows include secret checks and latest checked deploy runs are green.

## Remaining Watch Items

- `tastycutz` scheduled recovery processing is only a no-op until `RECOVERY_PROCESS_URL` and `RECOVERY_PROCESS_SECRET` are configured.
- `capital-city-provisions` should not be described as revenue-verified until real order, revenue, delivery, refund, and repeat-customer metrics are published.
- Repos without CI should either add minimal build checks or be explicitly labeled as documentation/archive-only.

## Operating Standard

Each active repository should expose:

1. Latest CI/build status.
2. Latest deployment status.
3. Known warnings or missing secrets.
4. Production URL, if any.
5. Public maturity label: empirical, production-facing, infrastructure, concept, archive, or unknown.
