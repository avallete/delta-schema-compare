# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-10-20)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `7931d4167c18c9d849a4ea5737dfcc13f09e36aa`
- checked-in/live `repos/pgschema` @ `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`

> The 2026-10-20 refresh advances checked-in/live `repos/pg-toolbelt` from
> `0abee28a54bd855c13d45e2d7ebb5cb647b46693` to `7931d4167c18c9d849a4ea5737dfcc13f09e36aa` through merged PR
> [#541](https://github.com/supabase/pg-toolbelt/pull/541), while
> checked-in/live `repos/pgschema` stays at `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`.
>
> - `gh search issues --repo pgplex/pgschema --state open --updated '>=2026-10-19'`
>   returned `[]`
> - `gh search issues --repo pgplex/pgschema --state closed --updated '>=2026-10-19'`
>   returned `[]`
> - `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-19'`
>   returned `[]`
> - older open PR [#662](https://github.com/pgplex/pgschema/pull/662)
>   remains watch-only upstream context for `MATCH FULL` foreign keys: exact
>   duplicate searches for `"MATCH FULL"` and `confmatchtype` still returned no
>   pg-toolbelt issue or PR, and current pg-delta still appears to preserve the
>   clause via verbatim `pg_get_constraintdef(con.oid)` extraction plus verbatim
>   `def` replay, but the current tree still lacks a dedicated scenario test
> - `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-19'`
>   surfaced open issues
>   [#339](https://github.com/supabase/pg-toolbelt/issues/339),
>   [#476](https://github.com/supabase/pg-toolbelt/issues/476),
>   [#525](https://github.com/supabase/pg-toolbelt/issues/525),
>   [#543](https://github.com/supabase/pg-toolbelt/issues/543), and
>   [#544](https://github.com/supabase/pg-toolbelt/issues/544)
> - `gh search prs --repo supabase/pg-toolbelt --state open --updated '>=2026-10-19'`
>   surfaced open PRs
>   [#506](https://github.com/supabase/pg-toolbelt/pull/506),
>   [#546](https://github.com/supabase/pg-toolbelt/pull/546),
>   [#547](https://github.com/supabase/pg-toolbelt/pull/547),
>   [#548](https://github.com/supabase/pg-toolbelt/pull/548), and
>   [#549](https://github.com/supabase/pg-toolbelt/pull/549)
> - `gh search prs --repo supabase/pg-toolbelt --merged --updated '>=2026-10-19'`
>   surfaced merged PR
>   [#541](https://github.com/supabase/pg-toolbelt/pull/541) only
> - PR [#541](https://github.com/supabase/pg-toolbelt/pull/541) closes
>   rewrite-risk issue [#530](https://github.com/supabase/pg-toolbelt/issues/530)
>   and is now in the checked-in/live head, but it only touches
>   `packages/pg-delta/src/proof/prove.ts` plus new inherited-rewrite corpus
>   cases; benchmark **021** still hinges on `a.attislocal` plus bare
>   `PARTITION OF ... ${bound}` rendering
> - open issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus
>   open PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) are now the
>   exact tracker / fix-in-progress path for benchmark **025** /
>   [#534](https://github.com/pgplex/pgschema/issues/534)
> - pg-toolbelt issue [#544](https://github.com/supabase/pg-toolbelt/issues/544)
>   still has no matching pgschema counterpart from the current `BETWEEN` /
>   `nested AND` keyword sweeps, and issue
>   [#525](https://github.com/supabase/pg-toolbelt/issues/525) still has no
>   matching pgschema counterpart from the `union alias` / `?column?` sweeps
> - issue [#476](https://github.com/supabase/pg-toolbelt/issues/476) plus open
>   PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) and issue
>   [#339](https://github.com/supabase/pg-toolbelt/issues/339) plus open PR
>   [#549](https://github.com/supabase/pg-toolbelt/pull/549) are adjacent
>   pg-delta global-state / role-management work; current pgschema keyword
>   sweeps still only land on the broader
>   [#627](https://github.com/pgplex/pgschema/issues/627) umbrella, which this
>   repo continues to treat as non-benchmark parity scope
> - direct source rechecks show the existing active gap paths remain unchanged:
>   benchmark **022** still collapses generated kind to `generatedExpr` plus
>   hard-coded `... STORED`, benchmark **024** still keeps PG18 `contype = 'n'`
>   rows out of diff-visible facts while planning plain `SET NOT NULL`, and
>   benchmark **025** still folds the self-referencing FK inline before its
>   backing same-table UNIQUE index exists on the checked-in/live head
> - `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
>   still returned `[]`
> - `benchmark/review-memory.json` needs fingerprint updates today because the
>   checked-in/live pg-delta head advanced even though the pgschema issue set
>   stayed fixed
>
> The active benchmarked gap set remains **021**, **022**, **024**, and
> **025**, and there is still **no open uncovered parity candidate** on the
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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread), adjacent [#530](https://github.com/supabase/pg-toolbelt/issues/530) (closed rewrite-risk precursor) | merged [#541](https://github.com/supabase/pg-toolbelt/pull/541) (rewrite-risk declarations only), adjacent [#470](https://github.com/supabase/pg-toolbelt/pull/470), [#480](https://github.com/supabase/pg-toolbelt/pull/480), and [#488](https://github.com/supabase/pg-toolbelt/pull/488) (merged), [#501](https://github.com/supabase/pg-toolbelt/pull/501) (merged partition-key retype), and [#504](https://github.com/supabase/pg-toolbelt/pull/504) (merged dependency-edge repair) | **Tracked (umbrella thread only)** |
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |
| 024 | [PG18 native NOT NULL validation](024-pg18-not-null-validation.md) | [#564](https://github.com/pgplex/pgschema/issues/564) | none found | historical [#174](https://github.com/supabase/pg-toolbelt/pull/174) (merged, legacy engine only), adjacent [#484](https://github.com/supabase/pg-toolbelt/pull/484) and [#485](https://github.com/supabase/pg-toolbelt/pull/485) (merged) | **Not covered** |
| 025 | [Self-referencing FK to non-PK UNIQUE key](025-self-referencing-fk-nonpk-unique-ordering.md) | [#534](https://github.com/pgplex/pgschema/issues/534) | [#543](https://github.com/supabase/pg-toolbelt/issues/543) (open) | open [#546](https://github.com/supabase/pg-toolbelt/pull/546) (exact fix in progress) | **Tracked (open issue + PR)** |

> Historical benchmark files are retained even after pg-delta fixes land.
> The status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Four resolved-issue benchmark scenarios remain active as unresolved behavior:

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
    closed rewrite-risk issue [#530](https://github.com/supabase/pg-toolbelt/issues/530),
    merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541),
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
  - the 2026-10-20 pg-delta delta only touches `src/proof/prove.ts` plus
    new inherited-rewrite corpus cases; it does not touch
    `src/extract/relations.ts` or `src/plan/rules/helpers.ts`, so umbrella
    issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains
    the only live tracker context
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
  - the 2026-10-20 pg-delta delta only touches `src/proof/prove.ts` plus
    new inherited-rewrite corpus cases; it does not touch
    `src/extract/relations.ts` or `src/plan/rules/tables.ts`, and there is
    still no exact current pg-toolbelt issue or PR for this benchmark
- **025** - self-referencing FK to a same-table non-PK UNIQUE key on the
  declarative export path
  - `repos/pg-toolbelt/packages/pg-delta/src/frontends/export-sql-files.ts`
    still makes `cyclicForeignKeys()` skip genuine self-references, so they
    remain eligible for inline folding instead of being routed to a later
    sibling `.fk.sql` file
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/constraints.ts` plus
    `repos/pg-toolbelt/packages/pg-delta/src/plan/internal.ts` still let
    validated FOREIGN KEY constraints fold inline during `schema export`
  - open issue [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus
    open PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) now form
    the exact tracker / fix-in-progress path for the self-referencing
    unique-index export failure, while
    `repos/pg-toolbelt/packages/pg-delta/tests/load-sql-files-reorder-on-failure.test.ts`
    still proves the loader cannot repair same-file statement order on the
    checked-in/live head

Because today's refresh advances only checked-in/live `pg-delta` from
`0abee28a54bd855c13d45e2d7ebb5cb647b46693` to
`7931d4167c18c9d849a4ea5737dfcc13f09e36aa` through merged PR
[#541](https://github.com/supabase/pg-toolbelt/pull/541), while the pgschema
open-issue, closed-issue, and open-PR updated-since queries all returned `[]`,
the active benchmark set stays stable at **021** / **022** / **024** / **025**.
Benchmarks **021** / **022** / **024** remain unchanged on the current heads:
PR [#541](https://github.com/supabase/pg-toolbelt/pull/541) merged adjacent
proof-declaration work but still leaves benchmark **021**'s extract / plan gap
untouched, and the `0abee28...7931d416` delta never touches the benchmark
**022** / **024** files where generated kind and PG18 native `NOT NULL`
validation remain unmodeled. Benchmark **025** likewise remains tracked rather
than solved because open issue
[#543](https://github.com/supabase/pg-toolbelt/issues/543) now has an exact
open fix PR [#546](https://github.com/supabase/pg-toolbelt/pull/546), but the
checked-in/live head still keeps genuine self-references inline in
`src/frontends/export-sql-files.ts`, still folds validated FKs inline during
export in `src/plan/rules/constraints.ts` and `src/plan/internal.ts`, and the
loader still cannot repair same-file order once the FK and its backing unique
index land together. PR [#662](https://github.com/pgplex/pgschema/pull/662)
remains watch-only because pg-delta still appears to preserve `MATCH FULL`
through verbatim constraint-definition extraction and replay, but no dedicated
scenario test or linked tracker exists yet. New pg-toolbelt issues
[#525](https://github.com/supabase/pg-toolbelt/issues/525) and
[#544](https://github.com/supabase/pg-toolbelt/issues/544) plus policy /
global-state PRs [#506](https://github.com/supabase/pg-toolbelt/pull/506),
[#548](https://github.com/supabase/pg-toolbelt/pull/548), and
[#549](https://github.com/supabase/pg-toolbelt/pull/549) add unmatched or
adjacent pg-toolbelt-side context only; they do not map to active pgschema
benchmark items from today's keyword sweeps. Exact duplicate searches for
`pgschema#499`, `pgschema#501`, `pgschema#564`, `pgschema#534`, and
`pgschema#653` still return no dedicated pg-toolbelt issue or PR, so umbrella
issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) still only
covers benchmarks **021** / **022** and benchmark **024** still has no exact
current pg-toolbelt issue or PR. There is still **no open uncovered parity
candidate** on the pgschema side.

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
[#598](https://github.com/pgplex/pgschema/issues/598),
[#624](https://github.com/pgplex/pgschema/issues/624),
[#625](https://github.com/pgplex/pgschema/issues/625),
[#626](https://github.com/pgplex/pgschema/issues/626),
[#627](https://github.com/pgplex/pgschema/issues/627),
[#638](https://github.com/pgplex/pgschema/issues/638),
[#639](https://github.com/pgplex/pgschema/issues/639), and
[#653](https://github.com/pgplex/pgschema/issues/653).

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
- **#624** SQL function created before `ADD COLUMN` it depends on - **covered**
  in current pg-delta via the routine-plan `check_function_bodies = off`
  preamble plus existing SQL-body forward-reference coverage
- **#625** existing composite-type attribute changes are silently skipped -
  **covered** in current pg-delta via composite `typeAttribute` facts and
  `ALTER TYPE ... ADD ATTRIBUTE ... CASCADE` planning
- **#626** composite type creation runs before its required table - **covered**
  in current pg-delta via dependency extraction that resolves composite row-type
  edges back onto the owning table fact
- **#627** opt-in global-state roles / ownership umbrella (plus open PR
  [#637](https://github.com/pgplex/pgschema/pull/637), which now closes child
  issues **#628-#636**) - **not added as a new benchmark parity item in this
  repo**. This remains pgschema's separate explicit global-manifest surface;
  adjacent pg-delta role / owner work exists in open PRs
  [#471](https://github.com/supabase/pg-toolbelt/pull/471) and
  [#493](https://github.com/supabase/pg-toolbelt/pull/493) plus merged
  membership fixes [#117](https://github.com/supabase/pg-toolbelt/pull/117),
  [#118](https://github.com/supabase/pg-toolbelt/pull/118), and
  [#461](https://github.com/supabase/pg-toolbelt/pull/461), but exact duplicate
  search `pgschema#627` still returns no dedicated pg-toolbelt issue or PR
- **#638** mixed column-privilege rendering (`GRANT INSERT, UPDATE (cols)`) -
  **covered** in current pg-delta, and open PR
  [#661](https://github.com/pgplex/pgschema/pull/661) is upstream catch-up:
  - `renderGrantSql()` renders column privileges as `PRIV (col), PRIV (col)`
  - `tests/column-grant-fidelity.test.ts` covers extracted table column grants
  - `src/frontends/sql-format/format-grant.test.ts` explicitly pins
    `GRANT SELECT (col), UPDATE (col) ...`
- **#639** partition bounds / attachment drift - **covered** in current
  pg-delta, and open PR [#660](https://github.com/pgplex/pgschema/pull/660) is
  upstream catch-up rather than a new parity gap:
  - extracted table facts preserve `partitionBound` and `parentTable`
  - `src/plan/rules/tables.ts` treats both attributes as `"replace"`
  - corpuses `table-ops--attach-partition` and `table-ops--detach-partition`
    cover attach / detach state changes
- **#653** inherited partition-index name collisions during dump replay -
  **covered / avoided** in current pg-delta:
  - `src/plan/rules/tables.ts` makes child `PARTITION OF` creation consume
    parent indexes plus parent PRIMARY KEY / UNIQUE constraints, so the
    standalone parent index exists before the child partition is created
  - `src/plan/partition-index-attach.test.ts` already covers child
    `CREATE INDEX` + `ATTACH PARTITION` plus parent-index rename / replacement
    behavior

There is currently **no open uncovered parity candidate** on the pgschema
side. The remaining active benchmarks **021** / **022** still only have
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) as
exact tracker context, benchmark **024** still has no exact current
pg-toolbelt issue or PR, open issue
[#639](https://github.com/pgplex/pgschema/issues/639) plus open PR
[#660](https://github.com/pgplex/pgschema/pull/660) remain covered upstream
catch-up, new issue [#653](https://github.com/pgplex/pgschema/issues/653) plus
open PR [#645](https://github.com/pgplex/pgschema/pull/645) is covered /
avoided rather than a new pg-delta gap, the broader global-state umbrella
[#627](https://github.com/pgplex/pgschema/issues/627) /
[#637](https://github.com/pgplex/pgschema/pull/637) still is not being
promoted into a benchmark gap here, and this repository still has no local
tracker issues.

## Recent closed-issue / tracker updates

No benchmark verdict changed in this refresh. The most relevant current tracker
updates are:

- pgschema issue [#534](https://github.com/pgplex/pgschema/issues/534) /
  merged PR [#540](https://github.com/pgplex/pgschema/pull/540) stays mapped
  to benchmark [025](025-self-referencing-fk-nonpk-unique-ordering.md) and
  open pg-toolbelt issue [#543](https://github.com/supabase/pg-toolbelt/issues/543)
  plus open fix PR [#546](https://github.com/supabase/pg-toolbelt/pull/546)
- the active benchmarked pg-toolbelt trackers are unchanged at the verdict
  level:
  - open umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still covers benchmarks **021** / **022**
  - closed issue [#530](https://github.com/supabase/pg-toolbelt/issues/530)
    and merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541)
    remain adjacent partition rewrite-risk context for benchmark **021**, but
    they do not touch `src/extract/relations.ts` or
    `src/plan/rules/tables.ts`
  - open issue [#543](https://github.com/supabase/pg-toolbelt/issues/543)
    plus open PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) are
    the exact tracker / fix-in-progress pair for benchmark **025**
- pg-toolbelt issue [#525](https://github.com/supabase/pg-toolbelt/issues/525)
  still has no matching pgschema counterpart from today's `union alias` /
  `?column?` keyword search, so it does not create a new benchmark item in this
  repo
- pg-toolbelt issue [#544](https://github.com/supabase/pg-toolbelt/issues/544)
  still has no matching pgschema counterpart from today's `BETWEEN` /
  `nested AND` keyword search, so it does not create a new benchmark item in
  this repo
- pg-toolbelt issue [#476](https://github.com/supabase/pg-toolbelt/issues/476)
  plus open PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) and
  pg-toolbelt issue [#339](https://github.com/supabase/pg-toolbelt/issues/339)
  plus open PR [#549](https://github.com/supabase/pg-toolbelt/pull/549) are
  adjacent role / global-state work; today's pgschema keyword sweeps still only
  land on umbrella issue [#627](https://github.com/pgplex/pgschema/issues/627),
  which this repo continues to exclude from benchmark promotion
- open PR [#506](https://github.com/supabase/pg-toolbelt/pull/506) remains
  unmatched policy-withheld-prerequisite context and does not map to a current
  pgschema benchmark item
- pgschema PR [#662](https://github.com/pgplex/pgschema/pull/662)
  (`MATCH FULL` foreign keys) remains watch-only upstream context even though
  the updated-since open-PR query returned `[]`: exact duplicate searches still
  found no linked pgschema issue or pg-toolbelt issue / PR, and pg-delta still
  appears to preserve the clause through verbatim
  `pg_get_constraintdef` extraction and verbatim `def` replay, but the current
  tree still lacks a dedicated scenario test
- exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
  `pgschema#534`, and `pgschema#653` still returned `[]`; keyword
  `"PARTITION OF"`, `"VIRTUAL" generated`, `"NOT NULL" "NOT VALID"`,
  `union alias`, `BETWEEN`, `nested AND`, `inherited partition index`, and the
  self-referencing unique-index search still only surface the existing active
  tracker context or unmatched watch-only notes already recorded in this repo
- label-filtered dry-run `compare_issues.py` / `compare_resolved.py` still
  returned **0 open** and **0 resolved** issues, so manual unlabeled sweeps
  remain required
- previously screened pgschema verdicts remain unchanged at the parity level:
  open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559), and
  [#597](https://github.com/pgplex/pgschema/issues/597) remain **not parity**;
  open issues [#598](https://github.com/pgplex/pgschema/issues/598),
  [#624](https://github.com/pgplex/pgschema/issues/624),
  [#625](https://github.com/pgplex/pgschema/issues/625),
  [#626](https://github.com/pgplex/pgschema/issues/626),
  [#638](https://github.com/pgplex/pgschema/issues/638),
  [#639](https://github.com/pgplex/pgschema/issues/639), and
  [#653](https://github.com/pgplex/pgschema/issues/653) remain **covered**;
  the narrowed global-state umbrella [#627](https://github.com/pgplex/pgschema/issues/627)
  plus closed child issues **#628-#636** is still treated as **not added as a
  benchmark parity gap in this repo**; active resolved benchmarks
  [#499](https://github.com/pgplex/pgschema/issues/499),
  [#501](https://github.com/pgplex/pgschema/issues/501),
  [#534](https://github.com/pgplex/pgschema/issues/534), and
  [#564](https://github.com/pgplex/pgschema/issues/564) remain
  **tracked** / **tracked** / **tracked** / **not covered** respectively
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

## Upstream watch list

- checked-in/live `pgschema` still sits at
  `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`; the updated-since open-issue,
  closed-issue, and open-PR queries for `>=2026-10-19` all returned `[]`.
  Open PR [#645](https://github.com/pgplex/pgschema/pull/645) remains the
  implementation thread for covered issue
  [#653](https://github.com/pgplex/pgschema/issues/653), not a new benchmark
  gap. Open PR [#662](https://github.com/pgplex/pgschema/pull/662) remains
  watch-only `MATCH FULL` context even though it did not move in today's
  updated-since sweep. Open PR [#660](https://github.com/pgplex/pgschema/pull/660)
  and open PR [#661](https://github.com/pgplex/pgschema/pull/661) remain
  covered / adjacent context already reflected in prior refreshes
- checked-in/live `pg-toolbelt` now sits at
  `7931d4167c18c9d849a4ea5737dfcc13f09e36aa`; the updated-since queries for `>=2026-10-19`
  surfaced open issues
  [#339](https://github.com/supabase/pg-toolbelt/issues/339),
  [#476](https://github.com/supabase/pg-toolbelt/issues/476),
  [#525](https://github.com/supabase/pg-toolbelt/issues/525),
  [#543](https://github.com/supabase/pg-toolbelt/issues/543), and
  [#544](https://github.com/supabase/pg-toolbelt/issues/544), open PRs
  [#506](https://github.com/supabase/pg-toolbelt/pull/506),
  [#546](https://github.com/supabase/pg-toolbelt/pull/546),
  [#547](https://github.com/supabase/pg-toolbelt/pull/547),
  [#548](https://github.com/supabase/pg-toolbelt/pull/548), and
  [#549](https://github.com/supabase/pg-toolbelt/pull/549), plus merged PR
  [#541](https://github.com/supabase/pg-toolbelt/pull/541)
- the nearby benchmark-relevant pg-toolbelt issue / PR landscape therefore now
  reads:
  - open issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still points at benchmarks **021** / **022**; exact searches for
    `pgschema#499` and `pgschema#501` still return no dedicated issue or PR
  - open issue [#502](https://github.com/supabase/pg-toolbelt/issues/502)
    plus closed issue [#530](https://github.com/supabase/pg-toolbelt/issues/530)
    and merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541)
    remain adjacent partition follow-up / rewrite-risk context for benchmark
    **021**; none of them changes child-local `PARTITION OF` column-element
    modeling
  - open issue [#543](https://github.com/supabase/pg-toolbelt/issues/543)
    plus open PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) are
    the exact current tracker / fix-in-progress path for benchmark **025** /
    pgschema [#534](https://github.com/pgplex/pgschema/issues/534), even though
    an exact `pgschema#534` text search still returns no dedicated issue or PR
  - issue [#525](https://github.com/supabase/pg-toolbelt/issues/525) remains
    unmatched upstream context; today's `union alias` / `?column?` search on
    pgschema returned `[]`
  - issue [#544](https://github.com/supabase/pg-toolbelt/issues/544) remains
    unmatched upstream context; today's `BETWEEN` / `nested AND` searches on
    pgschema returned `[]`
  - issue [#476](https://github.com/supabase/pg-toolbelt/issues/476) plus open
    PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) and issue
    [#339](https://github.com/supabase/pg-toolbelt/issues/339) plus open PR
    [#549](https://github.com/supabase/pg-toolbelt/pull/549) are adjacent role
    / user-mapping context around explicit global-state management; current
    pgschema keyword searches still only land on
    [#627](https://github.com/pgplex/pgschema/issues/627) and do not change the
    repo's benchmark scope
  - open PR [#506](https://github.com/supabase/pg-toolbelt/pull/506) remains
    unmatched policy-suppression context; today's pgschema keyword sweeps still
    found no counterpart
  - exact `"MATCH FULL"` / `confmatchtype` duplicate searches still return no
    pg-toolbelt issue or PR that maps to pgschema PR #662; current pg-delta
    source likely preserves the clause already, but the test gap keeps that
    scenario in watch-only status for now
  - exact `pgschema#653` and `inherited partition index` searches still return
    no pg-toolbelt issue or PR; current pg-delta still appears to avoid the
    collision through partition-index attach planning and child `PARTITION OF`
    create ordering
  - historical PR [#174](https://github.com/supabase/pg-toolbelt/pull/174)
    remains legacy-engine-only context for benchmark **024**; exact
    `pgschema#564` searches still return no current pg-toolbelt issue or PR
  - the broader global-state cluster is still centered on open umbrella issue
    [#627](https://github.com/pgplex/pgschema/issues/627) plus PR
    [#637](https://github.com/pgplex/pgschema/pull/637) after issues
    **#628-#636** closed; it is still not being promoted into new benchmark
    gap docs in this repo. Adjacent pg-delta global-state work now also
    includes issue [#476](https://github.com/supabase/pg-toolbelt/issues/476)
    / PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) and issue
    [#339](https://github.com/supabase/pg-toolbelt/issues/339) / PR
    [#549](https://github.com/supabase/pg-toolbelt/pull/549) alongside open
    PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471) and
    [#493](https://github.com/supabase/pg-toolbelt/pull/493) plus merged role /
    membership fixes [#117](https://github.com/supabase/pg-toolbelt/pull/117),
    [#118](https://github.com/supabase/pg-toolbelt/pull/118), and
    [#461](https://github.com/supabase/pg-toolbelt/pull/461)
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
