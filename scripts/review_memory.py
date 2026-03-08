"""Helpers for persisting issue review results between script runs."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def get_git_head(path: Path) -> str:
    """Return ``git rev-parse HEAD`` for *path*, or ``"unknown"`` on failure."""
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def load_review_memory(path: Path) -> dict[str, dict[str, dict[str, Any]]]:
    """Load the review-memory JSON file from *path*."""
    if not path.exists():
        return {"open": {}, "resolved": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"open": {}, "resolved": {}}

    if not isinstance(data, dict):
        return {"open": {}, "resolved": {}}

    data.setdefault("open", {})
    data.setdefault("resolved", {})
    return data


def save_review_memory(path: Path, memory: dict[str, dict[str, dict[str, Any]]]) -> None:
    """Persist *memory* to *path*."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(memory, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_fingerprint(issue: dict, pgdelta_sha: str, pgschema_sha: str) -> str:
    """Build a stable fingerprint to detect whether an issue review is stale."""
    payload = {
        "issue_updated_at": issue.get("updated_at"),
        "pgdelta_sha": pgdelta_sha,
        "pgschema_sha": pgschema_sha,
    }
    return json.dumps(payload, sort_keys=True)


def is_covered_cache_hit(
    memory: dict[str, dict[str, dict[str, Any]]],
    scope: str,
    issue_number: int,
    fingerprint: str,
) -> bool:
    """
    Return True when *issue_number* in *scope* was previously marked as covered
    using the same *fingerprint*.
    """
    entry = memory.get(scope, {}).get(str(issue_number))
    if not isinstance(entry, dict):
        return False
    return (
        entry.get("fingerprint") == fingerprint
        and entry.get("verdict") == "covered"
    )


def record_review_result(
    memory: dict[str, dict[str, dict[str, Any]]],
    scope: str,
    issue: dict,
    fingerprint: str,
    verdict: str,
) -> bool:
    """Record the latest review result for *issue* under *scope*."""
    memory.setdefault(scope, {})
    issue_key = str(issue["number"])
    existing = memory[scope].get(issue_key)
    if (
        isinstance(existing, dict)
        and existing.get("fingerprint") == fingerprint
        and existing.get("verdict") == verdict
    ):
        return False

    memory[scope][issue_key] = {
        "issue_number": issue["number"],
        "issue_title": issue.get("title", ""),
        "issue_url": issue.get("html_url", ""),
        "issue_updated_at": issue.get("updated_at"),
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "fingerprint": fingerprint,
        "verdict": verdict,
    }
    return True
