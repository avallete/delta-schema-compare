# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-10-24)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `6b82eff84dba925a176f0c6a78e5a16843885366`
- checked-in/live `repos/pgschema` @ `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`

> The 2026-10-24 refresh advances checked-in/live `repos/pg-toolbelt` from
> `265af521e462577886ea6fdbb5777e1a23811cce` to `6b82eff84dba925a176f0c6a78e5a16843885366`
> through merged PR [#559](https://github.com/supabase/pg-toolbelt/pull/559),
> while checked-in/live `repos/pgschema` stays at
> `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`. The only file in that range is
> `.github/CODEOWNERS`. `packages/pg-delta` is unchanged, so no benchmark
> verdict changes today.
>
> - `gh search issues --repo pgplex/pgschema --state open --updated '>=2026-10-23'`
>   returned `[]`
> - `gh search issues --repo pgplex/pgschema --state closed --updated '>=2026-10-23'`
>   returned `[]`
> - `gh search prs --repo pgplex/pgschema --state open --updated '>=2026-10-23'`
>   surfaced open PR [#645](https://github.com/pgplex/pgschema/pull/645)
>   (`updatedAt` `2026-10-23T10:28:25Z`). The update is a review comment
>   ("it would be nice to have it asap"); the latest commit is still
>   `6a620735` from 2026-10-16. It remains the implementation thread for
>   covered issue [#653](https://github.com/pgplex/pgschema/issues/653)
> - `gh search prs --repo pgplex/pgschema --merged --updated '>=2026-10-23'`
>   returned `[]`
> - the live open pgschema issue set is unchanged:
>   **#49 / #52 / #84 / #559 / #597 / #598 / #624 / #625 / #626 / #627 / #638 /
>   #639 / #653**
> - older open PR [#662](https://github.com/pgplex/pgschema/pull/662)
>   (`updatedAt` `2026-10-17T15:35:33Z`) remains watch-only upstream context for
>   `MATCH FULL` foreign keys: exact duplicate searches for `"MATCH FULL"` and
>   `confmatchtype` still returned no pg-toolbelt issue or PR, and current
>   pg-delta still preserves the clause via verbatim
>   `pg_get_constraintdef(con.oid)` extraction plus verbatim `def` replay.
>   The current tree still lacks a dedicated scenario test
> - `gh search issues --repo supabase/pg-toolbelt --state open --updated '>=2026-10-23'`
>   returned `[]`. Direct views keep issues
>   [#332](https://github.com/supabase/pg-toolbelt/issues/332),
>   [#518](https://github.com/supabase/pg-toolbelt/issues/518)
>   (`updatedAt` `2026-10-20T13:17:30Z`), and
>   [#554](https://github.com/supabase/pg-toolbelt/issues/554)
>   (`updatedAt` `2026-10-21T15:42:52Z`) open
> - `gh search issues --repo supabase/pg-toolbelt --state closed --updated '>=2026-10-23'`
>   returned `[]`
> - `gh search prs --repo supabase/pg-toolbelt --state open --updated '>=2026-10-23'`
>   returned `[]`. Direct views keep open PRs
>   [#471](https://github.com/supabase/pg-toolbelt/pull/471),
>   [#493](https://github.com/supabase/pg-toolbelt/pull/493),
>   [#506](https://github.com/supabase/pg-toolbelt/pull/506),
>   [#548](https://github.com/supabase/pg-toolbelt/pull/548),
>   [#555](https://github.com/supabase/pg-toolbelt/pull/555), and
>   [#558](https://github.com/supabase/pg-toolbelt/pull/558) at their
>   2026-10-22 `updatedAt` values
> - `gh search prs --repo supabase/pg-toolbelt --merged --updated '>=2026-10-23'`
>   surfaced merged PR [#559](https://github.com/supabase/pg-toolbelt/pull/559)
>   (`mergedAt` `2026-10-23T10:29:06Z`), which only rewrites `.github/CODEOWNERS`
> - direct source rechecks on the new head keep the active gap paths open:
>   benchmark **021** still hinges on `a.attislocal` (`relations.ts` line 189)
>   plus bare `PARTITION OF ... ${bound}` rendering (`tables.ts` line 52),
>   benchmark **022** still collapses generated kind to `generatedExpr`
>   (`relations.ts` lines 211 and 261) plus hard-coded `... STORED` in
>   `tables.ts` `columnClause()` (line 712), and benchmark **024** still keeps
>   PG18 `contype = 'n'` rows out of diff-visible facts (`relations.ts` lines
>   361-396) while planning plain `SET NOT NULL` (`tables.ts` line 449)
> - exact duplicate searches for `pgschema#499`, `pgschema#501`, `pgschema#564`,
>   `pgschema#534`, and `pgschema#653` still returned no dedicated pg-toolbelt
>   issue or PR
> - `gh issue list -R avallete/delta-schema-compare --state all --limit 50`
>   still returned `[]`
> - `benchmark/review-memory.json` fingerprints for the open watch list and
>   active resolved benchmarks **#499**, **#501**, **#534**, and **#564** were
>   refreshed because the checked-in/live pg-delta head advanced. Verdicts stay
>   the same
>
> The active benchmarked gap set remains **021**, **022**, and **024**.
> Benchmark **025** stays **Solved in pg-delta**. There is still **no open
> uncovered parity candidate** on the pgschema side.

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
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | adjacent [#553](https://github.com/supabase/pg-toolbelt/pull/553) (merged generated-column fold order only) and [#556](https://github.com/supabase/pg-toolbelt/pull/556) (merged helper move; `columnClause()` now lives in `tables.ts` and still hard-codes `STORED`) | **Tracked (umbrella thread only)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |
| 024 | [PG18 native NOT NULL validation](024-pg18-not-null-validation.md) | [#564](https://github.com/pgplex/pgschema/issues/564) | none found | historical [#174](https://github.com/supabase/pg-toolbelt/pull/174) (merged, legacy engine only), adjacent [#484](https://github.com/supabase/pg-toolbelt/pull/484) and [#485](https://github.com/supabase/pg-toolbelt/pull/485) (merged) | **Not covered** |
| 025 | [Self-referencing FK to non-PK UNIQUE key](025-self-referencing-fk-nonpk-unique-ordering.md) | [#534](https://github.com/pgplex/pgschema/issues/534) | [#543](https://github.com/supabase/pg-toolbelt/issues/543) (closed) | merged [#546](https://github.com/supabase/pg-toolbelt/pull/546) (exact fix) | **Solved in pg-delta** |

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
    closed rewrite-risk issue [#530](https://github.com/supabase/pg-toolbelt/issues/530),
    merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541),
    merged PR [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    merged stacked PR [#503](https://github.com/supabase/pg-toolbelt/pull/503),
    and merged PR [#504](https://github.com/supabase/pg-toolbelt/pull/504)
    sharpen nearby partition-key / rewrite-risk / dependency-edge behavior.
    Merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553) edits
    `src/plan/rules/tables.ts` for generated-column fold hints only. Merged PR
    [#550](https://github.com/supabase/pg-toolbelt/pull/550) now restores a
    non-subpartitioned child's own index storage options after
    `PARTITION OF`, and records further `INHERITS` parents as
    `inheritsAlso`. The partition-child create path and `a.attislocal` filter
    stay as they were
  - umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    remains the only exact tracker context
- **022** - PostgreSQL 18 `VIRTUAL` generated columns
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    collapses `attgenerated` to generated-expression presence instead of
    preserving `VIRTUAL` versus `STORED`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts`
    `columnClause()` hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`. Merged PR
    [#556](https://github.com/supabase/pg-toolbelt/pull/556) moved that helper
    out of `src/plan/rules/helpers.ts` without changing the keyword
  - merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553) still
    folds generated columns into `CREATE TABLE` through the same
    `columnClause()` helper, so the hard-coded `STORED` keyword also
    appears on the inline create path. Umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
    only live tracker context for the kind distinction
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
  - the 2026-10-23 pg-delta delta from
    `63b3f653d99f936fa40c5a7689d771e829f09f45` to
    `265af521e462577886ea6fdbb5777e1a23811cce` changes export round-trip
    fidelity, helper placement, apply error text, and shadow-load durability.
    It still lands no exact current pg-toolbelt issue or PR for this benchmark.
    Today's follow-on commit `6b82eff8` edits only `.github/CODEOWNERS`

Because today's refresh advances checked-in/live `pg-delta` from
`265af521e462577886ea6fdbb5777e1a23811cce` to
`6b82eff84dba925a176f0c6a78e5a16843885366` through merged PR
[#559](https://github.com/supabase/pg-toolbelt/pull/559), and that commit
edits only `.github/CODEOWNERS`, the active benchmark set stays **021** /
**022** / **024**. The pgschema open-issue, closed-issue, and merged-PR
updated-since queries for `>=2026-10-23` returned `[]`. The only open PR in
that window is [#645](https://github.com/pgplex/pgschema/pull/645), which
gained a comment and no new commits. Merged PRs
[#550](https://github.com/supabase/pg-toolbelt/pull/550) and
[#556](https://github.com/supabase/pg-toolbelt/pull/556) remain in history:
the first fixes multi-parent `INHERITS`, partition-child index storage
options, and row-type `CHECK` folding, and the second moves `columnClause()`
into `tables.ts` while still appending `STORED`. Those changes leave the
`VIRTUAL` versus `STORED` distinction, the partition-child column-element
path, and the PG18 `NOT NULL ... NOT VALID` workflow open. Benchmark **025**
stays solved from merged PR
[#546](https://github.com/supabase/pg-toolbelt/pull/546); the same-table fold
guard in `src/plan/internal.ts` is unchanged on this head. PR
[#662](https://github.com/pgplex/pgschema/pull/662) remains watch-only because
pg-delta preserves `MATCH FULL` through verbatim constraint-definition
extraction and replay, with no dedicated scenario test or linked tracker yet.
Open issue [#518](https://github.com/supabase/pg-toolbelt/issues/518) stays
open after partial coverage from merged PR
[#553](https://github.com/supabase/pg-toolbelt/pull/553); open follow-up
[#554](https://github.com/supabase/pg-toolbelt/issues/554) and open PR
[#555](https://github.com/supabase/pg-toolbelt/pull/555) are unmatched
pg-toolbelt-side context and did not move in today's window. Exact duplicate
searches for `pgschema#499`, `pgschema#501`, `pgschema#564`, and
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
pg-toolbelt issue or PR, benchmark
[#534](https://github.com/pgplex/pgschema/issues/534) now moves to **covered**
through merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546) on
the checked-in/live head, open issue
[#639](https://github.com/pgplex/pgschema/issues/639) plus open PR
[#660](https://github.com/pgplex/pgschema/pull/660) remain covered upstream
catch-up, open issue [#653](https://github.com/pgplex/pgschema/issues/653)
plus open PR [#645](https://github.com/pgplex/pgschema/pull/645) is covered /
avoided rather than a new pg-delta gap, the broader global-state umbrella
[#627](https://github.com/pgplex/pgschema/issues/627) /
[#637](https://github.com/pgplex/pgschema/pull/637) still is not being
promoted into a benchmark gap here, open issue
[#518](https://github.com/supabase/pg-toolbelt/issues/518) stays open after
partial coverage from merged PR
[#553](https://github.com/supabase/pg-toolbelt/pull/553), open follow-up
[#554](https://github.com/supabase/pg-toolbelt/issues/554) and open PR
[#555](https://github.com/supabase/pg-toolbelt/pull/555) remain unmatched
pg-toolbelt-side context, merged PR
[#550](https://github.com/supabase/pg-toolbelt/pull/550) is now in the
checked-in/live head as export-roundtrip fidelity work with no pgschema
counterpart, and this repository still has no local tracker issues.

## Recent closed-issue / tracker updates

No benchmark verdict changed in this refresh. Merged PR
[#559](https://github.com/supabase/pg-toolbelt/pull/559) is now in the
checked-in/live head and only rewrites `.github/CODEOWNERS`. Merged PRs
[#550](https://github.com/supabase/pg-toolbelt/pull/550),
[#551](https://github.com/supabase/pg-toolbelt/pull/551),
[#556](https://github.com/supabase/pg-toolbelt/pull/556), and
[#557](https://github.com/supabase/pg-toolbelt/pull/557) remain in that head
from the 2026-10-23 advance. Merged PR
[#553](https://github.com/supabase/pg-toolbelt/pull/553) remains the partial
coverage for open issue
[#518](https://github.com/supabase/pg-toolbelt/issues/518) on generated-column
and same-schema-type column order. The user-function `DEFAULT` case in that
issue stays open, and pgschema still has no matching column-order benchmark.
Open issue [#554](https://github.com/supabase/pg-toolbelt/issues/554) records
the remaining generated-column chain failure, and open PR
[#555](https://github.com/supabase/pg-toolbelt/pull/555) is unmatched
rename/respell settlement with new commits on 2026-10-22. The prior verdict
change that still stands is:

- pgschema issue [#534](https://github.com/pgplex/pgschema/issues/534) /
  merged PR [#540](https://github.com/pgplex/pgschema/pull/540) now moves
  benchmark [025](025-self-referencing-fk-nonpk-unique-ordering.md) to
  **Solved in pg-delta**:
  - closed pg-toolbelt issue
    [#543](https://github.com/supabase/pg-toolbelt/issues/543) plus merged PR
    [#546](https://github.com/supabase/pg-toolbelt/pull/546) are now in the
    checked-in/live head
  - `packages/pg-delta/src/plan/internal.ts` now blocks export-time inline
    folds when a same-table dependency is emitted after `CREATE TABLE`
  - `packages/pg-delta/tests/export-self-fk-on-unique-index.test.ts` now
    round-trips the exact export-reload scenario, and
    `packages/declarative-e2e/scenarios/self-fk-on-unique-index/` now covers
    the same shape through the declarative-e2e harness
- the remaining active benchmarked pg-toolbelt trackers are unchanged at the
  verdict level:
  - open umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still covers benchmarks **021** / **022**
  - closed issue [#530](https://github.com/supabase/pg-toolbelt/issues/530)
    and merged PR [#541](https://github.com/supabase/pg-toolbelt/pull/541)
    remain adjacent partition rewrite-risk context for benchmark **021**, but
    they do not touch `src/extract/relations.ts` or
    `src/plan/rules/tables.ts`
  - benchmark **024** still has no exact current pg-toolbelt issue or PR
- open issue [#518](https://github.com/supabase/pg-toolbelt/issues/518)
  remains open. Merged PR
  [#553](https://github.com/supabase/pg-toolbelt/pull/553) now covers its
  generated-column and same-schema-type order cases on the checked-in/live
  head, and open issue
  [#554](https://github.com/supabase/pg-toolbelt/issues/554) tracks the
  zero-argument `IMMUTABLE` follow-up. Today's pgschema searches for
  `generated expression column order` and `zero-arg` returned `[]`
- merged PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) is now
  in the checked-in/live head. It adds an export round-trip corpus gate plus
  three export fixes (multi-parent `INHERITS`, partition-child index storage
  options, and a row-type `CHECK` fold veto). Current pgschema keyword sweeps
  for `multi-parent`, `fillfactor`, and `row type` still find no open parity
  counterpart. One deferred corpus gap remains for sub-partition index
  options, recorded in pg-toolbelt
  `docs/roadmap/pg-delta-next-follow-ups.md`
- pg-toolbelt issues [#525](https://github.com/supabase/pg-toolbelt/issues/525)
  and [#544](https://github.com/supabase/pg-toolbelt/issues/544) still have no
  matching pgschema counterpart from the current `union alias` / `?column?` and
  `BETWEEN` / `nested AND` keyword searches
- merged PR [#549](https://github.com/supabase/pg-toolbelt/pull/549) plus open
  PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) and issues
  [#476](https://github.com/supabase/pg-toolbelt/issues/476) /
  [#339](https://github.com/supabase/pg-toolbelt/issues/339) are adjacent role
  / user-mapping work; today's pgschema keyword sweeps still only land on
  umbrella issue [#627](https://github.com/pgplex/pgschema/issues/627), which
  this repo continues to exclude from benchmark promotion
- merged PR [#551](https://github.com/supabase/pg-toolbelt/pull/551) is now
  in the checked-in/live head and remains unmatched apply/search_path context:
  apply stays on `search_path = pg_catalog` and explains `42883` failures
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
  and `pgschema#653` still returned `[]`; keyword `"PARTITION OF"`,
  `"VIRTUAL" generated`, `"NOT NULL" "NOT VALID"`, `union alias`,
  `BETWEEN`, `nested AND`, `inherited partition index`, and the export
  column-order search terms still only surface the existing active tracker
  context or unmatched watch-only notes already recorded in this repo
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
  [#564](https://github.com/pgplex/pgschema/issues/564) now remain
  **tracked** / **tracked** / **covered** / **not covered** respectively
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`

## Upstream watch list

- checked-in/live `pgschema` still sits at
  `24c6b689aa6571b2aaf94e8c5b915f0d9f58ecca`. The updated-since open-issue,
  closed-issue, and merged-PR queries for `>=2026-10-23` returned `[]`. The
  open-PR query surfaced [#645](https://github.com/pgplex/pgschema/pull/645)
  because of a 2026-10-23 comment; its commits are unchanged since 2026-10-16.
  Direct views keep the same open issue set. Open PR
  [#645](https://github.com/pgplex/pgschema/pull/645) remains the
  implementation thread for covered issue
  [#653](https://github.com/pgplex/pgschema/issues/653). Open PR
  [#662](https://github.com/pgplex/pgschema/pull/662) remains watch-only
  `MATCH FULL` context and did not move in today's updated-since sweep. Open
  PR [#660](https://github.com/pgplex/pgschema/pull/660) and open PR
  [#661](https://github.com/pgplex/pgschema/pull/661) remain covered /
  adjacent context already reflected in prior refreshes
- checked-in/live `pg-toolbelt` now sits at
  `6b82eff84dba925a176f0c6a78e5a16843885366`. The updated-since queries for
  `>=2026-10-23` surfaced no new open issues, no open PRs, and merged PR
  [#559](https://github.com/supabase/pg-toolbelt/pull/559). Direct views still
  show open issues [#332](https://github.com/supabase/pg-toolbelt/issues/332),
  [#518](https://github.com/supabase/pg-toolbelt/issues/518), and
  [#554](https://github.com/supabase/pg-toolbelt/issues/554), plus open PRs
  [#471](https://github.com/supabase/pg-toolbelt/pull/471),
  [#493](https://github.com/supabase/pg-toolbelt/pull/493),
  [#506](https://github.com/supabase/pg-toolbelt/pull/506),
  [#548](https://github.com/supabase/pg-toolbelt/pull/548),
  [#555](https://github.com/supabase/pg-toolbelt/pull/555), and
  [#558](https://github.com/supabase/pg-toolbelt/pull/558) at their 2026-10-22
  timestamps. PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471) and
  [#493](https://github.com/supabase/pg-toolbelt/pull/493) still have their
  latest commits from September
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
  - closed issue [#543](https://github.com/supabase/pg-toolbelt/issues/543)
    plus merged PR [#546](https://github.com/supabase/pg-toolbelt/pull/546)
    now solve benchmark **025** /
    pgschema [#534](https://github.com/pgplex/pgschema/issues/534) on the
    checked-in/live head, even though an exact `pgschema#534` text search still
    returns `[]`
  - issue [#518](https://github.com/supabase/pg-toolbelt/issues/518) remains
    open. Merged PR [#553](https://github.com/supabase/pg-toolbelt/pull/553)
    now covers the generated-column and same-schema-type slices on the
    checked-in/live head, and open issue
    [#554](https://github.com/supabase/pg-toolbelt/issues/554) tracks the
    zero-argument `IMMUTABLE` follow-up. Today's pgschema searches for
    `generated expression column order` and `zero-arg` returned `[]`. Open PR
    [#555](https://github.com/supabase/pg-toolbelt/pull/555) is unmatched
    rename/respell settlement and is not in the checked-in/live head
  - merged PR [#550](https://github.com/supabase/pg-toolbelt/pull/550) is now
    in the checked-in/live head as unmatched export-roundtrip fidelity work.
    Its remaining known gap is sub-partition index storage options, which
    Postgres rejects via `ALTER INDEX SET/RESET` on partitioned indexes
  - issues [#525](https://github.com/supabase/pg-toolbelt/issues/525) and
    [#544](https://github.com/supabase/pg-toolbelt/issues/544) remain
    unmatched upstream context
  - issue [#476](https://github.com/supabase/pg-toolbelt/issues/476) plus open
    PR [#548](https://github.com/supabase/pg-toolbelt/pull/548) and issue
    [#339](https://github.com/supabase/pg-toolbelt/issues/339) plus merged PR
    [#549](https://github.com/supabase/pg-toolbelt/pull/549) are adjacent role
    / user-mapping context around explicit global-state management; current
    pgschema keyword searches still only land on
    [#627](https://github.com/pgplex/pgschema/issues/627) and do not change the
    repo's benchmark scope
  - merged PR [#551](https://github.com/supabase/pg-toolbelt/pull/551) is now
    in the checked-in/live head and remains unmatched apply/search_path
    context
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
    / PR [#548](https://github.com/supabase/pg-toolbelt/pull/548), issue
    [#339](https://github.com/supabase/pg-toolbelt/issues/339) / PR
    [#549](https://github.com/supabase/pg-toolbelt/pull/549), merged PR
    [#551](https://github.com/supabase/pg-toolbelt/pull/551), and older open
    PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471) and
    [#493](https://github.com/supabase/pg-toolbelt/pull/493) alongside merged
    role / membership fixes
    [#117](https://github.com/supabase/pg-toolbelt/pull/117),
    [#118](https://github.com/supabase/pg-toolbelt/pull/118), and
    [#461](https://github.com/supabase/pg-toolbelt/pull/461)
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
