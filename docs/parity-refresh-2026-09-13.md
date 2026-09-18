# Parity refresh report - 2026-09-13

This report records the 2026-09-13 latest-state parity check between:

- `pgschema` (`repos/pgschema` @ `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`)
- checked-in/live `pg-delta`
  (`repos/pg-toolbelt` @ `85e8946a79b0a5b149fe9a772fef882c14cb9567`)

## 1) Benchmark status refresh

This refresh keeps the benchmark matrix unchanged versus
[`docs/parity-refresh-2026-09-12.md`](./parity-refresh-2026-09-12.md):

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, **019**, **020**, and **023** remain solved in current pg-delta
- benchmarks **021**, **022**, and **024** remain active unresolved gaps
- checked-in/live `pg-delta` remains at
  `85e8946a79b0a5b149fe9a772fef882c14cb9567`
  (`@supabase/pg-delta@1.0.0-alpha.50`)
- checked-in/live `pgschema` remains at
  `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`

### Current evidence on the current heads

There is no upstream code delta on either side since the 2026-09-12 refresh:

- `git -C repos/pgschema rev-parse HEAD` and
  `git -C repos/pgschema rev-parse origin/main` both return
  `319b88c83d62b2c9a62eff7a09ec6563954bcf4b`
- `git -C repos/pg-toolbelt rev-parse HEAD` and
  `git -C repos/pg-toolbelt rev-parse origin/main` both return
  `85e8946a79b0a5b149fe9a772fef882c14cb9567`

The active pg-delta benchmark paths therefore remain unchanged:

- benchmark **021** / pgschema
  [#499](https://github.com/pgplex/pgschema/issues/499):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still keeps
    relation columns gated by `a.attislocal`, so child-local overrides on
    inherited partition columns never surface as diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child
    column-element list for local `DEFAULT` / `NOT NULL` overrides
  - open pg-toolbelt PR
    [#470](https://github.com/supabase/pg-toolbelt/pull/470) remains adjacent
    only; it improves partition replacement/index-attach handling but does not
    add the missing child override model
- benchmark **022** / pgschema
  [#501](https://github.com/pgplex/pgschema/issues/501):
  - current pg-delta already covered issue
    [#591](https://github.com/pgplex/pgschema/issues/591)'s generated-
    expression-change family before upstream merged its fix, via
    `packages/pg-delta/corpus/alter-table--generated-column` and
    `generatedExpr: "replace"` in
    `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
  - the active benchmark **022** gap remains the missing `VIRTUAL` versus
    `STORED` kind: `relations.ts` still collapses `attgenerated` to generated
    expression presence, and `helpers.ts` still hard-codes
    `GENERATED ALWAYS AS (...) STORED`
- benchmark **024** / pgschema
  [#564](https://github.com/pgplex/pgschema/issues/564):
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    tracks nullability via `a.attnotnull` and filters table constraints to
    `con.contype IN ('p', 'u', 'f', 'c', 'x')`, so PG18 `contype = 'n'` state
    remains invisible
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
    a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`

Direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
`pgschema#564`, `pgschema#593`, `pgschema#594`, and `pgschema#595` still
return no dedicated pg-toolbelt issue or PR, and the target repo still has no
existing tracker issues.

## 2) Open / resolved pgschema delta on 2026-09-13

Today's upstream delta is a new open pgschema issue only:

- pgschema issue [#595](https://github.com/pgplex/pgschema/issues/595)
  (`dump takes some extension objects`) opened on 2026-09-13

### Current watch-list verdicts

- open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#588](https://github.com/pgplex/pgschema/issues/588), and
  [#594](https://github.com/pgplex/pgschema/issues/594) remain
  **not parity work for pg-delta**
- open issue [#593](https://github.com/pgplex/pgschema/issues/593) remains
  **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` preserves
    explicit non-default column collations from `a.attcollation`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` replays
    that state as `COLLATE ...` in `columnClause()`
- new open issue [#595](https://github.com/pgplex/pgschema/issues/595) is
  already **covered** in current pg-delta:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` tags
    extension-owned relations (including views) with `memberOfExtension` via
    `memberExtensionExpr("pg_class", "c.oid")`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/routines.ts` does the
    same for extension-owned routines via
    `memberExtensionExpr("pg_proc", "p.oid")`
  - `repos/pg-toolbelt/packages/pg-delta/src/policy/view.ts` keeps extension
    members reference-only in the managed view, and the export/load frontends
    already avoid recreating extension members directly; the relevant coverage
    lives in `tests/export-extension-member-parent.test.ts`,
    `tests/extension-member-acl.test.ts`, and
    `tests/load-sql-files-extension-rows.test.ts`
- resolved issue [#591](https://github.com/pgplex/pgschema/issues/591) still
  remains **covered** in current pg-delta via the existing
  generated-expression corpus scenario and `generatedExpr: "replace"` diff path
- there is currently **no open uncovered parity candidate** on the pgschema
  side

### pg-toolbelt open work check

- there are no new pg-toolbelt issues or PR updates since the 2026-09-12
  refresh
- nearby open pg-toolbelt PRs remain
  [#470](https://github.com/supabase/pg-toolbelt/pull/470),
  [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#472](https://github.com/supabase/pg-toolbelt/pull/472), and
  [#473](https://github.com/supabase/pg-toolbelt/pull/473)
- open PR [#470](https://github.com/supabase/pg-toolbelt/pull/470) is still
  adjacent but not exact: it improves partition replacement/index attach
  handling, yet leaves benchmark **021**'s child-local column override path
  unresolved
- PRs **#471**, **#472**, and **#473** remain unrelated to benchmarks
  **021**, **022**, or **024**
- umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
  still carries the only adjacent tracker context for benchmarks **021** /
  **022**; benchmark **024** still has no exact pg-toolbelt issue or PR

## 3) What changed in this refresh

- refresh `benchmark/README.md` to the 2026-09-13 latest-state snapshot
- refresh `benchmark/review-memory.json` review timestamps for the live
  watch-list items and active benchmarked issues, and add issue **#595** to the
  open watch list as **covered**
- add fresh 2026-09-13 refresh notes to benchmarks
  [021](../benchmark/021-partition-child-column-overrides.md),
  [022](../benchmark/022-virtual-generated-columns.md), and
  [024](../benchmark/024-pg18-not-null-validation.md)
- add this report as the 2026-09-13 latest-state sweep

## 4) Validation notes

This refresh was validated with:

- `git submodule update --init --recursive`
- `git submodule update --remote --merge`
- GitHub CLI updated-state queries for both upstream repos:
  - `gh issue list -R pgplex/pgschema --state open --limit 20 --json number,title,updatedAt,url`
  - `gh issue list -R pgplex/pgschema --state closed --search 'closed:>=2026-09-12'`
  - `gh pr list -R pgplex/pgschema --state merged --search 'merged:>=2026-09-12'`
  - `gh issue list -R supabase/pg-toolbelt --state open --limit 30 --json number,title,updatedAt,url`
  - `gh pr list -R supabase/pg-toolbelt --state open --limit 30 --json number,title,updatedAt,url`
- GitHub CLI issue / PR context checks for:
  - pgschema issue **#595**
  - pg-toolbelt issue **#332**
  - pg-toolbelt PRs **#470** and **#473**
  - target-repo issue list (`gh issue list -R avallete/delta-schema-compare --state all`)
- exact duplicate issue / PR searches across `supabase/pg-toolbelt` and
  `avallete/delta-schema-compare` for `pgschema#499`, `pgschema#501`,
  `pgschema#564`, `pgschema#593`, `pgschema#594`, `pgschema#595`,
  `pgschema#439`, and `pgschema#444`
- local source inspection of:
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/routines.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/policy/view.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/load-sql-files.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/export-extension-member-parent.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/extension-member-acl.test.ts`
  - `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-extension-rows.test.ts`
- repo Python validation after installing `requirements.txt`:
  - `DRY_RUN=true python3 scripts/compare_issues.py`
  - `DRY_RUN=true OUTPUT_MODE=benchmark python3 scripts/compare_resolved.py`
  - `python3 -m unittest tests.test_review_memory tests.test_compare_resolved_benchmark`
  - `python3 -m json.tool benchmark/review-memory.json >/dev/null`
  - `git diff --check`
- Bun-backed pg-delta runtime probes were not re-run in this environment
  because Bun is not currently installed in the pod and Docker is unavailable;
  the active gap paths were instead revalidated by unchanged-source inspection
  plus the existing focused runtime observations recorded in the active
  benchmark files
