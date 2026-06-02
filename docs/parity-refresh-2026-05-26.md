# Parity refresh report - 2026-05-26

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`)
- `pg-delta` (`repos/pg-toolbelt` @ `ee9385daf75f72d443882020247ffd2599050090`)

## 1) Benchmark issue status refresh

There is no resolved-issue parity-state delta versus the 2026-05-25 refresh.

### Still solved in pg-delta

- benchmark **005** / pgschema [#190](https://github.com/pgplex/pgschema/issues/190)
  remains solved in pg-delta via merged PR
  [#231](https://github.com/supabase/pg-toolbelt/pull/231) and closed issue
  [#130](https://github.com/supabase/pg-toolbelt/issues/130)
- benchmarks **007**, **008**, **013**, **015**, **016**, **017**, **018**,
  and **019** remain solved in pg-delta via their already-merged pg-toolbelt
  fixes

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
- pgschema [#408](https://github.com/pgplex/pgschema/issues/408): quoted custom
  or reserved type names in plan output
- pgschema [#436](https://github.com/pgplex/pgschema/issues/436): required
  extensions in dump output
  - evidence: pg-delta has first-class extension modeling in
    `src/core/objects/extension/` plus integration coverage in
    `tests/integration/extension-operations.test.ts`
- pgschema [#444](https://github.com/pgplex/pgschema/issues/444): `DROP COLUMN`
  ordered before dropping a dependent view in the same plan group
  - no duplicate pg-toolbelt issue drafted; pg-delta already covers this
    dependency class via closed issue
    [#139](https://github.com/supabase/pg-toolbelt/issues/139) and merged PR
    [#155](https://github.com/supabase/pg-toolbelt/pull/155)
  - evidence: `tests/integration/view-operations.test.ts` asserts `DROP VIEW`
    before the table change when projected columns change, and destructive
    table alters are routed to the drop phase in `src/core/sort/utils.ts`

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

- pgschema [#427](https://github.com/pgplex/pgschema/issues/427):
  schema-qualified functions in RLS policy expressions
  - still no matching pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)
- pgschema [#439](https://github.com/pgplex/pgschema/issues/439):
  replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old
  constraint
  - still no matching pg-toolbelt issue or PR found
  - draft-only issue text remains in
    [`docs/parity-issue-drafts-2026-05-23.md`](./parity-issue-drafts-2026-05-23.md)

### Open candidates not escalated to duplicate trackers

- pgschema [#418](https://github.com/pgplex/pgschema/issues/418):
  `CREATE INDEX CONCURRENTLY` on partitioned parents
  - no duplicate pg-toolbelt issue drafted; this is specific to pgschema's
    online-DDL rewrite and pg-delta does not synthesize `CONCURRENTLY`
- pgschema [#420](https://github.com/pgplex/pgschema/issues/420):
  `varchar(n)[]` typmod preservation
- pgschema [#421](https://github.com/pgplex/pgschema/issues/421): quoted
  mixed-case foreign-key column names
- pgschema [#422](https://github.com/pgplex/pgschema/issues/422): quoted
  mixed-case custom types

The current pg-delta source path still looks closer to correct than pgschema's
dump/plan path for #420 / #421 / #422, but there is still not enough exact
roundtrip evidence to promote them into benchmark entries or duplicate issue
drafts.

### Open items classified as not parity work

- pgschema [#49](https://github.com/pgplex/pgschema/issues/49): explicit rename
  / refactor workflow proposal
  - classified as `not_parity`; this is a pgschema-specific workflow design,
    not a concrete pg-delta diff or planning gap
- pgschema [#406](https://github.com/pgplex/pgschema/issues/406),
  [#407](https://github.com/pgplex/pgschema/issues/407),
  [#409](https://github.com/pgplex/pgschema/issues/409), and
  [#429](https://github.com/pgplex/pgschema/issues/429)
  - `.pgschemaignore` follow-ups remain pgschema-specific ignore-file work

## 3) Notes

- There is no parity-state delta versus the 2026-05-25 refresh.
- The active benchmarked gap set is unchanged: benchmark **020** remains the
  only unresolved historical parity gap.
- The current open pg-toolbelt parity trackers remain
  [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
  [#219](https://github.com/supabase/pg-toolbelt/issues/219).
- There is still no matching pg-toolbelt issue or PR for pgschema #412, #427,
  or #439.
- The automated `compare_issues.py` / `compare_resolved.py` dry runs still need
  to be interpreted alongside a manual unlabeled-issue sweep, because most of
  the current pgschema issues do not carry the `Bug` / `Feature` labels that
  those scripts filter on.
