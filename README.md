# AI Freedom Trust Federation Website

This folder contains the static public website for AI Freedom Trust Federation.

## Files

- `index.html` - one-page public website
- `styles.css` - responsive styling with no build step
- `assets/aift-federation-hero.png` - generated hero image used by the site
- `docs/organization-map.md` - umbrella structure and repository roles
- `docs/pdf/` - generated PDF documents from the LaTeX document engine
- `docs/aetherion-circleunchain-biozoe-source-summary.md` - preserved source synthesis for Aetherion, Circleunchain, Biozoe Coin, AetherCoin, and future biozoe coins
- `docs/aetherion-genesis-whitepaper-alpha.md` - alpha Genesis White Paper draft for Aetherion as a recursive civilization network
- `docs/aetherion-flight-paper-post-quantum-sovereign-network.md` - flagship flight paper draft for Aetherion as a post-quantum sovereign network
- `docs/aetherion-restorative-civilization-economy.md` - constitutional doctrine draft for Aetherion as a Restorative Civilization Economy
- `latex/` - LaTeX source, shared styles, and document engine instructions
- `scripts/build-latex.ps1` - builds LaTeX source files into public PDFs
- `.nojekyll` - keeps GitHub Pages from applying Jekyll processing

## LaTeX Documents

This repository includes a LaTeX document engine for polished doctrine papers, whitepapers, and trust documents.

Build every LaTeX document:

```powershell
.\scripts\build-latex.ps1
```

Final PDFs are written to `docs/pdf/`.

## GitHub Pages

This site can be hosted directly from a GitHub repository:

1. Commit these files to the public website repository, preferably `AIFreedomTrustFederation/www.aifreedomtrust.com`.
2. In GitHub, open repository Settings.
3. Go to Pages.
4. Set the source to `Deploy from a branch`.
5. Select the `main` branch and `/root`.
6. Save.

If using a custom domain, add the domain in the GitHub Pages settings and create a `CNAME` file containing that domain.
