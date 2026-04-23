from __future__ import annotations

import argparse
import json
import sys

from repo_health_cli.analyzer import analyze_repo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score the basic health of a Git repository.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to inspect.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON output.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        report = analyze_repo(args.path)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.as_json:
        print(json.dumps(report.to_dict(), indent=2))
        return 0

    print(f"Path: {report.path}")
    print(f"Score: {report.score}/100")
    for name, passed in report.checks.items():
        mark = "OK" if passed else "MISSING"
        print(f"- {name}: {mark}")
    if report.missing:
        print(f"Missing: {', '.join(report.missing)}")
    else:
        print("Missing: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

