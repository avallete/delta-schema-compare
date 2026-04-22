---
# Fill in the fields below to create a basic custom agent for your repository.
# The Copilot CLI can be used for local testing: https://gh.io/customagents/cli
# To make this agent available, merge this file into the default repository branch.
# For format details, see: https://gh.io/customagents/config

name: delta-schema-compare
description: Agent to compare pg-delta and pgschema features and bug parity
---

# delta-schema-compare

## Purpose

This repository automatically compares [pgschema](https://github.com/pgplex/pgschema) (a Go-based declarative schema migration tool) against [@supabase/pg-delta](https://github.com/supabase/pg-toolbelt/tree/main/packages/pg-delta) (a TypeScript/Bun schema diff tool) to identify coverage gaps. When pgschema tracks a bug or feature that pg-delta does not yet handle, this repo creates actionable tracking issues with reproduction SQL and suggested fixes.

---

## Quick Start

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/avallete/delta-schema-compare
cd delta-schema-compare

# Or, if already cloned:
git submodule update --init --recursive

# Update submodules to latest upstream
git submodule update --remote --merge

# Install Python dependencies (for running automation scripts)
pip install -r requirements.txt
```

---

## File Structure

```
.github/
  copilot-instructions.md        Copilot agent context for this repo
  workflows/
    compare-issues.yml           Daily workflow — open pgschema issues
    compare-resolved.yml         Weekly workflow — resolved / historical gaps
docs/
  coverage-guide.md              How to evaluate coverage and write tracking issues
  pgdelta-structure.md           pg-delta codebase map and integration test anatomy
repos/
  pgschema/                      git submodule — pgplex/pgschema (Go)
  pg-toolbelt/                   git submodule — supabase/pg-toolbelt (TypeScript)
    packages/pg-delta/           @supabase/pg-delta source and tests
scripts/
  compare_issues.py              Open-issue comparison and generation script
  compare_resolved.py            Resolved-issue (historical gap) comparison script
benchmark/
  001-exclude-constraints.md     15 documented gap analyses (001–015)
  ...
  README.md                      Summary table of all benchmarked gaps
requirements.txt                 Python dependencies (Python 3.11+)
```

---

## Submodule Paths

| Alias    | Path                                   | Upstream                                                                                                   |
| -------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| pgschema | `repos/pgschema/`                      | [pgplex/pgschema](https://github.com/pgplex/pgschema) — Go                                                 |
| pg-delta | `repos/pg-toolbelt/packages/pg-delta/` | [@supabase/pg-delta](https://github.com/supabase/pg-toolbelt/tree/main/packages/pg-delta) — TypeScript/Bun |

---

## Upstream Sources to Monitor

An agent working on this repo needs to consult **multiple upstream sources** beyond the local submodules:

### pgschema (Go) — what to watch

| Source        | URL                                                              | Why                                                        |
| ------------- | ---------------------------------------------------------------- | ---------------------------------------------------------- |
| Open issues   | `https://github.com/pgplex/pgschema/issues?q=is:issue+is:open`   | New bugs/features that pg-delta may not cover              |
| Closed issues | `https://github.com/pgplex/pgschema/issues?q=is:issue+is:closed` | Historical gaps — pgschema fixed it, pg-delta may not have |
| Merged PRs    | `https://github.com/pgplex/pgschema/pulls?q=is:pr+is:merged`     | Implementation details, test data, reproduction SQL        |

When evaluating a pgschema issue, **always check merged PRs** that reference the issue — they contain the actual fix, test cases, and SQL that reveal the exact behaviour pgschema now handles.

### pg-delta (TypeScript) — what to watch

| Source        | URL                                                    | Why                                               |
| ------------- | ------------------------------------------------------ | ------------------------------------------------- |
| Latest source | Local submodule `repos/pg-toolbelt/packages/pg-delta/` | Current implementation and test coverage          |
| Open issues   | `https://github.com/supabase/pg-toolbelt/issues`       | Known bugs / planned features — avoid duplicates  |
| Open PRs      | `https://github.com/supabase/pg-toolbelt/pulls`        | In-progress work — a gap may already be addressed |

Before creating a tracking issue, **check pg-delta's open issues and PRs** to avoid duplicating work that is already in progress or planned.

---

## Automation Workflows

### Daily — Open Issues (`compare-issues.yml`)

- **Schedule:** Every day at 08:00 UTC
- **Script:** `python scripts/compare_issues.py`
- **What it does:** Fetches open pgschema issues (currently filtered by `Bug`/`Feature` labels), checks pg-delta coverage via local search + LLM evaluation, creates tracking issues for uncovered gaps.
- **Labels applied:** `from-pgschema`, `needs-test`

### Weekly — Resolved Issues (`compare-resolved.yml`)

- **Schedule:** Every Monday at 09:00 UTC
- **Script:** `python scripts/compare_resolved.py`
- **What it does:** Fetches closed pgschema issues (currently filtered by `Bug`/`Feature` labels), checks if pg-delta still lacks coverage for the resolved scenario, creates tracking issues for historical gaps.
- **Labels applied:** `resolved-in-pgschema`, `needs-test`

### Running locally

```bash
export GITHUB_TOKEN=ghp_...
export DRY_RUN=true          # recommended for local testing

python scripts/compare_issues.py     # open issues
python scripts/compare_resolved.py   # resolved / historical gaps
```

### Workflow dispatch inputs

| Input     | Default           | Description                                       |
| --------- | ----------------- | ------------------------------------------------- |
| `dry_run` | `false`           | Log what would be created without creating issues |
| `model`   | `claude-opus-4.6` | GitHub Models model for coverage evaluation       |

---

## Benchmark → issue workflow SOP (required order)

When asked to create issues from the benchmark, always follow this order:

### 1) Map benchmark entries to pg-delta issues/PRs first

For each benchmark item:

1. Find matching pg-toolbelt issue(s) and PR(s).
2. Refresh the benchmark status as one of:
   - **covered** (fix merged and behavior is now covered),
   - **tracked** (issue/PR exists but is still in progress),
   - **not_covered** (no effective fix yet).
3. Update benchmark docs + `benchmark/review-memory.json` before drafting any
   new issue.

### 2) Find missing pg-toolbelt issues second

After status refresh:

1. Screen remaining pgschema scenarios that are not represented.
2. Check duplicates in pg-toolbelt issues and PRs.
3. Prepare issue drafts in markdown first (do not open immediately), each with:
   - context,
   - runnable MRE SQL,
   - concrete suggested fix paths.

This ordering prevents duplicate issue creation and keeps benchmark state
accurate before proposing net-new tracker issues.

### Label-filter caveat

Current automation scripts filter pgschema issues by `Bug`/`Feature` labels.
If upstream issues are unlabeled, script runs may miss relevant items; in that
case, do a manual issue/PR scan and record findings in benchmark memory/docs.

---

## Core Task: Evaluating Coverage

This is the primary task agents perform. Follow these four steps:

### Step 1 — Understand the pgschema issue

Read the issue title, body, and **any linked merged PRs**. Answer:

1. What **PostgreSQL object type** is involved? (table, index, constraint, view, function, trigger, type, policy, sequence, etc.)
2. What **specific DDL operation** or **behaviour** is wrong/missing? (e.g. `ALTER COLUMN TYPE ... USING`, `CREATE INDEX CONCURRENTLY` on partitioned table)
3. What **SQL** reproduces the problem?
4. Was the issue **fixed via a merged PR**? If so, what test cases / SQL does the PR contain?

### Step 2 — Search for coverage in pg-delta

#### 2a. Find the right test file

Integration tests live in `repos/pg-toolbelt/packages/pg-delta/tests/integration/`. Use this lookup table:

| Object type             | Test file                                               |
| ----------------------- | ------------------------------------------------------- |
| TABLE / columns         | `alter-table-operations.test.ts`                        |
| INDEX                   | `index-operations.test.ts`                              |
| CONSTRAINT              | `constraint-operations.test.ts`                         |
| FUNCTION                | `function-operations.test.ts`                           |
| VIEW                    | `catalog-diff.test.ts` or `mixed-objects.test.ts`       |
| MATERIALIZED VIEW       | `materialized-view-operations.test.ts`                  |
| POLICY / RLS            | `rls-operations.test.ts`, `policy-dependencies.test.ts` |
| SEQUENCE                | `sequence-operations.test.ts`                           |
| TYPE (enum / composite) | `catalog-diff.test.ts`                                  |
| TRIGGER                 | `catalog-diff.test.ts`                                  |
| AGGREGATE               | `aggregate-operations.test.ts`                          |
| PUBLICATION             | `publication-operations.test.ts`                        |
| SUBSCRIPTION            | `subscription-operations.test.ts`                       |
| EXTENSION               | `extension-operations.test.ts`                          |
| FDW                     | `foreign-data-wrapper-operations.test.ts`               |
| EVENT TRIGGER           | `event-trigger-operations.test.ts`                      |

#### 2b. Check whether the _specific scenario_ is tested

Open the test file and look for `initialSetup` / `testSql` blocks that match the scenario. **Having a test for the object type is not enough** — the exact behaviour must be present.

```bash
grep -rni "<keyword>" repos/pg-toolbelt/packages/pg-delta/tests/
```

#### 2c. Check the source object module

```
repos/pg-toolbelt/packages/pg-delta/src/core/objects/<object-type>/
```

If the handler class or change type for the specific operation is missing, the issue is definitely not covered.

#### 2d. Check pg-delta open issues and PRs

Before declaring a gap, check:

- `https://github.com/supabase/pg-toolbelt/issues` — is there already an open issue for this?
- `https://github.com/supabase/pg-toolbelt/pulls` — is there a PR already addressing this?

If work is already in progress, note it in the tracking issue rather than skipping it entirely.

### Step 3 — Verdict

| Situation                                                 | Verdict            |
| --------------------------------------------------------- | ------------------ |
| Integration test covers the exact scenario                | **Covered** — skip |
| Test exists for object type but not the specific scenario | **Not covered**    |
| Object type module exists but no test at all              | **Not covered**    |
| Object type is entirely absent from `src/core/objects/`   | **Not covered**    |

### Step 4 — Write the tracking issue

Use this template (all three sections required):

````markdown
## Context

<!-- 1-3 paragraphs:
  - What the pgschema issue describes
  - Which pg-delta object module / test file is involved
  - Why this matters for users migrating schemas
  - Whether the issue was resolved in pgschema (link merged PR if applicable) -->

Relates to pgschema issue #<N>: <URL>

## Test Case to Reproduce

**Initial state (both databases):**

```sql
CREATE SCHEMA test_schema;
-- ... base objects ...
```
````

**Change to diff (branch only):**

```sql
-- ... the DDL that pgschema handles but pg-delta does not ...
```

**Expected:** pg-delta generates the correct migration DDL.
**Actual:** pg-delta either generates incorrect DDL or throws an error.

## Suggested Fix

<!-- Be specific. Reference actual file paths:
  - "Add a new ChangeClass in src/core/objects/table/ for ..."
  - "Extend src/core/catalog.diff.ts to detect ..."
  - "Add an integration test in tests/integration/alter-table-operations.test.ts" -->

```

---

## Creating Benchmark Gap Analyses

Benchmark files live in `benchmark/` and document gaps in detail.

### Naming

Files follow the pattern `NNN-short-description.md` (e.g. `016-next-gap.md`). Check the highest existing number and increment.

### Required sections

1. **Context** — what the pgschema issue describes and why it matters
2. **Reproduction SQL** — runnable SQL demonstrating the scenario
3. **How pgschema handled it** — the approach taken in the Go codebase (check the merged PR!)
4. **Current pg-delta status** — what pg-delta supports today (with evidence from tests/source)
5. **Comparison of approaches** — pgschema vs pg-delta architecture differences
6. **Plan to handle it in pg-delta** — concrete steps to close the gap

### Severity guidelines

| Severity | Criteria |
|---|---|
| **Critical** | Data loss or silent corruption; produces wrong DDL that would break a migration |
| **High** | Incorrect output for a common scenario; workaround exists but is fragile |
| **Medium** | Edge case or uncommon DDL; most users unlikely to hit it |

### Updating the benchmark README

After adding a new file, add a row to the summary table in `benchmark/README.md`.

---

## Implementing Fixes in pg-delta

### 1. Locate the object module

```

repos/pg-toolbelt/packages/pg-delta/src/core/objects/<object-type>/

````

Key source files:
- `src/core/catalog.diff.ts` — top-level catalog diff orchestration
- `src/core/change.types.ts` — change type definitions
- `src/core/depend.ts` — dependency tracking
- `src/core/sort/` — dependency-aware change sorting (topological)
- `src/core/plan/` — migration plan generation and SQL formatting

### 2. Write an integration test

Every test follows the roundtrip fidelity pattern:

```typescript
import { describe, test } from "bun:test";
import { POSTGRES_VERSIONS } from "../constants.ts";
import { withDb } from "../utils.ts";
import { roundtripFidelityTest } from "./roundtrip.ts";

for (const pgVersion of POSTGRES_VERSIONS) {
  describe(`<feature> (pg${pgVersion})`, () => {
    test("<scenario>", withDb(pgVersion, async (db) => {
      await roundtripFidelityTest({
        mainSession: db.main,
        branchSession: db.branch,
        initialSetup: `
          -- SQL applied to *both* databases before the test
          CREATE SCHEMA test_schema;
          CREATE TABLE test_schema.users (id integer NOT NULL);
        `,
        testSql: `
          -- SQL representing the *change* to diff and migrate
          ALTER TABLE test_schema.users ADD COLUMN email text;
        `,
      });
    }));
  });
}
````

`roundtripFidelityTest` applies `testSql` to the branch database, diffs it against the main database, and verifies the generated DDL brings main up to date with branch.

### 3. Run tests

```bash
cd repos/pg-toolbelt
bun install
bun run test:pg-delta                                          # all pg-delta tests
bun test packages/pg-delta/tests/integration/<file>.test.ts    # single file
```

Requires Docker (for PostgreSQL containers).

---

## Labels Reference

| Label                  | Meaning                                                                    |
| ---------------------- | -------------------------------------------------------------------------- |
| `from-pgschema`        | Tracking issue generated from an **open** pgschema Bug/Feature issue       |
| `resolved-in-pgschema` | Tracking issue generated from a **closed** pgschema issue (historical gap) |
| `needs-test`           | A pg-delta integration test case is needed for this scenario               |

---

## Common Pitfalls

1. **Stale submodules** — Always run `git submodule update --remote --merge` before evaluating coverage. The local submodule may lag behind upstream, causing false "not covered" verdicts.

2. **Keyword match ≠ coverage** — Finding a keyword in a test file does not mean the scenario is covered. Read the `initialSetup` and `testSql` blocks to confirm the exact DDL operation is tested.

3. **Duplicate detection** — Before creating a tracking issue, search existing issues in this repo for the pgschema issue number. The automation scripts already do this, but manual agents must check too.

4. **Missing merged PR context** — pgschema issues alone may be vague. Always check merged PRs that reference the issue — they contain the actual fix, test SQL, and implementation details that are essential for writing accurate reproduction cases.

5. **Ignoring pg-delta open issues/PRs** — A gap may already be known or actively worked on in pg-toolbelt. Check open issues and PRs before creating a duplicate tracking issue.

6. **Wrong label combination** — Use `from-pgschema` for open pgschema issues, `resolved-in-pgschema` for closed ones. Never apply both to the same tracking issue.

7. **Overly broad "not covered"** — pg-delta may handle the general case but miss a specific edge case. Be precise about _what exactly_ is not covered rather than saying the entire object type lacks support.

---

## Further Reading

- `docs/coverage-guide.md` — detailed coverage evaluation guide with full issue template
- `docs/pgdelta-structure.md` — pg-delta directory map, test file listing, and test anatomy
- `.github/copilot-instructions.md` — Copilot-specific agent instructions
- `benchmark/README.md` — summary of all 15 benchmarked gaps with severity ratings

## Cursor Cloud specific instructions

### Services overview

This repo has two concerns:

1. **Python automation scripts** (`scripts/compare_issues.py`, `scripts/compare_resolved.py`) — the primary "application". They require `GITHUB_TOKEN` and use the GitHub Models API (no separate OpenAI key needed). Run with `DRY_RUN=true` for safe local testing.
2. **pg-delta submodule** (`repos/pg-toolbelt/packages/pg-delta/`) — a TypeScript/Bun schema diff tool whose tests require Docker (for PostgreSQL containers via testcontainers).

### Running services

| What | Command | Notes |
|---|---|---|
| Python scripts (dry run) | `DRY_RUN=true python3 scripts/compare_issues.py` | Needs `GITHUB_TOKEN` in env |
| Lint (pg-toolbelt) | `cd repos/pg-toolbelt && bun run format-and-lint` | Uses Biome |
| Type check (pg-toolbelt) | `cd repos/pg-toolbelt && bun run check-types` | |
| Build (pg-toolbelt) | `cd repos/pg-toolbelt && bun run build` | |
| Unit tests (pg-delta) | `cd repos/pg-toolbelt && bun test packages/pg-delta/src/` | No Docker needed |
| Integration tests (pg-delta) | `cd repos/pg-toolbelt && sudo -E env "PATH=$PATH" bun test packages/pg-delta/tests/integration/<file>.test.ts` | Requires Docker; see gotcha below |

### Gotchas

- **Docker must be running** before pg-delta integration tests. Start with `sudo dockerd &>/tmp/dockerd.log &` and wait ~3s. The daemon is configured with `fuse-overlayfs` storage driver and `iptables-legacy` for the cloud VM environment.
- **Integration tests need sudo** (or Docker socket access) because testcontainers spins up PostgreSQL containers. Use `sudo -E env "PATH=$PATH" bun test ...` to preserve the Bun path.
- **First integration test run may timeout** on the first test case of each PG version because Docker pulls the PostgreSQL image. Subsequent runs are fast.
- **Submodules must be initialized** before any script or test will work: `git submodule update --init --recursive`.
- **Bun is installed in `~/.bun/bin/`** — make sure it's on PATH (`export PATH="$HOME/.bun/bin:$PATH"`).
