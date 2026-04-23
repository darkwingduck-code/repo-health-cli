from __future__ import annotations

import json
from pathlib import Path

import pytest

from repo_health_cli.analyzer import analyze_repo
from repo_health_cli.cli import main


def write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_analyze_repo_scores_complete_repo(tmp_path: Path) -> None:
    write(tmp_path / "README.md", "# Demo")
    write(tmp_path / "LICENSE", "MIT")
    write(tmp_path / "tests" / "test_demo.py", "")
    write(tmp_path / ".github" / "workflows" / "ci.yml", "name: ci")

    report = analyze_repo(tmp_path)

    assert report.score == 100
    assert report.missing == []
    assert all(report.checks.values())


def test_analyze_repo_reports_missing_items(tmp_path: Path) -> None:
    write(tmp_path / "README.md", "# Demo")

    report = analyze_repo(tmp_path)

    assert report.score == 25
    assert report.checks["readme"] is True
    assert report.checks["license"] is False
    assert set(report.missing) == {"license", "tests", "ci"}


def test_cli_json_output(tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    write(tmp_path / "README.md", "# Demo")
    write(tmp_path / "LICENSE", "MIT")
    write(tmp_path / "tests" / "test_demo.py", "")
    monkeypatch.setattr("sys.argv", ["repo-health", str(tmp_path), "--json"])

    exit_code = main()
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["score"] == 75
    assert payload["checks"]["ci"] is False


def test_cli_errors_for_missing_path(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.argv", ["repo-health", "missing-path"])

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Path does not exist" in captured.err

