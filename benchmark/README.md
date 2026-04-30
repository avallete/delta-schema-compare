# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-04-30)

Refreshed against:

- `repos/pg-toolbelt` @ `67029213ea0e6e734849abfef4f051f8c3e02a5b`
- `repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`

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
| 020 | [Table-level UNIQUE NULLS NOT DISTINCT](020-unique-constraint-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | — | — | **Not covered (draft issue needed)** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.
>
> Note: benchmark 005 previously pointed at draft PR #146. That draft was later
> closed unmerged after the real fix landed in merged PR #231.

## Active gaps after refresh

Only this benchmark scenario remains active as unresolved:

- **020** — table-level `UNIQUE NULLS NOT DISTINCT` constraints

All earlier benchmarked scenarios (005-019) are now solved in the refreshed
pg-delta snapshot.

## New open pgschema issue screening (draft-only output)

Screened candidates:

- **#362** numeric precision changes — **covered** in pg-delta integration tests
- **#366** function privilege signatures with enum argument types — **tracked**
  by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#404** deferrable unique constraints — **tracked** by
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#408** quoted custom / reserved type names in plan output — **no duplicate
  pg-toolbelt issue drafted**; pg-delta still preserves quoted type names via
  `format_type(...)`-backed extraction
- **#414** views ordered before newly added columns — **covered** by the select-`*`
  view replacement coverage in `view-operations.test.ts` and mixed create /
  replace ordering coverage in `mixed-objects.test.ts`
- **#415** materialized-view refactor emits `DROP VIEW` instead of
  `DROP MATERIALIZED VIEW` — **covered** by materialized-view replacement tests;
  no duplicate issue drafted
- **#416** custom aggregates silently dropped from dump — **no duplicate
  pg-toolbelt issue drafted**; aggregate lifecycle and privilege coverage already
  exists in `aggregate-operations.test.ts`
- **#418** `CREATE INDEX CONCURRENTLY` on partitioned parents — **no duplicate
  pg-toolbelt issue drafted**; pg-delta serializes partitioned-parent indexes
  without `CONCURRENTLY` and has partitioned-table index coverage
- **#420** `varchar(n)[]` length modifier silently dropped in dump —
  **covered** by `format_type(a.atttypid, a.atttypmod)`-backed extraction
- **#421 / #422** quoted mixed-case FK columns / custom types — **not parity
  gaps for pg-delta**; these are specific to pgschema's dump + temp-schema
  roundtrip architecture, while pg-delta quotes identifiers during extraction
- **#423** `UNLOGGED` tables dropped from definitions — **covered** by table
  persistence support (`CREATE UNLOGGED TABLE`, `ALTER TABLE ... SET
  UNLOGGED/LOGGED`)
- **#406 / #407 / #409** `.pgschemaignore` follow-ups — **not parity work for
  pg-delta** (pgschema-specific ignore-file surface area)

Historical draft text is recorded in markdown for the tracked or not-yet-filed
parity issues:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)
  — historical drafts for pgschema #404 / #366, now tracked upstream as
  pg-toolbelt #218 / #219
- [`docs/parity-issue-drafts-2026-04-30.md`](../docs/parity-issue-drafts-2026-04-30.md)
  — new draft for pgschema #412 (`UNIQUE NULLS NOT DISTINCT` table constraints)

## Recent closed-issue screening notes

- **#410** built-in `name` type dumped as `char[]` — **covered** by
  `format_type(...)`-backed extraction in pg-delta
- **#412** table-level `UNIQUE NULLS NOT DISTINCT` — **not covered**; added as
  benchmark 020 and drafted for a future pg-toolbelt issue
- **#423** `UNLOGGED` tables dropped from definitions — **covered** by
  pg-delta's table persistence model and serializer support
