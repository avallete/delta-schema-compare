# Parity refresh report — 2026-05-01

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`)
- `pg-delta` (`repos/pg-toolbelt` @ `c7e97f8865d05e0afab0ea2a5d7107aa7b42ec8f`)

The refresh included:

1. updating both submodules to latest upstream,
2. re-checking the benchmark matrix against current pg-toolbelt issues/PRs,
3. manually scanning unlabeled recent pgschema issues so the review would not
   be limited by the scripts' `Bug` / `Feature` label filters.

## 1) Benchmark status refresh

All previously benchmarked historical gaps except one are now solved in current
pg-delta.

### Solved in pg-delta

- pgschema [#190](https://github.com/pgplex/pgschema/issues/190) ->
  pg-toolbelt [#130](https://github.com/supabase/pg-toolbelt/issues/130),
  fixed by [#231](https://github.com/supabase/pg-toolbelt/pull/231)
- pgschema [#326](https://github.com/pgplex/pgschema/issues/326) ->
  pg-toolbelt [#132](https://github.com/supabase/pg-toolbelt/issues/132),
  fixed by [#214](https://github.com/supabase/pg-toolbelt/pull/214)
- pgschema [#268](https://github.com/pgplex/pgschema/issues/268) ->
  pg-toolbelt [#133](https://github.com/supabase/pg-toolbelt/issues/133),
  fixed by [#149](https://github.com/supabase/pg-toolbelt/pull/149)
- pgschema [#279](https://github.com/pgplex/pgschema/issues/279) ->
  pg-toolbelt [#138](https://github.com/supabase/pg-toolbelt/issues/138),
  fixed by [#154](https://github.com/supabase/pg-toolbelt/pull/154)
- pgschema [#342](https://github.com/pgplex/pgschema/issues/342) ->
  pg-toolbelt [#140](https://github.com/supabase/pg-toolbelt/issues/140),
  fixed by [#200](https://github.com/supabase/pg-toolbelt/pull/200)
- pgschema [#355](https://github.com/pgplex/pgschema/issues/355) ->
  pg-toolbelt [#183](https://github.com/supabase/pg-toolbelt/issues/183),
  fixed by [#185](https://github.com/supabase/pg-toolbelt/pull/185)
- pgschema [#364](https://github.com/pgplex/pgschema/issues/364) ->
  pg-toolbelt [#182](https://github.com/supabase/pg-toolbelt/issues/182),
  fixed by [#213](https://github.com/supabase/pg-toolbelt/pull/213)
- pgschema [#373](https://github.com/pgplex/pgschema/issues/373) ->
  pg-toolbelt [#184](https://github.com/supabase/pg-toolbelt/issues/184),
  fixed by [#187](https://github.com/supabase/pg-toolbelt/pull/187)
- pgschema [#386](https://github.com/pgplex/pgschema/issues/386) ->
  pg-toolbelt [#198](https://github.com/supabase/pg-toolbelt/issues/198),
  fixed by [#212](https://github.com/supabase/pg-toolbelt/pull/212)

### Still missing historical gap

- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  table-level `UNIQUE NULLS NOT DISTINCT` constraints
  - benchmarked as
    [`benchmark/020-table-unique-nulls-not-distinct.md`](../benchmark/020-table-unique-nulls-not-distinct.md)
  - no matching pg-toolbelt issue or PR found during this refresh

## 2) Open pgschema issue screening

### Covered in current pg-delta

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362):
  numeric precision changes
  - evidence: `alter-table-operations.test.ts` includes numeric type-change
    roundtrip coverage
- pgschema [#401](https://github.com/pgplex/pgschema/issues/401):
  `RETURNS SETOF <table>` dependency ordering
  - evidence:
    `table-function-circular-dependency.test.ts` and
    `table-function-dependency-ordering.test.ts`
- pgschema [#414](https://github.com/pgplex/pgschema/issues/414):
  add-column + dependent-view ordering
  - evidence:
    `view-operations.test.ts` covers drop/recreate ordering for `SELECT *`
    views when base-table columns change, and pg-toolbelt
    [#139](https://github.com/supabase/pg-toolbelt/issues/139) /
    [#155](https://github.com/supabase/pg-toolbelt/pull/155) already landed
- pgschema [#415](https://github.com/pgplex/pgschema/issues/415):
  materialized-view drop kind mismatch
  - evidence:
    `materialized-view-operations.test.ts` exercises
    `DROP MATERIALIZED VIEW` ordering for replacement flows
- pgschema [#416](https://github.com/pgplex/pgschema/issues/416):
  custom aggregates omitted from dump
  - evidence: aggregate object support exists in source and
    `aggregate-operations.test.ts` covers create/alter/drop/comment/privileges

### Already tracked in pg-toolbelt

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404):
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`
  - tracked by
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366):
  function privileges with enum-typed arguments
  - tracked by
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

### Not treated as pg-delta parity gaps

- pgschema [#408](https://github.com/pgplex/pgschema/issues/408):
  quoted custom / reserved type names
  - pg-delta already relies on `format_type(...)` / `quote_ident(...)`
- pgschema [#418](https://github.com/pgplex/pgschema/issues/418):
  `CREATE INDEX CONCURRENTLY` on partitioned parents
  - this is specific to pgschema's online-DDL rewrite strategy; pg-delta emits
    canonical `CREATE INDEX` definitions from catalog state
- pgschema [#420](https://github.com/pgplex/pgschema/issues/420):
  `varchar(n)[]` typmod preservation
  - pg-delta uses `format_type(a.atttypid, a.atttypmod)` for column type
    extraction
- pgschema [#421](https://github.com/pgplex/pgschema/issues/421):
  quoted mixed-case FK columns
  - pg-delta quotes constraint column identifiers during extraction; the
    reported failure is tied to pgschema's dump/apply validation flow
- pgschema [#422](https://github.com/pgplex/pgschema/issues/422):
  quoted mixed-case custom types
  - pg-delta preserves quoted type names and already has special-character type
    coverage
- pgschema [#406](https://github.com/pgplex/pgschema/issues/406),
  [#407](https://github.com/pgplex/pgschema/issues/407),
  [#409](https://github.com/pgplex/pgschema/issues/409),
  [#419](https://github.com/pgplex/pgschema/issues/419)
  - `.pgschemaignore` surface area; not parity work for pg-delta

## 3) Recent closed-issue screening

- pgschema [#410](https://github.com/pgplex/pgschema/issues/410):
  built-in `name` type emitted as `char[]`
  - no pg-delta duplicate drafted; `format_type(...)`-based extraction already
    preserves the type identity
- pgschema [#412](https://github.com/pgplex/pgschema/issues/412):
  table-level `UNIQUE NULLS NOT DISTINCT`
  - still missing in pg-delta's table-constraint model/diff path
- pgschema [#423](https://github.com/pgplex/pgschema/issues/423):
  `UNLOGGED` dropped from table definitions
  - covered by pg-delta table persistence extraction/diff/create support

## 4) Output files updated in this refresh

- `benchmark/README.md`
- `benchmark/005-alter-column-type-using-clause.md`
- `benchmark/007-function-signature-change-requires-drop.md`
- `benchmark/013-sequence-identity-transitions.md`
- `benchmark/015-trigger-update-of-columns.md`
- `benchmark/016-unique-index-nulls-not-distinct.md`
- `benchmark/017-temporal-without-overlaps-period-constraints.md`
- `benchmark/019-columnless-check-no-inherit.md`
- `benchmark/020-table-unique-nulls-not-distinct.md`
- `benchmark/review-memory.json`
- `docs/parity-refresh-2026-05-01.md`
- `docs/parity-issue-drafts-2026-05-01.md`

