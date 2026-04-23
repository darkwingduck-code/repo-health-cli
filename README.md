# repo-health-cli

Small Python CLI that scores the basic health of a Git repository.

## What it checks

- `README` presence
- `LICENSE` presence
- test directory presence
- CI workflow presence
- `.gitignore` presence
- `CONTRIBUTING` presence

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

Example output:

```json
{
  "path": "C:\\project",
  "score": 70,
  "max_score": 100,
  "checks": {
    "readme": true,
    "license": true,
    "tests": true,
    "ci": false,
    "gitignore": true,
    "contributing": false
  },
  "missing": [
    "ci",
    "contributing"
  ]
}
```

## Scoring

The current scoring model totals `100` points:

- `README`: 20
- `LICENSE`: 20
- `tests`: 20
- `ci`: 20
- `gitignore`: 10
- `contributing`: 10

## Development

```bash
ruff check .
pytest -q
```
