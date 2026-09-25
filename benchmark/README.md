# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-09-25)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`
- checked-in/live `repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`

> The 2026-09-25 refresh keeps checked-in/live `pg-delta` at
> `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e` and keeps checked-in/live
> `pgschema` at `580f4040d0f3c1bfad1497918200c9c1f638a020`
>
> - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-24'`
>   returned `[]`, while
>   `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-24'`
>   surfaced open PR
>   [#622](https://github.com/pgplex/pgschema/pull/622) plus closed PR
>   [#605](https://github.com/pgplex/pgschema/pull/605)
> - open pgschema PR [#622](https://github.com/pgplex/pgschema/pull/622)
>   broadens upstream function-recreate dependent handling past the exact
>   dependent-view failure from issue
>   [#601](https://github.com/pgplex/pgschema/issues/601), but current
>   pg-delta already has generic replace-path dependent rebuild infrastructure,
>   so there is no benchmark status change from that follow-up alone
> - closed pgschema PR [#605](https://github.com/pgplex/pgschema/pull/605)
>   is the unrelated security-update bump and does not affect parity
> - there is no new merged `pg-toolbelt/main` code on top of the current
>   checked-in/live head
> - new open pg-toolbelt issue
>   [#489](https://github.com/supabase/pg-toolbelt/issues/489) reports missing
>   column grants on views in declarative schema output; broad privilege /
>   grant keyword searches on `pgplex/pgschema` did not find an exact matching
>   parity tracker, so this remains adjacent pg-toolbelt-side context rather
>   than a benchmark duplicate
> - new open pg-toolbelt PR
>   [#488](https://github.com/supabase/pg-toolbelt/pull/488) adds a test-only
>   partitioned-parent / `publish_via_partition_root = true` corpus scenario;
>   it does not change extraction or planning and is only adjacent context for
>   benchmark **021**
> - open pg-toolbelt issue
>   [#486](https://github.com/supabase/pg-toolbelt/issues/486) (shadow
>   non-superuser event-trigger loading) is adjacent tooling behavior rather
>   than pgschema parity work, while new open issue
>   [#487](https://github.com/supabase/pg-toolbelt/issues/487) is adjacent to
>   benchmark **005** but does not reopen the exact pgschema
>   [#190](https://github.com/pgplex/pgschema/issues/190) `text -> enum` +
>   default scenario
> - open issue [#482](https://github.com/supabase/pg-toolbelt/issues/482),
>   open issue [#483](https://github.com/supabase/pg-toolbelt/issues/483),
>   open PR [#484](https://github.com/supabase/pg-toolbelt/pull/484), and
>   open PR [#485](https://github.com/supabase/pg-toolbelt/pull/485) remain
>   adjacent context rather than duplicates of benchmarks **021**, **022**, or
>   **024**
> - open PR [#484](https://github.com/supabase/pg-toolbelt/pull/484) fixes
>   duplicate domain `NOT NULL` rendering on PostgreSQL 17+, while open PR
>   [#485](https://github.com/supabase/pg-toolbelt/pull/485) suppresses PG18
>   `dangling_edge` warnings for table `contype = 'n'` rows and explicitly
>   leaves the fact base, content hashes, and resulting plans unchanged
> - benchmark **024** therefore still has only historical duplicate-search
>   context via merged pg-toolbelt PR
>   [#174](https://github.com/supabase/pg-toolbelt/pull/174); PR **#485**
>   touches the same catalog family but is not an exact fix path
> - the open pg-toolbelt umbrella issue
>   [#332](https://github.com/supabase/pg-toolbelt/issues/332) still covers
>   only benchmarks **021** / **022**
> - the active benchmarked gap set therefore remains **021**, **022**, and
>   **024**
> - there is still **no open uncovered parity candidate** on the pgschema
>   side

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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | adjacent [#470](https://github.com/supabase/pg-toolbelt/pull/470) and [#480](https://github.com/supabase/pg-toolbelt/pull/480) (merged), [#488](https://github.com/supabase/pg-toolbelt/pull/488) (open test-only) | **Tracked (umbrella thread only)** |
| 022 | [VIRTUAL generated columns](022-virtual-generated-columns.md) | [#501](https://github.com/pgplex/pgschema/issues/501) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | none found | **Tracked (umbrella thread only)** |
| 023 | [FK before standalone unique index](023-fk-before-standalone-unique-index.md) | [#506](https://github.com/pgplex/pgschema/issues/506) | none found | adjacent [#361](https://github.com/supabase/pg-toolbelt/pull/361) (merged) | **Solved in pg-delta** |
| 024 | [PG18 native NOT NULL validation](024-pg18-not-null-validation.md) | [#564](https://github.com/pgplex/pgschema/issues/564) | none found | historical [#174](https://github.com/supabase/pg-toolbelt/pull/174) (merged, legacy engine only) | **Not covered** |

> Historical benchmark files are retained even after pg-delta fixes land.
> The status matrix above is the current source of truth for parity state.

## Active benchmarked gaps after refresh

Three resolved-issue benchmark scenarios remain active as unresolved behavior:

- **021** - child-specific `DEFAULT` / `NOT NULL` column overrides in
  `CREATE TABLE ... PARTITION OF ...`
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    keeps relation columns gated by `a.attislocal`, so child-local overrides
    on inherited partition columns do not become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits bare `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed
    child column-element list
  - merged PR [#470](https://github.com/supabase/pg-toolbelt/pull/470)
    (alpha.51) and merged PR
    [#480](https://github.com/supabase/pg-toolbelt/pull/480) remain adjacent
    only: they rebuild replace-path dependents and keep attached child indexes
    on a partition drop root, but still do not add child-local override
    extraction or rendering; umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
    only open tracker context
- **022** - PostgreSQL 18 `VIRTUAL` generated columns
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    collapses `attgenerated` to generated-expression presence instead of
    preserving `VIRTUAL` versus `STORED`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/helpers.ts` still
    hard-codes generated-column rendering as
    `GENERATED ALWAYS AS (...) STORED`
  - current pg-delta already covers resolved pgschema issue
    [#591](https://github.com/pgplex/pgschema/issues/591)'s
    generated-expression-change family, so the active gap remains only the
    generated kind distinction
- **024** - PostgreSQL 18 native `NOT NULL ... NOT VALID` state and pending
  validation visibility
  - `repos/pg-toolbelt/packages/pg-delta/src/extract/relations.ts` still
    models nullability through `a.attnotnull` and filters extracted table
    constraints to `con.contype IN ('p', 'u', 'f', 'c', 'x')`
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits a plain `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL`
  - there is still no exact pg-toolbelt issue or PR for this benchmark; open
    PR [#485](https://github.com/supabase/pg-toolbelt/pull/485) only filters
    PG18 `contype = 'n'` diagnostic noise and explicitly leaves the fact base
    and resulting plans unchanged

Because the checked-in/live `pg-delta` and `pgschema` heads are unchanged from
the 2026-09-24 refresh, the updated-since `gh` query for `pgplex/pgschema`
issues returned `[]`, the PR query surfaced only open follow-up PR
[#622](https://github.com/pgplex/pgschema/pull/622) plus closed unrelated
security PR [#605](https://github.com/pgplex/pgschema/pull/605), open issue
[#489](https://github.com/supabase/pg-toolbelt/issues/489) plus open PR
[#488](https://github.com/supabase/pg-toolbelt/pull/488) stay adjacent rather
than exact parity duplicates, the focused 2026-08-14 runtime observations for
benchmarks **021** / **022** remain the latest direct runtime evidence, and
benchmark **024** remains source-level not covered on the same current heads.

## Open pgschema issue screening (current state)

The current open pgschema watch list is now:
[#49](https://github.com/pgplex/pgschema/issues/49),
[#52](https://github.com/pgplex/pgschema/issues/52),
[#84](https://github.com/pgplex/pgschema/issues/84),
[#559](https://github.com/pgplex/pgschema/issues/559),
[#597](https://github.com/pgplex/pgschema/issues/597),
and [#598](https://github.com/pgplex/pgschema/issues/598).

Screened candidates:

- **#49** explicit rename / refactor workflow proposal - **not parity work for
  pg-delta**
- **#52** explicit before / after SQL file execution in plan output -
  **not parity work for pg-delta**
- **#84** feedback / testimonial collection thread - **not parity work for
  pg-delta**
- **#559** config-table data evolution / reference-data management -
  **not parity work for pg-delta**; merged pgschema PR
  [#612](https://github.com/pgplex/pgschema/pull/612) reverted that feature
  out of `main`, but row-data synchronization remains outside pg-delta's
  schema-diff scope
- **#597** broad multi-schema complexity / auto-ignore feedback - **not parity
  work for pg-delta**; it is general product feedback rather than a concrete
  pg-delta parity scenario
- **#598** interrupted `CREATE INDEX CONCURRENTLY` leaves an invalid index
  behind - **covered** in current pg-delta:
  - `src/extract/relations.ts` captures regular-index `indisvalid` as semantic
    `valid`
  - `src/plan/rules/indexes.ts` diffs `valid` with the `"replace"` strategy
  - `tests/index-invalid-repair.test.ts` covers the invalid-index repair path
  - open pgschema PR [#611](https://github.com/pgplex/pgschema/pull/611) is
    the upstream fix path on the pgschema side

There is currently **no open uncovered parity candidate** on the pgschema
side. The remaining active benchmarks **021** / **022** still only have
umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) as
exact tracker context; open PR
[#488](https://github.com/supabase/pg-toolbelt/pull/488) adds partitioned-
parent corpus coverage but not a fix. Benchmark **024** still has no exact
current pg-toolbelt issue or PR, open issue
[#489](https://github.com/supabase/pg-toolbelt/issues/489) is adjacent
view-column-grant context, open issue
[#482](https://github.com/supabase/pg-toolbelt/issues/482), open issue
[#483](https://github.com/supabase/pg-toolbelt/issues/483), open PR
[#484](https://github.com/supabase/pg-toolbelt/pull/484), and open PR
[#485](https://github.com/supabase/pg-toolbelt/pull/485) remain adjacent
domain-not-null / warning-surface work, merged PR
[#174](https://github.com/supabase/pg-toolbelt/pull/174) is only historical
pre-clean-room context for benchmark **024**, and issue
[#476](https://github.com/supabase/pg-toolbelt/issues/476), issue
[#477](https://github.com/supabase/pg-toolbelt/issues/477), PR
[#478](https://github.com/supabase/pg-toolbelt/pull/478), merged PR
[#480](https://github.com/supabase/pg-toolbelt/pull/480), and merged PR
[#481](https://github.com/supabase/pg-toolbelt/pull/481) remain adjacent
cluster-global role / identity-sequence privilege / partition-index / release
work rather than duplicates. This repository still has no local tracker
issues.

## Recent closed-issue / tracker updates

No benchmark item changed status in this refresh. The most relevant current
tracker updates are:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-24'`
  returned `[]`, while
  `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-24'`
  surfaced open follow-up PR
  [#622](https://github.com/pgplex/pgschema/pull/622) for covered issue
  [#601](https://github.com/pgplex/pgschema/issues/601) plus closed unrelated
  security PR [#605](https://github.com/pgplex/pgschema/pull/605)
- checked-in/live `pg-toolbelt` remains at
  `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`; there is no new merged
  `main`-branch code since the 2026-09-24 refresh
- open pg-toolbelt issue
  [#489](https://github.com/supabase/pg-toolbelt/issues/489) reports missing
  column grants on views in declarative schema output; privilege / grant
  keyword searches on `pgplex/pgschema` still do not surface an exact matching
  parity issue, so this is adjacent pg-toolbelt-side context rather than a
  duplicate benchmark candidate
- open pg-toolbelt PR
  [#488](https://github.com/supabase/pg-toolbelt/pull/488) adds a test-only
  corpus scenario around partitioned-parent replacement with `ON ONLY` parent
  indexes, cross-schema partitions, and `publish_via_partition_root = true`;
  it does not modify the active benchmark **021** extract / plan gap
- open pg-toolbelt issue
  [#486](https://github.com/supabase/pg-toolbelt/issues/486) reports a shadow
  non-superuser event-trigger load failure; this is adjacent platform/tooling
  behavior rather than a pgschema parity benchmark
- open pg-toolbelt issue
  [#487](https://github.com/supabase/pg-toolbelt/issues/487) reports that
  current `src/plan/rules/tables.ts` still emits a direct enum-to-enum cast
  for the differently named-type path; that is adjacent to benchmark **005**,
  but it does not duplicate the exact pgschema
  [#190](https://github.com/pgplex/pgschema/issues/190) `text -> enum` +
  default scenario that current pg-delta still covers
- open pg-toolbelt issue
  [#483](https://github.com/supabase/pg-toolbelt/issues/483) reports PG18
  `dangling_edge` warning noise on catalog `NOT NULL` rows
- open pg-toolbelt PR
  [#484](https://github.com/supabase/pg-toolbelt/pull/484) fixes duplicate
  domain `NOT NULL` rendering on PostgreSQL 17+
- open pg-toolbelt PR
  [#485](https://github.com/supabase/pg-toolbelt/pull/485), stacked on
  [#484](https://github.com/supabase/pg-toolbelt/pull/484), filters PG18
  table `contype = 'n'` dangling-edge warnings but explicitly leaves the fact
  base and plans unchanged, so it is adjacent rather than a benchmark **024**
  closure

- closed pgschema issue
  [#588](https://github.com/pgplex/pgschema/issues/588) is still **not parity
  work** for pg-delta; the related config-data request
  [#559](https://github.com/pgplex/pgschema/issues/559) is open again after
  merged revert PR [#612](https://github.com/pgplex/pgschema/pull/612)
- closed pgschema issue
  [#593](https://github.com/pgplex/pgschema/issues/593) remains **covered** in
  current pg-delta; merged PR
  [#613](https://github.com/pgplex/pgschema/pull/613) is the upstream fix
- closed pgschema issue
  [#594](https://github.com/pgplex/pgschema/issues/594) remains **not parity
  work** for pg-delta; merged PR
  [#614](https://github.com/pgplex/pgschema/pull/614) only hardens
  `.pgschemaignore` parsing by rejecting unknown keys
- closed pgschema issue
  [#596](https://github.com/pgplex/pgschema/issues/596) remains **not parity
  work** for pg-delta; merged PR
  [#615](https://github.com/pgplex/pgschema/pull/615) and merged follow-up PR
  [#616](https://github.com/pgplex/pgschema/pull/616) both land in
  pgschema's temp-schema / SQL-function body / batch-ordering path
- closed pgschema issue
  [#599](https://github.com/pgplex/pgschema/issues/599) remains **covered** in
  current pg-delta; merged PR
  [#617](https://github.com/pgplex/pgschema/pull/617) preserves trigger
  `ENABLE REPLICA` / `ENABLE ALWAYS` states upstream
- closed pgschema issue
  [#600](https://github.com/pgplex/pgschema/issues/600) remains **covered** in
  current pg-delta; merged PR
  [#618](https://github.com/pgplex/pgschema/pull/618) adds the same enum-label
  commit-boundary behavior pg-delta already models
- closed pgschema issue
  [#601](https://github.com/pgplex/pgschema/issues/601) remains **covered** in
  current pg-delta; merged PR
  [#619](https://github.com/pgplex/pgschema/pull/619) recreates dependent
  views around function replacement, which current pg-delta already covers,
  while open follow-up PR [#622](https://github.com/pgplex/pgschema/pull/622)
  broadens the upstream recreate-dependents flow to non-view dependents; the
  current pg-delta planner already has generic replacement expansion plus
  rebuildable default / constraint / index / policy / trigger / table kinds,
  so this stays watch-list context rather than a benchmark status change
- closed pgschema issue
  [#602](https://github.com/pgplex/pgschema/issues/602) remains **covered** in
  current pg-delta; merged PR
  [#620](https://github.com/pgplex/pgschema/pull/620) documents upstream
  ownership limits, while pg-delta already models owner edges and
  `ALTER ... OWNER TO`
- closed pgschema issue
  [#603](https://github.com/pgplex/pgschema/issues/603) remains **covered** in
  current pg-delta; merged PR
  [#621](https://github.com/pgplex/pgschema/pull/621) warns on unsupported
  no-effect statements, while pg-delta already preserves global
  `ALTER DEFAULT PRIVILEGES`
- closed pgschema issue
  [#606](https://github.com/pgplex/pgschema/issues/606) remains **covered** in
  current pg-delta; merged PR
  [#610](https://github.com/pgplex/pgschema/pull/610) preserves partitioned-
  table primary-key order upstream
- closed pgschema issue
  [#607](https://github.com/pgplex/pgschema/issues/607) remains **not parity
  work** for pg-delta; merged PR
  [#608](https://github.com/pgplex/pgschema/pull/608) fixes external-plan
  temp-schema resolution for extension-owned types, a pgschema-specific path
  current pg-delta does not use
- open pgschema PR
  [#611](https://github.com/pgplex/pgschema/pull/611) is the upstream fix path
  for covered issue [#598](https://github.com/pgplex/pgschema/issues/598)
- **#564** safer `NOT NULL` additions / PG18 native validation workflow remains
  **not covered** in current pg-delta as benchmark **024**
- there are still no local tracker issues in this repository

## Upstream watch list

- checked-in/live `pgschema` remains at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`; the updated-since issue query
  returned `[]`, the PR query surfaced open follow-up PR
  [#622](https://github.com/pgplex/pgschema/pull/622) for covered issue
  [#601](https://github.com/pgplex/pgschema/issues/601) plus closed unrelated
  security PR [#605](https://github.com/pgplex/pgschema/pull/605), and open
  PR [#611](https://github.com/pgplex/pgschema/pull/611) remains in flight
- checked-in/live `pg-toolbelt` remains at
  `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`; there is no new merged
  `main`-branch code since release PR
  [#481](https://github.com/supabase/pg-toolbelt/pull/481)
- the nearby pg-toolbelt issue/PR landscape is:
  - open issue [#489](https://github.com/supabase/pg-toolbelt/issues/489)
  - open PR [#488](https://github.com/supabase/pg-toolbelt/pull/488)
  - open issue [#487](https://github.com/supabase/pg-toolbelt/issues/487)
  - open issue [#486](https://github.com/supabase/pg-toolbelt/issues/486)
  - open PR [#485](https://github.com/supabase/pg-toolbelt/pull/485)
  - open PR [#484](https://github.com/supabase/pg-toolbelt/pull/484)
  - open issue [#483](https://github.com/supabase/pg-toolbelt/issues/483)
  - open issue [#482](https://github.com/supabase/pg-toolbelt/issues/482)
  - open issue [#476](https://github.com/supabase/pg-toolbelt/issues/476)
  - open issue [#477](https://github.com/supabase/pg-toolbelt/issues/477)
  - open PR [#478](https://github.com/supabase/pg-toolbelt/pull/478)
  - merged PR [#480](https://github.com/supabase/pg-toolbelt/pull/480)
  - merged PR [#481](https://github.com/supabase/pg-toolbelt/pull/481)
  - historical merged PR
    [#174](https://github.com/supabase/pg-toolbelt/pull/174)
  - older open PRs [#471](https://github.com/supabase/pg-toolbelt/pull/471),
    [#472](https://github.com/supabase/pg-toolbelt/pull/472), and
    [#473](https://github.com/supabase/pg-toolbelt/pull/473)
  - only umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still points at benchmarks **021** / **022**, and benchmark **024**
    still has no exact current pg-toolbelt issue or PR
  - issue **#489** is adjacent view-column-grant context with no exact current
    pgschema parity tracker, PR **#488** is adjacent partitioned-parent corpus
    coverage for benchmark **021**, issue **#487** is adjacent enum-cast
    context for benchmark **005**, issue **#486** is adjacent shadow-load /
    superuser tooling context, issues **#482** / **#483** and PRs **#484** /
    **#485** are adjacent domain-not-null / warning-surface context for
    benchmark **024**, and issue **#476**, issue **#477**, PR **#478**, PR
    **#480**, PR **#481**, and historical PR **#174** remain adjacent
    cluster-global role / identity-sequence privilege / partition-index /
    release / legacy-engine context rather than duplicates of the active
    benchmark set
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
