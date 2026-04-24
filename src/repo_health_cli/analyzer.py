from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


WEIGHTS = {
    "readme": 15,
    "license": 15,
    "tests": 20,
    "ci": 20,
    "gitignore": 10,
    "contributing": 10,
    "manifest": 5,
    "security": 5,
}


@dataclass(frozen=True)
class RepoHealthReport:
    path: str
    score: int
    max_score: int
    passed_checks: int
    total_checks: int
    checks: dict[str, bool]
    missing: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "score": self.score,
            "max_score": self.max_score,
            "passed_checks": self.passed_checks,
            "total_checks": self.total_checks,
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
        "manifest": any(
            (root / name).exists()
            for name in ("pyproject.toml", "package.json", "Cargo.toml", "go.mod", "pom.xml")
        ),
        "security": _has_any(root, ("SECURITY", "SECURITY.*", "security", "security.*")),
    }
    score = sum(WEIGHTS[name] for name, passed in checks.items() if passed)
    missing = [name for name, passed in checks.items() if not passed]
    return RepoHealthReport(
        path=str(root),
        score=score,
        max_score=sum(WEIGHTS.values()),
        passed_checks=sum(1 for passed in checks.values() if passed),
        total_checks=len(checks),
        checks=checks,
        missing=missing,
    )
