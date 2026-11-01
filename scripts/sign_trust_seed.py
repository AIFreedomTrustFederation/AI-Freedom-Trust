from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import trust_seed_identity


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sign the canonical local state of a trust seed.",
    )
    parser.add_argument("trust_seed", help="Path to the local trust seed directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    seed_dir = trust_seed_identity.resolve_cli_seed_path(args.trust_seed)
    record = trust_seed_identity.sign_seed(seed_dir)
    trust_seed_identity.print_sign_result(seed_dir, record)


if __name__ == "__main__":
    main()
