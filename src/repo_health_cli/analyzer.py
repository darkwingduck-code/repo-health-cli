from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


WEIGHTS = {
    "readme": 20,
    "license": 20,
    "tests": 20,
    "ci": 20,
    "gitignore": 10,
    "contributing": 10,
}


@dataclass(frozen=True)
class RepoHealthReport:
    path: str
    score: int
    max_score: int
    checks: dict[str, bool]
    missing: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "score": self.score,
            "max_score": self.max_score,
            "checks": self.checks,
            "missing": self.missing,
        }


def _has_any(path: Path, patterns: tuple[str, ...]) -> bool:
    return any(any(path.glob(pattern)) for pattern in patterns)


def analyze_repo(target: str | Path) -> RepoHealthReport:
    root = Path(target).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root}")

    checks = {
        "readme": _has_any(root, ("README", "README.*", "readme", "readme.*")),
        "license": _has_any(root, ("LICENSE", "LICENSE.*", "license", "license.*")),
        "tests": any((root / name).exists() for name in ("tests", "test")),
        "ci": any(
            (root / rel).exists()
            for rel in (
                ".github/workflows",
                ".gitlab-ci.yml",
                ".circleci/config.yml",
                "azure-pipelines.yml",
            )
        ),
        "gitignore": (root / ".gitignore").exists(),
        "contributing": _has_any(root, ("CONTRIBUTING", "CONTRIBUTING.*", "contributing", "contributing.*")),
    }
    score = sum(WEIGHTS[name] for name, passed in checks.items() if passed)
    missing = [name for name, passed in checks.items() if not passed]
    return RepoHealthReport(
        path=str(root),
        score=score,
        max_score=sum(WEIGHTS.values()),
        checks=checks,
        missing=missing,
    )
