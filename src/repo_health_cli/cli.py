from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from repo_health_cli.analyzer import analyze_repo


REPORT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "RepoHealthReport",
    "type": "object",
    "required": ["path", "score", "max_score", "passed_checks", "total_checks", "checks", "missing"],
    "properties": {
        "path": {"type": "string"},
        "score": {"type": "integer", "minimum": 0},
        "max_score": {"type": "integer", "minimum": 0},
        "passed_checks": {"type": "integer", "minimum": 0},
        "total_checks": {"type": "integer", "minimum": 0},
        "checks": {
            "type": "object",
            "additionalProperties": {"type": "boolean"},
        },
        "missing": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "additionalProperties": False,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score the basic health of a Git repository.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to inspect.")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON output.")
    parser.add_argument("--output", help="Write JSON output to a file.")
    parser.add_argument("--schema", action="store_true", help="Emit the JSON schema for report output.")
    return parser


def _write_json_file(target: str, payload: dict[str, object]) -> None:
    output_path = Path(target).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.schema:
        print(json.dumps(REPORT_SCHEMA, indent=2))
        return 0

    try:
        report = analyze_repo(args.path)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    report_payload = report.to_dict()

    if args.output:
        _write_json_file(args.output, report_payload)

    if args.as_json or args.output:
        print(json.dumps(report_payload, indent=2))
        return 0

    print(f"Path: {report.path}")
    print(f"Score: {report.score}/{report.max_score}")
    print(f"Checks: {report.passed_checks}/{report.total_checks}")
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
