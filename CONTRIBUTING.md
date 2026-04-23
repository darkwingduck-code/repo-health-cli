# Contributing

## Workflow

1. Create a feature branch from `main`.
2. Keep changes small and focused.
3. Run `ruff check .` and `pytest -q` before opening a pull request.
4. Open a PR with a clear summary and test notes.

## Branch Protection

Recommended protection for `main`:

- Require pull requests before merging
- Require the `test` GitHub Actions check to pass
- Require branches to be up to date before merging
- Restrict direct pushes to `main`
- Prefer squash merge

