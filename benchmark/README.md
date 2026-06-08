# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-06-08)

Refreshed against:

- `repos/pg-toolbelt` @ `f95e0a8b773539dfb60ebf541131ab9feba4a525`
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

There is no resolved-issue or open-issue parity-state delta versus the
2026-06-07 refresh: benchmark 020 remains the only active resolved-issue gap,
pg-toolbelt issues #218 and #219 remain the only active open parity trackers,
draft-only candidates #439 and #444 remain unduplicated, pgschema #449 / #450
remain classified as not parity work for pg-delta, and upstream pgschema PR
[#451](https://github.com/pgplex/pgschema/pull/451) is only a watch item for
already-screened quoted-name cases rather than a new pg-delta tracker.

There is also no upstream code delta versus the 2026-06-07 refresh: pg-delta
remains at `f95e0a8b773539dfb60ebf541131ab9feba4a525` and pgschema remains at
`592c19c95b06830255b45bc4d80eeacd62e7e727`. This refresh instead reconciles
the repo metadata with that snapshot: `benchmark/review-memory.json` is brought
forward to the current pg-delta fingerprint, and a focused unit-level diff
probe still produces zero planned changes when only the table-constraint
definition changes from `UNIQUE (a, b)` to
`UNIQUE NULLS NOT DISTINCT (a, b)`.

## Open pgschema issue screening (current state)

Screened candidates:

- **#362** numeric precision changes — **covered** in pg-delta integration tests
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered** in pg-delta integration tests
- **#404** deferrable unique constraints — **tracked** by [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- **#366** function privilege signatures with enum argument types — **tracked** by [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#414** views created after `ADD COLUMN` changes — **covered** in pg-delta's
  current sort path; pgschema fix PR [#417](https://github.com/pgplex/pgschema/pull/417)
  remains open, while pg-delta already roundtrips `ADD COLUMN` plus view
  creation in `mixed-objects.test.ts` and keeps table changes ahead of view
  creation during sorting
- **#415** materialized-view refactors — **covered** in pg-delta's dedicated
  materialized-view replacement path; `materialized-view-operations.test.ts`
  exercises replace flows and `materialized-view.drop.ts` emits
  `DROP MATERIALIZED VIEW`
- **#416** custom aggregates missing from dump output — **covered** in
  pg-delta's aggregate model, export mapping, and
  `aggregate-operations.test.ts`
- **#427** schema-qualified functions in RLS policy expressions — **covered**
  in current pg-delta; pgschema fix PR [#428](https://github.com/pgplex/pgschema/pull/428)
  remains open, while `rls-operations.test.ts` roundtrips a policy that calls a
  schema-qualified function, `policy-dependencies.test.ts` covers the related
  policy/function ordering path, and policy extraction preserves expressions via
  `pg_get_expr(...)`
- **#436** required extensions in dump output — **covered** in pg-delta's extension model and integration coverage (`src/core/objects/extension/`, `tests/integration/extension-operations.test.ts`)
- **#418** `CREATE INDEX CONCURRENTLY` on partitioned parents — **not parity
  work for pg-delta**; this is specific to pgschema's online-DDL rewrite and
  pg-delta does not synthesize `CONCURRENTLY`
- **#419** `.pgschemaignore` behavior differs by GitHub Actions install path —
  **not parity work for pg-delta**; this is packaging and install-surface
  behavior in pgschema rather than a catalog diff gap
- **#420** `varchar(n)[]` typmod preservation — **covered** in pg-delta's
  current source path; pgschema fix PR [#438](https://github.com/pgplex/pgschema/pull/438)
  is now merged, and pg-delta already preserves the typmod because column
  extraction uses `format_type(a.atttypid, a.atttypmod)`, type diffs key off
  `data_type_str`, and table create / alter SQL serialize `data_type_str`
  verbatim
- **#421 / #422** quoted-name dump edge cases — **not parity work for
  pg-delta**; these are tied to pgschema's dump -> temp-schema -> plan
  roundtrip path rather than pg-delta's catalog-diff workflow. Open upstream PR
  [#451](https://github.com/pgplex/pgschema/pull/451) overlaps the mixed-case
  trigger / FK quoting surface, but it does not change pg-delta's parity
  verdict
- **#439** replacing `UNIQUE` with `PRIMARY KEY` when dependents still point at the old constraint — **not covered**; draft issue text saved in [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- **#444** drop-column ordering with dependent views — **not covered**; pg-delta
  has analogous `ADD COLUMN` + view replacement coverage plus adjacent
  dependency-ordering work in [pg-toolbelt#263](https://github.com/supabase/pg-toolbelt/issues/263)
  plus open PR [#273](https://github.com/supabase/pg-toolbelt/pull/273) and
  open PR [#275](https://github.com/supabase/pg-toolbelt/pull/275), but there
  is still no exact `DROP COLUMN` + dependent-view regression or dedicated
  tracker. Draft issue text is saved in
  [`docs/parity-issue-drafts-2026-06-01.md`](../docs/parity-issue-drafts-2026-06-01.md)
- **#407 / #409 / #429** `.pgschemaignore` follow-ups — **not parity work for pg-delta** (pgschema-specific ignore-file surface area)
- **#447** `.pgschemaignore` constraints support — **not parity work for
  pg-delta**; this is another ignore-file feature request specific to
  pgschema's dump / plan surface area
- **#449** repeat drift for same-schema policy / CHECK expressions after apply
  — **not parity work for pg-delta**; this is a declarative-SQL vs live-catalog
  normalization issue in pgschema, while pg-delta compares policy expressions
  and CHECK definitions extracted from live catalogs on both sides
- **#450** missing role blocks plan/apply — **not parity work for pg-delta**;
  this is specific to pgschema applying dumped SQL into a temporary planning
  schema, while pg-delta diffs live catalogs directly and already models roles
  plus privilege dependencies
- **#49** explicit rename / refactor workflow proposal — **not parity work for pg-delta**; this is a pgschema-specific workflow design, not a current pg-delta diff or planning gap

Historical draft text is recorded in markdown for both the older tracked
scenarios and the newly screened uncovered candidates:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)
- [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- [`docs/parity-issue-drafts-2026-05-27.md`](../docs/parity-issue-drafts-2026-05-27.md)
- [`docs/parity-issue-drafts-2026-06-01.md`](../docs/parity-issue-drafts-2026-06-01.md)

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
- **#446** explicit `UNIQUE` constraints on `PRIMARY KEY` columns — **covered**
  in pg-delta's current table-constraint path; `constraint_type` includes both
  `p` and `u`, and the diff path compares constraints directly instead of
  normalizing redundant `UNIQUE` constraints away
