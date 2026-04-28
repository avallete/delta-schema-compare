# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-04-28)

GitHub issue/PR state verified via `gh issue view` / `gh pr view` on
`supabase/pg-toolbelt` (local submodule SHAs may differ).

## Benchmark status matrix

| # | File | pgschema | pg-toolbelt issue | pg-toolbelt PR | Current status |
|---|---|---|---|---|---|
| 005 | [ALTER column type USING](005-alter-column-type-using-clause.md) | [#190](https://github.com/pgplex/pgschema/issues/190) | [#130](https://github.com/supabase/pg-toolbelt/issues/130) (open) | [#146](https://github.com/supabase/pg-toolbelt/pull/146) (closed, not merged) | **Open — fix not on main** |
| 007 | [Function signature DROP](007-function-signature-change-requires-drop.md) | [#326](https://github.com/pgplex/pgschema/issues/326) | [#132](https://github.com/supabase/pg-toolbelt/issues/132) (closed) | [#214](https://github.com/supabase/pg-toolbelt/pull/214) (merged) | **Solved in pg-delta** |
| 008 | [Mat view cascade deps](008-materialized-view-cascade-dependencies.md) | [#268](https://github.com/pgplex/pgschema/issues/268) | [#133](https://github.com/supabase/pg-toolbelt/issues/133) (closed) | [#149](https://github.com/supabase/pg-toolbelt/pull/149) (merged) | **Solved in pg-delta** |
| 013 | [Sequence identity](013-sequence-identity-transitions.md) | [#279](https://github.com/pgplex/pgschema/issues/279) | [#138](https://github.com/supabase/pg-toolbelt/issues/138) (closed) | [#154](https://github.com/supabase/pg-toolbelt/pull/154) (merged) | **Solved in pg-delta** |
| 015 | [Trigger UPDATE OF columns](015-trigger-update-of-columns.md) | [#342](https://github.com/pgplex/pgschema/issues/342) | [#140](https://github.com/supabase/pg-toolbelt/issues/140) (closed) | [#200](https://github.com/supabase/pg-toolbelt/pull/200) (merged) | **Solved in pg-delta** |
| 016 | [Unique index NULLS NOT DISTINCT](016-unique-index-nulls-not-distinct.md) | [#355](https://github.com/pgplex/pgschema/issues/355) | [#183](https://github.com/supabase/pg-toolbelt/issues/183) (closed) | [#185](https://github.com/supabase/pg-toolbelt/pull/185) (merged) | **Solved in pg-delta** |
| 017 | [Temporal WITHOUT OVERLAPS / PERIOD constraints](017-temporal-without-overlaps-period-constraints.md) | [#364](https://github.com/pgplex/pgschema/issues/364) | [#182](https://github.com/supabase/pg-toolbelt/issues/182) (closed) | [#213](https://github.com/supabase/pg-toolbelt/pull/213) (merged) | **Solved in pg-delta** |
| 018 | [Cross-table RLS policy ordering](018-cross-table-rls-policy-ordering.md) | [#373](https://github.com/pgplex/pgschema/issues/373) | [#184](https://github.com/supabase/pg-toolbelt/issues/184) (closed) | [#187](https://github.com/supabase/pg-toolbelt/pull/187) (merged) | **Solved in pg-delta** |
| 019 | [Column-less CHECK NO INHERIT](019-columnless-check-no-inherit.md) | [#386](https://github.com/pgplex/pgschema/issues/386) | [#198](https://github.com/supabase/pg-toolbelt/issues/198) (closed) | [#212](https://github.com/supabase/pg-toolbelt/pull/212) (merged) | **Solved in pg-delta** |

Parity coverage trackers (still open on pg-toolbelt for tests / edge cases):

| Screening | pg-toolbelt issue | Notes |
|---|---|---|
| DEFERRABLE UNIQUE table constraint roundtrip | [#218](https://github.com/supabase/pg-toolbelt/issues/218) (open) | FK deferrable tests exist; UNIQUE deferrable still called out in issue body |
| Enum-arg function privilege SQL | [#219](https://github.com/supabase/pg-toolbelt/issues/219) (open) | |

## Active gaps after refresh

Unresolved **behavior** gap in this matrix:

- **005** — `ALTER COLUMN TYPE ... USING` / default-safe flow ([#130](https://github.com/supabase/pg-toolbelt/issues/130)): proposed fix PR [#146](https://github.com/supabase/pg-toolbelt/pull/146) did not merge; `AlterTableAlterColumnType` on upstream `main` still omits `USING` in its serializer.

Open **coverage** follow-ups (see table above): **#218**, **#219**.

## New open pgschema issue screening (draft-only output)

Screened candidates:

- **#362** numeric precision changes — **covered** in pg-delta integration tests
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered** in pg-delta integration tests
- **#404** deferrable unique constraints — **tracked** in pg-toolbelt issue [#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#366** function privilege signatures with enum argument types — **tracked** in pg-toolbelt issue [#219](https://github.com/supabase/pg-toolbelt/issues/219)

Draft details remain in:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)
