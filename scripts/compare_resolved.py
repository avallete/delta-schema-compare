#!/usr/bin/env python3
"""
Compare **closed** pgschema issues (Bug/Feature) against pgdelta test coverage.

While ``compare_issues.py`` looks at *open* pgschema issues (upcoming gaps),
this script looks at **resolved** issues — things pgschema has *already fixed*
that pg-delta may still not handle.  These are "historical gaps": pgschema
shipped a fix or feature, but the corresponding scenario has no test coverage
in pg-delta.

The script uses the same local-submodule search and GitHub Models LLM
evaluation approach as ``compare_issues.py``.

For each uncovered resolved issue a detailed GitHub issue is created in the
TARGET_REPO with labels ``resolved-in-pgschema`` and ``needs-test``.

Required environment variables:
    GITHUB_TOKEN        – GitHub token (read issues, write issues to this repo,
                          and access GitHub Models API).

Optional environment variables:
    PGSCHEMA_REPO       – GitHub repo to read issues from
                          (default: pgplex/pgschema).
    PGDELTA_LOCAL_PATH  – Local path to the pg-delta package inside the
                          pg-toolbelt submodule
                          (default: repos/pg-toolbelt/packages/pg-delta).
    PGSCHEMA_LOCAL_PATH – Local path to the pgschema submodule
                          (default: repos/pgschema).
    TARGET_REPO         – Repo where generated issues are created
                          (default: avallete/delta-schema-compare).
    MODEL               – GitHub Models model name
                          (default: claude-opus-4.6).
    DRY_RUN             – Set to "true" to skip issue creation (default: false).
"""

import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Optional

import requests
from openai import OpenAI
from review_memory import (
    build_fingerprint,
    get_git_head,
    is_covered_cache_hit,
    load_review_memory,
    record_review_result,
    save_review_memory,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")

PGSCHEMA_REPO: str = os.environ.get("PGSCHEMA_REPO", "pgplex/pgschema")
PGDELTA_LOCAL_PATH: Path = Path(
    os.environ.get("PGDELTA_LOCAL_PATH", "repos/pg-toolbelt/packages/pg-delta")
)
PGSCHEMA_LOCAL_PATH: Path = Path(
    os.environ.get("PGSCHEMA_LOCAL_PATH", "repos/pgschema")
)
TARGET_REPO: str = os.environ.get("TARGET_REPO", "avallete/delta-schema-compare")
MODEL: str = os.environ.get("MODEL", "claude-opus-4.6")
DRY_RUN: bool = os.environ.get("DRY_RUN", "false").lower() == "true"
REVIEW_MEMORY_PATH: Path = Path(
    os.environ.get("REVIEW_MEMORY_PATH", "benchmark/review-memory.json")
)

GITHUB_API = "https://api.github.com"
# GitHub Models endpoint – accessed with GITHUB_TOKEN, no extra API key needed.
GITHUB_MODELS_ENDPOINT = "https://models.inference.ai.azure.com"

TRACKING_LABEL = "resolved-in-pgschema"
NEEDS_TEST_LABEL = "needs-test"

_github_headers: dict[str, str] = {
    "Accept": "application/vnd.github.v3+json",
}

# Source file extensions to search inside local submodules
_SEARCH_EXTS = {".ts", ".go", ".sql"}


def _set_auth_header() -> None:
    if GITHUB_TOKEN:
        _github_headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------


def _get(url: str, params: Optional[dict] = None, retries: int = 3) -> requests.Response:
    """
    Issue a GET request to *url* with retry and rate-limit handling.

    If the GitHub API responds with a 403 that indicates rate limiting the
    function sleeps until the reset window has passed and then retries.
    """
    import time

    for attempt in range(retries):
        resp = requests.get(url, headers=_github_headers, params=params, timeout=30)
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset_ts = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(reset_ts - int(time.time()), 1) + 5
            logger.warning("Rate-limited. Waiting %d seconds…", wait)
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp
    resp.raise_for_status()
    return resp  # unreachable but satisfies type checkers


def paginate(url: str, params: Optional[dict] = None) -> list[dict]:
    """Collect all pages of a GitHub list endpoint."""
    results: list[dict] = []
    page = 1
    base_params = dict(params or {})
    base_params["per_page"] = 100
    while True:
        base_params["page"] = page
        resp = _get(url, base_params)
        data = resp.json()
        if not data:
            break
        results.extend(data)
        if len(data) < 100:
            break
        page += 1
    return results


# ---------------------------------------------------------------------------
# Fetch closed pgschema issues
# ---------------------------------------------------------------------------


def get_resolved_pgschema_issues() -> list[dict]:
    """Return all closed pgschema issues labelled Bug or Feature (deduped)."""
    url = f"{GITHUB_API}/repos/{PGSCHEMA_REPO}/issues"
    seen: set[int] = set()
    issues: list[dict] = []
    for label in ("Bug", "Feature"):
        for item in paginate(url, {"state": "closed", "labels": label}):
            # Skip pull requests
            if "pull_request" in item:
                continue
            if item["number"] not in seen:
                seen.add(item["number"])
                issues.append(item)
    return issues


# ---------------------------------------------------------------------------
# Local filesystem search (uses submodule clones)
# ---------------------------------------------------------------------------


def extract_keywords(title: str, body: str) -> list[str]:
    """
    Extract SQL-relevant search tokens from an issue title and body.

    Prefers words inside backtick spans (which may be multi-word SQL phrases),
    then falls back to plain-text tokens longer than 3 characters.
    Returns at most 8 unique, lower-cased tokens.
    """
    text = f"{title} {body or ''}"
    # Tokens from backtick spans (handles multi-word spans like `CREATE TABLE`)
    code_spans = re.findall(r"`([^`]{3,})`", text)
    code_words = [
        w for span in code_spans for w in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{2,}\b", span)
    ]
    # Plain-text tokens
    all_words = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]{3,})\b", text)

    stop = {
        "this", "that", "with", "from", "have", "been", "when", "will",
        "should", "would", "could", "schema", "issue", "table", "column",
        "index", "view", "function", "type", "default", "null", "true", "false",
        "postgres", "postgresql", "pgschema", "pgdelta",
    }
    seen: set[str] = set()
    result: list[str] = []
    for word in (code_words + all_words):
        lower = word.lower()
        if lower not in stop and lower not in seen:
            seen.add(lower)
            result.append(lower)
        if len(result) >= 8:
            break
    return result


def search_local_files(
    search_root: Path,
    keywords: list[str],
    max_files: int = 5,
) -> list[tuple[Path, str]]:
    """
    Walk *search_root* and return up to *max_files* (path, content) pairs
    for files that contain at least one of the given *keywords*.

    Only files with extensions in ``_SEARCH_EXTS`` are considered.
    """
    matches: list[tuple[Path, str]] = []
    for fpath in search_root.rglob("*"):
        if fpath.suffix not in _SEARCH_EXTS:
            continue
        try:
            content = fpath.read_text(errors="replace")
        except OSError:
            continue
        lower = content.lower()
        if any(kw in lower for kw in keywords):
            matches.append((fpath, content))
            if len(matches) >= max_files:
                break
    return matches


def has_local_coverage(issue: dict) -> bool:
    """
    Return True if *any* file in the local pg-delta codebase contains keywords
    extracted from the pgschema issue.

    This is a fast pre-filter before the more expensive LLM check.
    """
    title: str = issue.get("title", "")
    body: str = issue.get("body") or ""
    keywords = extract_keywords(title, body)

    # Search test files first, then source files
    for sub in ("tests", "src"):
        sub_path = PGDELTA_LOCAL_PATH / sub
        if not sub_path.exists():
            continue
        hits = search_local_files(sub_path, keywords[:5], max_files=1)
        if hits:
            logger.debug(
                "Keyword hit in %s for issue #%d",
                hits[0][0].relative_to(PGDELTA_LOCAL_PATH),
                issue["number"],
            )
            return True
    return False


def collect_pgdelta_snippets(issue: dict) -> list[str]:
    """
    Collect up to 4 relevant file excerpts from the pg-delta codebase for use
    as context in the LLM coverage check.
    """
    title: str = issue.get("title", "")
    body: str = issue.get("body") or ""
    keywords = extract_keywords(title, body)

    snippets: list[str] = []
    for sub in ("tests", "src"):
        if len(snippets) >= 4:
            break
        sub_path = PGDELTA_LOCAL_PATH / sub
        if not sub_path.exists():
            continue
        for fpath, content in search_local_files(sub_path, keywords[:6], max_files=4):
            if len(snippets) >= 4:
                break
            rel = fpath.relative_to(PGDELTA_LOCAL_PATH)
            excerpt = content[:4000]
            snippets.append(f"**File:** `{rel}`\n```\n{excerpt}\n```")
    return snippets


def collect_pgschema_snippets(issue: dict) -> list[str]:
    """
    Collect up to 2 relevant file excerpts from the pgschema codebase.
    """
    title: str = issue.get("title", "")
    body: str = issue.get("body") or ""
    keywords = extract_keywords(title, body)

    snippets: list[str] = []
    for sub in ("internal/diff", "ir"):
        if len(snippets) >= 2:
            break
        sub_path = PGSCHEMA_LOCAL_PATH / sub
        if not sub_path.exists():
            continue
        for fpath, content in search_local_files(sub_path, keywords[:4], max_files=2):
            if len(snippets) >= 2:
                break
            rel = fpath.relative_to(PGSCHEMA_LOCAL_PATH)
            excerpt = content[:3000]
            snippets.append(f"**File (pgschema):** `{rel}`\n```\n{excerpt}\n```")
    return snippets


# ---------------------------------------------------------------------------
# Duplicate-issue detection in TARGET_REPO
# ---------------------------------------------------------------------------


def get_tracked_issue_numbers(repo: str) -> set[int]:
    """
    Return pgschema issue numbers already tracked in *repo*
    (identified by the TRACKING_LABEL and a sentinel in the body).
    """
    url = f"{GITHUB_API}/repos/{repo}/issues"
    tracked: set[int] = set()
    for item in paginate(url, {"state": "all", "labels": TRACKING_LABEL}):
        body = item.get("body") or ""
        match = re.search(r"pgschema\s+issue\s+#(\d+)", body, re.IGNORECASE)
        if match:
            tracked.add(int(match.group(1)))
    return tracked


# ---------------------------------------------------------------------------
# Label management
# ---------------------------------------------------------------------------


def ensure_label(repo: str, name: str, color: str, description: str = "") -> None:
    """Create *name* in *repo* if it does not already exist."""
    check_url = f"{GITHUB_API}/repos/{repo}/labels/{requests.utils.quote(name)}"
    resp = requests.get(check_url, headers=_github_headers, timeout=30)
    if resp.status_code == 404:
        create_resp = requests.post(
            f"{GITHUB_API}/repos/{repo}/labels",
            headers=_github_headers,
            json={"name": name, "color": color, "description": description},
            timeout=30,
        )
        if not create_resp.ok:
            logger.warning(
                "Could not create label '%s' in %s: %s %s",
                name,
                repo,
                create_resp.status_code,
                create_resp.text,
            )


# ---------------------------------------------------------------------------
# GitHub Models (Copilot) LLM helpers
# ---------------------------------------------------------------------------

_llm_client: Optional[OpenAI] = None


def _get_llm_client() -> OpenAI:
    """
    Return an OpenAI-compatible client pointed at the GitHub Models endpoint.
    """
    global _llm_client
    if _llm_client is None:
        _llm_client = OpenAI(
            base_url=GITHUB_MODELS_ENDPOINT,
            api_key=GITHUB_TOKEN,
        )
    return _llm_client


COVERAGE_SYSTEM_PROMPT = """\
You are an expert in PostgreSQL tooling.  You will be given:
1. A GitHub issue from *pgschema* (a Go-based PostgreSQL declarative schema
   migration tool at pgplex/pgschema) that has been **closed / resolved**.
   This means pgschema has already fixed or implemented the described behaviour.
2. File excerpts from the *pg-delta* project (a TypeScript/Bun PostgreSQL
   schema diff tool at supabase/pg-toolbelt, package @supabase/pg-delta).

Decide whether the pg-delta excerpts already contain a test case or
implementation that **fully** covers the scenario described in the
(now-resolved) pgschema issue.

Rules:
- Only return {"covered": true} if there is clear evidence that pg-delta
  comprehensively addresses the exact scenario in the issue.
- If the snippets only partially address the issue, cover a related but
  different scenario, or merely import relevant packages without testing the
  behaviour, return {"covered": false}.
- If no snippets are provided, return {"covered": false}.

Reply ONLY with valid JSON:
{"covered": true}  or  {"covered": false}
"""

ISSUE_GENERATION_SYSTEM_PROMPT = """\
You are an expert PostgreSQL contributor familiar with both:
- *pgschema* (Go, pgplex/pgschema) – a declarative schema migration tool
- *pg-delta* (TypeScript/Bun, @supabase/pg-delta in supabase/pg-toolbelt) –
  a schema diff and migration-script generator

You are given a **closed / resolved** pgschema GitHub issue (Bug or Feature).
This means pgschema already handles this scenario correctly.  Your task is to
write a detailed, actionable issue to be filed in the *delta-schema-compare*
tracking repository, explaining what pg-delta is **still missing** — i.e. the
"historical gap" between what pgschema already supports and what pg-delta does
not yet cover.

The issue body MUST contain these exact markdown sections:
## Context
## Test Case to Reproduce
## Suggested Fix

Rules:
- "Context" must mention that pgschema has already resolved this issue and that
  pg-delta still lacks coverage.
- "Test Case to Reproduce" must include runnable SQL demonstrating the scenario.
- "Suggested Fix" must be specific: include a code sketch, file path hints, or
  algorithm description referencing pg-delta's TypeScript source layout
  (src/core/objects/, tests/integration/).
- Do NOT invent facts not present in the original issue.
- Keep the title concise (≤ 80 chars).

Reply ONLY with valid JSON:
{
  "title": "<issue title>",
  "body":  "<full markdown body>"
}
"""


def llm_has_coverage(pgschema_issue: dict, snippets: list[str]) -> bool:
    """Ask the LLM whether the provided pg-delta snippets cover the pgschema issue."""
    snippet_text = "\n\n---\n\n".join(snippets) if snippets else "(no relevant files found)"
    user_msg = (
        "### pgschema issue (resolved)\n"
        f"**Title:** {pgschema_issue['title']}\n\n"
        f"{pgschema_issue.get('body') or '*(no body)*'}\n\n"
        f"### pg-delta code excerpts\n{snippet_text}"
    )
    client = _get_llm_client()
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": COVERAGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    result = json.loads(resp.choices[0].message.content)
    return bool(result.get("covered", False))


def generate_tracking_issue(pgschema_issue: dict) -> dict[str, str]:
    """Use the LLM to generate a title + body for the tracking issue."""
    pgdelta_snippets = collect_pgdelta_snippets(pgschema_issue)
    pgschema_snippets = collect_pgschema_snippets(pgschema_issue)

    extra_ctx = ""
    if pgdelta_snippets:
        extra_ctx += "\n\n### Relevant pg-delta source excerpts\n" + "\n\n---\n\n".join(pgdelta_snippets)
    if pgschema_snippets:
        extra_ctx += "\n\n### Relevant pgschema source excerpts (for reference)\n" + "\n\n---\n\n".join(pgschema_snippets)

    user_msg = (
        "### Original pgschema issue (resolved)\n"
        f"**Title:** {pgschema_issue['title']}\n"
        f"**URL:** {pgschema_issue['html_url']}\n"
        f"**Labels:** {', '.join(l['name'] for l in pgschema_issue.get('labels', []))}\n"
        f"**State:** {pgschema_issue.get('state', 'closed')}\n\n"
        f"{pgschema_issue.get('body') or '*(no body)*'}"
        f"{extra_ctx}"
    )
    client = _get_llm_client()
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": ISSUE_GENERATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    return json.loads(resp.choices[0].message.content)


# ---------------------------------------------------------------------------
# Issue creation
# ---------------------------------------------------------------------------


def create_github_issue(
    repo: str,
    title: str,
    body: str,
    labels: list[str],
) -> dict:
    """Create an issue in *repo* and return the response JSON."""
    resp = requests.post(
        f"{GITHUB_API}/repos/{repo}/issues",
        headers=_github_headers,
        json={"title": title, "body": body, "labels": labels},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    _set_auth_header()

    if not GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN is not set – aborting.")
        sys.exit(1)

    logger.info("=== delta-schema-compare (resolved issues) starting ===")
    logger.info("pgschema repo      : %s", PGSCHEMA_REPO)
    logger.info("pg-delta local path: %s", PGDELTA_LOCAL_PATH)
    logger.info("pgschema local path: %s", PGSCHEMA_LOCAL_PATH)
    logger.info("target repo        : %s", TARGET_REPO)
    logger.info("model              : %s", MODEL)
    logger.info("dry run            : %s", DRY_RUN)
    logger.info("review memory path : %s", REVIEW_MEMORY_PATH)

    if not PGDELTA_LOCAL_PATH.exists():
        logger.error(
            "pg-delta path '%s' does not exist. "
            "Did you checkout with --recurse-submodules?",
            PGDELTA_LOCAL_PATH,
        )
        sys.exit(1)

    # ---- 1. Fetch closed pgschema issues ----
    logger.info("Fetching closed pgschema issues with Bug/Feature labels…")
    issues = get_resolved_pgschema_issues()
    logger.info("Found %d resolved issues to process.", len(issues))

    if not issues:
        logger.info("Nothing to do.")
        return

    # ---- 2. Ensure labels exist in target repo ----
    if not DRY_RUN:
        ensure_label(TARGET_REPO, TRACKING_LABEL, "1d76db", "Resolved in pgschema but not yet in pg-delta")
        ensure_label(TARGET_REPO, NEEDS_TEST_LABEL, "e4e669", "Needs a test case in pg-delta")

    # ---- 3. Find already-processed issues ----
    logger.info("Loading already-tracked resolved issue numbers…")
    tracked = get_tracked_issue_numbers(TARGET_REPO)
    logger.info("Already tracked: %d issue(s).", len(tracked))

    # ---- 3b. Load persisted review memory ----
    review_memory = load_review_memory(REVIEW_MEMORY_PATH)
    pgdelta_sha = get_git_head(PGDELTA_LOCAL_PATH)
    pgschema_sha = get_git_head(PGSCHEMA_LOCAL_PATH)
    logger.info("pg-delta HEAD       : %s", pgdelta_sha)
    logger.info("pgschema HEAD       : %s", pgschema_sha)

    # ---- 4. Process each issue ----
    created = 0
    skipped_tracked = 0
    skipped_covered = 0
    errors = 0

    for issue in issues:
        num: int = issue["number"]
        title: str = issue["title"]
        fingerprint = build_fingerprint(issue, pgdelta_sha, pgschema_sha)

        def remember(verdict: str) -> None:
            if record_review_result(review_memory, "resolved", issue, fingerprint, verdict):
                logger.debug("[#%d] Review memory updated (%s).", num, verdict)

        # "Tracked" is authoritative (issue already exists in TARGET_REPO), so it
        # takes precedence over review-memory cache checks.
        if num in tracked:
            logger.info("[#%d] Already tracked – skipping.", num)
            remember("tracked")
            skipped_tracked += 1
            continue

        if is_covered_cache_hit(review_memory, "resolved", num, fingerprint):
            logger.info("[#%d] Review-memory hit (still covered) – skipping.", num)
            skipped_covered += 1
            continue

        logger.info("[#%d] Checking pg-delta coverage for resolved issue: %s", num, title)

        # Fast local keyword check first
        covered_locally = has_local_coverage(issue)

        if covered_locally:
            # Keyword hit – use LLM to confirm full coverage
            snippets = collect_pgdelta_snippets(issue)
            covered_by_llm = llm_has_coverage(issue, snippets)
            if covered_by_llm:
                logger.info("[#%d] Fully covered in pg-delta – skipping.", num)
                remember("covered")
                skipped_covered += 1
                continue
            logger.info(
                "[#%d] Keyword hit but LLM says not fully covered – generating issue.", num
            )
        else:
            logger.info("[#%d] No local coverage found – generating tracking issue.", num)

        # ---- Generate issue with LLM ----
        try:
            generated = generate_tracking_issue(issue)
        except Exception as exc:
            logger.error("[#%d] LLM generation failed: %s", num, exc)
            remember("generation_error")
            errors += 1
            continue

        gen_title: str = generated.get("title", f"pgschema #{num}: {title}")
        gen_body: str = generated.get("body", "")

        # Append provenance footer (used for duplicate detection on future runs)
        gen_body += (
            f"\n\n---\n"
            f"*Automatically generated by "
            f"[delta-schema-compare](https://github.com/{TARGET_REPO}) "
            f"from resolved pgschema issue #{num}: {issue['html_url']}*"
        )

        if DRY_RUN:
            logger.info(
                "[#%d] DRY RUN – would create issue:\n  Title: %s\n  Body preview: %.200s",
                num,
                gen_title,
                gen_body,
            )
            remember("not_covered")
            created += 1
            continue

        try:
            new_issue = create_github_issue(
                TARGET_REPO,
                gen_title,
                gen_body,
                [TRACKING_LABEL, NEEDS_TEST_LABEL],
            )
            logger.info(
                "[#%d] Created issue in %s: %s", num, TARGET_REPO, new_issue["html_url"]
            )
            remember("not_covered")
            created += 1
        except requests.HTTPError as exc:
            logger.error("[#%d] Failed to create issue: %s", num, exc)
            remember("create_error")
            errors += 1

    try:
        save_review_memory(REVIEW_MEMORY_PATH, review_memory)
    except OSError as exc:
        logger.warning("Could not write review memory file '%s': %s", REVIEW_MEMORY_PATH, exc)

    # ---- Summary ----
    logger.info("=== Summary (resolved issues) ===")
    logger.info("Resolved issues processed: %d", len(issues))
    logger.info("Already tracked          : %d", skipped_tracked)
    logger.info("Covered in pgdelta       : %d", skipped_covered)
    logger.info("Issues created           : %d", created)
    logger.info("Errors                   : %d", errors)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
