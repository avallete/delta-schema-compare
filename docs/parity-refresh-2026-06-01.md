# Parity refresh report - 2026-06-01

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `592c19c95b06830255b45bc4d80eeacd62e7e727`)
- `pg-delta` (`repos/pg-toolbelt` @ `ee9385daf75f72d443882020247ffd2599050090`)

## 1) Benchmark issue status refresh

There is no resolved-issue parity-state delta versus the 2026-05-31 refresh.

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

### Still covered in pg-delta

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

- pgschema [#420](https://github.com/pgplex/pgschema/issues/420):
  `varchar(n)[]` typmod preservation
  - upstream pgschema fix PR [#438](https://github.com/pgplex/pgschema/pull/438)
    is merged, but the issue itself remains open
  - still no matching pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-27.md`](./parity-issue-drafts-2026-05-27.md)
- pgschema [#427](https://github.com/pgplex/pgschema/issues/427):
  schema-qualified functions in RLS policy expressions
  - pgschema still has open fix PR
    [#428](https://github.com/pgplex/pgschema/pull/428)
  - still no matching pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - still no matching pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  ordered before dropping a dependent view in the same plan group
  - this refresh reclassified the scenario from covered to not covered
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
  exercises same-schema function/type references in
  `check-constraint-ordering.test.ts`
- pgschema [#446](https://github.com/pgplex/pgschema/issues/446): redundant
  `UNIQUE` constraints on `PRIMARY KEY` columns are not parity work for
  pg-delta; pgschema drops them during desired-state normalization, while
  pg-delta reads table constraints directly from `pg_constraint` without
  collapsing `UNIQUE` under `PRIMARY KEY`

## 4) Notes

- The resolved benchmark set is unchanged versus the 2026-05-31 refresh.
- Benchmark **020** remains the only unresolved historical parity gap.
- The current open pg-toolbelt parity trackers remain
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219).
- The notable delta from the previous refresh is that pgschema #444 is now
  tracked as a draft-only uncovered candidate rather than covered, because the
  current pg-delta evidence only proves the analogous `ADD COLUMN` ordering
  case, not the exact `DROP COLUMN` scenario from the pgschema issue.
- There is still no exact matching pg-toolbelt issue or PR for pgschema #412,
  #420, #427, #439, or #444.
- The automated `compare_issues.py` / `compare_resolved.py` dry runs still need
  to be interpreted alongside a manual unlabeled-issue sweep, because most of
  the current pgschema issues do not carry the `Bug` / `Feature` labels that
  those scripts filter on.
