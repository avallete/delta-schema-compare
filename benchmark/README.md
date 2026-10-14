# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-10-14)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `0abee28a54bd855c13d45e2d7ebb5cb647b46693`
- checked-in/live `repos/pgschema` @ `2bb3352d40c5fc55c3c43abcce395dd11cd22450`

> The 2026-10-14 refresh keeps checked-in/live `repos/pg-toolbelt` at
> `0abee28a54bd855c13d45e2d7ebb5cb647b46693` and checked-in/live
> `repos/pgschema` at `2bb3352d40c5fc55c3c43abcce395dd11cd22450`; neither
> head moved since the 2026-10-13 refresh.
>
> - `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-13'`
>   surfaced open issue
>   [#644](https://github.com/pgplex/pgschema/issues/644)
>   (`dump and plan are slow over high-latency connections: one query per privilege row and per constraint column`)
>   plus open PR [#643](https://github.com/pgplex/pgschema/pull/643)
>   (`fix: preserve partition-index names and attachments in dumps`); #643 is
>   still open and outside the checked-in/live head, while #644 is pgschema-side
>   inspector / latency work rather than a new pg-delta parity gap
> - `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-13'`
>   surfaced only open PR
>   [#541](https://github.com/supabase/pg-toolbelt/pull/541)
>   (`fix(pg-delta): declare rewrites of partitions and inheritance children (CLI-2657)`);
>   it closes issue [#530](https://github.com/supabase/pg-toolbelt/issues/530)
>   but only touches `packages/pg-delta/src/proof/prove.ts` plus corpus data,
>   not the active gap files
> - `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
>   still returned `[]`
> - `benchmark/review-memory.json` adds open issue #644 to the cached
>   watch-list without changing any benchmark verdicts
>
> The active benchmarked gap set therefore remains **021**, **022**, and
> **024**, and there is still **no open uncovered parity candidate** on the
> pgschema side.

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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread), adjacent [#530](https://github.com/supabase/pg-toolbelt/issues/530) (open rewrite-risk follow-up) | open [#541](https://github.com/supabase/pg-toolbelt/pull/541) (rewrite-risk declarations only), adjacent [#470](https://github.com/supabase/pg-toolbelt/pull/470), [#480](https://github.com/supabase/pg-toolbelt/pull/480), and [#488](https://github.com/supabase/pg-toolbelt/pull/488) (merged), [#501](https://github.com/supabase/pg-toolbelt/pull/501) (merged partition-key retype), and [#504](https://github.com/supabase/pg-toolbelt/pull/504) (merged dependency-edge repair) | **Tracked (umbrella thread only)** |
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |
| 024 | [PG18 native NOT NULL validation](024-pg18-not-null-validation.md) | [#564](https://github.com/pgplex/pgschema/issues/564) | none found | historical [#174](https://github.com/supabase/pg-toolbelt/pull/174) (merged, legacy engine only), adjacent [#484](https://github.com/supabase/pg-toolbelt/pull/484) and [#485](https://github.com/supabase/pg-toolbelt/pull/485) (merged) | **Not covered** |

> Historical benchmark files are retained even after pg-delta fixes land.
> The status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Three resolved-issue benchmark scenarios remain active as unresolved behavior:

- **021** - child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    keeps inherited child columns gated by `a.attislocal`, so child-local
    overrides on inherited partition columns do not become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` now has
    merged `_partitionKey` / `replaceRoot` logic from PR
    [#501](https://github.com/supabase/pg-toolbelt/pull/501) and merged
    dependency-edge repairs from PR
    [#504](https://github.com/supabase/pg-toolbelt/pull/504), but the
    partition-child create path still emits bare
    `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed child
    column-element list
  - closed issue [#497](https://github.com/supabase/pg-toolbelt/issues/497),
    open follow-up issue [#502](https://github.com/supabase/pg-toolbelt/issues/502),
    adjacent rewrite-risk issue [#530](https://github.com/supabase/pg-toolbelt/issues/530),
    open PR [#541](https://github.com/supabase/pg-toolbelt/pull/541),
    merged PR [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    merged stacked PR [#503](https://github.com/supabase/pg-toolbelt/pull/503),
    and merged PR [#504](https://github.com/supabase/pg-toolbelt/pull/504)
    sharpen nearby partition-key / rewrite-risk / dependency-edge behavior;
    PR #541 closes #530's proof-declaration bug, but it still does not model
    the separate child-local partition-level default / not-null override
    problem tracked here
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only exact tracker context
- **022** - PostgreSQL 18 `VIRTUAL` generated columns
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    collapses `attgenerated` to generated-expression presence instead of
    preserving `VIRTUAL` versus `STORED`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - the 2026-10-13 pg-delta delta only touches `src/core/fact.ts`,
    `src/frontends/export-sql-files.ts`, `src/plan/graph.ts`,
    `src/plan/internal.ts`, and
    `src/plan/phases/replacement-expansion.ts`; none of those changes
    preserves generated kind, so umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
    only live tracker context
  - current pg-delta already covers resolved pgschema issue
    [#591](https://github.com/pgplex/pgschema/issues/591)'s
    generated-expression-change family, so the active gap remains only the
    generated kind distinction
- **024** - PostgreSQL 18 native `NOT NULL ... NOT VALID` state and pending
  validation visibility
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models nullability through `a.attnotnull`; PG18 `contype = 'n'` rows still
    only survive long enough to emit `table_not_null_comment_skipped`
    diagnostics for commented rows, not to become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - the 2026-10-13 pg-delta delta only touches `src/core/fact.ts`,
    `src/frontends/export-sql-files.ts`, `src/plan/graph.ts`,
    `src/plan/internal.ts`, and
    `src/plan/phases/replacement-expansion.ts`; there is still no exact
    current pg-toolbelt issue or PR for this benchmark

Because today's refresh keeps checked-in/live `pg-toolbelt` at
`0abee28a54bd855c13d45e2d7ebb5cb647b46693` and `pgschema` at
`2bb3352d40c5fc55c3c43abcce395dd11cd22450`, while updated-since checks surface
pgschema issue [#644](https://github.com/pgplex/pgschema/issues/644) plus open
PR [#643](https://github.com/pgplex/pgschema/pull/643) and pg-toolbelt open PR
[#541](https://github.com/supabase/pg-toolbelt/pull/541), active-path rechecks
still find `a.attislocal` in `relations.ts`, generated-column kind still
collapsed to expression presence plus a hard-coded `... STORED` renderer, and
PG18 table `contype = 'n'` rows still kept out of diff-visible facts. PR #541
only touches `packages/pg-delta/src/proof/prove.ts` plus corpus data, so the
checked-in/live active gap files remain unchanged. Exact duplicate searches for
`pgschema#499`, `pgschema#501`, `pgschema#564`, `pgschema#627`,
`pgschema#638`, `pgschema#639`, `pgschema#640`, `pgschema#641`, and
`pgschema#644` still return no dedicated pg-toolbelt issue or PR; keyword
`"PARTITION OF"` searches now surface umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332), follow-up
[#502](https://github.com/supabase/pg-toolbelt/issues/502), rewrite-risk issue
[#530](https://github.com/supabase/pg-toolbelt/issues/530), open PR
[#541](https://github.com/supabase/pg-toolbelt/pull/541), and adjacent
partition work such as PRs
[#501](https://github.com/supabase/pg-toolbelt/pull/501),
[#503](https://github.com/supabase/pg-toolbelt/pull/503),
[#504](https://github.com/supabase/pg-toolbelt/pull/504),
[#470](https://github.com/supabase/pg-toolbelt/pull/470),
[#383](https://github.com/supabase/pg-toolbelt/pull/383), and
[#514](https://github.com/supabase/pg-toolbelt/pull/514) rather than an exact
child-local override tracker; `"VIRTUAL" generated` still only surfaces live
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) plus
historical merged PRs [#378](https://github.com/supabase/pg-toolbelt/pull/378)
and [#299](https://github.com/supabase/pg-toolbelt/pull/299); and
`"NOT NULL" "NOT VALID"` still only surfaces merged PR
[#484](https://github.com/supabase/pg-toolbelt/pull/484), while umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) remains broader
adjacent fidelity context rather than an exact table-column PG18 tracker.
Open pgschema schema-diff issues [#638](https://github.com/pgplex/pgschema/issues/638),
[#639](https://github.com/pgplex/pgschema/issues/639),
[#640](https://github.com/pgplex/pgschema/issues/640), and
[#641](https://github.com/pgplex/pgschema/issues/641) remain covered or
avoided by current pg-delta, issue
[#644](https://github.com/pgplex/pgschema/issues/644) is latency-sensitive
inspector work rather than a new pg-delta parity gap, and the broader
global-state cluster rooted at
[#627](https://github.com/pgplex/pgschema/issues/627) plus open PR
[#637](https://github.com/pgplex/pgschema/pull/637) still does not produce a
new benchmark parity item in this repo. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) therefore still
only covers benchmarks **021** / **022**, benchmark **024** still has no
exact current pg-toolbelt issue or PR, and there is still **no open uncovered
parity candidate**.

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598),
[#623](https://github.com/pgplex/pgschema/issues/623),
[#624](https://github.com/pgplex/pgschema/issues/624),
[#625](https://github.com/pgplex/pgschema/issues/625),
[#626](https://github.com/pgplex/pgschema/issues/626),
[#627](https://github.com/pgplex/pgschema/issues/627),
[#628](https://github.com/pgplex/pgschema/issues/628),
[#629](https://github.com/pgplex/pgschema/issues/629),
[#630](https://github.com/pgplex/pgschema/issues/630),
[#631](https://github.com/pgplex/pgschema/issues/631),
[#632](https://github.com/pgplex/pgschema/issues/632),
[#633](https://github.com/pgplex/pgschema/issues/633),
[#634](https://github.com/pgplex/pgschema/issues/634),
[#635](https://github.com/pgplex/pgschema/issues/635),
[#636](https://github.com/pgplex/pgschema/issues/636),
[#638](https://github.com/pgplex/pgschema/issues/638),
[#639](https://github.com/pgplex/pgschema/issues/639),
[#640](https://github.com/pgplex/pgschema/issues/640),
[#641](https://github.com/pgplex/pgschema/issues/641), and
[#644](https://github.com/pgplex/pgschema/issues/644).

Screened candidates:

- **#49** explicit rename / refactor workflow proposal - **not parity work for
  pg-delta**
- **#52** explicit before / after SQL file execution in plan output - **not
  parity work for pg-delta**
- **#84** feedback / testimonial collection thread - **not parity work for
  pg-delta**
- **#559** config-table data evolution / reference-data management - **not
  parity work for pg-delta**
- **#597** broad multi-schema complexity / auto-ignore feedback - **not parity
  work for pg-delta**
- **#598** interrupted `CREATE INDEX CONCURRENTLY` leaves an invalid index
  behind - **covered** in current pg-delta:
  - `src/extract/relations.ts` captures regular-index `indisvalid` as semantic
    `valid`
  - `src/plan/rules/indexes.ts` diffs `valid` with the `"replace"` strategy
  - `tests/index-invalid-repair.test.ts` covers the invalid-index repair path
- **#623** publish release checksums - **not parity work for pg-delta**
- **#624** SQL function created before `ADD COLUMN` it depends on - **covered**
  in current pg-delta via the routine-plan `check_function_bodies = off`
  preamble plus existing SQL-body forward-reference coverage
- **#625** existing composite-type attribute changes are silently skipped -
  **covered** in current pg-delta via composite `typeAttribute` facts and
  `ALTER TYPE ... ADD ATTRIBUTE ... CASCADE` planning
- **#626** composite type creation runs before its required table - **covered**
  in current pg-delta via dependency extraction that resolves composite row-type
  edges back onto the owning table fact
- **#627 - #636** opt-in global-state roles / ownership cluster (plus open PR
  [#637](https://github.com/pgplex/pgschema/pull/637)) - **not added as new
  benchmark parity items in this repo**. These issues describe pgschema's new
  separate global-manifest surface; adjacent pg-delta role / owner work exists
  in open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471) and
  [#493](https://github.com/supabase/pg-toolbelt/pull/493) plus merged
  membership fixes [#117](https://github.com/supabase/pg-toolbelt/pull/117),
  [#118](https://github.com/supabase/pg-toolbelt/pull/118), and
  [#461](https://github.com/supabase/pg-toolbelt/pull/461), but exact duplicate
  search `pgschema#627` still returns no dedicated pg-toolbelt issue or PR
- **#638** mixed column-privilege rendering (`GRANT INSERT, UPDATE (cols)`) -
  **covered** in current pg-delta:
  - `renderGrantSql()` renders column privileges as `PRIV (col), PRIV (col)`
  - `tests/column-grant-fidelity.test.ts` covers extracted table column grants
  - `src/frontends/sql-format/format-grant.test.ts` explicitly pins
    `GRANT SELECT (col), UPDATE (col) ...`
- **#639** partition bounds / attachment drift - **covered** in current
  pg-delta:
  - extracted table facts preserve `partitionBound` and `parentTable`
  - `src/plan/rules/tables.ts` treats both attributes as `"replace"`
  - corpuses `table-ops--attach-partition` and `table-ops--detach-partition`
    cover attach / detach state changes
- **#640** privileges on partitioned tables are omitted - **covered** in
  current pg-delta:
  - relation extraction already includes partitioned tables in the table ACL
    path (`c.relkind IN ('r', 'p')`)
  - column ACL extraction likewise includes `relkind 'p'`
- **#641** schema-unqualified wait query after `CREATE INDEX CONCURRENTLY` -
  **covered / not a pg-delta gap**:
  - pg-delta apply executes action SQL directly via `client.query(action.sql)`
    instead of a separate name-based wait loop
  - invalid concurrent-index residue is already modeled through `indisvalid`
    and covered by `tests/index-invalid-repair.test.ts`
- **#644** latency-sensitive dump / plan inspector queries and same-name
  foreign-key column-order lookup - **not parity work for pg-delta**:
  - `src/extract/scope.ts` resolves ACL grantees in bulk from `aclexplode(...)`
    with `LEFT JOIN pg_roles g ON g.oid = e.grantee`, so pg-delta does not do
    one round-trip per privilege row
  - `src/extract/relations.ts` derives constraint key order with
    `unnest(con.conkey) WITH ORDINALITY`, so the same-name foreign-key
    misordering described in the issue is already avoided
  - the reported bottleneck is pgschema's high-latency inspector architecture
    rather than a missing pg-delta schema-diff capability

There is currently **no open uncovered parity candidate** on the pgschema
side. The remaining active benchmarks **021** / **022** still only have
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) as
exact tracker context, benchmark **024** still has no exact current
pg-toolbelt issue or PR, open PR
[#541](https://github.com/supabase/pg-toolbelt/pull/541) remains only adjacent
rewrite-risk work on top of the current pg-toolbelt head, and issue
[#644](https://github.com/pgplex/pgschema/issues/644) is not a new parity
candidate. This repository still has no local tracker issues.

## Recent closed-issue / tracker updates

No benchmark item changed status in this refresh. The most relevant current
tracker updates are:

- `gh search issues --repo pgplex/pgschema --include-prs --updated '>=2026-10-13'`
  surfaced open issue [#644](https://github.com/pgplex/pgschema/issues/644)
  plus open PR [#643](https://github.com/pgplex/pgschema/pull/643); #643
  remains open and outside the checked-in/live head, while #644 is pgschema
  inspector / latency work rather than a new pg-delta parity gap
- the new pgschema global-state cluster rooted at
  [#627](https://github.com/pgplex/pgschema/issues/627) /
  [#637](https://github.com/pgplex/pgschema/pull/637) is not being promoted
  into new benchmark gap docs in this repo, and the new schema-diff issues
  [#638](https://github.com/pgplex/pgschema/issues/638),
  [#639](https://github.com/pgplex/pgschema/issues/639),
  [#640](https://github.com/pgplex/pgschema/issues/640), and
  [#641](https://github.com/pgplex/pgschema/issues/641) are already covered or
  avoided in current pg-delta
- `gh search issues --repo supabase/pg-toolbelt --include-prs --updated '>=2026-10-13'`
  surfaced only open PR
  [#541](https://github.com/supabase/pg-toolbelt/pull/541); it closes
  rewrite-risk issue [#530](https://github.com/supabase/pg-toolbelt/issues/530)
  but the active benchmark paths `src/extract/relations.ts`,
  `src/plan/rules/tables.ts`, `src/plan/rules/helpers.ts`, and
  `src/plan/rules/constraints.ts` remain unchanged on the checked-in/live head
- exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
  `pgschema#627`, `pgschema#638`, `pgschema#639`, `pgschema#640`,
  `pgschema#641`, and `pgschema#644` still returned `[]`; keyword
  `"PARTITION OF"` still surfaces the existing umbrella / adjacent partition
  context, while `"VIRTUAL"
  generated` and `"NOT NULL" "NOT VALID"` still surface only the historical /
  adjacent context already recorded in active benchmarks **022** and **024**
- `benchmark/review-memory.json` now adds issue
  [#644](https://github.com/pgplex/pgschema/issues/644) to the cached
  watch-list without changing any benchmark verdicts
- previously screened pgschema verdicts remain unchanged: open issue
  [#598](https://github.com/pgplex/pgschema/issues/598) remains **covered**,
  open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559),
  [#597](https://github.com/pgplex/pgschema/issues/597),
  [#623](https://github.com/pgplex/pgschema/issues/623), and
  [#644](https://github.com/pgplex/pgschema/issues/644) remain **not parity**,
  open issues [#624](https://github.com/pgplex/pgschema/issues/624),
  [#625](https://github.com/pgplex/pgschema/issues/625),
  [#626](https://github.com/pgplex/pgschema/issues/626),
  [#638](https://github.com/pgplex/pgschema/issues/638),
  [#639](https://github.com/pgplex/pgschema/issues/639),
  [#640](https://github.com/pgplex/pgschema/issues/640), and
  [#641](https://github.com/pgplex/pgschema/issues/641) remain **covered**,
  the new global-state cluster [#627](https://github.com/pgplex/pgschema/issues/627)
  through [#636](https://github.com/pgplex/pgschema/issues/636) is still
  treated as **not added as a benchmark parity gap in this repo**, and active
  resolved benchmarks [#499](https://github.com/pgplex/pgschema/issues/499),
  [#501](https://github.com/pgplex/pgschema/issues/501), and
  [#564](https://github.com/pgplex/pgschema/issues/564) remain **tracked** /
  **tracked** / **not covered** respectively
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

## Upstream watch list

- checked-in/live `pgschema` still sits at
  `2bb3352d40c5fc55c3c43abcce395dd11cd22450`; the updated-since
  `--include-prs` query for `>=2026-10-13` surfaced open issue
  [#644](https://github.com/pgplex/pgschema/issues/644) plus open PR
  [#643](https://github.com/pgplex/pgschema/pull/643), but #643 is still
  outside the checked-in/live head and #644 is pgschema-side inspector /
  latency work rather than a new schema-diff parity gap
- checked-in/live `pg-toolbelt` still sits at
  `0abee28a54bd855c13d45e2d7ebb5cb647b46693`; the updated-since
  `--include-prs` query for `>=2026-10-13` surfaced only open PR
  [#541](https://github.com/supabase/pg-toolbelt/pull/541), which touches
  `src/proof/prove.ts` plus corpus data rather than the active gap files
- the nearby benchmark-relevant pg-toolbelt issue/PR landscape remains
  unchanged at the exact-gap level, and so does the parity mapping:
  - open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still points at benchmarks **021** / **022**; exact searches for
    `pgschema#499` and `pgschema#501` still return no dedicated issue or PR
  - open issues [#502](https://github.com/supabase/pg-toolbelt/issues/502)
    and [#530](https://github.com/supabase/pg-toolbelt/issues/530) remain the
    adjacent partition follow-up / rewrite-risk context for benchmark **021**,
    and open PR [#541](https://github.com/supabase/pg-toolbelt/pull/541) now
    proposes the fix for #530; keyword `"PARTITION OF"` searches now also surface merged PRs
    [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    [#503](https://github.com/supabase/pg-toolbelt/pull/503),
    [#504](https://github.com/supabase/pg-toolbelt/pull/504),
    [#470](https://github.com/supabase/pg-toolbelt/pull/470),
    [#383](https://github.com/supabase/pg-toolbelt/pull/383), and
    [#514](https://github.com/supabase/pg-toolbelt/pull/514); #541 fixes the
    rewrite-risk declaration bug but is still adjacent partition / proof work
    rather than an exact child-local override fix
  - historical PR [#174](https://github.com/supabase/pg-toolbelt/pull/174)
    remains legacy-engine-only context for benchmark **024**; exact
    `pgschema#564` searches still return no current pg-toolbelt issue or PR,
    while keyword `"NOT NULL" "NOT VALID"` now still surfaces merged PR
    [#484](https://github.com/supabase/pg-toolbelt/pull/484); umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains broader
    adjacent context rather than an exact tracker for that workflow
  - new open pgschema issues
    [#638](https://github.com/pgplex/pgschema/issues/638),
    [#639](https://github.com/pgplex/pgschema/issues/639),
    [#640](https://github.com/pgplex/pgschema/issues/640),
    [#641](https://github.com/pgplex/pgschema/issues/641), and
    [#644](https://github.com/pgplex/pgschema/issues/644) have no dedicated
    pg-toolbelt issue or PR because current pg-delta already renders column
    grants correctly, models partition attachment / bounds, includes
    partitioned tables in ACL extraction, executes concurrent-index SQL
    directly without a name-based wait loop, and avoids #644's FK-order
    sub-bug with `unnest(con.conkey) WITH ORDINALITY`
  - the broader global-state cluster rooted at
    [#627](https://github.com/pgplex/pgschema/issues/627) plus PR
    [#637](https://github.com/pgplex/pgschema/pull/637) is not being promoted
    into new benchmark gap docs in this repo; adjacent pg-delta owner / role
    work exists in open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471)
    and [#493](https://github.com/supabase/pg-toolbelt/pull/493) plus merged
    role / membership fixes [#117](https://github.com/supabase/pg-toolbelt/pull/117),
    [#118](https://github.com/supabase/pg-toolbelt/pull/118), and
    [#461](https://github.com/supabase/pg-toolbelt/pull/461)
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
