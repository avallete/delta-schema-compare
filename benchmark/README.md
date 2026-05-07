# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-05-07)

Refreshed against:

- `repos/pg-toolbelt` @ `102ef99ae5aabb29510d48b39fbb8ecee34f5458`
- `repos/pgschema` @ `e4f3a123d5ef8987e48379c4a2027b2de4c73a09`

Full refresh report:
[`docs/parity-refresh-2026-05-07.md`](../docs/parity-refresh-2026-05-07.md)

## Benchmark status matrix

| # | File | pgschema | pg-toolbelt issue | pg-toolbelt PR | Current status |
|---|---|---|---|---|---|
| 005 | [ALTER column type USING](005-alter-column-type-using-clause.md) | [#190](https://github.com/pgplex/pgschema/issues/190) | [#130](https://github.com/supabase/pg-toolbelt/issues/130) (closed) | [#146](https://github.com/supabase/pg-toolbelt/pull/146) (closed, not merged) | **Solved in pg-delta** |
| 007 | [Function signature DROP](007-function-signature-change-requires-drop.md) | [#326](https://github.com/pgplex/pgschema/issues/326) | [#132](https://github.com/supabase/pg-toolbelt/issues/132) (closed) | [#214](https://github.com/supabase/pg-toolbelt/pull/214) (merged) | **Solved in pg-delta** |
| 008 | [Mat view cascade deps](008-materialized-view-cascade-dependencies.md) | [#268](https://github.com/pgplex/pgschema/issues/268) | [#133](https://github.com/supabase/pg-toolbelt/issues/133) (closed) | [#149](https://github.com/supabase/pg-toolbelt/pull/149) (merged) | **Solved in pg-delta** |
| 013 | [Sequence identity](013-sequence-identity-transitions.md) | [#279](https://github.com/pgplex/pgschema/issues/279) | [#138](https://github.com/supabase/pg-toolbelt/issues/138) (closed) | [#154](https://github.com/supabase/pg-toolbelt/pull/154) (merged) | **Solved in pg-delta** |
| 015 | [Trigger UPDATE OF columns](015-trigger-update-of-columns.md) | [#342](https://github.com/pgplex/pgschema/issues/342) | [#140](https://github.com/supabase/pg-toolbelt/issues/140) (closed) | [#200](https://github.com/supabase/pg-toolbelt/pull/200) (merged) | **Solved in pg-delta** |
| 016 | [Unique index NULLS NOT DISTINCT](016-unique-index-nulls-not-distinct.md) | [#355](https://github.com/pgplex/pgschema/issues/355) | [#183](https://github.com/supabase/pg-toolbelt/issues/183) (closed) | [#185](https://github.com/supabase/pg-toolbelt/pull/185) (merged) | **Solved in pg-delta** |
| 017 | [Temporal WITHOUT OVERLAPS / PERIOD constraints](017-temporal-without-overlaps-period-constraints.md) | [#364](https://github.com/pgplex/pgschema/issues/364) | [#182](https://github.com/supabase/pg-toolbelt/issues/182) (closed) | [#213](https://github.com/supabase/pg-toolbelt/pull/213) (merged) | **Solved in pg-delta** |
| 018 | [Cross-table RLS policy ordering](018-cross-table-rls-policy-ordering.md) | [#373](https://github.com/pgplex/pgschema/issues/373) | [#184](https://github.com/supabase/pg-toolbelt/issues/184) (closed) | [#187](https://github.com/supabase/pg-toolbelt/pull/187) (merged) | **Solved in pg-delta** |
| 019 | [Column-less CHECK NO INHERIT](019-columnless-check-no-inherit.md) | [#386](https://github.com/pgplex/pgschema/issues/386) | [#198](https://github.com/supabase/pg-toolbelt/issues/198) (closed) | [#212](https://github.com/supabase/pg-toolbelt/pull/212) (merged) | **Solved in pg-delta** |
| 020 | [Table constraint UNIQUE NULLS NOT DISTINCT](020-table-constraint-unique-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | — | — | **Not covered (draft issue prepared)** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.
>
> Note: this matrix follows current pg-delta mainline behavior, not only the
> original PR linkage. For example, row 005 is now treated as solved because the
> `USING`/default-safe alter-column flow is present on current `main`, even
> though the original PR [#146](https://github.com/supabase/pg-toolbelt/pull/146)
> closed without merging.

## Active gaps after refresh

Only this historical benchmark scenario remains unresolved:

- **020** — table-level `UNIQUE NULLS NOT DISTINCT` constraints

A draft pg-toolbelt issue body for the remaining gap is recorded in
[`docs/parity-issue-drafts-2026-05-07.md`](../docs/parity-issue-drafts-2026-05-07.md).

## New open pgschema issue screening (draft-only output)

Screened candidates:

- **#362** numeric precision changes — **covered** in pg-delta integration tests
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered** in pg-delta integration tests
- **#404** deferrable unique constraints — **tracked** by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#366** function privilege signatures with enum argument types — **tracked** by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#408** quoted custom / reserved type names in plan output — **no duplicate pg-toolbelt issue drafted**; pg-delta already preserves `data_type_str` from `format_type(...)` and has quoted-type coverage in `type-operations.test.ts`
- **#414** `CREATE VIEW` after `ALTER TABLE ... ADD COLUMN` — upstream fix [pgschema#417](https://github.com/pgplex/pgschema/pull/417) is still open, so this remains a watch item rather than a new pg-toolbelt draft in this refresh
- **#427** schema-qualified functions in RLS policy expressions — **no duplicate pg-toolbelt issue drafted**; pg-delta already preserves `auth.uid()` / `auth.role()` in RLS policy extraction and SQL formatting, and the Supabase dbdev roundtrip covers auth-backed policies
- **#406 / #407 / #409 / #419** `.pgschemaignore` / workflow follow-ups — **not parity work for pg-delta** (pgschema-specific ignore-file surface area)

Historical draft text is still recorded in markdown for tracked and draft-only
parity issues:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)
- [`docs/parity-issue-drafts-2026-05-07.md`](../docs/parity-issue-drafts-2026-05-07.md)

## Recent closed-issue screening notes

- **#410** `name`-typed columns dumped as `char[]` — **covered**; pg-delta
  column extraction already relies on `format_type(a.atttypid, a.atttypmod)`
- **#412** table-level `UNIQUE NULLS NOT DISTINCT` constraints — **not
  covered**; added as benchmark item 020 with a draft pg-toolbelt issue body
- **#423** `UNLOGGED` tables — **covered** by pg-delta table persistence
  support (`CREATE UNLOGGED TABLE`, `ALTER TABLE ... SET UNLOGGED`, and
  `ALTER TABLE ... SET LOGGED`)

## Notes

- Manual unlabeled-issue sweeps are still required for this repo because recent
  pgschema issues often ship without `Bug` / `Feature` labels. The automation
  scripts can therefore return zero issues even when a manual parity review
  finds meaningful changes.
