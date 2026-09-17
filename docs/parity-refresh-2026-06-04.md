# Parity refresh report - 2026-06-04

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `592c19c95b06830255b45bc4d80eeacd62e7e727`)
- `pg-delta` (`repos/pg-toolbelt` @ `ee9385daf75f72d443882020247ffd2599050090`)

## 1) Benchmark issue status refresh

There is no resolved-issue parity-state delta versus the 2026-06-03 refresh.

### Still solved in pg-delta

- benchmarks **005**, **007**, **008**, **013**, **015**, **016**, **017**,
  **018**, and **019** remain solved in current pg-delta via already-merged
  pg-toolbelt fixes

### Still active in the resolved-issue benchmark

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints
  - benchmark file:
    [`benchmark/020-unique-constraint-nulls-not-distinct.md`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
  - no matching pg-toolbelt issue or PR found during this refresh

## 2) Existing open pgschema issue refresh

### Covered in current pg-delta

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362): numeric
  precision changes
- pgschema [#401](https://github.com/pgplex/pgschema/issues/401):
  `RETURNS SETOF <table>` dependency ordering
- pgschema [#414](https://github.com/pgplex/pgschema/issues/414): creating a
  view that references a newly added column
- pgschema [#415](https://github.com/pgplex/pgschema/issues/415):
  materialized-view refactor drop ordering and verb selection
- pgschema [#416](https://github.com/pgplex/pgschema/issues/416): custom
  aggregates in dump output
- pgschema [#420](https://github.com/pgplex/pgschema/issues/420):
  `varchar(n)[]` typmod preservation
- pgschema [#427](https://github.com/pgplex/pgschema/issues/427):
  schema-qualified functions in RLS policy expressions
- pgschema [#436](https://github.com/pgplex/pgschema/issues/436): required
  extensions in dump output

### Already tracked in pg-toolbelt

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - existing tracker remains open:
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366): function
  privilege signatures with enum argument types
  - existing tracker remains open:
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Draft-only uncovered open candidates

- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - still no matching pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  ordered before dropping a dependent view in the same plan group
  - pg-delta has analogous `ADD COLUMN` + dependent-view coverage via
    [pg-toolbelt#139](https://github.com/supabase/pg-toolbelt/issues/139) /
    [#155](https://github.com/supabase/pg-toolbelt/pull/155), plus adjacent
    dependency-chain work in
    [pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263), but
    there is still no exact `DROP COLUMN` + dependent-view regression or
    dedicated tracker
  - draft-only issue text is saved in
    [`docs/parity-issue-drafts-2026-06-01.md`](./parity-issue-drafts-2026-06-01.md)

### Open items classified as not parity work

- pgschema [#418](https://github.com/pgplex/pgschema/issues/418):
  `CREATE INDEX CONCURRENTLY` on partitioned parents
- pgschema [#419](https://github.com/pgplex/pgschema/issues/419):
  `.pgschemaignore` behavior differs by GitHub Actions install path
- pgschema [#447](https://github.com/pgplex/pgschema/issues/447):
  `.pgschemaignore` support for named constraints
- pgschema [#449](https://github.com/pgplex/pgschema/issues/449): repeat plan
  drift for same-schema policy and CHECK expressions after apply
  - this is a declarative-SQL vs live-catalog normalization problem in
    pgschema, not a pg-delta catalog-to-catalog diff gap
  - current pg-delta extracts policy expressions via `pg_get_expr(...)` in
    `src/core/objects/rls-policy/rls-policy.model.ts` and CHECK constraints via
    `pg_get_expr(...)` / `pg_get_constraintdef(...)` in
    `src/core/objects/table/table.model.ts`, so both sides already compare the
    same PostgreSQL-rendered catalog form
  - no matching pg-toolbelt issue or PR was found
- pgschema [#450](https://github.com/pgplex/pgschema/issues/450): missing role
  blocks plan and apply
  - this is specific to pgschema applying dumped SQL into a temporary planning
    schema when the grantee role does not exist there
  - pg-delta diffs live catalogs directly, models roles in
    `src/core/objects/role/`, and orders privilege changes behind role
    creation/dependencies in the current planner
  - no matching pg-toolbelt issue or PR was found
- pgschema [#421](https://github.com/pgplex/pgschema/issues/421): quoted
  mixed-case foreign-key column names
- pgschema [#422](https://github.com/pgplex/pgschema/issues/422): quoted
  mixed-case custom types
- pgschema [#49](https://github.com/pgplex/pgschema/issues/49): explicit rename
  / refactor workflow proposal
- pgschema [#407](https://github.com/pgplex/pgschema/issues/407),
  [#409](https://github.com/pgplex/pgschema/issues/409), and
  [#429](https://github.com/pgplex/pgschema/issues/429): `.pgschemaignore`
  follow-ups

## 3) Recently closed issue screening

No new parity-relevant pgschema merged PRs landed since the 2026-06-03
refresh. The current screened closed-item state is unchanged:

- pgschema [#406](https://github.com/pgplex/pgschema/issues/406): indexes in
  `.pgschemaignore` remain not parity work for pg-delta
- pgschema [#408](https://github.com/pgplex/pgschema/issues/408): quoted custom
  or reserved type names in plan output remain covered in current pg-delta via
  `format_type(...)`-based type extraction and quoted-type integration coverage
- pgschema [#410](https://github.com/pgplex/pgschema/issues/410): `name` typed
  columns are covered by pg-delta's `format_type(...)`-based column extraction
- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  `UNIQUE NULLS NOT DISTINCT` on table constraints remains not covered in
  current pg-delta and is benchmarked as
  [`020`](../benchmark/020-unique-constraint-nulls-not-distinct.md)
- pgschema [#423](https://github.com/pgplex/pgschema/issues/423): `UNLOGGED`
  tables remain covered by pg-delta's persistence extraction and diff logic
- pgschema [#426](https://github.com/pgplex/pgschema/issues/426): Docker Hub
  image lag is not parity work for pg-delta
- pgschema [#445](https://github.com/pgplex/pgschema/issues/445): same-schema
  CHECK constraint qualifier drift is not parity work for pg-delta; the issue is
  specific to pgschema's temp-schema normalization path, while pg-delta already
  exercises same-schema function / type references in
  `check-constraint-ordering.test.ts`
- pgschema [#446](https://github.com/pgplex/pgschema/issues/446): explicit
  `UNIQUE` constraints on `PRIMARY KEY` columns are covered in current
  pg-delta's table-constraint path

## 4) Notes

- The resolved benchmark set is unchanged versus the 2026-06-03 refresh.
- Benchmark **020** remains the only unresolved historical parity gap.
- The current open pg-toolbelt parity trackers remain
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219).
- The notable deltas from the previous refresh are:
  - new open issue #449 is screened as `not_parity`
  - new open issue #450 is screened as `not_parity`
- There is still no exact matching pg-toolbelt issue or PR for pgschema #412,
  #439, or #444.
- The automated `compare_issues.py` / `compare_resolved.py` dry runs still need
  to be interpreted alongside a manual unlabeled-issue sweep, because most of
  the current pgschema issues do not carry the `Bug` / `Feature` labels that
  those scripts filter on.
