# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-08-28)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `6f480e6ed707133e13bd76c5ff3a8df6102806ee`
- checked-in/live `repos/pgschema` @ `00db700e74b2b255e1e570495ae59fda6af38ed7`

> The 2026-08-28 refresh finds **no behavioral benchmark-matrix delta** versus
> the 2026-08-27 snapshot.
>
> - the active benchmarked gap set remains **021** and **022**
> - checked-in/live `repos/pg-toolbelt` remains at
>   `6f480e6ed707133e13bd76c5ff3a8df6102806ee`
>   (`@supabase/pg-delta@1.0.0-alpha.47`)
> - checked-in/live `repos/pgschema` advances to
>   `00db700e74b2b255e1e570495ae59fda6af38ed7`
>   after merged PRs
>   [#560](https://github.com/pgplex/pgschema/pull/560) and
>   [#562](https://github.com/pgplex/pgschema/pull/562)
> - checked-in/live `pg-delta` is unchanged from 2026-08-27, so the current
>   active-gap structural evidence still stands:
>   - `src/extract/relations.ts` still filters relation columns with
>     `a.attislocal`, so inherited partition-child local overrides never become
>     diff-visible facts
>   - `src/plan/rules/tables.ts` still hard-codes bare
>     `CREATE TABLE ... PARTITION OF ... ${bound}` rendering with no typed child
>     column-element list
>   - `src/extract/relations.ts` still stores only `generatedExpr` from
>     `attgenerated`
>   - `src/plan/rules/helpers.ts` still hard-codes
>     `GENERATED ALWAYS AS (...) STORED`
> - the current open pgschema watch list is now
>   [#49](https://github.com/pgplex/pgschema/issues/49),
>   [#52](https://github.com/pgplex/pgschema/issues/52),
>   [#84](https://github.com/pgplex/pgschema/issues/84),
>   [#450](https://github.com/pgplex/pgschema/issues/450), and
>   [#559](https://github.com/pgplex/pgschema/issues/559)
> - issue [#557](https://github.com/pgplex/pgschema/issues/557) closed on
>   2026-08-28 via merged PR
>   [#560](https://github.com/pgplex/pgschema/pull/560), but it remains
>   operational apply ergonomics rather than a schema-diff benchmark delta for
>   pg-delta
> - newly closed issue [#561](https://github.com/pgplex/pgschema/issues/561)
>   (`NULLS FIRST` / `NULLS LAST` index ordering) appears **covered** in current
>   pg-delta because standalone indexes are keyed on exact
>   `pg_get_indexdef(i.indexrelid)` output in
>   `src/extract/relations.ts`, and `src/plan/rules/indexes.ts` replays that
>   stored `def` unchanged apart from optional `CONCURRENTLY` insertion
> - direct exact duplicate searches for `pgschema#499`, `pgschema#501`,
>   `pgschema#439`, `pgschema#444`, `pgschema#559`, and `pgschema#561` still
>   return no dedicated pg-toolbelt issue or PR; keyword searches for
>   `VIRTUAL generated` and `PARTITION OF` still only surface umbrella fidelity
>   issue
>   [#332](https://github.com/supabase/pg-toolbelt/issues/332)
> - keyword searches for `lock timeout`, `config data`, `NULLS LAST`, and
>   related event-trigger RLS terms still surface no exact pg-toolbelt
>   duplicate for the latest pgschema watch-list and resolved-issue additions
> - current open pg-toolbelt PRs
>   [#449](https://github.com/supabase/pg-toolbelt/pull/449),
>   [#444](https://github.com/supabase/pg-toolbelt/pull/444),
>   [#432](https://github.com/supabase/pg-toolbelt/pull/432),
>   [#288](https://github.com/supabase/pg-toolbelt/pull/288) remain useful
>   context, but none is a dedicated exact duplicate of the active benchmarks or
>   the older draft-only gaps
>   [#439](https://github.com/pgplex/pgschema/issues/439) /
>   [#444](https://github.com/pgplex/pgschema/issues/444)
> - open pg-toolbelt issue
>   [#451](https://github.com/supabase/pg-toolbelt/issues/451) is useful new
>   upstream context on the pg-delta side, but it does not match a current open
>   pgschema watch-list issue or the active benchmark scenarios

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
| 020 | [UNIQUE constraint NULLS NOT DISTINCT](020-unique-constraint-nulls-not-distinct.md) | [#412](https://github.com/pgplex/pgschema/issues/412) | none found | none found | **Solved in pg-delta** |
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |

> Historical benchmark files are retained even after pg-delta fixes land.
> The status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Two resolved-issue benchmark scenarios remain active as unresolved behavior:

- **021** - child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`
- **022** - PostgreSQL 18 `VIRTUAL` generated columns

The checked-in/live `pg-delta` head is unchanged on 2026-08-28, so the
2026-08-27 structural-gap evidence still shows:

- benchmark **021** remains structurally uncovered because
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still filters
  child-inherited columns with `a.attislocal`, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still emits
  only a bare `CREATE TABLE ... PARTITION OF ... FOR VALUES ...` form with no
  child-local column-element list
- benchmark **022** remains structurally uncovered because
  `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still collapses
  `attgenerated` to `generatedExpr`, and
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still renders
  generated columns as `... STORED`
- the focused 2026-08-14 runtime probes remain the latest direct runtime
  evidence for both scenarios; nothing in the 2026-08-27 state changes those
  specific codepaths
- comments on the umbrella tracker
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332)
  now carry both fidelity-gap notes, but there is still no dedicated exact
  issue or PR for either benchmark

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#450](https://github.com/pgplex/pgschema/issues/450),
and [#559](https://github.com/pgplex/pgschema/issues/559).

Screened candidates:

- **#49** explicit rename / refactor workflow proposal - **not parity
  work for pg-delta**
- **#52** explicit before / after SQL file execution in plan output -
  **not parity work for pg-delta**
- **#84** feedback / testimonial collection thread - **not parity work
  for pg-delta**
- **#450** missing role blocks plan/apply - **not parity work for
  pg-delta**; this remains specific to pgschema's desired-state temp
  schema workflow, while pg-delta diffs live catalogs directly
- **#559** support config data evolution - **not parity work for pg-delta**;
  current pg-delta's
  SQL-file loader explicitly treats row-level comparison as out of scope, and
  `packages/pg-delta/tests/load-sql-files.test.ts` notes that the loader
  "deliberately never compares data"

There is currently **no dedicated exact open pg-toolbelt parity tracker** for
the active benchmarks above or for the older draft-only gaps
[#439](https://github.com/pgplex/pgschema/issues/439) /
[#444](https://github.com/pgplex/pgschema/issues/444). The remaining active
benchmarks **021** / **022** are only adjacently tracked under the open
umbrella fidelity issue
[pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332):
keyword duplicate searches still surface that issue, and comments on the issue
thread carry both gap notes, but there is still no dedicated issue or PR for
either benchmark. Exact duplicate searches for watch-list issues
[#559](https://github.com/pgplex/pgschema/issues/559) also return no dedicated
pg-toolbelt issue or PR, but it remains outside the schema-diff benchmark
matrix.

## Recent closed-issue / tracker updates

- no benchmark status rows changed between 2026-08-27 and 2026-08-28;
  checked-in/live `pg-toolbelt` is unchanged and `pgschema` advanced to
  `00db700e74b2b255e1e570495ae59fda6af38ed7`, but neither the issue
  [#557](https://github.com/pgplex/pgschema/issues/557) closure nor the newly
  fixed issue [#561](https://github.com/pgplex/pgschema/issues/561) changes the
  active benchmark matrix

- **#557** lock timeout and retries - closed by
  [pgschema#560](https://github.com/pgplex/pgschema/pull/560) and remains
  **not parity work for pg-delta**; current pg-delta already exposes
  `lockTimeoutMs` through `src/apply/apply-preamble.ts` and
  `src/cli/commands/schema.ts`, while the pgschema fix adds apply retry
  ergonomics rather than changing schema-diff fidelity

- **#561** index `NULLS FIRST` / `NULLS LAST` ordering - closed by
  [pgschema#562](https://github.com/pgplex/pgschema/pull/562) and appears
  **covered** in current pg-delta; `src/extract/relations.ts` stores exact
  `pg_get_indexdef(i.indexrelid)` output in standalone index facts, the diff
  keys indexes on exact `def`, and `src/plan/rules/indexes.ts` replays that
  definition unchanged apart from optional `CONCURRENTLY` insertion, so
  non-default null-ordering clauses should survive extraction, diff, and plan
  generation even though there is no dedicated exact regression test yet

- **#493** `--qualify-schema` type-reference follow-up - closed on
  2026-08-21 and remains **not parity work for pg-delta**; the issue is still
  about pgschema's desired-schema render / IR fidelity rather than pg-delta's
  live-catalog diff surface
- **#404** deferrable unique constraints - **covered** in current
  pg-delta; exact tracker
  [pg-toolbelt#218](https://github.com/supabase/pg-toolbelt/issues/218)
  closed on 2026-08-09 after the clean-room rewrite landed
- **#366** enum-arg function privilege signatures - **covered** in
  current pg-delta; exact tracker
  [pg-toolbelt#219](https://github.com/supabase/pg-toolbelt/issues/219)
  closed on 2026-08-09 after the clean-room rewrite landed
- **#551** removing an explicit RLS `WITH CHECK` clause - closed by
  [pgschema#554](https://github.com/pgplex/pgschema/pull/554) and remains
  **covered** in current pg-delta;
  `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/policies.ts` still
  rebuilds policies when `usingExpr` / `checkExpr` changes, and
  `src/plan/policy-clause-removal.test.ts` still pins the clause-removal path
- **#552** cross-schema partition child planning with an external plan database
  - closed by [pgschema#555](https://github.com/pgplex/pgschema/pull/555) and
  remains **not parity work for pg-delta**; the merged fix adds cross-schema
  partition-parent stubs in `repos/pgschema/cmd/plan/partition_stubs.go`,
  while pg-delta still diffs live catalogs directly and its active partition
  benchmark remains the separate child-override gap
  [021](021-partition-child-column-overrides.md)
- **#553** external plan database rejects `ALTER DEFAULT PRIVILEGES` in
  Supabase-style plans - closed by
  [pgschema#556](https://github.com/pgplex/pgschema/pull/556) and remains
  **not parity work for pg-delta**; the merged fix adds temporary role stubs
  for pgschema's external plan database, while current pg-delta already
  exercises default-privilege planning in Supabase-style contexts through
  `src/plan/rules/default-privilege.test.ts` and
  `src/policy/supabase-default-privileges.test.ts`
- **#412** `UNIQUE NULLS NOT DISTINCT` on table constraints - now
  **covered** in current pg-delta; benchmark [020](020-unique-constraint-nulls-not-distinct.md)
  is retained as a historical record
- **#518** extension-owned type schema mismatch - closed by
  [pgschema#544](https://github.com/pgplex/pgschema/pull/544) and still
  **not parity work for pg-delta**
- **#519** view normalization through the temporary plan schema - closed by
  [pgschema#520](https://github.com/pgplex/pgschema/pull/520) and still
  **not parity work for pg-delta**
- **#534** self-referencing FK to a non-PK standalone unique index on the same
  table - closed by [pgschema#540](https://github.com/pgplex/pgschema/pull/540)
  and remains **covered** in current pg-delta
- **#535** domain created over a table row type - closed by
  [pgschema#539](https://github.com/pgplex/pgschema/pull/539) and remains
  **covered** in current pg-delta
- **#536** dropping a foreign-keyed table/column in the wrong order - closed
  upstream and remains **covered** in current pg-delta
- **#537** built-in `ALTER COLUMN TYPE` without a `USING` clause - closed by
  [pgschema#541](https://github.com/pgplex/pgschema/pull/541), remains
  **covered** in current pg-delta, and matches the solved benchmark family in
  [005](005-alter-column-type-using-clause.md)
- **#538** dropping a table with a trigger - closed upstream; current pg-delta
  already has trigger-drop-before-function-drop coverage (historical tracker
  [pg-toolbelt#137](https://github.com/supabase/pg-toolbelt/issues/137) plus
  the `trigger-operations--trigger-drop-before-function-drop` corpus scenario)
- **#545** function signature depends on a deferred table row type - closed by
  [pgschema#546](https://github.com/pgplex/pgschema/pull/546); current
  pg-delta already resolves routine signature dependencies on relation row
  types through `pg_depend` in
  `repos/pg-toolbelt/packages/pg-delta/src/extract/dependencies.ts`, so no new
  benchmark file or duplicate tracker is needed
- **#548** cross-schema FK to `auth.users` when the `auth` schema is
  intentionally excluded from a pgschema dump - closed by
  [pgschema#549](https://github.com/pgplex/pgschema/pull/549) and remains
  **not parity work for pg-delta**; pg-delta diffs live catalogs directly and
  already carries `auth`-schema fixtures, so no benchmark or duplicate tracker
  change is needed
- **#499** child-specific column elements on `PARTITION OF` create -
  still **not covered in current behavior**, with only umbrella-thread context
  from [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332);
  benchmarked as [021](021-partition-child-column-overrides.md)
- **#501** PostgreSQL 18 `VIRTUAL` generated columns - still **not covered in
  current behavior**, with only umbrella-thread context from
  [pg-toolbelt#332](https://github.com/supabase/pg-toolbelt/issues/332);
  benchmarked as [022](022-virtual-generated-columns.md)
- **#506** new-table FK before standalone unique index - **covered** in
  current pg-delta; benchmark [023](023-fk-before-standalone-unique-index.md)
  is retained as a historical record
- draft-only gaps [#439](https://github.com/pgplex/pgschema/issues/439)
  and [#444](https://github.com/pgplex/pgschema/issues/444) still have no
  exact pg-toolbelt issue or PR

## Upstream watch list

- the current open pgschema watch scope is
  [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#450](https://github.com/pgplex/pgschema/issues/450), and
  [#559](https://github.com/pgplex/pgschema/issues/559)
- checked-in/live `pg-toolbelt` now sits at
  `6f480e6ed707133e13bd76c5ff3a8df6102806ee`
- checked-in/live `pgschema` now sits at
  `00db700e74b2b255e1e570495ae59fda6af38ed7`
- new open pg-toolbelt issue
  [#451](https://github.com/supabase/pg-toolbelt/issues/451) tracks event-
  trigger-driven RLS state drift on identical SQL inputs; it is useful current
  pg-delta context, but it does not map to an open pgschema issue or the active
  benchmarked gaps
- comments on open umbrella issue
  [#332](https://github.com/supabase/pg-toolbelt/issues/332) remain the
  closest tracker context for benchmarks **021** / **022**
- current open pg-toolbelt PRs
  [#449](https://github.com/supabase/pg-toolbelt/pull/449),
  [#444](https://github.com/supabase/pg-toolbelt/pull/444),
  [#432](https://github.com/supabase/pg-toolbelt/pull/432),
  and [#288](https://github.com/supabase/pg-toolbelt/pull/288) are useful current
  context, but none is a dedicated exact duplicate of benchmarks **021** /
  **022** or the draft-only gaps **#439** / **#444**

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by
  the automation scripts.
