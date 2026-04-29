# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-04-29)

Refreshed against:

- `repos/pg-toolbelt` @ `67029213ea0e6e734849abfef4f051f8c3e02a5b`
- `repos/pgschema` @ `cdac18aa71c35450636f4cc24d2726863c114492`

## Benchmark status matrix

| # | File | pgschema | pg-toolbelt issue | pg-toolbelt PR | Current status |
|---|---|---|---|---|---|
| 005 | [ALTER column type USING](005-alter-column-type-using-clause.md) | [#190](https://github.com/pgplex/pgschema/issues/190) | [#130](https://github.com/supabase/pg-toolbelt/issues/130) (closed) | [#146](https://github.com/supabase/pg-toolbelt/pull/146) (closed) | **Solved in pg-delta** |
| 007 | [Function signature DROP](007-function-signature-change-requires-drop.md) | [#326](https://github.com/pgplex/pgschema/issues/326) | [#132](https://github.com/supabase/pg-toolbelt/issues/132) (closed) | [#214](https://github.com/supabase/pg-toolbelt/pull/214) (merged) | **Solved in pg-delta** |
| 008 | [Mat view cascade deps](008-materialized-view-cascade-dependencies.md) | [#268](https://github.com/pgplex/pgschema/issues/268) | [#133](https://github.com/supabase/pg-toolbelt/issues/133) (closed) | [#149](https://github.com/supabase/pg-toolbelt/pull/149) (merged) | **Solved in pg-delta** |
| 013 | [Sequence identity](013-sequence-identity-transitions.md) | [#279](https://github.com/pgplex/pgschema/issues/279) | [#138](https://github.com/supabase/pg-toolbelt/issues/138) (closed) | [#154](https://github.com/supabase/pg-toolbelt/pull/154) (merged) | **Solved in pg-delta** |
| 015 | [Trigger UPDATE OF columns](015-trigger-update-of-columns.md) | [#342](https://github.com/pgplex/pgschema/issues/342) | [#140](https://github.com/supabase/pg-toolbelt/issues/140) (closed) | [#200](https://github.com/supabase/pg-toolbelt/pull/200) (merged) | **Solved in pg-delta** |
| 016 | [Unique index NULLS NOT DISTINCT](016-unique-index-nulls-not-distinct.md) | [#355](https://github.com/pgplex/pgschema/issues/355) | [#183](https://github.com/supabase/pg-toolbelt/issues/183) (closed) | [#185](https://github.com/supabase/pg-toolbelt/pull/185) (merged) | **Solved in pg-delta** |
| 017 | [Temporal WITHOUT OVERLAPS / PERIOD constraints](017-temporal-without-overlaps-period-constraints.md) | [#364](https://github.com/pgplex/pgschema/issues/364) | [#182](https://github.com/supabase/pg-toolbelt/issues/182) (closed) | [#213](https://github.com/supabase/pg-toolbelt/pull/213) (merged) | **Solved in pg-delta** |
| 018 | [Cross-table RLS policy ordering](018-cross-table-rls-policy-ordering.md) | [#373](https://github.com/pgplex/pgschema/issues/373) | [#184](https://github.com/supabase/pg-toolbelt/issues/184) (closed) | [#187](https://github.com/supabase/pg-toolbelt/pull/187) (merged) | **Solved in pg-delta** |
| 019 | [Column-less CHECK NO INHERIT](019-columnless-check-no-inherit.md) | [#386](https://github.com/pgplex/pgschema/issues/386) | [#198](https://github.com/supabase/pg-toolbelt/issues/198) (closed) | [#212](https://github.com/supabase/pg-toolbelt/pull/212) (merged) | **Solved in pg-delta** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.
>
> This refresh keys off the behavior present in the latest pg-delta mainline
> snapshot. A scenario can be marked as solved even if the original tracker PR
> ended up closed instead of merged, as long as equivalent behavior is now
> present in the current source tree and integration coverage.

## Active gaps after refresh

No historical benchmark scenario remains active in the current pg-delta
snapshot.

## New open pgschema issue screening (draft-only output)

Screened candidates:

- **#362** numeric precision changes — **covered** in
  `alter-table-operations.test.ts`
- **#366** function privilege signatures with enum argument types —
  **tracked** by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered** in
  `table-function-dependency-ordering.test.ts` and
  `table-function-circular-dependency.test.ts`
- **#404** deferrable unique constraints — **tracked** by
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#408** quoted custom / reserved type names in plan output —
  **no duplicate pg-toolbelt issue drafted**; pg-delta preserves
  `data_type_str` from `format_type(...)` and already has quoted-type coverage
  in `type-operations.test.ts`
- **#414** view ordering after column add — **covered** in
  `view-operations.test.ts`
- **#415** materialized-view drop/refactor semantics — **covered** in
  `materialized-view-operations.test.ts` and
  `src/core/objects/materialized-view/changes/materialized-view.drop.ts`
- **#416** aggregate parity — **covered** in `aggregate-operations.test.ts`
  and pg-delta's aggregate object support
- **#418** partitioned-parent index rewrite failure — **no duplicate
  pg-toolbelt issue drafted**; pg-delta serializes catalog-backed index
  definitions and does not inject `CONCURRENTLY` into partitioned-parent index
  SQL
- **#420** `varchar(n)[]` typmod preservation — **no duplicate pg-toolbelt
  issue drafted**; pg-delta preserves catalog `format_type(...)` output through
  `data_type_str`
- **#421** quoted mixed-case FK columns — **no duplicate pg-toolbelt issue
  drafted**; pg-delta keeps quoted identifiers via `quote_ident(...)` and
  `pg_get_constraintdef(...)`
- **#422** quoted mixed-case custom types — **no duplicate pg-toolbelt issue
  drafted**; pg-delta preserves mixed-case type names via `format_type(...)`
- **#406 / #407 / #409 / #419** `.pgschemaignore` follow-ups — **not parity
  work for pg-delta** (pgschema-specific ignore-file surface area)

Historical draft text is still recorded in markdown for the already-tracked
open parity issues:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)

The full dated refresh summary for this run is stored in:

- [`docs/parity-refresh-2026-04-29.md`](../docs/parity-refresh-2026-04-29.md)

## Recent closed-issue screening notes

- **#396** table-level CHECK constraints omitted from dump — **covered** in
  pg-delta's table-constraint extraction and integration coverage
- **#399** qualified references inside function bodies — **not a pg-delta
  parity gap**; this is specific to pgschema's temp-schema SQL rewrite path
- **#403** table row-type composite parameters in function validation — **not a
  pg-delta parity gap**; this is specific to pgschema's temp-schema validation
  architecture
- **#412** `NULLS NOT DISTINCT` follow-up — **covered in the current
  pg-delta snapshot**; benchmark entry `016` has been refreshed to reflect the
  landed integration coverage for the related unique-index parity case
