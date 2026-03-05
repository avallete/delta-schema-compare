# delta-schema-compare

Automated comparison between [pgschema](https://github.com/pgplex/pgschema)
issues and the test coverage of
[@supabase/pg-delta](https://github.com/supabase/pg-toolbelt/tree/main/packages/pg-delta).

Both upstream codebases are included as **git submodules**, making it easy to
browse the source locally or with the GitHub Copilot coding agent.

## What it does

### Open issues (daily)

A scheduled GitHub Actions workflow runs **every day at 08:00 UTC** and:

1. **Fetches** all open pgschema issues labelled **Bug** or **Feature**.
2. **Checks** whether the pg-delta codebase (local submodule) already contains
   a test case or implementation that covers the exact scenario described in
   each issue — using local filesystem search followed by LLM evaluation via
   the **GitHub Models API** (no separate API key needed).
3. **Generates** a detailed tracking issue (via GitHub Copilot / GitHub Models)
   for any uncovered case, including:
   - **Context** – how the pgschema issue relates to pg-delta.
   - **Test Case to Reproduce** – runnable SQL.
   - **Suggested Fix** – a concrete code sketch referencing pg-delta source paths.
4. **Creates** the generated issue in **this repository** with the labels
   `from-pgschema` and `needs-test`.

### Resolved issues — historical gaps (weekly)

A second workflow runs **every Monday at 09:00 UTC** and looks at the other
side of the coin: pgschema issues that have been **closed / resolved**.  These
represent bugs already fixed or features already implemented in pgschema.  If
pg-delta still lacks test coverage for the same scenario, there is a
"historical gap" — pgschema is ahead and pg-delta needs to catch up.

1. **Fetches** all closed pgschema issues labelled **Bug** or **Feature**.
2. **Checks** pg-delta coverage the same way (local search + LLM evaluation).
3. **Creates** a tracking issue with the labels `resolved-in-pgschema` and
   `needs-test` for each unresolved gap.

Duplicate detection ensures each pgschema issue is processed only once.

## Repository structure

```
.github/
  copilot-instructions.md    Copilot agent context for this repo
  workflows/
    compare-issues.yml       Daily workflow – open issues
    compare-resolved.yml     Weekly workflow – resolved / historical gaps
docs/
  pgdelta-structure.md       pg-delta codebase map and test anatomy
  coverage-guide.md          How to evaluate coverage and write tracking issues
repos/
  pgschema/                  git submodule – pgplex/pgschema (Go)
  pg-toolbelt/               git submodule – supabase/pg-toolbelt (TypeScript)
    packages/pg-delta/       @supabase/pg-delta source and tests
scripts/
  compare_issues.py          Open-issue comparison and generation script
  compare_resolved.py        Resolved-issue (historical gap) comparison script
requirements.txt             Python dependencies (Python 3.11+)
```

## Setup

### Required secrets

| Secret | Description |
|---|---|
| *(none extra)* | `GITHUB_TOKEN` is provided automatically by GitHub Actions |

The script uses the **GitHub Models API** (endpoint:
`https://models.inference.ai.azure.com`) with the workflow's `GITHUB_TOKEN`.
No `OPENAI_API_KEY` is required.

### Workflow dispatch inputs

Both workflows accept the same inputs:

| Input | Default | Description |
|---|---|---|
| `dry_run` | `false` | Log what would be created without creating issues |
| `model` | `claude-opus-4.6` | GitHub Models model for coverage evaluation and generation |

## Running locally

**Requirements:** Python 3.11+, git with submodule support.

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/avallete/delta-schema-compare
cd delta-schema-compare

# Or, if already cloned:
git submodule update --init --recursive

# Install Python dependencies
pip install -r requirements.txt

# Run (dry run recommended for local testing)
export GITHUB_TOKEN=ghp_...
export DRY_RUN=true

python scripts/compare_issues.py          # open issues
python scripts/compare_resolved.py       # resolved / historical gaps
```

## Using the Copilot coding agent

Because both upstream repos are available as local submodules, the GitHub
Copilot coding agent can browse them directly.  The file
`.github/copilot-instructions.md` provides Copilot with the context it needs
to:

- Locate the right test files in `repos/pg-toolbelt/packages/pg-delta/tests/`
- Understand the roundtrip fidelity test pattern
- Generate well-structured tracking issues following the template in
  `docs/coverage-guide.md`

To trigger the agent manually: open a new issue or comment, mention
`@github-copilot`, and describe which pgschema issue you want analysed.

## Labels used in this repo

| Label | Meaning |
|---|---|
| `from-pgschema` | Issue was auto-generated from an **open** pgschema Bug/Feature issue |
| `resolved-in-pgschema` | Issue was auto-generated from a **closed** pgschema issue (historical gap) |
| `needs-test` | A pg-delta integration test case is needed for this scenario |
