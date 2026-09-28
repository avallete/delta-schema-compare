# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-09-28)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`
- checked-in/live `repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`

> The 2026-09-28 refresh keeps checked-in/live `pg-delta` at
> `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e` and keeps checked-in/live
> `pgschema` at `580f4040d0f3c1bfad1497918200c9c1f638a020`, unchanged from the
> 2026-09-27 snapshot
>
> - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-27'`
>   returned `[]`, and
>   `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-27'`
>   also returned `[]`
> - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-27'`
>   returned only updated issue
>   [#497](https://github.com/supabase/pg-toolbelt/issues/497), and
>   `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-27'`
>   also returned `[]`
> - `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
>   returned `[]`
> - there is still no new merged `pg-toolbelt/main` code on top of the
>   current checked-in/live head
> - the nearby pg-toolbelt issue/PR landscape therefore stays unchanged in
>   substance from the 2026-09-27 snapshot: updated issue
>   [#497](https://github.com/supabase/pg-toolbelt/issues/497) remains
>   adjacent partition-key retype context only, including umbrella issue
>   [#332](https://github.com/supabase/pg-toolbelt/issues/332) for benchmarks
>   **021** / **022** and no exact current tracker for benchmark **024**
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
  - updated open issue [#497](https://github.com/supabase/pg-toolbelt/issues/497)
    still covers partition-key column retypes, not child-local `PARTITION OF`
    column override extraction or rendering
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
the 2026-09-27 refresh, the updated-since `gh` queries for `pgplex/pgschema`
returned `[]`, the `supabase/pg-toolbelt` updated-since issue query surfaced
only updated issue [#497](https://github.com/supabase/pg-toolbelt/issues/497),
and the remaining updated-since queries still returned `[]`; umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) still only covers
benchmarks **021** / **022**, benchmark **024** still has no exact current
pg-toolbelt issue or PR, the focused 2026-08-14 runtime observations for
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
exact tracker context, benchmark **024** still has no exact current
pg-toolbelt issue or PR, and the only pg-toolbelt-side delta since the
2026-09-27 refresh is updated issue
[#497](https://github.com/supabase/pg-toolbelt/issues/497), which still
remains adjacent partition-key retype context rather than a duplicate of the
active benchmark set. This repository still has no local tracker issues.

## Recent closed-issue / tracker updates

No benchmark item changed status in this refresh. The most relevant current
tracker updates are:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-27'`
  returned `[]`
- `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-27'`
  also returned `[]`
- `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-27'`
  returned updated issue [#497](https://github.com/supabase/pg-toolbelt/issues/497)
- `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-27'`
  also returned `[]`
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`
- checked-in/live `pg-toolbelt` remains at
  `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`; there is no new merged
  `main`-branch code since release PR
  [#481](https://github.com/supabase/pg-toolbelt/pull/481)
- updated issue [#497](https://github.com/supabase/pg-toolbelt/issues/497)
  still reports partition-key column retypes failing, which remains adjacent
  pg-toolbelt-side context rather than an exact duplicate of benchmarks
  **021**, **022**, or **024**
- previously screened pgschema verdicts remain unchanged because there was no
  new pgschema-side delta on 2026-09-28: open issue
  [#598](https://github.com/pgplex/pgschema/issues/598) remains **covered**,
  open issues [#49](https://github.com/pgplex/pgschema/issues/49),
  [#52](https://github.com/pgplex/pgschema/issues/52),
  [#84](https://github.com/pgplex/pgschema/issues/84),
  [#559](https://github.com/pgplex/pgschema/issues/559), and
  [#597](https://github.com/pgplex/pgschema/issues/597) remain **not parity**,
  closed issues [#599](https://github.com/pgplex/pgschema/issues/599),
  [#600](https://github.com/pgplex/pgschema/issues/600),
  [#601](https://github.com/pgplex/pgschema/issues/601),
  [#602](https://github.com/pgplex/pgschema/issues/602),
  [#603](https://github.com/pgplex/pgschema/issues/603), and
  [#606](https://github.com/pgplex/pgschema/issues/606) remain **covered**, and
  closed issues [#596](https://github.com/pgplex/pgschema/issues/596) and
  [#607](https://github.com/pgplex/pgschema/issues/607) remain
  **not parity work**
- **#564** safer `NOT NULL` additions / PG18 native validation workflow remains
  **not covered** in current pg-delta as benchmark **024**
- there are still no local tracker issues in this repository

## Upstream watch list

- checked-in/live `pgschema` remains at
  `580f4040d0f3c1bfad1497918200c9c1f638a020`; the updated-since issue query
  returned `[]`, the updated-since PR query also returned `[]`, and open PRs
  [#611](https://github.com/pgplex/pgschema/pull/611) and
  [#622](https://github.com/pgplex/pgschema/pull/622) remain in flight without
  new updates since 2026-09-24
- checked-in/live `pg-toolbelt` remains at
  `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e`; there is no new merged
  `main`-branch code since release PR
  [#481](https://github.com/supabase/pg-toolbelt/pull/481)
- the nearby pg-toolbelt issue/PR landscape is unchanged in substance from the
  2026-09-27 snapshot; the only updated item is open issue
  [#497](https://github.com/supabase/pg-toolbelt/issues/497):
  - open issue [#497](https://github.com/supabase/pg-toolbelt/issues/497)
  - open PR [#496](https://github.com/supabase/pg-toolbelt/pull/496)
  - open PR [#493](https://github.com/supabase/pg-toolbelt/pull/493)
  - open issue [#451](https://github.com/supabase/pg-toolbelt/issues/451)
  - open PR [#495](https://github.com/supabase/pg-toolbelt/pull/495)
  - open PR [#494](https://github.com/supabase/pg-toolbelt/pull/494)
  - open PR [#492](https://github.com/supabase/pg-toolbelt/pull/492)
  - open PR [#490](https://github.com/supabase/pg-toolbelt/pull/490)
  - open issue [#491](https://github.com/supabase/pg-toolbelt/issues/491)
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
  - issue **#497** remains adjacent partition-key retype context even after
    its 2026-09-27 update; issue **#451** is adjacent event-trigger/RLS
    context; issue **#491** plus PRs **#494** / **#496** are adjacent
    column-grant / view-grant context with no exact current pgschema parity
    tracker; PR **#490** is adjacent enum-cast context for benchmark **005**;
    issue **#489** is adjacent view-column-grant context; PR **#488** is
    adjacent partitioned-parent corpus coverage for benchmark **021**; issue
    **#487** is adjacent enum-cast context for benchmark **005**; issue
    **#486** is adjacent shadow-load / superuser tooling context; issues
    **#482** / **#483** and PRs **#484** / **#485** are adjacent
    domain-not-null / warning-surface context for benchmark **024**; PRs
    **#492**, **#493**, and **#495** are adjacent extraction /
    owner-capability / extension-export work without current pgschema parity
    trackers; and issue **#476**, issue **#477**, PR **#478**, PR **#480**,
    PR **#481**, and historical PR **#174** remain adjacent cluster-global
    role / identity-sequence privilege / partition-index / release /
    legacy-engine context rather than duplicates of the active benchmark set
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
