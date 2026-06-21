# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-06-21)

Refreshed against:

- `repos/pg-toolbelt` @ `c06f081208c067e9aab5a4f9b109cd2f5546bbc1`
- `repos/pgschema` @ `8b7a248ce08f155b43b31cdee9ea38751aff6d5d`

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

There is no benchmark-matrix parity delta versus the 2026-06-20 refresh:
benchmark 020 remains the only active resolved-issue gap.

No new upstream issue, PR, or submodule-head activity landed after the
2026-06-20 refresh. The June 20 screening conclusions therefore carry forward
unchanged:

- pgschema **#477** is already covered in pg-delta's current RLS policy path
- pgschema PR **#478** is already covered in pg-delta's current index
  storage-parameter path
- pgschema PR **#479** is only partially covered: trigger and sequence comments
  already roundtrip, but trigger enabled / disabled state still lacks an exact
  pg-delta tracker, so a draft-only issue body is saved in
  [`docs/parity-issue-drafts-2026-06-19.md`](../docs/parity-issue-drafts-2026-06-19.md)
- pgschema **#480** looks likely covered by current view / function dependency
  extraction and existing integration coverage, so no duplicate tracker was
  drafted in this refresh

There is still no upstream code-head delta in this refresh: the checked-in
submodules remain `pgschema@8b7a248ce08f155b43b31cdee9ea38751aff6d5d` and
`pg-delta@c06f081208c067e9aab5a4f9b109cd2f5546bbc1`, unchanged since
2026-06-20.

The focused unit-level revalidation from 2026-06-20 still reproduces benchmark 020: the
table-constraint diff probe returns zero planned changes when only the
definition changes from `UNIQUE (a, b)` to
`UNIQUE NULLS NOT DISTINCT (a, b)`. The same refresh also confirms the
draft-only #479 candidate: when a trigger's `enabled` state changes to
`DISABLED`, pg-delta currently serializes only `CREATE OR REPLACE TRIGGER ...`
with no `ALTER TABLE ... DISABLE TRIGGER ...` follow-up.

## Open pgschema issue screening (current state)

No new open pgschema issues were filed after the 2026-06-20 refresh; the
screened state below carries forward unchanged:

Screened candidates:

- **#362** numeric precision changes — **covered** in pg-delta integration tests
- **#401** `RETURNS SETOF <table>` dependency ordering — **covered** in pg-delta integration tests
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
  roundtrip path rather than pg-delta's catalog-diff workflow
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
- **#471** partitioned-table `ENABLE ROW LEVEL SECURITY` — **covered** in
  pg-delta's current table extraction / diff path; `table.model.ts` reads
  `relrowsecurity` for both regular and partitioned tables (`relkind in ('r',
  'p')`), `table.diff.ts` emits `ENABLE/DISABLE ROW LEVEL SECURITY`, and
  `rls-operations.test.ts` covers the generic RLS roundtrip path
- **#472** ignored child-trigger dumping with `.pgschemaignore` — **not parity
  work for pg-delta**; this is specific to pgschema's ignore-file handling and
  partition clone dumping
- **#473** partial-index predicate normalization (`IN (...)` vs
  `= ANY(ARRAY[...])`) — **not parity work for pg-delta**; pg-delta compares
  live catalog predicates via `pg_get_expr(i.indpred, i.indrelid)` rather than
  diffing rendered dump text
- **#477** restrictive RLS policies (`CREATE POLICY ... AS RESTRICTIVE`) —
  **covered** in current pg-delta; `rls-policy.model.ts` extracts
  `polpermissive`, `rls-policy.alter.test.ts` covers the drop + create path
  when permissive vs restrictive changes, and `rls-operations.test.ts` already
  roundtrips a `CREATE POLICY ... AS RESTRICTIVE ...` case
- **#480** dependency ordering on views and functions — **likely covered** in
  current pg-delta; `depend.ts` extracts both view rewrite relation / procedure
  edges, `table-function-dependency-ordering.test.ts` covers `RETURNS SETOF`
  table ordering, `function-operations.test.ts` covers function / view
  dependency ordering, and `view-operations.test.ts` covers drop / recreate
  ordering when a view's column set changes. No duplicate tracker was drafted
  in this refresh
- **#49** explicit rename / refactor workflow proposal — **not parity work for pg-delta**; this is a pgschema-specific workflow design, not a current pg-delta diff or planning gap

Historical draft text is recorded in markdown for both the older tracked
scenarios and the current draft-only uncovered candidates:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)
- [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- [`docs/parity-issue-drafts-2026-05-27.md`](../docs/parity-issue-drafts-2026-05-27.md)
- [`docs/parity-issue-drafts-2026-06-01.md`](../docs/parity-issue-drafts-2026-06-01.md)
- [`docs/parity-issue-drafts-2026-06-17.md`](../docs/parity-issue-drafts-2026-06-17.md)
- [`docs/parity-issue-drafts-2026-06-19.md`](../docs/parity-issue-drafts-2026-06-19.md)

## Recent closed-issue screening notes

- **#366** function privilege signatures with enum argument types — **closed
  upstream as `not_planned` and still tracked** by
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- **#404** deferrable unique constraints — **resolved upstream and still
  tracked** by
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
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
- **#439** constraint replacement with dependents — **resolved upstream and
  still not covered**; no exact pg-toolbelt issue / PR exists yet, and the
  saved draft remains in
  [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- **#444** drop-column ordering with dependent views — **resolved upstream and
  still not covered**; related pg-toolbelt work exists in
  [#263](https://github.com/supabase/pg-toolbelt/issues/263) (open),
  [#273](https://github.com/supabase/pg-toolbelt/pull/273) (merged),
  [#285](https://github.com/supabase/pg-toolbelt/pull/285) (open), and
  [#291](https://github.com/supabase/pg-toolbelt/pull/291) (open), but there is still
  no exact tracker. The saved draft remains in
  [`docs/parity-issue-drafts-2026-06-01.md`](../docs/parity-issue-drafts-2026-06-01.md)
- **#445** CHECK constraint qualifier drift for same-schema functions and types
  — **not parity work for pg-delta**; this is specific to pgschema's
  temp-schema normalization path, while pg-delta already exercises same-schema
  function and type references in `check-constraint-ordering.test.ts`
- **#446** explicit `UNIQUE` constraints on `PRIMARY KEY` columns — **covered**
  in pg-delta's current table-constraint path; `constraint_type` includes both
  `p` and `u`, and the diff path compares constraints directly instead of
  normalizing redundant `UNIQUE` constraints away

## Open upstream PR watch list

No new upstream PR activity landed after the 2026-06-20 refresh:

- pgschema [#475](https://github.com/pgplex/pgschema/pull/475) (`fix: order
  modified foreign keys after added unique constraints`) remains a
  **draft-only pg-delta parity candidate**. No exact pg-toolbelt issue / PR
  duplicate was found, so a candidate issue body remains saved in
  [`docs/parity-issue-drafts-2026-06-17.md`](../docs/parity-issue-drafts-2026-06-17.md)
- pgschema [#478](https://github.com/pgplex/pgschema/pull/478) (`feat: add
  support for index storage parameters (reloptions)`) is **covered** in current
  pg-delta; `index.model.ts` reads `reloptions`, `index.diff.ts` emits
  `ALTER INDEX ... SET/RESET (...)`, and `index.diff.test.ts` covers
  storage-parameter diffs. No duplicate tracker was drafted in this refresh
- pgschema [#479](https://github.com/pgplex/pgschema/pull/479) (`feat: add
  support for trigger comments, trigger enabled/disabled state, and sequence
  comments`) is **partially covered** in current pg-delta: trigger comments and
  sequence comments already have integration coverage, but trigger enabled /
  disabled state still lacks an exact pg-delta tracker. A draft-only issue body
  is saved in
  [`docs/parity-issue-drafts-2026-06-19.md`](../docs/parity-issue-drafts-2026-06-19.md)

During this refresh, newer pg-toolbelt issues
[#286](https://github.com/supabase/pg-toolbelt/issues/286) and
[#301](https://github.com/supabase/pg-toolbelt/issues/301) were also checked.
They are adjacent dependency/materialized-view work, but neither is an exact
duplicate of the current benchmark gap or draft-only parity candidates, so no
benchmark state changed.
