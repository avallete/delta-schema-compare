# Copilot Instructions — delta-schema-compare

## Purpose of this repository

This repository automatically compares open issues in
[pgschema](https://github.com/pgplex/pgschema) with the test coverage of
[@supabase/pg-delta](https://github.com/supabase/pg-toolbelt/tree/main/packages/pg-delta)
and tracks any gaps as actionable issues here.

Both upstream codebases are available locally as **git submodules**:

| Submodule path | Upstream |
|---|---|
| `repos/pgschema/` | pgplex/pgschema – Go-based declarative schema migration tool |
| `repos/pg-toolbelt/packages/pg-delta/` | @supabase/pg-delta – TypeScript schema diff tool |

## How to manually review coverage for a pgschema issue

1. Read the pgschema issue (title + body) carefully.
2. Extract the key PostgreSQL feature or behaviour being discussed
   (e.g. `GENERATED ALWAYS AS`, partitioned tables, RLS policies, enum types).
3. Search `repos/pg-toolbelt/packages/pg-delta/tests/integration/` for test
   files whose name or content relates to that feature.
   - Use `grep -ri "<keyword>" repos/pg-toolbelt/packages/pg-delta/tests/`
4. If a matching test file exists, check whether it actually tests the
   *exact scenario* in the pgschema issue — not merely the same object type.
5. If no test exists (or the existing test does not cover the scenario),
   generate a tracking issue following the template in
   `docs/coverage-guide.md`.
6. After each review run, update the review-memory file at
   `benchmark/review-memory.json` for every issue you checked:
   - Record the verdict (`covered`, `not_covered`, or `tracked`).
   - Include enough change markers to detect staleness at the next run
     (at minimum: pgschema issue `updated_at`, `repos/pgschema` HEAD, and
     `repos/pg-toolbelt/packages/pg-delta` HEAD).
   - If none of those markers changed, skip re-review and reuse the stored
     verdict.

## Benchmark-to-issue workflow (required order)

When asked to create issues from the benchmark, always use this sequence:

1. **Map benchmark ↔ pg-delta issues/PRs first**
   - Build a mapping from each benchmark item to matching pg-toolbelt issues/PRs.
   - Refresh each item's status as:
     - `covered` (merged fix and scenario now covered),
     - `tracked` (issue/PR exists but not merged),
     - `not_covered` (no effective fix yet).
   - Update benchmark markdown and review memory before drafting any new issue.

2. **Find truly missing pg-toolbelt issues second**
   - Screen new pgschema candidates not already represented.
   - Run duplicate checks against existing pg-toolbelt issues and PRs.
   - Draft missing issues in markdown first with:
     - context,
     - runnable MRE SQL,
     - suggested fix paths.
   - Do not open issues in the same pass unless explicitly requested.

## How to generate a tracking issue

Use the structure defined in `docs/coverage-guide.md`.  All generated issues
must:
- Reference the original pgschema issue URL.
- Include the labels `from-pgschema` and `needs-test`.
- Contain three sections: **Context**, **Test Case to Reproduce** (runnable
  SQL), and **Suggested Fix** (with pg-delta file paths where relevant).

## Key file locations

```
scripts/compare_issues.py          Main automation script
.github/workflows/compare-issues.yml  Daily workflow
docs/coverage-guide.md             Issue-generation template and guide
docs/pgdelta-structure.md          pg-delta codebase map
repos/pgschema/                    pgschema source (submodule)
repos/pg-toolbelt/packages/pg-delta/   pg-delta source (submodule)
```

## Important context about both tools

### pgschema (repos/pgschema/)
- **Language:** Go
- **Purpose:** Terraform-style declarative schema migration (dump → edit → plan → apply)
- **Test data:** `testdata/diff/` (150+ diff test cases), `testdata/dump/` (18 dump suites)
- **Architecture:** IR-based, inspector-only approach; both desired and current state come
  from database inspection (embedded-postgres for plan)
- **Issues:** Mostly around accurate introspection and diff generation for specific PostgreSQL
  objects

### @supabase/pg-delta (repos/pg-toolbelt/packages/pg-delta/)
- **Language:** TypeScript / Bun
- **Purpose:** Schema diff tool — connects to two databases, diffs catalogs, generates DDL
- **Test structure:**
  - `tests/integration/` — roundtrip fidelity tests (run `bun test tests/`)
  - `src/core/objects/` — per-object-type modules (table, function, view, etc.)
  - `src/core/sort/` — dependency-aware change sorting
- **Coverage:** An issue is "covered" only if there is an integration test that
  exercises the specific DDL scenario, not just if the object type is mentioned.
