#!/usr/bin/env python3
"""
Compare open pgschema issues (Bug/Feature) against pgdelta test coverage.

For each uncovered issue, an LLM generates a detailed issue (context, test case,
suggested fix) and creates it in the configured TARGET_REPO.

Required environment variables:
    GITHUB_TOKEN   – GitHub token with read access to source repos and write
                     access to TARGET_REPO.
    OPENAI_API_KEY – OpenAI API key used to evaluate coverage and generate issues.

Optional environment variables:
    PGSCHEMA_REPO  – Source issue repository (default: pgplex/pgschema).
    PGDELTA_REPO   – Repository that hosts the pgdelta tool
                     (default: supabase/pg-toolbelt).
    PGDELTA_PATH   – Sub-path inside PGDELTA_REPO to restrict code search
                     (default: pgdelta).
    TARGET_REPO    – Repository where generated issues are created
                     (default: avallete/delta-schema-compare).
    OPENAI_MODEL   – OpenAI chat model to use (default: gpt-4o-mini).
    DRY_RUN        – Set to "true" to skip issue creation (default: false).
"""

import json
import logging
import os
import re
import sys
import time
from typing import Optional

import requests
from openai import OpenAI

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")

PGSCHEMA_REPO: str = os.environ.get("PGSCHEMA_REPO", "pgplex/pgschema")
PGDELTA_REPO: str = os.environ.get("PGDELTA_REPO", "supabase/pg-toolbelt")
PGDELTA_PATH: str = os.environ.get("PGDELTA_PATH", "pgdelta")
TARGET_REPO: str = os.environ.get("TARGET_REPO", "avallete/delta-schema-compare")
OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
DRY_RUN: bool = os.environ.get("DRY_RUN", "false").lower() == "true"

GITHUB_API = "https://api.github.com"
# Label applied to generated issues so we can detect duplicates later.
TRACKING_LABEL = "from-pgschema"
NEEDS_TEST_LABEL = "needs-test"

_github_headers: dict[str, str] = {
    "Accept": "application/vnd.github.v3+json",
}


def _set_auth_header() -> None:
    if GITHUB_TOKEN:
        _github_headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------


def _get(url: str, params: Optional[dict] = None, retries: int = 3) -> requests.Response:
    """
    Issue a GET request to *url* with retry and rate-limit handling.

    If the GitHub API responds with a 403 that indicates rate limiting, the
    function sleeps until the reset window has passed and then retries.
    Non-rate-limit HTTP errors are re-raised immediately after exhausting
    retries.

    Args:
        url:     Full URL to request.
        params:  Optional query-string parameters.
        retries: Maximum number of attempts before raising.

    Returns:
        A :class:`requests.Response` with a 2xx or 422 status code.
    """
    for attempt in range(retries):
        resp = requests.get(url, headers=_github_headers, params=params, timeout=30)
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset_ts = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(reset_ts - int(time.time()), 1) + 5
            logger.warning("Rate-limited. Waiting %d seconds…", wait)
            time.sleep(wait)
            continue
        if resp.status_code == 422:
            # Unprocessable – usually a search with no results
            return resp
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
# Fetch pgschema issues
# ---------------------------------------------------------------------------


def get_pgschema_issues() -> list[dict]:
    """Return all open pgschema issues labelled Bug or Feature (deduped)."""
    url = f"{GITHUB_API}/repos/{PGSCHEMA_REPO}/issues"
    seen: set[int] = set()
    issues: list[dict] = []
    for label in ("Bug", "Feature"):
        for item in paginate(url, {"state": "open", "labels": label}):
            # Skip pull requests
            if "pull_request" in item:
                continue
            if item["number"] not in seen:
                seen.add(item["number"])
                issues.append(item)
    return issues


# ---------------------------------------------------------------------------
# pgdelta coverage check
# ---------------------------------------------------------------------------


def _code_search(query: str) -> int:
    """Return the total_count for a GitHub code search query.

    A 1-second pause is inserted before every call to stay comfortably within
    GitHub's secondary rate limit for code search (10 requests per minute for
    authenticated users).
    """
    time.sleep(1)
    resp = _get(f"{GITHUB_API}/search/code", {"q": query, "per_page": 1})
    if resp.status_code in (422, 503):
        return 0
    return resp.json().get("total_count", 0)


def extract_sql_keywords(title: str, body: str) -> list[str]:
    """
    Pull SQL-ish keywords from an issue.  We look for:
      - words that appear in both backtick spans and plain text
      - common PostgreSQL object names (TABLE, VIEW, INDEX, …)
    Returns at most 6 unique, lower-cased tokens > 3 chars.
    """
    text = f"{title} {body or ''}"
    # Prefer words/phrases inside code/backtick spans (may contain whitespace)
    code_spans = re.findall(r"`([^`]{3,})`", text)
    # Flatten multi-word spans into individual tokens
    code_words = [w for span in code_spans for w in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{2,}\b", span)]
    # All words longer than 3 chars from plain text
    all_words = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]{3,})\b", text)
    candidates = [w.lower() for w in (code_words + all_words)]
    stop = {
        "this", "that", "with", "from", "have", "been", "when", "will",
        "should", "would", "could", "schema", "issue", "table", "column",
        "index", "view", "function", "type", "default", "null",
    }
    seen: set[str] = set()
    result: list[str] = []
    for word in candidates:
        if word not in stop and word not in seen:
            seen.add(word)
            result.append(word)
        if len(result) >= 6:
            break
    return result


def has_pgdelta_coverage(issue: dict) -> bool:
    """
    Return True if there is *any* evidence in the pgdelta codebase that the
    issue is already addressed (test file, source file, or referenced issue).
    """
    title: str = issue.get("title", "")
    body: str = issue.get("body") or ""
    issue_number: int = issue["number"]

    base_query = f"repo:{PGDELTA_REPO} path:{PGDELTA_PATH}"

    # 1. Direct mention of the pgschema issue number
    if _code_search(f"{base_query} pgschema#{issue_number}") > 0:
        return True

    # 2. Keyword search against test files
    keywords = extract_sql_keywords(title, body)
    for keyword in keywords[:4]:
        q = f"{base_query} {keyword}"
        if _code_search(q) > 0:
            logger.debug("Keyword '%s' found in pgdelta – treating as covered", keyword)
            return True

    return False


# ---------------------------------------------------------------------------
# Duplicate-issue detection in TARGET_REPO
# ---------------------------------------------------------------------------


def get_tracked_issue_numbers(repo: str) -> set[int]:
    """
    Return pgschema issue numbers that have already been created in TARGET_REPO
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
    """Create a label in *repo* if it does not already exist."""
    url = f"{GITHUB_API}/repos/{repo}/labels/{requests.utils.quote(name)}"
    resp = requests.get(url, headers=_github_headers, timeout=30)
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
                name, repo, create_resp.status_code, create_resp.text,
            )


# ---------------------------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------------------------

_openai_client: Optional[OpenAI] = None


def _get_openai_client() -> OpenAI:
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=OPENAI_API_KEY)
    return _openai_client


COVERAGE_SYSTEM_PROMPT = """\
You are an expert in PostgreSQL tooling.  You will be given:
1. A GitHub issue from *pgschema* (a PostgreSQL schema introspection library).
2. A list of code snippets retrieved from the *pgdelta* project (a PostgreSQL
   schema diff / migration generator inside supabase/pg-toolbelt).

Decide whether the pgdelta snippets already contain a **test case** or
**implementation** that fully covers the scenario described in the pgschema issue.

Rules:
- Only return {"covered": true} if there is clear evidence that the pgdelta
  codebase comprehensively addresses the exact scenario in the issue.
- If the snippets only partially address the issue, cover a related but different
  scenario, or merely import relevant packages without testing the behaviour,
  return {"covered": false}.
- If no snippets were provided, return {"covered": false}.

Reply ONLY with valid JSON:
{"covered": true}  or  {"covered": false}
"""

ISSUE_GENERATION_SYSTEM_PROMPT = """\
You are an expert PostgreSQL and open-source contributor.
Given a GitHub issue from *pgschema* (a PostgreSQL schema introspection library),
write a detailed, actionable issue for the *pgdelta* project
(supabase/pg-toolbelt pgdelta tool).

The issue must contain these exact markdown sections:
## Context
## Test Case to Reproduce
## Suggested Fix

Rules:
- The "Test Case to Reproduce" section must include runnable SQL.
- The "Suggested Fix" must be specific (code sketch or algorithm description).
- Do NOT invent facts not present in the original issue.
- Keep the title concise (≤ 80 chars).

Reply ONLY with valid JSON:
{
  "title": "<issue title>",
  "body":  "<full markdown body>"
}
"""


def llm_has_coverage(pgschema_issue: dict, snippets: list[str]) -> bool:
    """Ask the LLM whether the provided snippets cover the pgschema issue."""
    snippet_text = "\n\n---\n\n".join(snippets) if snippets else "(no snippets found)"
    user_msg = (
        f"### pgschema issue\n"
        f"**Title:** {pgschema_issue['title']}\n\n"
        f"{pgschema_issue.get('body') or '*(no body)*'}\n\n"
        f"### pgdelta code snippets\n{snippet_text}"
    )
    client = _get_openai_client()
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": COVERAGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    result = json.loads(resp.choices[0].message.content)
    return bool(result.get("covered", False))


def generate_pgdelta_issue(pgschema_issue: dict) -> dict[str, str]:
    """Use the LLM to generate a title + body for a new pgdelta issue."""
    user_msg = (
        f"### Original pgschema issue\n"
        f"**Title:** {pgschema_issue['title']}\n"
        f"**URL:** {pgschema_issue['html_url']}\n"
        f"**Labels:** {', '.join(l['name'] for l in pgschema_issue.get('labels', []))}\n\n"
        f"{pgschema_issue.get('body') or '*(no body)*'}"
    )
    client = _get_openai_client()
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": ISSUE_GENERATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    return json.loads(resp.choices[0].message.content)


# ---------------------------------------------------------------------------
# Fetch relevant pgdelta snippets for LLM coverage check
# ---------------------------------------------------------------------------


def fetch_pgdelta_snippets(issue: dict) -> list[str]:
    """
    Retrieve up to 3 file contents from pgdelta that are most likely related
    to the pgschema issue, using GitHub code search.
    """
    title: str = issue.get("title", "")
    body: str = issue.get("body") or ""
    keywords = extract_sql_keywords(title, body)

    seen_urls: set[str] = set()
    snippets: list[str] = []

    for keyword in keywords[:4]:
        if len(snippets) >= 3:
            break
        time.sleep(1)
        q = f"repo:{PGDELTA_REPO} path:{PGDELTA_PATH} {keyword}"
        resp = _get(f"{GITHUB_API}/search/code", {"q": q, "per_page": 3})
        if resp.status_code not in (200,):
            continue
        items = resp.json().get("items", [])
        for item in items:
            raw_url = item.get("html_url", "").replace(
                "github.com", "raw.githubusercontent.com"
            ).replace("/blob/", "/")
            if raw_url in seen_urls or not raw_url:
                continue
            seen_urls.add(raw_url)
            try:
                file_resp = requests.get(raw_url, timeout=30)
                if file_resp.status_code == 200:
                    # Truncate large files to ~1 000 tokens (~4 000 chars) so
                    # the combined snippet payload stays within LLM context limits.
                    content = file_resp.text[:4000]
                    snippets.append(f"**File:** {item.get('path', raw_url)}\n```\n{content}\n```")
            except requests.RequestException:
                pass
            if len(snippets) >= 3:
                break

    return snippets


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

    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY is not set – aborting.")
        sys.exit(1)

    logger.info("=== delta-schema-compare starting ===")
    logger.info("pgschema repo : %s", PGSCHEMA_REPO)
    logger.info("pgdelta repo  : %s / %s", PGDELTA_REPO, PGDELTA_PATH)
    logger.info("target repo   : %s", TARGET_REPO)
    logger.info("dry run       : %s", DRY_RUN)

    # ---- 1. Fetch open pgschema issues ----
    logger.info("Fetching open pgschema issues with Bug/Feature labels…")
    issues = get_pgschema_issues()
    logger.info("Found %d issues to process.", len(issues))

    if not issues:
        logger.info("Nothing to do.")
        return

    # ---- 2. Ensure labels exist in target repo ----
    if not DRY_RUN:
        ensure_label(TARGET_REPO, TRACKING_LABEL, "0075ca", "Mirrored from pgschema")
        ensure_label(TARGET_REPO, NEEDS_TEST_LABEL, "e4e669", "Needs a test case in pgdelta")

    # ---- 3. Find already-processed issues ----
    logger.info("Loading already-tracked issue numbers…")
    tracked = get_tracked_issue_numbers(TARGET_REPO)
    logger.info("Already tracked: %d issue(s).", len(tracked))

    # ---- 4. Process each issue ----
    created = 0
    skipped_tracked = 0
    skipped_covered = 0
    errors = 0

    for issue in issues:
        num: int = issue["number"]
        title: str = issue["title"]

        if num in tracked:
            logger.info("[#%d] Already tracked – skipping.", num)
            skipped_tracked += 1
            continue

        logger.info("[#%d] Checking pgdelta coverage for: %s", num, title)

        # Fast keyword check first
        covered_by_keyword = has_pgdelta_coverage(issue)

        if covered_by_keyword:
            # Quick check says covered; use LLM to confirm
            snippets = fetch_pgdelta_snippets(issue)
            covered_by_llm = llm_has_coverage(issue, snippets)
            if covered_by_llm:
                logger.info("[#%d] Covered in pgdelta – skipping.", num)
                skipped_covered += 1
                continue
            logger.info(
                "[#%d] Keyword hit but LLM says not fully covered – generating issue.", num
            )
        else:
            logger.info("[#%d] No coverage found – generating pgdelta issue.", num)

        # ---- Generate issue with LLM ----
        try:
            generated = generate_pgdelta_issue(issue)
        except Exception as exc:
            logger.error("[#%d] LLM generation failed: %s", num, exc)
            errors += 1
            continue

        gen_title: str = generated.get("title", f"pgschema #{num}: {title}")
        gen_body: str = generated.get("body", "")

        # Append provenance footer
        gen_body += (
            f"\n\n---\n"
            f"*This issue was automatically generated by "
            f"[delta-schema-compare](https://github.com/{TARGET_REPO}) "
            f"from pgschema issue #{num}: {issue['html_url']}*"
        )

        if DRY_RUN:
            logger.info(
                "[#%d] DRY RUN – would create issue:\n  Title: %s\n  Body preview: %.200s",
                num,
                gen_title,
                gen_body,
            )
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
            created += 1
        except requests.HTTPError as exc:
            logger.error("[#%d] Failed to create issue: %s", num, exc)
            errors += 1

    # ---- Summary ----
    logger.info("=== Summary ===")
    logger.info("Issues processed  : %d", len(issues))
    logger.info("Already tracked   : %d", skipped_tracked)
    logger.info("Covered in pgdelta: %d", skipped_covered)
    logger.info("Issues created    : %d", created)
    logger.info("Errors            : %d", errors)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
