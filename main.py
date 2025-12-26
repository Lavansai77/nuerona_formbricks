#!/usr/bin/env python3

import sys
import argparse
from commands.up import run_up
from commands.down import run_down
from commands.generate import run_generate
from commands.seed import run_seed


def main():
    parser = argparse.ArgumentParser(
        description="Formbricks CLI - Manage local Formbricks instance"
    )

    subparsers = parser.add_subparsers(dest="service")
    formbricks_parser = subparsers.add_parser("formbricks")

    formbricks_subparsers = formbricks_parser.add_subparsers(dest="command")
    formbricks_subparsers.add_parser("up", help="Start Formbricks locally")
    formbricks_subparsers.add_parser("down", help="Stop Formbricks")
    formbricks_subparsers.add_parser("generate", help="Generate realistic survey data")
    formbricks_subparsers.add_parser("seed", help="Seed Formbricks with generated data")

    args = parser.parse_args()

    if args.service != "formbricks":
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "up":
            run_up()
        elif args.command == "down":
            run_down()
        elif args.command == "generate":
            run_generate()
        elif args.command == "seed":
            run_seed()
        else:
            formbricks_parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
