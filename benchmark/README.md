# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-05-02)

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
| 020 | [Unique constraint NULLS NOT DISTINCT](020-unique-constraint-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | — | — | **Not covered (issue draft prepared)** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.

## Active gaps after refresh

Only this benchmark scenario remains active as unresolved:

- **020** — table-level `UNIQUE NULLS NOT DISTINCT` constraints

Draft text for the unresolved historical gap is recorded here:

- [`docs/parity-issue-drafts-2026-05-02.md`](../docs/parity-issue-drafts-2026-05-02.md)

## Open pgschema issue screening (2026-05-02)

Screened parity-relevant open issues:

- **#362** numeric precision changes — **covered** in
  `tests/integration/alter-table-operations.test.ts`
- **#366** function privilege signatures with enum argument types —
  **tracked** by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered** in
  table/function dependency integration tests
- **#404** deferrable unique constraints — **tracked** by
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#408** quoted custom / reserved type names in plan output — **no duplicate
  pg-toolbelt issue drafted**; pg-delta keeps quoted type names via
  `format_type(...)` / `quote_ident(...)`
- **#414** new column + dependent view ordering — **covered** by current
  view replacement / ordering integration coverage
- **#415** materialized-view drops emitted as plain view drops — **covered** by
  materialized-view-specific replacement handling and integration tests
- **#416** custom aggregates dropped from dump — **covered** by aggregate object
  support and integration coverage in `aggregate-operations.test.ts`
- **#418** `CREATE INDEX CONCURRENTLY` on partitioned parents — **not a
  pg-delta parity gap**; no duplicate pg-toolbelt issue drafted
- **#420** `varchar(n)[]` typmod preservation — **no duplicate pg-toolbelt
  issue drafted**; pg-delta uses `format_type(a.atttypid, a.atttypmod)` for
  column `data_type_str`
- **#421** quoted mixed-case FK columns — **no duplicate pg-toolbelt issue
  drafted**; pg-delta extracts quoted identifiers with `quote_ident(...)`
- **#422** quoted mixed-case custom types — **no duplicate pg-toolbelt issue
  drafted**; pg-delta reuses quoted `format_type(...)` output and quoted custom
  type names
- **#406 / #407 / #409** `.pgschemaignore` follow-ups — **not parity work for
  pg-delta** (pgschema-specific ignore-file surface area)

Historical draft text for the two still-open tracked parity issues remains here:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)

## Recent closed-issue screening notes

- **#412** table-level `UNIQUE NULLS NOT DISTINCT` constraints — **not
  covered** in current pg-delta diff coverage; new benchmark entry `020` added
  and draft issue text prepared
