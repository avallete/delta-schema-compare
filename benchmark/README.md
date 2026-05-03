# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta. Historical writeups are retained even after fixes
land so the benchmark remains a durable record of what changed.

## Latest refresh snapshot (2026-05-03)

Refreshed against:

- `repos/pg-toolbelt` @ `c7e97f8865d05e0afab0ea2a5d7107aa7b42ec8f`
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
| 020 | [Table-constraint UNIQUE NULLS NOT DISTINCT](020-unique-constraint-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | — | — | **Not covered in pg-delta** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> matrix above is the current source of truth for parity status.
>
> The biggest change in this refresh is benchmark **005**: pg-toolbelt issue
> [#130](https://github.com/supabase/pg-toolbelt/issues/130) is now closed, the
> earlier draft PR [#146](https://github.com/supabase/pg-toolbelt/pull/146) was
> closed unmerged, and the effective fix landed in merged PR
> [#231](https://github.com/supabase/pg-toolbelt/pull/231).

## Active gaps after refresh

Only one historical benchmark scenario remains unresolved in the current
pg-delta snapshot:

- **020** — table-level `UNIQUE NULLS NOT DISTINCT` constraints

Open parity work from currently open pgschema issues remains tracked separately:

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) →
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) →
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

## Open pgschema issue screening (manual sweep, no duplicate tracker drafted)

Screened open candidates:

- **#362** numeric precision changes — **covered** in current pg-delta type
  diffing and integration tests
- **#366** enum-arg function privilege signatures — **tracked** by
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered** in current
  pg-delta integration tests
- **#404** deferrable unique constraints — **tracked** by
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#408** quoted custom / reserved type names in plan output — **no duplicate
  issue drafted**; pg-delta preserves `data_type_str` from `format_type(...)`
- **#414** views vs new-column ordering — **no duplicate issue drafted**;
  pg-delta already models column-level dependencies for referenced relations
- **#415** materialized-view kind confusion on drop / recreate — **no duplicate
  issue drafted**; pg-delta has dedicated materialized-view replacement coverage
- **#416** custom aggregates missing from dump — **no duplicate issue drafted**;
  aggregate support and integration coverage already exist in pg-delta
- **#418** `CREATE INDEX CONCURRENTLY` on partitioned parents — **no duplicate
  issue drafted**; pg-delta does not inject `CONCURRENTLY` and reuses captured
  index definitions
- **#420** `varchar(n)[]` typmod loss — **covered** by `format_type(...)`
  extraction and current roundtrip paths
- **#421** quoted mixed-case FK columns — **covered** by quoted constraint-column
  extraction in the table model
- **#422** quoted mixed-case custom types — **covered** by `format_type(...)`
  plus preserved quoted custom type names
- **#406 / #407 / #409 / #419** `.pgschemaignore` follow-ups — **not parity
  work for pg-delta** (pgschema-specific ignore-file surface area)

Historical draft text is still recorded for the two tracked open parity issues:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)

## Recent closed-issue screening notes

- **#410** built-in `name` type dumped as `char[]` — **no duplicate pg-toolbelt
  issue drafted**; pg-delta uses `format_type(a.atttypid, a.atttypmod)` and
  serializes `data_type_str` directly
- **#412** table-level `UNIQUE NULLS NOT DISTINCT` — **new historical benchmark
  gap**; see [020](020-unique-constraint-nulls-not-distinct.md)
- Draft tracker issue text for the unresolved #412 gap is stored in
  [`docs/parity-issue-drafts-2026-05-03.md`](../docs/parity-issue-drafts-2026-05-03.md)
- **#423** `UNLOGGED` dropped from table definitions — **no duplicate
  pg-toolbelt issue drafted**; pg-delta tracks `relpersistence`, serializes
  `CREATE UNLOGGED TABLE`, and diffs `LOGGED ↔ UNLOGGED`
- **#396** table-level CHECK constraints omitted from dump — **covered** in
  current pg-delta and now backed by benchmark 019's focused integration tests
- **#399** qualified references inside function bodies — **not a pg-delta parity
  gap**; specific to pgschema's temp-schema SQL rewrite path
- **#403** table row-type composite parameters in function validation — **not a
  pg-delta parity gap**; specific to pgschema's temp-schema validation
  architecture

## Workflow caveat

Manual unlabeled-issue sweeps remain necessary for this repository because
pgschema issues often ship without `Bug` / `Feature` labels. The compare
automation can therefore miss relevant parity work in dry-run unless the manual
screening notes above are also kept up to date.
