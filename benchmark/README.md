# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-07-23)

Refreshed against:

- `repos/pg-toolbelt` @ `c0decd173d191bc470bf7b8c8dd3e862f08ae398`
- `repos/pgschema` @ `a0acf0b9590a6bd7b3455d795f7e547490aa9699`

> The 2026-07-23 refresh found **no benchmark-matrix delta** and **no
> pg-delta code-head delta** versus the 2026-07-22 sweep: checked-in and live
> `pg-toolbelt` both still remain
> `c0decd173d191bc470bf7b8c8dd3e862f08ae398`, while `pgschema/main` advanced
> from `5f2b37bae6d51068b3a3b05fec3185c4219f8968` to
> `a0acf0b9590a6bd7b3455d795f7e547490aa9699` via merged
> [pgschema#514](https://github.com/pgplex/pgschema/pull/514) for still-open
> issue [#493](https://github.com/pgplex/pgschema/issues/493). That merged PR
> extends dump-side `--qualify-schema` handling for same-schema type
> references, but the upstream issue remains open for the still-outstanding
> function / procedure parameter and return-type slices, so it remains **not
> parity work** for pg-delta. The current open pgschema issue set still
> consists of [#49](https://github.com/pgplex/pgschema/issues/49),
> [#52](https://github.com/pgplex/pgschema/issues/52),
> [#84](https://github.com/pgplex/pgschema/issues/84),
> [#450](https://github.com/pgplex/pgschema/issues/450), and
> [#493](https://github.com/pgplex/pgschema/issues/493). Exact pg-toolbelt
> trackers still remain only
> [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
> [#219](https://github.com/supabase/pg-toolbelt/issues/219). New pg-toolbelt
> movement since the previous sweep is that
> [#356](https://github.com/supabase/pg-toolbelt/pull/356) is now merged while
> [#355](https://github.com/supabase/pg-toolbelt/pull/355) remains open;
> issues [#344](https://github.com/supabase/pg-toolbelt/issues/344) and
> [#346](https://github.com/supabase/pg-toolbelt/issues/346) also remain open,
> and open issue [#286](https://github.com/supabase/pg-toolbelt/issues/286)
> remains adjacent rather than an exact duplicate for the older draft-only gap
> [#439](https://github.com/pgplex/pgschema/issues/439). Broader open backlog
> issues [#332](https://github.com/supabase/pg-toolbelt/issues/332),
> [#333](https://github.com/supabase/pg-toolbelt/issues/333),
> [#339](https://github.com/supabase/pg-toolbelt/issues/339), and
> [#340](https://github.com/supabase/pg-toolbelt/issues/340) likewise remain
> adjacent rather than exact duplicates for benchmarks **020** through **023**
> or the older draft-only gaps
> [#439](https://github.com/pgplex/pgschema/issues/439) and
> [#444](https://github.com/pgplex/pgschema/issues/444). See
> [`docs/parity-refresh-2026-07-19.md`](../docs/parity-refresh-2026-07-19.md),
> [`docs/parity-refresh-2026-07-20.md`](../docs/parity-refresh-2026-07-20.md),
> [`docs/parity-refresh-2026-07-21.md`](../docs/parity-refresh-2026-07-21.md),
> [`docs/parity-refresh-2026-07-22.md`](../docs/parity-refresh-2026-07-22.md),
> and [`docs/parity-refresh-2026-07-23.md`](../docs/parity-refresh-2026-07-23.md)
> for the latest sweeps.

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
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | none found | none found | **Not covered** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | none found | **Not covered** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Four resolved-issue benchmark scenarios remain active as unresolved:

- **020** — `UNIQUE NULLS NOT DISTINCT` on table constraints
- **021** — child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`
- **022** — PostgreSQL 18 `VIRTUAL` generated columns
- **023** — new-table foreign key sorted before a standalone unique index on the
  referenced table

There is **no** benchmark-matrix delta versus the 2026-07-22 refresh.
Benchmarks 020, 021, 022, and 023 remain active with unchanged parity status.

There is **no** code-head delta in pg-delta for this refresh:

- `pg-delta` remains `c0decd173d191bc470bf7b8c8dd3e862f08ae398`
- `pgschema` advanced from `5f2b37bae6d51068b3a3b05fec3185c4219f8968` to
  `a0acf0b9590a6bd7b3455d795f7e547490aa9699`
- the pgschema delta is merged
  [pgschema#514](https://github.com/pgplex/pgschema/pull/514) for still-open
  issue [#493](https://github.com/pgplex/pgschema/issues/493), which extends
  dump-side same-schema type qualification under `--qualify-schema` without
  changing pg-delta's current parity classification

A targeted GitHub sweep for the latest upstream issue state now shows:

- **#505** `Can't drop trigger function` — **closed upstream** by merged
  [pgschema#511](https://github.com/pgplex/pgschema/pull/511) and still
  **covered** in current pg-delta. Existing trigger integration coverage already
  exercises dropping triggers before dropping the trigger function they call
- **#506** new table inline FK before new `UNIQUE` constraint / unique index on
  a pre-existing referenced table — **closed upstream** by merged
  [pgschema#507](https://github.com/pgplex/pgschema/pull/507). Current
  pg-delta still splits the scenario:
  - the new-`UNIQUE` table-constraint variant is already **covered**
  - the standalone unique-index variant remains **not covered** and is now
    benchmarked as [023](023-fk-before-standalone-unique-index.md)
- **#508** `INCLUDE` columns dropped when adding or rebuilding an index via
  `CREATE INDEX CONCURRENTLY` — **closed upstream** by merged
  [pgschema#512](https://github.com/pgplex/pgschema/pull/512) and remains
  **covered** in current pg-delta. A focused `CreateIndex` probe still
  preserved `INCLUDE (tenant)` in serialized SQL
- **#509** online index rebuild emits bare `DROP INDEX` after `DROP COLUMN`
  already removed the index — **closed upstream** by merged
  [pgschema#510](https://github.com/pgplex/pgschema/pull/510) and remains **not
  parity work for pg-delta's current default-branch planner**. pg-delta does
  not use pgschema's concurrent rebuild choreography, and a focused ordering
  probe still produced `DROP INDEX` -> `ALTER TABLE ... DROP COLUMN` ->
  `CREATE INDEX`
- the highest live pgschema issue number remains **#509**; newer numbers
  **#510**, **#511**, and **#512** are PRs, not issues

No new exact pg-toolbelt issue or PR was found for benchmarks 020, 021, 022,
or 023. Exact open pg-toolbelt trackers still exist only for:

- pgschema [#404](https://github.com/pgplex/pgschema/issues/404) ->
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
- pgschema [#366](https://github.com/pgplex/pgschema/issues/366) ->
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)

The active benchmark probes were rerun against the new pg-delta head in this
refresh:

- benchmark 020 still reproduces as a **zero-change** diff when toggling an
  existing plain `UNIQUE` table constraint to `UNIQUE NULLS NOT DISTINCT`,
  while creating a brand-new `NULLS NOT DISTINCT` table constraint still works
- benchmark 021 still emits only the bare `PARTITION OF ... FOR VALUES ...`
  statement with no child-specific column overrides
- benchmark 022 still serializes the PostgreSQL 18 case as `... STORED` rather
  than `... VIRTUAL`
- benchmark 023 newly reproduces as `CREATE TABLE child` -> `ADD child FK` ->
  `CREATE UNIQUE INDEX` for the standalone unique-index slice

Those executed checks leave benchmarks 020, 021, 022, and 023 as the active
benchmarked gaps after this refresh.

## Open pgschema issue screening (current state)

The currently still-open reviewed issue set is:

Screened candidates:

- **#49** explicit rename / refactor workflow proposal — **not parity work for
  pg-delta**; this is a pgschema-specific workflow design, not a current
  pg-delta diff or planning gap
- **#52** explicit before / after SQL file execution in plan output — **not
  parity work for pg-delta**; this is a pgschema-specific escape-hatch /
  workflow request rather than a live-catalog diff gap
- **#84** feedback / testimonial collection thread — **not parity work for
  pg-delta**; this is community outreach rather than schema-diff behavior
- **#450** missing role blocks plan/apply — **still not parity work for
  pg-delta** after its 2026-07-11 upstream update; this is specific to
  pgschema applying dumped SQL into a temporary planning schema, while pg-delta
  diffs live catalogs directly and already models roles plus privilege
  dependencies
- **#493** inspector / IR should preserve schema identity for type references
  under `--qualify-schema` — **not parity work for pg-delta**; merged
  [pgschema#514](https://github.com/pgplex/pgschema/pull/514) now implements
  same-schema type-reference qualification for columns, domains, aggregates,
  and composites, but the issue remains open for function / procedure
  parameter and return types and still does not change pg-delta parity
  classification
Issue [#513](https://github.com/pgplex/pgschema/issues/513) is no longer in
the open-screening set because it closed upstream on 2026-07-20 as completed
and still remains **not parity work for pg-delta**; see the closed-issue notes
below.
Historical draft text is recorded in markdown for the older tracked scenarios
and the remaining draft-only uncovered candidates. The 2026-07-04 note for
#501 and the 2026-07-07 note for #506 are retained as pre-promotion context
even though those gaps are now benchmarked as [022](022-virtual-generated-columns.md)
and [023](023-fk-before-standalone-unique-index.md):

- [`docs/parity-issue-drafts-2026-04-22.md`](../docs/parity-issue-drafts-2026-04-22.md)
- [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- [`docs/parity-issue-drafts-2026-05-27.md`](../docs/parity-issue-drafts-2026-05-27.md)
- [`docs/parity-issue-drafts-2026-06-01.md`](../docs/parity-issue-drafts-2026-06-01.md)
- [`docs/parity-issue-drafts-2026-06-17.md`](../docs/parity-issue-drafts-2026-06-17.md)
- [`docs/parity-issue-drafts-2026-06-19.md`](../docs/parity-issue-drafts-2026-06-19.md)
- [`docs/parity-issue-drafts-2026-07-03.md`](../docs/parity-issue-drafts-2026-07-03.md)
- [`docs/parity-issue-drafts-2026-07-04.md`](../docs/parity-issue-drafts-2026-07-04.md)
- [`docs/parity-issue-drafts-2026-07-07.md`](../docs/parity-issue-drafts-2026-07-07.md)

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
- **#501** PostgreSQL 18 `VIRTUAL` generated columns — **not covered** in
  current pg-delta; merged
  [pgschema#503](https://github.com/pgplex/pgschema/pull/503) closes the
  upstream issue, and the remaining pg-delta gap is now benchmarked as
  [022](022-virtual-generated-columns.md)
- **#502** `COMMENT ON COLUMN` misresolved when a table shares the target schema
  name — **closed upstream** by merged
  [pgschema#504](https://github.com/pgplex/pgschema/pull/504) and still **not
  parity work for pg-delta**; current column-comment serialization fully
  qualifies `schema.table.column`
- **#505** `Can't drop trigger function` — **closed upstream** by merged
  [pgschema#511](https://github.com/pgplex/pgschema/pull/511) and still
  **covered** in current pg-delta; existing `trigger-operations.test.ts`
  coverage already exercises dropping triggers before dropping the trigger
  function they call
- **#506** new table inline FK before a new `UNIQUE` constraint / unique index
  on a pre-existing referenced table — **closed upstream** by merged
  [pgschema#507](https://github.com/pgplex/pgschema/pull/507). The
  table-constraint slice is already covered, while the remaining standalone
  unique-index slice is now benchmarked as
  [023](023-fk-before-standalone-unique-index.md)
- **#508** `INCLUDE` columns dropped when adding or rebuilding an index via
  `CREATE INDEX CONCURRENTLY` — **closed upstream** by merged
  [pgschema#512](https://github.com/pgplex/pgschema/pull/512) and still
  **covered** in current pg-delta; `CreateIndex.serialize()` preserves the
  `INCLUDE` clause
- **#509** online index rebuild emits bare `DROP INDEX` after `DROP COLUMN`
  already removed the index — **closed upstream** by merged
  [pgschema#510](https://github.com/pgplex/pgschema/pull/510) and still **not
  parity work for pg-delta's current default-branch planner**
- **#513** full migration handling workflow — **closed upstream as completed**
  on 2026-07-20 and still **not parity work for pg-delta**; this is workflow /
  migration-history orchestration rather than a live-catalog diff or current
  planner gap
- **#515** trigger comment omitted when adding a trigger to an existing table
  — **closed upstream** by merged
  [pgschema#516](https://github.com/pgplex/pgschema/pull/516) and **covered**
  in current pg-delta for the reported comment scenario; `diffTriggers()`
  already emits `CreateTrigger` plus `CreateCommentOnTrigger` when a newly
  created trigger carries a comment, so no new benchmark file or duplicate
  pg-toolbelt tracker is needed
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
- **#439** constraint replacement with dependents — **resolved upstream** and
  still carried as a draft-only uncovered finding from earlier refreshes; no
  exact pg-toolbelt issue / PR exists yet, and the saved draft remains in
  [`docs/parity-issue-drafts-2026-05-23.md`](../docs/parity-issue-drafts-2026-05-23.md)
- **#444** drop-column ordering with dependent views — **resolved upstream** and
  still carried as a draft-only uncovered finding from earlier refreshes;
  related pg-toolbelt work exists in
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

- pgschema [#514](https://github.com/pgplex/pgschema/pull/514) (`feat(dump):
  qualify same-schema type references under --qualify-schema (#493)`) is now
  **merged** and remains **not parity work** for pg-delta; it extends
  pgschema's dump-only qualification mode for columns/domains/aggregates/
  composites, while issue #493 stays open for the remaining function /
  procedure signature slices rather than changing live-catalog diff or planner
  behavior
- pgschema [#504](https://github.com/pgplex/pgschema/pull/504) (`fix: always
  schema-qualify table in COMMENT ON COLUMN (#502)`) is now **merged** and
  remains **not parity work for pg-delta**
- pgschema [#507](https://github.com/pgplex/pgschema/pull/507) (`fix: defer new
  table inline FK when it depends on a new unique constraint (#506)`) is now
  **merged**. Current pg-delta already covers the new-`UNIQUE`
  table-constraint slice, but the standalone unique-index slice remains **not
  covered** and is now benchmarked as
  [023](023-fk-before-standalone-unique-index.md)
- pgschema [#510](https://github.com/pgplex/pgschema/pull/510) (`fix: use DROP
  INDEX IF EXISTS in online index rebuild (#509)`) is now **merged**. This is
  useful pgschema context, but it does not map to an exact current pg-delta
  tracker because the default-branch pg-delta planner already orders the
  analogous non-online steps safely
- pgschema [#511](https://github.com/pgplex/pgschema/pull/511) (`fix: drop
  triggers on dropped tables before their functions (#505)`) is now **merged**
  and remains **covered** in current pg-delta
- pgschema [#512](https://github.com/pgplex/pgschema/pull/512) (`fix: preserve
  INCLUDE columns in CREATE INDEX CONCURRENTLY (#508)`) is now **merged** and
  remains **covered** in current pg-delta
- pgschema [#516](https://github.com/pgplex/pgschema/pull/516) (`fix: emit
  COMMENT and DISABLE for newly added table triggers`) is now **merged** and
  remains **covered** in current pg-delta for the reported trigger-comment
  scenario. A focused 2026-07-22 local roundtrip probe still converged when
  the branch added a new commented trigger to an existing table
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
- pgschema [#503](https://github.com/pgplex/pgschema/pull/503) (`fix: support
  PG18 VIRTUAL generated columns (#501)`) is now **merged**, but the exact
  generated-column kind is still **not covered** in current pg-delta and is now
  benchmarked as [022](022-virtual-generated-columns.md)
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
(`c0decd173d191bc470bf7b8c8dd3e862f08ae398`) now also includes the alpha.32
non-superuser extraction fix from pg-toolbelt PR #337, but it still does not
include the unmerged trigger enabled-state work from pg-toolbelt PR #285.
Benchmarks 020, 021, 022, and 023 therefore remain the active resolved-issue
benchmark gaps, while the remaining trigger-state slice from pgschema PR #479
is now tracked by an exact in-flight pg-toolbelt PR rather than an untracked
draft-only gap.

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
  work, but it is not an exact duplicate of benchmark 020, benchmark 023, or
  the current draft-only items #439 / #444 / #479
- [#286](https://github.com/supabase/pg-toolbelt/issues/286) remains open for
  domain CHECK replacement expansion. This is useful adjacent dependency
  work, but it is not an exact duplicate of the draft-only
  `UNIQUE -> PRIMARY KEY` replacement gap from pgschema #439
- [#288](https://github.com/supabase/pg-toolbelt/pull/288) covers range-type
  creation dependencies in `pg-topo`. This is useful topology work, but it
  does not map to a current pgschema benchmark or draft-only parity item
- [#307](https://github.com/supabase/pg-toolbelt/pull/307) and
  [#315](https://github.com/supabase/pg-toolbelt/pull/315) are now
  closed/merged as adjacent `pg-delta-next` work. Neither PR affects the
  current-engine parity benchmark state
- [#350](https://github.com/supabase/pg-toolbelt/pull/350) and
  [#354](https://github.com/supabase/pg-toolbelt/pull/354) are now merged as
  adjacent corpus-seeding / proof work. They remain useful current context,
  but neither PR maps to benchmarks 020 through 023 or the older draft-only
  items
- [#355](https://github.com/supabase/pg-toolbelt/pull/355) remains open and
  [#356](https://github.com/supabase/pg-toolbelt/pull/356) is now merged as
  adjacent projection-audit / corpus-proof work tied to issue
  [#333](https://github.com/supabase/pg-toolbelt/issues/333). They improve
  plan-artifact visibility and test coverage, but they do not map to
  benchmarks 020 through 023, tracked issues #218 / #219, or the older
  draft-only items

Separately, pg-toolbelt
[#308](https://github.com/supabase/pg-toolbelt/issues/308) and
[#310](https://github.com/supabase/pg-toolbelt/pull/310) were checked as
adjacent function-privilege work. They are useful current context, but they do
not replace [#219](https://github.com/supabase/pg-toolbelt/issues/219): their
scope is `REVOKE EXECUTE ... FROM PUBLIC`, not the enum-typed function
signature drift from pgschema #366.
