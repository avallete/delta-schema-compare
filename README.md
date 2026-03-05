# delta-schema-compare

Automated comparison tool that bridges open issues in
[pgschema](https://github.com/pgplex/pgschema) with the
[pgdelta](https://github.com/supabase/pg-toolbelt) codebase.

## What it does

A scheduled GitHub Actions workflow runs weekly and:

1. **Fetches** all open pgschema issues labelled **Bug** or **Feature**.
2. **Checks** whether the [pgdelta](https://github.com/supabase/pg-toolbelt/tree/main/pgdelta)
   codebase already contains a test case or implementation that covers the scenario described
   in each issue (keyword search + LLM evaluation).
3. **Generates** a detailed issue (via OpenAI) for any uncovered case, including:
   - **Context** – how the pgschema issue relates to pgdelta.
   - **Test Case to Reproduce** – runnable SQL.
   - **Suggested Fix** – a concrete code sketch or algorithm outline.
4. **Creates** the generated issue in the configured `TARGET_REPO`
   (defaults to this repository) with the labels `from-pgschema` and `needs-test`.

Duplicate detection ensures each pgschema issue is processed only once.

## Setup

### Required secrets

| Secret | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key (used for coverage evaluation and issue generation) |

`GITHUB_TOKEN` is provided automatically by GitHub Actions.

### Optional variables (workflow dispatch inputs)

| Input | Default | Description |
|---|---|---|
| `dry_run` | `false` | Log what would be created without actually creating issues |
| `pgschema_repo` | `pgplex/pgschema` | Source repository for Bug/Feature issues |
| `pgdelta_repo` | `supabase/pg-toolbelt` | Repository hosting the pgdelta tool |
| `pgdelta_path` | `pgdelta` | Sub-path inside the pgdelta repo to scope code search |
| `target_repo` | `avallete/delta-schema-compare` | Where generated issues are filed |
| `openai_model` | `gpt-4o-mini` | OpenAI chat model to use |

> **Note:** If `TARGET_REPO` is an external repository, replace `GITHUB_TOKEN` with a
> fine-grained PAT (stored as a repository secret named `GH_PAT`) that has **Issues: write**
> permission on that repository, and update the workflow to use
> `${{ secrets.GH_PAT }}` instead of `${{ secrets.GITHUB_TOKEN }}`.

## Running locally

**Requirements:** Python 3.11+

```bash
pip install -r requirements.txt

export GITHUB_TOKEN=ghp_...
export OPENAI_API_KEY=sk-...
export TARGET_REPO=avallete/delta-schema-compare
export DRY_RUN=true   # optional – skip issue creation

python scripts/compare_issues.py
```

## Project structure

```
.github/
  workflows/
    compare-issues.yml   # Scheduled + manual-dispatch workflow
scripts/
  compare_issues.py      # Main comparison & generation script
requirements.txt         # Python dependencies
```
