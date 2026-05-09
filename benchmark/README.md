# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-05-09)

Refreshed against:

- `repos/pg-toolbelt` @ `102ef99ae5aabb29510d48b39fbb8ecee34f5458`
- `repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`

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
| 020 | [Table constraint NULLS NOT DISTINCT](020-unique-constraint-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | — | — | **Not covered in pg-delta** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.
>
> Note: some original tracking issues and PRs no longer mirror how a fix landed
> in pg-delta main. For example, pgschema #190 is now covered in the current
> pg-delta tree even though the original draft PR #146 was later closed.

## Active gaps after refresh

Only this benchmark scenario remains active as unresolved:

- **020** — table-level `UNIQUE ... NULLS NOT DISTINCT` constraints

## Open pgschema issue screening (manual sweep)

Screened open issues against the refreshed pg-delta tree:

- **#362** numeric precision changes — **covered** in `alter-table-operations.test.ts`
- **#366** function privilege signatures with enum argument types — **tracked** by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered**
- **#404** deferrable unique constraints — **tracked** by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#408** quoted or reserved custom type names in emitted SQL — **covered**
- **#414** new-column plus view ordering — **watch item**; pgschema [PR #417](https://github.com/pgplex/pgschema/pull/417) is still open, so no duplicate pg-toolbelt issue was drafted
- **#415** materialized-view drop relkind mismatch — **covered** by materialized-view integration coverage
- **#416** custom aggregates omitted from dump — **covered** by aggregate integration coverage
- **#418** `CREATE INDEX CONCURRENTLY` on partitioned parents — **not parity work for pg-delta** (pgschema online-DDL rewrite behavior)
- **#420** `varchar(n)[]` length modifier dump bug — **no duplicate issue drafted**; it needs a pg-delta-specific failing repro before tracking
- **#421 / #422** quoted mixed-case FK columns or custom types — **not parity work for pg-delta** (pgschema temp-schema roundtrip behavior)
- **#427** schema-qualified functions in RLS policy expressions — **covered** by pg-delta's policy-expression extraction plus qualified-function coverage

Detailed refresh notes and draft follow-up text live in:

- [`docs/parity-refresh-2026-05-09.md`](../docs/parity-refresh-2026-05-09.md)
- [`docs/parity-issue-drafts-2026-05-09.md`](../docs/parity-issue-drafts-2026-05-09.md)

## Recent closed-issue screening notes

- **#410** `name` type dump bug — **covered** by `format_type(...)`-backed type extraction
- **#412** table-level `UNIQUE NULLS NOT DISTINCT` constraints — **not covered** in current pg-delta; benchmarked as item **020**
- **#423** `UNLOGGED` tables — **covered** by table persistence diff and create support

## Automation caveat

Current automation scripts still filter pgschema issues by `Bug` / `Feature`
labels, but several recent parity-relevant pgschema issues are unlabeled.
Manual GitHub issue and PR screening remains necessary until that filter is
broadened.
