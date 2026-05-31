# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-05-31)

Refreshed against:

- `repos/pg-toolbelt` @ `ee9385daf75f72d443882020247ffd2599050090`
- `repos/pgschema` @ `592c19c95b06830255b45bc4d80eeacd62e7e727`

## Benchmark status matrix

| # | File | pgschema | pg-toolbelt issue | pg-toolbelt PR | Current status |
|---|---|---|---|---|---|
| 005 | [ALTER column type USING](005-alter-column-type-using-clause.md) | [#190](https://github.com/pgplex/pgschema/issues/190) | [#130](https://github.com/supabase/pg-toolbelt/issues/130) (closed) | [#146](https://github.com/supabase/pg-toolbelt/pull/146) (closed), replacement [#231](https://github.com/supabase/pg-toolbelt/pull/231) (merged) | **Solved in pg-delta** |
| 007 | [Function signature DROP](007-function-signature-change-requires-drop.md) | [#326](https://github.com/pgplex/pgschema/issues/326) | [#132](https://github.com/supabase/pg-toolbelt/issues/132) (closed) | [#214](https://github.com/supabase/pg-toolbelt/pull/214) (merged) | **Solved in pg-delta** |
| 008 | [Mat view cascade deps](008-materialized-view-cascade-dependencies.md) | [#268](https://github.com/pgplex/pgschema/issues/268) | [#133](https://github.com/supabase/pg-toolbelt/issues/133) (closed) | [#149](https://github.com/supabase/pg-toolbelt/pull/149) (merged) | **Solved in pg-delta** |
| 013 | [Sequence identity](013-sequence-identity-transitions.md) | [#279](https://github.com/pgplex/pgschema/issues/279) | [#138](https://github.com/supabase/pg-toolbelt/issues/138) (closed) | [#154](https://github.com/supabase/pg-toolbelt/pull/154) (merged) | **Solved in pg-delta** |
| 015 | [Trigger UPDATE OF columns](015-trigger-update-of-columns.md) | [#342](https://github.com/pgplex/pgschema/issues/342) | [#140](https://github.com/supabase/pg-toolbelt/issues/140) (closed) | [#200](https://github.com/supabase/pg-toolbelt/pull/200) (merged) | **Solved in pg-delta** |
| 016 | [Unique index NULLS NOT DISTINCT](016-unique-index-nulls-not-distinct.md) | [#355](https://github.com/pgplex/pgschema/issues/355) | [#183](https://github.com/supabase/pg-toolbelt/issues/183) (closed) | [#185](https://github.com/supabase/pg-toolbelt/pull/185) (merged) | **Solved in pg-delta** |
| 017 | [Temporal WITHOUT OVERLAPS / PERIOD constraints](017-temporal-without-overlaps-period-constraints.md) | [#364](https://github.com/pgplex/pgschema/issues/364) | [#182](https://github.com/supabase/pg-toolbelt/issues/182) (closed) | [#213](https://github.com/supabase/pg-toolbelt/pull/213) (merged) | **Solved in pg-delta** |
| 018 | [Cross-table RLS policy ordering](018-cross-table-rls-policy-ordering.md) | [#373](https://github.com/pgplex/pgschema/issues/373) | [#184](https://github.com/supabase/pg-toolbelt/issues/184) (closed) | [#187](https://github.com/supabase/pg-toolbelt/pull/187) (merged) | **Solved in pg-delta** |
| 019 | [Column-less CHECK NO INHERIT](019-columnless-check-no-inherit.md) | [#386](https://github.com/pgplex/pgschema/issues/386) | [#198](https://github.com/supabase/pg-toolbelt/issues/198) (closed) | [#212](https://github.com/supabase/pg-toolbelt/pull/212) (merged) | **Solved in pg-delta** |
| 020 | [UNIQUE constraint NULLS NOT DISTINCT](020-unique-constraint-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | none found | none found | **Not covered** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Only this resolved-issue benchmark scenario remains active as unresolved:

- **020** — `UNIQUE NULLS NOT DISTINCT` on table constraints

There is no resolved-issue parity-state delta versus the 2026-05-29 refresh:
benchmark 020 remains the only active resolved-issue gap.

## New open pgschema issue screening (draft-only output)

Screened candidates:

- **#362** numeric precision changes — **covered** in pg-delta integration tests
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered** in pg-delta integration tests
- **#404** deferrable unique constraints — **tracked** by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#366** function privilege signatures with enum argument types — **tracked** by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#414** views created after `ADD COLUMN` changes — **covered** in pg-delta's
  current sort path; `mixed-objects.test.ts` roundtrips `ADD COLUMN` plus view
  creation, and logical sorting keeps table changes ahead of view creation
- **#415** materialized-view refactors — **covered** in pg-delta's dedicated
  materialized-view replacement path; `materialized-view-operations.test.ts`
  exercises replace flows and `materialized-view.drop.ts` emits
  `DROP MATERIALIZED VIEW`
- **#416** custom aggregates missing from dump output — **covered** in
  pg-delta's aggregate model, export mapping, and
  `aggregate-operations.test.ts`
- **#436** required extensions in dump output — **covered** in pg-delta's extension model and integration coverage (`src/core/objects/extension/`, `tests/integration/extension-operations.test.ts`)
- **#444** drop-column ordering with dependent views — **covered** by pg-delta's existing view replacement path; `tests/integration/view-operations.test.ts` asserts `DROP VIEW` happens before the table change when projected columns change, matching the same dependency class fixed by [pg-toolbelt#139](https://github.com/supabase/pg-toolbelt/issues/139) / [#155](https://github.com/supabase/pg-toolbelt/pull/155)
- **#418** `CREATE INDEX CONCURRENTLY` on partitioned parents — **not parity
  work for pg-delta**; this is specific to pgschema's online-DDL rewrite and
  pg-delta does not synthesize `CONCURRENTLY`
- **#419** `.pgschemaignore` behavior differs by GitHub Actions install path —
  **not parity work for pg-delta**; this is packaging and install-surface
  behavior in pgschema rather than a catalog diff gap
- **#420** `varchar(n)[]` typmod preservation — **not covered**; upstream
  pgschema has now merged fix PR
  [#438](https://github.com/pgplex/pgschema/pull/438), but the issue remains
  open, there is still no matching pg-toolbelt issue or PR, and draft issue
  text is saved in
  [`docs/parity-issue-drafts-2026-05-27.md`](../docs/parity-issue-drafts-2026-05-27.md)
- **#421 / #422** quoted-name dump edge cases — **not parity work for
  pg-delta**; these are tied to pgschema's dump -> temp-schema -> plan
  roundtrip path rather than pg-delta's catalog-diff workflow
- **#427** schema-qualified functions in RLS policy expressions — **not covered**;
  pgschema now has open fix PR [#428](https://github.com/pgplex/pgschema/pull/428),
  while pg-delta still has no matching issue or PR. Draft issue text remains in
  [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- **#439** replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old constraint — **not covered**; draft issue text saved in [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- **#407 / #409 / #429** `.pgschemaignore` follow-ups — **not parity work for pg-delta** (pgschema-specific ignore-file surface area)
- **#49** explicit rename / refactor workflow proposal — **not parity work for pg-delta**; this is a pgschema-specific workflow design, not a current pg-delta diff or planning gap

Historical draft text is recorded in markdown for both the older tracked
scenarios and the newly screened uncovered candidates:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)
- [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- [`docs/parity-issue-drafts-2026-05-27.md`](../docs/parity-issue-drafts-2026-05-27.md)

## Recent closed-issue screening notes

- **#406** indexes in `.pgschemaignore` — **not parity work for pg-delta**;
  this is pgschema-specific ignore-file surface area rather than a catalog diff
  gap
- **#408** quoted custom / reserved type names in plan output — **covered** in
  the current pg-delta source path; column types come from `format_type(...)`
  and quoted custom types are exercised in `type-operations.test.ts`
- **#410** `name` typed columns rendered as `char[]` — **covered** in
  pg-delta's type extraction path via `format_type(...)`
- **#412** `UNIQUE NULLS NOT DISTINCT` on table constraints — **not covered** in
  the current pg-delta constraint path; benchmarked as [020](020-unique-constraint-nulls-not-distinct.md)
- **#423** `UNLOGGED` tables — **covered** in pg-delta's table persistence
  extraction and diff logic (`relpersistence`, `SET UNLOGGED`, `SET LOGGED`)
- **#426** Docker Hub image lag versus GitHub releases — **not parity work for
  pg-delta**; this is release packaging only
- **#445** CHECK constraint qualifier drift for same-schema functions and types
  — **not parity work for pg-delta**; this is specific to pgschema's
  temp-schema normalization path, while pg-delta already exercises same-schema
  function and type references in `check-constraint-ordering.test.ts`
- **#446** explicit `UNIQUE` constraints on `PRIMARY KEY` columns — **not
  parity work for pg-delta**; pgschema drops them during desired-state
  normalization, while pg-delta extracts table constraints directly from
  `pg_constraint` without collapsing `UNIQUE` under `PRIMARY KEY`
