# Federation Role: AI-Freedom-Trust

## Layer

`doctrine`

## Role

doctrine, trust research, alignment papers, and constitutional philosophy

## Operating Principle

This repository is part of the AI Freedom Trust Federation operating system. It remains sovereign in its own repo while participating in the shared federation control plane.

## Control Plane

Top-level workspace:

```bash
/data/data/com.termux/files/home/AIFT
```

Primary command:

```bash
/data/data/com.termux/files/home/AIFT/aift-os.sh
```

## Standard Commands

Status:

```bash
git status --short
```

Pull:

```bash
git pull --ff-only
```

Verify (from the repository root; Python 3.9+):

```bash
python3 -B scripts/validate_doctrine.py && python3 -B -m unittest discover -s tests -v
```

This runs the doctrine manifest/path and research-script syntax checks, then the Python unit tests. A failing check returns a nonzero status. It does not rebuild PDFs or rerun empirical research.

## Federation Metadata

This repo declares its federation role in:

```bash
aift.repo.json
```

The workspace-level federation manifest is generated at:

```bash
/data/data/com.termux/files/home/AIFT/manifests/workspace.json
```
