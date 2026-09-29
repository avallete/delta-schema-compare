# Benchmark - pgschema vs pg-delta parity status

This directory tracks parity between resolved pgschema issues and pg-delta.
Each benchmark file documents a scenario that was previously missing or
insufficient in pg-delta.

## Latest refresh snapshot (2026-09-29)

Refreshed against:

- checked-in/live `repos/pg-toolbelt` @ `e17c45925c3ddbf660dfb13c51029b605bcee448`
- checked-in/live `repos/pgschema` @ `580f4040d0f3c1bfad1497918200c9c1f638a020`

> The 2026-09-29 refresh advances checked-in/live `pg-delta` from
> `c00c4d0194a8aec34f3f6e85c1052fb5a62c0f5e` to
> `e17c45925c3ddbf660dfb13c51029b605bcee448` through merged PRs
> [#490](https://github.com/supabase/pg-toolbelt/pull/490),
> [#488](https://github.com/supabase/pg-toolbelt/pull/488),
> [#494](https://github.com/supabase/pg-toolbelt/pull/494),
> [#484](https://github.com/supabase/pg-toolbelt/pull/484),
> [#485](https://github.com/supabase/pg-toolbelt/pull/485),
> [#492](https://github.com/supabase/pg-toolbelt/pull/492), and
> [#499](https://github.com/supabase/pg-toolbelt/pull/499), while keeping
> checked-in/live `pgschema` at
> `580f4040d0f3c1bfad1497918200c9c1f638a020`, unchanged from the
> 2026-09-28 snapshot
>
> - `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-28'`
>   returned `[]`, and
>   `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-28'`
>   also returned `[]`
> - `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-28'`
>   returned closed issues
>   [#482](https://github.com/supabase/pg-toolbelt/issues/482),
>   [#483](https://github.com/supabase/pg-toolbelt/issues/483), and
>   [#487](https://github.com/supabase/pg-toolbelt/issues/487), while
>   `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-28'`
>   returned merged PRs
>   [#484](https://github.com/supabase/pg-toolbelt/pull/484),
>   [#485](https://github.com/supabase/pg-toolbelt/pull/485),
>   [#488](https://github.com/supabase/pg-toolbelt/pull/488),
>   [#490](https://github.com/supabase/pg-toolbelt/pull/490),
>   [#492](https://github.com/supabase/pg-toolbelt/pull/492),
>   [#494](https://github.com/supabase/pg-toolbelt/pull/494),
>   [#499](https://github.com/supabase/pg-toolbelt/pull/499), and open PRs
>   [#498](https://github.com/supabase/pg-toolbelt/pull/498),
>   [#500](https://github.com/supabase/pg-toolbelt/pull/500), and
>   [#501](https://github.com/supabase/pg-toolbelt/pull/501)
> - `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
>   returned `[]`
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
| 021 | [Partition child column overrides](021-partition-child-column-overrides.md) | [#499](https://github.com/pgplex/pgschema/issues/499) | [#332](https://github.com/supabase/pg-toolbelt/issues/332) (open umbrella / comment thread) | adjacent [#470](https://github.com/supabase/pg-toolbelt/pull/470), [#480](https://github.com/supabase/pg-toolbelt/pull/480), and [#488](https://github.com/supabase/pg-toolbelt/pull/488) (merged), [#501](https://github.com/supabase/pg-toolbelt/pull/501) (open partition-key retype) | **Tracked (umbrella thread only)** |
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
    keeps relation columns gated by `a.attislocal`, so child-local overrides
    on inherited partition columns do not become diff-visible facts
  - `repos/pg-toolbelt/packages/pg-delta/src/plan/rules/tables.ts` still
    emits bare `CREATE TABLE ... PARTITION OF ... ${bound}` with no typed
    child column-element list
  - merged PR [#470](https://github.com/supabase/pg-toolbelt/pull/470),
    merged PR [#480](https://github.com/supabase/pg-toolbelt/pull/480),
    merged PR [#488](https://github.com/supabase/pg-toolbelt/pull/488), and
    open PR [#501](https://github.com/supabase/pg-toolbelt/pull/501) remain
    adjacent only: #470 / #480 rebuild replace-path dependents and keep
    attached child indexes on a partition drop root, #488 is test-only corpus
    coverage for a different partitioned-parent mix, and #501 handles
    partition-key column retypes on the parent table rather than child-local
    `PARTITION OF` override extraction or rendering; umbrella issue
    [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains the
    only exact tracker context
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
  - the 2026-09-29 pg-delta delta lands in enum-retype casts, concurrent-drop
    retries, view/materialized-view column grants, and PG18 NOT NULL
    diagnostics; none of those changes preserves generated kind, so umbrella
    issue [#332](https://github.com/supabase/pg-toolbelt/issues/332) remains
    the only tracker context
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
  - merged PR [#485](https://github.com/supabase/pg-toolbelt/pull/485) now
    suppresses PG18 `contype = 'n'` diagnostic noise only, while merged PR
    [#484](https://github.com/supabase/pg-toolbelt/pull/484) fixes duplicate
    domain `NOT NULL` rendering on PostgreSQL 17+ only; neither changes
    table-column fact extraction or planning, and there is still no exact
    current pg-toolbelt issue or PR for this benchmark

Because checked-in/live `pg-delta` advanced to
`e17c45925c3ddbf660dfb13c51029b605bcee448` while checked-in/live `pgschema`
remained unchanged, source rechecks on the new pg-delta head still find
`a.attislocal` in `relations.ts`, generated-column kind still collapsed to
expression presence plus a hard-coded `... STORED` renderer, and PG18 table
`contype = 'n'` rows still kept out of diff-visible facts. Umbrella issue
[#332](https://github.com/supabase/pg-toolbelt/issues/332) therefore still
only covers benchmarks **021** / **022**, benchmark **024** still has no exact
current pg-toolbelt issue or PR, the focused 2026-08-14 runtime observations
for benchmarks **021** / **022** remain the latest direct runtime evidence,
and benchmark **024** remains source-level not covered on the new current
heads.

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
pg-toolbelt issue or PR, and the 2026-09-29 pg-toolbelt delta consists of
merged PRs [#484](https://github.com/supabase/pg-toolbelt/pull/484),
[#485](https://github.com/supabase/pg-toolbelt/pull/485),
[#488](https://github.com/supabase/pg-toolbelt/pull/488),
[#490](https://github.com/supabase/pg-toolbelt/pull/490),
[#492](https://github.com/supabase/pg-toolbelt/pull/492),
[#494](https://github.com/supabase/pg-toolbelt/pull/494), and
[#499](https://github.com/supabase/pg-toolbelt/pull/499) plus open PRs
[#498](https://github.com/supabase/pg-toolbelt/pull/498),
[#500](https://github.com/supabase/pg-toolbelt/pull/500), and
[#501](https://github.com/supabase/pg-toolbelt/pull/501), none of which
closes the active benchmark set. This repository still has no local tracker
issues.

## Recent closed-issue / tracker updates

No benchmark item changed status in this refresh. The most relevant current
tracker updates are:

- `gh issue list -R pgplex/pgschema --state all --search 'updated:>=2026-09-28'`
  returned `[]`
- `gh pr list -R pgplex/pgschema --state all --search 'updated:>=2026-09-28'`
  also returned `[]`
- `gh issue list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-28'`
  returned closed issues
  [#482](https://github.com/supabase/pg-toolbelt/issues/482),
  [#483](https://github.com/supabase/pg-toolbelt/issues/483), and
  [#487](https://github.com/supabase/pg-toolbelt/issues/487)
- `gh pr list -R supabase/pg-toolbelt --state all --search 'updated:>=2026-09-28'`
  returned merged PRs
  [#484](https://github.com/supabase/pg-toolbelt/pull/484),
  [#485](https://github.com/supabase/pg-toolbelt/pull/485),
  [#488](https://github.com/supabase/pg-toolbelt/pull/488),
  [#490](https://github.com/supabase/pg-toolbelt/pull/490),
  [#492](https://github.com/supabase/pg-toolbelt/pull/492),
  [#494](https://github.com/supabase/pg-toolbelt/pull/494),
  [#499](https://github.com/supabase/pg-toolbelt/pull/499), and open PRs
  [#498](https://github.com/supabase/pg-toolbelt/pull/498),
  [#500](https://github.com/supabase/pg-toolbelt/pull/500), and
  [#501](https://github.com/supabase/pg-toolbelt/pull/501)
- `gh issue list -R avallete/delta-schema-compare --state all --limit 200`
  still returned `[]`
- checked-in/live `pg-toolbelt` now advances to
  `e17c45925c3ddbf660dfb13c51029b605bcee448`
- merged PR [#490](https://github.com/supabase/pg-toolbelt/pull/490) closes
  issue [#487](https://github.com/supabase/pg-toolbelt/issues/487) and
  sharpens the already-solved enum-retype family around benchmark **005**
- merged PR [#494](https://github.com/supabase/pg-toolbelt/pull/494) closes a
  view/materialized-view column-grant gap outside the current benchmark set
- merged PRs [#484](https://github.com/supabase/pg-toolbelt/pull/484) and
  [#485](https://github.com/supabase/pg-toolbelt/pull/485) fix adjacent
  domain-only and diagnostics-only `NOT NULL` slices, but benchmark **024**
  remains not covered because table-column PG18 native
  `NOT NULL ... NOT VALID` state is still not diff-visible
- updated issue [#497](https://github.com/supabase/pg-toolbelt/issues/497)
  plus open PR [#501](https://github.com/supabase/pg-toolbelt/pull/501)
  remain adjacent partition-key retype context rather than exact duplicates of
  benchmarks **021**, **022**, or **024**
- previously screened pgschema verdicts remain unchanged because there was no
  new pgschema-side delta on 2026-09-29: open issue
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
- checked-in/live `pg-toolbelt` advances to
  `e17c45925c3ddbf660dfb13c51029b605bcee448` through merged PRs
  [#490](https://github.com/supabase/pg-toolbelt/pull/490),
  [#488](https://github.com/supabase/pg-toolbelt/pull/488),
  [#494](https://github.com/supabase/pg-toolbelt/pull/494),
  [#484](https://github.com/supabase/pg-toolbelt/pull/484),
  [#485](https://github.com/supabase/pg-toolbelt/pull/485),
  [#492](https://github.com/supabase/pg-toolbelt/pull/492), and
  [#499](https://github.com/supabase/pg-toolbelt/pull/499)
- the nearby pg-toolbelt issue/PR landscape changed, but not the parity
  mapping:
  - closed issues [#482](https://github.com/supabase/pg-toolbelt/issues/482),
    [#483](https://github.com/supabase/pg-toolbelt/issues/483), and
    [#487](https://github.com/supabase/pg-toolbelt/issues/487)
  - merged PRs [#484](https://github.com/supabase/pg-toolbelt/pull/484),
    [#485](https://github.com/supabase/pg-toolbelt/pull/485),
    [#488](https://github.com/supabase/pg-toolbelt/pull/488),
    [#490](https://github.com/supabase/pg-toolbelt/pull/490),
    [#492](https://github.com/supabase/pg-toolbelt/pull/492),
    [#494](https://github.com/supabase/pg-toolbelt/pull/494), and
    [#499](https://github.com/supabase/pg-toolbelt/pull/499)
  - open PRs [#498](https://github.com/supabase/pg-toolbelt/pull/498),
    [#500](https://github.com/supabase/pg-toolbelt/pull/500),
    [#501](https://github.com/supabase/pg-toolbelt/pull/501),
    [#496](https://github.com/supabase/pg-toolbelt/pull/496),
    [#495](https://github.com/supabase/pg-toolbelt/pull/495),
    [#493](https://github.com/supabase/pg-toolbelt/pull/493),
    [#478](https://github.com/supabase/pg-toolbelt/pull/478),
    [#473](https://github.com/supabase/pg-toolbelt/pull/473), and
    [#472](https://github.com/supabase/pg-toolbelt/pull/472)
  - only umbrella issue [#332](https://github.com/supabase/pg-toolbelt/issues/332)
    still points at benchmarks **021** / **022**, and benchmark **024**
    still has no exact current pg-toolbelt issue or PR
  - issue [#497](https://github.com/supabase/pg-toolbelt/issues/497) plus
    open PR [#501](https://github.com/supabase/pg-toolbelt/pull/501) remain
    adjacent partition-key retype context; merged PR
    [#494](https://github.com/supabase/pg-toolbelt/pull/494) is adjacent
    view-grant context; merged PRs
    [#484](https://github.com/supabase/pg-toolbelt/pull/484) and
    [#485](https://github.com/supabase/pg-toolbelt/pull/485) are adjacent
    domain/dangling-edge NOT NULL context; merged PR
    [#490](https://github.com/supabase/pg-toolbelt/pull/490) sharpens the
    already-solved enum-cast family around benchmark **005**; and historical
    PR [#174](https://github.com/supabase/pg-toolbelt/pull/174) remains
    legacy-engine-only context for benchmark **024**
- the target repo still has no local tracker issues

## Historical notes

- Detailed day-by-day refresh reports live in `docs/parity-refresh-*.md`.
- Draft-only uncovered scenarios remain recorded in
  `docs/parity-issue-drafts-*.md`.
- `benchmark/review-memory.json` is the cache / fingerprint source used by the
  automation scripts.
