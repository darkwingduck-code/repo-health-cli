# repo-health-cli

Small Python CLI that scores the basic health of a Git repository.

## What it checks

- `README` presence
- `LICENSE` presence
- test directory presence
- CI workflow presence
- `.gitignore` presence
- `CONTRIBUTING` presence
- project manifest presence
- `SECURITY` presence

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install .[dev] --no-build-isolation
repo-health .
```

## Example

```bash
repo-health . --json
```

```bash
repo-health --schema
```

```bash
repo-health . --output reports/health.json
```

Example output:

```json
{
  "path": "C:\\project",
  "score": 65,
  "max_score": 100,
  "passed_checks": 5,
  "total_checks": 8,
  "checks": {
    "readme": true,
    "license": true,
    "tests": true,
    "ci": false,
    "gitignore": true,
    "contributing": false,
    "manifest": true,
    "security": false
  },
  "missing": [
    "ci",
    "contributing",
    "security"
  ]
}
```

## Scoring

The current scoring model totals `100` points:

- `README`: 20
- `LICENSE`: 15
- `tests`: 20
- `ci`: 20
- `gitignore`: 10
- `contributing`: 10
- `manifest`: 5
- `security`: 5

Results can be printed as JSON, written to a file with `--output`, or consumed via the published schema from `--schema`.

## Development

```bash
ruff check .
pytest -q
```
