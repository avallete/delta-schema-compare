# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-05-21)

Refreshed against:

- `repos/pg-toolbelt` @ `0bd7dc229340157e31ae816261cf01744e5ad295`
- `repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`

This refresh found **no parity-state delta** versus the 2026-05-19 snapshot:
benchmark **020** remains the only unresolved historical gap, and the open
pg-delta parity trackers remain
[pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218) for
pgschema **#404** plus
[pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219) for
pgschema **#366**.

Latest detailed report:

- [`docs/parity-refresh-2026-05-21.md`](../docs/parity-refresh-2026-05-21.md)

## Benchmark status matrix

| # | File | pgschema | pg-toolbelt issue | pg-toolbelt PR | Current status |
|---|---|---|---|---|---|
| 005 | [ALTER column type USING](005-alter-column-type-using-clause.md) | [#190](https://github.com/pgplex/pgschema/issues/190) | [#130](https://github.com/supabase/pg-toolbelt/issues/130) (closed) | [#231](https://github.com/supabase/pg-toolbelt/pull/231) (merged) | **Solved in pg-delta** |
| 007 | [Function signature DROP](007-function-signature-change-requires-drop.md) | [#326](https://github.com/pgplex/pgschema/issues/326) | [#132](https://github.com/supabase/pg-toolbelt/issues/132) (closed) | [#214](https://github.com/supabase/pg-toolbelt/pull/214) (merged) | **Solved in pg-delta** |
| 008 | [Mat view cascade deps](008-materialized-view-cascade-dependencies.md) | [#268](https://github.com/pgplex/pgschema/issues/268) | [#133](https://github.com/supabase/pg-toolbelt/issues/133) (closed) | [#149](https://github.com/supabase/pg-toolbelt/pull/149) (merged) | **Solved in pg-delta** |
| 013 | [Sequence identity](013-sequence-identity-transitions.md) | [#279](https://github.com/pgplex/pgschema/issues/279) | [#138](https://github.com/supabase/pg-toolbelt/issues/138) (closed) | [#154](https://github.com/supabase/pg-toolbelt/pull/154) (merged) | **Solved in pg-delta** |
| 015 | [Trigger UPDATE OF columns](015-trigger-update-of-columns.md) | [#342](https://github.com/pgplex/pgschema/issues/342) | [#140](https://github.com/supabase/pg-toolbelt/issues/140) (closed) | [#200](https://github.com/supabase/pg-toolbelt/pull/200) (merged) | **Solved in pg-delta** |
| 016 | [Unique index NULLS NOT DISTINCT](016-unique-index-nulls-not-distinct.md) | [#355](https://github.com/pgplex/pgschema/issues/355) | [#183](https://github.com/supabase/pg-toolbelt/issues/183) (closed) | [#185](https://github.com/supabase/pg-toolbelt/pull/185) (merged) | **Solved in pg-delta** |
| 017 | [Temporal WITHOUT OVERLAPS / PERIOD constraints](017-temporal-without-overlaps-period-constraints.md) | [#364](https://github.com/pgplex/pgschema/issues/364) | [#182](https://github.com/supabase/pg-toolbelt/issues/182) (closed) | [#213](https://github.com/supabase/pg-toolbelt/pull/213) (merged) | **Solved in pg-delta** |
| 018 | [Cross-table RLS policy ordering](018-cross-table-rls-policy-ordering.md) | [#373](https://github.com/pgplex/pgschema/issues/373) | [#184](https://github.com/supabase/pg-toolbelt/issues/184) (closed) | [#187](https://github.com/supabase/pg-toolbelt/pull/187) (merged) | **Solved in pg-delta** |
| 019 | [Column-less CHECK NO INHERIT](019-columnless-check-no-inherit.md) | [#386](https://github.com/pgplex/pgschema/issues/386) | [#198](https://github.com/supabase/pg-toolbelt/issues/198) (closed) | [#212](https://github.com/supabase/pg-toolbelt/pull/212) (merged) | **Solved in pg-delta** |
| 020 | [Table constraint UNIQUE NULLS NOT DISTINCT](020-table-constraint-unique-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | — | — | **Not covered in pg-delta** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.

## Active gaps after refresh

Only this historical benchmark scenario remains active as unresolved:

- **020** — table-level `UNIQUE NULLS NOT DISTINCT` constraints
  ([pgschema#412](https://github.com/pgplex/pgschema/issues/412))

The two active open-issue parity trackers remain:

- **#404** — tracked by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#366** — tracked by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

## New open pgschema issue screening (draft-only output)

Screened candidates:

- **#362** numeric precision changes — **covered** in pg-delta integration tests
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered** in pg-delta integration tests
- **#415** materialized-view refactor drops — **covered** in pg-delta's
  materialized-view replacement integration tests
- **#436** required extensions in dump output — **covered** in pg-delta's
  extension export and dependency-ordering coverage
- **#404** deferrable unique constraints — **tracked** by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#366** function privilege signatures with enum argument types — **tracked** by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#408** quoted custom / reserved type names in plan output — **screened, no duplicate issue drafted**; pg-delta preserves column type text from `format_type(...)` and already roundtrips quoted custom types in `type-operations.test.ts`
- **#414** add-column plus new view ordering — **screened, no duplicate issue
  drafted**; current view ordering coverage exercises the same dependency
  family, but there is still no focused roundtrip for the exact pgschema repro
- **#416** custom aggregates omitted from dump — **not a current pg-delta
  parity gap**; aggregates are first-class catalog objects in pg-delta and
  already have create / drop / privilege coverage
- **#418** partitioned-parent indexes rewritten to `CREATE INDEX CONCURRENTLY` — **screened, no duplicate issue drafted**; current pg-delta does not inject `CONCURRENTLY` and already roundtrips parent-table indexes in `partitioned-table-operations.test.ts`
- **#420** `varchar(n)[]` typmods — **screened, no duplicate issue drafted**;
  column extraction uses `format_type(...)`, but current coverage is still
  indirect rather than a focused regression for the exact array-typmod case
- **#421** quoted mixed-case FK columns — **screened, no duplicate issue
  drafted**; table constraint extraction quotes column names via
  `quote_ident(...)`, but there is no focused mixed-case FK roundtrip yet
- **#422** quoted mixed-case custom types — **screened, no duplicate issue
  drafted**; pg-delta already preserves quoted type text via `format_type(...)`,
  but there is no focused `"MyStatus"` regression yet
- **#427** schema-qualified functions in RLS policies — **screened, no
  duplicate issue drafted**; policy expressions come from `pg_get_expr(...)`,
  but the current coverage remains adjacent rather than a dedicated
  `auth.uid()` regression
- **#49 / #406 / #407 / #409 / #419 / #429 / #439** rename workflow /
  `.pgschemaignore` / constraint-separation follow-ups — **not parity work for
  pg-delta** (pgschema-specific workflow/config surface area rather than a
  concrete pg-delta diff gap)

Current draft text is recorded in markdown here:

- [`docs/parity-issue-drafts-2026-05-17.md`](../docs/parity-issue-drafts-2026-05-17.md)

## Recent closed-issue screening notes

- **#396** table-level CHECK constraints omitted from dump — **covered** in
  pg-delta's table-constraint extraction and integration coverage
- **#399** qualified references inside function bodies — **not a pg-delta
  parity gap**; this is specific to pgschema's temp-schema SQL rewrite path
- **#403** table row-type composite parameters in function validation — **not a
  pg-delta parity gap**; this is specific to pgschema's temp-schema validation
  architecture
- **#410** built-in `name` columns dumped as `char[]` — **screened, no
  benchmark item added**; pg-delta column extraction preserves `data_type_str`
  via `format_type(a.atttypid, a.atttypmod)`, so this pgschema dump bug does
  not appear reproducible in current pg-delta
- **#423** `UNLOGGED` dropped from table definitions — **covered** in
  pg-delta's table persistence model and unit coverage for both
  `CREATE UNLOGGED TABLE` and `ALTER TABLE ... SET UNLOGGED`
- **#412** table-level `UNIQUE NULLS NOT DISTINCT` constraints — **not covered**
  in current pg-delta; benchmarked as
  [020](020-table-constraint-unique-nulls-not-distinct.md) and drafted in
  `docs/parity-issue-drafts-2026-05-17.md`
