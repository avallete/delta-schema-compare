# Parity refresh report — 2026-04-29

This report summarizes the latest parity comparison between:

- `pgschema` (`repos/pgschema` @ `cdac18aa71c35450636f4cc24d2726863c114492`)
- `pg-delta` (`repos/pg-toolbelt` @ `67029213ea0e6e734849abfef4f051f8c3e02a5b`)

## 1) Benchmark status refresh

The benchmark tracks nine historical parity scenarios. After refreshing the
submodules and re-checking the current pg-toolbelt issue/PR state, all nine are
now solved in the current pg-delta snapshot.

### Benchmark entries updated in this refresh

- pgschema [#190](https://github.com/pgplex/pgschema/issues/190) ->
  pg-toolbelt issue [#130](https://github.com/supabase/pg-toolbelt/issues/130)
  (**closed**), PR
  [#146](https://github.com/supabase/pg-toolbelt/pull/146) (**closed**):
  benchmark entry `005` flipped from tracked to solved after verifying the
  current mainline source/tests now emit `USING` casts and safe default
  sequencing.
- pgschema [#342](https://github.com/pgplex/pgschema/issues/342) ->
  pg-toolbelt issue [#140](https://github.com/supabase/pg-toolbelt/issues/140)
  (**closed**), PR
  [#200](https://github.com/supabase/pg-toolbelt/pull/200) (**merged**):
  benchmark entry `015` refreshed to point at the landed `UPDATE OF` trigger
  integration coverage.
- pgschema [#355](https://github.com/pgplex/pgschema/issues/355) ->
  pg-toolbelt issue [#183](https://github.com/supabase/pg-toolbelt/issues/183)
  (**closed**), PR
  [#185](https://github.com/supabase/pg-toolbelt/pull/185) (**merged**):
  benchmark entry `016` refreshed now that `NULLS NOT DISTINCT` integration
  coverage is present in-tree.
- pgschema [#364](https://github.com/pgplex/pgschema/issues/364) ->
  pg-toolbelt issue [#182](https://github.com/supabase/pg-toolbelt/issues/182)
  (**closed**), PR
  [#213](https://github.com/supabase/pg-toolbelt/pull/213) (**merged**):
  benchmark entry `017` refreshed to reflect the landed PG18 temporal
  constraint support and integration coverage.
- pgschema [#386](https://github.com/pgplex/pgschema/issues/386) ->
  pg-toolbelt issue [#198](https://github.com/supabase/pg-toolbelt/issues/198)
  (**closed**), PR
  [#212](https://github.com/supabase/pg-toolbelt/pull/212) (**merged**):
  benchmark entry `019` refreshed now that both column-less `CHECK (FALSE) NO
  INHERIT` regressions exist in the integration suite.

### Benchmark entries already solved and left as historical context

- pgschema [#326](https://github.com/pgplex/pgschema/issues/326) ->
  pg-toolbelt issue [#132](https://github.com/supabase/pg-toolbelt/issues/132),
  PR [#214](https://github.com/supabase/pg-toolbelt/pull/214)
- pgschema [#268](https://github.com/pgplex/pgschema/issues/268) ->
  pg-toolbelt issue [#133](https://github.com/supabase/pg-toolbelt/issues/133),
  PR [#149](https://github.com/supabase/pg-toolbelt/pull/149)
- pgschema [#279](https://github.com/pgplex/pgschema/issues/279) ->
  pg-toolbelt issue [#138](https://github.com/supabase/pg-toolbelt/issues/138),
  PR [#154](https://github.com/supabase/pg-toolbelt/pull/154)
- pgschema [#373](https://github.com/pgplex/pgschema/issues/373) ->
  pg-toolbelt issue [#184](https://github.com/supabase/pg-toolbelt/issues/184),
  PR [#187](https://github.com/supabase/pg-toolbelt/pull/187)

## 2) Open pgschema issue screening

The benchmark/issue SOP says to refresh existing known parity state first, then
screen remaining open pgschema issues while avoiding duplicate pg-toolbelt
trackers. This refresh followed that order.

### Still tracked in pg-toolbelt

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) ->
  pg-toolbelt [#218](https://github.com/supabase/pg-toolbelt/issues/218)
  remains relevant. Pg-delta's table constraint model and diff code already
  carry `deferrable` / `initially_deferred`, but there is still no exact
  roundtrip regression for `UNIQUE ... DEFERRABLE INITIALLY DEFERRED`, so the
  tracker still represents useful missing parity coverage.
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) ->
  pg-toolbelt [#219](https://github.com/supabase/pg-toolbelt/issues/219)
  remains relevant. The current tree still does not contain a dedicated
  regression for function privilege diffs on enum-typed function signatures.

### Covered in pg-delta / no duplicate issue drafted

- pgschema [#362](https://github.com/pgplex/pgschema/issues/362) — numeric
  precision changes are covered in
  `tests/integration/alter-table-operations.test.ts`.
- pgschema [#401](https://github.com/pgplex/pgschema/issues/401) —
  `RETURNS SETOF <table>` dependency ordering is covered in
  `tests/integration/table-function-dependency-ordering.test.ts` and
  `tests/integration/table-function-circular-dependency.test.ts`.
- pgschema [#408](https://github.com/pgplex/pgschema/issues/408) — quoted
  custom/reserved type names do not justify a new pg-toolbelt tracker; pg-delta
  preserves type names through `format_type(...)` and already has quoted-type
  coverage in `tests/integration/type-operations.test.ts`.
- pgschema [#414](https://github.com/pgplex/pgschema/issues/414) — view
  recreation ordering after a column add is already covered by pg-toolbelt
  issue [#139](https://github.com/supabase/pg-toolbelt/issues/139) (closed) and
  the regression in `tests/integration/view-operations.test.ts`.
- pgschema [#415](https://github.com/pgplex/pgschema/issues/415) — materialized
  view refactor/drop semantics are already covered by pg-toolbelt issue
  [#133](https://github.com/supabase/pg-toolbelt/issues/133) and
  `tests/integration/materialized-view-operations.test.ts`; no duplicate draft
  was needed.
- pgschema [#416](https://github.com/pgplex/pgschema/issues/416) — aggregate
  support is already present in pg-delta and covered in
  `tests/integration/aggregate-operations.test.ts`; no duplicate draft was
  needed.
- pgschema [#418](https://github.com/pgplex/pgschema/issues/418) — the failure
  is specific to pgschema's online-DDL rewrite adding `CONCURRENTLY`. Pg-delta
  reuses catalog-backed index definitions via `pg_get_indexdef(...)` and does
  not inject `CONCURRENTLY`, so no parity tracker was drafted.
- pgschema [#420](https://github.com/pgplex/pgschema/issues/420) —
  `varchar(n)[]` typmod fidelity is preserved through pg-delta's `data_type_str`
  handling, so no duplicate pg-toolbelt tracker was drafted.
- pgschema [#421](https://github.com/pgplex/pgschema/issues/421) — quoted
  mixed-case foreign key columns are already aligned with pg-delta's use of
  `quote_ident(...)` and `pg_get_constraintdef(...)`; no duplicate tracker was
  drafted.
- pgschema [#422](https://github.com/pgplex/pgschema/issues/422) — quoted
  mixed-case custom type names are already aligned with pg-delta's use of
  `format_type(...)`; no duplicate tracker was drafted.

### Not parity work for pg-delta

- pgschema [#406](https://github.com/pgplex/pgschema/issues/406)
- pgschema [#407](https://github.com/pgplex/pgschema/issues/407)
- pgschema [#409](https://github.com/pgplex/pgschema/issues/409)
- pgschema [#419](https://github.com/pgplex/pgschema/issues/419)

These are `.pgschemaignore` / packaging surface-area items specific to
pgschema's own workflow rather than pg-delta parity gaps.

## 3) Recent closed-issue notes

- pgschema [#396](https://github.com/pgplex/pgschema/issues/396) — covered in
  pg-delta's current table-constraint extraction and integration coverage.
- pgschema [#399](https://github.com/pgplex/pgschema/issues/399) — not a
  pg-delta parity gap; this is tied to pgschema's temp-schema SQL rewrite
  workflow.
- pgschema [#403](https://github.com/pgplex/pgschema/issues/403) — not a
  pg-delta parity gap; this is tied to pgschema's temp-schema validation
  architecture.
- pgschema [#412](https://github.com/pgplex/pgschema/issues/412) — treated as
  covered in the current pg-delta snapshot. The existing benchmark entry for
  the related `NULLS NOT DISTINCT` unique-index parity work (`016`) was updated
  to reflect the landed integration coverage now present in pg-delta.

## 4) Outcome of this refresh

- `benchmark/README.md` was refreshed to the new submodule SHAs and current
  pg-toolbelt issue/PR states.
- `benchmark/review-memory.json` was updated so future automation runs can reuse
  the current verdicts for the latest upstream SHAs.
- Historical benchmark entries `005`, `015`, `016`, `017`, and `019` were
  rewritten from "missing/tracked" language to current solved-parity language.
- No new pg-toolbelt issue drafts were needed in this run.

The only open parity trackers that still remain actionable after this refresh
are:

- [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
