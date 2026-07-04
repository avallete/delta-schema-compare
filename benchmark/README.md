# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-07-04)

Refreshed against:

- `repos/pg-toolbelt` @ `9284412d71635308ebb0c1537e0b0183d2cfa4da`
- `repos/pgschema` @ `7011b0a78cdd292ec24b9ddb775dc1c6ec84abe2`

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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | none found | none found | **Not covered** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Two resolved-issue benchmark scenarios remain active as unresolved:

- **020** — `UNIQUE NULLS NOT DISTINCT` on table constraints
- **021** — child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`

There **is** a benchmark-matrix parity delta versus the 2026-07-03 refresh:
benchmark 021 is newly promoted from the prior draft-only open finding after
pgschema issue #499 closed in merged
[pgschema#500](https://github.com/pgplex/pgschema/pull/500).

There is a pgschema code-head delta in this refresh:
`pgschema` advanced to `7011b0a78cdd292ec24b9ddb775dc1c6ec84abe2` via merged
[pgschema#498](https://github.com/pgplex/pgschema/pull/498) and
[pgschema#500](https://github.com/pgplex/pgschema/pull/500), while
`pg-delta` remains at `9284412d71635308ebb0c1537e0b0183d2cfa4da`.

A targeted GitHub sweep for updates after `2026-07-03T07:17:17Z` found four
new or newly-closed pgschema updates relevant to the current parity view:

- **#496** detached standalone partition children on create — **covered** in
  current pg-delta. The upstream issue is now closed by merged
  [pgschema#498](https://github.com/pgplex/pgschema/pull/498), and a focused
  local `CreateTable` probe still emits
  `CREATE TABLE ... PARTITION OF ... FOR VALUES ...`
- **#499** child-specific column elements on `PARTITION OF` create —
  **not covered** in current pg-delta. The upstream issue is now closed by
  merged [pgschema#500](https://github.com/pgplex/pgschema/pull/500), so this
  scenario is now benchmarked as [021](021-partition-child-column-overrides.md)
- **#501** PostgreSQL 18 `VIRTUAL` generated columns — **not covered** in
  current pg-delta. The table model collapses `attgenerated` to a boolean and
  current serialization hard-codes generated columns as `... STORED`, so a
  draft-only tracker note is now saved in
  [`docs/parity-issue-drafts-2026-07-04.md`](../docs/parity-issue-drafts-2026-07-04.md)
- **#502** `COMMENT ON COLUMN` misresolution when table name equals schema name
  — **not parity work for pg-delta**; this is specific to pgschema's
  desired-state SQL rewrite path rather than pg-delta's live-catalog diff
  model

No new exact pg-toolbelt issue or PR activity was found for benchmark 020,
benchmark 021, pgschema #366, #404, #439, #444, or the trigger enabled-state
slice from pgschema PR #479. Open
[pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285) remains
the exact in-flight tracker for trigger enabled / disabled state, while the new
partitioning and generated-column findings do not introduce a duplicate
tracker.

Benchmark 020 still reproduces as a zero-change table-constraint diff, and the
focused partition-child probe still emits a bare `PARTITION OF ... FOR VALUES`
statement with no child-specific column overrides. Those two executed checks
leave benchmarks 020 and 021 as the active benchmarked gaps after this refresh.

## Open pgschema issue screening (current state)

This pass removes the now-closed partitioning issues #496 / #499 from open
screening and adds the new open issues #501 / #502. The current still-open
reviewed issue set is:

Screened candidates:

- **#49** explicit rename / refactor workflow proposal — **not parity work for
  pg-delta**; this is a pgschema-specific workflow design, not a current
  pg-delta diff or planning gap
- **#52** explicit before / after SQL file execution in plan output — **not
  parity work for pg-delta**; this is a pgschema-specific escape-hatch /
  workflow request rather than a live-catalog diff gap
- **#84** feedback / testimonial collection thread — **not parity work for
  pg-delta**; this is community outreach rather than schema-diff behavior
- **#450** missing role blocks plan/apply — **not parity work for pg-delta**;
  this is specific to pgschema applying dumped SQL into a temporary planning
  schema, while pg-delta diffs live catalogs directly and already models roles
  plus privilege dependencies
- **#493** inspector / IR should preserve schema identity for type references
  under `--qualify-schema` — **not parity work for pg-delta**; this is a
  follow-up on pgschema's dump-only schema-qualification flag rather than a
  live-catalog diff or migration-planning gap
- **#501** PostgreSQL 18 `VIRTUAL` generated columns — **not covered** in
  current pg-delta; `table.model.ts` collapses `attgenerated` to
  `is_generated: boolean`, `table.create.ts` / `table.alter.ts` serialize
  generated columns as `... STORED`, and no integration regression currently
  covers `VIRTUAL`. No exact pg-toolbelt issue or PR exists yet, and the saved
  draft now lives in
  [`docs/parity-issue-drafts-2026-07-04.md`](../docs/parity-issue-drafts-2026-07-04.md)
- **#502** `COMMENT ON COLUMN` misresolved when table name equals schema name —
  **not parity work for pg-delta**; pg-delta extracts column comments directly
  from the live catalog and serializes fully qualified comment DDL instead of
  replaying desired-state SQL through a rewrite step

Historical draft text is recorded in markdown for both the older tracked
scenarios and the current draft-only uncovered candidates:

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)
- [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- [`docs/parity-issue-drafts-2026-05-27.md`](../docs/parity-issue-drafts-2026-05-27.md)
- [`docs/parity-issue-drafts-2026-06-01.md`](../docs/parity-issue-drafts-2026-06-01.md)
- [`docs/parity-issue-drafts-2026-06-17.md`](../docs/parity-issue-drafts-2026-06-17.md)
- [`docs/parity-issue-drafts-2026-06-19.md`](../docs/parity-issue-drafts-2026-06-19.md)
- [`docs/parity-issue-drafts-2026-07-03.md`](../docs/parity-issue-drafts-2026-07-03.md)
- [`docs/parity-issue-drafts-2026-07-04.md`](../docs/parity-issue-drafts-2026-07-04.md)

## Recent closed-issue screening notes

Additional issues that were still carried under open screening in the previous
snapshot are now closed upstream and keep the same pg-delta parity verdicts:

- **#495** partition-child PK / UNIQUE local-vs-inherited convergence —
  **covered** in current pg-delta; `table.model.ts` uses `coninhcount > 0` to
  detect partition clones and `table.diff.ts` skips clone/local churn when the
  constraint name and definition already match
- **#496** detached standalone partition children on create — **covered** in
  current pg-delta; `table.model.ts` extracts `parent_schema` /
  `partition_bound`, `table.create.ts` emits `CREATE TABLE ... PARTITION OF ...`,
  and merged [pgschema#498](https://github.com/pgplex/pgschema/pull/498) closes
  the upstream parity gap
- **#499** child-specific column elements on `PARTITION OF` create —
  **not covered** in current pg-delta; merged
  [pgschema#500](https://github.com/pgplex/pgschema/pull/500) closes the
  upstream issue, and the remaining pg-delta gap is now benchmarked as
  [021](021-partition-child-column-overrides.md)
- **#362**, **#401**, **#414**, **#415**, **#416**, **#420**, **#427**, and
  **#436** — **covered** in current pg-delta
- **#407**, **#409**, **#418**, **#419**, **#421**, **#422**, **#429**,
  **#447**, and **#449** — **not parity work for pg-delta**; these are
  ignore-file, packaging, or pgschema-specific normalization behaviors rather
  than live-catalog diff gaps

- **#366** function privilege signatures with enum argument types — **closed
  upstream as `not_planned` and still tracked** by
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- new adjacent pg-toolbelt work now exists in
  [#308](https://github.com/supabase/pg-toolbelt/issues/308) and
  [#310](https://github.com/supabase/pg-toolbelt/pull/310), but it covers
  `REVOKE EXECUTE ... FROM PUBLIC` on functions rather than the enum-typed
  signature drift from pgschema #366, so the parity label remains `tracked`
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
- **#321** `dump --qualify-schema` — **not parity work for pg-delta**; this is
  a pgschema dump-format / CLI feature rather than a live-catalog diff gap.
  The new open follow-up #493 keeps the same non-parity classification
- **#439** constraint replacement with dependents — **resolved upstream and
  still not covered**; no exact pg-toolbelt issue / PR exists yet, and the
  saved draft remains in
  [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- **#444** drop-column ordering with dependent views — **resolved upstream and
  still not covered**; related pg-toolbelt work exists in
  [#263](https://github.com/supabase/pg-toolbelt/issues/263) (open),
  [#273](https://github.com/supabase/pg-toolbelt/pull/273) (merged),
  [#285](https://github.com/supabase/pg-toolbelt/pull/285) (open), and
  [#291](https://github.com/supabase/pg-toolbelt/pull/291) (open), but the
  current pg-delta suite still has no exact `DROP COLUMN` / dependent-view
  regression and there is still no exact tracker. The saved draft remains in
  [`docs/parity-issue-drafts-2026-06-01.md`](../docs/parity-issue-drafts-2026-06-01.md)
- **#445** CHECK constraint qualifier drift for same-schema functions and types
  — **not parity work for pg-delta**; this is specific to pgschema's
  temp-schema normalization path, while pg-delta already exercises same-schema
  function and type references in `check-constraint-ordering.test.ts`
- **#446** explicit `UNIQUE` constraints on `PRIMARY KEY` columns — **covered**
  in pg-delta's current table-constraint path; `constraint_type` includes both
  `p` and `u`, and the diff path compares constraints directly instead of
  normalizing redundant `UNIQUE` constraints away
- **#471** partitioned-table `ENABLE ROW LEVEL SECURITY` — **covered** in
  current pg-delta and now **closed upstream**. The current table extraction /
  diff path already handles `relrowsecurity` for partitioned tables, and the
  reviewed item has been moved from `review-memory.open` to `review-memory.resolved`
- **#473** partial-index predicate normalization (`IN (...)` vs
  `= ANY(ARRAY[...])`) — **not parity work for pg-delta** and now **closed
  upstream**; pg-delta compares live catalog predicates via
  `pg_get_expr(i.indpred, i.indrelid)` rather than diffing rendered dump text
- **#472** ignored child-trigger dumping with `.pgschemaignore` — **not parity
  work for pg-delta**; this is specific to pgschema's ignore-file handling and
  partition clone dumping
- **#477** restrictive RLS policies (`CREATE POLICY ... AS RESTRICTIVE`) —
  **covered** in current pg-delta; `rls-policy.model.ts` extracts
  `polpermissive`, `rls-policy.alter.test.ts` covers the drop + create path
  when permissive vs restrictive changes, and `rls-operations.test.ts` already
  roundtrips a `CREATE POLICY ... AS RESTRICTIVE ...` case
- **#480** dependency ordering on views and functions — **covered** in current
  pg-delta. A focused 2026-06-23 plan probe for the exact
  `RETURNS vw_users` composite-rowtype case produced the convergent order:
  `DROP FUNCTION`, `DROP VIEW`, `ALTER TABLE`, `CREATE VIEW`, then
  `CREATE FUNCTION`, so no duplicate tracker is needed
- **#481** trigger `WHEN` enum-cast repeat-plan drift — **not parity work for
  pg-delta**; this is specific to pgschema's dump-time trigger deparse path,
  while pg-delta already diffs live catalog trigger definitions and
  `when_condition` text

## Open upstream PR watch list

Recent parity-relevant pgschema PR activity is now:

- pgschema [#497](https://github.com/pgplex/pgschema/pull/497) (`fix:
  partition child PK/UNIQUE constraints cause perpetual plan drift`) is now
  **covered** in current pg-delta. A focused local diff probe returned `0`
  planned changes between a child-local `UNIQUE` constraint and the inherited
  partition-clone form, matching the current `coninhcount`-based clone
  handling in `table.model.ts` and `table.diff.ts`
- pgschema [#498](https://github.com/pgplex/pgschema/pull/498) (`fix: emit
  PARTITION OF for partition children on create path`) is now **merged**, and
  the corresponding detached-partition create path remains **covered** in
  current pg-delta
- pgschema [#500](https://github.com/pgplex/pgschema/pull/500) (`fix: emit
  per-child column overrides in PARTITION OF`) is now **merged**, but the exact
  child-specific `DEFAULT` / `NOT NULL` override path is still **not covered**
  in current pg-delta and is now benchmarked as
  [021](021-partition-child-column-overrides.md)
- pgschema [#475](https://github.com/pgplex/pgschema/pull/475) (`fix: order
  modified foreign keys after added unique constraints`) now looks **covered**
  in current pg-delta. A focused 2026-06-23 plan probe for the saved draft SQL
  produced `DROP child FK` -> `ADD parent UNIQUE` -> `ADD child FK`, so the
  older draft in
  [`docs/parity-issue-drafts-2026-06-17.md`](../docs/parity-issue-drafts-2026-06-17.md)
  is retained as historical review context only
- pgschema [#478](https://github.com/pgplex/pgschema/pull/478) (`feat: add
  support for index storage parameters (reloptions)`) is **covered** in current
  pg-delta; `index.model.ts` reads `reloptions`, `index.diff.ts` emits
  `ALTER INDEX ... SET/RESET (...)`, and `index.diff.test.ts` covers
  storage-parameter diffs. No duplicate tracker was drafted in this refresh
- pgschema [#479](https://github.com/pgplex/pgschema/pull/479) (`feat: add
  support for trigger comments, trigger enabled/disabled state, and sequence
  comments`) is **partially covered** in current pg-delta: trigger comments and
  sequence comments already have integration coverage, and the remaining
  trigger enabled / disabled state slice is now **tracked in-flight** by open
  [pg-toolbelt#285](https://github.com/supabase/pg-toolbelt/pull/285). That PR
  includes explicit trigger-state regressions plus
  `ALTER TABLE ... DISABLE TRIGGER ...` implementation work, so the older draft
  in
  [`docs/parity-issue-drafts-2026-06-19.md`](../docs/parity-issue-drafts-2026-06-19.md)
  is retained as historical review context only

The checked-in pg-delta head in this refresh
(`9284412d71635308ebb0c1537e0b0183d2cfa4da`) already includes the trigger
quoted-name formatter coverage and matching integration regression checked in
the 2026-06-26 pass, but it still does not include the unmerged trigger
enabled-state work from pg-toolbelt PR #285. Benchmarks 020 and 021 therefore
remain the active resolved-issue benchmark gaps, while the remaining
trigger-state slice from pgschema PR #479 is now tracked by an exact in-flight
pg-toolbelt PR rather than an untracked draft-only gap.

Existing pg-toolbelt PR activity was also rechecked during this refresh:

- [#301](https://github.com/supabase/pg-toolbelt/issues/301) /
  [#305](https://github.com/supabase/pg-toolbelt/pull/305) now cover
  materialized-view definition stability under differing `search_path` values.
  This is adjacent to historical materialized-view parity work, but it is not
  an exact duplicate of benchmark 008, benchmark 020, or the current draft-only
  candidates
- [#304](https://github.com/supabase/pg-toolbelt/issues/304),
  [#313](https://github.com/supabase/pg-toolbelt/pull/313), and
  [#316](https://github.com/supabase/pg-toolbelt/pull/316) cover leading enum
  value insert ordering. No matching pgschema benchmark or screened issue
  currently maps to this exact scenario
- [#311](https://github.com/supabase/pg-toolbelt/issues/311) /
  [#314](https://github.com/supabase/pg-toolbelt/pull/314) cover mutual inline
  foreign-key cycles in declarative apply. This is useful adjacent dependency
  work, but it is not an exact duplicate of benchmark 020 or the current
  draft-only items #439 / #444 / #479
- [#288](https://github.com/supabase/pg-toolbelt/pull/288) covers range-type
  creation dependencies in `pg-topo`. This is useful topology work, but it
  does not map to a current pgschema benchmark or draft-only parity item
- [#307](https://github.com/supabase/pg-toolbelt/pull/307) remains open as
  adjacent `pg-delta-next` work, and
  [#315](https://github.com/supabase/pg-toolbelt/pull/315) is its RED test
  companion. Neither PR affects the current-engine parity benchmark state

Separately, pg-toolbelt
[#308](https://github.com/supabase/pg-toolbelt/issues/308) and
[#310](https://github.com/supabase/pg-toolbelt/pull/310) were checked as
adjacent function-privilege work. They are useful current context, but they do
not replace [#219](https://github.com/supabase/pg-toolbelt/issues/219): their
scope is `REVOKE EXECUTE ... FROM PUBLIC`, not the enum-typed function
signature drift from pgschema #366.
