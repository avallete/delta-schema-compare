# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

See also the dated refresh report for the latest manual review:

- [`docs/parity-refresh-2026-05-05.md`](../docs/parity-refresh-2026-05-05.md)

## Latest refresh snapshot (2026-05-05)

Refreshed against:

- `repos/pg-toolbelt` @ `9a0831a54e03d221f0461323ae93fb676722cc14`
- `repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`

## Benchmark status matrix

| # | File | pgschema | pg-toolbelt issue | pg-toolbelt PR | Current status |
|---|---|---|---|---|---|
| 005 | [ALTER column type USING](005-alter-column-type-using-clause.md) | [#190](https://github.com/pgplex/pgschema/issues/190) | [#130](https://github.com/supabase/pg-toolbelt/issues/130) (closed) | [#146](https://github.com/supabase/pg-toolbelt/pull/146) (closed, unmerged) | **Solved in current pg-delta** |
| 007 | [Function signature DROP](007-function-signature-change-requires-drop.md) | [#326](https://github.com/pgplex/pgschema/issues/326) | [#132](https://github.com/supabase/pg-toolbelt/issues/132) (closed) | [#214](https://github.com/supabase/pg-toolbelt/pull/214) (merged) | **Solved in pg-delta** |
| 008 | [Mat view cascade deps](008-materialized-view-cascade-dependencies.md) | [#268](https://github.com/pgplex/pgschema/issues/268) | [#133](https://github.com/supabase/pg-toolbelt/issues/133) (closed) | [#149](https://github.com/supabase/pg-toolbelt/pull/149) (merged) | **Solved in pg-delta** |
| 013 | [Sequence identity](013-sequence-identity-transitions.md) | [#279](https://github.com/pgplex/pgschema/issues/279) | [#138](https://github.com/supabase/pg-toolbelt/issues/138) (closed) | [#154](https://github.com/supabase/pg-toolbelt/pull/154) (merged) | **Solved in pg-delta** |
| 015 | [Trigger UPDATE OF columns](015-trigger-update-of-columns.md) | [#342](https://github.com/pgplex/pgschema/issues/342) | [#140](https://github.com/supabase/pg-toolbelt/issues/140) (closed) | [#200](https://github.com/supabase/pg-toolbelt/pull/200) (merged) | **Solved in pg-delta** |
| 016 | [Unique index NULLS NOT DISTINCT](016-unique-index-nulls-not-distinct.md) | [#355](https://github.com/pgplex/pgschema/issues/355) | [#183](https://github.com/supabase/pg-toolbelt/issues/183) (closed) | [#185](https://github.com/supabase/pg-toolbelt/pull/185) (merged) | **Solved in pg-delta** |
| 017 | [Temporal WITHOUT OVERLAPS / PERIOD constraints](017-temporal-without-overlaps-period-constraints.md) | [#364](https://github.com/pgplex/pgschema/issues/364) | [#182](https://github.com/supabase/pg-toolbelt/issues/182) (closed) | [#213](https://github.com/supabase/pg-toolbelt/pull/213) (merged) | **Solved in pg-delta** |
| 018 | [Cross-table RLS policy ordering](018-cross-table-rls-policy-ordering.md) | [#373](https://github.com/pgplex/pgschema/issues/373) | [#184](https://github.com/supabase/pg-toolbelt/issues/184) (closed) | [#187](https://github.com/supabase/pg-toolbelt/pull/187) (merged) | **Solved in pg-delta** |
| 019 | [Column-less CHECK NO INHERIT](019-columnless-check-no-inherit.md) | [#386](https://github.com/pgplex/pgschema/issues/386) | [#198](https://github.com/supabase/pg-toolbelt/issues/198) (closed) | [#212](https://github.com/supabase/pg-toolbelt/pull/212) (merged) | **Solved in pg-delta** |
| 020 | [Table UNIQUE NULLS NOT DISTINCT](020-unique-constraint-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | — | — | **Not yet covered** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.
>
> Note: benchmark item 005 is now solved in current pg-delta even though the
> original implementation PR (`pg-toolbelt#146`) was closed without merge. The
> current source and integration tests cover the behavior directly.

## Active gaps after refresh

Only this benchmark scenario remains active as unresolved:

- **020** — table-level `UNIQUE NULLS NOT DISTINCT` constraints

Draft issue bodies for unresolved or newly screened scenarios are recorded in:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)
- [`docs/parity-issue-drafts-2026-05-05.md`](../docs/parity-issue-drafts-2026-05-05.md)

## New open pgschema issue screening (draft-only output)

Screened candidates:

- **#362** numeric precision changes — **covered** in
  `alter-table-operations.test.ts`
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered** in
  `table-function-dependency-ordering.test.ts` and
  `table-function-circular-dependency.test.ts`
- **#404** deferrable unique constraints — **tracked** by
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#366** function privilege signatures with enum argument types —
  **tracked** by
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#415** materialized-view refactor drop kind — **no duplicate issue
  drafted**; current pg-delta has a dedicated materialized-view drop path
- **#416** custom aggregates omitted from dump — **no duplicate issue
  drafted**; pg-delta already has aggregate object support and integration
  coverage
- **#418** partitioned-parent concurrent index rewrite — **no duplicate issue
  drafted**; pg-delta preserves parent-index DDL without pgschema's
  `CONCURRENTLY` rewrite path
- **#420** `varchar(n)[]` typmod retention — **no duplicate issue drafted**;
  pg-delta still uses `format_type(a.atttypid, a.atttypmod)` for column
  `data_type_str`
- **#421 / #422** quoted mixed-case FK columns and custom type names —
  **no duplicate issue drafted**; pg-delta stores quoted identifiers and
  catalog-derived type strings rather than replaying temp-schema names
- **#427** schema-qualified functions in RLS policies — **no duplicate issue
  drafted**; pg-delta reads policy expressions via `pg_get_expr(...)`
- **#414** view creation vs added-column ordering — **draft issue body
  prepared** in
  [`docs/parity-issue-drafts-2026-05-05.md`](../docs/parity-issue-drafts-2026-05-05.md);
  no existing pg-toolbelt issue/PR found
- **#408** quoted reserved composite type names — **follow-up noted in the
  refresh report**; no duplicate pg-toolbelt issue drafted yet because current
  pg-delta serializers already emit catalog-derived `data_type_str`

## Recent closed-issue screening notes

- **#410** built-in `name` type dumped as `char[]` — **covered** by pg-delta's
  `format_type(...)`-based column extraction
- **#423** `UNLOGGED` tables dropped from dump — **covered** by pg-delta's
  table-persistence diff and create support (`SET UNLOGGED`, `CREATE UNLOGGED
  TABLE`)
- **#412** table-level `UNIQUE NULLS NOT DISTINCT` — **not yet covered** in
  current pg-delta benchmark item 020
