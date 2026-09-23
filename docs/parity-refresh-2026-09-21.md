# Parity refresh report - 2026-09-21

This report records the 2026-09-21 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `0882fc4cb6b792b79b599a414b434e4e048b6672`)

## 1) Benchmark status refresh

This refresh advances checked-in/live `pgschema` from
`b8e7e26a9db221ea01cdd64f4cfb8ca96923c536` to
`580f4040d0f3c1bfad1497918200c9c1f638a020` through merged PRs
[#616](https://github.com/pgplex/pgschema/pull/616),
[#617](https://github.com/pgplex/pgschema/pull/617),
[#618](https://github.com/pgplex/pgschema/pull/618),
[#619](https://github.com/pgplex/pgschema/pull/619),
[#620](https://github.com/pgplex/pgschema/pull/620),
[#621](https://github.com/pgplex/pgschema/pull/621), and
[#608](https://github.com/pgplex/pgschema/pull/608), while checked-in/live
`pg-delta` remains unchanged at `0882fc4cb6b792b79b599a414b434e4e048b6672`.

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain active unresolved gaps

### Current evidence on the current heads

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    relation columns gated by `a.attislocal`, so child-local overrides on
    inherited partition columns never surface as diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child column
    element list for local `DEFAULT` / `NOT NULL` overrides
  - open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only tracker context; open issues
    [#476](https://github.com/supabase/pg-toolbelt/issues/476) and
    [#477](https://github.com/supabase/pg-toolbelt/issues/477), open PR
    [#478](https://github.com/supabase/pg-toolbelt/pull/478), merged PR
    [#480](https://github.com/supabase/pg-toolbelt/pull/480), and open release
    PR [#481](https://github.com/supabase/pg-toolbelt/pull/481) remain
    adjacent rather than benchmark-closing
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still reads
    `attgenerated` but only preserves generated-expression presence, not the
    actual `VIRTUAL` versus `STORED` kind
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only tracker context; there is still no exact pg-toolbelt
    issue or PR for the generated-kind gap itself
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - there is still no exact pg-toolbelt issue or PR for this benchmark

The target repo still has no local tracker issues.

## 2) Open / resolved pgschema delta on 2026-09-21

There is real upstream activity since the 2026-09-20 refresh even though the
active pg-delta benchmark set does not change:

- issues [#599](https://github.com/pgplex/pgschema/issues/599),
  [#600](https://github.com/pgplex/pgschema/issues/600),
  [#601](https://github.com/pgplex/pgschema/issues/601),
  [#602](https://github.com/pgplex/pgschema/issues/602),
  [#603](https://github.com/pgplex/pgschema/issues/603), and
  [#607](https://github.com/pgplex/pgschema/issues/607) are now closed via
  merged PRs
  [#617](https://github.com/pgplex/pgschema/pull/617),
  [#618](https://github.com/pgplex/pgschema/pull/618),
  [#619](https://github.com/pgplex/pgschema/pull/619),
  [#620](https://github.com/pgplex/pgschema/pull/620),
  [#621](https://github.com/pgplex/pgschema/pull/621), and
  [#608](https://github.com/pgplex/pgschema/pull/608)
- merged PR [#616](https://github.com/pgplex/pgschema/pull/616) lands the
  SQL-function batch-ordering follow-up on already-upstream-only issue
  [#596](https://github.com/pgplex/pgschema/issues/596)
- open PR [#611](https://github.com/pgplex/pgschema/pull/611) remains the
  upstream fix path for covered issue
  [#598](https://github.com/pgplex/pgschema/issues/598)

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559), and
  [#597](https://github.com/pgplex/pgschema/issues/597) remain
  **not parity work for pg-delta**
- open issue [#598](https://github.com/pgplex/pgschema/issues/598) remains
  **covered** in current pg-delta
- there is currently **no open uncovered parity candidate** on the pgschema
  side

### Focus notes for the changed upstream items

- **#596** remains **not parity work** for pg-delta:
  - merged PR [#616](https://github.com/pgplex/pgschema/pull/616) continues
    the same temp-schema / SQL-function batch-ordering family after
    [#615](https://github.com/pgplex/pgschema/pull/615)
  - pg-delta diffs live catalogs and does not apply desired-state SQL into a
    temporary comparison schema
- **#598** remains **covered** in current pg-delta:
  - current pg-delta captures regular-index validity as semantic `valid`
  - `tests/index-invalid-repair.test.ts` covers the invalid-index repair path
  - open PR [#611](https://github.com/pgplex/pgschema/pull/611) remains the
    upstream fix path on the pgschema side
- **#599** remains **covered** in current pg-delta:
  - current pg-delta already models `pg_trigger.tgenabled`
  - `src/plan/rules/helpers.ts` maps `O/D/R/A` to `ENABLE`, `DISABLE`,
    `ENABLE REPLICA`, and `ENABLE ALWAYS`
- **#600** remains **covered** in current pg-delta:
  - `src/plan/rules/types.ts` already marks `ALTER TYPE ... ADD VALUE` actions
    as `transactionality: "commitBoundaryAfter"`
  - `src/apply/commit-boundary.test.ts` and the enum corpus cover the same
    commit-boundary behavior
- **#601** remains **covered** in current pg-delta:
  - current pg-delta already rebuilds dependent views around replace-path
    routine changes
  - `src/extract/dependencies.ts`, `src/plan/rules/routines.ts`, and
    `src/plan/rules/views.ts` still carry the same replace-path view
    dependency handling
- **#602** remains **covered** in current pg-delta:
  - merged PR [#620](https://github.com/pgplex/pgschema/pull/620) documents
    upstream ownership limits
  - pg-delta already models owner edges and emits `ALTER ... OWNER TO`
- **#603** remains **covered** in current pg-delta:
  - merged PR [#621](https://github.com/pgplex/pgschema/pull/621) warns about
    unsupported no-effect statements upstream
  - pg-delta already preserves global `ALTER DEFAULT PRIVILEGES` with
    `defaclnamespace = 0`
- **#607** remains **not parity work** for pg-delta:
  - merged PR [#608](https://github.com/pgplex/pgschema/pull/608) fixes
    extension-owned types in pgschema's external-plan temp schema
  - pg-delta diffs live catalogs instead of applying desired-state SQL to a
    temporary comparison schema

## 3) What changed in this refresh

- advance the checked-in `repos/pgschema` submodule pointer to
  `580f4040d0f3c1bfad1497918200c9c1f638a020`
- keep the checked-in `repos/pg-toolbelt` submodule pointer at
  `0882fc4cb6b792b79b599a414b434e4e048b6672`
- refresh `benchmark/README.md` to the 2026-09-21 latest-state snapshot
- add fresh 2026-09-21 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- refresh `benchmark/review-memory.json` bookkeeping:
  - move issues **#599** / **#600** / **#601** / **#602** / **#603** /
    **#607** from the open watch list to resolved status
  - refresh the remaining open watch-list fingerprints on the new pgschema SHA
  - refresh the active benchmark fingerprints for issues **#499** / **#501** /
    **#564**
- add this report as the 2026-09-21 latest-state sweep
- no new benchmark files and no new draft-only uncovered issue docs were
  needed

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state open --limit 50 --search 'sort:updated-desc' --json number,title,updatedAt,url,state,labels`
  - `gh issue list -R pgplex/pgschema --state closed --limit 30 --search 'closed:>=2026-09-20 sort:updated-desc' --json number,title,updatedAt,closedAt,url,state,labels`
  - `gh pr list -R pgplex/pgschema --state open --limit 20 --json number,title,updatedAt,url,isDraft,headRefName,baseRefName`
  - `gh pr list -R pgplex/pgschema --state merged --limit 20 --search 'merged:>=2026-09-20 sort:updated-desc' --json number,title,mergedAt,url,headRefName,baseRefName`
  - `gh issue list -R supabase/pg-toolbelt --state open --limit 100 --search 'sort:updated-desc' --json number,title,updatedAt,url,state`
  - `gh pr list -R supabase/pg-toolbelt --state open --limit 100 --search 'sort:updated-desc' --json number,title,updatedAt,url,isDraft,headRefName,baseRefName`
  - `gh pr list -R supabase/pg-toolbelt --state merged --limit 30 --search 'merged:>=2026-09-19 sort:updated-desc' --json number,title,mergedAt,url,headRefName,baseRefName`
  - focused duplicate / adjacency checks for benchmarks **021**, **022**, and
    **024** with `gh issue list` / `gh pr list` searches on the pg-toolbelt
    repo
  - `gh issue list -R avallete/delta-schema-compare --state all --limit 120 --json number,title,state,updatedAt,url` (**returned `[]`**)
- repo Python validation:
  - `python3 -m pip install -r requirements.txt`
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true python3 scripts/compare_issues.py` (**0 labeled open issues**)
  - `GITHUB_TOKEN="$(gh auth token)" DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py` (**0 labeled resolved issues**)
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark` (**9 tests**, pass)
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- no new pg-delta runtime probes were rerun in this refresh because
  `pg-toolbelt` did not move and the active gap verdicts are unchanged at the
  source / codepath level
