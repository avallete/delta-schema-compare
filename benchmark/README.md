# Benchmark — pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-08-07)

Refreshed against:

- checked-in `repos/pg-toolbelt` @ `2929e83981fee139772cc1c60255f1b2592a6f3a`
- live `pg-toolbelt` `main` @ `2929e83981fee139772cc1c60255f1b2592a6f3a`
- `repos/pgschema` @ `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`

> The 2026-08-07 refresh found **no benchmark-matrix delta** versus the
> 2026-08-06 sweep. The active benchmarked gap set therefore remains **020**,
> **021**, and **022**.
> checked-in/live `pg-delta` remain
> `2929e83981fee139772cc1c60255f1b2592a6f3a`, and focused runtime probes still
> show benchmark **020** planning zero statements, benchmark **021** omitting
> child overrides, and benchmark **022** collapsing `VIRTUAL` back to
> `STORED`.
> `pgschema/main` advanced from `b1d60e8d95cfc95508956e4c1e89572269410501` to
> `0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`, bringing in the merged fixes for
> issue [#530](https://github.com/pgplex/pgschema/issues/530) via
> [#531](https://github.com/pgplex/pgschema/pull/531) and issue
> [#532](https://github.com/pgplex/pgschema/issues/532) via
> [#533](https://github.com/pgplex/pgschema/pull/533).
> Current pg-delta already **covers** both ordering scenarios: the exact
> `#530` roundtrip still converges by prefixing the plan with
> `SET check_function_bodies = false`, and a focused 2026-08-07 pg17 runtime
> probe for `#532` planned the referenced `UNIQUE` constraint before the
> dependent `FOREIGN KEY`, applied cleanly, and left zero remaining changes.
> The current open pgschema issue set is now
> [#49](https://github.com/pgplex/pgschema/issues/49),
> [#52](https://github.com/pgplex/pgschema/issues/52),
> [#84](https://github.com/pgplex/pgschema/issues/84),
> [#450](https://github.com/pgplex/pgschema/issues/450),
> [#493](https://github.com/pgplex/pgschema/issues/493),
> [#518](https://github.com/pgplex/pgschema/issues/518), and
> [#519](https://github.com/pgplex/pgschema/issues/519).
> Exact open pg-toolbelt parity trackers still remain only
> [#218](https://github.com/supabase/pg-toolbelt/issues/218) and
> [#219](https://github.com/supabase/pg-toolbelt/issues/219).
> Open pgschema parity-relevant PRs now narrow back to
> [#517](https://github.com/pgplex/pgschema/pull/517) and
> [#520](https://github.com/pgplex/pgschema/pull/520); both
> [#531](https://github.com/pgplex/pgschema/pull/531) and
> [#533](https://github.com/pgplex/pgschema/pull/533) are merged.
> Adjacent pg-toolbelt work also remains unchanged in parity terms: open
> [#299](https://github.com/supabase/pg-toolbelt/pull/299) is still the
> `feat/pg-delta-next` cutover PR, while merged
> [#379](https://github.com/supabase/pg-toolbelt/pull/379),
> [#380](https://github.com/supabase/pg-toolbelt/pull/380), and
> [#381](https://github.com/supabase/pg-toolbelt/pull/381) still remain on
> `feat/pg-delta-next`, not on the current default-branch engine.
> Direct duplicate searches still found **no exact pg-toolbelt issue or PR**
> for active benchmarks **020** through **022**, the older draft-only gaps
> [#439](https://github.com/pgplex/pgschema/issues/439) and
> [#444](https://github.com/pgplex/pgschema/issues/444), or the newly closed
> ordering issue [#532](https://github.com/pgplex/pgschema/issues/532). The
> previously open ordering issue
> [#530](https://github.com/pgplex/pgschema/issues/530) also still does not
> need a duplicate tracker. See
> [`docs/parity-refresh-2026-08-01.md`](../docs/parity-refresh-2026-08-01.md),
> [`docs/parity-refresh-2026-08-03.md`](../docs/parity-refresh-2026-08-03.md),
> [`docs/parity-refresh-2026-08-04.md`](../docs/parity-refresh-2026-08-04.md),
> [`docs/parity-refresh-2026-08-05.md`](../docs/parity-refresh-2026-08-05.md),
> [`docs/parity-refresh-2026-08-06.md`](../docs/parity-refresh-2026-08-06.md),
> and [`docs/parity-refresh-2026-08-07.md`](../docs/parity-refresh-2026-08-07.md)
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
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |

> Historical benchmark files are retained even after pg-delta fixes land. The
> status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Three resolved-issue benchmark scenarios remain active as unresolved:

- **020** — `UNIQUE NULLS NOT DISTINCT` on table constraints
- **021** — child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`
- **022** — PostgreSQL 18 `VIRTUAL` generated columns

There is **no** benchmark-matrix delta versus the 2026-08-06 refresh.
This refresh advances checked-in `pgschema` from
`b1d60e8d95cfc95508956e4c1e89572269410501` to
`0cf544c03dcc71ae0656d0bc9ca87cae0b09432e`, while checked-in/live
`pg-delta` remain `2929e83981fee139772cc1c60255f1b2592a6f3a`:

- pgschema [#530](https://github.com/pgplex/pgschema/issues/530) is now closed
  by merged [#531](https://github.com/pgplex/pgschema/pull/531) and remains
  **covered** in current pg-delta; the exact 2026-08-07 pg17 roundtrip still
  converged cleanly by prefixing the plan with
  `SET check_function_bodies = false`
- newly closed pgschema
  [#532](https://github.com/pgplex/pgschema/issues/532) is also **covered** in
  current pg-delta; a focused 2026-08-07 pg17 runtime probe planned the
  referenced `UNIQUE` constraint before the dependent `FOREIGN KEY`, applied
  cleanly, and left zero remaining changes
- the earlier newly closed pgschema issue
  [#528](https://github.com/pgplex/pgschema/issues/528) remains **covered** in
  current pg-delta; the exact pg17 probe still preserves the full enum type
  name in `CREATE TABLE`
- newly closed pgschema issues
  [#523](https://github.com/pgplex/pgschema/issues/523),
  [#525](https://github.com/pgplex/pgschema/issues/525), and
  [#527](https://github.com/pgplex/pgschema/issues/527) remain **not parity
  work** for pg-delta
- the open pgschema issue set is now
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450),
  [#493](https://github.com/pgplex/pgschema/issues/493),
  [#518](https://github.com/pgplex/pgschema/issues/518), and
  [#519](https://github.com/pgplex/pgschema/issues/519)
- exact open pg-toolbelt parity trackers still exist only for:
  - pgschema [#404](https://github.com/pgplex/pgschema/issues/404) ->
    [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  - pgschema [#366](https://github.com/pgplex/pgschema/issues/366) ->
    [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
- open pgschema parity-relevant PRs now narrow back to
  [#517](https://github.com/pgplex/pgschema/pull/517) and
  [#520](https://github.com/pgplex/pgschema/pull/520); merged
  [#531](https://github.com/pgplex/pgschema/pull/531) and
  [#533](https://github.com/pgplex/pgschema/pull/533) remain useful context
  but do not add new pg-delta parity gaps
- adjacent pg-toolbelt work remains unchanged in parity terms:
  [#299](https://github.com/supabase/pg-toolbelt/pull/299) remains the open
  `feat/pg-delta-next` cutover PR, while
  [#379](https://github.com/supabase/pg-toolbelt/pull/379),
  [#380](https://github.com/supabase/pg-toolbelt/pull/380), and
  [#381](https://github.com/supabase/pg-toolbelt/pull/381) remain merged on
  `feat/pg-delta-next` rather than `main`

A targeted GitHub + runtime sweep for the current heads now shows:

- no new exact pg-toolbelt issue or PR for benchmarks **020**, **021**, or
  **022**
- direct duplicate probes still found no exact pg-toolbelt issue or PR for the
  older draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  / [#444](https://github.com/pgplex/pgschema/issues/444) or the newly closed
  ordering issue [#532](https://github.com/pgplex/pgschema/issues/532); the
  now-closed issue [#530](https://github.com/pgplex/pgschema/issues/530) also
  still needs no duplicate tracker
- benchmark **020** still plans **zero statements** when toggling an existing
  `UNIQUE` table constraint to `UNIQUE NULLS NOT DISTINCT`
- benchmark **021** still emits only
  `CREATE TABLE ... PARTITION OF ... FOR VALUES ...` and drops the
  child-specific `DEFAULT` / `NOT NULL` overrides
- benchmark **022** still serializes the PostgreSQL 18 case as
  `GENERATED ALWAYS AS (...) STORED` instead of preserving `VIRTUAL`

Those updated source/test notes still leave benchmarks 020, 021, and 022 as
the active benchmarked gaps after this refresh, while benchmark 023 remains
solved.

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
- **#518** extension-owned type schema mismatch causes false-positive diffs
  when pgschema's temp comparison database resolves an extension-owned type into
  a different schema than the real target — **not parity work for pg-delta**;
  pg-delta diffs live catalogs directly, already preserves non-public
  extension-owned types such as `test_schema.vector(768)`, and can model real
  extension schema moves via `ALTER EXTENSION ... SET SCHEMA`
- **#519** view normalization from #316 does not converge through the temporary
  plan schema — **not parity work for pg-delta**; the repeated diff depends on
  pgschema's desired-state temp schema plus qualifier normalization, while
  pg-delta extracts live view definitions from live catalogs, isolates
  `search_path`, and a focused pg17 `ltree` roundtrip probe with
  `public.nlevel(path)` converged cleanly without a repeated diff
Issue [#513](https://github.com/pgplex/pgschema/issues/513) is no longer in
the open-screening set because it closed upstream on 2026-07-20 as completed
and still remains **not parity work for pg-delta**; see the closed-issue notes
below.
Issue [#526](https://github.com/pgplex/pgschema/issues/526) is also no longer
in the open-screening set because it closed upstream on 2026-08-05 via merged
[pgschema#529](https://github.com/pgplex/pgschema/pull/529) and is already
**covered** in current pg-delta; see the closed-issue notes below.
Issue [#530](https://github.com/pgplex/pgschema/issues/530) is no longer in
the open-screening set because it closed upstream on 2026-08-06 via merged
[pgschema#531](https://github.com/pgplex/pgschema/pull/531) and remains
**covered** in current pg-delta; see the closed-issue notes below.
New issue [#532](https://github.com/pgplex/pgschema/issues/532) also closed
upstream on 2026-08-06 via merged
[pgschema#533](https://github.com/pgplex/pgschema/pull/533) and is likewise
already **covered** in current pg-delta; see the closed-issue notes below.
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
  table-constraint slice was already covered, and a focused 2026-07-28 pg17
  plan + roundtrip probe now shows the standalone unique-index slice is also
  covered in current pg-delta. The historical benchmark file is retained as
  [023](023-fk-before-standalone-unique-index.md), but the matrix status now
  moves to solved
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
- **#523** expose `can_run_in_transaction` on plan JSON steps — **closed
  upstream** and still **not parity work for pg-delta**; this is planner JSON
  metadata for downstream migration tooling rather than a live-catalog diff gap
- **#530** function -> table -> function ordering chain (`random_id()` ->
  `x` -> `x_is_flagged()`) — **closed upstream** by merged
  [pgschema#531](https://github.com/pgplex/pgschema/pull/531) and still
  **covered** in current pg-delta; a focused 2026-08-07 pg17 runtime probe
  emitted `SET check_function_bodies = false`, planned the exact
  `CREATE FUNCTION` -> `CREATE FUNCTION` -> `CREATE TABLE` + constraint
  sequence, applied cleanly, and left zero remaining changes
- **#532** FK referencing a `UNIQUE` constraint defined later in the desired
  state — **closed upstream** by merged
  [pgschema#533](https://github.com/pgplex/pgschema/pull/533) and already
  **covered** in current pg-delta; a focused 2026-08-07 pg17 runtime probe
  planned `ALTER TABLE ... ADD CONSTRAINT UNIQUE` before the dependent
  `ALTER TABLE ... ADD CONSTRAINT FOREIGN KEY`, applied cleanly, and left zero
  remaining changes, so no new benchmark file or duplicate tracker is needed
- **#525** close the gap of state-based workflow — **closed upstream** and
  still **not parity work for pg-delta**; this is workflow scope rather than a
  current pg-delta catalog-diff bug
- **#527** embedded PostgreSQL 17 plan artifact availability — **closed
  upstream** and still **not parity work for pg-delta**; this is embedded plan
  database packaging / availability rather than current diff behavior
- **#528** long enum type names truncated in generated column definitions —
  **closed upstream** and **covered** in current pg-delta; a focused
  2026-08-06 pg17 roundtrip emitted
  `CREATE TABLE repro.deal_area_market_info (... type repro.enum_deal_area_market_info_type NOT NULL)`
  with the full enum type name preserved, so no benchmark promotion or
  duplicate tracker is needed
- **#526** function `SET` clauses except `search_path` are dropped —
  **closed upstream** by merged
  [pgschema#529](https://github.com/pgplex/pgschema/pull/529) and **covered**
  in current pg-delta; `procedure.model.ts` already reads `p.proconfig`,
  `procedure.diff.ts` already emits function config `SET` / `RESET` changes,
  and a focused 2026-08-05 pg17 runtime probe emitted both
  `SET search_path TO 'public'` and `SET "TimeZone" TO 'UTC'` before
  roundtripping cleanly, so no new benchmark file or duplicate pg-toolbelt
  tracker is needed
- **#521** enum names being truncated in 1.12.1 — **closed upstream** by
  merged [pgschema#522](https://github.com/pgplex/pgschema/pull/522) and still
  **not parity work for pg-delta**; the failure came from pgschema's
  temporary-schema type-resolution `CASE` expressions resolving to
  PostgreSQL's `name` type and truncating long schema-qualified enum names,
  while pg-delta reads live column types with `format_type(a.atttypid,
  a.atttypmod)` and does not build temporary-schema-qualified type names in
  this path
- **#362**, **#401**, **#414**, **#415**, **#416**, **#420**, **#427**, and
  **#436** — **covered** in current pg-delta
- **#407**, **#409**, **#418**, **#419**, **#421**, **#422**, **#429**,
  **#447**, and **#449** — **not parity work for pg-delta**; these are
  ignore-file, packaging, or pgschema-specific normalization behaviors rather
  than live-catalog diff gaps

- **#366** function privilege signatures with enum argument types — **closed
  upstream as `not_planned` and still tracked** by
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219). A
  focused 2026-07-28 pg17 roundtrip probe for the exact enum-arg privilege
  scenario still converged on current pg-delta, so this remains a coverage
  tracker rather than a benchmark promotion
- adjacent pg-toolbelt work still includes closed
  [#308](https://github.com/supabase/pg-toolbelt/issues/308) plus merged
  [#357](https://github.com/supabase/pg-toolbelt/pull/357) /
  [#358](https://github.com/supabase/pg-toolbelt/pull/358), while open
  [#310](https://github.com/supabase/pg-toolbelt/pull/310) remains redundant
  follow-up work. That scope covers `REVOKE EXECUTE ... FROM PUBLIC` on
  functions rather than the enum-typed signature drift from pgschema #366, so
  the parity label remains `tracked`
- **#404** deferrable unique constraints — **resolved upstream and still
  tracked** by
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218). A
  focused 2026-07-28 pg17 roundtrip probe for the exact
  `UNIQUE ... DEFERRABLE INITIALLY DEFERRED` scenario still converged on
  current pg-delta, so this remains a coverage tracker rather than a benchmark
  promotion
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
  The still-open follow-up #493 keeps the same non-parity classification
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

- pgschema [#533](https://github.com/pgplex/pgschema/pull/533) (`fix:
  topologically sort constraints to ensure UNIQUE before FK dependencies
  (#532)`) is now **merged** against issue
  [#532](https://github.com/pgplex/pgschema/issues/532) and remains
  **covered** in current pg-delta; a focused 2026-08-07 pg17 runtime probe
  planned the referenced `UNIQUE` constraint before the dependent
  `FOREIGN KEY`, applied cleanly, and left zero remaining changes
- pgschema [#531](https://github.com/pgplex/pgschema/pull/531) (`fix:
  defer functions that reference new tables to after table creation (#530)`) is
  now **merged** against issue
  [#530](https://github.com/pgplex/pgschema/issues/530) and remains
  **covered** in current pg-delta; the 2026-08-07 pg17 roundtrip still
  converged cleanly by prefixing the plan with `SET check_function_bodies = false`,
  so this upstream fix does not create a new pg-delta parity gap
- pgschema [#529](https://github.com/pgplex/pgschema/pull/529) (`fix:
  preserve all function SET clauses from pg_proc.proconfig`) is now
  **merged** against issue
  [#526](https://github.com/pgplex/pgschema/issues/526) and remains
  **covered** in current pg-delta; current procedure extraction already reads
  `p.proconfig`, the diff path already emits config `SET` / `RESET` changes,
  and a focused 2026-08-05 pg17 runtime probe emitted both
  `SET search_path TO 'public'` and `SET "TimeZone" TO 'UTC'` before
  roundtripping cleanly
- pgschema [#517](https://github.com/pgplex/pgschema/pull/517) (`fix: strip
  extension-owned type schema qualifiers to prevent false-positive diffs`) is
  now **open** against issue
  [#518](https://github.com/pgplex/pgschema/issues/518) and remains **not
  parity work** for pg-delta; it strips schema qualifiers in pgschema's
  temporary comparison environment when both sides are owned by the same
  extension, while pg-delta already diffs live catalogs directly and
  roundtrips extension-owned types installed outside `public`
- pgschema [#522](https://github.com/pgplex/pgschema/pull/522) (`fix: prevent
  enum name truncation in schema-qualified type resolution (#521)`) is now
  **merged** and remains **not parity work** for pg-delta; the fix is specific
  to pgschema's temporary-schema type-resolution `CASE` expressions resolving
  to PostgreSQL's `name` type, while pg-delta reads live catalog types with
  `format_type(...)` and does not construct temporary-schema-qualified type
  names in this path
- pgschema [#520](https://github.com/pgplex/pgschema/pull/520) (`fix:
  normalize views after temporary schema rename`) is now **open** against issue
  [#519](https://github.com/pgplex/pgschema/issues/519) and remains **not
  parity work** for pg-delta; it targets pgschema's temporary-schema
  view-normalization path rather than live-catalog diff behavior
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
  **merged**. Current pg-delta already covered the new-`UNIQUE`
  table-constraint slice, and a focused 2026-07-28 pg17 plan + roundtrip probe
  now shows the standalone unique-index slice is also covered after the
  adjacent pg-topo ordering fix in
  [pg-toolbelt#361](https://github.com/supabase/pg-toolbelt/pull/361). The
  historical benchmark file remains
  [023](023-fk-before-standalone-unique-index.md), but its matrix status now
  moves to solved
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
(`2929e83981fee139772cc1c60255f1b2592a6f3a`) now matches live `main`. The
2026-08-06 delta from the previous checked-in head is still adjacent parser
work rather than a parity reclassification, and it still does not include the
unmerged trigger enabled-state work from pg-toolbelt PR #285. Benchmarks 020,
021, and 022 therefore remain the active resolved-issue benchmark gaps, while
benchmark 023 is now solved and the remaining trigger-state slice from
pgschema PR #479 is tracked by an exact in-flight pg-toolbelt PR rather than an
untracked draft-only gap.

Existing pg-toolbelt PR activity was also rechecked during this refresh:

- [#365](https://github.com/supabase/pg-toolbelt/issues/365) /
  [#368](https://github.com/supabase/pg-toolbelt/pull/368) now cover
  case-colliding schema export paths on case-insensitive filesystems. This is
  useful current context, but it is not an exact duplicate of benchmarks 020
  through 023, the current draft-only candidates, or open pgschema issues
  [#518](https://github.com/pgplex/pgschema/issues/518) /
  [#519](https://github.com/pgplex/pgschema/issues/519)
- [#301](https://github.com/supabase/pg-toolbelt/issues/301) /
  [#305](https://github.com/supabase/pg-toolbelt/pull/305) now cover
  materialized-view definition stability under differing `search_path` values.
  This is adjacent to historical materialized-view parity work, but it is not
  an exact duplicate of benchmark 008, benchmark 020, the current draft-only
  candidates, or open pgschema issue
  [#519](https://github.com/pgplex/pgschema/issues/519), which is about regular
  view normalization through pgschema's temporary desired-state schema rather
  than live materialized-view extraction
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
- [#355](https://github.com/supabase/pg-toolbelt/pull/355) and
  [#356](https://github.com/supabase/pg-toolbelt/pull/356) are now merged as
  adjacent projection-audit / corpus-proof work tied to issue
  [#333](https://github.com/supabase/pg-toolbelt/issues/333). They improve
  plan-artifact visibility and test coverage, but they do not map to
  benchmarks 020 through 023, tracked issues #218 / #219, or the older
  draft-only items

Separately, pg-toolbelt
[#308](https://github.com/supabase/pg-toolbelt/issues/308) is now closed by
merged [#357](https://github.com/supabase/pg-toolbelt/pull/357), and merged
[#358](https://github.com/supabase/pg-toolbelt/pull/358) plus still-open
[#310](https://github.com/supabase/pg-toolbelt/pull/310) remain adjacent
function-privilege work. They are useful current context, but they do not
replace [#219](https://github.com/supabase/pg-toolbelt/issues/219): their scope
is `REVOKE EXECUTE ... FROM PUBLIC`, not the enum-typed function signature
drift from pgschema #366.
