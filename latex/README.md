# AFT LaTeX Document Engine

This folder is the document engine for AI Freedom Trust Federation.

It turns doctrine, whitepapers, trust documents, flight papers, and future constitutional materials into polished PDFs while keeping the public website simple.

## Structure

- `documents/` - source `.tex` files for publishable documents
- `styles/` - shared AFT LaTeX styling
- `build/` - temporary build files, ignored by git
- `../docs/pdf/` - final generated PDFs intended for public linking

## Build

From the repository root:

```powershell
.\scripts\build-latex.ps1
```

To build one document:

```powershell
.\scripts\build-latex.ps1 -Document aetherion-restorative-civilization-economy
```

The script uses `xelatex` and writes finished PDFs to `docs/pdf/`.

## Authoring Notes

Start new documents from `documents/aetherion-restorative-civilization-economy.tex` or create a smaller template that imports:

```tex
\input{../styles/aftdoctrine.sty}
```

Keep legally sensitive claims in concept-stage language until reviewed. Public PDFs should avoid implying a live token sale, audited network, custody service, securities status, guaranteed returns, tax treatment, insurance protection, or production monetary engine.
