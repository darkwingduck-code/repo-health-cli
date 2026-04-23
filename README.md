# repo-health-cli

Small Python CLI that scores the basic health of a Git repository.

## What it checks

- `README` presence
- `LICENSE` presence
- test directory presence
- CI workflow presence

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

Example output:

```json
{
  "path": "C:\\project",
  "score": 75,
  "checks": {
    "readme": true,
    "license": true,
    "tests": true,
    "ci": false
  },
  "missing": [
    "ci"
  ]
}
```

## Development

```bash
ruff check .
pytest -q
```
